# -*- coding: utf-8 -*-
r"""技能（由引擎内联生成）
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
    "lionbox.skills.definition",
    "lionbox.skills.frontmatter",
    "lionbox.skills.parser",
    "lionbox.skills.repository",
    "lionbox.skills.catalog_spi",
    "lionbox.skills.controller",
    "lionbox.skills.legacy",
    "lionbox.skills.load_tool",
    "lionbox.skills",
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

# 【每个被内联模块各自原本的 __file__】有代码用它推算"程序装在哪"（例如技能目录：
# `skills/repository.py` 往上三层才是安装根）。内联后 `__file__` 全是 main.py 的路径，
# 向上推会跑到仓库外面 —— 实测后果是内置技能一个都找不到。所以按模块各记一份。
# 路径不必真实存在：用到的是路径运算，只要目录层级一致，算出的安装根就一样。
_ORIG_FILE_skills_definition = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\definition.py"
_ORIG_FILE_skills_frontmatter = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\frontmatter.py"
_ORIG_FILE_skills_parser = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\parser.py"
_ORIG_FILE_skills_repository = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\repository.py"
_ORIG_FILE_skills_catalog_spi = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\catalog_spi.py"
_ORIG_FILE_skills_controller = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\controller.py"
_ORIG_FILE_skills_legacy = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\legacy.py"
_ORIG_FILE_skills_load_tool = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\load_tool.py"
_ORIG_FILE_skills = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\skills\__init__.py"


# ========================================================================
# 原模块 lionbox/skills/definition.py
# ========================================================================
"""一个技能的完整定义 —— 也就是一份 `SKILL.md` 解析出来的结果。

【契约来源】逐项对照 Java 版 `core/plugin/skill/SkillDefinition.java`：
字段名、`usable()`/`requiredToolIds()`/`matchesKeywords()`/`catalogLine()`/
`bodyPreview()`/`isLegacy()`/`oneLine()` 的语义与边界都照抄。

【为什么是"文件 + 记录"而不是继续用写死的类】技能原本是四个写死的 Java 类
（BackendSkill 之类），加一个技能就得改代码、重新编译、重新打包。改成通用格式
（YAML frontmatter + Markdown 正文）以后：内置技能放安装目录的 `skills/`，
用户技能放 `~/.lioncode/skills/`，加技能 = 新建一个目录。

【为什么 error 是一个字段而不是抛异常】一份写坏的 SKILL.md 绝不能让应用起不来 ——
用户只是笔误，不该整个软件打不开。解析失败也返回一个 SkillDefinition，
只是 `error` 有值、`usable()` 为 False，列表接口里照样看得到它、也知道错在哪。
"""


import re
from dataclasses import dataclass, field
from typing import Any, Iterable

#: 内置技能的 id 集合。AgentLoop 里那份老的 `buildSkillPrompt()` 会按关键词把这四个
#: 技能的正文整段塞进系统提示词，所以注入技能目录时要避开这四个 —— 否则同一段正文
#: 会出现两遍，白烧 token。用户自己加的技能没有 Java 壳，由 SkillCatalogSpi 补上。
LEGACY_IDS = ("backend", "client", "document", "frontend")

#: 工具名 → 老插件 id 的映射：让 `required_tool_ids()` 还能返回老格式的 id。
TOOL_PLUGIN_IDS: dict[str, str] = {
    "read_file": "tool.file.read",
    "write_file": "tool.file.write",
    "create_file": "tool.file.write",
    "append_file": "tool.file.write",
    "modify_file": "tool.file.modify",
    "search_in_files": "tool.file.search",
    "glob_files": "tool.file.search",
    "list_directory": "tool.file.search",
    "execute_command": "tool.shell.execute",
    "run_background": "tool.shell.execute",
    "git_status": "tool.git.status",
    "git_commit": "tool.git.commit",
}


@dataclass
class SkillDefinition:
    """与 Java 版 `SkillDefinition` record 同构。

    `error` 用 None/空串表示"这份技能可用"（Java 侧是 null，进 JSON 时整个字段省略）。
    """

    id: str
    display_name: str = ""
    description: str = ""
    when_to_use: str = ""
    keywords: list[str] = field(default_factory=list)
    tools: list[str] = field(default_factory=list)
    mode: str = "any"
    model: str = ""
    version: str = "1.0.0"
    tags: list[str] = field(default_factory=list)
    task_types: list[str] = field(default_factory=list)
    body: str = ""
    source_path: str = ""
    builtin: bool = False
    error: str | None = None

    # ---- 判定 ----
    def usable(self) -> bool:
        """这份技能能不能用（解析没出错、正文非空）。"""
        return not (self.error or "").strip() and bool((self.body or "").strip())

    def required_tool_ids(self) -> list[str]:
        """老接口 `SkillPlugin#getRequiredToolIds()` 要的插件 id 形式。"""
        out: list[str] = []
        for t in self.tools or []:
            if t is None or not str(t).strip():
                continue
            key = str(t).strip().lower()
            out.append(TOOL_PLUGIN_IDS.get(key, str(t).strip()))
        return out

    def matches_keywords(self, user_message: str | None) -> bool:
        """关键词是否命中这条用户消息（老 `isApplicable()` 的通用版）。

        匹配规则分两种，别一刀切：
          - 纯 ASCII 关键词（api、java、css）按**词边界**匹配：老实现是 contains，
            于是 `api` 会在 "rapid" 里命中、`java` 会在 "javascript" 里命中。
          - 含中文的关键词照旧用 contains：中文没有词边界这回事。
        """
        if not user_message or not str(user_message).strip():
            return False
        if not self.keywords:
            return False
        lower = str(user_message).lower()
        for kw in self.keywords:
            if kw is None or not str(kw).strip():
                continue
            k = str(kw).strip().lower()
            if _is_ascii(k):
                # 前面不能是字母/数字/下划线；后面不能紧跟字母（允许跟数字：qt5 也算 qt）
                if re.search(r"(?<![a-z0-9_])" + re.escape(k) + r"(?![a-z])", lower):
                    return True
            elif k in lower:
                return True
        return False

    # ---- 展示 ----
    def catalog_line(self) -> str:
        """给模型看的一行目录：`- id — 名字：说明（什么时候用）`。"""
        line = f"- {self.id} — {self.display_name}：{one_line(self.description, 120)}"
        if self.when_to_use and self.when_to_use.strip():
            line += f"（什么时候用：{one_line(self.when_to_use, 140)}）"
        return line

    def body_preview(self, max_chars: int) -> str:
        """界面/接口里用的正文预览（压成一行、截断）。"""
        return one_line(self.body, max_chars)

    def body_lines(self) -> int:
        """正文行数（接口字段 bodyLines 用，对齐 Java 的 `body().lines().count()`）。"""
        if not self.body:
            return 0
        return len(self.body.splitlines())

    def to_dict(self) -> dict[str, Any]:
        """完整字段快照（`/api/skills` 的 skills 数组元素就是它，字段名照抄 Java）。"""
        return {
            "id": self.id,
            "name": self.id,          # name 与 id 是同一个东西，两个字段都给
            "displayName": self.display_name,
            "description": self.description,
            "whenToUse": self.when_to_use,
            "keywords": list(self.keywords or []),
            "tools": list(self.tools or []),
            "mode": self.mode,
            "model": self.model,
            "version": self.version,
            "tags": list(self.tags or []),
            "taskTypes": list(self.task_types or []),
            "bodyPreview": self.body_preview(160),
            "bodyLines": self.body_lines(),
            "source": self.source_path,
            "builtin": self.builtin,
            "error": self.error,
        }


def is_legacy(skill_id: str | None) -> bool:
    """一份技能是不是内置四件套之一。"""
    return bool(skill_id) and str(skill_id).strip().lower() in LEGACY_IDS


def one_line(text: str | None, max_chars: int) -> str:
    """合并空白并截断，给"一行显示"的场合用。"""
    if text is None:
        return ""
    flat = re.sub(r"\s+", " ", str(text)).strip()
    return flat if len(flat) <= max_chars else flat[:max_chars] + "…"


def _is_ascii(text: str) -> bool:
    return all(ord(ch) <= 127 for ch in text)


def str_list(raw: Any) -> list[str]:
    """YAML 列表容错：写成 `[a, b]`、写成多行 `- a`、或干脆写一个逗号串都认。"""
    out: list[str] = []
    if raw is None:
        return out
    if isinstance(raw, (list, tuple)):
        for item in raw:
            s = "" if item is None else str(item).strip()
            if s:
                out.append(s)
        return out
    for part in re.split(r"[,，]", str(raw)):
        if part.strip():
            out.append(part.strip())
    return out


def iter_ids(definitions: Iterable[SkillDefinition]) -> list[str]:
    return [d.id for d in definitions]


# ========================================================================
# 原模块 lionbox/skills/frontmatter.py
# ========================================================================
"""极简 YAML frontmatter 解析器（**零第三方依赖**，不引 PyYAML）。

