# -*- coding: utf-8 -*-
r"""一键启动：Lion Code 后端 + MiMo 兼容接口层 + 自带终端界面（tui/）。

三段式（顺序不能反）：

    ① main.py --backend-only        我们的 Python 后端（能力都在这）
    ② mimo适配.py                   MiMo 形状的兼容接口层（保留备用，界面不再依赖它）
    ③ tui/                          自带终端界面（OpenTUI + SolidJS）→ 直连 ① 的 HTTP

【为什么不再 attach MiMo】MiMo 前端与它的补丁机制已整体移除；界面换成仓库自带的 `tui/`
（同一渲染栈，但只做界面、直连后端，不经 8791 适配层）。

【看门狗】① ② 死掉会自动拉起 —— 这条是踩出来的：用户有一次盯着界面等了 10 分钟
"它啥也没干"，查下来是**后端与适配层的 python 进程一个都不在了**，界面还在、
但它在跟空气说话。前端是用户的（他自己关掉的就不该被拉起），所以只看 ① ②。
"""
from __future__ import annotations

import os
import subprocess
import sys
import threading
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.isfile(PY):
    PY = sys.executable

def _env_port(name: str, default: int) -> int:
    """读环境变量里的端口；**非法值显式告警并回退默认值**，绝不让 import 崩。

    【为什么不直接 `int(...)`】这两个值完全来自外部 shell 环境（全仓库只有本文件
    读它、没有任何脚本设置它），用户手误设成 `LION_CODE_BACKEND_PORT=18080a`
    就会在 **模块导入期**抛 ValueError —— 此时 `_LOGDIR` 还没建、**一行日志都打不出来**
    ✗（本会话反复抓的"失败仍报成功 / 静默失败"的同一类形态 ✓）。
    """
    raw = os.environ.get(name)
    if raw is None or not str(raw).strip():
        return default
    try:
        return int(str(raw).strip())
    except ValueError:
        print(f"[警告] 环境变量 {name}={raw!r} 不是整数，改用默认值 {default}", flush=True)
        return default


BACKEND_PORT = _env_port("LION_CODE_BACKEND_PORT", 18080)
ADAPTER_PORT = _env_port("LION_CODE_ADAPTER_PORT", 8791)

#: 看门狗节奏：12 秒一轮（够快，又不至于抖）。连挂多次后退避到 60 秒 ——
#: 端口被占、依赖缺失这类问题重启一百次也没用，退避能避免把日志刷爆。
WATCH_INTERVAL = 12.0
WATCH_BACKOFF_AFTER = 3          # 连续挂几次开始退避
WATCH_BACKOFF_INTERVAL = 60.0

try:
    # 【必须兜底】main.py 对同款调用也包了 try/except —— 某些环境里 stdout 没有
    # reconfigure（重定向到管道/被宿主接管时会 AttributeError），裸调会 import 期崩。
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:                                          # noqa: BLE001
    pass

def _detect_data_dir() -> str:
    """可写的运行数据根（日志 / 工作区 / MiMo home 都放它下面）。

    【为什么不能写死 `ROOT/.lbcheck`】打包安装到 `Program Files` 这类只读位置时，
    `os.makedirs(ROOT/.lbcheck)` 直接抛 PermissionError → **启动器第一句就崩** ✗
    （本会话反复吃过"静默失败"的亏，所以这里必须**显式探测 + 回退**）。
    回退到 `%LOCALAPPDATA%\\LionCode\\data` —— 那里任何用户都可写 ✓
    （真正持久化的 `~/.lioncode` 本来就在家目录，与安装位置无关 ✓）。
    """
    cand = os.path.join(ROOT, ".lbcheck")
    try:
        os.makedirs(cand, exist_ok=True)
        probe = os.path.join(cand, ".wprobe")
        with open(probe, "w", encoding="utf-8") as f:
            f.write("ok")
        os.remove(probe)
        return cand
    except OSError:
        fb = os.path.join(os.environ.get("LOCALAPPDATA") or os.path.expanduser("~"),
                          "LionCode", "data")
        os.makedirs(fb, exist_ok=True)
        return fb


