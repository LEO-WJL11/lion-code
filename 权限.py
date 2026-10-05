# -*- coding: utf-8 -*-
r"""权限（由引擎内联生成）
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
    "lionbox.agent.approval",
    "lionbox.agent.change",
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

# 【每个被内联模块各自原本的 __file__】有代码用它推算"程序装在哪"（例如技能目录：
# `skills/repository.py` 往上三层才是安装根）。内联后 `__file__` 全是 main.py 的路径，
# 向上推会跑到仓库外面 —— 实测后果是内置技能一个都找不到。所以按模块各记一份。
# 路径不必真实存在：用到的是路径运算，只要目录层级一致，算出的安装根就一样。
_ORIG_FILE_agent_approval = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\approval.py"
_ORIG_FILE_agent_change = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\agent\change.py"


# ========================================================================
# 原模块 lionbox/agent/approval.py
# ========================================================================
"""审批策略管理器 —— 逐条对照 Java `approval/ApprovalPolicy.java`（121 行）。

管理工具执行的审批策略，已接入 AgentLoop 执行链路：
  · 自动批准：直接执行
  · 需要确认：拒绝执行并明确提示（用户可在设置中把该工具改为自动批准）
  · 禁止执行：拒绝执行

默认策略：所有工具自动批准（保持开箱即用），
用户可通过 `/api/approvals` 接口或设置面板收紧特定工具的审批策略。

