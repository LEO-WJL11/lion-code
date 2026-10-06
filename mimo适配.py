# -*- coding: utf-8 -*-
r"""MiMo 兼容接口层 —— 让 MiMo Code 的原版界面直接跑在 Lion Code 后端上。

【它是什么】
MiMo Code 的前端（OpenTUI + SolidJS，`MiMo-Code-main/packages/cli/src/cli/cmd/tui/`）
是个纯客户端：它只认自己那套 HTTP API（从 `packages/sdk` 的生成代码里可以拿到全表，
139 个端点）。本文件在 Python 侧实现它的接口形状，把请求翻译成 Lion Code 后端
（`main.py` 的 `/api/*`）能听懂的东西。

于是：**MiMo 的前端一行都不用改**，只要用它的 attach 方式挂上来：

    mimo attach http://127.0.0.1:<端口>

【形状从哪抄的】`packages/sdk/src/v2/gen/types.gen.ts`（154 KB 生成类型）
  · Project          {id, worktree, vcs?, time:{created,updated}, sandboxes[]}
  · Session          {id, slug, projectID, directory, title, titleSource, titleRevision, version, time}
  · UserMessage      {id, sessionID, role:"user", time:{created}, agent, model:{providerID,modelID}}
  · AssistantMessage {id, sessionID, role:"assistant", parentID, modelID, providerID, mode, agent, time}
  · TextPart         {id, sessionID, messageID, type:"text", text, time:{start,end?}}
  · GlobalEvent      {directory, project?, workspace?, payload: {type, properties}}
  事件名（77 个里挑我们要的）：
    server.connected / session.created / session.updated / session.idle /
    message.updated / message.part.updated / message.part.delta / session.error

【跟 Lion Code 后端的对接】
  聊天走 `POST /api/chat/stream`（SSE，帧形状 {type, content, toolName, finished}），
  type 取 TEXT / TOOL_CALL / DONE / ERROR。会话用后端的 `/api/sessions`。
"""
from __future__ import annotations

import json
import os
import queue
import re
import sys
import threading
import time
import urllib.error
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VERSION = "1.5.46"
AGENT = "build"
PROVIDER_ID = "lionbox"
MODEL_ID = "lion-merged"

# ─────────────────────────────────────────── 后端地址（Lion Code 的 /api/*）
BACKEND = os.environ.get("LION_CODE_BACKEND", "http://127.0.0.1:8080").rstrip("/")


def _req(path: str, body: dict | None = None, timeout: float = 30.0):
    """调 Lion Code 后端。失败返回 None（调用方兜住）。"""
    url = BACKEND + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url, data=data, method="POST" if body is not None else "GET",
        headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read().decode("utf-8", "replace")
            return json.loads(raw) if raw.strip() else {}
    except Exception:                                     # noqa: BLE001
        return None


# ─────────────────────────────────────────── 内存状态
_LOCK = threading.RLock()
_SESSIONS: dict[str, dict] = {}          # id → Session
_MESSAGES: dict[str, list] = {}          # sessionID → [Message]
_PARTS: dict[str, list] = {}             # messageID → [Part]
_TOOLS: dict[str, dict] = {}             # 会话 → 工具（给 /session/{id}/task 之类兜底）
_SUBS: list[queue.Queue] = []            # SSE 订阅者
_WORKSPACES: list[dict] = []             # 工作区（/workspace 新建的）
_DIRECTORY = os.getcwd()
_PROJECT_ID = None


def now_ms() -> int:
    return int(time.time() * 1000)


def _slug(n: int = 8) -> str:
    return uuid.uuid4().hex[:n]


def broadcast(payload: dict) -> None:
    """把事件推给所有订阅者（GlobalEvent 外壳在这里补）。"""
    evt = {"directory": _DIRECTORY, "project": _PROJECT_ID, "payload": payload}
    line = "data: " + json.dumps(evt, ensure_ascii=False) + "\n\n"
    with _LOCK:
        subs = list(_SUBS)
    for q in subs:
        try:
            q.put_nowait(line)
        except Exception:                                 # noqa: BLE001
            pass