_LOGDIR = _detect_data_dir()


def log(msg: str) -> None:
    """控制台 + 看门狗日志各写一份。

    【为什么要落盘】用户看不到控制台滚动的内容（TUI 占屏），事后要能查
    "什么时候重启过、重启了几次" —— 本会话反复吃过"静默失败"的亏 ✗。
    """
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    try:
        with open(os.path.join(_LOGDIR, "watchdog.log"), "a",
                  encoding="utf-8", errors="replace") as f:
            f.write(line + "\n")
    except Exception:                                     # noqa: BLE001
        pass


def wait_up(url: str, timeout: float = 60.0, proc=None, stop=None) -> bool:
    """等服务开始监听。

    【`stop` 参数是干什么的】看门狗 `shutdown()` 之后，在途的 `wait_ready` 必须尽快
    让出 —— 否则"重启窗口内新拉起的进程无人回收" ✗ 会留下孤儿 backend/adapter，
    并污染下一轮健康检查（本会话 audit2 实测的那条 MEDIUM ✓）。
    """
    end = time.time() + timeout
    while time.time() < end:
        if stop is not None and stop.is_set():
            return False
        if proc is not None and proc.poll() is not None:
            return False
        try:
            with urllib.request.urlopen(url, timeout=2):
                return True
        except Exception:                                 # noqa: BLE001
            time.sleep(0.3)
    return False


# ── 两个服务的启动命令（看门狗重启时要用同一份 ✗ 不许各写一遍 ✓）───────────
def backend_cmd(workspace_root: str) -> list[str]:
    args = ["--backend-only",
            f"--server.port={BACKEND_PORT}",
            # 【--app-root 不能少】它决定去哪找 `runtime-vulkan/llama-server.exe`
            # 和 `*.gguf`。不给的话默认是 <仓库>\python（老布局），模型会被判为
            # "未安装"从而触发重新下载，本地模型永远起不来。
            f"--app-root={ROOT}",
            # 【工作区根目录】默认是 `~/lion-code-workspace`（照 Java 的
            # application.yml）。但那个目录下 `.lioncode/` 子目录的 ACL 受限，
            # 后端存会话元数据 / 事件会吃 Permission denied（实测日志里就是它），
            # 于是会话历史没法落盘。指到仓库内（已被 .gitignore 覆盖）。
            "--lion.workspace.default-path=" + workspace_root,
            "--config-dir=" + os.path.join(_LOGDIR, "mimo")]
    # 【打包版走 exe】Nuitka 编译分发时机器上没有 Python 解释器 ✗ ——
    # 同目录若有 `LionCode.exe` 就用它（开发期没这个文件，仍走 main.py ✓）。
    exe = os.path.join(ROOT, "LionCode.exe")
    if os.path.isfile(exe):
        return [exe] + args
    return [PY, os.path.join(ROOT, "main.py")] + args


def adapter_cmd(workspace_root: str) -> list[str]:
    args = [f"--port={ADAPTER_PORT}",
            f"--backend=http://127.0.0.1:{BACKEND_PORT}",
            f"--directory={os.getcwd()}",
            # 【必须和后端同一个值】适配层要用它去 <root>/.lioncode/conversations/
            # 读历史，侧边栏切换会话时才能回放出对话内容。
            f"--workspace={workspace_root}"]
    exe = os.path.join(ROOT, "adapter.exe")
    if os.path.isfile(exe):
        return [exe] + args
    return [PY, os.path.join(ROOT, "mimo适配.py")] + args


