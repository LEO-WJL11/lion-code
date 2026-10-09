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

import io
import json
import os
import queue
import re
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

VERSION = "1.5.46"
AGENT = "build"
#: agent 名 → 后端的工作模式（后端只认 STANDARD / MINIMAL ✓ 见 main.py 的
#: SELECTABLE 与 `POST /api/sessions/{id}/mode` ✓）。
#: 【为什么需要它】MiMo 的 agent 是它自己的概念 ✗，而我们只有"工作模式" ✓ ——
#: 用 agent 名当这两者的桥：`Tab` 切到 minimal → 会话模式切成 MINIMAL ✓
AGENT_MODES = {"build": "STANDARD", "minimal": "MINIMAL"}
PROVIDER_ID = "lionbox"
MODEL_ID = "lion-merged"

# ─────────────────────────────────────────── 后端地址（Lion Code 的 /api/*）
BACKEND = os.environ.get("LION_CODE_BACKEND", "http://127.0.0.1:8080").rstrip("/")


def _req(path: str, body: dict | None = None, timeout: float = 30.0,
         method: str | None = None):
    """调 Lion Code 后端。失败返回 None（调用方兜住）。"""
    url = BACKEND + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(
        url, data=data,
        method=method or ("POST" if body is not None else "GET"),
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
#: 默认工作区的 id —— 只生成一次，保证状态接口的键和列表对得上
_WORKSPACE_DEFAULT_ID = ""
#: /context-limit 设过的上下文窗口（token）；None = 从来没设过。
#: 【为什么留这份】后端只有**会话级**入口（POST /api/context → ContextBudget.set，
#: main.py:10789-10810 / 11630-11645），设一次只对当时存在的会话生效 ——
#: 新建的会话要靠 create_backend_session 里的回填钩子补上，才算"全局配置"。
_CONTEXT_LIMIT: int | None = None
#: 回显给 GET /config、GET /global/config 的 config 片段。
#: 前端 dialog-context-limit.tsx:83-101 写完会 dispose → bootstrap → 重读
#: merged config 验证 `applied.effective`，不回显 compaction.max_context
#: 就永远算 "shadowed" 报错 toast ✗（形状以 overflow.ts:44-51 的读法为准）。
_GLOBAL_CFG: dict = {}
_DIRECTORY = os.getcwd()
#: 持久化根（.lioncode 所在处）。启动器用 --workspace= 传入，与 main.py 的
#: --lion.workspace.default-path 取同一个值。留空则在候选根里搜。
_WORKSPACE_ROOT = ""
_PROJECT_ID = None


def now_ms() -> int:
    return int(time.time() * 1000)


def _slug(n: int = 8) -> str:
    return uuid.uuid4().hex[:n]


def _parse_tokens(v) -> int | None:
    """token 数解析：数字直接用；`"300K"` / `"1M"` 按前端 Token 的 K/M 后缀
    （MiMo-Code-main 的 dialog-context-limit.tsx:165 用 Token.parseQuantity）。
    百分比要模型窗口才能算，这里没有 → 返回 None（不猜 ✗）。"""
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return int(v)
    s = str(v or "").strip().upper()
    if not s or s.endswith("%"):
        return None
    mul = 1
    if s.endswith("K"):
        mul, s = 1000, s[:-1]
    elif s.endswith("M"):
        mul, s = 1_000_000, s[:-1]
    try:
        return int(float(s) * mul)
    except ValueError:
        return None


def extract_context_limit(cfg) -> tuple[bool, int | None]:
    """从 PATCH /global/config 的 config 里取"上下文上限"。

    返回 ``(有没有设上限的字段, 该设的 token 数)``：
      · ``(False, None)`` —— 压根没带这个字段：选模型/改 modalities/加 provider
        的 PATCH 也走这里（dialog-model.tsx:293、dialog-modalities.tsx:72、
        dialog-mimo-login.tsx:118 都发到同一端点），**一律别动后端**；
      · ``(True, None)`` —— 带了但值解析不了：调用方回 400。用户明确写了预算却
        静默忽略 = 又一次"报成功其实没生效" ✗；
      · ``(True, n)`` —— 真要写的值（0 = 恢复模型默认 / 不设限）。

    【两路来源，都读过消费方源码】
      ① 真前端 `/context-limit`（dialog-context-limit.tsx:75-78）写的是
         `{config:{compaction:{max_context:{ "<providerID>/<modelID>": tokens }}}}`
         —— 按模型 key 记账、0 = 恢复模型默认（overflow.ts:44-57）；
      ② 老客户端直接给标量 `{contextLimit|context_limit|limit|tokens}`。

    【key 怎么选】后端预算是**会话级**、不分模型（ContextBudget.set，
    main.py:11630），取值顺序：当前模型 key → `"*"` 通配（overflow.ts:49 的
    Wildcard.all）→ 只写了一个 key 就用它（TUI 的 selected model 是**本地**选择
    （local.model），不一定等于适配层 MODEL_ID，而 dialog 每次只写自己那一个 key
    （L77））→ 多个 key 都不含当前模型 = 本模型无预算 → (True, None) 不动后端。
    """
    if not isinstance(cfg, dict):
        return False, None
    comp = cfg.get("compaction")
    if isinstance(comp, dict) and "max_context" in comp:
        mc = comp.get("max_context")
        if isinstance(mc, dict):
            if not mc:                                # {} = 清空 = 模型默认
                return True, 0
            v = mc.get(f"{PROVIDER_ID}/{MODEL_ID}")
            if v is None:
                v = mc.get("*")                       # Wildcard 兜底（overflow.ts:49）
            if v is None and len(mc) == 1:
                v = next(iter(mc.values()))           # 单 key：就是调用方当前模型的意图
            if v is None:
                return True, None                     # 多 key 都不含当前模型 → 别动后端
            return True, _parse_tokens(v)             # None = 解析不了 → 400
        return True, _parse_tokens(mc)                # 标量 300000 / "300K" / "50%"→None
    for k in ("contextLimit", "context_limit", "limit", "tokens"):
        if k in cfg:
            return True, _parse_tokens(cfg.get(k))
    return False, None


def config_snapshot() -> dict:
    """GET /config / GET /global/config 要回显的 config 片段（深一层拷贝，锁内取）。"""
    with _LOCK:
        out = {k: v for k, v in _GLOBAL_CFG.items() if not isinstance(v, dict)}
        comp = _GLOBAL_CFG.get("compaction")
        if isinstance(comp, dict):
            out["compaction"] = {k: (dict(v) if isinstance(v, dict) else v)
                                 for k, v in comp.items()}
    return out


def _apply_context_limit(limit: int) -> tuple[int, int, int]:
    """把窗口上限写到**真实**后端会话上。返回 (成功, 失败, 尝试数)。

    【为什么必须是真实会话 id】后端 set 里 `session_id is None` 只返回不落盘、
    `sessionId=""` 写进 `_per_session[""]` 这个**幽灵键** —— 读取方
    `effective_context_limit`（main.py:14828-14839）传的是真实 UUID，幽灵键
    聊天时永远查不到（用 `GET ?sessionId=` 空值倒是能读回来，但没有任何会话
    用它）—— 老代码就是靠它"报成功却不生效"，实测见 do_PATCH 注释 ✗。
    会话 id 取两处并集：内存 _SESSIONS 的 backendID + 后端 /api/sessions 全量。
    """
    ids: set[str] = set()
    with _LOCK:
        for s in _SESSIONS.values():
            b = str(s.get("backendID") or "")
            if b:
                ids.add(b)
    listed = _req("/api/sessions") or {}
    list_ok = isinstance(listed, dict) and bool(listed.get("success"))
    for x in (listed.get("data") or [] if isinstance(listed, dict) else []):
        if isinstance(x, dict) and x.get("sessionId"):
            ids.add(str(x["sessionId"]))
    ok = fail = 0
    for b in sorted(ids):
        resp = _req("/api/context", {"sessionId": b, "tokens": limit}, timeout=10.0)
        if isinstance(resp, dict) and resp.get("success"):
            ok += 1
        else:
            fail += 1
            print(f"[上下文] 写入失败 session={b} 返回={resp!r}", flush=True)
    if not list_ok:
        fail += 1                                     # 连会话列表都没拿到 = 全靠内存里的漏网
        print(f"[上下文] 会话列表不可达，返回={listed!r}"[:300], flush=True)
    return ok, fail, len(ids)


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


def new_session(title: str = "新会话", parent: str | None = None,
                directory: str = "") -> dict:
    # 【id 由后端 id 派生】列表里点进来的会话就是这个形状；新建的也保持一致，
    # 否则同一条会话会在"内存随机 id"和"派生 id"下各出现一份。
    bid = ""
    try:
        bid = create_backend_session(directory)
    except Exception:                                     # noqa: BLE001
        pass
    sid = from_backend_id(bid) if bid else "ses_" + _slug(12)
    s = {"id": sid, "slug": _slug(6), "projectID": project()["id"],
         "directory": directory or _DIRECTORY, "parentID": parent, "title": title,
         "titleSource": "user", "titleRevision": 1, "version": VERSION,
         "backendID": bid,
         "time": {"created": now_ms(), "updated": now_ms()}}
    with _LOCK:
        _SESSIONS[sid] = s
        _MESSAGES[sid] = []
    broadcast({"type": "session.created", "properties": {"info": s}})
    return s


# ── 会话列表：把后端真实会话映射成 MiMo 形状 ──────────────────────────────
#: 形如 ses_<32位十六进制> 的 id 是我们派生的，可反查回后端 UUID
_SES_HEX = re.compile(r"^ses_([0-9a-fA-F]{32})$")


def from_backend_id(uuid: str) -> str:
    """后端 UUID → MiMo 侧 id（确定性派生，可逆）。"""
    return "ses_" + str(uuid).replace("-", "").lower()


def to_backend_id(mimo_sid: str) -> str:
    """MiMo 侧 id → 后端 UUID；不是派生形状就返回空串。"""
    m = _SES_HEX.match(str(mimo_sid or ""))
    if not m:
        return ""
    h = m.group(1).lower()
    return f"{h[0:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:32]}"


def _iso_ms(v) -> int:
    """ISO 时间串 → 毫秒；解析不了退回当前时间。"""
    if isinstance(v, (int, float)):
        return int(v * 1000) if v < 10_000_000_000 else int(v)
    s = str(v or "").strip()
    if not s:
        return now_ms()
    try:
        from datetime import datetime
        return int(datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp() * 1000)
    except Exception:                                     # noqa: BLE001
        return now_ms()


def _conv_roots(extra: str = "") -> list:
    r"""`.lioncode` 可能的所在根，按可信度排序。

    【为什么是搜而不是算】实测后端 /api/sessions 的 workspaceId 是**项目目录**
    （仓库根），而 .lioncode 落在 --lion.workspace.default-path 指定的
    **持久化根**（启动器给的是 <仓库>\.lbcheck\workspace）。两者名字和值都
    不同，算不出来；显式参数加候选搜索才可靠。
    """
    home = os.path.expanduser("~")
    cands = [
        _WORKSPACE_ROOT,
        os.environ.get("LION_WORKSPACE_DEFAULT_PATH", "").strip(),
        extra,
        os.path.join(_DIRECTORY, ".lbcheck", "workspace"),
        os.path.join(home, "lion-code-workspace"),
        _DIRECTORY,
    ]
    out, seen = [], set()
    for c in cands:
        c = str(c or "").strip()
        if c and c not in seen:
            seen.add(c)
            out.append(c)
    return out


def _find_persisted(backend_uuid: str, kind: str, extra: str = "") -> str:
    r"""在候选根里找 <root>/.lioncode/<kind>/<id>.json，返回第一个存在的。"""
    for root in _conv_roots(extra):
        try:
            p = os.path.join(root, ".lioncode", kind, backend_uuid + ".json")
            if os.path.isfile(p):
                return p
        except Exception:                                 # noqa: BLE001
            continue
    return ""


def _read_conv(backend_uuid: str, extra: str = "") -> list:
    """读持久化对话；任何异常都当没有历史，不让接口 500。"""
    try:
        p = _find_persisted(backend_uuid, "conversations", extra)
        if not p:
            return []
        with io.open(p, encoding="utf-8", errors="replace") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except Exception:                                     # noqa: BLE001
        return []


def _updated_ms(backend_uuid: str, fallback: int, extra: str = "") -> int:
    """最后活动时间：优先对话文件 mtime，其次会话元数据文件 mtime。"""
    for kind in ("conversations", "sessions"):
        p = _find_persisted(backend_uuid, kind, extra)
        if p:
            try:
                return int(os.path.getmtime(p) * 1000)
            except Exception:                             # noqa: BLE001
                continue
    return fallback


def _title_of(backend_uuid: str, name, fallback: str = "新会话", extra: str = "") -> str:
    """标题：后端 name → 首条用户消息 → 兜底。"""
    if isinstance(name, str) and name.strip():
        return name.strip()
    for rec in _read_conv(backend_uuid, extra):
        if isinstance(rec, dict) and str(rec.get("role")) == "user":
            txt = " ".join(str(rec.get("content") or "").split())
            if txt:
                return txt[:48] + ("…" if len(txt) > 48 else "")
    return fallback


def backend_sessions() -> list:
    """后端真实会话 → MiMo 的 Session 列表。"""
    r = _req("/api/sessions") or {}
    items = (r.get("data") or []) if isinstance(r, dict) else []
    out = []
    for x in items:
        if not isinstance(x, dict):
            continue
        uuid = str(x.get("sessionId") or x.get("id") or "")
        if not uuid:
            continue
        ws = str(x.get("workspaceId") or _DIRECTORY)
        created = _iso_ms(x.get("createdAt"))
        out.append({
            "id": from_backend_id(uuid),
            "slug": uuid.replace("-", "")[:8],
            "projectID": project()["id"],
            "directory": ws,
            "parentID": None,
            "title": _title_of(uuid, x.get("name"), extra=ws),
            "titleSource": "user" if x.get("name") else "auto",
            "titleRevision": 1,
            "version": VERSION,
            "backendID": uuid,
            "time": {"created": created, "updated": _updated_ms(uuid, created, extra=ws)},
        })
    return out


def all_sessions() -> list:
    """后端真实会话 + 本进程内存会话，按最后活动倒序（最新在上）。

    内存里的优先（那是正在聊的），避免同一会话出现两份。
    """
    with _LOCK:
        mem = list(_SESSIONS.values())
    merged, seen = [], set()
    for s in mem + backend_sessions():
        key = str(s.get("backendID") or s.get("id"))
        if key in seen:
            continue
        seen.add(key)
        merged.append(s)
    merged.sort(key=lambda s: int((s.get("time") or {}).get("updated") or 0), reverse=True)
    return merged


def session_messages(sid: str) -> tuple:
    """某会话的历史消息 + parts。

    内存里有（正在聊的）就用内存；否则回放持久化对话。
    返回 (messages, {messageID: [parts]})。
    """
    with _LOCK:
        mem = list(_MESSAGES.get(sid) or [])
        mem_parts = dict(_PARTS)
    if mem:
        return mem, {m["id"]: list(mem_parts.get(m["id"]) or []) for m in mem}

    bid = to_backend_id(sid)
    if not bid:
        with _LOCK:
            cur = _SESSIONS.get(sid)
        bid = str((cur or {}).get("backendID") or "")
    if not bid:
        return [], {}

    msgs, parts, parent = [], {}, ""
    for rec in _read_conv(bid):
        if not isinstance(rec, dict):
            continue
        role = str(rec.get("role") or "assistant")
        if role not in ("user", "assistant"):
            continue
        mid = str(rec.get("messageId") or ("msg_" + _slug(12)))
        base = {"id": mid, "sessionID": sid, "agentID": AGENT, "role": role,
                "time": {"created": now_ms(), "completed": now_ms()}}
        if role == "user":
            base.update({"agent": AGENT,
                         "model": {"providerID": PROVIDER_ID, "modelID": MODEL_ID}})
            parent = mid
        else:
            base.update({"parentID": parent, "modelID": MODEL_ID,
                         "providerID": PROVIDER_ID, "mode": "build", "agent": AGENT})
            # 历史消息同样必填 path/cost/tokens —— 重开/刷新会话读的就是这一条路径
            # （对话框崩不崩只看数据形状，历史与流式一视同仁 ✓）
            base.update(assistant_shape())
        msgs.append(base)
        mid_parts = []
        text = str(rec.get("content") or "")
        if text:
            mid_parts.append({"id": "prt_" + _slug(12), "sessionID": sid,
                              "messageID": mid, "type": "text", "text": text,
                              "time": {"start": now_ms(), "end": now_ms()}})
        reasoning = str(rec.get("reasoningContent") or "")
        if reasoning:
            mid_parts.append({"id": "prt_" + _slug(12), "sessionID": sid,
                              "messageID": mid, "type": "reasoning", "text": reasoning,
                              "time": {"start": now_ms(), "end": now_ms()}})
        parts[mid] = mid_parts
    return msgs, parts


def backend_session(session_id: str) -> str:
    """按需在后端建一个真会话，返回**后端认的** id。

    【为什么必须】适配层自己造的 id（ses_xxx）后端不认识，直接转发聊天会得到
    "会话不存在"。这里走后端既有的两步：POST /api/workspaces → POST /api/sessions。
    （之前拿假模型测没暴露：假模型不校验 sessionId。）
    """
    if not session_id:
        return ""
    # ① 由后端 id 派生出来的（列表里点进来的）→ 直接反查，不必创建
    direct = to_backend_id(session_id)
    if direct:
        return direct
    with _LOCK:
        s = _SESSIONS.get(session_id)
        if s is not None and s.get("backendID"):
            return str(s["backendID"])
    bid = create_backend_session()
    if bid:
        with _LOCK:
            cur = _SESSIONS.get(session_id)
            if cur is not None:
                cur["backendID"] = bid
    return str(bid)


def new_workspace_root() -> str:
    r"""新建工作区的落地根目录（`/new` 和 `/workspaces` 里"新建"的落点）。

    【为什么不直接用 `_WORKSPACE_ROOT`】那个名字已经属于**持久化根**
    （`.lioncode` 所在处，启动器用 `--workspace=` 传入，与后端
    `--lion.workspace.default-path` 同值）。这里在它下面再开一层 `workspaces/`；
    没传 `--workspace=` 时退回仓库内 `.lbcheck\workspace\workspaces`。
    """
    base = _WORKSPACE_ROOT or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), ".lbcheck", "workspace")
    return os.path.join(base, "workspaces")