【为什么自己写】PORTING.md 的硬约束是"只用标准库"：引 PyYAML 会带进一个第三方包，
和"安装不能慢、首次启动不能慢"直接冲突。而 SKILL.md 的 frontmatter 实际只用到
很小的一个 YAML 子集，自己解析完全够：

    name: pdf                        # 简单键值（可带引号）
    display_name: "PDF 处理"
    description: 一句话说明能力
    keywords: [pdf, 合并, 拆分]        # 行内列表
    tools:                           # 块状列表
      - read_file
      - execute_command
    model: ""

支持的语法就是上面这些：`key: value`、行内 `[a, b]`、块状 `- item`、`#` 注释、
空行、单双引号。**不支持的**（嵌套 map、多行折叠 `|`/`>`、锚点）一律当语法错误抛
`FrontmatterError` —— 由 `SkillParser.parse()` 接住、变成"这份技能有问题"的提示，
和 Java 版 snakeyaml 抛异常后的处理路径一致。

【与 Java 的差异】Java 用 snakeyaml，能解析嵌套结构；这里只解析一层键值。
技能格式本身只用一层（`SkillParser` 读完就是 `map.get("name")` 这种取值），
所以这个差异对真实技能文件没有影响；真遇到嵌套写法会明确报错而不是静默错解。
"""


from typing import Any


class FrontmatterError(ValueError):
    """frontmatter 语法错误（消息直接进技能定义里的 error 字段给用户看）。"""


def parse_frontmatter(text: str) -> dict[str, Any]:
    """把 frontmatter 文本解析成 `{键: 字符串或字符串列表}`。

    空内容返回空 dict；语法不对抛 `FrontmatterError`。
    """
    if text is None:
        return {}
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    out: dict[str, Any] = {}
    i = 0
    while i < len(lines):
        raw = lines[i]
        i += 1
        line = raw.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if stripped.startswith("- "):
            raise FrontmatterError(f"第 {i} 行是列表项，但它上面没有对应的键: {stripped}")

        key, sep, value = stripped.partition(":")
        if not sep:
            raise FrontmatterError(f"第 {i} 行不是「键: 值」的写法: {stripped}")
        key = key.strip()
        if not key:
            raise FrontmatterError(f"第 {i} 行的键名是空的: {stripped}")
        if key in out:
            raise FrontmatterError(f"第 {i} 行的键重复了: {key}")
        value = value.strip()

        if value.startswith("#"):
            value = ""
        if value:
            out[key] = _parse_inline(value, i)
            continue

        # `key:` 后面紧跟 `- item` 块状列表；没有就跟空串（和 snakeyaml 的 null 等价处理）
        items: list[str] = []
        while i < len(lines):
            nxt = lines[i].strip()
            if not nxt or nxt.startswith("#"):
                i += 1
                continue
            if nxt.startswith("- "):
                items.append(_unquote(nxt[2:].strip()))
                i += 1
                continue
            if nxt == "-":
                items.append("")
                i += 1
                continue
            break
        out[key] = items if items else ""
    return out


def _parse_inline(value: str, line_no: int) -> Any:
    """解析行内值：`[a, b]` → 列表；其余 → 去掉引号的字符串。"""
    if value.startswith("["):
        if not value.endswith("]"):
            raise FrontmatterError(f"第 {line_no} 行的行内列表没有用 ] 收尾: {value}")
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_unquote(part.strip()) for part in _split_inline(inner)]
    return _unquote(value)


def _split_inline(inner: str) -> list[str]:
    """按逗号切分行内列表，但引号里的逗号不算分隔符。"""
    parts: list[str] = []
    buf: list[str] = []
    quote = ""
    for ch in inner:
        if quote:
            buf.append(ch)
            if ch == quote:
                quote = ""
            continue
        if ch in ("'", '"'):
            quote = ch
            buf.append(ch)
            continue
        if ch in (",", "，"):
            parts.append("".join(buf))
            buf = []
            continue
        buf.append(ch)
    parts.append("".join(buf))
    return [p for p in (p.strip() for p in parts) if p != ""]


def _unquote(value: str) -> str:
    """去掉一层单/双引号（YAML 里 `model: ""` 要解成空串）。"""
    v = value.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in ("'", '"'):
        return v[1:-1]
    return v


# ========================================================================
# 原模块 lionbox/skills/parser.py
# ========================================================================
"""SKILL.md 解析器：YAML frontmatter + Markdown 正文 → `SkillDefinition`。

【契约来源】逐项对照 Java 版 `core/plugin/skill/SkillParser.java`：切分规则、
必填字段、id 合法性、`decode()` 的三级解码退路、以及"解析失败也返回对象"的行为全部照抄。

格式（通用 skill 格式，和社区那套一致，别人写的技能拷进来就能用）：

    ---
    name: pdf
    display_name: PDF 处理
    description: 一句话说明能力
    when_to_use: 什么情况下该用
    keywords: [pdf, 合并]
    tools: [read_file, execute_command]
    mode: standard
    model: ""
    ---
    正文：给模型的具体指令