【与 `change.py` 的分工】这里是**本地规则**（哪些工具一律禁、哪些要问用户），
快、确定、不花钱；`change.py` 是"AI 改的文件等你点通过才写进磁盘"那道人工作业闸门。
两者互补，都要过。
"""


import threading
from typing import Any, Iterable


class ToolPolicy:
    """工具策略（与 Java enum 同名同值）。"""

    AUTO_APPROVE = "AUTO_APPROVE"
    CONFIRM = "CONFIRM"
    BLOCK = "BLOCK"

    ALL = (AUTO_APPROVE, CONFIRM, BLOCK)

    @staticmethod
    def parse(raw: Any) -> str:
        v = str(raw or "").strip().upper()
        return v if v in ToolPolicy.ALL else ToolPolicy.AUTO_APPROVE


class ApprovalAction:
    """审批动作（带中文显示名，前端设置面板直接用）。"""

    AUTO_APPROVE = "AUTO_APPROVE"
    CONFIRM = "CONFIRM"
    BLOCK = "BLOCK"

    DISPLAY = {
        AUTO_APPROVE: "自动批准",
        CONFIRM: "需要确认",
        BLOCK: "禁止执行",
    }

    @staticmethod
    def display_name(action: str) -> str:
        return ApprovalAction.DISPLAY.get(action, "")


class ApprovalResult:
    """审批结果：`action` + 理由（自动批准时 reason 为 None）。"""

    __slots__ = ("action", "reason")

    def __init__(self, action: str, reason: str | None = None) -> None:
        self.action = action
        self.reason = reason

    @staticmethod
    def auto_approved() -> "ApprovalResult":
        return ApprovalResult(ApprovalAction.AUTO_APPROVE, None)

    @staticmethod
    def requires_confirmation(reason: str) -> "ApprovalResult":
        return ApprovalResult(ApprovalAction.CONFIRM, reason)

    @staticmethod
    def blocked(reason: str) -> "ApprovalResult":
        return ApprovalResult(ApprovalAction.BLOCK, reason)

    def __repr__(self) -> str:
        return f"ApprovalResult({self.action}, reason={self.reason!r})"


#: 出厂默认自动批准的工具 ID（只读操作，显式登记以便查询）
DEFAULT_AUTO_APPROVED: tuple[str, ...] = (
    "tool.file.read", "tool.file.list", "tool.file.search", "tool.file.glob",
    "tool.file.info", "tool.file.headtail", "tool.file.wc", "tool.file.linecount",
    "tool.file.tree", "tool.git.status", "tool.git.log", "tool.git.diff",
    "tool.git.remote", "tool.system.info", "tool.system.env", "tool.system.cwd",
    "tool.code.json", "tool.code.regex", "tool.code.base64", "tool.code.hash",
    "tool.code.uuid", "tool.code.timestamp", "tool.code.diff", "tool.code.string",
    "tool.code.cron", "tool.code.number", "tool.code.markdown", "tool.code.escape",
    "tool.web.search", "tool.http.get", "tool.web.fetch", "tool.web.dns",
)


class ApprovalPolicy:
    """三个集合 + 一把锁。

    【必须整体加锁】Java 版原来是"先清三个集合、再往其中一个加"，中间有窗口：
    并发的 `check_approval` 可能看到该工具**哪个集合里都没有**，于是返回 AUTO_APPROVE ——
    用户刚点了"禁止"的工具还有机会执行一次。`get_policy` 同样可能读到中间态。
    Python 侧用一把 RLock 把"清三个 + 加一个"整体罩住，语义与 Java 的 `synchronized` 一致。
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        #: 自动批准的工具 ID（只读操作默认在此集合）
        self._auto: set[str] = set(DEFAULT_AUTO_APPROVED)
        #: 需要确认的工具 ID
        self._confirm: set[str] = set()
        #: 禁止的工具 ID
        self._blocked: set[str] = set()
        # 注意：写操作（write/shell/git.commit 等）默认不在任何集合中，
        # 按"未知默认自动批准"规则处理，保证 Agent 开箱可用；
        # 需要收紧时由用户显式设置 CONFIRM / BLOCK。

    # ---- 查询 ----
    def check_approval(self, tool_id: str) -> ApprovalResult:
        """检查工具是否需要审批（已接入 AgentLoop.execute_tool）。"""
        with self._lock:
            if tool_id in self._blocked:
                return ApprovalResult.blocked("工具已被禁止: " + tool_id)
            if tool_id in self._confirm:
                return ApprovalResult.requires_confirmation(
                    "工具需要用户确认: " + tool_id + "（请在设置中将其改为自动批准，或保持禁止）")
            # 显式登记的只读工具 + 未登记工具均自动批准（开箱即用）
            return ApprovalResult.auto_approved()

    def get_policy(self, tool_id: str) -> str:
        """获取工具当前生效的审批策略（供查询接口/设置面板使用）。"""
        with self._lock:
            if tool_id in self._blocked:
                return ToolPolicy.BLOCK
            if tool_id in self._confirm:
                return ToolPolicy.CONFIRM
            return ToolPolicy.AUTO_APPROVE

    def get_policies(self, tools: Iterable[Any]) -> dict[str, str]:
        """批量获取工具策略（用于设置面板一次性展示）。

        :param tools: 工具实例（读 `.id`）或工具 id 字符串
        """
        result: dict[str, str] = {}
        for t in tools:
            tid = t if isinstance(t, str) else getattr(t, "id", None)
            if tid:
                result[str(tid)] = self.get_policy(str(tid))
        return result

    # ---- 修改 ----
    def set_tool_policy(self, tool_id: str, policy: str) -> None:
        """设置工具审批策略（一次原子替换三个集合）。"""
        p = ToolPolicy.parse(policy)
        with self._lock:
            self._auto.discard(tool_id)
            self._confirm.discard(tool_id)
            self._blocked.discard(tool_id)
            if p == ToolPolicy.AUTO_APPROVE:
                self._auto.add(tool_id)
            elif p == ToolPolicy.CONFIRM:
                self._confirm.add(tool_id)
            else:
                self._blocked.add(tool_id)

    # ---- 快照（接口/测试用）----
    def snapshot(self) -> dict[str, list[str]]:
        with self._lock:
            return {
                "autoApprove": sorted(self._auto),
                "confirm": sorted(self._confirm),
                "block": sorted(self._blocked),
            }


# ========================================================================
# 原模块 lionbox/agent/change.py
# ========================================================================
"""改动的人工审核闸门 —— 逐条对照 Java `core/agent/change/*.java`
（`Diff.java` 137 行 + `PendingChange.java` 76 行 + `ChangeReview.java` 351 行）。

【用户要的流程】"AI 写代码 → 人工审核 → 通过了这个文件才真正被改；否则打回去重写，
相当于作业。" 所以改文件的工具不再是"一调就落盘"，而是先把**改动**登记成一条待审记录，
立刻返回"已提交待审、未落盘"。人在界面（WebUI 或 VS Code 侧栏）看到 diff，点通过才真写，
点打回就丢掉并把理由回给模型，让它重写。

【为什么放在工具里而不是 AgentLoop 里】只有工具自己知道"改完的文件内容长什么样"
（尤其是 modify_file 的按行替换），在循环层拦是拿不到 diff 的。所以闸门做成一个
由工具调用的服务：`intercept` —— 一行调用，命中就返回"待审"结果。

【开关】认插件 `plugin.change-review` 的开关（设置里可关）。关掉就是老行为：直接落盘。
默认开 —— 这是用户明确要的默认。
"""