# ─────────────────────────────────────────── 数据构造
def project() -> dict:
    global _PROJECT_ID
    with _LOCK:
        if _PROJECT_ID is None:
            _PROJECT_ID = "prj_" + _slug(10)
        pid = _PROJECT_ID
    return {"id": pid, "worktree": _DIRECTORY,
            "vcs": "git" if os.path.isdir(os.path.join(_DIRECTORY, ".git")) else None,
            "name": os.path.basename(_DIRECTORY.rstrip("\\/")) or "lion-code",
            "time": {"created": now_ms(), "updated": now_ms()},
            "sandboxes": []}


def new_session(title: str = "新会话", parent: str | None = None) -> dict:
    sid = "ses_" + _slug(12)
    s = {"id": sid, "slug": _slug(6), "projectID": project()["id"],
         "directory": _DIRECTORY, "parentID": parent, "title": title,
         "titleSource": "user", "titleRevision": 1, "version": VERSION,
         "time": {"created": now_ms(), "updated": now_ms()}}
    with _LOCK:
        _SESSIONS[sid] = s
        _MESSAGES[sid] = []
    broadcast({"type": "session.created", "properties": {"info": s}})
    return s


def new_message(sid: str, role: str, parent: str = "", text: str = ""):
    """建一条消息（可选带一个文本 part），并按 MiMo 的事件协议广播出去。"""
    mid = ("msg_" if role == "user" else "msg_") + _slug(12)
    base = {"id": mid, "sessionID": sid, "agentID": AGENT, "role": role,
            "time": {"created": now_ms()}}
    if role == "user":
        base.update({"agent": AGENT,
                     "model": {"providerID": PROVIDER_ID, "modelID": MODEL_ID},
                     "time": {"created": now_ms()}})
    else:
        base.update({"parentID": parent, "modelID": MODEL_ID,
                     "providerID": PROVIDER_ID, "mode": "build", "agent": AGENT,
                     "time": {"created": now_ms()}})
    with _LOCK:
        _MESSAGES.setdefault(sid, []).append(base)
        _PARTS[mid] = []
    broadcast({"type": "message.updated", "properties": {"sessionID": sid, "info": base}})
    if role == "assistant":
        new_part_text(sid, mid, "", start=True)
    return mid


def new_part_text(sid: str, mid: str, text: str, start: bool = False, end: bool = False) -> dict:
    with _LOCK:
        parts = _PARTS.setdefault(mid, [])
        p = next((x for x in parts if x.get("type") == "text"), None)
        if p is None or start:
            p = {"id": "prt_" + _slug(12), "sessionID": sid, "messageID": mid,
                 "type": "text", "text": text, "time": {"start": now_ms()}}
            parts.append(p)
        else:
            p["text"] = p.get("text", "") + text
        if end:
            p.setdefault("time", {})["end"] = now_ms()
    broadcast({"type": "message.part.updated",
               "properties": {"sessionID": sid, "part": p, "time": now_ms()}})
    return p


def _finish_message(sid: str, mid: str) -> None:
    with _LOCK:
        for m in _MESSAGES.get(sid, []):
            if m["id"] == mid:
                m.setdefault("time", {})["completed"] = now_ms()
                broadcast({"type": "message.updated",
                           "properties": {"sessionID": sid, "info": m}})
                break
    for p in _PARTS.get(mid, []):
        if p.get("type") == "text":
            p.setdefault("time", {})["end"] = now_ms()
            broadcast({"type": "message.part.updated",
                       "properties": {"sessionID": sid, "part": p, "time": now_ms()}})


