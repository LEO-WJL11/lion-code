# -*- coding: utf-8 -*-
r"""插件管理（由引擎内联生成）
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
    "lionbox.plugins",
    "lionbox.plugins.base",
    "lionbox.plugins.lifecycle",
    "lionbox.automation.task",
    "lionbox.automation.due",
    "lionbox.automation.plugin",
    "lionbox.automation.runner",
    "lionbox.automation",
    "lionbox.plugindev.service",
    "lionbox.plugindev",
    "lionbox.plugins.review",
    "lionbox.team.member",
    "lionbox.team.agent_team",
    "lionbox.team.agent_team_tool",
    "lionbox.team.subagent",
    "lionbox.team.subagent_tool",
    "lionbox.team.registrar",
    "lionbox.team",
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

# 【每个被内联模块各自原本的 __file__】有代码用它推算"程序装在哪"（例如技能目录：
# `skills/repository.py` 往上三层才是安装根）。内联后 `__file__` 全是 main.py 的路径，
# 向上推会跑到仓库外面 —— 实测后果是内置技能一个都找不到。所以按模块各记一份。
# 路径不必真实存在：用到的是路径运算，只要目录层级一致，算出的安装根就一样。
_ORIG_FILE_plugins = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\plugins\__init__.py"
_ORIG_FILE_plugins_base = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\plugins\base.py"
_ORIG_FILE_plugins_lifecycle = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\plugins\lifecycle.py"
_ORIG_FILE_automation_task = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\automation\task.py"
_ORIG_FILE_automation_due = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\automation\due.py"
_ORIG_FILE_automation_plugin = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\automation\plugin.py"
_ORIG_FILE_automation_runner = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\automation\runner.py"
_ORIG_FILE_automation = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\automation\__init__.py"
_ORIG_FILE_plugindev_service = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\plugindev\service.py"
_ORIG_FILE_plugindev = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\plugindev\__init__.py"
_ORIG_FILE_plugins_review = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\plugins\review.py"
_ORIG_FILE_team_member = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\team\member.py"
_ORIG_FILE_team_agent_team = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\team\agent_team.py"
_ORIG_FILE_team_agent_team_tool = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\team\agent_team_tool.py"
_ORIG_FILE_team_subagent = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\team\subagent.py"
_ORIG_FILE_team_subagent_tool = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\team\subagent_tool.py"
_ORIG_FILE_team_registrar = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\team\registrar.py"
_ORIG_FILE_team = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\team\__init__.py"


# ========================================================================
# 原模块 lionbox/plugins.py
# ========================================================================
"""插件体系基础设施：`base.py`（工具基类/枚举/显式登记）+ `lifecycle.py`（生命周期与系统插件）。

    from lionbox.plugins.base import ToolPlugin, tool, REGISTRY, load_all
    from lionbox.plugins.lifecycle import (PluginSettings, PluginRegistry, PluginPaths,
                                           bootstrap_system_plugins, default_registry)

`base.py` 是冻结契约（工具层都按它写）；`lifecycle.py` 在它外面补上"一切皆插件"
要的那一层：设置持久化、九类索引、系统插件、门禁、加载器、Agent 主循环扩展点。
本 `__init__.py` 故意**不 import 任何子模块** —— 插件包是启动路径上的关键模块，
保持空实现可以避免任何循环导入。
"""


# ========================================================================
# 原模块 lionbox/plugins/base.py
# ========================================================================
"""插件基础设施：工具基类、枚举、注册表。

【契约来源】逐项对照 Java 版：
  `core/plugin/Plugin.java`、`PluginKind`、`AbstractToolPlugin`、`ToolResult`、
  `core/agent/AgentMode`、`PermissionLevel`、`ToolCategory`。
60 个工具都继承这里的 `ToolPlugin`，注册方式与 Java 一样是"声明 id/name/描述/schema，
由注册表统一收集"，这样 `/api/plugins` 的输出结构与系统提示词里的工具定义都不变。
"""


import os
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Iterable

# --------------------------------------------------------------------------
# 枚举（值与 Java 版一致，parse 也按同样的宽松规则）
# --------------------------------------------------------------------------


class PermissionLevel:
    READ_ONLY = "READ_ONLY"
    WRITE = "WRITE"
    #: Java 侧还有 WORKSPACE_WRITE（只允许改工作区内的文件）。
    #: 施工单元报上来的：少了它，改文件的工具只能返回裸字符串，别的模块会各自再踩一次。
    WORKSPACE_WRITE = "WORKSPACE_WRITE"
    EXECUTE = "EXECUTE"
    DANGEROUS = "DANGEROUS"

    #: 完整取值清单（顺序与 Java 枚举一致），parse 与校验都以它为准
    ALL = (READ_ONLY, WRITE, WORKSPACE_WRITE, EXECUTE, DANGEROUS)

    @staticmethod
    def parse(raw: Any) -> str:
        v = str(raw or "").strip().upper()
        return v if v in PermissionLevel.ALL else PermissionLevel.READ_ONLY


class ToolCategory:
    FILE_OPERATION = "FILE_OPERATION"
    #: 这两个值原来漏了 —— Java 的 `isAvailableInMode(MINIMAL)` 正是靠它们判定，
    #: 少了就只能返回裸字符串，容易在别处对不上。
    FILE_MODIFY = "FILE_MODIFY"
    FILE_SEARCH = "FILE_SEARCH"
    CODE = "CODE"
    GIT = "GIT"
    SHELL = "SHELL"
    WEB = "WEB"
    SYSTEM = "SYSTEM"
    CONTEXT = "CONTEXT"

    #: Java 侧还有这两个：`OTHER`（工具自己声明"其它"）与 `WEB_SEARCH`（搜索类单独归类）。
    #: 施工单元报上来的 —— 少了它们只能返回裸字符串，`/api/plugins` 逐字段对比会对不上。
    OTHER = "OTHER"
    WEB_SEARCH = "WEB_SEARCH"

    #: 与 Java 枚举逐项对齐的完整清单
    ALL = (FILE_OPERATION, FILE_MODIFY, FILE_SEARCH, CODE, GIT, SHELL, WEB, WEB_SEARCH,
           SYSTEM, CONTEXT, OTHER)

    #: 极简模式（MINIMAL）开放的工具类别 —— 对齐 Java 的 isAvailableInMode 判定
    MINIMAL_OPEN = (FILE_OPERATION, FILE_MODIFY, FILE_SEARCH, SHELL)


class PluginKind:
    """与 Java 版 PluginKind 相同的 9 个值（显示名/描述也照抄，前端按它分组）。"""

    BASE_TOOL = "BASE_TOOL"
    ADVANCED_TOOL = "ADVANCED_TOOL"
    SKILL = "SKILL"
    SUBAGENT = "SUBAGENT"
    TERMINAL = "TERMINAL"
    AGENT_LOOP = "AGENT_LOOP"
    AGENT_TEAM = "AGENT_TEAM"
    APPROVAL_REVIEW = "APPROVAL_REVIEW"
    AUTOMATION = "AUTOMATION"

    DISPLAY = {
        BASE_TOOL: ("基础工具", "极简模式就能用的工具（文件读写/终端这类「没它干不了活」的）"),
        ADVANCED_TOOL: ("进阶工具", "标准模式下才开放的工具（网络/Git/编解码等）"),
        SKILL: ("技能", "向系统提示词注入领域经验的技能包"),
        SUBAGENT: ("子智能体", "把子任务派给子智能体执行，可限制递归层级、并发数与所用模型"),
        TERMINAL: ("终端", "常驻终端插件：限制每条命令最长运行时间与最大输出"),
        AGENT_LOOP: ("Agent 大循环", "控制 Agent 派发工具调用的方式（轮次上限、工具超时、空转容忍）"),
        AGENT_TEAM: ("智能体团队", "一组用户自定义的智能体：每个用什么模式、负责干什么"),
        APPROVAL_REVIEW: ("自动授权审查", "用另一个模型对话审核危险的工具调用，决定是否拦截"),
        AUTOMATION: ("自动化任务", "按设定时间或周期，在指定会话里自动执行任务"),
    }

    @staticmethod
    def parse(raw: Any) -> str:
        v = str(raw or "").strip().upper()
        return v if v in PluginKind.DISPLAY else PluginKind.ADVANCED_TOOL


class AgentMode:
    """与 Java 版一致：PTC / CREATIVE / STANDARD / MINIMAL，界面只让选 STANDARD、MINIMAL。"""

    PTC = "PTC"
    CREATIVE = "CREATIVE"
    STANDARD = "STANDARD"
    MINIMAL = "MINIMAL"

    DISPLAY = {
        PTC: ("预规划模式", "模型预先完整规划全部工具调用步骤再执行"),
        CREATIVE: ("创造模式", "AI可以编写、修改、安装、卸载插件"),
        STANDARD: ("标准模式", "全部工具开放"),
        MINIMAL: ("极简模式", "仅开放文件、Shell工具"),
    }
    SELECTABLE = (STANDARD, MINIMAL)

    @staticmethod
    def from_name(name: Any) -> str:
        v = str(name or "").strip().upper()
        return v if v in AgentMode.DISPLAY else AgentMode.STANDARD

    @staticmethod
    def normalize(mode: Any) -> str:
        return AgentMode.from_name(mode)


# --------------------------------------------------------------------------
# 工具结果（字段与 Java 版 record ToolResult(success, content, metadata, error) 对齐）
# --------------------------------------------------------------------------


class ToolResult:
    __slots__ = ("success", "content", "metadata", "error")

    def __init__(self, success: bool, content: str = "", error: str = "",
                 metadata: dict[str, Any] | None = None) -> None:
        self.success = success
        self.content = content
        self.error = error
        self.metadata = metadata or {}

    @staticmethod
    def ok(content: str, metadata: dict[str, Any] | None = None) -> "ToolResult":
        return ToolResult(True, content=content, metadata=metadata)

    @staticmethod
    def fail(error: str) -> "ToolResult":
        return ToolResult(False, error=error)

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {"success": self.success}
        if self.content:
            d["content"] = self.content
        if self.error:
            d["error"] = self.error
        if self.metadata:
            d["metadata"] = self.metadata
        return d

    def __repr__(self) -> str:
        return f"ToolResult(success={self.success}, content={self.content[:60]!r}, error={self.error[:60]!r})"


# --------------------------------------------------------------------------
# 工具基类
# --------------------------------------------------------------------------


class ToolPlugin:
    """所有工具的基类。子类至少覆盖 id / name / description / parameters_schema / execute。

    与 Java 版 AbstractToolPlugin 的对应关系：
      getId/getName/getDescription/getCategory/getRequiredPermission -> 同名属性
      getParametersSchema() -> parameters_schema()
      execute(Map args)     -> execute(args) 返回 ToolResult
      getFunctionDefinition() -> function_definition()（OpenAI 工具定义形状）
    """

    #: 是否在极简模式（MINIMAL）下开放 —— 决定 PluginKind 是 BASE_TOOL 还是 ADVANCED_TOOL
    minimal_mode: bool = False

    def __init__(self, workspace: Path | None = None) -> None:
        self.workspace = Path(workspace) if workspace else Path.cwd()

    # ---- 元信息（子类覆盖）----
    @property
    def id(self) -> str:                      # noqa: A003
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> str:
        return ""

    @property
    def category(self) -> str:
        return ToolCategory.SYSTEM

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    @property
    def kind(self) -> str:
        return PluginKind.BASE_TOOL if self.minimal_mode else PluginKind.ADVANCED_TOOL

    def parameters_schema(self) -> dict[str, Any]:
        return {"type": "object", "properties": {}, "required": []}

    def function_definition(self) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters_schema(),
            },
        }

    def descriptor(self) -> dict[str, Any]:
        """给 `/api/plugins` 用的完整描述（字段名对齐 Java 版）。"""
        display, desc = PluginKind.DISPLAY.get(self.kind, ("", ""))
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "kind": self.kind,
            "kindDisplayName": display,
            "kindDescription": desc,
            "category": self.category,
            "permission": self.permission,
            "parameters": self.parameters_schema(),
            "minimalMode": self.minimal_mode,
        }

    # ---- 执行（子类覆盖）----
    def execute(self, args: dict[str, Any]) -> ToolResult:
        raise NotImplementedError

    # ---- 参数助手（与 Java 版同名同语义）----
    def get_string_arg(self, args: dict[str, Any], key: str, default: str = "") -> str:
        v = args.get(key)
        return default if v is None else str(v)

    def get_required_string_arg(self, args: dict[str, Any], key: str) -> str:
        """取必填字符串参数。**文案与 Java 逐字一致**（施工单元对照出来的差异点）。

        Java 原文：
            throw new IllegalArgumentException("缺少必需参数: " + key + requiredParamsHint());

        两个细节都要照抄：
          1. 字面量 "null"（模型有时真这么填）按缺参处理；
          2. 报错要**把本工具全部必填参数连说明一起回给模型** —— 只写"缺少必需参数: mode"，
             模型不知道 mode 该填什么。Java 注释里记着实测：head_tail_file 因为漏了 mode
             连错 5 次。带上说明后下一轮基本一次改对。
        """
        val = args.get(key)
        text = None if val is None else str(val)
        if text is None or text.strip() == "" or text.strip().lower() == "null":
            raise ValueError("缺少必需参数: " + key + self.required_params_hint())
        return text

    def required_params_hint(self) -> str:
        """本工具必填参数（带说明），附在缺参报错后面。等价于 Java 的 requiredParamsHint()。"""
        try:
            schema = self.parameters_schema() or {}
            req = schema.get("required") or []
            if not req:
                return ""
            props = schema.get("properties") or {}
            parts: list[str] = []
            for name in req:
                desc = ""
                prop = props.get(str(name))
                if isinstance(prop, dict):
                    d = prop.get("description")
                    desc = "" if d is None else str(d)
                parts.append(f"{name}（{desc}）")
            return "。本工具必填参数：" + "、".join(parts)
        except Exception:  # noqa: BLE001 提示失败不该掩盖"缺参"这个事实
            return ""

    def get_int_arg(self, args: dict[str, Any], key: str, default: int = 0) -> int:
        v = args.get(key)
        if v is None:
            return default
        try:
            return int(v)
        except (TypeError, ValueError):
            return default

    def get_bool_arg(self, args: dict[str, Any], key: str, default: bool = False) -> bool:
        v = args.get(key)
        if v is None:
            return default
        if isinstance(v, bool):
            return v
        return str(v).strip().lower() in ("1", "true", "yes", "on")

    def current_workspace(self) -> Path:
        """当前会话绑定的工作区路径（Java `AbstractToolPlugin.currentWorkspace()`）。

        【为什么需要】工作区是**按会话**绑定的，而 `self.workspace` 是构造期钉死的
        （`load_all()` 没传 workspace 时退化成 `Path.cwd()` = 进程 CWD）。凡是"要按
        当前会话的工作区办事"的工具（常驻终端、后台进程登记表…）都必须走这个方法，
        否则会把仓库根目录当成用户的工作区：

            实测 `_check_tool_idempotent.py` 最后一条 —— 在**非 git 仓库**的测试工作区里
            跑 `git status`，本该 exit 128 + "当前目录不是 git 仓库"的提示；
            因为终端的初始 cwd 变成了仓库根目录（那是个 git 仓库），
            `git status` 成功退出 0，模型拿到一句"一切正常"。
        """
        from lionbox.workspace.context import WorkspaceContext
        ws = WorkspaceContext.get()
        return Path(ws) if ws else self.workspace

    def resolve_path(self, path: str) -> Path:
        """解析路径参数：相对路径基于**当前会话绑定的工作区**根目录。

        逐字对齐 Java `AbstractToolPlugin.resolvePath`：

            protected String resolvePath(String rawPath) {
                return WorkspaceContext.resolve(rawPath);
            }

        【为什么不能只用 self.workspace】工作区是**按会话**绑定的（同一进程里不同会话
        可以是不同工作区），AgentLoop 在执行工具前把它放进线程上下文（`WorkspaceContext`）。
        这里原来用的是构造期钉死的 `self.workspace`（装配时传的是 None → 退化成 `Path('.')`
        = **进程 CWD**），于是所有相对路径都按仓库根目录解析 ——
        实测 `_check_tool_idempotent.py` 里"给目录统计 / 相对 workdir"一整片用例报
        `文件不存在: <仓库根>\\sub`，而它们本该落在测试工作区里。
        没有工作区上下文时（单测直接 `execute()`）才回落到 `self.workspace`，与 Java 的
        "未绑定工作区时不限制"一致。
        """
        raw = str(path)
        from lionbox.workspace.context import WorkspaceContext
        resolved = WorkspaceContext.resolve(raw)
        if resolved is not None and str(resolved) != raw:
            return Path(str(resolved))
        p = Path(raw)
        if p.is_absolute():
            return p
        return p if WorkspaceContext.get() else (self.workspace / p)

    # ---- 进程助手 ----
    @staticmethod
    def is_windows() -> bool:
        return sys.platform == "win32"

    @staticmethod
    def run_process(cmd: list[str] | str, cwd: Path | None = None, timeout: int = 60,
                    shell: bool = False, env: dict[str, str] | None = None) -> tuple[int, str]:
        """跑一个子进程并返回 (exit_code, 合并输出)。输出按 UTF-8 容错解码。"""
        full_env = dict(os.environ)
        if env:
            full_env.update(env)
        try:
            p = subprocess.run(cmd, cwd=str(cwd) if cwd else None, shell=shell,
                               capture_output=True, timeout=timeout, env=full_env,
                               creationflags=(0x08000000 if sys.platform == "win32" else 0))
        except subprocess.TimeoutExpired:
            return 124, f"命令超时（{timeout} 秒）"
        except OSError as e:
            return 127, f"无法执行命令: {e}"
        out = (p.stdout or b"") + (p.stderr or b"")
        return p.returncode, out.decode("utf-8", errors="replace")

    # ---- 结果助手 ----
    @staticmethod
    def success(content: str, metadata: dict[str, Any] | None = None) -> ToolResult:
        return ToolResult.ok(content, metadata)

    @staticmethod
    def error(error: str) -> ToolResult:
        return ToolResult.fail(error)


# --------------------------------------------------------------------------
# 注册表
# --------------------------------------------------------------------------


class PluginRegistry:
    """插件注册表。与 Java 版的 PluginAutoRegistration 等价：
    启动时把所有工具收进来，按 id 去重，按模式过滤。"""

    def __init__(self) -> None:
        self._by_id: dict[str, ToolPlugin] = {}
        self._by_name: dict[str, ToolPlugin] = {}

    def register(self, plugin: ToolPlugin) -> None:
        self._by_id[plugin.id] = plugin
        self._by_name[plugin.name] = plugin

    def register_all(self, plugins: Iterable[ToolPlugin]) -> int:
        n = 0
        for p in plugins:
            self.register(p)
            n += 1
        return n

    def get(self, tool_id: str) -> ToolPlugin | None:
        return self._by_id.get(tool_id)

    def by_name(self, name: str) -> ToolPlugin | None:
        return self._by_name.get(name)

    def is_registered(self, key: str) -> bool:
        """按 id 或 name 判断是否已注册。

        【为什么要有它】team 的注册器（`team.register_team_tools`）在补注册子智能体/团队
        工具前要先问一句"是不是已经注册过了" —— 这是 Java 侧 `PluginRegistry` 就有的方法，
        我第一版漏了，接线时报 AttributeError。id 与 name 都认，避免调用方记混。
        """
        return key in self._by_id or key in self._by_name

    def unregister(self, key: str) -> bool:
        """按 id 或 name 移除（插件热卸载用）。"""
        plugin = self._by_id.get(key) or self._by_name.get(key)
        if plugin is None:
            return False
        self._by_id.pop(plugin.id, None)
        self._by_name.pop(plugin.name, None)
        return True

    def all(self) -> list[ToolPlugin]:
        return list(self._by_id.values())

    def for_mode(self, mode: str) -> list[ToolPlugin]:
        if AgentMode.from_name(mode) == AgentMode.MINIMAL:
            return [p for p in self._by_id.values() if p.minimal_mode]
        return list(self._by_id.values())

    def function_definitions(self, mode: str = AgentMode.STANDARD) -> list[dict[str, Any]]:
        return [p.function_definition() for p in self.for_mode(mode)]

    def descriptors(self, mode: str | None = None) -> list[dict[str, Any]]:
        items = self.for_mode(mode) if mode else self.all()
        return [p.descriptor() for p in items]

    def __len__(self) -> int:
        return len(self._by_id)


#: 全局注册表（进程内单例，和 Java 版的 Spring 单例等价）
REGISTRY = PluginRegistry()

#: 工具类清单：各工具模块 import 时把类登记进来，启动时由 loader 统一实例化。
#: 用"显式登记"而不是目录扫描：扫描要遍历文件系统，启动慢且顺序不确定。
TOOL_CLASSES: list[type[ToolPlugin]] = []


def tool(cls: type[ToolPlugin]) -> type[ToolPlugin]:
    """装饰器：把一个工具类登记进 TOOL_CLASSES。"""
    TOOL_CLASSES.append(cls)
    return cls


def load_all(workspace: Path | None = None) -> PluginRegistry:
    """实例化所有已登记工具并注册。由 app 启动时调用（显式、无扫描）。"""
    REGISTRY.__init__()          # 重置，便于测试重复调用
    for cls in TOOL_CLASSES:
        try:
            REGISTRY.register(cls(workspace))
        except Exception as e:   # 单个工具构造失败不该拖垮整个启动
            print(f"[插件] 跳过 {cls.__name__}: {e}", flush=True)
    return REGISTRY


# ========================================================================
# 原模块 lionbox/plugins/lifecycle.py
# ========================================================================
"""插件生命周期：插件接口、设置持久化、注册表、加载器、门禁与系统插件。

【契约来源】逐项对照 Java 版 `core/plugin/` 下 13 个文件里除 `Plugin.java` / `PluginKind.java`
之外的部分（后两者已由已就绪的 `plugins/base.py` 覆盖）：

    PluginPaths       → PluginPaths        （插件目录的唯一定位处）
    PluginSettings    → PluginSettings     （用户开关 + 各类插件参数，落盘 settings.json）
    PluginRegistry    → PluginRegistry     （注册/注销/按类型与分类过滤/搜索/统计）
    PluginAutoRegist… → auto_register()    （启动时把技能与工具插件收进注册表）
    PluginBootstrap   → bootstrap_system_plugins()（终端/大循环/子智能体/团队/审查/自动化）
    PluginLoader      → PluginLoader       （外置插件扫描与热插拔）
    PluginGateSpi     → PluginGateSpi      （关掉的插件从工具清单里消失）
    TerminalPlugin    → TerminalPlugin     （常驻终端的限制值）
    AgentLoopPlugin   → AgentLoopPlugin    （大循环参数）
    EventBus          → EventBus           （插件间通信）
    ServiceContainer  → ServiceContainer   （插件间服务注册与发现）

【与 base.py 的关系（重要）】**不另起一套工具注册机制**：工具的收集与实例化仍然走
`plugins/base.py` 的 `TOOL_CLASSES` + `tool()` + `load_all()` + `REGISTRY`。
本模块的 `PluginRegistry` 只是**在它外面包一层**：同一个工具对象既在 `base.REGISTRY` 里
（Agent 主循环要按名字取工具、要 function_definition），也在本注册表的九类索引里
（设置面板要按类分组、门禁要按开关摘工具）。构造时默认就绑到 `base.REGISTRY` 这个单例。

【与 Java 的差异（都是语言差异，不是行为差异）】
  1. 插件加载器扫的是 `*.py` 而不是 `*.jar`：Python 没有 jar，外置插件的等价物是一个
     模块文件或包目录。隔离手段相应从"独立 ClassLoader"换成"独立模块命名空间 +
     丢弃模块引用"（`importlib.util.spec_from_file_location`）。
  2. 事件存储调用改成 Python 版 `events/store.py` 的 `record_event(session_id, event_type,
     data, summary)` 签名；事件类型用 `EventType.PLUGIN_LOADED` / `PLUGIN_UNLOADED`。
  3. `Plugin.PluginType` / `HealthStatus` 是普通类 + 常量（与 base.py 里枚举的写法一致），
     不用 enum.Enum，避免成员值与 Java 名字不一致时序列化出问题。