【为什么解析失败也要返回对象而不是抛异常】见 `SkillDefinition.error`：
用户手写 frontmatter 出错太正常了（少个冒号、中文冒号、列表没缩进），
一个坏文件不能让应用起不来，也不能让别的技能跟着消失。
"""


import re


#: 合法 id：字母数字和 . _ -（要和 `@skill:<id>` 的写法兼容，所以不放空格和中文）。
ID_PATTERN = re.compile(r"[A-Za-z0-9][A-Za-z0-9_.\-]*")

#: frontmatter 里那些"必须有"的字段：缺了模型就没法判断要不要用这个技能。
REQUIRED_FIELDS = ("name", "display_name", "description", "when_to_use")

#: 每个技能目录里约定的文件名（通用格式，改格式要同步改文档）。
SKILL_FILE = "SKILL.md"


def parse(dir_id: str, raw: str | None, source_path: str, builtin: bool) -> SkillDefinition:
    """解析一份 SKILL.md。

    :param dir_id:      目录名（frontmatter 里没写 name 时兜底当 id 用）
    :param raw:         文件内容
    :param source_path: 文件绝对路径（进 error 提示，用户知道去改哪个文件）
    :param builtin:     是否内置技能
    """
    text = "" if raw is None else str(raw).replace("\r\n", "\n").replace("\r", "\n")

    # ---- 1) 切 frontmatter 与正文 ----
    if not text.startswith("---"):
        return _broken(dir_id, source_path, builtin, text,
                       "缺少 YAML frontmatter：文件必须以一行 --- 开头")
    first_end = text.find("\n")
    close = text.find("\n---", first_end if first_end >= 0 else 0)
    if first_end < 0 or close < 0:
        return _broken(dir_id, source_path, builtin, text,
                       "frontmatter 没有结束：正文前面需要单独一行 ---")
    front = text[first_end + 1:close + 1]
    body_start = text.find("\n", close + 1)
    body = "" if body_start < 0 else text[body_start + 1:].strip()

    # ---- 2) YAML ----
    try:
        loaded = parse_frontmatter(front)
    except FrontmatterError as e:
        return _broken(dir_id, source_path, builtin, text, f"frontmatter YAML 语法错误：{e}")
    if not isinstance(loaded, dict):
        kind = "空" if loaded is None else type(loaded).__name__
        return _broken(dir_id, source_path, builtin, text,
                       f"frontmatter 不是键值对（YAML 解析出来是 {kind}）")
    mapping = {str(k).strip(): v for k, v in loaded.items()}

    # ---- 3) 必填字段 ----
    missing = [key for key in REQUIRED_FIELDS if not _str(mapping.get(key)).strip()]
    if missing:
        return _broken(dir_id, source_path, builtin, text,
                       "frontmatter 缺少必填字段：" + "、".join(missing))

    raw_id = _str(mapping.get("name"))
    if not ID_PATTERN.fullmatch(raw_id):
        return _broken(dir_id, source_path, builtin, text,
                       f"name 不合法（{raw_id}）：只能用字母、数字、. _ -，并且以字母或数字开头")

    mode = _str(mapping.get("mode"))
    defn = SkillDefinition(
        id=raw_id,
        display_name=_str(mapping.get("display_name")),
        description=_str(mapping.get("description")),
        when_to_use=_str(mapping.get("when_to_use")),
        keywords=str_list(mapping.get("keywords")),
        tools=str_list(mapping.get("tools")),
        mode="any" if not mode.strip() else mode.lower(),
        model=_str(mapping.get("model")),
        version=_str(mapping.get("version")) or "1.0.0",
        tags=str_list(mapping.get("tags")),
        task_types=str_list(mapping.get("task_types")),
        body=body,
        source_path=source_path,
        builtin=builtin,
        error=None,
    )

    # 正文为空 = 这个技能什么也教不了模型，当坏的报出来（比"加载成功但没用"强）
    if not defn.body.strip():
        return _broken(dir_id, source_path, builtin, text,
                       "正文是空的：技能得写给模型看的指令才有意义")
    return defn


def parse_file(path, builtin: bool) -> SkillDefinition:
    """读一个 SKILL.md 并解析（读盘失败也返回"坏技能"，不能把扫描带崩）。"""
    from pathlib import Path

    p = Path(path)
    dir_id = p.parent.name
    try:
        raw = decode(p.read_bytes())
    except OSError:
        return parse(dir_id, "", str(p.absolute()), builtin)
    return parse(dir_id, raw, str(p.absolute()), builtin)


def decode(data: bytes | None) -> str:
    """读 SKILL.md 的字节。

    【为什么要自己解码】用户技能是用户拿记事本写的，Windows 记事本默认 ANSI(GBK) ——
    直接按 UTF-8 严格解码会抛异常，表现就是"我明明写了技能，列表里却是坏的"。
    这里按 UTF-8 → GBK → 替换字符三级退，和工具层 read_file 的处理保持一致。
    """
    if not data:
        return ""
    offset = 3 if (len(data) >= 3 and data[0] == 0xEF and data[1] == 0xBB and data[2] == 0xBF) else 0
    payload = data[offset:]
    # 三级退：严格 UTF-8 → GBK（容错替换）→ UTF-8（容错替换）
    for encoding, errors in (("utf-8", "strict"), ("gbk", "replace"), ("utf-8", "replace")):
        try:
            return payload.decode(encoding, errors=errors)
        except (UnicodeDecodeError, LookupError):
            continue
    return payload.decode("utf-8", errors="replace")   # 兜底：绝不会走到（替换模式不会抛）


def _broken(dir_id: str, source_path: str, builtin: bool, raw: str,
            error: str) -> SkillDefinition:
    """解析失败的技能：照样返回对象，只是 error 有值、usable()=False。"""
    sid = (dir_id or "").strip() or "unknown"
    return SkillDefinition(
        id=sid, display_name=sid, description="", when_to_use="",
        keywords=[], tools=[], mode="any", model="", version="0.0.0",
        tags=[], task_types=[], body=(raw or "").strip(),
        source_path=source_path, builtin=builtin, error=error,
    )


def _str(value) -> str:
    return "" if value is None else str(value).strip()


# ========================================================================
# 原模块 lionbox/skills/repository.py
# ========================================================================
"""技能仓库：扫描技能目录、缓存解析结果、管理启用开关与会话指定技能。

【契约来源】逐项对照 Java 版 `core/plugin/skill/SkillRepository.java`。

两个来源，用户优先级更高（同 id 时用户那份覆盖内置的那份）：
  1. **内置**：安装目录下的 `skills/`（随安装包发布）—— `skills/<id>/SKILL.md`
  2. **用户**：`~/.lioncode/skills/`，和 `app-config.json` 同一个目录

【为什么缓存 + 手动 reload】技能是在系统提示词里出现的，每条消息都要用；
每轮去读盘既慢又可能读到写了一半的文件。所以启动时扫一次、缓存住，
用户改完文件调 `POST /api/skills/reload` 刷一次。

