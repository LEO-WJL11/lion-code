# -*- coding: utf-8 -*-
r"""沙箱（由引擎内联生成）
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
    "lionbox.workspace.context",
    "lionbox.workspace.manager",
    "lionbox.workspace",
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


# 【每个被内联模块各自原本的 __file__】有代码用它推算"程序装在哪"（例如技能目录：
# `skills/repository.py` 往上三层才是安装根）。内联后 `__file__` 全是 main.py 的路径，
# 向上推会跑到仓库外面 —— 实测后果是内置技能一个都找不到。所以按模块各记一份。
# 路径不必真实存在：用到的是路径运算，只要目录层级一致，算出的安装根就一样。
_ORIG_FILE_workspace_context = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\workspace\context.py"
_ORIG_FILE_workspace_manager = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\workspace\manager.py"
_ORIG_FILE_workspace = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\workspace\__init__.py"


# ========================================================================
# 原模块 lionbox/workspace/context.py
# ========================================================================
"""工具执行期间的工作区上下文（线程级）。

【契约来源】逐项对照 Java 版 `core/workspace/WorkspaceContext.java`：
线程局部存储、严格沙箱开关、`resolve()` 的三条分支（绝对路径 / 相对路径 / 没绑定工作区）、
以及**两条分支都要做的两道检查**（归一化包含性 + 真实路径包含性）全部照抄。

AgentLoop 在执行工具前设置当前会话绑定的工作区路径，各工具通过 `resolve()` 把相对路径
解析到工作区根目录下，从而实现"选择工作区 → 工具真正在该工作区内操作"。

沙箱：严格模式下，绑定工作区后绝对路径必须位于工作区内，否则抛
`WorkspaceViolation`（工具层统一捕获并返回错误），防止工具越界访问工作区外的文件。