# ─────────────────────────────────────────── 聊天：翻译到 Lion Code 后端
def _stream_backend(sid: str, text: str, mid: str, thinking: str = "HIGH") -> None:
    """把 Lion Code 后端的 SSE 翻译成 MiMo 的 message.part.* 事件。"""
    url = BACKEND + "/api/chat/stream"
    body = json.dumps({"sessionId": sid, "message": text,
                       "thinkingLevel": thinking}).encode("utf-8")
    req = urllib.request.Request(url, data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    acc = ""
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            for raw in r:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if not payload or payload == "[DONE]":
                    continue
                try:
                    f = json.loads(payload)
                except ValueError:
                    continue
                typ = str(f.get("type", "")).upper()
                content = str(f.get("content", ""))
                if typ == "TEXT":
                    acc += content
                    broadcast({"type": "message.part.delta",
                               "properties": {"sessionID": sid, "messageID": mid,
                                              "partID": _text_part_id(mid), "field": "text",
                                              "delta": content, "time": now_ms()}})
                    new_part_text(sid, mid, content)
                elif typ == "TOOL_CALL":
                    tool = str(f.get("toolName") or "tool")
                    broadcast({"type": "message.part.updated",
                               "properties": {"sessionID": sid, "time": now_ms(),
                                              "part": {"id": "prt_" + _slug(12),
                                                       "sessionID": sid, "messageID": mid,
                                                       "type": "tool", "tool": tool,
                                                       "state": {"status": "completed",
                                                                 "input": {}, "output": content,
                                                                 "title": tool}}}})
                elif typ == "ERROR":
                    broadcast({"type": "session.error",
                               "properties": {"sessionID": sid,
                                              "error": {"name": "UnknownError",
                                                        "data": {"message": content}}}})
    except Exception as e:                                # noqa: BLE001
        broadcast({"type": "session.error",
                   "properties": {"sessionID": sid,
                                  "error": {"name": "UnknownError",
                                            "data": {"message": f"{type(e).__name__}: {e}"}}}})
    _finish_message(sid, mid)
    broadcast({"type": "session.idle", "properties": {"sessionID": sid}})


def _text_part_id(mid: str) -> str:
    for p in _PARTS.get(mid, []):
        if p.get("type") == "text":
            return p["id"]
    return ""


def _extract_text(body: dict) -> str:
    parts = body.get("parts") or body.get("message") or []
    if isinstance(parts, str):
        return parts
    if isinstance(parts, dict):
        return str(parts.get("text") or parts.get("content") or "")
    out = []
    for p in parts if isinstance(parts, list) else []:
        if isinstance(p, dict) and p.get("type") in (None, "text"):
            out.append(str(p.get("text") or p.get("content") or ""))
    return "\n".join(x for x in out if x)


# ─────────────────────────────────────────── HTTP
LOG_PATH = os.environ.get("MIMO_ADAPTER_LOG") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), ".lbcheck", "mimo_adapter.log")