目录定位的多候选（为什么给一堆候选）：这个程序有好几种启动方式（安装目录启动、
项目根目录启动、开发时在 python/ 下跑），工作目录各不相同，"skills 在隔壁"
这件事必须多找几个地方 —— 和 Java 版 `LocalModelRuntime.appDirs()` 同一个理由。
"""


import os
import sys
import threading
from pathlib import Path


#: 关闭开关存在 app-config.json 的这个键下（和 activeAdapter 那些配置同一个文件）。
CFG_DISABLED = "skills.disabled"

#: 技能目录在提示词里的最大行数：目录只用来"让模型知道有哪些技能"，塞不下就截断。
CATALOG_MAX = 20

#: 显式指定内置技能目录的环境变量（等价 Java 的 `-Dlion.skills.dir=`）。
ENV_SKILLS_DIR = "LIONBOX_SKILLS_DIR"
ENV_SKILLS_DIR_ALT = "LION_SKILLS_DIR"

#: 启动脚本会设 `lionbox.home`（等价 Java 的 `-Dlionbox.home=`）。
ENV_LIONBOX_HOME = "LIONBOX_HOME"


class ReloadResult:
    """扫描结果。`broken` 是本次读取/解析失败的次数（含目录读不出来的）。"""

    __slots__ = ("count", "errors", "broken")

    def __init__(self, count: int, errors: int, broken: int) -> None:
        self.count = count
        self.errors = errors
        self.broken = broken

    def __repr__(self) -> str:
        return f"ReloadResult(count={self.count}, errors={self.errors}, broken={self.broken})"


class SkillRepository:
    """技能仓库（进程内单例，和 Java 版的 Spring 单例等价）。"""

    def __init__(self, config_store: AppConfigStore | None = None,
                 builtin_dir: str | Path | None = None,
                 user_dir: str | Path | None = None) -> None:
        from lionbox.config.store import AppConfigStore
        self.config_store = config_store if config_store is not None else AppConfigStore()
        self._configured_builtin_dir = str(builtin_dir) if builtin_dir else _configured_dir_from_env()
        self._user_dir_override = Path(user_dir) if user_dir else None
        self._lock = threading.RLock()
        #: id -> 定义（dict 保序，提示词与列表接口的顺序才稳定）
        self._skills: dict[str, SkillDefinition] = {}
        self.builtin_dir: Path | None = None
        self.user_skills_dir: Path | None = None
        #: 会话级"指定技能"（POST /api/skills/active 钉住的），内存存
        self._active_by_session: dict[str, list[str]] = {}

    # ------------------------------------------------------------------
    # 扫描 / 重载
    # ------------------------------------------------------------------
    def reload(self) -> ReloadResult:
        """重新扫描技能目录。先内置后用户：同 id 时用户那份后写进去，自然覆盖。"""
        with self._lock:
            builtin = self.resolve_builtin_dir()
            user = self._user_dir_override or (Path(os.path.expanduser("~")) / ".lioncode" / "skills")
            self.builtin_dir = builtin
            self.user_skills_dir = user

            # 用户技能目录顺手建出来：不然用户看到接口里返回的路径，
            # 却发现自己机器上没这个目录，还得自己猜层级
            try:
                user.mkdir(parents=True, exist_ok=True)
            except OSError:
                pass   # 建不出来不影响本次扫描

            found: dict[str, SkillDefinition] = {}
            broken = self._scan_dir(builtin, True, found)
            broken += self._scan_dir(user, False, found)

            error_count = sum(1 for d in found.values() if not d.usable())
            self._skills = dict(found)   # 保序副本
            return ReloadResult(len(found), error_count, broken)

    def _scan_dir(self, directory: Path | None, builtin: bool, into: dict[str, SkillDefinition]) -> int:
        """扫一个目录：只认 `<id>/SKILL.md` 这种两层结构。"""
        if directory is None or not directory.is_dir():
            return 0
        broken = 0
        try:
            sub_dirs = sorted((p for p in directory.iterdir()
                               if p.is_dir() and (p / SKILL_FILE).is_file()),
                              key=lambda p: p.name)
        except OSError:
            return 0
        for sub in sub_dirs:
            file = sub / SKILL_FILE
            try:
                defn = parse_file(file, builtin)
            except Exception as e:                     # 读盘失败也要算"坏技能"
                broken += 1
                defn = parse(sub.name, "", str(file.absolute()), builtin)
                defn.error = f"读取技能文件失败: {e}"
                into[defn.id] = defn
                continue
            if not defn.usable():
                broken += 1
            into[defn.id] = defn
        return broken

    def resolve_builtin_dir(self) -> Path:
        """找内置技能目录：返回第一个"真的存在"的候选。"""
        candidates: list[Path] = []
        if self._configured_builtin_dir and self._configured_builtin_dir.strip():
            candidates.append(Path(self._configured_builtin_dir.strip()))

        home = os.environ.get(ENV_LIONBOX_HOME, "")
        if home.strip():
            candidates.append(Path(home.strip()) / "skills")

        # Python 版的"程序装在哪"：包文件往上三层是仓库根/安装根，还有解释器所在目录。
        # （Java 用 Spring Boot 的 ApplicationHome 认出 fat jar；这里用包路径 + 解释器目录，
        #   理由相同：工作目录各不相同，"skills 在隔壁"要多找几个地方。）
        for base in self._app_home_candidates():
            _add_dir_candidates(candidates, base)

        cwd = os.getcwd()
        if cwd:
            candidates.append(Path(cwd) / "skills")
            candidates.append(Path(cwd) / "dist" / "skills")

        for c in candidates:
            if c.is_dir():
                return c.absolute()
        return (candidates[0] if candidates else Path("skills")).absolute()

    @staticmethod
    def _app_home_candidates() -> list[Path]:
        out: list[Path] = []
        here = _safe_resolve(Path(_ORIG_FILE_skills_repository))
        if here is not None:
            # repository.py -> skills -> lionbox -> python -> <项目/安装根>
            for index in (3, 2):
                if len(here.parents) > index:
                    out.append(here.parents[index])
        executable = _safe_resolve(Path(sys.executable))
        if executable is not None:
            out.append(executable.parent)
        return out

    # ------------------------------------------------------------------
    # 查询
    # ------------------------------------------------------------------
    def list(self) -> list[SkillDefinition]:
        """全部技能（含坏掉的、含被禁用的），顺序稳定。"""
        with self._lock:
            return list(self._skills.values())

    def enabled(self) -> list[SkillDefinition]:
        """只有可用的（解析没错）+ 用户没关掉的技能 —— 提示词和 skill_load 只认这些。"""
        disabled = self.disabled_ids()
        with self._lock:
            return [d for d in self._skills.values() if d.usable() and d.id not in disabled]

    def find(self, id_or_token: str | None) -> SkillDefinition | None:
        """按 id（或 `skill.<id>` 这种老插件 id 写法）找技能。两种写法都认。"""
        if not id_or_token or not str(id_or_token).strip():
            return None
        key = str(id_or_token).strip()
        with self._lock:
            direct = self._skills.get(key)
            if direct is not None:
                return direct
            lower = key.lower()
            if lower.startswith("skill."):
                stripped = self._skills.get(key[len("skill."):])
                if stripped is not None:
                    return stripped
                lower = lower[len("skill."):]
            for d in self._skills.values():
                if d.id.lower() == lower:
                    return d
        return None

    def find_enabled(self, id_or_token: str | None) -> SkillDefinition | None:
        """找"能用的"技能（不存在 / 坏了 / 被禁用 都返回 None，调用方据此给出原因）。"""
        defn = self.find(id_or_token)
        if defn is None or not defn.usable() or not self.is_enabled(defn.id):
            return None
        return defn

    def unusable_reason(self, id_or_token: str | None) -> str | None:
        """这个技能为什么不能用（给模型/用户一句能照着改的话）；能用时返回 None。"""
        defn = self.find(id_or_token)
        if defn is None:
            ids = [d.id for d in self.enabled()]
            listed = "、".join(ids) if ids else "一个都没有"
            return f"没有这个技能: {id_or_token}（可用技能: {listed}）"
        if not defn.usable():
            return f"技能 {defn.id} 有问题，用不了：{defn.error}"
        if not self.is_enabled(defn.id):
            return f"技能 {defn.id} 已被禁用（POST /api/skills/{defn.id}/enable 可以打开）"
        return None

    # ------------------------------------------------------------------
    # 启用 / 禁用（持久化到 app-config.json）
    # ------------------------------------------------------------------
    def is_enabled(self, skill_id: str) -> bool:
        return skill_id not in self.disabled_ids()

    def set_enabled(self, skill_id: str, enabled: bool) -> bool:
        """打开/关闭一个技能；返回 False 表示没有这个技能。"""
        defn = self.find(skill_id)
        if defn is None:
            return False
        disabled = [d for d in self.disabled_ids() if d != defn.id]
        if not enabled:
            disabled.append(defn.id)
        self.config_store.set(CFG_DISABLED, disabled)
        return True

    def disabled_ids(self) -> set[str]:
        """已经被关掉的技能 id 集合（配置里可能残留已删除的技能，读的时候顺手过滤）。"""
        raw = self.config_store.get(CFG_DISABLED, [])
        out: set[str] = set()
        if isinstance(raw, (list, tuple)):
            for item in raw:
                if item is not None and str(item).strip():
                    out.add(str(item).strip())
        return out

    # ------------------------------------------------------------------
    # 会话指定技能
    # ------------------------------------------------------------------
    def active_skills(self, session_id: str | None) -> list[str]:
        """这个会话被钉住的技能 id（过滤掉已经不存在的）。"""
        if session_id is None:
            return []
        with self._lock:
            ids = list(self._active_by_session.get(session_id, []))
            return [i for i in ids if i in self._skills]

    def set_active(self, session_id: str | None, ids: list[str] | None) -> list[str]:
        """给会话钉住技能（空列表=取消钉住）。返回不认识的 id 列表。"""
        unknown: list[str] = []
        resolved: list[str] = []
        for raw in ids or []:
            defn = self.find_enabled(raw)
            if defn is not None:
                if defn.id not in resolved:
                    resolved.append(defn.id)
            elif raw is not None and str(raw).strip():
                unknown.append(str(raw).strip())
        if session_id is not None:
            with self._lock:
                if resolved:
                    self._active_by_session[session_id] = resolved
                else:
                    self._active_by_session.pop(session_id, None)
        return unknown

    def active_definitions(self, session_id: str | None) -> list[SkillDefinition]:
        """钉住的技能定义（可用的），给提示词注入用。"""
        out: list[SkillDefinition] = []
        for skill_id in self.active_skills(session_id):
            defn = self.find_enabled(skill_id)
            if defn is not None:
                out.append(defn)
        return out

    def clear_session(self, session_id: str | None) -> None:
        """会话被销毁时清一下（避免长时间运行攒一堆死会话的钉住关系）。"""
        if session_id is None:
            return
        with self._lock:
            self._active_by_session.pop(session_id, None)

    # ------------------------------------------------------------------
    # 提示词
    # ------------------------------------------------------------------
    def catalog_text(self) -> str:
        """技能目录（系统提示词里那段"有哪些技能可用"）。

        【为什么只给一行、不给正文】提示词每轮都要发一遍，本地模型 11 token/s，
        把技能正文全塞进去等于每条消息先花一分钟"读说明书"。所以目录只列
        id + 名字 + 一句话 + 什么时候用，模型决定要用哪个时再调 `skill_load` 取正文。
        """
        items = self.enabled()
        if not items:
            return ""
        sb = ["## 技能（按需加载）\n",
              "下面每个技能是一套现成的做法。**某个技能匹配当前任务时，",
              "先调 skill_load（参数 name = 技能 id）拿到完整指令，再动手**；不符合就别加载。\n"]
        shown = 0
        for d in items:
            if shown >= CATALOG_MAX:
                break
            sb.append(d.catalog_line() + "\n")
            shown += 1
        if len(items) > shown:
            sb.append(f"（还有 {len(items) - shown} 个技能没列出来，可以调 skill_load 试名字）\n")
        return "".join(sb)

    def builtin_dir_string(self) -> str:
        """目录接口要返回的路径字符串（不存在也给路径，用户好照着建）。"""
        return "" if self.builtin_dir is None else str(self.builtin_dir)

    def user_dir_string(self) -> str:
        return "" if self.user_skills_dir is None else str(self.user_skills_dir)

    # ------------------------------------------------------------------
    # 接口用的快照
    # ------------------------------------------------------------------
    def skills_json(self) -> list[dict]:
        """技能列表的 JSON 形态（字段名和 Java 版 `SkillController.skillJsons()` 一致）。"""
        out: list[dict] = []
        disabled = self.disabled_ids()
        for d in self.list():
            item = d.to_dict()
            item["enabled"] = d.usable() and d.id not in disabled
            # null 字段整个省略（对齐 Java 的 NON_NULL）
            if not item.get("error"):
                item.pop("error", None)
            out.append(item)
        return out

    def summary(self) -> list[dict]:
        """给我/用户看的一行摘要（验收用：名字/描述/触发方式）。"""
        out: list[dict] = []
        for d in self.list():
            out.append({
                "id": d.id,
                "displayName": d.display_name,
                "description": one_line(d.description, 80),
                "whenToUse": one_line(d.when_to_use, 80),
                "keywords": list(d.keywords),
                "mode": d.mode,
                "model": d.model,
                "version": d.version,
                "builtin": d.builtin,
                "enabled": d.usable() and self.is_enabled(d.id),
                "trigger": "关键词命中 / 用户 @skill:{} / POST /api/skills/active 钉住".format(d.id),
                "error": d.error,
                "source": d.source_path,
            })
        return out


def _configured_dir_from_env() -> str:
    for name in (ENV_SKILLS_DIR, ENV_SKILLS_DIR_ALT):
        value = os.environ.get(name, "")
        if value.strip():
            return value.strip()
    return ""


def _safe_resolve(path: Path) -> Path | None:
    """`Path.resolve()` 的容错包装（路径拿不到就返回 None，由调用方跳过这个候选）。"""
    try:
        return path.resolve()
    except (OSError, RuntimeError):
        return None


def _add_dir_candidates(candidates: list[Path], base: Path) -> None:
    """从一个基准目录推出 skills/ 的候选：自己、dist 下、上一级。"""
    candidates.append(base / "skills")
    candidates.append(base / "dist" / "skills")
    if base.parent != base:
        candidates.append(base.parent / "skills")


# --------------------------------------------------------------------------
# 进程内单例
# --------------------------------------------------------------------------
_DEFAULT: SkillRepository | None = None
_DEFAULT_LOCK = threading.Lock()


def default_repository() -> SkillRepository:
    """取进程内默认仓库（第一次调用时扫描技能目录）。"""
    global _DEFAULT
    with _DEFAULT_LOCK:
        if _DEFAULT is None:
            repo = SkillRepository()
            repo.reload()
            _DEFAULT = repo
        return _DEFAULT


def set_default_repository(repo: SkillRepository | None) -> None:
    """替换默认仓库（测试/嵌入式用）。"""
    global _DEFAULT
    with _DEFAULT_LOCK:
        _DEFAULT = repo


# ========================================================================
# 原模块 lionbox/skills/catalog_spi.py
# ========================================================================
"""技能注入扩展点：把"技能目录"和"被指定/命中的技能正文"塞进系统提示词。