def workspace_directory(mimo_workspace_id: str) -> str:
    """MiMo 侧工作区 id（wrk_xxx）→ 真实目录；认不出来就用当前目录。

    我们后端的 workspaceId 就是路径，所以拿到目录就能把会话放进对应工作区。
    """
    if not mimo_workspace_id:
        return _DIRECTORY
    with _LOCK:
        for w in _WORKSPACES:
            if w.get("id") == mimo_workspace_id:
                return str(w.get("directory") or _DIRECTORY)
    return _DIRECTORY


def create_backend_session(directory: str = "") -> str:
    """在后端新建会话，返回 UUID。

    `POST /api/workspaces` 的 id 就是工作区**路径**（实测）；
    `POST /api/sessions` 返回 {sessionId, workspaceId, mode, createdAt, ...}。
    `directory` 决定这条会话属于哪个工作区。
    """
    path = directory or _DIRECTORY
    ws = _req("/api/workspaces", {"path": path}) or {}
    wsid = (ws.get("data") or {}).get("id")
    if not wsid:
        d = _req("/api/workspaces/default") or {}
        wsid = (d.get("data") or {}).get("id")
    if not wsid:
        wsid = path
    made = _req("/api/sessions", {"workspaceId": wsid, "mode": "STANDARD"}) or {}
    data = made.get("data") or {}
    sid = str(data.get("sessionId") or data.get("id") or "")
    # 【/context-limit 的回填钩子】全局设过的窗口上限，新建的会话也要带上 ——
    # 后端的预算是**按会话**记的（ContextBudget.set，main.py:11630），不回填
    # 就只有"设的那一刻已存在的会话"生效（_CONTEXT_LIMIT 为 None 时零开销 ✓）。
    with _LOCK:
        lim = _CONTEXT_LIMIT
    if sid and lim is not None:
        r = _req("/api/context", {"sessionId": sid, "tokens": lim}, timeout=10.0)
        if not (isinstance(r, dict) and r.get("success")):
            print(f"[上下文] 新会话回填失败 session={sid} 返回={r!r}", flush=True)
    return sid


