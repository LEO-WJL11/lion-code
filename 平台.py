# -*- coding: utf-8 -*-
r"""LionForge（狮铸）—— 项目 AI 开发平台。

【它是什么】在后端（main.py 的 HTTP 服务）上挂一个平台页 `/platform`：
用户填 项目名 / CPU 核数 / 内存 / 磁盘 / AI API / 开始提示词 → 平台用**现有 Agent 主循环**
（AgentLoop，与聊天、TUI 同一条链）在**专属工作区目录**里把项目构建出来；
构建完成后平台**自己把它跑起来做验证**（起进程 + HTTP 探活 + 取页面标题），通过才交付；
随后按产物形态自动部署：
  · 纯网页（web）        → 起服务并挂到 `/serve/<id>/`，用户直接访问
  · 纯客户端（client）   → 打 zip 挂到 `/dl/<id>/` 下载页
  · 前后端+客户端（三端）→ 网页照 web 部署，客户端照 client 出下载页
部署完用户仍可在平台页继续跟 AI 说话（同一条会话 ⇒ 同一份历史 ⇒ 改功能/修 bug）。

【资源从物理机分】创建项目时从物理机总量里划走 CPU 核数与内存：
  · 总量登记在 `<config>/platform/resources.json`（和为物理机上限，超额拒绝创建）
  · 运行时真正生效：CPU → SetProcessAffinityMask（亲和到前 N 核）
                   内存 → Windows Job Object 的 JobMemoryLimit（超限 OOM 杀进程）
  · 磁盘是配额登记：构建完核对实际占用，超了在日志与状态里如实标出
失败的限制不装死 —— 警告全部写进项目日志（honest over silent）。

【改动审核】Agent 写文件会进"待审改动"（ChangeReview）；平台构建是无人值守的，
所以构建/聊天期间由本模块的**放行线程**逐条 approve（产物由紧随其后的自测阶段验证）。
拿到闸门的方式：`工具.REVIEW_HOOK`（main 的 _wire_tool_hooks 挂上去的那一份）。

【诚实边界】
  · 自测 = "起得来 + HTTP 探活 + 页面标题"级别；应用层业务正确性由 Agent 自己写的
    自测脚本负责（提示词里明确要求它真跑真验）
  · 资源限制对**被启动的服务进程**生效；Agent 进程（后端自己）不在配额内
  · 下载页的 zip 是部署时打一次；项目更新后需要重新部署（POST /redeploy）
"""
from __future__ import annotations

import ctypes
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any, Callable

PLATFORM_NAME = "LionForge"
PLATFORM_TAG = "狮铸 · 项目 AI 开发平台"
LOCK = threading.RLock()
#: 项目状态机：created → building → testing → deploying → live / failed / stopped
ST_CREATED, ST_BUILDING, ST_TESTING, ST_DEPLOYING, ST_LIVE, ST_FAILED, ST_STOPPED = (
    "created", "building", "testing", "deploying", "live", "failed", "stopped")
#: 网页服务探测上限（秒）—— 起得慢的应用给足时间，但不能无限等
PROBE_TIMEOUT = 40
CREATE_NO_WINDOW = 0x08000000