import os
import threading
import time
from pathlib import Path
from typing import Any

#: 插件 id：设置里那个开关就是它
PLUGIN_ID = "plugin.change-review"

PENDING = "PENDING"
APPROVED = "APPROVED"
REJECTED = "REJECTED"


# ==========================================================================
# 行级差异（Diff.java）
# ==========================================================================


class Diff:
    """给人看的行级差异。

    【为什么自己写而不引库】要的就是"人扫一眼能看出改了哪几行"，不值得为此拖进一个
    diff 库；而且这里必须对**超大文件**有防护：几十万行的文件做 LCS 会直接把内存吃光，
    所以超过阈值就退化成"整文件替换"的摘要，并明确写出来（不装作是逐行 diff）。

    输出用常见的前缀：`+` 新增、`-` 删除、` ` 不变（只在不远处展示几行上下文）。
    """

    #: 超过多少行就放弃逐行比对（LCS 是 O(n*m)，这里 4000×4000 已经是上限）
    MAX_LINES_FOR_LCS = 4000
    #: 差异块前后各留几行上下文
    CONTEXT = 2
    #: 最多输出多少行（界面不需要看完整 diff，超了截断并注明）
    MAX_OUTPUT_LINES = 400

    @staticmethod
    def render(path: str, old_content: str | None, new_content: str | None) -> str:
        sb: list[str] = []
        if old_content is None:
            sb.append("新建文件：" + path + "\n")
            Diff._append_all(sb, "+", new_content)
            return "".join(sb)
        if new_content is None:
            sb.append("删除文件：" + path + "\n")
            Diff._append_all(sb, "-", old_content)
            return "".join(sb)
        if old_content == new_content:
            return "内容没有变化（" + path + "）"

        a = old_content.split("\n")
        b = new_content.split("\n")
        if len(a) > Diff.MAX_LINES_FOR_LCS or len(b) > Diff.MAX_LINES_FOR_LCS:
            sb.append("整文件替换：" + path + "\n")
            sb.append("  （文件太大，不做逐行比对：原 " + str(len(a))
                      + " 行 → 新 " + str(len(b)) + " 行）\n")
            Diff._append_all(sb, "+", new_content)
            return "".join(sb)

        ops = Diff._lcs_ops(a, b)      # 每项 (type, i, j)：0=保持 1=删 2=增
        changed = [k for k, op in enumerate(ops) if op[0] != 0]
        if not changed:
            return "内容没有变化（" + path + "）"

        sb.append(path + "：" + str(len(changed)) + " 处行变化\n")
        printed = 0
        last_printed = -99
        for idx in changed:
            if printed >= Diff.MAX_OUTPUT_LINES:
                sb.append("…… 还有更多差异，已截断（总共 " + str(len(changed)) + " 行变化）\n")
                break
            start = max(0, idx - Diff.CONTEXT)
            if start > last_printed + 1:
                sb.append("  ...\n")
            for k in range(max(start, last_printed + 1), min(len(ops) - 1, idx + Diff.CONTEXT) + 1):
                op = ops[k]
                if op[0] == 0:
                    sb.append("   " + a[op[1]] + "\n")
                elif op[0] == 1:
                    sb.append("  -" + a[op[1]] + "\n")
                else:
                    sb.append("  +" + b[op[2]] + "\n")
                printed += 1
            last_printed = min(len(ops) - 1, idx + Diff.CONTEXT)
        return "".join(sb)

    @staticmethod
    def _append_all(sb: list[str], prefix: str, content: str | None) -> None:
        if content is None:
            return
        lines = content.split("\n")
        n = min(len(lines), Diff.MAX_OUTPUT_LINES)
        for i in range(n):
            sb.append(" " + prefix + lines[i] + "\n")
        if len(lines) > n:
            sb.append("  …… 还有 " + str(len(lines) - n) + " 行（已截断）\n")

    @staticmethod
    def _lcs_ops(a: list[str], b: list[str]) -> list[tuple[int, int, int]]:
        """标准 LCS + 回溯，返回操作序列（与 Java `lcsOps` 逐行等价）。"""
        n = len(a)
        m = len(b)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        for i in range(n - 1, -1, -1):
            row = dp[i]
            nxt = dp[i + 1]
            ai = a[i]
            for j in range(m - 1, -1, -1):
                row[j] = nxt[j + 1] + 1 if ai == b[j] else max(nxt[j], row[j + 1])
        ops: list[tuple[int, int, int]] = []
        i = j = 0
        while i < n and j < m:
            if a[i] == b[j]:
                ops.append((0, i, j))
                i += 1
                j += 1
            elif dp[i + 1][j] >= dp[i][j + 1]:
                ops.append((1, i, -1))
                i += 1
            else:
                ops.append((2, -1, j))
                j += 1
        while i < n:
            ops.append((1, i, -1))
            i += 1
        while j < m:
            ops.append((2, -1, j))
            j += 1
        return ops