class _Server(ThreadingHTTPServer):
    """客户端中途断开（TUI 刷新/退出）是常态，不要刷一屏 traceback。"""

    daemon_threads = True

    def handle_error(self, request, client_address):
        if os.environ.get("MIMO_ADAPTER_DEBUG"):
            super().handle_error(request, client_address)


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):                    # noqa: A003
        # 每个请求都落盘：MiMo 的 TUI 请求到哪一步就退出，只能从这里看
        try:
            with open(LOG_PATH, "a", encoding="utf-8") as f:
                f.write("%s %s\n" % (self.command, self.path))
        except Exception:                                 # noqa: BLE001
            pass

    # -- 工具
    def _json(self, obj, code: int = 200) -> None:
        raw = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _body(self) -> dict:
        n = int(self.headers.get("Content-Length") or 0)
        if not n:
            return {}
        try:
            return json.loads(self.rfile.read(n).decode("utf-8")) or {}
        except Exception:                                 # noqa: BLE001
            return {}

    def _path(self) -> str:
        return self.path.split("?")[0].rstrip("/") or "/"

    # -- GET
    def do_GET(self):                                     # noqa: N802
        p = self._path()
        q = self.path

        if p == "/global/event" or p == "/event":
            return self._sse()

        if p == "/global/health":
            return self._json({"healthy": True, "version": VERSION})
        # 【必须实现】TUI 一启动就问它。opencode 的 Path 形状是
        # {home, state, config, worktree, directory}。之前这里返回 404，
        # 前端拿到 404 就直接退出（退出码 0，看着像"正常结束"）。
        if p == "/path":
            home = os.path.expanduser("~")
            return self._json({"home": home,
                               "state": os.path.join(home, ".local", "share", "lioncode"),
                               "config": os.path.join(home, ".config", "lioncode"),
                               "worktree": _DIRECTORY, "directory": _DIRECTORY})
        if p == "/experimental/resource":
            return self._json({"cpu": 0, "memory": 0, "uptime": 0})
        # 【不能返空数组】TUI 拿到空的工作区列表就会弹"新建工作区"，
        # 于是每次启动都强制你先建一个工作区才能发消息（实测就是这么卡住的）。
        # 结构照 SDK 的 Workspace：{id,type,name,branch,directory,extra,projectID}
        if p == "/experimental/workspace":
            with _LOCK:
                if not _WORKSPACES:
                    _WORKSPACES.append(self._workspace())
                return self._json(list(_WORKSPACES))
        if p == "/experimental/workspace/status":
            return self._json({self._workspace()["id"]: {"status": "ready"}})
        if p == "/experimental/console":
            return self._json({"org": None, "orgs": []})
        if p == "/global/config":
            return self._json({"theme": "mimocode", "model": MODEL_ID})
        if p == "/project/current" or p == "/project":
            return self._json(project())

        if p == "/config":
            return self._json({"model": f"{PROVIDER_ID}/{MODEL_ID}",
                               "theme": "mimocode", "autoupdate": False})
        if p in ("/config/providers", "/provider"):
            return self._json({"providers": [self._provider()], "default": {}})
        if p == "/provider/auth":
            return self._json({})

        if p == "/session":
            with _LOCK:
                return self._json(list(_SESSIONS.values()))
        if p == "/session/status":
            return self._json({})

        m = re.match(r"^/session/([^/]+)$", p)
        if m:
            with _LOCK:
                s = _SESSIONS.get(m.group(1))
            return self._json(s) if s else self._json({"error": "not found"}, 404)

        m = re.match(r"^/session/([^/]+)/message$", p)
        if m:
            with _LOCK:
                msgs = list(_MESSAGES.get(m.group(1), []))
            out = []
            for msg in msgs:
                out.append({"info": msg, "parts": _PARTS.get(msg["id"], [])})
            return self._json(out)

        if re.match(r"^/session/([^/]+)/(todo|children|diff|task|actors|recovery)$", p):
            return self._json([])
        if re.match(r"^/session/([^/]+)/message/([^/]+)$", p):
            mid = p.rsplit("/", 1)[1]
            with _LOCK:
                for msgs in _MESSAGES.values():
                    for msg in msgs:
                        if msg["id"] == mid:
                            return self._json({"info": msg, "parts": _PARTS.get(mid, [])})
            return self._json({"error": "not found"}, 404)

        if p == "/permission":
            return self._json([])
        if p == "/question":
            return self._json([])
        if p in ("/agent", "/agent/"):
            return self._json([{"name": AGENT, "description": "Lion Code 默认智能体",
                                "mode": "primary", "builtIn": True}])
        if p == "/skill":
            r = _req("/api/skills") or {}
            data = r.get("data") if isinstance(r, dict) else None
            items = data if isinstance(data, list) else []
            return self._json([{"name": str(x.get("name") or x.get("id") or x),
                                "description": str(x.get("description") or "")} for x in items])
        if p == "/command":
            return self._json([])
        if p in ("/lsp", "/formatter", "/mcp", "/vcs", "/file/status"):
            return self._json([] if p != "/vcs" else {})
        if p in ("/file", "/find", "/find/symbol"):
            return self._json([])

        return self._json({"error": "not implemented: " + p}, 404)

    def _workspace(self) -> dict:
        """默认工作区（当前目录）。返回它，TUI 就不会再逼你新建工作区。"""
        name = os.path.basename(_DIRECTORY.rstrip("\\/")) or "lion-code"
        return {"id": "wrk_" + _slug(10), "type": "local", "name": name,
                "branch": None, "directory": _DIRECTORY, "extra": None,
                "projectID": project()["id"]}

    def _model_ids(self) -> list:
        """真实可选的模型列表。

        【数据源】试过 `/api/models` —— 它是空的（`data: []`）。有内容的只有
        `/api/runtime/local/models`：三份量化，带中文标签与下载状态。
        云端配了 key 之后，`/api/models` 才会有东西，所以两个都读、合并去重。
        """
        ids = []

        # ① 本地量化（file 是它的标识）
        r = _req("/api/runtime/local/models") or {}
        data = r.get("data") if isinstance(r, dict) else None
        if isinstance(data, list):
            for x in data:
                if isinstance(x, dict):
                    n = x.get("file") or x.get("id") or x.get("name")
                    if n:
                        ids.append(str(n))
                elif isinstance(x, str):
                    ids.append(x)

        # ② 云端 / 其它（配了 key 才有）
        r2 = _req("/api/models") or {}
        d2 = r2.get("data") if isinstance(r2, dict) else None
        pool = []
        if isinstance(d2, dict):
            for key in ("local", "cloud", "models"):
                v = d2.get(key)
                if isinstance(v, list):
                    pool += v
        elif isinstance(d2, list):
            pool = d2
        for x in pool:
            if isinstance(x, dict):
                n = x.get("id") or x.get("name") or x.get("model")
                if n:
                    ids.append(str(n))
            elif isinstance(x, str):
                ids.append(x)

        # ③ 兜底：当前激活的那个
        if not ids:
            m = _req("/api/runtime/mode") or {}
            d = m.get("data") if isinstance(m, dict) else {}
            ids = [str((d or {}).get("model") or MODEL_ID)]

        seen, out = set(), []
        for x in ids:
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def _provider(self) -> dict:
        """/models 面板读的是 providers[].models —— 这里给真实列表，
        否则只能看到一个模型，等于没法切换。"""
        models = {}
        for mid in self._model_ids():
            models[mid] = {"id": mid, "name": mid, "attachment": False,
                           "reasoning": True, "temperature": True,
                           "tool_call": True, "cost": {"input": 0, "output": 0}}
        return {"id": PROVIDER_ID, "name": "Lion Code", "source": "custom",
                "env": [], "options": {}, "models": models}

    # -- SSE：界面"活过来"全靠它
    def _sse(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        q: queue.Queue = queue.Queue()
        with _LOCK:
            _SUBS.append(q)
        try:
            first = {"directory": _DIRECTORY, "project": _PROJECT_ID,
                     "payload": {"type": "server.connected", "properties": {}}}
            self.wfile.write(("data: " + json.dumps(first, ensure_ascii=False) + "\n\n").encode())
            self.wfile.flush()
            while True:
                try:
                    line = q.get(timeout=15)
                except queue.Empty:
                    self.wfile.write(b": ping\n\n")       # 心跳保活
                    self.wfile.flush()
                    continue
                self.wfile.write(line.encode("utf-8"))
                self.wfile.flush()
        except Exception:                                 # noqa: BLE001
            pass
        finally:
            with _LOCK:
                if q in _SUBS:
                    _SUBS.remove(q)

    # -- POST / PATCH / DELETE
    def do_POST(self):                                    # noqa: N802
        p = self._path()
        body = self._body()

        if p == "/session":
            title = str(body.get("title") or "新会话")
            return self._json(new_session(title))

        # 【/workspace 命令】新建工作区：结构照 SDK 的 Workspace
        if p == "/experimental/workspace":
            name = str(body.get("name") or "lion-code")
            directory = str(body.get("directory") or _DIRECTORY)
            ws = {"id": "wrk_" + _slug(10), "type": str(body.get("type") or "local"),
                  "name": name, "branch": body.get("branch"),
                  "directory": directory, "extra": None,
                  "projectID": project()["id"]}
            with _LOCK:
                _WORKSPACES.append(ws)
            broadcast({"type": "project.updated", "properties": {"workspace": ws}})
            return self._json(ws)

        # 【/compact 命令】压缩上下文：把会话在该后端侧做一次整理。
        # 我们后端没有独立的 compact 接口，这里给会话打上摘要标记并广播，
        # 前端会据此刷新上下文读数（真正的裁剪由后端按窗口自己触发）。
        m = re.match(r"^/session/([^/]+)/(summarize|compact)$", p)
        if m:
            sid = m.group(1)
            ctx = _req("/api/context?sessionId=" + sid) or {}
            with _LOCK:
                s = _SESSIONS.get(sid)
            if s is not None:
                s["summary"] = {"additions": 0, "deletions": 0, "files": 0}
                s.setdefault("time", {})["updated"] = now_ms()
                broadcast({"type": "session.compacted", "properties": {"info": s}})
                broadcast({"type": "session.updated", "properties": {"info": s}})
            return self._json({"success": True, "context": ctx.get("context", {})})

        m = re.match(r"^/session/([^/]+)/message$", p)
        if m:
            return self._chat(m.group(1), body, blocking=True)

        m = re.match(r"^/session/([^/]+)/prompt_async$", p)
        if m:
            return self._chat(m.group(1), body, blocking=False)

        m = re.match(r"^/session/([^/]+)/abort$", p)
        if m:
            _req("/api/chat/control/stop", {"sessionId": m.group(1)})
            broadcast({"type": "session.idle", "properties": {"sessionID": m.group(1)}})
            return self._json(True)

        m = re.match(r"^/session/([^/]+)/fork$", p)
        if m:
            with _LOCK:
                src = _SESSIONS.get(m.group(1)) or {}
            s = new_session(str(src.get("title") or "新会话") + "（分支）", parent=m.group(1))
            return self._json(s)

        if re.match(r"^/session/[^/]+/(summarize|revert|unrevert|init|predict|resume|ask|shell|command)$", p):
            return self._json(True)
        if re.match(r"^/session/[^/]+/permissions/[^/]+$", p):
            return self._json(True)
        if p.startswith("/permission") or p.startswith("/question"):
            return self._json(True)
        if p.startswith("/tui/"):
            return self._json(True)
        if p == "/global/dispose":
            return self._json(True)

        return self._json({"error": "not implemented: " + p}, 404)

    def _chat(self, sid: str, body: dict, blocking: bool):
        """发消息：先回执一条 user 消息，再开线程把回答流式推出去。"""
        with _LOCK:
            if sid not in _SESSIONS:
                _SESSIONS[sid] = {"id": sid, "slug": _slug(6), "projectID": project()["id"],
                                  "directory": _DIRECTORY, "title": "会话",
                                  "titleSource": "fallback", "titleRevision": 1,
                                  "version": VERSION,
                                  "time": {"created": now_ms(), "updated": now_ms()}}
                _MESSAGES.setdefault(sid, [])
        text = _extract_text(body)
        umid = new_message(sid, "user", text=text)
        if text:
            new_part_text(sid, umid, text, start=True, end=True)
        amid = new_message(sid, "assistant", parent=umid)
        t = threading.Thread(target=_stream_backend, args=(sid, text, amid),
                             kwargs={"thinking": str(body.get("thinkingLevel") or "HIGH")},
                             daemon=True)
        t.start()
        if blocking:
            t.join(timeout=600)
            with _LOCK:
                for msg in _MESSAGES.get(sid, []):
                    if msg["id"] == amid:
                        return self._json({"info": msg, "parts": _PARTS.get(amid, [])})
        return self._json({"info": {"id": amid, "sessionID": sid, "role": "assistant"},
                           "parts": []})

    def do_PATCH(self):                                   # noqa: N802
        p = self._path()
        body = self._body()

        # 【/context-limit 命令走这里】前端发 PATCH /global/config {config:{...}}
        # 或直接 {contextLimit/...}；把上下文上限转给我们后端的 /api/context。
        if p in ("/global/config", "/config"):
            cfg = body.get("config") if isinstance(body.get("config"), dict) else body
            limit = None
            for k in ("contextLimit", "context_limit", "limit", "tokens"):
                if isinstance(cfg.get(k), (int, float)):
                    limit = int(cfg[k])
                    break
            if limit is not None:
                # 后端约定：tokens=0 表示不设限
                _req("/api/context", {"sessionId": "", "tokens": limit})
                broadcast({"type": "session.updated",
                           "properties": {"info": {"contextLimit": limit}}})

            # 【/models 选完模型走这里】把模型切换落到后端
            want = None
            for k in ("model", "modelID", "modelId"):
                if isinstance(cfg.get(k), str) and cfg[k]:
                    want = cfg[k]
                    break
            if want:
                global MODEL_ID
                MODEL_ID = want
                # 本地量化用 file 名切换；认不出来就当普通模型名交给 mode 接口
                _req("/api/runtime/local/model", {"file": want}) or _req(
                    "/api/runtime/mode", {"mode": "local", "model": want})
            return self._json({"success": True})

        m = re.match(r"^/session/([^/]+)$", p)
        if m:
            with _LOCK:
                s = _SESSIONS.get(m.group(1))
                if s:
                    if body.get("title"):
                        s["title"] = str(body["title"])
                    s.setdefault("time", {})["updated"] = now_ms()
            if s:
                broadcast({"type": "session.updated", "properties": {"info": s}})
            return self._json(s or {})
        return self._json(True)

    def do_DELETE(self):                                  # noqa: N802
        p = self._path()
        m = re.match(r"^/session/([^/]+)$", p)
        if m:
            with _LOCK:
                s = _SESSIONS.pop(m.group(1), None)
                _MESSAGES.pop(m.group(1), None)
            if s:
                broadcast({"type": "session.deleted", "properties": {"info": s}})
            return self._json(True)
        return self._json(True)


def main(argv: list[str] | None = None) -> int:
    global BACKEND, _DIRECTORY
    args = list(sys.argv[1:] if argv is None else argv)
    port = 8791
    for i, a in enumerate(args):
        if a.startswith("--port="):
            port = int(a.split("=", 1)[1])
        elif a == "--port" and i + 1 < len(args):
            port = int(args[i + 1])
        elif a.startswith("--backend="):
            BACKEND = a.split("=", 1)[1].rstrip("/")
        elif a.startswith("--directory="):
            _DIRECTORY = a.split("=", 1)[1]
    srv = _Server(("127.0.0.1", port), Handler)
    srv.daemon_threads = True
    # 【预建一个会话，让前端直接进去】MiMo 的流程是"选工作区 → 选会话 → 聊天"，
    # 每次启动都手动选太烦。attach 支持 `--session <id>`，所以这里先建好、
    # 把 id 写到文件里，启动脚本读出来传给 attach，就跳过那两步选择。
    warm = new_session("Lion Code")
    try:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           ".lbcheck", "mimo_session.txt")
        os.makedirs(os.path.dirname(out), exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            f.write(warm["id"])
    except Exception:                                     # noqa: BLE001
        pass
    print(f"MiMo 兼容接口层已就绪: http://127.0.0.1:{port}  → 后端 {BACKEND}", flush=True)
    print(f"预建会话: {warm['id']}（前端用 --session 直接进入）", flush=True)
    print(f"用 MiMo 前端挂上来: bun run --conditions=browser ./src/index.ts "
          f"attach http://127.0.0.1:{port}", flush=True)
    try:
        srv.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())