【契约来源】逐项对照 Java 版 `core/plugin/skill/SkillCatalogSpi.java`。

【为什么走 SPI 而不是改 AgentLoop】AgentLoop 是所有功能共用的主循环，谁都能改它
就会天天冲突。`plugins/lifecycle.py` 已经留好了 `AgentSpi.extra_system_sections`
这个口子，技能只关心"往提示词里加几段话"，实现这一个方法就够了。

注入三块，顺序按重要性排（模型只看前几屏，重要的必须在前）：
  1. **本轮指定的技能**：用户用 `/api/skills/active` 钉住、或消息里写了 `@skill:<id>` 的。
  2. **关键词命中的技能**：只补 AgentLoop 老路径覆盖不到的那些（用户自己加的技能）。
     四个内置技能由 AgentLoop 里的老 `buildSkillPrompt()` 注入，这里再来一遍
     就是同一段话出现两遍，白烧 token。
  3. **技能目录**：一行一个，告诉模型"还有哪些技能、什么时候用、要用就先 skill_load"。
"""


from lionbox.plugins.lifecycle import AgentSpi

#: 单份技能正文注入上限：用户技能写失控（塞进去一本书）时不能让每条消息都爆掉。
MAX_BODY_CHARS = 8000


class SkillCatalogSpi(AgentSpi):
    """技能目录注入（实现 `AgentSpi.extra_system_sections` 与 `order`）。

    继承 `AgentSpi` 是为了拿到其余扩展点的**默认实现**（工具清单过滤、用户消息改写、
    大循环参数都不参与 → 原样返回）；只实现自己关心的那一个方法，和 Java 侧一样。
    """

    def __init__(self, repository: SkillRepository | None = None,
                 settings=None, registry=None, session_manager=None) -> None:
        self._repository = repository
        self.settings = settings
        self.registry = registry
        self.session_manager = session_manager

    @property
    def repository(self) -> SkillRepository:
        if self._repository is None:
            self._repository = default_repository()
        return self._repository

    # ---- SPI 元信息 ----
    def spi_name(self) -> str:
        return "技能目录注入"

    def order(self) -> int:
        """排在后面（默认 100）：技能是"可选能力"，不能挤掉前面的硬性格式约定。"""
        return 200

    # ---- 注册 / 注销 ----
    def register(self) -> None:
        """挂到 Agent 主循环（等价 Java 的 `@PostConstruct register()`）。"""
        from lionbox.plugins.lifecycle import register_spi
        register_spi(self)
        print(f"[技能] 技能目录注入已挂到 Agent 主循环（AgentSpi，order={self.order()}）", flush=True)

    def unregister(self) -> None:
        from lionbox.plugins.lifecycle import unregister_spi
        unregister_spi(self)

    # ---- 主体 ----
    def extra_system_sections(self, session_id: str | None = None,
                              workspace_path: str | None = None,
                              user_message: str | None = None) -> list[str]:
        sections: list[str] = []

        # 用户在设置里把"技能"这类插件关掉之后，提示词里就不该再出现技能目录/正文 ——
        # 否则开关只影响了界面上那个列表，模型照旧按技能办事，"关掉"是假的。
        if not self.skill_system_enabled():
            return sections

        already_given: set[str] = set()

        # 【极简模式只给目录，不给正文】AgentLoop 在 MINIMAL 下已经挡掉了技能正文
        # （正文里常写"用 web_search 查""用 git_commit 提交"，而极简模式没有这些工具，
        # 注进去等于教模型去调不存在的工具）。这条 SPI 路径也必须守同一道护栏。
        minimal = self.is_minimal_mode(session_id)

        # ---- 1) 钉住的技能：正文全给，模型不用再去 load ----
        pinned = [] if minimal else self.repository.active_definitions(session_id)
        if pinned:
            sb = ["## 本轮指定技能（用户指定，必须遵守）\n"]
            for d in pinned:
                sb.append(f"### {d.id} — {d.display_name}\n")
                sb.append(cap(d.body) + "\n\n")
                already_given.add(d.id)
            sections.append("".join(sb))

        # ---- 2) 关键词命中的技能（只补老路径漏掉的）----
        matched: list[SkillDefinition] = []
        for d in ([] if minimal else self.repository.enabled()):
            if d.id in already_given:
                continue
            # 内置四件套由 AgentLoop 的老实现按同样的关键词规则注入，这里跳过。
            # 【注意】哪天 AgentLoop 里那份老实现删掉了，把下面这行去掉即可由本类接管。
            if is_legacy(d.id):
                continue
            if d.matches_keywords(user_message):
                matched.append(d)
        if matched:
            sb = ["## 关键词命中的技能\n"]
            for d in matched:
                sb.append(f"### {d.id} — {d.display_name}\n")
                sb.append(cap(d.body) + "\n\n")
            sections.append("".join(sb))

        # ---- 3) 技能目录 ----
        catalog = self.repository.catalog_text()
        if catalog.strip():
            sections.append(catalog)
        return sections

    # ---- 开关与模式 ----
    def is_minimal_mode(self, session_id: str | None) -> bool:
        """本会话是不是"极简模式"；取不到就按 False（宁可多注入，也不误关整个技能功能）。"""
        try:
            sm = self._session_manager()
            if sm is None or session_id is None:
                return False
            mode = sm.get_effective_mode(session_id)
            from lionbox.plugins.base import AgentMode
            return AgentMode.from_name(mode) == AgentMode.MINIMAL
        except Exception as e:
            print(f"[技能] 查会话模式失败，按标准模式处理: {e}", flush=True)
            return False

    def skill_system_enabled(self) -> bool:
        """技能系统本身是不是被用户关掉了。

        判定：只要有**任何一个** kind=SKILL 的插件还开着，就算开着。
        还没起来 / 查不到 → 按开着处理，别把功能误关。
        """
        try:
            settings = self._settings()
            registry = self._registry()
            if settings is None or registry is None:
                return True
            from lionbox.plugins.base import PluginKind
            for p in registry.get_by_kind(PluginKind.SKILL):
                if settings.is_enabled(p):
                    return True
            return False
        except Exception as e:
            print(f"[技能] 查技能插件开关失败，按开着处理: {e}", flush=True)
            return True

    # ---- 依赖懒取（避免和其它模块形成构造期循环依赖）----
    def _settings(self):
        if self.settings is None:
            from lionbox.plugins.lifecycle import default_settings
            self.settings = default_settings()
        return self.settings

    def _registry(self):
        if self.registry is None:
            from lionbox.plugins.lifecycle import default_registry
            self.registry = default_registry()
        return self.registry

    def _session_manager(self):
        """【窄桩】`sessions/manager.py` 已就绪时取它的进程内单例；取不到就按标准模式。"""
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


def cap(body: str | None) -> str:
    """正文超长时截断并说明 —— 比整段丢掉好（模型至少知道有这个技能、可以 read_file 读全文）。"""
    if not body:
        return ""
    if len(body) <= MAX_BODY_CHARS:
        return body.strip()
    return (body[:MAX_BODY_CHARS]
            + f"\n\n（技能正文过长已截断，共 {len(body)} 字；完整内容请用 read_file 打开技能文件）")


#: 进程内单例（app 启动时挂一次）
_DEFAULT__skills_catalog_spi: SkillCatalogSpi | None = None


def default_catalog_spi() -> SkillCatalogSpi:
    global _DEFAULT__skills_catalog_spi
    if _DEFAULT__skills_catalog_spi is None:
        _DEFAULT__skills_catalog_spi = SkillCatalogSpi()
    return _DEFAULT__skills_catalog_spi


# ========================================================================
# 原模块 lionbox/skills/controller.py
# ========================================================================
"""技能管理接口的响应构造（`/api/skills`）。

