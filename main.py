# -*- coding: utf-8 -*-
r"""main（由引擎内联生成）
（由 `tools/dev/_inline_engine.py` 从 `python/lionbox/` 内联生成；代码逻辑未改动）

【别名模块】下面把本文件吸收的旧模块名注册进 sys.modules 指向本模块，于是原代码里的
`from lionbox.xxx import Yyy` 与 `from . import deps`（`deps.foo`）**一行都不用改**。
"""
from __future__ import annotations

import sys as _sys
# 内置名清单：子模块别名绝不能覆盖它们（`format` 就撞过）。
# 注意 `in` 不能直接用于模块对象（报 "argument of type 'module' is not a
# container or iterable"），必须先取成集合。
_BI = frozenset(dir(__import__("builtins")))

if "lionbox" not in _sys.modules:
    import types as _types
    import importlib.machinery as _mach
    _pkg = _types.ModuleType("lionbox")
    _pkg.__path__ = []
    _pkg.__spec__ = _mach.ModuleSpec("lionbox", loader=None, is_package=True)
    _sys.modules["lionbox"] = _pkg

_ALIASES = (
    "lionbox.api.deps",
    "lionbox.api.response",
    "lionbox.config",
    "lionbox.config.store",
    "lionbox.http",
    "lionbox.http.server",
    "lionbox.local",
    "lionbox.local.runtime",
    "lionbox.local.prewarm",
    "lionbox.api.runtime",
    "lionbox.api",
    "lionbox.app",
    "lionbox.api.workspaces",
    "lionbox.sessions.context",
    "lionbox.events.compat",
    "lionbox.events.model",
    "lionbox.events.store",
    "lionbox.events.legacy",
    "lionbox.events",
    "lionbox.sessions.ids",
    "lionbox.sessions.message",
    "lionbox.sessions.modes",
    "lionbox.sessions.session",
    "lionbox.sessions.persistence",
    "lionbox.sessions.history",
    "lionbox.sessions.manager",
    "lionbox.sessions.restorer",
    "lionbox.sessions.title",
    "lionbox.sessions",
    "lionbox.api.sessions",
    "lionbox.api.events",
    "lionbox.api.files",
    "lionbox.llm.types",
    "lionbox.llm.base",
    "lionbox.llm.errors",
    "lionbox.llm.transport",
    "lionbox.llm.openai",
    "lionbox.llm.anthropic",
    "lionbox.llm.local",
    "lionbox.llm.manager",
    "lionbox.llm",
    "lionbox.api.models",
    "lionbox.api.approvals",
    "lionbox.api.changes",
    "lionbox.agent.arg_aliases",
    "lionbox.agent.name_aliases",
    "lionbox.agent.parsing",
    "lionbox.agent.context",
    "lionbox.agent.control",
    "lionbox.agent.guard",
    "lionbox.agent.loop",
    "lionbox.agent",
    "lionbox.context.envelope",
    "lionbox.context.roots",
    "lionbox.context.mentions",
    "lionbox.context.search",
    "lionbox.context",
    "lionbox.api.context",
    "lionbox.api.questions",
    "lionbox.misc.question",
    "lionbox.misc.sound",
    "lionbox.misc",
    "lionbox.api.notifications",
    "lionbox.api.native_dialog",
    "lionbox.config.provider",
    "lionbox.config.app_config",
    "lionbox.api.providers",
    "lionbox.api.plugins",
    "lionbox.api.plugin_dev",
    "lionbox.api.skills",
    "lionbox.api.runtime_extra",
    "lionbox.api.chat",
    "lionbox.api.agent_control",
    "lionbox.assembly",
    "lionbox.__init__",
    "lionbox.__main__",
    "lionbox.agent._verify",
    "lionbox.agent._verify_integration",
    "lionbox.desktop",
    "lionbox.queue",
    "lionbox.queue.dispatcher",
    "lionbox.queue.message_queue",
    "lionbox.wiring",
)
for _n in _ALIASES:
    _sys.modules.setdefault(_n, _sys.modules[__name__])
# 子模块名绑成父模块属性：`from lionbox.tools.git import _git` 才不会因为
# 回退路径用 module.__name__（中文文件名）而失败。
for _n in _ALIASES:
    _p, _sep, _c = _n.rpartition(".")
# 【已存在就不要覆盖】这个名字可能本来就是本文件里的一个**函数/变量**
    # （例如 工具 里有个 `shell`），覆盖成模块对象后调用它就报
    # `'module' object is not callable`（实测：常驻终端起不来）。
    # 只有当它不是已有名字时，才需要有这条"子模块别名"。
    # 【绝不能用内置名当子模块别名】引擎里有 `tools/code/format.py`，
    # 这条会把模块级全局 `format` 覆盖成模块对象 → 同一文件里所有 `format(...)`
    # 调用都报 `'module' object is not callable`（实测：常驻终端起不来、9 个套件红）。
    # `int`/`str`/`id`/`type` 同理，一律跳过。
    if _c not in _BI and _sep and _p in _sys.modules and not hasattr(_sys.modules[_p], _c):
        try:
            setattr(_sys.modules[_p], _c, _sys.modules[__name__])
        except Exception:
            pass
del _n, _p, _sep, _c
if not getattr(_sys.modules[__name__], "__path__", None):
    _sys.modules[__name__].__path__ = []
# 【必须在模块体之前生效】引擎里有"导入时快照配置"的模块级常量，例如
#     sessions/persistence.py:  DEFAULT_WORKSPACE_PATH = workspace_default_path()
# 原来这些模块按需导入（CLI 已把 --lion.* 写进环境），内联后**所有模块体在导入本文件
# 时就跑完了**，而参数解析在文件末尾 —— 常量会快照到默认值（实测：套件指定的会话目录/
# 事件目录不生效，两个套件红）。所以这里先扫一遍 argv，把覆盖项写进环境。
# 映射表与引擎 `__main__.py` 的 PROPERTY_ENV 逐字一致（由补丁脚本从源码抓取）。
_LION_ENV = {
    "lion.workspace.default-path": "LION_WORKSPACE_DEFAULT_PATH",
    "lion.event.store-path": "LION_EVENT_STORE_PATH",
    "lion.plugin.scan-path": "LION_PLUGIN_SCAN_PATH",
    "lion.skills.dir": "LION_SKILLS_DIR",
    "lionbox.change-review.enabled": "LIONBOX_CHANGE_REVIEW_ENABLED",
}
for _a in _sys.argv[1:]:
    if _a.startswith("--"):
        _k, _eq, _v = _a[2:].partition("=")
        if _eq and _k in _LION_ENV:
            import os as _os
            _os.environ[_LION_ENV[_k]] = _v
# 【不要 del _a】argv 为空时循环体没跑，`_a` 从未定义 → `del _a` 会抛
# NameError（实测：`import main` 直接崩，当脚本跑却看不出问题）。留个循环变量无害。


# 前向依赖（加载顺序：沙箱 → 权限 → 插件管理 → 工具 → 技能 → main）
import 沙箱
import 权限
import 插件管理
import 工具
import 技能

# 【每个被内联模块各自原本的 __file__】有代码用它推算"程序装在哪"（例如技能目录：
# `skills/repository.py` 往上三层才是安装根）。内联后 `__file__` 全是 main.py 的路径，
# 向上推会跑到仓库外面 —— 实测后果是内置技能一个都找不到。所以按模块各记一份。
# 路径不必真实存在：用到的是路径运算，只要目录层级一致，算出的安装根就一样。
_ORIG_FILE_api_deps = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\deps.py"
_ORIG_FILE_api_response = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\response.py"
_ORIG_FILE_config = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\config\__init__.py"
_ORIG_FILE_config_store = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\config\store.py"
_ORIG_FILE_http = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\http\__init__.py"
_ORIG_FILE_http_server = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\http\server.py"
_ORIG_FILE_local = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\local\__init__.py"
_ORIG_FILE_local_runtime = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\local\runtime.py"
_ORIG_FILE_local_prewarm = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\local\prewarm.py"
_ORIG_FILE_api_runtime = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\runtime.py"
_ORIG_FILE_api = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\__init__.py"
_ORIG_FILE_app = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\app.py"
_ORIG_FILE_api_workspaces = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\workspaces.py"
_ORIG_FILE_sessions_context = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\context.py"
_ORIG_FILE_events_compat = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\events\compat.py"
_ORIG_FILE_events_model = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\events\model.py"
_ORIG_FILE_events_store = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\events\store.py"
_ORIG_FILE_events_legacy = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\events\legacy.py"
_ORIG_FILE_events = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\events\__init__.py"
_ORIG_FILE_sessions_ids = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\ids.py"
_ORIG_FILE_sessions_message = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\message.py"
_ORIG_FILE_sessions_modes = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\modes.py"
_ORIG_FILE_sessions_session = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\session.py"
_ORIG_FILE_sessions_persistence = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\persistence.py"
_ORIG_FILE_sessions_history = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\history.py"
_ORIG_FILE_sessions_manager = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\manager.py"
_ORIG_FILE_sessions_restorer = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\restorer.py"
_ORIG_FILE_sessions_title = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\title.py"
_ORIG_FILE_sessions = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\sessions\__init__.py"
_ORIG_FILE_api_sessions = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\sessions.py"
_ORIG_FILE_api_events = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\events.py"
_ORIG_FILE_api_files = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\files.py"
_ORIG_FILE_llm_types = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\types.py"
_ORIG_FILE_llm_base = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\base.py"
_ORIG_FILE_llm_errors = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\errors.py"
_ORIG_FILE_llm_transport = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\transport.py"
_ORIG_FILE_llm_openai = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\openai.py"
_ORIG_FILE_llm_anthropic = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\anthropic.py"
_ORIG_FILE_llm_local = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\local.py"
_ORIG_FILE_llm_manager = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\manager.py"
_ORIG_FILE_llm = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\llm\__init__.py"
_ORIG_FILE_api_models = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\models.py"
_ORIG_FILE_api_approvals = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\approvals.py"
_ORIG_FILE_api_changes = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\changes.py"
_ORIG_FILE_agent_arg_aliases = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\arg_aliases.py"
_ORIG_FILE_agent_name_aliases = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\name_aliases.py"
_ORIG_FILE_agent_parsing = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\parsing.py"
_ORIG_FILE_agent_context = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\context.py"
_ORIG_FILE_agent_control = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\control.py"
_ORIG_FILE_agent_guard = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\guard.py"
_ORIG_FILE_agent_loop = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\loop.py"
_ORIG_FILE_agent = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\__init__.py"
_ORIG_FILE_context_envelope = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\context\envelope.py"
_ORIG_FILE_context_roots = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\context\roots.py"
_ORIG_FILE_context_mentions = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\context\mentions.py"
_ORIG_FILE_context_search = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\context\search.py"
_ORIG_FILE_context = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\context\__init__.py"
_ORIG_FILE_api_context = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\context.py"
_ORIG_FILE_api_questions = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\questions.py"
_ORIG_FILE_misc_question = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\misc\question.py"
_ORIG_FILE_misc_sound = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\misc\sound.py"
_ORIG_FILE_misc = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\misc\__init__.py"
_ORIG_FILE_api_notifications = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\notifications.py"
_ORIG_FILE_api_native_dialog = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\native_dialog.py"
_ORIG_FILE_config_provider = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\config\provider.py"
_ORIG_FILE_config_app_config = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\config\app_config.py"
_ORIG_FILE_api_providers = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\providers.py"
_ORIG_FILE_api_plugins = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\plugins.py"
_ORIG_FILE_api_plugin_dev = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\plugin_dev.py"
_ORIG_FILE_api_skills = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\skills.py"
_ORIG_FILE_api_runtime_extra = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\runtime_extra.py"
_ORIG_FILE_api_chat = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\chat.py"
_ORIG_FILE_api_agent_control = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\api\agent_control.py"
_ORIG_FILE_assembly = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\assembly.py"
_ORIG_FILE___init__ = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\__init__.py"
_ORIG_FILE___main__ = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\__main__.py"
_ORIG_FILE_agent__verify = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\_verify.py"
_ORIG_FILE_agent__verify_integration = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\_verify_integration.py"
_ORIG_FILE_queue = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\queue\__init__.py"
_ORIG_FILE_queue_dispatcher = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\queue\dispatcher.py"
_ORIG_FILE_queue_message_queue = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\queue\message_queue.py"
_ORIG_FILE_wiring = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\wiring.py"


# ========================================================================
# 原模块 lionbox/api/deps.py
# ========================================================================
"""接口层共享上下文与服务定位 —— 所有 `api/*.py` 模块的公共地基。

【为什么要有这个文件】111 个接口分布在 17 个 controller 模块里，很多接口依赖同一份状态
（会话、工作区、事件、Agent 控制、提问…）。这些状态的真实实现由并行任务提供
（`lionbox.sessions` / `lionbox.events` / `lionbox.context` / `lionbox.agent`），
在它们到位之前，本文件提供**窄桩**：只保留 Java 侧的 JSON 形状与调用签名，
**不重复实现业务逻辑**（PORTING.md：不要自己实现别人的模块）。

每个桩都标了 `# 依赖：<模块>（由并行任务提供）`。真实模块到位后，装配方只需要：

    ctx.install("sessions", 真实 SessionManager 实例)

`ctx.service("sessions", factory)` 会优先返回已安装的真实对象，否则用窄桩。

【服务名清单（跨模块契约，改名字要同步所有使用者）】

| 服务名            | 归属模块（真实实现）        | 窄桩行为                       |
| ----------------- | --------------------------- | ------------------------------ |
| `sessions`        | `lionbox.sessions`          | 内存会话表（形状与 Java 一致） |
| `workspaces`      | `lionbox.context`（可选）   | **真实**：读写 config.workspaces |
| `events`          | `lionbox.events.store`      | 内存事件表（list 形状一致）    |
| `questions`       | `lionbox.agent`             | 内存待答提问表                 |
| `agent_control`   | `lionbox.agent`             | 内存 RUNNING/PAUSED/STOPPED    |
| `agent_loop`      | `lionbox.agent.loop`        | 缺依赖时明确报错，不假装成功   |
| `mentions`        | `lionbox.context`           | 不展开（返回原文）             |
| `changes`         | `lionbox.agent`（改动审查） | 空改动列表                     |
| `notifications`   | `lionbox.system`（通知）    | 读写 config.notification       |
| `title_service`   | `lionbox.sessions`          | 不生成标题（空操作）           |
"""


import datetime as _dt
import json
import logging
import os
import re
import threading
import uuid
from pathlib import Path
from typing import Any, Callable

log = logging.getLogger("lionbox.api.deps")

# --------------------------------------------------------------------------
# 小工具
# --------------------------------------------------------------------------

_SAFE_ID = re.compile(r"[^A-Za-z0-9._-]+")


def new_id(prefix: str, length: int = 8) -> str:
    """Java 侧惯用的短 id（`call_` + 8 位、`agent-` + 8 位…）。"""
    return prefix + uuid.uuid4().hex[:length]


def java_path(path: str | os.PathLike[str]) -> str:
    """Java `Path.of(p).toAbsolutePath().toString()` 的等价物。

    【为什么不能直接 str(Path(p))】Windows 上 Java 输出的是 `C:\\Users\\Leo\\Desktop`，
    小写盘符的原样保留；Python 的 pathlib 会规范成同样大小写，所以直接用 os.path.abspath
    最接近 Java 的行为（不做 casefold，避免与 Java 的 id 不一致）。
    """
    return os.path.abspath(str(path))


def now_instant() -> str:
    """Java `Instant.now()` 的 JSON 形态：`2026-10-03T11:55:28.690Z`（UTC、毫秒、Z 结尾）。"""
    return _dt.datetime.now(_dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.") + \
        f"{_dt.datetime.now(_dt.timezone.utc).microsecond // 1000:03d}Z"


def to_instant(value: Any) -> str:
    """把已有时间戳（str / float / datetime）转成 Instant 的 JSON 形态。"""
    if isinstance(value, str) and value:
        return value
    if isinstance(value, (int, float)):
        return _dt.datetime.fromtimestamp(float(value), _dt.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%S.") + f"{int(float(value) * 1000) % 1000:03d}Z"
    if isinstance(value, _dt.datetime):
        v = value.astimezone(_dt.timezone.utc) if value.tzinfo else value
        return v.strftime("%Y-%m-%dT%H:%M:%S.") + f"{v.microsecond // 1000:03d}Z"
    return now_instant()


def json_body(req: Any) -> dict[str, Any]:
    """请求体 JSON（空体/非法 JSON → 空 dict，与 Spring 的宽松行为一致）。"""
    value = req.json if hasattr(req, "json") else None
    return value if isinstance(value, dict) else {}


def body_value(body: dict[str, Any], *keys: str) -> Any:
    """取请求体里的第一个非 None 字段（兼容字段改名/驼峰差异时很有用）。"""
    for k in keys:
        if k in body and body[k] is not None:
            return body[k]
    return None


def as_str(value: Any, default: str = "") -> str:
    if value is None:
        return default
    if isinstance(value, str):
        return value
    return str(value)


def as_int(value: Any, default: int = 0) -> int:
    if value is None:
        return default
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def as_bool(value: Any, default: bool = False) -> bool:
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    return str(value).strip().lower() in ("1", "true", "yes", "on")


# --------------------------------------------------------------------------
# API Key 掩码（Java: com.lioncode.web.dto.SecretMask）
# --------------------------------------------------------------------------

DOTS = "••••"


class SecretMask:
    """API Key 的响应掩码。

    【为什么必须有】出厂的接口会把用户填的密钥明文回给客户端（`/api/runtime/mode`、
    `/api/chat/config` 回的都是整份配置快照）。服务虽然只绑回环，但本机任何进程、
    以及浏览器里的任意页面（配合 DNS rebinding）都能拿到 —— 等于把用户付费的密钥交出去。
    响应里给掩码（保留头 3 尾 4，便于辨认是哪一把）+ 布尔 `hasApiKey`；
    写入侧用 `is_mask` 判断"这是掩码不是真 key"，遇到掩码就用已存的真值。
    """

    @staticmethod
    def mask(key: Any) -> str:
        if key is None:
            return ""
        k = str(key).strip()
        if not k:
            return ""
        if len(k) <= 8:
            return DOTS + DOTS          # 太短：全部打点，不泄露长度分布
        return k[:3] + DOTS + k[-4:]

    @staticmethod
    def is_mask(value: Any) -> bool:
        return isinstance(value, str) and "••" in value

    @staticmethod
    def mask_deep(src: Any) -> dict[str, Any]:
        """递归把配置快照里所有 `apiKey` 字段换成掩码（**绝不能就地改**，
        否则内存里的真 key 会被覆盖成掩码，之后所有模型调用都会拿掩码去鉴权）。"""
        if not isinstance(src, dict):
            return {}
        out: dict[str, Any] = {}
        for k, v in src.items():
            if k == "apiKey" and isinstance(v, str):
                out["apiKey"] = SecretMask.mask(v)
                out["hasApiKey"] = bool(v.strip())
            elif isinstance(v, dict):
                out[k] = SecretMask.mask_deep(v)
            else:
                out[k] = v
        return out


# --------------------------------------------------------------------------
# 窄桩
# --------------------------------------------------------------------------


class DependencyMissing(RuntimeError):
    """依赖模块（并行任务）尚未就绪。**不吞异常**：让接口明确回一句能看懂的话。"""

    def __init__(self, what: str) -> None:
        super().__init__(f"{what} 尚未就绪（由并行任务提供）")
        self.what = what


class SessionStoreStub:
    """窄桩：内存会话表。

    # 依赖：lionbox.sessions（由并行任务提供）

    字段与 Java `SessionManager.Session` 一致：
    `sessionId / workspaceId / mode / createdAt / name`（name 可为 None）。
    真实的持久化（`~/.lioncode/sessions/*.json`）由 sessions 模块负责，这里只保证
    "接口形状对、同一进程内状态自洽"，绝不当成已完成实现。
    """

    def __init__(self) -> None:
        self._sessions: dict[str, dict[str, Any]] = {}
        self._mode_overrides: dict[str, str] = {}
        self._lock = threading.RLock()

    # ---- Java SessionManager 的对应方法（snake_case）----
    def create_session(self, workspace_id: str, mode: str = "STANDARD") -> dict[str, Any]:
        sid = str(uuid.uuid4())
        item = {"sessionId": sid, "workspaceId": workspace_id, "mode": mode,
                "createdAt": now_instant(), "name": None}
        with self._lock:
            self._sessions[sid] = item
        return dict(item)

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            item = self._sessions.get(session_id)
            return dict(item) if item else None

    def get_all_sessions(self) -> list[dict[str, Any]]:
        with self._lock:
            return [dict(v) for v in self._sessions.values()]

    def rename_session(self, session_id: str, name: str) -> bool:
        with self._lock:
            item = self._sessions.get(session_id)
            if item is None:
                return False
            item["name"] = name
            return True

    def move_session_to_workspace(self, session_id: str, workspace_id: str) -> bool:
        with self._lock:
            item = self._sessions.get(session_id)
            if item is None:
                return False
            item["workspaceId"] = workspace_id
            return True

    def set_title_if_absent(self, session_id: str, name: str) -> bool:
        with self._lock:
            item = self._sessions.get(session_id)
            if item is None or (item.get("name") or "").strip():
                return False
            item["name"] = name
            return True

    def update_mode(self, session_id: str, mode: str) -> bool:
        with self._lock:
            if session_id not in self._sessions:
                return False
            self._mode_overrides[session_id] = mode
            return True

    def get_effective_mode(self, session_id: str) -> str:
        with self._lock:
            override = self._mode_overrides.get(session_id)
            if override:
                return override
            item = self._sessions.get(session_id)
        return str(item.get("mode") or "STANDARD") if item else "STANDARD"

    def destroy_session(self, session_id: str) -> None:
        with self._lock:
            self._sessions.pop(session_id, None)
            self._mode_overrides.pop(session_id, None)


class WorkspaceStore:
    """工作区管理（**真实实现**：状态存在 `app-config.json` 的 `workspaces` 键下，
    与 Java `WorkspaceManager` 完全一致 —— 它注入的也是 AppConfigStore）。"""

    READ_ONLY = "READ_ONLY"
    WORKSPACE_WRITE = "WORKSPACE_WRITE"
    FULL_ACCESS = "FULL_ACCESS"
    ALL = (READ_ONLY, WORKSPACE_WRITE, FULL_ACCESS)

    def __init__(self, cfg: Any) -> None:
        self.cfg = cfg

    # ---- 读 ----
    def _load(self) -> dict[str, dict[str, Any]]:
        raw = self.cfg.get("workspaces") if self.cfg is not None else None
        out: dict[str, dict[str, Any]] = {}
        if isinstance(raw, dict):
            for wid, entry in raw.items():
                if isinstance(entry, dict):
                    path = as_str(entry.get("path") or wid)
                    perm = as_str(entry.get("permission"), self.WORKSPACE_WRITE)
                else:
                    path, perm = as_str(wid), as_str(entry, self.WORKSPACE_WRITE)
                if perm not in self.ALL:                     # 配置写歪了就回默认
                    perm = self.WORKSPACE_WRITE
                out[str(wid)] = {"id": str(wid), "path": path, "permission": perm}
        return out

    def _save(self, items: dict[str, dict[str, Any]]) -> None:
        payload = {k: {"path": v["path"], "permission": v["permission"]}
                   for k, v in items.items()}
        self.cfg.set("workspaces", payload)

    # ---- Java WorkspaceManager 的对应方法 ----
    def workspace_id_of(self, path: Any) -> str:
        """路径校验 + 归一化成工作区 ID（绝对路径）。

        【null / 空白 / 空串必须拦下】Java 的 `Path.of("")` 等于**当前进程工作目录**，
        会把用户根本没选过的目录静默注册成工作区。
        """
        if path is None or str(path).strip() == "":
            raise ValueError("工作区路径不能为空")
        try:
            return java_path(str(path))
        except (OSError, ValueError) as e:
            raise ValueError(f"工作区路径非法: {path}") from e

    def register_workspace(self, path: Any,
                           permission: str | None = None) -> dict[str, Any]:
        """注册工作区。已注册过的**不覆盖已有权限**：前端每次启动都会调
        `GET /api/workspaces/default` 重新注册默认工作区，覆盖会把用户手动设成
        "只读/全部权限"的工作区悄悄改回去。"""
        wid = self.workspace_id_of(path)
        items = self._load()
        existing = items.get(wid)
        if existing is not None:
            return existing
        perm = permission if permission in self.ALL else self.WORKSPACE_WRITE
        item = {"id": wid, "path": str(path), "permission": perm}
        items[wid] = item
        self._save(items)
        return item

    def get_workspace(self, wid: Any) -> dict[str, Any] | None:
        return self._load().get(str(wid))

    def get_all_workspaces(self) -> list[dict[str, Any]]:
        return list(self._load().values())

    def set_permission(self, wid: Any, permission: str) -> bool:
        if permission not in self.ALL:
            raise ValueError(f"无效的权限等级: {permission}")
        items = self._load()
        item = items.get(str(wid))
        if item is None:
            return False
        item["permission"] = permission
        self._save(items)
        return True


class EventStoreStub:
    """窄桩：内存事件表。

    # 依赖：lionbox.events.store（由并行任务提供）

    Java `EventStore.recordEvent(sessionId, type, data, message)` 的签名与
    `list_events(session_id)` 的形状（事件 DTO 由 events 模块定义）保持一致。
    """

    def __init__(self) -> None:
        self._events: dict[str, list[dict[str, Any]]] = {}
        self._lock = threading.RLock()

    def record_event(self, session_id: str | None, event_type: Any, data: dict[str, Any] | None = None,
                     message: str = "") -> dict[str, Any]:
        item = {
            "sessionId": session_id,
            "type": getattr(event_type, "value", event_type),
            "data": data or {},
            "message": message,
            "timestamp": now_instant(),
        }
        if session_id:
            with self._lock:
                self._events.setdefault(session_id, []).append(item)
        return item

    def list_events(self, session_id: str) -> list[dict[str, Any]]:
        with self._lock:
            return list(self._events.get(session_id, []))

    def get_events(self, session_id: str) -> list[dict[str, Any]]:
        return self.list_events(session_id)

    def clear(self, session_id: str) -> None:
        with self._lock:
            self._events.pop(session_id, None)


class AgentControlStub:
    """窄桩：会话运行控制。

    # 依赖：lionbox.agent（AgentControlManager，由并行任务提供）

    状态是易失的：每次新任务开始（processMessage 开头）自动 reset（Java 注释）。
    """

    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"

    def __init__(self) -> None:
        self._states: dict[str, str] = {}
        self._lock = threading.RLock()

    def reset(self, session_id: str) -> None:
        with self._lock:
            self._states.pop(session_id, None)

    def pause(self, session_id: str) -> None:
        with self._lock:
            self._states[session_id] = self.PAUSED

    def resume(self, session_id: str) -> None:
        with self._lock:
            self._states[session_id] = self.RUNNING

    def stop(self, session_id: str) -> None:
        with self._lock:
            self._states[session_id] = self.STOPPED

    def get_state(self, session_id: str) -> str:
        with self._lock:
            return self._states.get(session_id, self.RUNNING)

    def state_of(self, session_id: str) -> str:
        return self.get_state(session_id)


class QuestionServiceStub:
    """窄桩：用户提问（ask_user 工具用）。

    # 依赖：lionbox.agent（UserQuestionService，由并行任务提供）
    """

    DEFAULT_TIMEOUT_SECONDS = 300

    def __init__(self) -> None:
        self._pending: dict[str, dict[str, Any]] = {}
        self._events: dict[str, threading.Event] = {}
        self._answers: dict[str, str] = {}
        self._lock = threading.RLock()

    def ask(self, session_id: str, question: str, options: list[str] | None = None,
            timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, Any]:
        qid = new_id("q-")
        ev = threading.Event()
        with self._lock:
            self._pending[qid] = {"questionId": qid, "sessionId": session_id,
                                  "question": question, "options": list(options or []),
                                  "createdAt": now_instant()}
            self._events[qid] = ev
        got = ev.wait(timeout_seconds)
        with self._lock:
            self._pending.pop(qid, None)
            self._events.pop(qid, None)
            answer = self._answers.pop(qid, "")
        if got:
            return {"status": "ANSWERED", "answer": answer, "text": answer}
        return {"status": "TIMEOUT", "answer": "", "text": ""}

    def answer(self, question_id: str, answer: str) -> bool:
        with self._lock:
            ev = self._events.get(question_id)
            if ev is None:
                return False
            self._answers[question_id] = answer
            ev.set()
            return True

    def pending_of(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            for item in self._pending.values():
                if item["sessionId"] == session_id:
                    return dict(item)
        return None

    def cancel_session(self, session_id: str) -> int:
        with self._lock:
            ids = [q for q, item in self._pending.items() if item["sessionId"] == session_id]
            for q in ids:
                ev = self._events.pop(q, None)
                self._pending.pop(q, None)
                self._answers[q] = ""
                if ev is not None:
                    ev.set()
        return len(ids)

    def pending_count(self) -> int:
        with self._lock:
            return len(self._pending)

    def to_map(self, pending: dict[str, Any]) -> dict[str, Any]:
        return dict(pending)


class AgentLoopStub:
    """窄桩：Agent 主循环。

    # 依赖：lionbox.agent.loop（由并行任务提供）

    **不假装成功**：调用即抛 `DependencyMissing`，接口层会把它转成一句明确的错误
    （"Agent 主循环尚未就绪"），而不是返回空字符串让前端以为任务跑完了。
    """

    def process_message(self, session_id: str, message: str, mode: str = "STANDARD",
                        thinking_level: Any = None, model: str | None = None) -> str:
        raise DependencyMissing("Agent 主循环（lionbox.agent.loop）")

    def process_message_stream(self, session_id: str, message: str, mode: str = "STANDARD",
                               thinking_level: Any = None, model: str | None = None):
        raise DependencyMissing("Agent 主循环（lionbox.agent.loop）")


class MentionResolverStub:
    """窄桩：`@` 引用展开。

    # 依赖：lionbox.context（MentionResolver，由并行任务提供）

    没有它时**返回原文**（展开失败按原消息发下去 —— 与 Java 的兜底一致：
    引用读不到文件，不该让整条消息发不出去）。
    """

    @staticmethod
    def has_mention(message: str) -> bool:
        return bool(message) and "@" in message

    def expand(self, session_id: str, message: str) -> Any:
        class _Expansion:
            changed = False
            summary = ""
            notes: list[Any] = []

            @staticmethod
            def message() -> str:
                return message

        return _Expansion()


class NotificationStore:
    """通知设置（**真实实现**：读写 `app-config.json` 的 `notification` 键）。

    默认值与 Java `NotificationController`/前端一致：
    enabled/soundDone/soundApproval/soundQuestion/soundError/volume/minIntervalMs。
    """

    DEFAULTS: dict[str, Any] = {
        "enabled": True,
        "soundDone": True,
        "soundApproval": True,
        "soundQuestion": True,
        "soundError": True,
        "volume": 80,
        "minIntervalMs": 800,
    }

    def __init__(self, cfg: Any) -> None:
        self.cfg = cfg

    def snapshot(self) -> dict[str, Any]:
        raw = self.cfg.get("notification") if self.cfg is not None else None
        out = dict(self.DEFAULTS)
        if isinstance(raw, dict):
            for k, v in raw.items():
                if k in out:
                    out[k] = v
        return out

    def update(self, updates: dict[str, Any]) -> dict[str, Any]:
        cur = self.snapshot()
        for k, v in (updates or {}).items():
            if k in cur and v is not None:
                cur[k] = v
        self.cfg.set("notification", cur)
        return cur


# --------------------------------------------------------------------------
# 上下文
# --------------------------------------------------------------------------


class ApiContext:
    """接口层共享上下文。由 `api/__init__.py` 的装配钩子创建，模块之间只通过它取依赖。"""

    def __init__(self, app_root: Path | str, cfg: Any, runtime_api: Any = None,
                 adapters: Any = None, extra: dict[str, str] | None = None) -> None:
        self.app_root = Path(app_root)
        self.cfg = cfg
        self.runtime_api = runtime_api            # RuntimeApi（含 .runtime / .prewarm）
        self.extra = dict(extra or _extra_from_argv())
        self._services: dict[str, Any] = {}
        self._lock = threading.RLock()
        self._dispatcher: Any = None
        self._message_queue: Any = None
        self._adapters = adapters

    # ---- 服务定位 ----
    def install(self, name: str, obj: Any) -> Any:
        """装入真实实现（并行任务的模块到位后由装配方调用）。"""
        with self._lock:
            self._services[name] = obj
        return obj

    def has(self, name: str) -> bool:
        with self._lock:
            return name in self._services

    def service(self, name: str, factory: Callable[[], Any]) -> Any:
        with self._lock:
            if name not in self._services:
                self._services[name] = factory()
            return self._services[name]

    # ---- 常用派生 ----
    @property
    def runtime(self) -> Any:
        return getattr(self.runtime_api, "runtime", None)

    @property
    def prewarm(self) -> Any:
        return getattr(self.runtime_api, "prewarm", None)

    def adapters(self) -> Any:
        """适配器管理器（`llm.manager.AdapterManager`），首次访问时按配置装配。"""
        with self._lock:
            if self._adapters is None:
                from lionbox.llm import build_default_manager
                self._adapters = build_default_manager(
                    self.cfg, self.runtime, event_recorder=self.event_recorder)
            return self._adapters

    def event_recorder(self, session_id: str | None, data: dict[str, Any],
                       message: str) -> None:
        """适配器切换等事件写进事件存储（缺失时由窄桩兜住）。"""
        try:
            store = self.service("events", lambda: EventStoreStub())
            store.record_event(session_id, "ADAPTER_SWITCH", data, message)
        except Exception:
            log.warning("记录事件失败: %s", message, exc_info=True)

    def dispatcher(self) -> Any:
        """会话调度器（同一会话串行、不同会话互不阻塞）。"""
        with self._lock:
            if self._dispatcher is None:
                from lionbox.queue import MessageQueue, SessionDispatcher
                self._message_queue = MessageQueue()
                self._dispatcher = SessionDispatcher(
                    self._message_queue,
                    self.service("agent_loop", lambda: AgentLoopStub()),
                    self.service("agent_control", lambda: AgentControlStub()),
                    self.service("sessions", lambda: SessionStoreStub()),
                )
            return self._dispatcher

    def message_queue(self) -> Any:
        self.dispatcher()
        return self._message_queue


def _extra_from_argv() -> dict[str, str]:
    """从 `sys.argv` 收集 `--lionbox.*=value`（等价于 Java 的 `-D`）。

    【为什么要这么做】`app.py` 在构造完 HttpApp 之后才把 extra 挂到 `http.extra` 上，
    而路由注册发生在构造期间（RuntimeApi.register）—— 那时读不到它。
    插件开发模式之类的开关就靠这个提前拿到。
    """
    import sys
    out: dict[str, str] = {}
    argv = list(sys.argv[1:])
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--lionbox."):
            if "=" in a:
                k, v = a[2:].split("=", 1)
            else:
                k = a[2:]
                v = argv[i + 1] if i + 1 < len(argv) else ""
                i += 1
            out[k] = v
        i += 1
    return out


# --------------------------------------------------------------------------
# 服务访问器（各模块统一从这里取，不要自己 new）
# --------------------------------------------------------------------------


def sessions(ctx: ApiContext) -> Any:
    return ctx.service("sessions", lambda: SessionStoreStub())


def workspaces(ctx: ApiContext) -> WorkspaceStore:
    return ctx.service("workspaces", lambda: WorkspaceStore(ctx.cfg))


def events(ctx: ApiContext) -> Any:
    return ctx.service("events", lambda: EventStoreStub())


def agent_control(ctx: ApiContext) -> Any:
    return ctx.service("agent_control", lambda: AgentControlStub())


def questions(ctx: ApiContext) -> Any:
    return ctx.service("questions", lambda: QuestionServiceStub())


def agent_loop(ctx: ApiContext) -> Any:
    return ctx.service("agent_loop", lambda: AgentLoopStub())


def mentions(ctx: ApiContext) -> Any:
    return ctx.service("mentions", lambda: MentionResolverStub())


def notifications(ctx: ApiContext) -> NotificationStore:
    return ctx.service("notifications", lambda: NotificationStore(ctx.cfg))


def plugin_registry() -> Any:
    """工具/插件注册表（已就绪的基础设施）。

    【为什么不像别的一样做成可替换服务】`plugins/base.py` 的 `REGISTRY` 是显式登记的
    单例，按 PORTING.md 不允许目录扫描发现插件；这里只做一次转发。
    """
    from lionbox.plugins.base import REGISTRY
    return REGISTRY


def dump_json(data: Any) -> str:
    """与 http/server.py 的序列化保持一致（紧凑、不转义中文）。"""
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def spring_error(status: int, path: str, error: str | None = None) -> Any:
    """Spring 默认错误体的等价物。

    【为什么需要它】有些接口在 Java 里根本没进方法体：`@RequestBody` 缺失时 Spring 直接
    回 400 + 默认错误 JSON `{"timestamp","status","error","path"}`（前端与插件会按
    `status` 判断，比如"会话不存在"vs"请求体不合法"）。要逐字段对齐，就不能只回
    `{"success":false,"error":...}` —— 那是 200 + 业务错误，语义不同。
    """
    from lionbox.http.server import Response

    body = {"timestamp": now_instant(), "status": status,
            "error": error if error is not None else {400: "Bad Request",
                                                      404: "Not Found",
                                                      405: "Method Not Allowed",
                                                      500: "Internal Server Error"}.get(status, "Error"),
            "path": path}
    return Response.json(body, status=status)


# ========================================================================
# 原模块 lionbox/api/response.py
# ========================================================================
"""统一 API 响应包封。

【必须与 Java 版逐字段一致】Java 侧是：

    @JsonInclude(JsonInclude.Include.NON_NULL)
    public record ApiResponse<T>(boolean success, String message, T data, String error)

`NON_NULL` 是关键：**值为 null 的字段要整个省略**，而不是输出 `"message": null`。
前端 `web/index.html` 与 VS Code 插件都是按这个形状解析的，多一个 null 字段、
少一个 message 字段，都可能让它们判定失败。

- ok(data)        -> {"success": true,  "message": "操作成功", "data": ...}
- ok(msg, data)   -> {"success": true,  "message": msg,       "data": ...}
- error(err)      -> {"success": false, "error": err}
- error(msg, err) -> {"success": false, "message": msg,       "error": err}
"""


from typing import Any

OK_MESSAGE = "操作成功"


class ApiResponse:
    """与 Java 版 ApiResponse 同构的响应体。用 dict 而不是 dataclass：
    字段省略是"序列化期"行为，dict 更直白、也更好断言。"""

    __slots__ = ("_body",)

    def __init__(self, body: dict[str, Any]) -> None:
        self._body = body

    # ---- 构造 ----
    @staticmethod
    def ok(data: Any = None, message: str = OK_MESSAGE) -> "ApiResponse":
        body: dict[str, Any] = {"success": True, "message": message}
        if data is not None:
            body["data"] = data
        return ApiResponse(body)

    @staticmethod
    def ok_msg(message: str, data: Any = None) -> "ApiResponse":
        return ApiResponse.ok(data=data, message=message)

    @staticmethod
    def error(error: str, message: str | None = None) -> "ApiResponse":
        body: dict[str, Any] = {"success": False}
        if message is not None:
            body["message"] = message
        if error is not None:
            body["error"] = error
        return ApiResponse(body)

    # ---- 使用 ----
    @property
    def body(self) -> dict[str, Any]:
        return self._body

    @property
    def success(self) -> bool:
        return bool(self._body.get("success"))

    def __repr__(self) -> str:  # 便于调试与用例失败时打印
        return f"ApiResponse({self._body!r})"


# ========================================================================
# 原模块 lionbox/config.py
# ========================================================================
"""配置存储。"""



# ========================================================================
# 原模块 lionbox/config/store.py
# ========================================================================
"""应用配置存储 —— `{user.home}/.lioncode/app-config.json`。

【键名与文件位置必须与 Java 版完全一致】用户升级到 Python 版时，现有的
`app-config.json`（Provider 选择、本地模型参数、预热开关、工具调用模式…）必须能直接被读走，
不允许要求用户重新配置。写入用"临时文件 + 原子替换"，避免写一半断电留下半截 JSON
（Java 版 AppConfigStore 也是这么做的）。
"""


import json
import os
import tempfile
import threading
from pathlib import Path
from typing import Any

# 与 Java 版一致：安装程序会写这个标记文件告知"用户选了哪个模型"
INSTALL_MODEL_MARKER = "install-model.txt"

DEFAULTS: dict[str, Any] = {
    "providerMode": "local",
    "provider": "lionbox-local",
    "model": "lion-models1",
    "toolCallMode": "auto",
    # 本地 llama.cpp 运行时参数（键名与 Java 版 /api/runtime/local/config 一致）
    "llama": {
        "modelFile": "lion-merged-IQ4_XS.gguf",
        "modelName": "lion-models1",
        "host": "127.0.0.1",
        "port": 8788,
        "ctxSize": 262144,
        "ngl": 999,
        "kvCacheTypeK": "q4_0",
        "kvCacheTypeV": "q4_0",
        "flashAttn": True,
        "parallelSlots": 1,
        "threads": 0,
        "batchSize": 2048,
        "ubatchSize": 512,
        "temperature": 0.2,
        "topP": 0.9,
        "topK": 40,
        "minP": 0.05,
        "repeatPenalty": 1.05,
        "repeatLastN": 256,
        "seed": -1,
        "maxPredict": 4096,
        "extraArgs": "",
    },
}


#: 进程级默认配置目录覆盖。
#: 【为什么需要】`--config-dir` 原来只传给 app 自己 new 的那一个 `AppConfigStore`，
#: 而技能仓库、插件设置等模块各自 new 自己的实例（默认 `~/.lioncode`）——
#: 实测：用 `--config-dir` 起服务后点技能启停，写的还是 `~/.lioncode`，参数形同虚设。
#: 设成进程级默认值后所有实例一致（Java 侧本来就是同一个 Spring 单例，天然一致）。
_DEFAULT_BASE: Path | None = None


def set_default_base(path: str | os.PathLike[str] | None) -> None:
    """设置进程级默认配置目录（`--config-dir` 用）。传 None 还原。"""
    global _DEFAULT_BASE
    _DEFAULT_BASE = Path(path) if path else None


def _default_base() -> Path:
    return _DEFAULT_BASE if _DEFAULT_BASE is not None else (home_dir() / ".lioncode")

def home_dir() -> Path:
    """与 Java 的 `System.getProperty("user.home")` 对齐。"""
    return Path(os.path.expanduser("~"))


def workspace_default_path() -> Path:
    """默认工作区根目录 —— 对应 Java 属性 `lion.workspace.default-path`。

    【为什么要读环境变量】Java 版这个值是 Spring 的 `@Value`，启动时
    `--lion.workspace.default-path=D:\\tmp\\ws` 就能覆盖；Python 版没有属性源，
    `__main__` 把同名启动属性落到 `LION_WORKSPACE_DEFAULT_PATH` 上，这里读它。
    默认值与 Java 的 `application.yml` 一致：`${user.home}/lion-code-workspace`。
    """
    v = os.environ.get("LION_WORKSPACE_DEFAULT_PATH", "").strip()
    return Path(v) if v else home_dir() / "lion-code-workspace"


class AppConfigStore:
    def __init__(self, base: Path | None = None) -> None:
        self.base = Path(base) if base else _default_base()   # 允许传字符串，别让调用方踩这个坑
        self.file = self.base / "app-config.json"
        self._lock = threading.RLock()
        self._data: dict[str, Any] = {}
        self.load()

    # ---- 读写 ----
    def load(self) -> dict[str, Any]:
        with self._lock:
            data: dict[str, Any] = {}
            try:
                if self.file.is_file():
                    raw = self.file.read_text(encoding="utf-8")
                    parsed = json.loads(raw)
                    if isinstance(parsed, dict):
                        data = parsed
            except (OSError, ValueError):
                data = {}   # 坏文件不当机：用默认值继续，下次写入时覆盖
            self._data = data
            return data

    def save(self) -> None:
        with self._lock:
            self.base.mkdir(parents=True, exist_ok=True)
            payload = json.dumps(self._data, ensure_ascii=False, indent=2)
            fd, tmp = tempfile.mkstemp(dir=str(self.base), prefix=".app-config-", suffix=".tmp")
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as f:
                    f.write(payload)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp, self.file)   # 原子替换
            except BaseException:
                try:
                    os.unlink(tmp)
                except OSError:
                    pass
                raise

    # ---- 取值（键名与 Java 版一致）----
    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        with self._lock:
            self._data[key] = value
            self.save()

    def update(self, updates: dict[str, Any]) -> None:
        with self._lock:
            self._data.update(updates)
            self.save()

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            return json.loads(json.dumps(self._data))   # 深拷贝，调用方改不到内部

    # ---- 常用派生值 ----
    def llama(self) -> dict[str, Any]:
        with self._lock:
            cur = self._data.get("llama")
            merged = dict(DEFAULTS["llama"])
            if isinstance(cur, dict):
                merged.update(cur)
            return merged

    def update_llama(self, updates: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            cur = self._data.get("llama")
            merged = dict(DEFAULTS["llama"])
            if isinstance(cur, dict):
                merged.update(cur)
            merged.update(updates)
            self._data["llama"] = merged
            self.save()
            return merged

    @property
    def tool_call_mode(self) -> str:
        return normalize_tool_call_mode(self.get("toolCallMode", "auto"))

    @property
    def is_local_mode(self) -> bool:
        return self.get("providerMode", "local") == "local"

    def install_model_marker(self) -> str:
        """安装程序写的"用户选了哪个模型"标记（没有则空串）。"""
        try:
            p = self.base / INSTALL_MODEL_MARKER
            return p.read_text(encoding="utf-8").strip() if p.is_file() else ""
        except OSError:
            return ""


def normalize_tool_call_mode(value: Any) -> str:
    """与 Java 版 normalizeToolCallMode 对齐：只认 auto/native/text，其余回落 auto。

    【踩过的坑】这里原来写的是 `auto/native/prompt` —— `prompt` 根本不是契约里的值
    （Java 的常量是 `AppConfigStore.TOOLCALL_TEXT = "text"`）。后果是
    `POST /api/runtime/tool-call-mode {"mode":"text"}` 被"宽容归一"成 auto，
    `GET /api/runtime/mode` 回显 auto，`useNativeTools()` 也永远走不到文本通道 ——
    用户显式选"文本"在 Python 版上完全失效（`_check_tool_channel.py` 抓到）。
    `prompt` 作为历史别名仍然接受（内部 `AgentLoop(use_native_tools="prompt")` 在用），
    但一律归一到 `text`。
    """
    v = str(value or "").strip().lower()
    if v == "prompt":
        return "text"
    return v if v in ("auto", "native", "text") else "auto"


# ========================================================================
# 原模块 lionbox/http.py
# ========================================================================
"""HTTP 层：标准库服务器与路由（零第三方依赖）。"""



# ========================================================================
# 原模块 lionbox/http/server.py
# ========================================================================
"""极简 HTTP 服务与路由 —— 只用标准库，零第三方依赖。

【为什么不用 FastAPI/uvicorn】见 pyproject.toml 的说明：Java 版实测启动慢的主因是
"要读的文件数"（payload 11,623 个文件）。fastapi+uvicorn+pydantic 会再带进上千个依赖文件，
与"安装不能慢、首次启动不能慢"直接冲突。这里用 http.server + 自己写路由：
  · 启动只 import 标准库，实测 ~0.1 秒
  · 零依赖文件
  · 路由/参数/SSE 全部可控，能逐字段对齐 Java 版的响应包封

约定（与 Java 版 Spring MVC 对齐）：
  · 路由模板 `/api/sessions/{id}/history`，`{name}` 为路径参数
  · 请求体 JSON 解析进 Request.json
  · 处理函数返回 dict/list（自动包封）或 ApiResponse；返回 Response 则原样发出
  · SSE 用 Response.stream() —— 生成器产出 bytes/str，逐块 flush
"""


import json
import re
import threading
import time
import traceback
import urllib.parse
from collections.abc import Callable, Iterable, Iterator
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

# 【为什么这里用惰性导入】`lionbox.api.__init__` 在导入期会装装配钩子（它会导入
# `api.runtime`，而那个模块又回头导入本模块）。若在顶层导入 ApiResponse，就会形成
# "谁先被导入谁炸" 的循环：`import lionbox.http.server` 直接 ImportError。
# 放到函数里按需取，包之间就没有导入期依赖了。
def _api_response():
    from lionbox.api.response import ApiResponse
    return ApiResponse

# --------------------------------------------------------------------------
# 请求 / 响应
# --------------------------------------------------------------------------


class Request:
    __slots__ = ("method", "path", "query", "headers", "body", "params", "client")

    def __init__(self, method: str, path: str, query: dict[str, list[str]],
                 headers: dict[str, str], body: bytes, client: str = "") -> None:
        self.method = method
        self.path = path
        self.query = query
        self.headers = headers
        self.body = body
        self.params: dict[str, str] = {}   # 路径参数，由路由填入
        self.client = client

    # ---- 取值助手 ----
    def q(self, name: str, default: str | None = None) -> str | None:
        """查询参数（同名取第一个）。"""
        v = self.query.get(name)
        return v[0] if v else default

    def q_int(self, name: str, default: int) -> int:
        try:
            return int(self.q(name) or default)
        except (TypeError, ValueError):
            return default

    def q_bool(self, name: str, default: bool = False) -> bool:
        v = self.q(name)
        if v is None:
            return default
        return v.lower() in ("1", "true", "yes", "on")

    @property
    def json(self) -> Any:
        """解析 JSON 请求体；空体或非法 JSON 返回 None（与 Spring 的宽松行为一致）。"""
        if not self.body:
            return None
        try:
            return json.loads(self.body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return None

    def json_obj(self) -> dict[str, Any]:
        v = self.json
        return v if isinstance(v, dict) else {}

    def header(self, name: str, default: str = "") -> str:
        return self.headers.get(name.lower(), default)

    def __repr__(self) -> str:
        return f"<Request {self.method} {self.path}>"


class Response:
    """直接构造的响应。不返回它时，处理函数的返回值会被自动包封成 ApiResponse。"""

    __slots__ = ("status", "body", "content_type", "headers", "_stream", "_extra")

    def __init__(self, body: bytes | str = b"", status: int = 200,
                 content_type: str = "application/json; charset=utf-8",
                 headers: dict[str, str] | None = None) -> None:
        self.status = status
        self.body = body.encode("utf-8") if isinstance(body, str) else body
        self.content_type = content_type
        self.headers = headers or {}
        self._stream: Iterator[bytes | str] | None = None
        self._extra: dict[str, Any] = {}

    @staticmethod
    def json(data: Any, status: int = 200) -> "Response":
        return Response(json.dumps(data, ensure_ascii=False, separators=(",", ":")),
                        status=status)

    @staticmethod
    def text(s: str, status: int = 200) -> "Response":
        return Response(s, status=status, content_type="text/plain; charset=utf-8")

    @staticmethod
    def stream(chunks: Iterable[bytes | str], content_type: str = "text/event-stream; charset=utf-8",
               headers: dict[str, str] | None = None) -> "Response":
        r = Response(b"", status=200, content_type=content_type, headers=headers)
        r._stream = iter(chunks)
        return r

    @property
    def is_stream(self) -> bool:
        return self._stream is not None

    def iter_bytes(self) -> Iterator[bytes]:
        if self._stream is None:
            yield self.body
            return
        for c in self._stream:
            yield c.encode("utf-8") if isinstance(c, str) else c


# --------------------------------------------------------------------------
# 路由
# --------------------------------------------------------------------------


class Router:
    """路径模板路由。`{name}` 匹配单段（不含 /）。

    【匹配顺序：静态路径优先】实测踩过：`/api/plugins/stats` 被先注册的
    `/api/plugins/{pluginId}` 抢先匹配，变成"插件不存在: stats"；
    `/api/models/thinking-levels` 同样被 `/api/models/{adapterType}` 吃掉。
    Spring 的规则也是"精确路径 > 模板路径"，这里照做：无捕获组的静态路由先试，
    都不中再按注册顺序试带参数的。
    """

    def __init__(self) -> None:
        #: 全部路由，按注册顺序（供自检/文档枚举用）
        self._routes: list[tuple[str, re.Pattern[str], Callable[[Request], Any]]] = []
        #: 匹配用：静态（无捕获组）与动态分开，静态的先试
        self._static: list[tuple[str, re.Pattern[str], Callable[[Request], Any]]] = []
        self._dynamic: list[tuple[str, re.Pattern[str], Callable[[Request], Any]]] = []

    def add(self, method: str, pattern: str, handler: Callable[[Request], Any]) -> None:
        regex = re.sub(r"\{([A-Za-z_][A-Za-z0-9_]*)\}", r"(?P<\1>[^/]+)", pattern)
        entry = (method.upper(), re.compile("^" + regex + "$"), handler)
        self._routes.append(entry)
        (self._dynamic if entry[1].groups else self._static).append(entry)

    def route(self, method: str, pattern: str) -> Callable[[Callable[[Request], Any]], Callable[[Request], Any]]:
        def deco(fn: Callable[[Request], Any]) -> Callable[[Request], Any]:
            self.add(method, pattern, fn)
            return fn
        return deco

    def get(self, pattern: str):
        return self.route("GET", pattern)

    def post(self, pattern: str):
        return self.route("POST", pattern)

    def put(self, pattern: str):
        return self.route("PUT", pattern)

    def delete(self, pattern: str):
        return self.route("DELETE", pattern)

    def find(self, method: str, path: str) -> tuple[Callable[[Request], Any], dict[str, str]] | None:
        # 静态优先，再试参数路由（见类文档：/api/plugins/stats 不能被 {pluginId} 抢走）
        for group in (self._static, self._dynamic):
            for m, rx, fn in group:
                if m != method:
                    continue
                mo = rx.match(path)
                if mo:
                    return fn, mo.groupdict()
        return None

    @property
    def size(self) -> int:
        return len(self._routes)


# --------------------------------------------------------------------------
# 服务器
# --------------------------------------------------------------------------


class _Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"
    server_version = "Lion Code"
    sys_version = ""

    # 关掉逐请求的 stderr 噪声（Java 版也是只打业务日志）
    def log_message(self, fmt: str, *args: Any) -> None:  # noqa: A003
        pass

    def handle(self) -> None:
        """接住"客户端提前断开"。

        【为什么必须接】浏览器切页、`Invoke-WebRequest` 超时、界面轮询取消都会直接关连接，
        socketserver 这时会把整段 ConnectionResetError 堆栈打到 stderr —— 实测一次
        冒烟测试就刷出几十行，用户看到的日志全是红字，真正的错误反而被淹没。
        Java 那边这种断开是静默的。
        """
        try:
            super().handle()
        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
            self.close_connection = True

    # ---- 分发 ----
    def _serve(self) -> None:
        app = self.server.app  # type: ignore[attr-defined]
        started = time.perf_counter()
        try:
            u = urllib.parse.urlsplit(self.path)
            path = urllib.parse.unquote(u.path)
            query = urllib.parse.parse_qs(u.query, keep_blank_values=True)
            length = int(self.headers.get("Content-Length") or 0)
            body = self.rfile.read(length) if length > 0 else b""
            headers = {k.lower(): v for k, v in self.headers.items()}
            req = Request(self.command, path, query, headers, body,
                          client=str(self.client_address[0]) if self.client_address else "")

            hit = app.router.find(self.command, path)
            if hit is None:
                # 与 Spring 一致：未知路径 404 + 包封体
                self._send(Response.json(_api_response().error(f"没有这个接口: {path}").body, 404))
                return
            fn, params = hit
            req.params = params
            result = fn(req)
            if isinstance(result, Response):
                self._send(result)
            elif isinstance(result, _api_response()):
                self._send(Response.json(result.body))
            else:
                self._send(Response.json(_api_response().ok(result).body))
        except Exception as e:  # 处理函数抛错 -> 500 + 包封体（和 Java 的全局异常处理一致）
            tb = traceback.format_exc()
            try:
                self._send(Response.json(
                    _api_response().error(f"{type(e).__name__}: {e}").body, 500))
            except Exception:
                pass
            app.on_error(self.path, tb)
        finally:
            app.on_access(self.command, self.path, time.perf_counter() - started)

    def _send(self, resp: Response) -> None:
        if resp.is_stream:
            self.send_response(resp.status)
            self.send_header("Content-Type", resp.content_type)
            self.send_header("Cache-Control", "no-cache")
            self.send_header("Connection", "keep-alive")
            self.send_header("Transfer-Encoding", "chunked")
            for k, v in resp.headers.items():
                self.send_header(k, v)
            self.end_headers()
            for chunk in resp.iter_bytes():
                if not chunk:
                    continue
                self.wfile.write(b"%X\r\n" % len(chunk))
                self.wfile.write(chunk)
                self.wfile.write(b"\r\n")
                self.wfile.flush()
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
            return
        self.send_response(resp.status)
        self.send_header("Content-Type", resp.content_type)
        self.send_header("Content-Length", str(len(resp.body)))
        for k, v in resp.headers.items():
            self.send_header(k, v)
        self.end_headers()
        if resp.body:
            self.wfile.write(resp.body)

    do_GET = _serve
    do_POST = _serve
    do_PUT = _serve
    do_DELETE = _serve
    do_HEAD = _serve
    do_PATCH = _serve


class HttpApp:
    """应用容器：路由表 + 生命周期钩子。

    显式装配，没有 DI 容器 —— 启动路径一眼看得完，这是"启动快且可读"的前提。
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 8080) -> None:
        self.host = host
        self.port = port
        self.router = Router()
        self.started_at = time.time()
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None
        self.quiet = True
        self.slow_request_ms = 1000

    # 可被替换的钩子（日志/监控）
    def on_error(self, path: str, tb: str) -> None:
        print(f"[ERROR] {path}\n{tb}", flush=True)

    def on_access(self, method: str, path: str, seconds: float) -> None:
        if seconds * 1000 >= self.slow_request_ms:
            print(f"[SLOW] {method} {path} {seconds * 1000:.0f}ms", flush=True)

    def serve_forever(self, block: bool = True) -> None:
        srv = ThreadingHTTPServer((self.host, self.port), _Handler)
        srv.daemon_threads = True
        srv.app = self  # type: ignore[attr-defined]
        self._server = srv
        # 端口被占时 ThreadingHTTPServer 构造就会抛 OSError，调用方负责提示
        if block:
            srv.serve_forever()
        else:
            self._thread = threading.Thread(target=srv.serve_forever,
                                            name="lionbox-http", daemon=True)
            self._thread.start()

    def shutdown(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None


# ========================================================================
# 原模块 lionbox/local.py
# ========================================================================
"""本地模型运行时与预热。"""



# ========================================================================
# 原模块 lionbox/local/runtime.py
# ========================================================================
"""本地模型运行时（llama.cpp / llama-server 的 Python 管理）。

对照 Java 版 `model/runtime/LocalModelRuntime.java` 移植，**参数逐项对齐**：
    -m <model> -ngl <ngl> -c <ctx> [-ctk <k> -ctv <v>] [-fa on] -np <slots>
    [-t <n> -tb <n>] [-b <n>] [-ub <n>] --temp --top-p --top-k --min-p
    --repeat-penalty --repeat-last-n --host <h> --port <p> [extraArgs...]

生命周期与 Java 版一致（阶段名也一样，前端按 phase 显示）：
    idle -> loading -> ready / error
GPU 拉起失败会按 Java 版的做法**回落纯 CPU 重试一次**（ngl=0），
因为 Vulkan 在某些驱动上会初始化失败，而用户宁可慢也不要"起不来"。
"""


import os
import shlex
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any, Callable


RUNTIME_EXE_REL = Path("runtime-vulkan") / "llama-server.exe"
DEFAULT_LOG = Path(os.environ.get("TEMP", "/tmp")) / "lionbox-model.log"

#: 健康探测结果缓存时长（秒）。界面轮询与预热会同时问状态，没必要每次真去探。
HEALTH_CACHE_SECONDS = 1.5

#: 官方可选模型清单（体积是仓库里报的实际大小）。
#: 逐字对齐 Java `LocalModelRuntime.AVAILABLE_MODELS` —— 文案、体积、说明都是界面直接显示的，
#: 而且回归套件按这三个数字断言（8.87 / 5.24 / 4.87）。
AVAILABLE_MODELS: tuple[dict[str, Any], ...] = (
    {"file": "lion-merged-Q8_0.gguf", "label": "Q8_0（最高质量·默认）", "sizeGb": 8.87,
     "note": "原版精度，回答质量最好；下载 8.87 GB，解码约 11 token/s"},
    {"file": "lion-merged-Q4_K_M.gguf", "label": "Q4_K_M（平衡·推荐）", "sizeGb": 5.24,
     "note": "体积小 40%，解码约 1.7 倍快；质量略降"},
    {"file": "lion-merged-IQ4_XS.gguf", "label": "IQ4_XS（最小最快）", "sizeGb": 4.87,
     "note": "体积最小、速度最快；质量下降最明显，适合只看响应速度的场合"},
)

#: 小于这么大的文件当垃圾（与 Java `minModelBytes` 一致）
MIN_MODEL_BYTES = 1024 * 1024

# Windows: 不要弹出控制台窗口（Java 版是 -WindowStyle Hidden 的等效行为）
_CREATE_NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


#: 自动补齐权重的接线点（由 `api/runtime_extra.LocalModelsSupport.start_download` 挂上）。
#: 【为什么要一个接线点】Java 里"下载权重"这些方法本来就在 `LocalModelRuntime` 上；
#: Python 侧施工时把它们放进了 `api/runtime_extra.py` 的 `LocalModelsSupport`（同一个 runtime
#: 实例的薄适配层，见那里的说明）。而"模型没下载 → 自动去下"的启动路径在**本文件**里，
#: 不能反向 import api 层（会成环），所以照本仓库既有的做法（`_gate.set_review`、
#: `ask_user.set_question_service`）留一个显式接线点，由装配方挂上。
AUTO_DOWNLOADER: Callable[[str], dict[str, Any]] | None = None


def set_auto_downloader(fn: Callable[[str], dict[str, Any]] | None) -> None:
    """挂上/摘掉"后台下载指定权重"的实现（返回 `{started|downloaded|busy|error}`）。"""
    global AUTO_DOWNLOADER
    AUTO_DOWNLOADER = fn


def _now() -> float:
    return time.time()


class LocalModel:
    __slots__ = ("name", "path", "size_gb", "known", "size")

    def __init__(self, name: str, path: str, size: int, known: bool) -> None:
        self.name = name
        self.path = path
        self.size = size
        self.size_gb = round(size / 1073741824.0, 3)
        self.known = known

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "path": self.path, "sizeGb": self.size_gb,
                "known": self.known, "size": self.size}


class LocalModelRuntime:
    def __init__(self, app_root: Path, cfg: AppConfigStore,
                 start_timeout: int = 240, auto_download: bool = True) -> None:
        self.app_root = Path(app_root)
        self.cfg = cfg
        self.start_timeout = start_timeout
        self.auto_download = auto_download

        self._lock = threading.RLock()
        self._proc: subprocess.Popen | None = None
        self.phase = "idle"
        self.starting = False
        self.last_error = ""
        self.download_bytes = 0
        self.download_total = -1
        self.downloading_file = ""
        self._loading_since = 0.0
        self._started_with_ngl: int | None = None
        #: 实际拉起过的模型文件（Java `modelInUse`：**没启动过就是空串**，绝不假报成配置那个）
        self._model_in_use: str = ""
        #: 兜底用的模型文件（配置那份没就位时改用现成的；空 = 按配置来）
        self._override_file: str = ""
        self._health_cache: tuple[float, bool] | None = None
        self._last_known_running = False   # 下载期间沿用，避免状态接口被网络探测拖慢
        self._log_used: Path = DEFAULT_LOG

    # ------------------------------------------------------------------ 路径
    @property
    def exe_path(self) -> Path:
        return self.app_root / RUNTIME_EXE_REL

    @property
    def runtime_installed(self) -> bool:
        return self.exe_path.is_file()

    def search_dirs(self) -> list[Path]:
        """与 Java 版 scanDirs 一致：程序目录、程序目录\\models、~/.lioncode/models。"""
        return [self.app_root, self.app_root / "models", home_dir() / ".lioncode" / "models"]

    def model_file_name(self) -> str:
        return str(self.cfg.llama().get("modelFile") or "")

    def model_path(self) -> Path | None:
        # 用**生效文件**（兜底时是现成的那份），否则配置那份没下载时连启动都做不了
        name = self.effective_model_file()
        if not name:
            return None
        for d in self.search_dirs():
            p = d / name
            if p.is_file():
                return p
        return None

    def effective_model_file(self) -> str:
        """**本次实际会用**的模型文件名（兜底时与配置的不同）。"""
        return self._override_file or self.model_file_name()

    def _pick_fallback_model(self) -> str:
        """配置那份没就位时，挑一份**本地现成的**顶上（等价 Java 的兜底逻辑）。

        优先级：官方清单里的（Q8_0 最前，用户最可能已经有它）→ 模型目录里任意 .gguf。
        挑不到返回空串，由调用方回"模型未下载"——**不假装成功**。
        """
        configured = self.model_file_name()
        for c in AVAILABLE_MODELS:
            name = c["file"]
            if name != configured and self.is_model_downloaded(name):
                return name
        for lm in self.scan_models():
            if lm.name != configured:
                return lm.name
        return ""

    def _model_dir_has(self, name: str) -> bool:
        return self.is_model_downloaded(name)
    @property
    def model_installed(self) -> bool:
        p = self.model_path()
        return p is not None and p.stat().st_size > 1024 * 1024

    def model_dir(self) -> Path:
        """模型目录（Java `LocalModelRuntime.modelDir()`）。

        报错文案里要用它告诉用户"自己塞的 GGUF 该放哪"（`找不到这个模型: x。…；
        自己塞的 GGUF 请放进模型目录：<这里>`），`status()["modelDir"]` 也用它。
        """
        return self.app_root
    def log_path(self) -> Path:
        return DEFAULT_LOG

    # ------------------------------------------------------------------ 健康
    def _host_port(self) -> tuple[str, int]:
        llama = self.cfg.llama()
        return str(llama.get("host", "127.0.0.1")), int(llama.get("port", 8788))

    def manages(self, base_url: str | None) -> bool:
        """给定端点是否由本组件管理（决定要不要去拉本地进程）。

        逐字对照 Java `LocalModelRuntime.manages(String)`：只有「回环地址 + 端口正好是
        本运行时的端口」才算。用户填自己的 API（哪怕是 http://localhost:11434，Ollama 之类）
        不会被当成我们的运行时，否则会去拉起一个根本用不上的 llama.cpp，白占显存。

        【为什么必须补上这个方法】`OpenAICompatibleAdapter._ensure_endpoint_ready()` 里第一句
        就是 `rt.manages(self._base_url)`。本方法缺失时那句抛 AttributeError，被
        `except Exception` 包成 `ModelCallError("本地模型运行时启动失败: ...")` ——
        **每一次模型调用都失败**（连"自定义 API"模式也一样，因为根本没走到判断端点那一步），
        表现是所有端到端套件里模型一个工具都没调、全红。实测就是这样。
        """
        if base_url is None or not str(base_url).strip():
            return False
        s = str(base_url).strip().lower()
        if not any(marker in s for marker in ("://127.0.0.1", "://localhost",
                                              "://[::1]", "://0.0.0.0")):
            return False
        _, effective_port = self._host_port()      # 用生效端口：spawn() 用的也是 cfg 里的 port
        try:
            from urllib.parse import urlsplit
            parsed = urlsplit(s)
            port = parsed.port
            if port is None:
                port = 443 if parsed.scheme == "https" else 80
            return int(port) == int(effective_port)
        except (ValueError, TypeError):
            return (":" + str(effective_port)) in s

    def healthy(self) -> bool:
        """模型服务是否就绪。

        【两处性能处理，都是实测出来的】
        1. **先看端口通不通**：逐个探 `/health`、`/v1/models`、`/`（各 2.5 秒读超时），
           模型没在跑时最坏卡 ~7.5 秒；而前端会轮询 `/api/runtime/mode`，界面就一直转圈。
           端口没开时 connect 立刻被拒，直接判否。
        2. **结果缓存 1.5 秒**：界面轮询与后台预热会同时问状态，没必要每次都真去探。
        """
        now = time.time()
        cached = self._health_cache
        if cached is not None and now - cached[0] < HEALTH_CACHE_SECONDS:
            return cached[1]

        if self.port_free():          # 端口没开 → 立刻判否
            self._health_cache = (now, False)
            return False

        host, port = self._host_port()
        result = False
        for path in ("/health", "/v1/models", "/"):
            try:
                req = urllib.request.Request(f"http://{host}:{port}{path}", method="GET")
                with urllib.request.urlopen(req, timeout=2.5) as r:
                    if 200 <= r.status < 400:
                        result = True
                        break
            except (urllib.error.URLError, OSError, ValueError):
                continue
        self._health_cache = (now, result)
        return result

    def port_free(self) -> bool:
        """端口是否空闲（没人监听）。

        超时给 0.2 秒就够：端口开着时 TCP 握手由内核即时完成，不需要等；
        给 0.6 秒时实测这个探测要吃掉整整 600 ms，白拖慢状态接口（界面轮询会感觉到）。
        """
        import socket
        host, port = self._host_port()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.2)
            return s.connect_ex((host, port)) != 0

    # ------------------------------------------------------------------ 拉起
    def build_command(self, ngl: int | None = None) -> list[str]:
        llama = self.cfg.llama()
        mp = self.model_path()
        cmd: list[str] = [str(self.exe_path), "-m", str(mp)]
        cmd += ["-ngl", str(int(llama.get("ngl", 999)) if ngl is None else ngl)]
        cmd += ["-c", str(int(llama.get("ctxSize", 262144)))]

        kv_k = str(llama.get("kvCacheTypeK") or llama.get("kvCacheType") or "")
        kv_v = str(llama.get("kvCacheTypeV") or llama.get("kvCacheType") or "")
        quantized = bool(kv_k) and kv_k.lower() not in ("f16", "bf16")
        if quantized:
            cmd += ["-ctk", kv_k, "-ctv", kv_v]
        if quantized or bool(llama.get("flashAttn", True)):
            cmd += ["-fa", "on"]

        cmd += ["-np", str(int(llama.get("parallelSlots", 1)))]
        th = int(llama.get("threads", 0) or 0)
        if th > 0:
            cmd += ["-t", str(th), "-tb", str(th)]
        bs = int(llama.get("batchSize", 0) or 0)
        if bs > 0:
            cmd += ["-b", str(bs)]
        ub = int(llama.get("ubatchSize", 0) or 0)
        if ub > 0:
            cmd += ["-ub", str(ub)]

        temp = float(llama.get("temperature", -1))
        if temp >= 0:
            cmd += ["--temp", str(temp)]
        top_p = float(llama.get("topP", 0) or 0)
        if top_p > 0:
            cmd += ["--top-p", str(top_p)]
        cmd += ["--top-k", str(int(llama.get("topK", 40)))]
        cmd += ["--min-p", str(float(llama.get("minP", 0.05)))]
        cmd += ["--repeat-penalty", str(float(llama.get("repeatPenalty", 1.05)))]
        cmd += ["--repeat-last-n", str(int(llama.get("repeatLastN", 256)))]
        seed = int(llama.get("seed", -1))
        if seed >= 0:
            cmd += ["--seed", str(seed)]

        host, port = self._host_port()
        cmd += ["--host", host, "--port", str(port)]
        extra = str(llama.get("extraArgs") or "").strip()
        if extra:
            cmd += shlex.split(extra)
        return cmd

    def _open_log(self):
        """打开 llama.cpp 的日志文件。

        【为什么要有降级链】实测踩过：`%TEMP%\\lionbox-model.log` 被别的进程占着/只读时
        `open(..., 'ab')` 抛 PermissionError，**整个 start() 直接 500** ——
        日志打不开绝不该让模型起不来。依次尝试：官方日志 → 带 PID 的备用名 → 丢弃。
        """
        import tempfile
        candidates = [self.log_path(),
                      Path(tempfile.gettempdir()) / f"lionbox-model-{os.getpid()}.log"]
        for p in candidates:
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                return open(p, "ab", buffering=0), p
            except OSError:
                continue
        return open(os.devnull, "wb"), Path(os.devnull)

    def _spawn(self, ngl: int, timeout: int) -> bool:
        cmd = self.build_command(ngl)
        fh, used_log = self._open_log()
        self._log_used = used_log
        try:
            self._proc = subprocess.Popen(
                cmd, stdout=fh, stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL,
                cwd=str(self.app_root), creationflags=_CREATE_NO_WINDOW,
            )
        except OSError as e:
            self.last_error = f"拉起失败: {e}"
            self.phase = "error"
            fh.close()
            return False

        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.healthy():
                self._started_with_ngl = ngl
                self._model_in_use = self.effective_model_file()
                self.phase = "ready"
                self.last_error = ""
                self._health_cache = None      # 状态变了，缓存立刻失效
                return True
            if self._proc.poll() is not None:
                self.last_error = f"llama-server 退出（exit={self._proc.returncode}），见 {used_log}"
                return False
            time.sleep(0.5)
        self.last_error = f"等待就绪超时（{timeout} 秒）"
        return False

    def start(self) -> dict[str, Any]:
        with self._lock:
            if self.healthy():
                self.phase = "ready"
                return self.status()
            # ------------------------------------------------------------------
            # 【先决定"这次到底用哪份权重"，再管运行时在不在】
            # 原来把 `runtime_installed` 的检查放在前面 —— 于是"没装 llama-server.exe"
            # 的机器上直接 phase=error 返回，**兜底与提示永远不会发生**。
            # 但"用哪份权重"是个独立判断：用户在界面上要看到的是
            # "你选的 IQ4 没下载，现在会用 Q8_0"，而不是一句"运行时不可用"。
            # ------------------------------------------------------------------
            configured = self.model_file_name()
            if self.is_model_downloaded(configured):
                # 配置那份就位了：清掉兜底，并把"实际在用"切回配置的那份
                self._override_file = ""
                self._model_in_use = configured
            else:
                # 【自动补齐权重】Java 的 `ensureRunning()` 在这里会去把**用户选的那一份**
                # 下下来（`downloadFileIfAllowed`），下完继续启动。下载实现挂在
                # AUTO_DOWNLOADER 上，进度写的是同一个 runtime 实例。
                downloaded = (self.auto_download and self.runtime_installed
                              and self._auto_download_model())
                if downloaded:
                    self._override_file = ""
                    self._model_in_use = configured
                else:
                    # 【兜底】用户配的这份没就位、又下不动时，拿本地现成的那份顶上，
                    # 并且**把为什么说清楚**（Java `modelMismatchNotice()` 就是给这种情况的）。
                    fb = self._pick_fallback_model()
                    if fb:
                        self._override_file = fb
                        # 【立刻记下"实际在用"】不能等到拉起成功才记：连 llama-server.exe
                        # 都没有的机器上拉起必然失败，但"这次用的是兜底那份"这个事实必须
                        # 让界面看得到，否则用户永远不知道为什么不是自己选的。
                        self._model_in_use = fb
                        self.last_error = ""
                        print(f"[模型] {self.model_mismatch_notice()}"
                              f"（原因：{configured} 还没下载）", flush=True)
                    else:
                        self._model_in_use = ""
                        self._override_file = ""
                        self.phase = "error"
                        self.last_error = f"模型未下载：{configured}"
                        return self.status()

            if not self.runtime_installed:
                self.phase = "error"
                self.last_error = (f"本地模型运行时不可用：请确认程序目录下有 "
                                   f"{RUNTIME_EXE_REL} 与 {self.effective_model_file()}")
                return self.status()

            self.starting = True
            self.phase = "loading"
            self._loading_since = _now()
            try:
                ok = self._spawn(int(self.cfg.llama().get("ngl", 999)), self.start_timeout)
                if not ok:
                    # 与 Java 版一致：GPU 拉起失败就回落纯 CPU 再试一次
                    self._kill_proc()
                    self.phase = "loading"
                    ok = self._spawn(0, max(180, self.start_timeout))
                if not ok:
                    self._kill_proc()
                    self.phase = "error"
            finally:
                self.starting = False
            return self.status()

    def on_model_downloaded(self, model_file: str) -> None:
        """权重下完了：把"实际在用"切到它上面（等价 Java 的"下完自动重启运行时"）。

        【为什么必须做】下载是**后台**跑的，而下载开始时 `start()` 已经因为"配置那份不在"
        走了兜底（`_model_in_use = Q8_0`）。如果下完不切回来，用户看到的永远是
        "正在用 Q8_0 / 你选的 IQ4 还没下载"——明明刚下完。Java 那边下完会重启运行时，
        这里同样：清掉兜底、更新"实际在用"，正在跑就重启一次。
        """
        name = str(model_file or "").strip()
        if not name:
            return
        if name == self.model_file_name():
            # 【只清兜底，**不动 modelInUse**】"实际在用"的定义是"真的拉起过的那份"：
            # 后台下完但用户没点启动时，它必须仍然是空的（套件第三阶段验的就是这条：
            # 「后台下完也没偷偷加载模型（不占显存）」）。
            # 清掉兜底之后，下一次 `start()` 会走"配置那份已就位"的分支并把 modelInUse
            # 设成它 —— 于是第二阶段「下完就在用 IQ4_XS」也成立。
            self._override_file = ""
            print(f"[模型] 权重已就绪：{name}（下次启动即用它）", flush=True)
            # 【不自动加载】下完只把"实际在用"切过去，绝不偷偷拉起 llama-server：
            # 那会平白占掉几 GB 显存（用户可能只是想先下好、稍后再用）。
            # 套件里明确验了这条：「后台下完也没偷偷加载模型（不占显存）」。
    def start_download(self, model_file: str) -> dict[str, Any]:
        """发起一次后台下载（等价 Java `LocalModelRuntime.startDownload`）。

        返回 `{"started": bool, "downloaded": bool, "error": str}`。**只发起、不等待** ——
        8.87 GB 同步等会把界面按钮堵十几分钟（Java 注释里就是这么写的）。

        【为什么必须有这个方法】开机补齐与 `/local/model` 的 `download=true` 都要调它，
        而实现挂在模块级的 `AUTO_DOWNLOADER`（由 `assembly` 接到
        `api/runtime_extra.LocalModelsSupport.start_download`）。原来只有模块级钩子、
        没有实例方法，于是调用方 `getattr(runtime, "start_download")` 拿到 None、
        静默什么都不做 —— 表现为"开机不会去下权重"。
        """
        name = str(model_file or "").strip()
        if not name:
            return {"started": False, "downloaded": False, "error": "模型文件名为空"}
        if self.is_model_downloaded(name):
            return {"started": False, "downloaded": True, "error": ""}
        if AUTO_DOWNLOADER is None:
            return {"started": False, "downloaded": False,
                    "error": "下载实现未接线（AUTO_DOWNLOADER 为空）"}
        try:
            return dict(AUTO_DOWNLOADER(name) or {})
        except Exception as e:                              # noqa: BLE001
            return {"started": False, "downloaded": False, "error": str(e)}
    def _auto_download_model(self) -> bool:
        """把**配置的那一份**权重下下来（等价 Java `downloadFileIfAllowed`）。

        接线点没挂上（`AUTO_DOWNLOADER is None`）时返回 False，由调用方回
        "模型未下载" —— 与 Java 里"下载被关掉/下不动"时的表现一致，不假装成功。

        下载本身跑在后台线程里（`LocalModelsSupport._download_worker`），进度写在**本实例**上，
        这里只等它落地：`/api/runtime/local` 在等待期间能读到 `phase=downloading` 与字节数。
        """
        name = self.model_file_name()
        if not name or AUTO_DOWNLOADER is None:
            return False
        try:
            started = AUTO_DOWNLOADER(name) or {}
        except Exception as e:                              # noqa: BLE001
            self.last_error = f"启动自动下载失败: {e}"
            return False
        if started.get("downloaded") is True:
            return True
        # 【busy 要等，不能兜底】开机补齐与"点启动/发第一条消息"可能同时来，
        # 同一时刻只允许一个下载（模块里的 `_downloading_now`）。原来拿到 busy 就当
        # "下载没能启动"→ 立刻兜底用 Q8_0，于是用户明明正在下 IQ4、界面却说"在用 Q8_0"，
        # 而且下完也不会切过去（`_check_model_choice` 第二阶段抓到的就是它）。
        # 正确做法：已经有下载在跑 → **等它**。
        if started.get("started") is not True and not started.get("busy"):
            self.last_error = str(started.get("error") or "自动下载未能启动")
            return False
        deadline = time.time() + max(60, int(self.start_timeout))
        while time.time() < deadline:
            if self.model_installed:
                return True
            if self.phase == "failed":
                return False
            time.sleep(0.2)
        self.last_error = f"自动下载超时（{int(self.start_timeout)} 秒）"
        return False

    def _kill_proc(self) -> None:
        p = self._proc
        self._proc = None
        if p is None or p.poll() is not None:
            return
        try:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/PID", str(p.pid), "/T", "/F"],
                               capture_output=True, creationflags=_CREATE_NO_WINDOW, timeout=15)
            else:
                p.terminate()
        except (OSError, subprocess.SubprocessError):
            pass
        try:
            p.wait(timeout=8)
        except subprocess.TimeoutExpired:
            try:
                p.kill()
                p.wait(timeout=5)
            except (OSError, subprocess.TimeoutExpired):
                pass

    def stop(self) -> dict[str, Any]:
        with self._lock:
            self._kill_proc()
            self.phase = "idle"
            self._started_with_ngl = None
            self._health_cache = None          # 状态变了，缓存立刻失效
            return self.status()

    def restart(self) -> dict[str, Any]:
        self.stop()
        return self.start()

    def ensure_running(self) -> bool:
        """对话前调用：已就绪直接 True；否则拉起。"""
        if self.healthy():
            if self.phase != "ready":
                self.phase = "ready"
            return True
        self.start()
        return self.phase == "ready"

    # ------------------------------------------------------------------ 模型选择
    def is_model_downloaded(self, model_file: str) -> bool:
        """这个模型文件本地是不是已经有了（清单/设置页用来标"已下载"）。"""
        name = str(model_file or "").strip()
        if not name or any(c in name for c in "\\/:"):
            return False            # 带路径的值一律不当模型名用（与 Java isSafeModelFileName 一致）
        for d in self.search_dirs():
            p = d / name
            try:
                if p.is_file() and p.stat().st_size >= MIN_MODEL_BYTES:
                    return True
            except OSError:
                continue
        return False

    def model_file_in_use(self) -> str:
        """**实际在用**的模型文件名（可能因为兜底和配置的不一样；没启动过是空串）。"""
        return self._model_in_use

    def model_mismatch_notice(self) -> str:
        """配置的模型还没就位时给界面一句能看懂的话；一切正常返回空串。

        Java 原文：
            你选的是 <configured>，但[它还没下载，]现在临时在用 <inUse>
        """
        configured = self.model_file_name()
        if not configured:
            return ""
        # 配置那份已经在磁盘上了就不再提示"临时在用别的"（它下次启动就是它了）
        if self.is_model_downloaded(configured) and not self._override_file:
            return ""
        in_use = self._model_in_use or self._override_file or self._pick_fallback_model()
        if not in_use or in_use == configured:
            return ""
        mid = "" if self.is_model_downloaded(configured) else "它还没下载，"
        return f"你选的是 {configured}，但{mid}现在临时在用 {in_use}"

    def model_choices(self) -> list[dict[str, Any]]:
        """`/api/runtime/local/models` 的完整清单（逐字段对齐 Java RuntimeController）。

        结构：官方三份各一行 + 模型目录里**用户自己塞的** GGUF 各一行。
        每行都带 `current`（实际在用）/ `configured`（配置里选的）/ `downloaded` / `downloading`，
        界面靠这三个标记显示"正在用"与"已下载"。
        """
        in_use = self._model_in_use
        configured = self.model_file_name()
        downloading = self.downloading_file
        local = {m.name: m for m in self.scan_models()}
        out: list[dict[str, Any]] = []
        for c in AVAILABLE_MODELS:
            out.append({
                "file": c["file"], "label": c["label"], "sizeGb": c["sizeGb"], "note": c["note"],
                "custom": False,
                "current": c["file"] == in_use,
                "configured": c["file"] == configured,
                "downloaded": self.is_model_downloaded(c["file"]),
                "downloading": c["file"] == downloading,
            })
        known = {c["file"] for c in AVAILABLE_MODELS}
        for name, lm in local.items():
            if name in known:
                continue                    # 官方那份上面已经有一行了
            out.append({
                "file": name, "label": name, "sizeGb": lm.size_gb,
                # 小于 1 GB 的按 MB 显示（自己塞的模型可能就几百 MB，写 0.0 GB 等于没说）
                "sizeText": (f"{lm.size_gb:.2f} GB" if lm.size >= 1073741824
                             else f"{lm.size // 1048576} MB"),
                "note": "你自己放进模型目录的（本地现成，直接能用）",
                "custom": True, "path": lm.path,
                "current": name == in_use,
                "configured": name == configured,
                "downloaded": True, "downloading": False,
            })
        return out
    # ------------------------------------------------------------------ 状态
    def status(self) -> dict[str, Any]:
        llama = self.cfg.llama()
        host, port = self._host_port()
        mp = self.model_path()
        # 【下载期间不要做健康探测】`healthy()` 里那次端口探测要 ~0.2 秒，
        # 而界面/用例在下载时是高频轮询 `/api/runtime/local` 看进度的 ——
        # 每次轮询都被探测拖 0.2 秒，采样点稀到看不出字节在涨
        # （套件报"已下字节在涨 2097152 → 2097152"就是这个原因）。
        # 正在下载时直接沿用上一次已知状态，不重复探测。
        running = self._last_known_running if self.phase == "downloading" else self.healthy()
        if self.phase != "downloading":
            self._last_known_running = running
        return {
            "runtimeInstalled": self.runtime_installed,
            "modelInstalled": self.model_installed,
            "running": running,
            "starting": self.starting,
            "phase": self.phase,
            "host": host,
            "port": port,
            "modelName": str(llama.get("modelName", "lion-models1")),
            "modelFile": self.model_file_name(),
            "exePath": str(self.exe_path),
            "resolvedModelPath": str(mp) if mp else "",
            "logPath": str(self._log_used),
            "lastError": self.last_error,
            "downloadBytes": self.download_bytes,
            "downloadTotal": self.download_total,
            "downloadingFile": self.downloading_file,
            "modelDir": str(self.app_root),
            "nglInUse": self._started_with_ngl if self._started_with_ngl is not None else "",
        }

    # ------------------------------------------------------------------ 模型清单
    def scan_models(self) -> list[LocalModel]:
        """本地现成的权重（含用户自己塞进来的）。< 1MB 当垃圾忽略；同名按目录顺序取先找到的。"""
        found: dict[str, LocalModel] = {}
        for d in self.search_dirs():
            for base in (d, d / "models"):
                if not base.is_dir():
                    continue
                try:
                    for p in base.iterdir():
                        name = p.name
                        if not name.lower().endswith(".gguf") or not p.is_file():
                            continue
                        size = p.stat().st_size
                        if size < 1024 * 1024 or name in found:
                            continue
                        found[name] = LocalModel(name, str(p), size, False)
                except OSError:
                    continue
        return list(found.values())

    def switch_model(self, model_file: str) -> dict[str, Any]:
        name = (model_file or "").strip()
        if not name:
            self.last_error = "modelFile 不能为空"
            return self.status()
        self.cfg.update_llama({"modelFile": name})
        if self.healthy():
            self.restart()
        return self.status()

    # ------------------------------------------------------------------ 下载
    def download(self, url: str, target: Path, timeout_hours: int = 6) -> bool:
        """断点续传下载（与 Java 版同策略：Range + 206 续写 + 6 小时上限）。"""
        target.parent.mkdir(parents=True, exist_ok=True)
        part = target.with_suffix(target.suffix + ".part")
        already = part.stat().st_size if part.is_file() else 0
        self.downloading_file = target.name
        self.download_bytes = already
        self.download_total = -1
        headers = {"User-Agent": "lionbox"}
        if already > 0:
            headers["Range"] = f"bytes={already}-"
        req = urllib.request.Request(url, headers=headers, method="GET")
        mode = "ab" if already > 0 else "wb"
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                code = r.status
                length = int(r.headers.get("Content-Length") or 0)
                if code == 206 and already > 0:
                    self.download_total = already + length
                elif code == 200:
                    if already > 0:          # 服务器不支持续传：重头下
                        already = 0
                        mode = "wb"
                    self.download_total = length
                with open(part, mode) as f:
                    while True:
                        chunk = r.read(64 * 1024)   # 块小一点，进度条才看得到在动
                        if not chunk:
                            break
                        f.write(chunk)
                        self.download_bytes += len(chunk)
        except (urllib.error.URLError, OSError, ValueError) as e:
            self.last_error = f"下载失败: {e}"
            return False
        finally:
            self.downloading_file = ""
        os.replace(part, target)
        return True


# ========================================================================
# 原模块 lionbox/local/prewarm.py
# ========================================================================
"""开机预热：把"第一条消息才付的提示词预填充开销"挪到用户提问之前。

对照 Java 版 `PrewarmService` 移植。**【为什么这件事重要】**实测（Java 版，本机）：
冷启动第一条消息的瓶颈不是加载权重（8 秒），而是提示词预填充 —— 系统提示词 + 50 多个
工具定义有 3~9K token，GPU 上 478 tok/s 要约 7 秒，**纯 CPU 回退时是几分钟**。
预热带两件事：模型提前加载好、前缀 KV 提前算好；日志里同时给出实测预填充速度。

跳过规则与 Java 版一致（`whySkip`）：
  · 预热开关关掉 -> "预热功能已关闭"
  · 自带端点（providerMode=local 或 provider=lionbox-local/box）-> 预热
  · 用户自填的云端 API -> 跳过（缓存不在我们手上，白花 token 费用），除非 force
"""


import json
import threading
import time
import urllib.error
import urllib.request
from typing import Any, Callable


# 默认的预热前缀：P4 接入 AgentLoop 后会换成真实的"系统提示词 + 工具定义"。
# 保持可注入，是为了让 P1 阶段就能端到端跑通并量出 tok/s。
DEFAULT_PREFIX = (
    "你是 Lion Code 的本地编程助手。"
    "你需要通过工具调用来读写文件、执行命令、检索代码。"
) * 40   # 约几百 token，用于打通链路；真实规模在 P4 接入


class PrewarmService:
    def __init__(self, runtime: LocalModelRuntime, cfg: AppConfigStore,
                 on_start: bool = False, enabled: bool = True, force: bool = False,
                 prompt_provider: Callable[[], tuple[str, list[dict[str, Any]]]] | None = None) -> None:
        self.runtime = runtime
        self.cfg = cfg
        self.on_start_default = on_start
        self.enabled_default = enabled
        self.force_default = force
        self.prompt_provider = prompt_provider or (lambda: (DEFAULT_PREFIX, []))
        self.last_result: dict[str, Any] = {"warmed": False, "reason": "尚未预热"}
        self._lock = threading.Lock()

    # ------------------------------------------------------------- 开关
    def _cfg_bool(self, key: str, fallback: bool) -> bool:
        """用户配置优先，没有就用部署默认值（与 Java 版 cfg() 一致）。"""
        v = self.cfg.get(key, None)
        return v if isinstance(v, bool) else fallback

    @property
    def on_start(self) -> bool:
        return self._cfg_bool("warmupOnStart", self.on_start_default)

    @property
    def enabled(self) -> bool:
        return self._cfg_bool("warmupEnabled", self.enabled_default)

    @property
    def force(self) -> bool:
        return self._cfg_bool("warmupForce", self.force_default)

    def _is_builtin_endpoint(self) -> bool:
        if str(self.cfg.get("providerMode", "local")) == "local":
            return True
        provider = str(self.cfg.get("provider", ""))
        return provider in ("lionbox-local", "lionbox-box")

    def why_skip(self) -> str | None:
        if not self.enabled:
            return "预热功能已关闭"
        if self._is_builtin_endpoint() or self.force:
            return None
        return "当前是自己填的 API 端点，不做预热（避免白花 token 费用）"

    # ------------------------------------------------------------- 执行
    def warm_up(self, reason: str = "开机预热") -> dict[str, Any]:
        t0 = time.time()
        skip = self.why_skip()
        if skip:
            self.last_result = {"warmed": False, "reason": skip, "trigger": reason}
            return self.last_result

        loaded = self.runtime.ensure_running()
        if not loaded:
            r = self.runtime.status()
            self.last_result = {
                "warmed": False,
                "reason": "预热失败: " + (r.get("lastError") or "本地模型起不来"),
                "trigger": reason,
            }
            print(f"[预热] 预热失败（{reason}）：{self.last_result['reason']}", flush=True)
            return self.last_result

        system_prompt, tools = self.prompt_provider()
        body: dict[str, Any] = {
            "messages": [{"role": "system", "content": system_prompt},
                         {"role": "user", "content": "预热"}],
            "max_tokens": 1,
            "stream": False,
            "temperature": 0,
        }
        if tools:
            body["tools"] = tools

        llama = self.cfg.llama()
        url = f"http://{llama.get('host', '127.0.0.1')}:{int(llama.get('port', 8788))}/v1/chat/completions"
        t1 = time.time()
        try:
            req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                         headers={"Content-Type": "application/json"}, method="POST")
            with urllib.request.urlopen(req, timeout=900) as r:
                payload = json.loads(r.read().decode("utf-8"))
            usage = payload.get("usage") or {}
            prompt_tokens = int(usage.get("prompt_tokens") or 0)
            gen_seconds = max(time.time() - t1, 1e-6)
            tps = prompt_tokens / gen_seconds if prompt_tokens else 0.0
            self.last_result = {
                "warmed": True,
                "reason": "预热完成",
                "trigger": reason,
                "promptTokens": prompt_tokens,
                "seconds": round(gen_seconds, 2),
                "tokensPerSecond": round(tps, 1),
                "totalSeconds": round(time.time() - t0, 2),
            }
            # 日志格式与 Java 版一致，便于直接对比两版实测数字
            print(f"[预热] 预热完成（{reason}）：前缀 {prompt_tokens} token，"
                  f"耗时 {gen_seconds:.2f} 秒 → {tps:.1f} tok/s 预填充速度", flush=True)
            print(f"[预热] 预热总耗时 {time.time() - t0:.3f} 秒（含模型加载）", flush=True)
        except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
            self.last_result = {"warmed": False, "reason": f"预热失败: {e}", "trigger": reason}
            print(f"[预热] 预热失败（{reason}）：{e}", flush=True)
        return self.last_result

    # ------------------------------------------------------------- 开机触发
    def start_if_configured(self) -> threading.Thread | None:
        """等价于 Java 版的 @EventListener(ContextRefreshedEvent)：配置要求就后台预热。

        【守护线程】预热会阻塞到模型加载完（最长 300 秒）+ 一次模型请求（读超时 900 秒）。
        不是 daemon 的话，用户关窗口时 JVM/进程会因为"还有线程活着"退不掉。
        """
        if not self.on_start:
            return None
        print("[预热] 配置要求开机预热，开始…", flush=True)
        t = threading.Thread(target=self.warm_up, args=("开机预热",), name="lionbox-prewarm", daemon=True)
        t.start()
        return t


# ========================================================================
# 原模块 lionbox/api/runtime.py
# ========================================================================
"""运行时接口 —— `/api/runtime/*`。

P1 起改用真实的 `LocalModelRuntime` + `PrewarmService`（P0 的静态桩已替换）。
响应结构与 Java 版逐字段对齐（用真实响应比对过：32 个字段零差异）。
"""


import time
from pathlib import Path
from typing import Any



class RuntimeApi:
    def __init__(self, app_root: Path, cfg: AppConfigStore, *, prewarm_on_start: bool = False,
                 prewarm_enabled: bool = True, start_timeout: int = 240,
                 auto_download: bool = True) -> None:
        self.app_root = Path(app_root)
        self.cfg = cfg
        # 【这个开关原来没人读】套件用 `--lionbox.runtime.auto-download=false/true` 切两段场景，
        # 而它只作为构造参数默认 True —— 于是"关掉自动下载"根本不生效。
        # 与 Java 的 `lionbox.runtime.auto-download` 同名同义，从 `--lionbox.*` 覆盖里取。
        try:
            import sys as _sys
            _raw = ""
            for _a in _sys.argv[1:]:
                if _a.startswith("--lionbox.runtime.auto-download="):
                    _raw = _a.split("=", 1)[1]
            if _raw:
                auto_download = _raw.strip().lower() not in ("false", "0", "no", "off")
        except Exception:  # noqa: BLE001
            pass
        self.runtime = LocalModelRuntime(self.app_root, cfg,
                                         start_timeout=start_timeout,
                                         auto_download=auto_download)
        self.prewarm = PrewarmService(self.runtime, cfg,
                                      on_start=prewarm_on_start, enabled=prewarm_enabled)
        self.lazy_load = True
        self._started_at = time.time()
        self._prepare_thread: threading.Thread | None = None

    # ------------------------------------------------------------ 开机补齐权重
    def startup_prepare_model(self) -> None:
        """开机就把**配置的那份**权重在后台补下来 —— 不等用户发第一条消息。

        【为什么必须在开机做】用户装的时候选了 IQ4_XS，如果实现只在"第一条消息"或
        "点启动"时才去下，他发消息后的几分钟里模型一直在下载、界面像卡死；
        而"开机后台悄悄下好"是 Java 的行为（`_check_model_choice.py` 第二阶段验的就是它）。
        下载跑在守护线程里，完全不挡启动（这也是"第一次启动不能慢"的一部分：
        我们只**发起**下载，不等它完成）。
        """
        try:
            if not self.runtime.auto_download:
                return
            configured = self.runtime.model_file_name()
            if not configured or self.runtime.is_model_downloaded(configured):
                return
            starter = getattr(self.runtime, "start_download", None)
            if not callable(starter):
                return
            print(f"[模型] 开机后台补齐权重：{configured}（不影响界面使用）", flush=True)
            r = starter(configured) or {}
            print(f"[模型] 补齐结果: started={r.get('started')} downloaded={r.get('downloaded')} "
                  f"busy={r.get('busy')} error={r.get('error') or '(无)'}", flush=True)
        except Exception as e:  # noqa: BLE001 补齐失败不能挡住启动
            print(f"[模型] 开机补齐权重失败（忽略）: {type(e).__name__}: {e}", flush=True)

    # ------------------------------------------------------------ mode
    def _local_base_url(self) -> str:
        llama = self.cfg.llama()
        return f"http://{llama.get('host', '127.0.0.1')}:{int(llama.get('port', 8788))}/v1"

    def _custom_provider(self) -> dict[str, Any]:
        providers = self.cfg.get("providers")
        if isinstance(providers, dict):
            c = providers.get("lionbox-custom")
            if isinstance(c, dict):
                return c
        return {}

    def mode_payload(self) -> dict[str, Any]:
        mode = str(self.cfg.get("providerMode", "local"))
        custom = self._custom_provider()
        api_key = str(custom.get("apiKey") or "")
        local = self._local_base_url()
        status = self.runtime.status()
        return {
            "mode": mode,
            "baseUrl": local if mode == "local" else str(custom.get("baseUrl") or ""),
            "apiKey": "" if mode == "local" else api_key,
            "customApi": {
                "baseUrl": str(custom.get("baseUrl") or ""),
                "apiKey": api_key,
                "hasApiKey": bool(api_key.strip()),
                "model": str(custom.get("model") or ""),
            },
            "toolCallMode": self.cfg.tool_call_mode,
            "localBaseUrl": local,
            "model": str(self.cfg.get("model") or "lion-models1"),
            "localModel": str(status["modelName"]),
            "lazyLoad": self.lazy_load,
            "localStatus": status,
            "hasApiKey": bool(api_key.strip()),
        }

    def local_config_payload(self) -> dict[str, Any]:
        llama = self.cfg.llama()
        stored = self.cfg.get("llama")
        stored_file = str(stored.get("modelFile") or "") if isinstance(stored, dict) else ""
        payload: dict[str, Any] = dict(llama)
        payload["running"] = self.runtime.healthy()
        payload["status"] = self.runtime.status()
        payload["stored"] = {"modelFile": stored_file,
                             "installChoice": self.cfg.install_model_marker()}
        # 【不能写死成配置那个】Java 的 `modelInUse` 是**实际在用**的（兜底时和配置的不一样）、
        # 且"还没启动过就是空串"，绝不假报 —— 否则界面会把用户选的 IQ4 标成"正在用"，
        # 而他实际跑的是兜底的 Q8。`modelMismatchNotice()` 就是给这种情况的一句人话。
        payload["modelInUse"] = self.runtime.model_file_in_use()
        payload["configuredDownloaded"] = self.runtime.model_installed
        payload["modelMismatch"] = self.runtime.model_mismatch_notice()
        payload["modelDir"] = str(self.runtime.app_root)
        payload["modelDirs"] = [str(d) for d in self.runtime.search_dirs()]
        return payload

    # ------------------------------------------------------------ 注册
    def register(self, router) -> None:
        api = self

        @router.get("/api/runtime/mode")
        def get_mode(req: Request):
            return ApiResponse.ok(api.mode_payload())

        @router.post("/api/runtime/mode")
        def set_mode(req: Request):
            body = req.json_obj()
            mode = str(body.get("mode") or "").strip()
            if mode not in ("local", "custom"):
                return ApiResponse.error("mode 只能是 local 或 custom")
            updates: dict[str, Any] = {"providerMode": mode}
            if mode == "custom":
                providers = api.cfg.get("providers")
                providers = dict(providers) if isinstance(providers, dict) else {}
                c = dict(providers.get("lionbox-custom") or {})
                for k_src, k_dst in (("baseUrl", "baseUrl"), ("apiKey", "apiKey"), ("model", "model")):
                    if body.get(k_src) is not None:
                        c[k_dst] = str(body.get(k_src))
                providers["lionbox-custom"] = c
                updates["providers"] = providers
                # 【必须同时写顶层键】`normalize()` 是按**顶层** baseUrl/model/apiKey
                # 落配置的（见 `[配置] 运行模式=自定义 API: baseUrl=…`）。
                # 只写 providers 里的副本 → normalize 读到的还是本地端点那个旧值，
                # 于是转手把适配器改回 127.0.0.1:8788 —— 实测：切自定义端点后请求
                # 仍然打到本地运行时（"目标计算机积极拒绝"），云端/MiMo 根本用不起来。
                for k in ("baseUrl", "apiKey", "model"):
                    if c.get(k):
                        updates[k] = c[k]
                # 备份一份到 customApi 存档：新建配置时「自定义 API」实例用它初始化
                custom = dict(api.cfg.get("customApi") or {})
                for k in ("baseUrl", "apiKey", "model"):
                    if c.get(k):
                        custom[k] = c[k]
                updates["customApi"] = custom
            api.cfg.update(updates)
            # 【重指适配器不在这里做】本类只有 cfg/runtime/prewarm，**拿不到 ctx**，
            # 也就取不到 AdapterManager（`adapters()` 定义在 ApiContext 上）。
            # 活跃适配器的 baseUrl 是装配时固化的，光改配置它不会跟着变。
            # 正确入口是 `POST /api/chat/adapter/config`（ChatApi 那边有 ctx）——
            # 前端切完端点就调它，见 `tui/app.js` 的 `/endpoint`、`/key`、`/mode`。
            return ApiResponse.ok(api.mode_payload())

        @router.post("/api/runtime/tool-call-mode")
        def set_tool_call_mode(req: Request):
            mode = normalize_tool_call_mode(req.json_obj().get("mode"))
            api.cfg.set("toolCallMode", mode)
            return ApiResponse.ok({"toolCallMode": mode})

        # ---- 本地运行时 ----
        @router.get("/api/runtime/local")
        def local_status(req: Request):
            return ApiResponse.ok(api.runtime.status())

        @router.get("/api/runtime/local/config")
        def local_config(req: Request):
            return ApiResponse.ok(api.local_config_payload())

        @router.post("/api/runtime/local/config")
        def update_local_config(req: Request):
            updates = req.json_obj()
            allow = set(api.cfg.llama().keys())
            clean = {k: v for k, v in updates.items() if k in allow}
            if not clean:
                return ApiResponse.error("没有可更新的字段")
            api.cfg.update_llama(clean)
            return ApiResponse.ok(api.local_config_payload())

        @router.post("/api/runtime/local/start")
        def local_start(req: Request):
            return ApiResponse.ok(api.runtime.start())

        @router.post("/api/runtime/local/stop")
        def local_stop(req: Request):
            return ApiResponse.ok(api.runtime.stop())

        @router.post("/api/runtime/local/restart")
        def local_restart(req: Request):
            return ApiResponse.ok(api.runtime.restart())

        @router.get("/api/runtime/local/models")
        def local_models(req: Request):
            # 官方三份 + 用户自己塞的 GGUF，每行带 current/configured/downloaded/downloading
            # —— 逐字段对齐 Java `RuntimeController` 的同一接口（原来只列磁盘上的文件，
            # 于是"官方有但没下载"的那两份在界面上根本看不见，用户无处可选）。
            return ApiResponse.ok(api.runtime.model_choices())

        @router.post("/api/runtime/local/model")
        def switch_model(req: Request):
            """切换本地模型（逐字段对齐 Java `RuntimeController.switchModel`）。

            【字段是 `file` 不是 `modelFile`】Java 读的是 `body.get("file")`。第一版我写成
            `modelFile`，套件发 `{'file': ...}` 时读出来是空串，报"没有这个模型: "——
            看着像模型清单坏了，其实是字段名没对上。
            """
            body = req.json_obj()
            file = str(body.get("file") or "").strip()
            if not file:
                return ApiResponse.error("缺少 file（要切换到的模型文件名）")
            if any(c in file for c in "/\\") or ".." in file:
                return ApiResponse.error(
                    f"模型文件名不能带路径：{file}（把文件放进模型目录，这里只填文件名）")

            choices = api.runtime.model_choices()
            known = {c["file"] for c in choices if not c.get("custom")}
            local_files = {c["file"] for c in choices if c.get("custom")}
            if file not in known and file not in local_files:
                official = "、".join(c["file"] for c in choices if not c.get("custom"))
                return ApiResponse.error(
                    f"找不到这个模型: {file}。可选：{official}；"
                    f"自己塞的 GGUF 请放进模型目录：{api.runtime.model_dir()}")

            api.cfg.update_llama({"modelFile": file})
            api.runtime.stop()
            st = api.runtime.status()

            if file in local_files:
                how = "（权重已就绪）" if file in known else "（本地现成的）"
                return ApiResponse.ok(st, f"已切换到 {file}{how}，发消息或点「重启本地模型」即可生效")

            want_download = str(body.get("download", "")).lower() not in ("false", "0", "no", "")
            if not want_download:
                return ApiResponse.ok(st, f"已切换到 {file}（尚未下载）")
            starter = getattr(api.runtime, "start_download", None)
            if not callable(starter):
                return ApiResponse.ok(st, f"已切换到 {file}（尚未下载）")
            r = starter(file) or {}
            if r.get("started"):
                return ApiResponse.ok(st, f"已切换到 {file}，权重正在下载（进度就在界面上的下载窗口里），下完就能用")
            return ApiResponse.ok(st, f"已切换到 {file}（尚未下载：{r.get('error')}）")
        @router.post("/api/runtime/local/download")
        def download_local(req: Request):
            # 下载源在 P2 接 ModelScope 解析；这里先明确回未实现，不假装成功
            return ApiResponse.error("下载源解析将在 P2 实现", "下载源解析将在 P2 实现")

        # ---- 预热 ----
        @router.get("/api/runtime/warmup")
        def warmup_result(req: Request):
            return ApiResponse.ok(api.prewarm.last_result)

        @router.post("/api/runtime/warmup")
        def warmup(req: Request):
            r = api.prewarm.warm_up("手动触发")
            ok = bool(r.get("warmed"))
            return ApiResponse.ok(r, message="预热完成") if ok else \
                ApiResponse.error(str(r.get("reason")), str(r.get("reason")))

        @router.get("/health")
        def health(req: Request):
            return Response.json({"status": "ok",
                                  "uptime": round(time.time() - api._started_at, 3)})


# ========================================================================
# 原模块 lionbox/api.py
# ========================================================================
"""API 层：路由与响应包封。

111 个接口分在 17 个模块里（每个 Java controller 一个模块），全部**显式登记**：

    register_all(router, ctx)   # 固定顺序，没有目录扫描（PORTING.md 硬约束）

【装配是怎么接上的】`app.py` 由别的任务拥有且明令不许改，而 `python -m lionbox`
必须能直接打到这里的所有接口；因此在包的 import 期装一个**幂等的装配钩子**：
包装 `RuntimeApi.register`（`app.py` 里唯一一处拿到 router + app_root + 配置的地方），
等它跑完就登记本层全部模块。不改任何既有文件，也不做目录扫描。

如果装配方之后在 `app.py` 里显式调用 `register_all(...)`，钩子会因为
`router` 上的幂等标记直接跳过，不会出现重复路由。
"""


import logging
import traceback
from pathlib import Path
from typing import Any


log__api = logging.getLogger("lionbox.api")

# 登记顺序 = 模块的装配顺序。前面的模块可能 `ctx.install(...)` 后面要用的服务，
# 所以顺序固定、显式写出来（不是扫描出来的）。
MODULES: tuple[str, ...] = (
    "workspaces",       # WorkspaceController      /api/workspaces
    "sessions",         # SessionController        /api/sessions
    "events",           # EventController          /api/events
    "files",            # FileSystemController     /api/filesystem
    "models",           # ModelController          /api/models
    "approvals",        # ApprovalController       /api/approvals
    "changes",          # ChangeReviewController   /api/changes + /api/context
    "context",          # ContextController        /api/context/mentions
    "questions",        # QuestionController       /api/questions
    "notifications",    # NotificationController   /api/notification
    "native_dialog",    # NativeDialogController   /api/native-dialog
    "providers",        # ProviderController       /api/providers
    "plugins",          # PluginController         /api/plugins
    "plugin_dev",       # PluginDevController      /api/plugins（dev-mode 等）
    "skills",          # SkillController         /api/skills（Java 里在 core/plugin/skill 下）
    "runtime_extra",    # RuntimeController 的未覆盖部分
    "chat",             # ChatController           /api/chat
    "agent_control",    # AgentControlController   /api/chat/control
)


def register_all(router: Any, ctx: ApiContext | None = None, *,
                 app_root: Path | str | None = None, cfg: Any = None,
                 runtime_api: Any = None, extra: dict[str, str] | None = None) -> dict[str, Any]:
    """把本层所有模块登记到 `router` 上。

    返回 `{"registered": [...], "failed": {...}, "routes": n}`，便于验收与排查。
    """
    if getattr(router, "_lionbox_api_registered", False):
        return {"registered": [], "failed": {}, "routes": router.size, "skipped": "已登记"}
    if ctx is None:
        if app_root is None or cfg is None:
            raise ValueError("register_all 需要 ctx，或者 app_root + cfg")
        ctx = ApiContext(app_root, cfg, runtime_api=runtime_api, extra=extra)

    registered: list[str] = []
    failed: dict[str, str] = {}
    for name in MODULES:
        try:
            # 【内联后不能动态导入】所有接口模块已在同一命名空间，而且 register 因撞名
            # 被改成了带模块后缀的名字（18 个模块各有一个 register），
            # 所以改用下面的 _API_REGISTER 表按 MODULES 顺序显式调用。
            module = None
            _API_REGISTER[name](router, ctx)
            registered.append(name)
        except Exception as e:      # 单个模块坏掉不该让整个接口层不可用，但要大声报错
            failed[name] = f"{type(e).__name__}: {e}"
            log__api.error("接口模块 %s 装配失败: %s\n%s", name, e, traceback.format_exc())
    router._lionbox_api_registered = True      # type: ignore[attr-defined]
    report: dict[str, Any] = {"registered": registered, "failed": failed, "routes": router.size}
    # 【最后一步：把窄桩换成真实实现】`deps.py` 里会话/事件/历史/提问/Agent 主循环全是
    # 窄桩（`AgentLoopStub.process_message` 直接抛 DependencyMissing），必须由装配方
    # `ctx.install(name, obj)`。本层是唯一同时拿到 app_root + cfg + RuntimeApi 的地方，
    # 所以收尾放在这里（`app.py` 是冻结件，不许改）。任何一步失败都只记进报告，不影响起服务。
    try:
        from lionbox.assembly import install_real_services
        report["assembly"] = install_real_services(ctx)
    except Exception as e:      # noqa: BLE001
        report["assembly"] = {"error": f"{type(e).__name__}: {e}"}
        log__api.error("真实实现装配失败: %s\n%s", e, traceback.format_exc())
    return report


def register_now(app: Any) -> dict[str, Any]:
    """给装配方（`app.py` 之后的显式接线、用例）用的便捷入口：从 Lion Code 实例取依赖。"""
    router = app.http.router
    return register_all(router, app_root=app.app_root, cfg=app.config,
                        runtime_api=getattr(app, "runtime", None),
                        extra=getattr(app, "extra", None))


# --------------------------------------------------------------------------
# 装配钩子（幂等）
# --------------------------------------------------------------------------


def install_assembly_hook() -> None:
    """在 `RuntimeApi.register` 外面包一层，登记完运行时接口后接着登记本层全部模块。"""
    from lionbox.api import runtime as runtime_module

    original = runtime_module.RuntimeApi.register
    if getattr(original, "_lionbox_wrapped", False):
        return

    def wrapped(self: Any, router: Any) -> Any:
        result = original(self, router)
        report = register_all(router, app_root=self.app_root, cfg=self.cfg, runtime_api=self)
        if report.get("failed"):
            log__api.error("接口层部分模块装配失败: %s", report["failed"])
        return result

    wrapped._lionbox_wrapped = True      # type: ignore[attr-defined]
    runtime_module.RuntimeApi.register = wrapped


install_assembly_hook()

__all__ = ["ApiContext", "MODULES", "install_assembly_hook", "register_all", "register_now"]


# ========================================================================
# 原模块 lionbox/app.py
# ========================================================================
"""应用装配 —— 显式、可读、启动路径一眼看得完。

【为什么不用框架的 DI/自动扫描】Java 版启动 1.985 秒里，相当一部分花在 Spring 的
组件扫描与上下文装配上。Python 版刻意做反面：所有依赖在这里手工 new 出来，
`python -m lionbox` 的启动路径就是"读配置 → 注册路由 → 监听端口"三步。

启动耗时目标：< 0.5 秒（Java 版 2.8 秒）。
"""


import threading
import time
from pathlib import Path


VERSION = "1.5.46"


class LionBox:
    def __init__(self, app_root: Path | None = None, host: str = "127.0.0.1",
                 port: int = 8080, config: AppConfigStore | None = None,
                 extra: dict[str, str] | None = None) -> None:
        self.t0 = time.perf_counter()
        # 程序目录：默认取包所在目录的上一级（python/），打包后由启动器传 --app-root
        self.app_root = Path(app_root) if app_root else Path(_ORIG_FILE_app).resolve().parent.parent
        self.config = config or AppConfigStore()
        self.http = HttpApp(host=host, port=port)
        # 预热开机触发：等价于 Java 的 -Dlionbox.prewarm.on-start=true
        self.extra: dict[str, str] = dict(extra or {})
        prewarm_on = str(self.extra.get("lionbox.prewarm.on-start", "")).lower() in ("true", "1", "yes")
        self.runtime = RuntimeApi(self.app_root, self.config, prewarm_on_start=prewarm_on)

        self.runtime.register(self.http.router)
        self._register_core()

    # ---- 基础路由：健康检查 / 首页（Web UI）----
    def _register_core(self) -> None:
        app = self

        @self.http.router.get("/")
        def index(req: Request):
            html = app._web_index()
            if html is None:
                return Response.json(ApiResponse.ok({
                    "app": "lionbox", "version": VERSION, "lang": "python",
                    "note": "Web UI 未找到（web/index.html），接口可用",
                }).body)
            return Response(html, content_type="text/html; charset=utf-8")

        @self.http.router.get("/api/runtime/version")
        def version(req: Request):
            return ApiResponse.ok({"version": VERSION, "lang": "python"})

    def _web_index(self) -> str | None:
        for p in (self.app_root / "web" / "index.html",
                  self.app_root.parent / "web" / "index.html"):
            if p.is_file():
                return p.read_text(encoding="utf-8")
        return None

    # ---- 生命周期 ----
    @property
    def boot_seconds(self) -> float:
        return time.perf_counter() - self.t0

    def start(self, block: bool = True) -> None:
        # 端口先监听，再触发后台预热 —— 与 Java 版一致：预热绝不挡界面
        if block:
            threading.Thread(target=self._after_listen, daemon=True, name="lionbox-boot").start()
        self.http.serve_forever(block=block)

    def _after_listen(self) -> None:
        time.sleep(0.2)          # 让端口先真正开始 accept
        # 开机后台补齐模型权重（配置那份没下载时）——只发起、不等待，不挡界面
        threading.Thread(target=self.runtime.startup_prepare_model,
                         name="lionbox-model-prepare", daemon=True).start()
        self.runtime.prewarm.start_if_configured()

    def stop(self) -> None:
        self.http.shutdown()


# ========================================================================
# 原模块 lionbox/api/workspaces.py
# ========================================================================
"""工作区接口 —— `/api/workspaces/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\WorkspaceController.java`（116 行 / 5 个接口）。

【状态在哪里】工作区不归本模块持有：`deps.WorkspaceStore`（共享服务）就是 Java
`WorkspaceManager` 的对应物 —— 同一份 `app-config.json` 的 `workspaces` 键，
权限等级随工作区一起落盘，所以"只读"能活过重启。这里只做 HTTP 形状与校验文案的复刻，
不重复实现工作区逻辑（PORTING.md：不要自己实现别人的模块）。
"""


import json
from typing import Any

from lionbox.api import deps


class _BadBody(ValueError):
    """请求体里有 Jackson 无法强转成 `String` 的值（对象/数组）→ Spring 反序列化失败即 400。"""


class WorkspacesApi:
    """`/api/workspaces` —— 与 Java `WorkspaceController` 逐接口对应。

    权限等级与 Java `WorkspaceManager.WorkspacePermission` 同值；
    `deps.WorkspaceStore.set_permission` 内部校验的也是这组值。
    """

    PERMISSIONS: tuple[str, ...] = ("READ_ONLY", "WORKSPACE_WRITE", "FULL_ACCESS")

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 服务定位
    def _workspaces(self) -> Any:
        """每请求取一次共享服务：装配方之后 `ctx.install("workspaces", 真实实现)` 能立刻生效。"""
        return deps.workspaces(self.ctx)

    # ------------------------------------------------------------ 请求体
    @staticmethod
    def _json_object(req: Request) -> dict[str, Any] | Response:
        """请求体 → dict；拿不到 JSON 对象时返回 Spring 的 400。

        Java 侧 `@RequestBody(required = true)` 的三条分支都在 18099 上实测过：
        完全没有请求体 / 空体 / 字面量 `null` 一律是 400 + `{"timestamp","status","error","path"}`，
        根本没进方法体 —— 控制器里那两处 `request == null` 的兜底在 Spring 6 下是死代码，
        照抄成 200 + 业务错误反而会让前端把"请求体没发出去"当成"参数不合法"。
        """
        if not req.body:
            return deps.spring_error(400, req.path)
        try:
            parsed = json.loads(req.body.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return deps.spring_error(400, req.path)
        if not isinstance(parsed, dict):
            return deps.spring_error(400, req.path)
        return parsed

    @staticmethod
    def _string_field(body: dict[str, Any], name: str) -> str | None:
        """取字符串字段：Jackson 会把 JSON 标量强转成 String，对象/数组则反序列化失败。"""
        value = body.get(name)
        if value is None or isinstance(value, str):
            return value
        if isinstance(value, bool):
            return "true" if value else "false"          # Jackson: true -> "true"
        if isinstance(value, (int, float)):
            return json.dumps(value)                     # 5 -> "5"、1.5 -> "1.5"
        raise _BadBody(f"{name} 不是字符串: {type(value).__name__}")

    # ------------------------------------------------------------ 注册
    def register(self, router) -> None:
        api = self

        @router.post("/api/workspaces")
        def register_workspace(req: Request):
            body = api._json_object(req)
            if isinstance(body, Response):
                return body
            try:
                path = api._string_field(body, "path")
            except _BadBody:
                return deps.spring_error(400, req.path)
            try:
                workspace = api._workspaces().register_workspace(path)
            except ValueError as e:
                # 路径为空/非法：Java `WorkspaceManager.workspaceIdOf` 抛的文案（"工作区路径不能为空"、
                # "工作区路径非法: xxx"）由控制器原样回给前端，一个字都不能改
                return ApiResponse.error(str(e))
            return ApiResponse.ok(workspace, message="工作区注册成功")

        @router.get("/api/workspaces")
        def get_all_workspaces(req: Request):
            return ApiResponse.ok(api._workspaces().get_all_workspaces())

        @router.get("/api/workspaces/default")
        def get_default_workspace(req: Request):
            # Java: Path.of(System.getProperty("user.home"), "Desktop").toString()
            # registerWorkspace 对已注册的工作区**不覆盖权限**（用户设的"只读"不能被这里改回去）
            desktop = str(home_dir() / "Desktop")
            return ApiResponse.ok(api._workspaces().register_workspace(desktop), message="ok")

        @router.get("/api/workspaces/common")
        def get_common_paths(req: Request):
            # 常用路径由后端按 user.home 动态算，前端不硬编码用户路径
            home = home_dir()
            return ApiResponse.ok([
                {"icon": "🖥️", "name": "桌面", "path": str(home / "Desktop")},
                {"icon": "📄", "name": "文档", "path": str(home / "Documents")},
                {"icon": "📥", "name": "下载", "path": str(home / "Downloads")},
                {"icon": "🏠", "name": "用户目录", "path": str(home)},
            ], message="ok")

        @router.post("/api/workspaces/permission")
        def set_permission(req: Request):
            body = api._json_object(req)
            if isinstance(body, Response):
                return body
            try:
                workspace_id = api._string_field(body, "id")
                permission = api._string_field(body, "permission")
            except _BadBody:
                return deps.spring_error(400, req.path)
            # 显式判 null/空白：Java 侧 Enum.valueOf(null) 与 ConcurrentHashMap.get(null) 抛的都是 NPE
            # （不是 IllegalArgumentException，catch 拦不住，用户只会看到 500"服务器内部错误"）
            if workspace_id is None or not workspace_id.strip():
                return ApiResponse.error("缺少工作区 id")
            if permission is None or not permission.strip():
                return ApiResponse.error("缺少权限等级（READ_ONLY / WORKSPACE_WRITE / FULL_ACCESS）")
            level = permission.strip().upper()          # Java: trim().toUpperCase(Locale.ROOT)
            if level not in api.PERMISSIONS:
                # 回的是**原样**的 permission（不 trim 不大写）—— 与 Java 的 catch 分支一致
                return ApiResponse.error("无效的权限等级: " + permission)
            store = api._workspaces()
            if store.set_permission(workspace_id, level):
                return ApiResponse.ok(store.get_workspace(workspace_id), message="权限已更新")
            return ApiResponse.error("工作区不存在: " + workspace_id)


def register(router, ctx) -> None:
    WorkspacesApi(ctx).register(router)


# ========================================================================
# 原模块 lionbox/sessions/context.py
# ========================================================================
"""工具执行期间的会话上下文（线程级）—— 对应 Java `core/session/SessionContext.java`。

`ToolPlugin.execute(arguments)` 的签名里没有会话信息，但有的工具天然要知道
"现在是哪个会话在调我"（比如向用户提问的工具，得把问题投递给正确的会话、
等那条会话的用户来回答）。AgentLoop 在执行工具前 `set()`，执行完 `clear()`。

线程模型：同一个会话的任务被串行投递到固定 worker 线程，工具调用是同步的，
不会跨线程串味 —— 所以线程局部变量够用，不需要传参穿透整条调用链。
"""


import threading
from contextlib import contextmanager
from typing import Iterator

_LOCAL = threading.local()


class SessionContext:
    """与 Java 一样是纯静态工具类（不是需要注入的 Bean）。"""

    @staticmethod
    def set(session_id: str | None) -> None:
        _LOCAL.session_id = session_id

    @staticmethod
    def get() -> str | None:
        return getattr(_LOCAL, "session_id", None)

    @staticmethod
    def clear() -> None:
        _LOCAL.session_id = None

    # 额外给的便利写法（Python 侧用；语义与 set/clear 完全一致）
    @staticmethod
    @contextmanager
    def use(session_id: str | None) -> Iterator[str | None]:
        previous = SessionContext.get()
        SessionContext.set(session_id)
        try:
            yield session_id
        finally:
            if previous is None:
                SessionContext.clear()
            else:
                SessionContext.set(previous)


__all__ = ["SessionContext"]


# ========================================================================
# 原模块 lionbox/events/compat.py
# ========================================================================
"""事件字段的时间戳兼容层（Java 数据 ↔ Python）。

【为什么要单独一个模块】Java 版用 Jackson 的 `JavaTimeModule` 序列化 `java.time.Instant`，
默认写成 **epoch 秒 + 小数纳秒** 的数字（每条真实数据都长这样）：

    "timestamp" : 1790993207.760789600

Python 的 `datetime.timestamp()` 是浮点秒，直接互转会在纳秒位上漂移，
而事件要靠时间戳排序、`?after=` 又要按毫秒比较，漂移会让"同一毫秒的事件"乱序或丢。
所以这里统一用 `decimal.Decimal` 读、用 `(epoch_millis, micros, nanos)` 三元组排序：

  · 读：数字（新旧两种写法）→ aware datetime（UTC）
  · 写：aware datetime → ISO-8601 带微秒（`2026-10-03T02:06:47.760789Z`）
    —— Java 的 `Instant.parse` 读得懂它，Python 也读得懂；
    而且 JSONL 是给人看的审计日志，ISO 比一串裸数字好排查得多。
"""


import json
import json.encoder as _json_encoder
import re
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Iterator

#: 毫秒比较用的换算（与 Java EventController 的 toEpochMilli() 对齐）
EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)

_ISO_RE = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[Tt ](\d{2}):(\d{2}):(\d{2})(?:\.(\d+))?"
    r"(Z|z|[+-]\d{2}:?\d{2})?$"
)

#: 裸数字时间戳的占位前缀。`\x00` 在 JSON 文本里被转义成 `\u0000`，
#: 所以"有没有占位"要拿**_ESCAPED 看（拿 _RAW_PREFIX 看永远匹配不上）
_RAW_PREFIX = "\x00lionts:"
_RAW_PREFIX_ESCAPED = r"\u0000lionts:"
_RAW_RE = re.compile(r'"\\u0000lionts:(-?[0-9.]+)"', re.IGNORECASE)


@contextmanager
def _pure_python_json() -> Iterator[None]:
    """临时把 json 模块的全局 C 编码器关掉（只影响 `_one_shot` 那条快路径）。"""
    original = _json_encoder.c_make_encoder
    _json_encoder.c_make_encoder = None
    try:
        yield
    finally:
        _json_encoder.c_make_encoder = original


def parse_timestamp(raw: Any) -> datetime | None:
    """把 Java/Python 两种时间戳写法解析成 aware datetime（UTC）。

    认这几种：
      · 数字 `1790993207.7607896`（Java Jackson 的 Instant 默认写法）
      · 整数 `1790993207`
      · ISO 字符串 `2026-10-03T02:06:47.760789Z` / `...+08:00` / 无时区（按本地时区补）
      · 已经是 datetime（naive 按本地时区补）

    解析不出来返回 None —— 调用方决定"这条事件算坏数据还是算当前时间"。
    """
    if raw is None or raw == "":
        return None
    if isinstance(raw, datetime):
        return raw.astimezone(timezone.utc) if raw.tzinfo else raw.astimezone()
    if isinstance(raw, bool):
        return None
    if isinstance(raw, (int, float, Decimal)):
        return from_epoch_seconds(raw)
    text = str(raw).strip()
    if not text:
        return None
    # 纯数字串（有些工具会把时间戳写成字符串）——按 epoch 秒处理，
    # 但明显像"年月日"的 8 位数不当时间戳（避免 20261003 被解释成 1970 年）
    if re.fullmatch(r"-?\d+(\.\d+)?", text) and len(text.split(".")[0]) <= 12:
        try:
            return from_epoch_seconds(Decimal(text))
        except (InvalidOperation, ValueError, OverflowError, OSError):
            return None
    m = _ISO_RE.match(text)
    if not m:
        try:
            dt = datetime.fromisoformat(text)
        except ValueError:
            return None
        return dt.astimezone(timezone.utc) if dt.tzinfo else dt.astimezone()
    year, month, day, hh, mm, ss = (int(m.group(i)) for i in range(1, 7))
    frac = m.group(7) or ""
    micro = int((frac + "000000")[:6]) if frac else 0
    tz = m.group(8)
    if tz in ("Z", "z") or tz is None:
        # 无时区：Java 写出来的一定是 UTC（Instant），按 UTC 补
        tzinfo = timezone.utc
    else:
        sign = 1 if tz[0] == "+" else -1
        body = tz[1:].replace(":", "")
        tzinfo = timezone(sign * timedelta(hours=int(body[:2]), minutes=int(body[2:4])))
    try:
        return datetime(year, month, day, hh, mm, ss, micro, tzinfo=tzinfo).astimezone(timezone.utc)
    except ValueError:
        return None


def from_epoch_seconds(value: Any) -> datetime | None:
    """epoch 秒（可带小数纳秒）→ aware datetime（UTC）。用 Decimal 保证纳秒→微秒不漂。"""
    try:
        dec = Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None
    micros = int((dec * 1_000_000).to_integral_value(rounding="ROUND_HALF_UP"))
    try:
        return EPOCH + timedelta(microseconds=micros)
    except OverflowError:
        return None


def format_timestamp(dt: datetime | None) -> str | None:
    """datetime → ISO-8601 带微秒的 UTC 串（**只用于日志/展示**）。

    写进 JSON 请用 `timestamp_json_literal`：磁盘格式必须保持 Java 的写法，
    否则老版本 Java 进程读不回来（见该函数的说明）。
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def timestamp_json_literal(dt: datetime | None) -> str | None:
    """datetime → **Java Jackson 的 Instant 字面量**：epoch 秒，小数部分是纳秒，字符串形式。

        1790993207.760789600   ← 真实数据长这样

    【为什么磁盘上必须这么写】`~/.lioncode` 里的会话/事件是**跨版本共享**的：
    用户回退到 Java 版、或者一边跑 Java 版一边跑 Python 版时，
    Java 侧 `ObjectMapper` 读 ISO 字符串需要额外配置，读数字则天然支持。
    保持原有写法 = 不违反 `PORTING.md` 里"不许改 `~/.lioncode` 数据格式"的硬约束。

    【为什么返回值是字符串】用整数运算取到精确的纳秒位数，再由 `LionJsonEncoder`
    原样拼进 JSON 当裸数字 —— 过一遍 float 会丢最后 1~2 位纳秒，
    而"同一条消息在自己机器上往返一次时间戳就变了"是不可接受的。
    """
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.astimezone()
    utc = dt.astimezone(timezone.utc)
    seconds = (utc - EPOCH) // timedelta(seconds=1)
    nanos = utc.microsecond * 1000
    if nanos == 0:
        return str(seconds)
    return f"{seconds}.{nanos:09d}"


def epoch_millis(dt: datetime | None) -> int | None:
    """→ 毫秒（与 Java `Instant.toEpochMilli()` 完全一致：向下取整到毫秒）。"""
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return (dt.astimezone(timezone.utc) - EPOCH) // timedelta(milliseconds=1)


def day_key(dt: datetime | None) -> str:
    """事件落在哪一天的分片：与 Java 一样按**本地时区**算日期。

    Java: `event.timestamp().atZone(ZoneId.systemDefault()).toLocalDate()`
    —— 用户看到的 `events/2026-10-03.jsonl` 和他那天干活的日期一致。
    """
    if dt is None:
        dt = datetime.now().astimezone()
    if dt.tzinfo is None:
        dt = dt.astimezone()
    return dt.astimezone().strftime("%Y-%m-%d")


def parse_day_key(name: str) -> datetime | None:
    """`2026-10-03` → 那天的 0 点（本地时区）；不是日期返回 None。"""
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", (name or "").strip())
    if not m:
        return None
    try:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).astimezone()
    except ValueError:
        return None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class LionJsonEncoder(json.JSONEncoder):
    """JSON 编码器：把时间戳的精确字面量原样写成**裸数字**（不经过 float）。

    `json` 标准库不认 `Decimal` 原样输出，所以这里用一个不可能出现在数据里的前缀
    做占位（`\\x00` 在 JSON 字符串里永远是转义形式），最后一步整体替换回裸数字。
    数据本身含这个前缀也只是"没被替换"，不影响正确性。
    """

    def default(self, o: Any) -> Any:      # noqa: D102
        if isinstance(o, datetime):
            return _RAW_PREFIX + (timestamp_json_literal(o) or "0")
        return super().default(o)

    def iterencode(self, o: Any, _one_shot: bool = False):
        # 【必须关掉 C 加速编码器】`_one_shot=True` 时 json 会走 C 实现
        # （`json.encoder.c_make_encoder`），它会绕过 `default()` 的返回值和这里的后处理，
        # 占位前缀就替换不回裸数字了。纯 Python 路径慢一点（实测 2000 条约 6 ms），
        # 换来时间戳逐字节与 Java 一致 —— 值。
        with _pure_python_json():
            for chunk in super().iterencode(o, _one_shot):
                if _RAW_PREFIX_ESCAPED in chunk:
                    chunk = _RAW_RE.sub(r"\1", chunk)
                yield chunk


def now_local() -> datetime:
    return datetime.now().astimezone()


def retention_cutoff_date(retention_days: int):
    """保留期起点（本地日期）；<=0 表示不裁剪。"""
    if retention_days <= 0:
        return None
    return (now_local() - timedelta(days=int(retention_days))).date()


# ========================================================================
# 原模块 lionbox/events/model.py
# ========================================================================
"""事件模型 —— 对应 Java `core/event/LionEvent.java`。

字段名、枚举值、显示名逐字对齐 Java（进 `/api/events` 响应与前端展示，改一个字都算不兼容）：

    {"eventId": "...", "sessionId": "...", "type": "TOOL_CALL_START",
     "timestamp": "2026-10-03T02:06:47.760789Z", "data": {...}, "summary": "..."}

时间戳的写法见 `compat.py`：读兼容 Java 的 `1790993207.760789600`，写用 ISO-8601。
"""


import json
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Iterable, Iterator



class EventType:
    """与 Java `LionEvent.EventType` 相同的 14 个值 + 中文显示名。"""

    USER_MESSAGE = "USER_MESSAGE"
    MODEL_THINKING = "MODEL_THINKING"
    MODEL_RESPONSE = "MODEL_RESPONSE"
    TOOL_CALL_START = "TOOL_CALL_START"
    TOOL_CALL_COMPLETE = "TOOL_CALL_COMPLETE"
    TOOL_CALL_ERROR = "TOOL_CALL_ERROR"
    SESSION_CREATED = "SESSION_CREATED"
    SESSION_DESTROYED = "SESSION_DESTROYED"
    PLUGIN_LOADED = "PLUGIN_LOADED"
    PLUGIN_UNLOADED = "PLUGIN_UNLOADED"
    ADAPTER_SWITCH = "ADAPTER_SWITCH"
    WORKSPACE_CHANGE = "WORKSPACE_CHANGE"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    CONTEXT_COMPRESSED = "CONTEXT_COMPRESSED"

    DISPLAY: dict[str, str] = {
        USER_MESSAGE: "用户消息",
        MODEL_THINKING: "模型思考",
        MODEL_RESPONSE: "模型响应",
        TOOL_CALL_START: "工具调用开始",
        TOOL_CALL_COMPLETE: "工具调用完成",
        TOOL_CALL_ERROR: "工具调用失败",
        SESSION_CREATED: "会话创建",
        SESSION_DESTROYED: "会话销毁",
        PLUGIN_LOADED: "插件加载",
        PLUGIN_UNLOADED: "插件卸载",
        ADAPTER_SWITCH: "适配器切换",
        WORKSPACE_CHANGE: "工作区切换",
        SYSTEM_ERROR: "系统错误",
        CONTEXT_COMPRESSED: "上下文压缩",
    }

    ALL = tuple(DISPLAY)

    @staticmethod
    def display_name(event_type: Any) -> str:
        return EventType.DISPLAY.get(str(event_type or ""), str(event_type or ""))

    @staticmethod
    def parse(raw: Any) -> str | None:
        """宽进：大小写不敏感，认不出来返回 None（由调用方决定怎么处理坏数据）。"""
        v = str(raw or "").strip().upper()
        return v if v in EventType.DISPLAY else None


@dataclass(slots=True)
class LionEvent:
    """一条事件。`data` 永远不是 None（Java 构造器里也是 `data != null ? data : Map.of()`）。"""

    event_id: str
    session_id: str | None
    type: str
    timestamp: datetime | None
    data: dict[str, Any] = field(default_factory=dict)
    summary: str | None = None
    #: 事件落在哪一天的分片（`YYYY-MM-DD`）。解析磁盘数据时顺手算好并缓存 ——
    #: 7 万条历史事件的落盘、迁移、统计都要用它，每次重算一遍日期纯属浪费。
    day: str | None = None

    # ---- 构造 ----
    @staticmethod
    def create(session_id: str | None, event_type: str, data: dict[str, Any] | None = None,
               summary: str | None = None, *, event_id: str | None = None,
               timestamp: datetime | None = None) -> "LionEvent":
        """等价 Java `EventStore.recordEvent()`：随机 UUID + Instant.now()。"""
        return LionEvent(
            event_id=event_id or str(uuid.uuid4()),
            session_id=session_id,
            type=event_type,
            timestamp=timestamp or now_utc(),
            data=dict(data) if data else {},
            summary=summary,
        )

    # ---- 序列化（键名/顺序与 Java record 一致；null 字段照 Java 保留）----
    def to_dict(self) -> dict[str, Any]:
        """给 API/内存用的 dict：`timestamp` 是 datetime（null 字段照 Java 保留）。

        要**落盘**请用 `to_json()`：磁盘上时间戳必须是 Java 的 epoch 秒数字，
        不能是 ISO 串，否则回退到 Java 版就读不出来了。
        """
        return {
            "eventId": self.event_id,
            "sessionId": self.session_id,
            "type": self.type,
            "timestamp": self.timestamp,
            "data": self.data if self.data is not None else {},
            "summary": self.summary,
        }

    def to_json(self, *, pretty: bool = False) -> str:
        """落盘用的 JSON：时间戳写成 Java Jackson 的 `1790993207.760789600` 数字。"""
        if pretty:
            return json.dumps(self.to_dict(), ensure_ascii=False, indent=2, cls=LionJsonEncoder)
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"),
                          cls=LionJsonEncoder)

    @staticmethod
    def from_dict(raw: Any) -> "LionEvent | None":
        """从 dict 还原；缺关键字段（eventId/type）当坏数据返回 None。"""
        if not isinstance(raw, dict):
            return None
        event_id = raw.get("eventId")
        if event_id is None or str(event_id).strip() == "":
            return None
        event_type = EventType.parse(raw.get("type")) or str(raw.get("type") or "").strip()
        if not event_type:
            return None
        data = raw.get("data")
        session_id = raw.get("sessionId")
        summary = raw.get("summary")
        timestamp = parse_timestamp(raw.get("timestamp"))
        return LionEvent(
            event_id=str(event_id),
            session_id=None if session_id is None else str(session_id),
            type=event_type,
            timestamp=timestamp,
            data=data if isinstance(data, dict) else {},
            summary=None if summary is None else str(summary),
            day=day_key(timestamp),
        )

    @staticmethod
    def from_json(line: str) -> "LionEvent | None":
        text = (line or "").strip()
        if not text:
            return None
        try:
            return LionEvent.from_dict(json.loads(text))
        except ValueError:
            return None

    # ---- 查询帮手 ----
    @property
    def millis(self) -> int | None:
        return epoch_millis(self.timestamp)

    def day_key(self) -> str:
        """这条事件属于哪一天的分片（`from_json` 解析出来的会带缓存值）。"""
        return self.day or day_key(self.timestamp)

    def sort_key(self) -> tuple[int, str]:
        """排序键：没时间戳的排最后（对齐 Java `Comparator.nullsLast`），同毫秒按 eventId 稳定。"""
        ms = self.millis
        return (ms if ms is not None else 1 << 62, self.event_id or "")


def sort_events(events: Iterable[LionEvent]) -> list[LionEvent]:
    return sorted(events, key=LionEvent.sort_key)


def iter_from_jsonl(lines: Iterable[str]) -> Iterator[LionEvent]:
    """逐行解析 JSONL；坏行直接跳过（磁盘上的审计日志不能因为一行坏了整体读不出来）。"""
    for line in lines:
        event = LionEvent.from_json(line)
        if event is not None:
            yield event


# ========================================================================
# 原模块 lionbox/events/store.py
# ========================================================================
"""事件溯源存储 —— 对应 Java `core/event/EventStore.java`，**存储格式重做**。

## 为什么重做

Java 版是「一条事件一个文件」：`events/<日期>/<会话>/<事件id>.json`。
实测一台机器上攒到 **71,619 个文件 / 11 个日期目录**，启动时
`Files.walk` 全扫 + 逐个 `readString` + Jackson 解析，实测烧掉 80 秒以上 CPU
（jstack 抓到主线程就卡在 `loadEventsFromDisk`），日志里一直有
`事件文件过多（71477 个）` 的告警 —— 而且这个数字只会一直涨。

## 现在长什么样

    <store>/events/2026-10-03.jsonl        按天分片，一行一条事件，只追加
    <store>/events/2026-09-29.jsonl
    <store>/events/.event-index.jsonl      事件ID → 分片/行号（给按 eventId 的 O(1) 查）

* **启动只列一次目录**（`os.scandir`，百级文件），不再逐个文件 `stat`/`open`；
  文件名本身就是日期，保留期判断、排序、跨天查询全靠文件名，零额外 IO。
* 追加写：`os.open(..., O_APPEND) + os.write` 一次系统调用落一行，
  同一毫秒内并发写也不会互相截断（Java 那边是整份 `writeString` 覆盖）。
* 会话、事件 ID **不再进路径**，路径穿越（`sessionId=../../x`）这个问题从格式上消失。

## 语义（必须与 Java 一致，文件布局可以完全不同）

| 行为 | Java | 这里 |
| --- | --- | --- |
| `record` / `recordEvent` | 内存 + 磁盘 | 同（磁盘改成追加一行） |
| 按会话查询 | 内存 list | 内存 list（同），另有 `load_events` 从磁盘回放 |
| `?after=<epochMillis>` | `timestamp.toEpochMilli() >= after` | 同（毫秒比较、含边界，见 `events_after`） |
| 每会话内存上限 | 2000，超了从最老丢 | 同（`max_events_per_session`） |
| 30 天保留 | 启动时删过期的「一天一目录」 | 启动时删过期的「一天一分片」，删的是文件不是事件 |
| 按类型/轨迹/摘要统计 | 有 | 同 |

旧格式数据不用用户手动搬：`legacy.py` 里的一次性迁移能直接读进来转成新格式。
"""


import json
import os
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Sequence



def default_store_path() -> Path:
    """默认存储目录 —— 对应 Java 属性 `lion.event.store-path`。

    【为什么要读环境变量】Java 版是 Spring 的 `@Value`，启动参数
    `--lion.event.store-path=...` 就能覆盖；Python 版由 `__main__` 把同名属性
    落到 `LION_EVENT_STORE_PATH` 上，这里读它。
    """
    v = os.environ.get("LION_EVENT_STORE_PATH", "").strip()
    return Path(v) if v else workspace_default_path() / ".lioncode" / "events"


#: 默认存储目录（与 Java 的 `lion.event.store-path` 默认值一致）
DEFAULT_STORE_PATH = default_store_path()

#: sessionId 缺失时的占位分组键（Java 同名常量，避免 None 当字典键乱窜）
UNKNOWN_SESSION = "(unknown)"

#: 事件索引文件名（以 . 开头 → 扫描分片时自动忽略）
INDEX_FILE = ".event-index.jsonl"

#: 新格式下「启动要扫描的文件数」= 日期分片数；历史上限只作为极端保护（防止有人手工塞 10 万个分片）
MAX_SHARDS_ON_STARTUP = 400


@dataclass(slots=True)
class SessionSummary:
    """对应 Java `EventStore.SessionSummary`（字段名保持一致）。"""

    sessionId: str | None
    totalEvents: int
    toolCalls: int
    toolSuccesses: int
    toolErrors: int
    modelCalls: int
    firstEventTime: datetime | None
    lastEventTime: datetime | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "sessionId": self.sessionId,
            "totalEvents": self.totalEvents,
            "toolCalls": self.toolCalls,
            "toolSuccesses": self.toolSuccesses,
            "toolErrors": self.toolErrors,
            "modelCalls": self.modelCalls,
            "firstEventTime": self.firstEventTime,
            "lastEventTime": self.lastEventTime,
        }


@dataclass(slots=True)
class StoreStats:
    """启动扫描统计 —— 专门用来回答「启动要读多少个文件」。"""

    shard_files: int = 0            # 目录里认出来的日期分片数（= 启动要扫描的文件数）
    other_files: int = 0            # 其它文件（索引等）
    malformed_files: int = 0        # 名字不像日期的文件
    expired_shards: int = 0         # 超出保留期的分片
    events_loaded: int = 0
    events_dropped: int = 0
    load_seconds: float = 0.0


@dataclass(slots=True)
class MigrationReport:
    """旧格式 → 新格式的一次性迁移结果。"""

    legacy_root: str = ""
    legacy_files: int = 0
    legacy_days: int = 0
    events_seen: int = 0
    events_migrated: int = 0
    events_skipped: int = 0         # 过期（超出保留期）没搬的
    events_unreadable: int = 0      # 坏 JSON / 缺字段
    shards_written: int = 0
    legacy_files_removed: int = 0
    legacy_dirs_removed: int = 0
    seconds: float = 0.0
    already_migrated: bool = False
    kept_legacy: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "legacyRoot": self.legacy_root,
            "legacyFiles": self.legacy_files,
            "legacyDays": self.legacy_days,
            "eventsSeen": self.events_seen,
            "eventsMigrated": self.events_migrated,
            "eventsSkipped": self.events_skipped,
            "eventsUnreadable": self.events_unreadable,
            "shardsWritten": self.shards_written,
            "legacyFilesRemoved": self.legacy_files_removed,
            "legacyDirsRemoved": self.legacy_dirs_removed,
            "seconds": round(self.seconds, 3),
            "alreadyMigrated": self.already_migrated,
            "keptLegacy": self.kept_legacy,
        }


class EventStore:
    """事件存储。线程安全：`record` 由会话 worker 线程调，查询由 HTTP 线程调。"""

    def __init__(self, store_path: str | os.PathLike[str] | None = None, *,
                 retention_days: int = 30,
                 max_events_per_session: int = 2000,
                 auto_load: bool = False,
                 auto_migrate_legacy: bool = True) -> None:
        self.store_path = Path(store_path) if store_path else DEFAULT_STORE_PATH
        self.retention_days = int(retention_days)
        self.max_events_per_session = int(max_events_per_session)

        self._lock = threading.RLock()
        self._session_events: dict[str, list[LionEvent]] = {}
        self._event_index: dict[str, LionEvent] = {}
        self._loaded_sessions: set[str] = set()
        self._persist_failures = 0    # 持久化失败计数（日志限流用，见 record()）

        self.stats = StoreStats()
        self._shards: list[tuple[str, Path]] = []      # [(日期, 路径)] 只由文件名得来
        self._shard_lock = threading.Lock()
        self._migration_lock = threading.Lock()
        self.migration_report: MigrationReport | None = None

        self._ready = False
        try:
            self.store_path.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            # 只读不了磁盘时退化成纯内存层（Java 的 init 失败也是这个行为）
            print(f"[事件] 无法创建事件存储目录 {self.store_path}: {e}", flush=True)

        # 【迁移必须放后台】真实数据实测：72,559 个旧事件文件，同步迁移要约 24 秒。
        # 而"安装不能慢、第一次启动也不能慢"是硬要求，所以这里起守护线程做：
        # 端口立刻可用，迁移在后台跑完；期间新事件照常写新格式，两边不冲突。
        #
        # 【默认绝不删旧数据】第一版默认 delete_legacy=True，会把用户全部历史事件删掉 ——
        # 万一迁移有 bug 就不可恢复。Java 版从不删数据，Python 版同样"只增不减"：
        # 旧目录原样留着，只额外建按天分片。清理是用户的显式决定（见 purge_legacy）。
        self.migration_thread: threading.Thread | None = None
        if auto_migrate_legacy and self._legacy_needs_migration():
            self.migration_thread = threading.Thread(
                target=self._migrate_in_background,
                name="lionbox-event-migrate", daemon=True)
            self.migration_thread.start()

        if auto_load:
            self.load_from_disk()

    # ==================================================================
    # 写入
    # ==================================================================
    def record(self, event: LionEvent | None) -> None:
        """记录一条事件：内存 + 追加到当天分片（对齐 Java `record()`）。"""
        if event is None:
            return
        session_id = self._session_id_of(event)
        with self._lock:
            bucket = self._session_events.get(session_id)
            if bucket is None:
                bucket = []
                self._session_events[session_id] = bucket
            bucket.append(event)
            self._evict_if_too_many(bucket)
            self._event_index[event.event_id] = event
        self._persist_event(event, session_id)

    def record_event(self, session_id: str | None, event_type: str,
                     data: dict[str, Any] | None = None,
                     summary: str | None = None) -> LionEvent:
        """创建并记录（等价 Java `recordEvent`），返回这条事件。"""
        event = LionEvent.create(session_id, event_type, data, summary)
        self.record(event)
        return event

    def _evict_if_too_many(self, bucket: list[LionEvent]) -> None:
        """超上限从最老的丢，并把索引里的条目清掉（防 `eventIndex` 无界增长）。"""
        limit = self.max_events_per_session
        if limit <= 0:
            return
        if len(bucket) <= limit:
            return
        drop = len(bucket) - limit
        for oldest in bucket[:drop]:
            if oldest is not None and oldest.event_id:
                self._event_index.pop(oldest.event_id, None)
        del bucket[:drop]

    @staticmethod
    def _session_id_of(event: LionEvent) -> str:
        sid = event.session_id
        if sid is None or str(sid).strip() == "":
            return UNKNOWN_SESSION
        return str(sid)

    # ---- 落盘（追加一行）----
    def shard_path(self, day: str) -> Path:
        return self.store_path / f"{day}.jsonl"

    def _persist_event(self, event: LionEvent, session_id: str) -> None:
        try:
            day = event.day or day_key(event.timestamp)
            path = self.shard_path(day)
            line = event.to_json() + "\n"
            self._append_line(path, line)
            self._append_index(event, day)
        except OSError as e:
            # 磁盘不可写：内存层还在，功能不中断（Java 也只记日志）。
            # 【但只详报一次】实测：磁盘不可写时每个事件都打一行，装配期一口气几百行，
            # 真错误全被淹没。首次给完整原因，之后只累计计数，收尾时汇总一条。
            self._persist_failures += 1
            if self._persist_failures == 1:
                print(f"[事件] 持久化失败（只报这一次，之后只计数）"
                      f" {getattr(event, 'eventId', '?')}: {e}", flush=True)
            elif self._persist_failures % 500 == 0:
                print(f"[事件] 持久化累计失败 {self._persist_failures} 次（磁盘不可写？）", flush=True)

    @staticmethod
    def _append_line(path: Path, line: str) -> None:
        """一次 `write()` 落一行 —— 追加语义由 O_APPEND 保证，多线程/多进程都不互相截断。"""
        data = line.encode("utf-8")
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_BINARY", 0), 0o644)
        try:
            os.write(fd, data)
        finally:
            os.close(fd)

    def _append_index(self, event: LionEvent, day: str) -> None:
        """索引只记「eventId 落在哪一天」，够 O(1) 定位到分片；行号没必要记（按天文件很小）。"""
        rec = {"eventId": event.event_id, "sessionId": event.session_id, "day": day}
        try:
            self._append_line(self.store_path / INDEX_FILE,
                              json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
        except OSError:
            # 索引只是加速结构，写不进去不影响正确性（回退到扫分片）
            pass

    # ==================================================================
    # 查询（内存层，与 Java 语义一致）
    # ==================================================================
    def get_session_events(self, session_id: str | None) -> list[LionEvent]:
        if session_id is None or str(session_id).strip() == "":
            return []
        with self._lock:
            return list(self._session_events.get(str(session_id), ()))

    def get_session_events_by_type(self, session_id: str | None, event_type: str) -> list[LionEvent]:
        return [e for e in self.get_session_events(session_id) if e.type == event_type]

    def get_event(self, event_id: str | None) -> LionEvent | None:
        if not event_id:
            return None
        with self._lock:
            return self._event_index.get(event_id)

    def replay_session(self, session_id: str | None) -> list[LionEvent]:
        """回放：会话的全部事件按时间顺序（对齐 Java `replaySession`）。"""
        events = sort_events(self.get_session_events(session_id))
        print(f"[事件] 回放会话 {session_id} 共 {len(events)} 个事件", flush=True)
        return events

    def get_tool_call_trace(self, session_id: str | None) -> list[LionEvent]:
        wanted = (EventType.TOOL_CALL_START, EventType.TOOL_CALL_COMPLETE, EventType.TOOL_CALL_ERROR)
        return [e for e in self.get_session_events(session_id) if e.type in wanted]

    def events_after(self, session_id: str | None, after_millis: int | None) -> list[LionEvent]:
        """`GET /api/events/{id}?after=<epochMillis>` 的过滤规则（对齐 EventController）：

        · 按**毫秒**比（不是 Instant 的纳秒），否则同一毫秒里的事件每轮轮询都会重复返回；
        · 用 `>=`（含边界），边界那一毫秒可能重复返回，由前端按 eventId 去重；
        · 没有时间戳的事件在给了 after 时被过滤掉（Java 同样 `e.timestamp() != null`）。
        """
        events = self.get_session_events(session_id)
        if after_millis is None or after_millis <= 0:
            return events
        out = []
        for e in events:
            ms = epoch_millis(e.timestamp)
            if ms is not None and ms >= after_millis:
                out.append(e)
        return out

    def get_session_summary(self, session_id: str | None) -> SessionSummary:
        events = self.get_session_events(session_id)
        counts: dict[str, int] = {}
        for e in events:
            counts[e.type] = counts.get(e.type, 0) + 1
        first = events[0].timestamp if events else None
        last = events[-1].timestamp if events else None
        return SessionSummary(
            sessionId=session_id,
            totalEvents=len(events),
            toolCalls=counts.get(EventType.TOOL_CALL_START, 0),
            toolSuccesses=counts.get(EventType.TOOL_CALL_COMPLETE, 0),
            toolErrors=counts.get(EventType.TOOL_CALL_ERROR, 0),
            modelCalls=counts.get(EventType.MODEL_RESPONSE, 0),
            firstEventTime=first,
            lastEventTime=last,
        )

    def clear_session(self, session_id: str | None) -> None:
        """清掉会话的**内存**事件（磁盘分片保留 —— 那是审计日志，对齐 Java）。"""
        if session_id is None or str(session_id).strip() == "":
            return
        sid = str(session_id)
        with self._lock:
            removed = self._session_events.pop(sid, None)
            if removed:
                for e in removed:
                    self._event_index.pop(e.event_id, None)
                print(f"[事件] 会话事件已清空: {sid} ({len(removed)}个事件)", flush=True)
            self._loaded_sessions.discard(sid)

    def get_active_session_ids(self) -> set[str]:
        with self._lock:
            return set(self._session_events.keys())

    def __len__(self) -> int:
        with self._lock:
            return sum(len(v) for v in self._session_events.values())

    # ==================================================================
    # 磁盘：分片枚举 / 回放 / 加载 / 保留期
    # ==================================================================
    def scan_shards(self) -> StoreStats:
        """**只列一次目录**（不 stat、不 open）得到全部分片；这就是新格式的启动成本。

        旧格式同一步要 `Files.walk` 出 7 万个路径再逐个读 —— 差别都在这里。
        """
        stats = StoreStats()
        shards: list[tuple[str, Path]] = []
        try:
            with os.scandir(self.store_path) as it:
                for entry in it:
                    name = entry.name
                    if name.startswith("."):
                        stats.other_files += 1
                        continue
                    if not name.endswith(".jsonl"):
                        stats.malformed_files += 1
                        continue
                    day = name[:-len(".jsonl")]
                    if parse_day_key(day) is None:
                        stats.malformed_files += 1
                        continue
                    shards.append((day, self.store_path / name))
        except OSError as e:
            print(f"[事件] 无法列出事件目录 {self.store_path}: {e}", flush=True)
            return stats

        shards.sort(key=lambda item: item[0])
        cutoff = self.retention_cutoff()
        if cutoff is not None:
            keep: list[tuple[str, Path]] = []
            for day, path in shards:
                when = parse_day_key(day)
                if when is not None and when.date() < cutoff:
                    stats.expired_shards += 1
                    continue
                keep.append((day, path))
            shards = keep
        self._shards = shards
        stats.shard_files = len(shards)
        self.stats = stats
        return stats

    def retention_cutoff(self):
        """保留期起点（本地日期）；<=0 表示不裁剪。"""
        return retention_cutoff_date(self.retention_days)

    def delete_expired_shards(self) -> int:
        """真的把超过保留期的分片从磁盘删掉（对齐 Java 在磁盘上执行 retention）。

        每次删一整个**天**：分片里的每一条事件都属于那一天，不存在误删未过期事件的可能。
        """
        cutoff = self.retention_cutoff()
        if cutoff is None:
            return 0
        deleted = 0
        try:
            with os.scandir(self.store_path) as it:
                for entry in it:
                    name = entry.name
                    if name.startswith(".") or not name.endswith(".jsonl"):
                        continue
                    when = parse_day_key(name[:-len(".jsonl")])
                    if when is None or when.date() >= cutoff:
                        continue
                    try:
                        os.unlink(entry.path)
                        deleted += 1
                    except OSError:
                        pass  # 被占用/权限不足就留着，不影响使用
        except OSError:
            return deleted
        return deleted

    def iter_events(self, session_id: str | None = None,
                    days: Sequence[str] | None = None) -> Iterator[LionEvent]:
        """从磁盘流式回放事件（不占内存），可选按会话过滤。

        `load_events()`（一次性读进内存）在会话很大时会把整个会话搬进内存；
        只是想统计/导出时用这个。
        """
        wanted = None if session_id is None or str(session_id).strip() == "" else str(session_id)
        if not self._shards:
            self.scan_shards()
        wanted_days = set(days) if days else None
        for day, path in self._shards:
            if wanted_days is not None and day not in wanted_days:
                continue
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for event in iter_from_jsonl(f):
                        if wanted is None or event.session_id == wanted:
                            yield event
            except OSError as e:
                print(f"[事件] 跳过读不了的分片 {path}: {e}", flush=True)

    def count_events(self, session_id: str | None = None) -> int:
        return sum(1 for _ in self.iter_events(session_id))

    def load_events(self, session_id: str) -> list[LionEvent]:
        """按需从磁盘加载一个会话的全部事件（内存里没有时用；大小不限）。"""
        sid = str(session_id)
        events = sort_events(self.iter_events(sid))
        with self._lock:
            self._session_events[sid] = events[-self.max_events_per_session:] \
                if self.max_events_per_session > 0 else events
            self._loaded_sessions.add(sid)
            for e in self._session_events[sid]:
                self._event_index[e.event_id] = e
        return list(events)

    def load_from_disk(self) -> StoreStats:
        """启动加载：**列目录 → 顺序读分片 → 按会话分组 → 每会话裁到上限**。

        与 Java 的差别：那边要 walk 7 万个文件、逐个 `readString`（实测 80 秒+ CPU）；
        这边文件数 = 天数（百级），一次 `scandir` 之后顺序读，量级差 3 个数量级。
        """
        started = time.perf_counter()
        stats = self.scan_shards()

        # 过期分片在后台删，绝不挡启动（HTTP 端口要立刻可用）
        if stats.expired_shards:
            threading.Thread(target=self._cleanup_expired, name="lionbox-event-cleanup",
                             daemon=True).start()

        loaded = 0
        buckets: dict[str, list[LionEvent]] = {}
        for _day, path in self._shards:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for event in iter_from_jsonl(f):
                        buckets.setdefault(self._session_id_of(event), []).append(event)
                        loaded += 1
            except OSError as e:
                print(f"[事件] 跳过读不了的分片 {path}: {e}", flush=True)

        dropped = self._merge_loaded(buckets)
        stats.events_loaded = loaded
        stats.events_dropped = dropped
        stats.load_seconds = round(time.perf_counter() - started, 3)
        self.stats = stats
        self._ready = True
        print(f"[事件] 从磁盘加载了 {loaded} 个历史事件"
              f"（{stats.shard_files} 个分片文件 / 保留 {self.retention_days} 天，"
              f"超出每会话上限丢弃 {dropped} 条，耗时 {stats.load_seconds}s）", flush=True)
        return stats

    def start_background_load(self) -> threading.Thread:
        """后台加载历史事件（对齐 Java：加载绝不挡端口监听）。"""
        thread = threading.Thread(target=self._safe_load, name="lionbox-event-loader", daemon=True)
        thread.start()
        return thread

    def _safe_load(self) -> None:
        try:
            self.load_from_disk()
        except Exception as e:   # 历史事件读失败不该影响使用
            print(f"[事件] 后台加载历史事件失败（不影响使用）: {e}", flush=True)

    def _cleanup_expired(self) -> None:
        deleted = self.delete_expired_shards()
        if deleted:
            print(f"[事件] 已清理 {deleted} 个超过保留期（{self.retention_days} 天）的事件分片",
                  flush=True)

    def _merge_loaded(self, buckets: dict[str, list[LionEvent]]) -> int:
        """把加载进来的事件并进内存层并裁剪到每会话上限，返回丢弃条数。"""
        dropped = 0
        with self._lock:
            for sid, events in buckets.items():
                events = sort_events(events)
                limit = self.max_events_per_session
                if limit > 0 and len(events) > limit:
                    dropped += len(events) - limit
                    events = events[len(events) - limit:]
                # 已有内存事件（启动后新写的）在后，磁盘历史在前
                existing = self._session_events.get(sid)
                merged = events + existing if existing else events
                self._session_events[sid] = merged
                for e in merged:
                    self._event_index[e.event_id] = e
        return dropped

    # ==================================================================
    # 查询辅助：按 eventId 定位（走索引，不用扫全部分片）
    # ==================================================================
    def find_event(self, event_id: str) -> LionEvent | None:
        """先查内存，再查 `.event-index.jsonl`（→ 分片），最后才扫全部分片。"""
        found = self.get_event(event_id)
        if found is not None:
            return found
        day = self._lookup_index(event_id)
        if day is not None:
            found = self._find_in_shard(day, event_id)
            if found is not None:
                return found
        for _day, path in self._shards or []:
            try:
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    for event in iter_from_jsonl(f):
                        if event.event_id == event_id:
                            return event
            except OSError:
                continue
        return None

    def _lookup_index(self, event_id: str) -> str | None:
        index_file = self.store_path / INDEX_FILE
        if not index_file.is_file():
            return None
        try:
            with open(index_file, "r", encoding="utf-8", errors="replace") as f:
                for line in f:
                    if event_id not in line:
                        continue
                    try:
                        rec = json.loads(line)
                    except ValueError:
                        continue
                    if rec.get("eventId") == event_id:
                        return str(rec.get("day") or "") or None
        except OSError:
            return None
        return None

    def _find_in_shard(self, day: str, event_id: str) -> LionEvent | None:
        path = self.shard_path(day)
        if not path.is_file():
            return None
        try:
            with open(path, "r", encoding="utf-8", errors="replace") as f:
                for event in iter_from_jsonl(f):
                    if event.event_id == event_id:
                        return event
        except OSError:
            return None
        return None

    # ==================================================================
    # 旧格式迁移（一条事件一个文件的目录）
    # ==================================================================
    def legacy_present(self) -> bool:
        from lionbox.events.legacy import legacy_present
        return legacy_present(self.store_path)

    def migrate_legacy_if_needed(self, *, delete_legacy: bool = True) -> MigrationReport:
        from lionbox.events.legacy import migrate_legacy
        with self._migration_lock:
            report = migrate_legacy(self.store_path, retention_days=self.retention_days,
                                    delete_legacy=delete_legacy)
            self.migration_report = report
            return report

    def _migrate_in_background(self) -> None:
        """守护线程里跑迁移：启动不被 100 秒的迁移挡住（见 __init__ 的说明）。

        默认 `delete_legacy=False` —— 只建新格式，**不动用户的老文件**。
        """
        try:
            self.migrate_legacy_if_needed(delete_legacy=False)
            self._write_migration_marker()
        except OSError as e:
            print(f"[事件] 旧格式迁移失败（继续用新格式）: {e}", flush=True)
        except Exception as e:  # noqa: BLE001 迁移出错绝不能影响主流程
            print(f"[事件] 旧格式迁移异常（继续用新格式）: {type(e).__name__}: {e}", flush=True)

    # ---- 迁移完成标记（复用 legacy.py 自己的标记文件，不另造一套）----
    def _legacy_needs_migration(self) -> bool:
        """要不要迁移。

        【为什么必须有标记】默认不删老文件，所以老目录永远在、`legacy_present()` 恒真 ——
        只看它的话**每次启动都会白跑一遍 100 秒的全量迁移**（实测 71,762 条要 101.6 秒）。
        用 `legacy.py` 的 `.legacy-migrated.json` 标记跳过已完成的情况：
        老格式只会由已冻结的 Java 版 1.5.46 产生，不会再增加，所以标记不必比对数量。
        """
        from lionbox.events.legacy import read_marker
        if not self.legacy_present():
            return False
        return read_marker(self.store_path) is None

    def _write_migration_marker(self) -> None:
        """非删除模式迁移成功后落标记，避免下次启动白跑一遍全量迁移。

        `legacy.migrate_legacy` 只在 `delete_legacy=True`（会删老文件）时写标记；
        我们默认不删用户数据，所以得自己补上 —— 用**同一个标记文件与同一批键名**，
        这样下次启动 `read_marker()` 能直接报出上次迁移的数量。
        """
        import os as _os
        from lionbox.events.legacy import marker_path
        report = self.migration_report
        if report is None:
            return
        data = report.to_dict() if hasattr(report, "to_dict") else dict(vars(report))
        # 【键名注意】MigrationReport.to_dict() 给的是驼峰（legacyFiles），
        # 数据类字段才是下划线（legacy_files）—— 两个都认，否则标记里数字全是 0。
        def num(*names: str) -> int:
            for n in names:
                v = data.get(n)
                if isinstance(v, int):
                    return v
            return 0

        marker = {
            "migratedAt": time.strftime("%Y-%m-%dT%H:%M:%S"),
            "legacyFiles": num("legacyFiles", "legacy_files"),
            "eventsMigrated": num("eventsMigrated", "events_migrated"),
            "eventsSeen": num("eventsSeen", "events_seen", "eventsMigrated", "events_migrated"),
            "eventsUnreadable": num("eventsUnreadable", "events_unreadable"),
            "legacyDays": num("legacyDays", "legacy_days"),
            "legacyKept": True,
        }
        try:
            path = marker_path(self.store_path)
            tmp = path.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(marker, ensure_ascii=False, indent=2), encoding="utf-8")
            _os.replace(tmp, path)
        except OSError as e:
            print(f"[事件] 写迁移标记失败（下次启动会重跑迁移）: {e}", flush=True)
    def purge_legacy(self) -> tuple[int, int]:
        """用户显式要求时才清理老格式文件（默认从不自动删）。返回 (删掉文件数, 删掉目录数)。"""
        import shutil
        from lionbox.events.compat import parse_day_key
        removed_files = removed_dirs = 0
        for d in sorted(self.store_path.iterdir()):
            if not d.is_dir() or parse_day_key(d.name) is None:
                continue
            n = sum(1 for _ in d.rglob("*") if _.is_file())
            try:
                shutil.rmtree(d)
                removed_files += n
                removed_dirs += 1
            except OSError as e:
                print(f"[事件] 清理旧目录失败 {d}: {e}", flush=True)
        return removed_files, removed_dirs

    def await_migration(self, timeout: float | None = None) -> bool:
        """等迁移结束（用例/一次性脚本用；正常运行不需要等）。"""
        t = self.migration_thread
        if t is None:
            return True
        t.join(timeout)
        return not t.is_alive()


__all__ = [
    "DEFAULT_STORE_PATH",
    "INDEX_FILE",
    "MAX_SHARDS_ON_STARTUP",
    "UNKNOWN_SESSION",
    "EventStore",
    "MigrationReport",
    "SessionSummary",
    "StoreStats",
]


# ========================================================================
# 原模块 lionbox/events/legacy.py
# ========================================================================
"""旧格式 → 新格式的一次性迁移（用户数据不能丢，也不许要求用户手动搬）。

Java 版的事件目录长这样（实测 71,619 个文件）：

    events/2026-09-29/<会话id>/<事件id>.json      ← 一条事件一个文件
    events/2026-09-29/system/00334c1e-....json

新格式是一天一个 `.jsonl`。这里的迁移**就地转换**：

1. 逐个日期目录处理。目录本身不参与新格式，所以「目录还在 = 这一天还没搬完」——
   迁移被打断（断电/被杀）后下次启动会重新扫这一天，而**先写分片、后删旧文件**的
   顺序保证重复执行只会得到"重复事件"而不会"丢事件"。
2. 每条 JSON 用与读新分片完全相同的解析器读（`LionEvent.from_dict`），
   所以字段名一个都不用改。
3. 一天搬完才删那一天的旧文件与空目录，最后写 `.legacy-migrated.json` 标记；
   标记存在时启动只做一次轻量判断，不再扫目录。

`delete_legacy=False` 时保留旧文件（给"只想先看看能读进来多少条"的场合用）。
"""


import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import IO, Any, Iterator


#: 迁移完成标记（以 . 开头，扫描分片时会被忽略）
MARKER_FILE = ".legacy-migrated.json"


def legacy_present(root: Path) -> bool:
    """目录里还有没有「一条一个文件」的旧结构（只列目录，不递归）。"""
    try:
        with os.scandir(root) as it:
            for entry in it:
                if entry.name.startswith(".") or not entry.is_dir(follow_symlinks=False):
                    continue
                if parse_day_key(entry.name) is not None:
                    return True
    except OSError:
        return False
    return False


def marker_path(root: Path) -> Path:
    return root / MARKER_FILE


def read_marker(root: Path) -> dict[str, Any] | None:
    path = marker_path(root)
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def migrate_legacy(root: str | os.PathLike[str], *, retention_days: int = 30,
                   delete_legacy: bool = True) -> MigrationReport:
    """把 `root` 下的旧格式事件转成 `root/<日期>.jsonl`。可重复执行（幂等）。"""
    started = time.perf_counter()
    base = Path(root)
    report = MigrationReport(legacy_root=str(base), kept_legacy=not delete_legacy)

    if not base.is_dir():
        report.seconds = time.perf_counter() - started
        return report

    if not legacy_present(base):
        marker = read_marker(base)
        report.already_migrated = marker is not None or (base / INDEX_FILE).is_file()
        if marker:
            for key, field_name in (("legacyFiles", "legacy_files"),
                                    ("eventsMigrated", "events_migrated"),
                                    ("eventsSeen", "events_seen"),
                                    ("eventsUnreadable", "events_unreadable")):
                value = marker.get(key)
                if isinstance(value, int):
                    setattr(report, field_name, value)
        report.seconds = time.perf_counter() - started
        return report

    cutoff = _cutoff(retention_days)
    index_fp: IO[str] | None = None
    try:
        if delete_legacy:
            index_fp = open(base / INDEX_FILE, "a", encoding="utf-8")

        for day_dir in _legacy_day_dirs(base):
            day_name = day_dir.name
            events: list[LionEvent] = []
            files: list[str] = []
            for json_file in _legacy_json_files(day_dir):
                report.legacy_files += 1
                files.append(json_file)
                event = _read_legacy_file(json_file)
                report.events_seen += 1
                if event is None:
                    report.events_unreadable += 1
                    continue
                when = parse_timestamp(event.timestamp) or parse_day_key(day_name)
                if cutoff is not None and when is not None and when.date() < cutoff:
                    report.events_skipped += 1
                    continue
                if event.timestamp is None:
                    event.timestamp = when
                    event.day = day_key(when)      # 时间戳被补上了，日期缓存要跟着更新
                events.append(event)

            if events:
                shard = base / f"{_shard_day(events, day_name)}.jsonl"
                wrote = _append_shard(shard, events)
                report.events_migrated += len(events)
                report.shards_written += 1 if wrote else 0
                if index_fp is not None:
                    _append_index(index_fp, events, shard)

            if delete_legacy:
                report.legacy_files_removed += _remove_files(files)
                report.legacy_dirs_removed += _remove_empty_dirs(day_dir)
            report.legacy_days += 1
    finally:
        if index_fp is not None:
            index_fp.close()

    if delete_legacy:
        marker = {
            "migratedAt": format_timestamp(_now__events_legacy()),
            "legacyFiles": report.legacy_files,
            "legacyDays": report.legacy_days,
            "eventsSeen": report.events_seen,
            "eventsMigrated": report.events_migrated,
            "eventsSkipped": report.events_skipped,
            "eventsUnreadable": report.events_unreadable,
            "retentionDays": retention_days,
        }
        try:
            tmp = marker_path(base).with_suffix(".json.tmp")
            tmp.write_text(json.dumps(marker, ensure_ascii=False, indent=2), encoding="utf-8")
            os.replace(tmp, marker_path(base))
        except OSError as e:
            print(f"[事件迁移] 写迁移标记失败（不影响已迁移的数据）: {e}", flush=True)

    report.seconds = time.perf_counter() - started
    return report


# ----------------------------------------------------------------------
# 内部
# ----------------------------------------------------------------------


def _now__events_legacy():
    return datetime.now().astimezone()


def _cutoff(retention_days: int):
    return retention_cutoff_date(retention_days)


def _legacy_day_dirs(base: Path) -> Iterator[Path]:
    try:
        with os.scandir(base) as it:
            names = [e.name for e in it
                     if not e.name.startswith(".") and e.is_dir(follow_symlinks=False)
                     and parse_day_key(e.name) is not None]
    except OSError:
        return
    for name in sorted(names):
        yield base / name


def _legacy_json_files(day_dir: Path) -> Iterator[str]:
    """`<日期>/<会话>/*.json`：一层会话目录，外加（以防万一）日期目录下的散落 json。

    返回**路径字符串**而不是 `Path`：7 万个文件时，省掉每个文件的 `Path` 构造与成员调用，
    实测这一处就占了迁移总耗时的可观比例。
    """
    try:
        with os.scandir(day_dir) as it:
            entries = list(it)
    except OSError:
        return
    for entry in entries:
        if entry.name.startswith("."):
            continue
        try:
            if entry.is_dir(follow_symlinks=False):
                try:
                    with os.scandir(entry.path) as inner:
                        for f in inner:
                            if f.name.endswith(".json") and not f.name.startswith("."):
                                yield f.path
                except OSError:
                    continue
            elif entry.name.endswith(".json"):
                yield entry.path
        except OSError:
            continue


def _read_legacy_file(path: str | Path) -> LionEvent | None:
    """读一条旧事件。按 UTF-8 读（Java 的 Jackson 写的就是 UTF-8），坏字节替换后重试。"""
    try:
        with open(path, "rb") as f:
            raw = f.read()
    except OSError:
        return None
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")
    return LionEvent.from_json(text)


def _shard_day(events: list[LionEvent], fallback: str) -> str:
    """一个旧目录里的事件可能跨天（补写的历史事件）；按多数派选分片日期。

    少数派那几条会落在"多数派那一天"的分片里，但每条事件自带 timestamp，
    查询/排序/`?after=` 全都按 timestamp，不受影响。
    """
    counts: dict[str, int] = {}
    for e in events:
        key = e.day or day_key(e.timestamp)
        counts[key] = counts.get(key, 0) + 1
    if not counts:
        return fallback
    return max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]


def _append_shard(path: Path, events: list[LionEvent]) -> bool:
    """把一天的事件按时间排序后追加进分片。返回是否真的写了东西。"""
    ordered = sort_events(events)
    if not ordered:
        return False
    payload = "".join(e.to_json() + "\n" for e in ordered)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND | getattr(os, "O_BINARY", 0), 0o644)
    try:
        os.write(fd, payload.encode("utf-8"))
    finally:
        os.close(fd)
    return True


def _append_index(fp: IO[str], events: list[LionEvent], shard: Path) -> None:
    day = shard.stem
    for e in events:
        fp.write(json.dumps({"eventId": e.event_id, "sessionId": e.session_id, "day": day},
                            ensure_ascii=False, separators=(",", ":")) + "\n")
    fp.flush()


def _remove_files(files: list[str]) -> int:
    removed = 0
    for path in files:
        try:
            os.unlink(path)
            removed += 1
        except OSError:
            pass
    return removed


def _remove_empty_dirs(day_dir: Path) -> int:
    """删掉空会话目录与日期目录；还有东西（坏文件/占用）就留着。"""
    removed = 0
    try:
        with os.scandir(day_dir) as it:
            subdirs = [Path(e.path) for e in it if e.is_dir(follow_symlinks=False)]
    except OSError:
        return 0
    for sub in subdirs:
        try:
            os.rmdir(sub)
            removed += 1
        except OSError:
            pass
    try:
        os.rmdir(day_dir)
        removed += 1
    except OSError:
        pass
    return removed


def iter_legacy_events(root: str | os.PathLike[str]) -> Iterator[LionEvent]:
    """只读地遍历旧格式事件（**不改动任何文件**）—— 给统计/核对用。"""
    base = Path(root)
    for day_dir in _legacy_day_dirs(base):
        for json_file in _legacy_json_files(day_dir):
            event = _read_legacy_file(json_file)
            if event is not None:
                yield event


__all__ = [
    "INDEX_FILE",
    "MARKER_FILE",
    "iter_legacy_events",
    "legacy_present",
    "marker_path",
    "migrate_legacy",
    "read_marker",
]


# ========================================================================
# 原模块 lionbox/events.py
# ========================================================================
"""事件存储（P2）。

对应 Java `com.lioncode.core.event`，但**存储格式重做**：按天分片 + JSONL 追加写。

    from lionbox.events import EventStore, EventType, LionEvent

    store = EventStore()                       # 默认 ~/lion-code-workspace/.lioncode/events
    store.load_from_disk()                     # 只列百级分片文件，不再扫 7 万个 JSON
    store.record_event("session-1", EventType.USER_MESSAGE, {"text": "hi"}, "用户消息")

对外语义（`record` / 按会话查询 / `?after=` 增量 / 30 天保留 / 每会话上限裁剪）
与 Java 版一致，旧格式数据由 `migrate_legacy()` 一次性搬过来。
"""



__all__ = [
    "DEFAULT_STORE_PATH",
    "INDEX_FILE",
    "MAX_SHARDS_ON_STARTUP",
    "UNKNOWN_SESSION",
    "EventStore",
    "EventType",
    "LionEvent",
    "MigrationReport",
    "SessionSummary",
    "StoreStats",
    "day_key",
    "epoch_millis",
    "format_timestamp",
    "iter_from_jsonl",
    "iter_legacy_events",
    "legacy_present",
    "migrate_legacy",
    "now_utc",
    "parse_day_key",
    "parse_timestamp",
    "retention_cutoff_date",
    "sort_events",
]


# ========================================================================
# 原模块 lionbox/sessions/ids.py
# ========================================================================
"""会话 ID 的安全校验 —— 对应 Java `core/session/SessionIds.java`。

【为什么必须做】会话 id 是服务端生成的 UUID，但**从 REST 进来时是客户端可控的**：
`@PathVariable String sessionId` 会把 `..%5C..%5Cfoo` 解成 `..\\..\\foo`（Windows 上反斜杠是路径分隔符），
而持久化层直接把它拼成 `sessions\\<id>.json` / `conversations\\<id>.json` ——
不做白名单就会变成"删/读会话目录外任意 .json"。项目的 `docs/审计报告.md` 把这条列为 A-1。

只放行 UUID 那类字符（字母/数字/连字符/下划线/点），分隔符、上级引用、盘符、控制字符、空白一律挡掉。
真实会话 id 全部是 UUID，不会误伤。
"""


#: 长度上限：真实 UUID 是 36 字符，留足余量
MAX_LENGTH = 128

_ALLOWED = set("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_.")


def is_safe(session_id: object) -> bool:
    """是不是「安全的单段文件名」。"""
    if session_id is None:
        return False
    text = str(session_id)
    if text.strip() == "" or len(text) > MAX_LENGTH:
        return False
    if text in (".", ".."):
        return False
    return all(c in _ALLOWED for c in text)


def require_safe(session_id: object) -> str:
    """取安全 id，否则抛 `ValueError`（给"必须拿到一个 id 才能继续"的调用点用）。"""
    if not is_safe(session_id):
        raise ValueError(f"非法会话 id: {session_id!r}")
    return str(session_id)


__all__ = ["MAX_LENGTH", "is_safe", "require_safe"]


# ========================================================================
# 原模块 lionbox/sessions/message.py
# ========================================================================
"""对话消息模型 —— 对应 Java `core/session/ConversationMessage.java`。

【字段名一个字都不能改】用户 `~/.lioncode/conversations/<会话id>.json` 里
已有 Java 版写的数据，Python 版必须原样读得出来：

    [ {
      "messageId" : "00a66567-...",
      "sessionId" : "c68c51c4-...",
      "role" : "system",
      "content" : "【系统提示】...",
      "reasoningContent" : null,
      "toolCalls" : null,
      "toolCallId" : null,
      "toolName" : null,
      "timestamp" : 1790605415.761537300,
      "metadata" : { }
    }, ... ]

老版本还会多出/缺少字段，所以解析一律**容忍未知字段与缺失字段**
（Java 侧为此显式关掉了 `FAIL_ON_UNKNOWN_PROPERTIES`，
否则一个改名就会让整个对话从界面上静默消失）。
"""


import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


#: 角色常量
ROLE_USER = "user"
ROLE_ASSISTANT = "assistant"
ROLE_SYSTEM = "system"
ROLE_TOOL = "tool"


@dataclass(slots=True)
class ToolCallRecord:
    """对应 Java `ConversationMessage.ToolCallRecord`：{"id","name","arguments"}。"""

    id: str | None = None
    name: str | None = None
    arguments: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "arguments": self.arguments if self.arguments is not None else {},
        }

    @staticmethod
    def from_dict(raw: Any) -> "ToolCallRecord | None":
        if not isinstance(raw, dict):
            return None
        args = raw.get("arguments")
        return ToolCallRecord(
            id=None if raw.get("id") is None else str(raw.get("id")),
            name=None if raw.get("name") is None else str(raw.get("name")),
            arguments=args if isinstance(args, dict) else {},
        )


@dataclass(slots=True)
class ConversationMessage:
    """一条对话消息。字段与顺序对齐 Java record。"""

    message_id: str
    session_id: str
    role: str
    content: str | None = None
    reasoning_content: str | None = None
    tool_calls: list[ToolCallRecord] | None = None
    tool_call_id: str | None = None
    tool_name: str | None = None
    timestamp: datetime | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    # ---- 工厂（与 Java 同名同语义）----
    @staticmethod
    def user(session_id: str, content: str) -> "ConversationMessage":
        return ConversationMessage(str(uuid.uuid4()), session_id, ROLE_USER, content,
                                   timestamp=now_utc())

    @staticmethod
    def assistant(session_id: str, content: str,
                  reasoning_content: str | None = None) -> "ConversationMessage":
        return ConversationMessage(str(uuid.uuid4()), session_id, ROLE_ASSISTANT, content,
                                   reasoning_content=reasoning_content, timestamp=now_utc())

    @staticmethod
    def assistant_with_tool_calls(session_id: str, content: str,
                                  tool_calls: list[ToolCallRecord],
                                  reasoning_content: str | None = None) -> "ConversationMessage":
        return ConversationMessage(str(uuid.uuid4()), session_id, ROLE_ASSISTANT, content,
                                   reasoning_content=reasoning_content,
                                   tool_calls=list(tool_calls or []), timestamp=now_utc())

    @staticmethod
    def system(session_id: str, content: str) -> "ConversationMessage":
        return ConversationMessage(str(uuid.uuid4()), session_id, ROLE_SYSTEM, content,
                                   timestamp=now_utc())

    @staticmethod
    def tool_result(session_id: str, tool_call_id: str, tool_name: str,
                    content: str) -> "ConversationMessage":
        return ConversationMessage(str(uuid.uuid4()), session_id, ROLE_TOOL, content,
                                   tool_call_id=tool_call_id, tool_name=tool_name,
                                   timestamp=now_utc())

    # ---- 序列化（键名/顺序与 Java 一致，null 照 Java 保留）----
    def to_dict(self) -> dict[str, Any]:
        return {
            "messageId": self.message_id,
            "sessionId": self.session_id,
            "role": self.role,
            "content": self.content,
            "reasoningContent": self.reasoning_content,
            "toolCalls": [tc.to_dict() for tc in self.tool_calls] if self.tool_calls else None,
            "toolCallId": self.tool_call_id,
            "toolName": self.tool_name,
            # 与 Java Jackson 的 Instant 写法一致（epoch 秒 + 纳秒小数）
            "timestamp": self.timestamp,
            "metadata": self.metadata if self.metadata is not None else {},
        }

    @staticmethod
    def from_dict(raw: Any) -> "ConversationMessage | None":
        """容错解析：缺字段用默认值，多字段忽略；连 role 都没有就当坏数据返回 None。"""
        if not isinstance(raw, dict):
            return None
        role = raw.get("role")
        if role is None or str(role).strip() == "":
            return None
        tool_calls_raw = raw.get("toolCalls")
        tool_calls: list[ToolCallRecord] | None = None
        if isinstance(tool_calls_raw, list):
            tool_calls = [tc for tc in (ToolCallRecord.from_dict(x) for x in tool_calls_raw)
                          if tc is not None]
        metadata = raw.get("metadata")
        message_id = raw.get("messageId")
        session_id = raw.get("sessionId")
        return ConversationMessage(
            message_id="" if message_id is None else str(message_id),
            session_id="" if session_id is None else str(session_id),
            role=str(role),
            content=None if raw.get("content") is None else str(raw.get("content")),
            reasoning_content=None if raw.get("reasoningContent") is None
            else str(raw.get("reasoningContent")),
            tool_calls=tool_calls,
            tool_call_id=None if raw.get("toolCallId") is None else str(raw.get("toolCallId")),
            tool_name=None if raw.get("toolName") is None else str(raw.get("toolName")),
            timestamp=parse_timestamp(raw.get("timestamp")),
            metadata=metadata if isinstance(metadata, dict) else {},
        )

    # ---- 顺手属性 ----
    @property
    def has_tool_calls(self) -> bool:
        return bool(self.tool_calls)


__all__ = [
    "ROLE_ASSISTANT", "ROLE_SYSTEM", "ROLE_TOOL", "ROLE_USER",
    "ConversationMessage", "ToolCallRecord",
]


# ========================================================================
# 原模块 lionbox/sessions/modes.py
# ========================================================================
"""会话工作模式 —— 对应 Java `core/agent/AgentMode.java`。

【为什么放在 sessions 里】`SessionManager.Session` 的 `mode` 字段就是它，
会话持久化读老数据也必须认 `PTC`/`CREATIVE`（删掉枚举值会让那些会话直接加载不出来）。
本模块复用 `lionbox.plugins.base.AgentMode` 的字符串常量，保证与工具层
（`PluginRegistry.for_mode`）判定的模式**是同一套值**，不会出现"会话说是极简、
注册表却按标准放工具"的错位。
"""


from lionbox.plugins.base import AgentMode as _PluginAgentMode

#: 与 Java 枚举一字不差（含已不再开放的 PTC/CREATIVE，只为读老数据）
PTC = _PluginAgentMode.PTC
CREATIVE = _PluginAgentMode.CREATIVE
STANDARD = _PluginAgentMode.STANDARD
MINIMAL = _PluginAgentMode.MINIMAL

#: 界面上能选的模式 —— 就这两个（Java `AgentMode.SELECTABLE`）
SELECTABLE: tuple[str, ...] = (STANDARD, MINIMAL)

#: 中文显示名与说明（Java 枚举构造参数）
DISPLAY: dict[str, tuple[str, str]] = dict(_PluginAgentMode.DISPLAY)

#: 所有能解析出来的名字（含历史模式）
ALL: tuple[str, ...] = tuple(DISPLAY)


class UnknownMode(ValueError):
    """认不出来的模式名（对齐 Java `AgentMode.fromName` 抛 IllegalArgumentException）。"""


def normalize(mode: object) -> str:
    """把不再开放的模式归一成 STANDARD；其余原样返回（None 也当归一）。"""
    value = str(mode or "").strip().upper()
    if value in ("", PTC, CREATIVE):
        return STANDARD
    return value


def from_name(name: object) -> str:
    """按名字解析（大小写不敏感）。

    空/None 当标准模式；不认识的名字抛 `UnknownMode`（调用方报给用户），
    与 Java `AgentMode.fromName` 一致：PTC/CREATIVE 解析得到，但被归一成 STANDARD。
    """
    if name is None or str(name).strip() == "":
        return STANDARD
    value = str(name).strip().upper()
    if value not in DISPLAY:
        raise UnknownMode(f"无效的工作模式: {name}")
    return normalize(value)


def display_name(mode: object) -> str:
    return DISPLAY.get(str(mode or "").strip().upper(), ("", ""))[0]


__all__ = [
    "ALL", "CREATIVE", "DISPLAY", "MINIMAL", "PTC", "SELECTABLE", "STANDARD",
    "UnknownMode", "display_name", "from_name", "normalize",
]


# ========================================================================
# 原模块 lionbox/sessions/session.py
# ========================================================================
"""会话模型 —— 对应 Java `core/session/SessionManager.Session`（record）。

Java:
    record Session(String sessionId, String workspaceId, AgentMode mode,
                   Instant createdAt, String name)

`name`（会话标题）是后加的字段：新建时为 null（界面先显示会话 ID 前缀），
用户发出第一条消息后由标题生成器写入，用户也可以随时手动改。
老版本存下来的会话文件里没有这个字段，反序列化后就是 None，属于正常情况。
"""


from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from lionbox.sessions import modes


@dataclass(slots=True)
class Session:
    session_id: str
    workspace_id: str | None
    mode: str
    created_at: datetime | None = None
    name: str | None = None
    _extra: dict[str, Any] = field(default_factory=dict, repr=False)

    # ---- 展示 ----
    def display_name(self) -> str:
        """界面展示用：有名字用名字，没有就退回 ID 前缀（Java `displayName()`）。"""
        if self.name is not None and self.name.strip() != "":
            return self.name
        sid = self.session_id or "?"
        return "会话 " + (sid[:8] if len(sid) > 8 else sid)

    # ---- 序列化（键名固定，读写用户现有数据靠它）----
    def to_dict(self) -> dict[str, Any]:
        out = {
            "sessionId": self.session_id,
            "workspaceId": self.workspace_id,
            "mode": self.mode,
            # 与 Java Jackson 的 Instant 写法一致（epoch 秒 + 纳秒小数）
            "createdAt": self.created_at,
            "name": self.name,
        }
        out.update(self._extra)      # 不丢未知字段（跨版本往返）
        return out

    def to_json(self, *, pretty: bool = True) -> str:
        import json
        return json.dumps(self.to_dict(), ensure_ascii=False, cls=LionJsonEncoder,
                          indent=2 if pretty else None,
                          separators=None if pretty else (",", ":"))

    @staticmethod
    def from_dict(raw: Any) -> "Session | None":
        """从磁盘 JSON 还原；没有 sessionId 就当坏数据返回 None。

        容忍：缺失 `name`（老文件）、未知字段（新版本加的）、
        `createdAt` 是数字或 ISO 串。
        """
        if not isinstance(raw, dict):
            return None
        session_id = raw.get("sessionId")
        if session_id is None or str(session_id).strip() == "":
            return None
        known = {"sessionId", "workspaceId", "mode", "createdAt", "name"}
        extra = {k: v for k, v in raw.items() if k not in known}
        workspace_id = raw.get("workspaceId")
        name = raw.get("name")
        return Session(
            session_id=str(session_id),
            workspace_id=None if workspace_id is None else str(workspace_id),
            mode=modes.normalize(raw.get("mode")),
            created_at=parse_timestamp(raw.get("createdAt")) or now_utc(),
            name=None if name is None or str(name).strip() == "" else str(name),
            _extra=extra,
        )


__all__ = ["Session"]


# ========================================================================
# 原模块 lionbox/sessions/persistence.py
# ========================================================================
"""会话元数据持久化 —— 对应 Java `core/session/SessionPersistence.java`。

存储位置与文件名与 Java 版完全一致（**用户的现有数据必须能被直接读出来**）：

    ~/lion-code-workspace/.lioncode/sessions/<会话id>.json
    { "sessionId": "...", "workspaceId": "C:\\\\Users\\\\...", "mode": "STANDARD",
      "createdAt": 1790757909.563751400, "name": "我先了解工作区环境，然后逐个调用工具做测" }

* `createdAt` 老数据是 epoch 秒（Jackson 的 Instant 写法），读的时候用 `events.compat` 解析；
* `name` 是后加的字段，老文件里没有 → **缺失就当 None**，绝不能把它当"损坏的会话文件"整条跳过
  （Java 侧为此显式关掉了 `FAIL_ON_MISSING_CREATOR_PROPERTIES`）；
* 多出来的未知字段一律忽略（跨版本读）。
"""


import json
import os
import tempfile
from pathlib import Path
from typing import Any

from lionbox.sessions import ids

#: 默认工作区目录（与 Java `lion.workspace.default-path` 默认值一致）
DEFAULT_WORKSPACE_PATH = workspace_default_path()


def default_sessions_dir(workspace_path: str | os.PathLike[str] | None = None) -> Path:
    base = Path(workspace_path) if workspace_path else DEFAULT_WORKSPACE_PATH
    return base / ".lioncode" / "sessions"


class SessionPersistence:
    """会话元数据的读写。线程安全由"原子替换"保证（读到的永远是完整 JSON）。"""

    def __init__(self, workspace_path: str | os.PathLike[str] | None = None,
                 sessions_dir: str | os.PathLike[str] | None = None) -> None:
        self.sessions_dir = Path(sessions_dir) if sessions_dir else default_sessions_dir(workspace_path)
        try:
            self.sessions_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"[会话] 无法创建会话持久化目录 {self.sessions_dir}: {e}", flush=True)

    # ---- 路径 ----
    def file_for(self, session_id: str) -> Path:
        return self.sessions_dir / f"{session_id}.json"

    # ---- 写 ----
    def save_session(self, session: Session | None) -> bool:
        """保存会话元数据；id 非法直接拒绝（绝不参与拼路径）。"""
        if session is None or not ids.is_safe(session.session_id):
            print(f"[会话] 拒绝保存会话元数据：会话 id 非法: "
                  f"{'null' if session is None else session.session_id}", flush=True)
            return False
        try:
            self.write_atomically(self.file_for(session.session_id), session.to_json())
            return True
        except OSError as e:
            print(f"[会话] 保存会话元数据失败 {session.session_id}: {e}", flush=True)
            return False

    # ---- 读 ----
    def load_session(self, session_id: str) -> Session | None:
        """读一个会话；文件不存在或坏掉返回 None（绝不会因为一条坏数据打断启动）。"""
        if not ids.is_safe(session_id):
            print(f"[会话] 拒绝按非法会话 id 读取元数据: {session_id}", flush=True)
            return None
        path = self.file_for(session_id)
        if not path.is_file():
            return None
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"[会话] 加载会话元数据失败 {session_id}: {e}", flush=True)
            return None
        return Session.from_dict(raw)

    def load_all_sessions(self) -> list[Session]:
        """加载全部会话（跳过坏的，不抛异常）。"""
        out: list[Session] = []
        if not self.sessions_dir.is_dir():
            return out
        try:
            with os.scandir(self.sessions_dir) as it:
                entries = [Path(e.path) for e in it
                           if e.name.endswith(".json") and not e.name.startswith(".")]
        except OSError as e:
            print(f"[会话] 加载会话列表失败: {e}", flush=True)
            return out
        entries.sort(key=lambda p: p.name)
        for path in entries:
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, ValueError) as e:
                print(f"[会话] 跳过损坏的会话文件 {path}: {e}", flush=True)
                continue
            session = Session.from_dict(raw)
            if session is not None:
                out.append(session)
        return out

    def saved_session_ids(self) -> list[str]:
        try:
            with os.scandir(self.sessions_dir) as it:
                names = sorted(e.name for e in it
                               if e.name.endswith(".json") and not e.name.startswith("."))
        except OSError:
            return []
        return [name[:-len(".json")] for name in names]

    # ---- 删 ----
    def delete_session(self, session_id: str) -> bool:
        """`DELETE /api/sessions/{id}` 会走到这里，而 id 来自路径参数 —— 必须先校验。"""
        if not ids.is_safe(session_id):
            print(f"[会话] 拒绝按非法会话 id 删除元数据: {session_id}", flush=True)
            return False
        try:
            self.file_for(session_id).unlink(missing_ok=True)
            return True
        except OSError as e:
            print(f"[会话] 删除会话持久化数据失败 {session_id}: {e}", flush=True)
            return False

    # ---- 原子写（Java `ConversationHistory.writeAtomically` 的同一套做法）----
    @staticmethod
    def write_atomically(target: Path, text: str) -> None:
        """先写同目录临时文件再原子改名 —— 半截 JSON 会让整个对话静默消失。

        `os.replace` 在 Windows 上也是原子的（覆盖已存在的目标），
        所以"一边跑任务一边点审批"两个写方不会写出半截文件。
        """
        target.parent.mkdir(parents=True, exist_ok=True)
        fd, name = tempfile.mkstemp(dir=str(target.parent), prefix=target.name + ".",
                                    suffix=".tmp")
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as f:
                f.write(text)
                f.flush()
                os.fsync(f.fileno())
            os.replace(name, target)
        except BaseException:
            try:
                os.unlink(name)
            except OSError:
                pass
            raise


def session_to_dict(session: Session) -> dict[str, Any]:
    return session.to_dict()


__all__ = ["DEFAULT_WORKSPACE_PATH", "SessionPersistence", "default_sessions_dir",
           "session_to_dict"]


# ========================================================================
# 原模块 lionbox/sessions/history.py
# ========================================================================
"""对话历史 —— 对应 Java `core/session/ConversationHistory.java`。

存储位置与文件格式与 Java 版**完全一致**（用户的现有数据必须能直接读出来）：

    ~/lion-code-workspace/.lioncode/conversations/<会话id>.json
    [ { "messageId": ..., "sessionId": ..., "role": ..., "content": ...,
        "reasoningContent": ..., "toolCalls": ..., "toolCallId": ..., "toolName": ...,
        "timestamp": 1790605415.761537300, "metadata": {} }, ... ]

除了读写，这里还有**裁剪（prune）**：只保留最近 N 条，更早的真删并落盘。
两个保护不能少（Java 踩过）：
  1. 不越过工具调用的配对边界 —— 否则留下孤儿 tool 消息，有些 API 直接 400；
  2. `system` 消息永不删 —— 它们是会话的元信息（比如"这条会话用哪个工作区"）。
"""


import json
import os
import re
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from lionbox.sessions import ids

#: 默认工作区目录（与 Java `lion.workspace.default-path` 默认值一致）
DEFAULT_WORKSPACE_PATH__sessions_history = workspace_default_path()

_WS = re.compile(r"\s+")

#: 裁剪预览最多列几条（Java 里是 12 条 + 一行"还有 N 条"）
PREVIEW_LIMIT = 12


def default_conversations_dir(workspace_path: str | os.PathLike[str] | None = None) -> Path:
    base = Path(workspace_path) if workspace_path else DEFAULT_WORKSPACE_PATH__sessions_history
    return base / ".lioncode" / "conversations"


@dataclass(slots=True)
class PruneResult:
    """裁剪结果（给工具返回值/界面用），字段名对齐 Java record。"""

    total: int
    removed: int
    kept: int
    preview: list[str]
    dryRun: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "removed": self.removed,
            "kept": self.kept,
            "preview": self.preview,
            "dryRun": self.dryRun,
        }


class ConversationHistory:
    """每个会话的完整对话历史：追加、查询、落盘、恢复、裁剪。"""

    def __init__(self, workspace_path: str | os.PathLike[str] | None = None,
                 history_dir: str | os.PathLike[str] | None = None, *,
                 auto_load: bool = False) -> None:
        self.history_dir = Path(history_dir) if history_dir else default_conversations_dir(workspace_path)
        self._conversations: dict[str, list[ConversationMessage]] = {}
        self._lock = threading.RLock()
        try:
            self.history_dir.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            print(f"[对话] 无法创建对话历史目录 {self.history_dir}: {e}", flush=True)
            return
        if auto_load:
            restored = 0
            for saved_id in self.get_saved_session_ids():
                if self.load_from_disk(saved_id):
                    restored += 1
            print(f"[对话] 对话历史已从磁盘恢复: {restored} 个会话", flush=True)

    # ------------------------------------------------------------------
    # 追加 / 查询
    # ------------------------------------------------------------------
    def add_message(self, message: ConversationMessage) -> None:
        """追加并**立即落盘**（保证重启/刷新后对话不丢）。"""
        session_id = message.session_id
        changed = False
        with self._lock:
            bucket = self._conversations.get(session_id)
            if bucket is None:
                bucket = []
                self._conversations[session_id] = bucket
            bucket.append(message)
            changed = True
        if changed:
            self.save_to_disk(session_id)

    def get_history(self, session_id: str | None) -> list[ConversationMessage]:
        if session_id is None:
            return []
        with self._lock:
            return list(self._conversations.get(str(session_id), ()))

    def get_recent_messages(self, session_id: str | None, count: int) -> list[ConversationMessage]:
        if session_id is None:
            return []
        with self._lock:
            messages = self._conversations.get(str(session_id), ())
            if count <= 0:
                return list(messages)
            start = max(0, len(messages) - count)
            return list(messages[start:])

    def get_message_count(self, session_id: str | None) -> int:
        if session_id is None:
            return 0
        with self._lock:
            return len(self._conversations.get(str(session_id), ()))

    def clear_history(self, session_id: str | None) -> None:
        if session_id is None:
            return
        with self._lock:
            self._conversations.pop(str(session_id), None)
        print(f"[对话] 会话历史已清空: {session_id}", flush=True)

    # ------------------------------------------------------------------
    # 裁剪
    # ------------------------------------------------------------------
    def prune_history(self, session_id: str | None, keep_last: int,
                      dry_run: bool = False) -> PruneResult:
        """只保留最近 `keep_last` 条，更早的**真删**（并从磁盘落一次）。"""
        if session_id is None:
            return PruneResult(0, 0, 0, [], dry_run)
        with self._lock:
            messages = self._conversations.get(str(session_id))
            if not messages:
                return PruneResult(0, 0, 0, [], dry_run)
            total = len(messages)
            keep = max(2, int(keep_last))
            if total <= keep:
                return PruneResult(total, 0, total, [], dry_run)

            # 【system 前缀是保护区】会话开头的 system 消息是会话元信息，
            # 有些 API 还要求它在最前面；Java 的注释写着"system 消息永不删"，
            # 但它的 safeCut() 只保证切点是 user、回到 0 时照样把 system 删掉 ——
            # 那条文档化的承诺没兑现。这里把"第一轮用户消息之前"整段钉住，
            # 裁剪只在剩下的部分里挪切点（工具配对边界照样不越过）。
            protected = self._protected_prefix(messages)
            if total - protected <= keep:
                return PruneResult(total, 0, total, [], dry_run)

            cut = self.safe_cut(messages, protected, total - keep)
            if cut <= protected:
                return PruneResult(total, 0, total, [], dry_run)

            preview: list[str] = []
            for i in range(protected, cut):
                if len(preview) >= PREVIEW_LIMIT:
                    break
                preview.append(describe(messages[i]))
            if cut - protected > len(preview):
                preview.append(f"…… 还有 {cut - protected - len(preview)} 条")

            if dry_run:
                return PruneResult(total, cut - protected, total - (cut - protected), preview, True)

            kept = list(messages[cut:])
            self._conversations[str(session_id)] = messages[:protected] + kept
            kept = self._conversations[str(session_id)]
        self.save_to_disk(session_id)
        print(f"[对话] 会话 {session_id} 已裁剪: 原 {total} 条 → 留 {len(kept)} 条"
              f"（删 {cut - protected} 条" + (f"，保留 system 前缀 {protected} 条" if protected else "")
              + "）", flush=True)
        return PruneResult(total, cut - protected, len(kept), preview, False)

    @staticmethod
    def _protected_prefix(messages: list[ConversationMessage]) -> int:
        """第一轮用户消息之前的那几条（system 之类的会话元信息）不许被裁剪。"""
        for i, message in enumerate(messages):
            if message.role == ROLE_USER:
                return i
        return 0

    @staticmethod
    def safe_cut(messages: list[ConversationMessage], start: int, cut: int) -> int:
        """把切点挪到安全边界：不能落在某一轮工具调用的中间。

        从候选切点向后找第一条 `role=user` 的消息作为起点；找不到就往前退
        （宁可少删一点，也不能删出孤儿 tool 消息）。搜索范围不越过 `start`（保护区）。
        """
        for i in range(max(start, cut), len(messages)):
            if messages[i].role == ROLE_USER:
                return i
        for i in range(min(cut, len(messages)) - 1, start - 1, -1):
            if messages[i].role == ROLE_USER:
                return i + 1
        return start

    # ------------------------------------------------------------------
    # 磁盘
    # ------------------------------------------------------------------
    def file_for(self, session_id: str) -> Path:
        return self.history_dir / f"{session_id}.json"

    def save_to_disk(self, session_id: str) -> bool:
        with self._lock:
            messages = self._conversations.get(str(session_id))
            snapshot = list(messages) if messages else None
        if not snapshot:
            return False
        # 非法 id 不参与拼路径（会话 id 从 REST 路径参数进来时是客户端可控的）
        if not ids.is_safe(session_id):
            print(f"[对话] 拒绝按非法会话 id 保存历史: {session_id}", flush=True)
            return False
        try:
            payload = json.dumps([m.to_dict() for m in snapshot], ensure_ascii=False, indent=2,
                                 cls=LionJsonEncoder)
            SessionPersistence.write_atomically(self.file_for(session_id), payload)
        except OSError as e:
            print(f"[对话] 保存会话历史失败 {session_id}: {e}", flush=True)
            return False
        print(f"[对话] 会话历史已保存: {session_id} ({len(snapshot)}条消息)", flush=True)
        return True

    def load_from_disk(self, session_id: str) -> bool:
        if not ids.is_safe(session_id):
            print(f"[对话] 拒绝按非法会话 id 加载历史: {session_id}", flush=True)
            return False
        path = self.file_for(session_id)
        if not path.is_file():
            return False
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as e:
            print(f"[对话] 加载会话历史失败 {session_id}: {e}", flush=True)
            return False
        if not isinstance(raw, list):
            print(f"[对话] 加载会话历史失败 {session_id}: 文件不是消息数组", flush=True)
            return False
        messages = [m for m in (ConversationMessage.from_dict(x) for x in raw) if m is not None]
        dropped = len(raw) - len(messages)
        with self._lock:
            self._conversations[str(session_id)] = messages
        print(f"[对话] 会话历史已从磁盘加载: {session_id} ({len(messages)}条消息"
              + (f"，跳过 {dropped} 条坏数据" if dropped else "") + ")", flush=True)
        return True
    def delete_from_disk(self, session_id: str) -> bool:
        if not ids.is_safe(session_id):
            print(f"[对话] 拒绝按非法会话 id 删除历史文件: {session_id}", flush=True)
            return False
        try:
            existed = self.file_for(session_id).exists()
            self.file_for(session_id).unlink(missing_ok=True)
        except OSError as e:
            print(f"[对话] 删除会话历史文件失败 {session_id}: {e}", flush=True)
            return False
        if existed:
            print(f"[对话] 会话历史文件已删除: {session_id}", flush=True)
        return existed

    def get_saved_session_ids(self) -> list[str]:
        try:
            if not self.history_dir.is_dir():
                return []
            with os.scandir(self.history_dir) as it:
                names = sorted(e.name for e in it
                               if e.name.endswith(".json") and not e.name.startswith("."))
        except OSError as e:
            print(f"[对话] 获取已保存会话列表失败: {e}", flush=True)
            return []
        return [name[:-len(".json")] for name in names]


def describe(message: ConversationMessage) -> str:
    """一条消息的一行摘要（"用户：帮我把登录改成…"）。"""
    role = message.role or ""
    if role == "user":
        label = "用户"
    elif role == "assistant":
        label = (f"模型（调工具 {len(message.tool_calls)} 个）"
                 if message.tool_calls else "模型")
    elif role == "tool":
        label = "工具结果" + (f"({message.tool_name})" if message.tool_name else "")
    elif role == "system":
        label = "系统"
    else:
        label = role
    text = _WS.sub(" ", message.content or "").strip()
    if len(text) > 60:
        text = text[:60] + "…"
    return label + (f"：{text}" if text else "")


__all__ = ["DEFAULT_WORKSPACE_PATH", "ConversationHistory", "PruneResult",
           "default_conversations_dir", "describe"]


# ========================================================================
# 原模块 lionbox/sessions/manager.py
# ========================================================================
"""会话管理器 —— 对应 Java `core/session/SessionManager.java`。

管理 Agent 对话会话的生命周期，**强制绑定工作区**：未选择工作区不能创建会话。
运行时模式覆盖（`modeOverrides`）比 `Session.mode` 优先级高，用来做"会话中途切模式"。
"""


import threading
import uuid
from datetime import datetime
from typing import Iterable

from lionbox.sessions import modes


class SessionManager:
    """会话的创建 / 恢复 / 重命名 / 换工作区 / 切模式 / 销毁。"""

    def __init__(self, persistence: SessionPersistence | None = None) -> None:
        self._sessions: dict[str, Session] = {}
        self._mode_overrides: dict[str, str] = {}
        self._lock = threading.RLock()
        # setter 注入而不是构造器注入：SessionPersistence 自己初始化时要读磁盘，
        # 互相注入容易踩启动顺序（Java 侧同样的理由）
        self.persistence = persistence

    def set_persistence(self, persistence: SessionPersistence | None) -> None:
        self.persistence = persistence

    # ------------------------------------------------------------------
    # 创建 / 恢复
    # ------------------------------------------------------------------
    def create_session(self, workspace_id: str | None, mode: str | None = None) -> Session:
        """创建新会话。未绑定工作区抛 `IllegalStateError`（与 Java 同样的提示语）。"""
        if workspace_id is None or str(workspace_id).strip() == "":
            raise IllegalStateError("未绑定工作区，无法创建会话。请先选择工作区目录。")
        session_id = str(uuid.uuid4())
        # name 留空：等用户发出第一条消息后由标题生成器写入
        effective = modes.normalize(mode)
        session = Session(session_id, str(workspace_id), effective, now_utc(), None)
        with self._lock:
            self._sessions[session_id] = session
            self._mode_overrides[session_id] = effective
        print(f"[会话] 新会话已创建: {session_id} - 工作区: {workspace_id}, 模式: {effective}",
              flush=True)
        return session

    def restore_session(self, session_id: str, workspace_id: str | None, mode: str | None,
                        created_at: datetime | None, name: str | None = None) -> Session:
        """恢复历史会话（启动时从磁盘加载，跳过工作区强制检查）。"""
        effective = modes.normalize(mode)
        if mode is not None and str(mode).strip().upper() != effective:
            print(f"[会话] 会话 {session_id} 的模式 {mode} 已不再开放，按标准模式恢复", flush=True)
        session = Session(session_id, workspace_id, effective, created_at or now_utc(), name)
        with self._lock:
            self._sessions[session_id] = session
            # 必须是 effective：modeOverrides 优先级更高，
            # 存归一前的值等于让 PTC/CREATIVE 从后门继续生效
            self._mode_overrides[session_id] = effective
        print(f"[会话] 会话已从磁盘恢复: {session_id} - 工作区: {workspace_id}, "
              f"模式: {effective}, 名称: {name if name else '(未命名)'}", flush=True)
        return session

    # ------------------------------------------------------------------
    # 改名 / 换工作区
    # ------------------------------------------------------------------
    def rename_session(self, session_id: str, name: str | None) -> bool:
        """重命名（用户手动改，或模型自动生成）。Session 不可变 → 造新的替换并落盘。"""
        with self._lock:
            old = self._sessions.get(session_id)
            if old is None:
                print(f"[会话] 重命名失败，会话不存在: {session_id}", flush=True)
                return False
            cleaned = None if name is None else str(name).strip()
            if cleaned is not None and cleaned == "":
                cleaned = None
            if cleaned is not None and len(cleaned) > 60:
                cleaned = cleaned[:60]
            updated = Session(old.session_id, old.workspace_id, old.mode, old.created_at, cleaned,
                              old._extra)
            self._sessions[session_id] = updated
            persistence = self.persistence
        if persistence is not None:
            persistence.save_session(updated)
        print(f"[会话] 会话已重命名: {session_id} -> {cleaned}", flush=True)
        return True

    def move_session_to_workspace(self, session_id: str, workspace_id: str | None) -> bool:
        """把会话换到另一个工作区（只改绑定关系，不动已有对话内容）。"""
        with self._lock:
            old = self._sessions.get(session_id)
            if old is None:
                print(f"[会话] 换工作区失败，会话不存在: {session_id}", flush=True)
                return False
            if workspace_id is None or str(workspace_id).strip() == "":
                print(f"[会话] 换工作区失败，工作区为空: {session_id}", flush=True)
                return False
            if str(workspace_id) == old.workspace_id:
                return True
            updated = Session(old.session_id, str(workspace_id), old.mode, old.created_at, old.name,
                              old._extra)
            self._sessions[session_id] = updated
            persistence = self.persistence
        if persistence is not None:
            persistence.save_session(updated)
        print(f"[会话] 会话已换工作区: {session_id} -> {workspace_id}", flush=True)
        return True

    def set_title_if_absent(self, session_id: str, name: str | None) -> bool:
        """仅在会话还没有名字时写入（模型自动生成用，避免覆盖用户自己改的名字）。"""
        with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return False
            if session.name is not None and session.name.strip() != "":
                return False
        return self.rename_session(session_id, name)

    # ------------------------------------------------------------------
    # 模式
    # ------------------------------------------------------------------
    def update_mode(self, session_id: str, mode: str | None) -> bool:
        """运行时切换工作模式（立即生效，后续消息按新模式处理）。"""
        effective = modes.normalize(mode)
        with self._lock:
            if session_id not in self._sessions:
                print(f"[会话] 切换模式失败，会话不存在: {session_id}", flush=True)
                return False
            self._mode_overrides[session_id] = effective
        print(f"[会话] 会话模式已切换: {session_id} -> {effective}", flush=True)
        return True

    def get_effective_mode(self, session_id: str) -> str:
        """当前生效模式（含运行时覆盖）；会话不存在时回落到 STANDARD。"""
        with self._lock:
            override = self._mode_overrides.get(session_id)
            if override is not None:
                return override
            session = self._sessions.get(session_id)
        return session.mode if session is not None else modes.STANDARD

    # ------------------------------------------------------------------
    # 查询 / 销毁
    # ------------------------------------------------------------------
    def get_session(self, session_id: str | None) -> Session | None:
        if session_id is None:
            return None
        with self._lock:
            return self._sessions.get(str(session_id))

    def get_all_sessions(self) -> list[Session]:
        with self._lock:
            return list(self._sessions.values())

    def destroy_session(self, session_id: str) -> None:
        with self._lock:
            removed = self._sessions.pop(session_id, None)
            self._mode_overrides.pop(session_id, None)
        if removed is not None:
            print(f"[会话] 会话已销毁: {session_id}", flush=True)

    def __len__(self) -> int:
        with self._lock:
            return len(self._sessions)

    def __contains__(self, session_id: object) -> bool:
        with self._lock:
            return str(session_id) in self._sessions

    def session_ids(self) -> Iterable[str]:
        with self._lock:
            return tuple(self._sessions.keys())


class IllegalStateError(RuntimeError):
    """对应 Java 的 `IllegalStateException`（"未绑定工作区…"这类可展示给用户的错误）。"""


__all__ = ["IllegalStateError", "SessionManager"]


# ========================================================================
# 原模块 lionbox/sessions/restorer.py
# ========================================================================
"""启动状态恢复 —— 对应 Java `core/session/StartupRestorer.java` 的会话部分。

Java 的 `run()` 做两件事：
  1. `restoreSessions()`：从磁盘读全部会话 → 重新注册它绑定的工作区 → 放回 SessionManager
  2. `restoreAdapters()`：恢复适配器的 baseUrl / 激活适配器

第 2 件事属于 `llm`/`config` 模块（P4），不在 P2 范围；这里把会话恢复完整实现，
适配器恢复留成**显式传入的回调**，由装配层（app.py / llm 模块）接上去，
本模块不 import 任何 LLM 代码。
"""


from typing import Any, Callable



class StartupRestorer:
    """启动时把磁盘上的会话恢复进 `SessionManager`。"""

    def __init__(self, session_persistence: SessionPersistence, session_manager: SessionManager,
                 workspace_manager: Any = None,
                 adapter_restorer: Callable[[], Any] | None = None) -> None:
        self.session_persistence = session_persistence
        self.session_manager = session_manager
        self.workspace_manager = workspace_manager
        self.adapter_restorer = adapter_restorer

    def run(self) -> dict[str, Any]:
        sessions = self.restore_sessions()
        adapters = self.restore_adapters()
        return {"sessions": sessions, "adapters": adapters}

    # ------------------------------------------------------------------
    def restore_sessions(self) -> int:
        """恢复会话与工作区绑定。返回恢复的会话数。"""
        sessions = self.session_persistence.load_all_sessions()
        for session in sessions:
            # 会话绑定的工作区要重新注册（工作区只在内存里，重启就没了）
            self._register_workspace(session.workspace_id)
            self.session_manager.restore_session(
                session.session_id, session.workspace_id, session.mode,
                session.created_at, session.name)
        print(f"[启动] 已恢复 {len(sessions)} 个会话", flush=True)
        return len(sessions)

    def _register_workspace(self, workspace_id: str | None) -> None:
        if not workspace_id or self.workspace_manager is None:
            return
        getter = getattr(self.workspace_manager, "get_workspace", None)
        if callable(getter):
            try:
                if getter(workspace_id) is not None:
                    return
            except Exception:
                pass
        register = getattr(self.workspace_manager, "register_workspace", None)
        if callable(register):
            try:
                register(workspace_id)
            except Exception as e:   # 路径非法这类脏数据：不要让启动挂掉
                print(f"[启动] 注册工作区失败 {workspace_id}: {e}", flush=True)

    def restore_adapters(self) -> bool:
        """适配器恢复交给装配层（P4 的 llm 模块）；没接就什么都不做。"""
        if self.adapter_restorer is None:
            return False
        try:
            self.adapter_restorer()
            return True
        except Exception as e:
            print(f"[启动] 恢复适配器配置失败: {e}", flush=True)
            return False


__all__ = ["StartupRestorer"]


# ========================================================================
# 原模块 lionbox/sessions/title.py
# ========================================================================
"""会话标题生成 —— 对应 Java `core/session/SessionTitleService.java`。

以前界面上的会话名是会话 ID 的前 8 位（一串随机数），根本分不清哪条是哪条。
现在改成：用户在会话里发出**第一条消息**后，拿这条消息让模型生成一个短标题。

几个刻意的设计（照 Java 版）：
 1. **异步**：生成标题是一次额外的模型调用，绝不能让用户的首条消息多等几秒 ——
    丢到单线程守护队列里做，界面先用 ID 前缀显示。
 2. **只做一次**：会话已有名字就不再生成（`set_title_if_absent`），
    用户手动改过的名字不会被模型覆盖。
 3. **失败要有兜底**：模型调不通（断网、Key 错、本地模型没热）时用首条消息截断出标题。
 4. 并发去重：同一条会话的首条消息可能因重试被触发两次，用 `_in_flight` 挡住。

模型调用由装配层（P4 的 llm 模块）通过 `chat` 回调注入，
本模块不 import 任何模型适配器代码。
"""


import queue
import re
import threading
from typing import Any, Callable


#: 标题最多多少个字符
MAX_TITLE_CHARS = 20
#: 喂给模型的用户消息最长截多少字符（标题只需要知道大意）
MAX_INPUT_CHARS = 600
#: 标题任务的 max_tokens
MAX_TITLE_TOKENS = 128

SYSTEM_PROMPT = """你是会话标题生成器。根据用户的第一条消息，生成一个概括这次会话要做什么的短标题。

要求：
1. 不超过 12 个字（中文）或 6 个单词（英文），用与用户相同的语言
2. 只输出标题本身：不要引号、不要书名号、不要句末标点、不要解释、不要换行
3. 直接说做什么事，例如：修复登录超时、给配置加注释、排查内存泄漏、写单元测试
"""

#: 标题任务要明确关掉"思考"。
#: 思考类模型（返回里同时有 content 和 reasoning_content）在 max_tokens 给小的时候，
#: 会把预算全花在 reasoning 上，content 直接空串，标题就生成不出来。
#: 支持该参数的服务会照做；不支持的当未知字段忽略，不影响调用。
EXTRA_OPTIONS: dict[str, Any] = {"thinking": {"type": "disabled"}}

_PREFIXES = ("标题：", "标题:", "Title:", "title:", "会话标题：", "会话标题:")
_TRIM_HEAD = re.compile(r"^[\s\"'“”‘’《》<>#*`]+")
_TRIM_TAIL = re.compile(r"[\s\"'“”‘’《》<>#*`]+$")
_TRIM_PUNCT = re.compile(r"[。．.，,；;：:！!？?~～]+$")
_TITLE_LINE = re.compile(r"(?i)(?:^|\n)\s*(?:title|标题)\s*[:：]\s*([^\n。．]{1,40})")
_WS__sessions_title = re.compile(r"\s+")
_SOFT_PREFIXES = ("帮我", "麻烦", "请", "你能", "能不能", "帮忙")


class SessionTitleService:
    """异步生成会话标题（幂等：已有名字 / 正在生成 / 空消息都直接返回）。"""

    def __init__(self, session_manager: SessionManager,
                 chat: Callable[..., Any] | None = None,
                 config_store: Any = None,
                 default_model: str = "lion-models1") -> None:
        self.session_manager = session_manager
        self._chat = chat
        self.config_store = config_store
        self.default_model = default_model
        self._in_flight: set[str] = set()
        self._lock = threading.Lock()
        self._counter = 0
        self._queue: "queue.Queue[tuple[int, str, str] | None]" = queue.Queue()
        self._worker: threading.Thread | None = None

    def set_chat(self, chat: Callable[..., Any] | None) -> None:
        """装配层注入模型调用（签名见 `generate`）。"""
        self._chat = chat

    # ------------------------------------------------------------------
    # 对外
    # ------------------------------------------------------------------
    def needs_title(self, session_id: str | None) -> bool:
        session = self.session_manager.get_session(session_id)
        if session is None:
            return False
        return session.name is None or session.name.strip() == ""

    def generate_async(self, session_id: str | None, message: str | None) -> bool:
        """异步生成标题。返回是否真的排进了队列。"""
        if not session_id or not message or message.strip() == "":
            return False
        if not self.needs_title(session_id):
            return False
        with self._lock:
            if session_id in self._in_flight:
                return False
            self._in_flight.add(session_id)
            self._counter += 1
            task_id = self._counter
        self._ensure_worker()
        self._queue.put((task_id, session_id, message))
        return True

    def wait_idle(self, timeout: float = 5.0) -> bool:
        """等队列跑空（给测试/关闭时用）。返回是否在超时前跑空。"""
        if self._worker is None or not self._worker.is_alive():
            return True
        done = threading.Event()

        def _drain() -> None:
            self._queue.join()
            done.set()

        threading.Thread(target=_drain, daemon=True, name="session-title-wait").start()
        return done.wait(timeout)

    def shutdown(self) -> None:
        """停掉 worker（已在队列里的任务会被丢弃 —— 标题不是关键路径）。"""
        try:
            self._queue.put_nowait(None)
        except queue.Full:
            pass

    # ------------------------------------------------------------------
    # 内部
    # ------------------------------------------------------------------
    def _ensure_worker(self) -> None:
        if self._worker is not None and self._worker.is_alive():
            return
        with self._lock:
            if self._worker is not None and self._worker.is_alive():
                return
            self._worker = threading.Thread(target=self._loop, name="session-title", daemon=True)
            self._worker.start()

    def _loop(self) -> None:
        """单线程串行处理 —— 标题生成很轻，串行还能避免和主对话抢本地模型算力。"""
        while True:
            item = self._queue.get()
            try:
                if item is None:
                    return
                task_id, session_id, message = item
                self._handle(task_id, session_id, message)
            finally:
                self._queue.task_done()

    def _handle(self, task_id: int, session_id: str, message: str) -> None:
        try:
            title = self.generate(session_id, message)
            if title and title.strip() != "":
                ok = self.session_manager.set_title_if_absent(session_id, title)
                print(f"[标题#{task_id}] 会话 {session_id} 标题生成"
                      f"{'成功' if ok else '被跳过(已有名字)'}: {title}", flush=True)
        except Exception as e:
            print(f"[标题#{task_id}] 会话 {session_id} 标题生成失败，改用消息摘要兜底: {e}",
                  flush=True)
            self.session_manager.set_title_if_absent(session_id, fallback_title(message))
        finally:
            with self._lock:
                self._in_flight.discard(session_id)

    def generate(self, session_id: str, message: str) -> str:
        """真正去调模型生成标题；失败抛异常，由调用方兜底。

        `chat(messages, model=..., extra=..., max_tokens=...)` 返回的对象需要有
        `content` 与 `reasoning_content` 两个属性（与 Java `ModelResponse` 对齐）。
        """
        if self._chat is None:
            raise RuntimeError("没有可用的模型适配器")
        model = self.current_model()
        text = message if len(message) <= MAX_INPUT_CHARS else message[:MAX_INPUT_CHARS]
        messages = [{"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": text}]
        response = self._chat(messages, model=model, extra=EXTRA_OPTIONS,
                              max_tokens=MAX_TITLE_TOKENS)
        title = clean_title(getattr(response, "content", None))
        if not title:
            # 兜底 1：正文为空但思考内容有货 —— 从 reasoning 里抠一个出来
            title = clean_title(title_from_reasoning(getattr(response, "reasoning_content", None)))
        if not title:
            raise RuntimeError("模型返回了空标题")
        return title

    def current_model(self) -> str:
        """取当前配置的模型名；取不到回落到默认模型。"""
        saved = self._config_map("openai")
        model = saved.get("model")
        if isinstance(model, str) and model.strip():
            return model
        top = self._config_get("model", None)
        if isinstance(top, str) and top.strip():
            return top
        return self.default_model

    def _config_map(self, key: str) -> dict[str, Any]:
        if self.config_store is None:
            return {}
        getter = getattr(self.config_store, "get_map", None)
        if callable(getter):
            value = getter(key)
            return value if isinstance(value, dict) else {}
        value = self._config_get(key, None)
        return value if isinstance(value, dict) else {}

    def _config_get(self, key: str, default: Any) -> Any:
        if self.config_store is None:
            return default
        getter = getattr(self.config_store, "get", None)
        return getter(key, default) if callable(getter) else default


# ----------------------------------------------------------------------
# 纯函数（与 Java 同名，方便逐条对拍）
# ----------------------------------------------------------------------


def title_from_reasoning(reasoning: str | None) -> str | None:
    """从思考内容里抠标题：优先 `Title: xxx`/`标题：xxx`，否则取最后一行非空文本。"""
    if not reasoning or reasoning.strip() == "":
        return None
    last: str | None = None
    for match in _TITLE_LINE.finditer(reasoning):
        last = match.group(1).strip()
    if last:
        return last
    for line in reversed(reasoning.split("\n")):
        text = line.strip()
        if text:
            return text
    return None


def clean_title(raw: str | None) -> str | None:
    """清洗模型输出：去掉引号、书名号、markdown 标记、句末标点、多余换行。"""
    if raw is None:
        return None
    text = raw.strip()
    newline = text.find("\n")
    if newline > 0:
        text = text[:newline].strip()
    for prefix in _PREFIXES:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    text = _TRIM_HEAD.sub("", text)
    text = _TRIM_TAIL.sub("", text).strip()
    text = _TRIM_PUNCT.sub("", text).strip()
    if text == "":
        return None
    return text[:MAX_TITLE_CHARS]


def fallback_title(message: str | None) -> str:
    """兜底标题：拿首条消息的开头做摘要，去掉常见客套话。"""
    text = _WS__sessions_title.sub(" ", message or "").strip()
    for prefix in _SOFT_PREFIXES:
        while text.startswith(prefix):
            text = text[len(prefix):].strip()
    if text == "":
        return "新会话"
    return text[:12]


__all__ = ["EXTRA_OPTIONS", "MAX_INPUT_CHARS", "MAX_TITLE_CHARS", "MAX_TITLE_TOKENS",
           "SYSTEM_PROMPT", "SessionTitleService", "clean_title", "fallback_title",
           "title_from_reasoning"]


# ========================================================================
# 原模块 lionbox/sessions.py
# ========================================================================
"""会话管理（P2）—— 对应 Java `com.lioncode.core.session` 的 8 个类。

| Java | 这里 |
| --- | --- |
| `SessionManager`（含 `Session` record） | `manager.SessionManager` / `session.Session` |
| `ConversationHistory` | `history.ConversationHistory`（`PruneResult` 同） |
| `ConversationMessage`（含 `ToolCallRecord`） | `message.ConversationMessage` / `message.ToolCallRecord` |
| `SessionPersistence` | `persistence.SessionPersistence` |
| `SessionIds` | `ids.is_safe` |
| `SessionContext` | `context.SessionContext` |
| `StartupRestorer`（会话部分） | `restorer.StartupRestorer` |
| `SessionTitleService` | `title.SessionTitleService` |

**磁盘格式与 Java 版一字不改**：`~/.lioncode` 下已有的
`sessions/<id>.json` 与 `conversations/<id>.json` 直接读得出来，
`timestamp` 是 Jackson 的 epoch 秒写法也能解析。
"""



__all__ = [
    "AGENT_MODES",
    "CREATIVE",
    "ConversationHistory",
    "ConversationMessage",
    "DEFAULT_WORKSPACE_PATH",
    "IllegalStateError",
    "MINIMAL",
    "MODE_DISPLAY",
    "PTC",
    "PruneResult",
    "ROLE_ASSISTANT",
    "ROLE_SYSTEM",
    "ROLE_TOOL",
    "ROLE_USER",
    "SELECTABLE",
    "SESSION_ID_MAX_LENGTH",
    "STANDARD",
    "Session",
    "SessionContext",
    "SessionManager",
    "SessionPersistence",
    "SessionTitleService",
    "StartupRestorer",
    "ToolCallRecord",
    "UnknownMode",
    "clean_title",
    "default_conversations_dir",
    "default_sessions_dir",
    "describe",
    "fallback_title",
    "from_name",
    "is_safe",
    "normalize",
    "require_safe",
    "title_from_reasoning",
]


# ========================================================================
# 原模块 lionbox/api/sessions.py
# ========================================================================
"""会话接口 —— `/api/sessions/*`。

对应 Java ``src\\main\\java\\com\\lioncode\\web\\controller\\SessionController.java``
（247 行 / 8 个接口）：列表、创建、重命名、换工作区、单删、清空、切模式、取历史。

# 依赖：lionbox.sessions（会话 / 对话历史 / 会话持久化）、lionbox.skills、lionbox.events
#   —— P2 已把这三个模块实现出来，但**装配进 ApiContext 是装配方的动作**（`app.py`、`api/__init__.py`
#      都不在本任务范围内）。所以这里对依赖的取法是"能拿到真实实现就用真实的，拿不到才退窄桩"：
#      `history` / `skill_repository` 默认就是真实实现（读用户磁盘上的历史 / 与 Agent 共用技能单例），
#      `sessions` / `session_persistence` 按 SPEC 第 4 节留成窄桩等装配方 `ctx.install(...)` ——
#      装上之后本文件一行都不用改（见 `_sess_raw` 与 `_persist_session`：真实实现返回 `Session`
#      数据类、窄桩返回 dict，两种都认）。

【服务名（跨模块契约；取用时一律走 `ctx.service`，装配方 install 的真实实现优先）】

| 服务名                | 真实实现                               | 本模块未装配时的默认       |
| --------------------- | -------------------------------------- | -------------------------- |
| `sessions`            | `lionbox.sessions.SessionManager`      | `deps.SessionStoreStub`（**桩**，SPEC 4.2 的约定：装配方 `ctx.install`） |
| `session_persistence` | `lionbox.sessions.SessionPersistence`  | `_SessionPersistenceStub`（**桩**：接口层默认不往用户磁盘写会话元数据） |
| `history`             | `lionbox.sessions.ConversationHistory` | 真实实现（`auto_load=True`，等价 Java `@PostConstruct`）；模块缺失时才用 `_HistoryStub` |
| `skill_repository`    | `lionbox.skills.SkillRepository`       | 真实实现（`default_repository()`，与 `api/context.py` 同一个单例）；模块缺失时才用 `_SkillRepositoryStub` |
| `events`              | `lionbox.events.EventStore`            | `deps.EventStoreStub`（由 `api/events.py` 在装配时升级成真实存储） |
| `workspaces`          | `deps.WorkspaceStore`（**真实**，读写 app-config.json） | ——          |

`history` / `skill_repository` 两个服务名是与并行任务对齐过的：
`api/changes.py` 的 `_HistoryProxy` 就转发到 `history`（"与 /api/sessions/{id}/history 读的永远是同一份"），
`api/context.py` 用 `skill_repository` 取技能仓库 —— 名字不同就会各拿一份、状态对不上。

【逐字段对齐的三个要点（照 Java 实测，不照直觉）】

1. `SessionDto` 的 ``adapterType`` / ``name`` **即使为 null 也要输出**（Java record 字段，
   不是 `ApiResponse` 那种 `@JsonInclude(NON_NULL)` 省略）：实测
   ``{"sessionId":…,"adapterType":null,"name":null}``。
2. 四个 `@RequestBody` 接口在**请求体缺失/不是 JSON 对象**时，Spring 在进方法体之前就回
   400 + `{"timestamp","status":400,"error":"Bad Request","path"}`（实测 PUT 两个接口），
   所以"会话不存在"之类的业务判断排在它后面。
3. 错误文案逐字照抄：`会话不存在: <id>`、`缺少 workspaceId`、`工作区不存在: <id>`、
   `重命名失败`、`换工作区失败`、`模式切换失败`、`已重命名`、`会话已销毁`、`模式已切换`、
   `会话创建成功`、`已换到新工作区`、`已清空 N 个对话（M 个没删掉）`。
"""


import logging
import threading
from datetime import datetime, timezone
from typing import Any

from lionbox.api import deps

log__api_sessions = logging.getLogger("lionbox.api.sessions")

#: Java `SessionManager.createSession` 在工作区为空时抛的 IllegalStateException 文案
NO_WORKSPACE_ERROR = "未绑定工作区，无法创建会话。请先选择工作区目录。"
#: 无效模式的文案（Java 里是字符串拼接，`{mode}` 处放请求里的**原值**）
INVALID_MODE_ERROR = "无效的工作模式: {mode}（只有 STANDARD / MINIMAL）"

#: Java `SessionManager.Session` 的字段（record 组件名）
_SESSION_FIELDS = ("sessionId", "workspaceId", "mode", "createdAt", "name")
#: 真实 `lionbox.sessions.Session` 是 snake_case 数据类 —— 字段名映射
_SNAKE_FIELDS = {"sessionId": "session_id", "workspaceId": "workspace_id", "createdAt": "created_at"}
#: Java `ConversationMessage` 的字段（record 组件名，顺序即 Jackson 的输出顺序）
_MESSAGE_FIELDS = ("messageId", "sessionId", "role", "content", "reasoningContent",
                   "toolCalls", "toolCallId", "toolName", "timestamp", "metadata")
#: Java `AgentMode` 的全部枚举值（含只为读老数据保留的 PTC / CREATIVE）
_MODE_CODES = ("PTC", "CREATIVE", "STANDARD", "MINIMAL")

try:                                     # Python 侧的 AgentMode 就是 lionbox.sessions.modes
    from lionbox.sessions import modes as _modes
except ImportError:                      # 依赖：lionbox.sessions（由并行任务提供）
    _modes = None


class InvalidMode(ValueError):
    """对应 Java `AgentMode.fromName` 抛的 `IllegalArgumentException`。"""


# --------------------------------------------------------------------------
# 值转换（Java 的序列化形状 → Python，反过来也要）
# --------------------------------------------------------------------------


def _raw_text(value: Any) -> str:
    """请求体里的原值按 Jackson 的方式转成字符串（错误文案里要原样回显）。

    Jackson 把 JSON 的 true/false 读成 `"true"`/`"false"`、数字读成 `"5"`，
    Java 侧 `"无效的工作模式: " + request.mode()` 拼的就是这个形态。
    """
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _wire_instant(value: Any) -> Any:
    """会话时间戳 → Java `Instant` 的 JSON 写法（ISO_INSTANT：0/3/6/9 位小数 + `Z`）。

    【为什么要过一道手】Java 的 `SessionDto.createdAt` 是 `Instant`，Jackson 输出
    ``2026-09-30T08:31:07.455991Z``（小数位按 3/6/9 收敛）；而会话服务给回来的可能是
    字符串（窄桩）、`datetime`（真实 `Session`）或 epoch 秒（磁盘格式）。
    Python 的 `datetime` 只有微秒精度，所以最多 6 位小数 —— 这是精度上限，不是取舍。
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value or None             # 已经是 Java 形状的 ISO 串：原样发，不重新格式化
    if isinstance(value, datetime):
        dt = value.astimezone(timezone.utc) if value.tzinfo else value.astimezone()
    elif isinstance(value, (int, float)) and not isinstance(value, bool):
        dt = datetime.fromtimestamp(float(value), timezone.utc)
    else:
        raise TypeError(f"无法序列化成 Instant 的时间戳: {value!r}")
    base = dt.strftime("%Y-%m-%dT%H:%M:%S")
    micro = dt.microsecond
    if micro == 0:
        return base + "Z"
    if micro % 1000 == 0:
        return f"{base}.{micro // 1000:03d}Z"
    return f"{base}.{micro:06d}Z"


def _to_instant(value: Any) -> datetime | None:
    """`_wire_instant` 的反向：给真实 `SessionPersistence` 造 `Session` 时用。"""
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc) if value.tzinfo else value.astimezone()
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return datetime.fromtimestamp(float(value), timezone.utc)
    text = str(value).strip()
    if not text:
        return None
    if text[-1] in ("Z", "z"):
        text = text[:-1] + "+00:00"
    try:
        dt = datetime.fromisoformat(text)
    except ValueError:
        return None
    return dt.astimezone(timezone.utc) if dt.tzinfo else dt.astimezone()


def _parse_mode(name: Any) -> str:
    """Java `AgentMode.fromName`：空/null → STANDARD；PTC/CREATIVE 归一成 STANDARD；
    不认识的名字抛 `InvalidMode`（大小写不敏感）。"""
    if _modes is not None:
        try:
            return _modes.from_name(name)
        except _modes.UnknownMode as e:
            raise InvalidMode(str(e)) from None
    if name is None or str(name).strip() == "":
        return "STANDARD"
    code = str(name).strip().upper()
    if code not in _MODE_CODES:
        raise InvalidMode(code)
    return "STANDARD" if code in ("PTC", "CREATIVE") else code


def _clean_name(name: Any) -> str | None:
    """Java `SessionManager.renameSession` 的清洗规则：去首尾空白、全空白当清空、截断到 60。

    【为什么在接口层也做一遍】真实 `SessionManager.rename_session` 自己会清洗，但窄桩
    （`deps.SessionStoreStub`）只存不洗 —— 而"改完名字回什么"是前端按 Java 行为解析的。
    这段清洗对真实实现是**幂等**的，装上前后的响应完全一致。
    """
    if name is None:
        return None
    cleaned = str(name).strip()
    if cleaned == "":
        return None
    return cleaned[:60]


# --------------------------------------------------------------------------
# 服务返回对象 → Java 的 JSON 形状
# --------------------------------------------------------------------------


def _sess_raw(session: Any) -> dict[str, Any]:
    """会话对象 → `SessionManager.Session` 字段名（Java record 组件名）的 dict。

    【为什么要归一】共享服务有两种实现：deps 的窄桩返回 dict（键名就是 record 组件名），
    真实的 `lionbox.sessions.SessionManager` 返回 `Session` 数据类（snake_case 属性）。
    装配方换上真实实现时本模块不该改一行代码。
    """
    if isinstance(session, dict):
        return session
    if session is None:
        raise TypeError("会话服务返回了 null，无法构造 SessionDto")
    out: dict[str, Any] = {}
    for key in _SESSION_FIELDS:
        if hasattr(session, key):
            out[key] = getattr(session, key)
            continue
        snake = _SNAKE_FIELDS.get(key)
        if snake is not None and hasattr(session, snake):
            out[key] = getattr(session, snake)
            continue
        raise TypeError(f"会话对象缺少字段 {key}: {type(session).__name__}")
    return out


def _session_dto(raw: dict[str, Any], mode: Any) -> dict[str, Any]:
    """Java `new SessionDto(sessionId, workspaceId, mode, createdAt, null, name)`。

    【adapterType 恒为 null 且必须输出】Java 侧是 record 组件，Jackson **不会**省略它
    （探针实测 `"adapterType":null`）；前端按这个键存在与否判断会话来源。
    """
    return {
        "sessionId": raw.get("sessionId"),
        "workspaceId": raw.get("workspaceId"),
        "mode": _raw_text(mode),
        "createdAt": _wire_instant(raw.get("createdAt")),
        "adapterType": None,
        "name": raw.get("name"),
    }


def _message_json(message: Any) -> dict[str, Any]:
    """一条对话消息 → Java `ConversationMessage` 的 10 个字段（顺序即 Jackson 的顺序）。

    真实 `ConversationHistory` 返回 `ConversationMessage` 数据类（有 `to_dict()`），
    窄桩直接存 dict —— 两种都认，并补齐 Java record 一定有、而 dict 可能缺的键。
    """
    if not isinstance(message, dict):
        to_dict = getattr(message, "to_dict", None)
        if not callable(to_dict):
            raise TypeError(f"对话历史返回了非消息对象: {type(message).__name__}")
        message = to_dict()
    out: dict[str, Any] = {}
    for key in _MESSAGE_FIELDS:
        value = message.get(key)
        if key == "timestamp":
            value = _wire_instant(value)
        elif key == "metadata" and value is None:
            value = {}                   # Java 侧 metadata 至少是 Map.of()
        out[key] = value
    return out


_SESSION_CLASS: Any = None
_SESSION_CLASS_LOOKED_UP = False


def _session_class() -> Any:
    """真实 `lionbox.sessions.Session` 数据类（缺依赖时返回 None，走 dict 形态）。"""
    global _SESSION_CLASS, _SESSION_CLASS_LOOKED_UP
    if not _SESSION_CLASS_LOOKED_UP:
        _SESSION_CLASS_LOOKED_UP = True
        try:
            from lionbox.sessions.session import Session
            _SESSION_CLASS = Session
        except ImportError:              # 依赖：lionbox.sessions（由并行任务提供）
            _SESSION_CLASS = None
    return _SESSION_CLASS


def _session_record(spec: dict[str, Any]) -> Any:
    """字段 dict → 持久化服务收得下的形态（真实 `Session` 数据类，或原样 dict）。

    Java 里 `sessionPersistence.saveSession(new Session(...))` 传的是 record；
    Python 的真实 `SessionPersistence.save_session` 也收 `Session` 数据类。
    数据类不可用时（窄桩场景）原样传 dict —— `_SessionPersistenceStub` 收得下。
    """
    cls = _session_class()
    if cls is None:
        return spec
    return cls(session_id=spec.get("sessionId"), workspace_id=spec.get("workspaceId"),
               mode=spec.get("mode"), created_at=_to_instant(spec.get("createdAt")),
               name=spec.get("name"))


def _persist_session(persistence: Any, spec: dict[str, Any]) -> None:
    """Java `sessionPersistence.saveSession(...)`。缺方法就明确报错，不假装存过。"""
    saver = getattr(persistence, "save_session", None)
    if not callable(saver):
        raise deps.DependencyMissing("会话持久化（lionbox.sessions.SessionPersistence）")
    saver(_session_record(spec))


def _clear_events(store: Any, session_id: str) -> None:
    """Java `eventStore.clearSession(id)`（清内存索引；磁盘上的事件文件保留，那是审计日志）。

    deps 的窄桩把方法叫 `clear`，真实 `lionbox.events.EventStore` 叫 `clear_session`。
    """
    fn = getattr(store, "clear_session", None) or getattr(store, "clear", None)
    if not callable(fn):
        raise deps.DependencyMissing("事件存储（lionbox.events.EventStore）")
    fn(session_id)


def _require_json(req: Request) -> Response | None:
    """`@RequestBody` 缺失 / 不是 JSON 对象 → Spring 的 400（在进方法体之前）。

    Java 探针实测：`PUT /api/sessions/sess-missing/name` 不带请求体时回的是
    400 + `{"timestamp","status":400,"error":"Bad Request","path":...}`，
    **不是** 200 的"会话不存在"业务错误 —— 顺序不能反。
    """
    if not req.body or not isinstance(req.json, dict):
        return deps.spring_error(400, req.path)
    return None


# --------------------------------------------------------------------------
# 窄桩（真实实现到位后由 ctx.install 覆盖，形状与 Java 一致）
# --------------------------------------------------------------------------


class _HistoryStub:
    """窄桩：内存对话历史。

    # 依赖：lionbox.sessions.ConversationHistory（由并行任务提供）

    只保留 SessionController 用到的方法与 **Java 的 JSON 形状**（`ConversationMessage`
    的 10 个字段），**不落盘**：磁盘上的 `conversations/<id>.json` 归真实实现管。
    存的是 Java 字段名的 dict，写入方（agent）给 dict 或带 `to_dict()` 的对象都收。
    """

    def __init__(self) -> None:
        self._messages: dict[str, list[dict[str, Any]]] = {}
        self._lock = threading.RLock()

    def add_message(self, message: Any) -> None:
        item = _message_json(message)
        with self._lock:
            self._messages.setdefault(str(item.get("sessionId")), []).append(item)

    def get_history(self, session_id: str | None) -> list[dict[str, Any]]:
        if session_id is None:
            return []
        with self._lock:
            return [dict(m) for m in self._messages.get(str(session_id), ())]

    def get_message_count(self, session_id: str | None) -> int:
        if session_id is None:
            return 0
        with self._lock:
            return len(self._messages.get(str(session_id), ()))

    def clear_history(self, session_id: str | None) -> None:
        if session_id is None:
            return
        with self._lock:
            self._messages.pop(str(session_id), None)

    def delete_from_disk(self, session_id: str | None) -> None:
        """桩没有磁盘文件可删（**不是假装删过**：桩的存储本来就在内存，`clear_history`
        已经把它清干净了；真实实现会删 `conversations/<id>.json`）。"""


class _SessionPersistenceStub:
    """窄桩：会话元数据持久化（内存表，不落盘）。

    # 依赖：lionbox.sessions.SessionPersistence（由并行任务提供）

    真实实现写 `~/lion-code-workspace/.lioncode/sessions/<id>.json`；
    桩只保证"存过、删过"在同一个进程内自洽。
    """

    def __init__(self) -> None:
        self._saved: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()

    def save_session(self, session: Any) -> bool:
        spec = _sess_raw(session)
        session_id = spec.get("sessionId")
        if session_id is None:
            return False
        with self._lock:
            self._saved[str(session_id)] = dict(spec)
        return True

    def load_session(self, session_id: str) -> dict[str, Any] | None:
        with self._lock:
            item = self._saved.get(str(session_id))
            return dict(item) if item is not None else None

    def delete_session(self, session_id: str) -> bool:
        with self._lock:
            return self._saved.pop(str(session_id), None) is not None


class _SkillRepositoryStub:
    """窄桩：会话"钉住"的技能绑定。

    # 依赖：lionbox.skills.SkillRepository（由并行任务提供）

    真实实现在 `~/.lioncode/skills` 里扫技能；桩只保留下会话级的绑定表与
    `clear_session` 的调用签名（销毁会话时清掉，避免长时间运行攒死绑定）。
    """

    def __init__(self) -> None:
        self._active: dict[str, list[str]] = {}
        self._lock = threading.RLock()

    def active_skills(self, session_id: str | None) -> list[str]:
        if session_id is None:
            return []
        with self._lock:
            return list(self._active.get(str(session_id), ()))

    def set_active(self, session_id: str | None, ids: list[str] | None) -> list[str]:
        if session_id is None:
            return []
        with self._lock:
            self._active[str(session_id)] = list(ids or [])
            return list(self._active[str(session_id)])

    def clear_session(self, session_id: str | None) -> None:
        if session_id is None:
            return
        with self._lock:
            self._active.pop(str(session_id), None)


def _default_history() -> Any:
    """`history` 服务的默认实现：真实 `ConversationHistory`。

    `auto_load=True` 与 Java 的 `@PostConstruct init()` 一致（启动时把
    `~/lion-code-workspace/.lioncode/conversations/*.json` 读进内存），
    否则 `GET /api/sessions/{id}/history` 会看不到 Java 版看得到的历史。
    模块缺失时才退回 `_HistoryStub`（窄桩，进程内自洽但不落盘）。
    """
    try:
        from lionbox.sessions import ConversationHistory
    except ImportError:                  # 依赖：lionbox.sessions（由并行任务提供）
        return _HistoryStub()
    return ConversationHistory(auto_load=True)


def _default_skill_repository() -> Any:
    """`skill_repository` 服务的默认实现：真实 `SkillRepository` 单例。

    与 `api/context.py` 用的是**同一个** `default_repository()` 单例 ——
    销毁会话时清掉的"钉住技能"必须是 Agent 循环看见的那一份。
    """
    try:
        from lionbox.skills.repository import default_repository
    except ImportError:                  # 依赖：lionbox.skills（由并行任务提供）
        return _SkillRepositoryStub()
    return default_repository()


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class SessionsApi:
    """`/api/sessions/*` 的 8 个接口（对应 Java SessionController）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ---- 服务定位：装配方 install 的真实实现优先 ----
    def sessions(self) -> Any:
        return deps.sessions(self.ctx)

    def workspaces(self) -> Any:
        return deps.workspaces(self.ctx)

    def events(self) -> Any:
        return deps.events(self.ctx)

    def history(self) -> Any:
        return self.ctx.service("history", _default_history)

    def skills(self) -> Any:
        return self.ctx.service("skill_repository", _default_skill_repository)

    def persistence(self) -> Any:
        return self.ctx.service("session_persistence", _SessionPersistenceStub)

    def _provision(self) -> None:
        """装配期把共享服务装进上下文：同一进程里所有模块看到的是**同一份**会话状态。

        已经装过的（装配方的真实实现）不动 —— `ctx.service` 只在缺的时候建。
        放在 register() 里而不是首次请求时：本模块在 `api.MODULES` 里排第 2，
        先装好，后面的模块（`api/changes.py` 的 `_HistoryProxy`、`api/events.py` 会
        把这个槽位里的占位窄桩升级成真实存储）取到的就是我们这一份。

        `skill_repository` 不在这里预装：它的真实实现是 `default_repository()` 进程单例
        （谁先取都是同一个对象），预装只会在启动时白扫一遍技能目录。
        """
        self.sessions()
        self.workspaces()
        self.events()
        self.history()
        self.persistence()

    def _destroy_one(self, session_id: str) -> None:
        """Java `destroySession` 里那串清理（单删与"清空所有"共用一套）。"""
        self.sessions().destroy_session(session_id)
        self.persistence().delete_session(session_id)
        history = self.history()
        history.clear_history(session_id)
        history.delete_from_disk(session_id)
        self.skills().clear_session(session_id)
        _clear_events(self.events(), session_id)

    # ---- 注册 ----
    def register__api_sessions(self, router) -> None:
        api = self
        api._provision()

        @router.get("/api/sessions")
        def get_all_sessions(req: Request):
            store = api.sessions()
            out: list[dict[str, Any]] = []
            for session in store.get_all_sessions():
                raw = _sess_raw(session)
                out.append(_session_dto(raw, store.get_effective_mode(raw.get("sessionId"))))
            return ApiResponse.ok(out)

        @router.post("/api/sessions")
        def create_session(req: Request):
            bad = _require_json(req)
            if bad is not None:
                return bad
            body = req.json_obj()
            try:
                mode = _parse_mode(body.get("mode"))
            except InvalidMode:
                return ApiResponse.error(INVALID_MODE_ERROR.format(mode=_raw_text(body.get("mode"))))
            workspace_id = body.get("workspaceId")
            # 窄桩的 create_session 不做工作区校验（真实 SessionManager 会抛 IllegalStateError），
            # 而错误文案是硬要求 —— 这里先挡一道，真实实现到位后行为完全一致。
            if workspace_id is None or str(workspace_id).strip() == "":
                return ApiResponse.error(NO_WORKSPACE_ERROR)
            try:
                session = api.sessions().create_session(str(workspace_id), mode)
            except RuntimeError as e:      # Java: catch (IllegalStateException e)
                return ApiResponse.error(str(e))
            raw = _sess_raw(session)
            # Java 在这里显式落一次元数据（SessionManager.createSession 自己不落盘）
            _persist_session(api.persistence(), raw)
            # 新建会话用 record 自己的 mode（Java: session.mode().getCode()）
            return ApiResponse.ok(_session_dto(raw, raw.get("mode")), "会话创建成功")

        @router.put("/api/sessions/{sessionId}/name")
        def rename_session(req: Request):
            bad = _require_json(req)
            if bad is not None:
                return bad
            session_id = req.params["sessionId"]
            store = api.sessions()
            if store.get_session(session_id) is None:
                return ApiResponse.error("会话不存在: " + session_id)
            if not store.rename_session(session_id, _clean_name(req.json_obj().get("name"))):
                return ApiResponse.error("重命名失败")
            current = store.get_session(session_id)
            return ApiResponse.ok(_sess_raw(current).get("name") if current is not None else None,
                                  "已重命名")

        @router.put("/api/sessions/{sessionId}/workspace")
        def move_session_to_workspace(req: Request):
            bad = _require_json(req)
            if bad is not None:
                return bad
            session_id = req.params["sessionId"]
            store = api.sessions()
            if store.get_session(session_id) is None:
                return ApiResponse.error("会话不存在: " + session_id)
            workspace_id = req.json_obj().get("workspaceId")
            if workspace_id is None or str(workspace_id).strip() == "":
                return ApiResponse.error("缺少 workspaceId")
            workspace_id = str(workspace_id)
            if api.workspaces().get_workspace(workspace_id) is None:
                return ApiResponse.error("工作区不存在: " + workspace_id)
            if not store.move_session_to_workspace(session_id, workspace_id):
                return ApiResponse.error("换工作区失败")
            moved = store.get_session(session_id)
            if moved is None:
                return ApiResponse.error("会话不存在")
            return ApiResponse.ok(
                _session_dto(_sess_raw(moved), store.get_effective_mode(session_id)),
                "已换到新工作区")

        @router.delete("/api/sessions/{sessionId}")
        def destroy_session(req: Request):
            session_id = req.params["sessionId"]
            if session_id is None or session_id.strip() == "":
                return ApiResponse.error("缺少会话 id")
            # 先确认真的存在：不校验就删等于"删任意 id 都算成功"
            if api.sessions().get_session(session_id) is None:
                return ApiResponse.error("会话不存在: " + session_id)
            api._destroy_one(session_id)
            return ApiResponse.ok(None, "会话已销毁")

        @router.delete("/api/sessions")
        def destroy_all_sessions(req: Request):
            store = api.sessions()
            ids = [_sess_raw(s).get("sessionId") for s in store.get_all_sessions()]
            deleted = 0
            failed = 0
            for session_id in ids:
                try:
                    api._destroy_one(session_id)
                    deleted += 1
                except Exception as e:     # Java 的刻意设计：一个失败不影响其余，最后报数量
                    failed += 1
                    log__api_sessions.warning("清空对话时删除会话失败: %s - %s", session_id, e)
            log__api_sessions.info("用户清空所有对话: 共 %d 个，删除成功 %d，失败 %d", len(ids), deleted, failed)
            data = {"total": len(ids), "deleted": deleted, "failed": failed}
            message = f"已清空 {deleted} 个对话" + (f"（{failed} 个没删掉）" if failed else "")
            return ApiResponse.ok(data, message)

        @router.post("/api/sessions/{sessionId}/mode")
        def update_mode(req: Request):
            bad = _require_json(req)
            if bad is not None:
                return bad
            session_id = req.params["sessionId"]
            store = api.sessions()
            current = store.get_session(session_id)
            if current is None:
                return ApiResponse.error("会话不存在: " + session_id)
            mode_name = req.json_obj().get("mode")
            try:
                mode = _parse_mode(mode_name)
            except InvalidMode:
                return ApiResponse.error(INVALID_MODE_ERROR.format(mode=_raw_text(mode_name)))
            if not store.update_mode(session_id, mode):
                return ApiResponse.error("模式切换失败")
            # 用新模式重建元数据并落盘：modeOverrides 只在内存里，重启就没了
            latest = store.get_session(session_id)
            raw = _sess_raw(latest if latest is not None else current)
            _persist_session(api.persistence(), {**raw, "mode": mode})
            return ApiResponse.ok(mode, "模式已切换")

        @router.get("/api/sessions/{sessionId}/history")
        def get_history(req: Request):
            session_id = req.params["sessionId"]
            if api.sessions().get_session(session_id) is None:
                return ApiResponse.error("会话不存在: " + session_id)
            return ApiResponse.ok([_message_json(m) for m in api.history().get_history(session_id)])


def register__api_sessions(router, ctx) -> None:
    SessionsApi(ctx).register__api_sessions(router)


# ========================================================================
# 原模块 lionbox/api/events.py
# ========================================================================
"""事件查询接口 —— `/api/events/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\EventController.java`（56 行 / 1 个接口）：

    GET /api/events/{sessionId}?after=<epochMillis>
    → {"success":true,"message":"ok","data":[LionEvent…]}

前端 `web/index.html` 的 `pollEvents` 在任务运行期间每 800 ms 打一次这个接口
（带上"本轮见过的最大毫秒"），拿到的事件按 `eventId` 去重后画成
"🔧 调用工具 / ✅ 完成 / ❌ 失败"三行。所以 `message` 必须是 `ok`（不是默认的
"操作成功"），事件字段（eventId / sessionId / type / timestamp / data / summary）
一个都不能少 —— 少一个 `eventId`，前端每轮轮询都会把同一条事件重画一遍。

# 依赖：lionbox.events（由并行任务提供）—— 真实实现已就绪；装配方没装真实实现时，
#       装配期被 `api/sessions.py` 放进槽位的那份 `deps.EventStoreStub` 占位窄桩会在
#       第一次请求时被升级成真实存储（见 `EventApi.store`），拿不到真实存储才继续用窄桩。
"""


import re
from typing import Any

from lionbox.api import deps

#: 事件存储的查询方法名（按优先级探测）。
#: Java 是 `EventStore.getSessionEvents(sessionId)`；`deps.EventStoreStub` 与
#: `agent.loop.LocalEventStore` 这两份窄桩用的是 `list_events` / `get_events` 别名，
#: 真实 `lionbox.events.EventStore` 则是 `get_session_events`。
_QUERY_METHODS: tuple[str, ...] = ("get_session_events", "list_events", "get_events")

#: Java `Long` 的取值范围（越界的 `?after=` 在 Spring 里是类型转换失败 → 400）
_LONG_MIN = -9223372036854775808
_LONG_MAX = 9223372036854775807

#: `?after=` 非法（Spring 在进方法体之前就回 400）的哨兵
_BAD_AFTER = object()

#: 只认 ASCII 数字与正负号 —— Java 的 `Long.valueOf` 不认下划线 / 全角数字 /
#: 十六进制，Python 的 `int()` 认，所以这里不能直接把串丢给 `int()`
_LONG_RE = re.compile(r"[+-]?[0-9]+")


# --------------------------------------------------------------------------
# 取值 / 归一化
# --------------------------------------------------------------------------


def _field(item: Any, *names: str) -> Any:
    """从一条事件（dict 或对象）里取字段，兼容 camelCase 与 snake_case 两种写法。

    【为什么两种都要认】真实 `lionbox.events.LionEvent` 是 dataclass（`event_id`），
    而 deps/agent 的窄桩是 dict（`eventId`）。接口要能在任意一份实现上工作，
    但**输出**必须始终是 Java 的 camelCase 形状。
    """
    if isinstance(item, dict):
        for name in names:
            if name in item:
                return item[name]
        return None
    for name in names:
        value = getattr(item, name, None)
        if value is not None:
            return value
    return None


def _text(value: Any) -> str | None:
    """Java 的 String 字段：`null` 照旧输出 `null`。

    【为什么不省略 null 字段】`@JsonInclude(NON_NULL)` 只加在 `ApiResponse` 上，
    record 内部的字段（如 `eventId`/`summary`）Jackson 会照样输出 null。
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(getattr(value, "value", value))          # 枚举（EventType）取 value


def _data_obj(value: Any) -> dict[str, Any]:
    """`data` 永远是 JSON 对象（Java 构造器里 `data != null ? data : Map.of()`）。"""
    if isinstance(value, dict):
        return value
    return {}


def _instant_text(value: Any) -> str | None:
    """时间戳 → JSON 里的 Instant 串。

    · 已经是字符串（真实存储/窄桩写下来的 ISO-8601）→ 原样透传，
      不做 parse→format 往返：往返会把纳秒截成微秒，反而丢精度；
    · datetime / epoch 秒（`agent.loop.LocalEventStore` 写的是浮点秒）→
      用 `lionbox.events` 的同一个序列化器，保证全项目一种写法。
    """
    if value is None:
        return None
    if isinstance(value, str) and value:
        return value
    return format_timestamp(parse_timestamp(value))


def _millis_of(item: Any) -> int | None:
    """一条事件的 `Instant.toEpochMilli()`（解析不出时间戳 → None，判为"没有时间戳"）。"""
    return epoch_millis(parse_timestamp(_field(item, "timestamp")))


def _event_json(item: Any) -> dict[str, Any]:
    """把一条事件规整成 Java `LionEvent` 的 JSON 形状（键名与顺序逐字对齐）。

    字段顺序 = Java record 的组件声明序 = Jackson 的输出序，实测活体 Java
    （`GET /api/events/system`）：

        {"eventId":"…","sessionId":"system","type":"PLUGIN_LOADED","timestamp":"…Z",
         "data":{…},"summary":"插件已加载: system_info"}
    """
    if not isinstance(item, dict):
        to_dict = getattr(item, "to_dict", None)
        if callable(to_dict):
            mapped = to_dict()
            if isinstance(mapped, dict):
                item = mapped
    return {
        "eventId": _text(_field(item, "eventId", "event_id")),
        "sessionId": _text(_field(item, "sessionId", "session_id")),
        "type": _text(_field(item, "type", "eventType", "event_type")),
        "timestamp": _instant_text(_field(item, "timestamp")),
        "data": _data_obj(_field(item, "data")),
        "summary": _text(_field(item, "summary", "message")),
    }


def _parse_after(raw: Any) -> Any:
    """`?after=` 的解析（对齐 Spring 的 `@RequestParam(value="after") Long`）。

    · 缺省 / 空串 → `None`：Spring 把空串转成 null（实测 `?after=` 回 200 且不过滤）；
    · 合法 long → `int`（`<= 0` 时 EventController 自己不过滤）；
    · 其它（`abc` / `1.5` / 超出 long 范围）→ `_BAD_AFTER`：Spring 在进方法体之前
      就抛类型转换失败 → 400 + 默认错误体（实测 `?after=abc` 回 400）。
    """
    if raw is None:
        return None
    text = str(raw).strip()
    if text == "":
        return None
    if not _LONG_RE.fullmatch(text):
        return _BAD_AFTER
    value = int(text)
    if value < _LONG_MIN or value > _LONG_MAX:
        return _BAD_AFTER
    return value


def _shared_event_store() -> Any:
    """进程内共享的事件存储（`ctx.service("events", …)` 的默认工厂）。

    1. 先借插件系统那个单例：`plugins.lifecycle.default_event_sink()` 返回的就是
       `lionbox.events.store.EventStore`，插件加载/卸载事件写在它里面 ——
       接口读**同一个实例**才能看到真实状态（Java 侧 EventStore 也是单例 Bean）。
    2. 拿不到可查询的单例（磁盘不可写等降级路径，或装配方另装了别的实现）时，
       退回 `deps.EventStoreStub()` 这份窄桩：形状一致、只有内存态，
       **不假装有历史数据**，也不自己再实现一遍事件存储。
    """
    try:
        from lionbox.plugins.lifecycle import default_event_sink
    except ImportError:                                  # 裁剪过的部署：插件系统不在
        return deps.EventStoreStub()
    sink = default_event_sink()
    if callable(getattr(sink, "get_session_events", None)):
        return sink
    return deps.EventStoreStub()


class EventApi:
    """`/api/events` —— 对应 Java `EventController`。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx
        #: 装配期槽位里那份对象（`api/sessions.py` 先 provision 的占位窄桩）
        self._placeholder: Any = None

    # ------------------------------------------------------------ 事件存储
    def store(self) -> Any:
        """取事件存储（跨模块共享服务）—— 等价 Java 里注入的那个单例 `EventStore`。

        【为什么要"认领"槽位】`api/sessions.py` 排在 `api/__init__.py` 的 MODULES 第 2 位，
        它在装配期就 `deps.events(ctx)` 把**占位窄桩** `deps.EventStoreStub()` 放进了这个槽位；
        窄桩与真实事件存储是两个世界 —— 插件事件、Agent 事件都写在真实存储里，
        接口读窄桩就只能拿到空列表，前端每 800 ms 轮询的"🔧/✅/❌"永远画不出来。
        所以：**只**把装配期那份占位窄桩（还没被谁换掉时）升级成真实共享存储；
        装配方（或任何模块）自己 `ctx.install("events", …)` 进来的对象一概不动。
        """
        current = self.ctx.service("events", _shared_event_store)
        if current is self._placeholder and isinstance(current, deps.EventStoreStub):
            real = _shared_event_store()
            if not isinstance(real, deps.EventStoreStub):
                return self.ctx.install("events", real)
        return current

    def _load(self, session_id: str) -> list[Any]:
        """按会话取事件（等价 Java `eventStore.getSessionEvents(sessionId)`）。

        **不排序**：Java 的 `getSessionEvents` 直接返回内存列表（时间序由写入/加载保证），
        这里跟着存储的顺序走 —— 重新排序反而会在同毫秒事件上改变前端看到的先后。
        """
        store = self.store()
        for name in _QUERY_METHODS:
            fn = getattr(store, name, None)
            if callable(fn):
                items = fn(session_id)
                return [] if items is None else list(items)
        # 依赖缺失时不许假装成功：让 http/server.py 包成 500 并带上原因
        raise deps.DependencyMissing("事件存储（lionbox.events.store）")

    # ------------------------------------------------------------ 组装
    def payload(self, session_id: str, after: int | None) -> list[dict[str, Any]]:
        """Java `getEvents` 的方法体：取全部事件 → 可选按毫秒过滤 → 原样返回。"""
        events = self._load(session_id)
        if after is not None and after > 0:
            # 【为什么按毫秒比】前端只能表达毫秒（?after=<ms>），而事件时间戳带纳秒：
            # 拿 Instant 直接比会把"同一毫秒里的事件"每轮都重新返回一遍（Java 注释里的坑）。
            # 用 >= 含边界，边界那一毫秒可能重复返回，由前端按 eventId 去重。
            kept: list[Any] = []
            for item in events:
                millis = _millis_of(item)
                if millis is not None and millis >= after:
                    kept.append(item)
            events = kept
        return [_event_json(item) for item in events]

    # ------------------------------------------------------------ 注册
    def register__api_events(self, router) -> None:
        api = self
        # 装配期只"认领"槽位，**不**构造事件存储：真实 EventStore 的构造会顺带跑
        # 一次性的旧格式迁移（一条一个文件 → 按天分片），绝不能挡在启动路径上
        # （Java 版就是被这件事拖慢的）。这里只记下此刻槽位里的对象。
        if self.ctx.has("events"):
            self._placeholder = self.ctx.service("events", lambda: None)

        @router.get("/api/events/{sessionId}")
        def get_events(req: Request):
            after = _parse_after(req.q("after"))
            if after is _BAD_AFTER:
                # Spring 先做参数绑定再进方法体：`after=abc` 是 400，不是业务错误
                return deps.spring_error(400, req.path)
            events = api.payload(req.params.get("sessionId") or "", after)
            return ApiResponse.ok_msg("ok", events)


def register__api_events(router, ctx) -> None:
    EventApi(ctx).register__api_events(router)


# ========================================================================
# 原模块 lionbox/api/files.py
# ========================================================================
"""文件系统接口 —— `/api/filesystem/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\FileSystemController.java`
（250 行 / 4 个接口）：

    GET  /api/filesystem/browse     浏览目录（空 path 时回驱动器列表）
    GET  /api/filesystem/drives     驱动器列表
    GET  /api/filesystem/validate   校验路径（存在/目录/文件/可读/可写）
    POST /api/filesystem/mkdir      建目录（**只允许落在已注册工作区内**）

【没有依赖桩】Java 侧这个 controller 只注入了 `WorkspaceManager`，Python 侧由
`deps.workspaces(ctx)` 提供**真实实现**（同一份 `app-config.json` 的 `workspaces` 键），
所以 4 个接口都是真实实现，没有需要并行任务补的桩。

【两处必须逐字复刻 Java 语义的地方（照抄 `pathlib` 会对不上）】

1. `Path.of(...)` —— `sun.nio.fs.WindowsPathParser` 在**解析期**就拒绝非法字符并抛
   `InvalidPathException`，错误文案里带 `Illegal char <x> at index N`；`Path.toString()`
   会统一分隔符、折叠重复分隔符、去掉尾部分隔符，但**不**折叠 `.` / `..`
   （实测 Java：`Path.of(".").toAbsolutePath()` 是 `...\\Temp\\_lb_java\\.`，
   而 `Path.of("C:/Windows")` 是 `C:\\Windows`）。这些差异直接进 `currentPath` / 错误文案。

2. `Files.isWritable(...)` —— Windows 上走 `WindowsSecurity.checkAccessMask` → `AccessCheck`，
   是**基于 ACL** 的判定；Python 的 `os.access` 在 Windows 上只看"只读"属性（目录恒为 True），
   会把 `C:\\Windows` 报成可写（Java 探针实测 `writable=false`）。所以这里用标准库 `ctypes`
   调 `AccessCheck`，请求掩码取 `FILE_WRITE_DATA`——用自建 DACL 的实测反推出来的：
   同一个目录，ACE 只给 `WD` 时 Java 判可写、只给 `AD` 时判不可写，说明掩码就是
   `FILE_WRITE_DATA`（不是 `FILE_GENERIC_WRITE`）。
"""


import ctypes
import os
import shutil
import stat as stat_module
from functools import cmp_to_key
from typing import Any

from lionbox.api import deps

# --------------------------------------------------------------------------
# Java `Path.of(...)` 的等价物（sun.nio.fs.WindowsPathParser）
# --------------------------------------------------------------------------

#: JDK `WindowsPathParser.isInvalidPathChar`：这些字符在元素里非法（盘符后的冒号也算）
_INVALID_PATH_CHARS = frozenset('<>:"|?*')


class InvalidJavaPath(ValueError):
    """Java `InvalidPathException`：`message` 与 `getMessage()` 逐字一致。

    接口层直接把它拼进错误文案（`"浏览失败: " + e.getMessage()`），所以文案必须一致：
    `Illegal char <*> at index 5: C:\\Wi*ndows`、`Trailing char < > at index 10: C:\\Windows `。
    """

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


def _is_sep(ch: str) -> bool:
    # Java 的 WindowsPathParser 把 `/` 与 `\` 都当分隔符，解析期统一成 `\`
    return ch == "\\" or ch == "/"


def _split_root(text: str, raw: str) -> tuple[str, int]:
    """拆出根前缀，返回 `(root, rest_start)`；相对路径的 root 是 `""`。

    `root` 按 Java `Path.toString()` 的形态给（盘符根带尾分隔符、UNC 根带尾分隔符、
    `C:` 这种盘符相对路径不带），`rest_start` 是元素在**归一化字符串**里的起始下标
    （错误文案要给绝对下标，所以必须留着）。`raw` 只用于错误文案——Java 的
    `InvalidPathException` 原样回显传进来的那个字符串。
    """
    if not text:
        return "", 0
    if len(text) >= 2 and _is_sep(text[0]) and _is_sep(text[1]):
        # UNC：`\\\\server\\share\\...`（多余的前导分隔符会被折叠，实测 Java 如此）
        i = 2
        while i < len(text) and _is_sep(text[i]):
            i += 1
        server_end = i
        while server_end < len(text) and not _is_sep(text[server_end]):
            server_end += 1
        server = text[i:server_end]
        if not server:
            # 只有分隔符（`\\\\`）：JDK 报的是缺主机名，不是缺共享名
            raise InvalidJavaPath(f"UNC path is missing hostname: {raw}")
        if server_end >= len(text):
            raise InvalidJavaPath(f"UNC path is missing sharename: {raw}")
        j = server_end
        while j < len(text) and _is_sep(text[j]):
            j += 1
        share_end = j
        while share_end < len(text) and not _is_sep(text[share_end]):
            share_end += 1
        share = text[j:share_end]
        if not share:
            raise InvalidJavaPath(f"UNC path is missing sharename: {raw}")
        return "\\\\" + server + "\\" + share + "\\", share_end
    if len(text) >= 2 and text[1] == ":" and text[0].isalpha():
        # 盘符：`C:\\x` 是绝对路径（根 `C:\\`），`C:x` 是盘符相对路径（根 `C:`）
        if len(text) > 2 and _is_sep(text[2]):
            return text[:2] + "\\", 3
        return text[:2], 2
    if _is_sep(text[0]):
        # 根相对：`\\Windows`（toAbsolutePath 时会补上当前盘的根）
        return "\\", 1
    return "", 0


def _parse_java_path(raw: str) -> tuple[str, list[str]]:
    """`Path.of(raw)`：返回 `(root, elements)`。

    【为什么要自己写】JDK 在解析期就做三件事，`pathlib.PureWindowsPath` 一件都不做：
    1. 非法字符 → `InvalidPathException`（**不是**等到访问文件系统才报错）；
    2. 元素结尾是空格 → `Trailing char < > at index N`（`Path.of("  ")` 是非法路径，
       这也是 `/validate?path=%20%20` 在 Java 里回"路径非法"的原因）；
    3. 分隔符归一化 + 折叠重复分隔符 + 去掉尾部分隔符，但保留 `.` / `..` 元素。
    """
    text = raw.replace("/", "\\")
    root, start = _split_root(text, raw)
    # 尾部分隔符先去掉（`C:\\Windows\\` → `C:\\Windows`），根本身（`C:\\`）不受影响
    if root.endswith("\\") and start < len(text):
        text = text[:start].rstrip("\\") + "\\" + text[start:].rstrip("\\")
    elif not root:
        text = text.rstrip("\\")
    elements: list[str] = []
    i = start
    while i < len(text):
        if text[i] == "\\":
            i += 1
            continue
        begin = i
        while i < len(text) and text[i] != "\\":
            ch = text[i]
            if ch in _INVALID_PATH_CHARS or ch < " ":
                raise InvalidJavaPath(f"Illegal char <{ch}> at index {i}: {raw}")
            i += 1
        if text[i - 1] == " ":
            raise InvalidJavaPath(f"Trailing char < > at index {i - 1}: {raw}")
        elements.append(text[begin:i])
    return root, elements


def _java_path_string(root: str, elements: list[str]) -> str:
    """`Path.toString()`：相对路径原样、绝对路径补根、`C:` 这种盘符相对路径不带分隔符。"""
    if not elements:
        return root
    joined = "\\".join(elements)
    if not root:
        return joined
    return root + joined if root.endswith("\\") or root.endswith(":") else root + "\\" + joined


def _to_absolute(root: str, elements: list[str]) -> str:
    """`Path.toAbsolutePath().toString()`：相对路径前面接当前工作目录（**不做 normalize**）。

    【为什么必须用 `os.getcwd()` 而不是 `os.path.abspath`】Java 的 `toAbsolutePath()`
    只做"接上工作目录 + 归一化分隔符"，`.\\`、`..\\` 原样保留（实测 Java 探针：
    `browse?path=.` 的 `currentPath` 是 `...\\_lb_java\\.`）。`abspath` 会顺手 normalize，
    前端拿到的工作目录字符串就对不上了。
    """
    if root:
        if root.endswith(":"):
            # 盘符相对（`C:foo`）：Java 用"该盘的当前目录"补全；Win32 `GetFullPathName`
            # （`os.path.abspath` 在 Windows 上就是它）语义一致
            return os.path.abspath(_java_path_string(root, elements) or root + "\\")
        if root == "\\":
            # 根相对（`\\Windows`）：Java 补上当前盘的根
            return _default_root() + "\\".join(elements)
        return _java_path_string(root, elements)
    cwd = os.getcwd()
    if not elements:
        return cwd
    joined = "\\".join(elements)
    if cwd.endswith("\\"):
        return cwd + joined
    if cwd.endswith(":"):
        return cwd + "\\" + joined
    return cwd + "\\" + joined


def _default_root() -> str:
    """Java `WindowsFileSystem.defaultRoot()`：当前工作目录所在盘的根（`C:\\`）。"""
    drive, _ = os.path.splitdrive(os.getcwd())
    return drive + "\\" if drive else "\\"


def _parent_absolute(root: str, elements: list[str]) -> str | None:
    """`dirPath.getParent() != null ? dirPath.getParent().toAbsolutePath().toString() : null`。

    注意 `getParent()` 是拿**原路径**算的：`Path.of(".").getParent()` 是 null
    （单个相对元素没有父），而 `Path.of("C:\\Windows\\..").getParent()` 是 `C:\\Windows`。
    """
    if not elements:
        return None
    parents = elements[:-1]
    if not parents and not root:
        return None
    # 根下面的第一层元素：父目录就是根本身（`C:\\`、`\\\\server\\share\\`）
    return _to_absolute(root, parents)


def _join_java(parent: str, name: str) -> str:
    """Java `new File(dir, name).getAbsolutePath()`。"""
    if not parent:
        return name
    if parent.endswith("\\"):
        return parent + name
    return parent + "\\" + name


def _java_is_whitespace(ch: str) -> bool:
    """`Character.isWhitespace`：不含不换行空格（`\\u00a0` 等，Java 明确排除）。"""
    if ch in "\t\n\x0b\f\r\x1c\x1d\x1e\x1f":
        return True
    if ch in "\u00a0\u2007\u202f":
        return False
    return ch.isspace()


def _java_is_blank(value: str) -> bool:
    """`String.isBlank()`：空串或全空白。"""
    return all(_java_is_whitespace(ch) for ch in value)


def _spring_bool(value: str | None) -> bool:
    """Spring `StringToBooleanConverter`（`showFiles` 用了它）。

    只认 `true/on/yes/1` 与 `false/off/no/0`（忽略大小写、允许前后空白），空值回默认 false；
    其它值 Java 会抛转换异常 → Spring 回 400（调用方处理）。
    """
    if value is None or value.strip() == "":
        return False
    v = value.strip().lower()
    if v in ("true", "on", "yes", "1"):
        return True
    if v in ("false", "off", "no", "0"):
        return False
    raise ValueError(f"无效的布尔值: {value}")


def _compare_ignore_case(a: str, b: str) -> int:
    """`String.compareToIgnoreCase`：逐字符先 `toUpperCase` 再 `toLowerCase` 比较。

    【为什么不直接 `sorted(key=str.lower)`】Java 是**逐字符**转大小写，Python 的
    `str.lower()` 是整个字符串（还会对某些字符做多字符展开），排序结果会对不上，
    而目录顺序是前端直接显示的。
    """
    n1, n2 = len(a), len(b)
    for i in range(min(n1, n2)):
        c1, c2 = a[i], b[i]
        if c1 == c2:
            continue
        u1, u2 = c1.upper(), c2.upper()
        if len(u1) != 1:
            u1 = c1
        if len(u2) != 1:
            u2 = c2
        if u1 != u2:
            l1, l2 = u1.lower(), u2.lower()
            if len(l1) != 1:
                l1 = u1
            if len(l2) != 1:
                l2 = u2
            if l1 != l2:
                return ord(l1) - ord(l2)
    return n1 - n2


# --------------------------------------------------------------------------
# Windows 访问权限判定（`Files.isReadable` / `Files.isWritable` 的等价物）
# --------------------------------------------------------------------------


class _GenericMapping(ctypes.Structure):
    """Win32 `GENERIC_MAPPING`（AccessCheck 用它把通用权限映射成具体权限）。"""

    _fields_ = [("GenericRead", ctypes.c_uint32), ("GenericWrite", ctypes.c_uint32),
                ("GenericExecute", ctypes.c_uint32), ("GenericAll", ctypes.c_uint32)]


class _WindowsAcl:
    """只做一件事的 `AccessCheck` 绑定：这个路径对**当前进程令牌**是否可写。

    【为什么不能省】Java 的 `Files.isWritable` 在 Windows 上是 ACL 判定
    （`WindowsSecurity.checkAccessMask` → `AccessCheck`），不是看"只读"属性：
    实测 `C:\\Windows`、`C:\\Program Files`、`C:\\` 都是 `writable=false`，
    而 `C:\\PerfLogs`（令牌所在的 `Performance Log Users` 组有 `WD`）是 `true`。
    Python 的 `os.access(p, W_OK)` 在 Windows 上走 CRT `_waccess`（只看只读属性、
    目录恒为真），拿它当实现会让 `/validate` 对系统目录全部回 `writable=true`。
    """

    _SE_FILE_OBJECT = 1
    _DACL_SECURITY_INFORMATION = 0x00000004
    _OWNER_SECURITY_INFORMATION = 0x00000001
    _GROUP_SECURITY_INFORMATION = 0x00000002
    _TOKEN_QUERY = 0x0008
    _TOKEN_DUPLICATE = 0x0002
    _SECURITY_IMPERSONATION = 2
    _TOKEN_IMPERSONATION = 2
    #: JDK 反汇编 + 自建 DACL 实测反推：Java 请求的就是 FILE_WRITE_DATA（0x2）
    _FILE_WRITE_DATA = 0x0002

    def __init__(self) -> None:
        self.advapi32 = ctypes.WinDLL("advapi32", use_last_error=True)
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        adv, k32 = self.advapi32, self.kernel32
        adv.GetNamedSecurityInfoW.argtypes = [
            ctypes.c_wchar_p, ctypes.c_int, ctypes.c_uint32, ctypes.c_void_p, ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(ctypes.c_void_p),
            ctypes.POINTER(ctypes.c_void_p)]
        adv.GetNamedSecurityInfoW.restype = ctypes.c_uint32
        adv.OpenProcessToken.argtypes = [ctypes.c_void_p, ctypes.c_uint32,
                                         ctypes.POINTER(ctypes.c_void_p)]
        adv.OpenProcessToken.restype = ctypes.c_int
        adv.DuplicateTokenEx.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_void_p,
                                         ctypes.c_int, ctypes.c_int,
                                         ctypes.POINTER(ctypes.c_void_p)]
        adv.DuplicateTokenEx.restype = ctypes.c_int
        adv.AccessCheck.argtypes = [
            ctypes.c_void_p, ctypes.c_void_p, ctypes.c_uint32, ctypes.POINTER(_GenericMapping),
            ctypes.c_void_p, ctypes.POINTER(ctypes.c_uint32), ctypes.POINTER(ctypes.c_uint32),
            ctypes.POINTER(ctypes.c_int)]
        adv.AccessCheck.restype = ctypes.c_int
        k32.GetCurrentProcess.restype = ctypes.c_void_p
        k32.CloseHandle.argtypes = [ctypes.c_void_p]
        k32.LocalFree.argtypes = [ctypes.c_void_p]
        k32.LocalFree.restype = ctypes.c_void_p
        self.mapping = _GenericMapping(0x120089, 0x120116, 0x1200A0, 0x1F01FF)

    def _impersonation_token(self) -> ctypes.c_void_p | None:
        """`AccessCheck` 只接受**模拟**令牌（传主令牌会回 1309 ERROR_NO_IMPERSONATION_TOKEN）。"""
        primary = ctypes.c_void_p()
        if not self.advapi32.OpenProcessToken(
                self.kernel32.GetCurrentProcess(),
                self._TOKEN_QUERY | self._TOKEN_DUPLICATE, ctypes.byref(primary)):
            return None
        try:
            duplicate = ctypes.c_void_p()
            if not self.advapi32.DuplicateTokenEx(
                    primary, self._TOKEN_QUERY, None, self._SECURITY_IMPERSONATION,
                    self._TOKEN_IMPERSONATION, ctypes.byref(duplicate)):
                return None
            return duplicate
        finally:
            self.kernel32.CloseHandle(primary)

    def allows_write(self, path: str) -> bool:
        """拿不到安全描述符（路径不存在、或连 DACL 都没权限读，例如
        `C:\\Windows\\System32\\config`）时与 Java 一致：判不可写。"""
        descriptor = ctypes.c_void_p()
        rc = self.advapi32.GetNamedSecurityInfoW(
            path, self._SE_FILE_OBJECT,
            self._DACL_SECURITY_INFORMATION | self._OWNER_SECURITY_INFORMATION
            | self._GROUP_SECURITY_INFORMATION,
            None, None, None, None, ctypes.byref(descriptor))
        if rc != 0 or not descriptor:
            return False
        try:
            token = self._impersonation_token()
            if not token:
                return False
            try:
                privileges = ctypes.create_string_buffer(1024)
                size = ctypes.c_uint32(len(privileges))
                granted = ctypes.c_uint32()
                status = ctypes.c_int()
                ok = self.advapi32.AccessCheck(
                    descriptor, token, self._FILE_WRITE_DATA, ctypes.byref(self.mapping),
                    privileges, ctypes.byref(size), ctypes.byref(granted), ctypes.byref(status))
                return bool(ok) and bool(status.value)
            finally:
                self.kernel32.CloseHandle(token)
        finally:
            self.kernel32.LocalFree(descriptor)


_ACL_UNSET: Any = object()
_ACL_API: Any = _ACL_UNSET


def _acl_api() -> _WindowsAcl | None:
    """惰性装配（`ctypes.WinDLL` 只有 Windows 有；非 Windows 回 None → 退回 os.access）。"""
    global _ACL_API
    if _ACL_API is not _ACL_UNSET:
        return _ACL_API
    _ACL_API = None
    if os.name == "nt":
        try:
            _ACL_API = _WindowsAcl()
        except (OSError, AttributeError):
            _ACL_API = None
    return _ACL_API


def _allows_write(path: str) -> bool:
    api = _acl_api()
    if api is None:
        return os.access(path, os.W_OK)
    return api.allows_write(path)


def _has_readonly_attribute(path: str) -> bool:
    try:
        st = os.stat(path)
    except OSError:
        return False
    attrs = getattr(st, "st_file_attributes", 0) or 0
    return bool(attrs & getattr(stat_module, "FILE_ATTRIBUTE_READONLY", 0x1))


def _is_readable(path: str) -> bool:
    """`Files.isReadable`：`checkAccess(path, READ)` 会**真的打开一次** —— 目录开目录流
    （Windows 上是 `FindFirstFile`），文件开只读通道；开不了就是不可读（不是猜的）。

    【为什么连 `\\\\.\\pipe\\...` 要单独挡】那不是文件系统路径，`open` 会阻塞等对端，
    `/validate` 是 GET、前端会轮询，挂住一次就够难受了。
    """
    if path.startswith("\\\\") and path[2:3] in (".", "?"):
        return os.access(path, os.R_OK)
    if os.path.isdir(path):
        try:
            with os.scandir(path) as it:
                next(iter(it), None)      # 触发 FindFirstFile：能不能列目录就在这一步
            return True
        except OSError:
            return False
    try:
        handle = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0))
    except OSError:
        return False
    os.close(handle)
    return True


def _is_writable(path: str, is_dir: bool) -> bool:
    """`Files.isWritable`：`checkAccess(path, WRITE)` = ACL 必须给 `FILE_WRITE_DATA`，
    另外**文件**带只读属性时也判不可写（Java 在 ACL 通过后还会看一眼属性，目录不看）。"""
    if not _allows_write(path):
        return False
    if is_dir:
        return True
    return not _has_readonly_attribute(path)


# --------------------------------------------------------------------------
# 驱动器与目录枚举
# --------------------------------------------------------------------------


def _list_roots() -> list[str]:
    """`File.listRoots()`：Windows 上取逻辑驱动器位图，其它平台就是 `/`。"""
    if os.name != "nt":
        return ["/"]
    mask = int(ctypes.windll.kernel32.GetLogicalDrives())      # type: ignore[attr-defined]
    return [f"{chr(ord('A') + i)}:\\" for i in range(26) if mask & (1 << i)]


def _drive_infos() -> list[dict[str, Any]]:
    """`getDrives()`：映射 → 过滤不可读 → 保序（盘符升序，与 `File.listRoots()` 一致）。"""
    out: list[dict[str, Any]] = []
    for root in _list_roots():
        if not os.access(root, os.R_OK):        # Java: File.canRead()（同样是 CRT access）
            continue
        try:
            usage = shutil.disk_usage(root)
            total, free = int(usage.total), int(usage.free)
        except OSError:
            total = free = 0                    # Java 取不到空间时回 0
        label = root[:2] if root.endswith(":\\") else root
        out.append({"label": label, "path": root, "totalSpace": total,
                    "freeSpace": free, "readable": True})
    return out


def _read_entries(directory: str, current_path: str, show_files: bool) -> list[dict[str, Any]]:
    """`dir.listFiles()` 的等价物（拿不到就抛 OSError，由调用方转成 Java 的文案）。"""
    rows: list[tuple[str, bool, int | None, int]] = []
    with os.scandir(directory) as it:
        for entry in it:
            try:
                is_dir = entry.is_dir()
            except OSError:
                is_dir = False
            if not show_files and not is_dir:
                continue
            size: int | None = None
            modified = 0
            try:
                info = entry.stat()
                modified = int(info.st_mtime_ns // 1_000_000)   # Java: File.lastModified() 毫秒
                if not is_dir:
                    size = int(info.st_size)                    # Java: File.length()
            except OSError:
                size = None if is_dir else 0
            rows.append((entry.name, is_dir, size, modified))

    def compare(a: tuple[str, bool, int | None, int], b: tuple[str, bool, int | None, int]) -> int:
        if a[1] and not b[1]:
            return -1                       # 目录排前面
        if not a[1] and b[1]:
            return 1
        return _compare_ignore_case(a[0], b[0])

    rows.sort(key=cmp_to_key(compare))
    return [{"name": name, "path": _join_java(current_path, name), "isDirectory": is_dir,
             "size": size, "lastModified": modified}
            for (name, is_dir, size, modified) in rows]


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class FileSystemApi:
    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ mkdir 用
    def _inside_any_workspace(self, target: str) -> bool:
        """目标是否落在某个已注册工作区内（含工作区自身）；未注册任何工作区时一律拒绝。

        Java 侧是 `target.startsWith(root)`（Windows 上 `Path.startsWith` 按**整段名字**
        比较且忽略大小写），所以 `C:\\abc` 不算落在 `C:\\ab` 里；工作区路径本身非法就跳过。
        """
        for workspace in deps.workspaces(self.ctx).get_all_workspaces():
            raw = str(workspace.get("path") or "")
            try:
                root = _to_absolute(*_parse_java_path(raw)) if not _java_is_blank(raw) else ""
            except (InvalidJavaPath, OSError, ValueError):
                continue                    # 工作区路径本身非法：跳过（Java `catch ignored`）
            if not root:
                continue
            if _same_or_under(target, os.path.normpath(root)):
                return True
        return False

    # ------------------------------------------------------------ 注册
    def register__api_files(self, router) -> None:
        api = self

        @router.get("/api/filesystem/browse")
        def browse(req: Request):
            path = req.q("path") or ""
            # 空路径 = 还没选目录：回驱动器列表（前端第一层就是驱动器）
            if _java_is_blank(path):
                return ApiResponse.ok(_drive_infos())
            try:
                show_files = _spring_bool(req.q("showFiles"))
            except ValueError:
                return deps.spring_error(400, req.path)
            try:
                root, elements = _parse_java_path(path)
            except InvalidJavaPath as e:
                return ApiResponse.error("浏览失败: " + e.message)
            directory = _java_path_string(root, elements)
            if not os.path.isdir(directory):
                # 分开报"不存在"和"不是目录"：否则"权限不足/路径非法"看起来都像个空文件夹
                return ApiResponse.error(
                    ("不是目录: " if os.path.exists(directory) else "路径不存在: ") + path)
            current = _to_absolute(root, elements)
            if directory.startswith("\\\\.\\"):
                # 设备命名空间（`\\.\pipe` 这类）：Java 那边 `File.listFiles()` 返回 null，
                # 归到"无法读取该目录"；Python 的 scandir 只会给个空迭代器，得显式对齐
                return ApiResponse.error("无法读取该目录（权限不足或磁盘错误）: " + path)
            try:
                entries = _read_entries(directory, current, show_files)
            except OSError:
                return ApiResponse.error("无法读取该目录（权限不足或磁盘错误）: " + path)
            return ApiResponse.ok({"currentPath": current,
                                   "parentPath": _parent_absolute(root, elements),
                                   "entries": entries})

        @router.get("/api/filesystem/drives")
        def drives(req: Request):
            return ApiResponse.ok(_drive_infos())

        @router.get("/api/filesystem/validate")
        def validate(req: Request):
            raw = req.q("path")
            if raw is None:
                return deps.spring_error(400, req.path)     # 缺必填参数：Spring 直接 400
            try:
                target = _to_absolute(*_parse_java_path(raw))
                is_dir = os.path.isdir(target)
                return ApiResponse.ok({
                    "exists": os.path.exists(target),
                    "isDirectory": is_dir,
                    "isFile": os.path.isfile(target),
                    "readable": _is_readable(target),
                    "writable": _is_writable(target, is_dir),
                })
            except InvalidJavaPath:
                return ApiResponse.error("路径非法: " + raw)
            except OSError as e:
                return ApiResponse.error("检查路径失败: " + str(e))

        @router.post("/api/filesystem/mkdir")
        def create_directory(req: Request):
            media = (req.header("content-type") or "").split(";")[0].strip().lower()
            if media and media != "application/json" and not media.endswith("+json"):
                # Spring: 不支持的媒体类型（deps.spring_error 的表里没有 415，文案要自己给）
                return deps.spring_error(415, req.path, "Unsupported Media Type")
            if not (req.body or b"").strip():
                return deps.spring_error(400, req.path)     # Spring: 请求体缺失
            body = req.json
            if not isinstance(body, dict):
                return deps.spring_error(400, req.path)     # Spring: 请求体不是 JSON 对象
            value = body.get("path")
            path = "" if value is None else str(value)
            if _java_is_blank(path):
                return ApiResponse.error("路径不能为空")
            try:
                target = os.path.normpath(_to_absolute(*_parse_java_path(path)))
            except InvalidJavaPath:
                return ApiResponse.error("路径非法: " + path)
            if not api._inside_any_workspace(target):
                return ApiResponse.error(
                    "只能在本产品已注册的工作区内创建目录: " + path
                    + "（请先在界面里把该目录注册为工作区）")
            try:
                os.makedirs(target, exist_ok=True)          # Java: Files.createDirectories
            except OSError as e:
                return ApiResponse.error("创建目录失败: " + _mkdir_error(e, path))
            return ApiResponse.ok(None, "目录已创建")


def _same_or_under(target: str, root: str) -> bool:
    """`Path.startsWith`（Windows 上忽略大小写、按整段名字比较）。"""
    left = os.path.normcase(target).rstrip("\\")
    right = os.path.normcase(root).rstrip("\\")
    if not right:
        return False
    return left == right or left.startswith(right + "\\")


def _mkdir_error(exc: OSError, path: str) -> str:
    """`"创建目录失败: " + e.getMessage()`。

    Java 侧抛的是 `NoSuchFileException(file)` / `AccessDeniedException(file)` /
    `FileAlreadyExistsException(file)` —— `FileSystemException.getMessage()` 在只有 `file`
    没有 `reason` 时就是**路径本身**。实测 Java 的三种失败（目标已是文件、父级是文件、
    权限不足）回的都是路径，这里按 Win32 错误码等价映射：
    2 找不到文件、3 找不到路径、5 拒绝访问、123 文件名非法、183 已存在、267 目录名无效。
    """
    if getattr(exc, "winerror", None) in (2, 3, 5, 123, 183, 267) or isinstance(
            exc, (PermissionError, FileExistsError, NotADirectoryError, FileNotFoundError)):
        return path
    return str(exc)


def register__api_files(router, ctx) -> None:
    FileSystemApi(ctx).register__api_files(router)


# ========================================================================
# 原模块 lionbox/llm/types.py
# ========================================================================
"""模型适配层的数据类型 —— 与 Java 版 `com.lioncode.model.adapter` 的 record 一一对应。

对应关系（改字段名就是改协议，前端/AgentLoop 都按这些字段取值）：

| Java                              | 这里                        |
| --------------------------------- | --------------------------- |
| `ChatMessage` + `ChatMessage.ToolCall` | `ChatMessage` / `ToolCall` |
| `ModelChunk` + `ModelChunk.ToolCallDelta` | `ModelChunk` / `ToolCallDelta` |
| `ModelResponse` + `ModelResponse.TokenUsage` | `ModelResponse` / `TokenUsage` |
| `ModelInfo` + `ModelInfo.ThinkingLevelOption` | `ModelInfo` / `ThinkingLevelOption` |
| `ModelAdapter.AdapterType`        | `AdapterType`               |
| `ThinkingLevel`（core.agent）      | `ThinkingLevel`             |

【为什么用 dataclass 而不是 dict】Java 侧这些是强类型 record，适配器里到处 `msg.role()`；
Python 用 dataclass 才能在拼错字段名时立刻报错，而不是把拼错的键静默发到模型端点。
"""


from dataclasses import dataclass, field
from enum import Enum
from typing import Any


# --------------------------------------------------------------------------
# 思考等级（Java: com.lioncode.core.agent.ThinkingLevel）
# --------------------------------------------------------------------------


class ThinkingLevel(Enum):
    """思考等级。本地 GGUF 服务不传该参数，只有云端端点才下发。"""

    LOW = ("low", "低", 1024)
    MEDIUM = ("medium", "中", 4096)
    HIGH = ("high", "高", 16384)
    MAX = ("max", "最高", 32768)

    def __init__(self, code: str, display_name: str, token_budget: int) -> None:
        self.code = code
        self.display_name = display_name
        self.token_budget = token_budget

    @staticmethod
    def parse(name: Any, default: "ThinkingLevel | None" = None) -> "ThinkingLevel | None":
        """按名字解析（大小写不敏感）。与 Java `valueOf(name.toUpperCase())` + catch 一致：
        认不出来时**不抛错**，回落到 default（Java 侧回落 MEDIUM）。"""
        if name is None:
            return default
        try:
            return ThinkingLevel[str(name).strip().upper()]
        except KeyError:
            return default


# --------------------------------------------------------------------------
# 消息
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ToolCall:
    """模型请求的一次工具调用。`arguments` 已经解析成 dict（Java 侧同样如此）。"""

    id: str
    name: str
    arguments: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ChatMessage:
    """一条对话消息。role: system / user / assistant / tool。"""

    role: str
    content: str
    tool_calls: list[ToolCall] | None = None
    tool_call_id: str | None = None
    name: str | None = None
    reasoning_content: str | None = None

    # ---- 与 Java 的静态构造方法对齐 ----
    @staticmethod
    def system(content: str) -> "ChatMessage":
        return ChatMessage("system", content)

    @staticmethod
    def user(content: str) -> "ChatMessage":
        return ChatMessage("user", content)

    @staticmethod
    def assistant(content: str, reasoning_content: str | None = None) -> "ChatMessage":
        return ChatMessage("assistant", content, reasoning_content=reasoning_content)

    @staticmethod
    def tool_result(tool_call_id: str, content: str) -> "ChatMessage":
        return ChatMessage("tool", content, tool_call_id=tool_call_id)

    @staticmethod
    def assistant_with_tool_calls(content: str, tool_calls: list[ToolCall],
                                  reasoning_content: str | None = None) -> "ChatMessage":
        return ChatMessage("assistant", content, tool_calls=list(tool_calls),
                           reasoning_content=reasoning_content)


# --------------------------------------------------------------------------
# 流式块 / 响应
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ToolCallDelta:
    """工具调用增量。name/id 只在第一个分片里有值，arguments 按 index 累积。"""

    index: int
    id: str | None = None
    name_delta: str | None = None
    arguments_delta: str | None = None


@dataclass(frozen=True)
class ModelChunk:
    """流式模型响应块。"""

    delta_content: str = ""
    tool_call_deltas: list[ToolCallDelta] = field(default_factory=list)
    finished: bool = False
    finish_reason: str | None = None
    reasoning_content_delta: str | None = None


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


@dataclass(frozen=True)
class ModelResponse:
    """同步响应。

    `malformed_tool_call` 对应 Java 的同名字段：模型**想做**工具调用但调用残缺
    （缺 name / arguments 不是合法 JSON），这类调用已被丢弃。AgentLoop 靠它区分
    「模型正常收尾」与「模型吐了残缺调用」，后者要纠正重试。
    """

    content: str
    tool_calls: list[ToolCall] = field(default_factory=list)
    finished: bool = True
    usage: TokenUsage | None = None
    finish_reason: str | None = None
    reasoning_content: str | None = None
    malformed_tool_call: bool = False


# --------------------------------------------------------------------------
# 模型信息
# --------------------------------------------------------------------------


class ModelSource(Enum):
    CLOUD_API = "CLOUD_API"
    TOKEN_PLAN = "TOKEN_PLAN"
    LOCAL_GGUF = "LOCAL_GGUF"


@dataclass(frozen=True)
class ThinkingLevelOption:
    """Java: `ModelInfo.ThinkingLevelOption`。`isDefault` 是 JSON 里的键名。"""

    code: str
    display_name: str
    description: str
    token_budget: int
    is_default: bool

    def to_dict(self) -> dict[str, Any]:
        # 字段名与 Java record 的序列化结果一致（isDefault 是 record 里的组件名）
        return {
            "code": self.code,
            "displayName": self.display_name,
            "description": self.description,
            "tokenBudget": self.token_budget,
            "isDefault": self.is_default,
        }


@dataclass(frozen=True)
class ModelInfo:
    id: str
    name: str
    owner: str
    supports_thinking: bool
    supports_tool_calls: bool
    source: ModelSource
    tpm_limit: int | None = None
    rpm_limit: int | None = None
    thinking_levels: list[ThinkingLevelOption] = field(default_factory=list)
    max_context_tokens: int | None = None
    max_output_tokens: int | None = None

    def to_dict(self) -> dict[str, Any]:
        """Java 侧由 Jackson 序列化 record；null 字段同样会被 `NON_NULL` 省略吗？
        不会 —— 这里的 ModelInfo 是普通 record，Jackson 默认**会**输出 null。
        用 Java 实测对过：`/api/models/local` 的条目里 `tpmLimit`/`rpmLimit`
        确实出现为 null。所以这里显式保留 None，交由 json 序列化成 null。"""
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "supportsThinking": self.supports_thinking,
            "supportsToolCalls": self.supports_tool_calls,
            "source": self.source.value,
            "tpmLimit": self.tpm_limit,
            "rpmLimit": self.rpm_limit,
            "thinkingLevels": [lv.to_dict() for lv in self.thinking_levels],
            "maxContextTokens": self.max_context_tokens,
            "maxOutputTokens": self.max_output_tokens,
        }

    @staticmethod
    def simple(id: str, name: str, owner: str, supports_thinking: bool,
               supports_tool_calls: bool, source: ModelSource) -> "ModelInfo":
        return ModelInfo(id, name, owner, supports_thinking, supports_tool_calls, source)

    def default_thinking_level(self) -> ThinkingLevelOption | None:
        if not self.thinking_levels:
            return None
        for lv in self.thinking_levels:
            if lv.is_default:
                return lv
        return self.thinking_levels[0]


# --------------------------------------------------------------------------
# 适配器类型
# --------------------------------------------------------------------------


class AdapterType(Enum):
    """Java: `ModelAdapter.AdapterType`。枚举名进 `/api/chat/adapter/switch` 请求体、
    也进配置文件的 `activeAdapter`，所以名字必须一字不差。"""

    OPENAI_COMPATIBLE = "OPENAI_COMPATIBLE"
    ANTHROPIC = "ANTHROPIC"

    @staticmethod
    def parse(name: Any) -> "AdapterType | None":
        try:
            return AdapterType[str(name).strip().upper()]
        except (KeyError, AttributeError, TypeError):
            return None


# ========================================================================
# 原模块 lionbox/llm/base.py
# ========================================================================
"""适配器接口 —— 对应 Java `com.lioncode.model.adapter.ModelAdapter`。

【接口形状为什么长这样】Java 的 `chatStream` 返回 `Flux<ModelChunk>`；Python 里
用**生成器**代替：`for chunk in adapter.chat_stream(...)`，取消时 `gen.close()`
（Java 侧对应 `EventSource.cancel()`）。生成器被关闭时 `transport.iter_sse` 的
`finally` 会关掉底层连接，行为一致。

工具定义统一用 **OpenAI function calling 形状**（`{"name","description","parameters"}`），
Anthropic 适配器在内部转成 `input_schema` —— 与 Java 完全一致。
"""


from abc import ABC, abstractmethod
from collections.abc import Iterator
from typing import Any



class ModelAdapter(ABC):
    """所有适配器的基类。"""

    # ---- 身份 ----
    @property
    @abstractmethod
    def name(self) -> str:
        """适配器显示名（进 `/api/chat/adapter/status` 的 `data.name`）。"""

    @property
    @abstractmethod
    def adapter_type(self) -> AdapterType:
        """适配器类型（进 `data.type`，也是配置里 `activeAdapter` 的取值）。"""

    # ---- 能力协商 ----
    def prefers_text_tool_calls(self) -> bool:
        """该端点是否更适口「文本工具调用」约定（系统提示词里的 <tool_call> 格式）。

        返回 True 的端点不下发原生 tools 定义。目前两个内置适配器都返回 False：
        随软件拉起的 llama-server 会按模型 chat 模板解析工具调用（见
        `openai.py` 里的实测结论），云端 OpenAI 兼容 API 走原生 function calling 更稳。
        """
        return False

    def tool_definitions_rejected(self) -> bool:
        """该端点是否**刚刚拒绝过** tools 定义（HTTP 400）。

        一旦为 True，AgentLoop 下一轮就不再把 tools 下发，并且系统提示词要改回完整的
        文本 <tool_call> 说明 —— 否则会出现「工具定义被拒 + 提示词又不教文本格式」的双输局面。
        端点配置变更时应当复位。
        """
        return False

    # ---- 调用 ----
    @abstractmethod
    def chat(self, messages: list[ChatMessage], model: str,
             thinking_level: ThinkingLevel | None = None,
             tools: list[dict[str, Any]] | None = None) -> ModelResponse:
        """同步调用。"""

    def chat_with_options(self, messages: list[ChatMessage], model: str,
                          thinking_level: ThinkingLevel | None = None,
                          tools: list[dict[str, Any]] | None = None,
                          extra_body: dict[str, Any] | None = None,
                          max_tokens: int | None = None) -> ModelResponse:
        """带额外参数的同步调用（会话标题生成、审批审查这类"小任务"用）：

        - 关掉思考模型的思考过程（reasoning 会把 token 预算吃光，正文变空串）
        - 限制 max_tokens

        默认实现忽略额外参数、退回普通 chat —— **与 Java 接口默认实现一致**；
        具体适配器必须覆写它，否则额外参数会被静默丢掉。
        """
        return self.chat(messages, model, thinking_level, tools)

    @abstractmethod
    def chat_stream(self, messages: list[ChatMessage], model: str,
                    thinking_level: ThinkingLevel | None = None,
                    tools: list[dict[str, Any]] | None = None) -> Iterator[ModelChunk]:
        """流式调用（生成器）。"""

    def chat_stream_limited(self, messages: list[ChatMessage], model: str,
                            thinking_level: ThinkingLevel | None = None,
                            tools: list[dict[str, Any]] | None = None,
                            max_tokens: int | None = None) -> Iterator[ModelChunk]:
        """流式调用 + 本轮生成长度上限。

        【为什么必须能传进来】本地模型解码 11-12 token/s，llama-server 起来时带的是
        `-n 4096`，一轮话多就能写 6 分 20 秒。界面走的就是流式这条路，
        封顶只对非流式脚本生效是不够的。默认实现忽略该参数（Java 同）。
        """
        return self.chat_stream(messages, model, thinking_level, tools)

    @abstractmethod
    def available_models(self) -> list[ModelInfo]:
        """可用模型列表（拉不到时返回空列表，不抛异常 —— Java 同）。"""

    @abstractmethod
    def is_available(self) -> bool:
        """端点是否可用（配置齐了就算可用，不做连通性探测）。"""

    @abstractmethod
    def update_config(self, config: dict[str, Any] | None) -> None:
        """更新端点配置（baseUrl / apiKey）。"""


# ========================================================================
# 原模块 lionbox/llm/errors.py
# ========================================================================
"""适配层错误。

【为什么单独一个异常类】Java 侧抛 `RuntimeException("模型调用失败: HTTP 400 - {body}")`，
消息会被 ChatController 原样塞进 `ApiResponse.error(...)` 给用户看。这里的异常必须满足：

1. `str(e)` **直接可展示**给用户（中文、带上服务端返回的错误体，不吞细节）；
2. 消息里保留 `HTTP <code>` 字样 —— OpenAI 适配器的三层降级靠
   `"HTTP 400" in msg` 判定要不要去掉可选参数/工具定义重试。
"""



class ModelCallError(RuntimeError):
    """模型端点调用失败。`str(e)` 是给用户看的那句话。"""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message

    @property
    def http_status(self) -> int | None:
        """从消息里抠出 HTTP 状态码（没有则 None），供调用方判断是否可降级重试。"""
        marker = "HTTP "
        idx = self.message.find(marker)
        if idx < 0:
            return None
        digits = ""
        for ch in self.message[idx + len(marker):]:
            if ch.isdigit():
                digits += ch
            else:
                break
        return int(digits) if digits else None


# ========================================================================
# 原模块 lionbox/llm/transport.py
# ========================================================================
"""HTTP 传输层 —— 只用标准库 `urllib.request`。

【为什么不用 requests/httpx】PORTING.md 第一条硬约束：零第三方依赖。
Java 侧用 OkHttp，这里用 urllib，语义按需对齐：

| OkHttp 配置（Java）                         | 这里                              |
| ------------------------------------------- | --------------------------------- |
| connectTimeout 30s / writeTimeout 60s        | `CONNECT_TIMEOUT = 30`（socket 超时同时覆盖连接与写） |
| readTimeout 900s（聊天，慢在等服务端生成）    | `CHAT_READ_TIMEOUT = 900`         |
| readTimeout 20s（`/models` 必须快速失败）     | `SHORT_READ_TIMEOUT = 20`         |
| readTimeout 300s（Anthropic）                | `ANTHROPIC_READ_TIMEOUT = 300`    |
| OkHttp SSE `EventSourceListener.onEvent`     | `iter_sse()` 逐个 event 产出       |

【为什么超时这么长】同步（非流式）路径要等服务端把整段回答生成完才开始收字节；
本地模型 256K 上下文 + 最多 4096 token 输出，慢的时候要好几分钟。
`/models` 是"拉个清单"，正常几十毫秒就该回来，端点半死不活时必须快速失败，
否则会把请求线程挂满（Java 侧为此专门开了第二个 OkHttpClient）。
"""


import json
import socket
import urllib.error
import urllib.request
from collections.abc import Iterator
from typing import Any


CONNECT_TIMEOUT = 30.0
CHAT_READ_TIMEOUT = 900.0
SHORT_READ_TIMEOUT = 20.0
ANTHROPIC_READ_TIMEOUT = 300.0
WRITE_TIMEOUT = 60.0

_JSON_HEADERS = {"Content-Type": "application/json; charset=utf-8"}


def _read_error_body(exc: urllib.error.HTTPError) -> str:
    try:
        raw = exc.read()
    except Exception:  # 读错误体失败不能盖住真正的 HTTP 状态
        return "无响应体"
    if not raw:
        return "无响应体"
    return raw.decode("utf-8", errors="replace")


def _decode_json(raw: bytes) -> Any:
    if not raw:
        return None
    try:
        return json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:
        raise ModelCallError(f"模型调用失败: 响应不是合法 JSON（{e}）") from e


def _open(url: str, *, method: str, body: bytes | None, headers: dict[str, str],
          timeout: float) -> Any:
    """发一次请求。HTTP 错误一律转成 `ModelCallError`，消息里保留
    `HTTP <code>` 字样 —— 适配器的三层降级靠 `"HTTP 400" in message` 判定。"""
    req = urllib.request.Request(url, data=body, method=method)
    for k, v in headers.items():
        req.add_header(k, v)
    try:
        return urllib.request.urlopen(req, timeout=timeout)  # noqa: S310 (端点由用户配置，非外部输入拼装)
    except urllib.error.HTTPError as e:
        raise ModelCallError(f"HTTP {e.code} - {_read_error_body(e)}") from e
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", e)
        if isinstance(reason, socket.timeout):
            raise ModelCallError(f"请求超时（{timeout:.0f} 秒）: {url}") from e
        raise ModelCallError(f"无法连接模型端点: {reason}") from e
    except socket.timeout as e:
        raise ModelCallError(f"请求超时（{timeout:.0f} 秒）: {url}") from e
    except OSError as e:
        raise ModelCallError(f"网络错误: {e}") from e


def post_json(url: str, payload: dict[str, Any], *, headers: dict[str, str] | None = None,
              timeout: float = CHAT_READ_TIMEOUT, error_prefix: str = "模型调用失败") -> dict[str, Any]:
    """POST 一个 JSON 体，同步拿回完整 JSON 响应。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    hdrs = dict(_JSON_HEADERS)
    if headers:
        hdrs.update(headers)
    try:
        with _open(url, method="POST", body=body, headers=hdrs, timeout=timeout) as resp:
            data = _decode_json(resp.read())
    except ModelCallError as e:
        raise ModelCallError(f"{error_prefix}: {e}") from e
    return data if isinstance(data, dict) else {}


def get_json(url: str, *, headers: dict[str, str] | None = None,
             timeout: float = SHORT_READ_TIMEOUT) -> tuple[int, dict[str, Any]]:
    """GET 一个 JSON。返回 (状态码, 体)；非 2xx 时体为空 dict（调用方多半只需知道失败）。"""
    hdrs = {"Accept": "application/json"}
    if headers:
        hdrs.update(headers)
    try:
        with _open(url, method="GET", body=None, headers=hdrs, timeout=timeout) as resp:
            data = _decode_json(resp.read())
            return int(getattr(resp, "status", 200)), (data if isinstance(data, dict) else {})
    except ModelCallError as e:
        code = 0
        msg = str(e)
        if msg.startswith("HTTP "):
            try:
                code = int(msg.split()[1])
            except (IndexError, ValueError):
                code = 0
        return code, {}


class SseEvent:
    """一条 SSE 事件。`event` 是 `event:` 行（OkHttp 的 type），`data` 是 `data:` 行拼接。"""

    __slots__ = ("event", "data", "id")

    def __init__(self, event: str | None, data: str, id: str | None = None) -> None:
        self.event = event
        self.data = data
        self.id = id

    def __repr__(self) -> str:  # 便于日志排查
        return f"SseEvent(event={self.event!r}, data={self.data[:120]!r})"


class SseConnection:
    """已建立的 SSE 连接。

    【为什么把"建立"与"读取"分开】Java 的降级重试依赖**同步拿到 HTTP 400**：
    `EventSourceListener.onFailure(..., response.code()==400)` 时才换 stage 重发。
    Python 里如果直接用生成器，异常要等到第一次 `next()` 才抛出，重试逻辑会变得别扭。
    这里 `open_sse()` 立即发请求（同步拿到状态码），`events()` 再逐条读。
    """

    __slots__ = ("_resp", "_closed", "prefix")

    def __init__(self, resp: Any, prefix: str) -> None:
        self._resp = resp
        self._closed = False
        self.prefix = prefix

    def events(self) -> Iterator[SseEvent]:
        resp = self._resp
        event_name: str | None = None
        event_id: str | None = None
        data_lines: list[str] = []
        try:
            for raw in resp:
                line = raw.decode("utf-8", errors="replace").rstrip("\r\n")
                if line == "":
                    if data_lines:
                        yield SseEvent(event_name, "\n".join(data_lines), event_id)
                    event_name, event_id, data_lines = None, None, []
                    continue
                if line.startswith(":"):
                    continue                     # 注释/心跳
                field, _, value = line.partition(":")
                if value.startswith(" "):
                    value = value[1:]
                if field == "data":
                    data_lines.append(value)
                elif field == "event":
                    event_name = value
                elif field == "id":
                    event_id = value
            if data_lines:                        # 收尾时最后一条事件没有空行分隔
                yield SseEvent(event_name, "\n".join(data_lines), event_id)
        except ModelCallError:
            raise
        except (socket.timeout, OSError) as e:
            raise ModelCallError(f"{self.prefix}: 流式读取中断: {e}") from e

    def close(self) -> None:
        """取消订阅（Java: `EventSource.cancel()`）。重复调用无害。"""
        if self._closed:
            return
        self._closed = True
        try:
            self._resp.close()
        except Exception:
            pass

    def __enter__(self) -> "SseConnection":
        return self

    def __exit__(self, *exc: Any) -> None:
        self.close()


def open_sse(url: str, payload: dict[str, Any], *, headers: dict[str, str] | None = None,
             timeout: float = CHAT_READ_TIMEOUT, error_prefix: str = "模型调用失败") -> SseConnection:
    """POST 一个 JSON 体并建立 SSE 连接（同步抛出 HTTP 错误，供适配器按状态码降级）。"""
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    hdrs = dict(_JSON_HEADERS)
    hdrs.setdefault("Accept", "text/event-stream")
    if headers:
        hdrs.update(headers)
    try:
        resp = _open(url, method="POST", body=body, headers=hdrs, timeout=timeout)
    except ModelCallError as e:
        raise ModelCallError(f"{error_prefix}: {e}") from e
    return SseConnection(resp, error_prefix)


def iter_sse(url: str, payload: dict[str, Any], *, headers: dict[str, str] | None = None,
             timeout: float = CHAT_READ_TIMEOUT, error_prefix: str = "模型调用失败"
             ) -> Iterator[SseEvent]:
    """`open_sse` + `events()` 的便捷包装（用 `with` 保证连接关闭）。"""
    with open_sse(url, payload, headers=headers, timeout=timeout,
                  error_prefix=error_prefix) as conn:
        yield from conn.events()


# ========================================================================
# 原模块 lionbox/llm/openai.py
# ========================================================================
"""OpenAI 兼容适配器 —— 对应 Java `com.lioncode.model.adapter.OpenAICompatibleAdapter`（766 行）。

出厂用它对接**随软件自带、绑定回环地址**的本地模型运行时（llama.cpp / LM-Studio 等
GGUF 推理服务），也可以指到用户自己填的 OpenAI 兼容 API。要点：

- 同步 / 流式调用，工具调用（function calling）
- 三层降级重试（见 `_chat_internal` / `chat_stream_limited`）：把"用户自己填的 API"
  尽量用起来，而不是让界面上只显示一句 400
- `tools_rejected` 记忆：端点拒过 tools 定义后，AgentLoop 下一轮改回文本 <tool_call> 教学
- 惰性加载：端点由本地运行时托管时，发请求前先确保进程已起来（第一条消息才加载模型）
- API-Key 可选：本地运行时无需鉴权，留空即**不发送** Authorization 头

【与 Java 的差异（有意为之）】Java 用 Jackson 的 `ObjectNode`；这里用 dict。
Java 用 OkHttp/Reactor；这里用 `transport.py`（urllib + 生成器）。
所有**请求体字段名、响应解析规则、错误文案**逐字对齐。
"""


import json
import logging
import threading
import uuid
from collections.abc import Iterator
from typing import Any


log__llm_openai = logging.getLogger("lionbox.llm.openai")


# --------------------------------------------------------------------------
# 安全取值（Java 的 textOf / intOf）
# --------------------------------------------------------------------------


def text_of(node: Any, field: str, default: str | None) -> str | None:
    """安全取字符串字段。

    【必须自己判 None】JSON 里的 `"content": null` 若直接 `str(...)` 会变成字符串
    `"null"`，多数服务商（实测 MiMo 每一片 delta 都这样）会把 content/name/id 显式
    写成 null，不判的话模型正文会变成 `nullnullnullnull…`。
    """
    if not isinstance(node, dict):
        return default
    v = node.get(field)
    if v is None:
        return default
    if isinstance(v, str):
        return v
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    return default if not isinstance(v, str) else v


def int_of(node: Any, field: str) -> int | None:
    """安全取整数字段（缺失 / null / 非数字一律 None，绝不抛异常）。"""
    if not isinstance(node, dict):
        return None
    v = node.get(field)
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return int(v)


def parse_usage(usage_node: Any) -> TokenUsage | None:
    """解析 usage 块；服务端没给用量时返回 None。

    【为什么每个字段都要判空】以前 Java 侧是 `usageNode.get("prompt_tokens").asInt()`：
    usage 为 JSON null 时 NPE、只回 total_tokens 的实现同样 NPE，而 NPE 会从解析里冒出去
    被包成"模型调用失败"，于是**一次完全成功的回答被整段丢掉**（还会触发降级重试，白烧 token）。
    """
    if not isinstance(usage_node, dict):
        return None
    prompt = int_of(usage_node, "prompt_tokens")
    completion = int_of(usage_node, "completion_tokens")
    total = int_of(usage_node, "total_tokens")
    if prompt is None and completion is None and total is None:
        return None
    p = 0 if prompt is None else prompt
    c = 0 if completion is None else completion
    return TokenUsage(p, c, p + c if total is None else total)


def _safe_str(value: Any, fallback: str) -> str:
    """宽松转字符串：None → 用旧值；其它类型一律 str()（不抛类型错误）。

    【为什么不直接当字符串用】配置块是用户可写的 JSON（`/api/chat/adapter/config` 等），
    传个数字或对象进来时强转会抛异常，而且是在"保存配置"的请求里炸掉。
    """
    if value is None:
        return "" if fallback is None else fallback
    if isinstance(value, str):
        return value
    return str(value)


class OpenAICompatibleAdapter(ModelAdapter):
    """OpenAI 兼容协议适配器。"""

    def __init__(self, local_runtime: Any = None) -> None:
        # 本地模型运行时。用来看端点是不是由它托管，是就确保进程已经起来。
        # 用户填自己的 API 时 manages() 返回 False，永远不碰本地运行时。
        self._local_runtime = local_runtime
        self._base_url = ""
        self._api_key = ""
        self._tools_rejected = False
        self._lock = threading.RLock()

    # ------------------------------------------------------------ 身份
    @property
    def name(self) -> str:
        return "OpenAI兼容适配器"

    @property
    def adapter_type(self) -> AdapterType:
        return AdapterType.OPENAI_COMPATIBLE

    # ------------------------------------------------------------ 配置
    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def api_key(self) -> str:
        return self._api_key

    def update_config(self, config: dict[str, Any] | None) -> None:
        if config is None:
            return
        with self._lock:
            if "baseUrl" in config:
                self._base_url = _safe_str(config.get("baseUrl"), self._base_url)
            if "apiKey" in config:
                self._api_key = _safe_str(config.get("apiKey"), self._api_key)
            # 换了端点就忘掉上一次的"拒绝 tools"结论：新端点可能完全支持原生调用
            self._tools_rejected = False
        log__llm_openai.info("本地模型适配器配置已更新: baseUrl=%s", self._base_url)

    def is_available(self) -> bool:
        # 本地运行时无需 API-Key：只校验端点是否已配置
        return bool(self._base_url and self._base_url.strip())

    def tool_definitions_rejected(self) -> bool:
        return self._tools_rejected

    # ------------------------------------------------------------ 内部
    def _auth_token(self) -> str | None:
        """鉴权头取值；None 表示不发送 Authorization 头（本地运行时无需鉴权）。"""
        return self._api_key if (self._api_key and self._api_key.strip()) else None

    def _headers(self) -> dict[str, str]:
        token = self._auth_token()
        return {"Authorization": f"Bearer {token}"} if token else {}

    def _ensure_endpoint_ready(self) -> None:
        """发请求前的惰性加载钩子。

        这是整个惰性加载唯一真正需要拦截的地方：不管调用来自同步聊天、流式聊天
        还是会话标题生成，都必然经过这里。
        """
        rt = self._local_runtime
        if rt is None:
            return
        try:
            if not rt.manages(self._base_url):
                return          # 用户用的是自己的 API，本地模型不参与
            rt.ensure_running()
        except Exception as e:  # 运行时启动失败要让上层看到原因，不能静默继续
            raise ModelCallError(f"本地模型运行时启动失败: {e}") from e

    def _is_local_endpoint(self) -> bool:
        base = (self._base_url or "").lower()
        return ("localhost" in base) or ("127.0.0.1" in base) or ("0.0.0.0" in base)

    # ------------------------------------------------------------ 请求体
    def build_request(self, messages: list[ChatMessage], model: str,
                      thinking_level: ThinkingLevel | None, stream: bool,
                      tools: list[dict[str, Any]] | None,
                      strict_tool_params: bool) -> dict[str, Any]:
        request: dict[str, Any] = {"model": model, "stream": stream}

        msg_list: list[dict[str, Any]] = []
        for msg in messages:
            node: dict[str, Any] = {"role": msg.role, "content": msg.content}

            # 工具调用（过滤掉 name 为空的无效调用，防止 API 报错）
            if msg.tool_calls:
                arr: list[dict[str, Any]] = []
                for tc in msg.tool_calls:
                    if not tc.name or not tc.name.strip():
                        log__llm_openai.warning("跳过无效工具调用（name为空）: id=%s", tc.id)
                        continue
                    arr.append({
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.name,
                            "arguments": json.dumps(tc.arguments if tc.arguments is not None
                                                   else {}, ensure_ascii=False),
                        },
                    })
                if arr:                      # 全被过滤掉时不要留空数组
                    node["tool_calls"] = arr

            # 思考内容（thinking 模式必须原样回传，否则 API 报 400）
            if msg.reasoning_content and msg.reasoning_content.strip():
                node["reasoning_content"] = msg.reasoning_content

            if msg.tool_call_id is not None:
                node["tool_call_id"] = msg.tool_call_id
            msg_list.append(node)
        request["messages"] = msg_list

        # 工具定义（function calling）。统一形状：{"name","description","parameters"}
        if tools:
            tools_node: list[dict[str, Any]] = []
            for tool_def in tools:
                tools_node.append({
                    "type": "function",
                    "function": {
                        "name": tool_def.get("name"),
                        "description": tool_def.get("description"),
                        "parameters": tool_def.get("parameters"),
                    },
                })
            request["tools"] = tools_node
            # 原生 function calling 的两个配套参数（可由 strict_tool_params 关掉）：
            #   tool_choice=auto         —— 有的服务不默认走工具通道，显式声明更稳
            #   parallel_tool_calls=true —— AgentLoop 明确鼓励模型一轮给多个互不依赖的调用
            #     （提示词里写"最多 3 个"，本地 11 token/s 下就是 3 倍速）。
            #     万一某个端点不认这两个参数，下面的 HTTP 400 降级会去掉它们重试。
            if strict_tool_params:
                request["tool_choice"] = "auto"
                request["parallel_tool_calls"] = True

        # 思考等级（仅云端 API 传递，本地 GGUF 不传递）
        if thinking_level is not None and not self._is_local_endpoint():
            request["reasoning_effort"] = thinking_level.code
        return request

    # ------------------------------------------------------------ 同步调用
    def chat(self, messages: list[ChatMessage], model: str,
             thinking_level: ThinkingLevel | None = None,
             tools: list[dict[str, Any]] | None = None) -> ModelResponse:
        return self._chat_internal(messages, model, thinking_level, tools, None, None)

    def chat_with_options(self, messages: list[ChatMessage], model: str,
                          thinking_level: ThinkingLevel | None = None,
                          tools: list[dict[str, Any]] | None = None,
                          extra_body: dict[str, Any] | None = None,
                          max_tokens: int | None = None) -> ModelResponse:
        return self._chat_internal(messages, model, thinking_level, tools, extra_body, max_tokens)

    def _chat_internal(self, messages: list[ChatMessage], model: str,
                       thinking_level: ThinkingLevel | None,
                       tools: list[dict[str, Any]] | None,
                       extra_body: dict[str, Any] | None,
                       max_tokens: int | None) -> ModelResponse:
        """三层降级重试，都是为了让「用户自己填的 API」尽量能用起来：

          1. API 不认 tool_choice / parallel_tool_calls → 去掉这两个参数重试（工具定义留着）
          2. API 拒绝整个工具定义（HTTP 400）→ 去掉工具重试，Agent 退化成文本工具调用
          3. API 不认识某个可选参数（reasoning_effort / max_tokens）→ 可选参数一起去掉重试

        各家 OpenAI 兼容服务对可选字段的容忍度差别很大，例如 OpenAI 的 gpt-4o-mini
        收到 reasoning_effort 会直接 400。
        """
        last: ModelCallError | None = None
        msg = ""

        # 第 1 层：完整请求（工具定义 + tool_choice/parallel_tool_calls）
        try:
            return self._do_chat(messages, model, thinking_level, tools, extra_body,
                                 max_tokens, True)
        except ModelCallError as e:
            last, msg = e, e.message

        has_tools = bool(tools)

        # 第 2 层：不认工具配套参数 → 去掉 tool_choice / parallel_tool_calls，工具定义保留
        if has_tools and "HTTP 400" in msg:
            log__llm_openai.warning("接口不接受 tool_choice/parallel_tool_calls，去掉后重试: %s", msg)
            try:
                return self._do_chat(messages, model, thinking_level, tools, extra_body,
                                     max_tokens, False)
            except ModelCallError as e:
                last, msg = e, e.message

        # 第 3 层：整个工具定义被拒 → 去掉工具，降级成文本 <tool_call> 约定
        if has_tools and "HTTP 400" in msg:
            log__llm_openai.warning("携带工具定义调用失败，去掉工具重试（降级为XML/JSON文本工具调用）: %s", msg)
            self._tools_rejected = True     # 记下来：下一轮提示词改回文本格式教学
            try:
                return self._do_chat(messages, model, None, [], extra_body, max_tokens, False)
            except ModelCallError as e:
                last, msg = e, e.message

        # 第 4 层：可选参数被拒 → 可选参数一起去掉
        optional_rejected = "HTTP 400" in msg and any(
            k in msg for k in ("reasoning_effort", "max_tokens", "thinking",
                               "Unsupported parameter", "Invalid request parameters",
                               "tool_choice", "parallel_tool_calls"))
        if optional_rejected:
            log__llm_openai.warning("接口不接受可选参数，去掉后重试: %s", msg)
            try:
                return self._do_chat(messages, model, None, tools, None, None, False)
            except ModelCallError as e:
                last = e

        raise last if last is not None else ModelCallError("模型调用失败")

    def _do_chat(self, messages: list[ChatMessage], model: str,
                 thinking_level: ThinkingLevel | None,
                 tools: list[dict[str, Any]] | None,
                 extra_body: dict[str, Any] | None, max_tokens: int | None,
                 strict_tool_params: bool) -> ModelResponse:
        """真正发一次请求。"""
        self._ensure_endpoint_ready()       # 本地模式：第一条消息时才真正加载模型
        request = self.build_request(messages, model, thinking_level, False, tools,
                                     strict_tool_params)
        if max_tokens is not None and max_tokens > 0:
            request["max_tokens"] = max_tokens
        if extra_body:
            for k, v in extra_body.items():
                request[k] = v

        data = post_json(f"{self._base_url}/chat/completions", request,
                         headers=self._headers(), timeout=CHAT_READ_TIMEOUT)
        return self._parse_response(data)

    # ------------------------------------------------------------ 流式调用
    def chat_stream(self, messages: list[ChatMessage], model: str,
                    thinking_level: ThinkingLevel | None = None,
                    tools: list[dict[str, Any]] | None = None) -> Iterator[ModelChunk]:
        return self.chat_stream_limited(messages, model, thinking_level, tools, None)

    def chat_stream_limited(self, messages: list[ChatMessage], model: str,
                            thinking_level: ThinkingLevel | None = None,
                            tools: list[dict[str, Any]] | None = None,
                            max_tokens: int | None = None) -> Iterator[ModelChunk]:
        """流式调用，stage 0 → 1 → 2 逐级降级（HTTP 400 时）。"""
        has_tools = bool(tools)
        stage = 0
        conn = None
        while True:
            # stage 越高，请求越"朴素"
            effective_tools = [] if stage >= 2 else tools
            effective_thinking = None if stage >= 1 else thinking_level
            strict_tool_params = stage == 0
            self._ensure_endpoint_ready()
            request = self.build_request(messages, model, effective_thinking, True,
                                         effective_tools, strict_tool_params)
            if max_tokens is not None and max_tokens > 0:
                request["max_tokens"] = max_tokens
            try:
                conn = open_sse(f"{self._base_url}/chat/completions", request,
                                headers=self._headers(), timeout=CHAT_READ_TIMEOUT)
                break
            except ModelCallError as e:
                # 安全网：HTTP 400 时逐级降级（先去工具参数，再去工具定义）
                if e.http_status == 400 and stage < 2 and has_tools:
                    log__llm_openai.warning("流式请求被拒(HTTP 400)，降级到 stage %d 重试: %s",
                                stage + 1, e.message)
                    stage += 1
                    continue
                raise
        assert conn is not None
        try:
            for event in conn.events():
                data = event.data
                if data == "[DONE]":
                    return
                try:
                    yield self._parse_stream_chunk(data)
                except (ValueError, TypeError) as e:
                    log__llm_openai.warning("解析流式数据失败: %s (%s)", data, e)
        finally:
            conn.close()

    # ------------------------------------------------------------ 模型清单
    def available_models(self) -> list[ModelInfo]:
        if not self._base_url:
            return []
        status, body = get_json(f"{self._base_url}/models", headers=self._headers(),
                                timeout=SHORT_READ_TIMEOUT)
        if status < 200 or status >= 300:
            log__llm_openai.warning("获取模型列表失败: HTTP %s", status)
            return []
        return self._parse_models(body)

    def _parse_models(self, body: dict[str, Any]) -> list[ModelInfo]:
        data = body.get("data")
        if not isinstance(data, list):
            return []
        local = self._is_local_endpoint()
        models: list[ModelInfo] = []
        for model in data:
            # 【某条坏了不能带崩全部】没有 id 的条目直接跳过，其余照常返回。
            model_id = text_of(model, "id", "") or ""
            if not model_id.strip():
                continue
            owner = text_of(model, "owned_by", "unknown") or "unknown"
            models.append(ModelInfo(
                id=model_id, name=model_id, owner=owner,
                supports_thinking=False,          # 本地 GGUF 不提供云端厂商的思考等级参数
                supports_tool_calls=True,
                source=ModelSource.LOCAL_GGUF if local else ModelSource.CLOUD_API,
                tpm_limit=None, rpm_limit=None,
                thinking_levels=[],               # 本地模型不区分思考等级（前端隐藏该选项）
                max_context_tokens=int_of(model, "context_length"),
                max_output_tokens=int_of(model, "max_output_tokens"),
            ))
        return models

    # ------------------------------------------------------------ 响应解析
    def _parse_response(self, body: dict[str, Any]) -> ModelResponse:
        choices = body.get("choices")
        if not isinstance(choices, list) or not choices:
            return ModelResponse(content="", tool_calls=[], finished=True, usage=None,
                                 finish_reason="empty", reasoning_content=None)

        choice = choices[0] if isinstance(choices[0], dict) else {}
        message = choice.get("message") if isinstance(choice.get("message"), dict) else {}

        content = text_of(message, "content", "") or ""
        finish_reason = text_of(choice, "finish_reason", None)
        # 思考内容：DeepSeek 等 thinking 模式要求原样回传
        reasoning_content = text_of(message, "reasoning_content", None)

        # 解析工具调用（校验 name 有效性）。malformed=True 表示「模型确实想做工具调用，
        # 但那条调用是残缺的」—— AgentLoop 据此纠正重试，而不是当成"模型正常收尾"。
        tool_calls: list[ToolCall] = []
        malformed = False
        raw_calls = message.get("tool_calls")
        if isinstance(raw_calls, list):
            for tc in raw_calls:
                tc = tc if isinstance(tc, dict) else {}
                call_id = text_of(tc, "id", None)
                if not call_id or not call_id.strip():
                    call_id = "call_" + uuid.uuid4().hex[:8]
                name = None
                args_str = "{}"
                func = tc.get("function")
                if isinstance(func, dict):
                    name = text_of(func, "name", None)
                    args_str = text_of(func, "arguments", "{}") or "{}"
                if not name or not name.strip():
                    log__llm_openai.warning("API返回的工具调用缺少name（残缺调用）: id=%s, arguments=%s",
                                call_id, args_str)
                    malformed = True
                    continue
                try:
                    parsed = json.loads(args_str) if args_str.strip() else {}
                except ValueError:
                    # 参数不是合法 JSON：不能执行，但也不该让整次模型调用失败
                    log__llm_openai.warning("工具调用参数不是合法JSON（残缺调用）: name=%s, arguments=%s",
                                name, args_str)
                    malformed = True
                    continue
                tool_calls.append(ToolCall(call_id, name,
                                           parsed if isinstance(parsed, dict) else {}))

        return ModelResponse(content=content, tool_calls=tool_calls, finished=True,
                             usage=parse_usage(body.get("usage")),
                             finish_reason=finish_reason,
                             reasoning_content=reasoning_content,
                             malformed_tool_call=malformed)

    def _parse_stream_chunk(self, data: str) -> ModelChunk:
        root = json.loads(data)
        if not isinstance(root, dict):
            return ModelChunk()
        choices = root.get("choices")
        if not isinstance(choices, list) or not choices:
            return ModelChunk()

        choice = choices[0] if isinstance(choices[0], dict) else {}
        delta = choice.get("delta")
        if not isinstance(delta, dict):
            return ModelChunk()

        # 【坑】不能用 `"content" in delta` + str()：JSON null 会被转成字符串 "null"
        content = text_of(delta, "content", "") or ""
        finish_reason = text_of(choice, "finish_reason", None)
        reasoning_delta = text_of(delta, "reasoning_content", None)

        deltas: list[ToolCallDelta] = []
        tcs = delta.get("tool_calls")
        if isinstance(tcs, list):
            for tc in tcs:
                tc = tc if isinstance(tc, dict) else {}
                index = int_of(tc, "index")
                index = 0 if index is None else index
                call_id = text_of(tc, "id", None)
                name_delta = None
                args_delta = None
                func = tc.get("function")
                if isinstance(func, dict):
                    name_delta = text_of(func, "name", None)
                    if name_delta is not None and not name_delta.strip():
                        name_delta = None
                    args_delta = text_of(func, "arguments", None)
                deltas.append(ToolCallDelta(index=index, id=call_id,
                                            name_delta=name_delta,
                                            arguments_delta=args_delta))

        return ModelChunk(delta_content=content, tool_call_deltas=deltas,
                          finished=finish_reason is not None,
                          finish_reason=finish_reason,
                          reasoning_content_delta=reasoning_delta)


# ========================================================================
# 原模块 lionbox/llm/anthropic.py
# ========================================================================
"""Anthropic Messages API 适配器 —— 对应 Java `com.lioncode.model.adapter.AnthropicAdapter`（457 行）。

协议差异（这是本文件存在的唯一理由）：

| 维度        | OpenAI 兼容                      | Anthropic Messages              |
| ----------- | -------------------------------- | ------------------------------- |
| 路径        | `POST {base}/chat/completions`    | `POST {base}/v1/messages`       |
| 鉴权头      | `Authorization: Bearer <key>`     | `x-api-key: <key>` + `anthropic-version: 2023-06-01` |
| 系统提示词  | 一条 `role=system` 的消息         | 顶层 `system` 字符串（消息数组里不能有 system） |
| 消息内容    | 字符串                            | content 块数组（text / tool_use / tool_result） |
| 工具定义    | `function.parameters`             | 顶层 `input_schema`             |
| 工具调用    | `tool_calls[].function.arguments`（JSON 字符串） | `content[].type=tool_use` 的 `input`（对象） |
| 工具结果    | `role=tool` + `tool_call_id`      | `role=user` + `content[].type=tool_result` |
| `max_tokens`| 可选                              | **必填**（缺失即 400），默认 8192 |
| 流式事件    | `data: {...}` 的 `choices[].delta` | 事件类型 `content_block_delta` / `content_block_start` / `message_delta` / `message_stop` |

出厂只提供本地模型运行时（OpenAI 兼容协议），此适配器**不预设任何外部端点、
不内置任何云端模型清单**：必须显式配置 baseUrl + apiKey 后才可用（`is_available()`
只看 apiKey，与 Java 一致）。
"""


import json
import logging
import threading
from collections.abc import Iterator
from typing import Any


log__llm_anthropic = logging.getLogger("lionbox.llm.anthropic")

ANTHROPIC_VERSION = "2023-06-01"
# 没显式给 max_tokens 时用的默认输出上限（Messages API 这个字段是必填的）
DEFAULT_MAX_TOKENS = 8192


def _safe_str__llm_anthropic(value: Any, fallback: str) -> str:
    if value is None:
        return "" if fallback is None else fallback
    if isinstance(value, str):
        return value
    return str(value)


class AnthropicAdapter(ModelAdapter):
    def __init__(self) -> None:
        self._base_url = ""
        self._api_key = ""
        self._lock = threading.RLock()

    # ------------------------------------------------------------ 身份
    @property
    def name(self) -> str:
        return "Anthropic Claude原生适配器"

    @property
    def adapter_type(self) -> AdapterType:
        return AdapterType.ANTHROPIC

    @property
    def base_url(self) -> str:
        return self._base_url

    @property
    def api_key(self) -> str:
        return self._api_key

    # ------------------------------------------------------------ 配置
    def update_config(self, config: dict[str, Any] | None) -> None:
        if config is None:
            return
        with self._lock:
            if "baseUrl" in config:
                self._base_url = _safe_str__llm_anthropic(config.get("baseUrl"), self._base_url)
            if "apiKey" in config:
                self._api_key = _safe_str__llm_anthropic(config.get("apiKey"), self._api_key)
        log__llm_anthropic.info("Anthropic适配器配置已更新: baseUrl=%s", self._base_url)

    def is_available(self) -> bool:
        return bool(self._api_key and self._api_key.strip())

    def _headers(self) -> dict[str, str]:
        return {"x-api-key": self._api_key, "anthropic-version": ANTHROPIC_VERSION}

    # ------------------------------------------------------------ 调用
    def chat(self, messages: list[ChatMessage], model: str,
             thinking_level: ThinkingLevel | None = None,
             tools: list[dict[str, Any]] | None = None) -> ModelResponse:
        return self._chat_internal(messages, model, thinking_level, tools, None, None)

    def chat_with_options(self, messages: list[ChatMessage], model: str,
                          thinking_level: ThinkingLevel | None = None,
                          tools: list[dict[str, Any]] | None = None,
                          extra_body: dict[str, Any] | None = None,
                          max_tokens: int | None = None) -> ModelResponse:
        """必须实现：接口默认实现是"忽略额外参数、退回普通 chat"，而本适配器的
        `build_request` 把 max_tokens 写死成 8192。会话标题生成（要关思考过程）、
        审批审查（200 token 就够）传进来的 maxTokens/extraBody 会被静默丢掉，
        审查一次工具调用可能白生成 8000 个 token。"""
        return self._chat_internal(messages, model, thinking_level, tools, extra_body, max_tokens)

    def _chat_internal(self, messages: list[ChatMessage], model: str,
                       thinking_level: ThinkingLevel | None,
                       tools: list[dict[str, Any]] | None,
                       extra_body: dict[str, Any] | None,
                       max_tokens: int | None) -> ModelResponse:
        try:
            request = self.build_request(messages, model, thinking_level, False, tools, max_tokens)
            if extra_body:
                for k, v in extra_body.items():
                    request[k] = v
            data = post_json(f"{self._base_url}/v1/messages", request,
                             headers=self._headers(), timeout=ANTHROPIC_READ_TIMEOUT,
                             error_prefix="Anthropic调用失败")
            return self._parse_response(data)
        except ModelCallError:
            # 【为什么单独放行】下面的兜底会把刚抛出的 "Anthropic调用失败: HTTP 400 - ..."
            # 再包一层，界面变成 "Anthropic调用失败: Anthropic调用失败: HTTP 400 - ..."
            raise
        except Exception as e:
            log__llm_anthropic.error("Anthropic接口调用失败", exc_info=True)
            raise ModelCallError(f"Anthropic调用失败: {e}") from e

    def chat_stream(self, messages: list[ChatMessage], model: str,
                    thinking_level: ThinkingLevel | None = None,
                    tools: list[dict[str, Any]] | None = None) -> Iterator[ModelChunk]:
        return self.chat_stream_limited(messages, model, thinking_level, tools, None)

    def chat_stream_limited(self, messages: list[ChatMessage], model: str,
                            thinking_level: ThinkingLevel | None = None,
                            tools: list[dict[str, Any]] | None = None,
                            max_tokens: int | None = None) -> Iterator[ModelChunk]:
        request = self.build_request(messages, model, thinking_level, True, tools, max_tokens)
        conn = open_sse(f"{self._base_url}/v1/messages", request, headers=self._headers(),
                        timeout=ANTHROPIC_READ_TIMEOUT, error_prefix="Anthropic调用失败")
        try:
            for event in conn.events():
                try:
                    chunk = self._parse_stream_event(event.data)
                except (ValueError, TypeError) as e:
                    log__llm_anthropic.warning("解析Anthropic流式数据失败: %s (%s)", event.data, e)
                    continue
                if chunk is None:
                    continue
                yield chunk
                if chunk.finish_reason is not None:
                    return          # Java: message_delta 带 stop_reason 时 complete()
        finally:
            conn.close()

    # ------------------------------------------------------------ 请求体
    def build_request(self, messages: list[ChatMessage], model: str,
                      thinking_level: ThinkingLevel | None, stream: bool,
                      tools: list[dict[str, Any]] | None,
                      max_tokens: int | None) -> dict[str, Any]:
        request: dict[str, Any] = {
            "model": model,
            "max_tokens": max_tokens if (max_tokens is not None and max_tokens > 0)
            else DEFAULT_MAX_TOKENS,
            "stream": stream,
        }

        # 提取系统消息（Anthropic 把它放在顶层，而不是消息数组里）
        system_prompt = "\n".join(m.content for m in messages if m.role == "system")
        if system_prompt.strip():
            request["system"] = system_prompt.strip()

        msg_list: list[dict[str, Any]] = []
        for msg in messages:
            if msg.role == "system":
                continue
            node: dict[str, Any] = {"role": msg.role}
            content: list[dict[str, Any]] = []

            if msg.tool_calls:
                # 工具调用：content 块数组里的 tool_use（+ 可选正文）
                for tc in msg.tool_calls:
                    content.append({"type": "tool_use", "id": tc.id, "name": tc.name,
                                    "input": tc.arguments if tc.arguments is not None else {}})
                if msg.content and msg.content.strip():
                    content.append({"type": "text", "text": msg.content})
            elif msg.tool_call_id is not None:
                # 工具结果
                content.append({"type": "tool_result", "tool_use_id": msg.tool_call_id,
                                "content": msg.content})
            else:
                content.append({"type": "text", "text": msg.content})

            node["content"] = content
            msg_list.append(node)
        request["messages"] = msg_list

        # 工具定义（Anthropic 形状：顶层 name/description/input_schema）
        if tools:
            tools_node: list[dict[str, Any]] = []
            for tool_def in tools:
                tools_node.append({
                    "name": tool_def.get("name"),
                    "description": tool_def.get("description"),
                    "input_schema": tool_def.get("parameters"),
                })
            request["tools"] = tools_node

        # 思考等级（仅对支持的模型发送）
        if thinking_level is not None and self._supports_thinking(model):
            request["thinking"] = {"type": "enabled",
                                   "budget_tokens": thinking_level.token_budget}
        return request

    def _supports_thinking(self, model_id: str) -> bool:
        """本地模型运行时使用 OpenAI 兼容协议，此适配器不参与思考等级协商。"""
        return False

    # ------------------------------------------------------------ 响应解析
    def _parse_response(self, body: dict[str, Any]) -> ModelResponse:
        parts: list[str] = []
        tool_calls: list[ToolCall] = []

        blocks = body.get("content")
        if isinstance(blocks, list):
            for block in blocks:
                block = block if isinstance(block, dict) else {}
                # 逐字段判空：少一个 "type"/"text" 就抛错会让整次调用失败并触发重试
                btype = text_of(block, "type", "") or ""
                if btype == "text":
                    parts.append(text_of(block, "text", "") or "")
                elif btype == "tool_use":
                    call_id = text_of(block, "id", None)
                    name = text_of(block, "name", None)
                    if not name or not name.strip():
                        log__llm_anthropic.warning("Anthropic 返回的 tool_use 缺少 name，已丢弃: id=%s", call_id)
                        continue
                    raw_input = block.get("input")
                    args = raw_input if isinstance(raw_input, dict) else {}
                    tool_calls.append(ToolCall(call_id or "", name, args))

        content = "".join(parts)
        stop_reason = text_of(body, "stop_reason", None)
        finished = stop_reason in ("end_turn", "tool_use")

        usage: TokenUsage | None = None
        usage_node = body.get("usage")
        if isinstance(usage_node, dict):
            tokens_in = int_of(usage_node, "input_tokens")
            tokens_out = int_of(usage_node, "output_tokens")
            if tokens_in is not None or tokens_out is not None:
                i = 0 if tokens_in is None else tokens_in
                o = 0 if tokens_out is None else tokens_out
                usage = TokenUsage(i, o, i + o)

        return ModelResponse(content=content, tool_calls=tool_calls, finished=finished,
                             usage=usage, finish_reason=stop_reason, reasoning_content=None)

    def _parse_stream_event(self, data: str) -> ModelChunk | None:
        """把一条 Anthropic SSE 事件转成 `ModelChunk`；与本适配器无关的事件返回 None。"""
        event = json.loads(data)
        if not isinstance(event, dict):
            return None
        etype = text_of(event, "type", "") or ""
        index = int_of(event, "index")
        index = 0 if index is None else index

        if etype == "content_block_delta":
            delta = event.get("delta")
            if not isinstance(delta, dict):
                return None
            delta_type = text_of(delta, "type", "") or ""
            if delta_type == "text_delta":
                return ModelChunk(delta_content=text_of(delta, "text", "") or "")
            if delta_type == "input_json_delta":
                # 工具调用参数增量：与 AgentLoop 的累积器按 index 对接
                return ModelChunk(tool_call_deltas=[ToolCallDelta(
                    index=index, id=None, name_delta=None,
                    arguments_delta=text_of(delta, "partial_json", "") or "")])
            return None

        if etype == "content_block_start":
            block = event.get("content_block")
            if isinstance(block, dict) and (text_of(block, "type", "") or "") == "tool_use":
                # 工具调用开始：携带 index，供参数增量按 index 累积
                return ModelChunk(tool_call_deltas=[ToolCallDelta(
                    index=index, id=text_of(block, "id", None),
                    name_delta=text_of(block, "name", None), arguments_delta=None)])
            return None

        if etype == "message_delta":
            delta = event.get("delta")
            if isinstance(delta, dict) and delta.get("stop_reason") is not None:
                return ModelChunk(finished=True, finish_reason=str(delta.get("stop_reason")))
            return None

        if etype == "message_stop":
            return ModelChunk(finished=True)
        return None

    # ------------------------------------------------------------ 模型清单
    def available_models(self) -> list[ModelInfo]:
        """出厂只内置本地模型：此适配器不内置任何云端模型清单，
        避免 UI 或接口里冒出云端模型选项（Java 同：返回空列表）。"""
        return []


# ========================================================================
# 原模块 lionbox/llm/local.py
# ========================================================================
"""本地模型适配器 —— 指向随软件自带的 llama.cpp 运行时。

【为什么 Java 侧没有这个类，这里却有】Java 里"本地"不是一个类，而是
`OpenAICompatibleAdapter` + `LocalModelRuntime`：端点地址从 `llama.host/port`
推导成 `http://127.0.0.1:8788/v1`，发请求前由 `LocalModelRuntime.ensureRunning()`
惰性拉起进程。Python 这边保留一个**显式子类**，让"本地"有一个明确的落点：

- 端点默认值 = `http://{host}:{port}/v1`（出厂 127.0.0.1:8788）
- 永远挂着本地运行时（`manages()` 为真时发请求前确保进程已起）
- 端点配置变更后可以 `refresh_endpoint()` 重新推导（比如用户在设置里改了端口）

【绝不能改的两件事】`name` / `adapter_type` 必须与父类一致：
`/api/chat/adapter/status` 回的 `data.name` 在 Java 版是「OpenAI兼容适配器」，
前端按它显示；换个名字就是破坏兼容。
"""


from typing import Any


DEFAULT_LOCAL_HOST = "127.0.0.1"
DEFAULT_LOCAL_PORT = 8788


def local_base_url(cfg: Any = None) -> str:
    """从配置推导本地端点：`http://{llama.host}:{llama.port}/v1`。

    与 Java `AppConfigStore.localBaseUrl`（application.yml 的
    `lionbox.runtime.host/port`）语义一致；出厂值 127.0.0.1:8788。
    """
    host, port = DEFAULT_LOCAL_HOST, DEFAULT_LOCAL_PORT
    if cfg is not None:
        try:
            llama = cfg.llama() if hasattr(cfg, "llama") else {}
        except Exception:
            llama = {}
        if isinstance(llama, dict):
            host = str(llama.get("host") or host)
            try:
                port = int(llama.get("port") or port)
            except (TypeError, ValueError):
                port = DEFAULT_LOCAL_PORT
    return f"http://{host}:{port}/v1"


class LocalAdapter(OpenAICompatibleAdapter):
    """本地 GGUF 运行时适配器（OpenAI 兼容协议）。"""

    def __init__(self, local_runtime: Any = None, cfg: Any = None) -> None:
        super().__init__(local_runtime)
        self._cfg = cfg
        self._base_url = local_base_url(cfg)

    def refresh_endpoint(self) -> str:
        """重新推导端点（用户改了 llama.port 之后由调用方触发）。"""
        self._base_url = local_base_url(self._cfg)
        return self._base_url


# ========================================================================
# 原模块 lionbox/llm/manager.py
# ========================================================================
"""适配器管理器 —— 对应 Java `com.lioncode.model.adapter.AdapterManager`（141 行）
与启动恢复逻辑 `core.session.StartupRestorer`。

职责：
1. 注册两个内置适配器（OpenAI 兼容 / Anthropic），管理"当前活跃适配器"
2. 切换适配器（切换时记录 `ADAPTER_SWITCH` 事件，保护关键会话状态）
3. 启动时从 `~/.lioncode/app-config.json` 恢复端点配置与活跃适配器
   （出厂零配置时回落到本地端点 `http://127.0.0.1:8788/v1`）

【事件记录怎么接】Java 直接注入 `EventStore`；Python 侧事件存储由并行任务提供，
所以这里只接受一个 `event_recorder(session_id, data, message)` 回调，默认 None 不记录。
接入点由 `api/deps.py` 提供（模块齐了自动接上）。
"""


import logging
from collections.abc import Callable
from typing import Any


log__llm_manager = logging.getLogger("lionbox.llm.manager")

# 事件回调签名：(session_id, data, message) -> None
EventRecorder = Callable[[str | None, dict[str, Any], str], None]


class AdapterManager:
    def __init__(self, adapters: dict[AdapterType, ModelAdapter] | None = None,
                 event_recorder: EventRecorder | None = None) -> None:
        self._adapters: dict[AdapterType, ModelAdapter] = dict(adapters or {})
        self._event_recorder = event_recorder
        # 默认使用 OpenAI 兼容适配器（对本地模型运行时）
        self._active: ModelAdapter | None = self._adapters.get(AdapterType.OPENAI_COMPATIBLE)
        if self._active is not None:
            log__llm_manager.info("适配器管理器已初始化，当前适配器: %s", self._active.name)

    # ------------------------------------------------------------ 查询
    def get_active_adapter(self) -> ModelAdapter | None:
        return self._active

    def get_adapter(self, adapter_type: AdapterType) -> ModelAdapter | None:
        return self._adapters.get(adapter_type)

    def all_adapters(self) -> list[ModelAdapter]:
        return list(self._adapters.values())

    def is_adapter_available(self, adapter_type: AdapterType) -> bool:
        adapter = self._adapters.get(adapter_type)
        return adapter is not None and adapter.is_available()

    # ------------------------------------------------------------ 切换
    def restore_active_adapter(self, adapter_type: AdapterType) -> bool:
        """恢复激活适配器（启动恢复/配置保存场景）。

        **不做可用性检查**：即使端点尚未配置也先设为激活，配置保存后即生效（Java 同）。
        """
        adapter = self._adapters.get(adapter_type)
        if adapter is None:
            log__llm_manager.error("未找到适配器类型: %s", adapter_type)
            return False
        old = self._active
        self._active = adapter
        if old is not adapter and old is not None:
            log__llm_manager.info("激活适配器已恢复/切换: %s -> %s", old.name, adapter.name)
        return True

    def switch_adapter(self, adapter_type: AdapterType, session_id: str | None = None) -> bool:
        """切换适配器；目标不可用则拒绝（Java 同）。"""
        new_adapter = self._adapters.get(adapter_type)
        if new_adapter is None:
            log__llm_manager.error("未找到适配器类型: %s", adapter_type)
            return False
        old_adapter = self._active
        if not new_adapter.is_available():
            log__llm_manager.warning("目标适配器不可用: %s", adapter_type)
            return False

        # 记录切换事件（事件存储缺失时静默跳过，不阻塞切换本身）
        if self._event_recorder is not None and old_adapter is not None:
            self._event_recorder(session_id, {
                "fromAdapter": old_adapter.name,
                "toAdapter": new_adapter.name,
                "fromType": old_adapter.adapter_type.value,
                "toType": adapter_type.value,
            }, f"适配器切换: {old_adapter.name} -> {new_adapter.name}")

        self._active = new_adapter
        log__llm_manager.info("适配器已切换: %s -> %s",
                 old_adapter.name if old_adapter else "(无)", new_adapter.name)
        return True

    # ------------------------------------------------------------ 配置
    def update_adapter_config(self, adapter_type: AdapterType, config: dict[str, Any]) -> None:
        adapter = self._adapters.get(adapter_type)
        if adapter is not None:
            adapter.update_config(config)
            log__llm_manager.info("适配器配置已更新: %s", adapter_type.value)


def build_default_manager(cfg: Any, local_runtime: Any = None,
                          event_recorder: EventRecorder | None = None) -> AdapterManager:
    """按 Java `StartupRestorer.restoreAdapters()` + `AppConfigStore.applyDefaults()` 装配。

    恢复顺序（必须一致，否则首次开机会出现"适配器未配置"）：

    1. `openai` 块 → OpenAI 兼容适配器；baseUrl 缺失/空白时回落到应用级 `baseUrl`
       （再回落到本地端点）；apiKey 为空白时**不写入**，避免覆盖适配器内部状态
    2. `anthropic` 块 → Anthropic 适配器（出厂无端点，必须用户显式配置）
    3. `activeAdapter` → 活跃适配器；认不出来就用 OpenAI 兼容
    """
    def _saved(key: str) -> dict[str, Any]:
        try:
            block = cfg.get(key) if cfg is not None else None
        except Exception:
            block = None
        return block if isinstance(block, dict) else {}

    def _app_level(key: str) -> str:
        try:
            value = cfg.get(key) if cfg is not None else None
        except Exception:
            value = None
        return value if isinstance(value, str) else ""

    openai_adapter = LocalAdapter(local_runtime, cfg)
    anthropic_adapter = AnthropicAdapter()

    saved_openai = _saved("openai")
    base_url = saved_openai.get("baseUrl")
    base_url = base_url if isinstance(base_url, str) else ""
    api_key = saved_openai.get("apiKey")
    api_key = api_key if isinstance(api_key, str) else ""

    if not base_url.strip():
        base_url = _app_level("baseUrl") or local_base_url(cfg)
        log__llm_manager.info("适配器 OPENAI_COMPATIBLE 未保存端点，回落到默认本地端点: %s", base_url)

    openai_cfg: dict[str, Any] = {"baseUrl": base_url}
    if api_key.strip():
        openai_cfg["apiKey"] = api_key
    openai_adapter.update_config(openai_cfg)

    saved_anthropic = _saved("anthropic")
    anthropic_cfg: dict[str, Any] = {}
    if isinstance(saved_anthropic.get("baseUrl"), str):
        anthropic_cfg["baseUrl"] = saved_anthropic["baseUrl"]
    if isinstance(saved_anthropic.get("apiKey"), str) and saved_anthropic["apiKey"].strip():
        anthropic_cfg["apiKey"] = saved_anthropic["apiKey"]
    if anthropic_cfg:
        anthropic_adapter.update_config(anthropic_cfg)

    manager = AdapterManager({
        AdapterType.OPENAI_COMPATIBLE: openai_adapter,
        AdapterType.ANTHROPIC: anthropic_adapter,
    }, event_recorder=event_recorder)

    try:
        saved_active = cfg.get("activeAdapter") if cfg is not None else None
    except Exception:
        saved_active = None
    parsed = AdapterType.parse(saved_active) if saved_active else None
    if parsed is not None:
        manager.restore_active_adapter(parsed)
    else:
        manager.restore_active_adapter(AdapterType.OPENAI_COMPATIBLE)
    return manager


# ========================================================================
# 原模块 lionbox/llm.py
# ========================================================================
"""模型适配层：OpenAI 兼容 / Anthropic Messages / 本地 GGUF。

零第三方依赖（只用标准库 urllib + json + threading），与 Java 版
`com.lioncode.model.adapter` 包一一对应：

| Java                              | 这里              |
| --------------------------------- | ----------------- |
| `ModelAdapter`（接口）            | `base.ModelAdapter` |
| `OpenAICompatibleAdapter`         | `openai.OpenAICompatibleAdapter` |
| `AnthropicAdapter`                | `anthropic.AnthropicAdapter` |
| （无，本地端点即 OpenAI 兼容）     | `local.LocalAdapter` |
| `AdapterManager`                  | `manager.AdapterManager` |
| `ChatMessage` / `ModelChunk` / `ModelResponse` / `ModelInfo` | `types.*` |
| OkHttp + Reactor                  | `transport.py`（urllib + 生成器） |

典型用法（api 层）：

    from ..llm import build_default_manager

    adapters = build_default_manager(cfg, runtime_api.runtime)
    adapter = adapters.get_active_adapter()
    resp = adapter.chat(messages, model, ThinkingLevel.MEDIUM, tools)
    for chunk in adapter.chat_stream_limited(messages, model, level, tools, max_tokens=4096):
        ...
"""



__all__ = [
    "AdapterManager", "AdapterType", "AnthropicAdapter", "ChatMessage", "LocalAdapter",
    "ModelAdapter", "ModelCallError", "ModelChunk", "ModelInfo", "ModelResponse",
    "ModelSource", "OpenAICompatibleAdapter", "ThinkingLevel", "ThinkingLevelOption",
    "TokenUsage", "ToolCall", "ToolCallDelta", "build_default_manager", "local_base_url",
    "open_sse", "post_json",
]


# ========================================================================
# 原模块 lionbox/api/models.py
# ========================================================================
"""模型配置接口 —— `/api/models/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\ModelController.java`（165 行 / 6 个接口）。
# 依赖：lionbox.llm（由并行任务提供；已就绪，本模块用的是真实实现，没有桩）

【为什么这里一个模型字段都不自己造】Java 的六个接口全部只做「取适配器 → 包封」：
模型清单来自 `ModelAdapter.getAvailableModels()`（真去请求 `{baseUrl}/models`），
可用性来自 `isAvailable()`（端点是否配置），思考等级直接取 `ModelInfo.thinkingLevels()`。
Python 侧这套已在 `lionbox.llm`（`AdapterManager` / `OpenAICompatibleAdapter` /
`AnthropicAdapter` / `ModelInfo` / `ThinkingLevelOption`）里逐字段移植，所以本模块
**只调用适配器**：不缓存、不加工、不硬编码任何模型清单或错误文案以外的常量。

【路由登记顺序（必须与 Java 的匹配优先级一致）】`/api/models/{adapterType}` 必须
**最后**登记：`http/server.py` 的 `Router.find` 按登记顺序返回第一条命中的路由，
而 Spring 的路径匹配优先字面量段。若 `/thinking-levels` `/detail` `/local` `/cloud`
排在它后面，`GET /api/models/local` 会被当成 `adapterType` 并回 400 —— 与 Java 真值
（`data: []` 的本地模型清单）不符。
"""


import logging
from typing import Any

from lionbox.api import deps

log__api_models = logging.getLogger("lionbox.api.models")

# 「adapterType 不是合法枚举名」的哨兵。
# 【为什么不用 None】None 在 Java 里有确切含义：`@RequestParam(required = false)`
# 没传（或传了空串）时 Spring 的 StringToEnum 转换返回 null，方法体据此回落到活跃适配器。
_INVALID = object()


def _adapter_type_param(raw: str | None) -> Any:
    """查询参数 `adapterType` → `AdapterType`；`_INVALID` 表示该回 400。

    【必须自己解析，不能借用 `AdapterType.parse`】Spring 的 StringToEnum 规则是：
    空串 → null（等于没传，回落到活跃适配器）；其余 `Enum.valueOf(source.trim())`
    —— **大小写敏感**。`AdapterType.parse()` 会先 `upper()`，用它会让
    `?adapterType=anthropic` 在 Python 侧被当成合法值，而 Java 侧是
    400 Bad Request（实测真值：`GET /api/models/thinking-levels?modelId=...&adapterType=anthropic`
    → `{"timestamp":...,"status":400,"error":"Bad Request","path":"/api/models/thinking-levels"}`）。
    """
    if raw is None or raw == "":
        return None                    # Java: source.isEmpty() -> null（含 ?adapterType= 空值）
    try:
        return AdapterType[raw.strip()]
    except KeyError:
        return _INVALID


def _adapter_type_path(raw: str | None) -> Any:
    """路径参数 `{adapterType}` → `AdapterType`；`_INVALID` 表示该回 400。

    与查询参数同一套转换，唯一差别是「空」的处理：路径段至少一个字符，所以 raw 不会是
    空串；但 `/api/models/%20` 解码后是 `" "`，`Enum.valueOf(" ".trim())` 在 Java 里抛
    IllegalArgumentException（同样是 400），故 trim 后为空一律按非法处理。
    """
    if raw is None or raw.strip() == "":
        return _INVALID
    return _adapter_type_param(raw)


class ModelApi:
    """`/api/models/*` —— 对应 Java `ModelController`（构造注入的是 `AdapterManager`）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 适配器
    def adapters(self) -> Any:
        """适配器管理器（全进程共享一份）。

        【为什么走 ctx.service】`ApiContext.adapters()` 是 deps.py 给的规范入口
        （内部缓存一份）；SPEC 第 4 节又允许装配方用 `ctx.install("adapters", 真实对象)`
        替换共享服务。两个入口都认，避免出现「`/api/chat/adapter/switch` 切的是 A、
        模型清单读的还是 B」这种两个管理器并存的分叉。
        """
        return self.ctx.service("adapters", self.ctx.adapters)

    @staticmethod
    def _available(adapter: Any) -> list[Any]:
        """`adapter.getAvailableModels()` 的等价物：拿不到清单时回空列表。

        【为什么这里要 catch】Java 的 `OpenAICompatibleAdapter.getAvailableModels()`
        自己包了 `catch (Exception e) { log.error("获取模型列表异常", e); return List.of(); }`
        —— 端点没起、地址写歪、回的不是 JSON，接口回的都是 `{"success":true,"data":[]}`
        （实测真值），**不是** 500。Python 侧 `available_models()` 只在 HTTP 传输层吞掉
        `ModelCallError`；`urllib.request.Request()` 对非法 URL 抛的 `ValueError`
        （用户在设置里把 baseUrl 写成 `notaurl`）会冒到接口层。这里补齐 Java 那个 catch，
        并且照 Java 一样 `log.error`（不是静默吞掉）。
        """
        try:
            return list(adapter.available_models())
        except Exception:
            log__api_models.error("获取模型列表异常", exc_info=True)
            return []

    @staticmethod
    def _dump(models: list[Any]) -> list[dict[str, Any]]:
        """`ModelInfo` 列表 → JSON 体。

        Java 侧是 Jackson 序列化 record（11 个组件全输出，`tpmLimit`/`rpmLimit` 为 null
        时**保留 null**）；`llm.types.ModelInfo.to_dict()` 就是这个形状。
        """
        return [m.to_dict() for m in models]

    @staticmethod
    def _find(models: list[Any], model_id: str) -> Any:
        """Java: `models.stream().filter(m -> m.id().equals(modelId)).findFirst().orElse(null)`。"""
        for m in models:
            if m.id == model_id:
                return m
        return None

    # ------------------------------------------------------------ 注册
    def register__api_models(self, router) -> None:
        api = self

        # ---- 字面量路径：必须先于 `/api/models/{adapterType}` 登记（见模块文档）----

        @router.get("/api/models/thinking-levels")
        def thinking_levels(req: Request):
            # Spring 先解析 @RequestParam / @PathVariable 再进方法体：缺 modelId 或
            # adapterType 不是合法枚举名时直接 400，方法体一行都不执行。
            model_id = req.q("modelId")
            if model_id is None:
                return deps.spring_error(400, req.path)
            adapter_type = _adapter_type_param(req.q("adapterType"))
            if adapter_type is _INVALID:
                return deps.spring_error(400, req.path)

            adapter = (api.adapters().get_adapter(adapter_type) if adapter_type is not None
                       else api.adapters().get_active_adapter())
            if adapter is None or not adapter.is_available():
                return ApiResponse.error("适配器未配置或不可用")

            target = api._find(api._available(adapter), model_id)
            if target is None:
                return ApiResponse.error(f"未找到模型: {model_id}")

            levels = target.thinking_levels
            if not levels:                      # 不支持思考等级的模型回空列表
                return ApiResponse.ok([])
            return ApiResponse.ok([lv.to_dict() for lv in levels])

        @router.get("/api/models/detail")
        def model_detail(req: Request):
            model_id = req.q("modelId")
            if model_id is None:
                return deps.spring_error(400, req.path)
            adapter_type = _adapter_type_param(req.q("adapterType"))
            if adapter_type is _INVALID:
                return deps.spring_error(400, req.path)

            adapter = (api.adapters().get_adapter(adapter_type) if adapter_type is not None
                       else api.adapters().get_active_adapter())
            if adapter is None or not adapter.is_available():
                return ApiResponse.error("适配器未配置或不可用")

            target = api._find(api._available(adapter), model_id)
            if target is None:
                return ApiResponse.error(f"未找到模型: {model_id}")
            return ApiResponse.ok(target.to_dict())

        @router.get("/api/models/local")
        def local_models(req: Request):
            # Java 只看 OPENAI_COMPATIBLE 这一个适配器（本地 GGUF 与云端 API 都挂在它下面）
            adapter = api.adapters().get_adapter(AdapterType.OPENAI_COMPATIBLE)
            if adapter is None:
                return ApiResponse.error("未找到适配器")
            if not adapter.is_available():
                return ApiResponse.error("适配器不可用")
            models = api._available(adapter)
            return ApiResponse.ok(api._dump(
                [m for m in models if m.source is ModelSource.LOCAL_GGUF]))

        @router.get("/api/models/cloud")
        def cloud_models(req: Request):
            adapter = api.adapters().get_adapter(AdapterType.OPENAI_COMPATIBLE)
            if adapter is None:
                return ApiResponse.error("未找到适配器")
            if not adapter.is_available():
                return ApiResponse.error("适配器不可用")
            models = api._available(adapter)
            return ApiResponse.ok(api._dump(
                [m for m in models if m.source is not ModelSource.LOCAL_GGUF]))

        # ---- 精确路径 `/api/models` ----
        @router.get("/api/models")
        def all_models(req: Request):
            adapter = api.adapters().get_active_adapter()
            if adapter is None or not adapter.is_available():
                return ApiResponse.error("适配器未配置或不可用")
            return ApiResponse.ok(api._dump(api._available(adapter)))

        # ---- 路径变量：最后登记，否则会把上面四条字面量路径吃掉 ----
        @router.get("/api/models/{adapterType}")
        def models_by_adapter(req: Request):
            adapter_type = _adapter_type_path(req.params.get("adapterType"))
            if adapter_type is _INVALID:        # Spring 转换失败：400，不进方法体
                return deps.spring_error(400, req.path)

            adapter = api.adapters().get_adapter(adapter_type)
            if adapter is None:
                return ApiResponse.error(f"未找到适配器: {adapter_type.value}")
            if not adapter.is_available():
                return ApiResponse.error("适配器不可用")
            return ApiResponse.ok(api._dump(api._available(adapter)))


def register__api_models(router, ctx) -> None:
    ModelApi(ctx).register__api_models(router)


# ========================================================================
# 原模块 lionbox/api/approvals.py
# ========================================================================
"""审批策略接口 —— `/api/approvals`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\ApprovalController.java`（114 行 / 3 个接口）：

    GET  /api/approvals              列出全部工具及其当前审批策略
    POST /api/approvals/{toolId}     设置单个工具的审批策略
    POST /api/approvals              批量设置（`{"工具id":"策略"}`）

# 依赖：lionbox.agent.approval（由并行任务提供；**已就绪，非桩**）
    Java 侧 `ApprovalPolicy` 是 Spring 单例，同时注入 `ApprovalController` 与 `AgentLoop`；
    Python 的孪生实现是 `lionbox.agent.approval.ApprovalPolicy`（三个集合 + 一把锁 +
    出厂 AUTO_APPROVE 白名单，与 Java 逐项一致）。本模块只做接口语义：策略状态一律问它要，
    绝不在这里另存一份、也不硬编码任何策略值。
# 依赖：插件注册表（`deps.plugin_registry()` → `plugins/base.REGISTRY`，已就绪）
    等价 Java `PluginRegistry.getToolPlugins()`（工具清单来源）与 `getById(toolId)`
    （"工具是否存在"的判据）。60 个工具由 P3 任务登记，本模块不自己造清单。

【为什么策略对象走 `ctx.service("approvals")`】Java 里"接口改的策略"与"AgentLoop 判的策略"
是同一个 Spring 单例；Python 侧 `AgentLoop.__init__(approval=None)` 会自己 new 一个，
所以必须有一个共享落点：本模块用服务名 `approvals` 取（get-or-create，进程内唯一）。
装配方把 `AgentLoop(approval=ctx.service("approvals", ...))` 接上同一个实例即可，
本模块一行都不用改；反过来装配方 `ctx.install("approvals", 真实对象)` 也能直接接管
（见 SPEC 第 4 节）。

【为什么延迟导入 agent 包】`import lionbox.agent` 会连带主循环等约 200 ms 的模块，
而策略对象本身只有几十行；接口层每次启动都要装配，不值得为了它把 agent 拉进启动路径。
"""


from typing import Any

from lionbox.plugins.base import ToolPlugin
from lionbox.api import deps

#: 三条错误文案（与 Java 逐字一致，含中文全角括号）
ERR_NO_TOOL = "工具不存在: "
ERR_MISSING = "缺少策略（可选: AUTO_APPROVE / CONFIRM / BLOCK）"
ERR_INVALID = "无效策略: "
ERR_INVALID_TAIL = "（可选: AUTO_APPROVE / CONFIRM / BLOCK）"
ERR_EMPTY_BATCH = "请求体为空，应形如 {\"工具id\":\"策略\"}"

#: Java `String.trim()` 砍掉的是所有 <= U+0020 的字符，**不是** Unicode 空白
_TRIM_CHARS = "".join(chr(c) for c in range(0x21))

#: Java `Character.isWhitespace` 认的空白。故意**不含** U+00A0 / U+2007 / U+202F：
#: Java 视它们为非空白，`"\\u00a0".isBlank()` 是 false，而 Python 的 `str.isspace()`
#: 会把 U+00A0 算进去 —— 直接用 `strip()` 判断会让 `"\u00a0CONFIRM"` 在 Python 侧
#: 被当成合法策略写进配置，Java 侧却是"无效策略"。
_JAVA_SPACES = frozenset(
    "\t\n\x0b\f\r\x1c\x1d\x1e\x1f " + "".join(chr(c) for c in (
        0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x205F, 0x3000)))


class _NotString(Exception):
    """值转不成字符串 —— Jackson 反序列化 `Map<String,String>` / `String policy` 会直接 400。"""


def _java_trim(text: str) -> str:
    """Java `String.trim()`：只砍 <= U+0020（与 `str.strip()` 的全空白语义不同）。"""
    return text.strip(_TRIM_CHARS)


def _java_blank(text: str) -> bool:
    """Java `String.isBlank()`：全部字符都是 `Character.isWhitespace`（空串也算）。"""
    return all(ch in _JAVA_SPACES for ch in text)


def _jackson_string(value: Any) -> str | None:
    """Jackson 往 `String` 字段/`Map<String,String>` 里塞 JSON 值时的强转。

    实测 18099（`POST /api/approvals/tool.file.glob`，故意用非法策略以不改状态）：
    `123` -> `"无效策略: 123（…）"`、`true` -> `"无效策略: true（…）"`、
    `1.5` -> `"无效策略: 1.5（…）"` —— 即 `String.valueOf` 的语义，而不是"类型不符"。
    对象/数组转不成 String，Jackson 抛 MismatchedInputException -> Spring 400。
    """
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, bool):                 # 必须在 int 之前：Python 里 bool 是 int 的子类
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    raise _NotString(type(value).__name__)


def _new_policy() -> Any:
    """新建策略对象（Java 里由 Spring 容器保证单例，Python 侧靠 `ctx.service` 缓存）。"""
    from lionbox.agent.approval import ApprovalPolicy
    return ApprovalPolicy()


def _policy_names() -> tuple[str, ...]:
    """合法策略名 —— 单一来源是 `ApprovalPolicy.ToolPolicy`，接口层**不另抄一份**。

    【为什么必须自己校验一遍】`ApprovalPolicy.set_tool_policy` 走的是 `ToolPolicy.parse`，
    非法值会被它**静默降级成 AUTO_APPROVE**（宽松解析，供配置文件用）；而 Java 的
    `ToolPolicy.valueOf` 在控制器里抛 IllegalArgumentException 被翻译成"无效策略"。
    直接把用户输入丢给 set_tool_policy 会把"无效策略"变成"真的改了策略"。
    """
    from lionbox.agent.approval import ToolPolicy
    return tuple(ToolPolicy.ALL)


class ApprovalApi:
    """`/api/approvals` —— 对应 Java `ApprovalController`（注入 ApprovalPolicy + PluginRegistry）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 依赖
    def policy(self) -> Any:
        """共享的策略对象：`get_policy(tool_id)` / `set_tool_policy(tool_id, policy)`。"""
        return self.ctx.service("approvals", _new_policy)

    def registry(self) -> Any:
        """插件注册表（与 `/api/plugins` 用的是同一份，工具不存在时两边结论一致）。"""
        return deps.plugin_registry()

    def tools(self) -> list[Any]:
        """`PluginRegistry.getToolPlugins()` 的等价物：注册表里属于工具的那些插件。"""
        return [t for t in self.registry().all() if isinstance(t, ToolPlugin)]

    # ------------------------------------------------------------ 请求体
    @staticmethod
    def _object_body(req: Request) -> dict[str, Any] | Response:
        """Spring `@RequestBody`（必填）的等价解析：**拿不到对象就是 400**。

        实测 18099：空体、非法 JSON、字面量 `null`、数组/字符串体一律
        `400 + {"timestamp","status","error":"Bad Request","path"}`（请求根本没进方法体）；
        只有 `{}` 这类合法对象才进方法体走业务分支。这条顺序很重要 ——
        `POST /api/approvals/no.such.tool` 带空体回的是 **400 而不是"工具不存在"**。
        """
        value = req.json
        if not isinstance(value, dict):
            return deps.spring_error(400, req.path)
        return value

    # ------------------------------------------------------------ 注册
    def register__api_approvals(self, router) -> None:
        api = self

        @router.get("/api/approvals")
        def get_policies(req: Request):
            policy = api.policy()
            rows: list[dict[str, Any]] = []
            for tool in api.tools():
                desc = getattr(tool, "description", "")
                rows.append({
                    "toolId": str(tool.id),
                    "toolName": str(tool.name),
                    # record 里的字段 Jackson 会**输出** null（只有 ApiResponse 本身是 NON_NULL）
                    "description": None if desc is None else str(desc),
                    "policy": policy.get_policy(tool.id),
                })
            return ApiResponse.ok(rows)

        @router.post("/api/approvals/{toolId}")
        def set_policy(req: Request):
            body = api._object_body(req)
            if isinstance(body, Response):
                return body                    # 400：与 Java 一样在方法体之前就返回
            # 【顺序不能颠倒】Jackson 先把 `SetPolicyRequest` 整个反序列化完，再进方法体；
            # 所以"policy 是对象/数组"永远是 400，哪怕工具id 根本不存在
            # （18099 实测：`POST /api/approvals/no.such.tool` + `{"policy":{...}}` -> 400，
            #  而同一个不存在的工具 + `{"policy":"NOPE"}` -> 200 "工具不存在"）。
            try:
                raw = _jackson_string(body.get("policy"))
            except _NotString:
                return deps.spring_error(400, req.path)
            tool_id = req.params.get("toolId", "")
            if api.registry().get(tool_id) is None:
                return ApiResponse.error(ERR_NO_TOOL + tool_id)
            if raw is None or _java_blank(raw):
                return ApiResponse.error(ERR_MISSING)
            name = _java_trim(raw).upper()
            if name not in _policy_names():    # Java: ToolPolicy.valueOf 抛 IllegalArgumentException
                return ApiResponse.error(ERR_INVALID + raw + ERR_INVALID_TAIL)
            api.policy().set_tool_policy(tool_id, name)
            return ApiResponse.ok(name, "策略已更新")

        @router.post("/api/approvals")
        def set_policies(req: Request):
            body = api._object_body(req)
            if isinstance(body, Response):
                return body
            if not body:
                return ApiResponse.error(ERR_EMPTY_BATCH)
            # 先整体强转：Jackson 是把整张 Map 反序列化完才进方法体的，任何一个值
            # 是对象/数组都会 400，且**不会有半个工具的策略被改掉**。顺序不能颠倒。
            entries: list[tuple[Any, str | None]] = []
            for key, value in body.items():
                try:
                    entries.append((key, _jackson_string(value)))
                except _NotString:
                    return deps.spring_error(400, req.path)
            registry = api.registry()
            policy = api.policy()
            names = _policy_names()
            updated = 0
            skipped = 0
            for key, value in entries:
                if key is None or value is None:   # Java: entry.getKey()==null || getValue()==null
                    skipped += 1
                    continue
                name = _java_trim(value).upper()
                if name not in names:          # Java: 无效策略 -> catch IllegalArgumentException
                    skipped += 1
                    continue
                if registry.get(key) is None:  # Java: getById(key).isPresent()
                    skipped += 1
                    continue
                policy.set_tool_policy(key, name)
                updated += 1
            message = f"已更新 {updated} 个工具的策略"
            if skipped > 0:
                message += f"（跳过 {skipped} 项无效/不存在的工具）"
            # Java 是 ApiResponse.ok(message, null)：data 为 null -> NON_NULL 整个省略
            return ApiResponse.ok(None, message)


def register__api_approvals(router, ctx) -> None:
    ApprovalApi(ctx).register__api_approvals(router)


# ========================================================================
# 原模块 lionbox/api/changes.py
# ========================================================================
"""改动审核 + 上下文预算的接口 —— `/api/changes/*`、`/api/context`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\ChangeReviewController.java`（150 行 / 6 个接口）。

【为什么两个在一起（Java 注释）】它们是同一件事的两面：Agent 干活时要花钱（上下文窗口），
花完的产出要不要落地得人来点头。VS Code 侧栏和 WebUI 都靠这几个接口：
  * `GET  /api/changes?sessionId=&includeDecided=` —— 待审改动列表（带 diff）
  * `POST /api/changes/{id}/approve` —— 通过：真落盘
  * `POST /api/changes/{id}/reject`  —— 打回：不落盘，理由回给模型让它重写
  * `GET  /api/context?sessionId=`   —— 当前上下文窗口（默认值 / 会话覆盖）
  * `POST /api/context`              —— 手动设窗口

【这几条不走 `ApiResponse`】Java 这个 controller 返回的是**裸 Map**，不是 `ApiResponse`
record：`{"success":true,"enabled":…,"changes":[…],"pendingCount":…}` 里**没有 message 字段**，
失败也是 `{"success":false,"error":…}`。所以这里一律 `Response.json(...)` 手写（含状态码），
一个 `ApiResponse` 都不用 —— 多一个 `"message":"操作成功"` 就是破坏兼容。

【null 要输出，不能省略】Java 的 `summary()` / `one()` 返回 LinkedHashMap，Jackson 对 Map 的
null 值照常输出（`@JsonInclude(NON_NULL)` 只作用于 `ApiResponse` 这类 record 的属性；
同项目实测 `POST /api/plugins/sdk` 的响应体里就有 `"error":null`）。所以 `reason`、
`oldContent`、`newContent` 为 null 时原样输出 `null`。

【本模块拥有并 install 的两个共享服务（其它模块按名字取，别各自再 new）】
  * `changes`        —— `lionbox.agent.change.ChangeReview`（改文件工具的闸门）
  * `context_budget` —— `lionbox.agent.context.ContextBudget`（`context_window` 工具调的窗口）
两者都优先**借用已经接在工具接线点上的那一份**（`tools/file/_gate.REVIEW_HOOK`、
`tools/context/context_window.BUDGET`），因为 Java 里它们是 Spring 单例：工具登记改动、
controller 读列表必须是**同一个对象**，否则 `/api/changes` 会静默地永远是空的。
借用 `changes` 时还会确认它的插件开关真能读（`settings.is_enabled`）：装配方若传了答不了
这个的对象（例如整份 `AppConfigStore`），就补上 `PluginSettings` —— 不然"设置里关掉改动审核"
不会生效，与 Java 不符。

【会话历史】Java 是把"通过/打回"的结论写进 `ConversationHistory`（Spring 注入的单例）。
Python 侧按契约取 `history` 服务（`api/sessions.py` 用的就是这个名字），且**每次写入现取**
（`_HistoryProxy`）—— 装配方之后 install 真实 `ConversationHistory` 也能接上，
与 `/api/sessions/{id}/history` 读的永远是同一份。取不到时 `ChangeReview._note` 会安静跳过：
**接口响应完全不受影响**（结论仍记在改动记录里，`GET /api/changes/{id}` 看得到 reason），
只是会话里不会多出那条【人工审核】system 提示。

【`--lionbox.*` 开关】等价 Java 的 `@Value`：
  `lionbox.change-review.enabled`（默认 true）、`lionbox.agent.context-limit-tokens`（默认 16384）。
"""


import json
import logging
import re
from typing import Any

from lionbox.api import deps

log__api_changes = logging.getLogger("lionbox.api.changes")

#: 窗口下限（Java 里的字面量）：再小连系统提示 + 工具定义都放不下
MIN_TOKENS = 4096
#: 上下文窗口的出厂默认：`@Value("${lionbox.agent.context-limit-tokens:16384}")`
DEFAULT_CONTEXT_LIMIT = 16384

#: 错误文案（逐字照抄 Java —— 前端与插件按它判断，改一个字就是不兼容）
ERROR_TOKENS_NOT_INTEGER = "tokens 必须是整数"
ERROR_TOKENS_TOO_SMALL = "窗口至少 4096 token（再小连系统提示都放不下）"

#: Java `Integer.parseInt` 接受的字面量形状：可带 +/-，其余必须是十进制数字。
#: `\d` 与 Java 的 `Character.digit` 一样认全角/阿拉伯-印度数字（实测 "١٢٣٤٥" → 12345）。
_JAVA_INT = re.compile(r"[+-]?\d+")

#: Spring `StringToBooleanConverter` 认的字面量，认不出来一律 400（实测 `?includeDecided=abc` → 400）
_BOOL_TRUE = frozenset({"true", "on", "yes", "1"})
_BOOL_FALSE = frozenset({"false", "off", "no", "0"})


class _SpringError(Exception):
    """Spring 在**进方法体之前**就返回的错误（参数绑定 / 请求体反序列化失败）。

    调用方用 `deps.spring_error(e.status, req.path)` 复刻同样的状态码与错误体
    （Java 那边是 `{"timestamp","status","error","path"}`，不是业务包封体）。
    """

    def __init__(self, status: int) -> None:
        super().__init__(f"Spring {status}")
        self.status = status


# --------------------------------------------------------------------------
# Spring 参数绑定的等价物（这几条决定 400 还是 200，必须逐字对齐）
# --------------------------------------------------------------------------


def _spring_bool__api_changes(req: Request, name: str, default: bool) -> bool:
    """`@RequestParam(defaultValue="false") boolean` 的绑定规则。

    【为什么不能直接用 `req.q_bool`】Spring 认 true/on/yes/1 与 false/off/no/0（去空白、
    忽略大小写），**认不出来是 400**（实测 `?includeDecided=abc` → 400 + Spring 错误体），
    而 `req.q_bool` 会把任何不认识的值静默当成 false —— 那是把 400 悄悄变成 200。
    空值（`?includeDecided=`）走默认值（实测 200）。
    """
    raw = req.q(name)
    if raw is None:
        return default
    value = raw.strip().lower()
    if not value:
        return default
    if value in _BOOL_TRUE:
        return True
    if value in _BOOL_FALSE:
        return False
    raise _SpringError(400)


def _spring_map_body(req: Request) -> dict[str, Any] | None:
    """`@RequestBody(required=false) Map<String,Object> body` 的等价物。

    返回 None = Java 里的 `body == null`（**体长度为 0**，或者体就是 JSON `null`）。
    体不是 JSON 对象（数组/字符串/数字）或压根不是合法 JSON 时，Spring 在进方法体之前
    就回 400 —— 实测 `[]`、`{bad`、非法 UTF-8、**纯空白**（`b"   "`）都是 400，
    所以这里抛 `_SpringError(400)`；注意到 `b""` 与 `b"null"` 反而是 200（体为 null）。
    """
    raw = req.body
    if not raw:
        return None
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except (ValueError, UnicodeDecodeError) as e:      # JSON 坏了 / 不是 UTF-8
        raise _SpringError(400) from e
    if parsed is None:                                 # 体是 `null`：required=false 收到 null
        return None
    if not isinstance(parsed, dict):
        raise _SpringError(400)
    return parsed


def _java_value_string(value: Any) -> str:
    """Java `String.valueOf(Object)`：null → `"null"`，其余走 `toString()`。

    【为什么要这个】Java 侧是 `String.valueOf(body.getOrDefault("sessionId", ""))`：
      * 没这个键 → `""`
      * `"sessionId": null` → **字符串 `"null"`**（不是空串，实测会写到名为 "null" 的会话上）
      * `"reason": 123` → `"123"`
    浮点的 `Double.toString` 只在极大/极小值上与 Python 的 `str()` 有格式差异
    （Java `1.0E30` / Python `1e+30`），前端不会这么传，不做额外复刻。
    """
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return value
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, dict):                        # Java 的 AbstractMap.toString
        return "{" + ", ".join(f"{k}={_java_value_string(v)}" for k, v in value.items()) + "}"
    if isinstance(value, (list, tuple)):               # Java 的 AbstractCollection.toString
        return "[" + ", ".join(_java_value_string(v) for v in value) + "]"
    return str(value)


def _narrow_int32(value: int) -> int:
    """Java 的 long → int 窄化：取低 32 位再按有符号解释。

    实测：JSON 整数 `99999999999` → Java `Long.intValue()` → `1215752191`；
    `2147483648` → `-2147483648`。Python 的 int 是无限精度，不窄化就会不一致。
    """
    low = value & 0xFFFFFFFF
    return low - 0x100000000 if low >= 0x80000000 else low


def _narrow_double(value: float) -> int:
    """Java 的 double → int 窄化：NaN → 0、越界**饱和**到 int32 两端、否则向零取整。

    实测：`4096.9` → 4096、`1e30` → 2147483647、`1.9` → 1（判定为"小于 4096" → 400）。
    """
    if value != value:                                 # NaN
        return 0
    if value >= 2147483648.0:
        return 2147483647
    if value <= -2147483649.0:
        return -2147483648
    return int(value)                                  # int() 就是向零取整


def _as_java_int(raw: Any) -> int:
    """Java `raw instanceof Number n ? n.intValue() : Integer.parseInt(String.valueOf(raw).trim())`。

    两条路的差别要照抄（都实测过）：
      * JSON 数字 → 走 32 位窄化：`99999999999` → 1215752191、`1e30` → 2147483647；
      * 其余 → 走 `Integer.parseInt`：`" 8192 "` → 8192、`"+8192"` → 8192，
        `"8192.5"` / `"99999999999"`（**字符串**溢出）/ `true` → 400。
    :raises ValueError: 解析不出来（对应 Java 的 NumberFormatException → 400）
    """
    if isinstance(raw, bool):                          # Java: Boolean 不是 Number
        raise ValueError(ERROR_TOKENS_NOT_INTEGER)
    if isinstance(raw, int):
        return _narrow_int32(raw)
    if isinstance(raw, float):
        return _narrow_double(raw)
    text = _java_value_string(raw).strip()
    if not _JAVA_INT.fullmatch(text):
        raise ValueError(ERROR_TOKENS_NOT_INTEGER)
    value = int(text)                                  # 与 parseInt 一样只认十进制
    if not -2147483648 <= value <= 2147483647:         # parseInt 溢出也是 NumberFormatException
        raise ValueError(ERROR_TOKENS_NOT_INTEGER)
    return value


# --------------------------------------------------------------------------
# JSON 形态（逐字段照 Java 的 LinkedHashMap）
# --------------------------------------------------------------------------


def _count_lines(text: str | None) -> int:
    """Java `PendingChange.countLines`：null/空串 → 0，否则 `\\n` 个数 + 1（结尾换行算一行）。"""
    if not text:
        return 0
    return text.count("\n") + 1


def _summary_json(change: Any) -> dict[str, Any]:
    """`PendingChange.summary()` 的 JSON 形态（键名与顺序都照 Java 的 LinkedHashMap）。

    【为什么不直接调 `change.summary()`】那个方法在 `reason` 为 None 时**省略这个键**，
    而 Java 是 `m.put("reason", reason)` 无条件 put，Jackson 会输出 `"reason":null`
    （Map 的 null 值不受 `@JsonInclude(NON_NULL)` 影响）。前端按 `reason` 渲染打回理由，
    缺键和 null 在 JS 里几乎等价，但契约要求逐字段一致，所以这里按 Java 的 put 顺序重建。
    """
    return {
        "id": change.id,
        "sessionId": change.session_id,
        "toolName": change.tool_name,
        "path": change.path,
        "existed": bool(change.existed),
        "status": change.status,
        "reason": change.reason,
        "createdAt": change.created_at,
        "diff": change.diff,
        "addedLines": _count_lines(change.new_content),
        "removedLines": (_count_lines(change.old_content)
                         if change.existed and change.old_content is not None else 0),
    }


def _ok_body(message: str, change: Any) -> Response:
    """Java 的 `ok(message, c)`：`{"success":true,"message":…,"change":{summary}}`。"""
    return Response.json({"success": True, "message": message, "change": _summary_json(change)})


def _err_body(message: str, status: int) -> Response:
    """Java 的 `err(message)` + 状态码：`{"success":false,"error":…}`。"""
    return Response.json({"success": False, "error": message}, status)


def _message_of(exc: BaseException) -> str:
    """Java 的 `e.getMessage()`。

    【为什么不能直接用 `str(e)`】Python 的 `KeyError("没有这条改动：1")` 打印出来是
    `"'没有这条改动：1'"`（多一对引号），而 Java 抛的是 `IllegalArgumentException`
    且 `getMessage()` 没有引号 —— 前端和插件按这句话判断。
    """
    if isinstance(exc, KeyError) and exc.args:
        return str(exc.args[0])
    return str(exc)


# --------------------------------------------------------------------------
# 依赖：真实实现 + 工具接线点
# --------------------------------------------------------------------------


def _gate_module() -> Any:
    """`tools/file/_gate.py`（改文件的 5 个工具的闸门接线点）；工具层不可用时返回 None。"""
    try:
        from lionbox.tools.file import _gate
    except ImportError as e:            # 工具层还没到位（并行任务）：不接线，但不影响本模块的接口
        log__api_changes.warning("改动审核闸门接线点不可用: %s", e)
        return None
    return _gate


def _context_window_module() -> Any:
    """`tools/context/context_window.py`（上下文预算的接线点）；工具层不可用时返回 None。"""
    try:
        from lionbox.tools.context import context_window
    except ImportError as e:
        log__api_changes.warning("上下文预算接线点不可用: %s", e)
        return None
    return context_window


def _hooked_change_review() -> Any:
    """已经接在闸门上的那一份改动审核。

    【为什么要借】Java 里 `ChangeReview` 是 Spring 单例：工具登记改动、controller 读列表，
    拿的是同一个对象。Python 侧的接线点是全局的（`_gate.set_review`），装配方
    （`lionbox.wiring.wire_tool_hooks`）也会挂一次；本模块若再自己 new 一份，
    "/api/changes 永远是空的"就会变成一个静默的功能坏掉。所以谁先挂上就用谁。
    """
    gate = _gate_module()
    hook = getattr(gate, "REVIEW_HOOK", None) if gate is not None else None
    if hook is not None and callable(getattr(hook, "approve", None)) \
            and callable(getattr(hook, "list", None)):
        return hook
    return None


def _hooked_context_budget() -> Any:
    """已经接在 `context_window` 工具上的那一份上下文预算（同一个对象才能保证
    模型调窗口、界面看窗口、循环做压缩用的是同一个数字）。"""
    module = _context_window_module()
    budget = getattr(module, "BUDGET", None) if module is not None else None
    if budget is not None and callable(getattr(budget, "snapshot", None)):
        return budget
    return None


def _looks_like_history(candidate: Any) -> bool:
    return candidate is not None and callable(getattr(candidate, "add_message", None))


def _current_history(ctx: deps.ApiContext) -> Any:
    """当前的会话历史：`history` 服务优先（`api/sessions.py` 用的就是它），
    其次是挂在 `sessions` 服务上的 `history` 属性；都没有返回 None。"""
    if ctx.has("history"):
        candidate = ctx.service("history", lambda: None)
        if _looks_like_history(candidate):
            return candidate
    sessions = deps.sessions(ctx)
    for attr in ("history", "conversation_history"):
        candidate = getattr(sessions, attr, None)
        if _looks_like_history(candidate):
            return candidate
    return None


class _HistoryProxy:
    """把 `note` 转发到**当前**的 `history` 服务（每次调用现取）。

    【为什么要现取、不存一份】`api/sessions.py` 在装配期先 install 一份窄桩
    （`_HistoryStub`），装配方之后才 install 真实的 `ConversationHistory`。如果本模块在
    装配期就把"当时那一份"存进 `ChangeReview.history`，结论会写进一个没人读的桩里 ——
    表现就是"会话里看不到那条【人工审核】提示"。转发到当前服务，谁在线谁收，
    与 `/api/sessions/{id}/history` 读的永远是同一份。
    """

    __slots__ = ("_ctx",)

    def __init__(self, ctx: deps.ApiContext) -> None:
        self._ctx = ctx

    def add_message(self, message: Any) -> None:
        target = _current_history(self._ctx)
        if target is not None:
            target.add_message(message)

    def __getattr__(self, name: str) -> Any:
        target = _current_history(self._ctx)
        if target is None:
            raise AttributeError(name)
        return getattr(target, name)

    def __repr__(self) -> str:
        target = _current_history(self._ctx)
        return f"_HistoryProxy({type(target).__name__ if target is not None else '未接线'})"


def _flag_bool(ctx: deps.ApiContext, name: str, default: bool) -> bool:
    """`--lionbox.xxx=true|false`（等价 Java 的 `-D` / `@Value`）。"""
    raw = str(ctx.extra.get(name, "") or "").strip().lower()
    if not raw:
        return default
    if raw in _BOOL_TRUE:
        return True
    if raw in _BOOL_FALSE:
        return False
    log__api_changes.warning("%s=%r 不是布尔值，按默认值 %s 处理", name, raw, default)
    return default


def _flag_int(ctx: deps.ApiContext, name: str, default: int) -> int:
    raw = str(ctx.extra.get(name, "") or "").strip()
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        log__api_changes.warning("%s=%r 不是整数，按默认值 %d 处理", name, raw, default)
        return default


def _adopt_change_review(hooked: Any) -> Any:
    """借用工具已经挂上的那一份 ChangeReview，并把缺的线补上。

    【为什么补 settings】Java 的 `ChangeReview` 注入的是 `PluginSettings`
    （用户在设置里点过的开关落盘在 `plugins/settings.json`）。装配方如果传了别的对象
    （`lionbox.wiring` 现在传的是整个 `AppConfigStore`），`ChangeReview.enabled()` 会走它
    自己的兜底分支、**永远返回出厂默认值** —— 表现就是"设置里关掉改动审核，
    `GET /api/changes` 的 enabled 还是 true，文件照样被拦下来待审"。
    所以只在对方**答不了**这个开关时（没有 `is_enabled`）补上真实的插件设置，其余一律不动。
    """
    settings = getattr(hooked, "settings", None)
    if callable(getattr(settings, "is_enabled", None)):
        return hooked
    from lionbox.plugins.lifecycle import default_settings
    try:
        hooked.settings = default_settings()
    except (AttributeError, TypeError) as e:    # 对方对象不让改：如实记一条，接口照常工作
        log__api_changes.warning("借用的 ChangeReview 无法补上插件设置（插件开关会失效）: %s", e)
        return hooked
    log__api_changes.info("借用了已接线的 ChangeReview，已补上真实插件设置（settings.json 的开关）")
    return hooked


def _build_change_review(ctx: deps.ApiContext) -> Any:
    """`changes` 服务的工厂：真实的 `lionbox.agent.change.ChangeReview`（Java 同名类，不是桩）。"""
    hooked = _hooked_change_review()
    if hooked is not None:
        return _adopt_change_review(hooked)
    from lionbox.agent.change import ChangeReview
    from lionbox.plugins.lifecycle import default_settings
    return ChangeReview(
        history=_HistoryProxy(ctx),
        settings=default_settings(),
        enabled_by_default=_flag_bool(ctx, "lionbox.change-review.enabled", True))


def _build_context_budget(ctx: deps.ApiContext) -> Any:
    """`context_budget` 服务的工厂：真实的 `lionbox.agent.context.ContextBudget`。"""
    hooked = _hooked_context_budget()
    if hooked is not None:
        return hooked
    if ctx.has("agent_loop"):        # AgentLoop 自带的预算：借它，别让循环和界面各算一套
        loop = ctx.service("agent_loop", lambda: None)
        for attr in ("context_budget", "budget"):
            candidate = getattr(loop, attr, None)
            if candidate is not None and callable(getattr(candidate, "snapshot", None)):
                return candidate
    from lionbox.agent.context import ContextBudget
    return ContextBudget(_flag_int(ctx, "lionbox.agent.context-limit-tokens",
                                  DEFAULT_CONTEXT_LIMIT))


def _wire_tool_hooks(review: Any, budget: Any) -> None:
    """把本模块的闸门/预算挂到工具的显式接线点上（**只挂自己建的那一份**，别人的不覆盖）。"""
    gate = _gate_module()
    if gate is not None and gate.REVIEW_HOOK is None:
        gate.set_review(review)
    module = _context_window_module()
    if module is not None and module.BUDGET is None:
        module.set_budget(budget)


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class ChangeReviewApi:
    """`ChangeReviewController` 的 6 个接口。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 共享服务
    def review(self) -> Any:
        """改动审核闸门（`changes` 服务；首次取用时装配并缓存，等价于 `ctx.install`）。"""
        return self.ctx.service("changes", lambda: _build_change_review(self.ctx))

    def budget(self) -> Any:
        """上下文预算（`context_budget` 服务；同上）。"""
        return self.ctx.service("context_budget", lambda: _build_context_budget(self.ctx))

    # ------------------------------------------------------------ 注册
    def register__api_changes(self, router) -> None:
        api = self
        # 装配期取一次：既把服务 install 进 ctx（供别的模块取用），也把工具的接线点接上。
        # **处理函数里仍然现取**（`api.review()`）—— 装配方之后 install 的真实实现也能顶上，
        # 而 Java 那边本来就是"注入同一个单例，用时即最新"。
        _wire_tool_hooks(api.review(), api.budget())

        @router.get("/api/changes")
        def list_changes(req: Request):
            """待审改动列表。默认只给待审；`includeDecided=true` 连已通过/已打回的一起给。"""
            try:
                session_id = req.q("sessionId")
                include_decided = _spring_bool__api_changes(req, "includeDecided", False)
            except _SpringError as e:
                return deps.spring_error(e.status, req.path)
            review = api.review()
            return Response.json({
                "success": True,
                "enabled": bool(review.enabled()),
                "changes": [_summary_json(c) for c in review.list(session_id, include_decided)],
                "pendingCount": len(review.list(session_id, False)),
            })

        @router.post("/api/changes/{id}/approve")
        def approve_change(req: Request):
            """通过：真落盘，并把结论告诉会话里的模型。"""
            change_id = req.params["id"]
            try:
                done = api.review().approve(change_id)
            except KeyError as e:                       # Java: IllegalArgumentException → 404
                return _err_body(_message_of(e), 404)
            except ValueError as e:                     # 同上（Java 的 IllegalArgumentException）
                return _err_body(_message_of(e), 404)
            except Exception as e:                      # Java: catch (Exception) → 500
                log__api_changes.warning("通过改动 %s 失败", change_id, exc_info=True)
                return _err_body(_message_of(e), 500)
            return _ok_body("已通过并写入：" + str(done.path), done)

        @router.post("/api/changes/{id}/reject")
        def reject_change(req: Request):
            """打回：不落盘，把理由回给模型让它重写。"""
            change_id = req.params["id"]
            try:                                        # 体先绑（Java 也是先绑再进方法体）
                body = _spring_map_body(req)
            except _SpringError as e:
                return deps.spring_error(e.status, req.path)
            reason = None if body is None else _java_value_string(body.get("reason", ""))
            try:
                done = api.review().reject(change_id, reason)
            except KeyError as e:
                return _err_body(_message_of(e), 404)
            except ValueError as e:
                return _err_body(_message_of(e), 404)
            except Exception as e:
                log__api_changes.warning("打回改动 %s 失败", change_id, exc_info=True)
                return _err_body(_message_of(e), 500)
            return _ok_body("已打回，模型会按理由重写：" + str(done.path), done)

        @router.get("/api/changes/{id}")
        def get_change(req: Request):
            """一条改动的完整内容（界面展开看整份 diff/全文时用）。"""
            change_id = req.params["id"]
            item = api.review().get(change_id)
            if item is None:
                return _err_body("没有这条改动：" + change_id, 404)
            body = _summary_json(item)
            body["oldContent"] = item.old_content
            body["newContent"] = item.new_content
            return Response.json({"success": True, "change": body})

        @router.get("/api/context")
        def get_context(req: Request):
            """当前上下文窗口（默认值 / 会话覆盖）。"""
            session_id = req.q("sessionId")
            return Response.json({"success": True, "context": api.budget().snapshot(session_id)})

        @router.post("/api/context")
        def set_context(req: Request):
            """手动设窗口：tokens=0 表示不设限；不带 tokens 表示回到默认。"""
            try:
                body = _spring_map_body(req)
            except _SpringError as e:
                return deps.spring_error(e.status, req.path)
            # Java: body.getOrDefault("sessionId", "") 然后 String.valueOf(…)
            session_id = None if body is None else _java_value_string(body.get("sessionId", ""))
            raw = None if body is None else body.get("tokens")
            budget = api.budget()
            if raw is None:
                budget.reset(session_id)
            else:
                try:
                    tokens = _as_java_int(raw)
                except ValueError:
                    return _err_body(ERROR_TOKENS_NOT_INTEGER, 400)
                if tokens != 0 and tokens < MIN_TOKENS:
                    return _err_body(ERROR_TOKENS_TOO_SMALL, 400)
                budget.set(session_id, tokens)
            return Response.json({"success": True, "context": budget.snapshot(session_id)})


def register__api_changes(router, ctx) -> None:
    ChangeReviewApi(ctx).register__api_changes(router)


# ========================================================================
# 原模块 lionbox/agent/arg_aliases.py
# ========================================================================
"""工具**参数名**归一化 —— 逐条对照 Java `core/agent/ToolArgAliases.java`。

【为什么要有这个文件】文本通道下模型是自己手打 XML 标签的，参数名写歪是常态：
`<parameter=file_path>` 而工具声明的是 `path`、`<parameter=max_depth>` 而声明的是 `maxDepth`。
键名差一个字母，工具里 `args.get("path")` 就是 null，
用户看到的是"❌ read_file: 缺少 path 参数"——模型明明已经把值写出来了。
本机 11 token/s，重来一轮就是十几秒，这种失败纯属浪费。

做法很保守：**只改键名，不动值**；只在"唯一命中"时才改名（多个候选就放弃，
让工具照旧报缺参数），所以不会把正确的调用改坏。

【别名表逐条搬全】Java 里 37 组键、每组 4~12 个别名，全部照抄。
"""


from typing import Collection, Sequence

#: 工具声明的键名 → 模型常用的其他写法。顺序与 Java `LinkedHashMap` 一致。
ALIASES: dict[str, list[str]] = {
    "path": ["file_path", "filepath", "filename", "file_name", "file",
             "target_path", "dir", "directory", "location", "pathname", "abspath", "abs_path"],
    "source": ["src", "from", "old", "old_path", "oldpath", "source_path",
               "src_path", "from_path", "origin"],
    "target": ["dest", "destination", "to", "new", "new_path", "newpath",
               "target_path", "dest_path", "destination_path", "dst", "to_path"],
    "content": ["text", "data", "body", "value", "contents", "new_text",
                "new_content", "newText", "newContent", "payload"],
    "command": ["cmd", "command_line", "commandline", "shell_command",
                "script", "run", "cmdline"],
    "pattern": ["regex", "query", "search", "keyword", "search_pattern",
                "regexp", "expr"],
    "query": ["q", "keyword", "search", "term", "text", "search_query"],
    "input": ["text", "data", "value", "payload", "str", "string"],
    "url": ["uri", "link", "address", "href", "endpoint", "target_url"],
    "message": ["msg", "commit_message", "text", "description"],
    "lines": ["line_count", "num_lines", "n", "number_of_lines", "count"],
    "count": ["n", "num", "times", "number", "limit", "amount", "total"],
    "maxResults": ["limit", "max_results", "maxresults", "top", "max",
                   "maximum", "size", "num_results"],
    "maxDepth": ["depth", "max_depth", "maxdepth", "levels", "level", "d"],
    "name": ["key", "var", "variable", "env_name", "variable_name"],
    "text": ["value", "str", "string", "content_text"],
    "oldText": ["old_text", "oldtext", "old", "search", "from_text",
                "find", "original", "original_text"],
    "startLine": ["start_line", "startline", "from_line", "begin_line",
                  "start", "line_start"],
    "endLine": ["end_line", "endline", "to_line", "finish_line", "end",
                "line_end"],
    "operation": ["action", "op", "mode_action"],
    "format": ["fmt", "format_string", "pattern_format"],
    "domain": ["hostname", "host", "name_domain"],
    "algorithm": ["algo", "hash_type", "method"],
    "encoding": ["charset", "file_encoding", "enc"],
    "recursive": ["recurse", "recursion", "r"],
    "timeout": ["timeout_seconds", "timeoutSeconds", "seconds", "time_limit"],
    "workdir": ["cwd", "working_directory", "working_dir", "wd"],
    "savePath": ["save_path", "output", "output_path", "dest_path"],
    "filePattern": ["file_pattern", "glob", "include", "files", "filter"],
    "useRegex": ["use_regex", "regex_mode", "is_regex"],
    "action": ["op", "operation_type", "command_action"],
    "expression": ["expr", "cron", "cron_expression"],
    "branch": ["branch_name", "ref_name"],
    "value": ["val", "input_value", "number"],
    "from": ["source_lang", "from_lang", "source"],
    "to": ["target_lang", "to_lang", "target"],
}


def squash(s: str) -> str:
    """去掉大小写和分隔符差异（file_path ↔ filePath ↔ filepath）。"""
    return "".join(c for c in s.lower() if c not in "_- .")


def match_key(declared: str | None, given: Collection[str] | Sequence[str] | None) -> str | None:
    """在模型给的键里，找出对应"声明键"的那个键名。

    :param declared: 工具声明的参数名
    :param given:    模型实际给的键集合
    :return: 匹配到的键名；没把握（0 个或多个候选）时返回 None

    与 Java 版同序：① 忽略大小写完全相同 → ② 去掉分隔符后相同（要求唯一）
    → ③ 别名表（忽略大小写，要求唯一）。**别名表只按声明键的原样大小写查**
    （Java 是 `ALIASES.get(declared)`，不做 squash 兜底），保持一字不差。
    """
    if declared is None or given is None:
        return None
    keys = list(given)
    if not keys:
        return None

    # 1) 忽略大小写完全相同
    for g in keys:
        if g is not None and str(g).lower() == declared.lower():
            return g

    # 2) 去掉分隔符后相同（max_depth ↔ maxDepth）
    sq = squash(declared)
    only: str | None = None
    for g in keys:
        if g is not None and squash(str(g)) == sq:
            if only is not None:
                return None   # 多个候选 → 不猜
            only = g
    if only is not None:
        return only

    # 3) 别名表
    alts = ALIASES.get(declared)
    if alts is None:
        return None
    hit: str | None = None
    for alt in alts:
        for g in keys:
            if g is not None and str(g).lower() == alt.lower():
                if hit is not None:
                    return None   # 多个候选 → 不猜
                hit = g
    return hit


def size() -> int:
    """别名表大小（自检用）。"""
    return len(ALIASES)


# ========================================================================
# 原模块 lionbox/agent/name_aliases.py
# ========================================================================
"""工具名归一化 —— 逐条对照 Java `core/agent/ToolNameAliases.java`。

【这个文件为什么存在】本地跑的是 4bit 量化的 Qwen（IQ4_XS），它对"工具名"的回忆
明显偏向自己训练语料里的通用叫法：想列目录就写 `ls` / `list_files`，想读文件就写
`cat` / `read`，想跑命令就写 `bash`。这些名字在我们这里一个都不存在，于是用户看到的
是"未找到工具: ls"，白烧一轮推理（本机 11 token/s，一轮十几秒）。

归一化**只在精确查找失败之后**才做，所以永远不会把已经正确的调用改坏；而且只在
"有唯一把握"时才认（精确别名表 / 忽略大小写和分隔符后唯一命中 / 编辑距离 ≤1 的唯一
候选），拿不准就返回 None，让上层照旧报"未找到工具 + 建议"，不会把用户带沟里。

【别名表逐条搬全】不要只搬几个示例：Java 的注释里写得很清楚，压测里模型真的造过
`ls_directory` / `list_dir_contents` 这种"半对"的名字，表里没有就直接被判"未找到工具"。
"""


from typing import Iterable, Sequence

# --------------------------------------------------------------------------
# 别名表：模型常用的叫法 → 本项目的真实工具名。
# 只收"语义无歧义"的（head 绝不会被理解成别的），有歧义的一律不收。
#
# 【顺序有意义】Java 侧是 LinkedHashMap.put，后写的会**静默覆盖**先写的。
# dict 在 Python 3.7+ 也是插入序 + 后写覆盖，语义完全一致，所以下面的
# alias(...) 调用顺序必须与 Java 一字不差。
# --------------------------------------------------------------------------
ALIASES__agent_name_aliases: dict[str, str] = {}


def _alias(canonical: str, *names: str) -> None:
    for n in names:
        ALIASES__agent_name_aliases[n] = canonical


_alias("list_directory", "ls", "dir", "list", "listdir", "list_dir", "list_files",
       "listfiles", "list_folder", "list_directory_contents", "show_directory",
       # 压测里模型真的造过 ls_directory / list_dir_contents 这种"半对"的名字：
       # 归一化表里没有就直接被判"未找到工具"，白烧一轮（本机一轮十几秒）
       "ls_directory", "ls_dir", "lsdir", "lsdirs", "list_dir_contents", "list_dir_content",
       "ls_l", "ls_dir_list", "list_directory_content", "dir_list", "dirlist",
       "show_files", "list_all_files", "list_dir_files")
_alias("read_file", "cat", "read", "readfile", "read_text", "readtext", "view",
       "view_file", "open_file", "get_file_content", "file_read", "show_file")
_alias("head_tail_file", "head", "tail", "head_file", "tail_file", "read_head",
       "read_tail", "first_lines", "last_lines")
_alias("search_in_files", "grep", "search", "search_text", "search_content", "rg",
       "ripgrep", "find_in_files", "search_files", "grep_files", "search_in_file")
_alias("glob_files", "find", "glob", "ls_files", "glob_pattern", "match_files",
       "find_files", "list_files_by_pattern")
_alias("line_count", "wc", "wc_l", "linecount", "count_lines", "lines_count",
       "file_line_count", "count_loc", "loc")
_alias("word_count", "wc_words", "wordcount", "count_words", "file_word_count")
_alias("write_file", "write", "writefile", "save_file", "write_text", "create_or_update_file",
       "put_file", "overwrite_file")
_alias("create_file", "touch", "new_file", "create_empty_file", "make_file")
_alias("modify_file", "edit", "edit_file", "replace_in_file", "replace", "str_replace",
       "strreplace", "patch_file", "update_file", "insert_text")
_alias("append_file", "append", "append_to_file", "add_to_file", "append_text")
_alias("delete_file", "rm", "del", "remove", "delete", "delete_path", "rm_file",
       "remove_file", "unlink")
_alias("move_file", "mv", "move", "rename", "rename_file", "move_path")
_alias("copy_file", "cp", "copy", "copy_path", "duplicate_file")
_alias("create_directory", "mkdir", "create_dir", "new_directory", "make_directory")
# 【别在这里加 "ls_l"】它已经在上面 list_directory 那一组里登记过了。
# 别名表是 dict 赋值，后写的会**静默覆盖**先写的 —— Java 版这里原来也写了 "ls_l"，
# 于是模型喊 ls_l 会被解析成 file_info（看单个文件的元信息），而不是列目录，
# 和本文件开头"有歧义的一律不收"的约定正好相反。
_alias("file_info", "stat", "file_stat", "fileinfo", "get_file_info")
_alias("directory_tree", "tree", "dir_tree", "show_tree", "folder_tree")
_alias("execute_command", "bash", "sh", "shell", "run", "exec", "cmd", "command",
       "run_command", "execute", "terminal", "shell_execute", "powershell", "run_shell",
       "execute_shell", "run_terminal", "cli")
_alias("run_background", "bg", "background", "run_in_background", "start_background",
       "background_run", "spawn_process")
_alias("stop_background", "kill", "kill_process", "stop_process", "bg_stop")
_alias("fetch_url", "curl", "wget", "fetch", "http_fetch", "get_url", "fetch_page",
       "download_page")
_alias("http_get", "httpget", "get_request", "http_request")
_alias("http_post", "httppost", "post_request")
_alias("web_search", "websearch", "search_web", "browser_search", "google", "search_internet")
_alias("download_file", "wget_file", "download")
_alias("hash", "sha256", "md5", "sha1", "hash_string", "hash_file", "checksum")
_alias("base64", "b64", "base64_encode", "base64_decode", "encode_base64")
_alias("json_format", "json", "format_json", "json_parse", "json_beautify", "pretty_json")
_alias("yaml_process", "yaml", "format_yaml", "yaml_parse")
_alias("generate_uuid", "uuid", "uuid_generate", "gen_uuid", "new_uuid")
_alias("get_env", "env", "getenv", "environment", "env_var", "printenv")
_alias("dns_lookup", "dns", "nslookup", "resolve_dns", "dns_resolve")
_alias("timestamp", "time", "now", "current_time", "date", "get_time", "clock")
_alias("system_info", "sysinfo", "systeminfo", "system", "sys_info", "machine_info")
_alias("working_directory", "pwd", "cwd", "get_cwd", "get_working_directory")
_alias("translate", "translation", "translate_text")
_alias("regex_test", "regex", "regex_match", "test_regex")
_alias("string_utils", "string", "strings", "string_ops")
_alias("format_code", "format", "prettier", "formatter")
_alias("git_status", "gitstatus", "status")
_alias("git_log", "gitlog", "log")
_alias("git_diff", "gitdiff", "diff_git")
_alias("git_commit", "gitcommit", "commit")
_alias("git_branch", "gitbranch", "branch", "checkout")
_alias("git_init", "gitinit", "init_git")
_alias("git_remote", "gitremote", "remote")
_alias("git_stash", "gitstash", "stash")
_alias("git_reset", "gitreset", "reset")
_alias("diff_text", "diff", "compare_text", "text_diff")
_alias("markdown_render", "markdown", "md_render", "render_markdown")
_alias("change_permissions", "chmod", "permissions", "set_permissions")
_alias("escape_string", "escape", "unescape", "escape_text")
_alias("number_convert", "convert_number", "base_convert", "radix_convert")
_alias("ask_user", "ask", "question", "ask_question", "prompt_user")
_alias("cron_parse", "cron", "parse_cron")


def squash__agent_name_aliases(s: str) -> str:
    """去掉大小写/分隔符差异后的形态，用于"忽略大小写和 - _ 空格 ."的宽松匹配。"""
    return "".join(c for c in s.lower() if c not in "_- .")


def edit_distance_at_most_one(a: str, b: str) -> bool:
    """编辑距离是否 ≤1（只算增/删/改一个字符，不做完整 DP，够用且快）。

    与 Java 版 `editDistanceAtMostOne` 逐行等价（含"长度差 >1 直接否"这一条）。
    """
    if a == b:
        return True
    la, lb = len(a), len(b)
    if abs(la - lb) > 1:
        return False
    if la == lb:
        diff = 0
        for i in range(la):
            if a[i] != b[i]:
                diff += 1
                if diff > 1:
                    return False
        return True
    longer, shorter = (a, b) if la > lb else (b, a)
    i = j = 0
    skipped = False
    while i < len(longer) and j < len(shorter):
        if longer[i] == shorter[j]:
            i += 1
            j += 1
        else:
            if skipped:
                return False
            skipped = True
            i += 1
    return True


def resolve(raw_name: str | None, known: Sequence[str] | Iterable[str] | None) -> str | None:
    """把模型给的工具名解析成真实工具名。

    :param raw_name: 模型写的名字
    :param known:    当前真实注册且当前模式可用的工具名（大小写按原样）
    :return: 真实工具名；没把握时返回 None（上层照旧报错并给建议）

    判定顺序（**不要自己发明更宽松的规则**，Java 版就是这 5 步、每步都带"歧义就不猜"）：
      1) 忽略大小写精确命中；
      2) 精确别名表 → 别名表的 squash 形态；
      3) 去掉分隔符后唯一命中（file_path ↔ filepath、git-commit ↔ git_commit）；
      4) 名字里"包着"一个真实工具名（read_file_content / do_list_directory），要求唯一；
      5) 编辑距离 ≤1 且唯一（git_statuss → git_status）。
    """
    if not raw_name or not str(raw_name).strip():
        return None
    if known is None:
        return None
    names = list(known)
    if not names:
        return None
    name = str(raw_name).strip()

    # 1) 精确（大小写不敏感）命中：模型只是大小写写错，直接认
    for k in names:
        if k.lower() == name.lower():
            return k

    # 2) 别名表：exact → squashed
    hit = ALIASES__agent_name_aliases.get(name.lower())
    if hit is None:
        hit = ALIASES__agent_name_aliases.get(squash__agent_name_aliases(name))
    if hit is not None:
        for k in names:
            if k == hit:
                return k
        # 别名表里有、但当前模式没开放这个工具 → 不硬转，让上层正常报错
        return None

    # 3) 忽略分隔符后唯一命中（file_path ↔ filepath、git-commit ↔ git_commit）
    sq = squash__agent_name_aliases(name)
    only: str | None = None
    for k in names:
        if squash__agent_name_aliases(k) == sq:
            if only is not None:
                return None   # 不止一个 → 有歧义，不猜
            only = k
    if only is not None:
        return only

    # 4) 名字里"包着"一个真实工具名：read_file_content / do_list_directory /
    #    run_execute_command / git_status_now 这类"加料"写法。要求唯一命中，
    #    多个候选就放弃（宁可报"未找到工具"，也不要猜错工具去执行）。
    contained: str | None = None
    lower = name.lower()
    for k in names:
        if len(k) >= 5 and k.lower() in lower:
            if contained is not None:
                return None
            contained = k
    if contained is not None:
        return contained

    # 5) 编辑距离 ≤1 且唯一：处理单个字母打错（git_statuss → git_status）
    near: str | None = None
    for k in names:
        if edit_distance_at_most_one(lower, k.lower()):
            if near is not None:
                return None   # 多个候选 → 不猜，交给"你是不是想用"提示
            near = k
    return near


def size__agent_name_aliases() -> int:
    """别名表大小（自检用）。"""
    return len(ALIASES__agent_name_aliases)


# ========================================================================
# 原模块 lionbox/agent/parsing.py
# ========================================================================
"""Qwen / llama.cpp 模板原生工具调用的解析器 —— 逐条对照 Java
`core/agent/QwenToolCallParser.java`（181 行）。

【它修掉了什么】模型（我们的 GGUF 就是 Qwen 模板）最自然的输出是这个样子：

    我先了解工作区环境，然后逐个调用工具做测试。
    <tool_call>
    <function=execute_command>
    <parameter=command>
    ls -la && pwd
    </parameter>
    </function>
    </tool_call>

这**正是 llama-server 开 `--jinja` 时服务端会帮我们解析成标准 tool_calls 的格式**。
但我们没开 --jinja（本地运行时故意不下发 tools），所以这段文本原样落到 harness 手上；
而原来的解析器只认 `<name>/<arguments>` 和 JSON 两种写法，遇到 `<function=...>`
会拿去当 JSON 解析，报 "Unexpected character ('<')"，整轮工具调用作废 ——
模型白生成一轮，用户看到的就是"它说要调用工具，然后什么也没干"。

【不要自己发明更宽松的规则】Java 版的分支就下面这些，逐条搬过来：
  · `<function=名字>` … `</function>`（**必须有闭合标签**，残缺块不硬凑）；
    有没有 `<tool_call>` 外壳都认；
  · 函数体内 `<parameter=键>值</parameter>` 可以多个，值只做 `strip()`（保留内部换行）；
  · 一个 `<parameter>` 都没有时，才去尝试把函数体当 JSON 对象读（纯 JSON / ```json 围栏 /
    "我来调用一下："+JSON 三种写法）；读不出来当没参数；
  · 一次多个 `<tool_call>` 块全部解析出来（harness 自己决定一轮执行几个）。
"""


import json
import re
from typing import Any

#: `<function=工具名> … </function>`；工具名允许字母下划线开头，后面可带点、横线。
#: `(?s)` == re.DOTALL；`(.*?)` 非贪婪，与 Java `Matcher.find()` 语义一致。
FUNCTION = re.compile(r"<function\s*=\s*([A-Za-z_][\w.\-]*)\s*>(.*?)</function>", re.DOTALL)

#: `<parameter=参数名>值</parameter>`
PARAMETER = re.compile(r"<parameter\s*=\s*([A-Za-z_][\w.\-]*)\s*>(.*?)</parameter>", re.DOTALL)

#: `<tool_call>…</tool_call>` 整块（stripCalls 先删它）
_TOOL_CALL_BLOCK = re.compile(r"<tool_call>.*?</tool_call>", re.DOTALL)


class Call:
    """一次解析出来的调用：工具名 + 参数字典（对应 Java 的 `Call` record）。"""

    __slots__ = ("name", "arguments")

    def __init__(self, name: str, arguments: dict[str, Any]) -> None:
        self.name = name
        self.arguments = arguments

    def __repr__(self) -> str:
        return f"Call(name={self.name!r}, arguments={self.arguments!r})"


def _blank(s: str | None) -> bool:
    """Java `String.isBlank()`：null 或全部是空白字符。"""
    return s is None or str(s).strip() == ""


def parse(text: str | None) -> list[Call]:
    """解析文本里所有的模板原生工具调用（有没有 `<tool_call>` 外壳都认）。

    :param text: 模型输出
    :return: 解析结果；没有就返回空列表
    """
    calls: list[Call] = []
    if _blank(text):
        return calls
    for fn in FUNCTION.finditer(text):          # type: ignore[arg-type]
        name = fn.group(1).strip()
        if not name:
            continue
        args: dict[str, Any] = {}
        for pm in PARAMETER.finditer(fn.group(2)):
            args[pm.group(1).strip()] = _unescape(pm.group(2))
        if not args:
            # 【兜底】模型也常把参数写成 JSON 对象塞在 function 里（我们自己的用例、
            # 以及部分模板都这么发）。只认 <parameter=…> 的话这种调用会被当成
            # "没有参数"，工具回一句"缺少必需参数"，整轮就废了 —— 实测踩过。
            args.update(_parse_json_arguments(fn.group(2)))
        calls.append(Call(name, args))
    return calls


def strip_calls(text: str | None) -> str:
    """把模板原生的工具调用块从正文里删掉，剩下的才是给用户看的文字。

    先删 `<tool_call>…</tool_call>` 整块（含里面的 function），
    再兜底删掉没被包裹的 `<function=…>…</function>`。
    """
    if _blank(text):
        return text            # type: ignore[return-value]
    out = _TOOL_CALL_BLOCK.sub(" ", text)
    out = FUNCTION.sub(" ", out)
    return out.strip()


def _parse_json_arguments(body: str | None) -> dict[str, Any]:
    """把 `<function=…>` 里那块内容当 JSON 对象读出来（读不出来就返回空 dict）。

    兼容三种常见写法：纯 JSON、```json 围栏、以及前面带一句解释的文字 + JSON。
    """
    if _blank(body):
        return {}
    t = body.strip()                                    # type: ignore[union-attr]
    # 去掉 ```json … ``` 围栏
    if t.startswith("```"):
        nl = t.find("\n")
        if nl > 0:
            t = t[nl + 1:]
        if t.endswith("```"):
            t = t[:-3]
        t = t.strip()
    # 只取第一个 { 到最后一个 }（前面可能有一句"我来调用一下："）
    b = t.find("{")
    e = t.rfind("}")
    if b < 0 or e <= b:
        return {}
    raw = t[b:e + 1]
    try:
        parsed = json.loads(raw)
    except ValueError:
        return {}          # 不是 JSON 就当没参数，跟以前一样
    if not isinstance(parsed, dict):
        return {}          # Java 侧读成 Map 才有值；数组/标量一律当没参数
    return parsed


def _unescape(raw: str | None) -> str:
    """值就是原样的文本；只去掉首尾空白（多行命令要保留内部换行）。"""
    if raw is None:
        return ""
    return raw.strip()


# ========================================================================
# 原模块 lionbox/agent/context.py
# ========================================================================
"""上下文预算与压缩 —— 逐条对照 Java `core/agent/ContextBudget.java`（109 行）
与 `core/agent/ContextCompressor.java`（301 行）。

【ContextBudget 为什么要存在】本机模型是 256K 上下文，可**每一条消息都要把整个前缀
重新预填充一遍**（prefill），窗口开多大，每一轮就要多算多少 —— 这是这台机器上最贵的
一项开销。所以默认窗口收到 16K：够干绝大多数活，预填充也只有 256K 的十六分之一。
真遇到大项目 16K 不够时，由 Agent 自己用 `context_window` 工具把窗口调大，干完再调回来。

两层：全局默认（`lionbox.agent.context-limit-tokens`，默认 16384）+ 每会话覆盖
（Agent 用工具改的是这一层）。覆盖只在内存里，进程重启就回到默认 —— 这是有意的：
"临时为大项目开大窗口"本身就不该变成永久设置。

【ContextCompressor 为什么要存在】在这之前项目里**没有任何上下文管理**：每轮都把整个
会话历史原样发给模型，历史涨到超过 n_ctx 时 llama-server 直接回 400（"exceeds the
available context size"），用户看到的就是"模型调用失败"，而且这个会话**永久坏掉**。

做法（**抽取式**摘要，不额外调模型）：保留开头所有 system 消息 + 最后 keepRecent 条，
中间那段换成一条"【早前对话摘要】"的 user 消息。为什么用抽取式而不是让模型总结：
本地 11 token/s，让模型总结一次要十几秒到几十秒，而压缩是**在用户等待的链路上**发生的；
抽取式是纯字符串操作，微秒级，而且不会像小模型总结那样丢关键事实。

注意一个坑：**不能把 assistant(tool_calls) 和它后面的 tool 结果切散**，
否则请求直接 400（tool 消息必须紧跟对应的 tool_calls）。所以切点会往前对齐到安全边界。
"""


import math
import threading
from typing import Any, Sequence


# ==========================================================================
# 预算
# ==========================================================================


class ContextBudget:
    """会话的上下文窗口预算：全局默认 + 每会话覆盖。"""

    def __init__(self, default_limit: int = 16384) -> None:
        self._lock = threading.RLock()
        #: 全局默认窗口（token）。0 = 不限，交给"模型窗口 × 75%"那条老路。
        self._default_limit = max(0, int(default_limit))
        #: 每会话覆盖：sessionId -> token 数（0 表示这个会话不限）
        self._per_session: dict[str, int] = {}

    # ---- 查询 ----
    def default_limit(self) -> int:
        """全局默认（REST/界面显示用）。"""
        return self._default_limit

    def limit_for(self, session_id: str | None) -> int:
        """这个会话当前该用多大窗口。

        :return: token 数；0 表示"不设限，用模型窗口 × 75%"
        """
        if session_id is None:
            return self._default_limit
        with self._lock:
            v = self._per_session.get(session_id)
            return self._default_limit if v is None else v

    def is_overridden(self, session_id: str | None) -> bool:
        """这个会话有没有被 Agent 手动调过。"""
        if session_id is None:
            return False
        with self._lock:
            return session_id in self._per_session

    # ---- 修改 ----
    def set(self, session_id: str | None, tokens: int) -> int:
        """Agent 调窗口。

        :param tokens: 新的窗口大小；0 = 不设限（用模型窗口的 75%）
        :return: 生效后的值
        """
        v = max(0, int(tokens))
        if session_id is None:
            return v
        with self._lock:
            if v == self._default_limit:
                # 调回默认值就等于"没调过"，不留下覆盖记录
                self._per_session.pop(session_id, None)
            else:
                self._per_session[session_id] = v
        return v

    def reset(self, session_id: str | None) -> int:
        """回到全局默认。"""
        if session_id is not None:
            with self._lock:
                self._per_session.pop(session_id, None)
        return self._default_limit

    def forget(self, session_id: str | None) -> None:
        """会话结束/清空时把覆盖扔掉（sessionId 单调，不清也不会串，但清了更干净）。"""
        if session_id is not None:
            with self._lock:
                self._per_session.pop(session_id, None)

    def snapshot(self, session_id: str | None) -> dict[str, Any]:
        """快照（REST 返回给界面），键名与 Java 版一致。"""
        return {
            "defaultLimit": self._default_limit,
            "sessionLimit": self.limit_for(session_id),
            "overridden": self.is_overridden(session_id),
        }


# ==========================================================================
# 压缩
# ==========================================================================


class _Msg:
    """内部最小消息载体（提供 context.py 需要的 role/content/tool_calls 读口）。

    循环层的真实消息类在 `loop.py`，两者鸭子类型兼容：压缩只读这几个属性。
    """

    __slots__ = ("role", "content", "tool_calls", "tool_call_id", "name")

    def __init__(self, role: str, content: str = "", tool_calls: list[Any] | None = None,
                 tool_call_id: str | None = None, name: str | None = None) -> None:
        self.role = role
        self.content = content
        self.tool_calls = tool_calls
        self.tool_call_id = tool_call_id
        self.name = name


def user_message(content: str) -> _Msg:
    return _Msg("user", content)


def tool_result_message(tool_call_id: str | None, content: str) -> _Msg:
    return _Msg("tool", content, tool_call_id=tool_call_id)


class CompressResult:
    """压缩结果（对应 Java 的 `Result` record）。"""

    __slots__ = ("messages", "compressed", "tokens_before", "tokens_after", "dropped_messages")

    def __init__(self, messages: list[Any], compressed: bool, tokens_before: int,
                 tokens_after: int, dropped_messages: int) -> None:
        self.messages = messages
        self.compressed = compressed
        self.tokens_before = tokens_before
        self.tokens_after = tokens_after
        self.dropped_messages = dropped_messages

    def __repr__(self) -> str:
        return (f"CompressResult(compressed={self.compressed}, "
                f"{self.tokens_before}->{self.tokens_after}, dropped={self.dropped_messages})")


#: 单条消息在摘要里最多留多少字符（用户/助手的原话，留多了摘要本身就爆了）
DIGEST_USER_CHARS = 240
DIGEST_ASSISTANT_CHARS = 200
DIGEST_TOOL_CHARS = 140
#: 摘要整体上限（字符）。摘要本身也要花 token，不能无限长。
DIGEST_MAX_CHARS = 4000
#: 保留尾部里，单条工具结果最多留多少字符（防止一条超大输出把预算吃光）
TAIL_TOOL_MAX_CHARS = 8000


class ContextCompressor:
    """把中间那段历史折叠成摘要（纯函数，不调模型）。"""

    DIGEST_USER_CHARS = DIGEST_USER_CHARS
    DIGEST_ASSISTANT_CHARS = DIGEST_ASSISTANT_CHARS
    DIGEST_TOOL_CHARS = DIGEST_TOOL_CHARS
    DIGEST_MAX_CHARS = DIGEST_MAX_CHARS
    TAIL_TOOL_MAX_CHARS = TAIL_TOOL_MAX_CHARS

    # ---------------------------------------------------------------- token
    @staticmethod
    def estimate_text_tokens(text: str | None) -> int:
        """估算一段文本的 token 数。

        不引 tokenizer（本地模型的分词器在 llama-server 里，拿不到）；
        用经验公式：中日韩字符 ≈ 1 token/字，其余 ≈ 1 token/3.5 字符。
        Qwen 对中文差不多就是这个量级，估算只用来决定"要不要压缩"，留了 20% 余量。
        """
        if not text:
            return 0
        cjk = 0
        other = 0
        for ch in text:
            o = ord(ch)
            if 0x2E80 <= o <= 0x9FFF or 0xF900 <= o <= 0xFAFF or 0xFF00 <= o <= 0xFFEF:
                cjk += 1
            else:
                other += 1
        return cjk + int(math.ceil(other / 3.5))

    @staticmethod
    def estimate_tokens(messages: Sequence[Any]) -> int:
        """整份消息列表的 token 估算（含每条消息的固定开销）。"""
        total = 0
        for m in messages:
            total += 8            # role/分隔符等固定开销
            total += ContextCompressor.estimate_text_tokens(getattr(m, "content", "") or "")
            calls = getattr(m, "tool_calls", None)
            if calls:
                for tc in calls:
                    total += 16
                    total += ContextCompressor.estimate_text_tokens(getattr(tc, "name", "") or "")
                    total += ContextCompressor.estimate_text_tokens(
                        _stringify(getattr(tc, "arguments", None)))
        return total

    # ----------------------------------------------------------------- fit
    @staticmethod
    def fit(messages: list[Any], limit_tokens: int, keep_recent: int) -> CompressResult:
        """按预算裁剪消息。

        :param messages:     当前要发出去的消息（第一条通常是 system）
        :param limit_tokens: 预算上限；≤0 表示不压缩
        :param keep_recent:  尾部保留多少条（压不动时会自动往下调）
        """
        before = ContextCompressor.estimate_tokens(messages)
        if limit_tokens <= 0 or before <= limit_tokens or len(messages) <= 2:
            # 【不超预算时绝不能动消息】返回同一个列表对象，压缩本身不能有副作用
            return CompressResult(messages, False, before, before, 0)

        # 1) 头部：连续的 system 消息全部保留（Qwen 模板要求 system 必须在最前）
        head = 0
        while head < len(messages) and getattr(messages[head], "role", None) == "system":
            head += 1

        # 2) 尾部越压越少，直到进预算或者只剩最后两条
        best: CompressResult | None = None
        for keep in (keep_recent, max(4, keep_recent // 2), 4, 2):
            tail_start = max(head, len(messages) - keep)
            # 对齐到安全边界：第一条不能是 tool（否则是"孤儿"工具结果，服务端会 400）
            while tail_start > head and getattr(messages[tail_start], "role", None) == "tool":
                tail_start -= 1
            digest_source = messages[head:tail_start]
            out: list[Any] = list(messages[:head])
            # 摘要本身也要占预算：预算越小，摘要必须越短，否则"压完还是超"。
            # 中文大约 1 字 1 token，所以按 1/4 预算给字符数，最少 200 字。
            digest = ContextCompressor.digest(
                digest_source, min(DIGEST_MAX_CHARS, max(200, limit_tokens // 4)))
            if digest.strip():
                # 用 user 消息而不是 system：Qwen 模板对"夹在中间的 system"直接抛异常
                out.append(user_message(
                    "【早前对话摘要（系统自动压缩，" + str(len(digest_source))
                    + " 条历史消息已经折叠，原文不再发送。需要细节就用工具重新读一次文件/重新跑命令）】\n"
                    + digest))
            for m in messages[tail_start:]:
                out.append(ContextCompressor.trim_tool_result(m))
            after = ContextCompressor.estimate_tokens(out)
            candidate = CompressResult(out, True, before, after, len(digest_source))
            if best is None or candidate.tokens_after < best.tokens_after:
                best = candidate
            if after <= limit_tokens:
                return candidate

        # 3) 实在压不到预算以内（预算小到连摘要都放不下）：**也返回压过的版本**。
        #    返回原文等于保证服务端 400（整个会话直接废掉），返回压缩版至少还能继续对话 ——
        #    这是"两害相权取其轻"，不是理想状态，所以日志里会记真实 token 数。
        if best is not None and best.tokens_after < before:
            return best
        # 压不动（比如系统提示词本身就超预算、或者消息太少没有可折叠的中间段）：
        # 老老实实按原样返回，**不要**报一个"压缩了但一个 token 都没省"的假事件 ——
        # 压测里就是这么看到"3 次压缩、before==after"，日志和事件流全被噪音污染。
        return CompressResult(messages, False, before, before, 0)

    # -------------------------------------------------------------- helpers
    @staticmethod
    def trim_tool_result(m: Any) -> Any:
        """超大的工具结果就地截断（保留头部，尾部给一句说明）。"""
        content = getattr(m, "content", None)
        if getattr(m, "role", None) != "tool" or content is None or len(content) <= TAIL_TOOL_MAX_CHARS:
            return m
        cut = content[:TAIL_TOOL_MAX_CHARS] + "\n…（结果过长已截断，原始长度 " + str(len(content)) + " 字符）"
        return tool_result_message(getattr(m, "tool_call_id", None), cut)

    @staticmethod
    def digest(source: Sequence[Any], max_chars: int) -> str:
        """把一批消息压成一段人话摘要（抽取式，不调模型）。"""
        sb = ""      # 等价于 Java 的 StringBuilder：可变字符串，容量有限

        for m in source:
            role = getattr(m, "role", None)
            content = _squash_ws(getattr(m, "content", "") or "")
            if role == "user":
                if not content:
                    continue
                piece = "· 用户说：" + _cut(content, DIGEST_USER_CHARS) + "\n"
            elif role == "assistant":
                piece = ""
                calls = getattr(m, "tool_calls", None)
                if calls:
                    for tc in calls:
                        piece += ("· 调用工具：" + str(getattr(tc, "name", ""))
                                  + "(" + _cut(_stringify(getattr(tc, "arguments", None)), 120) + ")\n")
                if content:
                    piece += "· 助手结论：" + _cut(content, DIGEST_ASSISTANT_CHARS) + "\n"
                if not piece:
                    continue
            elif role == "tool":
                if not content:
                    continue
                piece = "· 工具结果：" + _cut(content, DIGEST_TOOL_CHARS) + "\n"
            else:
                continue

            sb += piece
            if len(sb) > max_chars:
                # 超了就**保留最近的**（前面的丢），因为越靠近现在越有用。
                # 与 Java 等价：从 s.length()-maxChars 处往后找第一个 '\n'，取它之后的内容。
                cut_at = sb.find("\n", len(sb) - max_chars)
                sb = "…（更早的摘要已省略）\n" + (sb[cut_at + 1:] if cut_at > 0 else sb)
                break
        return sb


# ------------------------------------------------------------------ 内部工具


def _cut(s: str, max_len: int) -> str:
    return s if len(s) <= max_len else s[:max_len] + "…"


_WS__agent_context = (" ", "\t", "\n", "\r", "\f", "\v")


def _squash_ws(s: str) -> str:
    """Java `s.replaceAll("\\\\s+", " ").trim()` 的等价实现（不引 re，快）。"""
    out: list[str] = []
    prev_ws = False
    for ch in s:
        if ch in _WS__agent_context or ch.isspace():
            if not prev_ws:
                out.append(" ")
            prev_ws = True
        else:
            out.append(ch)
            prev_ws = False
    return "".join(out).strip()


def _stringify(value: Any) -> str:
    """对应 Java `String.valueOf(arguments)`（Map.to-string 形状）。"""
    if value is None:
        return "null"
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        return "{" + ", ".join(f"{k}={_stringify(v)}" for k, v in value.items()) + "}"
    if isinstance(value, (list, tuple)):
        return "[" + ", ".join(_stringify(v) for v in value) + "]"
    return str(value)


# ========================================================================
# 原模块 lionbox/agent/control.py
# ========================================================================
"""Agent 运行控制 + 工作模式 + 思考等级 —— 对照 Java
`core/agent/AgentControlManager.java`、`core/agent/AgentMode.java`、
`core/agent/ThinkingLevel.java`。

【AgentControlManager 的作用】提供每个会话的暂停/继续/停止控制：
  · AgentLoop 每轮工具调用循环前调用 `check_control` 检查状态；
  · 暂停：循环阻塞等待，直到前端调用继续；
  · 停止：抛 `AgentStoppedException`，AgentLoop 捕获后中止任务。
状态是易失的：每次新任务开始（processMessage 开头）自动 reset。

【AgentMode 已就绪】枚举本身住在 `lionbox.plugins.base`（工具注册表要用它按模式过滤），
这里**重新导出**，这样 `from ..agent.control import AgentMode` 与 Java 的包结构对得上，
不会出现两份 AgentMode 常量互相比较不相等。
"""


import threading
import time
from typing import Any

from lionbox.plugins.base import AgentMode

__all__ = ["AgentMode", "ThinkingLevel", "AgentControlManager", "AgentStoppedException"]


class ThinkingLevel__agent_control:
    """模型思考等级。

    云端 API 后端可用，可下发思考等级参数；本地 GGUF 服务（OpenAI 兼容协议接入）
    不传思考等级参数。值与 Java enum 一一对应（code / 显示名 / token 预算）。
    """

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    MAX = "max"

    ALL = (LOW, MEDIUM, HIGH, MAX)

    DISPLAY = {
        LOW: ("低", 1024),
        MEDIUM: ("中", 4096),
        HIGH: ("高", 16384),
        MAX: ("最高", 32768),
    }

    @staticmethod
    def display_name(level: Any) -> str:
        return ThinkingLevel__agent_control.DISPLAY.get(ThinkingLevel__agent_control.from_name(level), ("低", 1024))[0]

    @staticmethod
    def token_budget(level: Any) -> int:
        return ThinkingLevel__agent_control.DISPLAY.get(ThinkingLevel__agent_control.from_name(level), ("低", 1024))[1]

    @staticmethod
    def from_name(name: Any) -> str:
        """按 code 解析（大小写不敏感）；空/不认识一律回落 LOW（与 Java 默认档一致）。"""
        v = str(name or "").strip().lower()
        return v if v in ThinkingLevel__agent_control.ALL else ThinkingLevel__agent_control.LOW

    @staticmethod
    def normalize(level: Any) -> str:
        return ThinkingLevel__agent_control.from_name(level)


class AgentStoppedException(RuntimeError):
    """停止信号异常（对应 Java 的 `AgentControlManager.AgentStoppedException`）。"""


class AgentControlManager:
    """会话 → 运行状态（RUNNING / PAUSED / STOPPED）。"""

    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"

    #: 暂停轮询间隔（毫秒）。Java 是 `Thread.sleep(300)`。
    POLL_SECONDS = 0.3

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._states: dict[str, str] = {}

    # ---- 控制 ----
    def reset(self, session_id: str) -> None:
        """新任务开始：清除该会话之前的暂停/停止状态。"""
        with self._lock:
            self._states.pop(session_id, None)

    def pause(self, session_id: str) -> None:
        with self._lock:
            self._states[session_id] = self.PAUSED

    def resume(self, session_id: str) -> None:
        with self._lock:
            self._states[session_id] = self.RUNNING

    def stop(self, session_id: str) -> None:
        """停止（暂停中也可以直接停止）。"""
        with self._lock:
            self._states[session_id] = self.STOPPED

    def get_state(self, session_id: str | None) -> str:
        with self._lock:
            return self._states.get(session_id, self.RUNNING)   # type: ignore[arg-type]

    # ---- 检查 ----
    def check_control(self, session_id: str) -> None:
        """AgentLoop 每轮循环前调用。

        · PAUSED：阻塞等待直到继续（轮询间隔 300ms，与 Java 一致）；
        · STOPPED：抛 `AgentStoppedException`；
        · RUNNING：直接返回。
        """
        while self.get_state(session_id) == self.PAUSED:
            time.sleep(self.POLL_SECONDS)
        if self.get_state(session_id) == self.STOPPED:
            raise AgentStoppedException("任务已被手动停止")

    def snapshot(self) -> dict[str, str]:
        """状态快照（排查/测试用）。"""
        with self._lock:
            return dict(self._states)


# ========================================================================
# 原模块 lionbox/agent/guard.py
# ========================================================================
"""工具调用的「重复/连续失败」统计器 —— 逐条对照 Java `core/agent/ToolCallGuard.java`。

**2026-09-30 起它不再拦任何调用**：用户明确要求"能把任务中断的东西都删掉"，
于是"同样参数 5 次就终止任务""重复 3 次/连续失败 6 次就跳过不执行"这些行为全部删除，
**只保留计数**（排查用）。要不要继续尝试由模型判断，停不停由用户按界面上的 ⏹ 决定。

下面这段是它当初为什么存在（留着当背景，**别再照着它把拦人逻辑加回来**）：

  一次真实跑测试（用户要求"把所有工具都调用一遍"）暴露了两个坑，两个都不是模型"笨"，
  而是 harness 没兜住：
    1. 同样的调用重复做：`create_directory` 连着成功 7 次，参数一模一样 ——
       第二次开始就不可能拿到新信息，纯烧时间（本地模型一轮 10~40 秒）。
    2. 失败后硬试：`fetch_url` 连续失败 40 多次；那时每个网络工具 connect 15s + read 30s，
       一条消息的 10 分钟上限就被这么耗光了，用户看到的是"❌ 处理超时"。

所以 `before_call` 永远返回 `Decision.ok()`；保留下来的常量是为了"以后真要恢复拦截时
有据可查"，当前代码路径**不会**用它们做判断。
"""


import threading
from typing import Any

#: 第几次同样的调用开始"只提示不执行"（历史常量，当前不生效）
REPEAT_SKIP_AT = 3
#: 第几次同样的调用直接终止任务（历史常量，当前不生效）
REPEAT_ABORT_AT = 5
#: 同一工具连续失败几次后"只提示不执行"（历史常量，当前不生效）
FAIL_SKIP_AT = 6
#: 同一工具连续失败几次时先提醒一次（历史常量，当前不生效）
FAIL_WARN_AT = 3


class Verdict:
    """判定结果（与 Java enum 同名同值）。"""

    OK = "OK"          # 正常执行
    SKIP = "SKIP"      # 别执行了，给模型一句纠正提示
    ABORT = "ABORT"    # 重复得太离谱，直接结束任务


class Decision:
    """判定结果：verdict + 给模型/用户看的说明 + 计数。"""

    __slots__ = ("verdict", "hint", "count")

    def __init__(self, verdict: str, hint: str | None = None, count: int = 0) -> None:
        self.verdict = verdict
        self.hint = hint
        self.count = count

    @staticmethod
    def ok() -> "Decision":
        return Decision(Verdict.OK, None, 0)

    def __repr__(self) -> str:
        return f"Decision({self.verdict}, hint={self.hint!r}, count={self.count})"


class ToolCallGuard:
    """按会话统计"同一调用做了几次""某工具连续失败几次"。

    与 Java 版一样分两张表：repeats（工具名+参数指纹 → 次数）、
    failures（工具名 → 连续失败次数）。Java 用 ConcurrentHashMap，这里用一把锁 +
    普通 dict —— 主循环是单线程的，但工具执行可能在别的线程回调，加锁更稳。
    """

    REPEAT_SKIP_AT = REPEAT_SKIP_AT
    REPEAT_ABORT_AT = REPEAT_ABORT_AT
    FAIL_SKIP_AT = FAIL_SKIP_AT
    FAIL_WARN_AT = FAIL_WARN_AT

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._repeats: dict[str, dict[str, int]] = {}
        self._failures: dict[str, dict[str, int]] = {}

    # ---- 生命周期 ----
    def reset(self, session_id: str | None) -> None:
        """每条用户消息开始时调用，跨消息不累计（上一条消息里调用过，这一条当然可以再调用）。"""
        with self._lock:
            self._repeats.pop(session_id, None)
            self._failures.pop(session_id, None)

    # ---- 调用前 ----
    def before_call(self, session_id: str | None, tool_name: str | None,
                    args_json: str | None) -> Decision:
        """执行前问一句：这次调用还要不要真的跑？

        **永远返回 Decision.ok()**：这里只统计（日志/排查用），不做任何拦截，
        也不往对话里塞【系统提示】。
        """
        if session_id is not None and tool_name is not None:
            key = tool_name + "|" + (args_json.strip() if args_json is not None else "")
            with self._lock:
                table = self._repeats.setdefault(session_id, {})
                table[key] = table.get(key, 0) + 1
        return Decision.ok()

    # ---- 调用后 ----
    def after_call(self, session_id: str | None, tool_name: str | None, success: bool) -> None:
        """执行结果回报（成功清零连续失败计数）。"""
        if session_id is None or tool_name is None:
            return
        with self._lock:
            table = self._failures.setdefault(session_id, {})
            if success:
                table.pop(tool_name, None)
            else:
                table[tool_name] = table.get(tool_name, 0) + 1

    def failure_count(self, session_id: str | None, tool_name: str | None) -> int:
        """连续失败次数（测试/日志用）。"""
        with self._lock:
            table: dict[str, int] | None = self._failures.get(session_id)  # type: ignore[arg-type]
            if not table:
                return 0
            return int(table.get(tool_name, 0))                          # type: ignore[arg-type]

    def repeat_count(self, session_id: str | None, tool_name: str | None,
                     args_json: str | None) -> int:
        """同一调用被请求过几次（Java 版没暴露这个读口，但计数本来就存着，便于排查）。"""
        key = (tool_name or "") + "|" + (args_json.strip() if args_json is not None else "")
        with self._lock:
            return int(self._repeats.get(session_id, {}).get(key, 0))    # type: ignore[arg-type]

    def snapshot(self) -> dict[str, Any]:
        """两张表的快照（排查用）。"""
        with self._lock:
            return {"repeats": {k: dict(v) for k, v in self._repeats.items()},
                    "failures": {k: dict(v) for k, v in self._failures.items()}}


# ========================================================================
# 原模块 lionbox/agent/loop.py
# ========================================================================
"""Agent 主循环 —— 逐条对照 Java `core/agent/AgentLoop.java`（2133 行）。

核心运行时：负责接收用户消息、调用模型、解析工具调用、执行工具、汇总结果。
与业务插件完全解耦。

核心特性：
  · 流式工具执行：识别到工具调用块就调度执行，不需要等待模型完整输出
  · 事件溯源：完整记录每一轮思考、工具调用、返回结果
  · 工具调用循环：自动处理多轮工具调用直到模型给出最终答案
  · 异常隔离：工具执行异常不会导致整个 Agent 循环崩溃
  · 多格式支持：同时支持 XML 和 JSON 格式的工具调用解析


模型调用层（`lionbox/llm/`，由另一位同事负责）通过下面这个**窄接口**接进来
---------------------------------------------------------------------------

**推荐直接把 `lionbox.llm.ModelAdapter` 传进来**（`AgentLoop(client=adapter)`）：
那种情况下走的就是 Java 的同一条路 —— `chat_with_options(messages, model,
thinking_level, tools, extra_body, max_tokens)` 与 `chat_stream_limited(...)` 生成器，
返回的 `llm.ModelResponse` / `llm.ModelChunk` 原样认得（dataclass，字段名与 Java 一致）。

另外也支持一个更窄的自定义客户端（便于测试与第三方接入）：

    class ChatClient(Protocol):
        def chat(self, messages, tools=None, model=None, thinking_level=None,
                 max_tokens=None, **opts) -> dict | object: ...
        def chat_stream(self, messages, tools=None, model=None, thinking_level=None,
                        max_tokens=None, **opts) -> Iterator[dict | object]: ...

`chat()` 的返回结构与 Java 适配器 `ModelResponse` 一致，下面三种形状都认
（不要求 llm 层改代码，也不要求 loop 层猜）：

  ① Java 适配器 / `lionbox.llm.ModelResponse` 形状（**首选**）::

        ModelResponse(content="...", tool_calls=[ToolCall(id=..., name=..., arguments={...})],
                      finish_reason="stop", reasoning_content=None, malformed_tool_call=False)
        # dict 写法等价：{"content": ..., "tool_calls": [...], "finish_reason": "stop",
        #                 "reasoning_content": None, "malformed_tool_call": False}
        # 也认 camelCase：finishReason / reasoningContent / malformedToolCall

  ② OpenAI 兼容形状（`choices[0].message`）::

        {"choices": [{"message": {"role": "assistant", "content": "...",
                                  "tool_calls": [{"id": "call_1", "type": "function",
                                                  "function": {"name": "read_file",
                                                               "arguments": "{\\"path\\":\\"a\\"}"}}]},
                      "finish_reason": "tool_calls"}],
         "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3}}

  ③ 带属性的对象（dataclass / SimpleNamespace）：读 `.content` / `.tool_calls` /
     `.finish_reason` / `.reasoning_content` / `.malformed_tool_call`。

`tool_calls[i].arguments` 允许是 dict，也允许是 JSON 字符串（OpenAI 就是这么给的）。

流式分片同样三种形状都认：`llm.ModelChunk(delta_content=..., tool_call_deltas=[
ToolCallDelta(index=0, id=..., name_delta=..., arguments_delta=...)], finish_reason=...)`、
自定义 dict `{"delta": {"content": ...}, "tool_call_deltas": [...]}`、
OpenAI 的 `{"choices":[{"delta":{...},"finish_reason":...}]}`。
**`tool_call_deltas` 里既可以是 dataclass 也可以是 dict**（按属性取，两种都行）。

两个方法都**可选**：只有 `chat()` 也能跑（流式接口会退化成"一次拿到整段再切片发出"）。


外部依赖（都由别人负责，这里只按下面的窄形状调用，缺了就退回内存桩）
--------------------------------------------------------------------

  · 事件存储：`event_store.record_event(session_id, event_type, data, summary)`，
    事件类型字符串与 Java `LionEvent.EventType` 同名。默认用真实的
    `lionbox.events.EventStore` 需要自己传进来；不传就用本模块的 `LocalEventStore` 内存桩。
  · 会话历史：`history.add_message(一条消息)` / `history.get_history(session_id)`。
    **`lionbox/sessions/ConversationHistory.add_message()` 收的是 ConversationMessage 对象**
    （与 Java 的 `addMessage(ConversationMessage)` 一致），所以本模块优先用
    `sessions.message.ConversationMessage` 造消息；导入不到才退回内存桩的散开签名。
  · 工作区：构造时传 `workspace=Path(...)`，或传 `workspace_resolver(session_id)`。
"""


import json
import os
import random
import re
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout
from typing import Any, Callable, Iterator, Protocol, Sequence, runtime_checkable

from lionbox.plugins.base import REGISTRY, AgentMode, PermissionLevel, ToolPlugin, ToolResult
from lionbox.agent import arg_aliases, name_aliases, parsing
from lionbox.agent.approval import ApprovalAction, ApprovalPolicy

# 会话历史（`lionbox/sessions/`，由另一位同事负责）：
#   · 在 → 用它真正的 ConversationMessage / ToolCallRecord，这样写进磁盘的 JSON
#     与 Java 版、与 /api/sessions 读出来的结构完全一致；
#   · 不在 → 用本模块的 `LocalConversationHistory`（内存桩），接口形状一致。
try:  # pragma: no cover - 取决于并行施工进度
    from lionbox.sessions.message import ConversationMessage as _SessionsMessage, ToolCallRecord__agent_loop as _SessionsToolCallRecord
except Exception:  # noqa: BLE001 - 任何导入问题都退回内存桩，不让主循环起不来
    _SessionsMessage = None
    _SessionsToolCallRecord = None

__all__ = [
    "ChatClient", "ChatMessage", "ToolCall", "ToolCallRecord", "ModelResponse",
    "AgentChunk", "AgentLoop", "MemoryEventStore", "InMemoryHistory",
    "LocalEventStore", "LocalConversationHistory", "SessionContext", "WorkspaceContext",
]


# ==========================================================================
# 模型调用层的窄接口
# ==========================================================================


@runtime_checkable
class ChatClient(Protocol):
    """loop 只依赖这两个方法（见模块 docstring 里的返回结构）。"""

    def chat(self, messages: list[Any], tools: list[dict[str, Any]] | None = None,
             model: str | None = None, thinking_level: str | None = None,
             max_tokens: int | None = None, **opts: Any) -> Any: ...

    def chat_stream(self, messages: list[Any], tools: list[dict[str, Any]] | None = None,
                    model: str | None = None, thinking_level: str | None = None,
                    max_tokens: int | None = None, **opts: Any) -> Iterator[Any]: ...


# ==========================================================================
# 消息模型（对应 model/adapter/ChatMessage.java）
# ==========================================================================


class ToolCall__agent_loop:
    """模型给的一次工具调用：id + 名字 + 参数字典。"""

    __slots__ = ("id", "name", "arguments")

    def __init__(self, call_id: str, name: str, arguments: dict[str, Any] | None = None) -> None:
        self.id = call_id
        self.name = name
        self.arguments = arguments if arguments is not None else {}

    def __repr__(self) -> str:
        return f"ToolCall({self.id!r}, {self.name!r}, {self.arguments!r})"


class ToolCallRecord__agent_loop:
    """会话历史里的工具调用记录（对应 ConversationMessage.ToolCallRecord）。"""

    __slots__ = ("id", "name", "arguments")

    def __init__(self, call_id: str, name: str, arguments: dict[str, Any] | None = None) -> None:
        self.id = call_id
        self.name = name
        self.arguments = arguments if arguments is not None else {}

    def to_dict(self) -> dict[str, Any]:
        return {"id": self.id, "name": self.name, "arguments": self.arguments}

    def __repr__(self) -> str:
        return f"ToolCallRecord({self.id!r}, {self.name!r})"


class ChatMessage__agent_loop:
    """发给模型的一条消息（role/content/tool_calls/tool_call_id/name/reasoning_content）。

    字段名与 Java `ChatMessage` record 一致；`to_openai()` 给出 llm 层最常见的
    OpenAI 兼容形状（llm 层愿意自己转也行，这里只是方便对接与自测打印）。
    """

    __slots__ = ("role", "content", "tool_calls", "tool_call_id", "name", "reasoning_content")

    def __init__(self, role: str, content: str = "", tool_calls: list[ToolCall__agent_loop] | None = None,
                 tool_call_id: str | None = None, name: str | None = None,
                 reasoning_content: str | None = None) -> None:
        self.role = role
        self.content = content
        self.tool_calls = tool_calls
        self.tool_call_id = tool_call_id
        self.name = name
        self.reasoning_content = reasoning_content

    # ---- 工厂（与 Java 同名）----
    @staticmethod
    def system(content: str) -> "ChatMessage":
        return ChatMessage__agent_loop("system", content)

    @staticmethod
    def user(content: str) -> "ChatMessage":
        return ChatMessage__agent_loop("user", content)

    @staticmethod
    def assistant(content: str, reasoning_content: str | None = None) -> "ChatMessage":
        return ChatMessage__agent_loop("assistant", content, reasoning_content=reasoning_content)

    @staticmethod
    def tool_result(tool_call_id: str | None, content: str) -> "ChatMessage":
        return ChatMessage__agent_loop("tool", content, tool_call_id=tool_call_id)

    @staticmethod
    def assistant_with_tool_calls(content: str, tool_calls: list[ToolCall__agent_loop],
                                  reasoning_content: str | None = None) -> "ChatMessage":
        return ChatMessage__agent_loop("assistant", content, tool_calls, reasoning_content=reasoning_content)

    # ---- 序列化 ----
    def to_openai(self) -> dict[str, Any]:
        m: dict[str, Any] = {"role": self.role}
        if self.content:
            m["content"] = self.content
        if self.reasoning_content:
            m["reasoning_content"] = self.reasoning_content
        if self.tool_calls:
            m["tool_calls"] = [{
                "id": tc.id, "type": "function",
                "function": {"name": tc.name,
                             "arguments": json.dumps(tc.arguments, ensure_ascii=False)},
            } for tc in self.tool_calls]
        if self.tool_call_id is not None:
            m["tool_call_id"] = self.tool_call_id
        if self.name:
            m["name"] = self.name
        return m

    def __repr__(self) -> str:
        return (f"ChatMessage({self.role!r}, content={self.content[:40]!r}, "
                f"tool_calls={self.tool_calls!r})")


class ModelResponse__agent_loop:
    """归一化后的模型响应（对应 Java `ModelResponse`）。"""

    __slots__ = ("content", "tool_calls", "finish_reason", "reasoning_content",
                 "malformed_tool_call", "raw")

    def __init__(self, content: str = "", tool_calls: list[ToolCall__agent_loop] | None = None,
                 finish_reason: str | None = None, reasoning_content: str | None = None,
                 malformed_tool_call: bool = False, raw: Any = None) -> None:
        self.content = content
        self.tool_calls = tool_calls if tool_calls is not None else []
        self.finish_reason = finish_reason
        self.reasoning_content = reasoning_content
        self.malformed_tool_call = malformed_tool_call
        self.raw = raw

    def __repr__(self) -> str:
        return (f"ModelResponse(content={self.content[:40]!r}, tool_calls={len(self.tool_calls)}, "
                f"finish={self.finish_reason!r}, malformed={self.malformed_tool_call})")


class AgentChunk:
    """Agent 流式输出块（对应 Java 的 `AgentChunk` record）。"""

    TEXT = "TEXT"
    TOOL_CALL = "TOOL_CALL"
    DONE = "DONE"
    ERROR = "ERROR"

    __slots__ = ("type", "content", "tool_name", "finished")

    def __init__(self, chunk_type: str, content: str = "", tool_name: str | None = None,
                 finished: bool = False) -> None:
        self.type = chunk_type
        self.content = content
        self.tool_name = tool_name
        self.finished = finished

    @staticmethod
    def text(content: str) -> "AgentChunk":
        return AgentChunk(AgentChunk.TEXT, content, None, False)

    @staticmethod
    def tool_call(tool_name: str, message: str) -> "AgentChunk":
        return AgentChunk(AgentChunk.TOOL_CALL, message, tool_name, False)

    @staticmethod
    def done(full_content: str) -> "AgentChunk":
        return AgentChunk(AgentChunk.DONE, full_content, None, True)

    @staticmethod
    def error(error: str) -> "AgentChunk":
        return AgentChunk(AgentChunk.ERROR, error, None, True)

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "content": self.content, "toolName": self.tool_name,
                "finished": self.finished}

    def __repr__(self) -> str:
        return f"AgentChunk({self.type}, {self.content[:30]!r}, tool={self.tool_name!r})"


# ==========================================================================
# 兜底实现：事件存储 / 会话历史（`lionbox/events/`、`lionbox/sessions/` 就绪后换成真的）
# ==========================================================================


class LocalEventStore:
    """**内存事件桩**（`lionbox/events/` 还没就绪时用）。

    形状对齐 Java `EventStore.recordEvent(sessionId, type, data, summary)`：
    事件类型用与 `LionEvent.EventType` 同名的字符串（USER_MESSAGE / MODEL_THINKING /
    MODEL_RESPONSE / TOOL_CALL_START / TOOL_CALL_COMPLETE / TOOL_CALL_ERROR /
    SYSTEM_ERROR / CONTEXT_COMPRESSED）。

    进程退出即丢，**不是**按天分片的真实事件存储 —— 真实实现由 `lionbox/events/` 提供，
    直接把它 `AgentLoop(event_store=...)` 传进来即可。
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self.events: list[dict[str, Any]] = []

    def record_event(self, session_id: str, event_type: str,
                     data: dict[str, Any] | None = None, summary: str = "") -> dict[str, Any]:
        ev = {"sessionId": session_id, "type": event_type, "data": data or {},
              "summary": summary, "timestamp": time.time()}
        with self._lock:
            self.events.append(ev)
        return ev

    # 与 Java 同名方法的口语化别名，便于其它模块对接
    record = record_event

    def list_events(self, session_id: str | None = None,
                    event_type: str | None = None) -> list[dict[str, Any]]:
        with self._lock:
            items = list(self.events)
        if session_id is not None:
            items = [e for e in items if e["sessionId"] == session_id]
        if event_type is not None:
            items = [e for e in items if e["type"] == event_type]
        return items

    def clear(self) -> None:
        with self._lock:
            self.events.clear()


#: 兼容别名（旧名，保留一个版本）
MemoryEventStore = LocalEventStore


class LocalConversationHistory:
    """**内存会话历史桩**（`lionbox/sessions/` 还没就绪时用）。

    Java 的 ConversationMessage 有 messageId/sessionId/role/content/reasoningContent/
    toolCalls/toolCallId/toolName/timestamp/metadata；这里保留同样的字段名，
    落盘与真实存储由 `lionbox/sessions/` 提供。
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._by_session: dict[str, list[Any]] = {}

    def add_message(self, session_id: str, role: str, content: str = "", *,
                    tool_calls: list[ToolCallRecord__agent_loop] | None = None,
                    tool_call_id: str | None = None, tool_name: str | None = None,
                    reasoning_content: str | None = None,
                    metadata: dict[str, Any] | None = None) -> Any:
        msg = _HistoryMessage(
            message_id=_new_uuid(),
            session_id=session_id, role=role, content=content,
            reasoning_content=reasoning_content, tool_calls=tool_calls,
            tool_call_id=tool_call_id, tool_name=tool_name,
            timestamp=time.time(), metadata=metadata or {})
        with self._lock:
            self._by_session.setdefault(session_id, []).append(msg)
        return msg

    # 口语化别名
    add = add_message

    def get_history(self, session_id: str) -> list[Any]:
        with self._lock:
            return list(self._by_session.get(session_id, []))

    def message_count(self, session_id: str) -> int:
        with self._lock:
            return len(self._by_session.get(session_id, []))

    def clear_history(self, session_id: str) -> None:
        with self._lock:
            self._by_session.pop(session_id, None)


#: 兼容别名（旧名，保留一个版本）
InMemoryHistory = LocalConversationHistory


class _HistoryMessage:
    """内存历史里的一条消息（字段名对齐 Java ConversationMessage）。"""

    __slots__ = ("message_id", "session_id", "role", "content", "reasoning_content",
                 "tool_calls", "tool_call_id", "tool_name", "timestamp", "metadata")

    def __init__(self, message_id: str, session_id: str, role: str, content: str,
                 reasoning_content: str | None, tool_calls: list[ToolCallRecord__agent_loop] | None,
                 tool_call_id: str | None, tool_name: str | None, timestamp: float,
                 metadata: dict[str, Any]) -> None:
        self.message_id = message_id
        self.session_id = session_id
        self.role = role
        self.content = content
        self.reasoning_content = reasoning_content
        self.tool_calls = tool_calls
        self.tool_call_id = tool_call_id
        self.tool_name = tool_name
        self.timestamp = timestamp
        self.metadata = metadata

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"messageId": self.message_id, "sessionId": self.session_id,
                             "role": self.role, "content": self.content}
        if self.reasoning_content is not None:
            d["reasoningContent"] = self.reasoning_content
        if self.tool_calls:
            d["toolCalls"] = [tc.to_dict() for tc in self.tool_calls]
        if self.tool_call_id is not None:
            d["toolCallId"] = self.tool_call_id
        if self.tool_name is not None:
            d["toolName"] = self.tool_name
        return d

    def __repr__(self) -> str:
        return f"_HistoryMessage({self.role!r}, {self.content[:40]!r})"


# ==========================================================================
# 上下文（ThreadLocal，Java 是 WorkspaceContext / SessionContext）
# ==========================================================================
#: 真实的会话/工作区上下文实现（工具读的也是这两份，见下面两个类的说明）
from lionbox.workspace.context import WorkspaceContext as WorkspaceContextBase


def _probe_bool(obj: Any, name: str, default: bool = False) -> bool:
    """读一个**可能是方法也可能是属性**的布尔探针（Java 侧统一是方法调用）。

    【为什么要这个助手】`bool(getattr(adapter, "someMethod", False))` 拿到的是 bound method，
    `bool(方法对象)` 恒为 True —— 与"这个方法返回什么"毫无关系。适配器上的
    `tool_definitions_rejected()` / `prefers_text_tool_calls()` 就是这么被读错的。
    """
    if obj is None:
        return default
    value = getattr(obj, name, None)
    if value is None:
        return default
    if callable(value):
        try:
            value = value()
        except Exception:                               # noqa: BLE001 探针抛错按默认值处理
            return default
    return bool(value)


class WorkspaceContext(WorkspaceContextBase):  # type: ignore[misc]
    r"""当前线程的会话工作区路径（对应 Java `core/workspace/WorkspaceContext`）。

    【为什么是继承而不是自己再写一份 thread-local】这里原来只有一个 `set/get/clear` 的
    独立实现，与 `lionbox/workspace/context.py` 各持一份 `threading.local()`：
    主循环 set 的是本类的，而**工具统一用 `lionbox.workspace.WorkspaceContext.resolve()`
    解析相对路径**（还带越界沙箱）—— 读到的是另一份、永远是 None，于是相对路径全部
    按**进程 CWD**（仓库根目录）解析。实测：`_check_tool_idempotent.py` 里
    "word_count 给目录 / read_file 给目录 / run_background 相对 workdir" 全报
    `文件不存在: <仓库根>\sub`（本该是测试工作区里的 sub）。
    工作区上下文全局只能有一份，所以直接继承真实实现。
    """


class SessionContext__agent_loop(SessionContext):  # type: ignore[misc]
    """当前线程的会话 ID（对应 Java `core/session/SessionContext`）。

    【为什么是继承而不是自己再写一份 thread-local】这里原来是一个**独立**的类，
    和 `lionbox/sessions/context.py` 各持一份 `threading.local()`。主循环 set 的是本类的，
    而工具（ask_user / context_prune / context_window）通过 `lionbox.sessions` 读的是**另一份**
    —— 永远读到 None，三个工具一起报"拿不到当前会话 id"（`_check_ask_user.py` /
    `_check_context_review.py` 抓到的就是这个）。会话上下文全局只能有一份，
    所以直接继承真实实现（shim 一下，`isinstance`/类型注解都不受影响）。
    """


# ==========================================================================
# 常量与提示词（与 Java 逐字一致）
# ==========================================================================

MAX_CALL_REPAIR = 2
MAX_TOOL_ROUNDS = 200
MAX_TOOLS_PER_ROUND = 3
LOCAL_MAX_TOKENS_PER_ROUND = 1024
MAX_TOKENS_CEILING = 4096
FALLBACK_CONTEXT_TOKENS = 32768

REPAIR_HINT_MALFORMED = (
    "【系统提示】你上一次的工具调用是**残缺的**（缺少工具名，或 arguments 不是合法的 JSON），"
    "因此没有被执行。请重新输出**一次完整**的工具调用：只调用一个工具，"
    "工具名必须来自可用工具列表，arguments 必须是合法的 JSON 对象。")
REPAIR_HINT_EMPTY = (
    "【系统提示】你上一次没有输出任何内容（正文为空，也没有工具调用）。"
    "请直接给出结论，或者调用合适的工具继续推进任务。")

TOOL_PROMPT_HINTS: dict[str, str] = {
    "read_file": "读文件内容（已经知道是哪个文件时用它）",
    "head_tail_file": "看文件开头/结尾 N 行。用户说“前 5 行/最后几行”就用它，**不要用 list_directory、不要用 read_file**",
    "line_count": "统计行数。用户问“有多少行代码/一共多少行”就用它；path 给目录会递归累计所有文件",
    "word_count": "统计行数、字数、字节数。用户问“多少字/多大”用它",
    "list_directory": "列目录下的文件和子目录。只在用户问“有哪些文件/列一下目录”时用",
    "directory_tree": "画目录树。用户说“目录结构/画给我看/树状”用它",
    "glob_files": "按名字或后缀找文件。用户说“所有 .java 文件/找找 xyz 文件”用它，pattern 传 **/*.java 这种",
    "search_in_files": "在**文件内容**里搜文本或正则。用户说“哪里提到了 TODO/搜一下内容”用它",
    "create_file": "只创建**空**文件。要写内容请用 write_file",
    "write_file": "新建文件并写入内容（也用于整体覆盖）。用户说“建个文件，写上…”用它",
    "append_file": "往文件末尾追加内容。用户说“追加一行/加到末尾”用它",
    "modify_file": "改文件内容：替换/插入/删除行。用 operation 指定动作，替换给 oldText+content，按行改给 startLine/endLine+content",
    "move_file": "移动或改名。source 是原路径、target 是新路径",
    "copy_file": "复制文件或目录。source → target",
    "delete_file": "删除文件或空目录。用户说“删掉/清理”用它",
    "create_directory": "创建目录（含父目录）",
    "file_info": "看文件大小、修改时间等信息",
    "execute_command": "在常驻终端里执行命令。用户说“跑一下/执行/编译/安装/装依赖”用它",
    "run_background": "后台运行长时间命令（服务、监听、常驻进程）",
    "stop_background": "停掉后台进程",
    "system_info": "系统信息（CPU、内存、操作系统）。用户问“什么配置/多少内存”用它",
    "timestamp": "当前时间。用户问“现在几点/今天几号”用它",
    "hash": "计算哈希值（md5/sha1/sha256）",
    "base64": "Base64 编码或解码",
    "json_format": "JSON 格式化、校验、压缩",
    "yaml_process": "YAML 格式化或校验",
    "generate_uuid": "生成 UUID",
    "get_env": "读环境变量",
    "dns_lookup": "域名解析成 IP",
    "fetch_url": "抓取网页正文（给定 URL 时用它）",
    "http_get": "发 HTTP GET 请求（要接口原始响应时用它）",
    "http_post": "发 HTTP POST 请求",
    "web_search": "联网搜索（不知道具体网址、要查资料时用它）",
    "download_file": "把 URL 上的文件下载到本地",
    "translate": "翻译文本",
    "working_directory": "查看或切换当前工作目录",
    # ---- 上下文经济：这两个工具是"省钱"用的，约束写在下面 CONTEXT_ECONOMY 那一节里 ----
    "context_window": "调整本会话的上下文窗口（默认 16K）。只有 16K 真装不下时才调大，做完立刻调回 16384",
    "context_prune": "删掉本会话前面那些已经没用的历史消息，只保留最近几条（真删）。方案定了、探查过程没用了就用它",
    "git_status": "查看 Git 仓库状态",
    "git_commit": "暂存并提交改动",
    "git_log": "查看提交历史",
    "git_diff": "查看改动差异",
    "git_branch": "查看、创建、切换分支",
    "git_init": "初始化 Git 仓库",
    "git_remote": "查看或管理远程仓库",
    "git_stash": "Git stash 保存/恢复/列出",
    "git_reset": "撤销暂存或回退提交",
    "ask_user": "需要用户做选择或补充信息时提问",
    "regex_test": "测试正则表达式匹配",
    "string_utils": "字符串处理：大小写、trim、长度",
    "escape_string": "字符串转义/反转义（html/json/java/url/regex/shell）",
    "number_convert": "进制转换",
    "format_code": "代码格式化（缩进、换行）",
    "markdown_render": "Markdown 转 HTML",
    "diff_text": "比较两段文本的差异",
    "change_permissions": "修改文件权限（可执行/可写/可读）",
    "cron_parse": "解析 Cron 表达式",
}

#: 从对照表的一行里认工具名（只认形如 xxx_yyy 的小写标识符）
TOOL_TOKEN = re.compile(r"\b([a-z][a-z0-9_]{2,})\b")

TOOL_CHOICE_TABLE = """## 别选错工具（下面这几组最容易混，逐条对照）
**总原则：用户已经指明是哪个文件/目录时，直接用针对它的那个工具，不要先 list_directory 逛一圈。**
- “文件的前 N 行 / 最后几行” → head_tail_file（不是 read_file，更不是 list_directory）
- “有多少行 / 统计行数 / 多少行代码”（文件或目录都算）→ line_count
- “有哪些文件 / 列一下目录” → list_directory；“目录结构 / 画成树” → directory_tree
- “找文件（按名字、后缀）” → glob_files；“找内容（哪里提到 X）” → search_in_files
- “建个文件并写上内容” → write_file；“只建一个空文件” → create_file
- “追加到末尾” → append_file；“替换/改内容/按行改” → modify_file
- “把 A 改名成 B / 移到某处” → move_file；“复制一份” → copy_file；“删掉” → delete_file
- “跑命令 / 编译 / 安装 / 执行一次” → execute_command
- “要一直跑的服务 / 每 5 秒做一次 / 常驻进程” → run_background（不要写脚本再手动跑）
- “现在几点 / 今天几号” → timestamp；“什么 CPU、多少内存” → system_info
- “算哈希” → hash；“base64” → base64；“JSON 格式化” → json_format
- “查资料 / 网上搜” → web_search；“抓某个网址” → fetch_url
- “把某段话翻译成英文/中文” → translate（不要自己翻译，用工具）
- “算一下/转换/解析”这类纯计算，先看有没有对应工具，有就用，别自己心算
"""

CONTEXT_ECONOMY = """【上下文怎么用才省钱】默认窗口是 16K，这是刻意的：窗口越大，每一轮要重算的前缀越多。
所以按下面的规矩来，别把窗口当成越大越好：
1. 默认什么都别做。16K 够干绝大多数活，不要一上来就调窗口。
2. 只有在**真的装不下**的时候才调大：比如要通读一个几千行的文件、或者同时盯好几个模块、
   或者已经压缩过两次还在原地打转。调的时候给一句 reason 说明为什么。
3. **用完立刻还**：那件事做完，马上把窗口调回 16384（context_window，tokens=16384）。
   忘了还，用户后面每一句话都要多花这笔预填充的钱。
4. 省上下文的优先顺序（从便宜到贵）：
   ① 只读你要改的那一段（read_file 带行号范围 / head_tail_file），别整文件读；
   ② 探查完就裁剪：方案定了、前面翻文件试错的过程没用了，用 context_prune 保留最近几条；
   ③ 还不够，最后才考虑调大窗口。
5. 裁剪前想先看看会删掉什么，用 context_prune 的 dry_run=true。
"""

MODE_STANDARD = """## 当前模式：标准模式（STANDARD）

你是全能型编程助手，拥有完整工具集（文件、Shell、Git、网络、代码工具）。

行为准则：
1. 收到任务先快速分析，然后立即动手执行，绝不停留在口头建议。
2. 优先用工具实际读取、修改、运行代码，用真实结果说话。
3. 互不依赖的调用一次给（最多 3 个）；有先后依赖的（得先看到结果才知道下一步）
   一轮只给一个 —— 代码不会丢掉你给的调用，但一次给太多会拖慢。
   注：这里原来写的是"每轮只调用一个工具"，和主提示词（"一次给最多 3 个"）
   以及 maxToolsPerRound 默认 0（不限）自相矛盾，模型两头看会犹豫。
4. 修改文件前先读取相关文件，修改后主动验证（编译/运行/测试）。
5. 输出保持结构化：简短说明 → 工具调用 → 结果总结。
6. 遇到错误时，先读错误信息再定位原因，不要盲目重试。

"""

MODE_PTC = """## 当前模式：PTC 预规划模式（Plan-Then-Code）

本模式下你**必须先规划、后执行**，严格按以下流程：

第一步：输出完整执行计划（用 Markdown 编号列表）：
- 目标拆解
- 每一步要调用的工具及其目的
- 风险点与验证方式
计划输出完毕后，再开始调用工具。

第二步：按计划**逐步执行**，每执行一步：
- 有先后依赖的步骤一轮只给一个调用；互不依赖的可以一轮一起给（最多 3 个）
- 拿到结果后对照计划核对进度
- 如结果与预期不符，先修正计划再继续

第三步：全部步骤完成后，输出执行总结（计划 vs 实际）。

禁止：跳过计划直接动手；计划被打乱后不回头对照。
（注：原来这里写"禁止一次调用多个工具"，和主提示词冲突，已按实际语义改写。）

"""

MODE_CREATIVE = """## 当前模式：创造模式（CREATIVE）

本模式用于**扩展 Lion-Code 自身能力**：编写、修改、安装、卸载插件。

你的创造空间：
1. 新插件源码写入工作区 `.lioncode/plugins/` 目录，按 ToolPlugin / SkillPlugin 接口实现。
2. 可以读取项目现有插件源码（core/plugin 目录）作为实现参考。
3. 可以使用全部工具（文件、Shell、Git、网络、代码工具），鼓励探索性方案。
4. 修改完插件后用 Shell 编译验证（如 mvn compile）。
5. 安装/卸载由运行时插件注册表管理，你负责产出高质量插件代码与说明。

行为准则：
- 大胆创造，但保证代码可编译、可测试。
- 每次只调用一个工具，逐步构建，不要试图一步到位。
- 交付时说明插件功能、用法和安装方式。

"""

MODE_MINIMAL = """## 当前模式：极简模式（MINIMAL）

本模式仅开放**文件工具和 Shell 工具**，追求最少步骤、最高效率。

行为准则：
1. 只使用文件工具（read_file / write_file / modify_file / create_file /
   append_file / delete_file / move_file / copy_file / list_directory /
   directory_tree / glob_files / search_in_files / line_count / word_count /
   head_tail_file / file_info / change_permissions）和 Shell 工具
   （execute_command / run_background / stop_background），不得调用其他任何工具。
2. 回复务必简短：不解释背景、不寒暄、不说废话，直接执行。
3. 能用一条命令完成的事，不要拆成多条。
4. 每轮只调用一个工具；结果返回后立即执行下一步。
5. 输出风格：一句话目标 → 工具调用 → 结果（如有错误，一句话说明并修复）。

"""

MODE_INSTRUCTIONS = {
    AgentMode.STANDARD: MODE_STANDARD,
    AgentMode.PTC: MODE_PTC,
    AgentMode.CREATIVE: MODE_CREATIVE,
    AgentMode.MINIMAL: MODE_MINIMAL,
}


# ==========================================================================
# 主循环
# ==========================================================================


class _ToolOutcome:
    """一次工具派发的结果（Java 只回 bool，这里多带一份正文给自测/上层用）。"""

    __slots__ = ("success", "content")

    def __init__(self, success: bool, content: str = "") -> None:
        self.success = success
        self.content = content

    def __bool__(self) -> bool:      # 兼容 Java 的 boolean 语义
        return self.success

    def __repr__(self) -> str:
        return f"_ToolOutcome(success={self.success}, content={self.content[:40]!r})"


class _ToolCallAccumulator:
    """工具调用增量累积器（流式分片用）。"""

    __slots__ = ("id", "name_builder", "args_builder")

    def __init__(self) -> None:
        self.id = "call_" + _new_uuid().replace("-", "")[:8]
        self.name_builder: list[str] = []
        self.args_builder: list[str] = []


class AgentLoop:
    """Agent 主循环。

    :param client:         模型调用层（见模块 docstring 的 ChatClient 接口）
    :param config_store:   `AppConfigStore`；读 `tool_call_mode` / `is_local_mode` /
                           `snapshot()["baseUrl"]`。传 None 时按"云端 + auto"处理。
    :param registry:       工具注册表，默认全局 `REGISTRY`
    :param event_store:    事件存储；None 时用 `LocalEventStore()`（内存桩）
    :param history:        会话历史；None 时用 `LocalConversationHistory()`（内存桩）
    :param workspace:      工作区路径（影响相对路径解析与系统提示词）
    :param control/guard/budget/approval: 各子系统，默认各建一个
    :param use_native_tools: 归一化后的工具调用通道 ——
                            "native" 强制下发 tools、"prompt"/"text" 强制不下发、
                            "auto" 按适配器能力与本地模式判断（与 Java 的 useNativeTools 一致）
    """

    def __init__(self, client: ChatClient | None = None, *, config_store: Any = None,
                 registry: Any = None, event_store: Any = None, history: Any = None,
                 workspace: str | os.PathLike[str] | None = None,
                 workspace_resolver: Callable[[str], str | os.PathLike[str] | None] | None = None,
                 permission_resolver: Callable[[str], str | None] | None = None,
                 control: AgentControlManager | None = None,
                 guard: ToolCallGuard | None = None,
                 budget: ContextBudget | None = None,
                 approval: ApprovalPolicy | None = None,
                 context_limit_tokens: int = 0,
                 context_keep_recent: int = 6,
                 tool_timeout_seconds: int = 600,
                 use_native_tools: str = "auto",
                 spi: Any = None) -> None:
        self.client = client
        self.config_store = config_store
        self.registry = registry if registry is not None else REGISTRY
        self.event_store = event_store if event_store is not None else LocalEventStore()
        self.history = history if history is not None else LocalConversationHistory()
        self.workspace = str(workspace) if workspace is not None else None
        self._workspace_resolver = workspace_resolver
        self._permission_resolver = permission_resolver
        # 历史层的 add_message 收的是「一条消息对象」（lionbox/sessions，与 Java 一致）
        # 还是散开的 (session_id, role, content) —— 签名看一眼，两种都支持
        self._history_takes_object = _accepts_message_object(
            getattr(self.history, "add_message", None))
        self.control = control if control is not None else AgentControlManager()
        self.tool_guard = guard if guard is not None else ToolCallGuard()
        self.context_budget = budget if budget is not None else ContextBudget()
        self.approval_policy = approval if approval is not None else ApprovalPolicy()
        self.spi = spi

        self.context_limit_tokens = int(context_limit_tokens)
        self.context_keep_recent = int(context_keep_recent)
        self.tool_timeout_seconds = int(tool_timeout_seconds)
        self._native_pref = str(use_native_tools or "auto").strip().lower()

        #: 会话 → 当前每轮生成长度上限（撞到 length 临时升档，下一条用户消息复位）
        self.round_cap_by_session: dict[str, int] = {}
        #: 模型窗口查询结果缓存（**按模型名分键**，换模型必须重查）
        self.model_context_cache: dict[str, int] = {}
        #: 每个会话"当前这一轮流式调用"的内层订阅句柄
        self._active_stream_sub: dict[str, Any] = {}
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # 系统提示词
    # ------------------------------------------------------------------
    def mode_instructions(self, mode: str) -> str:
        return MODE_INSTRUCTIONS.get(AgentMode.normalize(mode), MODE_STANDARD)

    def build_system_prompt(self, mode: str, workspace_path: str | None,
                            user_message: str, native_tools: bool,
                            session_id: str | None = None) -> str:
        mode = AgentMode.normalize(mode)
        p: list[str] = []
        p.append("你是 Lion-Code Agent，通过调用工具真实操作文件和命令来完成任务。\n\n")

        # 当前工作区：所有文件操作和命令执行都在此工作区内进行
        p.append("## 工作区\n")
        p.append((workspace_path if workspace_path is not None else "(未设置)") + "\n")
        p.append("文件与命令都在此工作区内；path 可用相对路径（相对工作区）或绝对路径。\n")
        # 执行环境：实测模型爱写 Unix 命令，在 Windows 的 cmd 里 ls/cat/rm 都报
        # "'ls' 不是内部或外部命令"。现在 execute_command 走 PowerShell
        # （ls/cat/rm/cp/mv/pwd 都是内置别名），这里把环境说清楚。
        if "win" in os.name.lower() or "windows" in sys.platform.lower():
            p.append("执行环境是 **Windows**，execute_command 走 PowerShell：ls/cat/rm/cp/mv/pwd 都能用，")
            p.append("但多条命令之间用 `;` 分隔，不要用 `&&`（Windows PowerShell 不认）。\n")
            p.append("execute_command 是**一个持续运行的终端**（同一工作区共用一个会话）：")
            p.append("cd 切过的目录、设过的变量和函数都会留到下一次调用，不用每条命令都重新 cd。\n")
        p.append("\n")

        # 根据模式添加专属提示词（每个模式独立撰写，行为规则各不相同）
        p.append(self.mode_instructions(mode))

        # 极简模式：把"真的可用的工具名"钉在提示词里。
        #
        # 【为什么非要写死一份】上面那段只说"仅开放文件工具和 Shell 工具"，而模型对
        # "文件工具"的理解是它自己训练里的那套名字（试过 list_files、file_read…）。
        # 实测极简模式跑一轮，它照样去调 web_search / timestamp —— 全是模式外的工具，
        # 用户看到的就是一屏 ❌。所以这里把筛选后的真实工具名直接列出来，不给它猜的空间。
        if mode == AgentMode.MINIMAL:
            minimal_names = sorted(
                t.name for t in self.filtered_tools(AgentMode.MINIMAL, session_id)
                if getattr(t, "name", None))
            p.append("本模式实际可用的工具**只有下面这些**（其余工具在本模式不存在，不要调用）：\n")
            p.append("、".join(minimal_names) + "\n\n")

        # 注入适用技能的领域能力提示词（按用户消息匹配）
        #
        # 【极简模式不注入】技能正文里经常出现"用 web_search 查一下""用 git_commit 提交"
        # 这类话，而极简模式只开放文件 + shell 工具 —— 注进去等于**教模型去调不存在的工具**，
        # 用户看到的就是一屏 ❌（实测套件就是这么抓到的：极简提示词里冒出 web_search）。
        if mode != AgentMode.MINIMAL:
            p.append(self.build_skill_prompt(user_message))

        # 输出纪律：本地模型约 10.8 token/s，一句话能交代的事写成一段就是几十秒。
        # 这几条集中放在一起（散着写模型会挑着遵守），顺序按"影响速度"排。
        p.append("\n## 输出纪律（直接影响速度，必须守）\n")
        p.append("1. 正文极简：一轮最多两句话（≤60 字）。不解释背景、不罗列计划、不复述文件内容、不重复工具结果。\n")
        p.append("2. 要动手就直接动手：不要写“我这就去读取/修改…”这类过渡句，直接给工具调用。\n")
        # 这一条直接决定"快不快"：本机 11-12 token/s，一轮一个工具 = 50 个工具 50 轮 ≈ 7 分钟。
        p.append("3. 互不依赖的调用要一次给（最多 3 个）：同时读几个文件、同时查几样信息，一轮里一起给；\n")
        p.append("   有先后依赖的（得先看到结果才知道下一步）就一轮只给一个。一次给太多会拖慢（建议 3 个以内）；代码不会丢掉你给的调用。\n")
        p.append("4. 工具结果回来后：能用一句话回答就回答，要继续做就直接调下一个工具，不要总结过程。\n")
        p.append("5. 不输出思考过程、不写“第一步/第二步”的规划清单、不复述工具参数。\n\n")

        # 工具说明。
        #
        # 原生通道：**不列清单** —— Qwen 的 Jinja 模板会自己把 tools 渲染成 "# Tools" 段
        # （还带 "Required parameters MUST be specified"），我们那份手写清单纯属重复，
        # 白白多烧一千多 token，还可能和模板里的定义打架。
        # 文本通道：清单就是模型能看到的**唯一**工具说明，所以必须列全，
        # 而且要带参数名（1.1.4 里工具第一次调用老失败，就是因为只给了名字和一句描述）。
        tools = self.filtered_tools(mode, session_id)
        if tools:
            if native_tools:
                p.append("## 可用工具\n")
                p.append("本次请求已随消息下发 " + str(len(tools))
                         + " 个工具定义（见 # Tools），参数名与必填项以那份定义为准，不要自己发明。\n")
                p.append("把调用放在 tool_calls 里返回，不要写成正文文字。\n\n")
            else:
                p.append("## 可用工具（" + str(len(tools)) + " 个）\n")
                p.append("括号里是参数名，带 * 的是必填。**参数名必须照抄**，写错或漏必填都会直接调用失败。\n")
                for tool in tools:
                    p.append("- " + str(tool.name) + self.tool_signature(tool) + ": "
                             + self.prompt_description(tool) + "\n")
                p.append("\n")
                p.append(self.tool_choice_table(tools) + "\n")

                p.append("## 工具调用格式\n")
                p.append("首选 JSON：\n")
                p.append("<tool_call>\n{\"name\": \"read_file\", \"arguments\": {\"path\": \"a.txt\"}}\n</tool_call>\n\n")
                p.append("也认 XML：\n")
                p.append("<tool_call>\n<name>read_file</name><arguments>{\"path\": \"a.txt\"}</arguments>\n</tool_call>\n\n")
                # 模型是按 Qwen 模板微调的，它最顺手的其实是下面这种；解析器三种都认，
                # 写清楚是为了让它别在格式上纠结（实测它会先吐一句说明再吐模板格式）。
                p.append("也认模板原生格式（**推荐用这个**）：\n")
                p.append("<tool_call>\n<function=read_file>\n<parameter=path>a.txt</parameter>\n</function>\n</tool_call>\n\n")
                p.append("- 只能用上面清单里的工具名，**不要发明工具**（发明出来的会被直接拒绝）。\n")
                p.append("- arguments 必须是合法 JSON；参数名只用上面工具里的，不要发明参数。\n")
                p.append("- 调用写进 <tool_call> 里，正文可以只有一句话，紧跟调用即可。\n\n")

                # 批量示例：实测**必须把例子写出来**，模型才会真的一轮给 3 个块；
                # 只写一句"可以一次给多个"它还是只给一个（试过）。
                # 一轮 3 个 = 轮数砍到 1/3，在 11 token/s 的本机就是实打实的 3 倍速。
                p.append("## 一次给多个调用（省时间，最多 3 个）\n")
                p.append("下面几件事互不依赖时，**连着写多个 <tool_call> 块一次给完**，别一个一个等：\n")
                p.append("<tool_call>\n<function=read_file>\n<parameter=path>a.txt</parameter>\n</function>\n</tool_call>\n")
                p.append("<tool_call>\n<function=system_info>\n</function>\n</tool_call>\n")
                p.append("<tool_call>\n<function=timestamp>\n<parameter=format>%H:%M</parameter>\n</function>\n</tool_call>\n\n")
                p.append("有先后依赖的（要先看到结果才知道下一步）仍然一次只给一个；一次超过 3 个会被丢掉。\n\n")
        p.append("## 必须用工具的情形\n")
        p.append("读/写/改/删文件、执行命令、看目录、搜内容、Git 操作、查系统信息 —— 一律调工具，不许只给建议。\n")

        # 上下文经济约束：只在"模型真的有这两个工具"时才写进去 ——
        # 用户在设置里把插件关掉后，提示词里就不该再出现它的用法（否则模型会去调一个不存在的工具）。
        if any(t.name == "context_window" for t in tools) or any(t.name == "context_prune" for t in tools):
            p.append("\n" + CONTEXT_ECONOMY + "\n")

        # 插件 SPI：追加段落（技能目录让模型自己挑技能、插件清单、团队智能体说明等）。
        # 放在最后：这些是"可选能力"，不能挤掉前面的硬性格式约定（模型只看前几屏）。
        for section in self._spi_sections(session_id, workspace_path, user_message):
            p.append("\n" + section + "\n")

        return "".join(p)

    def preview_system_prompt(self, mode: str, workspace_path: str | None,
                              user_message: str) -> str:
        """提示词体检用：把这一轮真正会发出去的系统提示词原样返回。"""
        return self.build_system_prompt(mode, workspace_path, user_message, self.use_native_tools())

    def preview_uses_native_tools(self) -> bool:
        """提示词体检用：当前这一轮走原生 function calling 还是文本 <tool_call> 约定。"""
        return self.use_native_tools()

    def preview_tool_definitions(self, mode: str, session_id: str | None = None
                                 ) -> list[dict[str, Any]]:
        """提示词体检用：原生通道下才会随请求下发的 tools 定义。"""
        return self.build_tool_definitions(mode, session_id)

    # ---- 提示词辅助 ----
    @staticmethod
    def prompt_description(tool: ToolPlugin) -> str:
        """清单里这条工具该怎么描述。

        【为什么要人工写一份覆盖】原来直接用工具自己的 description 砍到 48 字，
        结果模型**选错工具**：问"config.txt 前 5 行是什么"，它调 list_directory；
        问"统计多少行代码"，它还是调 list_directory —— 因为清单里
        `head_tail_file: 查看文件头部或尾部N行` 和 `line_count: 统计文件行数`
        这两句话没告诉它"用户这么说的时候该用我"。工具自己的描述是给"已经决定要用它的人"
        看的，清单要的是**选择依据**：触发词 + 和谁容易混。没写覆盖的工具继续用原描述，不会漏。
        """
        hint = TOOL_PROMPT_HINTS.get(tool.name)
        return hint if hint is not None else AgentLoop.short_description(tool.description)

    @staticmethod
    def tool_choice_table(available: Sequence[ToolPlugin]) -> str:
        """生成工具选择对照表，并**把手头没有的工具那几行去掉**。

        对照表是静态文案，里面点名了 head_tail_file、line_count 这些工具；
        用户在设置里把插件关掉之后，清单里已经没这个工具了，表格却还让模型去用它 ——
        模型照做就撞"未找到工具"，白烧一轮（本机一轮十几秒）。所以这里按当前实际可用的
        工具名过滤一遍：一行里"→"后面那个主工具不在名单里，整行删掉。
        """
        names = {t.name for t in available if getattr(t, "name", None)}
        out: list[str] = []
        for line in TOOL_CHOICE_TABLE.split("\n"):
            arrow = line.find("→")
            primary = None
            if arrow >= 0:
                m = TOOL_TOKEN.search(line[arrow:])
                if m:
                    primary = m.group(1)
            if primary is not None and primary not in names:
                continue   # 这个工具当前不可用，别让模型去调
            out.append(line + "\n")
        return "".join(out)

    @staticmethod
    def short_description(description: str | None) -> str:
        """工具描述砍到一句话：合并空白，遇到第一个句号/分号就截断，最长 48 字。

        清单只用来告诉模型"有哪些工具"，细节在微调时已经学过；
        原文照抄会把几百 token 的说明塞进每一轮请求里。
        """
        if description is None:
            return ""
        s = re.sub(r"\s+", " ", description).strip()
        cut = len(s)
        for sep in ("。", "；", ". ", "; "):
            i = s.find(sep)
            if 0 < i < cut:
                cut = i
        if cut > 48:
            cut = 48
        return s[:min(cut, len(s))].strip()

    @staticmethod
    def tool_signature(tool: ToolPlugin) -> str:
        """工具的参数签名，形如 `(path*, content)`，带 * 的是必填。

        【为什么必须有这个】一次真实测试（54 个工具逐一调用）里，几乎每个工具都是
        "第一次失败、第二次成功"，失败原因清一色是 `缺少必需参数: action` /
        `缺少必需参数: input` —— 因为文本通道下不下发 tools 定义，提示词里又只有工具名
        和一句描述，模型根本不知道参数该叫什么，只能猜。一次失败 = 一整轮
        （预填充+生成，本地 10~40 秒），参数名这几十个字符，换回来的是几十次往返。
        """
        try:
            definition = tool.function_definition()
            # 【注意嵌套层】Java 的 ToolPlugin.getFunctionDefinition() 返回的是
            # {"type":"function","function":{"name":…,"description":…,"parameters":{…}}}，
            # 而 AbstractToolPlugin 里还有个便捷方法直接给 parameters。
            # Python 侧 function_definition() 是前者，所以这里必须往 function 里再走一层
            # —— 少了这一层，清单里每个工具都不会带参数名，
            # 模型只能猜参数名，一次失败就是一整轮（本地 10~40 秒）。
            fn = definition.get("function") if isinstance(definition, dict) else None
            params = fn.get("parameters") if isinstance(fn, dict) else None
            if not isinstance(params, dict):
                return ""
            props = params.get("properties")
            if not isinstance(props, dict) or not props:
                return ""
            required = set()
            req_list = params.get("required")
            if isinstance(req_list, (list, tuple)):
                for r in req_list:
                    if r is not None:
                        required.add(str(r))
            parts = [str(k) + ("*" if str(k) in required else "") for k in props.keys()]
            return "(" + ", ".join(parts) + ")"
        except Exception:
            return ""

    def build_skill_prompt(self, user_message: str) -> str:
        """构建技能提示词片段（把适用技能的领域能力提示词注进系统提示词）。

        Java 版从 `pluginRegistry.getSkillPlugins()` 里挑 `isApplicable(userMessage)` 的技能。
        Python 侧技能插件（`lionbox/skills/`）还没就绪，注册表里也就没有技能插件；
        所以这里返回空串 —— **一旦技能模块就绪，把 `applicable_skills` 回调接上即可**
        （见 `AgentLoop(spi=...)` 的 `skills_for(user_message)` 约定）。
        """
        skills = self._skills_for(user_message)
        if not skills:
            return ""
        p: list[str] = ["\n## 激活的领域技能\n\n"]
        for skill in skills:
            # 【两个来源都要认】
            #   · 插件式技能（`skills/service.py`、`skills/legacy.py`）提供 `system_prompt_fragment()`
            #   · 文件式技能（`skills/definition.py` 的 `SkillDefinition`）只有 `body` 字段
            # 原来只认前者，于是**文件式技能一律被 continue 跳过** ——
            # 实测：`skills_for()` 明明命中了 document/frontend，系统提示词里却一个字都没有
            # （只有目录行，没有正文），`_check_skills_at` 的"关键词命中的技能正文照旧注入"
            # 与"钉住的技能正文每轮都在提示词里"两条一直红。
            fragment = getattr(skill, "system_prompt_fragment", None)
            if callable(fragment):
                fragment = fragment()
            if fragment is None or not str(fragment).strip():
                fragment = getattr(skill, "body", None)
            if fragment is None or not str(fragment).strip():
                continue
            # 标题：插件式有 name，文件式是 display_name / id
            title = (getattr(skill, "name", None)
                     or getattr(skill, "display_name", None)
                     or getattr(skill, "id", ""))
            p.append("### " + str(title) + "\n\n")
            p.append(str(fragment).strip() + "\n\n")
        return "".join(p)

    def _skills_for(self, user_message: str) -> list[Any]:
        if self.spi is None:
            return []
        fn = getattr(self.spi, "skills_for", None)
        if fn is None:
            return []
        try:
            return list(fn(user_message) or [])
        except Exception:
            return []

    # ------------------------------------------------------------------
    # SPI（技能注入 / @ 引用展开 / 工具过滤 / 大循环参数）
    # ------------------------------------------------------------------
    def _spi_sections(self, session_id: str | None, workspace_path: str | None,
                      user_message: str) -> list[str]:
        if self.spi is None:
            return []
        fn = getattr(self.spi, "extra_system_sections", None)
        if fn is None:
            return []
        try:
            items = fn(session_id, workspace_path, user_message) or []
        except Exception:
            return []
        return [str(s) for s in items if s is not None and str(s).strip()]

    def _apply_transforms(self, session_id: str, user_message: str) -> str:
        if self.spi is None:
            return user_message
        fn = getattr(self.spi, "transform_user_message", None)
        if fn is None:
            return user_message
        try:
            out = fn(session_id, user_message)
            return user_message if out is None else str(out)
        except Exception:
            return user_message

    def _loop_int(self, session_id: str, key: str, fallback: int) -> int:
        if self.spi is None:
            return fallback
        fn = getattr(self.spi, "loop_int", None)
        if fn is None:
            return fallback
        try:
            return int(fn(session_id, key, fallback))
        except Exception:
            return fallback

    def filtered_tools(self, mode: str, session_id: str | None = None) -> list[ToolPlugin]:
        """按模式取工具，再过一遍插件 SPI 的过滤。

        用户在设置里关掉的插件，它的工具直接从提示词里消失 —— 这样模型压根不会去调，
        比"调了再拒绝"省一整轮。
        """
        all_tools = self.registry.for_mode(mode)
        if self.spi is None:
            return all_tools
        fn = getattr(self.spi, "filter_tool_names", None)
        if fn is None:
            return all_tools
        try:
            names = set(fn(session_id, {t.name for t in all_tools}) or [])
        except Exception:
            return all_tools
        return [t for t in all_tools if t.name in names]

    # ------------------------------------------------------------------
    # 工具定义 / 通道选择
    # ------------------------------------------------------------------
    def build_tool_definitions(self, mode: str, session_id: str | None = None
                               ) -> list[dict[str, Any]]:
        """构建工具定义列表（OpenAI function calling 格式）。

        【为什么要带 sessionId】原生通道下这份定义是随请求下发的，等于模型看到的完整
        工具集；如果这里不过滤，用户在设置里关掉的插件**照样会被下发给模型、而且真调用了
        还能执行** —— "关掉插件"就变成了只影响文本通道的假开关。
        """
        tools = self.filtered_tools(mode, session_id)
        if not tools:
            return []
        definitions: list[dict[str, Any]] = []
        for tool in tools:
            # 跳过 name 或 description 为空的工具，防止模型 API 返回 400 错误
            name = getattr(tool, "name", None)
            desc = getattr(tool, "description", None)
            if not name or not str(name).strip() or not desc or not str(desc).strip():
                continue
            func_def = tool.function_definition()
            fn = func_def.get("function") if isinstance(func_def, dict) else None
            if not isinstance(fn, dict) or fn.get("name") is None or fn.get("description") is None:
                continue
            definitions.append(func_def)
        return definitions

    def _tool_call_mode(self) -> str:
        if self.config_store is None:
            return "auto"
        try:
            mode = getattr(self.config_store, "tool_call_mode", "auto")
        except Exception:
            mode = "auto"
        v = str(mode or "auto").strip().lower()
        # 契约值只有 auto / native / text（Java `AppConfigStore.TOOLCALL_TEXT`）；
        # `prompt` 是内部历史别名，统一归一到 text，别再让它漏出去。
        if v == "prompt":
            return "text"
        return v if v in ("auto", "native", "text") else "auto"

    def _is_local_mode(self) -> bool:
        if self.config_store is None:
            return False
        try:
            return bool(self.config_store.is_local_mode)
        except Exception:
            return False

    def use_native_tools(self) -> bool:
        """本轮是否走**原生 function calling**（把 tools 定义随请求下发）。

        三种取值（设置里可切，默认 auto）：
          auto   → 默认都走原生：云端 OpenAI 兼容 API 和随软件拉起的 llama-server 都支持。
                   llama-server 会按模型的 chat 模板把原生语法解析成标准 tool_calls；
                   实测不下发 tools 时模型会开始**编造工具**，所以本地也必须下发。
          native → 强制下发 tools
          text   → 强制不下发 tools，只靠系统提示词里的文本格式（给不认 tools 的端点兜底）

        无论哪种方式，**两种格式的解析器都在**：模型用哪种回就认哪种。

        【本地走文本通道】2026-09-29 抓包实测的结论：本机 llama-server 会把模型吐的多个
        `<tool_call>` 块**揉成一个调用**，把后续块的 XML 塞进第一个调用的 arguments 里
        （`{"path":"test.txt\\n</parameter></function>...`）→ 不是合法 JSON → 整轮作废，
        每轮 91 秒白烧。文本通道下模型输出是纯文本，多个块由我们自己的
        `QwenToolCallParser` 解析，服务端碰不到它。自定义 API（云端）仍然走原生。
        """
        adapter = self._active_adapter()
        # 【探针方法必须"调用"，不能只看有没有】`tool_definitions_rejected` /
        # `prefers_text_tool_calls` 在 `ModelAdapter` 上是**方法**（Java 也是方法调用）。
        # 写成 `bool(getattr(adapter, "xxx", False))` 拿到的是 bound method，
        # `bool(方法对象)` 恒为 True —— 结果 `use_native_tools()` 永远返回 False：
        # 本地模式显式选 native、自定义 API 走 auto，两条路都不下发 tools
        # （`_check_tool_channel.py` 抓到的：期望原生，实际文本）。
        rejected = _probe_bool(adapter, "tool_definitions_rejected")
        mode = self._tool_call_mode()
        if mode == "text":
            return False
        if mode == "native":
            return not rejected
        if self._native_pref in ("prompt", "text"):
            return False
        if self._native_pref == "native":
            return not rejected
        # ---- auto ----
        if self._is_local_mode():
            return False
        return adapter is None or (not _probe_bool(adapter, "prefers_text_tool_calls")
                                   and not rejected)

    def _active_adapter(self) -> Any:
        """当前激活的适配器（llm 层可能把它挂在 client 上，或由外部注入）。

        loop 只用到两个可选探针：`tool_definitions_rejected` / `prefers_text_tool_calls` /
        `get_available_models()`。拿不到就当作"没有适配器"，行为落到与 Java 一致的默认分支。
        """
        adapter = getattr(self.client, "active_adapter", None)
        if callable(adapter):
            try:
                adapter = adapter()
            except Exception:
                return None
        if adapter is not None:
            return adapter
        for attr in ("adapter", "model_adapter"):
            cand = getattr(self.client, attr, None)
            if cand is not None:
                return cand
        return None

    # ------------------------------------------------------------------
    # 主入口：同步
    # ------------------------------------------------------------------
    def process_message(self, session_id: str, user_message: str, mode: str,
                        thinking_level: str | None = None, model: str | None = None) -> str:
        """处理用户消息（同步模式），返回 Agent 最终响应。"""
        mode = AgentMode.normalize(mode)
        thinking_level = ThinkingLevel__agent_control.from_name(thinking_level)

        # 0. 插件扩展点：用户消息改写（@ 文件 / @ 历史对话 展开成真实上下文）。
        #    事件里记的是**用户原话**（界面上要显示用户输入的样子，展开后的几 KB 文件内容
        #    塞进事件流会把界面刷爆），对话历史里存的是**展开后**的内容（模型要看到上下文）。
        raw_user_message = user_message
        user_message = self._apply_transforms(session_id, user_message)

        # 1. 记录用户消息事件
        self._record(session_id, "USER_MESSAGE", {"content": raw_user_message},
                     "用户消息: " + _truncate(raw_user_message, 100))

        # 2. 保存用户消息到对话历史
        self._append_history(session_id, "user", user_message)

        # 2.5 新任务开始：清除之前的暂停/停止状态
        self.control.reset(session_id)
        self.tool_guard.reset(session_id)          # 新的一条用户消息：计数清零
        with self._lock:
            self.round_cap_by_session.pop(session_id, None)   # 生成上限也复位

        # 3. 构建消息列表
        messages: list[Any] = self.build_messages(session_id, mode, user_message)

        # 3.5 构建工具定义列表（仅原生 function calling 模式下随请求下发）
        native_tools = self.use_native_tools()
        tool_definitions = self.build_tool_definitions(mode, session_id) if native_tools else []

        # 4. 工具调用循环（无轮次上限，直到模型给出最终答案）
        round_no = 0
        repairs = 0   # 残缺工具调用 / 空响应的纠正次数（有上限，防止死循环）

        while True:
            round_no += 1

            # 4.4 大循环插件给的轮次上限（默认 0 = 不限，保持"只有用户能停"的老行为）。
            max_rounds = self._loop_int(session_id, "maxIterations", 0)
            if max_rounds > 0 and round_no > max_rounds:
                cap_msg = ("⏹ 已达到本轮最大工具调用轮数（" + str(max_rounds)
                           + "，可在 设置 → 插件 → Agent 大循环 里调整）。")
                self._record(session_id, "SYSTEM_ERROR",
                             {"error": "轮次上限", "rounds": round_no - 1}, cap_msg)
                self._sound("ERROR")
                self._append_history(session_id, "assistant", cap_msg)
                return cap_msg

            # 控制检查：暂停时阻塞等待，停止时中止任务
            try:
                self.control.check_control(session_id)
            except AgentStoppedException:
                stop_msg = "⏹ 任务已手动停止（共执行 " + str(round_no - 1) + " 轮工具调用）。"
                self._record(session_id, "SYSTEM_ERROR", {"error": "手动停止"}, "任务已手动停止")
                self._sound("ERROR")
                self._append_history(session_id, "assistant", stop_msg)
                return stop_msg

            # 4.5 上下文预算：历史 + 本轮到目前的工具结果快把模型窗口塞满时，先折叠成摘要。
            #     不做这件事的后果不是"变慢"，是**整个会话废掉**：请求超长 → 服务端 400 →
            #     用户看到"模型调用失败"，而且之后每条消息都还是超长。
            messages = self.maybe_compress_context(session_id, messages, model)

            # 5. 调用模型
            self._record(session_id, "MODEL_THINKING", {"round": round_no}, "模型思考中...")

            try:
                response = self._chat(messages, model, thinking_level, tool_definitions,
                                      self.max_tokens_per_round(session_id))
            except Exception as e:
                self._record(session_id, "SYSTEM_ERROR", {"error": str(e)},
                             "模型调用失败: " + str(e))
                self._sound("ERROR")
                return "模型调用失败: " + str(e)

            self._record(session_id, "MODEL_RESPONSE",
                         {"content": _truncate(response.content, 200),
                          "hasToolCalls": bool(response.tool_calls)}, "模型响应")

            # 撞到生成长度上限：本轮很可能被截断（大文件写入），把下一轮上限翻倍
            if response.finish_reason and "length" in response.finish_reason.lower():
                self.bump_round_cap(session_id)

            # 6. 如果没有工具调用，检查文本中是否有 XML/JSON 格式的工具调用
            tool_calls = list(response.tool_calls)
            response_content = response.content if response.content is not None else ""
            if not tool_calls:
                # 尝试从文本中解析工具调用（支持 XML 和 JSON 格式）
                tool_calls = self.parse_tool_calls_from_text(response_content)
                if tool_calls:
                    # 提取纯文本部分（去掉工具调用标签）
                    response_content = self.remove_tool_call_blocks(response_content)

            # 6.5 一轮执行几个工具：默认**不限制**（模型给几个执行几个 —— 用户明确要求过，
            #     本机 11 token/s，砍成一轮一个等于把 50 个工具拖成 7 分钟）。
            #     但"Agent 大循环插件"把它做成可配：用户设了上限就按上限截断 ——
            #     截断按**原始顺序**处理（超出的那条回一句"未执行、下一轮继续"），
            #     这样 tool 结果的顺序永远和模型给的调用顺序一致。
            declared_count = len(tool_calls)
            tools_cap = self._loop_int(session_id, "maxToolsPerRound", 0)
            if tools_cap > 0 and declared_count > tools_cap:
                self._record(session_id, "TOOL_CALL_START",
                             {"declared": declared_count, "cap": tools_cap},
                             "按用户设置截断本轮工具调用：" + str(declared_count) + " → " + str(tools_cap))

            # 7. 如果仍然没有工具调用，返回最终答案
            if not tool_calls:
                # 7.1 先判断这是不是「模型想做工具调用但调用残缺」或者「整轮什么都没输出」。
                #     这两种情况都不能当成正常收尾 —— 否则用户会收到一句空白回答、
                #     任务被静默结束。纠正一次再试，最多 MAX_CALL_REPAIR 次。
                malformed = bool(response.malformed_tool_call)
                if repairs < MAX_CALL_REPAIR and (malformed or not response_content.strip()):
                    repairs += 1
                    self._record(session_id, "TOOL_CALL_ERROR",
                                 {"malformed": malformed, "repair": repairs},
                                 "残缺工具调用，已纠正重试" if malformed else "空响应，已纠正重试")
                    self.add_notice(session_id, self.repair_hint(malformed))
                    messages = self.build_messages(session_id, mode, user_message)
                    continue

                final_answer = response_content
                self._append_history(session_id, "assistant", final_answer)
                self._sound("DONE")
                return final_answer

            # 8. 有工具调用：保存助手消息（含工具调用，过滤无效的）
            records = [ToolCallRecord__agent_loop(tc.id, tc.name, tc.arguments)
                       for tc in tool_calls if tc.name is not None and str(tc.name).strip()]
            if records:
                self._append_history(session_id, "assistant", response_content,
                                 tool_calls=records,
                                 reasoning_content=response.reasoning_content)
            else:
                self._append_history(session_id, "assistant", response_content,
                                 reasoning_content=response.reasoning_content)

            # 8.5 超出上限的调用，在这里（assistant 消息之后）补一条"未执行"的结果。
            #     不补的话模型看到"我发了 5 个、只回来 2 个"，要么以为干完了、
            #     要么怀疑工具坏了。顺序按原始调用顺序走，和 tool_calls 一一对应。
            executed = 0
            skipped_by_cap = 0

            # 9. 执行工具调用（执行前检查暂停/停止）
            for tool_call in tool_calls:
                if tools_cap > 0 and executed >= tools_cap:
                    self._append_history(
                        session_id, "tool",
                        "未执行：本轮工具调用数超过用户设置的上限（设置 → 插件 → Agent 大循环 → "
                        "一轮最多几个工具调用）。这一步没做，请在这一轮重新给出这个调用。",
                        tool_call_id=tool_call.id, tool_name=tool_call.name)
                    skipped_by_cap += 1
                    continue
                try:
                    self.control.check_control(session_id)
                except AgentStoppedException:
                    stop_msg = "⏹ 任务已手动停止（共执行 " + str(round_no) + " 轮工具调用）。"
                    self._record(session_id, "SYSTEM_ERROR", {"error": "手动停止"}, "任务已手动停止")
                    self._sound("ERROR")
                    self._append_history(session_id, "assistant", stop_msg)
                    return stop_msg
                if tool_call.name is not None and str(tool_call.name).strip():
                    # 【用户要求】这里原来会"重复调用就终止任务""连续失败就跳过不执行"，
                    # 还会往对话里插【系统提示】。现在这些都没有了：
                    # 要不要继续试由模型判断，停不停由用户按界面上的 ⏹ 决定。
                    self.tool_guard.before_call(session_id, tool_call.name,
                                                self.args_fingerprint(tool_call.arguments))
                    outcome = self.execute_tool(session_id, tool_call, mode)
                    self.tool_guard.after_call(session_id, tool_call.name, outcome.success)
                    executed += 1

            # 10. 更新消息列表，继续下一轮
            messages = self.build_messages(session_id, mode, user_message)

    # ------------------------------------------------------------------
    # 主入口：流式
    # ------------------------------------------------------------------
    def process_message_stream(self, session_id: str, user_message: str, mode: str,
                               thinking_level: str | None = None,
                               model: str | None = None) -> Iterator[AgentChunk]:
        """流式处理用户消息（返回生成器，支持前端实时展示）。

        Java 侧是 `Flux.create` + 递归 `processStreamRound`；Python 侧用生成器 +
        while 循环表达同一套流程（轮次、纠正预算、工具上限、暂停/停止检查一一对应）。
        若 llm 层只实现了 `chat()` 没实现 `chat_stream()`，第一轮会退化成
        "整段拿到再一次发出"（内容不丢，只是不逐字）。
        """
        mode = AgentMode.normalize(mode)
        thinking_level = ThinkingLevel__agent_control.from_name(thinking_level)

        self._record(session_id, "USER_MESSAGE", {"content": user_message}, "用户消息")
        self._append_history(session_id, "user", user_message)
        self.control.reset(session_id)
        self.tool_guard.reset(session_id)
        with self._lock:
            self.round_cap_by_session.pop(session_id, None)

        messages: list[Any] = self.build_messages(session_id, mode, user_message)
        native_tools = self.use_native_tools()
        tool_definitions = self.build_tool_definitions(mode, session_id) if native_tools else []

        round_no = 1
        repair_round = 0
        while True:
            # 控制检查：暂停时阻塞等待，停止时中止流
            try:
                self.control.check_control(session_id)
            except AgentStoppedException:
                self._sound("ERROR")
                yield AgentChunk.error("⏹ 任务已手动停止")
                return

            max_rounds = self._loop_int(session_id, "maxIterations", 0)
            if max_rounds > 0 and round_no > max_rounds:
                cap_msg = ("⏹ 已达到本轮最大工具调用轮数（" + str(max_rounds)
                           + "，可在 设置 → 插件 → Agent 大循环 里调整）。")
                self._record(session_id, "SYSTEM_ERROR",
                             {"error": "轮次上限", "rounds": round_no - 1}, cap_msg)
                self._sound("ERROR")
                self._append_history(session_id, "assistant", cap_msg)
                yield AgentChunk.done(cap_msg)
                return

            # 每一轮流式调用前都过一遍预算（工具结果会把历史撑大，这正是最容易超窗的时刻）
            messages = self.maybe_compress_context(session_id, messages, model)

            content_parts: list[str] = []
            reasoning_parts: list[str] = []
            accumulators: dict[int, _ToolCallAccumulator] = {}
            last_finish: list[str | None] = [None]
            stream_error: list[BaseException] = []

            try:
                for chunk in self._chat_stream(messages, model, thinking_level, tool_definitions,
                                               self.max_tokens_per_round(session_id)):
                    delta_text = _chunk_delta_text(chunk)
                    if delta_text:
                        content_parts.append(delta_text)
                        yield AgentChunk.text(delta_text)
                    rc = _chunk_reasoning(chunk)
                    if rc:
                        reasoning_parts.append(rc)
                    fr = _chunk_finish_reason(chunk)
                    if fr is not None:
                        last_finish[0] = fr
                    for d in _chunk_tool_call_deltas(chunk):
                        acc = accumulators.setdefault(int(d.get("index", 0)), _ToolCallAccumulator())
                        if d.get("id"):
                            acc.id = str(d["id"])
                        if d.get("name"):
                            acc.name_builder.append(str(d["name"]))
                        if d.get("arguments"):
                            acc.args_builder.append(str(d["arguments"]))
            except Exception as e:      # 流式调用失败
                self._record(session_id, "SYSTEM_ERROR", {"error": str(e)},
                             "流式调用失败: " + str(e))
                self._sound("ERROR")
                yield AgentChunk.error("模型调用失败: " + str(e))
                return

            if stream_error:
                self._sound("ERROR")
                yield AgentChunk.error("模型调用失败: " + str(stream_error[0]))
                return

            full_content = "".join(content_parts)
            reasoning = "".join(reasoning_parts) or None

            # 撞到长度上限：下一轮上限翻倍（写大文件本来就需要更多 token）
            if last_finish[0] and "length" in last_finish[0].lower():
                self.bump_round_cap(session_id)

            tool_calls = self.build_tool_calls_from_accumulators(accumulators)
            if not tool_calls:
                tool_calls = self.parse_tool_calls_from_text(full_content)
                if tool_calls:
                    full_content = self.remove_tool_call_blocks(full_content)

            if not tool_calls:
                # 【两条链路必须一致】第 2 轮以后同样要判「残缺工具调用 / 整轮空响应」。
                # 以前只有第一轮做纠正，后续轮次在这里**直接把空回答当最终答案**结束任务 ——
                # 用户收到一句空白。repair_round 是整条用户消息共用的一份预算。
                malformed = bool(accumulators)
                if repair_round < MAX_CALL_REPAIR and (malformed or not full_content.strip()):
                    next_repair = repair_round + 1
                    self._record(session_id, "TOOL_CALL_ERROR",
                                 {"malformed": malformed, "repair": next_repair},
                                 "残缺工具调用，已纠正重试" if malformed else "空响应，已纠正重试")
                    self._append_history(session_id, "user", self.repair_hint(malformed))
                    yield AgentChunk.text("\n\n⚠ 上次的工具调用不完整，正在重试…\n\n" if malformed
                                          else "\n\n⚠ 上次没有返回内容，正在重试…\n\n")
                    messages = self.build_messages(session_id, mode, user_message)
                    repair_round = next_repair
                    continue        # 重试同一轮，只把纠正预算往后推一格

                # 没有工具调用，流结束
                self._append_history(session_id, "assistant", full_content,
                                     reasoning_content=reasoning)
                self._sound("DONE")
                yield AgentChunk.done(full_content)
                return

            # 有工具调用：保存助手消息，执行工具，然后继续下一轮
            records = [ToolCallRecord__agent_loop(tc.id, tc.name, tc.arguments)
                       for tc in tool_calls if tc.name is not None and str(tc.name).strip()]
            if records:
                self._append_history(session_id, "assistant", full_content,
                                     tool_calls=records, reasoning_content=reasoning)
            else:
                self._append_history(session_id, "assistant", full_content,
                                     reasoning_content=reasoning)

            tools_cap = self._loop_int(session_id, "maxToolsPerRound", 0)
            executed = 0
            for tool_call in tool_calls:
                if tools_cap > 0 and executed >= tools_cap:
                    # 超限的按原始顺序补一条"未执行"，否则 tool_calls 与 tool 结果数量对不上
                    self._append_history(
                        session_id, "tool",
                        "未执行：本轮工具调用数超过用户设置的上限（设置 → 插件 → Agent 大循环 → "
                        "一轮最多几个工具调用）。这一步没做，请在这一轮重新给出这个调用。",
                        tool_call_id=tool_call.id, tool_name=tool_call.name)
                    continue
                try:
                    self.control.check_control(session_id)
                except AgentStoppedException:
                    self._sound("ERROR")
                    yield AgentChunk.error("⏹ 任务已手动停止")
                    return
                if tool_call.name is not None and str(tool_call.name).strip():
                    self.tool_guard.before_call(session_id, tool_call.name,
                                                self.args_fingerprint(tool_call.arguments))
                    outcome = self.execute_tool(session_id, tool_call, mode)
                    self.tool_guard.after_call(session_id, tool_call.name, outcome.success)
                    executed += 1
                    yield AgentChunk.tool_call(tool_call.name, "执行完成")

            messages = self.build_messages(session_id, mode, user_message)
            round_no += 1

    # ------------------------------------------------------------------
    # 工具执行
    # ------------------------------------------------------------------
    def execute_tool(self, session_id: str, tool_call: ToolCall__agent_loop, mode: str) -> _ToolOutcome:
        """执行一次工具调用。

        :return: `_ToolOutcome`（`bool(...)` 就是 Java 那个 boolean：True = 工具真的跑成功了；
                 False = 没找到工具 / 模式或权限不允许 / 执行失败）。
                 返回值喂给 `ToolCallGuard`，用来发现"某个工具在连续失败还硬试"。
        """
        tool_name = tool_call.name

        # 记录工具调用开始
        self._record(session_id, "TOOL_CALL_START",
                     {"toolName": tool_name, "arguments": tool_call.arguments},
                     "工具调用开始: " + str(tool_name))

        # 查找工具插件（用循环而不是推导式：下面 tool_name 会被归一化改名）
        found: ToolPlugin | None = None
        for t in self.registry.all():
            if t.name == tool_name or t.id == tool_name:
                found = t
                break

        # 找不到就试一次"工具名归一化"：量化模型很爱写 ls / cat / bash 这类通用叫法，
        # 直接判"未找到工具"等于白烧一轮推理（本机一轮十几秒）。
        # 只有精确查找失败时才归一化，绝不会把已经正确的调用改坏；拿不准就照旧报错。
        if found is None:
            known = [t.name for t in self.registry.all()
                     if getattr(t, "name", None) and str(t.name).strip()
                     and self._available_in_mode(t, mode)]
            canonical = name_aliases.resolve(tool_name, known)
            if canonical is not None:
                for t in self.registry.all():
                    if t.name == canonical:
                        found = t
                        break
                if found is not None:
                    tool_name = canonical

        if found is None:
            # 模型偶尔会发明工具名（实测它调用过 delete_directory_placeholder —— 没有这个工具）。
            # 只回一句"未找到工具"它下一轮还会试别的；带上最接近的现有工具，它基本能一次改对。
            error = "未找到工具: " + str(tool_name) + self.suggest_tool_names(tool_name, mode)
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name, "error": error}, error)
            self._reply_tool(session_id, tool_call.id, tool_name, "错误: " + error)
            return _ToolOutcome(False, "错误: " + error)

        tool = found

        # 检查模式权限
        if not self._available_in_mode(tool, mode):
            error = "工具 " + str(tool_name) + " 在 " + str(AgentMode.normalize(mode)) + " 模式下不可用"
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name, "error": error}, error)
            self._reply_tool(session_id, tool_call.id, tool_name, "错误: " + error)
            return _ToolOutcome(False, "错误: " + error)

        # 审批策略检查：禁止/需确认的工具直接拒绝并反馈给模型
        approval = self.approval_policy.check_approval(tool.id)
        if approval.action in (ApprovalAction.BLOCK, ApprovalAction.CONFIRM):
            error = approval.reason if approval.reason is not None \
                else "工具 " + str(tool_name) + " 需要用户确认后才能执行"
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name, "error": error, "approval": approval.action},
                         "审批拦截: " + str(tool_name))
            self._sound("APPROVAL")     # 需要审批：提醒音
            self._reply_tool(session_id, tool_call.id, tool_name, "错误: " + error)
            return _ToolOutcome(False, "错误: " + error)

        # 权限检查：工具所需权限不得高于会话工作区的授予权限
        if not self.check_permission(session_id, tool):
            error = ("工具 " + str(tool_name) + " 需要更高权限（当前工作区权限等级不足，"
                     + "可在工作区设置中提升权限）")
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name, "error": error}, error)
            self._reply_tool(session_id, tool_call.id, tool_name, "错误: " + error)
            return _ToolOutcome(False, "错误: " + error)

        # 自动授权审查：用**另一个模型**审这次危险调用，DENY 就拦下来。
        #
        # 【为什么放在这里】要在"真正执行工具之前"，但要排在本地审批策略与权限检查之后 ——
        # 那两道是"用户自己定的规矩"，不该为了省一次模型调用而跳过。
        # 插件（`plugins/review.py` 的 ApprovalReviewPlugin）的 `check()` 文档写明了这段语义：
        #   · needs_review=True → 用 decision 里的 provider/model 建一次对话、
        #     发 build_review_prompt()、用 parse_verdict() 解析；
        #   · DENY **不要抛异常中断整个任务**，把 deny_message() 当成工具结果回给模型 ——
        #     模型知道"这一步被拦了、原因是这个"，还能换个安全做法继续。
        # 这个插件以前**注册了但从来没人调**：界面上开关是开的、日志里也显示已加载，
        # 可实际上 DENY 完全不生效（`_check_plugin_extras.py` 抓到的）。
        review_denial = self._approval_review(session_id, tool_name, tool_call.arguments)
        if review_denial is not None:
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name, "error": review_denial, "approval": "REVIEW_DENY"},
                         "授权审查拦截: " + str(tool_name))
            self._reply_tool(session_id, tool_call.id, tool_name, "错误: " + review_denial)
            return _ToolOutcome(False, "错误: " + review_denial)

        # 执行工具（设置上下文：相对路径基于绑定的工作区解析；
        # 会话 ID 也一起放进去——ask_user 这类工具需要知道自己在哪个会话里）
        ws_path = self.resolve_workspace(session_id)
        WorkspaceContext.set(ws_path)
        SessionContext__agent_loop.set(session_id)
        try:
            # 【派发前先把参数类型转对】文本通道（本地模式默认）下所有参数都是字符串，
            # 而工具里写的是 ((Number) args.get("lines")).intValue() → ClassCastException，
            # 实测 glob_files / head_tail_file / directory_tree / modify_file 全中招。
            #
            # 并且**必须带超时**：工具自己卡住时（等网络/凭据/输入）不能再拖住整条任务。
            args = self.coerce_arguments(tool, tool_call.arguments)
            result = self.run_tool_with_timeout(tool, args, str(tool_name), session_id)

            if result.success:
                self._record(session_id, "TOOL_CALL_COMPLETE",
                             {"toolName": tool_name, "result": _truncate(result.content, 500)},
                             "工具调用成功: " + str(tool_name))
                self._reply_tool(session_id, tool_call.id, tool_name, result.content)
                return _ToolOutcome(True, result.content)
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name, "error": result.error},
                         "工具调用失败: " + str(tool_name))
            self._reply_tool(session_id, tool_call.id, tool_name,
                             "工具执行错误: " + str(result.error))
            return _ToolOutcome(False, "工具执行错误: " + str(result.error))
        except Exception as e:
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name, "error": str(e)},
                         "工具执行异常: " + str(e))
            self._reply_tool(session_id, tool_call.id, tool_name,
                             "工具执行异常: " + str(e))
            return _ToolOutcome(False, "工具执行异常: " + str(e))
        finally:
            WorkspaceContext.clear()
            SessionContext__agent_loop.clear()

    @staticmethod
    def _available_in_mode(tool: ToolPlugin, mode: str) -> bool:
        """Java `tool.isAvailableInMode(mode)`：极简模式只放行 minimal_mode 的工具。"""
        if AgentMode.normalize(mode) == AgentMode.MINIMAL:
            return bool(getattr(tool, "minimal_mode", False))
        return True

    def _reply_tool(self, session_id: str, tool_call_id: str | None, tool_name: str | None,
                    content: str) -> None:
        self._append_history(session_id, "tool", content,
                             tool_call_id=tool_call_id, tool_name=tool_name)

    def check_permission(self, session_id: str, tool: ToolPlugin) -> bool:
        """权限检查：工具所需权限等级 vs 会话绑定工作区的授予权限。

        READ_ONLY 工作区只能执行只读工具；WORKSPACE_WRITE 可执行只读 + 工作区写工具
        （不可执行 FULL_ACCESS 工具）；FULL_ACCESS 全部放行。未绑定工作区时不限制（保持兼容）。

        授予权限由 `permission_resolver(session_id)` 提供（工作区管理由 `context/` 负责）；
        没传就按 Java 的"未绑定工作区 → 不限"处理。
        """
        if self._permission_resolver is None:
            return True
        try:
            granted = self._permission_resolver(session_id)
        except Exception:
            return True
        if not granted:
            return True
        required = getattr(tool, "permission", PermissionLevel.READ_ONLY)
        g = str(granted).strip().upper()
        if g == "READ_ONLY":
            return required == PermissionLevel.READ_ONLY
        if g == "WORKSPACE_WRITE":
            return required != "FULL_ACCESS"
        if g == "FULL_ACCESS":
            return True
        return True

    def run_tool_with_timeout(self, tool: ToolPlugin, args: dict[str, Any],
                              tool_name: str, session_id: str) -> ToolResult:
        """带超时执行工具。

        执行放到单独线程，并**在该线程里重新设置上下文**（WorkspaceContext /
        SessionContext 是线程局部，不设的话相对路径解析会失效）。

        实测教训：`git_remote show origin` 会去连远端，git 在等凭据时**永远不关 stdout**，
        而工具里是 `readAllBytes()` 写在 `waitFor(30s)` **前面** —— 于是那个 30 秒超时
        形同虚设，整条消息卡了 3 分多钟，用户只能手动点停止。这里在**派发层**兜一道。
        """
        ws_path = self.resolve_workspace(session_id)
        timeout = self.timeout_for(session_id)
        ex = ThreadPoolExecutor(max_workers=1, thread_name_prefix="tool-" + tool_name)
        try:
            future = ex.submit(self._invoke_tool, tool, args, ws_path, session_id)
            return future.result(timeout=timeout)
        except FutureTimeout:
            # 【告诉工具"这次被放弃了"】Python 线程杀不掉，`cancel_futures` 只取消排队中的
            # 任务 —— 正在跑的 `Start-Sleep -Seconds 300` 会**一直占着常驻终端**，
            # 于是下一条 `execute_command` 也超时，用户看到"卡住的命令把终端堵死了"。
            # Java 侧靠 `PersistentShell` 自己的超时重启；这里在派发层补一个钩子：
            # 工具若实现了 `on_abandoned()` 就调它（终端工具会借此自杀重启）。
            try:
                hook = getattr(tool, "on_abandoned", None)
                if callable(hook):
                    hook()
            except Exception:                     # noqa: BLE001 清理失败不能改变"超时"这个结论
                pass
            self._record(session_id, "TOOL_CALL_ERROR",
                         {"toolName": tool_name,
                          "error": "工具执行超时（超过 " + str(timeout) + " 秒还没返回）"},
                         "工具执行超时: " + tool_name)
            return ToolResult.fail(
                "工具执行超时（超过 " + str(timeout) + " 秒还没返回）: " + tool_name
                + "。多半是在等网络、凭据或用户输入。请换个参数重试，或用别的等价工具完成这件事。")
        except Exception as e:
            return ToolResult.fail("工具执行异常: " + str(e))
        finally:
            self._record_tool_timeout_cleanup(ex)

    def _approval_review(self, session_id: str, tool_name: str | None,
                         arguments: dict[str, Any] | None) -> str | None:
        """自动授权审查：返回**拦截原因**（非 None = 拒绝执行这次工具调用）。

        【为什么单独一个方法】审查是"用另一次模型对话判断这次调用危不危险"，
        逻辑上独立于工具执行；失败一律**放行**（Java 的语义：审查不可用不能把应用变砖）。
        """
        try:
            from lionbox.plugins.lifecycle import default_registry
            for plugin in default_registry().get_by_kind("APPROVAL_REVIEW"):
                plugin_id = str(getattr(plugin, "id", "") or "")
                if plugin_id == "plugin.change-review":
                    continue        # 改动审核是另一个插件（写文件时才拦），不是这里的事
                check = getattr(plugin, "check", None)
                if not callable(check):
                    continue
                decision = check(session_id, tool_name, arguments)
                if not getattr(decision, "needs_review", False):
                    continue
                prompt = plugin.build_review_prompt(tool_name, arguments)
                reply = self._review_model_call(decision, prompt)
                verdict = plugin.parse_verdict(reply)
                if verdict is None or getattr(verdict, "allow", True):
                    continue        # 允许，或解析不出结论 → 放行
                reason = str(getattr(verdict, "reason", "") or "审查模型给出了 DENY")
                try:
                    return str(plugin.deny_message(tool_name, reason))
                except Exception:                     # noqa: BLE001
                    return (f"这次调用被自动授权审查拦下了（工具：{tool_name}）。\n"
                            f"审查意见：{reason}\n")
        except Exception:                             # noqa: BLE001 审查层任何异常都放行
            return None
        return None

    def _review_model_call(self, decision: Any, prompt: str) -> str | None:
        """为审查跑一次模型对话（用 decision 指定的 provider/model）。"""
        try:
            # 【必须带这条 system】Java `AgentLoop` 里审查调用是**两条消息**：
            #     ChatMessage.system("你是工具调用安全审核员，只回答 ALLOW 或 DENY，并给一句理由。")
            #   + 插件 `build_review_prompt()` 的结果作为 user 内容。
            # 少发这条 system 会有两个后果：① 审查模型没有"只回一行"的约束，
            # 回一段散文 → `parse_verdict` 认不出来 → 一律放行（DENY 形同虚设）；
            # ② 回归套件的假模型正是按这条 system 文案识别"这次是审查调用"的，
            # 认不出就走到别的分支去了（`_check_plugin_extras` 的 DENY 用例）。
            messages = [
                ChatMessage__agent_loop("system", "你是工具调用安全审核员，只回答 ALLOW 或 DENY，并给一句理由。"),
                ChatMessage__agent_loop("user", prompt),
            ]
            model = getattr(decision, "model", None) or None
            try:
                resp = self._chat(messages, model, "LOW", [], 512)
            except Exception:                         # noqa: BLE001
                # 审查指定了一个解析不到的模型名（用户填错、或那个 provider 没配）
                # 时退回主模型 —— 审查是额外的安全网，不该因为模型名写错就整体失效。
                if model is None:
                    raise
                resp = self._chat(messages, None, "LOW", [], 512)
            content = getattr(resp, "content", None)
            if content is None and isinstance(resp, dict):
                content = (resp.get("message") or {}).get("content") or resp.get("content")
            return None if content is None else str(content)
        except Exception:                             # noqa: BLE001 叫不动模型就放行
            return None

    @staticmethod
    def _invoke_tool(tool: ToolPlugin, args: dict[str, Any], ws_path: str | None,
                     session_id: str) -> ToolResult:
        if ws_path is not None:
            WorkspaceContext.set(ws_path)
        SessionContext__agent_loop.set(session_id)
        try:
            result = tool.execute(args)
            if isinstance(result, ToolResult):
                return result
            # 工具没按契约返回 ToolResult（例如返回了字符串）：不吞异常，明确报错
            return ToolResult.fail(f"工具 {tool.name} 没有返回 ToolResult（得到 {type(result).__name__}）")
        finally:
            WorkspaceContext.clear()
            SessionContext__agent_loop.clear()

    @staticmethod
    def _record_tool_timeout_cleanup(ex: ThreadPoolExecutor) -> None:
        # Java 侧是 ex.shutdownNow()：超时后不再让那个线程拖住进程
        try:
            ex.shutdown(wait=False, cancel_futures=True)
        except TypeError:      # 3.8 兼容（本工程是 3.14，只是为了稳）
            ex.shutdown(wait=False)

    def timeout_for(self, session_id: str) -> int:
        """本次派发实际用的工具超时：先问插件 SPI，插件没给就用配置里的值。

        做成方法而不是字段，是因为插件可以在运行时改设置 —— 缓存成字段的话，
        用户改完得重启才生效。
        """
        t = self._loop_int(session_id, "toolTimeoutSeconds", self.tool_timeout_seconds)
        return t if t > 0 else self.tool_timeout_seconds

    # ------------------------------------------------------------------
    # 工具名 / 参数修复
    # ------------------------------------------------------------------
    def suggest_tool_names(self, wrong: str | None, mode: str) -> str:
        """工具名写错时，挑几个最接近的现有工具名当提示（实测能省掉一整轮白跑）。

        用户日志里模型调过 `delete_directory_placeholder`（并不存在），只回"未找到工具"
        它会换个猜法继续试；带上候选它基本一次就改对。
        """
        if not wrong or not str(wrong).strip():
            return ""
        w = str(wrong).lower().replace("_", " ").strip()
        parts = [p for p in w.split() if p]
        scored: list[tuple[int, str]] = []
        for t in self.registry.for_mode(mode):
            name = (getattr(t, "name", "") or "").lower()
            if not name.strip():
                continue
            score = 0
            for p in parts:
                if len(p) >= 3 and p in name:
                    score += 2
            flat = name.replace("_", " ")
            if flat in w or w in flat:
                score += 3
            if score > 0:
                scored.append((score, t.name))
        if not scored:
            return "。可用工具见系统提示词里的清单（不要自己造工具名）"
        scored.sort(key=lambda kv: -kv[0])
        top = [name for _, name in scored[:3]]
        return "。你是不是想用这些之一：" + "、".join(top) + "（别自己造工具名）"

    def coerce_arguments(self, tool: ToolPlugin, arguments: dict[str, Any] | None
                         ) -> dict[str, Any] | None:
        """按工具自己声明的 JSON Schema，把参数值转成正确的类型。

        【为什么非要在这里做】模型给的是"文本"：文本通道（本地模式默认）下
        `<parameter=lines>5</parameter>` 解析出来是字符串 "5"，原生通道也可能给 `"5"`。
        而工具里的写法是 `((Number) arguments.get("lines")).intValue()` —— 直接
        `class java.lang.String cannot be cast to class java.lang.Number`。
        实测（用户装 1.1.8 后跑"把工具都调一遍"）：
          glob_files     ❌ 匹配失败: class java.lang.String cannot be cast to class java.lang.Number
          head_tail_file ❌ 读取失败: 同上
          directory_tree ❌ 生成目录树失败: 同上
        12 个工具文件都这么取参数（modify_file 的 startLine/endLine 同理）。

        只按 schema 里声明的类型转，不瞎猜：integer→int、number→float、
        boolean→bool、array/object→先当 JSON 解析、string→数字也转成字符串。
        转不了就原样留着，让工具自己报错，这里不抛异常。
        """
        if not arguments or tool is None:
            return arguments
        definition = tool.function_definition()
        # 【注意嵌套层】与 tool_signature 同理：function_definition() 给的是
        # {"type":"function","function":{"name":…,"parameters":{…}}}，
        # 参数 schema 在 function 里面。少了这一层，类型转换和参数名归一化**全都不会发生**
        # （实测表现：`<parameter=lines>5</parameter>` 到工具里还是字符串 "5"，
        #  工具里 ((Number) args.get("lines")) 直接 ClassCastException）。
        fn = definition.get("function") if isinstance(definition, dict) else None
        params = fn.get("parameters") if isinstance(fn, dict) else None
        if not isinstance(params, dict):
            return arguments
        props = params.get("properties")
        if not isinstance(props, dict):
            return arguments
        out = dict(arguments)

        # 0) 先把"键名写歪了"的参数改名到工具声明的名字上（file_path→path、max_depth→maxDepth、
        #    大小写不一致…）。只改键名、不动值，而且多个候选就放弃，所以不会有副作用。
        #    这一步在类型转换之前做，否则歪掉的键压根进不了下面的转换循环。
        for key in props.keys():
            key = str(key)
            if key in out:
                continue
            matched = arg_aliases.match_key(key, list(out.keys()))
            if matched is not None and out.get(matched) is not None:
                out[key] = out[matched]

        for key, prop in props.items():
            key = str(key)
            if key not in out or not isinstance(prop, dict):
                continue
            declared_type = "" if prop.get("type") is None else str(prop.get("type"))
            value = out.get(key)
            try:
                if isinstance(value, str):
                    t = value.strip()
                    # 模型偶尔把值连引号一起写进来：\"5\" / "5"
                    if len(t) > 1 and t.startswith('"') and t.endswith('"'):
                        t = t[1:-1]
                    if declared_type == "integer":
                        out[key] = int(t)
                    elif declared_type == "number":
                        out[key] = float(t)
                    elif declared_type == "boolean":
                        out[key] = t.lower() == "true" or t == "1"
                    elif declared_type in ("array", "object"):
                        if t.startswith("[") or t.startswith("{"):
                            out[key] = json.loads(t)
                    # 其余（string）：原样
                elif isinstance(value, (int, float)) and not isinstance(value, bool) \
                        and declared_type == "string":
                    out[key] = _num_to_str(value)
            except Exception:
                pass    # 转不了就原样传给工具，让它自己报错
        return out

    @staticmethod
    def args_fingerprint(arguments: dict[str, Any] | None) -> str:
        """参数指纹：用来判断"是不是一模一样的调用"（喂给 ToolCallGuard）。"""
        if not arguments:
            return "{}"
        try:
            return json.dumps({k: arguments[k] for k in sorted(arguments.keys(), key=str)},
                              ensure_ascii=False, default=str)
        except Exception:
            return str(arguments)

    # ------------------------------------------------------------------
    # 消息构建
    # ------------------------------------------------------------------
    def resolve_workspace(self, session_id: str | None) -> str | None:
        """会话绑定的工作区路径（会话 → 工作区映射由 `context/` 负责）。"""
        if self._workspace_resolver is not None and session_id is not None:
            try:
                got = self._workspace_resolver(session_id)
                if got:
                    return str(got)
            except Exception:
                pass
        return self.workspace

    def build_messages(self, session_id: str, mode: str, user_message: str) -> list[ChatMessage__agent_loop]:
        """构建模型消息列表。"""
        messages: list[ChatMessage__agent_loop] = []
        workspace_path = self.resolve_workspace(session_id)

        # 系统提示词（含模式专属提示词与适用技能的能力提示词）
        system_prompt = self.build_system_prompt(mode, workspace_path, user_message,
                                                 self.use_native_tools(), session_id)
        messages.append(ChatMessage__agent_loop.system(system_prompt))

        # 对话历史
        for msg in self._history_items(session_id):
            role = getattr(msg, "role", None)
            content = getattr(msg, "content", "") or ""
            if role == "user":
                messages.append(ChatMessage__agent_loop.user(content))
            elif role == "assistant":
                tcs = getattr(msg, "tool_calls", None) or []
                valid = [ToolCall__agent_loop(getattr(tc, "id", "") or "", getattr(tc, "name", "") or "",
                                  getattr(tc, "arguments", None))
                         for tc in tcs
                         if getattr(tc, "name", None) and str(tc.name).strip()]
                reasoning = getattr(msg, "reasoning_content", None)
                if valid:
                    messages.append(ChatMessage__agent_loop.assistant_with_tool_calls(content, valid, reasoning))
                else:
                    messages.append(ChatMessage__agent_loop.assistant(content, reasoning))
            elif role == "system":
                # 【必须只在最前面】Qwen 的 Jinja 模板（llama-server 现在默认启用 --jinja）
                # 对夹在中间的 system 消息直接 raise_exception('System message must be at
                # the beginning')，服务端 500，用户看到的是"模型调用失败"。
                # 老会话文件里可能已经存了这种消息，所以这里做一道兜底：
                # 非首条的 system → 降级成 user（带【系统提示】前缀，语义不变）。
                if not messages:
                    messages.append(ChatMessage__agent_loop.system(content))
                else:
                    messages.append(ChatMessage__agent_loop.user("【系统提示】" + content))
            elif role == "tool":
                messages.append(ChatMessage__agent_loop.tool_result(getattr(msg, "tool_call_id", None), content))
        return messages

    # ------------------------------------------------------------------
    # 会话历史
    # ------------------------------------------------------------------
    def _append_history(self, session_id: str, role: str, content: str, *,
                        tool_calls: list[Any] | None = None,
                        tool_call_id: str | None = None,
                        tool_name: str | None = None,
                        reasoning_content: str | None = None) -> None:
        """往会话历史追加一条消息（形状适配 `lionbox/sessions/` 与内存桩）。"""
        if self._history_takes_object:
            self.history.add_message(_make_history_message(
                session_id, role, content, tool_calls=tool_calls,
                tool_call_id=tool_call_id, tool_name=tool_name,
                reasoning_content=reasoning_content))
        else:
            self.history.add_message(session_id, role, content, tool_calls=tool_calls,
                                     tool_call_id=tool_call_id, tool_name=tool_name,
                                     reasoning_content=reasoning_content)

    def _append_tool_result(self, session_id: str, tool_call_id: str | None,
                            tool_name: str | None, content: str) -> None:
        self._append_history(session_id, "tool", content,
                             tool_call_id=tool_call_id, tool_name=tool_name)

    def _history_items(self, session_id: str) -> list[Any]:
        getter = getattr(self.history, "get_history", None)
        if getter is None:
            return []
        try:
            return list(getter(session_id) or [])
        except Exception:
            return []

    # ------------------------------------------------------------------
    # 模型调用
    # ------------------------------------------------------------------
    def _chat(self, messages: list[ChatMessage__agent_loop], model: str | None, thinking_level: str,
              tool_definitions: list[dict[str, Any]], max_tokens: int | None) -> ModelResponse__agent_loop:
        if self.client is None:
            raise RuntimeError("没有配置 ChatClient（模型调用层未接入）")
        tools_arg = tool_definitions if tool_definitions else None
        adapter = self._active_adapter()
        # ---- 路线 1：直接接 `lionbox/llm/` 的 ModelAdapter ----
        # Java 的 AgentLoop 调的就是 adapter.chatWithOptions(...)（带 max_tokens）；
        # Python 侧对应 chat_with_options，默认实现会退回 chat（忽略 max_tokens，与 Java 同）。
        if adapter is not None and self.client is adapter:
            with_opts = getattr(adapter, "chat_with_options", None)
            if with_opts is not None:
                try:
                    from lionbox.llm.types import ThinkingLevel__agent_control as _LLMThinkingLevel
                    level = _LLMThinkingLevel.parse(thinking_level)
                except Exception:
                    level = thinking_level
                return _normalize_response(with_opts(list(messages), model or "", level,
                                                     tools_arg, None, max_tokens))
            return _normalize_response(adapter.chat(list(messages), model or "", None, tools_arg))
        # ---- 路线 2：自定义 ChatClient（见模块顶部 docstring 的窄接口）----
        tools_for_client = tools_arg
        try:
            raw = self.client.chat(messages, tools=tools_for_client, model=model,
                                   thinking_level=thinking_level, max_tokens=max_tokens)
        except TypeError:
            # 只兜"对方签名更窄（只认 messages/tools/model）"这一种情况；
            # 第二次再 TypeError 就照原样抛出去，不吞 —— 吞了会把 llm 层的 bug 藏成"模型没反应"。
            raw = self.client.chat(messages, tools=tools_for_client, model=model)
        return _normalize_response(raw)

    def _chat_stream(self, messages: list[ChatMessage__agent_loop], model: str | None, thinking_level: str,
                     tool_definitions: list[dict[str, Any]],
                     max_tokens: int | None) -> Iterator[Any]:
        if self.client is None:
            raise RuntimeError("没有配置 ChatClient（模型调用层未接入）")
        tools_arg = tool_definitions if tool_definitions else None
        adapter = self._active_adapter()
        if adapter is not None and self.client is adapter:
            limited = getattr(adapter, "chat_stream_limited", None)
            if max_tokens is not None and limited is not None:
                it = limited(list(messages), model or "", None, tools_arg, max_tokens)
            else:
                it = adapter.chat_stream(list(messages), model or "", None, tools_arg)
            for chunk in it:
                yield chunk
            return
        stream_fn = getattr(self.client, "chat_stream", None)
        if stream_fn is None:
            # llm 层只有 chat()：退化成"一次拿完整段再切片发出"（内容不丢，只是不逐字）
            resp = self._chat(messages, model, thinking_level, tool_definitions, max_tokens)
            if resp.content:
                yield {"delta": {"content": resp.content}}
            deltas = [{"index": i, "id": tc.id, "name": tc.name,
                       "arguments": json.dumps(tc.arguments, ensure_ascii=False)}
                      for i, tc in enumerate(resp.tool_calls)]
            if deltas:
                yield {"tool_call_deltas": deltas}
            if resp.finish_reason:
                yield {"finish_reason": resp.finish_reason}
            return
        try:
            it = stream_fn(messages, tools=tools_arg, model=model,
                           thinking_level=thinking_level, max_tokens=max_tokens)
        except TypeError:
            it = stream_fn(messages, tools=tools_arg, model=model)
        for chunk in it:
            yield chunk

    def build_tool_calls_from_accumulators(
            self, accumulators: dict[int, _ToolCallAccumulator]) -> list[ToolCall__agent_loop]:
        """从流式增量累积器构建完整的工具调用列表（按 index 排序）。"""
        tool_calls: list[ToolCall__agent_loop] = []
        for index in sorted(accumulators.keys()):
            acc = accumulators[index]
            name = "".join(acc.name_builder).strip()
            args_str = "".join(acc.args_builder).strip()
            if not name:
                continue
            arguments: dict[str, Any]
            if not args_str:
                arguments = {}
            else:
                try:
                    parsed = json.loads(args_str)
                    arguments = parsed if isinstance(parsed, dict) else {}
                except ValueError:
                    arguments = {}
            tool_calls.append(ToolCall__agent_loop(acc.id, name, arguments))
        return tool_calls

    # ------------------------------------------------------------------
    # 文本通道的工具调用解析（模板原生 → XML → JSON）
    # ------------------------------------------------------------------
    def parse_tool_calls_from_text(self, text: str | None) -> list[ToolCall__agent_loop]:
        """从文本中解析工具调用（Qwen 模板原生 / XML / JSON）。

        解析顺序**不能改**：模板原生必须排在最前面。
        【为什么】我们的权重是 Qwen 模板，模型最习惯的输出就是这个形式
        （llama-server 开 --jinja 时服务端本来会替我们解析成标准 tool_calls，我们没开）。
        实测漏了这条就直接失败：模型输出了完整的
        `<tool_call><function=execute_command><parameter=command>ls -la && pwd</parameter></function></tool_call>`，
        下面的 JSON 解析器却把这个文本拿去当 JSON 解析，报 "Unexpected character ('<')"，
        整轮工具调用作废 —— 模型白写一轮，用户看到的是"它说要调用工具，然后什么都没发生"。
        """
        tool_calls: list[ToolCall__agent_loop] = []
        if text is None or not text.strip():
            return tool_calls

        # 0. 最先试 Qwen 模板原生格式 <tool_call><function=名字><parameter=键>值</parameter>
        for parsed in parsing.parse(text):
            tool_calls.append(ToolCall__agent_loop(_new_call_id(), parsed.name, parsed.arguments))
        if tool_calls:
            return tool_calls

        # 1. 再尝试解析 XML 格式
        tool_calls = self.parse_xml_tool_calls(text)
        if tool_calls:
            return tool_calls

        # 2. 再尝试解析 JSON 格式
        return self.parse_json_tool_calls(text)

    def remove_tool_call_blocks(self, text: str | None) -> str:
        """从文本中移除工具调用块（XML / JSON / 模板原生三种外壳）。"""
        if text is None or not text.strip():
            return text if text is not None else ""
        result = re.sub(r"(?s)<tool_call>.*?</tool_call>", "", text).strip()
        result = parsing.strip_calls(result)
        result = re.sub(r"```(?:xml|json)\s*```", "", result).strip()
        return result

    def parse_xml_tool_calls(self, text: str | None) -> list[ToolCall__agent_loop]:
        """从文本中解析 XML 格式的工具调用。

        支持格式：
            <tool_call>
              <name>tool_name</name>
              <arguments>{"key": "value"}</arguments>
            </tool_call>
        """
        tool_calls: list[ToolCall__agent_loop] = []
        if text is None or not text.strip():
            return tool_calls

        for block_m in re.finditer(r"(?s)<tool_call>(.*?)</tool_call>", text):
            block = block_m.group(1).strip()
            name_m = re.search(r"<name>(.*?)</name>", block)
            if not name_m:
                continue
            name = name_m.group(1).strip()
            args_m = re.search(r"(?s)<arguments>(.*?)</arguments>", block)
            args_str = args_m.group(1).strip() if args_m else "{}"
            arguments = _parse_json_object(args_str)
            tool_calls.append(ToolCall__agent_loop(_new_call_id(), name, arguments))

        # 宽容兜底：模型漏写 <tool_call> 包裹，直接给 <name>..</name><arguments>{..}</arguments>。
        # 实测云端模型（MiMo）在文本模式下就会这么吐，不认的话整轮工具调用直接丢掉。
        # 这个模式在正常正文里几乎不可能出现，误判风险很低。
        if not tool_calls:
            loose = re.compile(
                r"(?s)<name>\s*([A-Za-z_][\w.\-]*)\s*</name>\s*"
                r"<arguments>\s*(\{.*?\}|\[.*?\])\s*</arguments>")
            for m in loose.finditer(text):
                name = m.group(1).strip()
                parsed = _parse_json_object(m.group(2).strip())
                tool_calls.append(ToolCall__agent_loop(_new_call_id(), name, parsed))
        return tool_calls

    def parse_json_tool_calls(self, text: str | None) -> list[ToolCall__agent_loop]:
        """从文本中解析 JSON 格式的工具调用（6 种写法，与 Java 一致）。"""
        tool_calls: list[ToolCall__agent_loop] = []
        if text is None or not text.strip():
            return tool_calls

        # 1. <tool_call>…</tool_call> 标签格式
        for m in re.finditer(r"(?s)<tool_call>(.*?)</tool_call>", text):
            tc = self.parse_single_json_tool_call(m.group(1).strip())
            if tc is not None:
                tool_calls.append(tc)
        if tool_calls:
            return tool_calls

        # 2. ```json … ``` 代码块中的 <tool_call></tool_call>
        for m in re.finditer(r"```json\s*(.*?)```", text, re.DOTALL):
            block_content = m.group(1).strip()
            if "<tool_call>" in block_content:
                for inner in re.finditer(r"(?s)<tool_call>(.*?)</tool_call>", block_content):
                    tc = self.parse_single_json_tool_call(inner.group(1).strip())
                    if tc is not None:
                        tool_calls.append(tc)
        if tool_calls:
            return tool_calls

        # 3. ```json … ``` 代码块中的直接 JSON 对象或数组
        for m in re.finditer(r"```json\s*(.*?)```", text, re.DOTALL):
            json_content = m.group(1).strip()
            if "<tool_call>" in json_content:
                continue
            tool_calls.extend(self.parse_json_content_to_tool_calls(json_content))
        if tool_calls:
            return tool_calls

        # 4. 裸 JSON（不在代码块中）：匹配独立的 JSON 对象
        bare = re.compile(r"(?s)(\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\})")
        for m in bare.finditer(text):
            start = m.start()
            before = text[:start]
            if "<tool_call>" in before and "</tool_call>" not in before:
                continue
            tc = self.parse_single_json_tool_call(m.group(1).strip())
            if tc is not None:
                tool_calls.append(tc)
        return tool_calls

    def parse_json_content_to_tool_calls(self, json_content: str | None) -> list[ToolCall__agent_loop]:
        """解析 JSON 内容为工具调用列表（支持单对象和数组）。"""
        tool_calls: list[ToolCall__agent_loop] = []
        if json_content is None or not json_content.strip():
            return tool_calls
        s = json_content.strip()
        if s.startswith("["):
            try:
                items = json.loads(s)
            except ValueError:
                return tool_calls
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        tc = self.parse_tool_call_from_map(item)
                        if tc is not None:
                            tool_calls.append(tc)
            return tool_calls
        if s.startswith("{"):
            tc = self.parse_single_json_tool_call(s)
            if tc is not None:
                tool_calls.append(tc)
        return tool_calls

    def parse_single_json_tool_call(self, json_content: str | None) -> ToolCall__agent_loop | None:
        if json_content is None or not json_content.strip():
            return None
        try:
            parsed = json.loads(json_content)
        except ValueError:
            return None
        if not isinstance(parsed, dict):
            return None
        return self.parse_tool_call_from_map(parsed)

    def parse_tool_call_from_map(self, tool_call_map: dict[str, Any] | None) -> ToolCall__agent_loop | None:
        """从 dict 解析工具调用。

        支持多种格式：
          · {"name": "tool_name", "arguments": {...}}
          · {"tool": "tool_name", "arguments": {...}}
          · {"function": "tool_name", "arguments": {...}}
          · {"function": {"name": "tool_name", "arguments": {...}}}          （嵌套格式）
          · {"type": "function", "function": {"name": ..., "arguments": "{...}"}}（OpenAI 格式）
        """
        if not isinstance(tool_call_map, dict):
            return None

        name: str | None = None
        arguments: dict[str, Any] = {}

        # 1. 直接 name 字段
        name_obj = tool_call_map.get("name")
        if isinstance(name_obj, str):
            name = name_obj

        # 2. 尝试 tool 字段
        if name is None or not name.strip():
            name_obj = tool_call_map.get("tool")
            if isinstance(name_obj, str):
                name = name_obj

        # 3. 尝试 function 字段（可能是字符串或嵌套对象）
        if name is None or not name.strip():
            func_obj = tool_call_map.get("function")
            if isinstance(func_obj, str):
                name = func_obj
            elif isinstance(func_obj, dict):
                nested_name = func_obj.get("name")
                if isinstance(nested_name, str):
                    name = nested_name
                nested_args = func_obj.get("arguments")
                if isinstance(nested_args, dict):
                    arguments = nested_args
                elif isinstance(nested_args, str):
                    arguments = _parse_json_object(nested_args)

        if name is None or not name.strip():
            return None

        # 解析顶层 arguments（如果嵌套格式没解析到）
        if not arguments:
            args_obj = tool_call_map.get("arguments")
            if isinstance(args_obj, dict):
                arguments = args_obj
            elif isinstance(args_obj, str):
                arguments = _parse_json_object(args_obj)

        return ToolCall__agent_loop(_new_call_id(), name.strip(), arguments)

    # ------------------------------------------------------------------
    # 上下文预算
    # ------------------------------------------------------------------
    def effective_context_limit(self, model: str | None, session_id: str | None) -> int:
        """本次实际生效的上下文预算（token）。

        顺序：**会话自己调过的窗口**（Agent 用 context_window 工具设的）→
        全局默认（`lionbox.agent.context-limit-tokens`，出厂 16K，为的是省预填充）→
        模型窗口的 75%。前两层都是 0 才走到第三层。
        """
        budgeted = self.context_budget.limit_for(session_id)
        if budgeted > 0:
            return budgeted
        if self.context_limit_tokens > 0:
            return self.context_limit_tokens

        # 模型窗口查询结果缓存：**按模型名分键**。
        # 【为什么必须分键】原来是一个全局缓存：第一次问到的窗口会被永久复用，
        # 之后用户在下拉框换模型也不重查 —— 从大窗口模型换到小窗口云模型时，
        # 预算仍按旧模型算，于是不压缩、直接超窗 400，而且每条消息都失败。
        cache_key = model if (model and model.strip()) else "(default)"
        cached = self.model_context_cache.get(cache_key)
        if cached is not None and cached > 0:
            ctx = cached
        else:
            looked = 0
            try:
                adapter = self._active_adapter()
                getter = getattr(adapter, "get_available_models", None) if adapter else None
                if getter is not None:
                    for info in getter() or []:
                        max_ctx = _info_get(info, "maxContextTokens", "max_context_tokens")
                        if max_ctx:
                            if not model or not str(model).strip() \
                                    or str(model) == str(_info_get(info, "id", "id") or "") \
                                    or str(model) == str(_info_get(info, "name", "name") or ""):
                                looked = int(max_ctx)
                                break
            except Exception:
                looked = 0
            # 只有真查到了才缓存；查不到就用兜底但**不写缓存**，下次换模型/适配器就绪后还能查到
            if looked > 0:
                self.model_context_cache[cache_key] = looked
                ctx = looked
            else:
                ctx = FALLBACK_CONTEXT_TOKENS
        # 只用到窗口的 75%：回答本身、以及下一轮追加的工具结果都要占地方
        return max(2048, int(ctx * 0.75))

    def maybe_compress_context(self, session_id: str, messages: list[ChatMessage__agent_loop],
                               model: str | None) -> list[ChatMessage__agent_loop]:
        """超预算就把中间那段历史折叠成摘要。

        只在**真的要发请求之前**做，压缩结果只影响这一次请求，不动落盘的历史 ——
        用户切换会话回来还能看到完整原文，这一点很重要（摘要只是给模型的"记忆副本"）。
        """
        try:
            limit = self.effective_context_limit(model, session_id)
            keep = max(4, self.context_keep_recent)
            r = ContextCompressor.fit(list(messages), limit, keep)
            if not r.compressed:
                return messages
            self._record(session_id, "CONTEXT_COMPRESSED",
                         {"tokensBefore": r.tokens_before, "tokensAfter": r.tokens_after,
                          "dropped": r.dropped_messages, "limit": limit},
                         "上下文压缩：" + str(r.tokens_before) + " → " + str(r.tokens_after)
                         + " token，折叠 " + str(r.dropped_messages) + " 条历史")
            return list(r.messages)
        except Exception:
            # 压缩是"保命"机制，它自己出问题绝不能把正常对话带崩
            return messages

    # ------------------------------------------------------------------
    # 生成长度上限
    # ------------------------------------------------------------------
    def max_tokens_per_round(self, session_id: str) -> int | None:
        """一轮里最多生成多少 token —— 本地模型必须封顶。

        实测 llama-server 起来时带的是 `-n 4096`，而解码只有 11-12 token/s：
        模型要是话多，一轮就能写 4096 个 token ≈ **6 分 20 秒**（日志里真出现过
        `eval time = 380323.93 ms / 4096 tokens`）。用户看到的就是"卡住了"。
        本地封 1024（约 90 秒上限，正常一轮只要 40-60 个 token，够用）；
        云端不封，交给服务端默认。
        """
        if self.config_store is None:
            return None
        if self._is_local_mode():
            return self._round_cap(session_id)
        # 自定义 API 指到本机服务（127.0.0.1/localhost）也一样慢，一并封顶
        try:
            snapshot = self.config_store.snapshot()
        except Exception:
            snapshot = {}
        url = snapshot.get("baseUrl") if isinstance(snapshot, dict) else None
        if isinstance(url, str):
            lower = url.lower()
            if "127.0.0.1" in lower or "localhost" in lower or "0.0.0.0" in lower:
                return self._round_cap(session_id)
        return None

    def _round_cap(self, session_id: str) -> int:
        with self._lock:
            return self.round_cap_by_session.setdefault(session_id, LOCAL_MAX_TOKENS_PER_ROUND)

    def bump_round_cap(self, session_id: str) -> None:
        """撞到生成长度上限（finish_reason=length）：本轮多半被截断了（tool_call 写了一半）。

        下一轮把上限翻倍，让它能把"写大文件"这种本来就长的调用写完；顶层封
        MAX_TOKENS_CEILING。用户下一条消息会复位。
        """
        with self._lock:
            now = self.round_cap_by_session.get(session_id, LOCAL_MAX_TOKENS_PER_ROUND)
            nxt = min(now * 2, MAX_TOKENS_CEILING)
            if nxt != now:
                self.round_cap_by_session[session_id] = nxt

    # ------------------------------------------------------------------
    # 预热计划 / 杂项
    # ------------------------------------------------------------------
    def build_warmup_plan(self, mode: str, workspace_path: str | None) -> tuple[list[ChatMessage__agent_loop],
                                                                               list[dict[str, Any]]]:
        """构造预热请求，供本地运行时预热服务用。

        关键点：系统提示词必须和真实请求一模一样，所以这里走的是**同一个
        build_system_prompt 和同一个 build_tool_definitions**，不另写一份。
        用户消息传空串 → 技能块不命中 → 与绝大多数真实请求的提示词一致。

        :return: (messages, tool_definitions) —— 对应 Java 的 `WarmupPlan` record。
        """
        native_tools = self.use_native_tools()
        messages = [ChatMessage__agent_loop.system(self.build_system_prompt(mode, workspace_path, "",
                                                                native_tools)),
                    ChatMessage__agent_loop.user("预热")]
        tools = self.build_tool_definitions(mode) if native_tools else []
        return messages, tools

    @staticmethod
    def repair_hint(malformed: bool) -> str:
        """纠正提示词：针对「模型想做工具调用但调用残缺」和「整轮什么都没输出」两种失手。

        这两种情况在旧版里都表现为「没有工具调用 + 正文为空」→ 直接当成最终答案返回，
        用户看到一句空白回答，任务被静默结束（实测 MiMo 在提示词里看到文本格式示例时
        就会返回 name=null、arguments="{}"、finish_reason=stop 的残缺调用）。
        """
        return REPAIR_HINT_MALFORMED if malformed else REPAIR_HINT_EMPTY

    def add_notice(self, session_id: str, text: str) -> None:
        """往会话里塞一条「系统提示」。

        【注意用 user 角色而不是 system】Qwen 的 Jinja 模板（llama-server 默认启用 --jinja）
        遇到不在开头的 system 消息会直接 raise_exception：
        "System message must be at the beginning."，服务端回 HTTP 500，
        用户看到的是"模型调用失败: HTTP 500"，任务当场断掉。
        所以中途的提示一律走 user 角色（内容自带【系统提示】前缀），
        同时 build_messages() 里还有一道兜底：历史里的 system 消息不在开头也会降级成 user。
        """
        if not text or not text.strip():
            return
        body = text if text.startswith("【系统提示】") else "【系统提示】" + text
        self._append_history(session_id, "user", body)

    def _record(self, session_id: str, event_type: str, data: dict[str, Any],
                summary: str) -> None:
        store = self.event_store
        if store is None:
            return
        try:
            store.record_event(session_id, event_type, data, summary)
        except TypeError:
            # 对方的签名可能只认 (session_id, type, data) 或关键字
            try:
                store.record_event(session_id=session_id, event_type=event_type,
                                   data=data, summary=summary)
            except Exception:
                pass
        except Exception:
            # 事件写不进去不该把主循环带崩
            pass

    def _sound(self, kind: str) -> None:
        """提示音（Java 侧是 SoundNotifier）。`lionbox/system/` 就绪后由它实现，
        这里只在 client 提供了 `play_sound(kind)` 时转调；没有就静默。"""
        fn = getattr(self.client, "play_sound", None)
        if fn is None:
            return
        try:
            fn(kind)
        except Exception:
            pass


# ==========================================================================
# 模块级助手
# ==========================================================================


def _new_uuid() -> str:
    """生成 v4 UUID 字符串（等价 Java `UUID.randomUUID()`）。"""
    import uuid
    return str(uuid.uuid4())


def _new_call_id() -> str:
    """`call_` + 8 位十六进制（与 Java 的 `"call_" + UUID…substring(0,8)` 同形）。"""
    return "call_" + _new_uuid().replace("-", "")[:8]


# ==========================================================================
# 会话历史的统一存取
#
# `lionbox/sessions/ConversationHistory.add_message()` 收的是**一条消息对象**
# （Java 的 `addMessage(ConversationMessage)`），不是散开的参数。所以这里统一造对象：
# 有 sessions 模块就用它的 ConversationMessage，没有就用本模块的 `_HistoryMessage`。
# 两个形状都能被 `build_messages()` 按属性读出来。
# ==========================================================================


def _make_tool_call_records(calls: Sequence[ToolCall__agent_loop]) -> list[Any]:
    """把 ChatMessage.ToolCall 转成历史层要的 ToolCallRecord（只有有效的才留）。"""
    out: list[Any] = []
    for tc in calls:
        if tc.name is None or not str(tc.name).strip():
            continue
        if _SessionsToolCallRecord is not None:
            out.append(_SessionsToolCallRecord(id=tc.id, name=tc.name,
                                               arguments=dict(tc.arguments or {})))
        else:
            out.append(ToolCallRecord__agent_loop(tc.id, tc.name, dict(tc.arguments or {})))
    return out


def _make_history_message(session_id: str, role: str, content: str, *,
                          tool_calls: list[Any] | None = None,
                          tool_call_id: str | None = None,
                          tool_name: str | None = None,
                          reasoning_content: str | None = None) -> Any:
    """造一条会话历史消息（优先 sessions 模块的真实类型）。"""
    if _SessionsMessage is not None:
        kwargs: dict[str, Any] = {"reasoning_content": reasoning_content}
        if role == "assistant" and tool_calls:
            return _SessionsMessage.assistant_with_tool_calls(
                session_id, content, tool_calls, reasoning_content)
        if role == "tool":
            return _SessionsMessage.tool_result(session_id, tool_call_id or "",
                                                tool_name or "", content)
        if role == "system":
            return _SessionsMessage.system(session_id, content)
        if role == "assistant":
            return _SessionsMessage.assistant(session_id, content, reasoning_content)
        return _SessionsMessage.user(session_id, content)
    return _HistoryMessage(
        message_id=_new_uuid(), session_id=session_id, role=role, content=content,
        reasoning_content=reasoning_content, tool_calls=tool_calls,
        tool_call_id=tool_call_id, tool_name=tool_name, timestamp=time.time(),
        metadata={})


def _accepts_message_object(add_message: Any) -> bool:
    """判断 `history.add_message` 是收「一条消息对象」还是收散开的 (session, role, content)。

    真实实现来自 `lionbox/sessions/`（收对象）；本模块的内存桩两种都收。
    签名看不出来时按 Java 契约（收对象）处理。
    """
    try:
        import inspect
        params = list(inspect.signature(add_message).parameters.values())
    except (TypeError, ValueError):
        return True
    positional = [p for p in params
                  if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    return len(positional) <= 1


def _truncate(s: Any, max_len: int) -> str:
    if s is None:
        return ""
    text = s if isinstance(s, str) else str(s)
    return text if len(text) <= max_len else text[:max_len] + "..."


def _num_to_str(v: Any) -> str:
    """Java `String.valueOf(n)`：整数不带 .0。"""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


def _parse_json_object(raw: str | None) -> dict[str, Any]:
    """把一段字符串当 JSON 对象读（读不出来当没参数，与 Java 的 catch-空 Map 一致）。"""
    if raw is None or not str(raw).strip():
        return {}
    try:
        parsed = json.loads(raw)
    except ValueError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _info_get(info: Any, *names: str) -> Any:
    """从模型信息对象/dict 里按候选键名取值（兼容 camelCase 与 snake_case）。"""
    for n in names:
        if isinstance(info, dict):
            if n in info:
                return info[n]
        else:
            v = getattr(info, n, None)
            if v is not None:
                return v
    return None


def _normalize_response(raw: Any) -> ModelResponse__agent_loop:
    """把 llm 层给的响应归一成 ModelResponse（三种形状都认，见模块 docstring）。"""
    if raw is None:
        return ModelResponse__agent_loop()
    if isinstance(raw, ModelResponse__agent_loop):
        return raw

    finish_reason = _pick(raw, "finish_reason", "finishReason")
    content = _pick(raw, "content")
    tool_calls_raw = _pick(raw, "tool_calls", "toolCalls")
    reasoning = _pick(raw, "reasoning_content", "reasoningContent")
    malformed = _pick(raw, "malformed_tool_call", "malformedToolCall")

    # OpenAI 形状：choices[0].message
    choices = _pick(raw, "choices")
    if content is None and isinstance(choices, (list, tuple)) and choices:
        first = choices[0]
        message = _pick(first, "message") or {}
        content = _pick(message, "content")
        if tool_calls_raw is None:
            tool_calls_raw = _pick(message, "tool_calls", "toolCalls")
        if reasoning is None:
            reasoning = _pick(message, "reasoning_content", "reasoningContent")
        if finish_reason is None:
            finish_reason = _pick(first, "finish_reason", "finishReason")

    calls: list[ToolCall__agent_loop] = []
    if isinstance(tool_calls_raw, (list, tuple)):
        for i, tc in enumerate(tool_calls_raw):
            if tc is None:
                continue
            fn = _pick(tc, "function") or {}
            name = _pick(tc, "name") or _pick(fn, "name")
            args = _pick(tc, "arguments")
            if args is None:
                args = _pick(fn, "arguments")
            cid = _pick(tc, "id") or ("call_" + _new_uuid().replace("-", "")[:8])
            calls.append(ToolCall__agent_loop(str(cid),
                                  "" if name is None else str(name),
                                  _coerce_arguments_value(args)))
    elif isinstance(tool_calls_raw, dict):
        # 单条调用直接给成 dict
        single = _normalize_response({"tool_calls": None, **tool_calls_raw})
        calls = single.tool_calls

    # 有 tool_calls 但一个名字都没拼出来 → 残缺调用（Java 里就是 malformedToolCall）
    if malformed is None:
        malformed = bool(isinstance(tool_calls_raw, (list, tuple)) and len(tool_calls_raw) > 0
                         and not any(tc.name.strip() for tc in calls))
    if malformed and calls:
        calls = [tc for tc in calls if tc.name.strip()]

    if finish_reason is None and calls:
        finish_reason = "tool_calls"
    return ModelResponse__agent_loop(content="" if content is None else str(content),
                         tool_calls=calls,
                         finish_reason=None if finish_reason is None else str(finish_reason),
                         reasoning_content=None if reasoning is None else str(reasoning),
                         malformed_tool_call=bool(malformed),
                         raw=raw)


def _coerce_arguments_value(args: Any) -> dict[str, Any]:
    """工具调用的 arguments：dict 直接用，JSON 字符串就解析，别的当空。"""
    if isinstance(args, dict):
        return args
    if isinstance(args, str):
        return _parse_json_object(args)
    return {}


def _pick(obj: Any, *names: str) -> Any:
    """按候选键名/属性名取值（dict 与对象都支持）。"""
    if obj is None:
        return None
    for n in names:
        if isinstance(obj, dict):
            if n in obj:
                return obj[n]
        else:
            v = getattr(obj, n, None)
            if v is not None:
                return v
    return None


def _chunk_delta_text(chunk: Any) -> str:
    """流式分片里的正文增量（同时认 OpenAI 的 choices[0].delta.content）。"""
    v = _pick(chunk, "delta_content", "deltaContent")
    if v:
        return str(v)
    delta = _pick(chunk, "delta")
    if isinstance(delta, str):
        return delta
    if isinstance(delta, dict):
        c = delta.get("content")
        return "" if c is None else str(c)
    choices = _pick(chunk, "choices")
    if isinstance(choices, (list, tuple)) and choices:
        d = _pick(choices[0], "delta") or {}
        c = d.get("content") if isinstance(d, dict) else None
        return "" if c is None else str(c)
    return ""


def _chunk_reasoning(chunk: Any) -> str:
    v = _pick(chunk, "reasoning_content_delta", "reasoningContentDelta")
    if v:
        return str(v)
    delta = _pick(chunk, "delta")
    if isinstance(delta, dict) and delta.get("reasoning_content"):
        return str(delta["reasoning_content"])
    choices = _pick(chunk, "choices")
    if isinstance(choices, (list, tuple)) and choices:
        d = _pick(choices[0], "delta") or {}
        if isinstance(d, dict) and d.get("reasoning_content"):
            return str(d["reasoning_content"])
    return ""


def _chunk_finish_reason(chunk: Any) -> str | None:
    v = _pick(chunk, "finish_reason", "finishReason")
    if v:
        return str(v)
    choices = _pick(chunk, "choices")
    if isinstance(choices, (list, tuple)) and choices:
        fr = _pick(choices[0], "finish_reason", "finishReason")
        if fr:
            return str(fr)
    return None


def _chunk_tool_call_deltas(chunk: Any) -> list[dict[str, Any]]:
    """流式分片里的工具调用增量，统一成 {index,id,name,arguments} 列表。

    【必须用 _pick 而不是 d["index"]】`lionbox/llm` 的 `ModelChunk.tool_call_deltas`
    里装的是 `ToolCallDelta` **dataclass**（字段 index/id/name_delta/arguments_delta），
    不是 dict。按 dict 取会抛 KeyError —— 而且这个异常正好落在流式循环外面那层
    `except` 里，表现是"模型这一轮的工具调用莫名其妙没了，还多插了一条纠正提示"。
    所以这里 dict 形状与对象形状都要认。
    """
    out: list[dict[str, Any]] = []
    raw = _pick(chunk, "tool_call_deltas", "toolCallDeltas")
    if not raw:
        delta = _pick(chunk, "delta")
        if isinstance(delta, dict):
            raw = delta.get("tool_calls")
        elif delta is not None:
            raw = _pick(delta, "tool_calls", "toolCalls")
        else:
            choices = _pick(chunk, "choices")
            if isinstance(choices, (list, tuple)) and choices:
                d = _pick(choices[0], "delta") or {}
                if isinstance(d, dict):
                    raw = d.get("tool_calls")
                else:
                    raw = _pick(d, "tool_calls", "toolCalls")
    if not isinstance(raw, (list, tuple)):
        return out
    for i, d in enumerate(raw):
        if d is None:
            continue
        fn = _pick(d, "function") or {}
        index = _pick(d, "index")
        out.append({
            "index": i if index is None else index,
            "id": _pick(d, "id"),
            "name": _pick(d, "name", "name_delta", "nameDelta") or _pick(fn, "name"),
            "arguments": first_not_none(_pick(d, "arguments", "arguments_delta",
                                              "argumentsDelta"),
                                        _pick(fn, "arguments")),
        })
    return out


def first_not_none(*values: Any) -> Any:
    """取第一个不是 None 的值（分片字段名有好几种写法，按顺序试）。"""
    for v in values:
        if v is not None:
            return v
    return None


# ========================================================================
# 原模块 lionbox/agent.py
# ========================================================================
"""Agent 核心：主循环、工具调用解析与修复、审批、上下文预算、改动人工审核。

对照 Java 包 `com.lioncode.core.agent` + `com.lioncode.approval`：

    loop.py          ← AgentLoop.java (2133)
    parsing.py       ← QwenToolCallParser.java (181)
    name_aliases.py  ← ToolNameAliases.java (249)
    arg_aliases.py   ← ToolArgAliases.java (149)
    guard.py         ← ToolCallGuard.java (143)
    context.py       ← ContextBudget.java + ContextCompressor.java (328)
    control.py       ← AgentControlManager.java + AgentMode.java + ThinkingLevel.java (160)
    approval.py      ← approval/ApprovalPolicy.java (121)
    change.py        ← core/agent/change/*.java (475)

对外接口（供 api/ 与其它模块接）：

    loop = AgentLoop(client=chat_client, config_store=cfg, registry=REGISTRY,
                     event_store=<lionbox.events 的实现>,
                     history=<lionbox.sessions 的实现>,
                     workspace=Path(workspace_root))
    answer = loop.process_message(session_id, user_message, "STANDARD", "low", model)
    for chunk in loop.process_message_stream(session_id, user_message, "STANDARD", "low", model):
        ...

`client` 只需要 `chat(messages, tools=, model=, thinking_level=, max_tokens=)`，
`chat_stream(...)` 可选（缺了会退化成整段发出）。返回结构见 `loop.py` 顶部注释。

自验（157 项，纯标准库、不碰网络/模型）：

    python -m lionbox.agent._verify
"""


from lionbox.agent import arg_aliases, name_aliases, parsing
from lionbox.agent.approval import DEFAULT_AUTO_APPROVED, ApprovalAction, ApprovalPolicy, ApprovalResult, ToolPolicy
from lionbox.agent.change import APPROVED, PENDING, PLUGIN_ID, REJECTED, ChangeReview, Diff, PendingChange

__all__ = [
    # 主循环
    "AgentLoop", "ChatClient", "ChatMessage", "ToolCall", "ToolCallRecord",
    "ModelResponse", "AgentChunk",
    # 事件/历史的兜底桩（真实实现分别由 lionbox.events / lionbox.sessions 提供）
    "LocalEventStore", "MemoryEventStore", "LocalConversationHistory", "InMemoryHistory",
    "SessionContext", "WorkspaceContext",
    # 解析与修复
    "parsing", "name_aliases", "arg_aliases",
    # 统计/预算/控制
    "ToolCallGuard", "Decision", "Verdict",
    "ContextBudget", "ContextCompressor", "CompressResult",
    "AgentControlManager", "AgentMode", "AgentStoppedException", "ThinkingLevel",
    # 审批与改动审核
    "ApprovalPolicy", "ApprovalAction", "ApprovalResult", "ToolPolicy", "DEFAULT_AUTO_APPROVED",
    "ChangeReview", "PendingChange", "Diff", "PENDING", "APPROVED", "REJECTED", "PLUGIN_ID",
]


# ========================================================================
# 原模块 lionbox/context/envelope.py
# ========================================================================
"""新端点的响应外壳 —— 对应 Java `core/context/ApiEnvelope.java`（技能 / @ 引用两组接口用）。

【为什么长这样】项目里老的接口统一是 `ApiResponse`：`{success, message, data, error}`，
前端到处按 `res.success` / `res.data` 取；而技能和 @ 引用这两组接口的设计稿写的是
`{ok, skills:[...]}` / `{ok, items:[...]}` —— 两种写法都有人按着写代码。

与其赌一边，不如两边都给：顶层同时放 `ok`、`success` 和那份数据（`skills` / `items`），
另外在 `data` 里再放一份完整副本。这样 `res.ok`、`res.success`、`res.skills`、
`res.data.skills` 四种写法都能取到值，任何一边的前端代码都不会因为外壳判断错而白屏。
"""


from typing import Any


def ok(fields: dict[str, Any] | None = None, message: str = "操作成功") -> dict[str, Any]:
    """成功响应：`fields` 同时出现在顶层与 `data` 里。"""
    out: dict[str, Any] = {"ok": True, "success": True, "message": message}
    data: dict[str, Any] = {"ok": True}
    if fields:
        out.update(fields)
        data.update(fields)
    out["data"] = data
    return out


def error(reason: str) -> dict[str, Any]:
    """失败响应：`ok`/`success` 都是 false，`error` 里是能照着改的原因。"""
    return {"ok": False, "success": False, "error": reason}


class ApiEnvelope:
    """与 Java 静态工具类同名的门面（`ApiEnvelope.ok(...)` / `ApiEnvelope.error(...)`）。"""

    ok = staticmethod(ok)
    error = staticmethod(error)


__all__ = ["ApiEnvelope", "error", "ok"]


# ========================================================================
# 原模块 lionbox/context/roots.py
# ========================================================================
"""`@` 引用要用的「根目录」解析 —— 对应 Java `core/context/ContextRoots.java`。

解析顺序（和工具层 `WorkspaceContext.resolve` 保持一致，用户才不会觉得两套规则）：

1. 请求里显式给的 `root`（补全接口带过来的，用户在界面上选了目录）
2. 会话绑定的工作区（正常对话都走这条）
3. 都没有时退到进程工作目录（老会话、没绑定工作区的边缘情况）

【为什么要有越界检查】`@file` 是"把文件内容读出来发给模型"：不检查的话，
`@file:../../../../etc/passwd` 或 `@file:C:\\Windows\\...` 就能把工作区外的文件读进上下文。
工具层有同样的沙箱，这里必须对齐 —— 连 **符号链接/junction** 也要拦：
工作区里一个指向外面的 junction（`ws\\link -> C:\\Windows`）会让
`@file:link\\secret.txt` 把外面的文件读出来，而 `read_file` 对同一路径是拒绝的。
"""


import os
from pathlib import Path
from typing import Any


class ContextRoots:
    """根目录解析与越界检查。"""

    def __init__(self, session_manager: Any = None, workspace_manager: Any = None) -> None:
        self.session_manager = session_manager
        self.workspace_manager = workspace_manager

    # ------------------------------------------------------------------
    def resolve(self, session_id: str | None, explicit_root: str | None) -> Path:
        """解析根目录（绝对、规范化）。"""
        if explicit_root is not None and str(explicit_root).strip() != "":
            try:
                candidate = Path(str(explicit_root).strip()).expanduser().absolute()
                candidate = Path(os.path.normpath(str(candidate)))
                if candidate.is_dir():
                    return candidate
            except (OSError, ValueError):
                pass   # 非法路径（Windows 上很常见）→ 退到会话工作区
        workspace = self.session_workspace(session_id)
        if workspace is not None:
            return workspace
        return Path(os.path.normpath(os.path.abspath(os.getcwd())))

    def session_workspace(self, session_id: str | None) -> Path | None:
        """会话绑定的工作区路径；没有返回 None。"""
        if session_id is None or str(session_id).strip() == "":
            return None
        if self.session_manager is None:
            return None
        try:
            session = self.session_manager.get_session(str(session_id))
        except Exception:
            return None
        if session is None:
            return None
        try:
            path = self._workspace_path(session.workspace_id)
            if not path:
                return None
            return Path(os.path.normpath(os.path.abspath(str(path))))
        except Exception:
            # 工作区 id 不是合法路径这类脏数据：不要让 @ 引用把整条消息弄挂
            return None

    def _workspace_path(self, workspace_id: str | None) -> str | None:
        if not workspace_id:
            return None
        if self.workspace_manager is None:
            # 工作区 id 本身就是绝对路径（Java `WorkspaceManager.workspaceIdOf` 的定义）
            return str(workspace_id)
        getter = getattr(self.workspace_manager, "get_workspace", None)
        if not callable(getter):
            return str(workspace_id)
        workspace = getter(str(workspace_id))
        if workspace is None:
            return None
        path = getattr(workspace, "path", None)
        if path is None and isinstance(workspace, dict):
            path = workspace.get("path")
        return None if path is None else str(path)

    # ------------------------------------------------------------------
    def contain(self, root: Path | None, raw_path: str | None) -> Path | None:
        """把 `@file:` 里的路径解析成根目录内的真实路径。

        越界或非法时返回 None（调用方给一句"在工作区之外，已拒绝"）。
        """
        if root is None or raw_path is None or str(raw_path).strip() == "":
            return None
        try:
            raw = Path(str(raw_path).strip()).expanduser()
            if raw.is_absolute():
                target = Path(os.path.normpath(os.path.abspath(str(raw))))
            else:
                target = Path(os.path.normpath(os.path.join(str(root), str(raw))))
            root_norm = Path(os.path.normpath(os.path.abspath(str(root))))
            if not _is_within(target, root_norm):
                return None
            # 符号链接/junction：normalize 不解析链接，必须比真实路径
            real = target
            if not real.exists():
                real = real.parent      # 新建文件的场景：用父目录判
                if real is None or str(real) == "":
                    return target
            try:
                real_target = Path(os.path.realpath(real))
                real_root = Path(os.path.realpath(root_norm)) if root_norm.exists() else root_norm
            except OSError:
                return None
            return target if _is_within(real_target, real_root) else None
        except (OSError, ValueError):
            return None   # 路径里有非法字符（Windows 上很常见），或拿不到真实路径

    def display_path(self, root: Path | None, target: Path | None) -> str:
        """相对根目录的展示路径（统一用 `/` 分隔，前端 insert 直接用）。"""
        if target is None:
            return ""
        try:
            if root is not None and _is_within(Path(target), Path(root)):
                rel = os.path.relpath(str(target), str(root))
                return rel.replace("\\", "/")
        except (OSError, ValueError):
            pass   # 跨盘符时 relpath 会抛异常，退回绝对路径
        return str(target).replace("\\", "/")


def _is_within(target: Path, root: Path) -> bool:
    """`target` 是否在 `root` 之内（含相等）。大小写按平台规则比。"""
    try:
        t = os.path.normcase(os.path.abspath(str(target)))
        r = os.path.normcase(os.path.abspath(str(root)))
    except (OSError, ValueError):
        return False
    if t == r:
        return True
    return t.startswith(r.rstrip("\\/") + os.sep)


__all__ = ["ContextRoots"]


# ========================================================================
# 原模块 lionbox/context/mentions.py
# ========================================================================
"""`@` 引用的展开器 —— 对应 Java `core/context/MentionResolver.java`。

把用户消息里的 `@file:` / `@history:` / `@skill:`（以及 `/skill:`）就地换成真实上下文：

* `@file:src/main/java/X.java` —— 文件内容（≤200 行 / 20KB，超出明确标注截断）；
  目录则列前 100 项；路径在工作区之外一律拒绝。
* `@history:<会话id 或 关键词>` —— 那个会话最近的 ≤30 条消息（≤20KB）。
* `@skill:<技能id>` / `/skill:<技能id>` —— 技能正文（用户点名要用的）。

所有展开都**保留原 token**，内容紧跟在 token 后面用 `--- 引用开始/结束 ---` 包起来，
这样模型既知道用户引用了什么，也不会把文件内容和用户的话混在一起。

技能仓库由装配层注入（`skill_repository`），只需要提供 Java `SkillRepository` 的同名方法；
不注入时技能引用返回"技能功能不可用"，其余引用照常工作。
"""


import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


#: 一条引用最多给多少行文件内容：给多了会挤掉对话历史，模型反而看不见问题本身
MAX_FILE_LINES = 200
MAX_FILE_BYTES = 20 * 1024
#: 读文件时最多读这么多字节（防止用户 @ 一个几百 MB 的日志把内存打爆）
FILE_READ_CAP = 512 * 1024
MAX_DIR_ENTRIES = 100

MAX_HISTORY_MESSAGES = 30
MAX_HISTORY_BYTES = 20 * 1024
MAX_MESSAGE_CHARS = 800

MAX_SKILL_BYTES = 40 * 1024

#: 一轮消息里所有引用的总量上限：再多就没有"上下文"可言了，纯粹烧 token
MAX_TOTAL_BYTES = 80 * 1024

#: 引用语法：参数位二选一 —— 带双引号的（引号内原样取用）或裸串。
#: 裸串表达不了 `my file.ts`，前端选中这种文件时只能截成 `@file:my`，内容会静默没附上。
MENTION = re.compile(r'@(file|history|skill):("[^"]+"|[^\s]+)|/skill:([A-Za-z0-9_.\-]+)')

#: 尾巴上这些字符算"用户的话"，不算引用的一部分
TRAILING_PUNCT = "，。；：、！？）】」》”’)]}>\"',;"

_WS__context_mentions = re.compile(r"\s+")


@dataclass(slots=True)
class Note:
    """展开记录：给事件流和界面用（"已展开 @file:x（120 行）"）。"""

    type: str      # file / history / skill / error / skip
    token: str
    detail: str
    ok: bool

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "token": self.token, "detail": self.detail, "ok": self.ok}


@dataclass(slots=True)
class Expansion:
    """展开后的消息 + 展开记录。"""

    message: str | None
    notes: list[Note]

    @property
    def changed(self) -> bool:
        return bool(self.notes)

    def summary(self) -> str:
        """事件摘要：`已展开 @file:a.txt（120 行）；已展开 @skill:backend`。"""
        parts: list[str] = []
        seen: set[str] = set()
        for note in self.notes or []:
            if note.ok and note.type != "skip":
                text = f"已展开 {note.token}（{note.detail}）"
            elif not note.ok:
                text = f"展开失败 {note.token}：{note.detail}"
            else:
                continue
            if text not in seen:
                seen.add(text)
                parts.append(text)
        return "；".join(parts)


@dataclass(slots=True)
class _Block:
    text: str
    note: Note


class MentionResolver:
    """展开一条用户消息里的所有引用。"""

    def __init__(self, skill_repository: Any = None, session_manager: Any = None,
                 conversation_history: Any = None, roots: ContextRoots | None = None) -> None:
        self.skill_repository = skill_repository
        self.session_manager = session_manager
        self.conversation_history = conversation_history
        self.roots = roots or ContextRoots(session_manager)

    # ------------------------------------------------------------------
    def expand(self, session_id: str | None, message: str | None) -> Expansion:
        if not message or message.strip() == "" or not has_mention(message):
            return Expansion(message, [])
        root = self.roots.resolve(session_id, None)
        out: list[str] = []
        notes: list[Note] = []
        seen: set[str] = set()
        last = 0
        budget = MAX_TOTAL_BYTES

        for match in MENTION.finditer(message):
            kind = match.group(1) or "skill"
            arg = unquote(match.group(2) if match.group(1) else match.group(3))
            token = match.group(0)
            # 原样保留用户写的 token：模型要知道"这段内容是用户引用的"，用户回看也不困惑
            out.append(message[last:match.end()])
            last = match.end()

            if arg == "":
                block = self._fail(token, "引用后面没写名字（例如 @file:src/App.java）")
            elif f"{kind}:{arg}" in seen:
                block = self._plain(token, "（同一个引用上面已经展开过，这里不重复贴一遍）")
            elif budget <= 0:
                block = self._fail(
                    token, f"本轮引用内容已达上限（{MAX_TOTAL_BYTES // 1024}KB），"
                           "这一条没有展开。需要的话下一条消息单独引用它")
            else:
                seen.add(f"{kind}:{arg}")
                if kind == "file":
                    block = self._expand_file(token, arg, root)
                elif kind == "history":
                    block = self._expand_history(token, arg)
                else:
                    block = self._expand_skill(token, arg)
                budget -= len(block.text)
            out.append("\n" + block.text + "\n")
            notes.append(block.note)

        out.append(message[last:])
        return Expansion("".join(out), notes)

    # ------------------------------------------------------------------
    # @file:
    # ------------------------------------------------------------------
    def _expand_file(self, token: str, arg: str, root: Path | None) -> _Block:
        target = self.roots.contain(root, arg)
        if target is None:
            return self._fail(token, f"路径在工作区之外，已拒绝读取：{arg}（当前工作区/根目录：{root}）")
        if not target.exists():
            return self._fail(token, f"文件不存在：{arg}（根目录：{root}）{self._similar_hint(target)}")
        if target.is_dir():
            return self._expand_directory(token, arg, target, root)
        if not target.is_file():
            return self._fail(token, f"不是普通文件（可能是设备/管道）：{arg}")

        try:
            raw = read_capped(target, FILE_READ_CAP)
            cut_by_size = target.stat().st_size > len(raw)
            text = decode(raw)
        except OSError as e:
            print(f"[@引用] @file 读取失败: {target} - {e}", flush=True)
            return self._fail(token, f"读取失败：{arg} —— {e}")

        lines = re.split(r"\r?\n", text)
        total_lines = len(lines)
        body: list[str] = []
        used_bytes = 0
        taken = 0
        for line in lines:
            if taken >= MAX_FILE_LINES:
                break
            length = len(line.encode("utf-8")) + 1
            if used_bytes + length > MAX_FILE_BYTES:
                break
            body.append(line + "\n")
            used_bytes += length
            taken += 1
        truncated = taken < total_lines or cut_by_size
        display = self.roots.display_path(root, target)

        head = (f"--- 引用开始：文件 {display}（第 1-{taken} 行，共 {total_lines} 行")
        if truncated:
            head += (f"，**已截断**：只给了前 {taken} 行 / {MAX_FILE_BYTES // 1024}KB，"
                     "需要更多就再引用一次并说明要看哪一段")
        head += "）---\n"
        block = (head + "".join(body) + f"--- 引用结束：文件 {display} ---")

        detail = f"文件 {display}（{taken}/{total_lines} 行" + ("，已截断" if truncated else "") + "）"
        return _Block(block, Note("file", token, detail, True))

    def _expand_directory(self, token: str, arg: str, directory: Path, root: Path | None) -> _Block:
        display = self.roots.display_path(root, directory)
        lines = [f"--- 引用开始：目录 {display} ---\n"]
        count = 0
        try:
            with os.scandir(directory) as it:
                entries = sorted(it, key=lambda e: e.name)[:MAX_DIR_ENTRIES]
                for entry in entries:
                    try:
                        is_dir = entry.is_dir()
                    except OSError:
                        is_dir = False
                    lines.append(("[DIR]  " if is_dir else "[FILE] ") + entry.name + "\n")
                    count += 1
            if count == 0:
                lines.append("（空目录）\n")
        except OSError as e:
            return self._fail(token, f"目录读取失败：{arg} —— {e}")
        lines.append("（这是目录不是文件；要某个文件就 @file:它的路径）\n")
        lines.append(f"--- 引用结束：目录 {display} ---")
        return _Block("".join(lines),
                      Note("file", token, f"目录 {display}（{count} 项）", True))

    def _similar_hint(self, target: Path) -> str:
        """文件不存在时给几个相近的名字（和 read_file 的 similarPathHint 一个思路）。"""
        try:
            directory = target.parent
            if directory is None or not directory.is_dir():
                return ""
            want = target.name.lower()
            stem = want[:want.rfind(".")] if "." in want else want
            near: list[str] = []
            with os.scandir(directory) as it:
                for entry in it:
                    name = entry.name
                    lower = name.lower()
                    if stem and (stem in lower or lower in stem):
                        near.append(name)
                    if len(near) >= 5:
                        break
            return "" if not near else "。同目录下有这些相近的名字：" + "、".join(near)
        except OSError:
            return ""

    # ------------------------------------------------------------------
    # @history:
    # ------------------------------------------------------------------
    def _expand_history(self, token: str, arg: str) -> _Block:
        history_id = self._resolve_history_id(arg)
        if history_id is None:
            candidates = [f"{s.display_name()}({short_id(s.session_id)})"
                          for s in (self._all_sessions()[:8])]
            return self._fail(token, f"没找到历史对话：{arg}（可用的有："
                                    + ("、".join(candidates) if candidates else "当前没有历史对话")
                                    + "）")
        history = self._history(history_id)
        if not history and self.conversation_history is not None:
            # 内存里没有就去磁盘捞一次：历史文件按会话存，重启后按需加载也就够了
            try:
                self.conversation_history.load_from_disk(history_id)
            except Exception as e:
                print(f"[@引用] 按需加载会话历史失败 {history_id}: {e}", flush=True)
            history = self._history(history_id)
        if not history:
            return self._fail(token, f"历史对话 {arg} 里没有任何消息")

        session = self._session(history_id)
        label = session.display_name() if session is not None else f"会话 {short_id(history_id)}"
        recent = history[max(0, len(history) - MAX_HISTORY_MESSAGES):]

        parts = [f"--- 引用开始：历史会话「{label}」({short_id(history_id)})，"
                 f"最近 {len(recent)} 条消息 ---\n"]
        # 这句必须写：不写清楚，模型经常把历史会话里的内容当成当前对话的一部分
        parts.append("注意：下面是**另一个历史会话**的内容（不是当前会话），只作参考。"
                     "不要把它当成当前对话，也不要回复其中的问题；当前用户的问题在引用块之外。\n\n")

        used_bytes = 0
        included = 0
        for message in recent:
            line = render_message(message)
            if not line or line.strip() == "":
                continue
            length = len(line.encode("utf-8"))
            if used_bytes + length > MAX_HISTORY_BYTES:
                parts.append("…（历史内容过长，后面的消息省略了）\n")
                break
            parts.append(line + "\n")
            used_bytes += length
            included += 1
        parts.append(f"--- 引用结束：历史会话「{label}」({short_id(history_id)}) ---")

        detail = f"历史对话「{label}」({short_id(history_id)})，{included} 条消息"
        return _Block("".join(parts), Note("history", token, detail, True))

    def _resolve_history_id(self, arg: str) -> str | None:
        """支持直接给会话 id，也支持给关键词（标题/首条用户消息里包含它）。"""
        if self.session_manager is not None and self.session_manager.get_session(arg) is not None:
            return arg
        query = arg.lower()
        best: str | None = None
        best_score = 0
        for session in self._all_sessions():
            score = 0
            sid = (session.session_id or "").lower()
            if sid == query:
                score = 120
            elif sid.startswith(query):
                score = 100
            elif query in sid:
                score = 80
            name = (session.display_name() or "").lower()
            if name.strip() and query in name:
                score = max(score, 90)
            first = self._first_user_message(session.session_id)
            if first.strip() and query in first.lower():
                score = max(score, 70)
            if score > best_score:
                best_score = score
                best = session.session_id
        return best

    def _first_user_message(self, session_id: str | None) -> str:
        for message in self._history(session_id):
            if message.role == "user" and message.content and message.content.strip():
                return message.content
        return ""

    # ------------------------------------------------------------------
    # @skill: / /skill:
    # ------------------------------------------------------------------
    def _expand_skill(self, token: str, arg: str) -> _Block:
        if self.skill_repository is None:
            return self._fail(token, "技能功能尚未装配（缺少技能仓库）")
        reason = self.skill_repository.unusable_reason(arg)
        if reason:
            return self._fail(token, reason)
        definition = self.skill_repository.find_enabled(arg)
        if definition is None:
            return self._fail(token, f"技能不存在或未启用：{arg}")
        body = (getattr(definition, "body", "") or "").strip()
        cut = len(body) > MAX_SKILL_BYTES
        if cut:
            body = body[:MAX_SKILL_BYTES] + "\n…（技能正文过长，已截断）"
        skill_id = getattr(definition, "id", arg)
        display = getattr(definition, "displayName", None) or getattr(definition, "display_name", "")
        text = (f"--- 引用开始：技能 {skill_id}（{display}）---\n"
                "用户点名要用这个技能，本轮请按下面的指令执行：\n\n"
                f"{body}\n"
                f"--- 引用结束：技能 {skill_id} ---")
        return _Block(text, Note("skill", token,
                                 f"技能 {skill_id}（{display}）的完整指令", True))

    # ------------------------------------------------------------------
    # 小工具
    # ------------------------------------------------------------------
    @staticmethod
    def _fail(token: str, reason: str) -> _Block:
        return _Block(f"--- 引用失败：{token} ---\n原因：{reason}\n--- 引用结束 ---",
                      Note("error", token, reason, False))

    @staticmethod
    def _plain(token: str, text: str) -> _Block:
        return _Block(text, Note("skip", token, "重复引用，未重复展开", True))

    def _history(self, session_id: str | None) -> list[ConversationMessage]:
        if self.conversation_history is None or session_id is None:
            return []
        return list(self.conversation_history.get_history(session_id))

    def _session(self, session_id: str | None):
        if self.session_manager is None or session_id is None:
            return None
        return self.session_manager.get_session(session_id)

    def _all_sessions(self) -> list[Any]:
        if self.session_manager is None:
            return []
        return list(self.session_manager.get_all_sessions())


# ----------------------------------------------------------------------
# 模块级纯函数（与 Java 静态方法一一对应）
# ----------------------------------------------------------------------


def has_mention(message: str | None) -> bool:
    """消息里有没有引用记号（没有就整条快路径返回，省掉正则和读盘）。"""
    if not message:
        return False
    return ("@file:" in message or "@history:" in message
            or "@skill:" in message or "/skill:" in message)


def unquote(raw: str | None) -> str:
    """取出引用参数：带双引号的引号内原样取用（不修剪标点），其余走 `trim_punct`。"""
    if raw is None:
        return ""
    if len(raw) >= 2 and raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1].strip()
    return trim_punct(raw)


def trim_punct(text: str | None) -> str:
    if text is None:
        return ""
    out = text
    while out and out[-1] in TRAILING_PUNCT:
        out = out[:-1]
    return out.strip()


def short_id(session_id: str | None) -> str:
    if not session_id:
        return "?"
    return session_id[:8] if len(session_id) > 8 else session_id


def compact(text: str | None, max_chars: int) -> str:
    if text is None:
        return ""
    flat = _WS__context_mentions.sub(" ", text).strip()
    return flat if len(flat) <= max_chars else flat[:max_chars] + "…"


def render_message(message: ConversationMessage) -> str | None:
    """把一条消息压成紧凑的一两行（历史上下文是"参考"，不需要原文照搬）。"""
    role = message.role or "?"
    if role == "user":
        return "[用户] " + compact(message.content, MAX_MESSAGE_CHARS)
    if role == "assistant":
        if message.tool_calls:
            names = "、".join((tc.name or "?") for tc in message.tool_calls)
            text = "[助手→调用工具] " + names
            if message.content and message.content.strip():
                text += "；说明：" + compact(message.content, 200)
            return text
        return "[助手] " + compact(message.content, MAX_MESSAGE_CHARS)
    if role == "tool":
        return f"[工具结果:{message.tool_name or '?'}] " + compact(message.content, 300)
    if role == "system":
        return None      # 系统消息是提示词噪音，引进来没意义
    return f"[{role}] " + compact(message.content, 200)


def read_capped(path: Path, cap: int) -> bytes:
    """读文件，最多读 cap 个字节（防止 @ 一个大文件把内存打爆）。"""
    with open(path, "rb") as f:
        return f.read(cap)


def decode(raw: bytes) -> str:
    """容错解码：UTF-8 → GBK（Windows 上 ANSI 文件很常见，和工具层保持一致）。"""
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        pass
    for encoding in ("gbk", "latin-1"):
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace")


def one_line(text: str | None, max_chars: int) -> str:
    """合并空白并截断（技能说明等处用，和 `SkillDefinition.oneLine` 行为一致）。"""
    if text is None:
        return ""
    flat = _WS__context_mentions.sub(" ", text).strip()
    return flat if len(flat) <= max_chars else flat[:max_chars] + "…"


__all__ = [
    "FILE_READ_CAP", "MAX_DIR_ENTRIES", "MAX_FILE_BYTES", "MAX_FILE_LINES",
    "MAX_HISTORY_BYTES", "MAX_HISTORY_MESSAGES", "MAX_MESSAGE_CHARS", "MAX_SKILL_BYTES",
    "MAX_TOTAL_BYTES", "MENTION", "TRAILING_PUNCT", "Expansion", "MentionResolver", "Note",
    "compact", "decode", "has_mention", "one_line", "read_capped", "render_message",
    "short_id", "trim_punct", "unquote",
]


# ========================================================================
# 原模块 lionbox/context/search.py
# ========================================================================
"""`@` 引用的补全检索 —— 对应 Java `core/context/MentionSearchService.java`。

给前端"输入 @ 之后弹出的候选列表"提供数据。三类候选：`file`（工作区里的文件）、
`history`（历史对话）、`skill`（已启用的技能）。返回里的 `insert` 字段就是前端要插进
输入框的文本（形如 `@file:src/main/java/X.java`），和服务端展开器认的语法完全一致 ——
两边靠这个字段对齐，前端不需要自己拼。

【为什么要"防炸"】文件检索是用户边打字边调的（每敲一个字可能就调一次），
而工作区可能是几十万个文件的仓库（node_modules、target 就在里面）。所以：
跳过依赖/构建/IDE 目录、最多遍历 20000 个文件、最深 12 层、整个检索 2 秒硬上限，
超时就把已经找到的部分返回（宁可少给几个候选，也不能把界面卡住）。
"""


import os
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


#: 这些目录不该进候选：要么是依赖，要么是构建产物，要么是编辑器垃圾
SKIP_DIRS = frozenset({
    "node_modules", "target", "dist", "build", "out", "bin", "obj", "vendor",
    ".git", ".idea", ".vscode", ".gradle", ".mvn", ".next", ".nuxt", ".cache",
    "__pycache__", ".venv", "venv", "env", ".tox", "coverage", ".pytest_cache",
    "logs", "tmp", "temp", ".lioncode", "runtime-vulkan", "runtime-cpu", "models",
})

MAX_FILES = 20000
MAX_DEPTH = 12
DEADLINE_SECONDS = 2.0
DEFAULT_LIMIT = 20
MAX_LIMIT = 50


@dataclass(slots=True)
class Item:
    """一条候选（字段名与 Java record 一致，进 `/api/context/mentions` 响应）。"""

    type: str
    id: str
    label: str
    detail: str
    insert: str

    def to_dict(self) -> dict[str, Any]:
        return {"type": self.type, "id": self.id, "label": self.label,
                "detail": self.detail, "insert": self.insert}


@dataclass(slots=True)
class Result:
    """检索结果。`note` 为 None 时**整个省略**（Java 侧 `@JsonInclude(NON_NULL)`）。"""

    items: list[Item] = field(default_factory=list)
    truncated: bool = False
    elapsedMs: int = 0
    scannedFiles: int = 0
    root: str = ""
    note: str | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "items": [i.to_dict() for i in self.items],
            "truncated": self.truncated,
            "elapsedMs": self.elapsedMs,
            "scannedFiles": self.scannedFiles,
            "root": self.root,
        }
        if self.note is not None:
            out["note"] = self.note
        return out


@dataclass(slots=True)
class _Hit:
    score: int
    name: str
    rel: str
    size: int


class _Ctx:
    """遍历状态（文件数、命中、截止时间）。"""

    __slots__ = ("root", "query", "hits", "files", "truncated", "deadline")

    def __init__(self, root: Path, query: str, deadline: float) -> None:
        self.root = root
        self.query = query
        self.hits: list[_Hit] = []
        self.files = 0
        self.truncated = False
        self.deadline = deadline

    def stop(self) -> bool:
        return self.files > MAX_FILES or time.monotonic() > self.deadline


class MentionSearchService:
    """检索候选（文件 / 历史对话 / 技能）。"""

    def __init__(self, session_manager: Any = None, conversation_history: Any = None,
                 skill_repository: Any = None, roots: ContextRoots | None = None) -> None:
        self.session_manager = session_manager
        self.conversation_history = conversation_history
        self.skill_repository = skill_repository
        self.roots = roots or ContextRoots(session_manager)

    def search(self, q: str | None = None, kind: str | None = None, root: str | None = None,
               session_id: str | None = None, limit: int | None = None) -> Result:
        started = time.perf_counter()
        cap = DEFAULT_LIMIT if not limit or limit <= 0 else min(int(limit), MAX_LIMIT)
        k = (kind or "").strip().lower() or "all"
        query = (q or "").strip()

        items: list[Item] = []
        root_path = self.roots.resolve(session_id, root)
        note: str | None = None
        truncated = False
        scanned = 0

        if k in ("all", "skill"):
            items.extend(self._search_skills(query, cap))
        if k in ("all", "history"):
            items.extend(self._search_history(query, cap, session_id))
        if k in ("all", "file"):
            # 【为什么显式给的 root 不合法就不往下找了】前端传的 root 是"用户选的那个目录"，
            # 它不存在时如果静默退到会话工作区，用户会看到一堆"别的目录"的文件候选，
            # 却不知道自己在看哪儿 —— 明确告诉他目录不存在，比给错数据强。
            bad = bad_root(root)
            if bad is not None:
                note = "根目录不存在或不是目录：" + bad
            elif not root_path.is_dir():
                note = "工作区目录不存在或不可读：" + root_path
            else:
                ctx = _Ctx(root_path, query.lower(), time.monotonic() + DEADLINE_SECONDS)
                self._walk(root_path, 1, ctx)
                ctx.hits.sort(key=lambda h: (-h.score, len(h.rel), h.rel))
                for hit in ctx.hits[:min(cap, len(ctx.hits))]:
                    items.append(Item("file", hit.rel, hit.name,
                                      f"{hit.rel} · {human_size(hit.size)}",
                                      mention_token(hit.rel)))
                truncated = ctx.truncated
                scanned = ctx.files
                if truncated:
                    note = (f"已扫描 {scanned} 个文件后停止（目录太大或超过 "
                            f"{int(DEADLINE_SECONDS)} 秒上限），结果可能不全")

        elapsed_ms = int((time.perf_counter() - started) * 1000)
        return Result(items, truncated, elapsed_ms, scanned, str(root_path), note)

    # ------------------------------------------------------------------
    # 文件
    # ------------------------------------------------------------------
    def _walk(self, directory: Path, depth: int, ctx: _Ctx) -> None:
        if ctx.stop() or depth > MAX_DEPTH:
            ctx.truncated = True
            return
        try:
            with os.scandir(directory) as it:
                entries = list(it)
        except OSError as e:
            # 单个目录读不了（权限/被占用）就跳过它，不要影响其它目录
            print(f"[@检索] 跳过目录 {directory}: {e}", flush=True)
            return
        for entry in entries:
            if ctx.stop():
                return
            name = entry.name
            try:
                is_dir = entry.is_dir()
            except OSError:
                continue
            if is_dir:
                # 隐藏目录（.git/.idea/…）和依赖目录一律不进 —— 候选列表里出现
                # node_modules 里的文件对用户没有任何意义，还白花遍历时间
                if name.startswith(".") or name.lower() in SKIP_DIRS:
                    continue
                self._walk(Path(entry.path), depth + 1, ctx)
                continue
            ctx.files += 1
            if ctx.files > MAX_FILES:
                ctx.truncated = True
                return
            try:
                rel = os.path.relpath(entry.path, str(ctx.root)).replace("\\", "/")
            except (OSError, ValueError):
                continue
            score = score_file(name, rel, ctx.query)
            if score > 0:
                try:
                    size = entry.stat().st_size
                except OSError:
                    size = 0      # 拿不到大小不影响候选，detail 里显示 0 B
                ctx.hits.append(_Hit(score, name, rel, size))

    # ------------------------------------------------------------------
    # 历史对话
    # ------------------------------------------------------------------
    def _search_history(self, q: str, cap: int, current_session_id: str | None) -> list[Item]:
        query = q.lower()
        hits: list[tuple[int, Any, str]] = []
        for session in self._all_sessions():
            sid = session.session_id or ""
            if sid == current_session_id:
                continue                 # 当前会话不用 @ 引用自己
            title = session.display_name() or ""
            first = self._first_user_message(sid)
            lower_title = title.lower()
            lower_first = first.lower()
            if query == "":
                score = 50
            elif sid.lower() == query:
                score = 100
            elif query in lower_title:
                score = 85
            elif sid.lower().startswith(query):
                score = 70
            elif query in lower_first:
                score = 60
            else:
                score = 0
            if score > 0:
                hits.append((score, session, first))
        hits.sort(key=lambda h: (-h[0], -_created_ts(h[1])))
        out: list[Item] = []
        for _score, session, first in hits[:min(cap, len(hits))]:
            sid = session.session_id
            count = 0
            if self.conversation_history is not None:
                count = self.conversation_history.get_message_count(sid)
            detail = f"{count} 条消息" + ("" if not first.strip() else " · " + one_line(first, 60))
            out.append(Item("history", sid, session.display_name(), detail, "@history:" + sid))
        return out

    def _first_user_message(self, session_id: str | None) -> str:
        if self.conversation_history is None or session_id is None:
            return ""
        for message in self.conversation_history.get_history(session_id):
            if message.role == "user" and message.content and message.content.strip():
                return message.content
        return ""

    # ------------------------------------------------------------------
    # 技能
    # ------------------------------------------------------------------
    def _search_skills(self, q: str, cap: int) -> list[Item]:
        if self.skill_repository is None:
            return []
        query = q.lower()
        hits: list[tuple[int, Any]] = []
        for definition in self.skill_repository.list():
            usable = getattr(definition, "usable", None)
            if callable(usable) and not usable():
                continue
            skill_id = str(getattr(definition, "id", "") or "")
            if not self.skill_repository.is_enabled(skill_id):
                continue
            display = str(getattr(definition, "displayName", None)
                          or getattr(definition, "display_name", "") or "")
            description = str(getattr(definition, "description", "") or "")
            keywords = [str(k) for k in (getattr(definition, "keywords", None) or [])]
            if query == "":
                score = 50
            elif skill_id.lower() == query:
                score = 100
            elif any(k.lower() == query for k in keywords):
                score = 90
            elif query in skill_id.lower():
                score = 80
            elif query in display.lower():
                score = 70
            elif any(query in k.lower() for k in keywords):
                score = 65
            elif query in description.lower():
                score = 40
            else:
                score = 0
            if score > 0:
                hits.append((score, definition))
        hits.sort(key=lambda h: (-h[0], str(getattr(h[1], "id", ""))))
        out: list[Item] = []
        seen: set[str] = set()
        for _score, definition in hits:
            skill_id = str(getattr(definition, "id", "") or "")
            if skill_id in seen:
                continue
            seen.add(skill_id)
            display = str(getattr(definition, "displayName", None)
                          or getattr(definition, "display_name", "") or "")
            out.append(Item("skill", skill_id, display,
                            str(getattr(definition, "description", "") or ""),
                            "@skill:" + skill_id))
            if len(out) >= cap:
                break
        return out

    # ------------------------------------------------------------------
    def _all_sessions(self) -> list[Any]:
        if self.session_manager is None:
            return []
        return list(self.session_manager.get_all_sessions())


# ----------------------------------------------------------------------
# 模块级纯函数
# ----------------------------------------------------------------------


def bad_root(root: str | None) -> str | None:
    """显式传进来的 root 不合法时返回它（给提示用），合法或没传返回 None。"""
    if root is None or str(root).strip() == "":
        return None
    text = str(root).strip()
    try:
        return None if Path(text).is_dir() else text
    except (OSError, ValueError):
        return text   # 路径里有非法字符（Windows 上很常见）


def score_file(name: str, rel: str, q: str) -> int:
    """文件相关度打分：候选列表只有 20 行，文件名正好叫 skill 的必须排在路径里含 skill 的前面。"""
    if q == "":
        return 10
    n = name.lower()
    r = rel.lower()
    if n == q:
        return 100
    if n.startswith(q):
        return 90
    if q in n:
        return 75
    stem = n[:n.rfind(".")] if "." in n else n
    if stem == q:
        return 95
    if q in r:
        return 55
    if subsequence(n, q):        # 打字顺序匹配（skmd → SKILL.md 这类首字母缩写查询）
        return 25
    return 0


def subsequence(haystack: str, needle: str) -> bool:
    if needle == "":
        return True
    i = 0
    for ch in haystack:
        if i < len(needle) and ch == needle[i]:
            i += 1
    return i == len(needle)


def mention_token(rel: str | None) -> str:
    """生成 `@file:` 引用记号：含空格/制表符的路径加双引号（否则会被截成 `@file:my`）。"""
    if rel is None or rel.strip() == "":
        return "@file:"
    p = rel.replace("\\", "/")
    if " " in p or "\t" in p:
        return f'@file:"{p}"'
    return "@file:" + p


def human_size(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024.0:.1f} KB"
    return f"{size / 1024.0 / 1024.0:.1f} MB"


def _created_ts(session: Any) -> float:
    """会话创建时间（epoch 秒）；没有时间的当 0（排最后）。"""
    created = getattr(session, "created_at", None)
    if created is None:
        return 0.0
    try:
        return created.timestamp()
    except (OSError, ValueError, OverflowError):
        return 0.0


__all__ = [
    "DEADLINE_SECONDS", "DEFAULT_LIMIT", "MAX_DEPTH", "MAX_FILES", "MAX_LIMIT", "SKIP_DIRS",
    "Item", "MentionSearchService", "Result", "bad_root", "human_size", "mention_token",
    "score_file", "subsequence",
]


# ========================================================================
# 原模块 lionbox/context.py
# ========================================================================
"""工作区上下文（P2）—— 对应 Java `com.lioncode.core.context` 的 4 个类。

| Java | 这里 |
| --- | --- |
| `ContextRoots` | `roots.ContextRoots` |
| `MentionResolver`（含 `Note` / `Expansion`） | `mentions.MentionResolver` |
| `MentionSearchService`（含 `Item` / `Result`） | `search.MentionSearchService` |
| `ApiEnvelope` | `envelope.ApiEnvelope` |

技能仓库（`SkillRepository`）属于 P5，通过构造器注入；不注入时技能相关引用返回
"技能功能尚未装配"，文件/历史引用照常工作 —— 这样 P2 可以先独立验收。
"""



__all__ = [
    "ApiEnvelope",
    "ContextRoots",
    "Expansion",
    "Item",
    "MentionResolver",
    "MentionSearchService",
    "Note",
    "Result",
    "decode",
    "error",
    "has_mention",
    "mention_token",
    "ok",
    "one_line",
    "render_message",
]


# ========================================================================
# 原模块 lionbox/api/context.py
# ========================================================================
"""`@` 引用补全接口 —— `/api/context/mentions`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\ContextController.java`（81 行 / 1 个接口）。

前端在输入框里敲 `@` 之后调这个接口拿候选，选中后把 `insert` 原样插进输入框；
用户发出消息后，服务端（`MentionResolver`）按同一套语法把引用展开成真实上下文 ——
两边共用 `insert` 字段，前端不需要自己拼 `@file:` 前缀。

【响应外壳不是 ApiResponse】Java 用的是 `core/context/ApiEnvelope`：顶层同时给
`ok` / `success` / `message` 和业务字段（`items` / `q` / `kind` / `root` / `limit` /
`truncated` / `elapsedMs` / `scannedFiles` / `counts`，需要提示时再加 `note`），
`data` 里再放一份**同样的副本**（少 `success` / `message`）。
前端按 `res.ok` / `res.success` / `res.items` / `res.data.items` 四种写法取数据，
所以这里必须返回 `Response` 原样发出：返回 dict 或 ApiResponse 都会被再包一层，
`items` 就不在顶层了（老接口才是那种包法）。

# 依赖：lionbox.sessions（由并行任务提供）
#   会话/对话历史。`sessions` 服务未装配时是 `deps.SessionStoreStub` 窄桩（内存会话表），
#   此时 `kind=history` 类候选天然为空 —— 与 Java 在"没有任何会话"时同形。
#   装配方 `ctx.install("sessions", SessionManager(...))` 后即取真实会话（含磁盘上的老会话）。
# 依赖：lionbox.context（MentionSearchService / ContextRoots / ApiEnvelope，已就绪）
# 依赖：lionbox.skills（SkillRepository，已就绪）
"""


import datetime as _dt
import re
from typing import Any

from lionbox.skills.repository import default_repository
from lionbox.api import deps

#: Java `@RequestParam Integer limit` 的实际绑定规则（Spring 的 `Integer` 转换 + `Integer.parseInt`）。
#: 三处都和 Python 的 `int()` 不一样，所以不能用 int() 直接转（下面 `parse_limit` 里逐条说明）。
#: `\d` 在 Python 里就是 Unicode 的 Nd 类数字，和 Java `Character.digit` 的十进制数字一致。
_JAVA_WS = re.compile("[ \t\n\x0b\f\r\u001c-\u001f\u1680\u2000-\u2006\u2008-\u200a"
                      "\u2028\u2029\u205f\u3000]+")
_DECIMAL = re.compile(r"[+-]?\d+\Z")
_HEX = re.compile(r"(?:\d|[a-fA-F])+\Z")
_JAVA_INT_MIN = -2147483648
_JAVA_INT_MAX = 2147483647

#: `limit` 的默认值与上限（Java `MentionSearchService.DEFAULT_LIMIT` / `MAX_LIMIT`）。
DEFAULT_LIMIT__api_context = 20
MAX_LIMIT__api_context = 50


# --------------------------------------------------------------------------
# 参数与字段工具（与 Java 静态方法一一对应）
# --------------------------------------------------------------------------


def parse_limit(raw: str | None) -> int | None:
    """解析 `limit` 查询参数，与 Spring 绑定 `Integer` 的行为逐条对齐。

    Spring 那条链路的真实行为（**逐条在 18099 上实测过**，不是照文档猜的）是：

    * 先删掉**所有** Java 空白字符（含中间：`"1 0"` → 10；`"0x 10"` → 16）；
      删完是空串（`""`、`"   "`、`"\\t"`）→ 参数当没给（`None`，实测回落到 20）；
    * 认十六进制前缀 `0x` / `0X` / `#`（`0x10`→16、`#10`→16、`0x1f`→31）；
      **负号可以写在最前面**（`-0x10` → -16、`-#10` → -16），但 `+0x10` / `+#10` 是 400；
    * 其余按 `Integer.parseInt`：允许**一个**前导符号（`+5`→5、`-3`→-3），
      认 Unicode 数字（`"١٠"` → 10），不认下划线（`1_0`→400）、小数点（`3.7`→400）、
      进制后缀（`1e3`、`0b10`→400）、连续符号（`--5`、`-+5`、`+-5`→400）；
    * 超出 Java int 范围（`2147483648`）→ 400；
    * 最后 `limit <= 0` 由调用方回落到默认 20（Java 控制器里的三元表达式）。

    非法输入抛 `ValueError`，调用方回 Spring 的 400 错误体。

    【为什么不用 `int()` 直接转】`int("1_0")` 在 Python 里是 10（Java 400）、
    `int("0x10")` 报 ValueError 而 Java 给 16、`"\\xa05".strip()` 会把 NBSP 当空白
    （Java 的 `Character.isWhitespace('\\xa0')` 是 false → 400）——
    参数写错时必须和 Java 回一样的 400，不能悄悄按默认值跑。
    """
    if raw is None:
        return None
    text = _JAVA_WS.sub("", str(raw))
    if text == "":
        return None

    negative = False
    if text.startswith(("0x", "0X")):
        radix, digits = 16, text[2:]
    elif text.startswith("#"):
        radix, digits = 16, text[1:]
    elif text.startswith(("-0x", "-0X")):
        negative, radix, digits = True, 16, text[3:]
    elif text.startswith("-#"):
        negative, radix, digits = True, 16, text[2:]
    else:
        radix, digits = 10, text

    if (_HEX if radix == 16 else _DECIMAL).fullmatch(digits) is None:
        raise ValueError(f"limit 不是整数: {raw}")
    value = int(digits, radix)
    if negative:
        value = -value
    if value < _JAVA_INT_MIN or value > _JAVA_INT_MAX:
        raise ValueError(f"limit 超出 int 范围: {raw}")
    return value


def count_of(items: list[Any], type_name: str) -> int:
    """数某一类候选的条数（Java `countOf` 就是 `stream().filter(type::equals).count()`）。"""
    return sum(1 for item in items if getattr(item, "type", None) == type_name)


def parse_created_at(value: Any) -> _dt.datetime | None:
    """会话创建时间：窄桩存的是 Instant 字符串（`2026-10-03T11:55:28.690Z`），
    真实 `Session` 里是 datetime。解析不出来返回 `None`（排序时按 0 处理）。"""
    if isinstance(value, _dt.datetime):
        return value
    if isinstance(value, str) and value.strip():
        try:
            return _dt.datetime.fromisoformat(value.strip())
        except ValueError:
            return None
    return None


# --------------------------------------------------------------------------
# 窄桩的形状适配（唯一依赖桩的地方）
# --------------------------------------------------------------------------


class _DictSession:
    """把窄桩里的 **dict 会话**包成 Java `Session` record 的读取面。

    # 依赖：lionbox.sessions（由并行任务提供）

    【为什么需要它】`deps.SessionStoreStub` 按 JSON 形状存 dict（`sessionId` / `name`…），
    而 `MentionSearchService` / `ContextRoots` 是照 Java 的 `Session` record 写的
    （`session_id` / `workspace_id` / `display_name()` / `created_at.timestamp()`）。
    只做形状转换，不含任何会话业务逻辑；真实 `SessionManager` 装进来之后本类不参与
    （对象原样透传给检索服务）。
    """

    __slots__ = ("_raw",)

    def __init__(self, raw: dict[str, Any]) -> None:
        self._raw = raw

    @property
    def session_id(self) -> str:
        return str(self._raw.get("sessionId") or "")

    @property
    def workspace_id(self) -> str | None:
        value = self._raw.get("workspaceId")
        return None if value is None else str(value)

    @property
    def mode(self) -> str:
        return str(self._raw.get("mode") or "STANDARD")

    @property
    def created_at(self) -> _dt.datetime | None:
        return parse_created_at(self._raw.get("createdAt"))

    @property
    def name(self) -> str | None:
        value = self._raw.get("name")
        return None if value is None else str(value)

    def display_name(self) -> str:
        """界面展示用：有名字用名字，没有就退回 ID 前缀（与 Java `Session.displayName()` 一字不差）。"""
        name = self.name
        if name is not None and name.strip() != "":
            return name
        sid = self.session_id or "?"
        return "会话 " + (sid[:8] if len(sid) > 8 else sid)


class _SessionManagerView:
    """会话管理器的读取面：窄桩返回 dict 就包一层，真实实现原样透传。

    # 依赖：lionbox.sessions（由并行任务提供）

    只转发检索真正用到的 `get_session` / `get_all_sessions`，其余方法（建/删/改名…）
    由 `__getattr__` 直通 —— 接口层不替 sessions 模块实现业务逻辑。
    """

    __slots__ = ("_inner",)

    def __init__(self, inner: Any) -> None:
        self._inner = inner

    def get_session(self, session_id: str | None) -> Any:
        return _as_session(self._inner.get_session(session_id))

    def get_all_sessions(self) -> list[Any]:
        return [_as_session(s) for s in self._inner.get_all_sessions()]

    def __getattr__(self, name: str) -> Any:
        return getattr(self._inner, name)


def _as_session(session: Any) -> Any:
    return _DictSession(session) if isinstance(session, dict) else session


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class ContextApi:
    """`/api/context/*` 的处理器（Java 侧只有 `GET /mentions` 一个动作）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 依赖装配
    def sessions(self) -> _SessionManagerView:
        """会话管理器（装配方可替换的服务，见 deps.py 的服务名清单）。"""
        return _SessionManagerView(deps.sessions(self.ctx))

    def conversation_history(self) -> Any:
        """对话历史（真实实现：读 `~/lion-code-workspace/.lioncode/conversations/*.json`）。

        `auto_load=True` 与 Java 一致：Java 的 `ConversationHistory.init()` 启动时就把
        磁盘上的历史全读进内存，`detail` 里的"N 条消息 · 首条用户消息"才和 Java 相同。
        """
        return self.ctx.service("conversation_history",
                                lambda: ConversationHistory(auto_load=True))

    def skill_repository(self) -> Any:
        """技能仓库（进程内单例；装配方可 `ctx.install("skill_repository", repo)` 换掉）。"""
        return self.ctx.service("skill_repository", default_repository)

    def search_service(self) -> MentionSearchService:
        """`@` 候选检索服务。

        【为什么不复用 `deps.mentions()`】那一个是**展开器**（`MentionResolver`：把消息里的
        `@file:x` 换成文件内容，服务名 `mentions`）；这里要的是**检索**服务
        （`MentionSearchService`：给前端弹候选）。Java 侧同样是两个类，不能混用。

        【为什么每次请求现场装配、不缓存服务对象】构造它只是存几个引用（真正的重活
        ——扫技能目录、读对话历史——都在被引用服务自己的懒加载里），而 `sessions` /
        `workspaces` 是装配方可替换的服务：缓存住旧引用会让"装配方后装真实会话管理器"
        永远不生效（窄桩返回 dict、真实实现返回对象，形状还不一样）。
        装配方显式 `ctx.install("mention_search", 真实对象)` 时以它的为准。
        """
        if self.ctx.has("mention_search"):
            return self.ctx.service("mention_search", self._build_search_service)
        return self._build_search_service()

    def _build_search_service(self) -> MentionSearchService:
        sessions = self.sessions()
        return MentionSearchService(
            session_manager=sessions,
            conversation_history=self.conversation_history(),
            skill_repository=self.skill_repository(),
            roots=ContextRoots(sessions, deps.workspaces(self.ctx)),
        )

    # ------------------------------------------------------------ 注册
    def register__api_context(self, router) -> None:
        api = self

        @router.get("/api/context/mentions")
        def mentions(req: Request):
            try:
                limit = parse_limit(req.q("limit"))
            except ValueError:
                # Java 里这行根本进不到方法体：Spring 绑定 `Integer` 失败直接回 400 +
                # 默认错误体 `{"timestamp","status","error","path"}`。状态码语义不同
                # （400 vs 200+业务错误），必须照样复刻。
                return deps.spring_error(400, req.path)

            q = req.q("q")
            kind = req.q("kind")
            result = api.search_service().search(q=q, kind=kind, root=req.q("root"),
                                                session_id=req.q("sessionId"), limit=limit)

            counts = {"file": count_of(result.items, "file"),
                      "history": count_of(result.items, "history"),
                      "skill": count_of(result.items, "skill")}
            fields: dict[str, Any] = {
                "items": [item.to_dict() for item in result.items],
                # 下面三个回显的是**原样的请求参数**（Java：`q == null ? "" : q`），
                # 不是检索内部 trim/lower 之后的关键词：`?q=%20%20` 回的就是 "  "。
                "q": "" if q is None else q,
                "kind": "all" if kind is None or kind.strip() == "" else kind,
                "root": result.root,
                "limit": DEFAULT_LIMIT__api_context if limit is None or limit <= 0 else min(limit, MAX_LIMIT__api_context),
                "truncated": result.truncated,
                "elapsedMs": result.elapsedMs,
                "scannedFiles": result.scannedFiles,
                "counts": counts,
            }
            if result.note is not None:
                fields["note"] = result.note
            return Response.json(ok(fields))


def register__api_context(router, ctx) -> None:
    ContextApi(ctx).register__api_context(router)


# ========================================================================
# 原模块 lionbox/api/questions.py
# ========================================================================
"""提问接口 —— `/api/questions/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\QuestionController.java`
（84 行 / 3 个接口）。

Java 里的流程：模型调 `ask_user` → 后端登记一条待回答的问题并阻塞等待
→ 前端在处理期间轮询 `GET /api/questions/pending` 看到问题、弹出输入框
→ 用户填完 `POST /api/questions/answer` → 后端放行，答案回到模型。

# 依赖：lionbox.misc.question（提问服务，已就绪；缺了退 deps 窄桩，见 default_question_service）
# 依赖：lionbox.sessions（会话存在性检查，由并行任务提供；未装配时是 deps 的内存窄桩）

【逐字段对齐的四处细节（都是实测出来的，不能凭感觉写）】
1. 文案逐字照抄 Java：`会话不存在: <id>`、`缺少 questionId`、`回答不能为空`、
   `这个问题已经超时或已被取消，请等模型下一步的反应`；`/answer` 成功时 message 是
   `"已回答"`（不是默认的"操作成功"），data 里的 questionId 是**原样**（未 trim）而
   answer 是 trim 过的。
2. `/pending` 的 data 是 Java `UserQuestionService.toMap(Pending)` 的形状：
   `id / sessionId / question / options / askedAt / timeoutSeconds / deadlineAt`；
   `askedAt`、`deadlineAt` 是**毫秒**时间戳。前端读的是 `q.id`（见 `web/index.html`
   的 `pollQuestion`），不是 `questionId` —— 窄桩里的字段名与它不同，所以要归一。
   没有待答问题时 Java 是 `orElse(null)`，data 因 `ApiResponse` 的 NON_NULL **整个省略**。
3. `/pending` 缺 `sessionId` 查询参数是 **400**（Spring 的必填参数校验，方法体都不进），
   而 `sessionId=`（空串）是 200 + `会话不存在: ` —— 两者必须分开处理。
4. 请求体的校验顺序与 `String.trim()` / `String.isBlank()` 的语义照抄 Java：
   只有 ` <= U+0020` 的字符算可 trim，`U+3000` 之类不算；`isBlank()` 也不认 `U+00A0`。
   实测：`answer="　"`（全角空格）→ Java 回"已超时或已被取消"，不是"回答不能为空"。
"""


import dataclasses
import datetime as _dt
import logging
import time
import unicodedata
from typing import Any

from lionbox.api import deps

log__api_questions = logging.getLogger("lionbox.api.questions")

# --------------------------------------------------------------------------
# Java 字符串语义（Spring 的校验分支完全建立在这两个方法上）
# --------------------------------------------------------------------------

#: Java `String.trim()`：只去掉**码点 <= U+0020** 的首尾字符。
#: 不能用 `str.strip()` —— 它连 U+3000（全角空格）一起去掉，于是 `answer="　"`
#: 在 Java 是"非空"（实测走服务层回"已超时或已被取消"），Python 会错回"回答不能为空"。
_JAVA_TRIM_CHARS = "".join(chr(c) for c in range(0x21))

#: Java `Character.isWhitespace` 认的空白（`isBlank()` 就是"每个字符都是它"）。
#: 注意三个不换行空格 U+00A0 / U+2007 / U+202F 在 Java 里**不算**空白，
#: 而 Python 的 `str.isspace()` 认它们 —— 实测 NBSP 的 questionId 在 Java 会走到服务层。
_JAVA_WS_CHARS = "\t\n\x0b\f\r\x1c\x1d\x1e\x1f"
_JAVA_NON_WS_SPACES = "\u00a0\u2007\u202f"


def java_trim(text: str) -> str:
    """Java `String.trim()` 的等价物。"""
    return text.strip(_JAVA_TRIM_CHARS)


def java_is_blank(text: str) -> bool:
    """Java `String.isBlank()` 的等价物。"""
    for ch in text:
        if ch in _JAVA_NON_WS_SPACES:
            return False
        if ch not in _JAVA_WS_CHARS and unicodedata.category(ch) not in ("Zs", "Zl", "Zp"):
            return False
    return True


# --------------------------------------------------------------------------
# 请求体 / 待答问题的取值（Jackson 与 Java record 的语义）
# --------------------------------------------------------------------------


def _scalar_text(value: Any) -> str | None:
    """Jackson 把 JSON 标量绑到 `String` 的结果（Java `AnswerRequest.questionId/answer`）。

    null → None；字符串原样；数字 → `str`；布尔 → `"true"` / `"false"`（Java 的
    `Boolean.toString` 是小写，Python 的 `str(True)` 是 `"True"`，所以要单独处理）。
    数组 / 对象在 Java 是**反序列化阶段**就 400，调用方（`_request_body`）先拦掉。
    """
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _request_body(req: Request) -> dict[str, Any] | None:
    """Spring `@RequestBody AnswerRequest` 的等价解析；None 表示 Java 会直接回 400。

    实测（18099）：空体、非法 JSON、`null`、`[]`、`123`、`"abc"` 全是 400 ——
    只要不是 JSON 对象，方法体根本进不去（所以控制器里那句 `request == null` 是死代码）。
    """
    if not req.body:
        return None
    parsed = req.json
    return parsed if isinstance(parsed, dict) else None


# 窄桩（deps.QuestionServiceStub）与真实实现（misc.question）的字段名不同，这里都认。
_PENDING_ID_KEYS = ("id", "questionId", "question_id")
_PENDING_SESSION_KEYS = ("sessionId", "session_id")
_PENDING_ASKED_KEYS = ("askedAt", "asked_at", "createdAt", "created_at")
_PENDING_TIMEOUT_KEYS = ("timeoutSeconds", "timeout_seconds")


def _fields_of(pending: Any) -> dict[str, Any]:
    """把一条待答问题摊成字段字典：真实实现是 dataclass（`Pending`），窄桩是 dict。"""
    if isinstance(pending, dict):
        return dict(pending)
    if dataclasses.is_dataclass(pending) and not isinstance(pending, type):
        return dataclasses.asdict(pending)
    attrs = getattr(pending, "__dict__", None)
    if isinstance(attrs, dict):
        return dict(attrs)
    raise TypeError(f"待答问题的结构无法读取: {type(pending).__name__}")


def _first(fields: dict[str, Any], *names: str) -> Any:
    """取第一个有值的字段（字段改名/驼峰差异时的兼容取值）。"""
    for name in names:
        value = fields.get(name)
        if value is not None:
            return value
    return None


def _epoch_ms(value: Any) -> int:
    """提问时刻 → Java `Pending.askedAt` 的毫秒时间戳。

    真实实现存的就是毫秒（`misc.question` 的 `_now_ms`），窄桩存的是 `Instant` 字符串
    （`deps.now_instant()`，如 `2026-10-03T11:55:28.690Z`），两种都要认。
    取不到合法时间戳时用当前时刻兜底并告警：`askedAt` 只是界面倒计时的起点，
    不能因为它缺失就让前端连问题本身都拿不到（Java 的 Pending 一定有值）。
    """
    if isinstance(value, bool) or value is None:
        return int(time.time() * 1000)
    if isinstance(value, (int, float)):
        number = float(value)
        return int(number) if number >= 1e11 else int(number * 1000)   # 毫秒 / 秒
    try:
        stamp = _dt.datetime.fromisoformat(str(value))
    except ValueError:
        log__api_questions.warning("提问时间戳无法解析（%r），用当前时刻兜底", value)
        return int(time.time() * 1000)
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=_dt.timezone.utc)
    return int(stamp.timestamp() * 1000)


def _timeout_of(svc: Any, fields: dict[str, Any]) -> int:
    """本次提问的等待上限（秒）。Java 侧由 `Pending.timeoutSeconds` 记录，取不到就问服务。"""
    raw = _first(fields, *_PENDING_TIMEOUT_KEYS)
    if raw is None:
        raw = getattr(svc, "default_timeout_seconds", None)          # 真实实现
    if raw is None:
        raw = getattr(svc, "DEFAULT_TIMEOUT_SECONDS", None)          # 窄桩
    return deps.as_int(raw, deps.QuestionServiceStub.DEFAULT_TIMEOUT_SECONDS)


def _pending_map(svc: Any, pending: Any) -> dict[str, Any]:
    """Java `UserQuestionService.toMap(Pending)` 的等价物（字段名 / 单位 / 顺序一致）。

    【为什么要归一】真实实现返回 `Pending` dataclass（`id` / `asked_at`），deps 的窄桩
    返回 `questionId` / `createdAt` 形状的 dict；前端只认 Java 的 `toMap` 字段名
    （`web/index.html` 读 `q.id` / `q.question` / `q.options`），所以在这里统一。
    """
    fields = _fields_of(pending)
    asked_at = _epoch_ms(_first(fields, *_PENDING_ASKED_KEYS))
    timeout = _timeout_of(svc, fields)
    options = _first(fields, "options")
    return {
        "id": deps.as_str(_first(fields, *_PENDING_ID_KEYS)),
        "sessionId": deps.as_str(_first(fields, *_PENDING_SESSION_KEYS)),
        "question": _scalar_text(_first(fields, "question")),
        "options": [deps.as_str(o) for o in options] if isinstance(options, (list, tuple)) else [],
        "askedAt": asked_at,
        "timeoutSeconds": timeout,
        "deadlineAt": asked_at + timeout * 1000,
    }


# --------------------------------------------------------------------------
# 服务装配
# --------------------------------------------------------------------------


def default_question_service() -> Any:
    """提问服务的默认实现。

    优先级：装配方 `ctx.install("questions", ...)` 装进来的真实对象 > 本函数。
    本函数优先用 `lionbox.misc.question.UserQuestionService` —— 它就是 Java controller
    注入的那个类（`core/question/UserQuestionService`）的移植，`ask_user` 工具走的也是它；
    只有该模块缺失时才退回 `deps.QuestionServiceStub`（内存窄桩，问与答只在进程内自洽）。

    # 依赖：lionbox.misc.question（真实实现，已就绪）
    # 依赖：lionbox.agent（提问服务的真实装配由并行任务负责，装配方 install 即可覆盖）
    """
    try:
        from lionbox.misc.question import UserQuestionService
    except ImportError as e:        # 只有模块真的缺失才退窄桩，其它异常照常抛出
        log__api_questions.warning("lionbox.misc.question 不可用（%s），提问服务退回内存窄桩", e)
        return deps.QuestionServiceStub()
    return UserQuestionService()


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class QuestionsApi:
    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ---- 依赖 ----
    def _service(self) -> Any:
        """跨模块共享的提问服务实例（`ask_user`、会话停止时的取消用的是同一个）。"""
        return self.ctx.service("questions", default_question_service)

    def _session_exists(self, session_id: str) -> bool:
        """Java `sessionManager.getSession(sessionId).isEmpty()`。

        会话管理由并行任务提供（真实的 `lionbox.sessions.SessionManager` 只要被
        `ctx.install("sessions", ...)` 装进来就走它）；没装配时是 `deps` 的内存窄桩。
        """
        return deps.sessions(self.ctx).get_session(session_id) is not None

    # ---- 注册 ----
    def register__api_questions(self, router) -> None:
        api = self

        @router.get("/api/questions/pending")
        def pending(req: Request):
            session_id = req.q("sessionId")
            if session_id is None:
                # Spring：@RequestParam("sessionId") 是必填的，缺了连方法体都不进 → 400
                return deps.spring_error(400, req.path)
            if not api._session_exists(session_id):
                return ApiResponse.error(f"会话不存在: {session_id}")
            svc = api._service()
            item = svc.pending_of(session_id)
            # 没有待答问题时 data 是 null → NON_NULL 把整个 data 省略（前端据此收起输入框）
            return ApiResponse.ok(_pending_map(svc, item) if item is not None else None)

        @router.post("/api/questions/answer")
        def answer(req: Request):
            body = _request_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            if any(isinstance(body.get(key), (list, dict)) for key in ("questionId", "answer")):
                # Jackson 无法把数组/对象绑到 String：反序列化阶段就 400（实测）
                return deps.spring_error(400, req.path)

            question_id = _scalar_text(body.get("questionId"))
            if question_id is None or java_is_blank(question_id):
                return ApiResponse.error("缺少 questionId")
            answer_text = java_trim(_scalar_text(body.get("answer")) or "")
            if not answer_text:
                return ApiResponse.error("回答不能为空")
            if not api._service().answer(question_id, answer_text):
                return ApiResponse.error("这个问题已经超时或已被取消，请等模型下一步的反应")
            # data 里的 questionId 是请求里的原样值（Java 没 trim），answer 是 trim 过的
            return ApiResponse.ok({"questionId": question_id, "answer": answer_text}, "已回答")

        @router.get("/api/questions/stats")
        def stats(req: Request):
            return ApiResponse.ok({"pending": api._service().pending_count()})


def register__api_questions(router, ctx) -> None:
    QuestionsApi(ctx).register__api_questions(router)


# ========================================================================
# 原模块 lionbox/misc/question.py
# ========================================================================
"""向用户提问的服务。

【契约来源】逐项对照 Java 版 `core/question/UserQuestionService.java`：
三种结束方式（用户回答 / 超时 / 会话被中止）、默认 300 秒、400ms 轮询、
"取消必须能和超时区分开"的判定顺序、以及三段直接回给模型看的文案全部照抄。

模型调 `ask_user` 工具时，实际是走这里：
  1. 把问题登记成"待回答"，前端轮询 `GET /api/questions/pending` 就能看到并弹出输入框；
  2. 工具所在线程**阻塞等待**（最多 timeout_seconds 秒），等用户在界面上回答；
  3. 用户 `POST /api/questions/answer` 提交后，事件放行，答案作为工具结果回到模型。

为什么可以阻塞：AgentLoop 跑在会话自己的 worker 线程上，同一个会话本来就串行，
等用户回答不会拖住别的会话。
"""


import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

#: 默认等待时长（秒）。要比聊天接口那边 10 分钟的等待上限小得多。
DEFAULT_TIMEOUT_SECONDS = 300

#: 轮询间隔：等待期间用它定期醒来，检查问题是否被取消。
POLL_SECONDS = 0.4


class Status:
    """提问的结束状态。"""

    ANSWERED = "ANSWERED"
    TIMEOUT = "TIMEOUT"
    CANCELLED = "CANCELLED"

    ALL = (ANSWERED, TIMEOUT, CANCELLED)


@dataclass(frozen=True)
class Pending:
    """一条待回答的问题。"""

    id: str                       # noqa: A003
    session_id: str
    question: str
    options: list[str] = field(default_factory=list)
    asked_at: int = 0
    #: 最多等多久（秒）。界面上可以据此显示倒计时。
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS


@dataclass(frozen=True)
class Result__misc_question:
    """提问结果。

    :param status: 结束状态
    :param answer: 用户答案（仅 ANSWERED 时有值）
    :param text:   直接回给模型看的文本
    """

    status: str
    answer: str | None
    text: str


class _Waiter:
    """一次提问的等待状态。"""

    __slots__ = ("event", "answer", "cancelled")

    def __init__(self) -> None:
        self.event = threading.Event()
        self.answer: str | None = None
        self.cancelled = False


class UserQuestionService:
    """待回答问题的登记 / 等待 / 取消。"""

    def __init__(self, default_timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS) -> None:
        self.default_timeout_seconds = int(default_timeout_seconds)
        self._pending: dict[str, Pending] = {}
        self._waiters: dict[str, _Waiter] = {}
        self._lock = threading.RLock()

    # ------------------------------------------------------------------
    # 提问（阻塞）
    # ------------------------------------------------------------------
    def ask(self, session_id: str, question: str, options: list[str] | None = None,
            timeout_seconds: int = 0) -> Result__misc_question:
        """提问并等用户回答（阻塞）。

        :param session_id:      会话 ID
        :param question:        问题正文
        :param options:         可选项；为空表示让用户自由输入
        :param timeout_seconds: 最长等待秒数（<=0 用默认值）
        """
        timeout = int(timeout_seconds) if timeout_seconds and timeout_seconds > 0 \
            else self.default_timeout_seconds
        question_id = str(uuid.uuid4()).replace("-", "")[:12]
        opts = list(options) if options else []

        pending = Pending(question_id, session_id, question, opts, _now_ms(), timeout)
        waiter = _Waiter()
        with self._lock:
            self._pending[question_id] = pending
            self._waiters[question_id] = waiter
        print(f"[提问] 向用户提问: 会话={session_id}, 问题={_abbreviate(question)}, "
              f"选项={opts}, 等待上限={timeout}秒", flush=True)

        try:
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                if waiter.event.wait(POLL_SECONDS):
                    break                       # 用户答了，或被取消（下面统一判断）
                if waiter.cancelled:
                    return self._cancelled(session_id, question_id)
            # 【为什么这里还要再判一次 cancelled】`cancel_session()` 是先置 cancelled
            # 再 set 事件，wait 会立刻返回 True 从而 break 出循环 —— 只在循环里判的话，
            # 被取消的提问永远走不到 CANCELLED 分支，而是被当成"等满 N 秒没人回答"，
            # 回给模型一句"请基于现有信息继续"。用户明明点了停止，模型却继续干活。
            if waiter.cancelled:
                return self._cancelled(session_id, question_id)
            if waiter.answer is not None and waiter.answer.strip():
                print(f"[提问] 用户已回答: 会话={session_id}, 问题ID={question_id}, "
                      f"答案={_abbreviate(waiter.answer)}", flush=True)
                return Result__misc_question(Status.ANSWERED, waiter.answer, waiter.answer)
            print(f"[提问] 等待用户回答超时: 会话={session_id}, 问题ID={question_id}", flush=True)
            return Result__misc_question(Status.TIMEOUT, None,
                          f"（用户 {timeout} 秒内没有回答。请不要再重复提问，"
                          "先基于现有信息给出你能做的部分，并在回复里说明还缺什么。）")
        finally:
            with self._lock:
                self._pending.pop(question_id, None)
                self._waiters.pop(question_id, None)

    def _cancelled(self, session_id: str, question_id: str) -> Result__misc_question:
        """取消时的统一返回（超时/取消的文案必须能区分，否则模型会误以为还能继续）。"""
        print(f"[提问] 提问已取消: 会话={session_id}, 问题ID={question_id}", flush=True)
        return Result__misc_question(Status.CANCELLED, None,
                      "（提问已取消：会话被中止。请不要继续执行，直接停下来等用户下一步指示。）")

    # ------------------------------------------------------------------
    # 回答 / 查询 / 取消
    # ------------------------------------------------------------------
    def answer(self, question_id: str | None, answer: str | None) -> bool:
        """用户提交回答；返回是否命中了一个正在等待的问题。"""
        if question_id is None or not str(question_id).strip():
            return False                            # dict.get(None) 在 Java 会抛，这里直接挡掉
        with self._lock:
            waiter = self._waiters.get(str(question_id))
        if waiter is None:
            return False                            # 超时过了或者 ID 不对
        waiter.answer = "" if answer is None else str(answer).strip()
        waiter.event.set()
        return True

    def pending_of(self, session_id: str | None) -> Pending | None:
        """取某会话当前待回答的问题（前端轮询用）。"""
        if session_id is None:
            return None
        with self._lock:
            for pending in self._pending.values():
                if pending.session_id == session_id:
                    return pending
        return None

    def pending_list(self) -> list[Pending]:
        """全部待回答的问题（`GET /api/questions/pending` 不带会话时用）。"""
        with self._lock:
            return list(self._pending.values())

    def cancel_session(self, session_id: str | None) -> int:
        """取消某会话上所有等待中的提问（会话被手动停止时调用，别让 worker 线程一直挂着）。

        :return: 取消掉的条数
        """
        if session_id is None:
            return 0
        count = 0
        with self._lock:
            targets = [p for p in self._pending.values() if p.session_id == session_id]
        for pending in targets:
            with self._lock:
                waiter = self._waiters.get(pending.id)
            if waiter is not None:
                waiter.cancelled = True
                waiter.event.set()
                count += 1
        if count > 0:
            print(f"[提问] 已取消会话 {session_id} 上 {count} 个等待中的提问", flush=True)
        return count

    def pending_count(self) -> int:
        """当前待回答总数（诊断用）。"""
        with self._lock:
            return len(self._pending)

    def to_map(self, pending: Pending) -> dict[str, Any]:
        """给前端的状态快照（字段名与 Java `toMap` 一致）。"""
        return {
            "id": pending.id,
            "sessionId": pending.session_id,
            "question": pending.question,
            "options": list(pending.options),
            "askedAt": pending.asked_at,
            "timeoutSeconds": pending.timeout_seconds,
            "deadlineAt": pending.asked_at + pending.timeout_seconds * 1000,
        }


def _abbreviate(text: str | None) -> str:
    if text is None:
        return ""
    flat = " ".join(str(text).split())
    return flat if len(flat) <= 60 else flat[:60] + "…"


def _now_ms() -> int:
    return int(time.time() * 1000)


__all__ = ["DEFAULT_TIMEOUT_SECONDS", "POLL_SECONDS", "Pending", "Result", "Status",
           "UserQuestionService"]


# ========================================================================
# 原模块 lionbox/misc/sound.py
# ========================================================================
"""音效提醒（任务完成 / 需要审批 / 任务出错 / 模型提问）。

【契约来源】逐项对照 Java 版 `core/sound/SoundNotifier.java`：
配置键与默认值、四种音效、节流（每种音效各自计时）、音量换算、
"绝不抛异常 / 绝不阻塞调用方 / 配置每次播放前读一次"三条硬约束全部照抄。

三条硬约束（Java 注释里的原话，同样适用）：
  1. **绝不抛异常**。这是锦上添花的功能，开关关着、文件缺了、声卡不支持、
     音频线路被占用……一律静静跳过，只记 debug 日志，绝不影响主流程。
  2. **绝不阻塞调用方**。AgentLoop 在跑主循环，播放必须丢到守护线程里异步出声。
  3. **配置每次播放前读一次**，这样用户在设置里一改就立刻生效，不用重启。

【Python 侧怎么出声】Java 用 `javax.sound`（进程内播放）。Python 标准库里唯一能出声的
是 Windows 的 `winsound`（`SND_FILENAME | SND_ASYNC` 正好是"异步、不阻塞"），
所以：Windows 上走 `winsound`；其它平台没有标准库音频能力（不允许引第三方依赖），
就按"资源/设备不可用"降级 —— 只记一条日志，功能静默失效，和 Java 在无声卡机器上的表现一致。
"""


import os
import sys
import threading
import time
from pathlib import Path
from typing import Any


#: 声音资源相对目录（Java 的 classpath 路径是 `/static/sounds/<file>`）
SOUND_SUBDIR = ("static", "sounds")

#: 显式指定音效目录（便携版/测试用）
ENV_SOUNDS_DIR = "LIONBOX_SOUNDS_DIR"

#: 缓存里"没查过"的哨兵（None 表示"查过了，资源不存在"）
_MISSING = object()

#: 播放时落盘的 WAV 缓存目录名（`winsound` 只认文件名，不认内存里的字节）
_WAV_CACHE_DIRNAME = "lionbox-sounds"


class Kind:
    """提示音种类（Java 枚举 `Kind`，带文件名与对应的配置开关字段）。"""

    DONE = "DONE"
    APPROVAL = "APPROVAL"
    QUESTION = "QUESTION"
    ERROR = "ERROR"

    ALL = (DONE, APPROVAL, QUESTION, ERROR)

    #: 种类 -> (文件名, 配置键)
    SPEC = {
        DONE: ("done.wav", "soundDone"),
        APPROVAL: ("approval.wav", "soundApproval"),
        QUESTION: ("question.wav", "soundQuestion"),
        ERROR: ("error.wav", "soundError"),
    }

    DISPLAY = {DONE: "任务完成", APPROVAL: "需要审批", QUESTION: "模型提问", ERROR: "任务出错"}

    @staticmethod
    def parse(raw: Any) -> str | None:
        v = str(raw or "").strip().upper()
        return v if v in Kind.SPEC else None

    @staticmethod
    def file_name(kind: str) -> str:
        return Kind.SPEC.get(kind, ("", ""))[0]

    @staticmethod
    def config_key(kind: str) -> str:
        return Kind.SPEC.get(kind, ("", ""))[1]


class SoundNotifier:
    """音效提醒（配置存在 `AppConfigStore` 的 `notification` 键下）。"""

    #: 配置键
    CONFIG_KEY = "notification"

    #: 缺省值
    DEFAULT_ENABLED = True
    DEFAULT_VOLUME = 80
    DEFAULT_MIN_INTERVAL_MS = 800

    def __init__(self, config_store: AppConfigStore | None = None,
                 sounds_dir: str | Path | None = None) -> None:
        self.config_store = config_store if config_store is not None else AppConfigStore()
        self._sounds_dir_override = Path(sounds_dir) if sounds_dir else None
        self._lock = threading.RLock()
        #: 每种音效上次播放的时间戳，用于节流
        self._last_played_at: dict[str, float] = {}
        #: WAV 字节缓存：读一次就够了，不必每次播放都读
        self._sound_cache: dict[str, bytes | None] = {}
        #: 实际发起播放的次数（自测用）
        self._started_count = 0
        #: 播放失败/降级的记录（自测与诊断用；Java 只记 debug 日志）
        self.degraded: list[str] = []

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------
    def play(self, kind: str | None) -> None:
        """播放提示音（AgentLoop 的触发点调用）：严格按配置过一遍开关、音量、节流。"""
        self._emit(kind, preview=False)

    def preview(self, kind: str | None) -> None:
        """试听（设置界面的"试听"按钮）：不过总开关也不过节流，但仍尊重音量。"""
        self._emit(kind, preview=True)

    def is_enabled(self) -> bool:
        """总开关当前是否打开。"""
        return bool_of(self._config(), "enabled", self.DEFAULT_ENABLED)

    def started_count(self) -> int:
        """实际发起播放的次数（自测断言用）。"""
        with self._lock:
            return self._started_count

    def sound_bytes(self, kind: str | None) -> bytes | None:
        """读某个音效的原始字节（自测断言用，顺便能确认资源真的在）。"""
        return None if kind is None else self._load_sound(kind)

    def sounds_dir(self) -> Path | None:
        """当前解析到的音效目录（找不到返回 None）。"""
        if self._sounds_dir_override is not None:
            return self._sounds_dir_override if self._sounds_dir_override.is_dir() else None
        override = os.environ.get(ENV_SOUNDS_DIR, "").strip()
        if override:
            candidate = Path(override)
            return candidate if candidate.is_dir() else None
        for candidate in self._candidates():
            if candidate.is_dir():
                return candidate
        return None

    @staticmethod
    def with_defaults(raw: dict[str, Any] | None) -> dict[str, Any]:
        """把用户存的配置补全成完整结构（`GET /api/notification` 用）。"""
        source = raw if isinstance(raw, dict) else {}
        return {
            "enabled": bool_of(source, "enabled", SoundNotifier.DEFAULT_ENABLED),
            "soundDone": bool_of(source, "soundDone", True),
            "soundApproval": bool_of(source, "soundApproval", True),
            "soundQuestion": bool_of(source, "soundQuestion", True),
            "soundError": bool_of(source, "soundError", True),
            "volume": clamp(int_of__misc_sound(source, "volume", SoundNotifier.DEFAULT_VOLUME), 0, 100),
            "minIntervalMs": max(0, int_of__misc_sound(source, "minIntervalMs",
                                           SoundNotifier.DEFAULT_MIN_INTERVAL_MS)),
        }

    # ------------------------------------------------------------------
    # 内部实现
    # ------------------------------------------------------------------
    def _emit(self, kind: str | None, preview: bool) -> None:
        """统一入口；`preview=True` 时跳过开关与节流。"""
        if kind is None or kind not in Kind.SPEC:
            return
        try:
            cfg = self._config()
            if not preview:
                if not bool_of(cfg, "enabled", self.DEFAULT_ENABLED):
                    return                                   # 总开关关着
                if not bool_of(cfg, Kind.config_key(kind), True):
                    return                                   # 这一类关着

            volume = clamp(int_of__misc_sound(cfg, "volume", self.DEFAULT_VOLUME), 0, 100)
            if volume <= 0:
                return                                       # 静音

            if not preview and not self._allow_by_throttle(
                    kind, max(0, int_of__misc_sound(cfg, "minIntervalMs", self.DEFAULT_MIN_INTERVAL_MS))):
                return                                       # 太密了，跳过

            wav = self._load_sound(kind)
            if not wav:
                self._degrade(f"提示音资源缺失，跳过: {Kind.file_name(kind)}")
                return
            self._start_async(kind, wav, volume)
        except Exception as t:
            # 兜底：声音相关的一切问题都不该影响主流程
            self._degrade(f"播放提示音失败（忽略）: {t}")

    def _allow_by_throttle(self, kind: str, min_interval_ms: int) -> bool:
        """节流：每种音效各自计时，距上次播放不足间隔就跳过。

        用锁 + 记时间戳，避免同一时刻并发触发时叠在一起响。
        """
        if min_interval_ms <= 0:
            return True
        now = _now_ms__misc_sound()
        with self._lock:
            previous = self._last_played_at.get(kind)
            if previous is not None and now - previous < min_interval_ms:
                return False
            self._last_played_at[kind] = now
            return True

    def _start_async(self, kind: str, wav: bytes, volume: int) -> None:
        """守护线程里异步播放（绝不阻塞调用方）。"""

        def worker() -> None:
            try:
                if not _play_wav(wav, Kind.file_name(kind), volume):
                    self._degrade(f"音频设备不可用或系统不支持，跳过播放 {Kind.file_name(kind)}")
                    return
                with self._lock:
                    self._started_count += 1
            except Exception as e:                            # 播放线程里的异常绝不外泄
                self._degrade(f"播放异常，跳过 {Kind.file_name(kind)}: {e}")

        thread = threading.Thread(target=worker, name="lion-sound", daemon=True)
        thread.start()

    def _load_sound(self, kind: str) -> bytes | None:
        """读 WAV 字节，读到的缓存起来。"""
        cached = self._sound_cache.get(kind, _MISSING)
        if cached is not _MISSING:
            return cached
        file = Kind.file_name(kind)
        data: bytes | None = None
        directory = self.sounds_dir()
        if directory is not None:
            path = directory / file
            try:
                if path.is_file():
                    data = path.read_bytes()
            except OSError as e:
                self._degrade(f"读取提示音资源失败: {path} - {e}")
        with self._lock:
            self._sound_cache[kind] = data
        return data

    def _candidates(self) -> list[Path]:
        """音效目录的候选位置（和技能目录一样多找几个地方：工作目录各不相同）。"""
        out: list[Path] = []

        def add(base: Path) -> None:
            out.append(base.joinpath(*SOUND_SUBDIR))

        here = _safe_resolve(Path(_ORIG_FILE_misc_sound))
        if here is not None:
            # misc/sound.py -> misc -> lionbox -> python -> <项目/安装根>
            for index in (3, 2, 1):
                if len(here.parents) > index:
                    base = here.parents[index]
                    add(base)
                    add(base / "resources")
                    add(base / "src" / "main" / "resources")
            if len(here.parents) > 3:
                # 安装目录布局：<安装根>/dist/static/sounds
                out.append(here.parents[3] / "dist" / "static" / "sounds")
        executable = _safe_resolve(Path(sys.executable))
        if executable is not None:
            add(executable.parent)
        add(Path.cwd())
        return out

    def _config(self) -> dict[str, Any]:
        """读一次配置（AppConfigStore 本身是内存里的 map，开销可忽略）。"""
        raw = self.config_store.get(self.CONFIG_KEY, None)
        return raw if isinstance(raw, dict) else {}

    def _degrade(self, message: str) -> None:
        """记一条降级原因（不抛异常，也不静默 —— 排查时看得见）。"""
        with self._lock:
            if len(self.degraded) < 100:
                self.degraded.append(message)


# --------------------------------------------------------------------------
# 静态小工具（NotificationController 与自测共用；与 Java 同名同语义）
# --------------------------------------------------------------------------


def bool_of(cfg: dict[str, Any], key: str, default: bool) -> bool:
    """宽松读布尔：兼容存成 true / "true" 的情况。"""
    value = cfg.get(key)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in ("true", "1", "yes", "是", "开")
    return default


def int_of__misc_sound(cfg: dict[str, Any], key: str, default: int) -> int:
    """宽松读整数：兼容存成数字 / 字符串的情况。"""
    value = cfg.get(key)
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return default
    return default


def clamp(value: int, minimum: int, maximum: int) -> int:
    """把值夹到 [min, max]。"""
    return max(minimum, min(maximum, value))


# --------------------------------------------------------------------------
# 播放后端
# --------------------------------------------------------------------------


def _play_wav(wav: bytes, file_name: str, volume: int) -> bool:
    """播放一段 WAV；返回是否真的发起了播放。

    Windows：`winsound`（标准库）—— 先把字节落到一个固定的临时缓存目录再异步播放，
    因为 `winsound.PlaySound` 只认文件名/资源，不认内存里的字节。用固定目录（而不是
    每次 mkstemp）是为了**不泄漏临时文件**：四个音效各一份，写完就一直复用。

    【音量】`winsound` 不能设增益（Java 用 `FloatControl.MASTER_GAIN`）。
    音量已经在上层用于"0 = 静音"的判定；这里如实说明差异，不做假实现。

    非 Windows / 没有音频设备时返回 False，上层记一条降级原因（功能静默失效）。
    """
    if sys.platform != "win32":
        return False
    try:
        import tempfile
        import winsound
    except ImportError:
        return False
    try:
        directory = Path(tempfile.gettempdir()) / _WAV_CACHE_DIRNAME
        directory.mkdir(parents=True, exist_ok=True)
        path = directory / file_name
        if not path.is_file() or path.stat().st_size != len(wav):
            path.write_bytes(wav)
        winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC
                           | winsound.SND_NODEFAULT)
        return True
    except (OSError, RuntimeError):
        return False


def _now_ms__misc_sound() -> int:
    return int(time.time() * 1000)


def _safe_resolve(path: Path) -> Path | None:
    """`Path.resolve()` 的容错包装（拿不到就返回 None，调用方跳过这个候选）。"""
    try:
        return path.resolve()
    except (OSError, RuntimeError):
        return None


__all__ = ["ENV_SOUNDS_DIR", "Kind", "SOUND_SUBDIR", "SoundNotifier", "bool_of", "clamp",
           "int_of"]


# ========================================================================
# 原模块 lionbox/misc.py
# ========================================================================
"""边角模块（对应 Java 里不属于任何大类的几个小服务）。

| Java | 这里 |
| --- | --- |
| `core/question/UserQuestionService` | `question.UserQuestionService` |
| `core/sound/SoundNotifier` | `sound.SoundNotifier` / `sound.Kind` |
"""



__all__ = [
    "DEFAULT_TIMEOUT_SECONDS", "Kind", "Pending", "Result", "SoundNotifier", "Status",
    "UserQuestionService", "bool_of", "clamp", "int_of",
]


# ========================================================================
# 原模块 lionbox/api/notifications.py
# ========================================================================
"""音效提醒接口 —— `/api/notification`、`/api/notification/test`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\NotificationController.java`
（120 行 / 3 个接口）。

# 依赖：lionbox.misc.sound（由并行任务提供；**已到位，非桩**）
    Java 侧注入的是 `core/sound/SoundNotifier`：配置补值（`withDefaults`）、宽松取值
    （`bool` / `intOf`）、夹取（`clamp`）、音效种类（`Kind`）、真实播放都在那里。
    Python 的孪生实现是 `lionbox.misc.sound`，本模块**只负责接口语义**：
    字段白名单、与 Java 一致的强转与边界、错误文案、Spring 默认错误体、响应包封。
    配置读写走共享服务 `notifications`（`deps.NotificationStore`，真实实现：
    读写 `app-config.json` 的 `notification` 键，与 Java `AppConfigStore` 同一个键）。

【为什么强转要自己来一遍】Java 在控制器里对请求体做了两件前端能看见的事：
  · 只认 `BOOL_FIELDS` + `volume` + `minIntervalMs`，**未知字段直接忽略**（配置不会被写脏）；
  · `volume` 夹到 0~100、`minIntervalMs` 下限 0，且响应回的是**夹取后**的值。
把请求体原样存下去就会回一个 `volume: 150` 给前端，滑块与真实播放音量立刻对不上。
"""


import json
import logging
from typing import Any

from lionbox.api import deps

log__api_notifications = logging.getLogger("lionbox.api.notifications")

#: 允许通过接口修改的开关字段（Java `BOOL_FIELDS`，顺序也照抄）
BOOL_FIELDS: tuple[str, ...] = ("enabled", "soundDone", "soundApproval",
                                "soundQuestion", "soundError")


class NotificationApi:
    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 依赖
    def _store(self) -> Any:
        """通知配置的共享服务（读 `snapshot()` / 写 `update()`）。

        装配方之后 `ctx.install("notifications", 真实对象)` 会直接接管，
        本模块不用改（`deps.notifications` 已经优先返回已安装的实例）。
        """
        return deps.notifications(self.ctx)

    def _sound(self) -> SoundNotifier:
        """音效服务（Java 构造函数注入的 `SoundNotifier`）。

        【为什么用 ctx.cfg 而不是默认构造】`SoundNotifier()` 的默认值指向用户真实的
        `~/.lioncode`，那样测试/用例会污染用户的配置；必须显式给当前上下文这份配置。
        """
        return self.ctx.service("sound", lambda: SoundNotifier(self.ctx.cfg))

    def _current(self) -> dict[str, Any]:
        """当前配置（补全 + 夹取后的 7 个字段，与 Java `withDefaults(getMap(...))` 等价）。"""
        return SoundNotifier.with_defaults(self._store().snapshot())

    def _parse_body(self, req: Request) -> dict[str, Any] | Response | None:
        """Spring `@RequestBody(required = false) Map<String, Object>` 的等价解析。

        Java 实测（18099）：
          · 无请求体            -> `body == null`，按"没传字段"处理，正常保存（200）；
          · 字面量 `null`       -> 同上（Jackson 反序列化成 null）；
          · 非法 JSON / 数组    -> 进不了方法体，Spring 直接回 400 + 默认错误体。
        这里如实复刻：`None` = 没传；`Response` = 由调用方原样返回的 400。
        """
        raw = req.body
        if not raw:                                   # 空体：Java 里 body == null
            return None
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (ValueError, UnicodeDecodeError):
            return deps.spring_error(400, req.path)
        if parsed is None:                            # 字面量 null，等同没传
            return None
        if not isinstance(parsed, dict):
            return deps.spring_error(400, req.path)
        return parsed

    # ------------------------------------------------------------ 注册
    def register__api_notifications(self, router) -> None:
        api = self

        @router.get("/api/notification")
        def get_notification(req: Request):
            # Java: ApiResponse.ok(SoundNotifier.withDefaults(configStore.getMap(CONFIG_KEY)))
            return ApiResponse.ok(api._current())

        @router.post("/api/notification")
        def save_notification(req: Request):
            parsed = api._parse_body(req)
            if isinstance(parsed, Response):
                return parsed

            current = api._current()
            if parsed is not None:
                # 传哪个字段就改哪个，没传的保持原值（前端可以只提交一个开关）
                for key in BOOL_FIELDS:
                    if key in parsed:
                        current[key] = bool_of(parsed, key, bool(current.get(key)))
                if "volume" in parsed:
                    current["volume"] = clamp(
                        int_of__misc_sound(parsed, "volume",
                               int_of__misc_sound(current, "volume", SoundNotifier.DEFAULT_VOLUME)), 0, 100)
                if "minIntervalMs" in parsed:
                    current["minIntervalMs"] = max(
                        0, int_of__misc_sound(parsed, "minIntervalMs",
                                  int_of__misc_sound(current, "minIntervalMs",
                                         SoundNotifier.DEFAULT_MIN_INTERVAL_MS)))

            saved = api._store().update(current)      # 写 config.notification（立即生效）
            log__api_notifications.info("音效提醒配置已保存: enabled=%s, done=%s, approval=%s, question=%s, "
                     "error=%s, volume=%s", saved.get("enabled"), saved.get("soundDone"),
                     saved.get("soundApproval"), saved.get("soundQuestion"),
                     saved.get("soundError"), saved.get("volume"))
            return ApiResponse.ok(saved, "已保存")

        @router.post("/api/notification/test")
        def test_notification(req: Request):
            kind_raw = req.q("kind")
            if kind_raw is None:
                # Java 的 @RequestParam("kind") 是必填：缺参数在进方法体之前就被 Spring
                # 打回 400 + 默认错误体（实测 {"timestamp","status","error","path"}）
                return deps.spring_error(400, req.path)

            kind = Kind.parse(kind_raw)               # Java: trim().toUpperCase() 后 valueOf
            if kind is None:
                # 文案逐字照抄 Java（含中文括号；注意回显的是**原样**的 kind，不是 trim 后的）
                return ApiResponse.error(
                    f"未知的音效类型: {kind_raw}（可选 done / approval / error）")

            # 试听绕过节流与开关（允许连点），但音量仍按配置走
            volume = int_of__misc_sound(api._current(), "volume", SoundNotifier.DEFAULT_VOLUME)
            api._sound().preview(kind)
            # 【注意参数序】Java 是 `ApiResponse.ok(String message, T data)`，与 Python 侧
            # `ApiResponse.ok(data, message)` 相反 —— 这里必须用 `ok_msg(message, data)`，
            # 否则 message 与 data 会互换（前端读的是 data，会显示成一串中文提示）。
            if volume <= 0:
                return ApiResponse.ok_msg("音量是 0，听不到声音——把音量调大再试", kind)
            return ApiResponse.ok_msg(f"已播放 {kind.lower()} 音效", kind)


def register__api_notifications(router, ctx) -> None:
    NotificationApi(ctx).register__api_notifications(router)


# ========================================================================
# 原模块 lionbox/api/native_dialog.py
# ========================================================================
"""原生文件夹选择接口 —— `/api/native-dialog/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\NativeDialogController.java`（368 行 / 2 个接口）。

【`GET /select-directory` 的实现方式与 Java 逐环节对应】
Windows Vista+ 没有命令行版的"选择文件夹"，Java 版的做法是：把一段 PowerShell 脚本
（内嵌 C# COM 互操作，调 IFileDialog）写进临时目录的 `picker.ps1`（UTF-8 **带 BOM**），
用 `powershell -NoProfile -STA -WindowStyle Hidden -ExecutionPolicy Bypass -File` 拉起，
初始目录走环境变量 `LIONCODE_INITIAL_DIR`，选择结果由脚本写进 `LIONCODE_RESULT_FILE`
指向的文件（格式 `OK|路径` / `CANCEL|` / `FAIL|错误信息`）—— 不依赖控制台管道，
避免隐藏窗口与编码问题。这里把脚本、参数、环境变量、结果文件协议、超时（300 秒）、
退出码判定、stdout 兜底、错误文案全部照抄，只把 `ProcessBuilder` 换成 `subprocess`。

【并发闸门】Java 用 `static AtomicBoolean DIALOG_OPEN` 保证同一时间只弹一个窗口，
这里用等价的模块级 `DialogGate`（**进程级**）。第二次请求回
`文件夹选择窗口已打开，请先完成或关闭当前窗口`，前端按这句话提示用户。

【为什么 `select-directory` 没有"与 Java 真值的逐字段比对"】`.lbverify/java/` 里这一条的
status 是 0、body 是 `<TimeoutError: timed out>`：真实调用会弹系统对话框并把请求线程挂住，
探针采不到响应（SPEC 第 3 节也把本接口列进了禁调清单）。本模块的验证改用
"注入不开窗口的选择器驱动"覆盖全部分支，且 `PICKER_SCRIPT` 与 Java 源码的文本块逐字节比对。

# 依赖：无（零第三方依赖，只用标准库）。
# 选择器驱动按服务名 `native_dialog_picker` 取：装配方/用例可以用
# `ctx.install("native_dialog_picker", 别的驱动)` 换成不开真实窗口的实现，模块代码不用改。
"""


import logging
import os
import shutil
import subprocess
import tempfile
import threading
from pathlib import Path

from lionbox.api import deps

log__api_native_dialog = logging.getLogger("lionbox.api.native_dialog")

# Java: process.waitFor(300, TimeUnit.SECONDS) / waitFor(5, TimeUnit.SECONDS)
DIALOG_TIMEOUT_SECONDS = 300
KILL_GRACE_SECONDS = 5

# Java `NativeDialogController.PICKER_SCRIPT` 的文本块（Java 会剥掉 8 空格公共缩进 +
# 每行行尾空白，这里就是剥完之后的字节级等价物；用例会读 Java 源码现算并逐字节比对）。
PICKER_SCRIPT = r"""$ErrorActionPreference = 'Stop'
$resultFile = $env:LIONCODE_RESULT_FILE

function Write-Result([string]$status, [string]$detail) {
    try {
        $utf8NoBom = New-Object System.Text.UTF8Encoding($false)
        [System.IO.File]::WriteAllText($resultFile, ($status + '|' + $detail), $utf8NoBom)
    } catch {
        # 结果文件写失败时兜底输出到stdout
        Write-Output ($status + '|' + $detail)
    }
}

try {
    Add-Type -TypeDefinition @'
using System;
using System.Runtime.InteropServices;

public static class FolderPicker {

    [ComImport]
    [Guid("DC1C5A9C-E88A-4DDE-A5A1-60F82A20AEF7")]
    public class FileOpenDialogRCW { }

    [ComImport]
    [Guid("42F85136-DB7E-439C-85F1-E4075D135FC8")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    public interface IFileOpenDialog {
        [PreserveSig] int Show(IntPtr parent);
        void SetFileTypes(uint cFileTypes, [In] IntPtr rgFilterSpec);
        void SetFileTypeIndex(uint iFileType);
        void GetFileTypeIndex(out uint piFileType);
        void Advise(IntPtr pfde, out uint pdwCookie);
        void Unadvise(uint dwCookie);
        void SetOptions(uint fos);
        void GetOptions(out uint pfos);
        void SetDefaultFolder(IShellItem psi);
        void SetFolder(IShellItem psi);
        void GetFolder(out IShellItem ppsi);
        void GetCurrentSelection(out IShellItem ppsi);
        void SetFileName([MarshalAs(UnmanagedType.LPWStr)] string pszName);
        void GetFileName([MarshalAs(UnmanagedType.LPWStr)] out string pszName);
        void SetTitle([MarshalAs(UnmanagedType.LPWStr)] string pszTitle);
        void SetOkButtonLabel([MarshalAs(UnmanagedType.LPWStr)] string pszText);
        void SetFileNameLabel([MarshalAs(UnmanagedType.LPWStr)] string pszLabel);
        void GetResult(out IShellItem ppsi);
        void AddPlace(IShellItem psi, uint fdap);
        void SetDefaultExtension([MarshalAs(UnmanagedType.LPWStr)] string pszDefaultExtension);
        void Close(int hr);
        void SetClientGuid(ref Guid guid);
        void ClearClientData();
        void SetFilter(IntPtr pFilter);
        void GetResults(out IShellItemArray ppenum);
        void GetSelectedItems(out IShellItemArray ppsai);
    }

    [ComImport]
    [Guid("43826D1E-E718-42EE-BC55-A1E261C37BFE")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    public interface IShellItem {
        void BindToHandler(IntPtr pbc, ref Guid bhid, ref Guid riid, out IntPtr ppv);
        void GetParent(out IShellItem ppsi);
        void GetDisplayName(uint sigdnName, [MarshalAs(UnmanagedType.LPWStr)] out string ppszName);
        void GetAttributes(uint sfgaoMask, out uint psfgaoAttribs);
        void Compare(IShellItem psi, uint hint, out int piOrder);
    }

    [ComImport]
    [Guid("B63EA76D-1F85-456F-A19C-48159EFA858B")]
    [InterfaceType(ComInterfaceType.InterfaceIsIUnknown)]
    public interface IShellItemArray { }

    [DllImport("shell32.dll", CharSet = CharSet.Unicode)]
    private static extern int SHCreateItemFromParsingName(
        [MarshalAs(UnmanagedType.LPWStr)] string pszPath,
        IntPtr pbc,
        [In] ref Guid riid,
        [MarshalAs(UnmanagedType.Interface)] out IShellItem ppv);

    private static string GetPath(IShellItem item) {
        if (item == null) return null;
        try {
            string path;
            // SIGDN_FILESYSPATH；失败时COM互操作会抛出异常
            item.GetDisplayName(0x80058000, out path);
            return string.IsNullOrEmpty(path) ? null : path;
        } catch {
            return null;
        }
    }

    public static string PickFolder(string title, string initialPath) {
        var dialog = (IFileOpenDialog)new FileOpenDialogRCW();
        // FOS_PICKFOLDERS | FOS_FORCEFILESYSTEM | FOS_PATHMUSTEXIST
        uint options = 0x20 | 0x40 | 0x800;
        dialog.SetOptions(options);
        if (!string.IsNullOrEmpty(title)) {
            dialog.SetTitle(title);
        }
        if (!string.IsNullOrEmpty(initialPath)) {
            try {
                IShellItem folder;
                Guid shellItemGuid = typeof(IShellItem).GUID;
                int hr = SHCreateItemFromParsingName(initialPath, IntPtr.Zero, ref shellItemGuid, out folder);
                if (hr == 0 && folder != null) {
                    dialog.SetFolder(folder);
                }
            } catch { }
        }
        int showHr = dialog.Show(IntPtr.Zero);
        if (showHr == unchecked((int)0x800704C7)) {
            return null; // 用户取消：正常返回null
        }
        if (showHr != 0) {
            throw new Exception("Show failed, HRESULT=0x" + showHr.ToString("X8"));
        }
        IShellItem result = null;
        try {
            dialog.GetResult(out result);
        } catch {
            result = null;
        }
        string path = GetPath(result);
        if (path == null) {
            // GetResult失败时尝试GetCurrentSelection兜底
            IShellItem selected = null;
            try {
                dialog.GetCurrentSelection(out selected);
            } catch {
                selected = null;
            }
            path = GetPath(selected);
            if (path == null) {
                throw new Exception("GetResult/GetCurrentSelection failed");
            }
        }
        return path;
    }
}
'@
} catch {
    Write-Result 'FAIL' ("AddType编译失败: " + $_.Exception.Message)
    exit 1
}

$initial = $env:LIONCODE_INITIAL_DIR
$picked = $null

# 首选：现代 Explorer 风格文件夹选择窗口
try {
    $picked = [FolderPicker]::PickFolder('选择工作区目录', $initial)
} catch {
    # 现代对话框初始化/运行失败 → 回退传统对话框
    try {
        Add-Type -AssemblyName System.Windows.Forms
        $d = New-Object System.Windows.Forms.FolderBrowserDialog
        $d.Description = '选择工作区目录'
        $d.ShowNewFolderButton = $true
        if ($initial -and (Test-Path -LiteralPath $initial)) {
            $d.SelectedPath = $initial
        }
        if ($d.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            Write-Result 'OK' $d.SelectedPath
            exit 0
        }
        Write-Result 'CANCEL' ''
    } catch {
        Write-Result 'FAIL' ("回退对话框失败: " + $_.Exception.Message)
    }
    exit 1
}

if ($picked) {
    Write-Result 'OK' $picked
} else {
    # 用户在现代化对话框中点了取消
    Write-Result 'CANCEL' ''
}
"""


# --------------------------------------------------------------------------
# 并发闸门（Java: static AtomicBoolean DIALOG_OPEN）
# --------------------------------------------------------------------------


class DialogGate:
    """同一时间只允许一个文件夹选择对话框。

    【为什么是进程级】Java 的字段是 `static` —— 连点两次"选择文件夹"时，第二次必须被
    拒绝，而不是再弹一个窗口盖住第一个（第一个还占着用户注意力，两个窗口叠在一起
    用户根本分不清点的是哪个）。
    """

    def __init__(self) -> None:
        self._lock = threading.Lock()

    def try_enter(self) -> bool:
        """抢闸门；已有窗口打开时返回 False。"""
        return self._lock.acquire(blocking=False)

    def exit(self) -> None:
        """复位（Java `DIALOG_OPEN.set(false)`，在 finally 里无条件调用）。"""
        try:
            self._lock.release()
        except RuntimeError:
            # 只有"没进就出"这种代码写错才会走到这里：记下来，不吞。
            log__api_native_dialog.error("文件夹选择闸门被重复释放（当前未持有）")


DIALOG_OPEN = DialogGate()


# --------------------------------------------------------------------------
# 选择器驱动（Java: ProcessBuilder 那一段）
# --------------------------------------------------------------------------


class PickOutcome:
    """一次选择器运行的结果（Java 里散在 `selectDirectory` 局部变量里的那几项）。

    - `finished=False`：300 秒内没结束（Java 已 destroyForcibly，接口回超时文案）
    - `exit_code`：进程退出码；超时时为 None
    - `result`：结果文件内容（去 BOM / trim 之后），文件不存在时为 None
    - `stdout`：stdout+stderr 合并后的内容（**未** trim，Java 在用时才 trim）
    """

    __slots__ = ("finished", "exit_code", "result", "stdout")

    def __init__(self, finished: bool, exit_code: int | None, result: str | None,
                 stdout: str) -> None:
        self.finished = finished
        self.exit_code = exit_code
        self.result = result
        self.stdout = stdout

    def __repr__(self) -> str:
        return (f"PickOutcome(finished={self.finished}, exit_code={self.exit_code}, "
                f"result={self.result!r}, stdout={self.stdout[:80]!r})")


class PowerShellFolderPicker:
    """真实驱动：临时目录 + `picker.ps1` + 结果文件协议（会弹出真实的系统对话框）。"""

    def __init__(self, timeout_seconds: int = DIALOG_TIMEOUT_SECONDS,
                 kill_grace_seconds: int = KILL_GRACE_SECONDS) -> None:
        self.timeout_seconds = timeout_seconds
        self.kill_grace_seconds = kill_grace_seconds

    def pick(self, initial_path: str) -> PickOutcome:
        """弹一次选择窗口，返回结果。临时目录无论如何都会删掉（Java 的 finally）。"""
        temp_dir = Path(tempfile.mkdtemp(prefix="lioncode-picker"))
        try:
            script_file = temp_dir / "picker.ps1"
            result_file = temp_dir / "result.txt"
            stdout_file = temp_dir / "stdout.txt"
            # Java: Files.writeString(scriptFile, "\uFEFF" + PICKER_SCRIPT, UTF_8)
            # BOM 不能省：Windows PowerShell 5.1 对无 BOM 的 .ps1 按系统 ANSI 码页解码，
            # 脚本里的中文（对话框标题 '选择工作区目录'）会变乱码甚至语法错。
            script_file.write_text("\ufeff" + PICKER_SCRIPT, encoding="utf-8")

            env = dict(os.environ)
            env["LIONCODE_INITIAL_DIR"] = initial_path or ""
            env["LIONCODE_RESULT_FILE"] = str(result_file)

            finished, exit_code = self.run(script_file, stdout_file, env)
            stdout_text = self._read_stdout(stdout_file)

            result: str | None = None
            # 【故意不 catch 读失败】Java 在这里抛的 IOException 会被方法体的
            # catch (Exception e) 兜住，回 "打开对话框失败: ..."；这里保持同样的传播路径。
            if result_file.exists():
                result = result_file.read_text(encoding="utf-8").replace("\ufeff", "").strip()
            return PickOutcome(finished=finished, exit_code=exit_code, result=result,
                               stdout=stdout_text)
        finally:
            # Java: Files.walk(tempDir).sorted(reverseOrder()).deleteIfExists(...)，
            # 清理失败不影响主流程。
            shutil.rmtree(temp_dir, ignore_errors=True)

    @staticmethod
    def _read_stdout(stdout_file: Path) -> str:
        """读合并后的 stdout/stderr（Java: 读失败只记 debug，不让整个请求失败）。"""
        try:
            if stdout_file.exists():
                return stdout_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError) as e:
            log__api_native_dialog.debug("读取选择器 stdout 失败（忽略）: %s", e)
        return ""

    def run(self, script_file: Path, stdout_file: Path,
            env: dict[str, str]) -> tuple[bool, int | None]:
        """拉起 PowerShell 并等待，返回 `(是否在超时内结束, 退出码)`。

        【顺序很关键，照抄 Java 的注释】必须先把 stdout 重定向到文件，再去等待。
        如果像早先的实现那样"先在当前线程读完 stdout，再 waitFor(300s)"，
        readLine() 会一直阻塞到子进程关闭 stdout（也就是对话框关掉为止）——
        用户把选择窗口晾着不点，这个 HTTP 线程就永远卡住、超时形同虚设，
        而且 finally 里的闸门复位也永远不会执行，之后所有请求都被
        "文件夹选择窗口已打开"拒绝，只能重启应用。

        用例可以覆盖本方法换成"不开真实窗口"的驱动（见 `.lbverify/cases/native_dialog.py`）。
        """
        args = ["powershell", "-NoProfile", "-STA", "-WindowStyle", "Hidden",
                "-ExecutionPolicy", "Bypass", "-File", str(script_file)]
        with open(stdout_file, "wb") as out:
            # Java: redirectErrorStream(true) + redirectOutput(文件) —— stderr 并入同一文件
            proc = subprocess.Popen(args, stdin=subprocess.DEVNULL, stdout=out,
                                    stderr=subprocess.STDOUT, env=env, close_fds=True)
        try:
            return True, proc.wait(timeout=self.timeout_seconds)
        except subprocess.TimeoutExpired:
            proc.kill()
            try:
                proc.wait(timeout=self.kill_grace_seconds)
            except subprocess.TimeoutExpired:
                log__api_native_dialog.warning("选择器进程强制结束后仍未退出: pid=%s", proc.pid)
            return False, None


# --------------------------------------------------------------------------
# 常用目录（Java: System.getProperty("user.home") + File.listRoots()）
# --------------------------------------------------------------------------


def user_home() -> str:
    """`System.getProperty("user.home")` 的等价物（Windows 上都是 `%USERPROFILE%`）。"""
    home = os.path.expanduser("~")
    if home and home != "~":
        return home
    # 展开失败（USERPROFILE 缺失）：Java 的 user.home 一定有值，这里再按 HOMEDRIVE+HOMEPATH 兜一次
    drive = os.environ.get("HOMEDRIVE") or ""
    tail = os.environ.get("HOMEPATH") or ""
    if drive or tail:
        return drive + tail
    # 两者都没有：宁可明确报错（接口回 500），也不拼一个 "~\Desktop" 这种假路径给前端
    raise RuntimeError("无法确定用户主目录（USERPROFILE / HOMEDRIVE+HOMEPATH 均未设置）")


def drive_roots() -> list[str]:
    """`File.listRoots()` 的等价物：全部逻辑盘符的根（如 `['C:\\\\']`）。

    Java 的 listRoots 直接取 `GetLogicalDrives()` 的位掩码，**不按盘类型过滤**
    （网络盘、未就绪的可移动盘也算，前端只是拿来做快捷入口）。
    """
    if os.name != "nt":
        return [os.sep]
    listdrives = getattr(os, "listdrives", None)
    if listdrives is not None:                       # Python 3.12+ 内置
        return [str(d) for d in listdrives()]
    import ctypes                                    # 老解释器：直接问内核要同一个位掩码

    mask = ctypes.windll.kernel32.GetLogicalDrives()  # type: ignore[attr-defined]
    return [chr(ord("A") + i) + ":\\" for i in range(26) if mask & (1 << i)]


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class NativeDialogApi:
    """`NativeDialogController` 的 Python 等价物（2 个接口）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 依赖
    def _picker(self) -> PowerShellFolderPicker:
        """选择器驱动（服务名 `native_dialog_picker`）。

        取服务而不是自己 `new`：装配方/回归用例可以
        `ctx.install("native_dialog_picker", 不开窗口的驱动)`，模块代码一行都不用改。
        """
        return self.ctx.service("native_dialog_picker", lambda: PowerShellFolderPicker())

    # ------------------------------------------------------------ GET /select-directory
    def select_directory(self, initial_path: str) -> ApiResponse:
        """打开 Windows 标准样式的文件夹选择对话框（现代 Explorer 风格）。"""
        # 已有对话框打开时直接拒绝，避免连续点击弹出多个窗口
        if not DIALOG_OPEN.try_enter():
            return ApiResponse.error("文件夹选择窗口已打开，请先完成或关闭当前窗口")
        try:
            outcome = self._picker().pick(initial_path or "")
            stdout = outcome.stdout.strip()

            if not outcome.finished:
                log__api_native_dialog.warning("文件夹选择对话框超时，stdout: %s", stdout)
                return ApiResponse.error("对话框等待超时（5 分钟），已关闭；请重新打开并完成选择")

            result = outcome.result
            log__api_native_dialog.info("文件夹选择脚本结束 exit=%s result=%s stdout=%s",
                     outcome.exit_code, result, stdout)

            # 进程异常退出（崩溃/被杀）→ 明确报错，而非误判为取消
            if outcome.exit_code != 0 and (result is None or not result.startswith("OK|")):
                log__api_native_dialog.error("文件夹选择脚本异常退出: exit=%s result=%s stdout=%s",
                          outcome.exit_code, result, stdout)
                return ApiResponse.error(f"文件夹选择窗口异常退出（exit={outcome.exit_code}）")

            if result is None or result == "":
                # 结果文件缺失：极老路径或异常，看 stdout 兜底
                fallback = stdout
                if fallback and not fallback.startswith("FAIL"):
                    log__api_native_dialog.info("结果文件为空，使用 stdout 兜底: %s", fallback)
                    result = "OK|" + fallback

            if result is not None and result.startswith("OK|"):
                selected = result[3:].strip()
                if selected:
                    log__api_native_dialog.info("用户选择目录: %s", selected)
                    # Java: ApiResponse.ok("目录已选择", selected) —— message 在前、data 在后
                    return ApiResponse.ok(selected, "目录已选择")

            if result is not None and result.startswith("FAIL|"):
                msg = result[5:].strip()
                log__api_native_dialog.error("文件夹选择对话框失败: %s", msg)
                return ApiResponse.error("打开对话框失败: " + msg)

            # CANCEL 或未知
            log__api_native_dialog.info("用户取消文件夹选择或未选择目录 (result=%s, stdout=%s)", result, stdout)
            return ApiResponse.error("用户取消选择")
        except Exception as e:                       # 与 Java 的 catch (Exception e) 对齐
            log__api_native_dialog.error("打开文件夹选择对话框失败", exc_info=True)
            return ApiResponse.error("打开对话框失败: " + str(e))
        finally:
            DIALOG_OPEN.exit()

    # ------------------------------------------------------------ GET /common-dirs
    def common_dirs(self) -> ApiResponse:
        """系统常用目录（桌面/文档/下载/图片/用户目录 + 各磁盘根）。

        Java 用的是 LinkedHashMap，键序即插入序；Python 的 dict 同样保序，
        前端 `web/index.html` 按 `data['用户目录']` 取值，键名必须逐字一致。
        """
        home = user_home()
        # Java: home + File.separator + "Desktop"（只做字符串拼接，不检查目录是否存在）
        dirs: dict[str, str] = {
            "桌面": home + os.sep + "Desktop",
            "文档": home + os.sep + "Documents",
            "下载": home + os.sep + "Downloads",
            "图片": home + os.sep + "Pictures",
            "用户目录": home,
        }
        for root in drive_roots():
            label = root
            if label.endswith(":\\"):                # Java 里是字面量 ":\\"（Windows 专用）
                label = label[:2]
            dirs["磁盘 " + label] = root
        return ApiResponse.ok(dirs)

    # ------------------------------------------------------------ 注册
    def register__api_native_dialog(self, router) -> None:
        api = self

        @router.get("/api/native-dialog/select-directory")
        def select_directory(req: Request):
            # Java: @RequestParam(value = "initialPath", defaultValue = "") —— 缺省即空串
            return api.select_directory(req.q("initialPath") or "")

        @router.get("/api/native-dialog/common-dirs")
        def common_dirs(req: Request):
            return api.common_dirs()


def register__api_native_dialog(router, ctx) -> None:
    NativeDialogApi(ctx).register__api_native_dialog(router)


# ========================================================================
# 原模块 lionbox/config/provider.py
# ========================================================================
"""模型提供商配置 —— 逐项对照 Java `model/config/ModelProviderConfig.java`（record）。

本产品的模型运行时就用本机自带的本地运行时，绑定回环地址，因此内置模板列表刻意
只保留一个本地提供商，不再包含任何云端服务商。字段结构（含 Token-Plan 相关字段）
为兼容既有调用方而保持不变。
"""


from dataclasses import dataclass, field
from typing import Any

#: 本地模型运行时端口（与 Java 的 `LOCAL_RUNTIME_PORT` / application.yml 一致）
LOCAL_RUNTIME_PORT = 8788

#: 本地模型运行时主机（**仅回环地址**）
LOCAL_RUNTIME_HOST = "127.0.0.1"

#: 内置本地模型名称
LOCAL_MODEL_NAME = "lion-models1"

#: 内置模型文件（软件自带的 GGUF 权重；Java 常量写的是 Q8_0，安装包会按实际选择的版本覆盖）
LOCAL_MODEL_FILE = "lion-merged-Q8_0.gguf"

#: 内置提供商 id（与 AppConfigStore 的 LOCAL_PROVIDER_ID 一致）
LOCAL_PROVIDER_ID = "lionbox-local"

#: 自定义（用户自己填 OpenAI 兼容 API）提供商 id
CUSTOM_PROVIDER_ID = "lionbox-custom"

#: 协议类型
PROTOCOL_OPENAI = "openai"


def local_base_url__config_provider(host: str = LOCAL_RUNTIME_HOST, port: int = LOCAL_RUNTIME_PORT) -> str:
    """本地运行时默认 Base URL（端口与 application.yml 的 lionbox.runtime.port 一致）。"""
    return f"http://{host}:{port}/v1"


@dataclass
class ModelProviderConfig:
    """模型提供商配置。

    :param provider_id:         提供商ID
    :param display_name:        提供商显示名称
    :param standard_base_url:   普通按量端点 Base URL
    :param token_plan_base_url: Token-Plan 端点 Base URL（不支持则为 None）
    :param supports_token_plan: 是否支持 Token-Plan
    :param default_models:      默认模型列表
    :param protocol_type:       协议类型
    """

    provider_id: str
    display_name: str
    standard_base_url: str
    token_plan_base_url: str | None = None
    supports_token_plan: bool = False
    default_models: list[str] = field(default_factory=list)
    protocol_type: str = PROTOCOL_OPENAI

    def to_dict(self) -> dict[str, Any]:
        """字段名与 Java record 的 JSON 形状一致（null 字段整个省略）。"""
        out: dict[str, Any] = {
            "providerId": self.provider_id,
            "displayName": self.display_name,
            "standardBaseUrl": self.standard_base_url,
            "supportsTokenPlan": self.supports_token_plan,
            "defaultModels": list(self.default_models),
            "protocolType": self.protocol_type,
        }
        if self.token_plan_base_url:
            out["tokenPlanBaseUrl"] = self.token_plan_base_url
        return out

    @staticmethod
    def from_dict(raw: dict[str, Any] | None) -> "ModelProviderConfig | None":
        if not raw:
            return None
        provider_id = raw.get("providerId") or raw.get("id")
        if provider_id is None or not str(provider_id).strip():
            return None
        models = raw.get("defaultModels")
        return ModelProviderConfig(
            provider_id=str(provider_id).strip(),
            display_name=str(raw.get("displayName") or provider_id).strip(),
            standard_base_url=str(raw.get("standardBaseUrl") or raw.get("baseUrl") or ""),
            token_plan_base_url=(None if not raw.get("tokenPlanBaseUrl")
                                 else str(raw.get("tokenPlanBaseUrl"))),
            supports_token_plan=bool(raw.get("supportsTokenPlan", False)),
            default_models=[str(m) for m in models] if isinstance(models, list) else [],
            protocol_type=str(raw.get("protocolType") or PROTOCOL_OPENAI),
        )


def builtin_providers() -> list[ModelProviderConfig]:
    """内置提供商模板列表。

    **刻意只保留一项**：软件自带的本地模型运行时。模型在本机以 GGUF 形式本地推理，
    通过回环地址的 OpenAI 兼容端点提供服务，不需要 API-Key，也不允许连接任何云端服务商。
    """
    return [ModelProviderConfig(
        provider_id=LOCAL_PROVIDER_ID,
        display_name="Lion Code 本地模型",
        standard_base_url=local_base_url__config_provider(),
        token_plan_base_url=None,
        supports_token_plan=False,
        default_models=[LOCAL_MODEL_NAME],
        protocol_type=PROTOCOL_OPENAI,
    )]


def is_known_local_base_url(value: Any) -> bool:
    """判断给定 Base URL 是否属于本地端点。

    与 Java `AppConfigStore.isKnownLocalBaseUrl` 同一套判据：先比内置模板的端点，
    再看主机是不是回环地址（127.0.0.1 / localhost / [::1]）。
    """
    if not isinstance(value, str) or not value.strip():
        return False
    text = value.strip()
    for provider in builtin_providers():
        if text == provider.standard_base_url:
            return True
    lower = text.lower()
    return ("://127.0.0.1" in lower or "://localhost" in lower or "://[::1]" in lower)


__all__ = [
    "CUSTOM_PROVIDER_ID", "LOCAL_MODEL_FILE", "LOCAL_MODEL_NAME", "LOCAL_PROVIDER_ID",
    "LOCAL_RUNTIME_HOST", "LOCAL_RUNTIME_PORT", "PROTOCOL_OPENAI", "ModelProviderConfig",
    "builtin_providers", "is_known_local_base_url", "local_base_url",
]


# ========================================================================
# 原模块 lionbox/config/app_config.py
# ========================================================================
"""AppConfigStore 的补齐部分 —— 逐方法对照 Java `model/config/AppConfigStore.java`（582 行）。

【为什么是"补齐"而不是重写】`config/store.py` 已经有一个可用的 Python 版 AppConfigStore
（读写、原子落盘、`llama()` 默认值合并、`toolCallMode` 归一），而且它是**冻结契约**
（不许改）。本模块用组合的方式把它缺的那一半补上：

| Java `AppConfigStore` 成员 | 这里 |
| --- | --- |
| `getMap(key)` | `AppConfigExtras.get_map(key)` |
| `llamaConfig()`（原始，不并默认值） | `AppConfigExtras.llama_config()` |
| `llamaModelFile()` | `AppConfigExtras.llama_model_file()` |
| `normalizeToolCallMode()`（非法返回 null） | `parse_tool_call_mode()` |
| `applyDefaults()` | `AppConfigExtras.apply_defaults()` |
| `applyInstallerModelChoice()` | `AppConfigExtras.apply_installer_model_choice()` |
| `migrateLegacyModelName()` | `AppConfigExtras.migrate_legacy_model_name()` |
| `writeAdapterBlock()` / `ensureProviderInstance()` / `repairCustomProviderPointingAtLocal()` | 同名方法 |
| `MODE_LOCAL` / `MODE_CUSTOM` / `TOOLCALL_*` / 内置 provider id / 历史模型名 | 本模块常量 |

【两条规则别搞混（Java 注释里的原话）】
  * **本地模式 local**：端点与模型固定指向软件自带的运行时，密钥留空。
    应用启动时**不加载模型**，等第一条消息由本地运行时惰性拉起。
  * **自定义模式 custom**：用户自己填的 baseUrl / apiKey / model
    **原样保留，绝不覆盖、绝不抹除**。这种模式下本地模型永远不会被加载。

老版本（只支持本地）留下的配置里没有 `providerMode` 键，这里按现有端点推断：
回环地址 = 本地，其它非空地址 = 用户自己配的 API。
"""


from typing import Any


#: 运行模式：用软件自带的本地模型 / 用用户自己填的 OpenAI 兼容 API
MODE_LOCAL = "local"
MODE_CUSTOM = "custom"

#: 工具调用方式：自动（推荐）/ 强制原生 function calling / 强制文本约定
TOOLCALL_AUTO = "auto"
TOOLCALL_NATIVE = "native"
TOOLCALL_TEXT = "text"

#: 出厂默认模型
LOCAL_MODEL = LOCAL_MODEL_NAME

#: 历史配置里写下的模型名（早期版本在界面上直接暴露了底座模型名）。
#: 老配置靠 `migrate_legacy_model_name()` 迁移，不要删。
LEGACY_LOCAL_MODEL = "MiMo-V2.6-Distill-Qwen-9B"

#: 协议的内部标识（Java 里 activeAdapter 固定是它）
ACTIVE_ADAPTER = "OPENAI_COMPATIBLE"

#: 本地端点（Java 是 `@Value("${lionbox.runtime.base-url:...}")`）
LOCAL_BASE_URL = local_base_url__config_provider()


def parse_tool_call_mode(value: Any) -> str | None:
    """校验外部传入的工具调用方式，非法值返回 None（调用方据此报错）。

    【与 `store.normalize_tool_call_mode` 的分工】那个是"读配置时的宽容归一"（非法 → auto），
    这个是"校验用户输入"（非法 → None，让接口层回 400 而不是悄悄改成 auto）。
    两者语义不同，Java 里也是两个方法。
    """
    if value is None:
        return None
    v = str(value).strip().lower()
    return v if v in (TOOLCALL_AUTO, TOOLCALL_NATIVE, TOOLCALL_TEXT) else None


class AppConfigExtras:
    """给一个 `AppConfigStore` 补上 Java 版的启动初始化与 provider 实例维护能力。"""

    def __init__(self, store: AppConfigStore, local_base_url_value: str | None = None) -> None:
        self.store = store
        self.local_base_url__config_provider = (local_base_url_value or LOCAL_BASE_URL).rstrip("/")

    # ------------------------------------------------------------------
    # 读取
    # ------------------------------------------------------------------
    def get_map(self, key: str) -> dict[str, Any]:
        """取配置项（Map 类型）；不是 Map 就返回空表（与 Java `getMap` 一致）。"""
        value = self.store.get(key, None)
        return dict(value) if isinstance(value, dict) else {}

    def llama_config(self) -> dict[str, Any]:
        """llama.cpp 运行参数（**原始**，不合并默认值 —— Java `llamaConfig()` 就是这么做的）。"""
        return self.get_map("llama")

    def llama_model_file(self) -> str | None:
        """当前选用的模型文件名（安装时选的、或设置里改的；没有就返回 None 用默认）。"""
        value = str(self.llama_config().get("modelFile") or "").strip()
        return value or None

    # ------------------------------------------------------------------
    # 启动初始化
    # ------------------------------------------------------------------
    def init(self) -> bool:
        """等价 Java 的 `@PostConstruct init()` + `applyDefaults()` + `applyInstallerModelChoice()`。

        :return: 是否发生了配置变更（并已落盘）
        """
        changed = self.apply_defaults()
        changed = self.apply_installer_model_choice() or changed
        return changed

    def apply_defaults(self) -> bool:
        """施加默认配置（两种运行模式共存）。返回是否落盘。"""
        changed = False

        # ---- 1) 确定运行模式 ----
        mode = _str(self.store.get("providerMode", ""))
        if mode not in (MODE_LOCAL, MODE_CUSTOM):
            current = _str(self.store.get("baseUrl", ""))
            if not current:
                current = _str(self.get_map("openai").get("baseUrl"))
            mode = MODE_CUSTOM if (current and not is_known_local_base_url(current)) else MODE_LOCAL
            print(f"[配置] 未发现运行模式配置，按现有端点推断为: {mode}（端点={current}）", flush=True)
            changed = True
        if mode != _str(self.store.get("providerMode", "")):
            self.store.set("providerMode", mode)
            changed = True

        # ---- 1.5) 历史配置里的模型名迁移（老版本暴露的是底座模型名）----
        changed = self.migrate_legacy_model_name() or changed

        # ---- 2) 按模式落配置 ----
        if mode == MODE_CUSTOM:
            block = self.get_map("openai")
            url = _first_non_blank(_str(self.store.get("baseUrl", "")), _str(block.get("baseUrl")))
            model = _first_non_blank(_str(self.store.get("model", "")), _str(block.get("model")))
            key = _first_non_blank(_str(self.store.get("apiKey", "")), _str(block.get("apiKey")))
            if not url:
                print("[配置] 运行模式是自定义 API，但没有填端点，自动退回本地模型", flush=True)
                mode = MODE_LOCAL
                self.store.set("providerMode", MODE_LOCAL)
            else:
                changed = self._put_if_different("provider", CUSTOM_PROVIDER_ID) or changed
                changed = self._put_if_different("baseUrl", url) or changed
                changed = self._put_if_different("model", model) or changed
                changed = self._put_if_different("apiKey", key) or changed
                changed = self.write_adapter_block(url, model, key) or changed
                print(f"[配置] 运行模式=自定义 API: baseUrl={url}, model={model}, "
                      f"已配置密钥={bool(key)}", flush=True)
        if mode == MODE_LOCAL:
            changed = self._put_if_different("provider", LOCAL_PROVIDER_ID) or changed
            changed = self._put_if_different("baseUrl", self.local_base_url__config_provider) or changed
            changed = self._put_if_different("model", LOCAL_MODEL) or changed
            changed = self._put_if_different("apiKey", "") or changed
            changed = self.write_adapter_block(self.local_base_url__config_provider, LOCAL_MODEL, "") or changed

        # ---- 3) 协议固定走 OpenAI 兼容 ----
        if self.store.get("activeAdapter", None) != ACTIVE_ADAPTER:
            self.store.set("activeAdapter", ACTIVE_ADAPTER)
            changed = True

        # ---- 3.5) 工具调用方式（老配置没有这个键 → 补成 auto）----
        tool_call = _str(self.store.get("toolCallMode", "")).strip().lower()
        if tool_call not in (TOOLCALL_NATIVE, TOOLCALL_TEXT):
            if tool_call != TOOLCALL_AUTO:
                print(f"[配置] 工具调用方式未配置或非法（{tool_call}），回落到 auto", flush=True)
            changed = self._put_if_different("toolCallMode", TOOLCALL_AUTO) or changed

        # ---- 4) 两个内置实例都登记好，用户已有的实例不删 ----
        # 「自定义 API」实例要用**存档里**的用户端点来初始化：早先这里传当前生效的 baseUrl，
        # 默认等于本地端点，于是新建的配置里自定义实例指向 127.0.0.1:8788 ——
        # 而自定义模式下本地运行时根本不启动，用户切过去没改地址就直接连不上。
        custom_archive = self.get_map("customApi")
        changed = self.ensure_provider_instance(LOCAL_PROVIDER_ID, "Lion Code 本地模型",
                                               self.local_base_url__config_provider, LOCAL_MODEL) or changed
        changed = self.ensure_provider_instance(CUSTOM_PROVIDER_ID, "自定义 API",
                                               _str(custom_archive.get("baseUrl")),
                                               _str(custom_archive.get("model"))) or changed
        changed = self.repair_custom_provider_pointing_at_local(custom_archive) or changed

        if changed:
            self.store.save()
            print(f"[配置] 模型配置已更新: mode={self.store.get('providerMode', None)}, "
                  f"provider={self.store.get('provider', None)}, "
                  f"baseUrl={self.store.get('baseUrl', None)}, "
                  f"model={self.store.get('model', None)}", flush=True)
        return changed

    def apply_installer_model_choice(self) -> bool:
        """应用安装包里选的模型版本（`~/.lioncode/install-model.txt`）。

        与上次应用过的选择不同 → 写进 `llama.modelFile` 并记下这次的选择；
        相同 → 什么都不做（这样用户在设置页里改过的模型不会被安装包的选择反复覆盖）。
        标记文件不删：重装时选了别的版本才能再次生效。
        """
        try:
            chosen = self.store.install_model_marker()
            if not chosen:
                return False
            applied = _str(self.llama_config().get("installChoice")).strip()
            if chosen == applied:
                return False    # 这次安装的选择已经应用过了
            self.store.update_llama({"modelFile": chosen, "installChoice": chosen})
            print(f"[配置] 已应用安装时选择的模型: {chosen}", flush=True)
            return True
        except Exception as e:
            print(f"[配置] 应用安装时选择的模型失败（不影响启动）: {e}", flush=True)
            return False

    # ------------------------------------------------------------------
    # 迁移与修复
    # ------------------------------------------------------------------
    def migrate_legacy_model_name(self) -> bool:
        """把历史配置里残留的底座模型名改成 lion-models1。

        生效中的 `model` / `openai.model` 两个键在本地模式下本来就由第 2 步强制覆盖，
        真正会漏下来的是 `providers` 实例里登记的可选模型列表 —— 界面读的就是它，
        所以老配置升级后下拉框里还会显示底座名字。

        只动自带的那两个实例（本地实例、或端点仍是本地端点的实例）：
        自定义模式下用户完全可能自己就填了这个模型名，那是他的配置，不能改。
        """
        raw = self.store.get("providers", None)
        if not isinstance(raw, dict):
            return False
        providers = dict(raw)
        changed = False
        for key, value in providers.items():
            if not isinstance(value, dict):
                continue
            instance = dict(value)
            is_box_instance = (key == LOCAL_PROVIDER_ID
                               or is_known_local_base_url(instance.get("baseUrl")))
            if not is_box_instance:
                continue
            touched = False
            if _str(instance.get("model")) == LEGACY_LOCAL_MODEL:
                instance["model"] = LOCAL_MODEL
                touched = True
            models = instance.get("availableModels")
            if isinstance(models, list):
                fixed: list[Any] = []
                for item in models:
                    if not isinstance(item, dict):
                        fixed.append(item)
                        continue
                    model = dict(item)
                    for field in ("modelId", "modelName"):
                        if _str(model.get(field)) == LEGACY_LOCAL_MODEL:
                            model[field] = LOCAL_MODEL
                            touched = True
                    fixed.append(model)
                if touched:
                    instance["availableModels"] = fixed
            if touched:
                providers[key] = instance
                changed = True
        if changed:
            self.store.set("providers", providers)
            print(f"[配置] 历史配置中的模型名已更新：{LEGACY_LOCAL_MODEL} → {LOCAL_MODEL}", flush=True)
        return changed

    def repair_custom_provider_pointing_at_local(self,
                                                 custom_archive: dict[str, Any]) -> bool:
        """修复历史配置：「自定义 API」实例的 baseUrl 被初始化成了本地端点。

        自定义实例指向本地端点是一个永远不会工作的组合 —— 那个端点在自定义模式下不启动。
        所以一旦发现，就换成用户存档里的端点；存档也是空的话就留空，
        让界面把输入框空着提示用户填写，而不是给他一个看似填好的错误地址。
        """
        raw = self.store.get("providers", None)
        if not isinstance(raw, dict):
            return False
        instance_raw = raw.get(CUSTOM_PROVIDER_ID)
        if not isinstance(instance_raw, dict):
            return False
        instance = dict(instance_raw)
        if not is_known_local_base_url(instance.get("baseUrl")):
            return False
        url = _str(custom_archive.get("baseUrl"))
        model = _str(custom_archive.get("model"))
        instance["baseUrl"] = url
        instance["availableModels"] = ([] if not model else
                                       [{"modelId": model, "modelName": model, "selected": False}])
        providers = dict(raw)
        providers[CUSTOM_PROVIDER_ID] = instance
        self.store.set("providers", providers)
        print("[配置] 已修正「自定义 API」实例的错误端点（原本指向本地端点），现在为："
              + (url if url else "(空，等待用户填写)"), flush=True)
        return True

    # ------------------------------------------------------------------
    # 写入辅助
    # ------------------------------------------------------------------
    def write_adapter_block(self, url: str, model: str, key: str) -> bool:
        """同步适配器级配置块。

        ChatController 读写的就是这个块（key = `openai`），不保持同步的话
        界面上改了配置、实际请求还用旧的。
        """
        block = dict(self.get_map("openai"))
        changed = False
        if url != _str(block.get("baseUrl")):
            block["baseUrl"] = url
            changed = True
        if model != _str(block.get("model")):
            block["model"] = model
            changed = True
        if key != _str(block.get("apiKey")):
            block["apiKey"] = key
            changed = True
        if changed:
            self.store.set("openai", block)
        return changed

    def ensure_provider_instance(self, provider_id: str, display: str, url: str,
                                 model: str) -> bool:
        """确保 `providers` 里登记了某个内置实例；已存在就不动（保留用户填的密钥）。"""
        raw = self.store.get("providers", None)
        providers = dict(raw) if isinstance(raw, dict) else {}
        if provider_id in providers:
            return False
        providers[provider_id] = {
            "providerId": provider_id,
            "displayName": display,
            "baseUrl": url or "",
            "apiKey": "",
            "useTokenPlan": False,
            "protocolType": "openai",
            "supportsTokenPlan": False,
            "availableModels": ([] if not model else
                                [{"modelId": model, "modelName": model, "selected": False}]),
        }
        self.store.set("providers", providers)
        return True

    def provider_instances(self) -> list[ModelProviderConfig]:
        """把配置里登记过的实例读成 `ModelProviderConfig` 列表（接口层展示用）。"""
        raw = self.store.get("providers", None)
        if not isinstance(raw, dict):
            return builtin_providers()
        out: list[ModelProviderConfig] = []
        for value in raw.values():
            if not isinstance(value, dict):
                continue
            parsed = ModelProviderConfig.from_dict({
                "providerId": value.get("providerId"),
                "displayName": value.get("displayName"),
                "standardBaseUrl": value.get("baseUrl"),
                "tokenPlanBaseUrl": value.get("tokenPlanBaseUrl"),
                "supportsTokenPlan": value.get("supportsTokenPlan", False),
                "defaultModels": [m.get("modelId") for m in value.get("availableModels", [])
                                  if isinstance(m, dict) and m.get("modelId")],
                "protocolType": value.get("protocolType", "openai"),
            })
            if parsed is not None:
                out.append(parsed)
        return out or builtin_providers()

    def _put_if_different(self, key: str, value: str) -> bool:
        """有变化才写，避免每次启动都落盘。"""
        current = _str(self.store.get(key, ""))
        if value is not None and value != current:
            self.store.set(key, value)
            return True
        return False


def _str(value: Any) -> str:
    if isinstance(value, str):
        return value
    return "" if value is None else str(value)


def _first_non_blank(a: str, b: str) -> str:
    return a if a else b


def extend(store: AppConfigStore, local_base_url_value: str | None = None) -> AppConfigExtras:
    """给一个已有的 AppConfigStore 套上补齐能力（app 启动时调一次 `init()` 即可）。"""
    return AppConfigExtras(store, local_base_url_value)


__all__ = [
    "ACTIVE_ADAPTER", "AppConfigExtras", "LEGACY_LOCAL_MODEL", "LOCAL_BASE_URL", "LOCAL_MODEL",
    "MODE_CUSTOM", "MODE_LOCAL", "TOOLCALL_AUTO", "TOOLCALL_NATIVE", "TOOLCALL_TEXT",
    "extend", "parse_tool_call_mode",
]


# ========================================================================
# 原模块 lionbox/api/providers.py
# ========================================================================
"""提供商配置接口 —— `/api/providers/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\ProviderController.java`（456 行 / 7 个接口）。

【内置模板只有一项】Java 侧刻意只保留软件自带的本地模型运行时（`ModelProviderConfig.BUILTIN_PROVIDERS`：
回环地址 + OpenAI 兼容协议，不支持 Token-Plan），没有任何云端厂商模板；这里直接用
`lionbox.config.provider.builtin_providers()`（真实模块，不是桩）里的同一份清单。

【启动期那一步不能省】Java 的 `ProviderController.restoreProviders()`（`@PostConstruct`）只是把
`app-config.json` 的 `providers` 键读回内存；真正把出厂就该有的两个实例（`lionbox-local` /
`lionbox-custom`）写进配置的，是 `AppConfigStore.applyDefaults()` 的第 4 步。Python 的 `app.py`
没有调用 `AppConfigExtras.apply_defaults()`（那是启动流程，不归本模块），所以这里在构造时补上
**其中的第 4 步**：`ensure_provider_instance()` ×2 + `repair_custom_provider_pointing_at_local()`。
不补的话：`GET /api/providers/configured` 少掉本地实例，`POST /{id}/models` 与 `/endpoint`
一律回"提供商未配置"，跟 Java 的出厂行为对不上。

【数组顺序】Java 的 `userProviders` 是 `ConcurrentHashMap`，`GET /configured` 的顺序是**桶序**
而不是插入序（`persistProviders()` 落盘的顺序也是它）。前端只做遍历，但逐字段比对时顺序也算差异，
所以 `_java_map_order()` 按同一规则排。

【服务】本模块持有 `providers` 服务（`ProviderRegistry`）：`ctx.service("providers", …)` 可取到
"用户配置过的提供商实例表"，供 chat / models 等模块复用；真实状态就是 `app-config.json` 的
`providers` 键，不另存一份。
"""


import copy
import json
import logging
import threading
import urllib.error
import urllib.request
from typing import Any
from urllib.parse import urlsplit

from lionbox.api import deps

log__api_providers = logging.getLogger("lionbox.api.providers")

#: 配置键名（Java `ProviderController.CONFIG_KEY`）
CONFIG_KEY = "providers"

#: 用户自己填端点时用的显示名（Java `template.map(...).orElse("自定义")`）
CUSTOM_DISPLAY_NAME = "自定义"

#: customApi 存档初始化时用的显示名（Java `AppConfigStore.applyDefaults` 第 4 步的字面量）
CUSTOM_ARCHIVE_DISPLAY_NAME = "自定义 API"

#: 拉取模型列表的请求预算（秒）。Java 是 connect 15s / 请求 30s 两段超时，
#: 标准库的 urllib 只有一个超时参数，取请求预算；连接建立同样受这个值约束，不会更宽松。
MODELS_TIMEOUT_SECONDS = 30

#: Java record `ProviderInstance` 的字段（顺序就是 Jackson 的输出顺序）
INSTANCE_FIELDS = ("providerId", "displayName", "baseUrl", "apiKey", "useTokenPlan",
                   "protocolType", "supportsTokenPlan", "availableModels", "tpmLimit", "rpmLimit")

#: Java record `AvailableModel` 的字段
MODEL_FIELDS = ("modelId", "modelName", "selected", "tpmLimit", "rpmLimit")


# --------------------------------------------------------------------------
# Jackson 级的小工具（类型不对时 Java 由 Spring 直接回 400，这里必须同样拒绝）
# --------------------------------------------------------------------------


class _Invalid:
    """Jackson 反序列化失败（对应 Spring 的 400 Bad Request）。"""

    def __repr__(self) -> str:      # pragma: no cover - 仅调试用
        return "<invalid>"


#: 单例哨兵：字段类型无法按 Jackson 的规则转成目标类型
INVALID = _Invalid()


def _jackson_string__api_providers(value: Any) -> str | None | _Invalid:
    """`String` 属性的反序列化：标量可以强制转成字符串，对象/数组不行。"""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    return INVALID


def _jackson_bool(value: Any) -> bool | None | _Invalid:
    """`Boolean` 属性的反序列化。

    Java 实测：`"yes"` → 400（Jackson 只认 true/false，大小写不限），`1` / `0` → true / false，
    空串 → null。照抄这套边界。
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        text = value.strip()
        if text in ("true", "True", "TRUE"):
            return True
        if text in ("false", "False", "FALSE"):
            return False
        if not text:
            return None
        return INVALID
    return INVALID


def _jackson_long(value: Any) -> int | None | _Invalid:
    """`Long` 属性的反序列化（`tpmLimit` / `rpmLimit`）。"""
    if value is None:
        return None
    if isinstance(value, bool):
        return INVALID
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)               # Jackson 对浮点取整（截断）
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return INVALID
    return INVALID


# --------------------------------------------------------------------------
# 数据形状（Java record 的 JSON 形状：**所有字段都在**，null 也要输出）
# --------------------------------------------------------------------------


def _template_json(template: ModelProviderConfig) -> dict[str, Any]:
    """`ModelProviderConfig` 的 JSON。

    【为什么不用 `ModelProviderConfig.to_dict()`】它按 `@JsonInclude(NON_NULL)` 的直觉省略了
    `tokenPlanBaseUrl`，而 Java 的 record 组件**没有** NON_NULL 注解，实测响应里带
    `"tokenPlanBaseUrl":null`。逐字段一致优先，这里显式列出 7 个字段。
    """
    return {
        "providerId": template.provider_id,
        "displayName": template.display_name,
        "standardBaseUrl": template.standard_base_url,
        "tokenPlanBaseUrl": template.token_plan_base_url,
        "supportsTokenPlan": template.supports_token_plan,
        "defaultModels": list(template.default_models),
        "protocolType": template.protocol_type,
    }


def _model_json(model_id: Any, model_name: Any, selected: Any,
                tpm_limit: Any, rpm_limit: Any) -> dict[str, Any]:
    return {"modelId": model_id, "modelName": model_name, "selected": selected,
            "tpmLimit": tpm_limit, "rpmLimit": rpm_limit}


def _instance_json(provider_id: Any, display_name: Any, base_url: Any, api_key: Any,
                   use_token_plan: Any, protocol_type: Any, supports_token_plan: Any,
                   models: Any, tpm_limit: Any, rpm_limit: Any) -> dict[str, Any]:
    return {"providerId": provider_id, "displayName": display_name, "baseUrl": base_url,
            "apiKey": api_key, "useTokenPlan": use_token_plan, "protocolType": protocol_type,
            "supportsTokenPlan": supports_token_plan, "availableModels": models,
            "tpmLimit": tpm_limit, "rpmLimit": rpm_limit}


def _masked(instance: dict[str, Any]) -> dict[str, Any]:
    """响应专用的掩码副本（Java `ProviderController.masked`）。

    **绝不能就地改内存里的实例** —— 那份 apiKey 还要用来真发请求，被掩码盖掉就再也调不通了。
    """
    out = copy.deepcopy(instance)
    out["apiKey"] = deps.SecretMask.mask(instance.get("apiKey"))
    return out


def _restore_instance(raw: Any) -> dict[str, Any] | None:
    """把配置里的一个实例反序列化成 `ProviderInstance`；坏配置返回 None（跳过）。

    【为什么"多一个字段"也算坏】Java 的 `MODEL_MAPPER` 是 `new ObjectMapper()`
    （不是 Spring 那只关掉了 FAIL_ON_UNKNOWN_PROPERTIES 的），`convertValue` 遇到未知字段会抛错，
    被 `restoreProviders` 的 catch 记成"跳过损坏的提供商配置"。照抄这条判据，
    否则同一份老配置在两边会得到不同的 provider 列表。

    缺失字段与 Java 一致：对象类型的字段（displayName / baseUrl / availableModels / tpmLimit…）
    为 null，原始 boolean 字段（useTokenPlan / supportsTokenPlan / selected）为 false。
    """
    if not isinstance(raw, dict) or set(raw) - set(INSTANCE_FIELDS):
        return None
    provider_id = _jackson_string__api_providers(raw.get("providerId"))
    if provider_id is None or isinstance(provider_id, _Invalid):
        return None                     # Java: instance.providerId() == null → 不放进表
    display_name = _jackson_string__api_providers(raw.get("displayName"))
    base_url = _jackson_string__api_providers(raw.get("baseUrl"))
    api_key = _jackson_string__api_providers(raw.get("apiKey"))
    protocol_type = _jackson_string__api_providers(raw.get("protocolType"))
    use_token_plan = _jackson_bool(raw.get("useTokenPlan"))
    supports_token_plan = _jackson_bool(raw.get("supportsTokenPlan"))
    tpm_limit = _jackson_long(raw.get("tpmLimit"))
    rpm_limit = _jackson_long(raw.get("rpmLimit"))
    parsed = [display_name, base_url, api_key, protocol_type,
              use_token_plan, supports_token_plan, tpm_limit, rpm_limit]
    if any(isinstance(v, _Invalid) for v in parsed):
        return None

    models_raw = raw.get("availableModels")
    if models_raw is None:
        models: Any = None
    elif isinstance(models_raw, list):
        models = []
        for item in models_raw:
            model = _restore_model(item)
            if model is None:
                return None             # 坏元素 → 整条实例反序列化失败
            models.append(model)
    else:
        return None

    return _instance_json(provider_id, display_name, base_url, api_key,
                          bool(use_token_plan), protocol_type, bool(supports_token_plan),
                          models, tpm_limit, rpm_limit)


def _restore_model(raw: Any) -> dict[str, Any] | None:
    """`AvailableModel` 的反序列化（坏元素 → None → 整条实例被跳过）。"""
    if not isinstance(raw, dict) or set(raw) - set(MODEL_FIELDS):
        return None
    model_id = _jackson_string__api_providers(raw.get("modelId"))
    model_name = _jackson_string__api_providers(raw.get("modelName"))
    selected = _jackson_bool(raw.get("selected"))
    tpm_limit = _jackson_long(raw.get("tpmLimit"))
    rpm_limit = _jackson_long(raw.get("rpmLimit"))
    if any(isinstance(v, _Invalid) for v in (model_id, model_name, selected, tpm_limit, rpm_limit)):
        return None
    return _model_json(model_id, model_name, bool(selected), tpm_limit, rpm_limit)


def _java_string_hash(text: str) -> int:
    """Java `String.hashCode()`（int32 溢出语义）。"""
    h = 0
    for ch in text:
        h = (h * 31 + ord(ch)) & 0xFFFFFFFF
    return h


def _java_spread(text: str) -> int:
    """`ConcurrentHashMap.spread(h) = (h ^ (h >>> 16)) & 0x7fffffff`。"""
    h = _java_string_hash(text)
    return (h ^ (h >> 16)) & 0x7FFFFFFF


def _java_map_order(keys: Any) -> list[str]:
    """按 Java `ConcurrentHashMap` 的迭代顺序排列键（桶序，桶内保持插入序）。

    `ProviderController.userProviders` 是 ConcurrentHashMap，`GET /configured` 与
    `persistProviders()` 的顺序都由它决定。默认容量 16、负载因子 0.75，超过阈值翻倍。
    """
    ordered = list(keys)
    capacity = 16
    while len(ordered) > capacity - capacity // 4:
        capacity <<= 1
    buckets: dict[int, list[str]] = {}
    for key in ordered:
        buckets.setdefault(_java_spread(key) % capacity, []).append(key)
    return [k for index in sorted(buckets) for k in buckets[index]]


def _truncate__api_providers(text: Any, max_len: int) -> str:
    """Java `ProviderController.truncate`（日志里截断长响应体）。"""
    if text is None:
        return ""
    s = str(text)
    return s if len(s) <= max_len else s[:max_len] + "..."


def _is_loopback_url(url: Any) -> bool:
    """URL 的主机是不是回环地址（Java `isLoopbackUrl`）。

    【必须比主机名，不能比字符串前缀】`http://localhost.evil.com` / `http://127.0.0.1.attacker.com`
    都能骗过前缀比较；而这是"没有内置模板的自定义端点"唯一的闸门，
    过了闸之后 `POST /{id}/models` 会**带着用户存下来的密钥**去请求那个地址。
    Java 只比主机名（不看 scheme），`ftp://127.0.0.1/v1` 也算回环 —— 照抄，不擅自加严。
    """
    if url is None or not str(url).strip():
        return False
    try:
        host = urlsplit(str(url).strip()).hostname
    except ValueError:
        return False
    if host is None:
        return False
    host = host.lower()
    if host.startswith("[") and host.endswith("]"):
        host = host[1:-1]               # Java 同时认 "::1" 与 "[::1]"
    return host in ("127.0.0.1", "localhost", "::1", "0.0.0.0")


def _is_json_media_type(media_type: str) -> bool:
    """Spring 的 Jackson 转换器只认 `application/json` 与 `application/*+json`。"""
    return media_type == "application/json" or (
        media_type.startswith("application/") and media_type.endswith("+json"))


def _read_json_object(req: Request) -> Any:
    """复刻 Spring 对 `@RequestBody` 形状的校验：返回 dict（可继续）或 `Response`（400/415）。

    Java 实测：请求体为空 → 400；请求体不是 JSON 对象（`null` / `[]` / `"x"` / 数字 / 坏 JSON）
    → 400；Content-Type 不是 JSON → 415。响应体是 Spring 默认错误体（`deps.spring_error`）。

    【一处已知差异】Java 在**没有** Content-Type 头时也回 415（Spring 把缺失的 Content-Type
    当成 application/octet-stream）。Python 侧没有这个头就按 JSON 处理：`.lbverify` 的 harness
    不带任何头，若照抄 415 就没法在进程内验证 POST 接口；真实调用方（web/index.html、
    VS Code 插件）都会带 `application/json`。
    """
    media_type = (req.header("content-type") or "").split(";")[0].strip().lower()
    if not req.body:
        return deps.spring_error(400, req.path)
    if media_type and not _is_json_media_type(media_type):
        return deps.spring_error(415, req.path, "Unsupported Media Type")
    try:
        parsed = json.loads(req.body.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return deps.spring_error(400, req.path)
    if not isinstance(parsed, dict):
        return deps.spring_error(400, req.path)
    return parsed


def _read_configure_request(body: dict[str, Any], path: str) -> Any:
    """`ConfigureRequest` 的反序列化：字段类型收不下就 400（Jackson 的边界）。"""
    provider_id = _jackson_string__api_providers(body.get("providerId"))
    api_key = _jackson_string__api_providers(body.get("apiKey"))
    use_token_plan = _jackson_bool(body.get("useTokenPlan"))
    custom_base_url = _jackson_string__api_providers(body.get("customBaseUrl"))
    if any(isinstance(v, _Invalid)
           for v in (provider_id, api_key, use_token_plan, custom_base_url)):
        return deps.spring_error(400, path)
    return {"providerId": provider_id, "apiKey": api_key,
            "useTokenPlan": use_token_plan, "customBaseUrl": custom_base_url}


def _read_switch_request(body: dict[str, Any], path: str) -> Any:
    """`SwitchEndpointRequest` 的反序列化。"""
    endpoint_type = _jackson_string__api_providers(body.get("endpointType"))
    if isinstance(endpoint_type, _Invalid):
        return deps.spring_error(400, path)
    return {"endpointType": endpoint_type}


def _jackson_text(node: Any) -> str:
    """Jackson `JsonNode.asText("")` 的等价物（解析 `/v1/models` 的响应时用）。"""
    if node is None:
        return ""
    if isinstance(node, str):
        return node
    if isinstance(node, bool):
        return "true" if node else "false"
    if isinstance(node, (int, float)):
        return str(node)
    return ""                           # 对象/数组：Jackson 的 ContainerNode.asText() 是空串


def _fetch_models_from_api(instance: dict[str, Any]) -> list[dict[str, Any]]:
    """实时调用提供商的 `/models`（OpenAI 兼容格式）；失败返回空列表（Java 同名方法）。"""
    base_url = instance.get("baseUrl")
    if base_url is None or not str(base_url).strip():
        return []
    url = str(base_url)
    if not url.endswith("/"):
        url += "/"
    url += "models"

    log__api_providers.info("拉取模型列表: %s (%s)", instance.get("displayName"), url)
    headers = {"Accept": "application/json"}
    api_key = instance.get("apiKey")
    if api_key is not None and str(api_key).strip():
        headers["Authorization"] = "Bearer " + str(api_key)   # 未配密钥就不发这个头

    request = urllib.request.Request(url, headers=headers, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=MODELS_TIMEOUT_SECONDS) as response:
            status = int(response.status)
            raw = response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        try:
            detail = e.read().decode("utf-8", errors="replace")
        except OSError:
            detail = ""
        log__api_providers.warning("拉取模型列表失败: HTTP %s - %s", e.code, _truncate__api_providers(detail, 300))
        return []
    except (urllib.error.URLError, OSError, ValueError) as e:
        log__api_providers.warning("拉取模型列表异常: %s", e)
        return []

    if status < 200 or status >= 300:
        log__api_providers.warning("拉取模型列表失败: HTTP %s - %s", status, _truncate__api_providers(raw, 300))
        return []
    try:
        root = json.loads(raw)
    except ValueError:
        log__api_providers.warning("模型列表响应格式异常: %s", _truncate__api_providers(raw, 300))
        return []
    data = root.get("data") if isinstance(root, dict) else None
    if not isinstance(data, list):
        log__api_providers.warning("模型列表响应格式异常: %s", _truncate__api_providers(raw, 300))
        return []

    models: list[dict[str, Any]] = []
    for node in data:
        if not isinstance(node, dict):
            continue
        model_id = _jackson_text(node.get("id"))
        if not model_id.strip():
            continue
        display_name = node.get("display_name")
        text = _jackson_text(display_name)
        models.append(_model_json(model_id, text if text.strip() else model_id,
                                  False, None, None))
    return models


# --------------------------------------------------------------------------
# 服务：用户配置过的提供商实例表（Java `ProviderController.userProviders`）
# --------------------------------------------------------------------------


class ProviderRegistry:
    """`/api/providers` 的内存状态。

    Java 里是 `ConcurrentHashMap<String, ProviderInstance>`，持久化在 `app-config.json` 的
    `providers` 键；这里同构：`dict[str, dict]`，值是 `ProviderInstance` 的 JSON 形状
    （10 个字段全在，null 也保留，落盘后再读回来不会"多字段损坏"）。
    """

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx
        self.cfg = ctx.cfg
        # 与 Java `AppConfigStore` 的启动初始化共用一份实现（不重复实现别人的模块）
        self.extras = ctx.service("app_config_extras", lambda: AppConfigExtras(ctx.cfg))
        self._instances: dict[str, dict[str, Any]] = {}
        self._lock = threading.RLock()
        self.restore()

    # ------------------------------------------------------------ 模板
    @staticmethod
    def templates() -> list[ModelProviderConfig]:
        return builtin_providers()

    @staticmethod
    def template(provider_id: str) -> ModelProviderConfig | None:
        for template in builtin_providers():
            if template.provider_id == provider_id:
                return template
        return None

    def default_models(self, provider_id: str) -> list[str]:
        template = self.template(provider_id)
        return list(template.default_models) if template is not None else []

    # ------------------------------------------------------------ 启动恢复
    def restore(self) -> None:
        """对应 Java 的 `AppConfigStore.applyDefaults()` 第 4 步 + `restoreProviders()`。"""
        self._ensure_builtin_instances()
        saved = self.extras.get_map(CONFIG_KEY)
        restored: dict[str, dict[str, Any]] = {}
        for key, value in saved.items():
            instance = _restore_instance(value)
            if instance is None:
                log__api_providers.warning("跳过损坏的提供商配置: %s", key)
                continue
            restored[str(instance["providerId"])] = instance
        with self._lock:
            self._instances = restored
        log__api_providers.info("已从磁盘恢复 %d 个提供商配置", len(restored))

    def _ensure_builtin_instances(self) -> None:
        """把出厂内置的两个实例登记进配置（Java `ensureProviderInstance` / 修复历史端点）。

        已存在的实例**不动**，保留用户填的端点与密钥。
        """
        local = self.template(LOCAL_PROVIDER_ID)
        if local is not None:
            self.extras.ensure_provider_instance(
                local.provider_id, local.display_name, local.standard_base_url,
                local.default_models[0] if local.default_models else "")
        custom_archive = self.extras.get_map("customApi")
        self.extras.ensure_provider_instance(
            CUSTOM_PROVIDER_ID, CUSTOM_ARCHIVE_DISPLAY_NAME,
            deps.as_str(custom_archive.get("baseUrl")), deps.as_str(custom_archive.get("model")))
        self.extras.repair_custom_provider_pointing_at_local(custom_archive)

    # ------------------------------------------------------------ 读写
    def instances(self) -> list[dict[str, Any]]:
        """全部实例（顺序＝Java ConcurrentHashMap 的桶序，掩码未处理）。"""
        with self._lock:
            order = _java_map_order(self._instances)
            return [copy.deepcopy(self._instances[pid]) for pid in order]

    def get(self, provider_id: str) -> dict[str, Any] | None:
        with self._lock:
            found = self._instances.get(provider_id)
            return copy.deepcopy(found) if found is not None else None

    def put(self, instance: dict[str, Any]) -> dict[str, Any]:
        with self._lock:
            self._instances[str(instance.get("providerId"))] = copy.deepcopy(instance)
        self.persist()
        return instance

    def remove(self, provider_id: str) -> None:
        with self._lock:
            self._instances.pop(provider_id, None)
        self.persist()

    def persist(self) -> None:
        """落盘到 `app-config.json`（Java `persistProviders()`：整表覆盖，顺序同内存）。"""
        with self._lock:
            payload = {pid: copy.deepcopy(self._instances[pid])
                       for pid in _java_map_order(self._instances)}
        self.cfg.set(CONFIG_KEY, payload)


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class ProvidersApi:
    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx
        # 本模块持有 `providers` 服务（提供商实例表的唯一来源）；已装过真实现就复用它
        self.registry: ProviderRegistry = ctx.service(
            "providers", lambda: ProviderRegistry(ctx))

    # ------------------------------------------------------------ 业务
    def _build_instance(self, request: dict[str, Any],
                        template: ModelProviderConfig | None) -> dict[str, Any]:
        """按 Java `configureProvider` 的规则造一个新的 `ProviderInstance`。"""
        provider_id = str(request["providerId"])
        api_key = request["apiKey"]
        is_token_plan = request["useTokenPlan"] is True          # Java: Boolean.TRUE.equals(...)
        if template is not None:
            if (is_token_plan and template.supports_token_plan
                    and template.token_plan_base_url is not None):
                base_url = template.token_plan_base_url
            else:
                base_url = template.standard_base_url
            display_name = template.display_name
            protocol_type = template.protocol_type
            supports_token_plan = template.supports_token_plan
        else:
            base_url = request["customBaseUrl"]
            display_name = CUSTOM_DISPLAY_NAME
            protocol_type = "openai"
            supports_token_plan = False

        # 【密钥掩码识别】`GET /configured` 回的是掩码，界面原样回填、用户不改就原样提交；
        # 这里必须把"掩码"当成"没改"，沿用已存的真密钥，否则保存一次就把密钥写成
        # "sk-••••abcd"，之后所有调用都鉴权失败。
        existing = self.registry.get(provider_id)
        if api_key is None or not str(api_key).strip() or deps.SecretMask.is_mask(api_key):
            if existing is not None:
                api_key = existing.get("apiKey")
        return _instance_json(provider_id, display_name, base_url, api_key, is_token_plan,
                              protocol_type, supports_token_plan, [], None, None)

    def _fetch_and_cache_models(self, provider_id: str, instance: dict[str, Any]) -> tuple[list[dict[str, Any]], bool]:
        """拉模型列表 → 回退内置默认 → 更新实例缓存并落盘；返回 (模型, 是否来自实时接口)。"""
        models = _fetch_models_from_api(instance)
        from_api = len(models) > 0
        if not from_api:
            models = [_model_json(mid, mid, False, None, None)
                      for mid in self.registry.default_models(provider_id)]
            log__api_providers.warning("提供商 %s 模型列表实时获取失败，使用内置默认模型 %d 个",
                        provider_id, len(models))
        else:
            log__api_providers.info("提供商 %s 模型列表获取成功: %d 个模型", provider_id, len(models))
        updated = copy.deepcopy(instance)
        updated["availableModels"] = models
        self.registry.put(updated)
        return models, from_api

    # ------------------------------------------------------------ 注册
    def register__api_providers(self, router) -> None:
        api = self

        @router.get("/api/providers/templates")
        def get_templates(req: Request):
            return ApiResponse.ok([_template_json(t) for t in api.registry.templates()])

        @router.get("/api/providers/templates/token-plan")
        def get_token_plan_templates(req: Request):
            return ApiResponse.ok([_template_json(t) for t in api.registry.templates()
                                   if t.supports_token_plan])

        @router.post("/api/providers/configure")
        def configure_provider(req: Request):
            body = _read_json_object(req)
            if isinstance(body, Response):
                return body
            request = _read_configure_request(body, req.path)
            if isinstance(request, Response):
                return request
            provider_id = request["providerId"]
            if provider_id is None or not provider_id.strip():
                return ApiResponse.error("缺少 providerId")
            template = api.registry.template(provider_id)
            custom_base_url = request["customBaseUrl"]
            if template is None and custom_base_url is None:
                return ApiResponse.error("未找到提供商模板: " + provider_id)
            # 本地模式只允许回环端点：没有内置模板时，这是唯一一道闸
            if template is None and not _is_loopback_url(custom_base_url):
                return ApiResponse.error(
                    "本产品仅支持本机（回环地址）的模型端点，不支持外部服务商: " + provider_id)
            try:
                instance = api._build_instance(request, template)
                api.registry.put(instance)
            except Exception as e:          # Java: catch (Exception e) → "配置失败: " + getMessage()
                log__api_providers.warning("配置提供商失败: %s", e, exc_info=True)
                message = str(e) or "null"  # NPE 之类没有 message，Java 拼出来就是 "null"
                return ApiResponse.error("配置失败: " + message)
            log__api_providers.info("提供商已配置: %s (%s)", instance["displayName"],
                     "Token-Plan" if instance["useTokenPlan"] else "普通按量")
            return ApiResponse.ok(_masked(instance), "提供商配置成功")

        @router.get("/api/providers/configured")
        def get_configured_providers(req: Request):
            return ApiResponse.ok([_masked(i) for i in api.registry.instances()])

        @router.post("/api/providers/{providerId}/models")
        def fetch_models(req: Request):
            provider_id = req.params["providerId"]
            instance = api.registry.get(provider_id)
            if instance is None:
                return ApiResponse.error("提供商未配置: " + provider_id)
            models, from_api = api._fetch_and_cache_models(provider_id, instance)
            result = {"providerId": instance["providerId"], "baseUrl": instance.get("baseUrl"),
                      "models": models, "tpmLimit": instance.get("tpmLimit"),
                      "rpmLimit": instance.get("rpmLimit")}
            return ApiResponse.ok(result,
                                  "模型列表获取成功" if from_api else "使用内置默认模型列表")

        @router.post("/api/providers/{providerId}/endpoint")
        def switch_endpoint(req: Request):
            body = _read_json_object(req)
            if isinstance(body, Response):
                return body
            request = _read_switch_request(body, req.path)
            if isinstance(request, Response):
                return request
            provider_id = req.params["providerId"]
            instance = api.registry.get(provider_id)
            if instance is None:
                return ApiResponse.error("提供商未配置: " + provider_id)
            if not instance.get("supportsTokenPlan"):
                return ApiResponse.error("该提供商不支持Token-Plan切换")
            template = api.registry.template(provider_id)
            if template is None:
                return ApiResponse.error("未找到提供商模板")
            use_token_plan = request["endpointType"] == "token-plan"
            updated = copy.deepcopy(instance)
            updated["baseUrl"] = (template.token_plan_base_url if use_token_plan
                                  else template.standard_base_url)
            updated["useTokenPlan"] = use_token_plan
            api.registry.put(updated)
            log__api_providers.info("端点已切换: %s -> %s", provider_id,
                     "Token-Plan" if use_token_plan else "普通按量")
            return ApiResponse.ok(_masked(updated), "端点已切换")

        @router.delete("/api/providers/{providerId}")
        def remove_provider(req: Request):
            api.registry.remove(req.params["providerId"])
            return ApiResponse.ok(None, "提供商已删除")


def register__api_providers(router, ctx) -> None:
    ProvidersApi(ctx).register__api_providers(router)


# ========================================================================
# 原模块 lionbox/api/plugins.py
# ========================================================================
"""插件管理接口 —— `/api/plugins/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\PluginController.java`（611 行 / 23 个接口）。

【本模块是"一切皆插件"的门面】它把已就绪的插件基础设施拼成前端要的那份 JSON：
  * `plugins/base.py`       —— 工具基类、九类枚举（`PluginKind`）；
  * `plugins/lifecycle.py`  —— 设置持久化 / 注册表 / 加载器 / 系统插件 / 门禁 SPI；
  * `team/`、`automation/`、`plugins/review.py` —— 团队、自动化、自动授权审查；
  * `skills/`               —— 四个内置技能与 `skill_load`；
  * `plugindev/`            —— 开发模式开关（本模块只读它的 `is_dev_mode()`）。
老字段（`success`/`message`/`data`/`error`）与新字段（`ok`/`devMode`/`pluginsDir`/`kinds`/
`plugins`/`scanDirs`）**同时**返回 —— 加字段比改字段安全一百倍，前端与 VS Code 插件各读各的。

【装配点为什么落在本模块】`app.py` 与 `api/__init__.py` 都是冻结件（SPEC 明令不许改），
而"插件体系有没有被装起来"只有这里必须知道：`GET /api/plugins` 要的是完整注册表
（58 个工具 + 2 个团队工具 + 4 个技能 + 7 个系统插件 = 71 个，与 Java 实测一致）。
所以 `__init__` 里调一次 `ensure_plugin_runtime()`：**幂等、非侵入** ——
装配方在 app 启动时已经装过（注册表非空）就一个都不动。

【两处数组顺序不是契约】Java 侧 `TerminalPlugin.OWNED_TOOL_NAMES` 与
`ApprovalReviewPlugin.DEFAULT_REVIEW_TOOLS` 都是 `Set.of(...)`：JDK 对 `Set.of` 的迭代顺序
不保证（实际按 JVM 随机盐打乱，每次启动都可能不同，探针文件里的那个顺序只是当时那一次）。
所以 `ownedTools` / `defaultTools`（以及用户没配过 `tools` 时的 `review.tools`）在 Python 侧
给**确定性**顺序（字典序）；用户配置过的 `tools` 则按用户给的顺序（对应 Java 的 LinkedHashSet）。
逐字段比对时这三个数组按集合比。
"""


import datetime as _dt
from typing import Any

from lionbox.automation.plugin import AutomationPlugin
from lionbox.automation.task import now_utc
from lionbox.plugindev.service import PluginDevService
from lionbox.plugins.base import PluginKind
from lionbox.plugins.lifecycle import AgentLoopPlugin, PluginGateSpi, PluginLoader, PluginSettings, TerminalPlugin, bootstrap_system_plugins, default_paths, default_registry, default_settings, register_spi, registered_spis
from lionbox.plugins.review import ApprovalReviewPlugin
from lionbox.team.agent_team import AgentTeamPlugin
from lionbox.team.subagent import SubAgentPlugin
from lionbox.api import deps

# ---- 我拥有的服务（别的模块要用插件设置/注册表时从这里取，不要自己 new）----
SERVICE_PATHS = "plugin_paths"          # PluginPaths
SERVICE_SETTINGS = "plugin_settings"    # PluginSettings（settings.json 的唯一真身）
SERVICE_REGISTRY = "plugin_registry"    # plugins.lifecycle.PluginRegistry（九类索引）
SERVICE_LOADER = "plugin_loader"        # PluginLoader（外置插件扫描/热插拔）
SERVICE_DEV = "plugin_dev"              # PluginDevService（开发模式开关）

#: 判定"插件体系已经装好了"用的几个哨兵 id（分别代表工具 / 技能 / 系统插件三块）
_TOOL_SENTINEL = "tool.file.read"
_SKILL_SENTINEL = "skill.backend"
_SYSTEM_SENTINEL = TerminalPlugin.PLUGIN_ID


# --------------------------------------------------------------------------
# 装配（幂等）
# --------------------------------------------------------------------------


def ensure_plugin_runtime(registry: Any, settings: Any) -> list[str]:
    """把插件体系装齐：工具 → 团队工具 → 系统插件 → 技能 + 门禁 SPI。

    【为什么要这个函数】Java 侧由 `PluginBootstrap` + `PluginAutoRegistration` 在 Spring 启动时
    干这件事；Python 侧 `app.py` 是冻结件（不许改），装配只能落在"唯一必须拿到完整注册表"的
    地方，也就是本模块。做法保证三点：

      1. **幂等**：三块各自按哨兵 id 判断缺不缺，装过的一律不碰（装配方在 app 里装过也认）；
      2. **非侵入**：全部走已就绪模块自己的公开入口（`PluginRegistry.load_all` /
         `team.registrar.register_team_tools` / `lifecycle.bootstrap_system_plugins` /
         `skills.bootstrap_skills`），不重复实现任何一方的逻辑；
      3. **坏一块不能全废**：某一步失败只记进返回值并打控制台，接口照样能开
         （Java 侧的插件系统也是这个原则），绝不假装成功。

    :return: 装配过程中的问题列表（空 = 全部就绪）。
    """
    problems: list[str] = []

    if registry.get_by_id(_TOOL_SENTINEL) is None:
        try:
            registry.load_all()
        except Exception as e:      # noqa: BLE001 —— 装载失败要能开界面看原因，不能把接口带挂
            problems.append(f"工具装载失败: {type(e).__name__}: {e}")
            print(f"[插件] 工具装载失败（接口继续可用）: {type(e).__name__}: {e}", flush=True)

    try:
        from lionbox.team.registrar import register_team_tools
        register_team_tools(registry)
    except Exception as e:          # noqa: BLE001
        problems.append(f"团队工具注册失败: {type(e).__name__}: {e}")
        print(f"[插件] 团队工具注册失败（接口继续可用）: {type(e).__name__}: {e}", flush=True)

    if registry.get_by_id(_SYSTEM_SENTINEL) is None:
        try:
            bootstrap_system_plugins(registry)
        except Exception as e:      # noqa: BLE001
            problems.append(f"系统插件注册失败: {type(e).__name__}: {e}")
            print(f"[插件] 系统插件注册失败（接口继续可用）: {type(e).__name__}: {e}", flush=True)

    if registry.get_by_id(_SKILL_SENTINEL) is None:
        try:
            from lionbox.skills import bootstrap_skills
            bootstrap_skills(registry)
        except Exception as e:      # noqa: BLE001
            problems.append(f"技能装载失败: {type(e).__name__}: {e}")
            print(f"[插件] 技能装载失败（接口继续可用）: {type(e).__name__}: {e}", flush=True)

    # 门禁 SPI：用户在设置里关掉某个插件之后，它的工具必须真的从下发给模型的清单里消失
    # （等价 Java `PluginBootstrap` 里注册 PluginGateSpi 的那一步）。已经有人装过就不重复装。
    try:
        if not any(_spi_name(s) == "插件开关门禁" for s in registered_spis()):
            register_spi(PluginGateSpi(registry, settings))
    except Exception as e:          # noqa: BLE001
        problems.append(f"插件门禁 SPI 注册失败: {type(e).__name__}: {e}")
        print(f"[插件] 门禁 SPI 注册失败（开关仍会落盘）: {type(e).__name__}: {e}", flush=True)

    return problems


def _spi_name(spi: Any) -> str:
    try:
        return str(spi.spi_name())
    except Exception:               # noqa: BLE001 —— 第三方 SPI 的属性写崩了不能连累装配
        return ""


# --------------------------------------------------------------------------
# 取值助手（Java 同名静态方法的等价物）
# --------------------------------------------------------------------------


def _long_of(value: Any) -> int | None:
    """Java `PluginController.longOf`：Number → longValue；其余 parseLong(trim)，失败 → null。

    【Boolean 必须单独挡掉】Java 里 `Boolean` **不是** `Number`，`parseLong("true")` 会抛，
    于是 `intOf(true)` 得到 0（而不是 1）—— 这里必须一致，否则前端把开关的 true 传进数字字段
    时两边算出来的值会不一样。
    """
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    try:
        return int(str(value).strip())
    except ValueError:
        return None


def _int_of(value: Any) -> int:
    """Java `intOf`：`longOf(v)` 再 `intValue()`（低 32 位有符号，与 Java 的截断规则一致）。"""
    long_value = _long_of(value)
    if long_value is None:
        return 0
    return ((long_value + 0x80000000) & 0xFFFFFFFF) - 0x80000000


def _bool_of(value: Any) -> bool | None:
    """Java `Boolean.valueOf(String.valueOf(v))`：只认 "true"（大小写不敏感），其余 false。

    注意与"宽松读配置"（`as_bool`）的区别：这里是**请求体**校验，`1` / "是" 都算 false。
    """
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def _java_str(value: Any) -> str:
    """Java `String.valueOf(v)`：布尔输出小写 true/false（Python 的 str(True) 是 "True"）。"""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _str_of(body: dict[str, Any], key: str) -> str | None:
    """Java `PluginController.str(body, key)`：键不存在或值为 null → **null**（不是空串）。"""
    value = body.get(key)
    return None if value is None else _java_str(value)


def _attr(obj: Any, name: str, fallback: Any) -> Any:
    """读插件属性并兜异常/缺失。

    Java 的插件属性是接口方法（第三方插件写崩了会让整个接口 500），Python 是 @property ——
    同样是"别人的代码"，同样要兜（与 Java `safeKind` 的兜底同一语义）。
    """
    try:
        value = getattr(obj, name)
    except Exception:               # noqa: BLE001
        return fallback
    return fallback if value is None else value


def _is_initialized(plugin: Any) -> bool:
    """Java `Plugin.isInitialized()`；`base.ToolPlugin` 没有这个方法（Java 侧工具恒为 true）。"""
    method = getattr(plugin, "is_initialized", None)
    if not callable(method):
        return True
    try:
        return bool(method())
    except Exception:               # noqa: BLE001
        return False


def _instant_text__api_plugins(moment: _dt.datetime) -> str:
    """Java `Instant.toString()` 的等价物：UTC、秒后小数按 0/3/6/9 位去掉多余的零。"""
    if moment.tzinfo is not None:
        moment = moment.astimezone(_dt.timezone.utc)
    micros = moment.microsecond
    if micros == 0:
        fraction = ""
    elif micros % 1000 == 0:
        fraction = f".{micros // 1000:03d}"
    else:
        fraction = f".{micros:06d}"
    return moment.strftime("%Y-%m-%dT%H:%M:%S") + fraction + "Z"


# --------------------------------------------------------------------------
# 接口实现
# --------------------------------------------------------------------------


class PluginsApi:
    """`PluginController` 的 Python 实现（一个方法对应 Java 的一个 @Mapping）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx
        self.paths = ctx.service(SERVICE_PATHS, default_paths)
        self.settings = ctx.service(SERVICE_SETTINGS, default_settings)
        self.registry = self._resolve_registry()
        self.loader = ctx.service(SERVICE_LOADER, lambda: PluginLoader(self.registry, self.paths))
        self.dev = ctx.service(SERVICE_DEV, lambda: PluginDevService(self.paths, self.settings))

        # 装配（幂等）：注册表是空的时候才动手，装过就一个都不碰
        self.problems = ensure_plugin_runtime(self.registry, self.settings)

        # 六个系统插件的真身：优先用注册表里那一个（"同一份状态"才有意义），
        # 注册表里没有（装配方换过注册表）才自己造一个 —— 它们都只是无状态的门面 + 设置读写。
        self.terminal = self._system(TerminalPlugin.PLUGIN_ID, lambda: TerminalPlugin(self.settings))
        self.loop = self._system(AgentLoopPlugin.PLUGIN_ID, lambda: AgentLoopPlugin(self.settings))
        self.subagent = self._system(SubAgentPlugin.PLUGIN_ID, lambda: SubAgentPlugin(self.settings))
        self.team = self._system(AgentTeamPlugin.PLUGIN_ID, lambda: AgentTeamPlugin(self.settings))
        self.review = self._system(ApprovalReviewPlugin.PLUGIN_ID,
                                   lambda: ApprovalReviewPlugin(self.settings))
        self.automation = self._system(AutomationPlugin.PLUGIN_ID,
                                       lambda: AutomationPlugin(self.settings))

    # ------------------------------------------------------------ 基础设施
    def _resolve_registry(self) -> Any:
        """生命周期注册表（九类索引 + 系统插件）。"""
        registry = self.ctx.service(SERVICE_REGISTRY, default_registry)
        if not hasattr(registry, "kind_counts"):        # 被装成了 base.REGISTRY（只有工具收集）
            registry = default_registry()
            self.ctx.install(SERVICE_REGISTRY, registry)
        return registry

    def _system(self, plugin_id: str, factory: Any) -> Any:
        plugin = self.registry.get_by_id(plugin_id)
        return plugin if plugin is not None else factory()

    @staticmethod
    def _required_body(req: Request) -> dict[str, Any] | None:
        """Spring `@RequestBody Map<String, Object>` 的等价物：拿不到对象体 → None（回 400）。

        【为什么必须区分「{}」和「没有体」】Java 侧 `@RequestBody` 是 required 的：不带请求体、
        或体不是 JSON 对象时，Spring 在**进方法体之前**就回 400
        （`{"timestamp","status":400,"error":"Bad Request","path":…}`），方法体一行都不执行；
        而带一个 `{}` 是合法请求，会真的走到方法体里的校验分支。两者语义完全不同。
        """
        if not req.body or not req.body.strip():
            return None
        value = req.json
        return value if isinstance(value, dict) else None

    # ------------------------------------------------------------ 视图组装
    @staticmethod
    def _kind_of(plugin: Any) -> str:
        """Java `PluginController.safeKind`：kind 为 null / 抛异常 → ADVANCED_TOOL。

        Java 的 `getKind()` 返回枚举（不可能有非法值），Python 是字符串，所以非法值
        一律按进阶工具归类 —— 与 Java 的兜底落在同一个值上。
        """
        try:
            kind = plugin.kind
        except Exception:               # noqa: BLE001
            return PluginKind.ADVANCED_TOOL
        if not isinstance(kind, str) or kind not in PluginKind.DISPLAY:
            return PluginKind.ADVANCED_TOOL
        return kind

    @staticmethod
    def _legacy_info(plugin: Any) -> dict[str, Any]:
        """老的 `LegacyPluginInfo`（前端读 type/name/description，一个字都不能改）。"""
        return {
            "id": plugin.id,
            "name": _attr(plugin, "name", plugin.id),
            "description": _attr(plugin, "description", ""),
            "type": _attr(plugin, "type", "TOOL"),
            "version": _attr(plugin, "version", "1.0.0") or "1.0.0",
            "initialized": _is_initialized(plugin),
        }

    def _plugin_views(self) -> list[dict[str, Any]]:
        """注册表里的插件 + 加载失败的来源（坏插件也要在列表里看得见）。"""
        out: list[dict[str, Any]] = []
        for plugin in self.registry.get_all_plugins():
            external = self.loader.origin(plugin.id) is not None
            kind = self._kind_of(plugin)
            display, _ = PluginKind.DISPLAY.get(kind, ("", ""))
            name = _attr(plugin, "name", plugin.id)
            out.append({
                "id": plugin.id,
                "name": name,
                "kind": kind,
                "kindDisplayName": display,
                "description": _attr(plugin, "description", ""),
                "version": _attr(plugin, "version", "1.0.0") or "1.0.0",
                "enabled": bool(self.settings.is_enabled(plugin)),
                "builtin": not external,
                "hotReloadable": bool(external or _attr(plugin, "hot_reloadable", False)),
                "error": self.registry.get_error(plugin.id),
                "source": "external" if external else _attr(plugin, "source", "builtin"),
                "displayName": _attr(plugin, "display_name", name) or name,
                "broken": False,
            })
        # 加载失败的来源：id 用 `jar:<文件名>`（用户"我明明放了插件怎么列表里没有"的唯一解药）
        for failure in self.loader.get_failures():
            jar = _java_str(failure.get("jar") or "")
            plugin_id = _java_str(failure.get("pluginId") or "")
            failure_id = f"jar:{jar}" if (not plugin_id.strip() or "." in plugin_id) \
                else f"jar:{jar}:{plugin_id}"
            out.append({
                "id": failure_id,
                "name": jar,
                "kind": "UNKNOWN",
                "kindDisplayName": "加载失败",
                "description": "这个 jar 没能加载成功，错误见 error 字段",
                "version": "-",
                "enabled": False,
                "builtin": False,
                "hotReloadable": False,
                "error": failure.get("message"),
                "source": "external",
                "displayName": jar + "（加载失败）",
                "broken": True,
            })
        out.sort(key=lambda view: view["id"])
        return out

    def _kind_views(self) -> list[dict[str, Any]]:
        counts = self.registry.kind_counts()
        return [{"name": kind, "displayName": PluginKind.DISPLAY[kind][0],
                 "description": PluginKind.DISPLAY[kind][1],
                 "count": int(counts.get(kind, 0))}
                for kind in PluginKind.DISPLAY]

    @staticmethod
    def _owned_tools() -> list[str]:
        """终端插件"管着"的工具名。顺序见模块 docstring（Java 侧是 Set.of，不是契约）。"""
        return sorted(TerminalPlugin.OWNED_TOOL_NAMES)

    def _review_tools(self) -> list[str]:
        """当前的审查清单。

        用户配过 → 按用户给的顺序（Java 是 LinkedHashSet，保序）；没配过 / 全是空白项 →
        Java 的 `DEFAULT_REVIEW_TOOLS`，那是 `Set.of`（顺序不保证），这里取字典序。
        """
        raw = self.settings.section("review").get("tools")
        if isinstance(raw, list) and raw:
            names: list[str] = []
            for item in raw:
                if item is None:
                    continue
                text = _java_str(item).strip()
                if text and text not in names:
                    names.append(text)
            if names:
                return names
        return sorted(self.review.reviewed_tools())

    # ------------------------------------------------------------ 设置段
    def _terminal_section(self) -> dict[str, Any]:
        return {
            "maxCommandSeconds": self.terminal.max_command_seconds(),
            "maxOutputBytes": self.terminal.max_output_bytes(),
            "defaultMaxCommandSeconds": PluginSettings.DEFAULT_MAX_COMMAND_SECONDS,
            "defaultMaxOutputBytes": PluginSettings.DEFAULT_MAX_OUTPUT_BYTES,
            "ownedTools": self._owned_tools(),
        }

    def _loop_section(self) -> dict[str, Any]:
        return {
            "maxIterations": self.loop.max_iterations(),
            "toolTimeoutSeconds": self.loop.tool_timeout_seconds(),
            "silentRounds": self.loop.silent_rounds(),
            "maxToolsPerRound": self.loop.max_tools_per_round(),
            "defaultMaxIterations": PluginSettings.DEFAULT_MAX_ITERATIONS,
            "defaultToolTimeoutSeconds": PluginSettings.DEFAULT_TOOL_TIMEOUT_SECONDS,
            "defaultSilentRounds": PluginSettings.DEFAULT_SILENT_ROUNDS,
            "defaultMaxToolsPerRound": PluginSettings.DEFAULT_MAX_TOOLS_PER_ROUND,
        }

    def _subagent_section(self) -> dict[str, Any]:
        config = self.subagent.config()
        return {
            "enabled": bool(config.enabled),
            "maxDepth": config.max_depth,
            "maxConcurrency": config.max_concurrency,
            "provider": config.provider,
            "model": config.model,
        }

    def _review_section(self) -> dict[str, Any]:
        return {
            "enabled": bool(self.review.is_active()),
            "provider": self.review.provider(),
            "model": self.review.model(),
            "tools": self._review_tools(),
            "defaultTools": sorted(ApprovalReviewPlugin.DEFAULT_REVIEW_TOOLS),
        }

    def _settings_payload(self) -> dict[str, Any]:
        return {
            "pluginsDir": str(self.paths.plugins_dir()),
            "settingsFile": str(self.settings.file()),
            "devMode": bool(self.dev.is_dev_mode()),
            "terminal": self._terminal_section(),
            "loop": self._loop_section(),
            "subagent": self._subagent_section(),
            "review": self._review_section(),
            "team": {"members": [m.to_map() for m in self.team.members()]},
            "automation": {"tasks": [t.to_map() for t in self.automation.tasks()]},
        }

    def _due_views(self) -> list[dict[str, Any]]:
        """到点视图（纯查询，不会执行任何任务）。"""
        out: list[dict[str, Any]] = []
        for due in self.automation.poll_due(now_utc()):
            out.append({
                "id": due.task.id,
                "name": due.task.name,
                "sessionId": due.session_id,
                "prompt": due.prompt,
                "reason": due.reason,
                "dueAt": _instant_text__api_plugins(due.due_at),
            })
        return out

    # ------------------------------------------------------------ 开关
    def _toggle(self, plugin_id: str, enabled: bool) -> dict[str, Any]:
        """单插件开关。

        关掉 ≠ 卸载：插件仍在注册表里（列表上还能看到、随时能再打开），
        只是它的工具不再下发给模型（由门禁 SPI 每轮实时过滤）。
        """
        plugin = self.registry.get_by_id(plugin_id)
        default_value = False if plugin is None else bool(_attr(plugin, "enabled_by_default", True))
        if plugin is None:
            # 坏来源也能被"打开"（用户可能刚把它放进来还没 reload），但先要求它至少出现过
            known = any(plugin_id == _java_str(f.get("pluginId") or "")
                        or f"jar:{_java_str(f.get('jar') or '')}" == plugin_id
                        for f in self.loader.get_failures())
            if not known:
                return {"ok": False, "id": plugin_id, "enabled": False,
                        "message": "插件不存在: " + plugin_id}
        actual = self.settings.set_enabled(plugin_id, bool(enabled), default_value)
        return {"ok": True, "id": plugin_id, "enabled": bool(actual),
                "message": "插件已开启" if enabled else "插件已关闭（它的工具不再下发给模型）"}

    def _toggle_kind(self, kind: str, enabled: bool) -> dict[str, Any]:
        """整组开关：把某一类插件一次全开 / 全关（用户是按"一类"来理解的）。"""
        target = str(kind or "").strip().upper()
        if target not in PluginKind.DISPLAY:
            return {"ok": False, "kind": kind, "message": "没有这一类插件: " + str(kind)}
        changed: list[str] = []
        for plugin in self.registry.get_by_kind(target):
            self.settings.set_enabled(plugin.id, bool(enabled),
                                      bool(_attr(plugin, "enabled_by_default", True)))
            changed.append(plugin.id)
        return {"ok": True, "kind": target, "enabled": bool(enabled),
                "count": len(changed), "ids": changed}

    # ------------------------------------------------------------ 注册
    def register__api_plugins(self, router: Any) -> None:
        api = self

        # 【注册顺序 = Spring 的匹配优先级】精确路径必须排在 `{pluginId}` 前面：
        #   路由是"先登记先匹配"，而 Spring 也是精确路径优先于路径变量。
        #   顺序写错的话 `/api/plugins/settings` 会被当成 pluginId="settings"。
        #
        # 【共用命名空间】`/api/plugins/*` 上的另一个 controller 是 PluginDevController
        #   （`api/plugin_dev.py`：`/dev`、`/dev-mode`、`/sdk`、`/scaffold`）。
        #   它们不在本模块的注册顺序里，所以本模块的 `{pluginId}` 通配**不能**吃 2 段路径；
        #   对端模块自己用 `_literal_routes_first` 把字面量路径挪到路由表最前面，
        #   用例 `.lbverify/cases/plugins.py` 里有一条回归专门盯这件事。
        @router.get("/api/plugins")
        def get_all_plugins(req: Request):
            # 这个接口**不**返回 ApiResponse：Java 侧返回的是 PluginListView record（自带
            # success/message/data/error 字段），所以 `error` 即使为 null 也要原样输出。
            return Response.json({
                "success": True,
                "message": "操作成功",
                "data": [api._legacy_info(p) for p in api.registry.get_all_plugins()],
                "error": None,
                "ok": True,
                "devMode": bool(api.dev.is_dev_mode()),
                "pluginsDir": str(api.paths.plugins_dir()),
                "kinds": api._kind_views(),
                "plugins": api._plugin_views(),
                "scanDirs": [str(d) for d in api.paths.scan_dirs()],
            })

        @router.post("/api/plugins/scan")
        def scan_plugins(req: Request):
            report = api.loader.scan_and_load()
            message = f"扫描完成，加载 {report.loaded_count} 个插件"
            if report.error_count():
                message += f"，{report.error_count()} 个问题"
            return ApiResponse.ok({"loadedCount": report.loaded_count,
                                   "errors": list(report.errors)}, message)

        @router.post("/api/plugins/reload")
        def reload_plugins(req: Request):
            report = api.loader.reload()
            return Response.json({
                "ok": True,
                "count": report.loaded_count,
                "total": api.registry.size(),
                "errors": list(report.errors),
                "plugins": api._plugin_views(),
                "message": f"重载完成，加载 {report.loaded_count} 个插件",
            })

        # ---- 设置 ----
        @router.get("/api/plugins/settings")
        def get_settings(req: Request):
            return ApiResponse.ok(api._settings_payload())

        @router.post("/api/plugins/settings/terminal")
        def update_terminal(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            patch: dict[str, Any] = {}
            if body.get("maxCommandSeconds") is not None:
                patch["maxCommandSeconds"] = _int_of(body.get("maxCommandSeconds"))
            if body.get("maxOutputBytes") is not None:
                patch["maxOutputBytes"] = _int_of(body.get("maxOutputBytes"))
            api.settings.update_section("terminal", patch)
            return ApiResponse.ok(api._terminal_section(), "终端限制已更新")

        @router.post("/api/plugins/settings/loop")
        def update_loop(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            patch: dict[str, Any] = {}
            for key in ("maxIterations", "toolTimeoutSeconds", "silentRounds", "maxToolsPerRound"):
                if body.get(key) is not None:
                    patch[key] = _int_of(body.get(key))
            api.settings.update_section("loop", patch)
            return ApiResponse.ok(api._loop_section(), "大循环参数已更新")

        @router.post("/api/plugins/settings/subagent")
        def update_subagent(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            patch: dict[str, Any] = {}
            if body.get("maxDepth") is not None:
                patch["maxDepth"] = _int_of(body.get("maxDepth"))
            if body.get("maxConcurrency") is not None:
                patch["maxConcurrency"] = _int_of(body.get("maxConcurrency"))
            if body.get("provider") is not None:
                patch["provider"] = _java_str(body.get("provider"))
            if body.get("model") is not None:
                patch["model"] = _java_str(body.get("model"))
            api.settings.update_section("subagent", patch)
            return ApiResponse.ok(api._subagent_section(), "子智能体设置已更新")

        @router.post("/api/plugins/settings/review")
        def update_review(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            patch: dict[str, Any] = {}
            if body.get("provider") is not None:
                patch["provider"] = _java_str(body.get("provider"))
            if body.get("model") is not None:
                patch["model"] = _java_str(body.get("model"))
            tools = body.get("tools")
            if isinstance(tools, list):        # Java: `instanceof List<?> tools`
                names: list[str] = []
                for item in tools:
                    if item is not None and _java_str(item).strip():
                        names.append(_java_str(item).strip())
                patch["tools"] = names
            api.settings.update_section("review", patch)
            return ApiResponse.ok(api._review_section(), "审查设置已更新")

        # ---- 智能体团队 ----
        @router.get("/api/plugins/team")
        def list_team(req: Request):
            return ApiResponse.ok([m.to_map() for m in api.team.members()])

        @router.post("/api/plugins/team")
        def add_team_member(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            try:
                member = api.team.add(_str_of(body, "id"), _str_of(body, "name"),
                                      _str_of(body, "mode"), _str_of(body, "role"),
                                      _str_of(body, "model"), _bool_of(body.get("enabled")))
            except ValueError as e:
                return ApiResponse.error(str(e))
            return ApiResponse.ok(member.to_map(), "智能体已加入团队")

        @router.post("/api/plugins/team/{id}")
        def update_team_member(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            member_id = req.params["id"]
            try:
                member = api.team.update(member_id, body)
            except ValueError as e:
                return ApiResponse.error(str(e))
            if member is None:
                return ApiResponse.error("智能体不存在: " + member_id)
            return ApiResponse.ok(member.to_map(), "已更新")

        @router.delete("/api/plugins/team/{id}")
        def remove_team_member(req: Request):
            member_id = req.params["id"]
            if not api.team.remove(member_id):
                return ApiResponse.error("智能体不存在: " + member_id)
            return ApiResponse.ok({"id": member_id}, "已移除")

        # ---- 自动化任务 ----
        @router.get("/api/plugins/automation")
        def list_automation(req: Request):
            return ApiResponse.ok({"tasks": [t.to_map() for t in api.automation.tasks()],
                                   "due": api._due_views()})

        @router.get("/api/plugins/automation/due")
        def due_automation(req: Request):
            return ApiResponse.ok(api._due_views())

        @router.post("/api/plugins/automation")
        def add_automation(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            try:
                task = api.automation.add(_str_of(body, "id"), _str_of(body, "name"),
                                          _str_of(body, "sessionId"), _str_of(body, "prompt"),
                                          _bool_of(body.get("enabled")),
                                          _long_of(body.get("everySeconds")),
                                          _str_of(body, "at"))
            except ValueError as e:
                return ApiResponse.error(str(e))
            return ApiResponse.ok(task.to_map(), "任务已创建")

        @router.post("/api/plugins/automation/{id}")
        def update_automation(req: Request):
            body = api._required_body(req)
            if body is None:
                return deps.spring_error(400, req.path)
            task_id = req.params["id"]
            try:
                task = api.automation.update(task_id, body)
            except ValueError as e:
                return ApiResponse.error(str(e))
            if task is None:
                return ApiResponse.error("任务不存在: " + task_id)
            return ApiResponse.ok(task.to_map(), "已更新")

        @router.delete("/api/plugins/automation/{id}")
        def remove_automation(req: Request):
            task_id = req.params["id"]
            if not api.automation.remove(task_id):
                return ApiResponse.error("任务不存在: " + task_id)
            return ApiResponse.ok({"id": task_id}, "已删除")

        # ---- 整组开关 ----
        @router.post("/api/plugins/kind/{kind}/enable")
        def enable_kind(req: Request):
            return Response.json(api._toggle_kind(req.params["kind"], True))

        @router.post("/api/plugins/kind/{kind}/disable")
        def disable_kind(req: Request):
            return Response.json(api._toggle_kind(req.params["kind"], False))

        # ---- 单插件（路径变量放最后：精确路径优先）----
        @router.get("/api/plugins/{pluginId}")
        def get_plugin(req: Request):
            plugin_id = req.params["pluginId"]
            plugin = api.registry.get_by_id(plugin_id)
            if plugin is None:
                return ApiResponse.error("插件不存在: " + plugin_id)
            return ApiResponse.ok(api._legacy_info(plugin))

        @router.delete("/api/plugins/{pluginId}")
        def unload_plugin(req: Request):
            plugin_id = req.params["pluginId"]
            if not api.loader.unload_plugin(plugin_id):
                return ApiResponse.error("插件不存在或卸载失败: " + plugin_id)
            return ApiResponse.ok(None, "插件已卸载")

        @router.post("/api/plugins/{pluginId}/enable")
        def enable_plugin(req: Request):
            return Response.json(api._toggle(req.params["pluginId"], True))

        @router.post("/api/plugins/{pluginId}/disable")
        def disable_plugin(req: Request):
            return Response.json(api._toggle(req.params["pluginId"], False))


def register__api_plugins(router: Any, ctx: deps.ApiContext) -> None:
    PluginsApi(ctx).register__api_plugins(router)


# ========================================================================
# 原模块 lionbox/api/plugin_dev.py
# ========================================================================
"""插件开发模式接口 —— `/api/plugins/dev-mode`、`/api/plugins/scaffold`、`/api/plugins/dev`、`/api/plugins/sdk`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\PluginDevController.java`（144 行 / 5 个接口）。

【为什么这几个响应不套 ApiResponse】Java 侧这四个方法返回的是**裸 `LinkedHashMap`**
（`{"ok":true,...}`），不是 `ApiResponse`。前端 `App.respOk()` 先看 `ok` 字段、
`App.scaffoldPlugin()` 直接读 `res.path`；包成 `{"success":true,"data":{...}}` 之后
"生成骨架"按钮就再也拿不到路径了。所以这里一律用 `Response.json(...)` 原样发出。
同一个原因，**裸 Map 里的 null 必须显式输出**：Java 的 `@JsonInclude(NON_NULL)` 只加在
`ApiResponse` 上，实测 `POST /api/plugins/sdk` 的响应体里确实写着 `"error":null`。

【为什么接口层还要再解析一遍 kind / enabled】`lionbox.plugindev` 是开关与脚手架的真实实现，
但它对 `kind` 走的是 `plugins.base.PluginKind.parse` 的**宽松兜底**语义（认不出就默认
ADVANCED_TOOL），而 Java 的 controller 在认不出时**必须报错**，并且认中文显示名（`基础工具`）
和去分隔符写法（`agentloop` / `base-tool`）。两边可接受集合不同，所以这里按 Java 的
`PluginKind.parse` 逐行复刻匹配规则（`_parse_kind`），只把**规范后的枚举名**交给 service。
`enabled` 同理：Java 用 `Boolean.parseBoolean`，只有字符串 `"true"`（忽略大小写）才算真，
`{"enabled": 1}` 是 **false** —— 用 Python 的 `bool()` 会得到相反的结果。

# 依赖：lionbox.plugindev（已就绪，无桩：PluginDevService 提供 开关 / 脚手架 / SDK）
#      lionbox.plugins.lifecycle（已就绪，无桩：PluginPaths / PluginSettings）
"""


import logging
from typing import Any

from lionbox.plugindev import IllegalStateError, PluginDevService
from lionbox.plugins.base import PluginKind
from lionbox.plugins.lifecycle import PluginLoader, PluginPaths, PluginSettings, default_paths, default_settings
from lionbox.api import deps

log__api_plugin_dev = logging.getLogger("lionbox.api.plugin_dev")

#: 9 个插件分类，顺序与 Java `PluginKind.values()` 完全一致（报错文案要按这个顺序列出来）
KINDS: tuple[str, ...] = tuple(PluginKind.DISPLAY)

#: `GET /api/plugins/dev-mode` 里的提示语，逐字照抄 Java
HINT = ("开启方式：启动参数 --lionbox.plugin.dev-mode=true，"
        "或 POST /api/plugins/dev-mode {\"enabled\": true}（会持久化）")

#: `POST /api/plugins/scaffold` 成功后的话，逐字照抄 Java（前端只读 `res.path`，不显示这一句）
SCAFFOLD_MESSAGE = ("插件工程已生成。编译：powershell -ExecutionPolicy Bypass -File build.ps1；"
                    "然后 POST /api/plugins/reload 让插件生效。")

#: 开发模式没开启时的错误文案。与 `plugindev/service.py` 里 `scaffold` 抛出的那句一字不差：
#: Java 的校验顺序是「开发模式 → 插件ID → 分类」，接口层必须先复刻这一步，
#: 才能在"模式没开、分类也写错"时回这一句（而不是"未知的插件分类"）。
DEV_MODE_REQUIRED = ("插件开发模式未开启：请用 --lionbox.plugin.dev-mode=true 启动，"
                     "或先调用 POST /api/plugins/dev-mode {\"enabled\": true}")


# --------------------------------------------------------------------------
# 小工具：Java 语义的取值（不能用 Python 的直觉替代）
# --------------------------------------------------------------------------


def _java_str__api_plugin_dev(value: Any) -> str:
    """Java `String.valueOf(Object)` 的等价物（布尔输出小写、数字原样）。"""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def _java_str_or_none(value: Any) -> str | None:
    """Java `body.get(k) == null ? null : String.valueOf(body.get(k))`。"""
    return None if value is None else _java_str__api_plugin_dev(value)


def _java_bool(value: Any) -> bool:
    """Java `raw instanceof Boolean b ? b : Boolean.parseBoolean(String.valueOf(raw))`。

    Java 的 `parseBoolean` 只认字符串 "true"（忽略大小写）——**不 trim**、不认数字：
    `{"enabled": 1}` / `{"enabled": "yes"}` / `{"enabled": " true "}` 全是 false。
    """
    if isinstance(value, bool):
        return value
    return _java_str__api_plugin_dev(value).lower() == "true"


def _parse_kind(raw: Any) -> str | None:
    """Java `PluginKind.parse(String)` 的等价物；认不出来返回 None。

    三条匹配规则（与 Java 逐条对应）：
      1. 枚举名忽略大小写 —— `base_tool` / `BASE_TOOL`；
      2. 中文显示名逐字相等 —— `基础工具`；
      3. 去掉 `_` 与 `-` 后忽略大小写 —— `agentloop` / `AGENT-LOOP`
         （只去这两个符号，空格不在其列，所以 `Agent Loop` 不算）。

    【为什么不直接用 `plugins.base.PluginKind.parse`】那个函数的契约是"给个默认值"
    （认不出 → ADVANCED_TOOL），而这里的契约是"认不出 → 报错"，语义不同；
    且 `plugins/base.py` 是禁改文件，所以在本模块内复刻。
    """
    if raw is None or not _java_str__api_plugin_dev(raw).strip():
        return None
    want = _java_str__api_plugin_dev(raw).strip()
    folded = want.replace("_", "").replace("-", "").lower()
    for name in KINDS:
        if name.lower() == want.lower():
            return name
        if PluginKind.DISPLAY[name][0] == want:
            return name
        if name.replace("_", "").lower() == folded:
            return name
    return None


def _json_object(req: Request) -> dict[str, Any] | None:
    """取请求体 JSON 对象；**不是对象**（缺体 / 坏 JSON / 数组 / 标量）返回 None。

    Java 的 `@RequestBody Map<String,Object> body` 是必填的：缺请求体、JSON 坏了、
    顶层不是对象，Spring 都在进方法体之前回 400。所以要区分"空对象 `{}`"
    （合法，字段全当 null）与"没有请求体"（400），不能像别处那样一律兜成 `{}`。
    """
    payload = req.json
    return payload if isinstance(payload, dict) else None


# --------------------------------------------------------------------------
# 共享服务（与 PluginController 用同一份，别各算一份插件目录）
# --------------------------------------------------------------------------


def _plugin_paths(ctx: deps.ApiContext) -> PluginPaths:
    """插件目录定位。优先复用别的模块 `ctx.install("plugin_paths", ...)` 装好的实例。"""
    if ctx.has("plugin_paths"):
        return ctx.service("plugin_paths", default_paths)
    if ctx.has("plugin_settings"):
        shared = ctx.service("plugin_settings", default_settings)
        paths = getattr(shared, "paths", None)
        if isinstance(paths, PluginPaths):
            return paths          # 设置存在哪，开发工程就写到哪，不能两处各算
    return ctx.service("plugin_paths", default_paths)


def _plugin_settings(ctx: deps.ApiContext) -> PluginSettings:
    """插件设置（`settings.json`）。devMode 这个开关就存在它里面。"""
    if ctx.has("plugin_settings"):
        return ctx.service("plugin_settings", default_settings)
    return ctx.service("plugin_settings", lambda: PluginSettings(_plugin_paths(ctx)))


def _is_built(plugins_dir: Any, project_id: str) -> bool:
    """开发工程"装到插件目录了没有"（对应 Java 的 `Files.isRegularFile(pluginsDir/<id>.jar)`）。

    Java 判的是 jar，因为插件要 javac 编译；Python 没有编译步骤，加载器认的是
    `<id>.py` 单文件或含 `lionbox-plugin.json` 清单的 `<id>/` 目录
    （`plugins/lifecycle.py` 的 `PluginLoader.scan_and_load` 就是这么扫的）。
    字段名 `built` 与含义（"插件目录里有没有它的成品"）保持不变，
    顺带也认 Java 版留下的 `.jar`，用户从 Java 版迁过来时不会显示成"没构建"。
    """
    if (plugins_dir / f"{project_id}.py").is_file():
        return True
    if (plugins_dir / project_id / PluginLoader.MANIFEST_JSON).is_file():
        return True
    return (plugins_dir / f"{project_id}.jar").is_file()


def _project_sort_key(path: Any) -> tuple[str, str]:
    """开发工程排序键。Java 的 `Path.compareTo` 在 Windows 上忽略大小写，这里对齐它，
    再用原名兜底保证顺序稳定（目录枚举顺序本身是不确定的）。"""
    return (path.name.lower(), path.name)


def _literal_routes_first(router: Any, handlers: list[Any]) -> None:
    """把本控制器登记的**字面量**路由排到 `/{pluginId}` 这类占位路由前面。

    【为什么必须做】Spring 的路径匹配是"字面量优先"：`GET /api/plugins/dev-mode`
    永远命中 PluginDevController，不会被 PluginController 的 `@GetMapping("/{pluginId}")`
    抢走（Java 注释里专门写了这件事）。Python 侧的 Router 是**先登记先匹配**
    （`http/server.py` 的 `find` 顺序遍历），而装配顺序里 `plugins` 在 `plugin_dev` 之前 ——
    不调整的话 `GET /api/plugins/dev-mode` 会被当成"插件 id 叫 dev-mode"，
    回一套完全不同的结构，前端直接崩。

    只移动**自己刚登记的那几条**（按处理函数对象同一性判定），别人的路由顺序不动；
    拿不到路由表内部结构就安静跳过（不影响任何功能，只是退回先登记先匹配）。
    """
    routes = getattr(router, "_routes", None)
    if not isinstance(routes, list):
        return
    mine = [r for r in routes if any(r[2] is h for h in handlers)]
    if not mine or routes[:len(mine)] == mine:
        return
    routes[:] = mine + [r for r in routes if not any(r[2] is h for h in handlers)]


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class PluginDevApi:
    """PluginDevController 的 5 个端点。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ---- 依赖（懒取：装配方随时可以 ctx.install 覆盖真实实例）----
    def paths(self) -> PluginPaths:
        return _plugin_paths(self.ctx)

    def dev(self) -> PluginDevService:
        """插件开发服务（开关 / 脚手架 / SDK 的真实实现）。"""
        return self.ctx.service("plugin_dev", lambda: PluginDevService(
            paths=_plugin_paths(self.ctx), settings=_plugin_settings(self.ctx)))

    # ------------------------------------------------------------ 注册
    def register__api_plugin_dev(self, router) -> None:
        api = self

        @router.get("/api/plugins/dev-mode")
        def get_dev_mode(req: Request):
            """查开发模式状态（Java `devMode()`）。"""
            paths = api.paths()
            return Response.json({
                "ok": True,
                "devMode": api.dev().is_dev_mode(),
                "pluginsDir": str(paths.plugins_dir()),
                "devDir": str(paths.dev_dir()),
                "hint": HINT,
            })

        @router.post("/api/plugins/dev-mode")
        def set_dev_mode(req: Request):
            """运行时开关（持久化，重启后仍按这次的选择）。"""
            body = _json_object(req)
            if body is None:
                return deps.spring_error(400, req.path)
            actual = api.dev().set_dev_mode(_java_bool(body.get("enabled")))
            return Response.json({
                "ok": True,
                "devMode": actual,
                "message": "插件开发模式已开启" if actual else "插件开发模式已关闭",
            })

        @router.post("/api/plugins/scaffold")
        def scaffold(req: Request):
            """生成一个最小插件工程。

            校验顺序照 Java：开发模式 → 插件ID → 分类（顺序变了错误文案就会变），
            参数不合法回 `{"ok":false,"error":...}`（HTTP 仍是 200，前端按 ok 判断）。
            """
            body = _json_object(req)
            if body is None:
                return deps.spring_error(400, req.path)
            ident = _java_str_or_none(body.get("id"))
            name = _java_str_or_none(body.get("name"))
            kind_raw = _java_str_or_none(body.get("kind"))
            dev = api.dev()
            try:
                if not dev.is_dev_mode():
                    raise IllegalStateError(DEV_MODE_REQUIRED)
                safe = dev.safe_id(ident)
                kind = _parse_kind(kind_raw)
                if kind is None:
                    raise ValueError("未知的插件分类: " + _java_str__api_plugin_dev(kind_raw)
                                     + "（可选：" + " / ".join(KINDS) + "）")
                result = dev.scaffold(safe, name, kind)
            except (ValueError, IllegalStateError) as e:
                return Response.json({"ok": False, "error": str(e)})
            except Exception as e:                       # 落盘失败之类：照 Java 记日志并回一句
                log__api_plugin_dev.error("生成插件工程失败", exc_info=True)
                return Response.json({"ok": False,
                                      "error": f"生成失败: {type(e).__name__}: {e}"})
            return Response.json({
                "ok": True,
                "path": str(result.path),
                "files": list(result.files),
                "sdkJar": str(result.sdk) if result.sdk is not None else None,
                "message": SCAFFOLD_MESSAGE,
            })

        @router.get("/api/plugins/dev")
        def dev_projects(req: Request):
            """已经生成了哪些开发工程。列目录失败只记日志、照 Java 返回已拿到的部分。"""
            paths = api.paths()
            dev_dir = paths.dev_dir()
            projects: list[dict[str, Any]] = []
            if dev_dir.is_dir():
                try:
                    children = sorted(dev_dir.iterdir(), key=_project_sort_key)
                    dirs = [p for p in children if p.is_dir()]
                except OSError as e:                     # Java 也是 log.warn 后继续
                    log__api_plugin_dev.warning("列开发工程失败: %s", e)
                    dirs = []
                plugins_dir = paths.plugins_dir()
                for d in dirs:
                    projects.append({"id": d.name, "path": str(d),
                                     "built": _is_built(plugins_dir, d.name)})
            return Response.json({
                "ok": True,
                "devMode": api.dev().is_dev_mode(),
                "devDir": str(dev_dir),
                "projects": projects,
            })

        @router.post("/api/plugins/sdk")
        def build_sdk(req: Request):
            """生成/复用插件 SDK（编译插件用的接口包）。**没有请求体参数。**"""
            sdk = api.dev().ensure_sdk()
            return Response.json({
                "ok": sdk is not None,
                "path": str(sdk) if sdk is not None else None,
                "error": None if sdk is not None else "SDK 生成失败（详情见日志）",
            })

        _literal_routes_first(router, [get_dev_mode, set_dev_mode, scaffold,
                                       dev_projects, build_sdk])


def register__api_plugin_dev(router, ctx) -> None:
    PluginDevApi(ctx).register__api_plugin_dev(router)


# ========================================================================
# 原模块 lionbox/api/skills.py
# ========================================================================
"""技能接口 —— `/api/skills/*`（6 个）。

对应 Java `src\\main\\java\\com\\lioncode\\core\\plugin\\skill\\SkillController.java`
（在 `core/plugin/skill/` 下，**不在** `web/controller/`，所以逐接口对账时最容易被漏掉）。

| 方法 | 路径 | Java 行为 |
| --- | --- | --- |
| GET  | `/api/skills` | `{skillsDir, userSkillsDir, skills[]}` |
| POST | `/api/skills/reload` | message `已重新扫描技能目录，共 N 个技能[（M 个有问题）]` |
| POST | `/api/skills/{id}/enable` | 不存在 → `技能不存在: <id>`；成功 message `技能已启用: <id>` |
| POST | `/api/skills/{id}/disable` | 同上，`技能已禁用` |
| GET  | `/api/skills/active?sessionId=` | **可选**参数：缺失或全空白 → `缺少 sessionId`（200，不是 400）|
| POST | `/api/skills/active` | 体 `{sessionId, skills[]}`；会话不存在 → `会话不存在: <id>` |

业务逻辑本身在 `lionbox/skills/controller.py`（`SkillController`，逐字段对照 Java 移植的），
这里只做"路由 + 依赖装配 + 请求体解析"，不重复实现一遍响应构造。

【包封说明】Java 这个 controller 用的是 `ApiEnvelope`（数据同时挂顶层）；Python 侧按
`PORTING.md` 统一用 `ApiResponse`（数据在 `data`）。前端 `web/index.html` 两种都认
（`res.data || res`），所以不影响使用。
"""


import logging
from typing import Any

from lionbox.api import deps

log__api_skills = logging.getLogger("lionbox.api.skills")


class SkillsApi:
    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ---- 包封：与 Java 的 ApiEnvelope 逐字段一致 ----
    @staticmethod
    def _envelope(resp: Any) -> Any:
        """把控制器的 `ApiResponse` 换成 Java `ApiEnvelope` 那个形状（逐字段照抄）。

        【为什么这个 controller 特殊】Java 的 `SkillController` 用的是 `ApiEnvelope`
        （`core/context/ApiEnvelope.java`）。它的注释写清了原因：技能 / @ 引用这两组接口的
        设计稿写的是 `{ok, skills:[...]}`，而项目里老接口统一是 `{success, message, data}`
        —— **两种写法都有人按着写代码**，所以它两边都给：

            {ok:true, success:true, message:"操作成功", <业务字段…>, data:{ok:true, <业务字段…>}}

        实测 `_check_skills_at.py` 读的是 `res.get('skills')` 与 `res.get('ok')`（顶层），
        在只有 `data` 的形状下永远拿到 None，12 条断言全红，看起来像"技能系统坏了"。
        前端 `web/index.html` 两种都认（`res.data || res`），双写对谁都是安全的。
        """
        body = getattr(resp, "body", None)
        if not isinstance(body, dict):
            return resp

        if body.get("success"):
            data = body.get("data")
            data = data if isinstance(data, dict) else {}
            out: dict[str, Any] = {"ok": True, "success": True,
                                   "message": body.get("message") or "操作成功"}
            out.update(data)                       # 业务字段挂顶层
            inner: dict[str, Any] = {"ok": True}
            inner.update(data)
            out["data"] = inner
            return ApiResponse(out)

        out = {"ok": False, "success": False}
        if body.get("message") is not None:
            out["message"] = body["message"]
        if body.get("error") is not None:
            out["error"] = body["error"]
        return ApiResponse(out)
    # ---- 依赖 ----
    def _controller(self) -> Any:
        """技能控制器。仓库用 `skills.default_repository()` 的进程单例，
        这样 `skill_load` 工具、技能目录注入 SPI 与 `/api/skills` 看到的是同一份
        （用错实例会出现"接口里禁用了、提示词里还在"）。"""
        from lionbox.skills import SkillController, default_repository
        return SkillController(default_repository(),
                               session_manager=deps.sessions(self.ctx))

    def _session_exists(self, session_id: str) -> bool:
        return deps.sessions(self.ctx).get_session(session_id) is not None

    # ---- 注册 ----
    def register__api_skills(self, router) -> None:
        api = self

        @router.get("/api/skills")
        def list_skills(req: Request):
            return api._envelope(api._controller().list())

        @router.post("/api/skills/reload")
        def reload_skills(req: Request):
            return api._envelope(api._controller().reload())

        @router.post("/api/skills/{skillId}/enable")
        def enable_skill(req: Request):
            return api._envelope(api._controller().enable(req.params.get("skillId", "")))

        @router.post("/api/skills/{skillId}/disable")
        def disable_skill(req: Request):
            return api._envelope(api._controller().disable(req.params.get("skillId", "")))

        @router.get("/api/skills/active")
        def get_active(req: Request):
            # Java 这里是 @RequestParam(required = false)：缺失不是 400，而是"缺少 sessionId"
            return api._envelope(api._controller().get_active(req.q("sessionId")))

        @router.post("/api/skills/active")
        def set_active(req: Request):
            body = req.json_obj() if req.body else {}
            session_id = body.get("sessionId")
            skills = body.get("skills")
            if isinstance(skills, str) or not isinstance(skills, (list, type(None))):
                skills = None          # 形状不对就当没给，别把请求打 500
            return api._envelope(api._controller().set_active(
                None if session_id is None else str(session_id),
                [str(s) for s in skills] if isinstance(skills, list) else None))


def register__api_skills(router, ctx) -> None:
    SkillsApi(ctx).register__api_skills(router)

# ========================================================================
# 原模块 lionbox/api/runtime_extra.py
# ========================================================================
"""RuntimeController 的未覆盖部分 —— `/api/runtime/local/models/*` 与 `/api/runtime/prompt-preview`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\RuntimeController.java`（577 行 / 17 个接口）。
本模块**只登记 `api/runtime.py` 没实现的 3 条**（其余 14 条已经在那边注册，这里绝不重复登记）：

    POST /api/runtime/local/models/download   ← downloadOneModel（RuntimeController:329）
    POST /api/runtime/local/models/open-dir   ← openModelDir（RuntimeController:350）
    GET  /api/runtime/prompt-preview          ← promptPreview（RuntimeController:522）

【为什么这两条下载/目录接口要带一层薄适配】Java 里 `startDownload` / `modelDir` /
`isModelDownloaded` / `AVAILABLE_MODELS` 都在 `LocalModelRuntime` 上；Python 的
`lionbox.local.runtime.LocalModelRuntime`（P1 已就绪、本任务不许改）只提供
`download()` / `search_dirs()` / `model_file_name()` / `status()`，缺上面那几个。
所以本模块内放了 `LocalModelsSupport`：判据全部取自**真实状态**（`runtime.search_dirs()`
给出的目录、`runtime.app_root`、`app-config.json` 的 `llama.modelFile`、磁盘上文件的实际体积、
Java 的官方量化清单常量），**没有把探针里的字面量搬进实现**。
等 `local/runtime.py` 补齐同名方法，把 `LocalModelsSupport` 换成直接调用即可，接口代码不用动。

# 依赖：lionbox.agent.loop（由并行任务提供；**已就绪，非桩**）
    prompt-preview 要的就是 Java 那个 `AgentLoop` 单例（`previewSystemPrompt` /
    `previewUsesNativeTools` / `previewToolDefinitions` 三个方法在
    `lionbox.agent.loop.AgentLoop` 里逐一对齐）。装配方 `ctx.install("agent_loop", loop)`
    装进来的实例优先；没有就现场建一个真实的并装进去 —— 与 Java 的单例 bean 语义一致，
    绝不会"体检量的是另一份循环"。
# 依赖：lionbox.local.runtime 的 startDownload / modelDir（P1 模块尚未提供，见上）
"""


import json
import logging
import os
import subprocess
import sys
import threading
import urllib.parse
from pathlib import Path
from typing import Any

from lionbox.plugins.base import AgentMode
from lionbox.api import deps

log__api_runtime_extra = logging.getLogger("lionbox.api.runtime_extra")

# --------------------------------------------------------------------------
# Java 常量（逐字照抄：前端按这些名字/体积选量化版本，改一个字就是破坏兼容）
# --------------------------------------------------------------------------

#: `LocalModelRuntime.AVAILABLE_MODELS` —— ModelScope 仓库里实际存在的三份。
AVAILABLE_MODELS__api_runtime_extra: tuple[dict[str, Any], ...] = (
    {"file": "lion-merged-Q8_0.gguf", "label": "Q8_0（最高质量·默认）", "sizeGb": 8.87,
     "note": "原版精度，回答质量最好；下载 8.87 GB，解码约 11 token/s"},
    {"file": "lion-merged-Q4_K_M.gguf", "label": "Q4_K_M（平衡·推荐）", "sizeGb": 5.24,
     "note": "体积小 40%，解码约 1.7 倍快；质量略降"},
    {"file": "lion-merged-IQ4_XS.gguf", "label": "IQ4_XS（最小最快）", "sizeGb": 4.87,
     "note": "体积最小、速度最快；质量下降最明显，适合只看响应速度的场合"},
)

#: 下载源（Java `@Value("${lionbox.runtime.model-*}")` 的默认值；自测要指向假服务器时
#: 用 `--lionbox.runtime.model-base-url=...` 覆盖，等价 Java 的 `-D`）。
MODEL_BASE_URL = "https://modelscope.cn"
MODEL_REPO = "lionnezha/lion-models"
MODEL_REVISION = "master"

#: 小于这个体积不算权重（Java `min-model-bytes`）：防把错误页/半截文件当成模型。
MIN_MODEL_BYTES__api_runtime_extra = 1_000_000_000

#: 错误文案（与 Java 逐字一致，含中文全角括号）
ERR_NO_FILE = "缺少 file（要下载哪个模型文件）"
ERR_ONLY_LISTED = "只能下载清单里的量化版本："
ERR_BUSY_HEAD = "已经有一个下载在进行中（"
ERR_BUSY_TAIL = "），等它下完"
ERR_NO_FILE_NAME = "缺少文件名"

#: Java `String.trim()` 砍掉的是所有 <= U+0020 的字符，**不是** Unicode 空白；
#: `isBlank()` 用的是 `Character.isWhitespace`（**不含** U+00A0/U+2007/U+202F）。
#: `file` 是"缺参数"还是"参数非法"由它决定，所以按 Java 的语义来，不用 `str.strip()`。
_JAVA_TRIM = "".join(chr(c) for c in range(0x21))
_JAVA_WHITESPACE = frozenset(
    "\t\n\x0b\f\r\x1c\x1d\x1e\x1f " + "".join(chr(c) for c in (
        0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x205F, 0x3000)))

#: Spring 的 `StringToBooleanConverter`（`@RequestParam boolean full` 走的就是它）
_BOOL_TRUE__api_runtime_extra = frozenset(("true", "on", "yes", "1"))
_BOOL_FALSE__api_runtime_extra = frozenset(("false", "off", "no", "0", ""))

_CREATE_NO_WINDOW__api_runtime_extra = 0x08000000 if os.name == "nt" else 0


def java_trim__api_runtime_extra(s: str) -> str:
    """Java `String.trim()`。"""
    return s.strip(_JAVA_TRIM)


def java_is_blank__api_runtime_extra(s: str) -> bool:
    """Java `String.isBlank()`：空串或全是 `Character.isWhitespace` 认的空白。"""
    return all(ch in _JAVA_WHITESPACE for ch in s)


def java_str(value: Any) -> str:
    """Java `RuntimeController.str(Object)`：字符串原样、null → 空串、其余 String.valueOf。

    【为什么不用 `deps.as_str`】`as_str(True)` 得到 `"True"`，而 Java 的
    `String.valueOf(true)` 是 `"true"` —— 它进的是"缺少 file"以外的那些错误文案，
    前端/插件能看见，别在这里露馅。
    """
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def is_safe_model_file_name(file: str) -> bool:
    """Java `LocalModelRuntime.isSafeModelFileName`：只放行"纯文件名"的 GGUF。

    【为什么必须有这道关】`llama.modelFile` 是设置页可写的配置项，会一路被当成路径片段
    （`downloadTarget()` 里 `dir.resolve(name)`）。填 `..\\..\\x.gguf` 就能把下载中的
    `.part` 写到程序目录之外。目录分隔符、上级引用、盘符、非 GGUF 后缀一律挡掉。
    """
    if not file or java_is_blank__api_runtime_extra(file) or len(file) > 128:
        return False
    if "/" in file or "\\" in file or ".." in file:
        return False
    if ":" in file or "\0" in file:
        return False
    if not file.lower().endswith(".gguf"):
        return False
    return file not in (".", "..")


def known_model_names() -> str:
    """Java `knownModelNames()`：`a.gguf、b.gguf、c.gguf`（中文顿号分隔）。"""
    return "、".join(str(m["file"]) for m in AVAILABLE_MODELS__api_runtime_extra)


def is_known_model(file: str) -> bool:
    return any(str(m["file"]) == file for m in AVAILABLE_MODELS__api_runtime_extra)


def opener_argv(path: str) -> list[str]:
    """按平台给出"打开目录"的命令行 —— Java `openModelDir` 里的三个分支：

        os.name 含 "win" → explorer.exe；含 "mac" → open；否则 xdg-open。
    """
    if os.name == "nt":
        return ["explorer.exe", path]
    if sys.platform == "darwin":
        return ["open", path]
    return ["xdg-open", path]


def _open_directory(path: str) -> None:
    """在系统文件管理器里打开目录（Java 里的 `new ProcessBuilder(...).start()`）。

    起完立刻返回、**不等它退出**：explorer.exe 的退出码是 1（"已复用一个现有窗口"），
    wait 它反而会把成功误判成失败。Windows 上加 CREATE_NO_WINDOW —— explorer.exe 自己是
    GUI 程序不受影响，但别让调用方闪一个控制台窗口。
    """
    subprocess.Popen(opener_argv(path), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                     stderr=subprocess.DEVNULL, creationflags=_CREATE_NO_WINDOW__api_runtime_extra)


def java_agent_mode(name: str) -> str | None:
    """Java `AgentMode.fromName`：空白 → STANDARD；老名字 PTC/CREATIVE 归一到 STANDARD；
    不认识的名字在 Java 侧抛 `IllegalArgumentException`（由接口转成"未知模式"文案），
    这里返回 None 让调用方照原话报错。

    【为什么不直接用 `AgentMode.normalize` / `AgentMode.from_name`】`plugins/base.py` 里那两个
    等价于 Java 的 `valueOf` —— **不做 PTC/CREATIVE → STANDARD 的归一**（Java 的 `normalize`
    会；`base.py` 的只是 `from_name` 的别名）。直接用它的话 `?mode=PTC` 会原样回 "PTC"
    并按 PTC 建提示词，而 Java 回的是 STANDARD。这里按 Java 的两步语义自己走一遍。
    """
    raw = java_trim__api_runtime_extra(name).upper()
    if not raw:
        return AgentMode.STANDARD
    if raw not in AgentMode.DISPLAY:
        return None
    if raw in (AgentMode.PTC, AgentMode.CREATIVE):
        return AgentMode.STANDARD
    return raw


# --------------------------------------------------------------------------
# LocalModelRuntime 的下载/目录薄适配
# --------------------------------------------------------------------------


class LocalModelsSupport:
    """`/api/runtime/local/models/*` 用到的"模型清单 + 目录 + 下载"判据。

    这一层只补 Python `local/runtime.py` 还没提供的几个同名方法（Java 侧它们都在
    `LocalModelRuntime` 上）。**只读真实状态、只做 Java 已有的判断**，不另立一套规则：

      · 搜哪些目录   ← `runtime.search_dirs()`（程序目录、程序目录\\models、~/.lioncode/models）
      · 生效的模型   ← `runtime.model_file_name()`（= `app-config.json` 的 `llama.modelFile`）
      · "已下载"     ← 真的去那些目录里找这个文件、量它的体积（与 Java 同一套判据）
      · 下载落点     ← 程序目录里第一个"存在且可写"的，否则 `~/.lioncode/models`
    """

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx
        self._lock = threading.RLock()
        self._downloading_now = False
        self._downloading_file = ""

    # ------------------------------------------------------------ 依赖
    @property
    def runtime(self) -> Any:
        """本地运行时（Java 侧的 `LocalModelRuntime` Spring bean，必然存在）。

        缺失说明装配没做完 —— 明确抛错（`http/server.py` 会包成 500），不假装成功。
        """
        rt = self.ctx.runtime
        if rt is None:
            raise RuntimeError("本地运行时未装配（lionbox.api.runtime.RuntimeApi 缺失）")
        return rt

    def _option(self, name: str, default: Any) -> Any:
        """`--lionbox.runtime.xxx=v`（等价 Java 的 `-D` / `@Value`）。"""
        return self.ctx.extra.get(name, default)

    @property
    def min_model_bytes(self) -> int:
        raw = str(self._option("lionbox.runtime.min-model-bytes", MIN_MODEL_BYTES__api_runtime_extra))
        try:
            return int(raw)
        except ValueError:
            log__api_runtime_extra.warning("min-model-bytes=%r 不是整数，按默认值 %d 处理", raw, MIN_MODEL_BYTES__api_runtime_extra)
            return MIN_MODEL_BYTES__api_runtime_extra

    def _flag(self, name: str, default: str) -> str:
        value = str(self._option(name, default) or default)
        return value.strip() or default

    # ------------------------------------------------------------ 目录
    def scan_dirs(self) -> list[Path]:
        """会被搜模型文件的目录（真实来源：`runtime.search_dirs()`）。"""
        return [Path(str(d)) for d in self.runtime.search_dirs()]

    def _search_bases(self) -> list[Path]:
        """Java `scanDirs() × {dir, dir\\models}`。"""
        out: list[Path] = []
        for d in self.scan_dirs():
            for base in (d, d / "models"):
                if base not in out:
                    out.append(base)
        return out

    def download_dirs(self) -> list[Path]:
        """下载落点候选（Java `downloadTarget` 用的是 `appDirs()`，不是 `scanDirs()`）。

        Java 的 appDirs 是"程序目录的几种可能"（`-Dlionbox.home`、`user.dir`、
        `user.dir\\dist`、`user.dir\\output\\LionCode\\app`、jar 所在目录）。Python 侧程序
        目录由 `--app-root` 明确给出，这里按同样的语义给出候选并保持顺序。
        """
        out: list[Path] = []
        home = str(self._option("lionbox.home", "") or "").strip()
        if home:
            out.append(Path(home))
        out.append(Path(str(self.runtime.app_root)))
        cwd = Path(os.getcwd())
        out.extend((cwd, cwd / "dist", cwd / "output" / "LionCode" / "app"))
        seen: set[str] = set()
        unique: list[Path] = []
        for d in out:
            key = str(d).lower()
            if key not in seen:
                seen.add(key)
                unique.append(d)
        return unique

    def effective_model_file(self) -> str:
        """当前生效的模型文件名（Java `effectiveModelFile()`）。"""
        return str(self.runtime.model_file_name())

    def find_model_file(self, file: str) -> Path | None:
        """按文件名在搜索目录里找现成的权重（Java `findModelFile`）。"""
        if not is_safe_model_file_name(file):
            return None
        for base in self._search_bases():
            p = base / file
            try:
                if p.is_file():
                    return p
            except OSError:
                continue
        return None

    def is_model_downloaded(self, file: str) -> bool:
        """本地是否已经有这份权重（Java `isModelDownloaded`：找到且 >= minModelBytes）。"""
        p = self.find_model_file(file)
        if p is None:
            return False
        try:
            return p.stat().st_size >= self.min_model_bytes
        except OSError:
            return False

    def download_target(self, file: str) -> Path | None:
        """下载落到哪个文件（Java `downloadTarget`：程序目录里第一个可写的，否则 ~/.lioncode/models）。"""
        name = java_trim__api_runtime_extra(file) or self.effective_model_file()
        if not is_safe_model_file_name(name):
            log__api_runtime_extra.warning("模型文件名非法（含路径分隔符/上级引用），拒绝作为下载目标: %s", name)
            return None
        for d in self.download_dirs():
            try:
                if d.is_dir() and os.access(d, os.W_OK):
                    return d / name
            except OSError:
                continue
        home = home_dir() / ".lioncode" / "models"
        try:
            home.mkdir(parents=True, exist_ok=True)
            return home / name
        except OSError as e:
            log__api_runtime_extra.error("模型目录建不出来，没有可写目录存放权重: %s", e)
            return None

    def model_dir(self) -> str:
        """模型默认放哪（Java `modelDir()`，界面把它显示给用户、open-dir 也用它）。"""
        target = self.download_target(self.effective_model_file())
        if target is not None and target.parent is not None:
            return str(target.parent)
        return str(home_dir() / ".lioncode" / "models")

    # ------------------------------------------------------------ 下载
    def download_url(self, file: str) -> str:
        """ModelScope 的 repo 接口（会 302 到 LFS CDN），与 Java `downloadModel` 拼法一致。"""
        base = self._flag("lionbox.runtime.model-base-url", MODEL_BASE_URL)
        repo = self._flag("lionbox.runtime.model-repo", MODEL_REPO)
        revision = self._flag("lionbox.runtime.model-revision", MODEL_REVISION)
        return (f"{base}/api/v1/models/{repo}/repo?Revision={revision}&FilePath="
                + urllib.parse.quote_plus(file, safe=""))

    def start_download(self, file: str) -> dict[str, Any]:
        """后台下载**指定的一份**权重，不切换当前模型（Java `LocalModelRuntime.startDownload`）。

        返回值就是界面据以提示的那四个键：`started` / `downloaded` / `busy` / `error`。
        同一时刻只允许一个下载（开机后台下载、界面按钮、第一条消息可能同时来抢）。
        """
        r: dict[str, Any] = {}
        if not file or java_is_blank__api_runtime_extra(file):
            r["started"] = False
            r["error"] = ERR_NO_FILE_NAME
            return r
        if not is_known_model(file):
            # 只从官方仓库下清单里那几份；用户自己塞的 GGUF 本来就在本地，不用下
            r["started"] = False
            r["error"] = ERR_ONLY_LISTED + known_model_names()
            return r
        if self.is_model_downloaded(file):
            r["started"] = False
            r["downloaded"] = True
            return r
        with self._lock:
            if self._downloading_now:
                r["started"] = False
                r["busy"] = True
                r["error"] = ERR_BUSY_HEAD + self._downloading_file + ERR_BUSY_TAIL
                return r
            self._downloading_now = True
            self._downloading_file = file
        threading.Thread(target=self._download_worker, args=(file,),
                         name="lionbox-model-dl", daemon=True).start()
        r["started"] = True
        return r

    def _download_worker(self, file: str) -> None:
        """后台线程：真的把权重拉下来（Java `downloadFileIfAllowed` 的等价物）。

        与 Java 一致的三道关：已存在就跳过、没有可写目录就记日志放弃、下完校验
        「GGUF 魔数 + 最小体积」。失败一律记进 `phase` / `lastError` ——
        界面轮询 `GET /api/runtime/local` 就能看见，不是无声失败。
        """
        runtime = self.runtime
        try:
            if self.is_model_downloaded(file):
                print(f"[模型] 本地已有 {file}，跳过下载", flush=True)
                return
            target = self.download_target(file)
            if target is None:
                # 【必须用 print】原来这里是 `log.error` —— 而本应用**从未配置 logging**，
                # 于是这条关键诊断（"没有可写目录"）谁都看不见，表现为"下载静默不发生"。
                print(f"[模型] 找不到可写目录来存放模型权重: {file}", flush=True)
                return
            print(f"[模型] 开始下载 {file} → {target}", flush=True)
            runtime.downloading_file = file
            runtime.download_bytes = 0
            runtime.download_total = -1
            runtime.phase = "downloading"
            try:
                if not runtime.download(self.download_url(file), target):
                    raise OSError(runtime.last_error or f"下载 {file} 失败")
                self._verify_gguf(target)
                runtime.phase = "idle"
                # 【下完就切过去】否则用户会一直看到"你选的 IQ4 还没下载"（刚下完却还说没下）
                hook = getattr(runtime, "on_model_downloaded", None)
                if callable(hook):
                    hook(file)
                print(f"[模型] 权重已就绪：{file}，可到「设置 → 模型版本」里点「使用」", flush=True)
            except Exception as e:      # 与 Java 一致：失败落进 phase/lastError 再给人看
                runtime.phase = "failed"
                runtime.last_error = f"下载模型失败：{e}"
                log__api_runtime_extra.error("下载模型失败: %s", e)
        finally:
            runtime.downloading_file = ""
            with self._lock:
                self._downloading_now = False
                self._downloading_file = ""

    def _verify_gguf(self, target: Path) -> None:
        """校验下载结果（Java `downloadModel` 末尾那几行）。

        【为什么校验不过要把 .gguf 改回 .part】Python 的 `runtime.download()` 是"下完直接
        原子改名"，而 Java 的校验发生在改名之前。校验不过时把文件还原成 `.part`，
        磁盘状态就与 Java 一致了：半截文件留着等下次续传，`is_model_downloaded()`
        也不会把它当成一份可用权重（界面不会误标"已下载"）。
        """
        size = target.stat().st_size
        with open(target, "rb") as f:
            magic = f.read(4)
        if len(magic) != 4:
            self._keep_as_part(target)
            raise OSError(f"下载到的文件太短（{size} 字节）")
        if magic != b"GGUF":
            # 仓库里没有该文件时 ModelScope 会回一个 HTML/JSON 错误页，别把它留下
            try:
                target.unlink()
            except OSError as e:
                log__api_runtime_extra.warning("丢弃坏文件失败: %s", e)
            head = magic.decode("ascii", "replace")
            raise OSError(f"下载到的不是 GGUF（文件头是 \"{head}\"，可能是仓库里没有该文件），已丢弃")
        if size < self.min_model_bytes:
            self._keep_as_part(target)
            raise OSError(f"文件只有 {size} 字节，远小于预期；保留 .part 以便续传")

    @staticmethod
    def _keep_as_part(target: Path) -> None:
        """把没通过校验的半截文件还原成 `.part`（Java 那边它压根就没改过名）。"""
        part = target.with_name(target.name + ".part")
        try:
            os.replace(target, part)
        except OSError as e:
            log__api_runtime_extra.warning("保留 .part 失败: %s", e)


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class RuntimeExtraApi:
    """RuntimeController 剩下 3 条接口（其余 14 条在 `api/runtime.py`）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx
        self.models = LocalModelsSupport(ctx)

    # ------------------------------------------------------------ 依赖
    def agent_loop(self) -> Any:
        """Agent 主循环（Java 侧：`@Autowired(required=false) AgentLoop agentLoop`）。

        取用顺序与 Java 的 bean 查找一致：装配方 `ctx.install("agent_loop", loop)` 装进来的
        真实 AgentLoop 优先；没有、或者被装成了不含预览能力的窄桩，就现场建一个真实的
        `lionbox.agent.loop.AgentLoop` 并装进同一个服务名 —— Java 里全应用共用这一个单例，
        提示词体检量的必须是它，不能是另一份临时循环。
        """
        loop = self.ctx.service("agent_loop", lambda: None) if self.ctx.has("agent_loop") else None
        if callable(getattr(loop, "preview_system_prompt", None)):
            return loop
        try:
            from lionbox.agent.loop import AgentLoop
        except ImportError:
            # Java 侧是 `@Autowired(required=false)`：**没有这个 bean** 时控制器收到 null，
            # 接口照 Java 的原话回"AgentLoop 不可用（该接口只在完整应用里生效）"。
            # 只吞 ImportError（= bean 不存在）；构造过程里其它异常照旧抛出去让 500 兜底。
            return None
        return self.ctx.install("agent_loop", AgentLoop(
            config_store=self.ctx.cfg,
            registry=deps.plugin_registry(),
            event_store=deps.events(self.ctx),
            history=self._history(),
            workspace=str(self.ctx.app_root)))

    def _history(self) -> Any:
        """会话历史：装配方装进来的真实 `ConversationHistory` 优先，否则用会话服务。"""
        if self.ctx.has("history"):
            return self.ctx.service("history", lambda: None)
        return deps.sessions(self.ctx)

    # ------------------------------------------------------------ 注册
    def register__api_runtime_extra(self, router) -> None:
        api = self

        @router.post("/api/runtime/local/models/download")
        def download_one_model(req: Request):
            """只下载指定的那一份量化（不切换当前模型）。

            用户可以先把几份都下好再挑一份用；下载走后台线程，状态看 `/api/runtime/local`
            的 `phase=downloading` + `downloadBytes` / `downloadTotal`。
            """
            if not req.body or not isinstance(req.json, dict):
                # Java 的方法签名是 `@RequestBody Map<String, Object> body`：**体是必填的**，
                # 空体 / 不是 JSON 对象时 Spring 在进方法体之前就回 400（默认错误体）。
                # 这一条不在方法体里，所以只能在这里复刻（SPEC 第 2 节）。
                return deps.spring_error(400, req.path)
            body = req.json_obj()
            file = java_str(body.get("file"))
            if not file or java_is_blank__api_runtime_extra(file):
                return ApiResponse.error(ERR_NO_FILE)
            r = api.models.start_download(file)
            if r.get("downloaded") is True:
                return ApiResponse.ok_msg(file + " 本地已经有了", api.models.runtime.status())
            if r.get("started") is not True:
                # Java 这里用的是 `String.valueOf(r.get("error"))`：键不存在时得到字符串
                # "null"（不是空串）；照抄，别自作主张改成 ""。
                error = r.get("error")
                return ApiResponse({"success": False, "data": api.models.runtime.status(),
                                    "error": "null" if error is None else str(error)})
            log__api_runtime_extra.info("用户请求下载模型权重: %s", file)
            return ApiResponse.ok_msg(
                "已开始下载 " + file + "（进度就在界面上；下完可点「立即使用」）",
                api.models.runtime.status())

        @router.post("/api/runtime/local/models/open-dir")
        def open_model_dir(req: Request):
            """在资源管理器里打开模型目录（用户想自己往里塞 GGUF 时用）。"""
            directory = api.models.model_dir()
            data: dict[str, Any] = {"dir": directory}
            opened = False
            try:
                d = Path(directory)
                if not d.is_dir():
                    d.mkdir(parents=True, exist_ok=True)
                _open_directory(str(d))
                opened = True
            except OSError as e:
                log__api_runtime_extra.warning("打开模型目录失败: %s", e)
                data["error"] = str(e)
            data["opened"] = opened
            return ApiResponse.ok_msg(
                ("已打开模型目录：" if opened else "没能自动打开，请手动打开：") + directory, data)

        @router.get("/api/runtime/prompt-preview")
        def prompt_preview(req: Request):
            """提示词体检：把这一轮真正会发给模型的系统提示词 + 工具定义原样吐出来。

            存在的意义是「慢的问题要能被量化」—— 提示词多大、多少字符、和上一版比少了多少，
            都得有数。用本地运行时的 `/tokenize` 把返回的文本数一遍，就是模型眼里真实的 token 数。

            例：`GET /api/runtime/prompt-preview?mode=standard&message=帮我改一下这个文件`
            """
            mode_name = java_str(req.q("mode", "standard"))
            message = java_str(req.q("message", ""))
            workspace = java_str(req.q("workspace", ""))
            flag = java_trim__api_runtime_extra(java_str(req.q("full", "false"))).lower()
            if flag in _BOOL_TRUE__api_runtime_extra:
                full = True
            elif flag in _BOOL_FALSE__api_runtime_extra:
                full = False
            else:
                # Spring 的 StringToBooleanConverter 认不出就 Invalid boolean value → 400
                return deps.spring_error(400, req.path)

            loop = api.agent_loop()
            if loop is None:
                return ApiResponse({"success": False,
                                    "message": "AgentLoop 不可用（该接口只在完整应用里生效）"})
            mode = java_agent_mode(mode_name)
            if mode is None:
                return ApiResponse({"success": False,
                                    "message": "未知模式: " + mode_name + "（只有 standard / minimal）"})

            # Java: `System.getProperty("user.dir")`（界面不传工作区时量的是进程当前目录）
            ws = os.getcwd() if java_is_blank__api_runtime_extra(workspace) else workspace
            prompt = str(loop.preview_system_prompt(mode, ws, message))

            out: dict[str, Any] = {
                "mode": mode,
                "workspace": ws,
                "nativeTools": bool(loop.preview_uses_native_tools()),
                # 【对齐 Java 的 length()】Java 数的是 UTF-16 码元，Python 数的是码点；
                # BMP 内的字符（含全部中文、换行）两者完全相同，只有 emoji 这类代理对会差 1。
                "chars": len(prompt),
                # Java: `prompt.split("\n", -1).length` —— 带尾部的空串（Python 同语义）
                "lines": len(prompt.split("\n")),
            }
            try:
                defs = list(loop.preview_tool_definitions(mode))
                # Java 用 ObjectMapper 序列化（紧凑、不转义非 ASCII），字数与它一致
                as_json = json.dumps(defs, ensure_ascii=False, separators=(",", ":"))
                out["toolDefinitionsCount"] = len(defs)
                out["toolDefinitionsChars"] = len(as_json)
                if full:
                    out["toolDefinitions"] = as_json
            except Exception as e:
                out["toolDefinitionsError"] = str(e)
            # 默认只回前 400 字，够看结构；要看全文加 full=true（调提示词时才需要）
            out["head"] = prompt[:400] if len(prompt) > 400 else prompt
            # 【null 要留着】Java 的 `@JsonInclude(NON_NULL)` 管的是 ApiResponse 自己的字段，
            # **不管** Map 里的值；所以 full=false 时 data 里照样有 `"systemPrompt":null`。
            out["systemPrompt"] = prompt if full else None
            return ApiResponse.ok(out)


def register__api_runtime_extra(router, ctx) -> None:
    RuntimeExtraApi(ctx).register__api_runtime_extra(router)


# ========================================================================
# 原模块 lionbox/api/chat.py
# ========================================================================
"""聊天接口 —— `/api/chat/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\ChatController.java`（361 行 / 7 个接口）：

    POST /api/chat                  发送消息（同步；经 SessionDispatcher 队列串行 + Steer 插队）
    POST /api/chat/stream           发送消息（流式 SSE；与会话队列互斥）
    POST /api/chat/adapter/switch   切换模型适配器
    GET  /api/chat/adapter/status   当前适配器状态
    POST /api/chat/adapter/config   保存适配器配置（baseUrl / apiKey / model / thinkingLevel）
    POST /api/chat/adapter/model    保存当前模型与思考等级
    GET  /api/chat/config           完整配置快照（**所有 apiKey 换成掩码**）

【逐字段对齐的要点（全部按 18099 活体实测，不按直觉）】

1. `@RequestBody` 缺失 / 不是 JSON 对象时，Spring 在**进方法体之前**就回 400 +
   `{"timestamp","status":400,"error":"Bad Request","path":…}`。实测 `POST /api/chat` 与
   `POST /api/chat/stream` 的空体都是 400，**不是** 200 的"缺少 sessionId"。

2. 错误文案逐字照抄（实测）：`缺少 sessionId（会话不存在）`（null **或全空白**）、
   `消息内容为空`、`会话不存在: <id>`（同步，带 id）/ `会话不存在`（流式，**不带 id**）、
   `会话正忙，请等待当前任务完成`、`无效的适配器类型: <请求原值>`、`适配器切换失败`、
   `处理消息失败: …`、`等待模型响应超过 N 秒（…）`。

3. 流式的 `Flux<AgentChunk>` 每帧是 `data:{…}\\n\\n`（`data:` 后**没有空格**），JSON 紧凑，
   `toolName` 为 null 时**照样输出** —— `AgentChunk` 是普通 record，只有 `ApiResponse` 才带
   `@JsonInclude(NON_NULL)`。实测首帧：
   `data:{"type":"ERROR","content":"缺少 sessionId（会话不存在）","toolName":null,"finished":true}`

4. `POST /api/chat/adapter/switch` 的 `{}`（adapterType 为 null）在 Java 里是
   `AdapterType.valueOf(null)` → **NPE 未被捕获** → Spring 回 **500** + 默认错误体
   （`.lbverify\\java\\POST_api_chat_adapter_switch.json` 记的就是这个）；
   空串 / 非法串 / 数字则走 `IllegalArgumentException` → 200 `无效的适配器类型: <原值>`
   （实测 `""`、`"NOPE"`、`123` 三种）。两条分支必须都照原样复刻。

5. Java 的 `ApiResponse.ok(String message, T data)` 参数顺序是 **(message, data)**，而 Python 的
   `ApiResponse.ok(data, message)` 相反：保存类接口回的是 `{"success":true,"message":"适配器配置已保存"}`
   （data 为 null 被 NON_NULL 整个省略），不能回成默认的"操作成功"。

# 依赖：lionbox.agent（AgentLoop 主循环，由并行任务提供）
#   装配方 `ctx.install("agent_loop", AgentLoop(...))` 之前，`deps.AgentLoopStub` 会抛
#   `DependencyMissing`：同步接口如实回 `处理消息失败: …`，流式接口发一帧 ERROR 后收流，
#   **绝不假装跑完**（那会让界面显示成"模型没说话"）。
# 依赖：lionbox.sessions（会话 + 标题生成，由并行任务提供）
#   会话：`deps.sessions()`（装配方 install 真实 SessionManager 后自动生效）。
#   标题：真实 `lionbox.sessions.title.SessionTitleService` 只在共享会话服务**不是**窄桩时
#   才构造（窄桩的会话是 dict、真实 Session 是数据类，硬塞进去会在请求路径上抛 AttributeError）。
# 依赖：lionbox.context（`@` 引用展开，由并行任务提供）
#   真实 `MentionResolver` 优先进口；模块缺失才退 `deps.MentionResolverStub`（不展开）。
# 依赖：lionbox.events（事件存储，由并行任务提供）
#   展开记录写 `TOOL_CALL_COMPLETE + toolName=context_expand`（界面上的工具行直接显示它）。
"""


import logging
from typing import Any, Iterator

from lionbox.api import deps

log__api_chat = logging.getLogger("lionbox.api.chat")

#: Java `getSavedModel()` 的"出厂默认：内置本地模型"（Java 里就是字面量，不看配置）
DEFAULT_MODEL = "lion-models1"

#: `AdapterType` 的两个名字（Java `AdapterType.valueOf` 是**大小写敏感**的精确匹配，
#: 所以不能用 `llm.types.AdapterType.parse`（它会 upper()，会把 "openai_compatible" 也认下来）。
#: 键 = Java `ModelAdapter.AdapterType` 的枚举名 = 配置里 `activeAdapter` 的取值。
_ADAPTER_TYPES: dict[str, Any] = {}

#: `adapterKey(AdapterType)`：Java switch 表达式，落到配置文件的键名
_ADAPTER_KEYS = {"OPENAI_COMPATIBLE": "openai", "ANTHROPIC": "anthropic"}

#: SSE 的内容类型：Java `produces = MediaType.TEXT_EVENT_STREAM_VALUE`，实测响应头就是
#: `text/event-stream`（**不带 charset**，浏览器对 SSE 本来就按 UTF-8 解）。
_SSE_CONTENT_TYPE = "text/event-stream"

#: Java `Character.isWhitespace` 认的空白字符。故意**不含** U+00A0 / U+2007 / U+202F：
#: Java 的 `"\u00a0".isBlank()` 是 **false**，而 Python 的 `str.strip()` 会把 NBSP 当空白 ——
#: 直接用 strip() 判断，`{"sessionId":"\u00a0"}` 在 Python 侧会变成"缺少 sessionId"，
#: Java 侧却会走到"会话不存在: \u00a0"。
_JAVA_SPACES__api_chat = frozenset(
    "\t\n\x0b\f\r\x1c\x1d\x1e\x1f " + "".join(chr(c) for c in (
        0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x205F, 0x3000)))


class _NotScalar(Exception):
    """值转不成 String/Boolean —— Jackson 反序列化阶段就会 400（请求根本进不了方法体）。"""


def _adapter_types() -> dict[str, Any]:
    """`AdapterType` 枚举名 → 枚举成员（延迟建表：接口层要快，import 期不算它）。"""
    if not _ADAPTER_TYPES:
        from lionbox.llm.types import AdapterType
        for member in AdapterType:
            _ADAPTER_TYPES[member.value] = member
    return _ADAPTER_TYPES


# --------------------------------------------------------------------------
# Jackson ↔ Java 基础类型的对齐
# --------------------------------------------------------------------------


def _java_blank__api_chat(text: str | None) -> bool:
    """Java `String.isBlank()`（null 也算空白；调用点原本都先判了 null）。"""
    return text is None or all(ch in _JAVA_SPACES__api_chat for ch in text)


def _jackson_string__api_chat(value: Any) -> str | None:
    """Jackson 往 `String` 组件里塞 JSON 值时的强转（与 `approvals.py` 同一套语义）。

    实测（18099）：`"adapterType": 123` → `无效的适配器类型: 123`，即走的是
    `String.valueOf` 而不是"类型不符"；对象/数组转不成 String，Jackson 抛
    MismatchedInputException → Spring 400。
    """
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, bool):                 # 必须在 int 之前：Python 里 bool 是 int 的子类
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    raise _NotScalar(type(value).__name__)


def _jackson_boolean(value: Any) -> bool | None:
    """Jackson 往 `Boolean` 组件里塞 JSON 值时的强转（`isSteer`）。

    接受 true/false、整型（非 0 为真）、`"true"`/`"false"`（去空白后精确匹配）与空串（→ null）；
    其余（别的字符串、对象、数组）Jackson 一律 400。
    """
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value != 0
    if isinstance(value, str):
        text = value.strip()
        if text == "true":
            return True
        if text == "false":
            return False
        if text == "":
            return None
        raise _NotScalar("Boolean")
    raise _NotScalar(type(value).__name__)


def _object_body(req: Request) -> dict[str, Any] | Response:
    """Spring `@RequestBody`（必填）的等价解析：**拿不到对象就是 400**。

    实测 18099：空体、非法 JSON、字面量 `null`、数组/字符串体一律
    `400 + {"timestamp","status":400,"error":"Bad Request","path":…}`（方法体都没进）。
    """
    value = req.json
    if not isinstance(value, dict):
        return deps.spring_error(400, req.path)
    return value


# --------------------------------------------------------------------------
# 共享服务（一律走 ctx.service：装配方 install 的真实实现优先）
# --------------------------------------------------------------------------


def _build_conversation_history() -> Any:
    """真实对话历史（`@history:` 引用要用；`auto_load=False` 与接口层一致：按需读盘）。"""
    from lionbox.sessions.history import ConversationHistory
    return ConversationHistory(auto_load=False)


def _build_skill_repository() -> Any:
    """真实技能仓库（`@skill:` 引用要用；进程内单例，与 `/api/context/mentions` 同一份）。"""
    from lionbox.skills.repository import default_repository
    return default_repository()


def _optional_service(ctx: deps.ApiContext, name: str, build: Any) -> Any:
    """取一个**可选**服务：模块缺失时记一条日志并返回 None。

    调用方（`MentionResolver`）对 None 有明确语义（该类引用标"不可用"，其余照常展开），
    所以这不是吞异常 —— 依赖真的不在时的降级路径，日志里有原因。
    """
    try:
        return ctx.service(name, build)
    except ImportError as e:            # 依赖：lionbox.sessions / lionbox.skills（由并行任务提供）
        log__api_chat.warning("服务 %s 不可用（%s），相关引用类型不展开", name, e)
        return None


def _default_mention_resolver(ctx: deps.ApiContext) -> Any:
    """`@` 引用展开器的默认实现（优先真实 `lionbox.context.MentionResolver`）。

    Java 侧 `MentionResolver` 是 Spring 单例、注入了技能仓库 / 会话管理 / 对话历史；
    这里按同样的三件套装配：会话管理器用共享服务（窄桩也收，`ContextRoots` 对 dict 会话
    会退到进程工作目录），技能仓库与对话历史缺模块时传 None（对应类别名不展开）。
    """
    try:
        from lionbox.context.mentions import MentionResolver
    except ImportError:                 # 依赖：lionbox.context（由并行任务提供）
        return deps.MentionResolverStub()
    return MentionResolver(
        skill_repository=_optional_service(ctx, "skill_repository", _build_skill_repository),
        session_manager=deps.sessions(ctx),
        conversation_history=_optional_service(ctx, "conversation_history",
                                               _build_conversation_history),
    )


def _title_chat(ctx: deps.ApiContext) -> Any:
    """喂给 `SessionTitleService` 的模型调用（Java 里就是它注入的 `AdapterManager` + 适配器）。

    标题服务传进来的是"角色 + 文本"的 dict，适配器要的是 `ChatMessage` 数据类 ——
    只做形状转换，不额外拼提示词（提示词在 title 模块里，与 Java 一致）。
    """
    def chat(messages: Any, model: str | None = None, extra: dict[str, Any] | None = None,
             max_tokens: int | None = None) -> Any:
        from lionbox.llm.types import ChatMessage
        adapter = ctx.adapters().get_active_adapter()
        if adapter is None:
            raise RuntimeError("没有可用的模型适配器")
        converted = [ChatMessage(str(m.get("role") or "user"), str(m.get("content") or ""))
                     for m in messages]
        return adapter.chat_with_options(converted, model, None, None, extra, max_tokens)

    return chat


class _TitleServiceStub:
    """窄桩：会话标题生成（不生成）。

    # 依赖：lionbox.sessions.title（由并行任务提供）

    Java 侧这个调用是**异步、失败有兜底**的旁路（标题只影响界面显示），所以桩的语义是
    "什么都没做"（返回 False），而不是"假装生成了"。真实 `SessionTitleService` 需要
    属性形态的会话对象（`session.name`），窄桩的会话是 dict —— 硬接上去会在**请求路径上**
    抛 AttributeError（比"没标题"糟得多），所以只有共享会话服务不是窄桩时才构造真实实现。
    """

    def generate_async(self, session_id: str | None, message: str | None) -> bool:
        return False


def _default_title_service(ctx: deps.ApiContext) -> Any:
    """标题生成器的默认实现：会话服务是真家伙时用真实 `SessionTitleService`，否则空操作。"""
    sessions = deps.sessions(ctx)
    if isinstance(sessions, deps.SessionStoreStub):
        return _TitleServiceStub()
    try:
        from lionbox.sessions.title import SessionTitleService
    except ImportError:                 # 依赖：lionbox.sessions（由并行任务提供）
        return _TitleServiceStub()
    return SessionTitleService(sessions, chat=_title_chat(ctx), config_store=ctx.cfg)


# --------------------------------------------------------------------------
# SSE（`Flux<AgentChunk>` 的等价物）
# --------------------------------------------------------------------------


def _chunk_json(chunk: Any) -> dict[str, Any]:
    """`AgentLoop.AgentChunk` 的 JSON 形状（四个字段，null 也输出，顺序即 record 声明序）。"""
    if not isinstance(chunk, dict):
        to_dict = getattr(chunk, "to_dict", None)
        chunk = to_dict() if callable(to_dict) else None
    if not isinstance(chunk, dict):
        raise TypeError(f"Agent 流式块不是 AgentChunk: {type(chunk).__name__}")
    return {
        "type": chunk.get("type"),
        "content": chunk.get("content"),
        "toolName": chunk.get("toolName"),
        "finished": chunk.get("finished"),
    }


def _frame(payload: dict[str, Any]) -> str:
    """一帧 SSE：`data:` + 紧凑 JSON + 空行（Spring 的 SSE 编码器就是这个写法）。"""
    return "data:" + deps.dump_json(payload) + "\n\n"


def _error_frame(text: str) -> str:
    """`AgentChunk.error(text)` 的一帧（`Flux.just(AgentChunk.error(...))` 的等价物）。"""
    return _frame({"type": "ERROR", "content": text, "toolName": None, "finished": True})


def _error_response(text: str) -> Response:
    return Response.stream([_error_frame(text)], content_type=_SSE_CONTENT_TYPE)


# --------------------------------------------------------------------------
# 接口
# --------------------------------------------------------------------------


class ChatApi:
    """`/api/chat/*` 的 7 个接口（对应 Java `ChatController`）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 依赖
    def adapters(self) -> Any:
        """适配器管理器（`ctx.adapters()` 是规范入口；装配方 `install("adapters", …)` 优先）。"""
        return self.ctx.service("adapters", self.ctx.adapters)

    def sessions(self) -> Any:
        """会话管理器（跨模块共享：装配方的真实 `SessionManager` 优先）。"""
        return deps.sessions(self.ctx)

    def events(self) -> Any:
        """事件存储（跨模块共享）。**每次请求现取**：`api/events.py` 会把装配期的占位窄桩
        升级成真实存储，缓存住旧引用会让展开事件写进没人读的那一份。"""
        return deps.events(self.ctx)

    def mention_resolver(self) -> Any:
        return self.ctx.service("mentions", lambda: _default_mention_resolver(self.ctx))

    def title_service(self) -> Any:
        return self.ctx.service("title_service", lambda: _default_title_service(self.ctx))

    def dispatcher(self) -> Any:
        """会话消息调度器（`SessionDispatcher`：同会话串行、Steer 插队、流式互斥）。"""
        return self.ctx.dispatcher()

    def http_wait_seconds(self) -> int:
        """同步接口最多等多久（Java `@Value("${lionbox.agent.http-wait-seconds:0}")`）。

        0 = 不设上限（默认，见 Java 注释：本地模型慢，工具多的任务不能砍）。
        取值来源与 Java 的 `-D` 同义：`--lionbox.agent.http-wait-seconds=1800`。
        """
        return max(0, deps.as_int(self.ctx.extra.get("lionbox.agent.http-wait-seconds"), 0))

    # ------------------------------------------------------------ 消息处理
    def expand_mentions(self, session_id: str, message: str | None) -> str | None:
        """展开消息里的 `@` 引用（Java `ChatController.expandMentions`）。

        · 没有引用记号 → 一个正则都不跑（每条消息都走这里，必须便宜）；
        · 展开失败 → **按原消息发下去**（引用读不到文件不该让整条消息发不出去）；
        · 展开成功 → 写一条 `TOOL_CALL_COMPLETE + toolName=context_expand` 事件，
          否则用户在事件流里看到的还是原样，会以为 `@file:` 没生效。
        """
        resolver = self.mention_resolver()
        if message is None or not _has_mention(resolver, message):
            return message
        try:
            expansion = resolver.expand(session_id, message)
            if not bool(getattr(expansion, "changed", False)):
                return message
            summary = _expansion_summary(expansion)
            if not _java_blank__api_chat(summary):
                self.events().record_event(session_id, "TOOL_CALL_COMPLETE", {
                    "toolName": "context_expand",
                    "result": summary,
                    "mentions": _mention_tokens(expansion),
                }, "已展开引用: " + summary)
            return _expansion_message(expansion, message)
        except Exception as e:          # Java: catch (Exception e) { log.warn; return message; }
            log__api_chat.warning("@ 引用展开失败，按原消息发送: %s: %s", type(e).__name__, e,
                        exc_info=True)
            return message

    def saved_model(self) -> str:
        """`getSavedModel(adapterManager.getActiveAdapter())`。

        读**当前激活适配器**对应的配置块（`openai` / `anthropic`）里的 `model`；
        没有或全空白时回落到出厂默认 `lion-models1`。
        """
        adapter = self.adapters().get_active_adapter()
        if adapter is not None:
            saved = _config_map(self.ctx.cfg, _adapter_key(adapter.adapter_type))
            model = saved.get("model")
            if isinstance(model, str) and not _java_blank__api_chat(model):
                return model
        return DEFAULT_MODEL

    def send(self, session_id: str, message: str, model: str | None,
             level_name: str | None, steer: bool) -> ApiResponse:
        """Java `sendMessage` 的后半段：算模型名 → 展开引用 → 生成标题 → 入队 → 等结果。

        各字段由调用方（路由处理函数）按 Jackson 的规则转好再传进来 —— 不用共享可变状态：
        接口层是并发的，把"当前请求体"挂在 self 上会让两条消息串味。
        """
        api = self
        level = _parse_level(level_name)
        if _java_blank__api_chat(model):
            model = api.saved_model()

        # @ 引用展开放在入队之前（Java 注释：展开要读盘，入队之后就是"轮到我才做"了）
        expanded = api.expand_mentions(session_id, message)
        # 标题拿**用户原话**（`@file:src/x.java` 当标题比几千字文件内容合适得多）
        api.title_service().generate_async(session_id, message)

        future = api.dispatcher().submit(session_id, expanded, model, level, steer)
        wait = api.http_wait_seconds()
        try:
            # Java: future.get() —— 任务失败时抛 ExecutionException，它的 message 是
            # `异常类名: 原因`；Python 的 Future.result() 直接抛原始异常，这里补上类名。
            response = future.result(timeout=wait) if wait > 0 else future.result()
        except TimeoutError:
            return ApiResponse.error(
                "等待模型响应超过 " + str(wait) + " 秒（可用 --lionbox.agent.http-wait-seconds 调整；"
                "任务可能仍在后台运行，可到会话里查看，或用界面上的停止按钮中止）")
        except Exception as e:
            return ApiResponse.error(f"处理消息失败: {type(e).__name__}: {e}")
        return ApiResponse.ok(response)

    # ------------------------------------------------------------ 注册
    def register__api_chat(self, router) -> None:
        api = self

        @router.post("/api/chat")
        def send_message(req: Request):
            body = _object_body(req)
            if isinstance(body, Response):
                return body                     # 400：与 Java 一样在方法体之前就返回
            try:
                session_id = _jackson_string__api_chat(body.get("sessionId"))
                message = _jackson_string__api_chat(body.get("message"))
                model = _jackson_string__api_chat(body.get("model"))
                level_name = _jackson_string__api_chat(body.get("thinkingLevel"))
                steer = _jackson_boolean(body.get("isSteer"))
            except _NotScalar:
                # Jackson 先把整个 ChatRequest 反序列化完才进方法体：类型对不上就是 400
                return deps.spring_error(400, req.path)
            if _java_blank__api_chat(session_id):
                return ApiResponse.error("缺少 sessionId（会话不存在）")
            if _java_blank__api_chat(message):
                return ApiResponse.error("消息内容为空")
            if api.sessions().get_session(session_id) is None:
                return ApiResponse.error("会话不存在: " + str(session_id))
            return api.send(str(session_id), str(message), model, level_name, steer is True)

        @router.post("/api/chat/stream")
        def send_message_stream(req: Request):
            body = _object_body(req)
            if isinstance(body, Response):
                return body
            try:
                session_id = _jackson_string__api_chat(body.get("sessionId"))
                message = _jackson_string__api_chat(body.get("message"))
                model = _jackson_string__api_chat(body.get("model"))
                level_name = _jackson_string__api_chat(body.get("thinkingLevel"))
            except _NotScalar:
                return deps.spring_error(400, req.path)
            if _java_blank__api_chat(session_id):
                return _error_response("缺少 sessionId（会话不存在）")
            if _java_blank__api_chat(message):
                return _error_response("消息内容为空")
            session_id = str(session_id)
            message = str(message)
            store = api.sessions()
            if store.get_session(session_id) is None:
                # 【注意】流式这条的文案**不带会话 id**（实测：`会话不存在`）
                return _error_response("会话不存在")

            dispatcher = api.dispatcher()
            # 会话忙（有同步任务在跑/排队）时拒绝流式：否则两边同时写历史会写乱
            if not dispatcher.try_acquire_stream(session_id):
                return _error_response("会话正忙，请等待当前任务完成")

            level = _parse_level(level_name)
            if _java_blank__api_chat(model):
                model = api.saved_model()
            # 首条消息触发标题生成（异步、失败有兜底）——同样用用户原话
            api.title_service().generate_async(session_id, message)
            # @ 引用展开：和同步接口同一套逻辑（两条路不能有两套行为）
            expanded = api.expand_mentions(session_id, message)

            return Response.stream(
                api._stream_frames(session_id, str(expanded), level, model),
                content_type=_SSE_CONTENT_TYPE)

        @router.post("/api/chat/adapter/switch")
        def switch_adapter(req: Request):
            body = _object_body(req)
            if isinstance(body, Response):
                return body
            try:
                raw = _jackson_string__api_chat(body.get("adapterType"))
                session_id = _jackson_string__api_chat(body.get("sessionId"))
            except _NotScalar:
                return deps.spring_error(400, req.path)
            if raw is None:
                # 【必须复刻 500】Java 直接 `AdapterType.valueOf(null)`：NPE 不在 catch
                # (IllegalArgumentException) 的范围内 → Spring 回 500 + 默认错误体。
                # 换成"无效的适配器类型: null"就是改了语义（前端按 HTTP 状态区分故障类型）。
                return deps.spring_error(500, req.path)
            adapter_type = _adapter_types().get(raw)      # valueOf：大小写敏感、精确匹配
            if adapter_type is None:
                return ApiResponse.error("无效的适配器类型: " + raw)
            manager = api.adapters()
            if not manager.switch_adapter(adapter_type, session_id):
                return ApiResponse.error("适配器切换失败")
            # 持久化激活适配器（Java: configStore.set("activeAdapter", type.name())）
            api.ctx.cfg.set("activeAdapter", adapter_type.value)
            return ApiResponse.ok("适配器已切换至: " + adapter_type.value)

        @router.get("/api/chat/adapter/status")
        def get_adapter_status(req: Request):
            active = api.adapters().get_active_adapter()
            if active is None:
                raise deps.DependencyMissing("模型适配器（lionbox.llm.manager.AdapterManager）")
            return ApiResponse.ok({
                # AdapterStatus 是普通 record：三个字段始终输出，没有 NON_NULL 省略
                "name": active.name,
                "type": active.adapter_type.value,
                "available": bool(active.is_available()),
            })

        @router.post("/api/chat/adapter/config")
        def update_adapter_config(req: Request):
            body = _object_body(req)
            if isinstance(body, Response):
                return body
            try:
                # Jackson 先整份反序列化：任何一个字段是对象/数组 → 400（一个字段都不写）
                base_url = _jackson_string__api_chat(body.get("baseUrl"))
                api_key = _jackson_string__api_chat(body.get("apiKey"))
                raw_type = _jackson_string__api_chat(body.get("adapterType"))
                model = _jackson_string__api_chat(body.get("model"))
                thinking = _jackson_string__api_chat(body.get("thinkingLevel"))
            except _NotScalar:
                return deps.spring_error(400, req.path)

            manager = api.adapters()
            # 目标适配器：请求指定，否则当前激活的（Java 里 active 永不为 null）
            target = manager.get_active_adapter()
            if target is None:
                raise deps.DependencyMissing("模型适配器（lionbox.llm.manager.AdapterManager）")
            target_type = target.adapter_type
            if not _java_blank__api_chat(raw_type):
                wanted = _adapter_types().get(raw_type)     # 认不出来 → 忽略，仍用当前激活的
                if wanted is not None:
                    target_type = wanted
                    target = manager.get_adapter(wanted) or target

            # 只放进"请求里给了值"的键（Java：null 不写，空串照写）
            cfg: dict[str, Any] = {}
            if base_url is not None:
                cfg["baseUrl"] = base_url
            if api_key is not None:
                cfg["apiKey"] = api_key
            target.update_config(cfg)

            key = _adapter_key(target_type)
            saved = dict(_config_map(api.ctx.cfg, key))
            saved.update(cfg)
            if not _java_blank__api_chat(model):
                saved["model"] = model
            if not _java_blank__api_chat(thinking):
                saved["thinkingLevel"] = thinking
            api.ctx.cfg.set(key, saved)

            # 配置保存即意图使用：跳过可用性检查直接设为激活（Java 同）
            manager.restore_active_adapter(target_type)
            api.ctx.cfg.set("activeAdapter", target_type.value)
            # Java: ApiResponse.ok("适配器配置已保存", null) —— (message, data) 顺序
            return ApiResponse.ok(None, "适配器配置已保存")

        @router.post("/api/chat/adapter/model")
        def save_model_selection(req: Request):
            body = _object_body(req)
            if isinstance(body, Response):
                return body
            try:
                model = _jackson_string__api_chat(body.get("model"))
                thinking = _jackson_string__api_chat(body.get("thinkingLevel"))
            except _NotScalar:
                return deps.spring_error(400, req.path)
            manager = api.adapters()
            active = manager.get_active_adapter()
            if active is None:
                raise deps.DependencyMissing("模型适配器（lionbox.llm.manager.AdapterManager）")
            key = _adapter_key(active.adapter_type)
            saved = dict(_config_map(api.ctx.cfg, key))
            # 【这里没有 isBlank 判断】Java 只判 null：`{"model":""}` 会把空串存进去
            if model is not None:
                saved["model"] = model
            if thinking is not None:
                saved["thinkingLevel"] = thinking
            api.ctx.cfg.set(key, saved)
            return ApiResponse.ok(None, "模型选择已保存")

        @router.get("/api/chat/config")
        def get_config(req: Request):
            # 【必须掩码】快照里有 openai / anthropic / customApi / providers.* 的 apiKey：
            # 原样回给客户端等于把用户的付费密钥交出去（Java 侧就是这么修的）。
            return ApiResponse.ok(deps.SecretMask.mask_deep(api.ctx.cfg.snapshot()))

    # ------------------------------------------------------------ 流式帧
    def _stream_frames(self, session_id: str, message: str, level: Any,
                       model: str | None) -> Iterator[str]:
        """把 `AgentLoop.process_message_stream` 的块转成 SSE 帧，并在结束时释放会话。

        等价 Java 的 `.doFinally(signal -> dispatcher.releaseStream(sessionId))`：
        释放必须放在 finally 里 —— 客户端中途断开时生成器被 close()，同样要解锁，
        否则那条会话会永远"正忙"。
        """
        dispatcher = self.dispatcher()
        try:
            loop = self.ctx.service("agent_loop", lambda: deps.AgentLoopStub())
            mode = self.sessions().get_effective_mode(session_id)
            for chunk in loop.process_message_stream(session_id, message, mode, level, model):
                yield _frame(_chunk_json(chunk))
        except Exception as e:
            # 依赖没接线（AgentLoopStub 抛 DependencyMissing）或主循环启动即失败：
            # 已经发出 SSE 头就不能再回 500 了，发一帧 ERROR 收流 —— 客户端能看懂原因，
            # 也不会把"没反应"误当成"模型没说话"。
            log__api_chat.error("流式处理失败（会话 %s）: %s: %s", session_id, type(e).__name__, e,
                      exc_info=True)
            yield _error_frame(f"处理消息失败: {type(e).__name__}: {e}")
        finally:
            dispatcher.release_stream(session_id)


# --------------------------------------------------------------------------
# 纯函数（与 Java 同名，方便逐条对拍）
# --------------------------------------------------------------------------


def _adapter_key(adapter_type: Any) -> str:
    """Java `adapterKey(AdapterType)`：OPENAI_COMPATIBLE → "openai"、ANTHROPIC → "anthropic"。"""
    name = str(getattr(adapter_type, "value", adapter_type))
    key = _ADAPTER_KEYS.get(name)
    if key is None:
        raise ValueError(f"未知的适配器类型: {name}")
    return key


def _config_map(cfg: Any, key: str) -> dict[str, Any]:
    """Java `configStore.getMap(key)`：非对象/缺失一律当空表（**返回副本**，改它不动配置）。"""
    value = cfg.get(key) if cfg is not None else None
    return dict(value) if isinstance(value, dict) else {}


def _parse_level(name: str | None) -> str:
    """Java `parseLevel`：`ThinkingLevel.valueOf(name.toUpperCase())`，认不出来回落 MEDIUM。

    返回 **Java 的枚举名**（`LOW` / `MEDIUM` / `HIGH` / `MAX`）—— 这正是 Java 侧
    `ThinkingLevel.name()` 在两条链路之间传递的形态：`SessionDispatcher` 拿它当队列字段，
    `AgentLoop` 的两个入口接受的也是"名字 / 代码"字符串（传枚举对象反而会被
    `ThinkingLevel.from_name` 当成不认识的名字，一路降级到 LOW）。
    """
    if name is None:
        return "MEDIUM"
    from lionbox.llm.types import ThinkingLevel
    return ThinkingLevel.parse(name, ThinkingLevel.MEDIUM).name


def _has_mention(resolver: Any, message: str) -> bool:
    """`MentionResolver.hasMention(message)`（真实模块里是模块级函数，窄桩里是静态方法）。"""
    fn = getattr(resolver, "has_mention", None)
    if callable(fn):
        return bool(fn(message))
    try:
        from lionbox.context.mentions import has_mention
    except ImportError:                 # 依赖：lionbox.context（由并行任务提供）
        return "@" in message
    return bool(has_mention(message))


def _expansion_message(expansion: Any, fallback: str) -> str:
    """`expansion.message()`：真实 `Expansion` 是字段（str），窄桩里是可调用的静态方法。"""
    value = getattr(expansion, "message", None)
    if callable(value):
        value = value()
    return value if isinstance(value, str) else fallback


def _expansion_summary(expansion: Any) -> str:
    """`expansion.summary()`（真实实现与窄桩都是方法）。"""
    fn = getattr(expansion, "summary", None)
    value = fn() if callable(fn) else ""
    return value if isinstance(value, str) else ""


def _mention_tokens(expansion: Any) -> list[str]:
    """Java: `expansion.notes().stream().map(Note::token).toList()`。"""
    notes = getattr(expansion, "notes", None) or []
    out: list[str] = []
    for note in notes:
        token = note.get("token") if isinstance(note, dict) else getattr(note, "token", None)
        out.append("" if token is None else str(token))
    return out


def register__api_chat(router, ctx) -> None:
    ChatApi(ctx).register__api_chat(router)


# ========================================================================
# 原模块 lionbox/api/agent_control.py
# ========================================================================
"""Agent 运行控制接口 —— `/api/chat/control/*`。

对应 Java `src\\main\\java\\com\\lioncode\\web\\controller\\AgentControlController.java`
（85 行 / 4 个接口）。前端在任务运行期间调用：

    POST /api/chat/control/pause    暂停（下一轮工具调用前生效）
    POST /api/chat/control/resume   继续
    POST /api/chat/control/stop     停止（下一轮工具调用前生效）
    GET  /api/chat/control/status   查询当前状态

# 依赖：lionbox.agent（AgentControlManager / UserQuestionService，由并行任务提供）
    Java 侧两个注入对象都是 Spring 单例：`AgentControlManager`（会话 → RUNNING/PAUSED/STOPPED）
    与 `UserQuestionService`（`stop` 时取消该会话上等待中的提问）。Python 侧的真实实现是
    `lionbox.agent.control.AgentControlManager`（已就绪）与提问服务，但**装配到 ApiContext
    是装配方的动作**（`app.py` / `api/__init__.py` 都不在本任务范围内），因此这里统一走
    `ctx.service("agent_control", ...)`，未装配时退回 `deps` 的窄桩（形状一致、进程内自洽）。
    装配方 `ctx.install("agent_control", 真实实例)` 之后本文件一行都不用改 ——
    前提是**同时把它交给 `queue.SessionDispatcher`**（同一个实例，见文件末尾注释）。

【状态来源是真状态，不是常量】三个 GET/POST 的成功响应本身不带状态值，
`GET /status` 回的是 `agent_control.get_state(sessionId).name()` 的**真实当前值**，
`stop` 的文案里那个数字来自 `questions.cancel_session(sessionId)` 的**真实返回条数**
（Java: `cancelled > 0 ? "已请求停止（同时取消了 N 个等待中的提问）" : "已请求停止"`）。

【逐字段对齐的六处细节（全部是 18099 实测出来的，不是照源码猜的）】

1. 成功的 `data` 是 **null**，`ApiResponse` 的 `@JsonInclude(NON_NULL)` 会把整个 `data`
   省略：`POST /pause {"sessionId":"probe-nope"}` → `{"success":true,"message":"已暂停"}`
   —— 没有 `data` 键。逐字照抄：`已暂停` / `已继续` / `已请求停止` / `已继续`。
2. `GET /status` 的 message 是 `"ok"`（**不是**默认的"操作成功"），data 是状态名字符串。
3. `@RequestBody` 缺失 / 非法 JSON / 字面量 `null` / 数组 / 数字 / 字符串体 → Spring 在进
   方法体之前就回 `400 + {"timestamp","status":400,"error":"Bad Request","path":…}`
   （实测六种原始体全是 400）→ `deps.spring_error(400, req.path)`。
4. `{"sessionId":"   "}`（全空白）走的是控制器里那句 `isBlank()` → `sessionId不能为空`；
   而 `{"sessionId":123}` 被 Jackson 绑成 `"123"`（非空）→ 成功。所以判定必须用 Java 的
   `String.isBlank()` 语义，**不能**直接用 `str.strip()`：实测 `"\u00a0"`（NBSP）、
   `"\u202f"`（NNBSP）、`"\u200b"`（ZWSP）在 Java 里**不是**空白（回"已暂停"），
   而 Python 的 `isspace()` 认 U+00A0；反过来 U+2007（FIGURE SPACE）在 Java 里**是**空白，
   它在 Python 里却不是 —— 两个方向都得按 `Character.isWhitespace` 校正。
5. `sessionId` 字段是**原样**送进 `agentControl` 的（Java 没 trim，见第 4 点的 `"   "`），
   所以 Python 侧也不许 trim；`sessionid`（小写 d）不是 record 组件，Jackson 忽略 → 仍是
   `sessionId不能为空`（实测）。
6. `GET /status` 缺 `sessionId` 查询参数是 **400**（Spring 必填参数校验，方法体都不进）；
   但 `?sessionId=`、`?sessionId=%20`、`?sessionId=%E3%80%80` 在 Java 里回的是 **200 +
   `RUNNING`** —— 因为 Spring 的 `StringTrimmerEditor(emptyAsNull=true)` 把"trim 后为空"的
   查询参数转成 **null**，`ConcurrentHashMap.getOrDefault(null, RUNNING)` 于是给默认值
   （实测 `?sessionId=%C2%A0` 是 PAUSED，NBSP 不被 trim）。所以 `None` 与空白要走同一分支。
"""


from typing import Any

from lionbox.api import deps

#: 错误文案（与 Java 逐字一致，无标点、无空格）
ERR_MISSING_SESSION = "sessionId不能为空"

#: 成功文案（Java `ApiResponse.ok(message, null)`，data 省略）
MSG_PAUSED = "已暂停"
MSG_RESUMED = "已继续"
MSG_STOPPED = "已请求停止"
MSG_STOPPED_CANCELLED = "已请求停止（同时取消了 {n} 个等待中的提问）"
#: `GET /status` 的 message（Java 写的是 "ok"）
MSG_STATUS = "ok"

#: Java `Character.isWhitespace` 认的空白（`String.isBlank()` = "每个字符都是它"）。
#: Python 的 `str.isspace()` 与它**几乎**一致，但 U+00A0 / U+202F 两个"Zs 类却非空白"的
#: 字符必须排除（见 `_JAVA_NON_BLANK`）；反过来 U+2007（FIGURE SPACE）Java **认**为空白
#: （`isWhitespace(0x2007)` 是 true，实测回"sessionId不能为空"），所以它在下面这个集合里。
_JAVA_SPACES__api_agent_control = frozenset(
    "\t\n\x0b\f\r\x1c\x1d\x1e\x1f " + "".join(chr(c) for c in (
        0x1680, *range(0x2000, 0x200B), 0x2028, 0x2029, 0x205F, 0x3000)))
#: 这两个在 Unicode 里是 Zs，Java 的 `Character.isWhitespace` 却回 false（实测：`"\u00a0"`
#: 与 `"\u202f"` 都能正常暂停，而 `str.isspace()` 认它们）
_JAVA_NON_BLANK = frozenset("\u00a0\u202f")


class _NotString__api_agent_control(Exception):
    """JSON 对象/数组绑不到 Java `String` —— Jackson 反序列化阶段就 400。"""


def _java_blank__api_agent_control(text: str) -> bool:
    """Java `String.isBlank()`：空串算空白；U+00A0 / U+202F 等**不算**（见 `_JAVA_SPACES`）。"""
    return not any(ch in _JAVA_NON_BLANK for ch in text) and all(ch in _JAVA_SPACES__api_agent_control
                                                                 for ch in text)


def _jackson_string__api_agent_control(value: Any) -> str | None:
    """Jackson 往 `ControlRequest.sessionId`（`String`）里塞 JSON 值时的强转。

    实测 18099：`123` → `"123"`（真去暂停，回"已暂停"）；`true` → `"true"`；
    对象 / 数组转不成 String，Jackson 抛 MismatchedInputException → Spring 400。
    """
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, bool):             # 必须在 int 之前：Python 里 bool 是 int 的子类
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    raise _NotString__api_agent_control(type(value).__name__)


def request_session_id(req: Request) -> str | None | Response:
    """`POST` 请求体 → `ControlRequest.sessionId`；拿不到对象时返回 `Response`（400）。

    返回 `None` 表示 Java 的 `request.sessionId() == null`（含显式 `null` 与"无此字段"）。
    """
    body = req.json
    if not isinstance(body, dict):          # 空体 / 非法 JSON / null / 数组 / 标量体
        return deps.spring_error(400, req.path)
    try:
        return _jackson_string__api_agent_control(body.get("sessionId"))
    except _NotString__api_agent_control:
        # 数组/对象绑不到 String：Jackson 抛 MismatchedInputException → Spring 400（实测）
        return deps.spring_error(400, req.path)


def query_session_id(req: Request) -> str | None | Response:
    """`GET /status` 的 `@RequestParam("sessionId")`；缺参数时返回 `Response`（400）。

    `?sessionId=` / `?sessionId=%20` 在 Java 里被 `StringTrimmerEditor(emptyAsNull=true)`
    归一成 null，所以这里也把"trim 后为空"折成 None（`get_state(None)` → RUNNING）。
    """
    raw = req.q("sessionId")
    if raw is None:                         # 参数整个缺失：Spring 必填校验 → 400
        return deps.spring_error(400, req.path)
    return None if not raw.strip() else raw


class AgentControlApi:
    """`/api/chat/control/*` —— 对应 Java `AgentControlController`（注入两个单例服务）。"""

    def __init__(self, ctx: deps.ApiContext) -> None:
        self.ctx = ctx

    # ------------------------------------------------------------ 依赖
    def control(self) -> Any:
        """运行控制（`pause` / `resume` / `stop` / `get_state`）。

        `deps.agent_control(ctx)` 就是 `ctx.service("agent_control", AgentControlStub)`：
        装配方 install 了真实 `lionbox.agent.AgentControlManager` 就用它，否则是窄桩。
        """
        return deps.agent_control(self.ctx)

    def questions(self) -> Any:
        """提问服务（`stop` 时取消该会话上等待中的提问，别让 worker 挂满 5 分钟）。

        与 `/api/questions/*` 取的是**同一个** `ctx.service("questions", …)`，
        所以 `POST /stop` 取消掉的提问，前端轮询 `/api/questions/pending` 也能立刻看到。
        """
        return deps.questions(self.ctx)

    # ------------------------------------------------------------ 共享逻辑
    def _check(self, req: Request) -> str | Response:
        """三个 POST 的共同前半段：请求体 → sessionId → 非空校验。

        返回 `str` 表示通过了 Java 的校验；返回 `Response` 是原样发出的 400。
        """
        session_id = request_session_id(req)
        if isinstance(session_id, Response):
            return session_id               # 请求体不是 JSON 对象 → Spring 直接 400
        if session_id is None or _java_blank__api_agent_control(session_id):
            return ApiResponse.error(ERR_MISSING_SESSION)
        return session_id

    def _state_of(self, session_id: str | None) -> str:
        """当前状态名（Java `agentControl.getState(id).name()`）。"""
        state = self.control().get_state(session_id)
        return str(getattr(state, "value", state))

    def _cancel_pending_questions(self, session_id: str) -> int:
        """取消该会话上等待中的提问并返回条数（Java `questionService.cancelSession`）。"""
        return deps.as_int(self.questions().cancel_session(session_id), 0)

    # ------------------------------------------------------------ 注册
    def register__api_agent_control(self, router) -> None:
        api = self

        @router.post("/api/chat/control/pause")
        def pause(req: Request):
            session_id = api._check(req)
            if not isinstance(session_id, str):
                return session_id
            api.control().pause(session_id)
            return ApiResponse.ok(data=None, message=MSG_PAUSED)

        @router.post("/api/chat/control/resume")
        def resume(req: Request):
            session_id = api._check(req)
            if not isinstance(session_id, str):
                return session_id
            api.control().resume(session_id)
            return ApiResponse.ok(data=None, message=MSG_RESUMED)

        @router.post("/api/chat/control/stop")
        def stop(req: Request):
            session_id = api._check(req)
            if not isinstance(session_id, str):
                return session_id
            api.control().stop(session_id)
            cancelled = api._cancel_pending_questions(session_id)
            message = (MSG_STOPPED_CANCELLED.format(n=cancelled) if cancelled > 0
                       else MSG_STOPPED)
            return ApiResponse.ok(data=None, message=message)

        @router.get("/api/chat/control/status")
        def status(req: Request):
            session_id = query_session_id(req)
            if isinstance(session_id, Response):
                return session_id           # 缺 sessionId 查询参数 → 400
            return ApiResponse.ok(api._state_of(session_id), message=MSG_STATUS)


def register__api_agent_control(router, ctx) -> None:
    AgentControlApi(ctx).register__api_agent_control(router)


# ========================================================================
# 原模块 lionbox/assembly.py
# ========================================================================
"""把**真实实现**装进接口层 —— 收尾 `api/deps.py` 里那些"窄桩"。

【为什么需要这个文件】`api/*` 的 111 个接口一直是照着"装配方之后会把真实对象
`ctx.install(name, obj)` 进来"写的：会话、事件、历史、提问、改动审核、Agent 主循环
在 `deps.py` 里都给的是窄桩（`SessionStoreStub` / `EventStoreStub` / `AgentLoopStub`…），
`AgentLoopStub.process_message` 直接抛 `DependencyMissing`。

而在本文件出现之前，**全项目没有任何一处调用 `ctx.install(...)`** ——
`wiring.py` 里的 `Wiring` 类把对象图建得好好的，却是一段死代码（零调用方）。
后果是 `/api/chat` 一律回"Agent 主循环尚未就绪"，工具永远不执行：
十几个端到端套件（多轮工具、工具参数强转、GBK、常驻终端、@ 引用、技能、
事件去重、ask_user…）全红，而且报的是同一句话。

【为什么不做成"改 app.py 去 new Wiring"】`app.py` 是冻结件（别的任务的产物，明令不许改）。
装配只能落在接口层自己的钩子上：`api/__init__.register_all()` 拿得到
`app_root + cfg + RuntimeApi`，正好是装配所需的全部输入。

【顺序】（有依赖，别随意调换）
    配置启动初始化 → 事件存储 → 会话/历史 → 技能仓库 → 提问/控制/审批 →
    改动审核闸门 → 适配器 + Agent 主循环 → 工具接线点 → 团队工具

【容错原则】任何一步失败都只记进返回值并打日志，绝不让应用起不来 ——
但在**日志和报告里如实说清哪一步没装上**，不假装成功。
"""


import traceback
from pathlib import Path
from typing import Any


#: 窄桩类型（用来判断"这一槽位里还是占位物吗"）。延迟导入，避免装配期循环。
def _stub_types() -> tuple[type, ...]:
    from lionbox.api import deps
    return (deps.SessionStoreStub, deps.EventStoreStub, deps.AgentLoopStub,
            deps.AgentControlStub, deps.QuestionServiceStub, deps.MentionResolverStub)


def _flag(ctx: Any, key: str, default: Any = "") -> str:
    """取启动属性（等价 Spring 的 `@Value`；`--lionbox.xxx=yyy` → extra["lionbox.xxx"]）。"""
    try:
        raw = ctx.extra.get(key, None)
    except Exception:                                   # noqa: BLE001
        raw = None
    if raw is None or str(raw).strip() == "":
        return default
    return str(raw)


def _flag_int__assembly(ctx: Any, key: str, default: int) -> int:
    try:
        return int(_flag(ctx, key, str(default)))
    except (TypeError, ValueError):
        return default


def _flag_bool__assembly(ctx: Any, key: str, default: bool) -> bool:
    raw = str(_flag(ctx, key, "true" if default else "false")).strip().lower()
    return raw in ("1", "true", "yes", "on")


# --------------------------------------------------------------------------
# ChatClient 门面：每次调用都取"当前激活的适配器"
# --------------------------------------------------------------------------
class AdapterClient:
    """把 `AdapterManager` 包成 `AgentLoop` 要的 ChatClient。

    【为什么不直接把适配器实例塞给 AgentLoop】Java 的 AgentLoop 注入的是
    **AdapterManager**，`adapterManager.getActiveAdapter()` 是每次调用现取的 ——
    用户在界面上切换适配器后立刻生效。Python 这边把实例钉死在构造期的话，
    切完还要重启才算数。所以这里包一层门面，`active_adapter` 是个方法，
    `AgentLoop._active_adapter()` 正好按"可调用就调用"处理。
    """

    def __init__(self, manager: Any) -> None:
        self._manager = manager

    def active_adapter(self) -> Any:
        return self._manager.get_active_adapter()

    def _level(self, thinking_level: Any) -> Any:
        try:
            from lionbox.llm.types import ThinkingLevel
            return ThinkingLevel.parse(thinking_level)
        except Exception:                               # noqa: BLE001
            return thinking_level

    def chat(self, messages: list[Any], tools: list[dict[str, Any]] | None = None,
             model: str | None = None, thinking_level: Any = None,
             max_tokens: int | None = None) -> Any:
        adapter = self.active_adapter()
        if adapter is None:
            raise RuntimeError("没有配置可用的模型适配器")
        level = self._level(thinking_level)
        with_opts = getattr(adapter, "chat_with_options", None)
        if with_opts is not None:
            return with_opts(list(messages), model or "", level, tools or None, None, max_tokens)
        return adapter.chat(list(messages), model or "", level, tools or None)

    def chat_stream(self, messages: list[Any], tools: list[dict[str, Any]] | None = None,
                    model: str | None = None, thinking_level: Any = None,
                    max_tokens: int | None = None):
        adapter = self.active_adapter()
        if adapter is None:
            raise RuntimeError("没有配置可用的模型适配器")
        level = self._level(thinking_level)
        limited = getattr(adapter, "chat_stream_limited", None)
        if max_tokens is not None and limited is not None:
            yield from limited(list(messages), model or "", level, tools or None, max_tokens)
            return
        yield from adapter.chat_stream(list(messages), model or "", level, tools or None)

    def play_sound(self, kind: str) -> None:
        """声音提示（Java `AgentLoop` 里也是从 client 上取的旁路能力）。"""
        fn = getattr(self._manager, "play_sound", None)
        if callable(fn):
            fn(kind)


# --------------------------------------------------------------------------
# SPI 桥：把全局扩展点注册表接成 AgentLoop 要的那**一个**对象
# --------------------------------------------------------------------------
class SpiBridge:
    """`AgentLoop(spi=...)` 只接受一个对象，而扩展点是一张注册表 —— 这里做桥接。

    【为什么必须有】技能目录注入、插件开关门禁、@ 引用展开、大循环参数、工具过滤
    全在 `plugins.lifecycle` 的 SPI 注册表里；AgentLoop 拿不到它们，
    用户"关掉插件"就只是界面上变灰，模型照样会去调那个工具。
    """

    def __init__(self, skill_repository: Any = None) -> None:
        self.skills = skill_repository

    # ---- 逐个转发到注册表的聚合函数 ----
    def filter_tool_names(self, session_id: str | None, names: set[str]) -> set[str]:
        from lionbox.plugins.lifecycle import filter_tool_names
        return filter_tool_names(session_id, names)

    def extra_system_sections(self, session_id: str | None, workspace_path: str | None,
                              user_message: str | None) -> list[str]:
        """把所有 SPI 追加的系统提示词段落收集起来（含技能目录）。

        【这里原来导错了名字】`AgentLoop._spi_sections` 要的是 `extra_system_sections`
        （本方法名没错），但本方法去 `plugins.lifecycle` 导入的也是 `extra_system_sections`
        —— 那边**没有**这个模块级函数，聚合函数叫 `collect_extra_sections`（它逐个遍历
        注册表里的 SPI，取各自的 `extra_system_sections`）。于是 ImportError 被上层
        `except Exception: return []` 吞掉：

            实测：技能目录（每个技能一行）与用户自定义技能永远进不了系统提示词，
            `_check_skills_at` 里"★ 系统提示词里有技能目录"那条一直红，
            而日志上却显示"技能目录注入已挂到 Agent 主循环" —— 看着像接好了。
        """
        from lionbox.plugins.lifecycle import collect_extra_sections
        return collect_extra_sections(session_id, workspace_path, user_message)

    def transform_user_message(self, session_id: str | None, user_message: str) -> str:
        from lionbox.plugins.lifecycle import transform_user_message
        return transform_user_message(session_id, user_message)

    def loop_int(self, session_id: str | None, key: str, fallback: int) -> int:
        from lionbox.plugins.lifecycle import loop_options
        value = loop_options(session_id).get(key, fallback)
        try:
            return int(value)
        except (TypeError, ValueError):
            return fallback

    def skills_for(self, user_message: str | None) -> list[Any]:
        """关键词命中的技能（正文要注进系统提示词）。

        Java 侧是 `pluginRegistry.getSkillPlugins()` 里挑 `isApplicable(msg)` 的那些；
        Python 侧技能定义自己带 `matches_keywords()`，规则一致。只挑**启用中**的，
        用户在设置里关掉的技能不该继续往提示词里塞。
        """
        repo = self.skills
        if repo is None:
            return []
        out: list[Any] = []
        try:
            for definition in repo.list():
                sid = getattr(definition, "id", None)
                try:
                    if sid is not None and not repo.is_enabled(sid):
                        continue
                except Exception:                       # noqa: BLE001
                    pass
                matcher = getattr(definition, "matches_keywords", None)
                if callable(matcher) and matcher(user_message):
                    out.append(definition)
        except Exception:                               # noqa: BLE001
            return []
        return out


# --------------------------------------------------------------------------
# 主入口
# --------------------------------------------------------------------------
def install_real_services(ctx: Any) -> dict[str, Any]:
    """把真实实现装进 `ApiContext`。返回 `{"installed": [...], "problems": [...]}`。"""
    installed: list[str] = []
    problems: list[str] = []

    def step(name: str, fn: Any) -> Any:
        try:
            value = fn()
            installed.append(name)
            return value
        except Exception as e:                          # noqa: BLE001
            problems.append(f"{name}: {type(e).__name__}: {e}")
            print(f"[装配] {name} 未完成（其余功能继续）: {type(e).__name__}: {e}", flush=True)
            print(traceback.format_exc(), flush=True)
            return None

    cfg = ctx.cfg
    app_root = Path(ctx.app_root)
    report: dict[str, Any] = {"installed": installed, "problems": problems}

    # ---- 0) 启动配置初始化（Java 的 @PostConstruct init()）------------------
    # 【没这一步会怎样】老配置里的底座模型名不迁移、安装程序写的 install-model.txt
    # 不生效、默认 provider 实例不补 —— 界面上的模型名与实际跑的对不上。
    def _config():
        from lionbox.config.app_config import AppConfigExtras
        extras = AppConfigExtras(cfg)
        extras.init()
        ctx.install("app_config_extras", extras)
        return extras
    step("配置启动初始化(AppConfigExtras.init)", _config)

    # ---- 1) 事件存储 -------------------------------------------------------
    events = step("事件存储(EventStore)", lambda: _build_events(ctx))

    # ---- 2) 会话 / 对话历史 -------------------------------------------------
    sessions = step("会话管理(SessionManager)", lambda: _build_sessions(ctx))
    history = step("对话历史(ConversationHistory)", lambda: _build_history(ctx))

    # ---- 3) 技能仓库 -------------------------------------------------------
    skills = step("技能仓库(SkillRepository)", lambda: _build_skills(ctx))

    # ---- 4) 提问 / 运行控制 / 授权策略 --------------------------------------
    questions = step("用户提问(UserQuestionService)", lambda: _build_questions(ctx))
    control = step("运行控制(AgentControlManager)", lambda: _build_control(ctx))
    approval = step("授权策略(ApprovalPolicy)", lambda: _build_approval(ctx))

    # ---- 5) 改动人工审核闸门 -----------------------------------------------
    review = step("改动审核(ChangeReview)", lambda: _build_review(ctx, history))

    # ---- 6) 适配器 + Agent 主循环 ------------------------------------------
    loop = step("Agent 主循环(AgentLoop)",
                lambda: _build_loop(ctx, cfg, history, events, control, approval))

    # 预算对象必须**同一个**：界面上改窗口（`/api/context`）与模型调 context_window 工具
    # 改的是同一份状态，否则"工具说改了、再查还是旧值"。
    if loop is not None:
        budget = getattr(loop, "context_budget", None)
        if budget is not None:
            ctx.install("context_budget", budget)
            step("上下文预算接线(context_window)", lambda: _hook_budget(budget))

    # ---- 7) 工具接线点 -----------------------------------------------------
    step("context_prune 接线", lambda: _hook_prune(history))
    step("ask_user 接线", lambda: _hook_ask_user(questions))
    step("模型自动下载接线", lambda: _hook_auto_download(ctx))

    # ---- 8) 团队工具（**必须带上 loop**）-----------------------------------
    step("子智能体/团队工具接线", lambda: _wire_team(loop, sessions, cfg))

    report["events"] = events
    report["sessions"] = sessions
    report["history"] = history
    report["loop"] = loop
    if installed:
        print(f"[装配] 真实实现已装入接口层: {', '.join(installed)}", flush=True)
    for p in problems:
        print(f"[装配] 未完成: {p}", flush=True)
    return report


# --------------------------------------------------------------------------
# 各步实现（单独函数，便于单测与排查）
# --------------------------------------------------------------------------
def _build_events(ctx: Any) -> Any:
    from lionbox.events.store import EventStore
    from lionbox.plugins.lifecycle import set_default_event_sink
    store = EventStore(auto_migrate_legacy=True)
    # 【必须先把事件 sink 换成它】否则插件注册/工具调用的事件写进插件系统自己那份
    # EventStore，而接口读的是另一个实例 —— 前端轮询的 🔧/✅/❌ 永远画不出来。
    set_default_event_sink(store)
    ctx.install("events", store)
    return store


def _build_sessions(ctx: Any) -> Any:
    from lionbox.sessions import SessionManager, SessionPersistence
    persistence = SessionPersistence()
    manager = SessionManager()
    manager.set_persistence(persistence)
    # 【启动时把历史会话读进来】等价 Java `SessionManager` 的 `@PostConstruct init()`
    # （`persistence.loadAllSessions()` → `restoreSession(...)`）。
    # 不读的话 `/api/sessions` 只看得到本次进程新建的会话 —— 用户重启软件后对话列表全空，
    # 而且老会话里那些已废弃的模式（PTC/CREATIVE）也不会走 `restore_session` 的归一
    # （`_check_modes.py` 抓到的就是这个）。坏文件由 `load_all_sessions` 自己跳过。
    try:
        for session in persistence.load_all_sessions():
            manager.restore_session(session.session_id, session.workspace_id, session.mode,
                                    session.created_at, session.name)
    except Exception as e:                              # noqa: BLE001 读不了就当没有历史
        print(f"[装配] 历史会话加载失败（继续，列表为空）: {type(e).__name__}: {e}", flush=True)
    ctx.install("session_persistence", persistence)
    ctx.install("sessions", manager)
    return manager


def _build_history(ctx: Any) -> Any:
    from lionbox.sessions import ConversationHistory
    history = ConversationHistory(auto_load=True)
    ctx.install("history", history)
    ctx.install("conversation_history", history)
    return history


def _build_skills(ctx: Any) -> Any:
    from lionbox.skills.repository import default_repository
    repo = default_repository()
    ctx.install("skill_repository", repo)
    return repo


def _build_questions(ctx: Any) -> Any:
    from lionbox.misc.question import UserQuestionService
    service = UserQuestionService()
    ctx.install("questions", service)
    return service


def _build_control(ctx: Any) -> Any:
    from lionbox.agent.control import AgentControlManager
    control = AgentControlManager()
    ctx.install("agent_control", control)
    return control


def _build_approval(ctx: Any) -> Any:
    from lionbox.agent import ApprovalPolicy
    policy = ApprovalPolicy()
    ctx.install("approvals", policy)
    return policy


def _build_review(ctx: Any, history: Any) -> Any:
    """改动审核闸门。

    `api/changes.py` 在装配期已经建过一份（并挂在工具的闸门接线点上），这里优先复用它
    —— 审核对象必须**只有一个**：界面上点"通过"和工具拦下改动要作用在同一份待审列表上。
    """
    from lionbox.agent.change import ChangeReview
    from lionbox.plugins.lifecycle import default_settings
    from lionbox.tools.file import _gate

    existing = None
    try:
        existing = ctx.service("changes", lambda: None)
    except Exception:                                   # noqa: BLE001
        existing = None
    if existing is not None and callable(getattr(existing, "intercept", None)):
        review = existing
        # settings 必须是插件设置对象：`ChangeReview.enabled()` 靠它读 settings.json 里的开关，
        # 传 AppConfigStore 会走兜底分支 → "设置里关掉了，文件照样被拦下来待审"。
        if not callable(getattr(getattr(review, "settings", None), "is_enabled", None)):
            try:
                review.settings = default_settings()
            except (AttributeError, TypeError):
                pass
        if history is not None and getattr(review, "history", None) is None:
            try:
                review.history = history
            except (AttributeError, TypeError):
                pass
    else:
        review = ChangeReview(history=history, settings=default_settings(),
                              enabled_by_default=_review_default(ctx))
    ctx.install("changes", review)
    if _gate.REVIEW_HOOK is None:
        _gate.set_review(review)
    return review


def _review_default(ctx: Any) -> bool:
    """出厂默认值 = 启动属性 `lionbox.change-review.enabled`（Java 的 `@Value` 同名键）。"""
    return _flag_bool__assembly(ctx, "lionbox.change-review.enabled", True)


def _build_loop(ctx: Any, cfg: Any, history: Any, events: Any,
                control: Any, approval: Any) -> Any:
    from lionbox.agent import AgentLoop
    from lionbox.plugins.base import REGISTRY
    from lionbox.tools import load as load_tools

    # 工具注册表：插件体系已经装过一次（`api/plugins.py`），这里只保证它非空。
    registry = REGISTRY
    if not list(registry.all()):
        registry = load_tools(None)

    adapters = ctx.adapters()
    client = AdapterClient(adapters)

    budget = ctx.service("context_budget", lambda: None)
    skills = ctx.service("skill_repository", lambda: None)
    sessions = ctx.service("sessions", lambda: None)

    loop = AgentLoop(
        client=client,
        config_store=cfg,
        registry=registry,
        event_store=events,
        history=history,
        workspace=None,          # 每个会话各自绑工作区，见下面的 workspace_resolver
        workspace_resolver=_workspace_resolver(sessions),
        permission_resolver=_permission_resolver(ctx, sessions),
        control=control,
        approval=approval,
        budget=budget,
        context_limit_tokens=_flag_int__assembly(ctx, "lionbox.agent.context-limit-tokens", 0),
        context_keep_recent=_flag_int__assembly(ctx, "lionbox.agent.context-keep-recent", 6),
        tool_timeout_seconds=_flag_int__assembly(ctx, "lionbox.agent.tool-timeout-seconds", 600),
        use_native_tools=normalize_tool_call_mode(_flag(ctx, "lionbox.agent.tool-call-mode", "auto")),
        spi=SpiBridge(skills),
    )
    ctx.install("agent_loop", loop)
    return loop


def _session_workspace_id(session: Any) -> str | None:
    """从会话对象上取工作区路径（`workspaceId` 就是工作区绝对路径，与 Java 一致）。"""
    if session is None:
        return None
    for attr in ("workspaceId", "workspace_id", "workspace"):
        value = getattr(session, attr, None)
        if value:
            return str(value)
    if isinstance(session, dict):
        for key in ("workspaceId", "workspace_id", "workspace"):
            if session.get(key):
                return str(session[key])
    return None


def _workspace_resolver(sessions: Any):
    """会话 → 工作区路径。

    【为什么必须有】`AgentLoop.resolve_workspace()` 在没有 resolver 时只会回落到
    构造时那个 `workspace`；装配方给的是 None（每个会话绑的工作区都不一样，不能在构造期钉死），
    于是 `WorkspaceContext` 里是空的，**工具把相对路径按进程 CWD（仓库根目录）解析** ——
    实测 `_check_tool_idempotent.py` 全套相对路径用例都报
    `文件不存在: <仓库根>\\sub`，而它们本该落在测试工作区里。
    Java 侧这一步是 `SessionManager` + `WorkspaceContext` 一起完成的。
    """
    def resolve(session_id: str | None) -> str | None:
        if not session_id or sessions is None:
            return None
        try:
            session = sessions.get_session(session_id)
        except Exception:                               # noqa: BLE001
            return None
        return _session_workspace_id(session)
    return resolve


def _permission_resolver(ctx: Any, sessions: Any):
    """会话 → 工作区权限等级（`READ_ONLY` / `WORKSPACE_WRITE` / `FULL_ACCESS`）。

    用户把某个工作区设成只读之后，写文件的工具必须真的被挡住；`AgentLoop.check_permission`
    靠的就是这个回调（Java 里从 `WorkspaceManager` 取）。
    """
    def resolve(session_id: str | None) -> str | None:
        ws_id = _workspace_resolver(sessions)(session_id)
        if not ws_id:
            return None
        try:
            store = ctx.service("workspaces", lambda: None)
            entry = store.get_workspace(ws_id) if store is not None else None
        except Exception:                               # noqa: BLE001
            return None
        if isinstance(entry, dict):
            value = entry.get("permission")
            return str(value) if value else None
        return None
    return resolve


def _hook_budget(budget: Any) -> None:
    from lionbox.tools.context import context_window
    context_window.set_budget(budget)


def _hook_prune(history: Any) -> None:
    if history is None:
        return
    from lionbox.tools.context import context_prune
    setter = getattr(context_prune, "set_history", None)
    if callable(setter):
        setter(history)


def _hook_ask_user(questions: Any) -> None:
    if questions is None:
        return
    from lionbox.tools.system import ask_user
    setter = getattr(ask_user, "set_question_service", None)
    if callable(setter):
        setter(questions)


def _hook_auto_download(ctx: Any) -> Any:
    """把"后台下载指定权重"接到本地运行时的启动路径上（模型没下载时自动补齐）。

    Java 里这些下载方法本来就在 `LocalModelRuntime` 上；Python 侧它们在
    `api/runtime_extra.LocalModelsSupport` 里（同一个 runtime 实例的薄适配层），
    所以这里用接线点把它挂回去（`local/runtime.set_auto_downloader`）。
    """
    from lionbox.api.runtime_extra import LocalModelsSupport
    from lionbox.local import runtime as local_runtime
    support = LocalModelsSupport(ctx)
    local_runtime.set_auto_downloader(support.start_download)
    return support


def _wire_team(loop: Any, sessions: Any, cfg: Any) -> list[str]:
    """把 `agent_spawn` / `agent_team_run` 挂上 **带 AgentLoop 的**那一份。

    【为什么不是简单再调一次 register_team_tools】`api/plugins.py` 在接口装配期
    已经调过一次 `register_team_tools(registry)`（那时还没有 AgentLoop），
    而注册器对已注册的 id 直接 `continue` —— 再调一次也不会把 loop 补上，
    结果是"子智能体工具在、但一派发就说没接线"。所以这里先把旧的两个摘掉再重挂。

    【settings 必须传插件设置对象，不是 AppConfigStore】子智能体/团队插件读的是
    `settings.int_of(...)` / `settings.is_enabled(...)`（`PluginSettings` 的接口），
    传 AppConfigStore 会抛 `'AppConfigStore' object has no attribute 'int_of'`，
    工具一调就报"工具执行异常"（`_check_plugin_extras.py` 抓到的就是这个）。
    """
    from lionbox.plugins.lifecycle import default_registry, default_settings
    from lionbox.team.registrar import register_team_tools

    registry = default_registry()
    for tool_id in ("tool.agent.spawn", "tool.agent.team"):
        remover = getattr(registry, "unregister", None)
        if callable(remover):
            try:
                if registry.get_by_id(tool_id) is not None:
                    remover(tool_id)
            except Exception:                           # noqa: BLE001
                pass
    return register_team_tools(registry, agent_loop=loop, session_manager=sessions,
                               settings=default_settings())

# ========================================================================
# 原模块 lionbox/__init__.py
# ========================================================================
"""Lion Code Python 版。"""



# ========================================================================
# 原模块 lionbox/__main__.py
# ========================================================================
"""`python -m lionbox` 入口。

参数与 Java 版启动器保持一致，这样 `launcher.ps1` 只改一行命令就能切过来：
  Java:  java -Dlionbox.prewarm.on-start=true -jar xxx.jar --server.port=8080
  Python: python -m lionbox --server.port=8080 --lionbox.prewarm.on-start=true

支持 `--lionbox.*` 形式的覆盖（与 Spring 的 `-D` 同义），未识别的键进 extra，供后续模块读取。
"""


import argparse
import os
import sys
from pathlib import Path

#: argparse 自己负责的选项名（其余 `--xxx=yyy` 一律当"启动属性覆盖"，等价 Spring 的 `--key=value`）
ARGPARSE_OPTS = frozenset({
    "server.port", "server.address", "bind-addr", "app-root", "config-dir",
    "version", "help",
})

#: Java 启动属性 → Python 侧等价的进程级开关。
#: 【为什么要这张表】Java 版这些值是 Spring 的 `@Value`，任何 `--key=value` 都能覆盖；
#: Python 版没有属性源，必须在 `main()` 一开始把它们落到环境变量上 ——
#: 而 `events.store` / `sessions.history` 这些模块的默认路径是**import 期**算出来的，
#: 所以设置必须发生在 import `lionbox.app` 之前（这正是本文件把 import 挪进 main 的原因）。
PROPERTY_ENV = {
    "lion.workspace.default-path": "LION_WORKSPACE_DEFAULT_PATH",
    "lion.event.store-path": "LION_EVENT_STORE_PATH",
    "lion.plugin.scan-path": "LION_PLUGIN_SCAN_PATH",
    "lion.skills.dir": "LION_SKILLS_DIR",
    "lionbox.change-review.enabled": "LIONBOX_CHANGE_REVIEW_ENABLED",
}


def _collect_overrides(argv: list[str]) -> tuple[dict[str, str], list[str]]:
    """把 `--key=value` / `--key value` 拆成 (覆盖项, 其余参数)。

    【踩过的坑】原来只认 `--lionbox.*`，于是 `--lion.workspace.default-path=...`
    （Java 的 application.yml 属性，套件里到处在用）会掉进 argparse，直接
    "unrecognized arguments" 退出 —— 后端起不来，看起来却像应用坏了。
    """
    extra: dict[str, str] = {}
    rest: list[str] = []
    i = 0
    while i < len(argv):
        a = argv[i]
        key = a[2:].split("=", 1)[0] if a.startswith("--") else ""
        if key and key not in ARGPARSE_OPTS:
            if "=" in a:
                k, v = a[2:].split("=", 1)
            elif i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                k = a[2:]
                v = argv[i + 1]
                i += 1
            else:
                k, v = a[2:], ""
            extra[k] = v
        else:
            rest.append(a)
        i += 1
    return extra, rest


def _apply_property_overrides(extra: dict[str, str]) -> None:
    """把 Java 风格的启动属性落到环境变量（必须在 import lionbox.app 之前调用）。"""
    for key, env in PROPERTY_ENV.items():
        if key in extra:
            os.environ[env] = str(extra[key])


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="lionbox", description="Lion Code 本地 AI 编程助手（Python 版）")
    p.add_argument("--server.port", dest="port", type=int, default=8080)
    p.add_argument("--server.address", dest="host", default="127.0.0.1")
    p.add_argument("--bind-addr", dest="bind", default=None,
                   help="host:port 形式（与 code-server 风格一致）")
    p.add_argument("--app-root", dest="app_root", default=None,
                   help="程序目录（放 runtime-vulkan/、*.gguf、web/ 的地方）")
    p.add_argument("--config-dir", dest="config_dir", default=None,
                   help="配置目录（默认 ~/.lioncode）")
    p.add_argument("--version", action="store_true")
    return p


def main(argv: list[str] | None = None) -> int:
    # 【必须先把标准输出切成 UTF-8】Windows 下输出被重定向到文件时，Python 用系统 ANSI 代码页
    # （中文机器上是 GBK）编码，启动横幅里的 emoji / 中文会直接抛 UnicodeEncodeError 把进程打死。
    # Java 版靠启动器的 `-Dfile.encoding=UTF-8` 躲过这件事，Python 这边在进程内自己做，
    # 不依赖调用方设置环境变量。
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[union-attr]
        except (AttributeError, ValueError, OSError):
            pass

    # 【把 logging 接上】应用里到处是 `log.info/error`，但从来没配置过 logging ——
    # 那些信息（"找不到可写目录""GGUF 魔数校验失败"之类）全部无声丢弃，
    # 排查时只能看到"什么都没发生"。命令行模式下直接打到 stderr。
    import logging
    logging.basicConfig(level=logging.INFO,
                        format="%(levelname)s %(name)s: %(message)s",
                        stream=sys.stderr)

    argv = list(sys.argv[1:] if argv is None else argv)
    extra, rest = _collect_overrides(argv)
    _apply_property_overrides(extra)      # 必须在下面这些 import 之前

    from lionbox.app import VERSION, LionBox
    from lionbox.config.store import AppConfigStore

    args = build_parser().parse_args(rest)
    if args.version:
        print(f"lionbox {VERSION} (python)")
        return 0

    host, port = args.host, args.port
    if args.bind and ":" in args.bind:
        h, p = args.bind.rsplit(":", 1)
        host, port = h or host, int(p)

    app_root = Path(args.app_root) if args.app_root else None
    # 先把默认目录设成进程级：技能仓库/插件设置等模块各自 new AppConfigStore 时才一致
    if args.config_dir:
        from lionbox.config.store import set_default_base
        set_default_base(args.config_dir)
    cfg = AppConfigStore(Path(args.config_dir) if args.config_dir else None)

    app = LionBox(app_root=app_root, host=host, port=port, config=cfg, extra=extra)
    app.http.extra = extra  # type: ignore[attr-defined]

    print(f"🦁 Lion Code (Python {sys.version_info.major}.{sys.version_info.minor}) "
          f"启动完成，监听端口: {port}  （装配耗时 {app.boot_seconds * 1000:.0f} ms）", flush=True)
    if extra:
        print("   覆盖配置: " + ", ".join(f"{k}={v}" for k, v in extra.items()), flush=True)
    try:
        app.start(block=True)
    except KeyboardInterrupt:
        pass
    finally:
        app.stop()
    return 0


if __name__ == "__lionbox_inlined__":  # 内联后不再作为入口
    raise SystemExit(main())


# ========================================================================
# 原模块 lionbox/agent/_verify.py
# ========================================================================
"""Agent 核心的自验脚本（**只依赖标准库与本包**，可随时重跑）。

跑法：
    cd C:\\Users\\Leo\\Desktop\\lion-code\\python
    .\\.venv\\Scripts\\python.exe -m lionbox.agent._verify

覆盖：
  A. 解析器：12 个「本地模型风格」的坏工具调用样本，逐个走
     parsing.parse → name_aliases.resolve → arg_aliases.match_key → AgentLoop.coerce_arguments，
     打印「输入 → 解析结果」；再验证 AgentLoop 的 XML / JSON 文本通道解析。
  B. 工具名归一化 / 参数名归一化的判定表（含「有歧义就不猜」）。
  C. 主循环：脚本化 FakeChatClient（先给一次工具调用、再给最终回答）跑通一轮，
     验证工具被派发、结果回灌、第二轮结束、事件被记录；再验证文本通道、
     未找到工具、残缺调用纠正、流式链路、极简模式。
  D. ToolCallGuard：只统计不拦截。
  E. ContextCompressor / ContextBudget：预算内、system 在最前、不切散 tool 配对。
  F. ApprovalPolicy：默认放行 / CONFIRM / BLOCK。
  G. ChangeReview + Diff + PendingChange：不落盘 → 通过才写盘；打回；冲突检测。
"""


import io
import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from lionbox.agent import arg_aliases, name_aliases, parsing
from lionbox.agent.approval import ApprovalAction, ApprovalPolicy, ToolPolicy
from lionbox.agent.change import APPROVED, PENDING, REJECTED, ChangeReview, Diff, PendingChange
from lionbox.plugins.base import PermissionLevel, PluginRegistry, ToolCategory, ToolPlugin, ToolResult

# stdout 按 UTF-8 输出，避免 Windows 控制台把中文写成乱码
if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace",
                                  line_buffering=True)

PASS = 0
FAIL = 0

#: 与真实注册表同名同 schema 的最小工具替身（真实 60 个工具由 lionbox/tools/ 提供，
#: 这里只对齐「名字 / schema / 权限」三件事，用来验证主循环）
L = "\u300c"      # 中文左书名号，用来代替会污染源码的引号
R = "\u300d"


def q(text: str) -> str:
    return L + text + R


def check(label: str, ok: bool, detail: str = "") -> bool:
    global PASS, FAIL
    if ok:
        PASS += 1
        print("  [OK]   " + label)
    else:
        FAIL += 1
        print("  [FAIL] " + label + ("   <- " + detail if detail else ""))
    return ok


def section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


# ==========================================================================
# 测试用工具（最小替身）
# ==========================================================================


class ReadFileTool(ToolPlugin):
    minimal_mode = True

    @property
    def id(self): return "tool.file.read"

    @property
    def name(self): return "read_file"

    @property
    def description(self): return "读取文件内容"

    @property
    def category(self): return ToolCategory.FILE_OPERATION

    @property
    def permission(self): return PermissionLevel.READ_ONLY

    def parameters_schema(self):
        return {"type": "object", "properties": {"path": {"type": "string"}},
                "required": ["path"]}

    def execute(self, args):
        if "path" not in args:
            return ToolResult.fail("缺少 path 参数")
        return ToolResult.ok("文件内容：" + str(args["path"]).replace("\\", "/").split("/")[-1])


class HeadTailTool(ToolPlugin):
    minimal_mode = True

    @property
    def id(self): return "tool.file.headtail"

    @property
    def name(self): return "head_tail_file"

    @property
    def description(self): return "查看文件头部或尾部N行"

    @property
    def category(self): return ToolCategory.FILE_OPERATION

    def parameters_schema(self):
        return {"type": "object",
                "properties": {"path": {"type": "string"}, "lines": {"type": "integer"}},
                "required": ["path"]}

    def execute(self, args):
        # 真实工具里就是 ((Number) args.get("lines")).intValue()：
        # 字符串 "5" 会 ClassCastException —— coerce_arguments 必须把它转成 int
        if not isinstance(args.get("lines"), int):
            return ToolResult.fail("参数 lines 不是数字: " + type(args.get("lines")).__name__)
        return ToolResult.ok("前 " + str(args["lines"]) + " 行（" + str(args["path"]) + "）")


class WriteFileTool(ToolPlugin):
    minimal_mode = True

    @property
    def id(self): return "tool.file.write"

    @property
    def name(self): return "write_file"

    @property
    def description(self): return "新建文件并写入内容"

    @property
    def category(self): return ToolCategory.FILE_OPERATION

    @property
    def permission(self): return PermissionLevel.WRITE

    def parameters_schema(self):
        return {"type": "object",
                "properties": {"path": {"type": "string"}, "content": {"type": "string"}},
                "required": ["path"]}

    def execute(self, args):
        p = self.resolve_path(str(args.get("path", "")))
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(str(args.get("content", "")), encoding="utf-8")
        return ToolResult.ok("已写入 " + p.name)


class ExecuteCommandTool(ToolPlugin):
    minimal_mode = True

    @property
    def id(self): return "tool.shell.execute"

    @property
    def name(self): return "execute_command"

    @property
    def description(self): return "执行命令"

    @property
    def category(self): return ToolCategory.SHELL

    @property
    def permission(self): return PermissionLevel.EXECUTE

    def parameters_schema(self):
        return {"type": "object", "properties": {"command": {"type": "string"}},
                "required": ["command"]}

    def execute(self, args):
        return ToolResult.ok("$ " + str(args.get("command", "")))


class MoveFileTool(ToolPlugin):
    minimal_mode = True

    @property
    def id(self): return "tool.file.move"

    @property
    def name(self): return "move_file"

    @property
    def description(self): return "移动或改名"

    @property
    def category(self): return ToolCategory.FILE_OPERATION

    @property
    def permission(self): return PermissionLevel.WRITE

    def parameters_schema(self):
        return {"type": "object",
                "properties": {"source": {"type": "string"}, "target": {"type": "string"}},
                "required": ["source", "target"]}

    def execute(self, args):
        if "source" not in args or "target" not in args:
            return ToolResult.fail("缺少参数: "
                                   + json.dumps(sorted(args.keys()), ensure_ascii=False))
        return ToolResult.ok("已移动 " + str(args["source"]) + " → " + str(args["target"]))


class ContextWindowTool(ToolPlugin):
    """真实存在（tool.context.window），用来验证提示词里的「上下文经济」那一段。

    提示词里点名的是 context_window 这个词，所以替身也必须叫这个名字，
    否则 TOOL_TOKEN 正则抓不到对照表里 → 后面那个词，表格过滤测不出来。
    """

    minimal_mode = False

    @property
    def id(self): return "tool.context.window"

    @property
    def name(self): return "context_window"

    @property
    def description(self): return "调整本会话的上下文窗口"

    @property
    def category(self): return ToolCategory.CONTEXT

    def parameters_schema(self):
        return {"type": "object", "properties": {"tokens": {"type": "integer"}},
                "required": ["tokens"]}

    def execute(self, args):
        return ToolResult.ok("窗口 = " + str(args.get("tokens")))


class WebSearchTool(ToolPlugin):
    """永久注册表里的「模式外」工具，用来验证极简模式拒绝。"""

    minimal_mode = False

    @property
    def id(self): return "tool.web.search"

    @property
    def name(self): return "web_search"

    @property
    def description(self): return "联网搜索"

    @property
    def category(self): return ToolCategory.WEB

    def parameters_schema(self):
        return {"type": "object", "properties": {"query": {"type": "string"}},
                "required": ["query"]}

    def execute(self, args):
        return ToolResult.ok("搜索结果")


class ListDirectoryTool(ReadFileTool):
    """真实注册表里 list_directory 也是 (path*) 形状，这里用同一份替身占名，
    好让「模型喊 ls / list_dir → 归一化成 list_directory → 真的执行」这条链路能被验证。"""

    @property
    def id(self): return "tool.file.list"

    @property
    def name(self): return "list_directory"

    @property
    def description(self): return "列出目录内容"

    def execute(self, args):
        return ToolResult.ok("目录内容：" + str(args.get("path", "")))


def build_registry(workspace: Path) -> PluginRegistry:
    reg = PluginRegistry()
    for cls in (ReadFileTool, HeadTailTool, WriteFileTool, ExecuteCommandTool, MoveFileTool,
                ContextWindowTool, WebSearchTool, ListDirectoryTool):
        reg.register(cls(workspace))
    return reg


#: 工具名归一化的 known 列表。**以 Java `ToolNameAliases.main` 里那份为基础**
#: （read_file / list_directory / execute_command / head_tail_file / line_count /
#:  git_status / git_commit），再加上样本里出现的真实工具名。
#: 两条负向用例必须留着，它们盯的是「别名表里有、但当前模式没开放 → 不硬转」这条分支：
#: translate 在别名表里但不在 known 里、delete_directory_placeholder 压根不在表里。
KNOWN_TOOLS = ["read_file", "list_directory", "execute_command", "head_tail_file",
               "line_count", "git_status", "git_commit",
               "write_file", "timestamp", "git_log"]

#: 样本里出现的工具名 → 用来跑参数名归一化 / 类型转换的 schema 替身
SCHEMA_TOOLS: dict[str, type[ToolPlugin]] = {
    "read_file": ReadFileTool,
    "list_directory": ReadFileTool,
    "head_tail_file": HeadTailTool,
    "write_file": WriteFileTool,
    "execute_command": ExecuteCommandTool,
    "timestamp": ContextWindowTool,
    "git_status": ExecuteCommandTool,
    "git_log": ExecuteCommandTool,
}


# ==========================================================================
# 脚本化的假 ChatClient
# ==========================================================================


class FakeChatClient:
    """按脚本吐响应；同时把每次请求的 messages 记下来，供断言「结果是否回灌」。"""

    def __init__(self, script: list[Any]) -> None:
        self.script = list(script)
        self.calls: list[list[ChatMessage__agent_loop]] = []
        self.tools_seen: list[Any] = []
        self.max_tokens_seen: list[Any] = []
        self.sounds: list[str] = []

    def chat(self, messages, tools=None, model=None, thinking_level=None,
             max_tokens=None, **opts):
        self.calls.append(list(messages))
        self.tools_seen.append(tools)
        self.max_tokens_seen.append(max_tokens)
        if not self.script:
            return {"content": "（脚本已空）", "tool_calls": [], "finish_reason": "stop"}
        item = self.script.pop(0)
        return item(messages) if callable(item) else item

    def play_sound(self, kind: str) -> None:
        self.sounds.append(kind)


class FakeStreamChatClient(FakeChatClient):
    """只实现 chat_stream 的客户端（脚本每项是一串分片）。"""

    def chat_stream(self, messages, tools=None, model=None, thinking_level=None,
                    max_tokens=None, **opts):
        self.calls.append(list(messages))
        self.tools_seen.append(tools)
        item = self.script.pop(0)
        for c in item:
            yield c


def native_tool_call(call_id: str, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    return {"id": call_id, "name": name, "arguments": arguments}


def tool_messages(messages: list[ChatMessage__agent_loop]) -> list[ChatMessage__agent_loop]:
    return [m for m in messages if m.role == "tool"]


# ==========================================================================
# A. 解析器：12 个本地模型风格的坏工具调用样本
# ==========================================================================

SAMPLES: list[tuple[str, str, str]] = [
    ("1", "工具名写错（ls），参数名写错（file_path）",
     "我看看目录里有什么。\n<tool_call>\n<function=ls>\n<parameter=file_path>src</parameter>\n"
     "</function>\n</tool_call>"),

    ("2", "JSON 缺右括号 + 一次两个块（尾部被服务端截断的形状）",
     "<tool_call>\n<function=execute_command>\n<parameter=command>echo hi</parameter>\n"
     "</function>\n</tool_call>\n<tool_call>\n<function=read_file>\n<parameter=path>a.txt\n"
     "</parameter>\n</function>\n</tool_call>"),

    ("3", "参数是已解析的 JSON 对象（没有 parameter 标签）",
     "<tool_call>\n<function=write_file>\n{\"path\": \"out/a.txt\", \"content\": \"hello\"}\n"
     "</function>\n</tool_call>"),

    ("4", "参数是 JSON 字符串 + ```json 围栏 + 前面带一句解释",
     "<tool_call>\n<function=write_file>\n我来写一下：\n```json\n"
     "{\"file_path\": \"b.txt\", \"text\": \"hi\"}\n```\n</function>\n</tool_call>"),

    ("5", "一次多个调用（模板原生，无 tool_call 外壳讲解）",
     "<tool_call>\n<function=git_status>\n<parameter=path>.</parameter>\n</function>\n</tool_call>\n"
     "<tool_call>\n<function=git_log>\n<parameter=count>3</parameter>\n</function>\n</tool_call>"),

    ("6", "空转重复：同一调用连写两次（Guard 只统计不拦）",
     "<tool_call>\n<function=timestamp>\n</function>\n</tool_call>\n"
     "<tool_call>\n<function=timestamp>\n</function>\n</tool_call>"),

    ("7", "缺右括号 / 缺 </function>（残缺块，不许硬凑）",
     "<tool_call>\n<function=read_file>\n<parameter=path>missing.txt"),

    ("8", "函数体里没有 parameter 标签，直接跟 JSON 且键名是 camelCase",
     "<tool_call>\n<function=head_tail_file>\n{\"path\": \"x.txt\", \"lines\": \"5\"}\n"
     "</function>\n</tool_call>"),

    ("9", "工具名多打一个字母（git_statuss）+ 值里带换行的多行命令",
     "<tool_call>\n<function=git_statuss>\n<parameter=path>\nrepo\n</parameter>\n"
     "</function>\n</tool_call>"),

    ("10", "半对的名字（list_dir_contents）+ 递归参数",
     "<tool_call>\n<function=list_dir_contents>\n<parameter=path>.</parameter>\n"
     "<parameter=recursive>true</parameter>\n</function>\n</tool_call>"),

    ("11", "普通正文，不该被误判成工具调用",
     "我先看看这个目录里有什么，然后告诉你。"),

    ("12", "模型自造工具名（delete_directory_placeholder，项目里并不存在）",
     "<tool_call>\n<function=delete_directory_placeholder>\n<parameter=path>tmp</parameter>\n"
     "</function>\n</tool_call>"),
]


#: 只为了调 `coerce_arguments` / `tool_signature` / `build_system_prompt` 存在的循环实例。
#: 强制 use_native_tools="prompt"：这样文本通道的清单/对照表/参数签名一定写进提示词。
#: auto 在「没有适配器」时按 Java 的规则判**原生**通道（那时清单是不写的，Qwen 模板自己渲染）。
_SCHEMA_LOOP = AgentLoop(client=None, registry=build_registry(Path(".")),
                         use_native_tools="prompt")


def sample_fix(raw_name: str, raw_args: dict[str, Any], tool_for_schema: Any
               ) -> tuple[str | None, dict[str, Any], str]:
    """走一遍真实链路：名字归一化 → 参数名归一化 → 类型转换。"""
    canonical = name_aliases.resolve(raw_name, KNOWN_TOOLS)
    args = dict(raw_args)
    rename_log: list[str] = []
    schema = tool_for_schema.parameters_schema() if tool_for_schema is not None else {}
    props = schema.get("properties", {})
    for declared in props:
        if declared in args:
            continue
        matched = arg_aliases.match_key(declared, list(args.keys()))
        if matched is not None and args.get(matched) is not None:
            args[declared] = args[matched]
            rename_log.append(matched + " → " + declared)
    coerced = _SCHEMA_LOOP.coerce_arguments(tool_for_schema, args) \
        if tool_for_schema is not None else args
    return canonical, coerced, ", ".join(rename_log)


def run_parser_samples() -> None:
    section("A. 解析器：本地模型风格的坏工具调用样本（输入 → 解析结果）")

    schema_of = {name: cls(Path(".")) for name, cls in SCHEMA_TOOLS.items()}

    for num, title, text in SAMPLES:
        print("\n--- 样本 " + num + "：" + title)
        print("    输入 : " + text.replace("\n", "\\n")[:170])
        calls = parsing.parse(text)
        if not calls:
            print("    解析 : 无工具调用（按普通正文处理）")
            print("    剥离 : strip_calls → " + repr(parsing.strip_calls(text))[:110])
            if num == "7":
                check("样本 7 残缺块不硬凑（解析结果为空）", not calls)
            if num == "11":
                check("样本 11 普通正文不误判", not calls)
            continue

        for i, call in enumerate(calls):
            tool = schema_of.get(call.name) or schema_of.get(
                name_aliases.resolve(call.name, KNOWN_TOOLS) or "")
            canonical, fixed, rename_log = sample_fix(call.name, call.arguments, tool)
            print("    调用{}: 原名={!r} 参数={}".format(
                i + 1, call.name, json.dumps(call.arguments, ensure_ascii=False)))
            print("           归一化工具名: {!r} -> {!r}".format(call.name, canonical))
            print("           参数名修复  : {}".format(rename_log or "（无需修复）"))
            print("           最终参数    : {}".format(
                json.dumps(fixed, ensure_ascii=False, default=str)))

        if num == "1":
            check("样本 1 ls → list_directory",
                  name_aliases.resolve("ls", KNOWN_TOOLS) == "list_directory")
        if num == "3":
            check("样本 3 JSON 对象被读成参数",
                  calls[0].arguments == {"path": "out/a.txt", "content": "hello"})
        if num == "4":
            check("样本 4 围栏 + 前导解释也能读出来",
                  calls[0].arguments == {"file_path": "b.txt", "text": "hi"})
        if num == "5":
            check("样本 5 一次两个调用都解析出来", len(calls) == 2)
        if num == "6":
            check("样本 6 空转重复：两个块都解析出来（拦不拦是 Guard 的事，它不拦）",
                  len(calls) == 2 and calls[0].name == calls[1].name == "timestamp")
        if num == "8":
            check("样本 8 参数先当字符串读出来（类型转换交给 coerce_arguments）",
                  isinstance(calls[0].arguments.get("lines"), str))
        if num == "9":
            check("样本 9 git_statuss → git_status（编辑距离 1）",
                  name_aliases.resolve("git_statuss", KNOWN_TOOLS) == "git_status")
        if num == "10":
            check("样本 10 list_dir_contents → list_directory",
                  name_aliases.resolve("list_dir_contents", KNOWN_TOOLS) == "list_directory")
        if num == "12":
            check("样本 12 自造工具名解析不出候选（上层会报未找到 + 建议）",
                  name_aliases.resolve("delete_directory_placeholder", KNOWN_TOOLS) is None)

    loop = AgentLoop(client=FakeChatClient([]), registry=build_registry(Path(".")))
    tcs = loop.parse_tool_calls_from_text(SAMPLES[0][2])
    check("AgentLoop.parse_tool_calls_from_text 走模板原生通道",
          len(tcs) == 1 and tcs[0].name == "ls" and tcs[0].arguments == {"file_path": "src"})

    xml = ("<tool_call><name>read_file</name><arguments>{\"path\": \"a.txt\"}</arguments>"
           "</tool_call>")
    tcs = loop.parse_tool_calls_from_text(xml)
    check("XML name/arguments 通道", len(tcs) == 1 and tcs[0].name == "read_file")

    loose = "<name>read_file</name><arguments>{\"path\": \"b.txt\"}</arguments>"
    tcs = loop.parse_tool_calls_from_text(loose)
    check("未包裹 tool_call 的宽松 XML 通道（MiMo 会这么吐）",
          len(tcs) == 1 and tcs[0].arguments.get("path") == "b.txt")

    js = "```json\n{\"name\": \"read_file\", \"arguments\": {\"path\": \"c.txt\"}}\n```"
    tcs = loop.parse_tool_calls_from_text(js)
    check("```json 代码块里的裸 JSON 通道",
          len(tcs) == 1 and tcs[0].arguments.get("path") == "c.txt")

    nested = ("<tool_call>{\"type\": \"function\", \"function\": {\"name\": \"read_file\", "
              "\"arguments\": \"{\\\"path\\\": \\\"d.txt\\\"}\"}}</tool_call>")
    tcs = loop.parse_tool_calls_from_text(nested)
    check("OpenAI 嵌套 function 格式（arguments 是 JSON 字符串）",
          len(tcs) == 1 and tcs[0].arguments.get("path") == "d.txt")

    check("remove_tool_call_blocks 剥离后只剩正文",
          loop.remove_tool_call_blocks(SAMPLES[0][2]).strip() == "我看看目录里有什么。")


# ==========================================================================
# B. 别名判定表
# ==========================================================================


def run_alias_tables() -> None:
    section("B. 工具名 / 参数名归一化判定表")

    cases: list[tuple[str, str | None]] = [
        # 前 19 条照抄 Java ToolNameAliases.main 的自检用例
        ("ls", "list_directory"), ("list_files", "list_directory"),
        ("List_Directory", "list_directory"), ("ls_directory", "list_directory"),
        ("read_file_content", "read_file"), ("do_list_directory", "list_directory"),
        ("Status", "git_status"), ("cat", "read_file"), ("read", "read_file"),
        ("head", "head_tail_file"), ("bash", "execute_command"),
        ("run_command", "execute_command"), ("wc", "line_count"),
        ("git_statuss", "git_status"), ("git-commit", "git_commit"),
        ("readfile", "read_file"), ("delete_directory_placeholder", None),
        ("translate", None), ("", None),
        # 别名表里有、但当前模式没开放这个工具 → 不硬转
        ("web_search", None),
    ]
    for raw, expect in cases:
        got = name_aliases.resolve(raw, KNOWN_TOOLS)
        check("工具名 {!r} -> {!r}".format(raw, expect), got == expect, "实际 " + repr(got))

    check("ls_l 仍然是 list_directory（别名表不许再被 file_info 覆盖）",
          name_aliases.resolve("ls_l", KNOWN_TOOLS + ["file_info"]) == "list_directory")
    check("包含多个真实工具名 -> 不猜",
          name_aliases.resolve("read_file_and_git_commit", ["read_file", "git_commit"]) is None)
    check("别名表大小 = 267（逐条搬全）", name_aliases.size() == 267)
    check("参数别名表 = 36 组 / 188 个别名",
          arg_aliases.size() == 36 and sum(len(v) for v in arg_aliases.ALIASES.values()) == 188)

    arg_cases = [
        ("path", ["file_path"], "file_path"), ("path", ["FilePath"], "FilePath"),
        ("maxDepth", ["max_depth"], "max_depth"), ("maxDepth", ["maxdepth"], "maxdepth"),
        ("content", ["contents"], "contents"), ("command", ["cmd"], "cmd"),
        ("source", ["src"], "src"), ("target", ["destination"], "destination"),
        ("path", ["unknown_key"], None), ("path", [], None),
        ("path", ["path"], "path"),
    ]
    for declared, given, expect in arg_cases:
        got = arg_aliases.match_key(declared, given)
        check("参数 {!r} + {!r} -> {!r}".format(declared, given, expect), got == expect,
              "实际 " + repr(got))
    check("参数名多候选 -> 不猜",
          arg_aliases.match_key("content", ["text", "data"]) is None)


# ==========================================================================
# C. 主循环
# ==========================================================================


def run_main_loop(work: Path) -> None:
    section("C. 主循环：FakeChatClient 跑通一轮（工具派发 / 结果回灌 / 第二轮结束 / 事件）")

    events = LocalEventStore()
    history = LocalConversationHistory()
    client = FakeChatClient([
        {"content": "先读一下文件。",
         "tool_calls": [native_tool_call("call_1", "read_file", {"path": "notes.txt"})],
         "finish_reason": "tool_calls"},
        {"content": "读完了，内容是 notes.txt。", "tool_calls": [], "finish_reason": "stop"},
    ])
    loop = AgentLoop(client=client, registry=build_registry(work), event_store=events,
                     history=history, workspace=work)
    answer = loop.process_message("s1", "读一下 notes.txt", "STANDARD", "low", "fake-model")

    print("\n  最终回答: " + answer)
    print("  模型调用次数: " + str(len(client.calls)))
    print("  第 1 轮发的消息数: " + str(len(client.calls[0])))
    print("  第 2 轮发的消息数: " + str(len(client.calls[1])))
    for m in client.calls[1]:
        print("     [{:9}] {}".format(m.role, (m.content or "").replace("\n", " ")[:70]))

    check("最终回答来自第 2 轮", answer == "读完了，内容是 notes.txt。")
    check("模型被调用 2 次（工具轮 + 收尾轮）", len(client.calls) == 2)

    tm = tool_messages(client.calls[1])
    check("工具结果被回灌进第 2 轮请求", len(tm) == 1,
          "实际 " + str([m.content for m in tm]))
    check("tool 消息带 tool_call_id", bool(tm) and tm[0].tool_call_id == "call_1")
    check("tool 消息内容是工具的真实输出", bool(tm) and "notes.txt" in tm[0].content)

    with_calls = [m for m in client.calls[1] if m.role == "assistant" and m.tool_calls]
    check("assistant(tool_calls) 写进历史并与 tool 结果配对（不会被切散）",
          len(with_calls) == 1 and with_calls[0].tool_calls[0].name == "read_file")
    check("第 1 条永远是 system",
          client.calls[0][0].role == "system" and client.calls[1][0].role == "system")
    check("这一轮的工具定义（文本通道下发 None / 原生通道下发完整定义）",
          client.tools_seen[0] is None or isinstance(client.tools_seen[0], list))
    prompt_text = _SCHEMA_LOOP.build_system_prompt("STANDARD", str(work), "hi", False)
    native_text = _SCHEMA_LOOP.build_system_prompt("STANDARD", str(work), "hi", True)
    check("系统提示词里有工具清单（文本通道）",
          "## 可用工具（" in prompt_text and "- read_file(path*)" in prompt_text)
    check("清单里每个工具都带参数签名（带 * 的是必填）",
          "- head_tail_file(path*, lines)" in prompt_text
          and "- write_file(path*, content)" in prompt_text)
    check("系统提示词里有工具选择对照表", "别选错工具" in prompt_text)
    check("系统提示词里有上下文经济约束（有 context_window 工具才写）",
          "【上下文怎么用才省钱】" in prompt_text)
    check("原生通道不列清单（Qwen 模板自己渲染 # Tools，列了纯属重复烧 token）",
          "## 可用工具（" not in native_text and "## 可用工具\n" in native_text)
    check("原生通道要求把调用放在 tool_calls 里", "把调用放在 tool_calls 里返回" in native_text)
    check("历史里留下了 user/assistant/tool 三种消息",
          {getattr(m, "role", None) for m in history.get_history("s1")}
          >= {"user", "assistant", "tool"})

    kinds = [e["type"] for e in events.list_events("s1")]
    print("\n  事件序列:")
    for e in events.list_events("s1"):
        print("     {:20} {}".format(e["type"], e["summary"][:60]))
    for want in ("USER_MESSAGE", "MODEL_THINKING", "MODEL_RESPONSE", "TOOL_CALL_START",
                 "TOOL_CALL_COMPLETE"):
        check("事件被记录: " + want, want in kinds)
    check("完成时出了成功提示音", bool(client.sounds) and client.sounds[-1] == "DONE")

    # ---- 文本通道：模型把调用写在正文里 ----
    print("\n  --- 文本通道（模型把 <tool_call><function=...> 写在正文里）---")
    history2 = LocalConversationHistory()
    client2 = FakeChatClient([
        {"content": "<tool_call>\n<function=list_dir>\n<parameter=file_path>.</parameter>\n"
                    "</function>\n</tool_call>",
         "tool_calls": [], "finish_reason": "stop"},
        {"content": "目录里有一个文件。", "tool_calls": [], "finish_reason": "stop"},
    ])
    loop2 = AgentLoop(client=client2, registry=build_registry(work),
                      event_store=LocalEventStore(), history=history2, workspace=work)
    ans2 = loop2.process_message("s2", "列一下目录", "STANDARD", "low", "fake-model")
    tm2 = tool_messages(client2.calls[1])
    print("  最终回答: " + ans2)
    print("  回灌的 tool 结果: " + str([m.content for m in tm2]))
    check("文本通道：list_dir 被归一化成 list_directory 并真的执行了",
          len(tm2) == 1 and tm2[0].content == "目录内容：.",
          "实际 " + str([m.content for m in tm2]))
    check("文本通道：正文里的 tool_call 被剥掉，不当成回答",
          ans2 == "目录里有一个文件。")

    # ---- 未找到工具 + 建议 ----
    print("\n  --- 未找到工具：带上最接近的候选 ---")
    history3 = LocalConversationHistory()
    client3 = FakeChatClient([
        {"content": "", "tool_calls": [native_tool_call("c1", "file_read_all", {"path": "a"})],
         "finish_reason": "tool_calls"},
        {"content": "好，换一个工具。", "tool_calls": [], "finish_reason": "stop"},
    ])
    loop3 = AgentLoop(client=client3, registry=build_registry(work),
                      event_store=LocalEventStore(), history=history3, workspace=work)
    loop3.process_message("s3", "把文件都读一遍", "STANDARD", "low", "m")
    err = tool_messages(client3.calls[1])[0].content
    print("  回给模型的错误: " + err[:130])
    check("未找到工具时带上候选建议",
          err.startswith("错误: 未找到工具: file_read_all")
          and "你是不是想用这些之一" in err and "read_file" in err,
          err)

    # 连一个相近候选都没有时，给一句"看清单"的兜底说明
    history3b = LocalConversationHistory()
    client3b = FakeChatClient([
        {"content": "", "tool_calls": [native_tool_call("c1", "delete_directory_placeholder",
                                                        {"path": "tmp"})],
         "finish_reason": "tool_calls"},
        {"content": "好，换一个工具。", "tool_calls": [], "finish_reason": "stop"},
    ])
    loop3b = AgentLoop(client=client3b, registry=build_registry(work),
                       event_store=LocalEventStore(), history=history3b, workspace=work)
    loop3b.process_message("s3b", "删掉 tmp 目录", "STANDARD", "low", "m")
    err3b = tool_messages(client3b.calls[1])[0].content
    print("  自造工具名时的错误: " + err3b[:130])
    check("自造工具名的错误里必须带「未找到工具」+ 一句照做建议",
          "未找到工具: delete_directory_placeholder" in err3b
          and ("你是不是想用这些之一" in err3b or "可用工具见系统提示词里的清单" in err3b))

    # ---- 残缺调用 -> 纠正重试 ----
    print("\n  --- 残缺工具调用：纠正重试（上限 MAX_CALL_REPAIR = 2）---")
    history4 = LocalConversationHistory()
    events4 = LocalEventStore()
    client4 = FakeChatClient([
        {"content": "", "tool_calls": [], "finish_reason": "stop",
         "malformed_tool_call": True},
        {"content": "", "tool_calls": [], "finish_reason": "stop",
         "malformed_tool_call": True},
        {"content": "这次给结论。", "tool_calls": [], "finish_reason": "stop"},
    ])
    loop4 = AgentLoop(client=client4, registry=build_registry(work), event_store=events4,
                      history=history4, workspace=work)
    ans4 = loop4.process_message("s4", "干活", "STANDARD", "low", "m")
    print("  最终回答: " + ans4 + "；模型调用次数 " + str(len(client4.calls)))
    check("残缺调用被纠正重试（共 3 次模型调用）", len(client4.calls) == 3)
    check("纠正提示以「【系统提示】」+ user 角色插入",
          any(m.role == "user" and "你上一次的工具调用是**残缺的**" in m.content
              for m in client4.calls[1]))
    check("两次纠正后按正常收尾处理", ans4 == "这次给结论。")
    check("纠正事件被记录", len(events4.list_events("s4", "TOOL_CALL_ERROR")) == 2)

    # ---- 参数类型转换 ----
    print("\n  --- coerce_arguments：字符串 5 -> int 5 ---")
    coerced = _SCHEMA_LOOP.coerce_arguments(HeadTailTool(work), {"path": "x.txt", "lines": "5"})
    print("  " + json.dumps(coerced, ensure_ascii=False))
    check("lines '5' -> 5（int）", coerced["lines"] == 5 and isinstance(coerced["lines"], int))
    coerced2 = _SCHEMA_LOOP.coerce_arguments(MoveFileTool(work),
                                             {"src": "a.txt", "dest_path": "b.txt"})
    print("  " + json.dumps(coerced2, ensure_ascii=False))
    check("参数名归一化 src→source、dest_path→target",
          coerced2.get("source") == "a.txt" and coerced2.get("target") == "b.txt")

    # ---- 流式链路 ----
    print("\n  --- 流式链路（chat_stream 分片）---")
    history5 = LocalConversationHistory()
    events5 = LocalEventStore()
    stream = FakeStreamChatClient([
        [{"delta": {"content": "先看看。"}},
         {"tool_call_deltas": [{"index": 0, "id": "call_s1", "name": "read_",
                               "arguments": "{\"path\": "},
                              {"index": 0, "name": "file",
                               "arguments": "\"x.txt\"}"}]},
         {"finish_reason": "tool_calls"}],
        [{"delta": {"content": "看完了，x.txt 存在。"}}, {"finish_reason": "stop"}],
    ])
    loop5 = AgentLoop(client=stream, registry=build_registry(work), event_store=events5,
                      history=history5, workspace=work)
    chunks = list(loop5.process_message_stream("s5", "看看 x.txt", "STANDARD", "low", "m"))
    print("  流式块: " + str([c.to_dict() for c in chunks]))
    check("流式：文本增量被发出",
          any(c.type == "TEXT" and c.content == "先看看。" for c in chunks))
    check("流式：工具执行后发 TOOL_CALL 块",
          any(c.type == "TOOL_CALL" and c.tool_name == "read_file" for c in chunks))
    check("流式：最后一块是 DONE",
          chunks[-1].type == "DONE" and chunks[-1].content == "看完了，x.txt 存在。")
    check("流式：分片拼出的工具名 read_ + file = read_file，参数拼成合法 JSON",
          len(tool_messages(stream.calls[1])) == 1
          and "x.txt" in tool_messages(stream.calls[1])[0].content)
    check("流式：事件也被记录",
          "TOOL_CALL_COMPLETE" in [e["type"] for e in events5.list_events("s5")])

    # ---- 极简模式 ----
    print("\n  --- 极简模式：web_search 不在模式内 ---")
    history6 = LocalConversationHistory()
    client6 = FakeChatClient([
        {"content": "", "tool_calls": [native_tool_call("c1", "web_search", {"query": "x"})],
         "finish_reason": "tool_calls"},
        {"content": "不搜了。", "tool_calls": [], "finish_reason": "stop"},
    ])
    loop6 = AgentLoop(client=client6, registry=build_registry(work),
                      event_store=LocalEventStore(), history=history6, workspace=work)
    loop6.process_message("s6", "搜一下", "MINIMAL", "low", "m")
    err6 = tool_messages(client6.calls[1])[0].content
    print("  回给模型的错误: " + err6)
    check("极简模式拒绝模式外工具",
          "在 MINIMAL 模式下不可用" in err6 or "未找到工具" in err6)
    check("极简模式的提示词里列出了真实工具名",
          "本模式实际可用的工具**只有下面这些**" in client6.calls[0][0].content)
    check("极简模式不注入技能段（避免教模型调不存在的工具）",
          "激活的领域技能" not in client6.calls[0][0].content)


# ==========================================================================
# D. ToolCallGuard
# ==========================================================================


def run_guard() -> None:
    section("D. ToolCallGuard：只统计，不拦")
    g = ToolCallGuard()
    all_ok = True
    for i in range(1, 11):
        d = g.before_call("s1", "git_status", '{"path":"repo"}')
        if d.verdict != Verdict.OK or d.hint is not None:
            all_ok = False
            print("  第 {} 次被拦了: {} / {}".format(i, d.verdict, d.hint))
    check("同一调用连问 10 次都放行（不再跳过、不再终止任务）", all_ok)
    check("重复次数照常统计（第 10 次 = 10）",
          g.repeat_count("s1", "git_status", '{"path":"repo"}') == 10)

    for _ in range(10):
        g.after_call("s1", "number_convert", False)
    dec = g.before_call("s1", "number_convert", '{"v":7}')
    check("连续失败 10 次后仍然放行",
          dec.verdict == Verdict.OK and dec.hint is None)
    check("连续失败次数照常统计（10）", g.failure_count("s1", "number_convert") == 10)
    g.after_call("s1", "number_convert", True)
    check("成功一次就把连续失败清零", g.failure_count("s1", "number_convert") == 0)
    g.reset("s1")
    check("reset 清掉本会话计数", g.failure_count("s1", "number_convert") == 0)
    check("历史常量保留（3 / 5 / 6 / 3）",
          (ToolCallGuard.REPEAT_SKIP_AT, ToolCallGuard.REPEAT_ABORT_AT,
           ToolCallGuard.FAIL_SKIP_AT, ToolCallGuard.FAIL_WARN_AT) == (3, 5, 6, 3))


# ==========================================================================
# E. 上下文预算与压缩
# ==========================================================================


def run_context() -> None:
    section("E. ContextCompressor / ContextBudget")

    budget = ContextBudget(16384)
    check("默认窗口 = 16384", budget.default_limit() == 16384)
    check("会话默认用全局值", budget.limit_for("s1") == 16384)
    budget.set("s1", 32768)
    check("会话覆盖生效", budget.limit_for("s1") == 32768 and budget.is_overridden("s1"))
    budget.set("s1", 16384)
    check("调回默认值等于没调过", not budget.is_overridden("s1"))
    budget.set("s2", 0)
    check("0 = 不设限", budget.limit_for("s2") == 0)
    print("  快照: " + json.dumps(budget.snapshot("s2"), ensure_ascii=False))
    check("快照键名与 Java 一致",
          set(budget.snapshot("s2").keys()) == {"defaultLimit", "sessionLimit", "overridden"})

    check("estimate_text_tokens 中文 1 字 1 token",
          ContextCompressor.estimate_text_tokens("你好") == 2)
    check("estimate_text_tokens 纯 ASCII 按 3.5 字符/token",
          ContextCompressor.estimate_text_tokens("a" * 35) == 10)

    messages: list[ChatMessage__agent_loop] = [ChatMessage__agent_loop.system("你是助手。")]
    for i in range(20):
        messages.append(ChatMessage__agent_loop.user("第 {} 步：读一下文件 f{}.txt，我关心端口号 {}。"
                                         .format(i, i, i)))
        messages.append(ChatMessage__agent_loop.assistant_with_tool_calls(
            "", [ToolCall__agent_loop("call{}".format(i), "read_file", {"path": "f{}.txt".format(i)})]))
        messages.append(ChatMessage__agent_loop.tool_result("call{}".format(i), "内容" * 400 + " 端口 8788"))
    messages.append(ChatMessage__agent_loop.user("总结一下"))

    before = ContextCompressor.estimate_tokens(messages)
    print("\n  压缩前：{} 条消息，约 {} token".format(len(messages), before))
    r = ContextCompressor.fit(list(messages), 2000, 8)
    print("  压缩后：{} 条，约 {} token，折叠 {} 条"
          .format(len(r.messages), r.tokens_after, r.dropped_messages))
    check("压缩后必须进预算（2000）", r.compressed and r.tokens_after <= 2000,
          "实际 " + str(r.tokens_after))
    check("system 消息必须在最前", bool(r.messages) and r.messages[0].role == "system")

    orphan = None
    for i, m in enumerate(r.messages):
        if m.role != "tool":
            continue
        prev = r.messages[i - 1] if i > 0 else None
        matched = (prev is not None and prev.role == "assistant" and prev.tool_calls
                   and any(tc.id == m.tool_call_id for tc in prev.tool_calls))
        if not matched:
            orphan = m
            break
    check("工具结果不能与它的调用被切散（无孤儿 tool 消息）", orphan is None,
          "孤儿: " + repr(orphan))

    digest_msg = [m for m in r.messages if "早前对话摘要" in (m.content or "")]
    print("  摘要首行: " + (digest_msg[0].content.split("\n")[0][:95] if digest_msg else "(无)"))
    check("摘要里保留了用户说过的话",
          bool(digest_msg) and "用户说" in digest_msg[0].content)
    check("摘要用 user 角色（Qwen 模板不允许夹在中间的 system）",
          bool(digest_msg) and digest_msg[0].role == "user")

    small = list(messages[:3])
    none = ContextCompressor.fit(small, 100000, 8)
    check("没超预算时原样返回、不复制不改动",
          (not none.compressed) and none.messages is small)

    tiny = ContextCompressor.fit(list(messages), 300, 16)
    print("  极小预算（300）：{} -> {} token".format(before, tiny.tokens_after))
    check("极小预算下也要收敛", tiny.compressed and tiny.tokens_after < before / 4)

    trimmed = ContextCompressor.trim_tool_result(ChatMessage__agent_loop.tool_result("c1", "x" * 20000))
    check("超长工具结果被就地截断（保留头部 + 说明）",
          len(trimmed.content) < 20000 and "结果过长已截断" in trimmed.content)

    events = LocalEventStore()
    loop = AgentLoop(client=FakeChatClient([]), registry=build_registry(Path(".")),
                     event_store=events, history=LocalConversationHistory(),
                     budget=ContextBudget(16384), use_native_tools="prompt")
    loop.context_budget.set("big", 1000)
    loop.maybe_compress_context("big", list(messages), "m")
    check("超预算时发出 CONTEXT_COMPRESSED 事件",
          len(events.list_events("big", "CONTEXT_COMPRESSED")) == 1)
    check("预算顺序：会话覆盖优先于全局默认",
          loop.effective_context_limit("m", "big") == 1000)
    check("会话没调过 -> 用全局默认 16384",
          loop.effective_context_limit("m", "none") == 16384)
    loop.context_budget.set("zero", 0)
    check("会话设为 0 = 不设限，此时不走全局默认（落到模型窗口 75% 那条路）",
          loop.context_budget.limit_for("zero") == 0
          and loop.effective_context_limit("m", "zero") == 24576)


# ==========================================================================
# F. ApprovalPolicy
# ==========================================================================


def run_approval() -> None:
    section("F. ApprovalPolicy")
    p = ApprovalPolicy()
    check("只读工具默认自动批准",
          p.check_approval("tool.file.read").action == ApprovalAction.AUTO_APPROVE
          and p.check_approval("tool.file.read").reason is None)
    check("未登记的工具也自动批准（开箱即用）",
          p.check_approval("tool.file.write").action == ApprovalAction.AUTO_APPROVE)
    check("默认自动批准清单与 Java 一致（32 个）",
          len(p.snapshot()["autoApprove"]) == 32)

    p.set_tool_policy("tool.file.write", ToolPolicy.CONFIRM)
    res = p.check_approval("tool.file.write")
    print("  CONFIRM 理由: " + str(res.reason))
    check("设为 CONFIRM 后返回需要确认",
          res.action == ApprovalAction.CONFIRM
          and res.reason == "工具需要用户确认: tool.file.write"
                            "（请在设置中将其改为自动批准，或保持禁止）")
    check("get_policy 保持一致", p.get_policy("tool.file.write") == ToolPolicy.CONFIRM)

    p.set_tool_policy("tool.file.write", ToolPolicy.BLOCK)
    res = p.check_approval("tool.file.write")
    print("  BLOCK 理由: " + str(res.reason))
    check("设为 BLOCK 后返回禁止执行",
          res.action == ApprovalAction.BLOCK
          and res.reason == "工具已被禁止: tool.file.write")
    check("一次原子替换：CONFIRM 集合里已经不剩它了",
          "tool.file.write" not in p.snapshot()["confirm"])

    p.set_tool_policy("tool.file.write", ToolPolicy.AUTO_APPROVE)
    check("改回自动批准",
          p.check_approval("tool.file.write").action == ApprovalAction.AUTO_APPROVE)
    print("  批量策略: " + json.dumps(
        p.get_policies([ReadFileTool(Path(".")), WriteFileTool(Path("."))]),
        ensure_ascii=False))


# ==========================================================================
# G. ChangeReview
# ==========================================================================


def cid_of(gate: Any) -> str:
    return gate.content.split("编号：")[1].split("\n")[0].strip()


def run_change_review(work: Path) -> None:
    section("G. ChangeReview：改文件先待审，点通过才落盘")

    target = work / "review" / "sample.txt"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("line1\nline2\nline3\n", encoding="utf-8")

    history = LocalConversationHistory()
    review = ChangeReview(history=history)
    check("默认开着（用户要的就是先审后用）", review.enabled() is True)

    gate = review.intercept("write_file", str(target), "line1\nline2\nline3\n",
                            "line1\nCHANGED\nline3\n", session_id="s9")
    print("\n  闸门返回给模型的话:")
    for line in (gate.content if gate else "(None)").split("\n"):
        print("    " + line)
    check("闸门拦下来了（返回 ToolResult，不落盘）", gate is not None and gate.success)
    check("**文件还没被改**", target.read_text(encoding="utf-8") == "line1\nline2\nline3\n")

    pending = review.list("s9", False)
    check("待审列表里有 1 条", len(pending) == 1)
    c = pending[0]
    print("\n  diff:")
    for line in c.diff.split("\n"):
        print("    " + line)
    check("diff 里能看到 - 和 + 两行", "-line2" in c.diff and "+CHANGED" in c.diff)
    print("  summary: " + json.dumps(c.summary(), ensure_ascii=False)[:230])
    check("summary 键名与 Java 一致",
          set(c.summary().keys()) == {"id", "sessionId", "toolName", "path", "existed",
                                      "status", "createdAt", "diff", "addedLines",
                                      "removedLines"})
    check("status = PENDING", c.status == PENDING)

    stats = review.stats("s9")
    check("stats 结构对齐（enabled/pendingCount/pending）",
          set(stats.keys()) == {"enabled", "pendingCount", "pending"}
          and stats["pendingCount"] == 1)

    done = review.approve(c.id)
    print("\n  通过后文件内容: " + repr(target.read_text(encoding="utf-8")))
    check("点通过才真落盘", target.read_text(encoding="utf-8") == "line1\nCHANGED\nline3\n")
    check("状态变 APPROVED", done.status == APPROVED)
    notes = [m for m in history.get_history("s9") if m.role == "system"]
    print("  写回会话的结论: " + (notes[-1].content if notes else "(无)"))
    check("通过结论写回会话（system 消息，AgentLoop 会降级成 user 发给模型）",
          bool(notes) and "已通过" in notes[-1].content)
    try:
        review.approve(c.id)
        check("同一条不能批两次", False)
    except RuntimeError as e:
        check("同一条不能批两次", "已经处理过了" in str(e))

    gate2 = review.intercept("modify_file", str(target), "line1\nCHANGED\nline3\n",
                             "line1\nREJECTED_ME\nline3\n", session_id="s9")
    rejected = review.reject(cid_of(gate2), "变量名不符合规范")
    check("打回不落盘",
          target.read_text(encoding="utf-8") == "line1\nCHANGED\nline3\n"
          and rejected.status == REJECTED)
    notes = [m for m in history.get_history("s9") if m.role == "system"]
    print("  打回结论: " + notes[-1].content.replace("\n", " "))
    check("打回理由回给模型", "打回理由：变量名不符合规范" in notes[-1].content)
    check("列表默认只给待审（打回的不在里面）",
          all(x.status == PENDING for x in review.list("s9", False)))
    check("include_decided=True 能回看", len(review.list("s9", True)) == 2)

    gate3 = review.intercept("write_file", str(target), "line1\nCHANGED\nline3\n",
                             "line1\nMINE\nline3\n", session_id="s9")
    cid3 = cid_of(gate3)
    target.write_text("line1\nSOMEONE_ELSE\nline3\n", encoding="utf-8")
    try:
        review.approve(cid3)
        check("提交后被别人改过 -> 取消写入", False)
    except RuntimeError as e:
        print("\n  冲突报错: " + str(e))
        check("提交后被别人改过 -> 取消写入",
              "被改动过" in str(e)
              and target.read_text(encoding="utf-8") == "line1\nSOMEONE_ELSE\nline3\n")

    d = work / "review" / "deldir"
    (d / "sub").mkdir(parents=True, exist_ok=True)
    (d / "sub" / "a.txt").write_text("x", encoding="utf-8")
    gate4 = review.intercept("delete_file", str(d), "(目录)", None, session_id="s9")
    check("删除目录也要先待审", d.exists())
    review.approve(cid_of(gate4))
    check("通过后目录被递归删除（不会卡在「目录不是空的」）", not d.exists())

    crlf = work / "review" / "win.bat"
    crlf.write_bytes("a\r\nb\r\nc\r\n".encode("utf-8"))
    # modify_file 登记的旧内容是 readTextLines 之后用 "\n" 拼回来的（\r 已剥、尾行已去），
    # 新内容同理；所以期望值末尾没有换行 —— 与 Java 的 comparable/写入口径一致
    gate5 = review.intercept("modify_file", str(crlf), "a\nb\nc", "a\nB\nc", session_id="s9")
    review.approve(cid_of(gate5))
    check("CRLF 文件审核通过后仍然全是 CRLF（不会整体变成 LF）",
          crlf.read_bytes() == b"a\r\nB\r\nc", repr(crlf.read_bytes()))

    gbk = work / "review" / "gbk.txt"
    gbk.write_bytes("中文一\n中文二\n".encode("gbk"))
    gate6 = review.intercept("write_file", str(gbk), "中文一\n中文二\n",
                             "中文一改\n中文二\n", session_id="s9")
    review.approve(cid_of(gate6))
    check("GBK 文件审核通过后仍是 GBK（严格解码判定）",
          gbk.read_bytes().decode("gbk") == "中文一改\n中文二\n", repr(gbk.read_bytes()))

    class OffSettings:
        def is_enabled(self, plugin_id, default):
            return False

    review_off = ChangeReview(history=LocalConversationHistory(), settings=OffSettings())
    check("设置里关掉开关 -> 不再拦（直接落盘）",
          review_off.enabled() is False
          and review_off.intercept("write_file", str(target), "x", "y") is None)
    check("PLUGIN_ID 与 Java 一致", ChangeReview.PLUGIN_ID == "plugin.change-review")

    r2 = ChangeReview(history=LocalConversationHistory())
    for i in range(260):
        r2.submit("sx", "write_file", "f{}.txt".format(i), None, "c{}".format(i))
    check("每会话上限 200 条（全是待审时也要丢最老的）", len(r2.list("sx", True)) == 200,
          "实际 " + str(len(r2.list("sx", True))))

    check("Diff：内容没变", "内容没有变化" in Diff.render("a.txt", "same", "same"))
    check("Diff：新建", Diff.render("a.txt", None, "x\ny").startswith("新建文件：a.txt"))
    check("Diff：删除", Diff.render("a.txt", "x\ny", None).startswith("删除文件：a.txt"))
    huge = "\n".join(str(i) for i in range(4001))
    check("Diff：超大文件退化成整文件替换摘要",
          "整文件替换" in Diff.render("big.txt", huge, huge + "\nextra"))
    check("Diff：400 行上限截断",
          "已截断" in Diff.render("m.txt", "\n".join("a" for _ in range(600)),
                                  "\n".join("b" for _ in range(600))))
    check("PendingChange.removedLines 语义（尾部换行算一行）",
          PendingChange("C1", "s", "t", "p", True, "a\nb\n", "a", "", 0, PENDING,
                        None).summary()["removedLines"] == 3)


# ==========================================================================
# main
# ==========================================================================


def main__agent__verify() -> int:
    work = Path(tempfile.mkdtemp(prefix="lionbox-agent-verify-"))
    print("临时工作区: " + str(work))
    try:
        run_parser_samples()
        run_alias_tables()
        run_main_loop(work)
        run_guard()
        run_context()
        run_approval()
        run_change_review(work)
    finally:
        shutil.rmtree(work, ignore_errors=True)

    section("汇总")
    print("通过 {} 项，失败 {} 项".format(PASS, FAIL))
    return 1 if FAIL else 0


if __name__ == "__lionbox_inlined__":  # 内联后不再作为入口
    sys.exit(main__agent__verify())


# ========================================================================
# 原模块 lionbox/agent/_verify_integration.py
# ========================================================================
"""端到端接线自验：`AgentLoop` + **真实的** `lionbox.sessions` / `lionbox.events`。

`_verify.py` 用的是内存桩（保证 agent 包自己永远能跑）；这个脚本用并行施工的
邻座模块的真实类型跑一遍，确认"窄接口"真的对得上：

    python -m lionbox.agent._verify_integration

注意：`lionbox/sessions/`、`lionbox/events/` 由别的同事负责，**还在变**。
这个脚本只做只读式的对接验证，不修改它们的任何文件；它们改了形状这里会先红。
"""


import shutil
import sys
import tempfile
from pathlib import Path

# 注意：`_verify` 在 import 时已经把 stdout 换成 UTF-8 包装了，
# 这里**不能**再包一次 —— 前一个包装对象被 GC 时会连带关掉底层 buffer。


def main__agent__verify_integration() -> int:
    section("H. 接线自验：AgentLoop + lionbox.sessions.ConversationHistory + lionbox.events.EventStore")

    try:
        from lionbox.sessions.history import ConversationHistory
        from lionbox.sessions.message import ConversationMessage
    except Exception as e:      # noqa: BLE001
        print("  [SKIP] lionbox.sessions 还不可用：" + repr(e))
        return 0
    try:
        from lionbox.events.store import EventStore
        from lionbox.events.model import EventType
    except Exception as e:      # noqa: BLE001
        print("  [SKIP] lionbox.events 还不可用：" + repr(e))
        return 0

    work = Path(tempfile.mkdtemp(prefix="lionbox-agent-it-"))
    try:
        history = ConversationHistory(history_dir=work / "conversations")
        events = EventStore(work / "events", auto_migrate_legacy=False)

        client = FakeChatClient([
            {"content": "先读文件。",
             "tool_calls": [native_tool_call("call_1", "read_file", {"path": "a.txt"})],
             "finish_reason": "tool_calls"},
            {"content": "读完了。", "tool_calls": [], "finish_reason": "stop"},
        ])
        loop = AgentLoop(client=client, registry=build_registry(work), event_store=events,
                         history=history, workspace=work)
        answer = loop.process_message("it-1", "读 a.txt", "STANDARD", "low", "m")
        print("  最终回答: " + answer)

        check("真实 ConversationHistory：add_message 收的是消息对象（我们适配到了）",
              loop._history_takes_object is True)
        msgs = history.get_history("it-1")
        print("  历史条数: " + str(len(msgs))
              + "；类型: " + type(msgs[0]).__name__ if msgs else "  历史为空")
        check("历史里落了 4 条（user / assistant(tool_calls) / tool / assistant）",
              len(msgs) == 4, "实际 " + str(len(msgs)))
        check("历史里第一条是真实的 ConversationMessage",
              bool(msgs) and isinstance(msgs[0], ConversationMessage))
        check("assistant 消息带 toolCalls（配得上后面的 tool 结果）",
              any(m.role == "assistant" and m.tool_calls for m in msgs))
        check("tool 消息带 toolCallId / toolName",
              any(m.role == "tool" and m.tool_call_id == "call_1"
                  and m.tool_name == "read_file" for m in msgs))
        check("历史落盘了（sessions 自己负责写盘）",
              (work / "conversations" / "it-1.json").is_file())

        evs = events.get_session_events("it-1")
        kinds = [getattr(e, "type", None) for e in evs]
        print("  事件类型: " + str(kinds))
        for want in (EventType.USER_MESSAGE, EventType.TOOL_CALL_START,
                     EventType.TOOL_CALL_COMPLETE):
            check("真实 EventStore 收到 " + want, want in kinds)

        # 第二轮：历史里的消息能被 build_messages 正确还原（含 tool 配对）
        rebuilt = loop.build_messages("it-1", "STANDARD", "读 a.txt")
        roles = [m.role for m in rebuilt]
        print("  build_messages 还原的角色序列: " + str(roles))
        check("还原出 system + user + assistant(tool_calls) + tool + assistant（收尾轮）",
              roles == ["system", "user", "assistant", "tool", "assistant"],
              "实际 " + str(roles))
        check("assistant 的工具调用被还原",
              rebuilt[2].tool_calls and rebuilt[2].tool_calls[0].name == "read_file")
        check("tool 结果带 tool_call_id 且内容是真实工具输出",
              rebuilt[3].tool_call_id == "call_1" and "a.txt" in rebuilt[3].content)

        # 历史里的 system 消息不在开头 -> 必须降级成 user（Qwen 模板会 500）
        history.add_message(ConversationMessage.system("it-1", "【人工审核】改动已通过"))
        rebuilt2 = loop.build_messages("it-1", "STANDARD", "读 a.txt")
        check("中途的 system 被降级成 user 且带【系统提示】前缀",
              rebuilt2[-1].role == "user" and rebuilt2[-1].content.startswith("【系统提示】"),
              rebuilt2[-1].role + " / " + rebuilt2[-1].content[:30])

        # ---- 直接把 lionbox/llm 的 ModelAdapter 当 client 用 ----
        from lionbox.llm.types import AdapterType, ChatMessage as LLMChatMessage, ModelChunk, ModelInfo, ModelResponse as LLMResponse, ThinkingLevel as LLMThinkingLevel, ToolCall as LLMToolCall
        try:
            from lionbox.llm.base import ModelAdapter
        except Exception as e:      # noqa: BLE001
            print("  [SKIP] lionbox.llm 适配器基类不可用：" + repr(e))
            return 0

        class ScriptedAdapter(ModelAdapter):
            """最小适配器替身：只实现接口，验证 AgentLoop 能直接接 `llm.ModelAdapter`。"""

            def __init__(self, script):
                self.script = list(script)
                self.seen_max_tokens = []

            @property
            def name(self):
                return "scripted"

            @property
            def adapter_type(self):
                return AdapterType.OPENAI_COMPATIBLE

            def available_models(self):
                return [ModelInfo(id="m", name="m", owner="x", supports_thinking=False,
                                  supports_tool_calls=True, max_context_tokens=262144)]

            def is_available(self):
                return True

            def update_config(self, config):
                return None

            def _next(self):
                return self.script.pop(0)

            def chat(self, messages, model, thinking_level=None, tools=None):
                return self._next()

            def chat_with_options(self, messages, model, thinking_level=None, tools=None,
                                  extra_body=None, max_tokens=None):
                self.seen_max_tokens.append(max_tokens)
                return self._next()

            def chat_stream(self, messages, model, thinking_level=None, tools=None):
                yield from self._next()

            def chat_stream_limited(self, messages, model, thinking_level=None, tools=None,
                                    max_tokens=None):
                self.seen_max_tokens.append(max_tokens)
                yield from self._next()

        adapter = ScriptedAdapter([
            LLMResponse(content="查一下。",
                        tool_calls=[LLMToolCall(id="call_a", name="read_file",
                                                arguments={"path": "b.txt"})],
                        finish_reason="tool_calls"),
            LLMResponse(content="查完了。", finish_reason="stop"),
        ])
        client = FakeChatClient([])
        loop2 = AgentLoop(client=adapter, registry=build_registry(work), event_store=events,
                          history=ConversationHistory(history_dir=work / "conversations2"),
                          workspace=work)
        answer2 = loop2.process_message("it-2", "读 b.txt", "STANDARD", "low", "m")
        print("  用真实 ModelAdapter 的最终回答: " + answer2)
        check("AgentLoop 能直接接 lionbox.llm.ModelAdapter", answer2 == "查完了。")
        check("走的是 chat_with_options（带 max_tokens，与 Java 一致）",
              adapter.seen_max_tokens == [None] or all(
                  v is None or isinstance(v, int) for v in adapter.seen_max_tokens),
              str(adapter.seen_max_tokens))
        check("ModelResponse.tool_calls 被正确读出来并执行了",
              loop2._history_items("it-2")[2].tool_name == "read_file")

        # 流式：ModelChunk 形状
        adapter2 = ScriptedAdapter([
            [ModelChunk(delta_content="先看看。"),
             ModelChunk(tool_call_deltas=[_delta(0, "call_b", "read_", "{\"path\": "),
                                          _delta(0, None, "file", "\"c.txt\"}")],
                        finish_reason="tool_calls")],
            [ModelChunk(delta_content="看完了。", finish_reason="stop")],
        ])
        loop3 = AgentLoop(client=adapter2, registry=build_registry(work), event_store=events,
                          history=ConversationHistory(history_dir=work / "conversations3"),
                          workspace=work)
        chunks = list(loop3.process_message_stream("it-3", "看 c.txt", "STANDARD", "low", "m"))
        print("  流式块: " + str([c.to_dict() for c in chunks]))
        check("ModelChunk 流式：文本 + 工具分片 + DONE 都出来了",
              chunks[-1].type == "DONE" and chunks[-1].content == "看完了。"
              and any(c.type == "TOOL_CALL" and c.tool_name == "read_file" for c in chunks))
        check("流式分片拼出的参数能落到工具里",
              any(m.role == "tool" and "c.txt" in (m.content or "")
                  for m in loop3._history_items("it-3")))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    return 0


def _delta(index, call_id, name, arguments):
    from lionbox.llm.types import ToolCallDelta
    return ToolCallDelta(index=index, id=call_id, name_delta=name, arguments_delta=arguments)


if __name__ == "__lionbox_inlined__":  # 内联后不再作为入口
    sys.exit(main__agent__verify_integration())


# ========================================================================
# 原模块 lionbox/queue.py
# ========================================================================
"""会话消息队列：同会话串行、不同会话互不阻塞。

对应 Java `com.lioncode.queue` 包（257 行）：

    MessageQueue      → message_queue.MessageQueue       （按会话隔离的优先级队列）
    SessionDispatcher → dispatcher.SessionDispatcher     （每会话一个 Worker 串行消费）
"""



__all__ = [
    "DEFAULT_CAPACITY", "IDLE_TIMEOUT_SECONDS", "IllegalStateError", "MessageQueue",
    "QueuedMessage", "SessionDispatcher",
]


# ========================================================================
# 原模块 lionbox/queue/dispatcher.py
# ========================================================================
"""会话消息调度器 —— 对应 Java `com.lioncode.queue.SessionDispatcher`（177 行）。

核心职责（Java 注释里强调过的那条）：
**同一会话串行、不同会话互不阻塞。**
每个会话同一时刻只有一个 Worker 在处理，彻底解决"两个请求同时打一个会话
搞乱对话历史"的并发问题；而不同会话各跑各的，一个会话在等模型不会挡住另一个。

- 消费 `MessageQueue`：FIFO + Steer 插队（Steer 先中断当前任务再插队）
- 结果通过 future 回填给 HTTP 请求线程
- 流式接口用 `try_acquire_stream` 与会话队列互斥（不能一边排队一边流式写历史）

【实现选择】Java 用 `Executors.newCachedThreadPool`（每会话一个临时 Worker、空闲自动退出）。
这里用 `threading.Thread(daemon=True)` 起同样的"临时 Worker"：空闲 30 秒自动退出，
下次提交再起。线程比线程池对象更轻，也免了池的关闭顺序问题。
"""


import logging
import threading
from concurrent.futures import Future
from typing import Any, Protocol

from lionbox.plugins.base import AgentMode

log__queue_dispatcher = logging.getLogger("lionbox.queue.dispatcher")

IDLE_TIMEOUT_SECONDS = 30.0


class AgentLoopLike(Protocol):
    """`lionbox.agent.loop.AgentLoop` 的形状（并行任务提供，这里只约定调用签名）。"""

    def process_message(self, session_id: str, message: str, mode: str,
                        thinking_level: Any, model: str | None) -> str | None: ...


class AgentControlLike(Protocol):
    """`lionbox.agent` 的运行控制（暂停/继续/停止）；由 api 层注入同一个实例。"""

    def stop(self, session_id: str) -> None: ...


class SessionDispatcher:
    def __init__(self, message_queue: MessageQueue, agent_loop: AgentLoopLike,
                 agent_control: AgentControlLike | None = None,
                 session_manager: Any = None) -> None:
        self.message_queue = message_queue
        self.agent_loop = agent_loop
        self.agent_control = agent_control
        self.session_manager = session_manager

        # 正在处理的会话集合（保证每会话单 Worker）
        self._active_sessions: set[str] = set()
        # 流式处理占用的会话（流式接口不与队列混跑，但需互斥）
        self._streaming_sessions: set[str] = set()
        self._lock = threading.RLock()

    # ------------------------------------------------------------ 提交
    def submit(self, session_id: str, user_message: str, model: str | None = None,
               thinking_level: Any = None, steer: bool = False) -> "Future[str]":
        """提交消息并返回结果 future（同步 HTTP 接口等它）。

        `steer=True`：插队模式 —— 先中断当前任务（该任务会以"已停止"回复它的调用方），
        本消息以最高优先级插到队首。
        """
        if steer:
            log__queue_dispatcher.info("Steer插队: 中断会话 %s 当前任务", session_id)
            if self.agent_control is not None:
                self.agent_control.stop(session_id)
        level_name = _level_name(thinking_level)
        message = self.message_queue.submit(
            session_id, user_message, 100 if steer else 0, steer, model, level_name)
        # 队列满被拒时 future 已经带着异常完成了，不必再起一个只会空转 30 秒的 worker
        if not message.future.done():
            self._start_worker(session_id)
        return message.future

    # ------------------------------------------------------------ 状态
    def is_busy(self, session_id: str) -> bool:
        with self._lock:
            if session_id in self._active_sessions or session_id in self._streaming_sessions:
                return True
        return self.message_queue.pending_count(session_id) > 0

    def try_acquire_stream(self, session_id: str) -> bool:
        """流式接口占用会话（与队列处理互斥）。忙时返回 False，调用方回"会话正忙"。"""
        with self._lock:
            if self.is_busy(session_id):
                return False
            self._streaming_sessions.add(session_id)
            return True

    def release_stream(self, session_id: str) -> None:
        with self._lock:
            self._streaming_sessions.discard(session_id)

    # ------------------------------------------------------------ Worker
    def _start_worker(self, session_id: str) -> None:
        with self._lock:
            if session_id in self._active_sessions:
                return          # 已有 Worker 在处理该会话
            self._active_sessions.add(session_id)
        threading.Thread(target=self._worker_entry, args=(session_id,),
                         name="lion-session-worker", daemon=True).start()

    def _worker_entry(self, session_id: str) -> None:
        try:
            self._drain(session_id)
        finally:
            with self._lock:
                self._active_sessions.discard(session_id)
            # 退出前复查：期间可能又有新消息入队
            if self.message_queue.pending_count(session_id) > 0:
                self._start_worker(session_id)

    def _drain(self, session_id: str) -> None:
        """Worker 主循环：逐条消费该会话队列，空闲 30 秒自动退出。"""
        while True:
            message = self.message_queue.poll(session_id, IDLE_TIMEOUT_SECONDS)
            if message is None:
                return          # 队列空闲，退出 Worker
            try:
                self._handle(session_id, message)
            except BaseException as t:   # noqa: BLE001
                # 【必须捕获 BaseException，不能只 catch Exception】Java 侧注释说明了原因：
                # 只抓 Exception 时，一旦冒出 Error（最典型的是 OOM，长任务很容易撞），
                # future **永远不会完成** —— 那条 HTTP 请求一直挂着，用户点"继续"也没用。
                log__queue_dispatcher.error("消息处理失败: %s (会话: %s)", message.id, session_id, exc_info=True)
                if not message.future.done():
                    message.future.set_exception(
                        t if isinstance(t, Exception) else RuntimeError(str(t)))

    def _handle(self, session_id: str, message: QueuedMessage) -> None:
        # 处理时取会话当前生效模式（运行期间可能被切换）
        mode = self._effective_mode(session_id)
        level = _parse_level__queue_dispatcher(message.thinking_level)
        result = self.agent_loop.process_message(session_id, message.content, mode, level,
                                                 message.model)
        if not message.future.done():
            # 归一化 None：future 回 None 会让 ChatController 把它塞进响应体，
            # 前端拿到 null 显示空白
            message.future.set_result("" if result is None else result)

    def _effective_mode(self, session_id: str) -> str:
        manager = self.session_manager
        if manager is not None:
            getter = getattr(manager, "get_effective_mode", None)
            if callable(getter):
                try:
                    return AgentMode.normalize(getter(session_id))
                except Exception:
                    log__queue_dispatcher.warning("取会话生效模式失败，回落标准模式: %s", session_id, exc_info=True)
        return AgentMode.STANDARD

    # ------------------------------------------------------------ 关闭
    def shutdown(self) -> None:
        """对应 Java 的 `@PreDestroy`：Worker 都是 daemon 线程，这里只做标记。"""
        with self._lock:
            self._active_sessions.clear()
            self._streaming_sessions.clear()


def _level_name(thinking_level: Any) -> str:
    """Java: `thinkingLevel != null ? thinkingLevel.name() : "MEDIUM"`。"""
    if thinking_level is None:
        return "MEDIUM"
    name = getattr(thinking_level, "name", None)
    if isinstance(name, str):
        return name
    return str(thinking_level)


def _parse_level__queue_dispatcher(name: Any) -> Any:
    """把队列里的等级名解析回 ThinkingLevel；认不出来回落 MEDIUM（Java 同）。"""
    from lionbox.llm.types import ThinkingLevel
    return ThinkingLevel.parse(name, ThinkingLevel.MEDIUM)


# ========================================================================
# 原模块 lionbox/queue/message_queue.py
# ========================================================================
"""消息队列 —— 对应 Java `com.lioncode.queue.MessageQueue`（132 行）。

每个会话一条**优先级**队列，由 `SessionDispatcher` 串行消费：

- 同会话消息严格 FIFO —— 保证对话历史不会被并发写乱
- Steer（用户插队指令）优先级最高：先中断当前任务再插到队首
- 消息携带 future，处理完成后回填结果给 HTTP 请求线程

【容量保护】`lion.queue.capacity`（出厂 1000）在 Java 版里曾经"配置写了但没人读"，
PriorityBlockingQueue 实际上是"初始容量 64、无上限"，客户端循环 POST /api/chat
就能把消息无限堆在堆里直到 OOM。这里真正把它接上：达到上限时拒绝**普通**消息
（返回一个已失败的 future），Steer 不受限制 —— 它本来就是用来救场的。
"""


import itertools
import queue as _queue
import threading
from concurrent.futures import Future
from dataclasses import dataclass, field
from typing import Any

DEFAULT_CAPACITY = 1000


@dataclass
class QueuedMessage:
    """队列消息。`id` 形如 `msg_12`，同优先级按入队序号 FIFO。"""

    id: str
    session_id: str
    content: str
    priority: int
    is_steer: bool
    model: str | None
    thinking_level: str
    future: "Future[str]" = field(default_factory=Future)

    @property
    def seq(self) -> int:
        """从 id 里抠出全局序号（`msg_12` → 12）；解析失败按 0 处理（Java 同）。"""
        try:
            return int(self.id[4:])
        except (ValueError, TypeError):
            return 0


class MessageQueue:
    """按会话隔离的优先级消息队列。"""

    def __init__(self, capacity: int = DEFAULT_CAPACITY) -> None:
        self.capacity = int(capacity)
        self._queues: dict[str, "_queue.PriorityQueue[tuple[int, int, QueuedMessage]]"] = {}
        self._sequence = itertools.count(1)
        # 【必须是 RLock】submit() 持锁期间会调用 _queue_of()，它也要拿同一把锁；
        # 用普通 Lock 会在这里自锁死（HTTP 线程直接挂住，表现为接口不返回）。
        self._lock = threading.RLock()

    # ------------------------------------------------------------ 提交
    def submit(self, session_id: str, content: str, priority: int = 0,
               is_steer: bool = False, model: str | None = None,
               thinking_level: str = "MEDIUM") -> QueuedMessage:
        """提交消息。

        队列满时**只拦普通消息**：返回一个已经带着异常的 future（调用方 await 时
        立刻拿到"会话待处理消息过多"，而不是空等 30 秒）。
        """
        with self._lock:
            message_id = f"msg_{next(self._sequence)}"
            q = self._queue_of(session_id)
            if not is_steer and self.capacity > 0 and q.qsize() >= self.capacity:
                rejected = QueuedMessage(message_id, session_id, content, priority,
                                         is_steer, model, thinking_level, Future())
                rejected.future.set_exception(IllegalStateError__queue_message_queue(
                    f"会话待处理消息过多（上限 {self.capacity} 条），请等当前任务跑完再发"))
                return rejected

            message = QueuedMessage(message_id, session_id, content, priority, is_steer,
                                    model, thinking_level, Future())
            # 优先级高的在前；同优先级按入队序号（FIFO）。元组比较永不会落到 message 上。
            q.put((-priority, message.seq, message))
            return message

    # ------------------------------------------------------------ 取出
    def take(self, session_id: str) -> QueuedMessage:
        """取出会话的下一条消息（阻塞直到有消息）。"""
        _, _, message = self._queue_of(session_id).get()
        return message

    def poll(self, session_id: str, timeout: float) -> QueuedMessage | None:
        """取出会话的下一条消息；超时返回 None（Worker 靠它空闲退出）。"""
        try:
            _, _, message = self._queue_of(session_id).get(timeout=timeout)
            return message
        except _queue.Empty:
            return None

    # ------------------------------------------------------------ 统计
    def pending_count(self, session_id: str) -> int:
        with self._lock:
            q = self._queues.get(session_id)
            return 0 if q is None else q.qsize()

    def size(self) -> int:
        with self._lock:
            return sum(q.qsize() for q in self._queues.values())

    # ------------------------------------------------------------ 内部
    def _queue_of(self, session_id: str) -> "_queue.PriorityQueue[tuple[int, int, QueuedMessage]]":
        with self._lock:
            q = self._queues.get(session_id)
            if q is None:
                q = _queue.PriorityQueue()
                self._queues[session_id] = q
            return q


class IllegalStateError__queue_message_queue(RuntimeError):
    """与 Java `IllegalStateException` 对应（队列满时塞进 future 的异常类型）。"""


def message_data(message: QueuedMessage) -> dict[str, Any]:
    """队列消息的调试视图（日志/用例断言用）。"""
    return {
        "id": message.id, "session_id": message.session_id, "priority": message.priority,
        "is_steer": message.is_steer, "model": message.model,
        "thinking_level": message.thinking_level,
    }


# ========================================================================
# 原模块 lionbox/wiring.py
# ========================================================================
"""全项目装配：把各模块连成一个可用的对象图。

【为什么单独一个文件】Java 版这些连接是 Spring 的 @Autowired 自动完成的（60 个插件、
17 个 controller、事件存储、会话、适配器互相注入）。Python 版刻意**显式装配**：
启动路径就是"读配置 → 建对象 → 注册路由 → 监听端口"，一眼看得完，
这也正是 Python 版 import+装配 64 ms（Java Spring 上下文 1,985 ms）的原因之一。

装配顺序（有依赖关系，不要随意调换）：
    config → events / sessions / context → plugins(base 已就绪) → tools →
    llm 适配器 → agent(Approve/ChangeReview/Guard/Context) → api
"""


import threading
from pathlib import Path
from typing import Any



class Wiring:
    def __init__(self, app_root: Path, cfg: AppConfigStore, *,
                 workspace: Path | None = None, local_runtime: Any = None) -> None:
        self.app_root = Path(app_root)
        self.cfg = cfg
        self.workspace = Path(workspace) if workspace else None
        self.local_runtime = local_runtime
        self.lock = threading.RLock()
        self.notes: list[str] = []      # 装配过程中降级/跳过的说明（启动日志会打出来）

        self.events = None
        self.history = None
        self.sessions = None
        self.changes = None
        self.approval = None
        self.adapters = None
        self.registry = None
        self.loop = None

        self._build_storage()
        self._build_tools()
        self._build_llm()
        self._build_agent()
        self.wire_plugins()
        self.wire_team()

    # ------------------------------------------------------------------ 存储
    def _build_storage(self) -> None:
        # 事件存储：默认位置与 Java 版一致（~/.lioncode 下），并把旧的"一条一个文件"
        # 目录自动迁移成按天分片（用户现有数据不能丢，也不要求他手动搬）
        try:
            from lionbox.events import EventStore
            # 【路径交给 events 模块自己的默认值】它是对照 Java 的 EventStore 移植的，
            # 自己再拼一份 ~/.lioncode/events 会与 Java 的实际位置对不上（用户数据读不到）。
            self.events = EventStore(auto_migrate_legacy=True)
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"事件存储未就绪（用内存桩）: {type(e).__name__}: {e}")

        try:
            from lionbox.sessions import ConversationHistory
            self.history = ConversationHistory(
                workspace_path=str(self.workspace) if self.workspace else None,
                auto_load=False)
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"对话历史未就绪（用内存桩）: {type(e).__name__}: {e}")

        try:
            from lionbox.sessions import SessionManager, SessionPersistence
            self.sessions = SessionManager()
            try:
                self.sessions.set_persistence(SessionPersistence())
            except Exception as e:  # noqa: BLE001 持久化不可用不影响内存会话
                self.notes.append(f"会话持久化未接线: {type(e).__name__}: {e}")
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"会话管理未就绪: {type(e).__name__}: {e}")

    # ------------------------------------------------------------------ 工具
    def _build_tools(self) -> None:
        try:
            from lionbox.plugins.base import REGISTRY
            from lionbox.tools import load as load_tools
            self.registry = load_tools(self.workspace)
            self.notes.append(f"工具装载 {len(self.registry)} 个")
        except Exception as e:  # noqa: BLE001
            from lionbox.plugins.base import REGISTRY
            self.registry = REGISTRY
            self.notes.append(f"工具装载失败: {type(e).__name__}: {e}")

    # ------------------------------------------------------------------ 模型
    def _build_llm(self) -> None:
        try:
            from lionbox.llm.manager import build_default_manager
            self.adapters = build_default_manager(self.cfg, self.local_runtime)
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"模型适配器未就绪: {type(e).__name__}: {e}")

    def active_client(self) -> Any:
        """当前模式对应的适配器（local / custom 由 config 决定）。"""
        if self.adapters is None:
            return None
        for name in ("get_active_adapter", "active", "current", "resolve_active", "get_active"):
            fn = getattr(self.adapters, name, None)
            if callable(fn):
                try:
                    return fn()
                except Exception:  # noqa: BLE001
                    continue
        # 退路：直接按属性名取
        mode = str(self.cfg.get("providerMode", "local"))
        for attr in (("local" if mode == "local" else "custom"), mode, "local"):
            got = getattr(self.adapters, attr, None)
            if got is not None:
                return got
        return None

    # ------------------------------------------------------------------ Agent
    def _build_agent(self) -> None:
        try:
            from lionbox.agent import AgentLoop, ApprovalPolicy, ChangeReview
            self.approval = ApprovalPolicy()
            self.changes = ChangeReview(history=self.history,
                                        settings=self.cfg,
                                        enabled_by_default=True)
            self.loop = AgentLoop(
                client=self.active_client(),
                config_store=self.cfg,
                registry=self.registry,
                event_store=self.events,
                history=self.history,
                workspace=str(self.workspace) if self.workspace else None,
                approval=self.approval,
            )
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"Agent 主循环未就绪: {type(e).__name__}: {e}")

    # ------------------------------------------------------------------ 工具接线
    def wire_tool_hooks(self) -> None:
        """把工具的"接线点"接上真实实现。

        施工单元按规范留了显式接线点、不接线时**如实报失败**（不假装成功）：
          `tools/file/_gate.set_review(...)` —— 写文件的 5 个工具要过改动审核；
          `ask_user.set_question_service/set_sound_notifier`；
          `context_prune.set_history` / `context_window.set_budget`。
        这里在 app 启动时统一接上，避免每个工具各自去猜依赖在哪。
        """
        if self.loop is not None:
            try:
                from lionbox.tools.file import _gate
                _gate.set_review(self.changes)
            except Exception as e:  # noqa: BLE001
                self.notes.append(f"改动审核闸门未接线: {type(e).__name__}: {e}")

        try:
            from lionbox.tools.context import context_prune
            if self.history is not None:
                setter = getattr(context_prune, "set_history", None)
                if callable(setter):
                    setter(self.history)
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"context_prune 未接线: {type(e).__name__}: {e}")

        try:
            from lionbox.tools.context import context_window
            if self.loop is not None:
                setter = getattr(context_window, "set_budget", None)
                if callable(setter):
                    setter(getattr(self.loop, "budget", None))
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"context_window 未接线: {type(e).__name__}: {e}")

        try:
            from lionbox.tools.system import ask_user
            from lionbox.misc.question import UserQuestionService
            setter = getattr(ask_user, "set_question_service", None)
            if callable(setter):
                setter(UserQuestionService())
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"ask_user 未接线: {type(e).__name__}: {e}")

    # ------------------------------------------------------------------ 插件体系
    def wire_plugins(self) -> None:
        """一键装配插件体系：外置插件 → 工具 → 技能 → 7 个系统插件 → 门禁 → 自动化轮询。

        Java 里这几步是 Spring 组件扫描 + `PluginAutoRegistration` 干的；Python 版由
        `plugins.lifecycle.bootstrap_all` 按同一顺序显式执行，启动路径可读、可断言。
        """
        self.plugin_summary = {}
        try:
            from lionbox.plugins.lifecycle import bootstrap_all, set_default_event_sink
            # 【必须先设事件 sink】否则插件注册事件会落到它自己新建的 EventStore 上，
            # 那个默认路径在受限环境下写不了，事件只能打日志丢掉。
            if self.events is not None:
                set_default_event_sink(self.events)
            self.plugin_summary = bootstrap_all(
                session_manager=self.sessions,
                dispatcher=getattr(self, "dispatcher", None),
                config_store=self.cfg,
                load_tools=False,      # 工具已在 _build_tools() 装过（见 lifecycle 里的说明）
            )
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"插件体系装配未完成: {type(e).__name__}: {e}")

    def wire_team(self) -> None:
        """注册子智能体 / 团队工具。必须在 AgentLoop 构造之后（它们要拿 loop 引用）。"""
        if self.loop is None or self.registry is None:
            return
        try:
            from lionbox.team import register_team_tools
            register_team_tools(self.registry, agent_loop=self.loop,
                                session_manager=self.sessions, settings=self.cfg)
        except Exception as e:  # noqa: BLE001
            self.notes.append(f"团队工具未注册: {type(e).__name__}: {e}")
    # ------------------------------------------------------------------ 概览
    def summary(self) -> dict[str, Any]:
        return {
            # 【必须用 is not None】EventStore / SessionManager 定义了 __len__，
            # 空的时候对象是 falsy —— 用真值判断会把"已装配但还没数据"误报成 None。
            "events": type(self.events).__name__ if self.events is not None else None,
            "history": type(self.history).__name__ if self.history is not None else None,
            "sessions": type(self.sessions).__name__ if self.sessions is not None else None,
            "tools": len(self.registry) if self.registry is not None else 0,
            "adapters": type(self.adapters).__name__ if self.adapters is not None else None,
            "client": type(self.active_client()).__name__ if self.active_client() is not None else None,
            "agent": type(self.loop).__name__ if self.loop is not None else None,
            "notes": self.notes,
        }


# 接口模块登记表（内联后替代动态导入；顺序与 MODULES 一致）
_API_REGISTER = {
    "workspaces": register,
    "sessions": register__api_sessions,
    "events": register__api_events,
    "files": register__api_files,
    "models": register__api_models,
    "approvals": register__api_approvals,
    "changes": register__api_changes,
    "context": register__api_context,
    "questions": register__api_questions,
    "notifications": register__api_notifications,
    "native_dialog": register__api_native_dialog,
    "providers": register__api_providers,
    "plugins": register__api_plugins,
    "plugin_dev": register__api_plugin_dev,
    "skills": register__api_skills,
    "runtime_extra": register__api_runtime_extra,
    "chat": register__api_chat,
    "agent_control": register__api_agent_control,
}


# ==========================================================================
# 主程序入口（在 PyCharm 里直接 Run 这个文件）
#   默认：桌面版（起后端 + 编辑器 + 开窗口）
#   --backend-only：只起后端（调接口/跑回归用）
#   --no-window   ：起后端与编辑器，不开窗口
# ==========================================================================


# ==========================================================================
# 前端启动 —— Ink（React for CLIs）
#
# 后端就是本文件里的那套 HTTP 服务（`--backend-only` 单独起）；界面完全交给
# `tui/app.js`。这里只负责：起后端子进程 → 等它监听 → 拉起 node 跑界面 → 收尾。
#
# 【为什么不带 Python 界面兜底】界面只有 Ink 一个实现，避免两套界面两套行为。
# 缺 node 或没装依赖时给一句明确的补救指令，而不是悄悄换一个长得不一样的界面。
# ==========================================================================


def _ink_frontend_cmd() -> list | None:
    """终端界面的启动命令；不可用返回 None（并说明缺什么）。

    【为什么是 bun 不是 node】界面用 OpenTUI 渲染（与 MiMo Code 同款：
    `@opentui/core` + `@opentui/solid` + solid-js）。OpenTUI 的渲染器走 **Bun 的
    原生 FFI**，在 Node 上直接报：
        Failed to initialize OpenTUI render library:
        OpenTUI native FFI is not available for this runtime yet
    所以这里必须找 bun。JSX runtime 由 tui/bunfig.toml 的
    `preload = ["@opentui/solid/preload"]` 挂上（缺了会报 jsxDEV 找不到）。
    """
    root = os.path.dirname(os.path.abspath(__file__))
    tui = os.path.join(root, "tui")
    app = os.path.join(tui, "src", "index.tsx")
    if not os.path.isfile(app):
        print(f"找不到界面文件: {app}")
        return None
    if not os.path.isdir(os.path.join(tui, "node_modules", "@opentui", "core")):
        print("界面依赖还没装。在 tui/ 目录里执行一次（需要 Bun）：")
        print("    bun install")
        return None
    bun = shutil.which("bun")
    if not bun:
        print("PATH 里找不到 bun（OpenTUI 只能在 Bun 上跑，Node 不行）。")
        print("装 Bun：npm install -g bun   （或 https://bun.sh）")
        return None
    # --conditions=browser 是 MiMo 那边的入口写法，少它会在依赖解析上翻车
    # 【cwd 必须切到 tui/】Bun 读 `bunfig.toml` 是按 **cwd** 找的，不看脚本路径。
    # 主程序是从仓库根目录启动的，不切目录就找不到那份 preload（JSX runtime），
    # 于是 Bun 退回默认 React runtime，报：
    #     Cannot find module 'react/jsx-dev-runtime' from '.../tui/src/index.tsx'
    # （`bun --cwd` 不能放在 `run` 前面，所以由调用方用 subprocess 的 cwd 切。）
    return [bun, "run", "--conditions=browser", app]


def _wait_backend(port: int, proc, timeout: float = 90.0) -> bool:
    """等后端开始监听（连不上时 urllib 抛异常，别拿返回值判断）。"""
    import time as _t
    import urllib.request
    deadline = _t.time() + timeout
    url = f"http://127.0.0.1:{port}/health"
    while _t.time() < deadline:
        if proc.poll() is not None:
            return False
        try:
            with urllib.request.urlopen(url, timeout=2):
                return True
        except Exception:                                 # noqa: BLE001
            _t.sleep(0.25)
    return False


def _ink_main(argv: list | None = None) -> int:
    """起后端 + 拉起 Ink 界面。"""
    import subprocess
    import time as _t
    from pathlib import Path as _Path

    args = list(sys.argv[1:] if argv is None else argv)
    port = 8080
    workspace = None
    script_arg = ""
    rest: list = []
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--server.port="):
            port = int(a.split("=", 1)[1])
        elif a == "--server.port" and i + 1 < len(args):
            i += 1
            port = int(args[i])
        elif a.startswith("--lion.workspace.default-path="):
            workspace = a.split("=", 1)[1]
            rest.append(a)
        elif a.startswith("--script="):
            script_arg = a                                  # 只给界面用，后端不认
        else:
            rest.append(a)
        i += 1

    ink = _ink_frontend_cmd()
    if ink is None:
        return 1

    # 【不是在真终端里就跑不起来 TUI】PyCharm 的 Run 窗口、管道、重定向都没有 TTY：
    # Ink 的 ANSI 光标控制在那儿会变成一堆乱字，看起来就像"还是 python 终端"。
    # 所以这种情况下自己开一个真终端窗口（优先 Windows Terminal），把界面放进去跑。
    if os.name == "nt" and not sys.stdout.isatty() and not script_arg:
        passthrough = [a for a in args if a != "--backend-only"]
        exe, me = sys.executable, os.path.abspath(__file__)
        wt = shutil.which("wt")
        try:
            if wt:
                # -d 指定工作目录；cmd /k 让窗口在程序退出后不立刻关掉
                subprocess.Popen([wt, "-d", os.getcwd(), "cmd", "/k", exe, me,
                                  *passthrough])
            else:
                subprocess.Popen(["cmd", "/c", "start", "", "cmd", "/k", exe, me,
                                  *passthrough])
        except Exception as e:                            # noqa: BLE001
            print(f"开新终端窗口失败: {type(e).__name__}: {e}")
            print("请手动打开 Windows Terminal / PowerShell，然后运行：")
            print(f'    "{exe}" "{me}"')
            return 1
        print("当前窗口不是真终端（没有 TTY），界面已在新开的终端窗口里启动。")
        print("也可以直接双击仓库根目录的「启动LionCode.cmd」。")
        return 0

    # 后端起成子进程：它的日志（[对话]/[插件]/[会话] 那些 print）会和 Ink 的画面
    # 抢同一块终端，落进日志文件才干净；Ctrl+C 也只该中断任务，不该掀掉后端。
    log_dir = _Path(os.getcwd()) / ".lionbox"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        log_dir = _Path(os.getcwd())
    try:
        log_file = (log_dir / "backend.log").open("a", encoding="utf-8", errors="replace")
    except OSError:
        log_file = open(os.devnull, "w", encoding="utf-8")
    server_args = [f"--server.port={port}", *rest]
    log_file.write(f"\n===== {_t.strftime('%Y-%m-%d %H:%M:%S')} 后端启动 "
                   f"{' '.join(server_args)} =====\n")
    log_file.flush()

    try:
        proc = subprocess.Popen(
            [sys.executable, os.path.abspath(__file__), "--backend-only", *server_args],
            stdout=log_file, stderr=log_file, stdin=subprocess.DEVNULL, cwd=os.getcwd())
    except Exception as e:                                # noqa: BLE001
        print(f"起不来后端子进程: {type(e).__name__}: {e}")
        return 1

    rc = 0
    try:
        if not _wait_backend(port, proc):
            print("后端没能起来（端口可能被占用）。日志尾部：")
            try:
                log_file.flush()
                for line in (log_dir / "backend.log").read_text(
                        encoding="utf-8", errors="replace").splitlines()[-12:]:
                    print("   " + line)
            except Exception:                             # noqa: BLE001
                pass
            print(f"完整日志：{log_dir / 'backend.log'}")
            return 1
        cmd = [*ink, f"--port={port}", f"--workspace={workspace or os.getcwd()}"]
        if script_arg:
            cmd.append(script_arg)
        # 切到 tui/：Bun 是按 **cwd** 找 bunfig.toml / tsconfig.json 的，不看脚本路径。
        # 从仓库根目录启动它会把 JSX 退化成 React runtime，报：
        #     Cannot find module 'react/jsx-dev-runtime' from '.../tui/src/index.tsx'
        tui_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tui")
        print(f"[界面] {' '.join(cmd)}", flush=True)
        print(f"[界面] 工作目录 {tui_dir}", flush=True)
        rc = subprocess.call(cmd, cwd=tui_dir)
    except KeyboardInterrupt:
        rc = 0
    finally:
        try:
            proc.terminate()
            proc.wait(timeout=8)
        except Exception:                                 # noqa: BLE001
            try:
                proc.kill()
            except Exception:                             # noqa: BLE001
                pass
    return int(rc or 0)


# ==========================================================================
# 主程序入口（在 PyCharm 里直接 Run 这个文件）
#   默认：Ink 终端界面（后端自动起）
#   --backend-only：只起 HTTP 后端，不起界面（调接口 / 跑自动化用）
# ==========================================================================
def _host_main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if "--backend-only" in args:
        rest = [a for a in args if a != "--backend-only"]
        print("Lion Code 后端启动中（只有接口，没有界面）… Ctrl+C 结束", flush=True)
        return int(main(rest) or 0)
    return int(_ink_main(args) or 0)


if __name__ == "__main__":
    raise SystemExit(_host_main())