【窄桩】`events/` 已就绪，所以事件是真实落库的；只有"事件存储实例"需要外部注入，
默认取 `events.store` 里的进程内单例，取不到就退化成内存接收器（见 `_InMemoryEventSink`）。
"""


import importlib.util
import json
import os
import sys
import threading
from pathlib import Path
from typing import Any, Callable, Iterable


# --------------------------------------------------------------------------
# 枚举与常量（与 Java 同名同值）
# --------------------------------------------------------------------------


class PluginType:
    """插件类型：技能 / 工具 / 系统（Java 的 `Plugin.PluginType`）。"""

    SKILL = "SKILL"
    TOOL = "TOOL"
    SYSTEM = "SYSTEM"

    DISPLAY = {SKILL: "技能", TOOL: "工具", SYSTEM: "系统"}
    ALL = (SKILL, TOOL, SYSTEM)

    @staticmethod
    def parse(raw: Any) -> str:
        v = str(raw or "").strip().upper()
        return v if v in PluginType.DISPLAY else PluginType.TOOL


class HealthStatus:
    """插件健康状态（Java 的 `Plugin.HealthStatus`）。"""

    HEALTHY = "HEALTHY"
    DEGRADED = "DEGRADED"
    UNHEALTHY = "UNHEALTHY"

    DISPLAY = {HEALTHY: "健康", DEGRADED: "降级", UNHEALTHY: "不健康"}


# --------------------------------------------------------------------------
# 插件接口
# --------------------------------------------------------------------------


class Plugin:
    """插件统一接口（Java `Plugin`，生命周期：创建 → initialize() → 使用中 → destroy()）。

    全部方法都有默认实现，理由和 Java 一样：现有工具类一行都不改也必须能跑，
    而且外置插件按老接口写也不能因为升级就崩 —— 不实现 = 走默认。
    """

    #: 出厂默认是否开启（真正"默认关"的只有会主动干活的插件：自动化任务、自动审查）
    enabled_by_default: bool = True
    #: 卸载后不重启能不能再装回来（内置插件 False，外置插件 True）
    hot_reloadable: bool = False
    #: 插件来源：builtin（随软件自带）/ external（用户放进插件目录的）
    source: str = "builtin"
    author: str = "Lion-Code"

    @property
    def id(self) -> str:                      # noqa: A003
        raise NotImplementedError

    @property
    def name(self) -> str:
        raise NotImplementedError

    @property
    def description(self) -> str:
        return ""

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def version(self) -> str:
        return "1.0.0"

    @property
    def kind(self) -> str:
        """插件分类（设置面板分组、按类开关用）。

        默认实现是**派生**出来的，这正是"不用改 60 个工具类"的关键：
        工具按「极简模式能不能用」自动分成基础工具/进阶工具，技能类归 SKILL；
        只有终端、大循环、团队这些"系统插件"才需要显式覆盖。
        """
        if self.type == PluginType.SKILL:
            return PluginKind.SKILL
        if isinstance(self, ToolPlugin):
            return PluginKind.BASE_TOOL if self.minimal_mode else PluginKind.ADVANCED_TOOL
        return PluginKind.ADVANCED_TOOL

    @property
    def display_name(self) -> str:
        """界面上显示的名字（默认取 name，工具类给的是给模型看的英文名）。"""
        name = self.name
        return name if name else self.id

    @property
    def tags(self) -> list[str]:
        return []

    @property
    def metadata(self) -> dict[str, Any]:
        return {}

    def initialize(self) -> None:
        """初始化（注册时调用）。"""

    def destroy(self) -> None:
        """销毁（注销时调用）。"""

    def is_initialized(self) -> bool:
        return True

    def health_status(self) -> str:
        return HealthStatus.HEALTHY

    # ---- 给 `/api/plugins` 用的描述（字段名对齐 Java 版）----
    def descriptor(self) -> dict[str, Any]:
        display, desc = PluginKind.DISPLAY.get(self.kind, ("", ""))
        out: dict[str, Any] = {
            "id": self.id,
            "name": self.name,
            "displayName": self.display_name,
            "description": self.description,
            "type": self.type,
            "typeDisplayName": PluginType.DISPLAY.get(self.type, ""),
            "kind": self.kind,
            "kindDisplayName": display,
            "kindDescription": desc,
            "version": self.version,
            "author": self.author,
            "source": self.source,
            "enabledByDefault": self.enabled_by_default,
            "hotReloadable": self.hot_reloadable,
            "tags": list(self.tags),
            "initialized": self.is_initialized(),
            "health": self.health_status(),
        }
        if isinstance(self, ToolPlugin):
            out["category"] = self.category
            out["permission"] = self.permission
            out["minimalMode"] = self.minimal_mode
            out["parameters"] = self.parameters_schema()
        md = self.metadata
        if md:
            out["metadata"] = md
        return out


# --------------------------------------------------------------------------
# 服务容器 / 事件总线
# --------------------------------------------------------------------------


class ServiceContainer:
    """服务容器（插件间的服务注册与发现）。"""

    def __init__(self) -> None:
        self._services: dict[str, Any] = {}
        self._lock = threading.RLock()

    def register_service(self, service_type: Any, instance: Any = None) -> None:
        """注册服务：`register_service(SomeClass, obj)` 或 `register_service("名字", obj)`。"""
        if instance is None and not isinstance(service_type, (str, type)):
            raise ValueError("注册服务需要 (服务类型, 实例) 两个参数")
        key = self._key(service_type)
        with self._lock:
            self._services[key] = instance

    def get_service(self, service_type: Any) -> Any | None:
        with self._lock:
            return self._services.get(self._key(service_type))

    def has_service(self, service_type: Any) -> bool:
        with self._lock:
            return self._key(service_type) in self._services

    def remove_service(self, service_type: Any) -> None:
        with self._lock:
            self._services.pop(self._key(service_type), None)

    def registered_services(self) -> list[str]:
        with self._lock:
            return list(self._services)

    @staticmethod
    def _key(service_type: Any) -> str:
        if isinstance(service_type, str):
            return service_type
        if isinstance(service_type, type):
            return f"{service_type.__module__}.{service_type.__qualname__}"
        return str(service_type)


class Events:
    """内置事件类型常量（与 Java `EventBus.Events` 一致）。"""

    PLUGIN_LOADED = "plugin.loaded"
    PLUGIN_UNLOADED = "plugin.unloaded"
    SESSION_CREATED = "session.created"
    SESSION_DESTROYED = "session.destroyed"
    ADAPTER_SWITCHED = "adapter.switched"
    WORKSPACE_CHANGED = "workspace.changed"
    TOOL_EXECUTED = "tool.executed"
    USER_MESSAGE = "user.message"
    MODEL_RESPONSE = "model.response"


class EventBus:
    """事件总线：解耦的事件发布/订阅机制，用于插件间通信。

    【关于异常】Java 版对每个订阅者单独 try/catch 并记 error 日志 —— 一个订阅者炸了
    不能让别的订阅者收不到事件。这里保持同样的隔离，但**不隐藏**：异常进 `last_errors`，
    也打到控制台（`[事件总线] ...`），排查时看得见。
    """

    def __init__(self) -> None:
        self._subscribers: dict[str, list[Callable[[Any], None]]] = {}
        self._lock = threading.RLock()
        self.last_errors: list[str] = []

    def subscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        with self._lock:
            self._subscribers.setdefault(event_type, []).append(handler)

    def unsubscribe(self, event_type: str, handler: Callable[[Any], None]) -> None:
        with self._lock:
            handlers = self._subscribers.get(event_type)
            if handlers and handler in handlers:
                handlers.remove(handler)

    def publish(self, event_type: str, event_data: Any = None) -> int:
        """发布事件（同步），返回成功处理的订阅者个数。"""
        with self._lock:
            handlers = list(self._subscribers.get(event_type, []))
        handled = 0
        for handler in handlers:
            try:
                handler(event_data)
                handled += 1
            except Exception as e:
                msg = f"事件处理异常: {event_type} - {e}"
                self.last_errors.append(msg)
                print(f"[事件总线] {msg}", flush=True)
        return handled

    def event_types(self) -> list[str]:
        with self._lock:
            return list(self._subscribers)

    def subscriber_count(self, event_type: str) -> int:
        with self._lock:
            return len(self._subscribers.get(event_type, []))


# --------------------------------------------------------------------------
# 插件目录定位
# --------------------------------------------------------------------------


def _config_default_base() -> Path:
    """进程级配置目录（`--config-dir` 会用 `set_default_base` 设它）。

    插件设置、事件存储、模型目录等所有"用户级"路径都该走同一个基准，
    否则会出现"改了配置目录、只有一部分生效"这种最难查的问题。
    """
    try:
        from lionbox.config.store import _default_base
        return Path(_default_base())
    except Exception:                                     # noqa: BLE001
        return Path(os.path.expanduser("~")) / ".lioncode"

class PluginPaths:
    """插件目录的唯一定位处（插件文件、设置文件、开发工程都在它下面）。

    定位顺序（越靠前优先级越高）：
      1. 显式 `plugins_dir`（测试/便携版，指哪打哪）
      2. 环境变量 `LIONBOX_PLUGINS_DIR`（等价 Java 的 `-Dlionbox.plugins.dir`）
      3. `{用户配置目录}/plugins`，其中用户配置目录 = `LIONCODE_HOME` 或 `~/.lioncode`
         —— 和 `AppConfigStore` 的 `app-config.json` 同一套约定（也与
         `tools/shell/terminal_limits.py` 读设置文件的路径保持一致）。

    目录本身**不在这里创建**：只有真要写文件时才 mkdir，否则每次启动都会凭空多出一个空目录。
    """

    ENV_PLUGINS_DIR = "LIONBOX_PLUGINS_DIR"
    ENV_LIONCODE_HOME = "LIONCODE_HOME"
    ENV_SCAN_PATH = "LION_PLUGIN_SCAN_PATH"

    def __init__(self, plugins_dir: str | Path | None = None,
                 scan_path: str | Path | None = None) -> None:
        self._explicit = Path(plugins_dir) if plugins_dir else None
        self._scan_path = str(scan_path) if scan_path else os.environ.get(self.ENV_SCAN_PATH, "")
        self._cached: Path | None = None

    def plugins_dir(self) -> Path:
        if self._cached is None:
            self._cached = self._resolve()
        return self._cached

    def _resolve(self) -> Path:
        if self._explicit is not None:
            return self._explicit.absolute()
        override = os.environ.get(self.ENV_PLUGINS_DIR, "")
        if override.strip():
            return Path(override.strip()).absolute()
        home = os.environ.get(self.ENV_LIONCODE_HOME, "").strip()
        # 【必须跟着进程级配置目录走】插件设置原来只认 `LIONCODE_HOME` / `~/.lioncode`，
        # 而 `--config-dir` 是通过 `config.store.set_default_base()` 设的进程级覆盖 ——
        # 于是"用 --config-dir 起服务"时，插件开关仍然写到 `~/.lioncode/plugins/settings.json`：
        #   · 在受限环境里那个路径写不了 → 保存失败 → 用户点了"启用插件"却**根本没生效**
        #     （实测 `_check_plugin_extras` 的"授权审查 DENY"用例就是这么红的：
        #      设置存不下去 → is_active() 一直 False → 审查永不触发）；
        #   · 更普遍的问题是"两套配置目录"，与配置存储器的行为不一致。
        base = Path(home) if home else _config_default_base()
        return (base / "plugins").absolute()

    def extra_scan_dirs(self) -> list[Path]:
        """额外要扫描的插件目录（老配置项）；只收"真的存在、且和主目录不同"的。"""
        out: list[Path] = []
        if not self._scan_path.strip():
            return out
        try:
            p = Path(self._scan_path.strip()).absolute()
        except OSError:
            return out
        if p != self.plugins_dir() and p.is_dir():
            out.append(p)
        return out

    def scan_dirs(self) -> list[Path]:
        """全部要扫描的目录（主目录在前）。"""
        return [self.plugins_dir(), *self.extra_scan_dirs()]

    def settings_file(self) -> Path:
        """用户开关 + 各类插件参数都存这里。"""
        return self.plugins_dir() / "settings.json"

    def dev_dir(self) -> Path:
        """插件开发模式生成工程的地方（`plugins/dev/<插件id>/`）。"""
        return self.plugins_dir() / "dev"

    def sdk_dir(self) -> Path:
        """插件 SDK 的存放目录（`plugins/sdk/`）。"""
        return self.plugins_dir() / "sdk"

    def invalidate(self) -> None:
        """清掉缓存（测试/换目录时用）。"""
        self._cached = None


# --------------------------------------------------------------------------
# 插件设置
# --------------------------------------------------------------------------


class PluginSettings:
    """插件设置（用户开关 + 各类插件参数）的持久化，存 `{插件目录}/settings.json`。

    【只存"和默认值不一样"的开关】没动过的插件不在文件里出现，这样以后改代码里的
    默认值能自然生效，而不是被一份陈年老配置按在原地。用户明确点过开关的才记下来。

    【绝不能因为设置文件坏了就起不来】用户手改坏一个 JSON 括号，整个软件打不开是最糟的
    失败方式 —— 坏了就当默认设置，并把文件挪到 `settings.json.broken` 留证据。
    """

    # ---- 终端插件默认值（"现在实际行为"的写照，改它等于改所有老用户的行为）----
    DEFAULT_MAX_COMMAND_SECONDS = 300
    DEFAULT_MAX_OUTPUT_BYTES = 200_000

    # ---- 大循环 ----
    DEFAULT_MAX_ITERATIONS = 200
    DEFAULT_TOOL_TIMEOUT_SECONDS = 600
    DEFAULT_SILENT_ROUNDS = 2
    DEFAULT_MAX_TOOLS_PER_ROUND = 0        # 0 = 不限（出厂值）

    # ---- 子智能体 ----
    DEFAULT_SUBAGENT_MAX_DEPTH = 1
    DEFAULT_SUBAGENT_MAX_CONCURRENCY = 3

    def __init__(self, paths: PluginPaths | None = None) -> None:
        self.paths = paths or default_paths()
        self._data: dict[str, Any] = {}
        self._lock = threading.RLock()
        self.load()

    # ---- 加载 / 落盘 ----
    def load(self) -> dict[str, Any]:
        file = self.paths.settings_file()
        data: dict[str, Any] = {}
        if file.is_file():
            try:
                loaded = json.loads(file.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    data = loaded
            except (OSError, ValueError) as e:
                # 坏了就当默认设置，并把文件挪到一边留证据
                print(f"[插件设置] 设置文件解析失败，本次按默认设置运行: {file}（{e}）", flush=True)
                self._backup_broken(file)
        with self._lock:
            self._data = data
        try:
            self.paths.plugins_dir().mkdir(parents=True, exist_ok=True)
        except OSError:
            pass   # 建不出来不影响启动
        return data

    @staticmethod
    def _backup_broken(file: Path) -> None:
        try:
            broken = file.with_name("settings.json.broken")
            os.replace(file, broken)
            print(f"[插件设置] 已把损坏的设置文件改名为: {broken}", flush=True)
        except OSError as e:
            print(f"[插件设置] 备份损坏的设置文件也失败了: {e}", flush=True)

    def save(self) -> None:
        """原子落盘：先写 .tmp 再 replace，避免半截 JSON 让"所有设置丢了"。"""
        file = self.paths.settings_file()
        tmp = file.with_name("settings.json.tmp")
        with self._lock:
            payload = json.dumps(self._data, ensure_ascii=False, indent=2)
        try:
            file.parent.mkdir(parents=True, exist_ok=True)
            tmp.write_text(payload, encoding="utf-8")
            os.replace(tmp, file)
        except OSError as e:
            print(f"[插件设置] 保存插件设置失败: {file}（{e}）", flush=True)

    # ---- 开关 ----
    def enabled_overrides(self) -> dict[str, bool]:
        """用户显式设置过的开关：插件id -> 是否开启。"""
        raw = self._data.get("enabled")
        if not isinstance(raw, dict):
            return {}
        return {str(k): bool(v) for k, v in raw.items() if isinstance(v, bool)}

    def is_enabled(self, plugin: Any, default_value: bool = True) -> bool:
        """这个插件现在开没开。

        没被用户点过 → 用插件自己声明的默认值。这就是"重启后还在"的全部秘密：
        用户点过的才写进文件，没点过的永远跟着代码走。

        参数可以是插件对象，也可以是插件 id（`agent/change.py` 就是按 id 调的）。
        """
        if plugin is None:
            return True
        if isinstance(plugin, str):
            return self.enabled_overrides().get(plugin, default_value)
        pid = getattr(plugin, "id", None)
        if pid is None:
            raise TypeError("is_enabled 需要插件对象或插件 id")
        fallback = getattr(plugin, "enabled_by_default", default_value)
        return self.enabled_overrides().get(pid, bool(fallback))

    def set_enabled(self, plugin_id: str, enabled: bool, default_value: bool = True) -> bool:
        """记下用户的选择；与默认值相同就删掉这条记录（让"以后改默认值"能生效）。"""
        with self._lock:
            raw = self._data.get("enabled")
            mapping = dict(raw) if isinstance(raw, dict) else {}
            if bool(enabled) == bool(default_value):
                mapping.pop(plugin_id, None)
            else:
                mapping[plugin_id] = bool(enabled)
            self._data["enabled"] = mapping
        self.save()
        return bool(enabled)

    # ---- 通用读写 ----
    def section(self, name: str) -> dict[str, Any]:
        """取整个参数段（只读快照，改它不会影响设置）。"""
        raw = self._data.get(name)
        return dict(raw) if isinstance(raw, dict) else {}

    def update_section(self, name: str, updates: dict[str, Any] | None) -> dict[str, Any]:
        """合并写入参数段（只覆盖传进来的键，None 值 = 删除该键），写完立即落盘。"""
        with self._lock:
            merged = self.section(name)
            for k, v in (updates or {}).items():
                if v is None:
                    merged.pop(k, None)
                else:
                    merged[k] = v
            self._data[name] = merged
        self.save()
        return merged

    def put(self, section: str, key: str, value: Any) -> None:
        """直接替换参数段里的一个值（列表用，比如团队成员、自动化任务）。"""
        with self._lock:
            merged = self.section(section)
            if value is None:
                merged.pop(key, None)
            else:
                merged[key] = value
            self._data[section] = merged
        self.save()

    def top(self, key: str) -> Any:
        return self._data.get(key)

    def put_top(self, key: str, value: Any) -> None:
        with self._lock:
            if value is None:
                self._data.pop(key, None)
            else:
                self._data[key] = value
        self.save()

    def int_of(self, section: str, key: str, fallback: int) -> int:
        """int 型读取：字符串数字也认（配置文件常被手改成 "300"）。"""
        return _to_int(self.section(section).get(key), fallback)

    def bool_of(self, section: str, key: str, fallback: bool) -> bool:
        """宽松读布尔：true/false、"true"/"1"/"yes"/"是"/"开" 都认。"""
        v = self.section(section).get(key)
        if isinstance(v, bool):
            return v
        if isinstance(v, str):
            s = v.strip().lower()
            if s in ("true", "1", "yes", "是", "开"):
                return True
            if s in ("false", "0", "no", "否", "关"):
                return False
        return fallback

    def string_of(self, section: str, key: str, fallback: str) -> str:
        v = self.section(section).get(key)
        return fallback if v is None else str(v)

    def list_of(self, section: str, key: str) -> list[dict[str, Any]]:
        """列表读取：元素统一当 Map 用（团队成员、自动化任务都是这种结构）。"""
        raw = self.section(section).get(key)
        if not isinstance(raw, list):
            return []
        return [dict(item) for item in raw if isinstance(item, dict)]

    def snapshot(self) -> dict[str, Any]:
        """全量快照（REST 返回给前端用）。"""
        with self._lock:
            return json.loads(json.dumps(self._data))

    def file(self) -> Path:
        return self.paths.settings_file()


def _to_int(value: Any, fallback: int) -> int:
    if isinstance(value, bool):
        return fallback
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return fallback
    return fallback


# --------------------------------------------------------------------------
# 事件存储（窄接口）
# --------------------------------------------------------------------------


class _InMemoryEventSink:
    """【窄桩】拿不到 `events.store.EventStore` 时的最小事件接收器（内存里攒着）。

    正常运行路径永远走真实的 EventStore；这个兜底只是保证"插件注册"这件事
    不会因为事件存储没就绪而失败（插件系统的第一原则：坏一块不能全废）。
    """

    def __init__(self) -> None:
        self.records: list[dict[str, Any]] = []

    def record_event(self, session_id: str | None, event_type: str,
                     data: dict[str, Any] | None = None, summary: str | None = None) -> Any:
        self.records.append({"sessionId": session_id, "eventType": event_type,
                             "data": data or {}, "summary": summary})
        return None


_SINK_LOCK = threading.RLock()
_SINK_CACHE: Any = None


def default_event_sink() -> Any:
    """取进程内默认事件存储；`events` 包没就绪时退化成内存接收器。"""
    global _SINK_CACHE
    with _SINK_LOCK:
        if _SINK_CACHE is None:
            try:
                from lionbox.events.store import EventStore
                _SINK_CACHE = EventStore()
            except Exception:                       # 尚未就绪 / 目录不可写
                _SINK_CACHE = _InMemoryEventSink()
        return _SINK_CACHE


def set_default_event_sink(sink: Any) -> None:
    """替换默认事件接收器（app 启动时注入真实 EventStore，或测试用假对象）。"""
    global _SINK_CACHE
    with _SINK_LOCK:
        _SINK_CACHE = sink


# --------------------------------------------------------------------------
# 插件注册表
# --------------------------------------------------------------------------


class PluginRegistry__plugins_lifecycle:
    """插件注册表：统一管理所有插件的注册、加载、发现、卸载。

    **工具仍然由 base.py 收集**（`TOOL_CLASSES` + `load_all()`），本类只是把同一批对象
    编上索引，让设置面板、门禁、`/api/plugins` 能按九类分组查询。
    """

    def __init__(self, tool_registry: Any = None, event_sink: Any = None,
                 event_bus: EventBus | None = None,
                 settings: PluginSettings | None = None) -> None:
        self.tools = tool_registry if tool_registry is not None else REGISTRY
        self.event_sink = event_sink
        self.event_bus = event_bus if event_bus is not None else default_event_bus()
        #: 描述里的 `enabled` 要看用户的开关；默认取进程内单例（app 里和系统插件同一份）
        self.settings = settings
        self._plugins: dict[str, Any] = {}
        self._kind_index: dict[str, list[str]] = {k: [] for k in PluginKind.DISPLAY}
        self._category_index: dict[str, list[str]] = {c: [] for c in ToolCategory.ALL}
        self._errors: dict[str, str] = {}
        self._lock = threading.RLock()

    # ---- 注册 / 注销 ----
    def register(self, plugin: Any) -> None:
        pid = plugin.id
        with self._lock:
            if pid in self._plugins:
                print(f"[插件] 插件已存在，将覆盖: {pid}", flush=True)
                self.unregister(pid)
            self._plugins[pid] = plugin
            if isinstance(plugin, ToolPlugin):
                self.tools.register(plugin)
                self._index_add(self._category_index, getattr(plugin, "category", None), pid)

            # 分类索引：getKind() 是派生出来的，但它是插件自己的代码，
            # 第三方插件写崩了不能把注册流程带下去
            try:
                kind = plugin.kind
            except Exception as e:
                kind = PluginKind.ADVANCED_TOOL
                self._errors[pid] = f"kind 抛异常: {e}"
                print(f"[插件] {pid} 的 kind 抛异常，按进阶工具归类: {e}", flush=True)
            self._index_add(self._kind_index, kind, pid)

            # 初始化：第三方插件的 initialize() 里可能连数据库、读文件、起线程 —— 什么都可能抛。
            # 抛了也要留在注册表里（带 error 显示），否则用户看不到自己插件为什么没生效。
            # 【为什么用 getattr 而不是直接调】已就绪的 `base.ToolPlugin` 没有 initialize()
            # （Java 里 ToolPlugin 继承 Plugin 才有）；工具走的是 base 那套契约，
            # 不能因为多了一层插件索引就要求它实现插件接口。
            initializer = getattr(plugin, "initialize", None)
            if callable(initializer):
                try:
                    initializer()
                except Exception as e:
                    self._errors[pid] = f"初始化失败 {type(e).__name__}: {e}"
                    print(f"[插件] 插件初始化失败（已注册但标记为异常）: {pid} - {e}", flush=True)

            # 实现了 AgentSpi 的插件注册后**自动挂上主循环扩展点**（等价 Java 里
            # PluginLoader 对外置插件做的 "instanceof AgentSpi → AgentSpi.register"，
            # 以及系统插件自己 @PostConstruct 里的注册）。卸载时对称地摘掉。
            if isinstance(plugin, AgentSpi):
                register_spi(plugin)

        self._record("PLUGIN_LOADED", pid, {
            "pluginId": pid,
            "pluginName": _safe(lambda: plugin.name, ""),
            "pluginType": _safe(lambda: plugin.type, PluginType.SYSTEM),
            "pluginKind": kind,
        }, f"插件已加载: {_safe(lambda: plugin.name, pid)}")
        self.event_bus.publish(Events.PLUGIN_LOADED, pid)
        print(f"[插件] 插件已注册: {pid} ({kind})", flush=True)

    def unregister(self, plugin_id: str) -> bool:
        """注销插件（热卸载）。"""
        with self._lock:
            removed = self._plugins.pop(plugin_id, None)
        if removed is None:
            print(f"[插件] 尝试注销不存在的插件: {plugin_id}", flush=True)
            return False
        with self._lock:
            if isinstance(removed, ToolPlugin):
                self._drop_from_tool_registry(removed)
            for index in self._kind_index.values():
                if plugin_id in index:
                    index.remove(plugin_id)
            for index in self._category_index.values():
                if plugin_id in index:
                    index.remove(plugin_id)
            self._errors.pop(plugin_id, None)

        # 卸载时把它贡献的 AgentSpi 扩展点也摘掉：不摘的话，卸载后它还会继续
        # 影响工具清单 / 提示词 / 大循环参数（Java 的 PluginLoader 也是这么做的）。
        if isinstance(removed, AgentSpi):
            unregister_spi(removed)

        # destroy() 同样可能抛（比如它要关的句柄早就没了），不能让一次卸载把调用方打挂。
        # 同样用 getattr：工具类只有 base.py 那套契约，不一定有 destroy()。
        destroyer = getattr(removed, "destroy", None)
        if callable(destroyer):
            try:
                destroyer()
            except Exception as e:
                print(f"[插件] 插件 destroy() 抛异常（已忽略）: {plugin_id} - {e}", flush=True)

        self._record("PLUGIN_UNLOADED", plugin_id, {
            "pluginId": plugin_id,
            "pluginName": _safe(lambda: removed.name, ""),
        }, f"插件已卸载: {_safe(lambda: removed.name, plugin_id)}")
        self.event_bus.publish(Events.PLUGIN_UNLOADED, plugin_id)
        print(f"[插件] 插件已注销: {plugin_id}", flush=True)
        return True

    def _drop_from_tool_registry(self, plugin: Any) -> None:
        """把工具从 base 注册表里摘掉。

        【为什么直接动 `_by_id` / `_by_name`】已就绪的 `base.PluginRegistry` 只有
        `register`、没有 `unregister`（Java 版的卸载在 PluginRegistry 里，Python 版
        按契约只做了"收集"这一半）。插件系统要支持热卸载，就必须能摘；
        这里按它的字段名做最小操作，不修改 base.py 一个字。
        """
        by_id = getattr(self.tools, "_by_id", None)
        by_name = getattr(self.tools, "_by_name", None)
        if isinstance(by_id, dict):
            by_id.pop(plugin.id, None)
        if isinstance(by_name, dict):
            name = _safe(lambda: plugin.name, "")
            if by_name.get(name) is plugin:
                by_name.pop(name, None)

    def sync_tools(self, tool_registry: Any = None) -> int:
        """把 base 注册表里已有的工具编进本注册表的索引（启动时与测试时调）。"""
        source = tool_registry if tool_registry is not None else self.tools
        count = 0
        for tool in source.all():
            with self._lock:
                self._plugins[tool.id] = tool
                self._index_add(self._kind_index, _safe(lambda t=tool: t.kind,
                                                        PluginKind.ADVANCED_TOOL), tool.id)
                self._index_add(self._category_index, getattr(tool, "category", None), tool.id)
            count += 1
        return count

    def load_all(self, workspace: Path | None = None) -> "PluginRegistry":
        """实例化全部已登记工具并把它们编进索引。

        【走谁的路】工具侧有自己的装载入口 `lionbox.tools.load()`（显式 import 57 个工具
        模块触发 `@tool` 登记，再调 `base.load_all()`）—— 这里优先用它，因为它才是
        "哪些工具存在"的唯一名单；拿不到（测试环境只 import 了部分工具）就退回
        `base.load_all()`，两条路最终都落到同一个 `base.REGISTRY` 上。
        """
        registry = None
        try:
            from lionbox.tools import load as load_tools_package
            registry = load_tools_package(workspace)
        except Exception as e:
            print(f"[插件] 工具装载入口不可用，退回 base.load_all(): {e}", flush=True)
        if registry is None:
            registry = load_all(workspace)
        self.tools = registry
        self.sync_tools(registry)
        return self

    @staticmethod
    def _index_add(index: dict[str, list[str]], key: Any, value: str) -> None:
        bucket = index.get(str(key))
        if bucket is None:
            bucket = index.setdefault(str(key), [])
        if value not in bucket:
            bucket.append(value)

    def _record(self, event_type: str, session_id: str, data: dict[str, Any],
                summary: str) -> None:
        sink = self.event_sink if self.event_sink is not None else default_event_sink()
        try:
            sink.record_event("system", event_type, data, summary)
        except Exception as e:
            print(f"[插件] 记录事件失败（忽略）: {event_type} - {e}", flush=True)

    # ---- 查询 ----
    def get_by_kind(self, kind: str) -> list[Any]:
        with self._lock:
            ids = list(self._kind_index.get(kind, []))
        return [self._plugins[i] for i in ids if i in self._plugins]

    def kind_counts(self) -> dict[str, int]:
        """每个分类各有几个插件（九类全部返回，哪怕是 0）。"""
        with self._lock:
            return {kind: sum(1 for i in ids if i in self._plugins)
                    for kind, ids in self._kind_index.items()}

    def get_error(self, plugin_id: str) -> str | None:
        return self._errors.get(plugin_id)

    def tool_name_to_plugin_id(self) -> dict[str, str]:
        """工具名 -> 插件ID 的映射（关掉哪个插件，就把它贡献的工具名摘掉）。"""
        out: dict[str, str] = {}
        for tool in self.get_tool_plugins():
            name = _safe(lambda t=tool: t.name, "")
            if name:
                out[name] = tool.id
        return out

    def get_by_id(self, plugin_id: str) -> Any | None:
        return self._plugins.get(plugin_id)

    def get_all_plugins(self) -> list[Any]:
        with self._lock:
            return list(self._plugins.values())

    def get_skill_plugins(self) -> list[Any]:
        return [p for p in self.get_all_plugins() if _safe(lambda p=p: p.type, "") == PluginType.SKILL]

    def get_tool_plugins(self) -> list[ToolPlugin]:
        return [p for p in self.get_all_plugins() if isinstance(p, ToolPlugin)]

    def get_tools_by_category(self, category: str) -> list[ToolPlugin]:
        with self._lock:
            ids = list(self._category_index.get(category, []))
        return [self._plugins[i] for i in ids
                if i in self._plugins and isinstance(self._plugins[i], ToolPlugin)]

    def get_tools_by_mode(self, mode: str) -> list[ToolPlugin]:
        return [t for t in self.get_tool_plugins() if tool_available_in_mode(t, mode)]

    def get_tools_by_mode_and_permission(self, mode: str, permission: str) -> list[ToolPlugin]:
        return [t for t in self.get_tools_by_mode(mode)
                if has_permission(_safe(lambda t=t: t.permission, PermissionLevel.READ_ONLY),
                                  permission)]

    def search_plugins(self, keyword: str) -> list[Any]:
        """搜索插件（按名称、描述、id 模糊匹配）。"""
        lower = (keyword or "").lower()
        out: list[Any] = []
        for p in self.get_all_plugins():
            haystack = " ".join([_safe(lambda p=p: p.name, ""),
                                 _safe(lambda p=p: p.description, ""),
                                 _safe(lambda p=p: p.id, "")]).lower()
            if lower in haystack:
                out.append(p)
        return out

    def is_registered(self, plugin_id: str) -> bool:
        return plugin_id in self._plugins

    def size(self) -> int:
        return len(self._plugins)

    def __len__(self) -> int:
        return len(self._plugins)

    def get_stats(self) -> dict[str, Any]:
        plugins = self.get_all_plugins()
        category_counts: dict[str, int] = {}
        for cat in ToolCategory.ALL:
            count = len(self.get_tools_by_category(cat))
            if count > 0:
                category_counts[cat] = count
        return {
            "totalPlugins": len(plugins),
            "skillCount": sum(1 for p in plugins
                              if _safe(lambda p=p: p.type, "") == PluginType.SKILL),
            "toolCount": sum(1 for p in plugins if isinstance(p, ToolPlugin)),
            "categoryCounts": category_counts,
            "kindCounts": self.kind_counts(),
        }

    # ---- 对外快照（`/api/plugins`）----
    def descriptors(self, mode: str | None = None) -> list[dict[str, Any]]:
        """给 `/api/plugins` 的清单。

        工具沿用 base 的 `descriptor()`（字段名与 Java 工具描述一致），
        系统插件用 `Plugin.descriptor()`，并按用户开关补上 `enabled` 与 `error`。
        """
        settings = self.settings if self.settings is not None else default_settings()
        items: list[dict[str, Any]] = []
        seen: set[str] = set()
        for plugin in self.get_all_plugins():
            if plugin.id in seen:
                continue
            seen.add(plugin.id)
            if mode is not None and isinstance(plugin, ToolPlugin) \
                    and not tool_available_in_mode(plugin, mode):
                continue
            item = plugin.descriptor()
            item["enabled"] = bool(settings.is_enabled(plugin))
            err = self.get_error(plugin.id)
            if err:
                item["error"] = err
            items.append(item)
        return items

    def function_definitions(self, mode: str = AgentMode.STANDARD) -> list[dict[str, Any]]:
        return self.tools.function_definitions(mode)


def _safe(getter: Callable[[], Any], fallback: Any) -> Any:
    """读插件属性时兜异常：第三方插件属性抛异常不该把列表接口打挂。"""
    try:
        return getter()
    except Exception:
        return fallback


def tool_available_in_mode(tool: Any, mode: str) -> bool:
    """工具在某个模式下能不能用。

    【与 Java 的差异】Java 的 `AbstractToolPlugin.isAvailableInMode` 默认按"类别 +
    minimal 标记"判定；Python 版 base.py 把它收敛成一个 `minimal_mode` 布尔（工具类
    自己声明）。这里按 `minimal_mode` 判定，与 base.py 的 `for_mode` 保持同一套规则 ——
    两处规则必须一致，否则"设置面板里禁用"和"下发给模型的清单"会对不上。
    """
    if AgentMode.from_name(mode) == AgentMode.MINIMAL:
        return bool(getattr(tool, "minimal_mode", False))
    return True


def has_permission(required: str, granted: str) -> bool:
    """权限检查。

    【命名映射】Java 的 `ToolPlugin.PermissionLevel` 是
    READ_ONLY / WORKSPACE_WRITE / FULL_ACCESS，而已就绪的 `plugins/base.py` 用的是
    READ_ONLY / WRITE / EXECUTE / DANGEROUS。这里把两套名字对齐成同一把尺子
    （WORKSPACE_WRITE≈WRITE/EXECUTE，FULL_ACCESS≈DANGEROUS），
    而不是改 base.py（它是冻结契约）。
    """
    req = _canonical_permission(required)
    got = _canonical_permission(granted)
    if req == "READ_ONLY":
        return True
    if req == "WORKSPACE_WRITE":
        return got in ("WORKSPACE_WRITE", "FULL_ACCESS")
    return got == "FULL_ACCESS"


def _canonical_permission(value: str) -> str:
    v = str(value or "").strip().upper()
    if v in ("WRITE", "WORKSPACE_WRITE", "EXECUTE"):
        return "WORKSPACE_WRITE"
    if v in ("DANGEROUS", "FULL_ACCESS"):
        return "FULL_ACCESS"
    return "READ_ONLY"


# --------------------------------------------------------------------------
# 自动注册 / 系统插件启动
# --------------------------------------------------------------------------


def auto_register(registry: PluginRegistry__plugins_lifecycle, skill_plugins: Iterable[Any] | None = None,
                  tool_plugins: Iterable[Any] | None = None) -> int:
    """等价 Java `PluginAutoRegistration`：把技能插件与工具插件收进注册表。

    工具默认取 `base.TOOL_CLASSES`（已由 `load_all()` 实例化的那批）——
    这样"谁提供工具"永远只有一处定义。
    """
    skills = list(skill_plugins or [])
    tools = list(tool_plugins) if tool_plugins is not None else [
        p for p in REGISTRY.all()]
    print("[插件] === 插件自动注册开始 ===", flush=True)
    for skill in skills:
        registry.register(skill)
    for tool in tools:
        registry.register(tool)
    total = len(skills) + len(tools)
    print(f"[插件] === 插件自动注册完成 === 共 {total} 个插件"
          f"（{len(skills)} 个技能 + {len(tools)} 个工具）", flush=True)
    return total


def default_system_plugins(settings: PluginSettings | None = None) -> list[Any]:
    """构造 7 个系统插件：终端 / 大循环 / 子智能体 / 智能体团队 / 授权审查 / 自动化 / 改动审核。

    真身分别住在 lifecycle / team / review / automation 里，这里只是把它们凑齐 ——
    等价 Java `PluginBootstrap` 的构造器注入。
    """
    from lionbox.automation.plugin import AutomationPlugin
    from lionbox.team.agent_team import AgentTeamPlugin
    from lionbox.team.subagent import SubAgentPlugin
    from lionbox.plugins.review import ApprovalReviewPlugin, ChangeReviewPlugin

    s = settings or default_settings()
    return [
        TerminalPlugin(s),
        AgentLoopPlugin(s),
        SubAgentPlugin(s),
        AgentTeamPlugin(s),
        ApprovalReviewPlugin(s),
        AutomationPlugin(s),
        ChangeReviewPlugin(),
    ]


def bootstrap_system_plugins(registry: PluginRegistry__plugins_lifecycle,
                             plugins: Iterable[Any] | None = None) -> int:
    """等价 Java `PluginBootstrap`：逐个注册系统插件，逐个兜异常。

    某一个系统插件出问题不能让其余插件陪葬 —— 插件系统的第一原则是"坏一块不能全废"。
    """
    if plugins is None:
        try:
            plugins = default_system_plugins()
        except Exception as e:
            print(f"[插件] 构造系统插件失败（其余功能继续）: {e}", flush=True)
            return 0
    items = list(plugins)
    ok = 0
    for p in items:
        try:
            registry.register(p)
            ok += 1
        except Exception as e:
            print(f"[插件] 系统插件注册失败（其余插件继续）: "
                  f"{_safe(lambda p=p: p.id, '?')} - {e}", flush=True)
    print(f"[插件] === 系统插件注册完成 === {ok}/{len(items)}"
          "（终端 / 大循环 / 子智能体 / 智能体团队 / 授权审查 / 自动化任务 / 改动审核）",
          flush=True)
    return ok


def bootstrap_all(registry: PluginRegistry__plugins_lifecycle | None = None,
                  settings: PluginSettings | None = None,
                  workspace: Path | None = None,
                  session_manager: Any = None,
                  dispatcher: Any = None,
                  config_store: Any = None,
                  start_automation: bool = True,
                  scan_external: bool = True) -> dict[str, Any]:
    """把整个插件体系按 Java 的启动顺序装起来（**app 启动时调这一个就够**）。

    顺序与 Java 一致（每一步都 fail-soft，坏一块不能全废）：
      1. 外置插件扫描（`PluginLoader.init`，等价 `@PostConstruct`）
      2. 工具装载（`registry.load_all` → `tools.load` → `base.load_all`）
      3. 技能（仓库扫描 + 四个兼容壳 + `skill_load` + 技能目录注入 SPI）
      4. 系统插件（终端/大循环/子智能体/团队/审查/自动化/改动审核）
      5. 门禁 SPI（关掉的插件从工具清单里消失）
      6. 自动化轮询（守护线程，每 15 秒一次）

    :return: 一份装配摘要（数量 + 关键对象），日志里也会逐条打印。
    """
    # 【注意别写成 `registry or default_registry()`】PluginRegistry 实现了 __len__，
    # 空注册表是"假值"，`or` 会静默换成一个新实例 —— 调用方随后查自己那个注册表
    # 就会看到一片空白。对象默认值一律用 `is None` 判断。
    s = settings if settings is not None else default_settings()
    reg = registry if registry is not None else default_registry()
    if reg.settings is None:
        reg.settings = s

    summary: dict[str, Any] = {}

    # 1) 外置插件
    loader = PluginLoader(reg, s.paths)
    if scan_external:
        summary["external"] = loader.init()
    summary["loader"] = loader

    # 2) 工具
    # 【load_tools=False 的用途】装配方（`wiring.py`）为了先构造 AgentLoop 已经装过一次了。
    # `load_all()` 会把注册表重置再装一遍，重复调用虽然幂等，但实测日志里每个工具都打两次
    # "插件已存在，将覆盖"，白花启动时间 —— 而"第一次启动也不能慢"是硬要求。
    if load_tools:
        reg.load_all(workspace)
    summary["tools"] = len(reg.get_tool_plugins())

    # 3) 技能
    try:
        from lionbox.skills import bootstrap_skills
        summary["skills"] = bootstrap_skills(reg, session_manager=session_manager, settings=s)
        summary["skills"].pop("spi", None)     # 摘要里不放对象
    except Exception as e:
        print(f"[插件] 技能装配失败（其余功能继续）: {e}", flush=True)
        summary["skills"] = {"error": str(e)}

    # 4) 系统插件
    summary["systemPlugins"] = bootstrap_system_plugins(reg, default_system_plugins(s))

    # 5) 门禁
    gate = PluginGateSpi(reg, s)
    register_spi(gate)
    print("[插件] 插件开关门禁已挂到 Agent 主循环（关掉的插件不会出现在工具清单里）", flush=True)
    summary["gate"] = gate

    # 6) 自动化轮询
    if start_automation:
        try:
            from lionbox.automation import AutomationRunner
            runner = AutomationRunner(registry=reg, settings=s, session_manager=session_manager,
                                      dispatcher=dispatcher, config_store=config_store)
            runner.start()
            summary["automation"] = runner
        except Exception as e:
            print(f"[插件] 自动化轮询启动失败（其余功能继续）: {e}", flush=True)
            summary["automation"] = None

    summary["stats"] = reg.get_stats()
    print(f"[插件] 插件体系装配完成：{summary['stats']['totalPlugins']} 个插件"
          f"（工具 {summary['stats']['toolCount']}，技能 {summary['stats']['skillCount']}）",
          flush=True)
    return summary


# --------------------------------------------------------------------------
# 插件加载器（外置插件）
# --------------------------------------------------------------------------


class LoadedSource:
    """一个已加载的外置插件来源（等价 Java 的 `PluginLoader.LoadedJar`）。"""

    __slots__ = ("source_key", "path", "module", "plugin_ids")

    def __init__(self, source_key: str, path: Path, module: Any, plugin_ids: list[str]) -> None:
        self.source_key = source_key
        self.path = path
        self.module = module
        self.plugin_ids = plugin_ids


class PluginLoadFailure:
    """某个来源 / 某个类加载失败（坏插件也要在界面上看得见）。"""

    __slots__ = ("source", "plugin_id", "message")

    def __init__(self, source: str, plugin_id: str | None, message: str) -> None:
        self.source = source
        self.plugin_id = plugin_id
        self.message = message

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"jar": self.source, "message": self.message}
        if self.plugin_id:
            out["pluginId"] = self.plugin_id
        return out


class ScanReport:
    """扫描报告（等价 Java `PluginLoader.ScanReport`）。"""

    __slots__ = ("loaded_count", "errors")

    def __init__(self, loaded_count: int, errors: list[str]) -> None:
        self.loaded_count = loaded_count
        self.errors = errors

    def error_count(self) -> int:
        return len(self.errors)

    def __repr__(self) -> str:
        return f"ScanReport(loaded={self.loaded_count}, errors={len(self.errors)})"


class PluginLoader:
    """外置插件加载器（热插拔的落地部分）。

    【Python 版怎么"装插件"】Java 扫 `*.jar` 并用独立 ClassLoader 隔离；Python 没有 jar，
    等价物是插件目录下的 `*.py` 或含清单的包目录。发现插件类的三种方式：

      1. 清单 `lionbox-plugin.json`：`{"main": "plugin.py", "classes": ["MyTool"]}`
         （单文件来源用同名的 `<模块名>.lionbox-plugin.json`）
      2. 兼容 Java 的 `lionbox-plugin.properties`：`plugin.main=...` / `plugin.class=...`
      3. 模块自己声明的 `PLUGIN_CLASSES = [...]`（最省事，推荐）

    **只扫插件目录第一层**：`dev/` 下面是插件开发模式生成、用户正在改的工程，
    绝不能顺手加载进来（和 Java 版只扫第一层 jar 同一个理由）。

    **一条铁律**：插件目录不存在 / 是空的 / 某个插件文件是坏的，都不能让应用起不来。
    最坏的结果应该只是"列表里多了一条红色错误"，而不是"软件打不开了"。
    """

    MANIFEST_JSON = "lionbox-plugin.json"
    MANIFEST_PROPS = "lionbox-plugin.properties"
    ENTRY_MODULE = "__init__.py"
    ENV_HOT_RELOAD = "LIONBOX_PLUGIN_HOT_RELOAD"

    def __init__(self, registry: PluginRegistry__plugins_lifecycle | None = None,
                 paths: PluginPaths | None = None, hot_reload: bool | None = None) -> None:
        self.registry = registry or default_registry()
        self.paths = paths or default_paths()
        if hot_reload is None:
            raw = os.environ.get(self.ENV_HOT_RELOAD, "true").strip().lower()
            hot_reload = raw not in ("false", "0", "no", "off")
        self.hot_reload_enabled = bool(hot_reload)
        self._loaded: dict[str, LoadedSource] = {}
        self._plugin_to_source: dict[str, str] = {}
        self._failures: list[PluginLoadFailure] = []
        self._lock = threading.RLock()

    # ---- 加载 ----
    def init(self) -> ScanReport:
        print(f"[插件] 插件加载器已初始化，热加载: {self.hot_reload_enabled}，"
              f"插件目录: {self.paths.plugins_dir()}", flush=True)
        try:
            return self.scan_and_load()
        except Exception as e:
            print(f"[插件] 启动时扫描插件目录失败（忽略，应用继续启动）: {e}", flush=True)
            self._failures.append(PluginLoadFailure("-", None, f"扫描失败: {e}"))
            return ScanReport(0, [f"扫描失败: {e}"])

    def scan_and_load(self) -> ScanReport:
        """扫描插件目录并加载其中的插件来源。"""
        errors: list[str] = []
        total = 0
        for directory in self.paths.scan_dirs():
            if not directory.is_dir():
                # 【不是错误】出厂状态就是这样：还没人放过插件
                continue
            try:
                candidates = sorted(
                    [p for p in directory.iterdir()
                     if (p.is_file() and p.suffix.lower() == ".py"
                         and not p.name.startswith("_"))
                     or (p.is_dir() and (p / self.MANIFEST_JSON).is_file())],
                    key=lambda p: p.name)
            except OSError as e:
                errors.append(f"扫描失败 {directory}: {e}")
                continue
            for candidate in candidates:
                total += self._load_source(candidate, errors)
        print(f"[插件] 插件扫描完成: 加载 {total} 个插件（{len(errors)} 个问题）", flush=True)
        return ScanReport(total, errors)

    def _load_source(self, path: Path, errors: list[str]) -> int:
        key = str(path.absolute())
        if key in self._loaded:
            return 0
        name = path.name
        try:
            entry, class_names = self._read_manifest(path)
            module = self._import_source(path, entry, class_names)
            declared = list(getattr(module, "PLUGIN_CLASSES", []) or [])
            if not declared:
                # 不是错误，只是这个文件里没有插件
                print(f"[插件] 插件来源中没有发现插件类: {name}", flush=True)
                return 0

            registered: list[str] = []
            for candidate in declared:
                try:
                    plugin = candidate() if isinstance(candidate, type) else candidate
                    if not hasattr(plugin, "id"):
                        continue
                    if self.registry.is_registered(plugin.id):
                        msg = f"插件ID冲突，跳过: {plugin.id}"
                        errors.append(f"{msg}（来源: {name}）")
                        self._failures.append(PluginLoadFailure(name, plugin.id, msg))
                        continue
                    plugin.source = "external"
                    plugin.hot_reloadable = True
                    self.registry.register(plugin)
                    registered.append(plugin.id)
                except Exception as e:
                    # 【一个类炸了不能带走整个来源】其它插件类继续加载
                    msg = f"类加载失败: {candidate} - {e}"
                    errors.append(msg)
                    self._failures.append(PluginLoadFailure(name, str(candidate), msg))
            if registered:
                self._loaded[key] = LoadedSource(key, path, module, registered)
                for pid in registered:
                    self._plugin_to_source[pid] = key
                print(f"[插件] 外置插件已加载: {name}（{len(registered)} 个插件）", flush=True)
            return len(registered)
        except Exception as e:
            print(f"[插件] 读取插件来源失败（忽略它，应用继续）: {name} - {e}", flush=True)
            errors.append(f"插件来源读取失败: {name} - {e}")
            self._failures.append(PluginLoadFailure(name, None, f"插件来源读取失败: {e}"))
            return 0

    def _read_manifest(self, path: Path) -> tuple[str | None, list[str]]:
        """读清单：返回 `(入口文件相对路径, 声明的插件类名列表)`。

        目录来源看 `lionbox-plugin.json` 的 `main`（默认 `__init__.py`），
        单文件来源看同名的 `<模块名>.lionbox-plugin.json`（可选，不写就用模块自己的
        `PLUGIN_CLASSES`）。还兼容 Java 老写法的 `lionbox-plugin.properties`。
        """
        if path.is_dir():
            manifest = path / self.MANIFEST_JSON
            if not manifest.is_file():
                manifest = path / self.MANIFEST_PROPS
        else:
            manifest = path.with_name(path.stem + "." + self.MANIFEST_JSON)
            if not manifest.is_file():
                manifest = path.with_name(path.stem + "." + self.MANIFEST_PROPS)

        entry: str | None = None
        raw_names: list[str] = []
        if manifest.is_file():
            try:
                if manifest.suffix == ".json":
                    data = json.loads(manifest.read_text(encoding="utf-8"))
                    if isinstance(data, dict):
                        main = data.get("main")
                        entry = str(main) if main else None
                        values = data.get("classes", [])
                        raw_names = [str(v) for v in values] if isinstance(values, list) else []
                else:
                    for line in manifest.read_text(encoding="utf-8").splitlines():
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        key, _, value = line.partition("=")
                        if key.strip() == "plugin.main" and value.strip():
                            entry = value.strip()
                        if key.strip() in ("plugin.class", "plugin.classes", "plugins"):
                            raw_names.extend(part.strip() for part in
                                             value.replace(";", ",").replace(" ", ",").split(",")
                                             if part.strip())
            except (OSError, ValueError) as e:
                raise RuntimeError(f"读取插件清单失败: {e}") from e
        return entry, raw_names

    def _import_source(self, path: Path, entry: str | None, raw_names: list[str]) -> Any:
        """把插件来源 import 成一个独立模块命名空间（等价"独立 ClassLoader"）。"""
        if path.is_dir():
            target = (path / (entry or self.ENTRY_MODULE))
        else:
            target = path
        if not target.is_file():
            raise RuntimeError(f"清单里写的入口文件不存在: {target}")
        mod_name = f"lionbox_ext_{path.stem}_{abs(hash(str(target))) % 100000}"
        # 包目录形式（有 __init__.py）用包语义加载，单文件用模块语义
        is_package = path.is_dir() and target.name == self.ENTRY_MODULE
        if is_package:
            spec = importlib.util.spec_from_file_location(
                mod_name, target, submodule_search_locations=[str(path)])
        else:
            spec = importlib.util.spec_from_file_location(mod_name, target)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"无法加载插件模块: {target}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module        # 让模块内的相对 import / dataclass 能工作
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(mod_name, None)
            raise
        if raw_names:
            resolved: list[Any] = []
            for raw in raw_names:
                short = raw.rsplit(".", 1)[-1]
                obj = getattr(module, short, None)
                if obj is None:
                    raise RuntimeError(f"清单里声明的插件类在模块里找不到: {raw}")
                resolved.append(obj)
            module.__dict__["_RESOLVED_PLUGIN_CLASSES"] = resolved
            module.PLUGIN_CLASSES = resolved
        return module

    # ---- 卸载 ----
    def load_plugin(self, plugin: Any) -> bool:
        if self.registry.is_registered(plugin.id):
            print(f"[插件] 插件已存在: {plugin.id}", flush=True)
            return False
        self.registry.register(plugin)
        return True

    def load_plugins(self, plugins: Iterable[Any]) -> int:
        items = list(plugins)
        loaded = sum(1 for p in items if self.load_plugin(p))
        print(f"[插件] 批量加载完成: {loaded}/{len(items)}", flush=True)
        return loaded

    def unload_plugin(self, plugin_id: str) -> bool:
        """卸载插件：外置的连模块一起丢掉，内置的只是从注册表里摘掉。"""
        key = self._plugin_to_source.get(plugin_id)
        if key is not None:
            return self.unload_source(key) > 0
        return self.registry.unregister(plugin_id)

    def unload_source(self, source_key: str) -> int:
        """卸载一整个来源：它的全部插件都要摘掉，最后丢弃模块引用。"""
        with self._lock:
            state = self._loaded.pop(source_key, None)
        if state is None:
            return 0
        removed = 0
        for pid in state.plugin_ids:
            plugin = self.registry.get_by_id(pid)
            if plugin is not None:
                unregister_spi(plugin)          # SPI 也要摘，否则卸载后还在影响主循环
            if self.registry.unregister(pid):
                removed += 1
            self._plugin_to_source.pop(pid, None)
        # 丢弃模块：下次加载才能拿到新版本（等价 Java 关掉 ClassLoader）
        mod_name = getattr(state.module, "__name__", None)
        if mod_name:
            sys.modules.pop(mod_name, None)
        print(f"[插件] 插件来源已卸载: {state.path.name}"
              f"（摘掉 {removed} 个插件，模块已丢弃）", flush=True)
        return removed

    def unload_all_external(self) -> int:
        with self._lock:
            keys = list(self._loaded)
        return sum(self.unload_source(k) for k in keys)

    def reload_plugin(self, plugin_id: str, new_version: Any) -> bool:
        if not self.hot_reload_enabled:
            print("[插件] 热加载已禁用", flush=True)
            return False
        self.registry.unregister(plugin_id)
        self.registry.register(new_version)
        print(f"[插件] 插件已热重载: {plugin_id}", flush=True)
        return True

    def reload(self) -> ScanReport:
        """重新扫描：先卸掉所有外置插件，再从头扫一遍。"""
        self.unload_all_external()
        self._failures.clear()
        return self.scan_and_load()

    # ---- 查询 ----
    def get_loaded_count(self) -> int:
        return self.registry.size()

    def is_hot_reload_enabled(self) -> bool:
        return self.hot_reload_enabled

    def origin(self, plugin_id: str) -> dict[str, Any] | None:
        """外置插件的来源信息（内置插件返回 None）。"""
        key = self._plugin_to_source.get(plugin_id)
        if key is None:
            return None
        state = self._loaded.get(key)
        path = state.path if state else Path(key)
        return {"jarName": path.name, "path": str(path)}

    def get_failures(self) -> list[dict[str, Any]]:
        return [f.to_dict() for f in self._failures]

    def loaded_source_names(self) -> list[str]:
        return list(self._loaded)


# --------------------------------------------------------------------------
# Agent 主循环扩展点（SPI）
# --------------------------------------------------------------------------


class AgentSpi:
    """Agent 主循环扩展点（Java `core/agent/spi/AgentSpi`）。

    【为什么走 SPI 而不是改 AgentLoop】AgentLoop 是所有功能共用的主循环，
    每个功能都去改它必然天天冲突。各功能只实现自己关心的那一个方法就够了。
    """

    def spi_name(self) -> str:
        return self.__class__.__name__

    def order(self) -> int:
        """排序权重（小的先跑）。默认 100。"""
        return 100

    def filter_tool_names(self, session_id: str | None, names: set[str]) -> set[str]:
        """决定这一轮下发给模型的工具清单。"""
        return names

    def extra_system_sections(self, session_id: str | None, workspace_path: str | None,
                              user_message: str | None) -> list[str]:
        """往系统提示词追加段落。"""
        return []

    def transform_user_message(self, session_id: str | None, user_message: str) -> str:
        """改写用户消息（例如展开 @ 引用）。"""
        return user_message

    def loop_options(self, session_id: str | None) -> dict[str, Any]:
        """覆盖主循环参数（最大轮次 / 工具超时 / 空转容忍）。"""
        return {}


_SPIS: list[AgentSpi] = []
_SPI_LOCK = threading.RLock()


def register_spi(spi: AgentSpi) -> None:
    with _SPI_LOCK:
        if spi not in _SPIS:
            _SPIS.append(spi)


def unregister_spi(spi: AgentSpi) -> None:
    with _SPI_LOCK:
        if spi in _SPIS:
            _SPIS.remove(spi)


def registered_spis() -> list[AgentSpi]:
    with _SPI_LOCK:
        return sorted(_SPIS, key=lambda s: (s.order(), _spi_label(s)))


def filter_tool_names(session_id: str | None, names: Iterable[str]) -> set[str]:
    """依次过所有 SPI 的工具过滤（门禁 order=10，排在最前）。

    【为什么用 getattr】扩展点是给插件实现的，插件可能只写了自己关心的那一个方法
    （Java 侧靠接口的 default 方法兜底；Python 这里 duck-typing，缺方法就当"不处理"）。
    """
    current = set(names)
    for spi in registered_spis():
        handler = getattr(spi, "filter_tool_names", None)
        if not callable(handler):
            continue
        try:
            current = set(handler(session_id, current))
        except Exception as e:
            print(f"[插件] SPI {_spi_label(spi)} 过滤工具清单失败（忽略它）: {e}", flush=True)
    return current


def collect_extra_sections(session_id: str | None, workspace_path: str | None,
                           user_message: str | None) -> list[str]:
    """收集所有 SPI 追加的系统提示词段落（按 order 排序，技能目录排在后面）。"""
    out: list[str] = []
    for spi in registered_spis():
        handler = getattr(spi, "extra_system_sections", None)
        if not callable(handler):
            continue
        try:
            for section in handler(session_id, workspace_path, user_message) or []:
                if section and str(section).strip():
                    out.append(str(section))
        except Exception as e:
            print(f"[插件] SPI {_spi_label(spi)} 追加提示词段落失败（忽略它）: {e}", flush=True)
    return out


def transform_user_message(session_id: str | None, user_message: str) -> str:
    text = user_message
    for spi in registered_spis():
        handler = getattr(spi, "transform_user_message", None)
        if not callable(handler):
            continue
        try:
            text = handler(session_id, text)
        except Exception as e:
            print(f"[插件] SPI {_spi_label(spi)} 改写用户消息失败（忽略它）: {e}", flush=True)
    return text


def loop_options(session_id: str | None = None) -> dict[str, Any]:
    """合并所有 SPI 给出的主循环参数（后注册的覆盖先注册的）。"""
    merged: dict[str, Any] = {}
    for spi in registered_spis():
        handler = getattr(spi, "loop_options", None)
        if not callable(handler):
            continue
        try:
            merged.update(handler(session_id) or {})
        except Exception as e:
            print(f"[插件] SPI {_spi_label(spi)} 提供大循环参数失败（忽略它）: {e}", flush=True)
    return merged


def _spi_label(spi: Any) -> str:
    """SPI 的名字（第三方插件没实现 spi_name、或它抛异常，都不能让日志挂掉）。"""
    name = getattr(spi, "spi_name", None)
    if callable(name):
        try:
            return str(name())
        except Exception as e:
            print(f"[插件] SPI {type(spi).__name__} 的 spi_name() 抛异常（已忽略）: {e}", flush=True)
    return type(spi).__name__


# --------------------------------------------------------------------------
# 门禁 SPI：关掉的插件不出现在工具清单里
# --------------------------------------------------------------------------


class PluginGateSpi(AgentSpi):
    """把"用户在设置里关掉的插件"翻译成"下发给模型的工具清单里没有它"。

    【为什么这是插件系统能不能用的关键一环】只把开关存进文件、界面上显示个灰点，
    那是假开关：模型照样会去调那个工具。真正生效必须**在提示词层面**消失 ——
    工具清单是模型唯一知道"自己会什么"的途径，清单里没有，它就压根不会去试，
    也就不会出现"调一次 ❌、再换写法调一次 ❌"的烧轮次现象。
    """

    def __init__(self, registry: PluginRegistry__plugins_lifecycle | None = None,
                 settings: PluginSettings | None = None) -> None:
        self.registry = registry or default_registry()
        self.settings = settings or default_settings()

    def spi_name(self) -> str:
        return "插件开关门禁"

    def order(self) -> int:
        """排在最前面：别的 SPI 拿到的是"已经按开关过滤过"的清单。"""
        return 10

    def filter_tool_names(self, session_id: str | None, names: set[str]) -> set[str]:
        if not names:
            return names
        name_to_plugin = self.registry.tool_name_to_plugin_id()
        kept = set(names)
        dropped: set[str] = set()

        # 1) 终端插件：它不是工具本身，而是"一组 shell 工具 + 它们的限制"。
        #    它被关掉时，它管的这一组工具要一起摘掉（否则"关掉终端插件"就成了空话）。
        if not self._is_enabled(TerminalPlugin.PLUGIN_ID):
            for owned in TerminalPlugin.OWNED_TOOL_NAMES:
                if owned in kept:
                    kept.discard(owned)
                    dropped.add(owned)

        # 2) 单个工具插件：关掉谁就摘掉谁贡献的工具
        for name in names:
            plugin_id = name_to_plugin.get(name)
            if plugin_id is None or name not in kept:
                continue
            if not self._is_enabled(plugin_id):
                kept.discard(name)
                dropped.add(name)

        if dropped:
            print(f"[插件] 按插件开关摘掉 {len(dropped)} 个工具: {sorted(dropped)}", flush=True)
        return kept

    def _is_enabled(self, plugin_id: str) -> bool:
        """查不到插件实例时按"开"处理（启动瞬间注册表还没填好，全砍掉会吓人）。"""
        plugin = self.registry.get_by_id(plugin_id)
        if plugin is None:
            return True
        return self.settings.is_enabled(plugin)


# --------------------------------------------------------------------------
# 系统插件：终端
# --------------------------------------------------------------------------


class TerminalPlugin(Plugin):
    """终端插件：常驻终端的行为约束（超时、输出上限）。

    它本身不提供工具（`execute_command` 仍然是各自的 `ToolPlugin`），
    它管的是**这个工具怎么跑**；关掉它会把这个工具从清单里摘掉。

    【与 tools/shell/terminal_limits.py 的关系】那边是工具层的读取实现（按 mtime 缓存
    读 `settings.json` 的 terminal 段），语义与本类完全一致；本类是插件层的真身
    （设置面板里那个可开关、可改参数的条目）。两者读同一个文件、同一批默认值。
    """

    PLUGIN_ID = "plugin.terminal"

    #: 这个插件"管着"的工具名：关掉插件 = 这几个工具一起从清单里消失
    #: 【2026-10】run_background / stop_background 已随工具削减删除，只剩 execute_command。
    OWNED_TOOL_NAMES = frozenset({"execute_command"})

    def __init__(self, settings: PluginSettings | None = None) -> None:
        self.settings = settings or default_settings()

    @property
    def id(self) -> str:                      # noqa: A003
        return self.PLUGIN_ID

    @property
    def name(self) -> str:
        return "terminal"

    @property
    def display_name(self) -> str:
        return "终端"

    @property
    def description(self) -> str:
        return "常驻终端：限制每条命令最长运行时间、最多输出多少字节（超出截断并告知模型）"

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.TERMINAL

    # ---- 限制值：每次都从设置里现读 ----
    def max_command_seconds(self) -> int:
        """一条命令最多跑多少秒（0 或负数没有意义，回落默认值）。

        【为什么不做成字段缓存】用户在设置面板把 300 改成 30，必须**下一条命令**就生效。
        """
        v = self.settings.int_of("terminal", "maxCommandSeconds",
                                 PluginSettings.DEFAULT_MAX_COMMAND_SECONDS)
        return v if v > 0 else PluginSettings.DEFAULT_MAX_COMMAND_SECONDS

    def max_output_bytes(self) -> int:
        """一条命令最多带回多少字节。0 = 不限制（老行为）。"""
        v = self.settings.int_of("terminal", "maxOutputBytes",
                                 PluginSettings.DEFAULT_MAX_OUTPUT_BYTES)
        return max(v, 0)

    def clamp_timeout(self, requested_seconds: int | None) -> int:
        """把工具请求的超时和插件上限取小值（规定优先，否则模型写 99999 就绕过去了）。"""
        limit = self.max_command_seconds()
        if requested_seconds is None or requested_seconds <= 0:
            return limit
        return min(int(requested_seconds), limit)


# --------------------------------------------------------------------------
# 系统插件：Agent 大循环
# --------------------------------------------------------------------------


class AgentLoopPlugin(Plugin, AgentSpi):
    """Agent 大循环插件：控制"Agent 怎么派发工具调用"（轮次上限 / 工具超时 / 空转容忍）。

    【为什么用 SPI 而不是直接改 AgentLoop 的常量】这三个值本质是"策略"，
    走 SPI 之后：插件开 = 用设置里的值，插件关 = AgentLoop 走它自己的默认值。
    """

    PLUGIN_ID = "plugin.agent-loop"

    def __init__(self, settings: PluginSettings | None = None) -> None:
        self.settings = settings or default_settings()

    @property
    def id(self) -> str:                      # noqa: A003
        return self.PLUGIN_ID

    @property
    def name(self) -> str:
        return "agent_loop"

    @property
    def display_name(self) -> str:
        return "Agent 大循环"

    @property
    def description(self) -> str:
        return "控制 Agent 派发工具调用的方式：最大轮次、单个工具超时、连续空转容忍轮数"

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.AGENT_LOOP

    def spi_name(self) -> str:
        return "Agent 大循环插件"

    def order(self) -> int:
        return 100

    # ---- 设置读写（REST 与 AgentLoop 都走这里）----
    def max_iterations(self) -> int:
        v = self.settings.int_of("loop", "maxIterations", PluginSettings.DEFAULT_MAX_ITERATIONS)
        return v if v > 0 else PluginSettings.DEFAULT_MAX_ITERATIONS

    def tool_timeout_seconds(self) -> int:
        v = self.settings.int_of("loop", "toolTimeoutSeconds",
                                 PluginSettings.DEFAULT_TOOL_TIMEOUT_SECONDS)
        return v if v > 0 else PluginSettings.DEFAULT_TOOL_TIMEOUT_SECONDS

    def silent_rounds(self) -> int:
        v = self.settings.int_of("loop", "silentRounds", PluginSettings.DEFAULT_SILENT_ROUNDS)
        return max(v, 0)

    def max_tools_per_round(self) -> int:
        """一轮最多执行几个工具调用（0 = 不限，出厂值）。"""
        v = self.settings.int_of("loop", "maxToolsPerRound",
                                 PluginSettings.DEFAULT_MAX_TOOLS_PER_ROUND)
        return max(v, 0)

    def loop_options(self, session_id: str | None = None) -> dict[str, Any]:
        """把设置交给 AgentLoop；插件被关掉时返回空表 = 回到出厂行为。

        【只回"用户真的在设置里改过的"项】不能把默认值也一起回上去 ——
        回上去就等于**覆盖**了配置文件里的值，`--tool-timeout-seconds=20` 这类启动参数
        会被插件的默认值悄悄顶掉。语义：设置里没写 → 不吭声；写了 → 按用户写的来。
        """
        if not self.settings.is_enabled(self):
            return {}
        section = self.settings.section("loop")
        out: dict[str, Any] = {}
        if "maxIterations" in section:
            out["maxIterations"] = self.max_iterations()
        if "toolTimeoutSeconds" in section:
            out["toolTimeoutSeconds"] = self.tool_timeout_seconds()
        if "silentRounds" in section:
            out["silentRounds"] = self.silent_rounds()
        if "maxToolsPerRound" in section:
            out["maxToolsPerRound"] = self.max_tools_per_round()
        return out


# --------------------------------------------------------------------------
# 进程内单例（等价 Java 的 Spring 单例）
# --------------------------------------------------------------------------
_PATHS: PluginPaths | None = None
_SETTINGS: PluginSettings | None = None
_REGISTRY: PluginRegistry__plugins_lifecycle | None = None
_BUS: EventBus | None = None
_SINGLETON_LOCK = threading.RLock()


def default_paths() -> PluginPaths:
    global _PATHS
    with _SINGLETON_LOCK:
        if _PATHS is None:
            _PATHS = PluginPaths()
        return _PATHS


def default_settings() -> PluginSettings:
    global _SETTINGS
    with _SINGLETON_LOCK:
        if _SETTINGS is None:
            _SETTINGS = PluginSettings(default_paths())
        return _SETTINGS


def default_event_bus() -> EventBus:
    global _BUS
    with _SINGLETON_LOCK:
        if _BUS is None:
            _BUS = EventBus()
        return _BUS


def default_registry() -> PluginRegistry__plugins_lifecycle:
    global _REGISTRY
    with _SINGLETON_LOCK:
        if _REGISTRY is None:
            _REGISTRY = PluginRegistry__plugins_lifecycle()
        return _REGISTRY


def set_default_registry(registry: PluginRegistry__plugins_lifecycle | None) -> None:
    global _REGISTRY
    with _SINGLETON_LOCK:
        _REGISTRY = registry


def set_default_settings(settings: PluginSettings | None) -> None:
    global _SETTINGS
    with _SINGLETON_LOCK:
        _SETTINGS = settings


def reset_singletons() -> None:
    """把全部单例清空（测试用：让下一次 default_*() 重新构造）。"""
    global _PATHS, _SETTINGS, _REGISTRY, _BUS
    with _SINGLETON_LOCK:
        _PATHS = None
        _SETTINGS = None
        _REGISTRY = None
        _BUS = None


# ========================================================================
# 原模块 lionbox/automation/task.py
# ========================================================================
"""一条自动化任务："什么时候、在哪个会话里、干什么"。

