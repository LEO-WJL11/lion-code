# -*- coding: utf-8 -*-
r"""真模型验证：提示词接线后，模型还会不会写 Unix 命令。

改造前的证据（用户实测贴出来的）：
    which node npm python3 ollama 2>&1; node --version 2>&1; python3 --version 2>&1
    ↑ which 不存在   ↑ python3 不存在   ↑ ; 串了 4 条不相关命令

判据：新提示词下，模型为"这台机器装了 git 吗"发出的命令应当
  · 用 where（不是 which）
  · 用 python（如果用到）
  · 不把多条不相关命令用 ; 串成一条
  · 不假设 ollama/rg 这类没装的东西
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\Leo\Desktop\lion-code"
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
PORT = 18085


def call(url, body=None, method="GET", timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=data, method=method,
                               headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(r, timeout=timeout) as resp:
            t = resp.read().decode("utf-8", "replace")
            return resp.status, json.loads(t or "null")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")
    except Exception as e:                                # noqa: BLE001
        return 0, f"{type(e).__name__}: {e}"


def wait(url, secs=90):
    for _ in range(secs * 2):
        try:
            with urllib.request.urlopen(url, timeout=2):
                return True
        except Exception:                                 # noqa: BLE001
            time.sleep(0.5)
    return False


def main() -> int:
    env = dict(os.environ, PYTHONIOENCODING="utf-8",
               TMP=os.path.join(ROOT, ".lbcheck", "tmp"),
               TEMP=os.path.join(ROOT, ".lbcheck", "tmp"),
               TMPDIR=os.path.join(ROOT, ".lbcheck", "tmp"))
    blog = open(os.path.join(ROOT, ".lbcheck", "prompttest.log"), "w", encoding="utf-8")
    be = subprocess.Popen([PY, os.path.join(ROOT, "main.py"), "--backend-only",
                           f"--server.port={PORT}", f"--app-root={ROOT}",
                           f"--lion.workspace.default-path={os.path.join(ROOT, '.lbcheck', 'pt-ws')}",
                           f"--config-dir={os.path.join(ROOT, '.lbcheck', 'pt-cfg')}"],
                          cwd=ROOT, env=env, stdout=blog, stderr=blog)
    if not wait(f"http://127.0.0.1:{PORT}/health"):
        print("✗ 后端没起来"); be.terminate(); return 1
    st, s = call(f"http://127.0.0.1:{PORT}/api/runtime/local")
    phase = (s.get("data") or {}).get("phase") if isinstance(s, dict) else None
    if phase != "ready":
        call(f"http://127.0.0.1:{PORT}/api/runtime/local/start", {}, "POST")
        for _ in range(90):
            st, s = call(f"http://127.0.0.1:{PORT}/api/runtime/local")
            phase = (s.get("data") or {}).get("phase") if isinstance(s, dict) else None
            if phase == "ready":
                break
            time.sleep(2)
    print(f"模型 phase={phase}")

    st, ws = call(f"http://127.0.0.1:{PORT}/api/workspaces", {"path": ROOT}, "POST")
    wsid = (ws.get("data") or {}).get("id") if isinstance(ws, dict) else None
    st, se = call(f"http://127.0.0.1:{PORT}/api/sessions",
                  {"workspaceId": wsid, "mode": "STANDARD"}, "POST")
    sid = (se.get("data") or {}).get("sessionId") or (se.get("data") or {}).get("id")

    for q in ["这台机器装了 git 吗？什么版本？", "python 是哪个版本？"]:
        print("\n" + "=" * 68)
        print("提问:", q)
        body = json.dumps({"sessionId": sid, "message": q}).encode()
        req = urllib.request.Request(f"http://127.0.0.1:{PORT}/api/chat/stream", data=body,
                                     method="POST", headers={"Content-Type": "application/json"})
        text, tools = "", []
        try:
            with urllib.request.urlopen(req, timeout=420) as resp:
                for raw in resp:
                    line = raw.decode("utf-8", "replace").strip()
                    if not line.startswith("data:"):
                        continue
                    try:
                        f = json.loads(line[5:].strip())
                    except ValueError:
                        continue
                    if f.get("type") == "TEXT":
                        text += str(f.get("content") or "")
                    elif f.get("type") == "TOOL_CALL":
                        tools.append(str(f.get("toolName")))
        except Exception as e:                            # noqa: BLE001
            print("  流中断:", type(e).__name__, e)
        print("  模型输出全文:")
        for ln in text.split("\n"):
            if ln.strip():
                print("    " + ln.strip()[:150])
        print("  执行的工具:", tools)

        cmds = re.findall(r"<parameter=command>(.*?)</parameter>", text, re.S)
        if not cmds:
            cmds = re.findall(r'"command"\s*:\s*"([^"]+)"', text)
        print("  抓到的 command:", cmds)
        bad = [c for c in cmds if re.search(r"\bwhich\b|\bpython3\b", c)]
        print("  " + ("✓ 没有 which / python3" if not bad else "✗ 仍有 Unix 写法: " + str(bad)))

    be.terminate(); time.sleep(1)
    if be.poll() is None:
        be.kill()
    blog.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())