# ==========================================================================
# 一条待审改动（PendingChange.java）
# ==========================================================================


class PendingChange:
    """一条待人工审核的改动。

    字段与 Java record 一一对应：id / sessionId / toolName / path / existed /
    oldContent / newContent / diff / createdAt / status / reason。
    """

    __slots__ = ("id", "session_id", "tool_name", "path", "existed", "old_content",
                 "new_content", "diff", "created_at", "status", "reason")

    PENDING = PENDING
    APPROVED = APPROVED
    REJECTED = REJECTED

    def __init__(self, change_id: str, session_id: str | None, tool_name: str, path: str,
                 existed: bool, old_content: str | None, new_content: str | None,
                 diff: str, created_at: int, status: str, reason: str | None) -> None:
        self.id = change_id
        self.session_id = session_id
        self.tool_name = tool_name
        self.path = path
        self.existed = existed
        self.old_content = old_content
        self.new_content = new_content
        self.diff = diff
        self.created_at = created_at
        self.status = status
        self.reason = reason

    def with_status(self, new_status: str, new_reason: str | None) -> "PendingChange":
        return PendingChange(self.id, self.session_id, self.tool_name, self.path, self.existed,
                             self.old_content, self.new_content, self.diff, self.created_at,
                             new_status, new_reason)

    def summary(self) -> dict[str, Any]:
        """给界面看的摘要（不返回全文，几十 KB 的内容不该塞进列表接口）。

        字段名与 Java 版一字不差（前端按这些键渲染），null 字段整个省略
        （Java 侧是 `@JsonInclude(NON_NULL)`）。
        """
        m: dict[str, Any] = {
            "id": self.id,
            "sessionId": self.session_id,
            "toolName": self.tool_name,
            "path": self.path,
            "existed": self.existed,
            "status": self.status,
        }
        if self.reason is not None:
            m["reason"] = self.reason
        m["createdAt"] = self.created_at
        m["diff"] = self.diff
        m["addedLines"] = _count_lines(self.new_content)
        m["removedLines"] = _count_lines(self.old_content) if (self.existed and self.old_content is not None) else 0
        return m

    def __repr__(self) -> str:
        return (f"PendingChange({self.id}, {self.tool_name}, {self.path}, "
                f"{self.status})")


def _count_lines(s: str | None) -> int:
    if not s:
        return 0
    return s.count("\n") + 1


# ==========================================================================
# 审核闸门（ChangeReview.java）
# ==========================================================================