class Watchdog(threading.Thread):
    """盯着 ① ② 还在不在，死了就拉起来。

    【边界】只管自己拉起的两个进程 ✗ ——
      · llama-server 归后端自己管（它有 `POST /api/runtime/local/start` ✓）
      · MiMo 前端归用户（他自己关窗口是正常行为 ✓ 拉起反而吓人 ✗）
    """

    def __init__(self, workspace_root: str, backend_log, adapter_log):
        super().__init__(daemon=True, name="watchdog")
        self.workspace_root = workspace_root
        self.backend_log = backend_log
        self.adapter_log = adapter_log
        self.procs: dict[str, subprocess.Popen] = {}
        self.fails = {"backend": 0, "adapter": 0}
        self.restarts = {"backend": 0, "adapter": 0}
        self.stop_event = threading.Event()

    # -- 启动
    def _env(self) -> dict[str, str]:
        """子进程环境：与**前端同一套临时目录口径**。

        【为什么 backend/adapter 也要】`TMP/TEMP/TMPDIR/SQLITE_TMPDIR` 原来只注入给
        前端子进程（main() 里那份 env ✓），两个服务的临时文件会回退到系统 `%TEMP%`。
        本机实测过"工作区外的 temp 不可写"这类问题（cl 的 `_CL_*` Permission denied、
        link 的 `lnk*.tmp` LNK1104 都是同源 ✓）—— 三段统一用 `_LOGDIR/tmp` 才一致 ✓。
        """
        tmp = os.path.join(_LOGDIR, "tmp")
        try:
            os.makedirs(tmp, exist_ok=True)
        except OSError:
            pass
        env = dict(os.environ)
        for k in ("TMP", "TEMP", "TMPDIR", "SQLITE_TMPDIR"):
            env[k] = tmp
        return env

    def spawn(self, which: str) -> subprocess.Popen:
        env = self._env()
        if which == "backend":
            p = subprocess.Popen(backend_cmd(self.workspace_root), cwd=ROOT,
                                 stdout=self.backend_log, stderr=self.backend_log,
                                 env=env)
        else:
            p = subprocess.Popen(adapter_cmd(self.workspace_root), cwd=ROOT,
                                 stdout=self.adapter_log, stderr=self.adapter_log,
                                 env=env)
        self.procs[which] = p
        return p

    def wait_ready(self, which: str, proc: subprocess.Popen, timeout: float) -> bool:
        url = (f"http://127.0.0.1:{BACKEND_PORT}/health" if which == "backend"
               else f"http://127.0.0.1:{ADAPTER_PORT}/global/health")
        # 传 stop：shutdown() 之后在途的等待要能被打断（见 wait_up 的说明）
        return wait_up(url, timeout, proc, self.stop_event)

    # -- 一轮检查
    def check_once(self) -> None:
        for which in ("backend", "adapter"):
            proc = self.procs.get(which)
            if proc is None:
                continue
            if proc.poll() is None:
                # 进程还活着 → 计数复位。原实现只在"看门狗自己拉起且健康检查成功"
                # 才清零 ✗ —— 外部把服务拉回来之后计数残留，退避态被永久化、
                # 每分钟误报"连续失败"（audit2 LOW ✓）。
                self.fails[which] = 0
                continue
            if self.stop_event.is_set():
                return
            code = proc.returncode
            self.fails[which] += 1
            self.restarts[which] += 1
            log(f"「看门狗」{which} 已退出（code={code}），第 {self.restarts[which]} 次拉起…")
            try:
                if self.stop_event.is_set():
                    return
                newp = self.spawn(which)
                ok = self.wait_ready(which, newp, 90 if which == "backend" else 30)
                if ok:
                    log(f"「看门狗」{which} 已恢复 ✓（累计重启 {self.restarts[which]} 次）")
                    self.fails[which] = 0
                else:
                    log(f"「看门狗」{which} 拉起后仍不可用 ✗"
                        f"（连续第 {self.fails[which]} 次）—— 详见 {_LOGDIR}\\"
                        f"{'backend' if which == 'backend' else 'adapter'}.log")
            except Exception as e:                         # noqa: BLE001
                log(f"「看门狗」拉起 {which} 失败: {type(e).__name__}: {e}")

    def run(self) -> None:
        while not self.stop_event.wait(WATCH_INTERVAL):
            self.check_once()
            # 连续挂 → 退避，别把日志刷爆（端口被占/依赖缺失时重启一百次也没用 ✓）
            if max(self.fails.values()) >= WATCH_BACKOFF_AFTER:
                log(f"「看门狗」连续失败 {self.fails}，退避 {WATCH_BACKOFF_INTERVAL:.0f} 秒")
                if self.stop_event.wait(WATCH_BACKOFF_INTERVAL):
                    return

    def shutdown(self) -> None:
        # 顺序很重要：**先置位**（让在途的 wait_ready 立刻让出 ✓）再回收进程 ✗
        self.stop_event.set()
        for which, p in list(self.procs.items()):
            try:
                p.terminate()
            except Exception:                                 # noqa: BLE001
                pass
            # 【只 terminate 不 wait 是不够的】子进程可能还没退、端口还占着，
            # 下一次启动会直接"端口被占" ✗（用户看到的就是"起不来"却查不出原因）。
            # 等一会儿，还没退就 kill 兜底；回收不掉要留痕，不许静默 ✓
            try:
                p.wait(timeout=8)
            except Exception:                                 # noqa: BLE001
                try:
                    p.kill()
                    p.wait(timeout=4)
                except Exception:                             # noqa: BLE001
                    log(f"「看门狗」{which} 未能回收（pid={p.pid}），可能残留")