【契约来源】逐项对照 Java 版 `core/plugin/automation/AutomationTask.java`：
到点判定 `isDue` 的三种情况、`dueReason` 的文案、宽容的时间解析（`parseTime`）、
`toMap/fromMap` 的键名与脏数据处理全部照抄。

【为什么时间要宽容解析】时间会从界面输入框、REST 参数、手改的 JSON 三个地方进来。
只认一种格式的话，用户写 `2026-09-30 09:00` 就会被判成"没配时间"，
而任务看起来是配好的 —— 这种"静默不触发"最难排查。认不出来返回 None（等于没配）。
"""


import uuid
from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from typing import Any


@dataclass
class AutomationTask:
    """一条自动化任务。

    :param id:           唯一标识
    :param name:         显示名
    :param session_id:   在哪个会话里执行（必须明确：自动化最容易出的事故就是"跑错会话"）
    :param prompt:       要发给模型的指令
    :param enabled:      是否启用
    :param every_seconds: 周期秒数（>0 表示每隔这么久跑一次；0 表示不是周期任务）
    :param at:           一次性任务的执行时刻（ISO-8601；None 表示不是一次性任务）
    :param last_run_at:  上次真正执行的时刻（ISO-8601；None 表示还没跑过）
    """

    id: str                       # noqa: A003
    name: str
    session_id: str = ""
    prompt: str = ""
    enabled: bool = True
    every_seconds: int = 0
    at: str | None = None
    last_run_at: str | None = None

    @staticmethod
    def create(task_id: str | None, name: str | None, session_id: str | None,
               prompt: str | None, enabled: bool | None = None,
               every_seconds: int | None = None, at: str | None = None,
               last_run_at: str | None = None) -> "AutomationTask":
        """新建（id 留空自动生成）。"""
        tid = str(task_id).strip() if task_id is not None and str(task_id).strip() else \
            "task-" + str(uuid.uuid4())[:8]
        tname = str(name).strip() if name is not None and str(name).strip() else "未命名任务"
        every = 0 if every_seconds is None else max(int(every_seconds), 0)
        return AutomationTask(
            id=tid,
            name=tname,
            session_id="" if session_id is None else str(session_id).strip(),
            prompt="" if prompt is None else str(prompt).strip(),
            enabled=True if enabled is None else bool(enabled),
            every_seconds=every,
            at=None if at is None or not str(at).strip() else str(at).strip(),
            last_run_at=(None if last_run_at is None or not str(last_run_at).strip()
                         else str(last_run_at).strip()),
        )

    # ------------------------------------------------------------------
    # 到点判定
    # ------------------------------------------------------------------
    def is_due(self, now: datetime | None) -> bool:
        """这条任务现在到点了吗。

        三种情况：
          * 停用的任务永远不到点；
          * 一次性任务（有 `at`）：到点且还没跑过 → 到点。**跑过就不再触发**
            （不做"每天同一时刻"的猜测，用户想要周期就配周期）；
          * 周期任务（`every_seconds>0`）：从没跑过 → 立刻算到点（用户刚配好就等一个周期
            才动，会让人以为没生效）；跑过 → 距上次执行满一个周期才算到点。
        """
        if not self.enabled or now is None:
            return False
        last = parse_time(self.last_run_at)
        at_instant = parse_time(self.at)
        if at_instant is not None and last is None and now >= at_instant:
            return True
        if self.every_seconds > 0:
            if last is None:
                return True
            return now >= last + timedelta(seconds=self.every_seconds)
        return False

    def due_reason(self, now: datetime | None) -> str:
        """到点的原因（写日志/界面提示用，别让用户猜"它为什么跑了"）。"""
        last = parse_time(self.last_run_at)
        at_instant = parse_time(self.at)
        if at_instant is not None and last is None and now is not None and now >= at_instant:
            return f"到达设定时间 {self.at}"
        if self.every_seconds > 0 and (last is None or (now is not None
                                                        and now >= last + timedelta(
                                                            seconds=self.every_seconds))):
            return "周期任务首次触发" if last is None else f"距上次执行已满 {self.every_seconds} 秒"
        return "未到点"

    # ------------------------------------------------------------------
    # 序列化
    # ------------------------------------------------------------------
    def to_map(self) -> dict[str, Any]:
        """存进 settings.json 的形状（键名与 Java 一字不差）。"""
        return {
            "id": self.id,
            "name": self.name,
            "sessionId": self.session_id,
            "prompt": self.prompt,
            "enabled": self.enabled,
            "everySeconds": self.every_seconds,
            "at": self.at,
            "lastRunAt": self.last_run_at,
        }

    @staticmethod
    def from_map(raw: dict[str, Any] | None) -> "AutomationTask | None":
        """从设置里的一条记录还原；没有 id 的当脏数据丢掉（删不掉也改不了）。"""
        if not raw:
            return None
        task_id = raw.get("id")
        if task_id is None or not str(task_id).strip():
            return None
        return AutomationTask.create(
            str(task_id), _str(raw.get("name")), _str(raw.get("sessionId")),
            _str(raw.get("prompt")), _bool(raw.get("enabled")), _num(raw.get("everySeconds")),
            _str(raw.get("at")), _str(raw.get("lastRunAt")))


def parse_time(raw: str | None) -> datetime | None:
    """宽容解析时间字符串，统一返回**带时区的 UTC** datetime；认不出来返回 None。

    认这几种（Java 版认的三种 + Python 的 ISO 变体）：
      * `2026-09-30T09:00:00Z` / `+08:00`（带时区偏移）
      * `2026-09-30T09:00` / `2026-09-30 09:00`（按本机时区）
      * `2026-09-30`（当天零点，本机时区）
    """
    if raw is None or not str(raw).strip():
        return None
    text = str(raw).strip()
    candidate = text.replace("Z", "+00:00").replace("z", "+00:00").replace(" ", "T")
    # 依次试：完整 ISO（带时区/不带）→ 只有日期（按当天零点、本机时区）
    for parser in (lambda: _to_utc(datetime.fromisoformat(candidate)),
                   lambda: _to_utc(datetime.combine(date.fromisoformat(text[:10]),
                                                   datetime.min.time()))):
        try:
            return parser()
        except ValueError:
            continue
    return None


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _to_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        # 没有时区信息 = 用户按本机时间写的（Java 也是 atZone(systemDefault())）
        return value.astimezone()
    return value.astimezone(timezone.utc)


def _str(value: Any) -> str | None:
    return None if value is None else str(value)


def _bool(value: Any) -> bool | None:
    if isinstance(value, bool):
        return value
    if value is None:
        return None
    return str(value).strip().lower() in ("true", "1", "yes", "是", "开")


def _num(value: Any) -> int | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value.strip())
        except ValueError:
            return None
    return None


__all__ = ["AutomationTask", "now_utc", "parse_time"]


# ========================================================================
# 原模块 lionbox/automation/due.py
# ========================================================================
"""「这条任务该跑了」—— 到点判定的返回值。