class ChangeReview:
    """改动的人工审核闸门。

    :param history: 会话历史（`add_message(session_id, role, content)` 形状）；
                    审核通过/打回后要往会话里插一条 system 消息，让模型下一轮看得见。
    :param settings: 插件开关（`is_enabled(plugin_id, default) -> bool`）；传 None 就用出厂默认。
    :param enabled_by_default: 出厂默认：True（用户要的就是"先审后用"）。
    """

    PLUGIN_ID = PLUGIN_ID
    #: 每个会话最多留多少条记录，防止长跑会话把内存堆满
    MAX_PER_SESSION = 200

    def __init__(self, history: Any = None, settings: Any = None,
                 enabled_by_default: bool = True) -> None:
        self.history = history
        self.settings = settings
        self.enabled_by_default = bool(enabled_by_default)
        self._lock = threading.RLock()
        #: id -> 改动。审完也留着（界面能回看"通过/打回了什么"），重启后清空
        self._changes: dict[str, PendingChange] = {}
        self._seq = 0

    # ------------------------------------------------------------ 开关
    def enabled(self) -> bool:
        """审核开着吗。

        判定顺序：用户在设置里点过的插件开关（落盘、重启还在）→ 出厂默认值
        （配置项 `lionbox.change-review.enabled`，默认 True）。

        【踩过的坑】第一版写成"插件注册了就问插件自己的 isEnabledByDefault()"，
        结果配置项那个开关**完全不起作用** —— 测试环境用
        `--lionbox.change-review.enabled=false` 关它，文件还是全被拦下来待审，
        五个工具用例一起红。配置项必须就是"没人点过开关时用的默认值"，插件注册与否都一样。
        """
        if self.settings is None:
            return self.enabled_by_default
        try:
            return bool(self.settings.is_enabled(PLUGIN_ID, self.enabled_by_default))
        except Exception:
            return self.enabled_by_default

    # ------------------------------------------------------------ 闸门
    def intercept(self, tool_name: str, path: str, old_content: str | None,
                  new_content: str | None, session_id: str | None = None) -> Any | None:
        """闸门：改文件前调它。

        :return: 有值 = **不要落盘**，直接把返回的 ToolResult 交回去（已经登记待审）；
                 None = 照常落盘。
        """
        if not self.enabled():
            return None
        # 【会话 id 必须在这里补上】工具的闸门接线点（`tools/file/_gate.intercept`）只传
        # 4 个参数（与 Java 的 `ChangeReview.intercept(name, path, old, new)` 同形），
        # 会话 id 由 SessionContext 提供 —— Java 里也是这么写的：
        # `String sessionId = SessionContext.get();`。
        # 不补的话每条待审改动都记在 sessionId=None 名下，
        # `GET /api/changes?sessionId=X` 永远返回空（pendingCount=0），
        # 界面上"待审改动"那一栏永远看不见东西（`_check_context_review.py` 抓到的就是这个）。
        if session_id is None:
            try:
                from lionbox.sessions import SessionContext
                session_id = SessionContext.get()
            except Exception:                           # noqa: BLE001 会话模块缺失时按无会话处理
                session_id = None
        from lionbox.plugins.base import ToolResult
        c = self.submit(session_id, tool_name, path, old_content, new_content)
        action = "删除" if new_content is None else ("新建" if old_content is None else "修改")
        return ToolResult.ok(
            "已提交人工审核，**还没落盘**。\n"
            "  编号：" + c.id + "\n"
            "  文件：" + path + "（" + action + "）\n"
            "  人在界面上点「通过」之后才会真正写进去；点「打回」你会收到理由，按理由重写。\n"
            "  现在继续做别的、或者直接结束这一轮都行 —— 别再重复提交同一个文件的改动。")

    # ------------------------------------------------------------ 登记
    def submit(self, session_id: str | None, tool_name: str, path: str,
               old_content: str | None, new_content: str | None) -> PendingChange:
        """登记一条待审改动。"""
        with self._lock:
            self._seq += 1
            seq = self._seq
            change_id = "C" + str(int(time.time() * 1000) % 100000) + "-" + str(seq)
            diff = Diff.render(path, old_content, new_content)
            c = PendingChange(change_id, session_id, tool_name, path,
                              old_content is not None, old_content, new_content, diff,
                              int(time.time() * 1000), PENDING, None)
            self._changes[change_id] = c
            self._trim(session_id)
        return c

    # ------------------------------------------------------------ 查询
    def list(self, session_id: str | None, include_decided: bool = False) -> list[PendingChange]:
        """待审列表（默认只给待审；include_decided=True 连已通过/已打回的一起给，界面回看用）。"""
        out: list[PendingChange] = []
        with self._lock:
            for c in self._changes.values():
                if session_id is not None and session_id.strip() and session_id != c.session_id:
                    continue
                if not include_decided and c.status != PENDING:
                    continue
                out.append(c)
        out.sort(key=lambda x: x.created_at)
        return out

    def get(self, change_id: str) -> PendingChange | None:
        with self._lock:
            return self._changes.get(change_id)

    def stats(self, session_id: str | None) -> dict[str, Any]:
        """统计信息（界面顶部显示"还有几条待审"）。"""
        pending = self.list(session_id, False)
        return {
            "enabled": self.enabled(),
            "pendingCount": len(pending),
            "pending": [c.summary() for c in pending],
        }

    # ------------------------------------------------------------ 裁决
    def approve(self, change_id: str) -> PendingChange:
        """通过：真落盘，并把结论告诉模型（下一条消息它就看得见）。"""
        c = self._require(change_id)
        if c.status != PENDING:
            raise RuntimeError("这条改动已经处理过了：" + c.status)
        try:
            p = Path(c.path)
            if c.new_content is None:
                _delete_target(p)
            else:
                # 【先确认文件没被别人改过】人工审核的意义就是"人看过这个 diff 才放行"。
                # 从提交到点「通过」之间，文件可能被用户自己、别的工具或 git pull 改过；
                # 直接写下去就是拿模型基于**旧内容**算出来的结果，覆盖掉这些新改动。
                current = _decode(p) if p.is_file() else None
                if c.old_content is not None and current is not None \
                        and _comparable(current) != _comparable(c.old_content):
                    raise _ConflictError(
                        "文件在提交审核之后被改动过，为避免覆盖新内容，本次写入已取消。"
                        "请让 Agent 重新读取该文件并重新提交改动。")
                if p.parent is not None and str(p.parent):
                    p.parent.mkdir(parents=True, exist_ok=True)
                payload = _preserve_line_separator(p, c.new_content)
                p.write_bytes(payload.encode(_charset_of(p), errors="replace"))
        except _ConflictError:
            raise
        except OSError as e:
            raise RuntimeError("写入失败: " + str(e)) from e
        done = c.with_status(APPROVED, None)
        with self._lock:
            self._changes[change_id] = done
        self._note(c.session_id, "【人工审核】改动 " + change_id + " 已通过，已写入 " + c.path
                   + "（" + ("删除" if c.new_content is None
                             else "写入 " + str(len(c.new_content)) + " 字符") + "）。")
        return done

    def reject(self, change_id: str, reason: str | None = None) -> PendingChange:
        """打回：不落盘，把理由回给模型让它重写。"""
        c = self._require(change_id)
        if c.status != PENDING:
            raise RuntimeError("这条改动已经处理过了：" + c.status)
        done = c.with_status(REJECTED, reason if reason is not None else "")
        with self._lock:
            self._changes[change_id] = done
        self._note(c.session_id, "【人工审核】改动 " + change_id + "（" + c.path
                   + "）被**打回**，没有落盘。"
                   + ("" if not reason or not reason.strip() else "打回理由：" + reason + "。")
                   + "请按这个理由重写，然后重新提交。")
        return done

    # ------------------------------------------------------------ 内部
    def _note(self, session_id: str | None, text: str) -> None:
        """把结论写进会话历史。

        写成 system 消息：AgentLoop 重建历史时会把它降级成带【系统提示】前缀的
        user 消息，模型下一轮必然看到；用户也能在对话里看到"这条改动通过了/被打回了"。

        `lionbox/sessions/ConversationHistory.add_message()` 收的是**一条 ConversationMessage**
        （同 Java）。这里优先用 `ConversationMessage.system(...)` 造对象；退路是
        `history.add_message(session_id, "system", text)`（内存桩那种签名）。
        """
        if session_id is None or not session_id.strip() or self.history is None:
            return
        add = getattr(self.history, "add_message", None)
        if add is None:
            add = getattr(self.history, "add", None)
        if add is None:
            return
        try:
            try:
                from lionbox.sessions.message import ConversationMessage
                add(ConversationMessage.system(session_id, text))
                return
            except Exception:
                pass
            add(session_id, "system", text)
        except Exception:
            # 会话历史写不进去不该让"点通过"失败 —— 文件已经落盘了
            pass

    def _require(self, change_id: str) -> PendingChange:
        with self._lock:
            c = self._changes.get(change_id)
        if c is None:
            raise KeyError("没有这条改动：" + change_id)
        return c

    def _trim(self, session_id: str | None) -> None:
        """每个会话只留最近 MAX_PER_SESSION 条，超了丢最老的（已处理过的优先丢）。

        【审计发现】原来的循环只在"状态不是待审"时才 remove：如果这 200 条**全是待审**，
        drop 一条都减不掉，映射继续无界增长（模型连续提交、用户不点通过就会一直涨）。
        现在先丢已处理的；还不够就丢最老的**待审**记录（drop oldest pending）。
        """
        mine = [c for c in self._changes.values() if c.session_id == session_id]
        if len(mine) <= self.MAX_PER_SESSION:
            return
        drop = len(mine) - self.MAX_PER_SESSION
        mine.sort(key=lambda x: x.created_at)
        for c in mine:
            if drop <= 0:
                break
            if c.status != PENDING:
                self._changes.pop(c.id, None)
                drop -= 1
        for c in mine:
            if drop <= 0:
                break
            if c.status == PENDING:
                self._changes.pop(c.id, None)
                drop -= 1


