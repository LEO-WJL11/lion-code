# -*- coding: utf-8 -*-
r"""一键启动：Lion Code 后端 + MiMo 兼容接口层 + MiMo 原版前端。

三段式（顺序不能反）：

    ① main.py --backend-only        我们的 Python 后端（能力都在这）
    ② mimo适配.py                   把 MiMo 的 139 个端点形状翻译到 ①
    ③ MiMo 前端 attach 到 ②         MiMo 的 TUI 一行不改，直接挂上去

【为什么用 attach】MiMo 的 TUI 只是个客户端（`packages/cli/src/cli/cmd/tui/`），
它的 `attach <url>` 子命令专门用来挂到任意服务端上 —— 这就是"改接口"的入口。
不 attach 的话它会自己去起它自己那套服务端，那就是 MiMo 的后端，不是我们的。

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
MIMO_CLI = os.path.join(ROOT, "MiMo-Code-main", "packages", "cli")

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
    print("[3/3] 拉起 MiMo 原版前端（attach 到适配层）…", flush=True)
    # 适配层启动时会预建一个会话并把 id 写在这里。带上 --session 就跳过 MiMo
    # 那两步"选工作区 / 选会话"的选择界面，直接进聊天。
    extra: list[str] = []
    try:
        p = os.path.join(_LOGDIR, "mimo_session.txt")
        with open(p, encoding="utf-8") as f:
            sid = f.read().strip()
        if sid:
            extra = ["--session", sid]
            print(f"      直接进入预建会话 {sid}", flush=True)
    except Exception:                                     # noqa: BLE001
        pass
    print(f"      {bun} run --conditions=browser ./src/index.ts "
          f"attach http://127.0.0.1:{ADAPTER_PORT} {' '.join(extra)}", flush=True)
    # 【只重定向 stderr】TUI 必须拿到真终端（stdout 不能动），但它的报错走
    # console.error = stderr，而 TUI 会把屏幕糊掉、错误看不见。
    # 插件加载失败就是这样被吞掉的：runtime 的 fail() 只 console.error 不抛异常，
    # 表现成"侧栏插件一个都不渲染"，却查不到任何原因。落到文件里就能看了。
    # （打开这个文件的动作放在下面的 try 里 ✗ —— 放在外面抛了就没人收尾，见 audit2。）
    # 【必须搬 home】MiMo 默认把状态放在 `~/.local/share/mimocode`（xdgData）等
    # 四处，SQLite 库 `mimocode.db` 就在那儿。那个位置在沙箱里**不可写**：
    #   PRAGMA wal_checkpoint(PASSIVE) → "attempt to write a readonly database"
    #   → db.ts:97 抛错 → 插件运行时 load() 失败 → 所有内置侧栏插件从未激活
    #     （runtime 的 fail() 只 console.error，TUI 占屏所以完全看不见）
    # 注意 DACL 本身没问题（用户是 (OI)(CI)(F)、无 Deny）——是进程令牌被限制在
    # 工作区内，所以正确解法是把状态搬进能写的地方，而不是去改权限。
    # MIMOCODE_HOME 是官方开关（flag.ts:458 / shared/global.ts:26）：设了就把它
    # 当 home，data/cache/config/state 四个目录都落在它下面。
    mimo_home = os.path.join(_LOGDIR, "mimo-home")
    # 【临时目录也得搬】SQLite 建 FTS5 虚拟表、跑迁移 DDL、checkpoint 都要写临时
    # 文件，默认落在 %TEMP%（工作区外 → 沙箱里不可写），报的是
    #   SQLiteError: unable to open database file
    # 这个错误藏在 DrizzleError 的 `cause` 里（前端日志只显示外层 ✗），
    # 最初那条 `wal_checkpoint(PASSIVE)` 报 readonly 也是同一个原因。
    # ⚠ `os.makedirs` 统一放到下面的 try 里 —— 放在外面抛了就没人收尾（audit2 ✗）。
    tmp = os.path.join(logdir, "tmp")
    env = dict(os.environ)
    env["MIMOCODE_HOME"] = mimo_home
    for k in ("TMP", "TEMP", "TMPDIR", "SQLITE_TMPDIR"):
        env[k] = tmp
    # 【这三步都可能抛，抛了就没人收尾】wd.start() 之后没有 try/finally ✗ ——
    # 一旦中途抛异常（bun/MiMo CLI 不存在、mimo-home 建不出来、frontend.log 打不开），
    # backend/adapter 就**无人 terminate** ✗，下一次启动必然"端口被占"。
    # 所以每一处都接住并让 rc≠0，落到下面统一的收尾流程 ✓。
    rc = 1
    try:
        os.makedirs(mimo_home, exist_ok=True)
        os.makedirs(tmp, exist_ok=True)
        frontend_log = open(os.path.join(logdir, "frontend.log"), "a",
                            encoding="utf-8", errors="replace")
    except OSError as e:
        print(f"✗ 建 MiMo home / 临时目录 / 前端日志失败: {type(e).__name__}: {e}", flush=True)
        frontend_log = None
        rc = 1
    print(f"      MiMo home → {mimo_home}", flush=True)
    print(f"      临时目录  → {tmp}", flush=True)

    if frontend_log is not None and rc == 0:
        try:
            rc = subprocess.call(
                [bun, "run", "--conditions=browser", "./src/index.ts",
                 "attach", f"http://127.0.0.1:{ADAPTER_PORT}", "--dir",
                 os.getcwd(), *extra],
                cwd=MIMO_CLI, stderr=frontend_log, env=env)
        except FileNotFoundError as e:
            # bun 没装 / MiMo 前端目录缺失 —— 这是打包后最常见的失败 ✗
            print(f"✗ 找不到可执行文件: {getattr(e, 'filename', e)}", flush=True)
            print("  · bun 缺失 → npm install -g bun（或把 bun.exe 放进安装目录）", flush=True)
            print("  · 报的是 src/index.ts → 安装包没带 MiMo 前端源码", flush=True)
            rc = 127
        except Exception as e:                             # noqa: BLE001
            print(f"✗ 前端启动失败: {type(e).__name__}: {e}", flush=True)
            rc = 1
    print(f"前端已退出（{rc}），收尾。", flush=True)
    # 【收尾顺序】先停看门狗 ✗ —— 否则收尾期间它会把刚 terminate 的服务又拉起来 ✓
    log("「看门狗」停止（前端已退出）")
    wd.shutdown()
    # join 的超时要盖过 shutdown 里的等待（terminate→wait(8s)→kill→wait(4s) ≈ 12s）✗
    # 原来只给 5 秒，看门狗线程还在 check_once 里就被丢下了 → 在途拉起的进程无人回收 ✗
    wd.join(timeout=20)
    if wd.is_alive():
        log("「看门狗」线程 20 秒后仍未退出（可能卡在健康检查），已放弃等待")
    # 【必须复位控制台】MiMo 的 TUI 会打开鼠标上报/备用屏等模式，退出时**不还原**。
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