【契约来源】`core/plugin/automation/DueTask.java`（record）：
`task` / `reason` / `due_at` 三个字段，外加 `sessionId()` / `prompt()` 两个转发。
`due_at` 是判定时用的时刻，调用方拿它去调 `mark_run(task_id, due_at)`。
"""


from dataclasses import dataclass
from datetime import datetime



@dataclass(frozen=True)
class DueTask:
    task: AutomationTask
    reason: str
    due_at: datetime

    @property
    def session_id(self) -> str:
        """要在哪个会话里跑。"""
        return self.task.session_id

    @property
    def prompt(self) -> str:
        """要发给模型的指令。"""
        return self.task.prompt

    def __repr__(self) -> str:
        return (f"DueTask(task={self.task.id}, reason={self.reason!r}, "
                f"due_at={self.due_at.isoformat()})")


__all__ = ["DueTask"]


# ========================================================================
# 原模块 lionbox/automation/plugin.py
# ========================================================================
"""自动化任务插件：按设定时间/周期，在指定会话里自动执行任务。

【契约来源】逐项对照 Java 版 `core/plugin/automation/AutomationPlugin.java`。

**刻意不做的两件事**（都是为了避免和会话循环打架）：
  1. **不起线程、不起定时器**：真正的执行必须走会话自己的那条串行通道（否则"自动任务"
     和"用户正在发的消息"会同时改同一个会话，最轻是消息乱序，最重是两边各自以为自己在跑）。
     所以这里只提供 `poll_due(now)`：一个**纯函数**，谁在驱动会话谁就来问一句"有到点的吗"。
  2. **不自己推进 lastRunAt**：`poll_due` 反复调用必须返回同样的结果（纯函数才可测、
     才不会被重复调用搞乱），所以"跑完了"这件事由调用方用 `mark_run` 显式回报。
     漏调 `mark_run` 的后果是任务会被重复触发 —— 这一点在接线时必须注意。