【契约来源】逐项对照 Java 版 `core/plugin/skill/SkillController.java` 的
`list` / `reload` / `enable` / `disable` / `getActive` / `setActive` 六个动作与
它们的字段名；**只搬响应构造，不注册路由** —— 路由归 `api/*` 层（那是接口层的活，
本模块属于 `core/plugin/skill`，和 Java 一样只负责"把数据摆成前端要的形状"）。

【与 Java 的一处差异】Java 用 `ApiEnvelope`（顶层同时给 ok/success，数据既在顶层也在
`data` 里）；Python 侧的契约是 `PORTING.md` 定的 `ApiResponse`（`success/message/data`），
所以这里统一返回 `ApiResponse`。字段集合（skillsDir / userSkillsDir / skills …）不变。
"""


from typing import Any



class SkillController:
    """技能管理接口的处理器（无状态，可直接被 HTTP 路由层调用）。"""

    def __init__(self, repository: SkillRepository | None = None, session_manager=None) -> None:
        self._repository = repository
        self.session_manager = session_manager

    @property
    def repository(self) -> SkillRepository:
        if self._repository is None:
            self._repository = default_repository()
        return self._repository

    # ------------------------------------------------------------------
    # GET /api/skills
    # ------------------------------------------------------------------
    def list(self) -> ApiResponse:
        """技能列表（含坏掉的、被禁用的，坏的原因在 error 字段里）。"""
        from lionbox.api.response import ApiResponse
        return ApiResponse.ok({
            "skillsDir": self.repository.builtin_dir_string(),
            "userSkillsDir": self.repository.user_dir_string(),
            "skills": self.repository.skills_json(),
        })

    # ------------------------------------------------------------------
    # POST /api/skills/reload
    # ------------------------------------------------------------------
    def reload(self) -> ApiResponse:
        """重新扫描技能目录（用户新增/修改 SKILL.md 后不用重启）。"""
        from lionbox.api.response import ApiResponse
        result = self.repository.reload()
        message = f"已重新扫描技能目录，共 {result.count} 个技能"
        if result.errors > 0:
            message += f"（{result.errors} 个有问题）"
        return ApiResponse.ok({
            "count": result.count,
            "errorCount": result.errors,
            "skillsDir": self.repository.builtin_dir_string(),
            "userSkillsDir": self.repository.user_dir_string(),
            "skills": self.repository.skills_json(),
        }, message)

    # ------------------------------------------------------------------
    # POST /api/skills/{id}/enable | /disable
    # ------------------------------------------------------------------
    def enable(self, skill_id: str) -> ApiResponse:
        from lionbox.api.response import ApiResponse
        return self._set_enabled(skill_id, True)

    def disable(self, skill_id: str) -> ApiResponse:
        from lionbox.api.response import ApiResponse
        return self._set_enabled(skill_id, False)

    def _set_enabled(self, skill_id: str, enabled: bool) -> ApiResponse:
        from lionbox.api.response import ApiResponse
        if not self.repository.set_enabled(skill_id, enabled):
            return ApiResponse.error(f"技能不存在: {skill_id}")
        # 用仓库里真实的 id 回（用户可能写的是 skill.backend 这种老写法）
        defn = self.repository.find(skill_id)
        real_id = defn.id if defn is not None else skill_id
        verb = "启用" if enabled else "禁用"
        return ApiResponse.ok({"id": real_id, "enabled": enabled},
                              f"技能已{verb}: {real_id}")

    # ------------------------------------------------------------------
    # GET /api/skills/active?sessionId=
    # ------------------------------------------------------------------
    def get_active(self, session_id: str | None) -> ApiResponse:
        """当前会话钉住的技能。"""
        from lionbox.api.response import ApiResponse
        if not session_id or not str(session_id).strip():
            return ApiResponse.error("缺少 sessionId")
        return ApiResponse.ok({
            "sessionId": session_id,
            "skills": self.repository.active_skills(session_id),
        })

    # ------------------------------------------------------------------
    # POST /api/skills/active
    # ------------------------------------------------------------------
    def set_active(self, session_id: str | None, skills: list[str] | None) -> ApiResponse:
        """给会话钉住技能：之后每一轮都会把它们的正文注入上下文，不用模型自己去调 skill_load。"""
        from lionbox.api.response import ApiResponse
        if not session_id or not str(session_id).strip():
            return ApiResponse.error("缺少 sessionId")
        if self.session_manager is not None and self.session_manager.get_session(session_id) is None:
            return ApiResponse.error(f"会话不存在: {session_id}")
        unknown = self.repository.set_active(session_id, skills)
        data: dict[str, Any] = {
            "sessionId": session_id,
            "skills": self.repository.active_skills(session_id),
        }
        if unknown:
            data["unknown"] = unknown
        message = ("已更新本会话的技能" if not unknown
                   else "已更新本会话的技能；这些技能没找到或不可用，已忽略: " + "、".join(unknown))
        return ApiResponse.ok(data, message)


# ========================================================================
# 原模块 lionbox/skills/legacy.py
# ========================================================================
"""老接口兼容壳：`SkillPlugin` / `FileBackedSkill` 与四个内置技能类。