def assistant_shape() -> dict:
    """AssistantMessage 必填、而适配层两处构造都漏掉的三组字段。

    【以哪为准】`packages/sdk/src/v2/gen/types.gen.ts` 的 AssistantMessage（L1028）：
        L1054  path:   {cwd, root}                                ← 必填
        L1059  cost:   number                                     ← 必填
        L1060  tokens: {input, output, reasoning, cache:{read,write}}  ← 必填
    （UserMessage 没有这三项 ✓ 我们 user 分支本来就对 ✓）

    【谁在读、为什么缺了就 fatal】全是**裸读**（没有 ?.）：
        dialog-status.tsx:28   item.role === "assistant" && item.tokens.output > 0
                               → 打开状态对话框直接 "Cannot read properties of
                                 undefined (reading 'output')" ✓✓
        dialog-status.tsx:38   last.tokens.input + … + last.tokens.cache.read
                               + last.tokens.cache.write
        acp/agent.ts:110/1386  msg.tokens.input / .output / .reasoning

    【为什么先补 0】后端 SSE **不发 usage 帧**（main.py 里搜不到）、
    `ConversationMessage`（main.py:4905）也没有 token 字段 ⇒ 真值拿不到 ✗。
    补 0 是类型安全的：dialog-status 的 findLast 因 `> 0` 不命中该条 →
    `last` 为 undefined → L37 三元给 undefined → 对话框正常打开、只是不显示用量 ✓。
    要显示真用量得后端加 usage 帧 —— 已记入"未做"，不假装有数据 ✗。
    """
    return {"path": {"cwd": _DIRECTORY, "root": _DIRECTORY},
            "cost": 0,
            "tokens": {"input": 0, "output": 0, "reasoning": 0,
                       "cache": {"read": 0, "write": 0}}}


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
        # 必填三项（path/cost/tokens）—— 缺了 status 对话框一开就崩，见 assistant_shape()
        base.update(assistant_shape())
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
    # 【必须用后端 id】适配层的 ses_xxx 后端不认识 → 直接转发就是"会话不存在"
    bid = backend_session(sid) or sid
    body = json.dumps({"sessionId": bid, "message": text,
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
                    # 【必须完全符合前端的 ToolPart 类型 —— 否则一有工具调用就 fatal】✗
                    # 以 `packages/sdk/src/v2/gen/types.gen.ts` 的 ToolPart 为准：
                    #   {id, sessionID, messageID, type:"tool", callID, tool, state}
                    #   state（ToolStateCompleted）= {status, input, output, title,
                    #                                metadata, time:{start,end}}
                    # 逐条对上，"谁在读"都有出处：
                    #   · state.metadata —— index.tsx:318-328 对**每个** tool part 调
                    #     planSwitchTarget ✓，而 plan-switch.ts:5 是
                    #     `part.state.metadata.switched`（**没有** ?. ✓）
                    #     ⇒ metadata 缺失 = 一有工具调用就 "Cannot read properties
                    #       of undefined (reading 'switched')" ✓✓
                    #   · state.time —— index.tsx:3200 读 `state.time.compacted` ✓
                    #     2343/2350 读 `state.time.start` ✓ 同样没有 ?. ✓
                    #   · callID —— index.tsx:2146 用它对权限请求 ✓（缺了权限关联不上 ✓）
                    # 我原来这三样**一个都没给** ✗（只给了 status/input/output/title ✓）
                    _t = now_ms()
                    part = {"id": "prt_" + _slug(12), "sessionID": sid, "messageID": mid,
                            "type": "tool", "callID": "call_" + _slug(12), "tool": tool,
                            "state": {"status": "completed", "input": {}, "output": content,
                                      "title": tool, "metadata": {},
                                      "time": {"start": _t, "end": _t}}}
                    # 【存进消息里】原来只广播不存 ✗ → 刷新/重开这个会话时工具调用整段消失 ✓
                    # （前端的会话正文是 GET /session/{id}/message 拿的 ✓）
                    with _LOCK:
                        _PARTS.setdefault(mid, []).append(part)
                    broadcast({"type": "message.part.updated",
                               "properties": {"sessionID": sid, "time": now_ms(),
                                              "part": part}})
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
    def _encode(self, obj) -> bytes:
        """JSON 序列化（纯 CPU、有界）——**持 _LOCK 时只允许做到这一步**。"""
        return json.dumps(obj, ensure_ascii=False).encode("utf-8")

    def _emit(self, raw: bytes, code: int = 200) -> None:
        """把已编码的响应写到 socket（**必须在 _LOCK 之外调**）。

        【为什么】协议是 HTTP/1.1 且 wbufsize=0：send_response / wfile.write
        直接进内核发送缓冲，对端停读（浏览器后台标签页就是这么干的）时缓冲写满
        这里就**阻塞**。以前 `with _LOCK: return self._json(...)` 把这种阻塞变
        成全局锁持有 —— _LOCK 还管 broadcast(107)、SSE 订阅、所有会话读写，
        一处卡 = 整个适配层停摆（审 #1180/#735/#829/#1080）。
        约定：锁内算数据 + _encode，锁外 _emit。
        """
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _json(self, obj, code: int = 200) -> None:
        self._emit(self._encode(obj), code)

    def _workspace_of(self, body: dict | None = None) -> str:
        """当前请求属于哪个工作区（MiMo 侧 id）。

        SDK 把它放在请求头 `x-mimocode-workspace`
        （packages/sdk/src/v2/client.ts:82-85）；部分调用还会带 `?workspace=`
        或 body 里的 workspace。三处都读，读不到就当默认工作区。
        """
        h = self.headers.get("x-mimocode-workspace")
        if h:
            return urllib.parse.unquote(h).strip()
        q = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if q.get("workspace"):
            return str(q["workspace"][0]).strip()
        if isinstance(body, dict) and isinstance(body.get("workspace"), str):
            return str(body["workspace"]).strip()
        return ""

    def _body(self) -> dict:
        # Content-Length 不是纯数字（"abc"、"10, 10"）时 int() 直接 ValueError ——
        # 以前它逃出 do_POST 被 _Server.handle_error 静默吞掉（628-630，不开
        # MIMO_ADAPTER_DEBUG 一行日志都不打）→ 客户端只看到连接被掐、服务端零痕迹
        # （审 #671）。坏了就断开连接：body 长度未知，继续读会把残留字节当下一条
        # 请求解析，HTTP/1.1 keep-alive 下后患更大。
        try:
            n = int(self.headers.get("Content-Length") or 0)
        except (TypeError, ValueError):
            self.close_connection = True
            return {}
        if not n:
            return {}
        try:
            parsed = json.loads(self.rfile.read(n).decode("utf-8"))
        except Exception:                                 # noqa: BLE001
            return {}
        # JSON 数组/字符串经 `or {}` 也会原样返回（非 dict），而调用方全按 dict 用
        # （body.get(...) → AttributeError）→ 统一当空 dict（审 #671）。
        return parsed if isinstance(parsed, dict) else {}

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
            # 【必须是"资源 map"，不是 CPU 指标】我原来返回 {"cpu","memory","uptime"}
            # ✗ —— 那是按名字瞎猜的。真消费方（先读再改的）：
            #   sync.tsx:923-924   guard(sdk.client.experimental.resource.list(...),
            #                       (x) => setStore("mcp_resource", reconcile(x.data ?? {})))
            #   sync.tsx:277-279    mcp_resource: { [key: string]: McpResource }  ← **dict**
            #   types.gen.ts:3079   McpResource = {name, uri, description?, mimeType?, client}
            #   autocomplete.tsx:317-318
            #       for (const res of Object.values(sync.data.mcp_resource)) {
            #         const text = `${res.name} (${res.uri})`   ← 无 ?. 保护 ✓
            #   ⇒ 拿到 {cpu:0,...} 时 Object.values 给出三个**数字**，
            #      res.name / res.uri 全是 undefined → 自动补全里凭空多出
            #      3 条 "undefined (undefined)" 的垃圾选项（实测可见）✗
            # 我们没有 MCP 资源 ⇒ 返回**空 map**（形状对、语义对、不产生垃圾）✓
            return self._json({})
        # 【必须实现，且必须是数组】"新建工作区"对话框一打开就拉这个端点
        # （dialog-workspace-create.tsx:185），然后把结果直接 `.map`（L223）：
        #     list.map((item) => ({title: item.name, value: item.type, ...}))
        # 未实现时走通用兜底返回了**字典** —— 字典是 truthy，绕过了前端的
        # `if (!list)` 保护（L214），于是 `list.map is not a function` 直接崩界面。
        # 形状照前端的 `type Adaptor = {type, name, description}`（L14-18）；
        # `type` 会原样进 `workspace.create({type})`，所以只列我们真支持的那种。
        if p == "/experimental/workspace/adaptor":
            return self._json([
                {"type": "local", "name": "本地目录",
                 "description": "在本地磁盘上新建一个工作区目录"},
            ])
        # 【不能返空数组】TUI 拿到空的工作区列表就会弹"新建工作区"，
        # 于是每次启动都强制你先建一个工作区才能发消息（实测就是这么卡住的）。
        # 结构照 SDK 的 Workspace：{id,type,name,branch,directory,extra,projectID}
        if p == "/experimental/workspace":
            with _LOCK:
                if not _WORKSPACES:
                    _WORKSPACES.append(self._workspace())
                raw = self._encode(list(_WORKSPACES))   # 锁内只编码（快照原子）
            return self._emit(raw)                      # socket 写在锁外（见 _emit）
        if p == "/experimental/workspace/status":
            # 【形状】前端读的是数组 [{workspaceID, status}, ...]
            # （context/project.tsx:64 直接对它 .map），返回字典会被整段丢掉。
            # 取值用前端枚举里的 "connected"，否则会话列表会显示成异常状态。
            with _LOCK:
                if not _WORKSPACES:
                    _WORKSPACES.append(self._workspace())
                items = list(_WORKSPACES)
            return self._json([{"workspaceID": w["id"], "status": "connected"}
                               for w in items])
        if p == "/experimental/console":
            # 【字段名必须以 config/console-state.ts 的 ConsoleState 为准】✗
            # 我原来返回 {"org", "orgs"} —— **名字全不对** ✓，前端拿到的
            # `consoleManagedProviders` 是 undefined ✓ → provider-origin.ts 里
            #   Array.isArray(x) ? x.includes(id) : x.has(id)
            # 不是数组就走 .has() → `undefined.has` → **打开模型对话框就 fatal** ✓
            # 规范形状（ConsoleState ✓）：
            #   consoleManagedProviders: string[]（必填 ✗ 缺了就崩 ✓）
            #   activeOrgName?: string
            #   switchableOrgCount: number
            # 我们不做 console 托管，所以给"空"的那一份 ✓ —— 但**字段一个不能少** ✓
            return self._json({"consoleManagedProviders": [], "switchableOrgCount": 0})
        # 权限提问的超时（毫秒）；null = 不超时。前端启动时会探一次，
        # 不实现就吃 404 字典 —— 这里没人 .map，不至于崩，但补上更干净。
        if p == "/permission/ask-timeout":
            return self._json(None)
        if p == "/global/config":
            # 回显 /context-limit 写过的 compaction.max_context（形状以
            # overflow.ts:44-51 的读法为准）—— 前端写完 dispose→bootstrap→重读
            # merged config 验证 effective（dialog-context-limit.tsx:90-101），
            # 不回显就永远弹 "shadowed" 错误 toast ✗
            return self._json({"theme": "mimocode", "model": MODEL_ID,
                               **config_snapshot()})
        if p == "/project/current" or p == "/project":
            return self._json(project())

        if p == "/config":
            # 同上：sync.tsx:864 的 bootstrap 读的是 GET /config（sync.data.config
            # 就是它），compaction 的回显必须挂在这条上才有人看到
            return self._json({"model": f"{PROVIDER_ID}/{MODEL_ID}",
                               "theme": "mimocode", "autoupdate": False,
                               **config_snapshot()})
        if p in ("/config/providers", "/provider"):
            # 【同一个响应要填三处，字段缺一个就崩】✓ 前端 tui/context/sync.tsx：
            #   provider         ← 本响应的 .providers   ✓
            #   provider_default ← 本响应的 .default     ✓
            #   provider_next    ← **整个响应**           ✗
            # 而 provider_next 的消费方（dialog-provider.tsx 用 remeda 的 sortBy/map ✓）
            # 会 `...` 展开它的 .all ✗ —— 少了就是
            #   "Spread syntax requires ...iterable not be null or undefined" ✓
            # 真实现场：打开模型对话框直接 fatal error ✓（用户报的那个 ✓）
            # ⇒ **all / default / connected / authenticated 四个字段缺一不可** ✓
            _prov = self._provider()
            return self._json({
                "providers": [_prov],
                "default": {},
                # 全部已配置的 provider（前端按 id 排序/分组用 ✓）
                "all": [_prov],
                # 已连接 / 已认证的 id 列表（前端 `connected.includes(provider.id)` ✓）
                "connected": [PROVIDER_ID],
                "authenticated": [PROVIDER_ID],
            })
        if p == "/provider/auth":
            return self._json({})

        if p == "/session":
            # 【不能只返回内存】那只有本次启动见过的会话；侧边栏要的是后端
            # 持久化的全部会话（标题 + 最后活动时间），最新在上。
            return self._json(all_sessions())
        if p == "/session/status":
            return self._json({})

        m = re.match(r"^/session/([^/]+)$", p)
        if m:
            with _LOCK:
                s = _SESSIONS.get(m.group(1))
            if s is None:
                # 列表里点进来的历史会话：内存没有，但从后端列表能构造
                s = next((x for x in backend_sessions() if x["id"] == m.group(1)), None)
            return self._json(s) if s else self._json({"error": "not found"}, 404)

        m = re.match(r"^/session/([^/]+)/message$", p)
        if m:
            # 历史会话（列表里点进来的）内存里没有消息 → 回放持久化对话。
            # parts 也必须取自 hist_parts：回放出来的 part 不在 _PARTS 里，
            # 用 _PARTS 查会得到空数组（消息有、内容空）。
            msgs, hist_parts = session_messages(m.group(1))
            out = []
            for msg in msgs:
                out.append({"info": msg,
                            "parts": hist_parts.get(msg["id"]) or _PARTS.get(msg["id"], [])})
            return self._json(out)

        if re.match(r"^/session/([^/]+)/(todo|children|diff|task|actors|recovery)$", p):
            return self._json([])
        if re.match(r"^/session/([^/]+)/message/([^/]+)$", p):
            mid = p.rsplit("/", 1)[1]
            raw = None
            with _LOCK:
                for msgs in _MESSAGES.values():
                    for msg in msgs:
                        if msg["id"] == mid:
                            # 锁内只编码快照（dict(msg)/list() 拆引用），socket 写挪到锁外
                            raw = self._encode({"info": dict(msg),
                                                "parts": list(_PARTS.get(mid, []))})
                            break
                    if raw is not None:
                        break
            if raw is not None:
                return self._emit(raw)
            return self._json({"error": "not found"}, 404)

        if p == "/permission":
            return self._json([])
        if p == "/question":
            return self._json([])
        if p in ("/agent", "/agent/"):
            # 【这就是"切模式"的入口】MiMo 的 `Tab` 与 `/agents` 都读这个列表 ✓
            # agent 切换是**本地 store**（tui/context/local.tsx 的 setAgentStore ✓），
            # 切完随**消息**发出来（SDK: agent?: string ✓）—— 所以列表里必须有
            # 第二个 agent，用户才切得动 ✗（原来只有一个 build ✓）。
            # 名 → 后端工作模式的映射见 AGENT_MODES；实际切模式在收到消息时做。
            return self._json([
                {"name": "build", "description": "标准模式（STANDARD）—— 默认，能力全开",
                 "mode": "primary", "builtIn": True},
                {"name": "minimal", "description": "极简模式（MINIMAL）—— 提示词更短、更省 token",
                 "mode": "primary", "builtIn": True},
            ])
        if p == "/skill":
            # 【真实形状 —— 2026-10-09 打真后端 :18080 实测，不是猜的】
            # GET /api/skills 走 _envelope（main.py:20640-20674）双写：
            #   {ok, success, message, skillsDir, userSkillsDir,
            #    skills:[{id,name,displayName,description,...}, …],   ← 顶层一份
            #    data:{ok, skillsDir, skills:[…]}}                   ← data 也一份
            # **data 是 dict 不是 list** —— 原来 `items = data if isinstance(data,
            # list)` 恒为 [] ✗，/skill 永远返回空数组、前端技能面板静默为空。
            # 改前实测：后端 skills 有 4 条（backend/client/document/frontend），
            # GET /skill → []。取值首选 data.skills，envelope 顶层 skills 兜底。
            r = _req("/api/skills") or {}
            data = r.get("data") if isinstance(r, dict) else None
            if isinstance(data, dict):
                items = data.get("skills")
            elif isinstance(data, list):
                items = data
            else:
                items = r.get("skills")
            items = items if isinstance(items, list) else []
            return self._json([{"name": str(x.get("name") or x.get("id") or ""),
                                "description": str(x.get("description") or "")}
                               for x in items if isinstance(x, dict)])
        if p == "/command":
            return self._json([])
        if p in ("/lsp", "/formatter", "/vcs", "/file/status"):
            # lsp/formatter 消费方是 `reconcile(x.data ?? [])` → **数组** ✓（sync.tsx:921/926）
            # vcs 是 `reconcile(x.data)` 进 `vcs: VcsInfo | undefined`（sync.tsx:931），
            #   VcsInfo = {branch?, default_branch?}（types.gen.ts:3355，两字段全可选 ✓）
            #   plugin/api.tsx:143 有 `if (!sync.data.vcs) return` 兜底 ✓ ⇒ 空 dict 安全
            return self._json({} if p == "/vcs" else [])
        if p == "/mcp":
            # 【必须是 dict 不是数组】sync.tsx:922
            #   guard(sdk.client.mcp.status(...), (x) => setStore("mcp", reconcile(x.data ?? {})))
            #   sync.tsx:274-276  mcp: { [key: string]: McpStatus }   ← **dict**
            # 我原来和 lsp 一起返回 [] ✗ —— 数组塞进 dict store，
            # reconcile 会按数字键处理（空数组时侥幸无害，非空即错位）⇒ 单独返 {} ✓
            return self._json({})
        if p in ("/file", "/find", "/find/symbol"):
            return self._json([])

        return self._json({"error": "not implemented: " + p}, 404)

    def _workspace(self) -> dict:
        """默认工作区（当前目录）。返回它，TUI 就不会再逼你新建工作区。

        id 只生成一次：每次调用都换 id 的话，状态接口的键就和列表对不上了。
        """
        global _WORKSPACE_DEFAULT_ID
        name = os.path.basename(_DIRECTORY.rstrip("\\/")) or "lion-code"
        with _LOCK:
            if not _WORKSPACE_DEFAULT_ID:
                _WORKSPACE_DEFAULT_ID = "wrk_" + _slug(10)
            wid = _WORKSPACE_DEFAULT_ID
        return {"id": wid, "type": "local", "name": name,
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
            # 【必须只收"裸文件名"】`/api/models` 会把模型的**完整路径**也带出来
            # （实测多出一条 `C:\Users\Leo\Desktop\lion-code\lion-merged-IQ4_XS.gguf` ✓），
            # 混进列表后界面上就多出第 4 个选项，用户选中它必然失败 ✗ ——
            # 用户报过这个 ✓。判据：含路径分隔符的一律跳过 ✓（后端只认文件名 ✓）。
            if "\\" in x or "/" in x:
                continue
            if x not in seen:
                seen.add(x)
                out.append(x)
        return out

    def _restart_runtime(self, want: str) -> None:
        """切完模型后重启本地运行时（异步线程里跑 ✓）。

        【为什么必须做】只改配置不重启，llama-server 会继续用旧权重 ✓ ——
        用户切了 Q4_K_M，跑的还是 IQ4_XS，现象是"切了没反应" ✗。
        【失败要如实报】不许假装成功 ✗（本会话反复吃"静默"的亏 ✓）——
        打到自己这份日志（→ `.lbcheck/adapter.log` ✓）里，用户查得到 ✓。
        """
        try:
            r = _req("/api/runtime/local/restart", {}, timeout=180.0, method="POST")
            ok = isinstance(r, dict) and r.get("success") is not False
            if ok:
                print(f"[模型] 已切到 {want}，本地运行时已重启 ✓", flush=True)
            else:
                print(f"[模型] 已切到 {want}，但运行时重启返回异常: {str(r)[:200]}",
                      flush=True)
        except Exception as e:                                 # noqa: BLE001
            print(f"[模型] 已切到 {want}，但运行时重启失败: {type(e).__name__}: {e}",
                  flush=True)

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
            # 【工作区】`/new` 与 `/workspaces` 都是「先选工作区再开会话」，
            # 会话要真的落在那份目录里，否则"选择工作区"只是换个标题。
            return self._json(new_session(
                title, directory=workspace_directory(self._workspace_of(body))))

        # 【删除工作区】有的 SDK 用 POST 做删除，这里一并接住
        if re.match(r"^/experimental/workspace/(remove|delete)$", p):
            return self._json(self._remove_workspace(body))

        # 【/workspace 命令】新建/登记工作区：结构照 SDK 的 Workspace
        if p == "/experimental/workspace":
            # 【directory 走 query，不走 body】SDK 生成的 create 里
            #   args: [{in:"query",key:"directory"}, ... {in:"body",key:"type"} ...]
            # （packages/sdk/src/v2/gen/sdk.gen.ts:705）
            # 所以只读 body 会**永远读不到路径** ✗ —— 这就是"新建工作区只会
            # 自动编号建空目录、没法用自己项目目录"的根因。两个地方都读。
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            want = str((qs.get("directory") or [""])[0]).strip() or \
                   str(body.get("directory") or "").strip()

            if want:
                # 【用户指定了目录】已存在就直接登记 —— **不建、不覆盖、不动里面
                # 任何文件**（用户可能把自己的项目目录登记进来 ✗ 删他代码是灾难）。
                directory = os.path.abspath(os.path.expanduser(want))
                if os.path.isdir(directory):
                    pass                                  # 登记已有目录 ✓
                else:
                    try:
                        os.makedirs(directory, exist_ok=True)   # 不存在才建 ✓
                    except OSError:
                        return self._json({"error": "cannot create directory: " + want}, 400)
                    except Exception:                     # noqa: BLE001
                        pass
                # 名字默认取目录名；适配层建的 ones 已自带序号，天然不重名
                base = os.path.basename(directory.rstrip("\\/")) or "workspace"
                name = str(body.get("name") or base)
            else:
                # 【没给目录】保持原行为：自动编号 + 在 workspace_root 下建目录
                # （前端只发 {type, branch} 时走这条；别改回去 ✗）
                with _LOCK:
                    seq = len(_WORKSPACES) + 1
                base = os.path.basename(_DIRECTORY.rstrip("\\/")) or "lion-code"
                directory = os.path.join(new_workspace_root(), f"{base}-{seq}")
                try:
                    os.makedirs(directory, exist_ok=True)
                except OSError:
                    directory = _DIRECTORY
                name = str(body.get("name") or f"{base}-{seq}")

            # 【同名去重】登记两个同名目录（不同路径）时，名字后面补序号，
            # 否则列表里分不清谁是谁。
            with _LOCK:
                taken = {w.get("name") for w in _WORKSPACES}
            if name in taken:
                i = 2
                while f"{name}-{i}" in taken:
                    i += 1
                name = f"{name}-{i}"

            # 【同一目录重复登记】直接返回已有的那个，避免列表里出现两条一样的
            # （锁内只算快照，socket 写挪到锁外 —— 见 _emit）
            dup = None
            with _LOCK:
                for w in _WORKSPACES:
                    if os.path.normcase(str(w.get("directory") or "")) == os.path.normcase(directory):
                        dup = dict(w)
                        break
            if dup is not None:
                return self._json(dup)

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
            ctx = _req("/api/context?sessionId=" + (backend_session(sid) or sid)) or {}
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
            _req("/api/chat/control/stop", 
                 {"sessionId": backend_session(m.group(1)) or m.group(1)})
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
        # 【按 agent 切工作模式】MiMo 的 `Tab` / `/agents` 切的是它自己的 agent
        # （本地 store ✓），切完随消息发出来（SDK 字段 `agent` / `agentID` ✓）。
        # 我们后端只有工作模式（STANDARD / MINIMAL ✓），所以在这里把 agent 名
        # 翻译成模式并**真的切掉该会话的模式** ✓ —— 否则"切了但没生效" ✗。
        # 只在变化时调一次（每轮都调会白多一次后端往返 ✓）。
        want_mode = AGENT_MODES.get(str(body.get("agent") or body.get("agentID") or "").strip())
        if want_mode:
            _bid = backend_session(sid)
            # 【直接 POST，不要先读当前模式】后端**没有** `GET /api/sessions/{id}/mode`
            # ✗（只有 POST ✓ 见 main.py 的 `@router.post(".../mode")`）——
            # 我第一版先 GET 再比较，拿到 404 → 当前模式是空串 → 条件恒假 →
            # **从来不切** ✗。POST 是幂等的，直接设即可（一次本地调用，代价可忽略 ✓）。
            if _bid:
                _req("/api/sessions/" + _bid + "/mode", {"mode": want_mode}, method="POST")
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
            raw = None
            with _LOCK:
                for msg in _MESSAGES.get(sid, []):
                    if msg["id"] == amid:
                        # 锁内编码快照、锁外写 socket（见 _emit）：这条响应带着该轮
                        # 全部工具输出，可能上百 KB，阻塞写卡住全局锁就全盘停摆
                        raw = self._encode({"info": dict(msg),
                                            "parts": list(_PARTS.get(amid, []))})
                        break
            if raw is not None:
                return self._emit(raw)
        # 【兜底响应也必须是完整 AssistantMessage】以 `MiMo-Code-main\packages\sdk
        # \src\v2\gen\types.gen.ts` 的 AssistantMessage（L1028）为准：
        # time{created}、parentID、modelID、providerID、mode、agent、path、cost、
        # tokens 全是必填（L1033-1069）；缺 path/cost/tokens 的后果见
        # assistant_shape() 的注释 —— 消费方裸读：acp/agent.ts:1386
        # `msg.tokens.input`（session.prompt 的返回就是这里，L1410-1416）✗。
        # 触发点：prompt_async（上面 blocking=False 必经）+ 阻塞路径 600s 超时
        # 或消息被并发删除。time.completed 此刻**不给**：流可能还在跑，给 completed
        # 就是撒谎（真实完成时间由 _finish_message 写，types 里 completed 也是可选）。
        n = now_ms()
        info = {"id": amid, "sessionID": sid, "agentID": AGENT, "role": "assistant",
                "parentID": umid, "modelID": MODEL_ID, "providerID": PROVIDER_ID,
                "mode": "build", "agent": AGENT, "time": {"created": n}}
        info.update(assistant_shape())      # path/cost/tokens（475-479 同款）
        with _LOCK:
            raw = self._encode({"info": info, "parts": list(_PARTS.get(amid, []))})
        return self._emit(raw)

    def do_PATCH(self):                                   # noqa: N802
        # Python 要求 global 声明先于函数内对该名字的**一切**使用（否则
        # SyntaxError: name used prior to global declaration）—— 声明放最前面。
        global MODEL_ID, _CONTEXT_LIMIT
        p = self._path()
        body = self._body()

        # 【/context-limit 命令走这里】前端 PATCH /global/config {config:{...}}
        # 或老客户端直接 {contextLimit/...}；转成我们后端 POST /api/context 的
        # 会话级预算（见 extract_context_limit / _apply_context_limit 的注释）。
        if p in ("/global/config", "/config"):
            cfg = body.get("config") if isinstance(body.get("config"), dict) else body
            # 【上下文上限：写**真实**会话 + 如实报错】审 #1199。
            # 旧代码 `_req("/api/context", {"sessionId": "", "tokens": limit})`
            # 写的是幽灵键：后端 set 把它记进 `_per_session[""]`（main.py:11630-
            # 11645），而读取方 effective_context_limit 传的是**真实会话 UUID**
            # （main.py:14828-14839）—— 幽灵键没有任何聊天会读到。实测
            # （老代码+活后端，见 .lbcheck\verify_before_ghost.py）：PATCH
            # {contextLimit:111111} → 200 {"success":true}，真实会话的
            # GET /api/context 依旧 {"sessionLimit":16384,"overridden":false}
            # ✗ **永不生效却报成功**。（幽灵键用 GET ?sessionId= 能读回来，
            # 但聊天路径永远查不到它。）
            intent, limit = extract_context_limit(cfg)
            if intent:
                comp_in = cfg.get("compaction") if isinstance(cfg, dict) else None
                if limit is None:
                    # 带了字段却换算不出来：静默跳过就是重蹈"报成功其实没生效" ✗
                    raw = (comp_in.get("max_context")
                           if isinstance(comp_in, dict) else None)
                    if raw is None:
                        raw = {k: cfg.get(k) for k in
                               ("contextLimit", "context_limit", "limit", "tokens")
                               if k in cfg}
                    msg = ("无法应用的上下文上限（要整数 token 或 \"300K\"/\"1M\"，"
                           "key 还要对得上当前模型）: "
                           + json.dumps(raw, ensure_ascii=False, default=str))
                    print("[上下文] " + msg, flush=True)
                    return self._json({"message": msg, "error": msg}, 400)
                # 【先写后端、看结果，成功才落本地状态】顺序反了就会"内存记着已设、
                # 后端实际没设"，GET /config 还跟着谎报生效 ✗
                ok_n, fail_n, total = _apply_context_limit(limit)
                if fail_n:
                    # 失败必须**非 2xx**：前端只看 res.error，而非 2xx 的
                    # {success:false} 它当成功（client.gen.ts:129 / :227）。
                    msg = (f"上下文上限未生效：{fail_n} 个写入失败"
                           f"（成功 {ok_n}/{total}）")
                    print("[上下文] " + msg, flush=True)
                    return self._json({"message": msg, "error": msg}, 400)
                with _LOCK:
                    _CONTEXT_LIMIT = limit
                    if isinstance(comp_in, dict) and "max_context" in comp_in:
                        # 回显**原样 key**：写入方 dialog-context-limit.tsx:38 用的是
                        # `${selected.providerID}/${selected.modelID}`，selected 是
                        # TUI 的**本地**选择（local.model），不一定等于适配层
                        # MODEL_ID —— 自己拼 key 会对不上，前端重读就报 shadowed ✗
                        mc = comp_in.get("max_context")
                        comp_cfg = _GLOBAL_CFG.setdefault("compaction", {})
                        cur = comp_cfg.get("max_context")
                        if isinstance(mc, dict) and isinstance(cur, dict):
                            cur.update(mc)
                        else:
                            comp_cfg["max_context"] = (
                                dict(mc) if isinstance(mc, dict) else mc)
                broadcast({"type": "session.updated",
                           "properties": {"info": {"contextLimit": limit}}})

            # 【/models 选完模型走这里】把模型切换落到后端
            want = None
            for k in ("model", "modelID", "modelId"):
                if isinstance(cfg.get(k), str) and cfg[k]:
                    want = cfg[k]
                    break
            if want:
                changed = want != MODEL_ID
                MODEL_ID = want
                # 本地量化用 file 名切换；认不出来就当普通模型名交给 mode 接口
                _req("/api/runtime/local/model", {"file": want}) or _req(
                    "/api/runtime/mode", {"mode": "local", "model": want})
                # 【切完必须重启运行时】实测：切换只改了**配置**（`modelFile` 变成
                # 新量化 ✓），但**正在跑的 llama-server 还是旧模型** ✗ ——
                # 用户以为切了、实际没换 ✓（用户报过这个 ✓）。
                # 后端有这个端点 ✓（`@router.post("/api/runtime/local/restart")` ✓
                # —— 读出来的，不是猜的 ✗）。
                # 【异步】重启要几十秒 ✗：卡住这个 PATCH 会让界面看起来像死了 ✓。
                # 【只在真的变了时重启】用户重复选同一个模型不该触发重启 ✓。
                if changed:
                    threading.Thread(target=self._restart_runtime, args=(want,),
                                     daemon=True).start()
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
        # 未知 PATCH 不再无条件回"假成功"（审 #1318）：与 do_POST 的 404 一致。
        # 已核对 TUI 侧的 PATCH 调用只有 global.config.update 与 session.update
        # （sdk.gen.ts 的 .patch< 共 5 个：global/config、/config、/session/{id}
        # 都接住了，project/{id}、part/{id} 在 cli/src 里查无调用方）。
        return self._json({"error": "not implemented: " + p}, 404)

    # -- 工作区删除（MiMo 有几个可能的入口，全部接住）
    def _remove_workspace(self, body: dict) -> dict:
        """从列表摘掉一个工作区；目录落在我们工作区根下时一并删除。"""
        q = self.path.split("?", 1)[1] if "?" in self.path else ""
        wid = ""
        for src in (body.get("id"), body.get("workspaceID"), body.get("workspaceId"),
                    body.get("name")):
            if isinstance(src, str) and src:
                wid = src
                break
        if not wid and q:
            for pair in q.split("&"):
                if pair.startswith(("id=", "workspaceID=")):
                    wid = urllib.parse.unquote(pair.split("=", 1)[1])
                    break
        if not wid:
            # 裸 id 形态 `/experimental/workspace/wrk_xxx`（DELETE 的常规形态，
            # 外层 do_DELETE 的正则明确接住了它）也必须解得出来 —— 原来的
            # `([^/]+)/(remove|delete)?$` 里那个 "/" 是**必需**的（(remove|delete)?
            # 只是可选组），没有后缀段整串不匹配 → wid 恒空 → 永远报
            # "缺少工作区 id"，工作区永远删不掉（审 #1257；
            # 改前实测 DELETE /experimental/workspace/wrk_bogus123 →
            # {"success": false, "message": "缺少工作区 id"}）。
            m2 = re.match(r"^/experimental/workspace/([^/]+)(?:/(?:remove|delete))?$",
                          self._path())
            wid = urllib.parse.unquote(m2.group(1)) if m2 else ""
        if not wid:
            return {"success": False, "message": "缺少工作区 id"}

        gone = None
        with _LOCK:
            for i, w in enumerate(list(_WORKSPACES)):
                if wid in (str(w.get("id")), str(w.get("name"))):
                    gone = _WORKSPACES.pop(i)
                    break
        if gone is None:
            return {"success": False, "message": "工作区不存在: " + wid}

        # 【只清理适配层自己建的空目录】工作区删除的语义是"从应用里注销"，
        # 不是删用户的文件 ✗ —— 用户完全可能把真实项目目录注册成工作区，
        # 无条件 rmtree 就是删他的代码。这里要求同时满足：
        #   ① 在 <workspace_root>/workspaces/ 之下（适配层建的都在这）
        #   ② 目录为空（非空说明用户在里头放东西了，一律不碰）
        d = str(gone.get("directory") or "")
        # 根必须与**创建侧同源**：new_workspace_root()（见其 docstring）。
        # 原来用 `os.path.abspath(_WORKSPACE_ROOT or "")` —— _WORKSPACE_ROOT 为空
        # 时 abspath("") 是 **cwd**，而实际创建落在 <脚本目录>/.lbcheck/workspace，
        # 前缀判断恒假 → 适配层自建的空目录永不回收（审 #1277）；`if root` 那个
        # 守卫也因此恒真（abspath 永不返回空串），是死守卫。
        made = new_workspace_root()
        if d and os.path.abspath(d).startswith(os.path.abspath(made) + os.sep):
            target = os.path.abspath(d)
            if os.path.isdir(target) and not os.listdir(target):
                try:
                    os.rmdir(target)
                except OSError:
                    pass
        broadcast({"type": "project.updated", "properties": {"workspace": gone}})
        return {"success": True, "id": wid}

    def do_DELETE(self):                                  # noqa: N802
        p = self._path()
        body = self._body()

        # 【删除工作区】路径有好几种可能，都接住（日志会记录实际到达的那个）
        if p in ("/experimental/workspace", "/experimental/workspace/remove",
                 "/experimental/workspace/delete") or \
                re.match(r"^/experimental/workspace/[^/]+(/remove|/delete)?$", p):
            return self._json(self._remove_workspace(body))

        m = re.match(r"^/session/([^/]+)$", p)
        if m:
            sid = m.group(1)
            with _LOCK:
                s = _SESSIONS.get(sid)
            # 【必须落到后端，而且必须看结果】原来只删内存 → 重启后对话又回来
            # （看着成功其实没删）；后来补了 _req 却**丢弃返回值** —— _req 内部
            # `except: return None` 永不抛，下面原来的 try/except 是死代码，
            # 后端删失败照样回 true（审 #1308；旧代码 + 死后端实测：
            # DELETE /session/ses_xxx → HTTP 200 `true`，后端根本没收到请求）。
            bid = (s or {}).get("backendID") or backend_session(sid)
            if bid:
                resp = _req("/api/sessions/" + str(bid), method="DELETE")
                # 后端返回（main.py:7048-7062，实测 HTTP 200 + ApiResponse 包封）：
                #   成功   {"success":true,...}
                #   已不在 {"success":false,"error":"会话不存在: …"}  ← 幂等当成功
                #   真失败 {"success":false,"error":"删除会话失败…"}  ← 磁盘没删掉
                #   None   网络不通 / 5xx（_req 在 61-75 行吞掉异常）
                err = ""
                if resp is None:
                    err = "后端不可达，会话未删除: " + str(bid)
                elif not (isinstance(resp, dict) and resp.get("success")):
                    e = str(resp.get("error") or resp.get("message") or resp) \
                        if isinstance(resp, dict) else str(resp)
                    if "会话不存在" not in e:          # 幂等：后端说本来就没有 → 算删成
                        err = "后端删除失败: " + e
                if err:
                    # 失败就不动内存、不广播 —— 前端要能看到"没删成"。返回必须是
                    # **非 2xx**：SDK 只有非 2xx 才进 result.error（client.gen.ts:227），
                    # 前端 sidebar.tsx:94-99 / dialog-session-list.tsx:244-259 才弹错误。
                    print("[会话] 删除失败 " + err, flush=True)
                    return self._json({"message": err, "error": err}, 400)
            with _LOCK:
                s = _SESSIONS.pop(sid, None)
                msgs = _MESSAGES.pop(sid, None) or []
                # 回收该会话全部消息的 parts（审 #1314：原来的
                # `_PARTS.clear() if False else None` 是**恒 None 的死表达式**，
                # 一个键都没删过 → 长驻进程里 parts 只增不减；也不能直接
                # _PARTS.clear() —— 那会把**其它会话**的 parts 一起清掉）
                for mm in msgs:
                    _PARTS.pop(str(mm.get("id") or ""), None)
            if s:
                broadcast({"type": "session.deleted", "properties": {"info": s}})
            return self._json(True)
        # 未实现的 DELETE 不再无条件回 true（审 #1318）：有副作用的方法报"假成功"
        # 比报错更糟，且与 do_POST 的 404 一致。已核对 TUI 只调用 session.delete 与
        # experimental.workspace.delete（上面两段都接住了），其余 DELETE 端点
        # （pty/worktree/share/message-part/auth）在 cli/src 里查无调用方。
        return self._json({"error": "not implemented: " + p}, 404)


def main(argv: list[str] | None = None) -> int:
    global BACKEND, _DIRECTORY, _WORKSPACE_ROOT
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
        elif a.startswith("--workspace="):
            _WORKSPACE_ROOT = a.split("=", 1)[1]
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