（真正在轮询的是 `runner.AutomationRunner`，它按 15 秒一次的节奏调这里的纯函数。）
"""


from datetime import datetime
from typing import Any



class AutomationPlugin(Plugin):
    """自动化任务插件（纯配置 + 纯计算：没配任务时 `poll_due` 永远返回空表）。"""

    PLUGIN_ID = "plugin.automation"

    def __init__(self, settings: PluginSettings | None = None) -> None:
        self.settings = settings or default_settings()

    # ---- 插件元信息 ----
    @property
    def id(self) -> str:                      # noqa: A003
        return self.PLUGIN_ID

    @property
    def name(self) -> str:
        return "automation"

    @property
    def display_name(self) -> str:
        return "自动化任务"

    @property
    def description(self) -> str:
        return "按设定时间或周期，在指定会话里自动执行任务（时间到点判定，执行由主循环驱动）"

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.AUTOMATION

    # ------------------------------------------------------------------
    # 增删改查
    # ------------------------------------------------------------------
    def tasks(self) -> list[AutomationTask]:
        out: list[AutomationTask] = []
        for raw in self.settings.list_of("automation", "tasks"):
            task = AutomationTask.from_map(raw)
            if task is not None:
                out.append(task)
        return out

    def find(self, task_id: str | None) -> AutomationTask | None:
        if task_id is None:
            return None
        for t in self.tasks():
            if t.id == task_id:
                return t
        return None

    def add(self, task_id: str | None, name: str | None, session_id: str | None,
            prompt: str | None, enabled: bool | None = None,
            every_seconds: int | None = None, at: str | None = None) -> AutomationTask:
        """新增任务。

        校验三件事（都是"配错了就永远不会按预期跑"的典型）：会话必须填、指令必须填、
        时间必须能解析。宁可当场报错，也不要存一条永远不触发的任务 ——
        那种任务在界面上看起来一切正常。

        :raises ValueError: 参数不合法
        """
        if session_id is None or not str(session_id).strip():
            raise ValueError("必须指定在哪个会话里执行（sessionId 不能为空）")
        if prompt is None or not str(prompt).strip():
            raise ValueError("任务内容不能为空（prompt 必填）")
        if at is not None and str(at).strip() and parse_time(at) is None:
            raise ValueError(f"时间格式无法识别: {at}"
                             "（建议 ISO-8601，例如 2026-09-30T09:00 或 2026-09-30T09:00:00+08:00）")
        every = 0 if every_seconds is None else int(every_seconds)
        if (at is None or not str(at).strip()) and every <= 0:
            raise ValueError("必须给出「执行时间」或「周期间隔秒数」其中之一")
        created = AutomationTask.create(task_id, name, session_id, prompt, enabled, every, at, None)
        if self.find(created.id) is not None:
            raise ValueError(f"任务ID已存在: {created.id}")
        items = self.settings.list_of("automation", "tasks")
        items.append(created.to_map())
        self.settings.put("automation", "tasks", items)
        print(f"[自动化] 自动化任务已新增: {created.name}（会话 {created.session_id}，"
              f"周期 {created.every_seconds}s，定时 {created.at}）", flush=True)
        return created

    def update(self, task_id: str, patch: dict[str, Any] | None) -> AutomationTask | None:
        """部分更新（只改传进来的键）。

        :raises ValueError: 时间格式认不出来 / 周期秒数不是整数
        """
        old = self.find(task_id)
        if old is None:
            return None
        at = old.at
        if patch is not None and "at" in patch:
            at = None if patch.get("at") is None else str(patch.get("at"))
        if at is not None and str(at).strip() and parse_time(at) is None:
            raise ValueError(f"时间格式无法识别: {at}")
        every = old.every_seconds
        if patch is not None and patch.get("everySeconds") is not None:
            try:
                every = int(str(patch.get("everySeconds")).strip())
            except ValueError:
                raise ValueError(f"周期秒数必须是整数: {patch.get('everySeconds')}") from None
        enabled = old.enabled
        if patch is not None and patch.get("enabled") is not None:
            value = patch.get("enabled")
            enabled = value if isinstance(value, bool) else \
                str(value).strip().lower() in ("true", "1", "yes", "是", "开")
        last_run = old.last_run_at
        if patch is not None and "lastRunAt" in patch:
            last_run = None if patch.get("lastRunAt") is None else str(patch.get("lastRunAt"))
        updated = AutomationTask.create(old.id, _pick(patch, "name", old.name),
                                        _pick(patch, "sessionId", old.session_id),
                                        _pick(patch, "prompt", old.prompt),
                                        enabled, every, at, last_run)
        self._replace(updated)
        return updated

    def remove(self, task_id: str) -> bool:
        """删除任务。"""
        items = self.settings.list_of("automation", "tasks")
        kept: list[dict[str, Any]] = []
        removed = False
        for raw in items:
            task = AutomationTask.from_map(raw)
            if task is not None and task.id == task_id:
                removed = True
                continue
            kept.append(raw)
        if removed:
            self.settings.put("automation", "tasks", kept)
        return removed

    # ------------------------------------------------------------------
    # 到点判定（纯函数，交给驱动循环调用）
    # ------------------------------------------------------------------
    def poll_due(self, now: datetime | None = None) -> list[DueTask]:
        """现在有哪些任务到点了。

        **纯函数**：不改任何状态、不起线程、不发消息。同样的 now 调多少次结果都一样。
        插件被用户关掉时返回空表（关掉就是关掉，不留后门）。
        """
        if not self.settings.is_enabled(self):
            return []
        moment = now if now is not None else now_utc()
        return [DueTask(t, t.due_reason(moment), moment) for t in self.tasks() if t.is_due(moment)]

    def mark_run(self, task_id: str, when: datetime | None = None) -> None:
        """回报"这条任务这次真的跑过了"，把 lastRunAt 推到给定时刻。

        由调用方在执行完之后调（见 `poll_due` 的说明）。
        **只推进、不回退**：乱序调用（旧时刻后到）不会把时间改回去，避免任务被反复触发。
        """
        task = self.find(task_id)
        if task is None:
            return
        moment = when if when is not None else now_utc()
        old = parse_time(task.last_run_at)
        if old is not None and old > moment:
            return
        updated = AutomationTask.create(task.id, task.name, task.session_id, task.prompt,
                                        task.enabled, task.every_seconds, task.at,
                                        moment.isoformat())
        self._replace(updated)
        print(f"[自动化] 自动化任务已执行: {task.name}（下次判定基准 {moment.isoformat()}）",
              flush=True)

    def _replace(self, updated: AutomationTask) -> None:
        items = self.settings.list_of("automation", "tasks")
        for i, raw in enumerate(items):
            task = AutomationTask.from_map(raw)
            if task is not None and task.id == updated.id:
                items[i] = updated.to_map()
        self.settings.put("automation", "tasks", items)


def _pick(patch: dict[str, Any] | None, key: str, fallback: str) -> str:
    if patch is None or key not in patch or patch.get(key) is None:
        return fallback
    return str(patch.get(key))


__all__ = ["AutomationPlugin"]


# ========================================================================
# 原模块 lionbox/automation/runner.py
# ========================================================================
"""自动化任务的"心脏"：定时看有没有到点的任务，到点就把它的 prompt 丢进对应会话。

【契约来源】逐项对照 Java 版 `core/plugin/automation/AutomationRunner.java`：
15 秒轮询、守护线程、`resolveModel()` 的兜底（`lion-models1`）、
"会话不存在就记账跳过"、异常不搞死调度线程 —— 行为全部照抄。

【为什么是"往会话里丢一条消息"而不是别的做法】用户要的是"按设定时间/周期，在会话中
自动执行任务"。会话本身就是这个软件的执行单元：丢一条消息进去，走的就是和用户手打
一模一样的那条链路（队列 → AgentLoop → 工具 → 事件流），用户切回那个会话能看见完整的
执行过程，也能随时点停止。另起一条"后台执行链路"只会造出一个用户看不见、也管不了的黑盒。

【轮询而不改状态】`AutomationPlugin.poll_due` 是**纯函数**（只看不写），
判定完由这里调 `mark_run` 落"上次执行时间"。记账放在 submit 之后**立刻**做 ——
如果等到 future 完成再记，一轮长任务期间会被重复触发。
"""


import threading
from datetime import datetime
from typing import Any


#: 轮询间隔（秒）。任务粒度最细是分钟级，15 秒足够准，也不会白烧 CPU。
POLL_SECONDS = 15

#: 出厂默认模型（`resolve_model` 的兜底值）
DEFAULT_MODEL = "lion-models1"


class NullDispatcher:
    """【窄桩】会话分发器还没就绪时的替身：**明确报错**，不假装成功。

    Java 侧是 `core/queue/SessionDispatcher.submit(sessionId, userMessage, model,
    thinkingLevel, steer)`。Python 版的分发器由 `agent/`+`sessions/` 那两块负责，
    本模块按同一签名调用；拿不到实现时这里抛错，`tick()` 会把它记成"投递失败"，
    而不是静默丢掉一条自动化任务。
    """

    def submit(self, session_id: str, user_message: str, model: str | None = None,
               thinking_level: str | None = None, steer: bool = False) -> Any:
        raise RuntimeError("会话分发器尚未就绪（SessionDispatcher.submit 不可用）："
                           "自动化任务无法投递，请先接上会话队列")


class AutomationRunner:
    """自动化任务的轮询器（守护线程 + 固定延迟）。"""

    def __init__(self, registry=None, settings=None, session_manager=None, dispatcher=None,
                 config_store=None, poll_seconds: int | None = None) -> None:
        self.registry = registry
        self.settings = settings
        self.session_manager = session_manager
        self.dispatcher = dispatcher
        self.config_store = config_store
        self.poll_seconds = int(poll_seconds) if poll_seconds else POLL_SECONDS
        self._thread: threading.Thread | None = None
        self._stop = threading.Event()
        self._warned_no_session_manager = False
        #: 投递记录（自测/诊断用：每次尝试投递都留一行）
        self.deliveries: list[dict[str, Any]] = []

    # ------------------------------------------------------------------
    # 启停
    # ------------------------------------------------------------------
    def start(self) -> None:
        """启动轮询（守护线程：应用关闭时不会被它拖住）。"""
        if self._thread is not None and self._thread.is_alive():
            return
        self._stop.clear()
        self._thread = threading.Thread(target=self._loop, name="lionbox-automation", daemon=True)
        self._thread.start()
        print(f"[自动化] 自动化任务轮询已启动（每 {self.poll_seconds} 秒检查一次）", flush=True)

    def stop(self) -> None:
        self._stop.set()
        thread = self._thread
        if thread is not None and thread.is_alive():
            thread.join(timeout=2.0)
        self._thread = None

    def is_running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _loop(self) -> None:
        """固定延迟：上一轮跑完再等一个间隔（等价 `scheduleWithFixedDelay`）。"""
        while not self._stop.is_set():
            if self._stop.wait(self.poll_seconds):
                return
            self.tick()

    # ------------------------------------------------------------------
    # 一次轮询
    # ------------------------------------------------------------------
    def tick(self) -> int:
        """把到点的任务丢进会话；返回本次投递条数。

        任何异常都不把调度线程搞死（但都会打出来 —— 不静默吞掉）。
        """
        from lionbox.agent.control import ThinkingLevel
        delivered = 0
        try:
            plugin = self.automation_plugin()
            if plugin is None:
                return 0
            due = plugin.poll_due(now_utc())
            for item in due:
                session_id = item.session_id
                if not self._session_exists(session_id):
                    # 会话被删了：不再执行，但仍然记账，让用户自己看到任务"跑不动"
                    print(f"[自动化] 自动化任务 {item.task.id} 指向的会话 {session_id} 不存在，跳过",
                          flush=True)
                    plugin.mark_run(item.task.id, now_utc())
                    self.deliveries.append({"taskId": item.task.id, "sessionId": session_id,
                                            "ok": False, "reason": "会话不存在"})
                    continue
                try:
                    self._dispatcher().submit(session_id, item.prompt, self.resolve_model(),
                                              ThinkingLevel.MEDIUM, False)
                    plugin.mark_run(item.task.id, item.due_at)
                    delivered += 1
                    print(f"[自动化] 自动化任务已投递：{item.task.name} → 会话 {session_id}"
                          f"（{item.reason}）", flush=True)
                    self.deliveries.append({"taskId": item.task.id, "name": item.task.name,
                                            "sessionId": session_id, "prompt": item.prompt,
                                            "reason": item.reason, "ok": True,
                                            "dueAt": _iso(item.due_at)})
                except Exception as e:
                    print(f"[自动化] 自动化任务 {item.task.id} 投递失败: {e}", flush=True)
                    self.deliveries.append({"taskId": item.task.id, "sessionId": session_id,
                                            "ok": False, "reason": str(e)})
        except Exception as e:
            print(f"[自动化] 自动化轮询异常（忽略本轮）: {e}", flush=True)
        return delivered

    # ------------------------------------------------------------------
    # 依赖
    # ------------------------------------------------------------------
    def automation_plugin(self) -> AutomationPlugin | None:
        """取自动化插件；被用户关掉了就什么都不做。"""
        registry = self._registry()
        if registry is None:
            return None
        plugin = registry.get_by_id(AutomationPlugin.PLUGIN_ID)
        if not isinstance(plugin, AutomationPlugin):
            return None
        if not self._settings().is_enabled(plugin):
            return None
        return plugin

    def resolve_model(self) -> str:
        """自动化任务该用哪个模型。

        【为什么不能传 None】`SessionDispatcher.submit` 的第 3 个位置参数就是**模型名**。
        传 None 会让发出去的请求变成 `"model": null`，除了模型名不对，
        上下文窗口预算还会因为 model 为空而取到错的默认值。
        """
        store = self.config_store
        if store is None:
            try:
                from lionbox.config.store import AppConfigStore
                store = AppConfigStore()
            except Exception:
                store = None
        model = store.get("model", None) if store is not None else None
        if isinstance(model, str) and model.strip():
            return model
        return DEFAULT_MODEL

    def _session_exists(self, session_id: str | None) -> bool:
        if not session_id:
            return False
        manager = self._session_manager()
        if manager is None:
            if not self._warned_no_session_manager:
                self._warned_no_session_manager = True
                print("[自动化] 会话管理器不可用，跳过会话存在性校验（任务照常投递）", flush=True)
            return True
        return manager.get_session(session_id) is not None

    def _registry(self):
        if self.registry is None:
            from lionbox.plugins.lifecycle import default_registry
            self.registry = default_registry()
        return self.registry

    def _settings(self):
        if self.settings is None:
            from lionbox.plugins.lifecycle import default_settings
            self.settings = default_settings()
        return self.settings

    def _session_manager(self):
        """【窄桩】取进程内会话管理器；`sessions/manager.py` 就绪时按约定懒取单例。"""
        if self.session_manager is not None:
            return self.session_manager
        try:
            from lionbox.sessions import manager as sessions_manager
        except ImportError:
            return None
        for attr in ("SESSION_MANAGER", "MANAGER", "default_manager"):
            got = getattr(sessions_manager, attr, None)
            if got is None:
                continue
            self.session_manager = got() if callable(got) else got
            return self.session_manager
        return None

    def _dispatcher(self):
        """【窄桩】取会话分发器；找不到就返回 `NullDispatcher`（投递会明确失败）。"""
        if self.dispatcher is None:
            self.dispatcher = default_dispatcher()
        return self.dispatcher


def default_dispatcher():
    """按 `SessionDispatcher.submit` 的约定懒取分发器；没有就返回 `NullDispatcher`。

    【窄桩说明】Java 侧是 `core/queue/SessionDispatcher`（会话串行队列）。
    Python 版的分发器由 `agent/` + `sessions/` 那两块负责，本模块只按同一签名调用。
    这里依次到 `queue` / `sessions` / `agent` 三个包下找它，找不到就用 `NullDispatcher`
    —— 投递会**明确报错**（记成"投递失败"），不会静默丢掉任务。
    """
    import importlib

    for module_name in ("lionbox.queue.dispatcher", "lionbox.sessions.dispatcher",
                        "lionbox.agent.dispatcher"):
        try:
            module = importlib.import_module(module_name)
        except ImportError:
            continue
        for attr in ("SESSION_DISPATCHER", "DISPATCHER", "default_dispatcher", "SessionDispatcher"):
            got = getattr(module, attr, None)
            if got is None:
                continue
            if isinstance(got, type):
                try:
                    return got()
                except Exception:
                    continue
            if hasattr(got, "submit"):
                return got
            if callable(got):
                try:
                    return got()
                except Exception:
                    continue
    return NullDispatcher()


def _iso(moment: datetime | None) -> str | None:
    return None if moment is None else moment.isoformat()


__all__ = ["DEFAULT_MODEL", "POLL_SECONDS", "AutomationRunner", "NullDispatcher",
           "default_dispatcher"]


# ========================================================================
# 原模块 lionbox/automation.py
# ========================================================================
"""自动化任务（对应 Java `core/plugin/automation/`）。

| Java | 这里 |
| --- | --- |
| `AutomationTask` | `task.AutomationTask` |
| `DueTask` | `due.DueTask` |
| `AutomationPlugin` | `plugin.AutomationPlugin` |
| `AutomationRunner` | `runner.AutomationRunner` |

分工很清楚：插件管"什么时候该跑"（纯函数 `poll_due`），runner 管"跑了就记账"
（`mark_run`）并把 prompt 丢进对应会话。启动日志：
`自动化任务轮询已启动（每 15 秒检查一次）`。
"""



__all__ = [
    "AutomationPlugin", "AutomationRunner", "AutomationTask", "DEFAULT_MODEL", "DueTask",
    "NullDispatcher", "POLL_SECONDS", "default_dispatcher", "now_utc", "parse_time",
]


# ========================================================================
# 原模块 lionbox/plugindev/service.py
# ========================================================================
"""插件开发模式：开启后，用户可以在软件里直接生成一个**能加载、能跑**的插件工程。

【契约来源】逐项对照 Java 版 `core/plugin/dev/PluginDevService.java`（546 行）：
开关优先级（运行时设置 > 启动参数）、id 安全校验（挡住 `..` 与路径分隔符）、
"绝不覆盖用户已有工程"、类名驼峰化、按分类生成不同骨架、SDK 导出，语义全部照抄。

三件事：
  1. **开关**：启动参数 `--lionbox.plugin.dev-mode=true`（Python 侧读环境变量
     `LIONBOX_PLUGIN_DEV_MODE`），或运行时用端点改（运行时改动会持久化，重启后仍按上次的选择）；
  2. **脚手架**：`plugins/dev/<插件id>/` 下生成源码 + 清单 + 自检脚本 + README；
  3. **SDK**：把本程序自己的插件接口导出成一份可读的接口清单
     （`plugins/sdk/lionbox-plugin-api.md`）—— 用户照着它写插件不用猜有哪些方法。