def _frontend_crashed(logdir: str) -> bool:
    """前端是不是**崩**了（而不是用户正常退出）✗ —— 读 frontend.log 尾部找 Bun 的崩溃签名。

    【为什么值得专门判】本机已积累 17 份崩溃报告，全在 **opentui.dll** 原生层
    （`panic(main thread): Segmentation fault` …）—— 那是上游 bug，我们治不了 ✗。
    但"崩了还静默把整套收掉、控制台停在崩溃前最后一帧"是**我们的锅** ✗✗：
    用户只会盯着一块冻结的黑屏等，永远不知道**该重开一次**。让失败出声是底线 ✓。
    """
    try:
        with open(os.path.join(logdir, "frontend.log"), "r",
                  encoding="utf-8", errors="replace") as f:
            tail = f.read()[-8000:]
        return "Bun has crashed" in tail or "Segmentation fault" in tail
    except OSError:
        return False


def main() -> int:
    # 日志目录：后端的 stdout **不能留给控制台** —— 它会直接盖在 TUI 上
    # （实测：`[会话] 保存会话元数据失败…` 那几行糊在输入框上）。
    logdir = _LOGDIR
    os.makedirs(logdir, exist_ok=True)
    backend_log = open(os.path.join(logdir, "backend.log"), "a",
                       encoding="utf-8", errors="replace")

    # 持久化根：`.lioncode`（会话元数据 / 对话历史）就落在这里。
    # 后端与适配层**必须用同一个值** —— 适配层要靠它找到对话文件来回放历史，
    # 否则只能靠候选搜索兜底。这里算一次、两边共用，避免以后改单边漂移。
    # 数据根必须用 `_LOGDIR`（它会回退到可写位置）✗ 不能写死 ROOT/.lbcheck
    workspace_root = os.path.join(_LOGDIR, "workspace")

    wd = Watchdog(workspace_root,
                  backend_log,
                  open(os.path.join(logdir, "adapter.log"), "a",
                       encoding="utf-8", errors="replace"))

    # ① 后端
    print(f"[1/3] 启动 Lion Code 后端 :{BACKEND_PORT} …", flush=True)
    backend = wd.spawn("backend")
    if not wd.wait_ready("backend", backend, 90):
        print("后端没起来，退出。", flush=True)
        backend.terminate()
        return 1
    print("      后端就绪", flush=True)

    # ② 适配层
    print(f"[2/3] 启动 MiMo 兼容接口层 :{ADAPTER_PORT} …", flush=True)
    adapter = wd.spawn("adapter")
    if not wd.wait_ready("adapter", adapter, 30):
        print("适配层没起来，退出。", flush=True)
        backend.terminate()
        adapter.terminate()
        return 1
    print("      适配层就绪", flush=True)

    # 看门狗开工（前端起来之前就开，覆盖"刚起来那会儿崩掉"这种情况 ✓）
    wd.start()
    log(f"「看门狗」已启动：每 {WATCH_INTERVAL:.0f} 秒检查一次，只看后端与适配层")

    # ③ MiMo 前端
    # 【打包版必须优先用同目录的 bun.exe】安装后的机器上**没有全局 bun**
    # （`%APPDATA%\npm\bun.cmd` 和 PATH 上的 `bun` 都可能没有），而第三段 TUI
    # 非 bun 起不来（OpenTUI 走 Bun 原生 FFI，Node 上直接报
    # "OpenTUI native FFI is not available"）。查找顺序：
    #   ① 同目录 bun.exe（安装包自带，82 MB，随 start.exe 一起装）
    #   ② %APPDATA%\npm\bun.cmd（开发机的全局安装，保持原有行为）
    #   ③ PATH 上的 bun（最后兜底）
    bun = "bun"
    for _cand in (os.path.join(ROOT, "bun.exe"),
                  os.path.join(os.environ.get("APPDATA", ""), "npm", "bun.cmd")):
        if _cand and os.path.isfile(_cand):
            bun = _cand
            break
    print(f"[3/3] 拉起 Lion Code 终端界面（tui/ → 后端 :{BACKEND_PORT}）…", flush=True)
    # 【为什么不再 attach MiMo】MiMo 前端与它的补丁机制已整体移除；界面换成仓库自带的
    # `tui/`（OpenTUI + SolidJS，同一渲染栈，但**只做界面**、直连后端 HTTP —— 不再需要
    # 8791 适配层参与这条链）。启动约定沿用 main.py 的 `_ink_frontend_cmd`：
    #   cwd 必须切到 tui/（Bun 按 cwd 找 bunfig.toml 的 preload，否则 JSX runtime 报错）
    #   --conditions=browser 少它会在依赖解析上翻车
    #   --port <后端端口>（tui/src/index.tsx: PORT = Number(arg("port","8080"))）
    tui_app = os.path.join(ROOT, "tui", "src", "index.tsx")
    rc = 1
    frontend_log = None
    if not os.path.isfile(tui_app):
        bar = "=" * 62
        print(bar, flush=True)
        print("✗ 找不到界面入口: " + tui_app, flush=True)
        print("  安装包没带 tui/ 前端源码（打包 staging 漏了）", flush=True)
        print(bar, flush=True)
        rc = 127
    else:
        print(f"      {bun} run --conditions=browser src/index.tsx --port {BACKEND_PORT}", flush=True)
        # 【只重定向 stderr】TUI 必须拿到真终端（stdout 不能动），但它的报错走
        # console.error = stderr，而 TUI 占屏后错误看不见 ⇒ 落到文件里才能查。
        # 【三步都可能抛，抛了也要走下面的统一收尾】—— wd.start() 之后没有 try/finally，
        # 中途抛异常会让 backend/adapter 无人 terminate（下次启动"端口被占"）。
        try:
            os.makedirs(_LOGDIR, exist_ok=True)
            tmp = os.path.join(logdir, "tmp")
            os.makedirs(tmp, exist_ok=True)
            frontend_log = open(os.path.join(logdir, "frontend.log"), "a",
                                encoding="utf-8", errors="replace")
            env = dict(os.environ)
            for k in ("TMP", "TEMP", "TMPDIR", "SQLITE_TMPDIR"):
                env[k] = tmp
            rc = 0
        except OSError as e:
            print(f"✗ 建临时目录 / 前端日志失败: {type(e).__name__}: {e}", flush=True)
        if frontend_log is not None and rc == 0:
            try:
                # cwd 必须是 tui/：Bun 按 cwd 找 bunfig.toml 的 preload（JSX runtime）
                rc = subprocess.call(
                    [bun, "run", "--conditions=browser", "src/index.tsx",
                     "--port", str(BACKEND_PORT)],
                    cwd=os.path.join(ROOT, "tui"),
                    stderr=frontend_log, env=env)
            except FileNotFoundError as e:
                print(f"✗ 找不到可执行文件: {getattr(e, 'filename', e)}", flush=True)
                print("  · bun 缺失 → npm install -g bun（或把 bun.exe 放进安装目录）", flush=True)
                print("  · 报的是 src/index.tsx → 安装包没带 tui/ 源码", flush=True)
                rc = 127
            except Exception as e:                             # noqa: BLE001
                print(f"✗ 界面启动失败: {type(e).__name__}: {e}", flush=True)
                rc = 1
    print(f"界面已退出（{rc}），收尾。", flush=True)
    # 【崩溃必须出声】TUI 崩掉时控制台会停在**崩溃前最后一帧**（用户看到的就是一块
    # 冻结的黑屏 ✗✗）—— 而收尾一跑，后端/适配层也一起没了，看起来像"整套死掉"。
    # opentui.dll 段错误是上游 bug（本机 17 份报告），治不了 ✗；但"静默"是我们的锅 ✓。
    if rc != 0 and _frontend_crashed(logdir):
        bar = "=" * 62
        print(bar, flush=True)
        print("✗ 界面进程崩溃了（不是你的操作有问题）", flush=True)
        print("  症状: OpenTUI 原生库段错误（opentui.dll）—— 上游渲染层 bug", flush=True)
        print("  处理: 直接重新打开本程序即可 ✓ 数据没有损坏", flush=True)
        print(f"  日志: {os.path.join(logdir, 'frontend.log')}", flush=True)
        print(bar, flush=True)
    # 【收尾顺序】先停看门狗 ✗ —— 否则收尾期间它会把刚 terminate 的服务又拉起来 ✓
    log("「看门狗」停止（前端已退出）")
    wd.shutdown()
    # join 的超时要盖过 shutdown 里的等待（terminate→wait(8s)→kill→wait(4s) ≈ 12s）✗
    # 原来只给 5 秒，看门狗线程还在 check_once 里就被丢下了 → 在途拉起的进程无人回收 ✗
    wd.join(timeout=20)
    if wd.is_alive():
        log("「看门狗」线程 20 秒后仍未退出（可能卡在健康检查），已放弃等待")
    # 【必须复位控制台】OpenTUI 的界面会打开鼠标上报/备用屏等模式，退出时**不还原**。
    # 不还原的话，之后这个窗口会把鼠标事件当普通文字打出来，满屏
    # `^[[<35;96;43M` 这种（实测就是这么被看到的）。
    # 关鼠标上报(1000/1002/1003/1006) + 退备用屏(1049) + 显示光标(25)
    try:
        sys.stdout.write("\x1b[?1000l\x1b[?1002l\x1b[?1003l\x1b[?1006l"
                         "\x1b[?1049l\x1b[?25h")
        sys.stdout.flush()
    except Exception:                                     # noqa: BLE001
        pass
    print("（已复位终端模式；这个窗口现在可以正常用了）", flush=True)
    log(f"收尾完成（本次累计重启：后端 {wd.restarts['backend']} 次 / "
        f"适配层 {wd.restarts['adapter']} 次）")
    # 【必须把前端退出码透传出去】原来这里恒 `return 0` ✗ ——
    # 前端崩掉（attach 到已死的适配层、yargs 报错、TUI 异常）时 rc≠0，但外层
    # `_run_mimo.cmd` 用 `%errorlevel%` 显示的永远是 "-- exited, code 0 --"。
    # 这正是本项目反复抓的"失败仍报成功" ✓ —— 滚动缓冲里那行"前端已退出（1）"
    # 与外层显示的 0 互相矛盾，查问题的人会被带偏。
    return 0 if rc == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())