# ============================================================ 物理机资源
def physical_specs() -> dict[str, Any]:
    """物理机规格：核数 / 内存 MB / 磁盘可用 GB / 系统版本。"""
    cores = os.cpu_count() or 4
    ram_mb = 8192
    try:
        class _MSX(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_uint32), ("dwMemoryLoad", ctypes.c_uint32),
                        ("ullTotalPhys", ctypes.c_uint64), ("ullAvailPhys", ctypes.c_uint64),
                        ("ullTotalPageFile", ctypes.c_uint64), ("ullAvailPageFile", ctypes.c_uint64),
                        ("ullTotalVirtual", ctypes.c_uint64), ("ullAvailVirtual", ctypes.c_uint64),
                        ("ullAvailExtendedVirtual", ctypes.c_uint64)]
        m = _MSX()
        m.dwLength = ctypes.sizeof(_MSX)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(m)):
            ram_mb = int(m.ullTotalPhys // (1024 * 1024))
    except Exception:                                       # noqa: BLE001 非 Windows/失败 → 兜底
        pass
    disk_gb = 0
    try:
        root = os.path.splitdrive(os.getcwd())[0] or "C:"
        free = shutil.disk_usage(root)
        disk_gb = int(free.total // (1024 ** 3))
    except Exception:                                       # noqa: BLE001
        pass
    os_name = ""
    try:
        os_name = " ".join(x for x in sys.getwindowsversion()[:3] if x) and \
            f"Windows {sys.getwindowsversion().major}.{sys.getwindowsversion().minor} (build {sys.getwindowsversion().build})"
    except Exception:                                       # noqa: BLE001
        os_name = sys.platform
    return {"cores": cores, "ramMb": ram_mb, "diskGb": disk_gb, "os": os_name}


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


# ============================================================ 资源池
class ResourcePool:
    """项目运行时的资源登记与进程级强制。"""

    def __init__(self, state_path: Path) -> None:
        self.path = state_path
        self._alloc: dict[str, dict[str, Any]] = {}
        try:
            self._alloc = json.loads(state_path.read_text(encoding="utf-8"))
        except Exception:                                   # noqa: BLE001 没有/坏 → 空池
            pass

    def _save(self) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            tmp = self.path.with_suffix(".tmp")
            tmp.write_text(json.dumps(self._alloc, ensure_ascii=False, indent=1), encoding="utf-8")
            os.replace(tmp, self.path)
        except OSError as e:
            print(f"[平台] 资源池落盘失败: {e}", flush=True)

    def used(self) -> dict[str, int]:
        cpu = sum(int(v.get("cpu", 0)) for v in self._alloc.values())
        mem = sum(int(v.get("memMb", 0)) for v in self._alloc.values())
        disk = sum(int(v.get("diskGb", 0)) for v in self._alloc.values())
        return {"cpu": cpu, "memMb": mem, "diskGb": disk, "count": len(self._alloc)}

    def allocate(self, pid: str, cpu: int, mem_mb: int, disk_gb: int) -> str | None:
        """登记配额；超物理机总量返回原因（None = 成功）。"""
        specs = physical_specs()
        used = self.used()
        if used["cpu"] + cpu > specs["cores"]:
            return f"CPU 配额不足：物理机 {specs['cores']} 核，已分配 {used['cpu']}，本次要 {cpu}"
        if used["memMb"] + mem_mb > specs["ramMb"]:
            return f"内存配额不足：物理机 {specs['ramMb']} MB，已分配 {used['memMb']}，本次要 {mem_mb}"
        with LOCK:
            self._alloc[pid] = {"cpu": cpu, "memMb": mem_mb, "diskGb": disk_gb, "at": _now()}
            self._save()
        return None

    def release(self, pid: str) -> bool:
        """释放配额；返回这次是否真的释放了（幂等：没登记过返回 False）。"""
        with LOCK:
            if self._alloc.pop(pid, None) is not None:
                self._save()
                return True
        return False


def apply_process_limits(pid: int, cpu_cores: int, mem_mb: int) -> list[str]:
    """把 CPU/内存限制落到进程上；每条失败都变成警告（不吞）。"""
    warns: list[str] = []
    k32 = ctypes.windll.kernel32 if hasattr(ctypes, "windll") else None
    if k32 is None:
        return ["非 Windows：CPU/内存限制未生效"]
    # CPU 亲和：掩码前 N 位
    try:
        PROCESS_SET_INFORMATION = 0x0200
        h = k32.OpenProcess(PROCESS_SET_INFORMATION, False, pid)
        if not h:
            warns.append(f"OpenProcess(CPU) 失败 errno={ctypes.get_last_error()}")
        else:
            mask = (1 << max(1, min(cpu_cores, 64))) - 1
            ok = k32.SetProcessAffinityMask(h, ctypes.c_size_t(mask))
            k32.CloseHandle(h)
            if not ok:
                warns.append("SetProcessAffinityMask 失败")
    except Exception as e:                                   # noqa: BLE001
        warns.append(f"CPU 亲和设置异常: {e}")
    # 内存：Job Object 的 JobMemoryLimit（超限由系统 OOM 杀，而不是拖垮物理机）
    try:
        JOB_OBJECT_LIMIT_JOB_MEMORY = 0x200
        JobObjectExtendedLimitInformation = 9
        PROCESS_SET_QUOTA = 0x0100
        PROCESS_TERMINATE = 0x0001

        class _BASIC(ctypes.Structure):
            _fields_ = [("PerProcessUserTimeLimit", ctypes.c_int64),
                        ("PerJobUserTimeLimit", ctypes.c_int64),
                        ("LimitFlags", ctypes.c_uint32),
                        ("MinimumWorkingSetSize", ctypes.c_size_t),
                        ("MaximumWorkingSetSize", ctypes.c_size_t),
                        ("ActiveProcessLimit", ctypes.c_uint32),
                        ("Affinity", ctypes.c_size_t),
                        ("PriorityClass", ctypes.c_uint32),
                        ("SchedulingClass", ctypes.c_uint32)]

        class _IO(ctypes.Structure):
            _fields_ = [(n, ctypes.c_uint64) for n in
                        ("ReadOperationCount", "WriteOperationCount", "OtherOperationCount",
                         "ReadTransferCount", "WriteTransferCount", "OtherTransferCount")]

        class _EXT(ctypes.Structure):
            _fields_ = [("BasicLimitInformation", _BASIC), ("IoInfo", _IO),
                        ("ProcessMemoryLimit", ctypes.c_size_t), ("JobMemoryLimit", ctypes.c_size_t),
                        ("PeakProcessMemoryUsed", ctypes.c_size_t), ("PeakJobMemoryUsed", ctypes.c_size_t)]

        job = k32.CreateJobObjectW(None, None)
        if not job:
            warns.append("CreateJobObject 失败")
            return warns
        info = _EXT()
        info.BasicLimitInformation.LimitFlags = JOB_OBJECT_LIMIT_JOB_MEMORY
        info.JobMemoryLimit = int(mem_mb) * 1024 * 1024
        if not k32.SetInformationJobObject(job, JobObjectExtendedLimitInformation,
                                           ctypes.byref(info), ctypes.sizeof(info)):
            warns.append("SetInformationJobObject 失败")
            return warns
        ph = k32.OpenProcess(PROCESS_SET_QUOTA | PROCESS_TERMINATE, False, pid)
        if not ph:
            warns.append(f"OpenProcess(内存配额) 失败 errno={ctypes.get_last_error()}")
            return warns
        ok = k32.AssignProcessToJobObject(job, ph)
        k32.CloseHandle(ph)
        if not ok:
            warns.append("AssignProcessToJobObject 失败")
    except Exception as e:                                   # noqa: BLE001
        warns.append(f"内存限制设置异常: {e}")
    return warns


# ============================================================ 存储
def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, path)


class ProjectStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self._items: list[dict[str, Any]] = []
        try:
            self._items = json.loads(path.read_text(encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            pass

    def save(self) -> None:
        with LOCK:
            _atomic_json(self.path, self._items)

    def all(self) -> list[dict[str, Any]]:
        with LOCK:
            return [dict(p) for p in self._items]

    def get(self, pid: str) -> dict[str, Any] | None:
        with LOCK:
            for p in self._items:
                if p["id"] == pid:
                    return dict(p)
        return None

    def update(self, pid: str, **fields: Any) -> None:
        with LOCK:
            for p in self._items:
                if p["id"] == pid:
                    p.update(fields)
                    break
        self.save()

    def add(self, item: dict[str, Any]) -> None:
        with LOCK:
            self._items.append(item)
        self.save()


# ============================================================ 主体
class PlatformApi:
    """/platform 页面 + /api/platform/* 接口 + /serve /dl 部署出口。"""

    def __init__(self, ctx: Any, Response: Any) -> None:
        self.ctx = ctx
        self.Response = Response
        base = Path(getattr(getattr(ctx, "cfg", None), "base", None) or (Path.home() / ".lioncode"))
        self.dir = base / "platform"
        self.projects_dir = self.dir / "projects"
        self.projects_dir.mkdir(parents=True, exist_ok=True)
        self.pool = ResourcePool(self.dir / "resources.json")
        self.store = ProjectStore(self.dir / "projects.json")
        #: 运行中的部署进程 {pid: Popen}（平台活着才在；重启后进程丢失 → 详情标 degraded）
        self._procs: dict[str, subprocess.Popen[str]] = {}
        self._stop_flags: dict[str, threading.Event] = {}
        self._busy: set[str] = set()
        # 端口分配从 19000 起顺延，避开后端/适配器常用端口
        self._next_port = 19000
        self._reconcile()

    def _reconcile(self) -> None:
        """启动时自愈：上个进程留下的 building/testing/deploying 状态 = 已中断。
        后端一重启，那些状态就没有线程在推进（实测踩过：卡在 building 15 分钟
        但其实是旧进程的僵尸状态 ✗✗✗）—— 立刻标失败并给出可执行的下一步。"""
        for p in self.store.all():
            if p.get("status") in (ST_BUILDING, ST_TESTING, ST_DEPLOYING):
                self.store.update(p["id"], status=ST_FAILED,
                                  error="构建被后端重启中断（上个进程没跑完）——"
                                        "在下方对话框里说「继续」让 AI 从中断处接着做")
            elif p.get("status") == ST_LIVE and str(p.get("kind") or "") in ("", "unknown"):
                # 另一类僵尸：修复前的版本会把 unknown 标成 live（实测发生过 ✗✗✗）。
                self.store.update(p["id"], status=ST_FAILED,
                                  error="该记录来自旧版本的误判（没有产物却标了已上线）——重新构建或让 AI 重做")
        # 【僵尸配额清理】失败/中断的项目不该继续占资源池（实测：历史失败项目留下
        # 7 条 14 核/14GB 的死配额 ✗✗✗，池按物理机总量算，攒几次就建不了新项目）。
        # 规则：只有 live 项目保留配额；其余（failed/stopped/不存在）一律回收。
        live_ids = {p["id"] for p in self.store.all() if p.get("status") == ST_LIVE}
        for held in list(self.pool._alloc):
            if held not in live_ids:
                if self.pool.release(held):
                    print(f"[平台] 回收无主配额: {held}（项目非 live）", flush=True)

    # ---------------------------------------------------- 依赖定位
    def _deps(self) -> Any:
        from lionbox.api import deps                     # noqa: PLC0415 main 装配后才可用
        return deps

    def _agent(self) -> Any:
        return self._deps().agent_loop(self.ctx)

    def _review_hook(self) -> Any:
        try:
            import 工具                                    # noqa: PLC0415 闸门挂在工具模块上
            return getattr(工具, "REVIEW_HOOK", None)
        except Exception:                                   # noqa: BLE001
            return None

    # ---------------------------------------------------- 日志
    def log(self, pid: str, line: str) -> None:
        text = f"[{_now()}] {line}"
        print(f"[平台/{pid[:8]}] {line}", flush=True)
        try:
            p = self.projects_dir / pid / ".lionforge.log"
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "a", encoding="utf-8") as f:
                f.write(text + "\n")
        except OSError:
            pass

    def read_log(self, pid: str, tail: int = 400) -> str:
        p = self.projects_dir / pid / ".lionforge.log"
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
            return "\n".join(lines[-tail:])
        except OSError:
            return ""

    # ---------------------------------------------------- Agent 执行（带自动放行）
    def _current_model(self) -> str | None:
        """当前该用的模型名 —— 与 ChatApi.saved_model 同语义：
        活适配器实例上的 model → 配置块(openai)的 model → 顶层 model → None。
        【为什么必须解析】process_message(model=None) 会让请求里 model 为 null，
        云端直接回 400 "Unsupported model"（首次实测就踩了这条 ✗✗✗）。
        """
        try:
            adapter = self.ctx.adapters().get_active_adapter()
            if adapter is not None:
                m = getattr(adapter, "model", None)
                if isinstance(m, str) and m.strip():
                    return m
                blk = self.ctx.cfg.get("openai")
                if isinstance(blk, dict) and str(blk.get("model") or "").strip():
                    return str(blk["model"])
            m = self.ctx.cfg.get("model")
            if isinstance(m, str) and m.strip():
                return m
        except Exception:                                   # noqa: BLE001 解析失败 → None
            pass
        return None

    def _agent_run(self, pid: str, session_id: str, message: str, thinking: str = "HIGH") -> str:
        """跑一轮 Agent；期间放行线程逐条 approve 待审改动。返回回复文本。"""
        stop = threading.Event()

        def approver() -> None:
            hook = self._review_hook()
            if hook is None:
                return
            while not stop.is_set():
                try:
                    for c in list(hook.list(session_id)):
                        cid = getattr(c, "id", None)
                        if cid:
                            hook.approve(cid)
                            self.log(pid, f"审核放行: {cid} {getattr(c, 'path', '')}")
                except Exception as e:                       # noqa: BLE001 放行线程不能影响主线程
                    self.log(pid, f"审核放行线程异常（忽略）: {type(e).__name__}: {e}")
                stop.wait(1.5)

        t = threading.Thread(target=approver, daemon=True, name=f"lionforge-approve-{pid[:8]}")
        t.start()
        try:
            reply = self._agent().process_message(session_id, message, "STANDARD",
                                                  thinking, self._current_model())
            return str(reply or "")
        finally:
            stop.set()
            t.join(timeout=5)
            # 【竞态终扫】模型**最后一轮**提交的待审改动，1.5s 轮询可能赶不上
            # （实测：C8562-1 卡在待审、AI 自己说"尚未落盘" ✗✗✗）。退出前同步扫几遍。
            for _ in range(6):
                try:
                    hook = self._review_hook()
                    pending = [c for c in (hook.list(session_id) if hook else [])
                               if getattr(c, "id", None)]
                except Exception:                           # noqa: BLE001
                    break
                if not pending:
                    break
                for c in pending:
                    try:
                        hook.approve(c.id)
                        self.log(pid, f"审核放行(终扫): {c.id} {getattr(c, 'path', '')}")
                    except Exception as e:                   # noqa: BLE001
                        self.log(pid, f"审核放行失败: {type(e).__name__}: {e}")
                time.sleep(0.4)

    # ---------------------------------------------------- 构建 → 自测 → 部署
    def _build_pipeline(self, pid: str) -> None:
        try:
            p = self.store.get(pid)
            if p is None:
                return
            src = self.projects_dir / pid
            session_id = p["sessionId"]
            self.log(pid, "构建开始（Agent 接管；写文件会自动放行，产物由自测阶段把关）")
            self.store.update(pid, status=ST_BUILDING)
            prompt = self._build_prompt(p)
            t0 = time.time()
            # 心跳：Agent 那轮可能是几分钟的云端长响应，平台日志必须能看出"还活着"
            # （实测首版没有任何心跳，构建期查状态只能干等 ✗✗✗）
            beat_stop = threading.Event()

            def heartbeat() -> None:
                while not beat_stop.wait(30):
                    self.log(pid, f"构建中… 已 {int(time.time() - t0)} 秒（Agent 正在跑）")

            threading.Thread(target=heartbeat, daemon=True,
                             name=f"lionforge-beat-{pid[:8]}").start()
            try:
                reply = self._agent_run(pid, session_id, prompt)
            finally:
                beat_stop.set()
            self.log(pid, f"Agent 完成，耗时 {int(time.time() - t0)} 秒")
            # 【停止权优先】用户在构建期间点了停止 ⇒ 不进自测/部署（状态保持已停止）
            if not self._still_running(pid):
                self.log(pid, "构建期间被用户停止（跳过自测与部署）")
                return
            self.store.update(pid, status=ST_TESTING, buildReply=reply[:4000])
            self._test_and_deploy(pid, src)
        except Exception as e:                               # noqa: BLE001 平台不许静默失败
            self.log(pid, f"❌ 管线异常: {type(e).__name__}: {e}")
            self._release_quota(pid, "管线异常")
            if self._still_running(pid):
                self.store.update(pid, status=ST_FAILED, error=f"{type(e).__name__}: {e}")
        finally:
            with LOCK:
                self._busy.discard(pid)

    def _build_prompt(self, p: dict[str, Any]) -> str:
        src = self.projects_dir / p["id"]
        return (
            "你是 LionForge 平台的构建 Agent，在**当前工作区目录**（就是本项目目录）里交付一个完整可运行的项目。\n"
            f"【项目名】{p['name']}\n"
            f"【项目绝对路径】{src} —— 所有文件的创建/修改/读取一律用这个绝对路径开头，"
            "不要写到任何别的目录（比如仓库根）。\n"
            f"【资源配额】CPU {p['cpu']} 核 / 内存 {p['memoryMb']} MB / 磁盘 {p['diskGb']} GB —— "
            "程序本身要尊重这些限制（别引入超大依赖/权重；服务默认监听 {PORT} 环境变量指定的端口）。\n"
            f"【用户需求】{p['prompt']}\n"
            "【交付要求（必须全部做到）】\n"
            "1. 在本目录里创建完整源码；入口清晰（网页应用给 server 或纯静态入口）。\n"
            "2. 写 README.md：怎么启动、目录结构、技术选型。\n"
            "3. **必须真自测**：真的把它启动起来/跑起来，用命令验证关键路径"
            "（服务类用 HTTP 请求验证状态码与页面标题；脚本类直接运行断言输出），"
            "把「执行的命令 + 真实输出」写进最后的结论。\n"
            "4. 自测不通过就继续修，修到通过为止；若确实修不通，结论里如实写「未通过 + 原因」。\n"
            "5. 若产物是网页应用，额外把**离线静态副本**放到 dist/client/ 下并打成 zip"
            "（Windows PowerShell 可用 Compress-Archive）——这是给用户的下载包。\n"
            "6. 最后用一段话总结：做了什么、自测结果（含关键命令输出）、怎么运行。\n"
            "先想清楚再动手；过程中不需要反问我，自己推进。"
        )

    # ---------------------------------------------------- 自测 + 部署
    def _classify(self, src: Path) -> str:
        pj = src / "package.json"
        has_web = (src / "public" / "index.html").is_file() or (src / "index.html").is_file()
        script_start = False
        try:
            script_start = bool(json.loads(pj.read_text(encoding="utf-8")).get("scripts", {}).get("start"))
        except Exception:                                   # noqa: BLE001
            pass
        has_web = has_web or script_start or (src / "server.js").is_file() or (src / "app.js").is_file()
        has_client = False
        for d in ("dist", "build", "out", "release"):
            dd = src / d
            if dd.is_dir() and any(dd.rglob("*.exe")):
                has_client = True
        if list(src.glob("*.exe")) or list(src.glob("*.msi")):
            has_client = True
        if has_web and has_client:
            return "three-tier"
        if has_web:
            return "web"
        if has_client:
            return "client"
        return "unknown"

    def _pick_port(self) -> int:
        """挑一个**当前空闲**的端口。
        【为什么不能单调 +1 就返回】原实现从不 bind 验证 ⇒ 19000+ 里被别的服务/
        别的项目占着的端口照样会被发出去 ⇒ 新进程绑不上、探活探到**别人的服务**
        当成自己部署成功的证据 ✗✗✗（连挑 50 次都不空 → 返回 0，调用方按静态站处理）。"""
        for _ in range(50):
            port = self._next_port
            self._next_port += 1
            if self._next_port > 19999:
                self._next_port = 19000
            if self._port_free(port):
                return port
        return 0

    def _start_server(self, pid: str, src: Path, port: int) -> subprocess.Popen[str] | None:
        """起网页服务（优先 bun，其次 node/npm）；起不来返回 None（当静态站处理）。"""
        env = dict(os.environ)
        env["PORT"] = str(port)
        env["HOST"] = "127.0.0.1"
        cmd: list[str] | None = None
        try:
            pj = json.loads((src / "package.json").read_text(encoding="utf-8"))
        except Exception:                                   # noqa: BLE001
            pj = {}
        bun = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bun.exe")
        if not os.path.isfile(bun):
            bun = shutil.which("bun") or ""
        node = shutil.which("node") or ""
        entry = next((e for e in ("server.js", "app.js", "index.js") if (src / e).is_file()), None)
        if pj.get("scripts", {}).get("start"):
            if bun:
                cmd = [bun, "run", "start"]
            elif node:
                cmd = [node, "server.js"] if (src / "server.js").is_file() else None
        elif entry:
            runner = bun or node
            if runner:
                cmd = [runner, entry]
        if cmd is None:
            self.log(pid, "未找到可启动的服务入口 → 按静态站部署")
            return None
        logf = open(self.projects_dir / pid / ".server.log", "a", encoding="utf-8")
        proc = subprocess.Popen(cmd, cwd=str(src), env=env, stdout=logf, stderr=logf,
                                creationflags=CREATE_NO_WINDOW)
        # 【限制必须传项目配额】第一版写死 apply_process_limits(pid, 0, 0) ✗✗✗：
        # cpu=0 被夹成 1 核、mem=0 变成"0 字节上限"，配额完全没生效（实测亲和 0x1≠0x3）。
        p = self.store.get(pid) or {}
        warns = apply_process_limits(proc.pid, int(p.get("cpu", 1)), int(p.get("memoryMb", 1024)))
        self.log(pid, f"服务已启动: {' '.join(cmd)} pid={proc.pid} port={port}"
                      + (f"  ⚠ 限制未生效: {'; '.join(warns)}" if warns else "  ✓ 资源限制已生效"))
        return proc

    def _probe(self, port: int) -> tuple[bool, int, str]:
        """探测 http://127.0.0.1:port/；返回 (通?, 状态码, 页面标题)。"""
        deadline = time.time() + PROBE_TIMEOUT
        last = ""
        while time.time() < deadline:
            try:
                req = urllib.request.Request(f"http://127.0.0.1:{port}/")
                with urllib.request.urlopen(req, timeout=3) as r:
                    body = r.read(200000).decode("utf-8", "replace")
                    title = re.search(r"<title[^>]*>(.*?)</title>", body, re.S | re.I)
                    return True, int(r.status), (title.group(1).strip()[:80] if title else "")
            except urllib.error.HTTPError as e:              # HTTP 错误也算"服务活着"
                return True, int(e.code), ""
            except Exception as e:                           # noqa: BLE001 连接拒绝 → 继续等
                last = f"{type(e).__name__}"
                time.sleep(1.0)
        return False, 0, last

    def _zip_client(self, pid: str, src: Path) -> list[str]:
        """把客户端产物/离线副本打成 zip；返回产物文件名列表。"""
        out_dir = self.projects_dir / pid / ".lionforge"
        out_dir.mkdir(parents=True, exist_ok=True)
        made: list[str] = []
        for d in ("dist/client", "dist", "build", "out", "release"):
            dd = src / d
            if not dd.is_dir():
                continue
            if d == "dist/client":
                zp = out_dir / f"{pid}-client.zip"
                with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
                    for f in dd.rglob("*"):
                        if f.is_file():
                            z.write(f, f.relative_to(dd).as_posix())
                made.append(zp.name)
            # 打包目录里的安装器/可执行（客户端产物常见的落点）
            for f in list(dd.rglob("*.exe")) + list(dd.rglob("*.msi")):
                dst = out_dir / f.name
                if not dst.exists():
                    shutil.copy2(f, dst)
                made.append(dst.name)
        for f in list(src.glob("*.exe")) + list(src.glob("*.msi")):
            dst = out_dir / f.name
            shutil.copy2(f, dst)
            made.append(dst.name)
        # 无论有没有客户端产物，都给一份源码 zip（下载页总要有东西可下）
        zp = out_dir / f"{pid}-source.zip"
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in src.rglob("*"):
                if f.is_file() and ".lionforge" not in f.parts and "node_modules" not in f.parts:
                    z.write(f, f.relative_to(src).as_posix())
        made.append(zp.name)
        return made

    def _stop_proc(self, pid: str) -> None:
        """停掉本项目已登记的服务进程（stop / redeploy / 探活失败前都要先走它）。
        【为什么抽出来】redeploy 原来直接 _start_server ⇒ 旧进程不被杀、一直占着端口，
        新进程绑不上端口死掉、`_procs` 被覆盖成死进程 ⇒ 之后 stop 杀的是死进程、
        老进程变永久孤儿（实测推演 ✗✗✗）。统一走这里就不会漏杀。"""
        proc = self._procs.pop(pid, None)
        if proc is None:
            return
        try:
            proc.terminate()
            proc.wait(timeout=6)
        except Exception:                                   # noqa: BLE001
            try:
                proc.kill()
            except Exception:                               # noqa: BLE001
                pass

    @staticmethod
    def _port_free(port: int) -> bool:
        """端口当前是否空闲（bind 一次即测，随后释放）。"""
        try:
            with socket.socket() as s:
                s.bind(("127.0.0.1", int(port)))
            return True
        except OSError:
            return False

    def _test_and_deploy(self, pid: str, src: Path) -> None:
        p = self.store.get(pid)
        if p is None:
            return
        # 【停止权优先】构建/自测期间用户点了"停止" ⇒ 后续状态一律不写（否则
        # stop 会被构建线程改回 testing/live 并把服务真的拉起来 ✗✗✗）。
        if p.get("status") == ST_STOPPED:
            self.log(pid, "项目已被停止，跳过部署")
            return
        kind = self._classify(src)
        self.log(pid, f"自测开始：产物形态 = {kind}")
        self.store.update(pid, status=ST_TESTING, kind=kind)
        web_url = None
        test = {"kind": kind, "ok": False, "http": None, "title": None, "note": ""}
        if kind in ("web", "three-tier"):
            # 重部署复用旧端口，但**必须先确认它空闲** —— 单调 +1 或旧进程没死时
            # 挑到被占端口 ⇒ 新进程绑不上、探活探到**别人的服务**当自己的 ✗✗✗。
            port = int(p.get("port") or 0)
            if not port or not self._port_free(port):
                port = self._pick_port()
            proc = self._start_server(pid, src, port) if port else None
            if proc is not None:
                self._procs[pid] = proc
                ok, code, title = self._probe(port)
                test.update(ok=ok, http=code, title=title)
                self.log(pid, f"自测探活: ok={ok} http={code} title={title!r}")
                if ok:
                    web_url = f"/serve/{pid}/"
                    self.store.update(pid, port=port, webUrl=web_url)
                else:
                    self.log(pid, "❌ 自测未通过：服务起不来或探活超时（server.log 有明细）")
                    self._stop_proc(pid)        # 半死进程不许留着占资源（探活失败即回收）
            else:
                if not port:
                    self.log(pid, "⚠ 无可用端口（19000-19999 全占）→ 按静态站处理")
                # 静态站：只要目录里有 html 就算通过
                html = src / "public" / "index.html"
                if not html.is_file():
                    html = src / "index.html"
                test.update(ok=html.is_file(), note="静态站" if html.is_file() else "无 HTML 入口")
                self.log(pid, f"静态站判定: {'通过' if test['ok'] else '❌ 没有 index.html'}")
                if test["ok"]:
                    web_url = f"/serve/{pid}/"
                    self.store.update(pid, webUrl=web_url)
        # 客户端产物 → zip + 下载页（web-only 项目也会有源码 zip，下载页始终可用）
        artifacts = self._zip_client(pid, src)
        self.store.update(pid, artifacts=artifacts, dlUrl=f"/dl/{pid}/")
        self.log(pid, f"下载包就绪: {', '.join(artifacts)}  → /dl/{pid}/")
        # 磁盘配额核对（如实报告，不装死）
        used_mb = sum(f.stat().st_size for f in src.rglob("*") if f.is_file()) // (1024 * 1024)
        over = used_mb > int(p.get("diskGb", 0)) * 1024
        self.log(pid, f"磁盘占用 {used_mb} MB / 配额 {p.get('diskGb')} GB" + ("（⚠ 超配额）" if over else ""))
        if not test["ok"] and kind in ("web", "three-tier"):
            self._release_quota(pid, "自测未通过")
            self.store.update(pid, status=ST_FAILED, test=test,
                              error="自测未通过（服务探活失败）——产物保留在项目目录，可让 AI 继续修")
            return
        if kind == "unknown":
            # 【没有任何可识别产物 = 构建失败】第一次实测：Agent 那轮拿到空模型名、
            # 云端 400，目录里一个文件都没有，管线却标了 live ✗✗✗ —— 产物形态
            # 认不出来就必须算失败，不许用"部署完成"骗人。
            self._release_quota(pid, "没有可识别产物")
            self.store.update(pid, status=ST_FAILED, test=test,
                              error="Agent 没有产出可识别的产物（多半是构建那轮失败了，"
                                    "看上面的「Agent 结论」）—— 可继续对话让它重做")
            return
        # 【停止权优先】最终状态写入前再核一次：部署期间用户点了停止就不许改写成 live
        if not self._still_running(pid):
            self._release_quota(pid, "部署期间被停止")
            self.log(pid, "部署被用户停止打断（不写 live、不保留配额）")
            return
        self.store.update(pid, status=ST_LIVE, test=test)
        self.log(pid, f"✅ 部署完成：网页={web_url or '（无）'} 下载页=/dl/{pid}/")
        # 配额保留到显式 stop/失败释放 —— 见 stop_project 与 _release_quota

    def _still_running(self, pid: str) -> bool:
        cur = self.store.get(pid)
        return cur is not None and cur.get("status") != ST_STOPPED

    def _release_quota(self, pid: str, why: str) -> None:
        """失败/中断即释放配额 —— 原来只有 stop 释放 ✗✗✗：项目连续失败几次后
        资源池被僵尸配额占满、再也建不了新项目（总池是按物理机总量算的）。
        之后若点「重新部署」，会由 _ensure_quota 重新划走。"""
        if self.pool.release(pid):
            self.log(pid, f"资源配额已释放（{why}）")

    def _ensure_quota(self, pid: str) -> str | None:
        """重新部署前确保配额在册（失败已释放过 / 后端重启后池与状态不同步）；
        划不到就如实返回原因（不许"没配额也照样起服务"绕过总池）。"""
        p = self.store.get(pid) or {}
        return self.pool.allocate(pid, int(p.get("cpu", 1)), int(p.get("memoryMb", 1024)),
                                  int(p.get("diskGb", 5)))

    # ---------------------------------------------------- API 处理
    def info(self) -> dict[str, Any]:
        specs = physical_specs()
        used = self.pool.used()
        return {"name": PLATFORM_NAME, "tag": PLATFORM_TAG, "physical": specs, "used": used,
                "options": {"cpu": list(range(1, max(2, min(specs["cores"], 8)))),
                            "memMb": [512, 1024, 2048, 4096, 8192],
                            "diskGb": [2, 5, 10, 20, 50]}}

    def create_project(self, body: dict[str, Any]) -> dict[str, Any]:
        name = str(body.get("name") or "").strip() or "未命名项目"
        prompt = str(body.get("prompt") or "").strip()
        if not prompt:
            return {"ok": False, "error": "缺少「开始提示词」——要告诉 AI 做什么"}
        try:
            cpu = int(body.get("cpu") or 2)
            mem = int(body.get("memoryMb") or 2048)
            disk = int(body.get("diskGb") or 5)
        except (TypeError, ValueError):
            return {"ok": False, "error": "资源参数必须是数字"}
        specs = physical_specs()
        if cpu < 1 or cpu > specs["cores"]:
            return {"ok": False, "error": f"CPU 必须在 1..{specs['cores']}（物理机核数）"}
        if mem < 256 or mem > specs["ramMb"]:
            return {"ok": False, "error": f"内存必须在 256..{specs['ramMb']} MB（物理机总量）"}
        pid = datetime.now().strftime("p%Y%m%d%H%M%S") + os.urandom(3).hex()
        src = self.projects_dir / pid
        src.mkdir(parents=True, exist_ok=True)
        err = self.pool.allocate(pid, cpu, mem, disk)
        if err:
            shutil.rmtree(src, ignore_errors=True)
            return {"ok": False, "error": err}
        # AI API：给了就写进配置并重指适配器（与 /api/chat/adapter/config 同语义：掩码=没改）
        ai = body.get("aiApi") or {}
        ai_used = {"baseUrl": "", "model": "", "hasKey": False}
        if isinstance(ai, dict) and any([ai.get("baseUrl"), ai.get("apiKey"), ai.get("model")]):
            try:
                cfg = self.ctx.cfg
                providers = dict(cfg.get("providers") or {})
                cur = dict(providers.get("lionbox-custom") or {})
                updates: dict[str, Any] = {"providerMode": "custom"}
                for k in ("baseUrl", "apiKey", "model"):
                    v = ai.get(k)
                    if v is not None and str(v).strip() and not str(v).endswith("••••") and "•" not in str(v):
                        cur[k] = str(v)
                        updates[k] = str(v)
                providers["lionbox-custom"] = cur
                updates["providers"] = providers
                cfg.update(updates)
                target = self.ctx.adapters().get_active_adapter()
                if target is not None:
                    patch = {k: cur[k] for k in ("baseUrl", "apiKey", "model") if cur.get(k)}
                    target.update_config(patch)
                ai_used = {"baseUrl": cur.get("baseUrl", ""), "model": cur.get("model", ""),
                           "hasKey": bool(cur.get("apiKey"))}
            except Exception as e:                           # noqa: BLE001 不让创建被它挡住
                self.log(pid, f"⚠ AI API 应用失败（仍用当前配置继续）: {type(e).__name__}: {e}")
        # 工作区 + 会话（与 TUI/聊天同一套存储 ⇒ 后续可以在平台或 TUI 里继续聊）
        deps = self._deps()
        ws_item = deps.workspaces(self.ctx).register_workspace(str(src))
        # 【register_workspace 返回条目 dict {'id','path','permission'}，不是 id】
        # 第一版把整个 dict `str(wid)` 当 workspace_id 传给 create_session ✗✗✗：
        # 会话绑的工作区 id 变成 "{'id': ...}" 垃圾串 ⇒ Agent 写文件时按它拼路径 ⇒
        # WinError 123（非法路径）⇒ 审核放行一直失败 ⇒ Agent 无限重试、files=0、
        # 卡 building 十几分钟（2026-10-17 实测）。取 id 字段（str 也兼容）。
        wid = str(ws_item.get("id") if isinstance(ws_item, dict)
                  else getattr(ws_item, "id", ws_item))
        session = deps.sessions(self.ctx).create_session(wid, "STANDARD")
        # 【会话持久化预检】SessionManager.createSession 自己不落盘（POST 里是显式
        # _persist_session），而本机的会话持久化目录可能不可写（sessions/events EACCES ✗）
        # ⇒ 后端一重启会话就查无 ⇒ AI 会回退到仓库根干活（实测发生 ✗✗✗）。
        # 有可写性问题就**在日志里明说**，不让用户事后懵。
        try:
            _sp = deps.sessions(self.ctx)
            sess_dir = getattr(getattr(_sp, "persistence", None), "sessions_dir", None)
            if sess_dir is not None:
                Path(str(sess_dir)).mkdir(parents=True, exist_ok=True)
                probe = Path(str(sess_dir)) / "_lionforge_write_probe.tmp"
                probe.write_text("x", encoding="utf-8")
                probe.unlink()
        except Exception as e:                               # noqa: BLE001
            print(f"[平台] ⚠ 会话持久化不可写（后端重启会丢会话，必要时重建项目）: "
                  f"{type(e).__name__}: {e}", flush=True)
        # 【真实 SessionManager 返回 Session 对象，窄桩返回 dict】两种都认：
        # 对象看 .session_id（team/subagent_tool 同款用法），dict 看 sessionId/id。
        sid_attr = getattr(session, "session_id", None)
        if sid_attr:
            session_id = str(sid_attr)
        elif isinstance(session, dict):
            session_id = str(session.get("sessionId") or session.get("id") or "")
        else:
            session_id = ""
        if not session_id:
            shutil.rmtree(src, ignore_errors=True)
            self.pool.release(pid)
            return {"ok": False, "error": "会话创建失败（拿不到 sessionId）"}
        item = {"id": pid, "name": name, "prompt": prompt, "cpu": cpu, "memoryMb": mem,
                "diskGb": disk, "sessionId": session_id, "workspaceId": wid, "aiApi": ai_used,
                "status": ST_CREATED, "kind": "", "createdAt": _now(), "webUrl": None,
                "dlUrl": None, "test": {}, "artifacts": [], "buildReply": "", "error": ""}
        self.store.add(item)
        self.log(pid, f"项目已创建：{name}（CPU {cpu} 核 / 内存 {mem} MB / 磁盘 {disk} GB）")
        with LOCK:
            self._busy.add(pid)
        threading.Thread(target=self._build_pipeline, args=(pid,), daemon=True,
                         name=f"lionforge-build-{pid[:8]}").start()
        return {"ok": True, "id": pid, "sessionId": session_id}

    def chat(self, pid: str, message: str) -> dict[str, Any]:
        p = self.store.get(pid)
        if p is None:
            return {"ok": False, "error": "项目不存在"}
        # 【会话必须还在】后端重启后会话靠持久化恢复；持久化目录不可写时（本机沙箱
        # 就踩过：sessions/events 落盘 EACCES ✗✗✗）会话查无 ⇒ AgentLoop 的
        # resolve_workspace 回退到**仓库根** ⇒ AI 改错目录（实测去改了 docs/ 下的文件 ✗✗✗）。
        # 宁可诚实失败，也绝不能让它在错的目录里动手。
        try:
            alive = self._deps().sessions(self.ctx).get_session(p["sessionId"])
        except Exception:                                   # noqa: BLE001
            alive = None
        if not alive:
            return {"ok": False,
                    "error": "会话已随后端重启丢失（会话持久化目录不可写）。"
                             "请点「重新构建」或重建项目，不要继续改——否则会写到错误目录。"}
        with LOCK:
            if pid in self._busy:
                return {"ok": False, "error": "项目正在构建/部署中，等它交付后再聊（看状态）"}
            self._busy.add(pid)
        try:
            # 【每条消息都带绝对项目路径】就算 workspace 解析回退，AI 也照绝对路径干活
            src = str(self.projects_dir / pid)
            message = (f"（项目绝对路径：{src} —— 本项目所有文件的读写都必须用这个绝对路径，"
                       f"不要写到别处）\n" + message)
            self.log(pid, f"用户消息: {message[:120]}")
            t0 = time.time()
            reply = self._agent_run(pid, p["sessionId"], message)
            self.log(pid, f"AI 回复（{int(time.time() - t0)}s）: {reply[:200]}")
            # 改动后服务若在跑，重启一次让它带新代码（最朴素但可靠的部署语义）
            note = ""
            if pid in self._procs:
                note = "已重启部署服务（改动已生效）"
                self._restart_deploy(pid)
            return {"ok": True, "reply": reply, "note": note}
        except Exception as e:                               # noqa: BLE001
            self.log(pid, f"聊天异常: {type(e).__name__}: {e}")
            return {"ok": False, "error": f"{type(e).__name__}: {e}"}
        finally:
            with LOCK:
                self._busy.discard(pid)

    def _restart_deploy(self, pid: str) -> None:
        p = self.store.get(pid)
        src = self.projects_dir / pid
        self._stop_proc(pid)                # 统一走停进程助手（否则旧进程会成孤儿）
        port = int(p.get("port") or 0)
        if not port or not self._port_free(port):
            port = self._pick_port()
        if not port:
            self.log(pid, "⚠ 无可用端口，部署未重启")
            return
        proc = self._start_server(pid, src, port)
        if proc is not None:
            self._procs[pid] = proc
            ok, code, _ = self._probe(port)
            self.store.update(pid, port=port, webUrl=f"/serve/{pid}/",
                              test=dict(p.get("test") or {}, ok=ok, http=code))
            self.log(pid, f"部署已重启: ok={ok} http={code}")

    def stop_project(self, pid: str) -> dict[str, Any]:
        p = self.store.get(pid)
        if p is None:
            return {"ok": False, "error": "项目不存在"}
        # 先改状态再杀进程：构建线程的后续写入都会被 `_still_running` 挡掉
        # （否则 stop 后构建线程照样把状态改回 live 并起服务 ✗✗✗）
        self.store.update(pid, status=ST_STOPPED)
        self._stop_proc(pid)
        self.pool.release(pid)
        self.log(pid, "已停止（状态=已停止；服务进程已终止；资源配额已释放）")
        return {"ok": True}


# ============================================================ HTTP 出口
MIME = {".html": "text/html; charset=utf-8", ".js": "application/javascript; charset=utf-8",
        ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
        ".png": "image/png", ".svg": "image/svg+xml", ".jpg": "image/jpeg",
        ".ico": "image/x-icon", ".txt": "text/plain; charset=utf-8", ".zip": "application/zip",
        ".md": "text/plain; charset=utf-8"}


def _pid_of(req_path: str, tail: str) -> str:
    """从 /api/platform/projects/<pid>/<tail> 里取出 pid。
    【踩过的坑】第一版写 `path.split("/")[-1]` ⇒ 对 /chat、/log、/stop 取到的是
    "chat"/"log"/"stop" 本身 ✗✗✗（详情接口没有尾巴所以没暴露）⇒ 聊天永远 409"项目不存在"。
    """
    m = re.search(r"^/api/platform/projects/([^/]+)" + re.escape(tail) + r"/?$", req_path)
    return m.group(1) if m else ""


def register(router: Any, ctx: Any, Response: Any) -> None:
    """把 LionForge 挂到后端路由上（main 的 register__api_platform 调用）。"""
    api = PlatformApi(ctx, Response)

    @router.get("/platform")
    def platform_page(req: Any) -> Any:
        return Response(PLATFORM_HTML, content_type="text/html; charset=utf-8")

    @router.get("/api/platform/info")
    def platform_info(req: Any) -> Any:
        return Response.json(api.info())

    @router.get("/api/platform/projects")
    def platform_list(req: Any) -> Any:
        items = sorted(api.store.all(), key=lambda x: x.get("createdAt", ""), reverse=True)
        return Response.json({"items": items, "busy": sorted(api._busy)})

    @router.post("/api/platform/projects")
    def platform_create(req: Any) -> Any:
        body = req.json_obj() if hasattr(req, "json_obj") else {}
        if not isinstance(body, dict):
            body = {}
        out = api.create_project(body)
        return Response.json(out, status=200 if out.get("ok") else 400)

    @router.get("/api/platform/projects/{pid}")
    def platform_detail(req: Any) -> Any:
        pid = req.path.rstrip("/").split("/")[-1]
        p = api.store.get(pid)
        if p is None:
            return Response.json({"ok": False, "error": "项目不存在"}, status=404)
        p["log"] = api.read_log(pid)
        p["busy"] = pid in api._busy
        # 密钥不回显（平台页只显示 hasKey）
        p["aiApi"] = {"baseUrl": (p.get("aiApi") or {}).get("baseUrl", ""),
                      "model": (p.get("aiApi") or {}).get("model", ""),
                      "hasKey": bool((p.get("aiApi") or {}).get("hasKey"))}
        return Response.json(p)

    @router.get("/api/platform/projects/{pid}/log")
    def platform_log(req: Any) -> Any:
        pid = _pid_of(req.path, "/log")
        return Response(api.read_log(pid, tail=200), content_type="text/plain; charset=utf-8")

    @router.post("/api/platform/projects/{pid}/chat")
    def platform_chat(req: Any) -> Any:
        pid = _pid_of(req.path, "/chat")
        body = req.json_obj() if hasattr(req, "json_obj") else {}
        msg = str((body or {}).get("message") or "").strip()
        if not msg:
            return Response.json({"ok": False, "error": "消息为空"}, status=400)
        out = api.chat(pid, msg)
        return Response.json(out, status=200 if out.get("ok") else 409)

    @router.post("/api/platform/projects/{pid}/stop")
    def platform_stop(req: Any) -> Any:
        pid = _pid_of(req.path, "/stop")
        return Response.json(api.stop_project(pid))

    @router.post("/api/platform/projects/{pid}/redeploy")
    def platform_redeploy(req: Any) -> Any:
        """重新自测 + 部署（后端重启后 _procs 丢了、或用户手改了代码时用）。"""
        pid = _pid_of(req.path, "/redeploy")
        p = api.store.get(pid)
        if p is None:
            return Response.json({"ok": False, "error": "项目不存在"}, status=404)
        with LOCK:
            if pid in api._busy:
                return Response.json({"ok": False, "error": "项目正在忙"}, status=409)
            api._busy.add(pid)

        def run() -> None:
            try:
                # 【先停旧、再确保配额】原实现直接 _start_server ⇒ 旧进程成孤儿、
                # 新进程绑不上端口（端口被旧进程占着）✗✗✗；配额若因失败/重启不在册，
                # 也要在这里重新划走，否则等于绕过物理机总池。
                api._stop_proc(pid)
                qerr = api._ensure_quota(pid)
                if qerr:
                    api.log(pid, f"重新部署被拒：{qerr}")
                    api.store.update(pid, status=ST_FAILED, error=qerr)
                    return
                api.log(pid, "重新部署（自测 + 部署）…")
                api._test_and_deploy(pid, api.projects_dir / pid)
            except Exception as e:                           # noqa: BLE001
                api.log(pid, f"❌ 重新部署异常: {type(e).__name__}: {e}")
                api._release_quota(pid, "重新部署异常")
                if api._still_running(pid):
                    api.store.update(pid, status=ST_FAILED, error=f"{type(e).__name__}: {e}")
            finally:
                with LOCK:
                    api._busy.discard(pid)

        threading.Thread(target=run, daemon=True, name=f"lionforge-redeploy-{pid[:8]}").start()
        return Response.json({"ok": True})

    # {rest*} = 多段透传（Router 支持 `{name*}` 匹配剩余全部段）——部署应用的
    # HTML 里都是相对路径（./app.js、/assets/x.css），必须整段转给它。
    # 【尾斜杠必须单独注册】`{rest*}` 用 `.+`（非空），`/serve/<id>/` 的 rest 是空串 ⇒
    # 两个模板都罩不住它（实测 404"没有这个接口" ✗✗✗），所以把 "/" 版本显式加上。
    @router.get("/serve/{pid}")
    @router.get("/serve/{pid}/")
    @router.get("/serve/{pid}/{rest*}")
    @router.post("/serve/{pid}")
    @router.post("/serve/{pid}/")
    @router.post("/serve/{pid}/{rest*}")
    def serve_deployed(req: Any) -> Any:
        parts = req.path.split("/")
        pid = parts[2]
        rest = "/".join(parts[3:]) if len(parts) > 3 else ""
        p = api.store.get(pid)
        if p is None:
            return Response.json({"ok": False, "error": "项目不存在"}, status=404)
        proc = api._procs.get(pid)
        src = api.projects_dir / pid
        if proc is not None and p.get("port"):
            try:
                url = f"http://127.0.0.1:{p['port']}/{urllib.parse.quote(rest)}"
                with urllib.request.urlopen(url, timeout=30) as r:
                    body = r.read()
                    ctype = r.headers.get("Content-Type") or "text/html; charset=utf-8"
                return Response(body, content_type=ctype)
            except urllib.error.HTTPError as e:
                return Response(e.read(), status=int(e.code))
            except Exception as e:                           # noqa: BLE001
                return Response.json({"ok": False, "error": f"代理失败: {e}"}, status=502)
        # 静态站
        root = src / "public"
        if not root.is_dir():
            root = src
        rel = urllib.parse.unquote(rest) or "index.html"
        target = (root / rel).resolve()
        try:
            target.relative_to(root.resolve())
        except ValueError:
            return Response.json({"ok": False, "error": "非法路径"}, status=400)
        if target.is_dir():
            target = target / "index.html"
        if not target.is_file():
            return Response.json({"ok": False, "error": "文件不存在"}, status=404)
        ctype = MIME.get(target.suffix.lower(), "application/octet-stream")
        return Response(target.read_bytes(), content_type=ctype)

    @router.get("/dl/{pid}")
    @router.get("/dl/{pid}/")
    def download_page(req: Any) -> Any:
        pid = req.path.rstrip("/").split("/")[-1]
        p = api.store.get(pid)
        if p is None:
            return Response.json({"ok": False, "error": "项目不存在"}, status=404)
        return Response(_dl_html(api, p), content_type="text/html; charset=utf-8")

    @router.get("/dl/{pid}/{name}")
    def download_file(req: Any) -> Any:
        parts = req.path.split("/")
        pid, name = parts[2], parts[3]
        if api.store.get(pid) is None:
            return Response.json({"ok": False, "error": "项目不存在"}, status=404)
        f = api.projects_dir / pid / ".lionforge" / name
        if not f.is_file():
            return Response.json({"ok": False, "error": "产物不存在"}, status=404)
        ctype = MIME.get(f.suffix.lower(), "application/octet-stream")
        return Response(f.read_bytes(), content_type=ctype,
                        headers={"Content-Disposition": f'attachment; filename="{name}"'})


def _dl_html(api: PlatformApi, p: dict[str, Any]) -> str:
    # 【项目名/文件名是外部输入】f-string 直接进 HTML = XSS；下载页与平台页同一
    # origin，恶意租户起个 <script> 名字就能在别人打开下载页时执行（多租户服务器是真风险）。
    from html import escape as _esc
    pname = _esc(str(p.get("name") or ""))
    rows = []
    for name in p.get("artifacts") or []:
        f = api.projects_dir / p["id"] / ".lionforge" / name
        size = f"{f.stat().st_size // 1024} KB" if f.is_file() else "缺失"
        rows.append(f'<tr><td><a href="/dl/{p["id"]}/{urllib.parse.quote(name)}">'
                    f'{_esc(str(name))}</td><td>{size}</td></tr>')
    body = "\n".join(rows) or '<tr><td colspan="2">（还没有产物）</td></tr>'
    return f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{pname} · 下载</title>
<style>body{{background:#0d1117;color:#e6edf3;font:15px/1.7 -apple-system,"Segoe UI",Consolas,sans-serif;}}
.wrap{{max-width:760px;margin:40px auto;padding:0 20px}}a{{color:#e3b341}}
table{{width:100%;border-collapse:collapse;margin-top:16px}}th,td{{border:1px solid #30363d;padding:8px 12px;text-align:left}}</style>
</head><body><div class="wrap">
<h1>{pname}</h1><p class="muted">由 LionForge（狮铸）构建与部署 · {_esc(str(p.get('kind', '')))}</p>
<table><tr><th>产物</th><th>大小</th></tr>{body}</table>
<p><a href="/platform">← 返回 LionForge</a></p></div></body></html>"""


# ============================================================ 平台页（自包含，无外链）
PLATFORM_HTML = r"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>LionForge 狮铸 · 项目 AI 开发平台</title>
<style>
:root{--bg:#0d1117;--panel:#161b22;--fg:#e6edf3;--mut:#8b949e;--acc:#e3b341;--ok:#3fb950;--bad:#f85149;--line:#30363d}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:14.5px/1.65 -apple-system,"Segoe UI",Consolas,"Microsoft YaHei",sans-serif}
.wrap{max-width:1080px;margin:0 auto;padding:28px 18px 90px}h1{font-size:24px;margin:0 0 4px}
.sub{color:var(--mut);margin-bottom:18px}.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:16px 18px;margin-bottom:18px}
label{display:block;color:var(--mut);font-size:13px;margin:10px 0 4px}input,select,textarea{width:100%;background:#0d1117;color:var(--fg);border:1px solid var(--line);border-radius:6px;padding:8px 10px;font:inherit}
textarea{min-height:84px;resize:vertical}.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:12px}
button{background:var(--acc);color:#1a1200;border:0;border-radius:6px;padding:9px 16px;font:inherit;font-weight:600;cursor:pointer}
button.ghost{background:transparent;color:var(--fg);border:1px solid var(--line);font-weight:400;padding:6px 10px;margin-right:6px}
button:disabled{opacity:.5;cursor:default}.badge{display:inline-block;padding:1px 8px;border-radius:99px;font-size:12px;border:1px solid var(--line)}
.b-building,.b-testing,.b-deploying{color:var(--acc);border-color:var(--acc)}.b-live{color:var(--ok);border-color:var(--ok)}
.b-failed{color:var(--bad);border-color:var(--bad)}.b-stopped,.b-created{color:var(--mut)}
.card{border:1px solid var(--line);border-radius:8px;padding:12px 14px;margin-bottom:12px;background:#0f141a}
.muted{color:var(--mut);font-size:13px}pre{background:#0a0d12;border:1px solid var(--line);border-radius:6px;padding:10px;max-height:300px;overflow:auto;font-size:12.5px;white-space:pre-wrap}
.err{color:var(--bad)}a{color:var(--acc)}.grid2{display:grid;grid-template-columns:1fr 1fr;gap:18px}@media(max-width:820px){.grid2{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<h1>LionForge <span style="font-size:15px;color:var(--mut)">狮铸 · 项目 AI 开发平台</span></h1>
<div class="sub" id="spec">物理机资源加载中…</div>
<div class="panel"><h3 style="margin:0 0 4px">创建项目</h3>
<div class="row"><div><label>项目名</label><input id="name" placeholder="例如：每日账本"></div>
<div><label>CPU（核）</label><select id="cpu"></select></div>
<div><label>内存（MB）</label><select id="mem"></select></div>
<div><label>磁盘（GB）</label><select id="disk"></select></div></div>
<label>AI API</label>
<select id="apisel" onchange="document.getElementById('ai').style.display=this.value==='custom'?'block':'none'">
<option value="current">沿用当前已配置的模型</option><option value="custom">自定义（写进全局配置）</option></select>
<div id="ai" style="display:none"><div class="row">
<div><label>API 地址 baseUrl</label><input id="baseUrl" placeholder="https://…/v1"></div>
<div><label>API Key</label><input id="apiKey" placeholder="sk-…（掩码=不改）"></div>
<div><label>模型名</label><input id="model" placeholder="mimo-v2.6-flash"></div></div></div>
<label>项目开始提示词（AI 做什么）</label>
<textarea id="prompt" placeholder="例：做一个每日账本网页：可增删记录、按月统计、数据存本地；界面简洁中文；自测要真启动服务并验证"></textarea>
<div style="margin-top:12px"><button onclick="create()">创建并交给 Agent</button>
<span class="muted" id="msg"></span></div></div>
<div class="grid2"><div><h3 style="margin:0 0 8px">项目</h3><div id="list"></div></div>
<div><h3 style="margin:0 0 8px">详情</h3><div id="detail" class="muted">点左侧项目查看 / 聊天</div></div></div>
</div><script>
let OPTS=null,SEL=null,POLL=null,DLOG=null;
const $=id=>document.getElementById(id);
async function j(url,opt){const r=await fetch(url,opt);let d=null;try{d=await r.json()}catch(e){}
 if(!r.ok)throw new Error((d&&d.error)||r.status);return d}
async function loadInfo(){const i=await j('/api/platform/info');OPTS=i.options;
 $('spec').innerHTML=`物理机 <b>${i.physical.cores}</b> 核 / <b>${i.physical.ramMb}</b> MB 内存 / 磁盘 <b>${i.physical.diskGb}</b> GB · ${i.physical.os||''}
 · 已分配 <b>${i.used.cpu}</b> 核 / <b>${i.used.memMb}</b> MB（${i.used.count} 个项目）`;
 fill('cpu',i.options.cpu);fill('mem',i.options.memMb);fill('disk',i.options.diskGb);}
function fill(id,arr){const s=$(id);s.innerHTML=arr.map(v=>`<option>${v}</option>`).join('')}
async function create(){const msg=$('msg');msg.textContent='创建中…';
 const body={name:$('name').value||'未命名项目',prompt:$('prompt').value,cpu:+$('cpu').value,
  memoryMb:+$('mem').value,diskGb:+$('disk').value,
  aiApi:$('apisel').value==='custom'?{baseUrl:$('baseUrl').value,apiKey:$('apiKey').value,model:$('model').value}:{}};
 try{const d=await j('/api/platform/projects',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
  msg.textContent='已创建，正在进入 Agent 对话页…';$('prompt').value='';refresh();
  // 【创建即进入对话页】原来只刷列表、要手动点"详情" ✗✗✗ —— 创建后直接打开
  // 该项目的详情/对话面板（构建日志 + 与 AI 对话都在那里，边建边看）。
  detail(d.id)}
 catch(e){msg.innerHTML='<span class="err">'+esc(e.message)+'</span>'}}
async function refresh(){try{const d=await j('/api/platform/projects');$('list').innerHTML=d.items.map(p=>card(p,d.busy)).join('')||'<div class="muted">还没有项目</div>'}catch(e){}}
function card(p,busy){const b=busy.includes(p.id)||['building','testing','deploying'].includes(p.status);
 // 【项目名是用户输入，必须转义】直接插 innerHTML 是 XSS（多租户服务器上是真风险：
 // 一个租户起个 <img onerror=…> 名字就能在别的租户看同一页时执行）—— 名称/标题/错误
 // 文案全都过 esc()。
 return `<div class="card"><b>${esc(p.name)}</b> <span class="badge b-${p.status}">${esc(statusText(p.status))}</span>
 <div class="muted">${p.cpu} 核 · ${p.memoryMb} MB · ${p.diskGb} GB${p.kind?' · '+kindText(p.kind):''} · ${p.createdAt}</div>
 <div style="margin-top:8px"><button class="ghost" onclick="detail('${p.id}')">详情</button>
 ${p.webUrl?`<button class="ghost" onclick="open('/serve/${p.id}/')">打开网页</button>`:''}
 ${p.dlUrl?`<button class="ghost" onclick="open('/dl/${p.id}/')">下载页</button>`:''}
 <button class="ghost" onclick="stopP('${p.id}')">停止</button></div></div>`}
const statusText=s=>({created:'待构建',building:'Agent 构建中',testing:'自测中',deploying:'部署中',live:'已上线',failed:'失败',stopped:'已停止'})[s]||s;
const kindText=k=>({web:'网页','client':'客户端','three-tier':'三端','unknown':'未知'})[k]||k;
function open(u){window.open(u,'_blank')}
async function stopP(id){await j('/api/platform/projects/'+id+'/stop',{method:'POST'});refresh()}
async function redeploy(id){await j('/api/platform/projects/'+id+'/redeploy',{method:'POST'});refresh();detail(id)}
async function detail(id){SEL=id;const p=await j('/api/platform/projects/'+id);
 const t=p.test||{};
 $('detail').innerHTML=`<div class="card"><b>${esc(p.name)}</b> <span class="badge b-${p.status}">${esc(statusText(p.status))}</span>
 <div class="muted">会话 ${esc(p.sessionId)}</div>
 ${t.kind?`<div class="muted">自测: ${esc(kindText(t.kind))}${t.http!==null?' · HTTP '+esc(String(t.http)):''}${t.title?' · 标题「'+esc(t.title)+'」':''}</div>`:''}
 ${p.webUrl?`<div>网页：<a href="${p.webUrl}" target="_blank">${esc(p.webUrl)}</a></div>`:''}
 ${p.dlUrl?`<div>下载页：<a href="${p.dlUrl}" target="_blank">${esc(p.dlUrl)}</a></div>`:''}
 ${p.error?`<div class="err">${esc(p.error)}</div>`:''}
 <div class="muted" style="margin-top:6px">隔离说明：本项目的工作目录就是这个租户实例的<b>全部可见空间</b>
 —— Agent 的文件工具被硬性限定在该目录内（越界访问会被直接拒绝）。shell 命令以该目录为工作目录启动；
 若需要 OS 级强隔离（多租户同机），需要把实例跑进受限账户/容器 —— 见 README 的部署说明。</div>
 <div style="margin-top:8px"><button class="ghost" onclick="redeploy('${p.id}')">重新部署</button></div>
 ${p.buildReply?`<details><summary class="muted">Agent 结论</summary><div class="muted">${esc(p.buildReply)}</div></details>`:''}
 </div>
 <div class="card"><b>构建/部署日志</b><pre id="dlog">${esc(p.log||'（暂无）')}</pre></div>
 <div class="card"><b>继续跟 AI 说话</b>（改功能 / 修 bug，都在同一会话）
 <div id="msgs" class="muted">${p.busy?'⏳ Agent 正在构建/部署中 —— 完成后这里就能对话（本面板每 5 秒自动刷新）':'发送记录见日志'}</div>
 <textarea id="chatin" ${p.busy?'disabled':''} placeholder="${p.busy?'构建中…请稍候':'例：把标题改成「我的账本」并自测一遍'}"></textarea>
 <div style="margin-top:8px"><button id="chatsend" onclick="send()" ${p.busy?'disabled':''}>发送</button><span class="muted" id="chatmsg"></span></div></div>`;}
 // 构建期间自动刷新本面板：忙 ⇒ 5 秒后重取（聊天框从禁用变可用就是靠它）；
 // 闲 ⇒ 不再重取（避免把用户已输入但没发的文字清掉）。
 if(p.busy) setTimeout(()=>{if(SEL===p.id) detail(p.id)},5000)}
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
async function send(){const id=SEL,msg=$('chatin').value.trim();if(!msg)return;
 $('chatsend').disabled=true;$('chatmsg').textContent='AI 思考中…（改动+自测需要时间）';
 try{const d=await j('/api/platform/projects/'+id+'/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:msg})});
  $('chatmsg').textContent=d.note||'完成';detail(id)}
 catch(e){$('chatmsg').innerHTML='<span class="err">'+esc(e.message)+'</span>'}
 finally{$('chatsend').disabled=false}}
loadInfo();refresh();setInterval(refresh,4000);
setInterval(()=>{if(SEL){fetch('/api/platform/projects/'+SEL+'/log').then(r=>r.text()).then(t=>{const el=$('dlog');if(el)el.textContent=t||'（暂无）'}).catch(()=>{})}},3000);
</script></body></html>"""