【与 Java 的差异（必须说明）】Java 生成的是 **Java 源码 + build.ps1 + `lionbox-plugin-api.jar`**，
因为插件要 `javac` 编译、而接口类藏在 fat jar 的 `BOOT-INF/classes` 里（javac 读不进去，
所以必须抽一个 SDK jar 出来）。Python 版**根本没有编译这一步**：插件就是一个 `.py`
文件，`plugins/PluginLoader` 直接 import 它。所以：
  * 生成的是 `plugin.py`（不是 `XxxTool.java`）；
  * 不生成 build 脚本，改成生成 `check.py`（自检：加载插件并真跑一次工具）；
  * SDK 从"接口 jar"变成"接口清单文档"（内容是从运行中的类里**现取**的，不会过期）。
这一层差异是语言决定的，行为语义（开关、安全校验、不覆盖、分类骨架）保持一致。
"""


import json
import os
import re
from pathlib import Path
from typing import Any


#: 启动参数给的值（`--lionbox.plugin.dev-mode=true` → 环境变量 LIONBOX_PLUGIN_DEV_MODE）
ENV_DEV_MODE = "LIONBOX_PLUGIN_DEV_MODE"

#: 插件 id 的安全白名单：字母开头，只允许字母数字 . _ -，长度 2..64
ID_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9._\-]{1,63}")


class ScaffoldResult:
    """生成插件工程的结果。

    :param path:   工程目录
    :param files:  生成的文件（相对工程目录）
    :param sdk:    SDK 接口清单（生成失败时为 None，此时 README 里说明了怎么手动补）
    """

    __slots__ = ("path", "files", "sdk")

    def __init__(self, path: Path, files: list[str], sdk: Path | None) -> None:
        self.path = path
        self.files = files
        self.sdk = sdk

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {"path": str(self.path), "files": list(self.files)}
        if self.sdk is not None:
            out["sdk"] = str(self.sdk)
        return out


class PluginDevService:
    """插件开发模式服务。"""

    def __init__(self, paths: PluginPaths | None = None, settings: PluginSettings | None = None,
                 dev_mode_by_startup: bool | None = None) -> None:
        self.paths = paths or default_paths()
        self.settings = settings or default_settings()
        if dev_mode_by_startup is None:
            raw = os.environ.get(ENV_DEV_MODE, "false").strip().lower()
            dev_mode_by_startup = raw in ("true", "1", "yes", "on")
        self.dev_mode_by_startup = bool(dev_mode_by_startup)

    # ------------------------------------------------------------------
    # 开关
    # ------------------------------------------------------------------
    def is_dev_mode(self) -> bool:
        """现在是不是开发模式。

        优先级：运行时设置（settings.json 里的 devMode） > 启动参数。
        这样"启动时开了、运行时关掉"能生效，而且关掉之后重启不会又变回开着 ——
        用户点过的选择必须比启动参数大，否则他会觉得这个开关"关不掉"。
        """
        override = self.settings.top("devMode")
        if isinstance(override, bool):
            return override
        if isinstance(override, str):
            return override.strip().lower() in ("true", "1", "yes", "on")
        return self.dev_mode_by_startup

    def set_dev_mode(self, enabled: bool) -> bool:
        """运行时开关（会持久化）。"""
        self.settings.put_top("devMode", bool(enabled))
        print(f"[插件开发] 插件开发模式已{'开启' if enabled else '关闭'}", flush=True)
        return bool(enabled)

    # ------------------------------------------------------------------
    # 脚手架
    # ------------------------------------------------------------------
    def scaffold(self, plugin_id: str, name: str | None = None,
                 kind: str | None = None) -> ScaffoldResult:
        """生成一个最小插件工程。

        :raises ValueError:            参数不合法
        :raises IllegalStateError:     开发模式没开 / 工程目录已存在且不为空
        """
        if not self.is_dev_mode():
            raise IllegalStateError(
                "插件开发模式未开启：请用 --lionbox.plugin.dev-mode=true 启动，"
                "或先调用 POST /api/plugins/dev-mode {\"enabled\": true}")

        safe = self.safe_id(plugin_id)
        plugin_kind = PluginKind.parse(kind)
        if kind is not None and str(kind).strip() and \
                str(kind).strip().upper() not in PluginKind.DISPLAY:
            raise ValueError("未知的插件分类: " + str(kind) + "（可选："
                             + " / ".join(PluginKind.DISPLAY) + "）")

        display_name = name.strip() if name is not None and str(name).strip() else safe
        class_name = camel(safe) + suffix_for(plugin_kind)
        package = "lionbox_plugins." + re.sub(r"[^a-z0-9_]", "_", safe.lower())
        project_dir = self.paths.dev_dir() / safe

        if project_dir.is_dir() and has_any_file(project_dir):
            # 【绝不覆盖】用户可能已经在那儿改了半天代码。想重来就自己删掉目录。
            raise IllegalStateError(f"工程目录已存在且不为空，请先删除或换个 id: {project_dir}")

        project_dir.mkdir(parents=True, exist_ok=True)
        files: list[str] = []

        source = self.render_source(package, class_name, display_name, safe, plugin_kind)
        write(project_dir / "plugin.py", source)
        files.append("plugin.py")

        write(project_dir / "lionbox-plugin.json", json.dumps({
            "id": safe,
            "name": display_name,
            "kind": plugin_kind,
            "main": "plugin.py",
            # 加载器按这个清单实例化插件类（等价 Java 的 META-INF/lionbox-plugin.properties）
            "classes": [class_name],
        }, ensure_ascii=False, indent=2) + "\n")
        files.append("lionbox-plugin.json")

        check = self.render_check(safe, class_name)
        write(project_dir / "check.py", check)
        files.append("check.py")

        sdk = self.ensure_sdk()
        write(project_dir / "README.md",
              self.render_readme(safe, display_name, plugin_kind, class_name, sdk, project_dir))
        files.append("README.md")

        print(f"[插件开发] 插件工程已生成: {project_dir}（{plugin_kind}）", flush=True)
        return ScaffoldResult(project_dir, files, sdk)

    def safe_id(self, plugin_id: str | None) -> str:
        """校验插件ID并当做目录名用。

        【安全】id 直接变成目录名，所以必须在这里挡住 `..` 和路径分隔符 ——
        否则一个 `../../` 就能把文件写到插件目录外面去。
        """
        if plugin_id is None or not str(plugin_id).strip():
            raise ValueError("插件ID不能为空")
        value = str(plugin_id).strip()
        if not ID_PATTERN.fullmatch(value):
            raise ValueError("插件ID只能包含字母、数字、点、下划线、短横线，长度 2-64："
                             + str(plugin_id))
        if ".." in value:
            raise ValueError("插件ID不能包含 .. : " + str(plugin_id))
        return value

    # ------------------------------------------------------------------
    # 源码模板
    # ------------------------------------------------------------------
    def render_source(self, package: str, class_name: str, display_name: str,
                      plugin_id: str, kind: str) -> str:
        if kind == PluginKind.SKILL:
            return skill_template(class_name, display_name, plugin_id)
        if kind in (PluginKind.BASE_TOOL, PluginKind.ADVANCED_TOOL):
            return tool_template(class_name, display_name, plugin_id, kind == PluginKind.BASE_TOOL)
        return system_template(class_name, display_name, plugin_id, kind)

    def render_check(self, plugin_id: str, class_name: str) -> str:
        """生成自检脚本：加载插件、跑一次工具、打印结果（等价 Java 的 build.ps1 那一步）。"""
        return (f'"""插件自检：加载 {plugin_id}（类 {class_name}）并真跑一次工具。\n\n'
                '用法： python check.py   （在工程目录下直接跑）\n'
                '"""\n\n'
                "import sys\n"
                "from pathlib import Path\n\n"
                "HERE = Path(__file__).resolve().parent\n"
                "sys.path.insert(0, str(HERE))       # 插件本体就在隔壁\n"
                "sys.path.insert(0, str(Path.cwd()))  # 在 Lion Code 的 python/ 目录下跑时能找到 lionbox\n\n"
                "try:\n"
                "    import lionbox.plugins.base  # noqa: F401\n"
                "except ImportError:\n"
                "    print('✗ 找不到 lionbox 包：请在 Lion Code 安装目录（或本项目的 python/ 目录）下运行，'\n"
                "          '或先设置 PYTHONPATH 指向它。')\n"
                "    raise SystemExit(2)\n\n"
                "import plugin as mod  # noqa: E402  （插件本体就在隔壁）\n\n\n"
                "def main() -> int:\n"
                "    classes = list(getattr(mod, 'PLUGIN_CLASSES', []))\n"
                "    if not classes:\n"
                "        print('✗ plugin.py 里没有 PLUGIN_CLASSES，加载器发现不了你的插件')\n"
                "        return 1\n"
                "    for cls in classes:\n"
                "        instance = cls()\n"
                "        print(f'✓ 插件可实例化: {instance.id} / {instance.name}'\n"
                "              f'（分类 {instance.kind}，'\n"
                "              f'默认开启 {getattr(instance, \"enabled_by_default\", True)}）')\n"
                "        run = getattr(instance, 'execute', None)\n"
                "        if run is not None:\n"
                "            result = run({'text': 'hello'})\n"
                "            print(f'✓ 工具执行: success={result.success} '\n"
                "                  f'content={result.content or result.error}')\n"
                "    print('下一步：把本目录拷到插件目录，或调 POST /api/plugins/reload')\n"
                "    return 0\n\n\n"
                "if __name__ == '__main__':\n"
                "    raise SystemExit(main())\n")

    def render_readme(self, plugin_id: str, display_name: str, kind: str, class_name: str,
                      sdk: Path | None, project_dir: Path) -> str:
        sdk_line = ("SDK 接口清单已经生成好了：`" + str(sdk) + "`（由本程序导出，照着它写就行）。"
                    if sdk is not None else
                    "SDK 接口清单这次没生成成功（插件目录不可写？）。可以直接读 "
                    "`lionbox/plugins/base.py` 与 `lionbox/plugins/lifecycle.py`，"
                    "里面就是全部接口。")
        return f"""# {display_name}（插件 id: `{plugin_id}`）

这是 Lion Code **插件开发模式**生成的最小插件工程，分类是「{PluginKind.DISPLAY.get(kind, ("", ""))[0]}」。
它现在就能加载、能跑 —— 先跑通一遍，再改成你需要的样子。

## 目录结构

```
{project_dir.name}/
  plugin.py             ← 插件本体（改这里）
  lionbox-plugin.json   ← 清单：声明哪个类是插件（改类名时这里要一起改）
  check.py              ← 自检脚本：加载 + 真跑一次工具
  README.md             ← 你正在看的这个
```

## 加载（三步）

1. 自检：`python check.py`（能打印 `✓` 就说明插件本身没问题）
2. 把本目录整体拷到插件目录（`{self.paths.plugins_dir()}`），或直接在本目录下调
   `POST /api/plugins/reload`
3. 到「设置 → 插件」里确认它出现了、开关是开的；然后让模型调用它试试

**Python 版没有编译步骤** —— 插件就是一个 `.py` 文件，加载器直接 import 它
（Java 版要 javac 编译再打成 jar，那是语言差异）。

{sdk_line}

## 要改的地方

- **插件ID**（`id`）：设置里的开关、日志、卸载都认它，**必须全库唯一**，
  和别的插件重了会被跳过（列表里会出现一条"ID冲突"的错误）。
- **工具名**（`name`）：模型就是按这个名字调用的。改成你想让模型做的事，
  例如 `check_license_header`。别和内置工具重名，重名会让内置那个失效。
- **说明**（`description`）：写在工具清单里给模型看，写清"什么时候该用它"。
- **参数**（`parameters_schema()`）：JSON Schema，`required` 里的参数模型必须给。
- **逻辑**（`execute()`）：真正干活的地方。记住两条约定：
  成功用 `self.success(...)`，失败用 `self.error(...)`；错误信息要写成"能照着改"的话。
- **模式**（`minimal_mode`）：`True` = 极简模式也能用（基础工具），`False` = 只在标准模式
  （进阶工具）。分类就是从它派生出来的，不用另外声明。

## 热插拔是怎么工作的（以及什么时候会不灵）

- 加载：加载器扫插件目录下的 `*.py`（和含清单的包目录），每个来源用**独立的模块命名空间**
  加载，所以你改完再 `reload` 就能生效，不用重启软件。
- 卸载：`DELETE /api/plugins/{id}` 会把插件从注册表里摘掉、丢掉模块引用。
- **注意**：如果你在 `initialize()` 里起了线程、开了端口、注册了全局监听，
  一定要在 `destroy()` 里关掉 —— 丢掉模块引用不会自动帮你收拾这些。
- 插件之间**不要**互相 import 对方的类：每个插件是独立的模块命名空间，
  跨插件引用容易拿到旧对象。要通信就用返回给模型的结果、或事件总线。

## 能插进主循环吗？

能。让插件类**同时继承** `lionbox.plugins.lifecycle.AgentSpi`，注册时它是插件、
跑起来它是扩展点。可用的扩展点（都只要实现你关心的那一个）：

| 方法 | 作用 |
|---|---|
| `filter_tool_names` | 决定这一轮下发给模型的工具清单 |
| `extra_system_sections` | 往系统提示词追加段落 |
| `transform_user_message` | 改写用户消息（例如展开 @ 引用） |
| `loop_options` | 覆盖主循环参数（最大轮次/工具超时/空转容忍） |

> 提示：`extra_system_sections` 里塞的东西每一轮都会进提示词，写短一点。

## 这个骨架的类名

`{class_name}`（在 `plugin.py` 里；改它记得同步改 `lionbox-plugin.json` 的 `classes`）。
"""

    # ------------------------------------------------------------------
    # SDK（插件接口清单）
    # ------------------------------------------------------------------
    def ensure_sdk(self) -> Path | None:
        """生成（或复用）插件 SDK 接口清单；失败返回 None（不该让整个脚手架失败）。

        【为什么是"清单文档"而不是"jar"】见模块 docstring：Java 需要 SDK jar 是因为
        javac 读不进 fat jar；Python 没有编译步骤，用户真正需要的是"有哪些类、哪些方法、
        哪些方法必须实现"。所以这里从**运行中的类**现取签名写成文档 —— 不会过期。
        """
        try:
            return self._ensure_sdk_doc()
        except Exception as e:
            print(f"[插件开发] 生成插件 SDK 失败（脚手架继续，用户可手动看源码）: {e}", flush=True)
            return None

    def _ensure_sdk_doc(self) -> Path:
        sdk_dir = self.paths.sdk_dir()
        sdk_dir.mkdir(parents=True, exist_ok=True)
        target = sdk_dir / "lionbox-plugin-api.md"
        content = sdk_document()
        if target.is_file() and target.read_text(encoding="utf-8") == content:
            return target          # 同一份程序，不用重复写
        target.write_text(content, encoding="utf-8")
        print(f"[插件开发] 插件 SDK 已生成: {target}", flush=True)
        return target


class IllegalStateError(RuntimeError):
    """状态不对（开发模式没开 / 工程目录已被占用）。"""


def suffix_for(kind: str) -> str:
    """按分类给类名加后缀（与 Java `suffixFor` 一致）。"""
    if kind == PluginKind.SKILL:
        return "Skill"
    if kind in (PluginKind.BASE_TOOL, PluginKind.ADVANCED_TOOL):
        return "Tool"
    return "Plugin"


def has_any_file(directory: Path) -> bool:
    """目录里有没有东西（用于"绝不覆盖用户已有工程"的判定）。"""
    try:
        return any(directory.iterdir())
    except OSError:
        return True     # 读不了就当有东西：宁可拒绝生成，也不能把用户的东西盖了


def camel(plugin_id: str) -> str:
    """demo.echo → DemoEcho（给类名用）。"""
    parts = [p for p in re.split(r"[._\-]+", plugin_id) if p]
    if not parts:
        return "My"
    return "".join(p[:1].upper() + p[1:] for p in parts)


def write(file: Path, content: str) -> None:
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content, encoding="utf-8")


# --------------------------------------------------------------------------
# 骨架模板
# --------------------------------------------------------------------------


def tool_template(class_name: str, display_name: str, plugin_id: str, minimal: bool) -> str:
    """工具插件骨架（基础工具 / 进阶工具）。"""
    mode_comment = (
        "# 极简模式也放行（基础工具）。\n"
        "    # 不声明 minimal_mode 的话，极简模式里就看不见这个工具。\n"
        "    minimal_mode = True"
        if minimal else
        "# 只在标准模式可用（进阶工具）：极简模式是给「少而精」的场景用的。\n"
        "    minimal_mode = False")
    return f'''"""{display_name}（Lion Code 插件开发模式生成的示例工具插件）。

它已经是一个**能加载、能跑**的完整插件：自检通过后放进插件目录、
调一次 POST /api/plugins/reload，模型就能看到并使用它了。
"""

from __future__ import annotations

from lionbox.plugins.base import (PermissionLevel, ToolCategory, ToolPlugin, ToolResult)


class {class_name}(ToolPlugin):
    """示例工具插件：把输入的文本原样返回，用来验证插件能被加载和执行。"""

    {mode_comment}

    # ---- 唯一ID：设置里的开关、日志、卸载都认它。必须全库唯一，重了会被跳过 ----
    @property
    def id(self) -> str:
        return "{plugin_id}"

    # ---- 工具名：模型看到并调用的名字（英文、下划线，别和内置工具重名）----
    @property
    def name(self) -> str:
        return "{plugin_id.replace('.', '_').replace('-', '_')}"

    @property
    def description(self) -> str:
        return "示例插件：把输入的文本原样返回，用来验证插件能被加载和执行"

    @property
    def category(self) -> str:
        return ToolCategory.SYSTEM

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict:
        """参数 schema：写清类型和说明，模型才给得对。"""
        return {{
            "type": "object",
            "properties": {{
                "text": {{"type": "string", "description": "要回显的文本"}},
            }},
            "required": ["text"],
        }}

    def execute(self, args: dict) -> ToolResult:
        """真正干活的地方。

        约定：成功用 `self.success(...)`，失败用 `self.error(...)`（error 的内容会原样
        回给模型，所以要写成"能照着改"的话，别只写"失败了"）。异常一定要自己接住 ——
        插件抛出去的异常会变成模型看到的一整轮报错。
        """
        try:
            text = self.get_required_string_arg(args, "text")
        except ValueError as e:
            return self.error(f"缺少参数: {{e}}")
        return self.success("插件收到: " + text)


# 加载器按这个清单实例化插件类（改类名时记得同步改 lionbox-plugin.json 的 classes）
PLUGIN_CLASSES = [{class_name}]
'''


def skill_template(class_name: str, display_name: str, plugin_id: str) -> str:
    """技能插件骨架（往系统提示词里注入领域经验）。"""
    return f'''"""{display_name}（Lion Code 插件开发模式生成的示例技能插件）。

技能和工具的区别：工具是"模型能做的事"，技能是"模型该知道的规矩"。
技能把一段领域经验注入系统提示词，让模型在这个领域里少走弯路。

（另一种做法：直接在 `skills/<id>/SKILL.md` 里写 frontmatter + 正文，
不需要写 Python —— 那种技能用户改起来更方便。）
"""

from __future__ import annotations

from lionbox.plugins.lifecycle import Plugin, PluginType


class {class_name}(Plugin):
    """示例技能插件。"""

    @property
    def id(self) -> str:
        return "{plugin_id}"

    @property
    def name(self) -> str:
        return "{plugin_id.replace('.', '_').replace('-', '_')}"

    @property
    def display_name(self) -> str:
        return "{display_name}"

    @property
    def description(self) -> str:
        return "示例技能：往系统提示词里注入一段领域提示"

    @property
    def type(self) -> str:
        return PluginType.SKILL

    def system_prompt_fragment(self) -> str:
        """注入系统提示词的片段。

        【写短】这段文字每一轮请求都会带上，写几百字等于每轮都多花几百 token。
        只写"模型不知道、又必须知道"的规矩，通用常识别写。
        """
        return "## 示例技能\\n回答里必须提到「插件开发模式」这个词。"

    def required_tool_ids(self) -> list[str]:
        """这个技能依赖哪些工具（只做展示，工具开关仍然各自独立）。"""
        return []

    def task_type_descriptions(self) -> list[str]:
        return ["演示技能插件怎么工作"]


PLUGIN_CLASSES = [{class_name}]
'''


def system_template(class_name: str, display_name: str, plugin_id: str, kind: str) -> str:
    """其他系统插件骨架（终端/大循环/子智能体/团队/审查/自动化）。"""
    return f'''"""{display_name}（Lion Code 插件开发模式生成的系统插件骨架）。

系统插件不提供工具，它"改变别的插件怎么跑"。如果要插进 Agent 主循环，
让它同时继承 `lionbox.plugins.lifecycle.AgentSpi`：注册后扩展点就会生效，
卸载时自动摘掉。
"""

from __future__ import annotations

from lionbox.plugins.base import PluginKind
from lionbox.plugins.lifecycle import Plugin, PluginType


class {class_name}(Plugin):
    """示例系统插件。"""

    @property
    def id(self) -> str:
        return "{plugin_id}"

    @property
    def name(self) -> str:
        return "{plugin_id.replace('.', '_').replace('-', '_')}"

    @property
    def display_name(self) -> str:
        return "{display_name}"

    @property
    def description(self) -> str:
        return "示例系统插件（{PluginKind.DISPLAY.get(kind, ("", ""))[0]}）"

    @property
    def type(self) -> str:
        """系统插件：既不是工具也不是技能。"""
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.{kind}

    @property
    def enabled_by_default(self) -> bool:
        """默认开不开。

        会主动干活、或会明显改变体感的插件（自动化、审查）应当返回 False，
        让用户主动开 —— 升级完就悄悄改变行为是最招人烦的。
        """
        return False


PLUGIN_CLASSES = [{class_name}]
'''


def sdk_document() -> str:
    """插件 SDK 接口清单（从运行中的类现取，保证不过期）。"""
    from lionbox.plugins.lifecycle import AgentSpi, Plugin, PluginSettings
    from lionbox.plugins.base import ToolPlugin

    def methods(cls: type) -> str:
        names = sorted(n for n in vars(cls) if not n.startswith("_"))
        return "、".join(f"`{n}`" for n in names) if names else "（无）"

    return f"""# Lion Code 插件 SDK（自动生成，别手改）

这份清单由 `PluginDevService.ensure_sdk()` 从**运行中的类**现取，所以永远和当前版本一致。

## 两种插件基类

| 你要做什么 | 继承 | 必须实现 |
|---|---|---|
| 给模型加一个能调用的工具 | `lionbox.plugins.base.ToolPlugin` | `id`、`name`、`parameters_schema()`、`execute(args)` |
| 改主循环行为 / 注入提示词 / 纯配置插件 | `lionbox.plugins.lifecycle.Plugin` | `id`、`name`、`description` |
| 技能（注入领域经验） | `Plugin` + 覆盖 `type` 返回 `PluginType.SKILL` | `id`、`name`、`system_prompt_fragment()` |

## `ToolPlugin` 的可用成员

{methods(ToolPlugin)}

约定：
- `execute(args) -> ToolResult`：成功 `self.success(文本)`，失败 `self.error(原因)`。
- 参数助手：`get_string_arg` / `get_required_string_arg` / `get_int_arg` / `get_bool_arg`。
- `minimal_mode`：`True` = 极简模式也开放（基础工具），`False` = 只在标准模式（进阶工具）。
- `category` / `permission`：用 `ToolCategory` / `PermissionLevel` 里的常量。

## `Plugin` 的可用成员

{methods(Plugin)}

## 扩展点 `AgentSpi`（可选，多继承）

{methods(AgentSpi)}

| 方法 | 作用 | 默认 |
|---|---|---|
| `filter_tool_names(session_id, names)` | 决定这一轮下发给模型的工具名集合 | 原样返回 |
| `extra_system_sections(session_id, workspace_path, user_message)` | 追加系统提示词段落 | `[]` |
| `transform_user_message(session_id, user_message)` | 改写用户消息 | 原样返回 |
| `loop_options(session_id)` | 覆盖主循环参数 | `{{}}` |
| `order()` | 排序权重（小的先跑） | `100` |

## 清单文件 `lionbox-plugin.json`

```json
{{
  "id": "my.plugin",
  "name": "我的插件",
  "kind": "ADVANCED_TOOL",
  "main": "plugin.py",
  "classes": ["MyTool"]
}}
```

## 设置持久化

插件参数统一存 `settings.json`（`PluginSettings`），按段读写：

```python
settings = PluginSettings()                    # 默认指向插件目录
settings.int_of("myplugin", "limit", 10)       # 读（字符串数字也认）
settings.put("myplugin", "limit", 20)          # 写（立刻原子落盘）
settings.is_enabled(plugin)                    # 用户开关（没点过 = 插件自己声明的默认值）
```

开关语义：**只存"和默认值不一样"的**，这样以后改代码里的默认值能自然生效。

## 插件目录

- 主目录：`{default_paths().plugins_dir()}`
- 设置文件：`{default_paths().settings_file()}`
- 开发工程：`{default_paths().dev_dir()}`
- 可用环境变量覆盖：`LIONBOX_PLUGINS_DIR`（插件目录）、`LIONCODE_HOME`（用户配置根）

## 插件设置里的默认值（改之前想清楚，它们就是"现在的行为"）

| 键 | 默认 | 含义 |
|---|---|---|
| `terminal.maxCommandSeconds` | `{PluginSettings.DEFAULT_MAX_COMMAND_SECONDS}` | 一条命令最长跑多久 |
| `terminal.maxOutputBytes` | `{PluginSettings.DEFAULT_MAX_OUTPUT_BYTES}` | 一条命令最多带回多少字节（0=不限） |
| `loop.maxIterations` | `{PluginSettings.DEFAULT_MAX_ITERATIONS}` | 一条消息最多几轮工具调用 |
| `loop.toolTimeoutSeconds` | `{PluginSettings.DEFAULT_TOOL_TIMEOUT_SECONDS}` | 单个工具最多跑多少秒 |
| `loop.silentRounds` | `{PluginSettings.DEFAULT_SILENT_ROUNDS}` | 连续几轮空转就收尾 |
| `loop.maxToolsPerRound` | `{PluginSettings.DEFAULT_MAX_TOOLS_PER_ROUND}` | 一轮最多执行几个调用（0=不限） |
| `subagent.maxDepth` | `{PluginSettings.DEFAULT_SUBAGENT_MAX_DEPTH}` | 子智能体递归层级上限 |
| `subagent.maxConcurrency` | `{PluginSettings.DEFAULT_SUBAGENT_MAX_CONCURRENCY}` | 同时最多几个子智能体 |
"""