【契约来源】逐项对照 Java 版 `core/plugin/skill/SkillPlugin.java`、
`FileBackedSkill.java`、`BackendSkill.java`、`ClientSkill.java`、`DocumentSkill.java`、
`FrontendSkill.java`。

【为什么留着 SkillPlugin 这套老接口】AgentLoop、PluginRegistry 都还按 SkillPlugin
找技能（`pluginRegistry.getSkillPlugins()`），直接删掉会把别人的代码打断。所以四个
技能类保留成"壳"：内容全部搬进 `skills/<id>/SKILL.md`，这里只负责把文件里的东西读出来、
用老接口的样子交出去 —— 插件 id 也保持 `skill.backend` 这种老写法。

【文件坏了会怎样】技能文件缺失或解析失败时，这个壳退化成"名字还在、正文为空、
isApplicable 永远 False"，也就是这个技能静默失效 —— 而不是让应用起不来。
坏在哪，`GET /api/skills` 的 error 字段里写着。
"""


from lionbox.plugins.lifecycle import Plugin, PluginType
from lionbox.plugins.base import PluginKind


class SkillPlugin(Plugin):
    """技能插件接口（Java `SkillPlugin`）：提供特定领域的能力。"""

    @property
    def type(self) -> str:
        return PluginType.SKILL

    def system_prompt_fragment(self) -> str:
        """技能提供的系统提示词片段（增强 Agent 在该领域的能力）。"""
        raise NotImplementedError

    def required_tool_ids(self) -> list[str]:
        """该技能依赖的工具插件 ID 列表。"""
        raise NotImplementedError

    def task_type_descriptions(self) -> list[str]:
        """该技能适用的任务类型描述。"""
        raise NotImplementedError

    def is_applicable(self, user_message: str | None) -> bool:
        """判断该技能是否适用于给定的用户消息（默认适用于所有消息）。"""
        return True


class FileBackedSkill(SkillPlugin):
    """兼容壳基类：把"读 SKILL.md 的技能仓库"包装成老的 `SkillPlugin` 接口。"""

    def __init__(self, repository: SkillRepository | None = None) -> None:
        self._repository = repository

    @property
    def repository(self) -> SkillRepository:
        if self._repository is None:
            self._repository = default_repository()
        return self._repository

    # ---- 子类覆盖 ----
    @property
    def skill_id(self) -> str:
        raise NotImplementedError

    @property
    def fallback_name(self) -> str:
        raise NotImplementedError

    @property
    def fallback_description(self) -> str:
        raise NotImplementedError

    # ---- 老接口实现 ----
    @property
    def id(self) -> str:                      # noqa: A003
        # 插件 id 保持 "skill.xxx" 的老写法：日志、/api/plugins、老用户的印象里都是这个
        return "skill." + self.skill_id

    @property
    def definition(self) -> SkillDefinition | None:
        """当前这份技能定义（可能不存在）。"""
        return self.repository.find(self.skill_id)

    @property
    def name(self) -> str:
        d = self.definition
        return d.display_name if (d is not None and d.display_name.strip()) else self.fallback_name

    @property
    def description(self) -> str:
        d = self.definition
        return d.description if (d is not None and d.description.strip()) else self.fallback_description

    @property
    def version(self) -> str:
        d = self.definition
        return d.version if (d is not None and d.version.strip()) else "1.0.0"

    @property
    def tags(self) -> list[str]:
        d = self.definition
        return list(d.tags) if d is not None else []

    @property
    def kind(self) -> str:
        return PluginKind.SKILL

    def system_prompt_fragment(self) -> str:
        d = self.definition
        return d.body if (d is not None and d.usable()) else ""

    def required_tool_ids(self) -> list[str]:
        d = self.definition
        return d.required_tool_ids() if d is not None else []

    def task_type_descriptions(self) -> list[str]:
        d = self.definition
        return list(d.task_types) if d is not None else []

    def is_applicable(self, user_message: str | None) -> bool:
        # 坏掉的、被用户禁用的技能一律不匹配 —— 否则"禁用"这个开关等于没用
        # （AgentLoop 会照样把正文注进提示词）
        d = self.definition
        if d is None or not d.usable() or not self.repository.is_enabled(d.id):
            return False
        return d.matches_keywords(user_message)


class BackendSkill(FileBackedSkill):
    """后端开发技能包（兼容壳）。"""

    @property
    def skill_id(self) -> str:
        return "backend"

    @property
    def fallback_name(self) -> str:
        return "后端开发技能"

    @property
    def fallback_description(self) -> str:
        return "后端代码编写、调试、编译排错、接口设计、依赖处理等后端相关能力"


class ClientSkill(FileBackedSkill):
    """客户端开发技能包（兼容壳）。"""

    @property
    def skill_id(self) -> str:
        return "client"

    @property
    def fallback_name(self) -> str:
        return "客户端开发技能"

    @property
    def fallback_description(self) -> str:
        return "桌面客户端程序开发相关能力，支持Electron、Qt、JavaFX等框架"


class DocumentSkill(FileBackedSkill):
    """文档读写技能包（兼容壳）。"""

    @property
    def skill_id(self) -> str:
        return "document"

    @property
    def fallback_name(self) -> str:
        return "文档读写技能"

    @property
    def fallback_description(self) -> str:
        return "专门负责撰写文档、阅读解析各类文档、文档整理、文档格式转换相关能力"


class FrontendSkill(FileBackedSkill):
    """前端开发技能包（兼容壳）。"""

    @property
    def skill_id(self) -> str:
        return "frontend"

    @property
    def fallback_name(self) -> str:
        return "前端开发技能"

    @property
    def fallback_description(self) -> str:
        return "网页前端编写、样式调试、组件开发、接口对接等前端相关能力"


#: 内置四件套（顺序与 Java 的组件扫描顺序一致，注册进注册表后分组稳定）
LEGACY_SKILL_CLASSES: tuple[type[FileBackedSkill], ...] = (
    BackendSkill, ClientSkill, DocumentSkill, FrontendSkill,
)


def legacy_skills(repository: SkillRepository | None = None) -> list[FileBackedSkill]:
    """构造四个内置技能壳（技能正文来自 `skills/<id>/SKILL.md`）。"""
    return [cls(repository) for cls in LEGACY_SKILL_CLASSES]


# ========================================================================
# 原模块 lionbox/skills/load_tool.py
# ========================================================================
"""`skill_load` 工具：按 id 取回某个技能的完整指令。

