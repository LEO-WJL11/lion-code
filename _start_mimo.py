# -*- coding: utf-8 -*-
r"""一键启动：Lion Code 后端 + MiMo 兼容接口层 + MiMo 原版前端。

三段式（顺序不能反）：

    ① main.py --backend-only        我们的 Python 后端（能力都在这）
    ② mimo适配.py                   把 MiMo 的 139 个端点形状翻译到 ①
    ③ MiMo 前端 attach 到 ②         MiMo 的 TUI 一行不改，直接挂上去

【为什么用 attach】MiMo 的 TUI 只是个客户端（`packages/cli/src/cli/cmd/tui/`），
它的 `attach <url>` 子命令专门用来挂到任意服务端上 —— 这就是"改接口"的入口。
不 attach 的话它会自己去起它自己那套服务端，那就是 MiMo 的后端，不是我们的。
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.isfile(PY):
    PY = sys.executable
MIMO_CLI = os.path.join(ROOT, "MiMo-Code-main", "packages", "cli")

BACKEND_PORT = int(os.environ.get("LION_CODE_BACKEND_PORT", "18080"))
ADAPTER_PORT = int(os.environ.get("LION_CODE_ADAPTER_PORT", "8791"))

sys.stdout.reconfigure(encoding="utf-8", errors="replace")


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


def main() -> int:
    # ① 后端
    print(f"[1/3] 启动 Lion Code 后端 :{BACKEND_PORT} …", flush=True)
    backend = subprocess.Popen(
        [PY, os.path.join(ROOT, "main.py"), "--backend-only",
         f"--server.port={BACKEND_PORT}",
         # 【--app-root 不能少】它决定去哪找 `runtime-vulkan/llama-server.exe`
         # 和 `*.gguf`。不给的话默认是 <仓库>\python（老布局），模型会被判为
         # "未安装"从而触发重新下载，本地模型永远起不来。
         f"--app-root={ROOT}",
         "--config-dir=" + os.path.join(ROOT, ".lbcheck", "mimo")],
        cwd=ROOT)
    if not wait_up(f"http://127.0.0.1:{BACKEND_PORT}/health", 90, backend):
        print("后端没起来，退出。", flush=True)
        backend.terminate()
        return 1
    print("      后端就绪", flush=True)

    # ② 适配层
    print(f"[2/3] 启动 MiMo 兼容接口层 :{ADAPTER_PORT} …", flush=True)
    adapter = subprocess.Popen(
        [PY, os.path.join(ROOT, "mimo适配.py"), f"--port={ADAPTER_PORT}",
         f"--backend=http://127.0.0.1:{BACKEND_PORT}",
         f"--directory={os.getcwd()}"], cwd=ROOT)
    if not wait_up(f"http://127.0.0.1:{ADAPTER_PORT}/global/health", 30, adapter):
        print("适配层没起来，退出。", flush=True)
        backend.terminate()
        adapter.terminate()
        return 1
    print("      适配层就绪", flush=True)

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
    rc = subprocess.call(
        [bun, "run", "--conditions=browser", "./src/index.ts",
         "attach", f"http://127.0.0.1:{ADAPTER_PORT}", "--dir", os.getcwd(), *extra],
        cwd=MIMO_CLI)
    print(f"前端已退出（{rc}），收尾。", flush=True)
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
    for p in (adapter, backend):
        try:
            p.terminate()
        except Exception:                                 # noqa: BLE001
            pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())