__all__ = ["ENV_DEV_MODE", "ID_PATTERN", "IllegalStateError", "PluginDevService",
           "ScaffoldResult", "camel", "has_any_file", "sdk_document", "suffix_for"]


# ========================================================================
# 原模块 lionbox/plugindev.py
# ========================================================================
"""插件开发模式（对应 Java `core/plugin/dev/PluginDevService.java`）。

开启后，用户（或 AI）可以在软件里直接生成一个**能加载、能跑**的插件工程：
`python/lionbox/plugindev/service.py` 负责脚手架与 SDK 接口清单。

    from lionbox.plugindev import PluginDevService

    dev = PluginDevService()
    dev.set_dev_mode(True)
    result = dev.scaffold("demo.echo", "回显工具", "ADVANCED_TOOL")
    print(result.files)
"""



__all__ = [
    "ENV_DEV_MODE", "ID_PATTERN", "IllegalStateError", "PluginDevService", "ScaffoldResult",
    "camel", "has_any_file", "sdk_document", "suffix_for",
]


# ========================================================================
# 原模块 lionbox/plugins/review.py
# ========================================================================
"""自动授权审查 + 改动人工审核两个系统插件。

【契约来源】
  * `core/plugin/review/ApprovalReviewPlugin.java`（209 行）
  * `core/plugin/change/ChangeReviewPlugin.java`（45 行）

【两者的分工（别混）】
  * **自动授权审查**：动手**之前**，让另一个模型看一眼这次工具调用该不该放行
    （只回 ALLOW 或 `DENY: 理由`）。它解决的是"审批弹窗太多了"—— 用户不可能每条命令
    都点一次同意，但完全免审批又不敢。默认**关闭**：它会在每次危险调用前多打一次模型
    对话，对本地模型来说是实打实的几十秒，这种"会明显改变体感"的能力必须用户主动开。
  * **改动人工审核**：动完手**之后**、落盘之前等人点头（真正干活的是
    `agent/change.py` 的 `ChangeReview`；本类只是"让它在插件列表里有一个能被开关的条目"）。
    默认**开启**：这是用户明确要的默认行为（先审后用）。

两个都开就是双保险：模型先审，人再终审。
"""


import re
from typing import Any



class ReviewDecision:
    """审查结论。

    :param needs_review: 这次调用要不要送去审查
    :param tool_name:    被审的工具名
    :param provider:     审查用提供商（空 = 沿用主 Agent）
    :param model:        审查用模型（空 = 沿用主 Agent）
    :param reason:       为什么需要/不需要审查（写日志与界面提示用）
    """

    __slots__ = ("needs_review", "tool_name", "provider", "model", "reason")

    def __init__(self, needs_review: bool, tool_name: str | None, provider: str,
                 model: str, reason: str) -> None:
        self.needs_review = needs_review
        self.tool_name = tool_name
        self.provider = provider
        self.model = model
        self.reason = reason

    def __repr__(self) -> str:
        return (f"ReviewDecision(needs_review={self.needs_review}, "
                f"tool_name={self.tool_name!r}, reason={self.reason!r})")


class Verdict:
    """放行判定：`allow` True = 放行，False = 拦截；`reason` 会进日志，拦截时还会回给模型。"""

    __slots__ = ("allow", "reason")

    def __init__(self, allow: bool, reason: str) -> None:
        self.allow = allow
        self.reason = reason

    def __repr__(self) -> str:
        return f"Verdict(allow={self.allow}, reason={self.reason!r})"


class ApprovalReviewPlugin(Plugin):
    """自动授权审查插件：动手之前，先让另一个模型看一眼这次工具调用该不该放行。"""

    PLUGIN_ID = "plugin.approval-review"

    #: 默认要审查的工具：能改文件系统 / 能执行任意命令 / 能往外部送东西的那些。
    #: 纯读的那 21 个里的其余工具不审 —— 全审等于每条都慢一倍，用户很快就会把这个
    #: 插件关掉，那还不如一开始就只审危险的。
    #: 【2026-10】指向已删工具的条目（run_background / stop_background / move_file /
    #: change_permissions / git_reset / git_stash / git_remote / http_post）已清掉。
    DEFAULT_REVIEW_TOOLS = frozenset({
        "execute_command",
        "delete_file",
        "download_file",
    })

    def __init__(self, settings: PluginSettings | None = None) -> None:
        self.settings = settings or default_settings()

    # ---- 插件元信息 ----
    @property
    def id(self) -> str:                      # noqa: A003
        return self.PLUGIN_ID

    @property
    def name(self) -> str:
        return "approval_review"

    @property
    def display_name(self) -> str:
        return "自动授权审查"

    @property
    def description(self) -> str:
        return "执行危险工具前，让另一个模型对话审核该不该放行（用哪个模型可配置）"

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.APPROVAL_REVIEW

    @property
    def enabled_by_default(self) -> bool:
        """默认关闭（见模块 docstring：会明显改变体感的能力必须用户主动开）。"""
        return False

    # ---- 配置 ----
    def provider(self) -> str:
        """审查用的提供商（空 = 跟主 Agent 一样）。"""
        return self.settings.string_of("review", "provider", "")

    def model(self) -> str:
        """审查用的模型（空 = 跟主 Agent 一样）。"""
        return self.settings.string_of("review", "model", "")

    def reviewed_tools(self) -> frozenset[str]:
        """需要审查的工具名集合（用户没配过就用默认那批危险的）。"""
        raw = self.settings.section("review").get("tools")
        if not isinstance(raw, list) or not raw:
            return self.DEFAULT_REVIEW_TOOLS
        out = {str(o).strip() for o in raw if o is not None and str(o).strip()}
        return frozenset(out) if out else self.DEFAULT_REVIEW_TOOLS

    def is_active(self) -> bool:
        return self.settings.is_enabled(self)

    # ---- 判定骨架 ----
    def check(self, session_id: str | None, tool_name: str | None,
              arguments: dict[str, Any] | None = None) -> ReviewDecision:
        """这次工具调用要不要拦截审查。

        【接线点】AgentLoop 里、真正执行工具**之前**调它（就在 runToolWithTimeout 前面）。
        判定 needs_review=True 时：用 `decision.provider()/model()` 建一次对话，
        把 `build_review_prompt()` 的结果发过去，拿 `parse_verdict()` 解析；
        DENY 时**不要抛异常中断整个任务**，而是把 `deny_message()` 当成工具结果回给模型 ——
        这样模型知道"这一步被拦了、原因是这个"，还能换个安全做法继续。

        【为什么工具名匹配用"小写精确"而不是包含】包含匹配会让 `git_commit` 命中
        `git_commit_amend` 这类无关名字，误审和漏审都是从这种"差不多"开始的。
        """
        if not self.is_active():
            return ReviewDecision(False, tool_name, self.provider(), self.model(), "插件未开启")
        if not tool_name or not str(tool_name).strip():
            return ReviewDecision(False, tool_name, self.provider(), self.model(), "工具名为空")
        tools = self.reviewed_tools()
        hit = any(t.lower() == str(tool_name).strip().lower() for t in tools)
        if not hit:
            return ReviewDecision(False, tool_name, self.provider(), self.model(),
                                  f"不在审查清单里（当前审查 {len(tools)} 个工具）")
        return ReviewDecision(True, str(tool_name).strip(), self.provider(), self.model(),
                              "命中审查清单，需要另一个模型审核")

    def build_review_prompt(self, tool_name: str, arguments: dict[str, Any] | None,
                            workspace_path: str | None) -> str:
        """给审查模型看的提示词。

        写死的三条要求（必须回 ALLOW/DENY、只回一行、不确定就 DENY）是有意为之：
        审查调用是要被程序解析的，模型回一段散文就等于这次审查作废。
        """
        sb = ["你是 Lion Code 的工具调用安全审查员。判断下面这次工具调用该不该放行。\n",
              "只回一行，格式必须是：ALLOW 或 DENY: 一句话理由。不要解释、不要加别的字。\n",
              "判断标准：只读/可逆/在工作区内 = ALLOW；删数据、覆盖文件、动远端仓库、",
              "执行破坏性命令（格式化、递归删除、改系统设置）、访问工作区外路径 = DENY。\n",
              "拿不准就 DENY。\n\n",
              f"工具：{tool_name}\n"]
        if workspace_path and str(workspace_path).strip():
            sb.append(f"工作区：{workspace_path}\n")
        sb.append("参数：" + (repr(arguments) if arguments is not None else "{}") + "\n")
        return "".join(sb)

    @staticmethod
    def parse_verdict(model_reply: str | None) -> Verdict:
        """解析审查模型的回答。

        【认不出来时放行，不是拦下】这是刻意的：审查插件是"额外的安全网"，
        真正的主闸是审批策略。如果审查模型抽风（回了半句、回了中文、什么都没回），
        这里拦下来会让用户"什么都没干成、还不知道为什么" —— 比漏放一次更糟。
        所以认不出来 = ALLOW，但理由里写明"未能解析，已按放行处理"，让日志查得出来。

        【谁先出现谁说了算】不能写成"先判 DENY"：`ALLOW, but I considered DENY` 这类
        正常放行的回答会被判成拒绝，表现就是"审查插件一开，正常工具也莫名其妙被拦"。
        另外不能在 `upper()` 的结果里取下标再切原文（某些字符大写后长度会变），
        所以直接在原文上做大小写不敏感的查找。
        """
        if model_reply is None or not str(model_reply).strip():
            return Verdict(True, "审查模型没有返回内容，按放行处理")
        text = str(model_reply).strip()
        deny = re.search("deny", text, re.IGNORECASE)
        allow = re.search("allow", text, re.IGNORECASE)
        if allow is not None and (deny is None or allow.start() < deny.start()):
            return Verdict(True, "审查模型放行")
        if deny is not None:
            reason = re.sub(r"^[\s:：,，-]+", "", text[deny.end():]).strip()
            return Verdict(False, reason or "审查模型判定为拒绝（未给理由）")
        return Verdict(True, f"未能解析审查结果（原文：{_shorten(text)}），按放行处理")

    def deny_message(self, tool_name: str, reason: str) -> str:
        """拦截时回给模型的话（工具结果）。

        必须写清三件事：被拦了、为什么、下一步怎么办。只写"被拒绝"的话，
        模型会原样再试一次 —— 而它每试一次就多烧一轮。
        """
        return (f"这次调用被自动授权审查拦下了（工具：{tool_name}）。\n"
                f"审查意见：{reason}\n"
                "请改用不会造成破坏的做法：把破坏性操作改成只读查看、把删除改成先备份再确认、"
                "或者向用户说明你为什么需要这个操作，让用户来决定。\n"
                "（用户可在设置 → 插件 → 自动授权审查里调整审查用的模型或关掉这个插件。）")


class ChangeReviewPlugin(Plugin):
    """改动人工审核插件：AI 改的文件先攒成待审改动，人点「通过」才真正落盘。

    真正干活的是 `agent/change.py` 的 `ChangeReview`（它按本插件的 id 查开关：
    `settings.is_enabled("plugin.change-review", True)`）；关掉即老行为：直接落盘。
    """

    PLUGIN_ID = "plugin.change-review"

    @property
    def id(self) -> str:                      # noqa: A003
        return self.PLUGIN_ID

    @property
    def name(self) -> str:
        return "change_review"

    @property
    def display_name(self) -> str:
        return "改动人工审核"

    @property
    def description(self) -> str:
        return "AI 改的每个文件先攒成待审改动，人在界面上点通过才真正落盘；打回则按理由重写"

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.APPROVAL_REVIEW

    @property
    def enabled_by_default(self) -> bool:
        """默认开启：这是用户明确要的默认行为（先审后用）。"""
        return True


def _shorten(text: str) -> str:
    flat = re.sub(r"\s+", " ", text).strip()
    return flat if len(flat) <= 60 else flat[:60] + "…"


# ========================================================================
# 原模块 lionbox/team/member.py
# ========================================================================
"""智能体团队里的一个成员：用哪个模式、负责干什么。

【契约来源】逐项对照 Java 版 `core/plugin/team/TeamMember.java`（record）：
字段、`create()` 的默认值（id 自动生成 `agent-xxxxxxxx`、名字 "未命名智能体"、
模式默认 STANDARD）、`toMap()` 的键名、`fromMap()` 对脏数据的处理（没有 id 就丢掉）全部照抄。
"""


import uuid
from dataclasses import dataclass
from typing import Any

#: 模式只认这两个（PTC/CREATIVE 会被归一成 STANDARD，规则与全局模式归一一致）
ALLOWED_MODES = ("MINIMAL", "STANDARD")


@dataclass
class TeamMember:
    """团队里的一个智能体。

    :param id:      唯一标识（用户不填就自动生成，增删改查都按它定位）
    :param name:    显示名（"代码审查员""文档写手"…）
    :param mode:    工作模式：MINIMAL（极简）/ STANDARD（标准）
    :param role:    职责说明（这句会进系统提示词，让模型知道这个成员该干什么）
    :param model:   该成员用哪个模型（空 = 跟主 Agent 一样）
    :param enabled: 这个成员是否参与
    """

    id: str                       # noqa: A003
    name: str
    mode: str
    role: str = ""
    model: str = ""
    enabled: bool = True

    @staticmethod
    def create(member_id: str | None, name: str | None, mode: str | None,
               role: str | None, model: str | None,
               enabled: bool | None = None) -> "TeamMember":
        """新建一个成员（id 留空时自动生成）。"""
        mid = str(member_id).strip() if member_id is not None and str(member_id).strip() else \
            "agent-" + str(uuid.uuid4())[:8]
        mname = str(name).strip() if name is not None and str(name).strip() else "未命名智能体"
        mmode = str(mode).strip().upper() if mode is not None and str(mode).strip() else "STANDARD"
        return TeamMember(
            id=mid,
            name=mname,
            mode=mmode,
            role="" if role is None else str(role).strip(),
            model="" if model is None else str(model).strip(),
            enabled=True if enabled is None else bool(enabled),
        )

    def to_map(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "mode": self.mode,
            "role": self.role,
            "model": self.model,
            "enabled": self.enabled,
        }

    @staticmethod
    def from_map(raw: dict[str, Any] | None) -> "TeamMember | None":
        """从设置里的一条记录还原；没有 id 的当脏数据丢掉（没法改也没法删）。"""
        if not raw:
            return None
        member_id = raw.get("id")
        if member_id is None or not str(member_id).strip():
            return None
        enabled_raw = raw.get("enabled")
        if isinstance(enabled_raw, bool):
            enabled = enabled_raw
        elif enabled_raw is None:
            enabled = True
        else:
            enabled = str(enabled_raw).strip().lower() in ("true", "1", "yes", "是", "开")
        return TeamMember.create(str(member_id), _str__team_member(raw.get("name")), _str__team_member(raw.get("mode")),
                                 _str__team_member(raw.get("role")), _str__team_member(raw.get("model")), enabled)


def _str__team_member(value: Any) -> str | None:
    return None if value is None else str(value)


# ========================================================================
# 原模块 lionbox/team/agent_team.py
# ========================================================================
"""智能体团队插件：用户自己定义"有哪些智能体、各自用什么模式、负责干什么"。

【契约来源】逐项对照 Java 版 `core/plugin/team/AgentTeamPlugin.java`。

一个团队就是一组 `TeamMember`。它做三件事：
  1. 配置持久化（存在 settings.json 的 `team.members` 里，重启还在）；
  2. 增删改查（REST 端点直接调这里）；
  3. 把团队说明注入系统提示词（`AgentSpi.extra_system_sections`）——
     否则"配置了团队"对模型来说是隐形的，等于没配。
"""


from typing import Any



class AgentTeamPlugin(Plugin, AgentSpi):
    """智能体团队插件。"""

    PLUGIN_ID = "plugin.agent-team"

    def __init__(self, settings: PluginSettings | None = None) -> None:
        self.settings = settings or default_settings()

    # ------------------------------------------------------------------
    # 插件元信息
    # ------------------------------------------------------------------
    @property
    def id(self) -> str:                      # noqa: A003
        return self.PLUGIN_ID

    @property
    def name(self) -> str:
        return "agent_team"

    @property
    def display_name(self) -> str:
        return "智能体团队"

    @property
    def description(self) -> str:
        return "用户自定义的智能体集群：每个智能体用什么模式（极简/标准）、负责干什么"

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.AGENT_TEAM

    # ------------------------------------------------------------------
    # SPI
    # ------------------------------------------------------------------
    def spi_name(self) -> str:
        return "智能体团队插件"

    def order(self) -> int:
        """团队说明放在提示词靠后位置，别挤掉硬性格式约定。"""
        return 200

    def register(self) -> None:
        register_spi(self)
        print("[团队] 智能体团队已挂到 Agent 主循环（AgentSpi）", flush=True)

    def unregister(self) -> None:
        unregister_spi(self)

    # ------------------------------------------------------------------
    # 增删改查
    # ------------------------------------------------------------------
    def members(self) -> list[TeamMember]:
        """全部成员（含被停用的：界面上要显示成灰的，删掉就看不见了）。"""
        out: list[TeamMember] = []
        for raw in self.settings.list_of("team", "members"):
            member = TeamMember.from_map(raw)
            if member is not None:
                out.append(member)
        return out

    def active_members(self) -> list[TeamMember]:
        """参与干活的成员（停用的不算）。"""
        return [m for m in self.members() if m.enabled]

    def find(self, member_id: str | None) -> TeamMember | None:
        if member_id is None:
            return None
        for m in self.members():
            if m.id == member_id:
                return m
        return None

    def add(self, member_id: str | None, name: str | None, mode: str | None,
            role: str | None, model: str | None,
            enabled: bool | None = None) -> TeamMember:
        """新增成员。

        模式写错（比如 "fast"）当场报错，而不是先存下来、等到真的用它跑任务时才炸。
        PTC/CREATIVE 会被归一成 STANDARD（老配置不会因此失效）。

        :raises ValueError: 模式名不认识 / id 已存在
        """
        normalized_mode = _parse_mode_strict(mode)
        created = TeamMember.create(member_id, name, normalized_mode, role, model, enabled)
        if self.find(created.id) is not None:
            raise ValueError(f"智能体ID已存在: {created.id}")
        items = self.settings.list_of("team", "members")
        items.append(created.to_map())
        self.settings.put("team", "members", items)
        print(f"[团队] 智能体团队成员已新增: {created.name}（{created.mode}）", flush=True)
        return created

    def update(self, member_id: str, patch: dict[str, Any] | None) -> TeamMember | None:
        """部分更新：只改传进来的字段，其余保持原样。

        【为什么不做整体替换】前端"改个名字"只发 name，整体替换会把 role/model 抹掉 ——
        这种"改一处丢三处"的 bug 在设置页里特别容易发生，也特别难被发现。

        :raises ValueError: 模式名不认识
        """
        old = self.find(member_id)
        if old is None:
            return None
        mode = old.mode
        if patch is not None and patch.get("mode") is not None:
            mode = _parse_mode_strict(str(patch.get("mode")))
        updated = TeamMember(
            id=old.id,
            name=_pick__team_agent_team(patch, "name", old.name),
            mode=mode,
            role=_pick__team_agent_team(patch, "role", old.role),
            model=_pick__team_agent_team(patch, "model", old.model),
            enabled=_pick_bool(patch, "enabled", old.enabled),
        )
        items = self.settings.list_of("team", "members")
        for i, raw in enumerate(items):
            current = TeamMember.from_map(raw)
            if current is not None and current.id == member_id:
                items[i] = updated.to_map()
        self.settings.put("team", "members", items)
        return updated

    def remove(self, member_id: str) -> bool:
        """删除成员。"""
        items = self.settings.list_of("team", "members")
        kept: list[dict[str, Any]] = []
        removed = False
        for raw in items:
            current = TeamMember.from_map(raw)
            if current is not None and current.id == member_id:
                removed = True
                continue
            kept.append(raw)
        if removed:
            self.settings.put("team", "members", kept)
        return removed

    # ------------------------------------------------------------------
    # 注入系统提示词
    # ------------------------------------------------------------------
    def extra_system_sections(self, session_id: str | None = None,
                              workspace_path: str | None = None,
                              user_message: str | None = None) -> list[str]:
        if not self.settings.is_enabled(self):
            return []
        active = self.active_members()
        if not active:
            return []      # 没配成员就一个字都不加，别给提示词添噪音
        sb = ["## 智能体团队\n",
              "用户为这个工作区配置了以下智能体分工，处理对应类型的任务时按它们各自的定位来做：\n"]
        for m in active:
            sb.append(f"- {m.name}（模式：{'极简' if m.mode == 'MINIMAL' else '标准'}")
            if m.model.strip():
                sb.append(f"，模型：{m.model}")
            sb.append("）")
            if m.role.strip():
                sb.append(f"：{m.role}")
            sb.append("\n")
        return ["".join(sb)]


def _parse_mode_strict(mode: str | None) -> str:
    """严格解析模式名（认不出来就报错，与 Java 的 `AgentMode.fromName` 一致）。

    【与 `plugins.base.AgentMode.from_name` 的分工】base 里那个是"宽松归一"（认不出来
    一律回落 STANDARD），用于读老数据；这里是"用户输入校验"，写错必须当场告诉他。
    """
    value = str(mode or "").strip().upper()
    if value == "":
        return AgentMode.STANDARD
    if value in AgentMode.DISPLAY:
        return AgentMode.normalize(value)      # PTC/CREATIVE → STANDARD
    raise ValueError(f"不支持的模式: {mode}（可选 {' / '.join(ALLOWED_MODES)}）")


def _pick__team_agent_team(patch: dict[str, Any] | None, key: str, fallback: str) -> str:
    if patch is None or key not in patch or patch.get(key) is None:
        return fallback
    return str(patch.get(key))


def _pick_bool(patch: dict[str, Any] | None, key: str, fallback: bool) -> bool:
    if patch is None or key not in patch or patch.get(key) is None:
        return fallback
    value = patch.get(key)
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in ("true", "1", "yes", "是", "开")


# ========================================================================
# 原模块 lionbox/team/agent_team_tool.py
# ========================================================================
"""`agent_team_run` 工具：把一件任务**分给团队里几个成员各干一段**，最后汇总回主 Agent。

【契约来源】逐项对照 Java 版 `core/plugin/team/AgentTeamTool.java`：
id / name / description / parameters_schema 逐字一致；成员挑选规则（逗号/分号/空白分隔）、
串行执行、报告格式（每人一节 + 成功/失败计数）、4000 字截断全部照抄。

成员是谁、用什么模式、负责什么，都由用户在"设置 → 插件 → 智能体团队"里配
（名字、模式 MINIMAL/STANDARD、职责说明、模型），这个工具只负责按配置派活。

【为什么串行而不是并发】本机 llama-server 是**单 slot**（-c 全给一个对话），
并发派 4 个成员只会让 4 个请求排队，还互相抢 KV cache；日志里看起来"同时在跑"，
实际总耗时一样、失败率更高。所以这里一个一个来，并在结果里写清楚顺序。
"""