【契约来源】逐项对照 Java 版 `core/plugin/skill/SkillLoadTool.java`：
id / name / description / parameters_schema 与 Java **逐字一致**（它们进系统提示词、
进 `/api/plugins`、也进回归套件断言）。

【为什么要有这个工具】系统提示词里只放"技能目录"（一行一个：id、名字、一句话、
什么时候用），不放正文 —— 正文全塞进去，每条消息都要先花上千 token 读一遍技能说明书，
本地模型 11 token/s，这就是实打实的一分钟。目录让**模型自己判断**要不要用某个技能，
要用了再调它取正文，只在这一轮付费。

【为什么极简模式也开放】技能目录在两个模式下都会注入提示词；目录里写了
"先调 skill_load"，工具却不在极简模式的清单里，模型一调就是一次 ❌ 白跑一轮。
这个工具本身只读内存里的技能文件，零副作用，放行没有风险。
"""


from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class SkillLoadTool(ToolPlugin):
    """`skill_load`：加载某个技能的完整指令。"""

    #: 极简模式也开放（Java 的 `isAvailableInMode` 恒为 true → 归 BASE_TOOL）
    minimal_mode = True

    def __init__(self, workspace=None, repository: SkillRepository | None = None) -> None:
        super().__init__(workspace)
        self._repository = repository

    @property
    def repository(self) -> SkillRepository:
        """技能仓库（默认取进程内单例，构造时注入则用注入的 —— 测试友好）。"""
        if self._repository is None:
            self._repository = default_repository()
        return self._repository

    @property
    def id(self) -> str:                      # noqa: A003
        return "tool.skill.load"

    @property
    def name(self) -> str:
        return "skill_load"

    @property
    def description(self) -> str:
        return "加载某个技能的完整指令（技能 id 见系统提示词的技能目录）；按技能做事之前先调它"

    @property
    def category(self) -> str:
        # Java 版是 ToolCategory.OTHER；Python 版 base.py 的等价分类是 SYSTEM
        return ToolCategory.SYSTEM

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "技能 id，例如 backend"},
            },
            "required": ["name"],
        }

    def execute(self, args: dict) -> ToolResult:
        try:
            name = self.get_required_string_arg(args, "name")
        except ValueError as e:
            return self.error(str(e))

        # 不存在 / 解析坏了 / 被用户禁用 —— 三种情况给三种能照着改的提示，
        # 不要一律回"技能不存在"（实测模型会反复换名字重试，白烧好几轮）
        reason = self.repository.unusable_reason(name)
        if reason is not None:
            return self.error(reason)

        defn = self.repository.find_enabled(name)
        if defn is None:                      # unusable_reason 已经覆盖，这里只是兜底
            return self.error(f"技能 {name} 当前不可用")

        text = (f"技能 {defn.id}（{defn.display_name}）的完整指令，"
                f"请按下面这套做法完成当前任务：\n\n{defn.body.strip()}")
        if defn.tools:
            text += "\n\n（这个技能通常要用到的工具：" + "、".join(defn.tools) + "）"
        return self.success(text)


# ========================================================================
# 原模块 lionbox/skills.py
# ========================================================================
"""技能包（对应 Java `core/plugin/skill/`）。

一份技能就是安装目录（或用户配置目录）下的 `skills/<id>/SKILL.md`：
YAML frontmatter + Markdown 正文。模型靠技能目录里的"一句话说明 + 什么时候用"自己挑，
用户也可以用 `@skill:<id>` 或 `POST /api/skills/active` 指定。

    from lionbox.skills import SkillRepository, SkillLoadTool, default_catalog_spi

    repo = SkillRepository(); repo.reload()
    print(repo.catalog_text())
"""



__all__ = [
    "BackendSkill", "CATALOG_MAX", "CFG_DISABLED", "ClientSkill", "DocumentSkill",
    "FileBackedSkill", "FrontendSkill", "FrontmatterError", "ID_PATTERN",
    "LEGACY_IDS", "LEGACY_SKILL_CLASSES", "REQUIRED_FIELDS", "ReloadResult", "SKILL_FILE",
    "SkillCatalogSpi", "SkillController", "SkillDefinition", "SkillLoadTool", "SkillPlugin",
    "SkillRepository", "TOOL_PLUGIN_IDS", "decode", "default_catalog_spi",
    "default_repository", "is_legacy", "legacy_skills", "one_line", "parse", "parse_file",
    "parse_frontmatter", "set_default_repository",
]


def bootstrap_skills(registry=None, repository: SkillRepository | None = None,
                     session_manager=None, settings=None) -> dict:
    """把技能这一套挂起来（app 启动时调一次）。

    做三件事：扫描技能目录 → 把四个内置兼容壳和 `skill_load` 工具注册进插件注册表 →
    把技能目录注入挂到 Agent 主循环（AgentSpi）。

    :param settings: 插件设置。注入了就用注入的 —— 技能系统"是不是被用户关掉"要看
        用户那份设置，用错实例（比如进程单例）会出现"设置里关掉了、提示词里还在"。
    :return: `{"count":…, "errors":…, "skills":[…id…], "spi":…}`
    """
    repo = repository if repository is not None else default_repository()
    result = repo.reload()

    if registry is None:
        from lionbox.plugins.lifecycle import default_registry
        registry = default_registry()

    registered: list[str] = []
    for skill in legacy_skills(repo):
        registry.register(skill)
        registered.append(skill.id)

    from lionbox.plugins.base import REGISTRY as TOOL_REGISTRY
    loader_tool = TOOL_REGISTRY.get("tool.skill.load") or SkillLoadTool(repository=repo)
    registry.register(loader_tool)
    registered.append(loader_tool.id)

    spi = SkillCatalogSpi(repo, settings=settings, registry=registry,
                          session_manager=session_manager)
    spi.register()
    return {
        "count": result.count,
        "errors": result.errors,
        "broken": result.broken,
        "skills": [d.id for d in repo.list()],
        "registered": registered,
        "spi": spi,
    }