【相对路径为什么也要校验】以前只有绝对路径分支做校验，相对路径直接拼接就返回了 ——
`path="..\\..\\..\\Windows\\System32\\drivers\\etc\\hosts"` 会原样拼成
`C:\\ws\\..\\..\\..\\Windows\\...\\hosts` 交给工具，工具再 normalize 之后就落在工作区外面：
沙箱形同虚设（写文件、读文件、删除全都逃得出去）。现在统一归一化之后再判断。
"""


import os
from pathlib import Path
from threading import local
from typing import Any

#: 严格沙箱开关的配置名（等价 Java 的 `lion.workspace.strict`，Python 侧读环境变量）
ENV_STRICT = "LION_WORKSPACE_STRICT"

_LOCAL = local()
_STRICT = True


class WorkspaceViolation(RuntimeError):
    """路径越界（对齐 Java 抛的 `IllegalStateException`，工具层捕获后回错误给模型）。"""


class WorkspaceContext:
    """与 Java 一样是纯静态工具类（不是需要注入的对象）。"""

    @staticmethod
    def set(workspace_path: str | os.PathLike[str] | None) -> None:
        """设置当前线程的工作区路径。"""
        _LOCAL.workspace = None if workspace_path is None else str(workspace_path)

    @staticmethod
    def get() -> str | None:
        """当前线程的工作区路径（可能为 None）。"""
        return getattr(_LOCAL, "workspace", None)

    @staticmethod
    def clear() -> None:
        """清除当前线程的工作区上下文。"""
        _LOCAL.workspace = None

    @staticmethod
    def set_strict_mode(strict: bool) -> None:
        """设置严格沙箱开关（由配置注入）。"""
        global _STRICT
        _STRICT = bool(strict)

    @staticmethod
    def is_strict_mode() -> bool:
        return _STRICT

    @staticmethod
    def resolve(raw_path: str | os.PathLike[str] | None) -> str | None:
        """解析路径：

        * 绝对路径：严格模式下校验必须位于工作区内（越界抛 `WorkspaceViolation`）
        * 相对路径：拼接到工作区根目录下，**并且同样做越界校验**
        * 无工作区上下文：原样返回（未绑定工作区时不限制）
        """
        if raw_path is None or str(raw_path).strip() == "":
            return raw_path if raw_path is None else str(raw_path)
        raw = str(raw_path)
        path = Path(raw)
        ws = WorkspaceContext.get()
        strict = _STRICT and bool(ws and str(ws).strip())

        if path.is_absolute():
            if strict:
                ws_path = _norm(ws)
                absolute = _norm(raw)
                _check_inside(absolute, ws_path, raw, ws)
                # 符号链接/junction 也要拦：normpath 只处理 ".."，不会解析链接
                _check_real_path_inside(absolute, ws_path, raw, ws)
            return raw

        if not ws or not str(ws).strip():
            return raw
        ws_path = _norm(ws)
        resolved = Path(os.path.normpath(os.path.join(str(ws_path), raw)))
        if strict:
            # 校验放在归一化之后：先判断再归一化是典型漏洞（校验用的是没归一化的串）
            _check_inside(resolved, ws_path, raw, ws)
            # 【必须和绝对路径分支走同一道链接检查】否则工作区内一个指向外面的链接
            # （ws\link -> C:\Windows）用相对路径 "link\System32\..." 就能穿出去，
            # 而同一个目标用绝对路径写却会被拦下 —— 两条分支行为必须一致。
            _check_real_path_inside(resolved, ws_path, raw, ws)
        return str(resolved)

    @staticmethod
    def is_inside(candidate: str | os.PathLike[str] | None,
                  root: str | os.PathLike[str] | None) -> bool:
        """给定路径是否在根目录内（不做越界抛错，供调用方自己决定怎么报）。"""
        if candidate is None or root is None:
            return False
        try:
            real_candidate = _real_or_self(_norm(candidate))
            real_root = _real_or_self(_norm(root))
        except OSError:
            return False
        return _starts_with(real_candidate, real_root)


def _norm(value: Any) -> Path:
    """绝对化 + 归一化（不解析符号链接）。"""
    return Path(os.path.normpath(os.path.abspath(str(value))))


def _check_inside(candidate: Path, ws_path: Path, raw_path: str, ws: str | None) -> None:
    """归一化后的包含性判断。"""
    if not _starts_with(candidate, ws_path):
        raise WorkspaceViolation(
            f"路径在工作区之外，已阻止访问: {raw_path}（当前工作区: {ws}）")


def _check_real_path_inside(absolute: Path, ws_path: Path, raw_path: str,
                            ws: str | None) -> None:
    """解析真实路径（跟随符号链接）后再判一次。

    目标不存在时（新建文件的场景）用父目录判断，父目录也不存在就跳过 ——
    这种情况由 `_check_inside` 的字符串判断兜底。
    """
    real = absolute
    if not real.exists():
        parent = real.parent
        if parent is None or str(parent) == str(real):
            return
        real = parent
    try:
        real_path = _real_or_self(real)
        real_ws = _real_or_self(ws_path) if ws_path.exists() else ws_path
    except OSError:
        # 拿不到真实路径（权限等）：退回字符串判断的结果，不额外放行也不额外拦截
        return
    _check_inside(real_path, real_ws, raw_path, ws)


def _real_or_self(path: Path) -> Path:
    """`os.path.realpath` 的包装：Windows 上路径不存在时也返回归一化结果。"""
    return Path(os.path.realpath(str(path)))


def _starts_with(candidate: Path, root: Path) -> bool:
    """大小写不敏感的包含性判断（Windows 盘符/路径大小写不敏感）。"""
    try:
        candidate.relative_to(root)
        return True
    except ValueError:
        if os.name != "nt":
            return False
    c = str(candidate).lower().replace("/", "\\").rstrip("\\")
    r = str(root).lower().replace("/", "\\").rstrip("\\")
    return c == r or c.startswith(r + "\\")


def strict_from_env(default: bool = True) -> bool:
    """读 `LION_WORKSPACE_STRICT`（对应 Java 的 `lion.workspace.strict`，默认开）。"""
    raw = os.environ.get(ENV_STRICT, "").strip().lower()
    if not raw:
        return default
    return raw not in ("false", "0", "no", "off", "否", "关")


def install_strict_mode_from_env() -> bool:
    """把环境变量里的严格开关装进 `WorkspaceContext`（app 启动时调一次）。"""
    strict = strict_from_env()
    WorkspaceContext.set_strict_mode(strict)
    return strict


__all__ = ["ENV_STRICT", "WorkspaceContext", "WorkspaceViolation", "install_strict_mode_from_env",
           "strict_from_env"]


# ========================================================================
# 原模块 lionbox/workspace/manager.py
# ========================================================================
"""工作区管理器 —— 逐项对照 Java `core/workspace/WorkspaceManager.java`。

