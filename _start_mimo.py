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

BACKEND_PORT = int(os.environ.get("LION_CODE_BACKEND_PORT", "18080"))
ADAPTER_PORT = int(os.environ.get("LION_CODE_ADAPTER_PORT", "8791"))

#: 看门狗节奏：12 秒一轮（够快，又不至于抖）。连挂多次后退避到 60 秒 ——
#: 端口被占、依赖缺失这类问题重启一百次也没用，退避能避免把日志刷爆。
WATCH_INTERVAL = 12.0
WATCH_BACKOFF_AFTER = 3          # 连续挂几次开始退避
WATCH_BACKOFF_INTERVAL = 60.0

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

_LOGDIR = os.path.join(ROOT, ".lbcheck")


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


def wait_up(url: str, timeout: float = 60.0, proc=None) -> bool:
    end = time.time() + timeout
    while time.time() < end:
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
    return [PY, os.path.join(ROOT, "main.py"), "--backend-only",
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
            "--config-dir=" + os.path.join(ROOT, ".lbcheck", "mimo")]


def adapter_cmd(workspace_root: str) -> list[str]:
    return [PY, os.path.join(ROOT, "mimo适配.py"), f"--port={ADAPTER_PORT}",
            f"--backend=http://127.0.0.1:{BACKEND_PORT}",
            f"--directory={os.getcwd()}",
            # 【必须和后端同一个值】适配层要用它去 <root>/.lioncode/conversations/
            # 读历史，侧边栏切换会话时才能回放出对话内容。
            f"--workspace={workspace_root}"]


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
    def spawn(self, which: str) -> subprocess.Popen:
        if which == "backend":
            p = subprocess.Popen(backend_cmd(self.workspace_root), cwd=ROOT,
                                 stdout=self.backend_log, stderr=self.backend_log)
        else:
            p = subprocess.Popen(adapter_cmd(self.workspace_root), cwd=ROOT,
                                 stdout=self.adapter_log, stderr=self.adapter_log)
        self.procs[which] = p
        return p

    def wait_ready(self, which: str, proc: subprocess.Popen, timeout: float) -> bool:
        url = (f"http://127.0.0.1:{BACKEND_PORT}/health" if which == "backend"
               else f"http://127.0.0.1:{ADAPTER_PORT}/global/health")
        return wait_up(url, timeout, proc)

    # -- 一轮检查
    def check_once(self) -> None:
        for which in ("backend", "adapter"):
            proc = self.procs.get(which)
            if proc is None or proc.poll() is None:
                continue
            code = proc.returncode
            self.fails[which] += 1
            self.restarts[which] += 1
            log(f"「看门狗」{which} 已退出（code={code}），第 {self.restarts[which]} 次拉起…")
            try:
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
        self.stop_event.set()
        for p in self.procs.values():
            try:
                p.terminate()
            except Exception:                                 # noqa: BLE001
                pass


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
    workspace_root = os.path.join(ROOT, ".lbcheck", "workspace")

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
    bun = os.path.join(os.environ.get("APPDATA", ""), "npm", "bun.cmd")
    if not os.path.isfile(bun):
        bun = "bun"
    print("[3/3] 拉起 MiMo 原版前端（attach 到适配层）…", flush=True)
    # 适配层启动时会预建一个会话并把 id 写在这里。带上 --session 就跳过 MiMo
    # 那两步"选工作区 / 选会话"的选择界面，直接进聊天。
    extra: list[str] = []
    try:
        p = os.path.join(ROOT, ".lbcheck", "mimo_session.txt")
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
    frontend_log = open(os.path.join(logdir, "frontend.log"), "a",
                        encoding="utf-8", errors="replace")
    # 【必须搬 home】MiMo 默认把状态放在 `~/.local/share/mimocode`（xdgData）等
    # 四处，SQLite 库 `mimocode.db` 就在那儿。那个位置在沙箱里**不可写**：
    #   PRAGMA wal_checkpoint(PASSIVE) → "attempt to write a readonly database"
    #   → db.ts:97 抛错 → 插件运行时 load() 失败 → 所有内置侧栏插件从未激活
    #     （runtime 的 fail() 只 console.error，TUI 占屏所以完全看不见）
    # 注意 DACL 本身没问题（用户是 (OI)(CI)(F)、无 Deny）——是进程令牌被限制在
    # 工作区内，所以正确解法是把状态搬进能写的地方，而不是去改权限。
    # MIMOCODE_HOME 是官方开关（flag.ts:458 / shared/global.ts:26）：设了就把它
    # 当 home，data/cache/config/state 四个目录都落在它下面。
    mimo_home = os.path.join(ROOT, ".lbcheck", "mimo-home")
    os.makedirs(mimo_home, exist_ok=True)
    # 【临时目录也得搬】SQLite 建 FTS5 虚拟表、跑迁移 DDL、checkpoint 都要写临时
    # 文件，默认落在 %TEMP%（工作区外 → 沙箱里不可写），报的是
    #   SQLiteError: unable to open database file
    # 这个错误藏在 DrizzleError 的 `cause` 里（前端日志只显示外层 ✗），
    # 最初那条 `wal_checkpoint(PASSIVE)` 报 readonly 也是同一个原因。
    tmp = os.path.join(logdir, "tmp")
    os.makedirs(tmp, exist_ok=True)
    env = dict(os.environ)
    env["MIMOCODE_HOME"] = mimo_home
    for k in ("TMP", "TEMP", "TMPDIR", "SQLITE_TMPDIR"):
        env[k] = tmp
    print(f"      MiMo home → {mimo_home}", flush=True)
    print(f"      临时目录  → {tmp}", flush=True)
    rc = subprocess.call(
        [bun, "run", "--conditions=browser", "./src/index.ts",
         "attach", f"http://127.0.0.1:{ADAPTER_PORT}", "--dir", os.getcwd(), *extra],
        cwd=MIMO_CLI, stderr=frontend_log, env=env)
    print(f"前端已退出（{rc}），收尾。", flush=True)
    # 【收尾顺序】先停看门狗 ✗ —— 否则收尾期间它会把刚 terminate 的服务又拉起来 ✓
    log("「看门狗」停止（前端已退出）")
    wd.shutdown()
    wd.join(timeout=5)
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())