class _ConflictError(RuntimeError):
    """文件在提交审核之后被改动过（Java 侧是 IllegalStateException）。"""


# ------------------------------------------------------------------ 文件助手
# 口径必须与工具侧的 AbstractToolPlugin 一致，否则"同一个动作走不走人工审核结果不一样"。


def _delete_target(p: Path) -> None:
    """执行一条"删除类"改动（new_content is None）。

    【为什么不能只用 unlink】`delete_file` 支持 `recursive=true` 的目录删除，
    它登记的就是 newContent=null；而 approve() 原来只调 `deleteIfExists(p)` ——
    对非空目录直接抛 DirectoryNotEmptyException，用户点「通过」永远得到
    "写入失败: …目录不是空的"，这条改动**永远批不掉**。
    目录一律按递归删除处理，和工具侧的语义保持一致。
    """
    if not p.is_dir():
        try:
            p.unlink()
        except FileNotFoundError:
            pass
        return
    # 先删子项再删父目录：深度优先，最深的先删
    for root, dirs, files in os.walk(p, topdown=False):
        for name in files:
            try:
                (Path(root) / name).unlink()
            except FileNotFoundError:
                pass
        for name in dirs:
            try:
                (Path(root) / name).rmdir()
            except OSError:
                pass
    try:
        p.rmdir()
    except FileNotFoundError:
        pass