三级工作区权限：只读 / 工作区写 / 全部权限。**强制绑定工作区**：未选择工作区，
不能创建和使用对话会话（这条由 `sessions/manager.py` 执行）。

【为什么必须持久化权限】原来工作区只在内存里，重启后由启动恢复流程按会话重新注册、
权限一律回到默认的 WORKSPACE_WRITE —— 用户特意设成"只读"的工作区（这是界面上明确提供、
且 AgentLoop 真的会强制执行的安全控制）重启一次就悄悄又能写了。存一份到
`app-config.json` 的 `workspaces` 键下，代价极小。
"""


import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any


#: 权限存在 app-config.json 的这个键下（键名与 Java 一字不差）
CFG_WORKSPACES = "workspaces"


class WorkspacePermission:
    """工作区权限枚举（值与 Java 一字不差 —— 它会被持久化，改名字会让老配置读不出来）。"""

    READ_ONLY = "READ_ONLY"
    WORKSPACE_WRITE = "WORKSPACE_WRITE"
    FULL_ACCESS = "FULL_ACCESS"

    ALL = (READ_ONLY, WORKSPACE_WRITE, FULL_ACCESS)

    DISPLAY = {
        READ_ONLY: "只读",
        WORKSPACE_WRITE: "工作区写",
        FULL_ACCESS: "全部权限",
    }

    @staticmethod
    def parse(raw: Any) -> str:
        v = str(raw or "").strip().upper()
        return v if v in WorkspacePermission.ALL else WorkspacePermission.WORKSPACE_WRITE


@dataclass(frozen=True)
class Workspace:
    """工作区数据类（Java 的 `record Workspace(id, path, permission)`）。"""

    id: str                       # noqa: A003
    path: str
    permission: str = WorkspacePermission.WORKSPACE_WRITE

    def to_map(self) -> dict[str, Any]:
        return {"path": self.path, "permission": self.permission}


class WorkspaceManager:
    """工作区的注册 / 查询 / 权限管理（含持久化）。"""

    def __init__(self, config_store: AppConfigStore | None = None) -> None:
        """不传 `config_store` 时不读也不写 app-config.json（探针/单测用）。"""
        from lionbox.config.store import AppConfigStore
        self.config_store = config_store
        self._workspaces: dict[str, Workspace] = {}
        self._lock = threading.RLock()
        self._restore_from_config()

    # ------------------------------------------------------------------
    # 持久化
    # ------------------------------------------------------------------
    def _restore_from_config(self) -> None:
        """启动时恢复工作区与它们各自的权限等级。"""
        if self.config_store is None:
            return
        raw = self.config_store.get(CFG_WORKSPACES, None)
        if not isinstance(raw, dict):
            return
        restored = 0
        for workspace_id, instance in raw.items():
            if not isinstance(instance, dict):
                continue
            path = instance.get("path")
            if not isinstance(path, str) or not path.strip():
                continue
            permission = WorkspacePermission.parse(instance.get("permission"))
            self._workspaces[str(workspace_id)] = Workspace(str(workspace_id), path, permission)
            restored += 1
        if restored:
            print(f"[工作区] 已从配置恢复 {restored} 个工作区（含权限等级）", flush=True)

    def _persist_to_config(self) -> None:
        """整份覆盖落盘（工作区数量很小，不值得做增量）。"""
        if self.config_store is None:
            return
        out: dict[str, Any] = {}
        with self._lock:
            for workspace in self._workspaces.values():
                out[workspace.id] = workspace.to_map()
        self.config_store.set(CFG_WORKSPACES, out)

    # ------------------------------------------------------------------
    # 注册 / 查询
    # ------------------------------------------------------------------
    def register_workspace(self, path: str, permission: str | None = None) -> Workspace:
        """注册工作区（默认授予"工作区写"权限）。

        已经注册过的工作区**不覆盖它已有的权限等级**：前端每次启动都会调
        `GET /api/workspaces/default` 重新注册一遍默认工作区，以前那会把用户手动设成
        "只读/全部权限"的工作区悄悄改回"工作区写"。

        【空/非法路径必须在这里就拦下】`Path("")` 等于**当前进程工作目录**，
        会把用户根本没选过的目录静默注册成工作区。

        :raises ValueError: 路径为空或不是合法路径
        """
        workspace_id = workspace_id_of(path)
        with self._lock:
            existing = self._workspaces.get(workspace_id)
            if existing is not None and permission is None:
                return existing
        return self._store(Workspace(workspace_id, path,
                                     WorkspacePermission.parse(permission)))

    def set_permission(self, workspace_id: str, permission: str) -> bool:
        """更新工作区权限等级（只读 / 工作区写 / 全部权限）。

        权限在 AgentLoop 执行工具时强制执行；写入后立即落盘，否则"只读"重启后又能写。
        """
        with self._lock:
            existing = self._workspaces.get(workspace_id)
            if existing is None:
                print(f"[工作区] 更新权限失败，工作区不存在: {workspace_id}", flush=True)
                return False
            self._workspaces[workspace_id] = Workspace(existing.id, existing.path,
                                                       WorkspacePermission.parse(permission))
        self._persist_to_config()
        print(f"[工作区] 工作区权限已更新: {workspace_id} -> {permission}", flush=True)
        return True

    def get_workspace(self, workspace_id: str | None) -> Workspace | None:
        """获取工作区（没有返回 None）。"""
        if workspace_id is None:
            return None
        with self._lock:
            return self._workspaces.get(str(workspace_id))

    def get_all_workspaces(self) -> list[Workspace]:
        with self._lock:
            return list(self._workspaces.values())

    def permission_of(self, workspace_id: str | None) -> str | None:
        """某个工作区的权限等级（未注册返回 None）。

        给 AgentLoop / 工具层做权限判定用（Java 侧由 `WorkspaceManager` 查、AgentLoop 执行）。
        """
        workspace = self.get_workspace(workspace_id)
        return None if workspace is None else workspace.permission

    def __len__(self) -> int:
        with self._lock:
            return len(self._workspaces)

    # ------------------------------------------------------------------
    def _store(self, workspace: Workspace) -> Workspace:
        with self._lock:
            self._workspaces[workspace.id] = workspace
        self._persist_to_config()
        print(f"[工作区] 工作区已注册: {workspace.path} (权限: {workspace.permission})", flush=True)
        return workspace


def workspace_id_of(path: str | None) -> str:
    """路径校验 + 归一化成工作区 ID（绝对路径）。

    :raises ValueError: 路径为空或非法
    """
    if path is None or not str(path).strip():
        raise ValueError("工作区路径不能为空")
    try:
        return str(Path(str(path)).absolute())
    except (OSError, ValueError) as e:
        # Windows 上的非法字符会抛 OSError/ValueError：统一成 ValueError，
        # 接口层才拦得住（否则用户看到的是 500）
        raise ValueError(f"工作区路径非法: {path}") from e


def normalize_permission(raw: Any) -> str:
    """权限名归一（脏配置回默认 WORKSPACE_WRITE，与 Java 的 try/catch 一致）。"""
    return WorkspacePermission.parse(raw)


__all__ = ["CFG_WORKSPACES", "Workspace", "WorkspaceManager", "WorkspacePermission",
           "normalize_permission", "workspace_id_of"]


# ========================================================================
# 原模块 lionbox/workspace.py
# ========================================================================
"""工作区（对应 Java `core/workspace/`）。

| Java | 这里 |
| --- | --- |
| `WorkspaceContext`（线程级工作区 + 严格沙箱） | `context.WorkspaceContext` |
| `WorkspaceManager`（注册 / 权限 / 持久化） | `manager.WorkspaceManager` |

    from lionbox.workspace import WorkspaceContext, WorkspaceManager

    WorkspaceContext.set(r"C:/work/demo")
    print(WorkspaceContext.resolve("a.txt"))        # C:/work/demo/a.txt
    print(WorkspaceContext.resolve("C:/Windows"))   # 抛 WorkspaceViolation
"""



__all__ = [
    "CFG_WORKSPACES", "ENV_STRICT", "Workspace", "WorkspaceContext", "WorkspaceManager",
    "WorkspacePermission", "WorkspaceViolation", "install_strict_mode_from_env",
    "normalize_permission", "strict_from_env", "workspace_id_of",
]