import re
import time


#: 单个成员结论的长度上限（汇总报告不该被一个人撑爆）
MAX_ANSWER_CHARS = 4000


class AgentTeamTool(ToolPlugin):
    """`agent_team_run`：把任务交给配置好的智能体团队，各成员分头做完再汇总。"""

    def __init__(self, plugin: AgentTeamPlugin, agent_loop=None, session_manager=None,
                 settings: PluginSettings | None = None, workspace=None) -> None:
        super().__init__(workspace)
        self.plugin = plugin
        self.agent_loop = agent_loop
        self.session_manager = session_manager
        self.settings = settings or default_settings()

    # ---- 元信息 ----
    @property
    def id(self) -> str:                      # noqa: A003
        return "tool.agent.team"

    @property
    def name(self) -> str:
        return "agent_team_run"

    @property
    def description(self) -> str:
        return ("把一件任务交给配置好的智能体团队，各成员按自己的职责分头做完再汇总。"
                "members 留空 = 全部启用的成员；也可以只点某几个（逗号分隔的成员 id）。")

    @property
    def kind(self) -> str:
        return PluginKind.AGENT_TEAM

    @property
    def category(self) -> str:
        return ToolCategory.SYSTEM

    @property
    def permission(self) -> str:
        return PermissionLevel.WRITE

    @property
    def minimal_mode(self) -> bool:
        # 团队属于进阶能力，极简模式不给
        return False

    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "task": {"type": "string",
                         "description": "要团队一起完成的总体任务（每个成员都会按自己的职责理解它）"},
                "members": {"type": "string",
                            "description": "可选：只让这几个成员干活，逗号分隔的成员 id（留空 = 全部启用的成员）"},
            },
            "required": ["task"],
        }

    # ---- 执行 ----
    def execute(self, args: dict) -> ToolResult:
        # 【开关必须是真开关】用户关的是**系统插件** plugin.agent-team，
        # 而门禁按"工具插件 id"(tool.agent.team) 查，两者 id 对不上 —— 所以这里显式判断。
        from lionbox.agent.control import ThinkingLevel
        from lionbox.sessions.context import SessionContext
        if not self.settings.is_enabled(AgentTeamPlugin.PLUGIN_ID,
                                        self.plugin.enabled_by_default):
            return self.error("智能体团队插件已在设置里关闭（设置 → 插件 → 智能体团队）。")

        task = self.get_string_arg(args, "task", "")
        if not task.strip():
            return self.error("agent_team_run 需要 task 参数：写清楚要团队做什么")

        members = self.pick_members(self.get_string_arg(args, "members", ""))
        if not members:
            return self.error("团队里没有可用的成员。请先在 设置 → 插件 → 智能体团队 里加成员"
                              "（每个成员要有名字、模式，和一句「负责干什么」）")

        parent_session_id = SessionContext.get()
        workspace_id = self._workspace_id_of(parent_session_id)
        if workspace_id is None:
            return self.error("派团队失败：当前会话没有绑定工作区")

        report = [f"【智能体团队执行结果】共 {len(members)} 个成员，"
                  "按顺序执行（本机模型是单通道，串行更稳）\n"]
        ok = 0
        fail = 0
        for m in members:
            mode = AgentMode.MINIMAL if m.mode.lower() == "minimal" else AgentMode.STANDARD
            child = self.session_manager.create_session(workspace_id, mode)
            self.session_manager.rename_session(child.session_id, "团队/" + m.name)
            prompt = (f"你是团队里的【{m.name}】。\n"
                      f"你的职责：{m.role.strip() if m.role and m.role.strip() else '（未填写，按名字理解）'}\n\n"
                      f"【团队要完成的任务】\n{task}\n\n"
                      "只做你职责范围内的事；动手要用工具；做完用一段话给结论："
                      "你做了什么、结果如何、有没有需要别人接手的地方。")
            started = _now_ms()
            try:
                model = m.model if (m.model or "").strip() else None
                answer = self.agent_loop.process_message(child.session_id, prompt, mode,
                                                        ThinkingLevel.LOW, model)
                body = answer if answer is not None and str(answer).strip() else "（没有给出结论）"
                body = str(body)
                if len(body) > MAX_ANSWER_CHARS:
                    body = body[:MAX_ANSWER_CHARS] + "\n…（已截断）"
                report.append(f"\n### {m.name}（{mode}，{(_now_ms() - started) // 1000} 秒）\n"
                              f"{body}\n")
                ok += 1
            except Exception as e:
                print(f"[团队] 团队成员 {m.name} 执行异常: {e}", flush=True)
                report.append(f"\n### {m.name} ❌ 执行异常\n{e}\n")
                fail += 1
        report.append(f"\n（成功 {ok} 个，失败 {fail} 个）")
        text = "".join(report)
        return self.error(text) if (fail > 0 and ok == 0) else self.success(text)

    # ---- 辅助 ----
    def pick_members(self, raw: str | None) -> list[TeamMember]:
        """挑成员：给了 id 列表就按它挑，否则用全部启用的成员。"""
        out: list[TeamMember] = []
        if raw is None or not str(raw).strip():
            out.extend(self.plugin.active_members())
            return out
        for member_id in re.split(r"[,，;；\s]+", str(raw)):
            if not member_id.strip():
                continue
            found = self.plugin.find(member_id.strip())
            if found is not None:
                out.append(found)
        return out

    def _workspace_id_of(self, session_id: str | None) -> str | None:
        if session_id is None or self.session_manager is None:
            return None
        session = self.session_manager.get_session(session_id)
        return None if session is None else session.workspace_id


def _now_ms() -> int:
    return int(time.time() * 1000)


# ========================================================================
# 原模块 lionbox/team/subagent.py
# ========================================================================
"""子智能体插件：把子任务派给"另一个自己"去干，并给这件事套上三条缰绳。

【契约来源】逐项对照 Java 版 `core/plugin/team/SubAgentConfig.java` +
`core/plugin/team/SubAgentPlugin.java`。

职责划分：本模块只管"能不能派、派几个、用哪个模型"（`check_spawn` / `check_concurrency` /
`config`）；**真正派活的是 `subagent_tool.py` 的 `agent_spawn` 工具** ——
它由 `registrar.py` 注册进插件注册表，模型一轮里调它，它就在一条同步链路上
起一个独立会话跑子 Agent，跑完把结论当工具结果带回主 Agent。

【为什么不在这里直接起线程去跑子智能体】AgentLoop 是按会话串行推进的，
插件自己起线程会让"这个会话现在有几件事在跑"变得没人说得清（谁的上下文、谁的审批、
谁的工作区？）。所以派发走的是主循环自己的工具调用链路，串行、可停、可审计。
"""


from dataclasses import dataclass



@dataclass
class SubAgentConfig:
    """子智能体的运行约束（递归层级上限 / 并发数量上限 / 用哪个模型）。

    :param enabled:        插件是否开启（关掉 = 不允许派子智能体）
    :param max_depth:      递归层级上限。0 = 只允许主 Agent 自己干；1 = 主 Agent 可以派
                           子智能体，但子智能体不能再往下派；2 = 允许"子智能体再派子智能体"。
    :param max_concurrency: 同时最多几个子智能体在跑
    :param provider:       子智能体用哪个提供商（空 = 跟主 Agent 一样）
    :param model:          子智能体用哪个模型（空 = 跟主 Agent 一样）
    """

    enabled: bool
    max_depth: int
    max_concurrency: int
    provider: str = ""
    model: str = ""

    def is_depth_allowed(self, depth: int) -> bool:
        """这个层级的子智能体允不允许存在（主 Agent = 0 层）。"""
        return self.enabled and 0 <= depth <= self.max_depth

    def is_concurrency_allowed(self, running: int) -> bool:
        return self.enabled and running < self.max_concurrency

    def model_label(self) -> str:
        """用的模型描述（给日志/提示词用）。"""
        if not (self.model or "").strip():
            return "（跟主 Agent 相同）"
        if not (self.provider or "").strip():
            return self.model
        return f"{self.provider} / {self.model}"


class SubAgentPlugin(Plugin):
    """子智能体插件（系统插件，可开关）。"""

    PLUGIN_ID = "plugin.subagent"

    def __init__(self, settings: PluginSettings | None = None) -> None:
        self.settings = settings or default_settings()

    @property
    def id(self) -> str:                      # noqa: A003
        return self.PLUGIN_ID

    @property
    def name(self) -> str:
        return "subagent"

    @property
    def display_name(self) -> str:
        return "子智能体"

    @property
    def description(self) -> str:
        return "把子任务派给子智能体执行：可限制递归层级、并发数量，并指定它用哪个模型"

    @property
    def type(self) -> str:
        return PluginType.SYSTEM

    @property
    def kind(self) -> str:
        return PluginKind.SUBAGENT

    # ------------------------------------------------------------------
    # 配置
    # ------------------------------------------------------------------
    def config(self) -> SubAgentConfig:
        """当前配置（每次现读，用户在设置里改完立刻生效）。"""
        depth = self.settings.int_of("subagent", "maxDepth",
                                     PluginSettings.DEFAULT_SUBAGENT_MAX_DEPTH)
        concurrency = self.settings.int_of("subagent", "maxConcurrency",
                                           PluginSettings.DEFAULT_SUBAGENT_MAX_CONCURRENCY)
        return SubAgentConfig(
            enabled=bool(self.settings.is_enabled(self)),
            max_depth=max(depth, 0),
            max_concurrency=max(concurrency, 1),
            provider=self.settings.string_of("subagent", "provider", ""),
            model=self.settings.string_of("subagent", "model", ""),
        )

    # ------------------------------------------------------------------
    # 强制校验（AgentLoop 接线时直接调这两个）
    # ------------------------------------------------------------------
    def check_spawn(self, depth: int) -> str | None:
        """这一层能不能派子智能体：返回 None = 放行；返回字符串 = **明确拒绝的理由**。

        调用方应当把这个字符串当成工具结果回给模型（而不是抛异常），
        这样模型下一轮就知道"别再试了，是层级/开关的问题"，不会反复重试烧轮次。

        :param depth: **当前发起派发的 Agent 所在层级**（主 Agent = 0，子智能体 = 1）
            —— 与 Java `SubAgentPlugin.checkSpawn` 的 javadoc 一致。

        【与 Java 的差异（修了一个 off-by-one）】Java 的 `SubAgentTool` 把
        **子**层级传了进来（`checkSpawn(childDepth)`，主 Agent 传的是 1），
        而方法体判的是 `depth >= maxDepth` —— 于是默认配置（maxDepth=1）下
        `1 >= 1` 恒成立，**agent_spawn 永远被拒**，"主 Agent 可以派一层子智能体"
        这个写在 `SubAgentConfig` 文档里的语义根本走不到。
        这里按文档语义传"发起方所在层级"：maxDepth=1 → 0 层可派、1 层不可派；
        maxDepth=0 → 谁都不能派；maxDepth=2 → 允许"子智能体再派子智能体"。
        """
        cfg = self.config()
        if not cfg.enabled:
            return ("子智能体插件已被用户在设置里关闭，不能派发子智能体；"
                    "请自己完成任务，或在设置 → 插件里重新开启「子智能体」。")
        if depth < 0:
            # 层级不该是负数；真出现了说明调用方传错了，直接拒绝比猜一个值安全
            return f"派发子智能体失败：层级参数非法（depth={depth}）。"
        if depth >= cfg.max_depth:
            return (f"已达子智能体递归层级上限（当前第 {depth} 层，上限 "
                    f"{cfg.max_depth} 层）：这一层不能再派子智能体，请自己完成任务。"
                    "需要更深的层级，可在设置 → 插件 → 子智能体里调大「递归层级上限」。")
        return None

    def check_concurrency(self, running: int) -> str | None:
        """还能不能再开一个子智能体（并发上限）。返回 None = 放行。"""
        cfg = self.config()
        if not cfg.enabled:
            return "子智能体插件已被用户在设置里关闭，不能派发子智能体。"
        if not cfg.is_concurrency_allowed(running):
            return (f"子智能体并发已达上限（正在跑 {running} 个，上限 "
                    f"{cfg.max_concurrency} 个）：先等它们出结果，或在设置里调大「并发数量上限」。")
        return None

    def child_depth(self, parent_depth: int) -> int:
        """子智能体这一层可用的层级号：主 Agent(0) 派出来的就是 1。

        放在插件里，免得调用方各自 +1 加错。
        """
        return int(parent_depth) + 1


# ========================================================================
# 原模块 lionbox/team/subagent_tool.py
# ========================================================================
"""`agent_spawn` 工具：把一件事**整包**交给一个独立的子 Agent 去干。

【契约来源】逐项对照 Java 版 `core/plugin/team/SubAgentTool.java`：
id / name / description / parameters_schema 逐字一致；两道闸门（层级、并发）、
ThreadLocal 层级计数、回答截断（6000 字）、异常处理文案全部照抄。

【和"再调几个工具"有什么不一样】主 Agent 的上下文里已经塞满了前面几十轮的工具结果，
再做一件独立的事，那些无关历史全都跟着发一遍（本机 11 token/s，白烧时间），
而且主 Agent 中途分心很容易把两件事搅在一起。子智能体开的是**全新会话**：
干净上下文 + 只带这一件事的说明，干完只把结论带回来。这就是"派活"的价值。

【约束是插件给的，不是这里写死的】递归层级上限、并发上限、用哪个模型，全部读
`SubAgentPlugin` 的设置。超限时**不抛异常**，而是把一句人话当工具结果回给模型 ——
模型看到就能自己改做法（"层级超了，我自己直接干"），整个任务不会因为一次越界就废掉。
"""


import re
import threading
import time


#: 子 Agent 最终回答带回主 Agent 时的长度上限（结论不需要上万字）
MAX_ANSWER_CHARS__team_subagent_tool = 6000


class _Counter:
    """当前正在跑的子智能体数量（跨会话，防止同时派太多把本机模型挤爆）。"""

    def __init__(self) -> None:
        self._value = 0
        self._lock = threading.Lock()

    def increment(self) -> int:
        with self._lock:
            self._value += 1
            return self._value

    def decrement(self) -> int:
        with self._lock:
            self._value -= 1
            return self._value

    def get(self) -> int:
        with self._lock:
            return self._value


class SubAgentTool(ToolPlugin):
    """`agent_spawn`：派一个子智能体独立完成一件完整的事，只把结论带回来。"""

    #: 当前递归深度（线程局部）。
    #: 【为什么用线程局部而不是参数】子 Agent 是**同步**跑在派发它的那条线程上的
    #: （`agent_loop.process_message` 会一直跑到出结果），所以"这条线程现在在第几层"
    #: 就是天然准确的层级。子 Agent 再派子智能体时读到的是同一份计数，层级自然累加。
    _DEPTH = threading.local()

    #: 当前正在跑的子智能体数量（进程级，跨会话共享）
    _RUNNING = _Counter()

    def __init__(self, plugin: SubAgentPlugin, agent_loop=None, session_manager=None,
                 workspace=None) -> None:
        super().__init__(workspace)
        self.plugin = plugin
        self.agent_loop = agent_loop
        self.session_manager = session_manager

    # ---- 元信息 ----
    @property
    def id(self) -> str:                      # noqa: A003
        return "tool.agent.spawn"

    @property
    def name(self) -> str:
        return "agent_spawn"

    @property
    def description(self) -> str:
        return ("派一个子智能体独立完成一件完整的事，只把结论带回来（适合独立、边界清楚、"
                "又不想污染当前上下文的活）。task 里要写清楚要什么结果、给哪些线索。")

    @property
    def kind(self) -> str:
        return PluginKind.SUBAGENT

    @property
    def category(self) -> str:
        # Java 版是 ToolCategory.OTHER；Python 版 base.py 的等价分类是 SYSTEM
        return ToolCategory.SYSTEM

    @property
    def permission(self) -> str:
        # 子智能体可能去改文件，所以按"工作区写"要权限，不能算只读
        return PermissionLevel.WRITE

    @property
    def minimal_mode(self) -> bool:
        # 派活属于"进阶能力"：极简模式（只给文件 + shell）里不出现
        return False

    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "task": {"type": "string",
                         "description": "交给子智能体的完整任务说明：要什么结果、已知线索、边界条件"},
                "mode": {"type": "string",
                         "description": "子智能体的工作模式：standard（默认）或 minimal（只给文件+终端）"},
                "model": {"type": "string",
                          "description": "可选：让子智能体用哪个模型（留空 = 用插件设置里的默认）"},
            },
            "required": ["task"],
        }

    # ---- 执行 ----
    def execute(self, args: dict) -> ToolResult:
        from lionbox.agent.control import ThinkingLevel
        from lionbox.sessions.context import SessionContext
        task = self.get_string_arg(args, "task", "")
        if not task.strip():
            return self.error("agent_spawn 需要 task 参数：把要子智能体做的事写清楚")

        config = self.plugin.config()
        parent_depth = self.current_depth()
        child_depth = self.plugin.child_depth(parent_depth)

        # 1) 层级闸门：超了就回一句人话，不抛异常（模型会自己改成"我来干"）。
        #    传的是**发起方**所在层级（见 SubAgentPlugin.check_spawn 里的差异说明）
        blocked = self.plugin.check_spawn(parent_depth)
        if blocked is not None:
            return self.error(blocked)

        # 2) 并发闸门：先占坑再判断，判断不过立刻还回去
        running = self._RUNNING.increment()
        try:
            too_many = self.plugin.check_concurrency(running)
            if too_many is not None:
                return self.error(too_many)

            parent_session_id = SessionContext.get()
            workspace_id = self._workspace_id_of(parent_session_id)
            if workspace_id is None:
                return self.error("派子智能体失败：当前会话没有绑定工作区（子智能体需要一个能干活的工作区）")

            child_mode = parse_mode(self.get_string_arg(args, "mode", "standard"))
            model = self.get_string_arg(args, "model", "") or config.model
            if not str(model or "").strip():
                model = None

            child = self.session_manager.create_session(workspace_id, child_mode)
            self.session_manager.rename_session(child.session_id,
                                                "子智能体：" + first_line(task, 24))

            prompt = ("你是被主 Agent 派来做一件具体事情的子智能体，做完就把结论说清楚。\n"
                      f"【任务】\n{task}\n\n"
                      "要求：动手时用工具，别只给建议；做完用一段话给结论（做了什么、结果是什么、"
                      "有什么没做完）。不要反问，除非缺的信息确实无法从工作区推断。")

            previous_depth = self.current_depth()
            self._set_depth(child_depth)
            started = _now_ms__team_subagent_tool()
            try:
                answer = self.agent_loop.process_message(child.session_id, prompt, child_mode,
                                                        ThinkingLevel.LOW, model)
                cost = _now_ms__team_subagent_tool() - started
                print(f"[子智能体] 子智能体完成：层级 {child_depth}，模式 {child_mode}，"
                      f"耗时 {cost} ms，会话 {child.session_id}", flush=True)
                body = answer if answer is not None and str(answer).strip() else "（子智能体没有给出结论）"
                body = str(body)
                if len(body) > MAX_ANSWER_CHARS__team_subagent_tool:
                    body = body[:MAX_ANSWER_CHARS__team_subagent_tool] + "\n…（结论过长已截断）"
                return self.success(
                    f"【子智能体结论】（层级 {child_depth}，模式 {child_mode}，"
                    f"耗时 {cost // 1000} 秒，会话 {child.session_id}）\n{body}")
            finally:
                self._set_depth(previous_depth)
        except Exception as e:
            # 子智能体炸了不能把主任务带崩：回一句错误让模型自己决定是重试还是自己干
            print(f"[子智能体] 子智能体执行异常: {e}", flush=True)
            return self.error(f"子智能体执行异常：{e}（可以自己直接做，或换个说法再派一次）")
        finally:
            self._RUNNING.decrement()

    # ---- 依赖与层级 ----
    def _workspace_id_of(self, session_id: str | None) -> str | None:
        if session_id is None or self.session_manager is None:
            return None
        session = self.session_manager.get_session(session_id)
        return None if session is None else session.workspace_id

    def current_depth(self) -> int:
        """当前这条线程的递归层级（0 = 主 Agent 自己）。"""
        return int(getattr(self._DEPTH, "value", 0))

    def _set_depth(self, depth: int) -> None:
        self._DEPTH.value = int(depth)

    @classmethod
    def running_count(cls) -> int:
        """当前正在跑的子智能体个数（诊断/测试用）。"""
        return cls._RUNNING.get()


def parse_mode(raw: str | None) -> str:
    """解析子智能体模式：认得 minimal/极简 就极简，其余标准（与 Java 一致）。"""
    if raw is None or not str(raw).strip():
        return AgentMode.STANDARD
    s = str(raw).strip().lower()
    if "min" in s or "简" in s:
        return AgentMode.MINIMAL
    return AgentMode.STANDARD


def first_line(text: str, max_chars: int) -> str:
    one = re.sub(r"\s+", " ", str(text)).strip()
    return one if len(one) <= max_chars else one[:max_chars] + "…"


def _now_ms__team_subagent_tool() -> int:
    return int(time.time() * 1000)


# ========================================================================
# 原模块 lionbox/team/registrar.py
# ========================================================================
"""把"子智能体"和"智能体团队"两个工具挂进插件注册表。

【契约来源】逐项对照 Java 版 `core/plugin/team/TeamToolRegistrar.java`。

【为什么不直接在工具类上打 @tool（也不做扫描）】这两个工具要注入 AgentLoop，
而 AgentLoop 又依赖插件注册表 —— 工具如果也走"启动时批量实例化"，很容易和
"注册表 → 工具 → AgentLoop → 注册表"绕成一个环。这里由一个独立的注册器在启动完成后
手动构造再登记，依赖方向永远是单向的，也方便按插件开关决定要不要挂
（用户关掉插件就不注册，模型连工具名都看不到）。
"""




def register_team_tools(registry, subagent_plugin: SubAgentPlugin | None = None,
                        team_plugin: AgentTeamPlugin | None = None,
                        agent_loop=None, session_manager=None, settings=None) -> list[str]:
    """注册 `agent_spawn` 与 `agent_team_run`；返回真正挂上去的 id 列表。

    挂不上最多是少两个工具，绝不能让应用起不来（单个工具单独兜异常）。
    """
    sub = subagent_plugin or SubAgentPlugin(settings)
    team = team_plugin or AgentTeamPlugin(settings)
    tools = [
        ("tool.agent.spawn", SubAgentTool(sub, agent_loop, session_manager)),
        ("tool.agent.team", AgentTeamTool(team, agent_loop, session_manager, settings)),
    ]
    registered: list[str] = []
    for tool_id, tool in tools:
        if registry.is_registered(tool_id):
            continue
        try:
            registry.register(tool)
            registered.append(tool_id)
            print(f"[团队] 智能体团队工具已注册：{tool.name}（{tool_id}）", flush=True)
        except Exception as e:
            print(f"[团队] 注册 {tool_id} 失败: {e}", flush=True)
    return registered


# ========================================================================
# 原模块 lionbox/team.py
# ========================================================================
"""子代理团队（对应 Java `core/plugin/team/`）。

| Java | 这里 |
| --- | --- |
| `TeamMember` | `member.TeamMember` |
| `SubAgentConfig` | `subagent.SubAgentConfig` |
| `SubAgentPlugin` | `subagent.SubAgentPlugin` |
| `SubAgentTool`（`agent_spawn`） | `subagent_tool.SubAgentTool` |
| `AgentTeamPlugin` | `agent_team.AgentTeamPlugin` |
| `AgentTeamTool`（`agent_team_run`） | `agent_team_tool.AgentTeamTool` |
| `TeamToolRegistrar` | `registrar.register_team_tools` |

两条能力：
  * **子智能体**：把一件独立的事整包交给子 Agent，跑完只把结论带回来。可限制
    递归层级（`subagent.maxDepth`）、并发数（`subagent.maxConcurrency`）、所用模型。
  * **智能体团队**：用户自定义一组"谁负责什么"，`agent_team_run` 按配置派活再汇总。
"""



__all__ = [
    "ALLOWED_MODES", "AgentTeamPlugin", "AgentTeamTool", "SubAgentConfig", "SubAgentPlugin",
    "SubAgentTool", "TeamMember", "register_team_tools",
]