def _decode(p: Path) -> str:
    """按文件原编码读回（口径与 AbstractToolPlugin.decodeText 一致）。"""
    return p.read_bytes().decode(_charset_of(p), errors="replace")


def _comparable(s: str | None) -> str | None:
    """比对用的规范化。

    不同工具登记旧内容的口径不完全一样：`write_file`/`append_file` 传的是原样读出的文本
    （保留 \\r\\n 与结尾换行），`modify_file` 传的是 readTextLines 之后用 "\\n" 拼回来的
    （\\r 已被剥掉、结尾空行已去掉）。所以比对前统一换行、去掉结尾空白，
    避免"文件根本没被人动过却误报冲突"。
    """
    if s is None:
        return None
    return s.replace("\r\n", "\n").replace("\r", "\n").rstrip()


def _preserve_line_separator(p: Path, content: str) -> str:
    """保留文件原有的换行风格。

    `modify_file` 在"直接写"那条路上是**特意**按检测到的分隔符写回的；
    而审核通过这条路原来直接写 LF 拼出来的字符串，于是一个只改了一行的 .bat/.cmd/.csproj
    会被**整体改成 LF**。同一个动作走不走人工审核结果不一样，这是不对的。
    """
    try:
        if not p.is_file():
            return content
        raw = p.read_bytes()
        if b"\r\n" in raw:
            return content.replace("\r\n", "\n").replace("\n", "\r\n")
    except OSError:
        pass   # 读不了就按原样写
    return content


def _charset_of(p: Path) -> str:
    """和工具那边的口径一致：已有文件按原编码写回；新文件 UTF-8。

    【必须用严格解码】Java 版原来这里是 `new String(bytes, UTF_8)` 再看有没有 U+FFFD ——
    `new String` 遇到非法字节不抛异常、只替换成 U+FFFD；而很多 GBK 字节对本身就是合法
    UTF-8 序列、能解出别的字符且不产生 U+FFFD，于是 GBK 文件会被判成 UTF-8。
    表现：同一个文件走"直接写"是 GBK、走"人工审核通过"就变成 UTF-8。

    Python 的 `bytes.decode("utf-8")` 默认就是严格模式（等价于 Java 的 REPORT），
    非法字节直接抛 UnicodeDecodeError —— 正好是我们要的口径。
    """
    try:
        if not p.is_file():
            return "utf-8"
        data = p.read_bytes()
        if not data:
            return "utf-8"
        data.decode("utf-8")        # 严格：失败即非 UTF-8
        return "utf-8"
    except (OSError, UnicodeDecodeError):
        return "gbk"


def pending_changes_none() -> list[PendingChange]:
    """待审列表（按时间正序）—— 对应 Java 的 `PendingChange.none()`。"""
    return []
