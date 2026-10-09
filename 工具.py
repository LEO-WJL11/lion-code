# -*- coding: utf-8 -*-
r"""工具（由引擎内联生成）
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
    "lionbox.tools",
    "lionbox.tools.file._common",
    "lionbox.tools.file._gate",
    "lionbox.tools.file.file_append",
    "lionbox.tools.file.file_chmod",
    "lionbox.tools.file.file_copy",
    "lionbox.tools.file.file_delete",
    "lionbox.tools.file.file_glob",
    "lionbox.tools.file.file_head_tail",
    "lionbox.tools.file.file_info",
    "lionbox.tools.file.file_line_count",
    "lionbox.tools.file.file_list",
    "lionbox.tools.file.file_mkdir",
    "lionbox.tools.file.file_modify",
    "lionbox.tools.file.file_move",
    "lionbox.tools.file.file_read",
    "lionbox.tools.file.file_search",
    "lionbox.tools.file.file_touch",
    "lionbox.tools.file.file_tree",
    "lionbox.tools.file.file_wc",
    "lionbox.tools.file.file_write",
    "lionbox.tools.file",
    "lionbox.tools.context.context_prune",
    "lionbox.tools.context.context_window",
    "lionbox.tools.context",
    "lionbox.tools.code.base64",
    "lionbox.tools.code.cron",
    "lionbox.tools.code.diff",
    "lionbox.tools.code.escape",
    "lionbox.tools.code.format",
    "lionbox.tools.code.hash",
    "lionbox.tools.code.json",
    "lionbox.tools.code.markdown",
    "lionbox.tools.code.number",
    "lionbox.tools.code.regex",
    "lionbox.tools.code.string",
    "lionbox.tools.code.timestamp",
    "lionbox.tools.code.uuid",
    "lionbox.tools.code.yaml",
    "lionbox.tools.code",
    "lionbox.tools.git._git",
    "lionbox.tools.git.git_branch",
    "lionbox.tools.git.git_commit",
    "lionbox.tools.git.git_diff",
    "lionbox.tools.git.git_init",
    "lionbox.tools.git.git_log",
    "lionbox.tools.git.git_remote",
    "lionbox.tools.git.git_reset",
    "lionbox.tools.git.git_stash",
    "lionbox.tools.git.git_status",
    "lionbox.tools.git",
    "lionbox.tools.shell.persistent_shell",
    "lionbox.tools.shell.shell_background",
    "lionbox.tools.shell.terminal_limits",
    "lionbox.tools.shell.shell_execute",
    "lionbox.tools.shell.shell_stop",
    "lionbox.tools.shell",
    "lionbox.tools.system.ask_user",
    "lionbox.tools.system.env_var",
    "lionbox.tools.system.system_info",
    "lionbox.tools.system.working_dir",
    "lionbox.tools.system",
    "lionbox.tools.web.dns_lookup",
    "lionbox.tools.web.download_file",
    "lionbox.tools.web.http_get",
    "lionbox.tools.web.fetch_url",
    "lionbox.tools.web.headless_browser",
    "lionbox.tools.web.http_post",
    "lionbox.tools.web.translate",
    "lionbox.tools.web.web_search",
    "lionbox.tools.web",
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

# 【每个被内联模块各自原本的 __file__】有代码用它推算"程序装在哪"（例如技能目录：
# `skills/repository.py` 往上三层才是安装根）。内联后 `__file__` 全是 main.py 的路径，
# 向上推会跑到仓库外面 —— 实测后果是内置技能一个都找不到。所以按模块各记一份。
# 路径不必真实存在：用到的是路径运算，只要目录层级一致，算出的安装根就一样。
_ORIG_FILE_tools = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\__init__.py"
_ORIG_FILE_tools_file__common = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\_common.py"
_ORIG_FILE_tools_file__gate = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\_gate.py"
_ORIG_FILE_tools_file_file_append = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_append.py"
_ORIG_FILE_tools_file_file_chmod = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_chmod.py"
_ORIG_FILE_tools_file_file_copy = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_copy.py"
_ORIG_FILE_tools_file_file_delete = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_delete.py"
_ORIG_FILE_tools_file_file_glob = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_glob.py"
_ORIG_FILE_tools_file_file_head_tail = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_head_tail.py"
_ORIG_FILE_tools_file_file_info = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_info.py"
_ORIG_FILE_tools_file_file_line_count = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_line_count.py"
_ORIG_FILE_tools_file_file_list = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_list.py"
_ORIG_FILE_tools_file_file_mkdir = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_mkdir.py"
_ORIG_FILE_tools_file_file_modify = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_modify.py"
_ORIG_FILE_tools_file_file_move = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_move.py"
_ORIG_FILE_tools_file_file_read = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_read.py"
_ORIG_FILE_tools_file_file_search = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_search.py"
_ORIG_FILE_tools_file_file_touch = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_touch.py"
_ORIG_FILE_tools_file_file_tree = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_tree.py"
_ORIG_FILE_tools_file_file_wc = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_wc.py"
_ORIG_FILE_tools_file_file_write = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\file_write.py"
_ORIG_FILE_tools_file = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\file\__init__.py"
_ORIG_FILE_tools_context_context_prune = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\context\context_prune.py"
_ORIG_FILE_tools_context_context_window = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\context\context_window.py"
_ORIG_FILE_tools_context = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\context\__init__.py"
_ORIG_FILE_tools_code_base64 = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\base64.py"
_ORIG_FILE_tools_code_cron = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\cron.py"
_ORIG_FILE_tools_code_diff = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\diff.py"
_ORIG_FILE_tools_code_escape = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\escape.py"
_ORIG_FILE_tools_code_format = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\format.py"
_ORIG_FILE_tools_code_hash = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\hash.py"
_ORIG_FILE_tools_code_json = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\json.py"
_ORIG_FILE_tools_code_markdown = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\markdown.py"
_ORIG_FILE_tools_code_number = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\number.py"
_ORIG_FILE_tools_code_regex = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\regex.py"
_ORIG_FILE_tools_code_string = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\string.py"
_ORIG_FILE_tools_code_timestamp = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\timestamp.py"
_ORIG_FILE_tools_code_uuid = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\uuid.py"
_ORIG_FILE_tools_code_yaml = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\yaml.py"
_ORIG_FILE_tools_code = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\code\__init__.py"
_ORIG_FILE_tools_git__git = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\_git.py"
_ORIG_FILE_tools_git_git_branch = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_branch.py"
_ORIG_FILE_tools_git_git_commit = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_commit.py"
_ORIG_FILE_tools_git_git_diff = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_diff.py"
_ORIG_FILE_tools_git_git_init = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_init.py"
_ORIG_FILE_tools_git_git_log = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_log.py"
_ORIG_FILE_tools_git_git_remote = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_remote.py"
_ORIG_FILE_tools_git_git_reset = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_reset.py"
_ORIG_FILE_tools_git_git_stash = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_stash.py"
_ORIG_FILE_tools_git_git_status = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\git_status.py"
_ORIG_FILE_tools_git = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\git\__init__.py"
_ORIG_FILE_tools_shell_persistent_shell = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\shell\persistent_shell.py"
_ORIG_FILE_tools_shell_shell_background = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\shell\shell_background.py"
_ORIG_FILE_tools_shell_terminal_limits = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\shell\terminal_limits.py"
_ORIG_FILE_tools_shell_shell_execute = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\shell\shell_execute.py"
_ORIG_FILE_tools_shell_shell_stop = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\shell\shell_stop.py"
_ORIG_FILE_tools_shell = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\shell\__init__.py"
_ORIG_FILE_tools_system_ask_user = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\system\ask_user.py"
_ORIG_FILE_tools_system_env_var = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\system\env_var.py"
_ORIG_FILE_tools_system_system_info = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\system\system_info.py"
_ORIG_FILE_tools_system_working_dir = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\system\working_dir.py"
_ORIG_FILE_tools_system = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\system\__init__.py"
_ORIG_FILE_tools_web_dns_lookup = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\dns_lookup.py"
_ORIG_FILE_tools_web_download_file = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\download_file.py"
_ORIG_FILE_tools_web_http_get = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\http_get.py"
_ORIG_FILE_tools_web_fetch_url = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\fetch_url.py"
_ORIG_FILE_tools_web_headless_browser = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\headless_browser.py"
_ORIG_FILE_tools_web_http_post = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\http_post.py"
_ORIG_FILE_tools_web_translate = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\translate.py"
_ORIG_FILE_tools_web_web_search = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\web_search.py"
_ORIG_FILE_tools_web = r"C:\Users\Leo\Desktop\lion-code\python\lionbox\tools\web\__init__.py"


# ========================================================================
# 原模块 lionbox/tools.py
# ========================================================================
"""工具装载：把 57 个工具显式 import 进来，让它们的 @tool 装饰器完成登记。



【为什么是显式名单而不是目录扫描】扫描要遍历文件系统、顺序不确定，而且会让启动路径

变成"先发现再加载"。写死名单后加载就是一条确定的 import 链，启动耗时可控

（实测：Python 侧 import + 装配 64 ms）。名单由 Java 源码 `core/plugin/tool/**` 生成。



【为什么 import 放在 load() 里而不是模块顶层】工具子包与 `plugins.base` 之间存在互相引用，

放顶层会在 `import lionbox.tools` 的瞬间触发循环导入，且任一子包有问题会连累整个包不可用。

放进 load() 后逐个导入、逐个兜错：一个工具坏掉不影响其余 —— 与 `plugins.base.load_all()`

的容错策略一致。

"""





from pathlib import Path



#: (包名, 模块名, 类名) —— 由 Java 源码目录生成，供用例与文档核对数量

TOOL_MODULES: list[tuple[str, str, str]] = [

    ("code", "base64", "Base64Tool"),

    ("code", "cron", "CronTool"),

    ("code", "diff", "DiffTool"),

    ("code", "escape", "EscapeTool"),

    ("code", "format", "CodeFormatTool"),

    ("code", "hash", "HashTool"),

    ("code", "json", "JsonTool"),

    ("code", "markdown", "MarkdownTool"),

    ("code", "number", "NumberTool"),

    ("code", "regex", "RegexTool"),

    ("code", "string", "StringTool"),

    ("code", "timestamp", "TimestampTool"),

    ("code", "uuid", "UuidTool"),

    ("code", "yaml", "YamlTool"),

    ("context", "context_prune", "ContextPruneTool"),

    ("context", "context_window", "ContextWindowTool"),

    ("file", "file_append", "FileAppendTool"),

    ("file", "file_chmod", "FileChmodTool"),

    ("file", "file_copy", "FileCopyTool"),

    ("file", "file_delete", "FileDeleteTool"),

    ("file", "file_glob", "FileGlobTool"),

    ("file", "file_head_tail", "FileHeadTailTool"),

    ("file", "file_info", "FileInfoTool"),

    ("file", "file_line_count", "FileLineCountTool"),

    ("file", "file_list", "FileListTool"),

    ("file", "file_mkdir", "FileMkdirTool"),

    ("file", "file_modify", "FileModifyTool"),

    ("file", "file_move", "FileMoveTool"),

    ("file", "file_read", "FileReadTool"),

    ("file", "file_search", "FileSearchTool"),

    ("file", "file_touch", "FileTouchTool"),

    ("file", "file_tree", "FileTreeTool"),

    ("file", "file_wc", "FileWcTool"),

    ("file", "file_write", "FileWriteTool"),

    ("git", "git_branch", "GitBranchTool"),

    ("git", "git_commit", "GitCommitTool"),

    ("git", "git_diff", "GitDiffTool"),

    ("git", "git_init", "GitInitTool"),

    ("git", "git_log", "GitLogTool"),

    ("git", "git_remote", "GitRemoteTool"),

    ("git", "git_reset", "GitResetTool"),

    ("git", "git_stash", "GitStashTool"),

    ("git", "git_status", "GitStatusTool"),

    ("shell", "shell_background", "ShellBackgroundTool"),

    ("shell", "shell_execute", "ShellExecuteTool"),

    ("shell", "shell_stop", "ShellStopTool"),

    ("system", "ask_user", "AskUserTool"),

    ("system", "env_var", "EnvVarTool"),

    ("system", "system_info", "SystemInfoTool"),

    ("system", "working_dir", "WorkingDirTool"),

]



SUBPACKAGES = ("code", "context", "file", "git", "shell", "system", "web")



_loaded = False





def load(workspace: Path | None = None):

    """导入所有工具子包（触发 @tool 登记）并实例化注册。返回注册表。"""

    global _loaded

    import importlib



    for name in SUBPACKAGES:

        try:

            None  # 子包已内联进本文件：登记在导入时就完成，无需动态导入

        except Exception as e:  # noqa: BLE001

            print(f"[工具] 子包 {name} 导入失败，跳过: {type(e).__name__}: {e}", flush=True)



    from lionbox.plugins.base import load_all
    registry = load_all(workspace)

    _loaded = True

    return registry



# ========================================================================
# 原模块 lionbox/tools/file/_common.py
# ========================================================================
"""文件类工具共用的底层助手。

【契约来源】逐项对照 Java 版 `core/plugin/tool/AbstractToolPlugin.java` 与
`core/plugin/tool/file/FileWcTool.java`，函数名刻意取成与 Java 同名，
这样后面移植别的工具类时可以直接 `from ._common import looks_binary`，不用改调用点。

只放"被多个工具用到"的东西；单工具用的私有逻辑留在各自的模块里。

【为什么这些行为不能简化】
1. `decode_text` 必须是"UTF-8 严格 → GBK → UTF-8 替换"三级退路。
   `new String(bytes, UTF_8)` / `bytes.decode("utf-8")` **都不会抛异常**，
   它们把非法字节换成 U+FFFD —— 拿它当"先试 UTF-8"用，GBK 中文文件读出来全是乱码。
   必须用严格解码器：真抛了才说明不是 UTF-8。
2. `charset_of` / `write_text_preserving_charset`：记事本存的 ANSI(GBK) 中文文件
   被改一次就变成 UTF-8（内容不乱，但编码被悄悄换了）。
3. `strip_leading_bom`：只去掉**开头**那一个 U+FEFF。它出现在正文中间是合法的零宽字符，
   不能全局清掉；也不在字节层砍 EF BB BF —— 那会改到"UTF-8 严格失败才退 GBK"的判定顺序。
4. `looks_binary`：`decode_text` 永不抛异常，所以"读不出来就是二进制"是**死代码**。
   必须按字节判：NUL，或 `\\t \\n \\r \\f \\b` 之外的控制字符超过一成。
"""


import os
import re
import sys
from pathlib import Path

__all__ = [
    "charset_of",
    "decode_text",
    "detect_line_separator",
    "glob_to_regex",
    "glob_matches",
    "java_trim",
    "looks_binary",
    "path_sort_key",
    "read_text_file",
    "read_text_lines",
    "similar_path_hint",
    "sorted_children",
    "translate_glob",
    "walk_entries",
    "walk_files",
    "write_text_preserving_charset",
]

BINARY_SAMPLE_BYTES = 8192
"""二进制取样长度：与 Java 版 `FileWcTool.looksBinary` 的 8KB 一致。"""

_CONTROL_OK = (0x09, 0x0A, 0x0D, 0x0C, 0x08)  # \t \n \r \f \b

#: `String.trim()` 去掉的是**所有 codePoint <= U+0020** 的首尾字符（0x00-0x20 共 33 个），
#: 不是"列出来的那几个空白"——`str.strip(" \t\n\r\f\v")` 只去 6 个，
#: 以 \x00、\x1f 这类控制字符开头的文本就漏掉了（count_words 判空/file_search 清洗都会偏）。
_JAVA_TRIM_WS = "".join(chr(i) for i in range(0x21))


def java_trim(text: str) -> str:
    """`String.trim()` 的等价物：只去 <= U+0020 的首尾字符。

    【别用 `str.strip()`】Python 的 strip 还会去掉 U+3000（全角空格）、U+00A0 这些，
    Java 的 trim 不会。判空/判 null 的字面量走的是 Java 语义，差一个字符结论就反了。
    """
    return text.strip(_JAVA_TRIM_WS)


# --------------------------------------------------------------------------
# 容错编解码
# --------------------------------------------------------------------------


def _strip_leading_bom(text: str) -> str:
    """去掉开头的 UTF-8 BOM。只去第一个，正文中间的 U+FEFF 是合法零宽字符。"""
    return text[1:] if text.startswith("\ufeff") else text


def _call_codec(codec: str, data: bytes) -> bytes | None:
    """拿指定编码做一次无损往返；不能无损往返返回 None。

    GBK 是 ASCII 的超集、UTF-8 也是，所以"解出来只包含 ASCII"时，
    UTF-8 并不会抛异常 —— 光看抛不抛会把 GBK 内容误判成 UTF-8。往返一次才能分辨。
    """
    try:
        return data.decode(codec).encode(codec)
    except (UnicodeDecodeError, UnicodeEncodeError, LookupError):
        return None


def _decode_gbk_lenient(data: bytes) -> str:
    """GBK 的**永不失败**解码：坏字节换成 U+FFFD，好字节照样留住。

    对应 Java 的 `Charset.forName("GBK").newDecoder().onMalformedInput(REPLACE)`。
    为什么不能直接 `data.decode("gbk", "replace")`：Python 的 gbk 编解码器是**严格**映射，
    换不回去的字节（GBK 用户自定义区、0x80 这类）会抛 LookupError，于是被整段换成 U+FFFD；
    Java 那边那些字节是有字形的。这里退到 cp936 逐字节解，尽量和 Java 对齐。
    """
    try:
        return data.decode("cp936", "replace")
    except LookupError:
        pass
    buf: list[str] = []
    i = 0
    n = len(data)
    while i < n:
        byte = data[i]
        if byte < 0x80:
            buf.append(chr(byte))
            i += 1
            continue
        if 0x81 <= byte <= 0xFE and i + 1 < n:
            pair = data[i:i + 2]
            try:
                buf.append(pair.decode("gbk"))
                i += 2
                continue
            except (UnicodeDecodeError, LookupError):
                pass
        buf.append("\ufffd")
        i += 1
    return "".join(buf)


def decode_text(data: bytes) -> str:
    """按 UTF-8 → GBK → 替换 的顺序容错解码（Windows 上命令输出常是 GBK）。

    每条退路上解出来的文本都要去掉开头的 BOM。
    """
    try:
        return _strip_leading_bom(data.decode("utf-8", "strict"))
    except UnicodeDecodeError:
        pass
    except LookupError:  # pragma: no cover - 标准库必然有 utf-8
        return _strip_leading_bom(data.decode("utf-8", "replace"))
    return _strip_leading_bom(_decode_gbk_lenient(data))


def charset_of(path: Path) -> str:
    """认出这个文件原本是什么编码（UTF-8 还是 GBK）。

    读的时候用 `decode_text` 容错，写回去必须用**同一个编码**。
    文件不存在或空文件按 UTF-8。
    """
    try:
        if not path.exists():
            return "utf-8"
        data = path.read_bytes()
        if not data:
            return "utf-8"
        data.decode("utf-8", "strict")
        return "utf-8"
    except (UnicodeDecodeError, OSError):
        return "gbk"


def write_text_preserving_charset(path: Path, content: str) -> None:
    """按文件原有编码写回（不存在则 UTF-8），语义同 Java 的 `writeTextPreservingCharset`。"""
    path.write_bytes(content.encode(charset_of(path), "replace"))


def read_text_file(path: Path) -> str:
    """容错读整个文本文件（同 Java 的 `readTextFile`）。"""
    return decode_text(path.read_bytes())


def read_text_lines(path: Path) -> list[str]:
    """容错读文本文件并按行切开。

    行语义与 Java 的 `readTextLines` 一致：按 `\\r?\\n` 切，末尾多出来的那个空行去掉。
    所以"以换行结尾"不会多算一行，"空文件"是 0 行。
    """
    text = decode_text(path.read_bytes())
    lines = text.split("\n")
    lines = [ln[:-1] if ln.endswith("\r") else ln for ln in lines]
    if lines and lines[-1] == "":
        lines.pop()
    return lines


def detect_line_separator(text: str) -> str:
    """原文用的是什么换行符（没有就 LF）—— 写回时保持一致，别把 LF 文件变成 CRLF。"""
    return "\r\n" if text and "\r\n" in text else "\n"


def looks_binary(data: bytes) -> bool:
    """这个文件是不是二进制（取样前 8KB，同 Java 的 `FileWcTool.looksBinary`）。

    判据：出现 NUL 字节，或者 `\\t \\n \\r \\f \\b` 之外的控制字符超过一成。
    对文本文件不会误判；对图片/exe/zip 则能挡住那些"看着挺正常"的假行数。
    """
    sample = data[:BINARY_SAMPLE_BYTES]
    n = len(sample)
    if n == 0:
        return False
    control = 0
    for byte in sample:
        if byte == 0:
            return True
        if byte < 0x20 and byte not in _CONTROL_OK:
            control += 1
    return control * 10 > n


# --------------------------------------------------------------------------
# 路径与遍历
# --------------------------------------------------------------------------


#: "不设层数上限"用的深度。统计类工具（line_count / word_count 的目录累计）问的是
#: "这个目录里一共多少行"，Java 那边用的就是不带 maxDepth 的 `Files.walk(dir)`；
#: file_glob / file_search 显式传 10 是为了对齐 `Files.walk(dir, 10)`，两回事，别混用。
WALK_UNLIMITED_DEPTH = 1_000_000


def walk_files(root: Path, max_depth: int = 10) -> list[Path]:
    """等价于 Java 的 `Files.walk(root, maxDepth).filter(Files::isRegularFile)`。

    返回的是**普通文件**，顺序按目录逐层展开（先父目录的内容，再子目录），
    不跟符号链接目录，碰到读不了的目录直接跳过。
    """
    out: list[Path] = []
    root = Path(root)
    # (目录, 剩余深度)；剩余深度 0 表示"这个目录本身不再展开"
    stack: list[tuple[Path, int]] = [(root, max_depth)]
    while stack:
        current, depth = stack.pop()
        try:
            entries = list(os.scandir(current))
        except OSError:
            continue
        subdirs: list[Path] = []
        for entry in entries:
            try:
                if entry.is_file(follow_symlinks=True):
                    out.append(Path(entry.path))
                elif entry.is_dir(follow_symlinks=True) and depth > 1:
                    subdirs.append(Path(entry.path))
            except OSError:
                continue
        # 栈是后进先出，倒着压才能让先扫到的目录先展开
        for d in reversed(subdirs):
            stack.append((d, depth - 1))
    return out


def walk_entries(root: Path, max_depth: int) -> list[tuple[Path, str]]:
    """等价于 Java 的 `Files.walk(dir, maxDepth)`：返回 `(路径, 相对路径)`，含根自己。

    相对路径用 `os.sep` 拼（Windows 上是 `\\`，与 Java `Path.relativize().toString()` 一致）；
    根自己算 `.`（Java 里 relativize 得到空串，调用方会补成 `.` —— 这里直接补好）。
    """
    root = Path(root)
    out: list[tuple[Path, str]] = [(root, ".")]
    depth = max(0, max_depth)
    if depth == 0:
        return out
    stack: list[tuple[Path, int, str]] = [(root, depth, "")]
    while stack:
        current, remaining, rel = stack.pop()
        try:
            entries = list(os.scandir(current))
        except OSError:
            continue
        subdirs: list[tuple[Path, int, str]] = []
        for entry in entries:
            child_rel = entry.name if not rel else rel + os.sep + entry.name
            out.append((Path(entry.path), child_rel))
            try:
                if entry.is_dir(follow_symlinks=True) and remaining > 1:
                    subdirs.append((Path(entry.path), remaining - 1, child_rel))
            except OSError:
                continue
        for item in reversed(subdirs):
            stack.append(item)
    return out


def path_sort_key(path: Path) -> str:
    """`Files.list(dir).sorted()` 的排序键。

    Java 在 Windows 上是 `WindowsPath`，比较用的是大小写不敏感的字符串序；
    POSIX 上就是普通字符串序。这里对齐这个差异。
    """
    text = str(path)
    return text.lower() if sys.platform == "win32" else text


def sorted_children(path: Path) -> list[Path] | None:
    """`Files.list(dir).sorted()`：目录里的条目按路径排好序；读不了返回 None。"""
    try:
        entries = [Path(e.path) for e in os.scandir(path)]
    except OSError:
        return None
    entries.sort(key=path_sort_key)
    return entries


def similar_path_hint(raw_path: str, workspace: Path | None = None) -> str:
    """文件不存在时，给一句"同目录下有相近的名字"。

    实测：模型把 `test.txt` 记成 `test_file.txt`、把 `note.md` 写成 `notes.md`，
    只回一句"文件不存在"，它就再试一次（还是错）。给个候选名字，下一轮基本一次就对。
    """
    try:
        raw = str(raw_path)
        parent = os.path.dirname(raw)
        if not parent:
            parent = str(workspace) if workspace else "."
        directory = Path(parent)
        if not directory.is_dir():
            return ""
        want = os.path.basename(raw).lower()
        want_tokens = _tokens(want)
        near: list[str] = []
        try:
            names = [e.name for e in os.scandir(directory)]
        except OSError:
            return ""
        for name in names:
            low = name.lower()
            if low == want:
                continue
            hit = want in low or low in want
            if not hit:
                # 模型把 note_file.txt 记成 nope_note.txt —— 去掉下划线/横线后再比一次
                flat_n = low.replace("_", "").replace("-", "")
                flat_w = want.replace("_", "").replace("-", "")
                hit = flat_n in flat_w or flat_w in flat_n
            if not hit:
                # 再按"共同词"比一次（只比下划线那一种太死，等于没有）
                for token in want_tokens:
                    if len(token) >= 3 and token in _tokens(low):
                        hit = True
                        break
            if hit:
                near.append(name)
        if not near:
            return ""
        return "（同目录下有这些相近的名字，看看是不是其中之一: " + "、".join(near[:5]) + "）"
    except Exception:
        return ""


def _tokens(name: str) -> list[str]:
    """把文件名切成词（按 . _ - 空格 切），用于"相近名字"比对。"""
    return [t for t in re.split(r"[._\-\s]+", name) if t and not t.isspace()]


# --------------------------------------------------------------------------
# glob（对齐 java.nio 的 PathMatcher：`**` 不跨目录、`**/` 要求至少一层）
# --------------------------------------------------------------------------


def glob_to_regex(pattern: str) -> str:
    """把 Java `FileSystems.getDefault().getPathMatcher("glob:" + p)` 的语法翻成正则。

    【Python 的 fnmatch/Path.glob 都不能用】两者对 `**` 的语义与 Java 不同，实测对照如下
    （`Paths.get(相对路径)` 直接喂给 PathMatcher，Windows 上实测）：

        `**`              => 匹配一切（A.java、sub/B.java、sub/deep/C.java）—— `**` 可以跨 **0** 层
        `**/*`            => 只匹配**至少一层**目录下的（sub/B.java、d/A.bak），根下的 A.java **不匹配**
        `**/*.java`       => 同上，根下的 A.java **不匹配**
        `**/**/*.java`    => 要**两层**以上（sub/deep/C.java），一层的不匹配
        `*`               => 只匹配根下（A.java），**跨不了** `/`
        `sub/**`          => sub 底下的一切，含直接子项（sub/B.java）

    规律就是：`**` = 任意多的任意字符（含空），而它后面跟着 `/` 时那个 `/` 是**必须真出现**的，
    所以 `**/*` 里那个分隔符不能省 —— "可以少一层"这种口径和 Java 对不上，
    `glob_files(pattern="**/*.txt")` 会凭空多报根目录下的文件。
    """
    out: list[str] = []
    i = 0
    n = len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == "*":
            if i + 1 < n and pattern[i + 1] == "*":
                # `**` = 任意多字符（含空）
                out.append(".*")
                i += 2
                continue
            out.append("[^/]*")
            i += 1
            continue
        if ch == "?":
            out.append("[^/]")
            i += 1
            continue
        if ch == "[":
            end = _find_class_end(pattern, i + 1)
            if end < 0:
                out.append(re.escape(ch))
                i += 1
                continue
            body = pattern[i + 1:end]
            out.append(_translate_class(body))
            i = end + 1
            continue
        if ch == "{":
            end = _find_brace_end(pattern, i + 1)
            if end < 0:
                out.append(re.escape(ch))
                i += 1
                continue
            # 组里仍是一个完整 glob（`{**/*.java,*.java}` 的两支各自要有 glob 语义），
            # 所以递归翻，不能 re.escape
            alts = [_split_brace(branch) for branch in pattern[i + 1:end].split(",")]
            out.append("(?:" + "|".join(glob_to_regex(a) for a in alts) + ")")
            i = end + 1
            continue
        if ch == "\\" and i + 1 < n:
            out.append(re.escape(pattern[i + 1]))
            i += 2
            continue
        out.append(re.escape(ch))
        i += 1
    return "".join(out)


def _find_class_end(pattern: str, start: int) -> int:
    i = start
    if i < len(pattern) and pattern[i] == "!":
        i += 1
    if i < len(pattern) and pattern[i] == "]":
        i += 1
    while i < len(pattern):
        if pattern[i] == "]":
            return i
        if pattern[i] == "\\":
            i += 1
        i += 1
    return -1


def _find_brace_end(pattern: str, start: int) -> int:
    """找到配对的 `}`（支持嵌套，找不到返回 -1）。"""
    depth = 0
    i = start
    while i < len(pattern):
        if pattern[i] == "\\":
            i += 2
            continue
        if pattern[i] == "{":
            depth += 1
        elif pattern[i] == "}":
            if depth == 0:
                return i
            depth -= 1
        i += 1
    return -1


def _split_brace(body: str) -> str:
    """清掉组内可能残留的嵌套括号（Java 的 glob 组不支持嵌套，这里只做防御）。"""
    return body.replace("{", "").replace("}", "")


def _translate_class(body: str) -> str:
    """把 `[abc]` / `[!abc]` / `[a-z]` 翻成正则字符类（Java 的 `!` 等于正则的 `^`）。"""
    negate = body.startswith("!")
    if negate:
        body = body[1:]
    out = ["["]
    if negate:
        out.append("^")
    i = 0
    while i < len(body):
        ch = body[i]
        if ch == "\\" and i + 1 < len(body):
            out.append(re.escape(body[i + 1]))
            i += 2
            continue
        if ch in "^]\\":
            out.append("\\" + ch)
        elif ch == "[":
            out.append("\\[")
        else:
            out.append(ch)
        i += 1
    out.append("]")
    return "".join(out)


def translate_glob(pattern: str) -> re.Pattern[str]:
    """编译一个 Java 语义的 glob，用来 `matches(相对路径)`。"""
    return re.compile(glob_to_regex(pattern) + r"\Z")


#: 从 Probe2 实测出来的对照表（pattern, 相对路径, 期望是否匹配）—— 移植时的回归锚点
JAVA_GLOB_CASES: tuple[tuple[str, str, bool], ...] = (
    ("**", "A.java", True),
    ("**", "sub/B.java", True),
    ("**", "sub/deep/C.java", True),
    ("**/*", "A.java", False),
    ("**/*", "sub/B.java", True),
    ("**/*", "d/A.bak", True),
    ("**/*.java", "A.java", False),
    ("**/*.java", "sub/B.java", True),
    ("**/*.java", "sub/deep/C.java", True),
    ("**/*.txt", "note.txt", False),
    ("**/**", "sub/B.java", True),
    ("**/**/*.java", "sub/B.java", False),
    ("**/**/*.java", "sub/deep/C.java", True),
    ("*", "A.java", True),
    ("*", "note.txt", True),
    ("*", "d/A.bak", False),
    ("*.java", "A.java", True),
    ("*.java", "sub/B.java", False),
    ("d/*", "d/A.bak", True),
    ("sub/**", "sub/B.java", True),
    ("sub/**", "sub/deep/C.java", True),
    ("sub/**/*.java", "sub/B.java", False),
    ("sub/**/*.java", "sub/deep/C.java", True),
    ("{**/*.java,*.java}", "A.java", True),
    ("{**/*.java,*.java}", "sub/B.java", True),
    ("**/*.{java,txt}", "sub/B.java", True),
    ("**/*.{java,txt}", "A.java", False),
)


def glob_matches(pattern: str, relative: str) -> bool:
    """相对路径按 Java 的 PathMatcher 语义匹配（统一用 `/` 当分隔符）。"""
    return bool(translate_glob(pattern).match(relative.replace(os.sep, "/")))


# --------------------------------------------------------------------------
# 杂项
# --------------------------------------------------------------------------


def is_windows() -> bool:
    """是不是 Windows（对齐 Java 的 `isWindows()`）。"""
    return sys.platform == "win32"


# ========================================================================
# 原模块 lionbox/tools/file/_gate.py
# ========================================================================
"""改动人工审核闸门（ChangeReview）的接线点。

【为什么单独一个模块】`change_review.py` 是另一个施工单元的产物，按分工不能替它建文件。
所以这里只留一个**接线用的钩子**：
  - 接线方（`lionbox.agent.change_review`）拿到真正的闸门后调 `set_review(...)` 挂上；
  - 改文件的工具统一调 `intercept(...)`，Java 的调用点逐字对得上：

        Optional<ToolResult> gate = changeReview.intercept(name, path, oldContent, newContent);
        if (gate.isPresent()) return gate.get();

  - 没挂闸门时 `intercept` 返回 `None`（= Java 的 `Optional.empty()`），
    工具就照常落盘 —— 与 Java 里"审核没开"的行为一致。

【为什么显式登记而不是目录扫描/延迟导入】
PORTING.md 第三条：不许用目录扫描发现插件。这里同样用显式 `set_review`，
启动顺序可控，也不会因为模块还没到位就在 import 期炸掉。
"""


from typing import Any, Callable, Protocol

__all__ = ["REVIEW_HOOK", "ReviewHook", "intercept", "set_review"]


class ReviewHook(Protocol):
    """闸门接口：与 Java `ChangeReview.intercept` 同形。

    返回 `None` 表示放行（没有待审改动）；返回 `ToolResult` 表示这次调用已被
    "攒成待审改动"，工具应当把这个结果原样回给模型，**不要落盘**。
    """

    def intercept(self, tool_name: str, path: str, old_content: str | None,
                  new_content: str | None) -> Any | None:
        ...


REVIEW_HOOK: ReviewHook | None = None
"""当前挂上的闸门；None = 审核没开（或还没接线）。"""


def set_review(hook: ReviewHook | None) -> None:
    """挂上/摘掉闸门。接线方在启动时调一次。"""
    global REVIEW_HOOK
    REVIEW_HOOK = hook


def intercept(tool_name: str, path: str, old_content: str | None,
              new_content: str | None) -> Any | None:
    """登记一次待审改动。

    :param tool_name: 工具名（Java 传的是 `getName()`）
    :param path: 已经 resolve 过的绝对路径
    :param old_content: 原文（文件不存在传 None）；递归删目录时 Java 传的是一句中文摘要
    :param new_content: 新文（删除传 None）
    :return: 有待审改动时返回工具结果（调用方直接 `return` 它），否则 None
    """
    hook: Callable[..., Any] | None = REVIEW_HOOK.intercept if REVIEW_HOOK else None
    if hook is None:
        return None
    return hook(tool_name, path, old_content, new_content)


# ========================================================================
# 原模块 lionbox/tools/file/file_append.py
# ========================================================================
"""`append_file` —— 向文件末尾追加内容。

【契约来源】`core/plugin/tool/file/FileAppendTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolPlugin, ToolResult, tool


@tool
class FileAppendTool(ToolPlugin):
    """文件追加工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_MODIFY 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.append"

    @property
    def name(self) -> str:
        return "append_file"

    @property
    def description(self) -> str:
        return "向文件末尾追加内容"

    @property
    def category(self) -> str:
        return "FILE_MODIFY"

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "content": {"type": "string", "description": "追加内容"},
            },
            "required": ["path", "content"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            content = self.get_required_string_arg(args, "content")

            # 追加也用文件原本的编码：GBK 的中文文件追加之后仍是 GBK，不会变成混合编码
            target = Path(path)
            old = read_text_file(target) if target.is_file() else None
            gate = intercept(self.name, str(path), old, content if old is None else old + content)
            if gate is not None:
                return gate

            # Java: Files.writeString(..., charsetOf(path), CREATE, APPEND) —— 不截断
            with target.open("ab") as fh:
                fh.write(content.encode(charset_of(target), "replace"))
            return self.success(f"内容已追加到: {path}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"追加失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_chmod.py
# ========================================================================
"""`change_permissions` —— 修改文件权限。

【契约来源】`core/plugin/tool/file/FileChmodTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【行为】Java 走 POSIX 权限集，在不支持的系统上抛 `UnsupportedOperationException`，
退回 `File.setReadable/setWritable/setExecutable`（三个参数默认值都是 **false**：
不传就表示"关掉"）。Python 在 Windows 上没有 os.chmod 的权限位语义，
所以用同一套判据分流：`os.name == "posix"` 走 chmod，否则走只读位。
"""


import os
import stat
from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolPlugin, ToolResult, tool


@tool
class FileChmodTool(ToolPlugin):
    """文件权限修改工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_MODIFY 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.chmod"

    @property
    def name(self) -> str:
        return "change_permissions"

    @property
    def description(self) -> str:
        return "修改文件权限"

    @property
    def category(self) -> str:
        return "FILE_MODIFY"

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "readable": {"type": "boolean", "description": "可读"},
                "writable": {"type": "boolean", "description": "可写"},
                "executable": {"type": "boolean", "description": "可执行"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            file_path = Path(path)

            readable = self.get_bool_arg(args, "readable", False)
            writable = self.get_bool_arg(args, "writable", False)
            executable = self.get_bool_arg(args, "executable", False)

            if os.name == "posix":
                # Java 只加 OWNER_* 三位的权限（从空集合开始，所以另外六位清 0）
                mode = 0
                if readable:
                    mode |= stat.S_IRUSR
                if writable:
                    mode |= stat.S_IWUSR
                if executable:
                    mode |= stat.S_IXUSR
                os.chmod(file_path, mode)
            else:
                # Windows：Java 退到 File.setReadable/setWritable/setExecutable。
                # 只有"可写"这一位是真实生效的（只读属性），其余两位 Windows 上无对应语义。
                # 【OSError 不能吞】路径不存在/被占用时 os.chmod 会抛 FileNotFoundError/
                # PermissionError，原来 `except OSError: pass` 之后照样回"权限已修改"，
                # 模型据此以为改好了继续往下走（失败仍报成功）。这里如实报错。
                try:
                    os.chmod(file_path, stat.S_IREAD | (stat.S_IWRITE if writable else 0))
                except OSError as e:
                    return self.error(f"修改权限失败: {type(e).__name__}: {e}")

            return self.success(f"权限已修改: {path}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"修改权限失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_copy.py
# ========================================================================
"""`copy_file` —— 复制文件或目录到目标路径。

【契约来源】`core/plugin/tool/file/FileCopyTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。
"""


import shutil
from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileCopyTool(ToolPlugin):
    """文件复制工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.copy"

    @property
    def name(self) -> str:
        return "copy_file"

    @property
    def description(self) -> str:
        return "复制文件或目录到目标路径"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "源路径"},
                "target": {"type": "string", "description": "目标路径"},
            },
            "required": ["source", "target"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            # 参数别名：模型常写 src/from，只认 source 会白报一次"缺少必需参数"
            merged = dict(args)
            if "source" not in merged:
                for alias in ("src", "from", "path", "oldPath"):
                    if merged.get(alias) is not None:
                        merged["source"] = merged[alias]
                        break
            if "target" not in merged:
                for alias in ("dest", "destination", "to", "newPath"):
                    if merged.get(alias) is not None:
                        merged["target"] = merged[alias]
                        break

            source = self.resolve_path(self.get_required_string_arg(merged, "source"))
            target = self.resolve_path(self.get_required_string_arg(merged, "target"))

            source_path = Path(source)
            target_path = Path(target)

            if not source_path.exists():
                return self.error(f"源路径不存在: {source}")

            if source_path.is_dir():
                # 复制目录：目标目录先建出来，再逐个条目按相对路径铺过去
                target_path.mkdir(parents=True, exist_ok=True)
                for src in _walk(source_path):
                    dest = target_path / src.relative_to(source_path)
                    if src.is_dir():
                        dest.mkdir(parents=True, exist_ok=True)
                    else:
                        shutil.copyfile(src, dest)
            else:
                # 复制文件
                if target_path.parent != Path(""):
                    target_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source_path, target_path)

            return self.success(f"已复制: {source} -> {target}")

        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"复制失败: {e}")


def _walk(root: Path) -> list[Path]:
    """`Files.walk(root)`：先根自己，再逐层展开（含空目录，否则复制会漏掉它们）。"""
    out: list[Path] = [root]
    stack: list[Path] = [root]
    while stack:
        current = stack.pop()
        try:
            children = sorted(current.iterdir(), key=lambda p: str(p))
        except OSError:
            continue
        for child in children:
            out.append(child)
            try:
                if child.is_dir() and not child.is_symlink():
                    stack.append(child)
            except OSError:
                continue
    return out


# ========================================================================
# 原模块 lionbox/tools/file/file_delete.py
# ========================================================================
"""`delete_file` —— 删除指定路径的文件或空目录。

【契约来源】`core/plugin/tool/file/FileDeleteTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【三条实测出来的规矩，一条都不能少】
1. 不许删工作区根目录（或它的上级）—— 模型"清理"时会直接把工作区根删掉。
2. 路径本来就不存在 = 已经满足（删除的语义就是"删完它不在"），当成功回，别让它白跑一轮。
3. 要连内容一起删必须显式 `recursive=true`；否则只删空目录。
"""


import os
import shutil
from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileDeleteTool(ToolPlugin):
    """文件删除工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.delete"

    @property
    def name(self) -> str:
        return "delete_file"

    @property
    def description(self) -> str:
        return "删除指定路径的文件或空目录"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件或目录路径"},
                "recursive": {
                    "type": "boolean", "default": False,
                    "description": "删目录时是否连内容一起删（默认 false，只删空目录）",
                },
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            target = Path(path)

            # 【安全护栏】不许删工作区根目录（或它的上级）。
            # 实测：模型跑"把工具都用一遍，最后清理"时直接
            # delete_file(path=<工作区根>, recursive=true) —— 那是要删掉用户整个工作区。
            if self._is_workspace_root_or_above(target):
                return self.error(
                    f"拒绝删除当前工作区根目录: {path}"
                    f"。删这里的文件请指定具体子路径（例如 {path}\\\\某个文件.txt），"
                    "整体清理请用 execute_command 里明确写出要删的目录。")

            if not target.exists():
                # 【实测】模型清理自己建的东西时会重复删同一个路径（"确保它没了"），
                # 第二次必然 ❌"路径不存在"。不存在 = 已经满足，直接当成功回。
                return self.success(f"路径本来就不存在（无需删除）: {path}")

            if target.is_dir():
                # 【实测】模型想清掉整棵目录树时会撞上"目录不为空，无法删除"。
                # 给它一个 recursive 开关，显式要求才递归删。
                recursive = self.get_bool_arg(args, "recursive", False)
                if recursive:
                    # 【必须过人工审核】递归删目录是破坏性最强的一种删除。
                    # oldContent 给一句摘要，newContent=None 表示"删除"。
                    gate_dir = intercept(self.name, str(path), "目录及其全部内容（递归删除）", None)
                    if gate_dir is not None:
                        return gate_dir
                    _remove_tree(target)
                    if target.exists():
                        # Java 逐文件删在 Windows 上偶尔还是删不干净（只读/长路径/占用），
                        # 退回系统的 rmdir /s /q —— 它对只读和长路径都比逐个删宽。
                        if os.name == "nt" and _remove_with_cmd(target):
                            return self.success(f"已递归删除目录（走系统 rmdir）: {path}")
                        return self.error(
                            f"删除失败（部分内容删不掉，可能被占用或权限不足）: {path}"
                            "。可以改用 execute_command 跑 Remove-Item -Recurse -Force。")
                    return self.success(f"已递归删除目录: {path}")

                # 只删除空目录
                try:
                    if any(target.iterdir()):
                        return self.error(
                            f"目录不为空: {path}"
                            "（要连内容一起删就加 recursive=true；只是想删它里面的文件就先 "
                            "delete_file 那些文件）")
                except OSError:
                    pass
                gate = intercept(self.name, str(path),
                                 read_text_file(target) if target.is_file() else None, None)
                if gate is not None:
                    return gate
                target.rmdir()
            else:
                # 【必须过人工审核】普通文件删除原来也是直接落盘。
                gate_file = intercept(self.name, str(path), read_text_file(target), None)
                if gate_file is not None:
                    return gate_file
                target.unlink()

            return self.success(f"已删除: {path}")

        except OSError as e:
            return self.error(f"删除失败: {e}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"参数错误: {e}")

    def _is_workspace_root_or_above(self, target: Path) -> bool:
        """这个路径是不是当前工作区根目录（或它的上级）。

        【必须用 current_workspace()，不能用 self.workspace】`self.workspace` 是**构造期**
        钉死的（`load_all()` 没传工作区时退化成进程 CWD = 仓库根），而工作区是**按会话**
        绑定的；拿构造期那个当基准，这条护栏就形同虚设：

            实测 `_check_fix_round6.py` —— 会话工作区是 `...\\_lionfix6\\ws`，
            模型一句 `delete_directory(ws, recursive=true)` 把**整个工作区递归删光**，
            而护栏比较的是仓库根，判定"不是工作区根目录"，于是放行。
            紧接着套件去读 `ws\\note.txt` 直接 FileNotFoundError。

        这与 `resolve_path()` 用 `WorkspaceContext.resolve()` 是同一个道理（见 base.py）。
        """
        ws = self.current_workspace()
        if ws is None:
            return False
        try:
            root = Path(ws).resolve()
            resolved = target.resolve()
            return resolved == root or _is_ancestor(resolved, root)
        except OSError:
            return False


def _is_ancestor(candidate: Path, descendant: Path) -> bool:
    """candidate 是不是 descendant 的上级（Java: root.startsWith(t)）。"""
    try:
        return descendant.relative_to(candidate) != Path(".")
    except ValueError:
        return False


def _remove_tree(target: Path) -> None:
    """递归删目录树，尽量对齐 Java 那套"删不掉就清只读再删一次"。"""

    def on_error(func: Any, path: str, _exc: Any) -> None:
        try:
            os.chmod(path, 0o700)      # Windows 上 .git 里的对象/索引是只读的
            func(path)
        except OSError:
            pass

    shutil.rmtree(target, onerror=on_error)


def _remove_with_cmd(target: Path) -> bool:
    """Windows 上退回系统的 `rmdir /s /q`（对只读/长路径更宽）。"""
    code, _ = ToolPlugin.run_process(["cmd", "/c", "rmdir", "/s", "/q", str(target)], timeout=60)
    return code == 0 and not target.exists()


# ========================================================================
# 原模块 lionbox/tools/file/file_glob.py
# ========================================================================
"""`glob_files` —— 使用glob模式匹配文件路径。

【契约来源】`core/plugin/tool/file/FileGlobTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【两个实测行为】
1. `path` 可选：模型想"列出所有文件"时只给 pattern，以前直接报"缺少必需参数: path"。
   缺省就用当前工作区。
2. glob 是 **java.nio 的 PathMatcher 语义**，不是 Python 的 fnmatch：
   `**/*.java` 在 Java 里**匹配不到**根目录下的 `A.java`（实测），Python 的 fnmatch 匹配得到。
   差一个文件就会让结果对不上，所以走 `_common.glob_matches` 自己翻的正则。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolPlugin, ToolResult, tool


@tool
class FileGlobTool(ToolPlugin):
    """文件路径匹配工具（Glob）。"""

    minimal_mode = True          # Java: ToolCategory.FILE_SEARCH 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.glob"

    @property
    def name(self) -> str:
        return "glob_files"

    @property
    def description(self) -> str:
        return "使用glob模式匹配文件路径"

    @property
    def category(self) -> str:
        return "FILE_SEARCH"

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "搜索根目录（可选，默认当前工作区）"},
                "pattern": {"type": "string", "description": "glob模式，如 **/*.java"},
                "maxResults": {"type": "integer", "description": "最大结果数", "default": 100},
            },
            "required": ["pattern"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            # path 可选：实测模型想"列出所有文件"时只给 pattern（glob_files(pattern="*")），
            # 以前直接报"缺少必需参数: path"，白跑一轮。默认就用当前工作区。
            raw_path = self.get_string_arg(args, "path", "")
            if not raw_path.strip():
                raw_path = str(self.current_workspace() or ".")   # 当前会话的工作区，不是构造期那个
            path = self.resolve_path(raw_path)
            pattern = self.get_required_string_arg(args, "pattern")
            max_results = self.get_int_arg(args, "maxResults", 100)

            search_dir = Path(path)
            if not search_dir.exists():
                return self.error(f"路径不存在: {path}")

            results: list[str] = []
            # Java: Files.walk(searchDir, 10).filter(isRegularFile).filter(matcher)
            for candidate in walk_files(search_dir, 10):
                if len(results) >= max_results:
                    break
                try:
                    rel = candidate.relative_to(search_dir)
                except ValueError:
                    continue
                if not rel.parts:
                    continue
                # `**/*.java` 这类模式里写的是 `/`；Java 的 PathMatcher 也按 `/` 收，
                # 所以匹配用 POSIX 形式，返回给模型的仍是原生分隔符（与 Java 一致）。
                if glob_matches(pattern, rel.as_posix()):
                    results.append(str(rel))

            if not results:
                return self.success("未找到匹配文件")

            return self.success(
                f"找到 {len(results)} 个文件:\n" + "".join(f"{r}\n" for r in results))

        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"匹配失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_head_tail.py
# ========================================================================
"""`head_tail_file` —— 查看文件头部或尾部N行。

【契约来源】`core/plugin/tool/file/FileHeadTailTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【三个实测坑】
1. `mode` 缺省当 head（模型经常漏这个参数，直接报错会让它连错好几轮）。
2. `lines` < 1 要明确报错：原来 head 走 subList(0, -1)、tail 走 subList(size+1, size)，
   崩出来的是 "fromIndex > toIndex"，模型完全看不出是自己把行数写错了。
3. 传进来是目录时不给"头几行"，而是把目录条目当行列出来（模型通常正是想看这个）。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileHeadTailTool(ToolPlugin):
    """文件头尾查看工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.headtail"

    @property
    def name(self) -> str:
        return "head_tail_file"

    @property
    def description(self) -> str:
        return "查看文件头部或尾部N行"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "mode": {"type": "string", "description": "head 或 tail（默认 head）", "default": "head"},
                "lines": {"type": "integer", "description": "行数", "default": 10},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            file_path = Path(path)
            if not file_path.exists():
                return self.error(
                    f"文件不存在: {path}{similar_path_hint(str(path), self.current_workspace())}")

            # mode 缺省当 head；【必须归一化 + 校验取值】原来只判 `mode == "head"`，
            # 传 "Head"/"HEAD"/手滑写成 "heda" 全部落进 else → 不报错地返回**文件末尾**，
            # 与调用方"看开头"的意图正好相反（静默给错数据，比报错更难查）。
            mode = self.get_string_arg(args, "mode", "head")
            mode = (mode or "").strip().lower()
            if mode == "":
                mode = "head"
            if mode not in ("head", "tail"):
                return self.error(
                    f"mode 必须是 head 或 tail（当前: {mode}）。"
                    "例：mode=head 看开头、mode=tail 看结尾")
            lines = self.get_int_arg(args, "lines", 10)
            if lines < 1:
                return self.error(
                    f"行数必须是 >= 1 的整数（当前: lines={lines}）。"
                    "例：lines=10、mode=head 看前 10 行；lines=20、mode=tail 看后 20 行")

            if file_path.is_dir():
                # 目录没有"头几行"这回事，就把目录内容当前几行给它
                entries: list[str] = []
                for p in (sorted_children(file_path) or [])[:max(1, lines)]:
                    entries.append(("[DIR]  " if p.is_dir() else "[FILE] ") + p.name)
                if not entries:
                    entries.append("（空目录）")
                out = ["这是目录，不是文件；列的是它的条目:"]
                for i, entry in enumerate(entries):
                    out.append(f"{i + 1}: {entry}")
                return self.success("\n".join(out) + "\n")

            all_lines = read_text_lines(file_path)
            if mode == "head":
                result = all_lines[:min(lines, len(all_lines))]
            else:
                result = all_lines[max(0, len(all_lines) - lines):]

            return self.success("".join(
                f"{i + 1}: {line}\n" for i, line in enumerate(result)))

        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"读取失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_info.py
# ========================================================================
"""`file_info` —— 查看文件详细信息（大小、修改时间等）。

【契约来源】`core/plugin/tool/file/FileInfoTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【修改时间的格式】Java 是 `String.format("%s", FileTime)`，即 `FileTime.toString()` ——
ISO-8601 的 `yyyy-MM-ddTHH:mm:ss[.fffffffff]Z`，小数位数是 0/3/6/9 位（按精度截断）。
这里按同一格式手写（NTFS 是 100ns 精度 → JDK 取到纳秒 → 9 位小数），别用 Python 默认的
`datetime.__str__`（那是 `2024-01-15 10:30:45.123456`，中间是空格、没有 Z，对不上）。
"""


import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileInfoTool(ToolPlugin):
    """文件信息查看工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.info"

    @property
    def name(self) -> str:
        return "file_info"

    @property
    def description(self) -> str:
        return "查看文件详细信息（大小、修改时间等）"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            file_path = Path(path)
            if not file_path.exists():
                return self.error(f"路径不存在: {path}")

            stat = file_path.stat()
            size = stat.st_size
            is_dir = file_path.is_dir()

            return self.success(
                f"路径: {path}\n"
                f"类型: {'目录' if is_dir else '文件'}\n"
                f"大小: {size} 字节\n"
                f"最后修改: {_file_time(stat.st_mtime_ns)}\n"
                f"可读: {'true' if os.access(file_path, os.R_OK) else 'false'}\n"
                f"可写: {'true' if os.access(file_path, os.W_OK) else 'false'}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"获取文件信息失败: {e}")


def _file_time(mtime_ns: int) -> str:
    """`java.nio.file.attribute.FileTime.toString()` 的等价输出（UTC，ISO-8601）。

    【实测，别照文档猜】Windows/NTFS 上的输出是 `2026-10-03T11:50:31.68373Z` ——
    **5 位**小数，不是 ISO_INSTANT 文档里写的 3/6/9 位。JDK 是拿到多少纳秒就原样写多少
    （NTFS 的 100ns 精度 → 去掉末尾的 0 之后经常是 5 位或 7 位）。
    所以这里也按"原样、去尾零"输出，两边才对得上。
    """
    seconds, nanos = divmod(mtime_ns, 1_000_000_000)
    stamp = datetime.fromtimestamp(seconds, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S")
    if nanos == 0:
        return stamp + "Z"
    return f"{stamp}.{nanos:09d}".rstrip("0") + "Z"


# ========================================================================
# 原模块 lionbox/tools/file/file_line_count.py
# ========================================================================
"""`line_count` —— 统计文件行数。

【契约来源】`core/plugin/tool/file/FileLineCountTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【两个实测坑，一个都不能漏】
1. 传进来是目录时要去**遍历累加**（模型问的是"这个目录里一共多少行"），不是报错。
2. **二进制文件必须真的跳过**：Java 里原来的 `catch(Exception)` 是死代码 ——
   `readTextLines` 内部三级容错（UTF-8 严格 → GBK → 替换）永远不抛，
   于是 `.zip/.exe` 也会被当文本数进去，同一个目录里 line_count 报"总行数: 3"、
   word_count 报"行数: 2"，两个工具对同一个目录给出不同答案。
   这里复用 `looks_binary`（和 word_count 同一套判据）。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileLineCountTool(ToolPlugin):
    """文件行数统计工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.linecount"

    @property
    def name(self) -> str:
        return "line_count"

    @property
    def description(self) -> str:
        return "统计文件行数"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            target = Path(path)

            if target.is_dir():
                total = 0
                files = 0
                skipped = 0
                # 【统计不设层数上限】walk_files 的默认 10 层是给 file_glob/file_search
                # 对齐 Java `Files.walk(dir, 10)` 用的；"这个目录一共多少行"没有层数上限
                # （node_modules/.venv 深处的文件原来会被静默漏掉、少算还不吭声）。
                for candidate in walk_files(target, WALK_UNLIMITED_DEPTH):
                    try:
                        # 【二进制必须真的跳过】按字节判，不靠"解码抛不抛"（它永远不抛）
                        with candidate.open("rb") as fh:
                            head = fh.read(BINARY_SAMPLE_BYTES)
                        if looks_binary(head):
                            skipped += 1
                            continue
                        total += len(read_text_lines(candidate))
                        files += 1
                    except OSError:
                        # 读不了的文件跳过，不让一个坏文件废掉整次统计
                        skipped += 1
                out = (f"这是目录，已按**目录累计**统计: {path}"
                       f"\n文本文件数: {files}\n总行数: {total}")
                if skipped > 0:
                    out += f"\n（已跳过 {skipped} 个二进制/读不了的文件）"
                return self.success(out)

            if not target.exists():
                return self.error(f"文件不存在: {path}")

            # 【单文件也要判二进制】decode_text 三级容错永不抛，.zip/.exe/图片走到下面
            # 会按垃圾字节里的 \n 切出一堆"假行数"返回成功；同一个文件 word_count 会明说
            # "看着是二进制"，两个工具对同一个文件给出不同答案 —— 这里补齐同一套判据。
            with target.open("rb") as fh:
                head = fh.read(BINARY_SAMPLE_BYTES)
            if looks_binary(head):
                return self.success(
                    f"（{path} 看着是二进制（含 NUL 或大量控制字符），不统计行数；"
                    "要大小/类型用 file_info）")

            # 容错读：记事本存的 ANSI/GBK 中文文件按 UTF-8 严格解码会抛
            # MalformedInputException，word_count 早就容错读了，这里对齐。
            count = len(read_text_lines(target))
            return self.success(f"行数: {count}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"统计失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_list.py
# ========================================================================
"""`list_directory` —— 列出目录下的文件和子目录。

【契约来源】`core/plugin/tool/file/FileListTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【顺序】Java 的 `Files.list(dir)` 返回的是**目录流本身的顺序**（NTFS 上大致按名字，
但没有排序保证），`Files.walk` 同理 —— 所以这里不排序，照系统给的顺序输出，
免得和 Java 版逐行对比时顺序对不上。
"""


import os
from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileListTool(ToolPlugin):
    """目录列表工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.list"

    @property
    def name(self) -> str:
        return "list_directory"

    @property
    def description(self) -> str:
        return "列出目录下的文件和子目录"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "目录路径"},
                "recursive": {"type": "boolean", "description": "是否递归列出", "default": False},
                "maxDepth": {"type": "integer", "description": "最大递归深度", "default": 3},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            recursive = self.get_bool_arg(args, "recursive", False)
            max_depth = self.get_int_arg(args, "maxDepth", 3)

            dir_path = Path(path)
            if not dir_path.exists():
                return self.error(f"路径不存在: {path}")
            if not dir_path.is_dir():
                return self.error(f"不是目录: {path}")

            lines = [f"目录: {path}"]
            if recursive:
                # Java: Files.walk(dirPath, maxDepth) —— 含根自己，根显示成 "."
                for entry, rel in walk_entries(dir_path, max(0, max_depth)):
                    lines.append(("[DIR] " if entry.is_dir() else "[FILE] ") + rel)
            else:
                # Java: Files.list(dirPath) —— 只列直接子项
                try:
                    children = [Path(e.path) for e in os.scandir(dir_path)]
                except OSError as e:
                    return self.error(f"列出目录失败: {e}")
                for child in children:
                    lines.append(("[DIR] " if child.is_dir() else "[FILE] ") + child.name)

            return self.success("\n".join(lines) + "\n")

        except OSError as e:
            return self.error(f"列出目录失败: {e}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"参数错误: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_mkdir.py
# ========================================================================
"""`create_directory` —— 创建目录（含父目录）。

【契约来源】`core/plugin/tool/file/FileMkdirTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolPlugin, ToolResult, tool


@tool
class FileMkdirTool(ToolPlugin):
    """创建目录工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.mkdir"

    @property
    def name(self) -> str:
        return "create_directory"

    @property
    def description(self) -> str:
        return "创建目录（含父目录）"

    @property
    def category(self) -> str:
        return "FILE_OPERATION"

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "目录路径"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            Path(path).mkdir(parents=True, exist_ok=True)
            return self.success(f"目录已创建: {path}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"创建目录失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_modify.py
# ========================================================================
"""`modify_file` —— 修改文件内容，支持替换、插入、删除行。

【契约来源】`core/plugin/tool/file/FileModifyTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【为什么这么长】这里的每一条分支都是踩出来的：
- 文件不存在 + operation=create/write/new/touch → 直接建（模型会把它当 create_file 用）；
- 文件已存在 + create → 当整体覆盖（免得模型在 create/replace 之间来回试）；
- replace 优先按 `oldText` 原文替换（模型经常只给 content 不给行号）；
- 落盘必须用**文件原本的编码**和**原本的换行风格**：
  `Files.write(Path, Iterable, Charset)` 会逐行补 `System.lineSeparator()`，
  Windows 上就是 CRLF —— 一个 LF 文件只改一行也会被整篇转成 CRLF。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolPlugin, ToolResult, tool

_CREATE_OPS = ("create", "write", "new", "touch")


@tool
class FileModifyTool(ToolPlugin):
    """文件内容修改工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_MODIFY 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.modify"

    @property
    def name(self) -> str:
        return "modify_file"

    @property
    def description(self) -> str:
        return "修改文件内容，支持替换、插入、删除行"

    @property
    def category(self) -> str:
        return "FILE_MODIFY"

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "operation": {
                    "type": "string",
                    "description": "操作类型: replace / insert / delete / append（追加到末尾）"
                                   "/ create（新建或整体覆盖）",
                },
                "startLine": {"type": "integer", "description": "起始行号"},
                "endLine": {"type": "integer", "description": "结束行号（replace操作）"},
                "content": {"type": "string", "description": "新内容"},
                "oldText": {
                    "type": "string",
                    "description": "replace 用：要替换掉的原文（给了它就不用行号）",
                },
                "all": {
                    "type": "boolean",
                    "description": "replace 用：是否替换所有出现（默认只替换第一处）",
                },
            },
            "required": ["path", "operation"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            operation = self.get_required_string_arg(args, "operation")

            file_path = Path(path)
            operation_low = operation.strip().lower()

            if not file_path.exists():
                # 【实测】模型会把 modify_file 当"建文件"用（operation=create），
                # 以前只回一句"文件不存在"，白跑一轮。
                if operation_low in _CREATE_OPS:
                    if file_path.parent != Path(""):
                        file_path.parent.mkdir(parents=True, exist_ok=True)
                    gate = intercept(self.name, str(path), None, self.get_string_arg(args, "content", ""))
                    if gate is not None:
                        return gate
                    # Java 这里写死 StandardCharsets.UTF_8（不走 charsetOf）
                    file_path.write_bytes(
                        self.get_string_arg(args, "content", "").encode("utf-8", "replace"))
                    return self.success(
                        f"文件不存在，已按 create 语义新建: {path}"
                        "（新建文件也可以直接用 create_file；改已有文件用 replace/append）")
                return self.error(
                    f"文件不存在: {path}（想新建：operation=create 并带上 content，"
                    "或直接用 create_file / write_file）")

            lines = read_text_lines(file_path)
            # 留一份原文：审核要拿它和"改完之后"比对（lines 后面会被就地改）。
            # 用**真原文**（保留原分隔符与末尾换行），否则闸门里的 diff 看不到
            # "末尾换行被改掉"这类差异，人工审核等于白看。
            original_text = read_text_file(file_path)
            sep = detect_line_separator(original_text)
            had_trailing = original_text.endswith("\n")
            start_line = self.get_int_arg(args, "startLine", 0)
            content = self.get_string_arg(args, "content", "")

            if operation_low in _CREATE_OPS:
                # 【已存在文件 + 没传 content 时绝不能覆盖】get_string_arg 把缺失兜成 ""，
                # 直接写回就把整个文件清空了还回"已覆盖写入" —— touch/write/new 都会踩
                # （文件已存在时模型只是想"确认它在"，并不是要清空）。
                if args.get("content") is None:
                    if operation_low == "touch":
                        # 与 create_file 对已存在文件的口径一致：什么都没动，也如实说
                        return self.success(f"文件已存在，未做任何改动: {path}")
                    return self.error(
                        f"要覆盖已有文件必须带 content（要写进去的完整内容）：{path}。"
                        "不带 content 不会动这个文件；只想在末尾加内容用 operation=append")
                # 文件已经在了：create 没法"再建一次"，把它明确给的 content 当作整体覆盖
                gate = intercept(self.name, str(path), original_text, content)
                if gate is not None:
                    return gate
                write_text_preserving_charset(file_path, content)
                return self.success(f"文件已存在，已按 create 覆盖写入: {path}")

            if operation_low == "replace":
                # ① 给了 oldText 就按文本替换（最省事，也不用数行号）
                old_text = self.get_string_arg(args, "oldText", "")
                if old_text:
                    full = "\n".join(lines)
                    if old_text not in full:
                        return self.error(
                            "要替换的原文没找到（oldText 要和文件里一字不差，"
                            f"先用 read_file 看一眼）：{old_text[:min(60, len(old_text))]}")
                    replace_all = self.get_bool_arg(args, "all", False)
                    replaced = (full.replace(old_text, content) if replace_all
                                else full.replace(old_text, content, 1))
                    # full 是 LF 形式：写回时要转回原分隔符并补回末尾换行
                    new_text = _to_file_text(replaced, sep, had_trailing)
                    gate = intercept(self.name, str(path), original_text, new_text)
                    if gate is not None:
                        return gate
                    write_text_preserving_charset(file_path, new_text)
                    times = _count_occurrences(full, old_text) if replace_all else 1
                    return self.success(f"已替换 {times} 处（按原文匹配）：{path}")

                # ② 没给 oldText 就得给行号；这里把话说清楚，别只回一句"行号超出范围: 0"
                if start_line < 1:
                    return self.error(
                        "replace 需要行号或原文：给 startLine（可加 endLine），"
                        "或者给 oldText + content 让我按原文替换")
                end_line = self.get_int_arg(args, "endLine", start_line)
                if start_line > len(lines):
                    return self.error(
                        f"起始行号超出范围: {start_line}（这个文件只有 {len(lines)} 行）")
                end_line = min(end_line, len(lines))
                # 替换指定行范围（倒着删）
                for i in range(end_line, start_line - 1, -1):
                    del lines[i - 1]
                for offset, new_line in enumerate(content.split("\n")):
                    lines.insert(start_line - 1 + offset, new_line)

            elif operation_low == "insert":
                if start_line < 1:
                    return self.error(
                        f"insert 需要在第几行插入：给 startLine（1 = 文件开头，"
                        f"{len(lines) + 1} = 文件末尾）")
                if start_line > len(lines) + 1:
                    return self.error(
                        f"插入位置超出范围: {start_line} (有效范围: 1-{len(lines) + 1})")
                for offset, new_line in enumerate(content.split("\n")):
                    lines.insert(start_line - 1 + offset, new_line)

            elif operation_low == "delete":
                if start_line < 1 or start_line > len(lines):
                    return self.error(
                        f"行号超出范围: {start_line}（这个文件只有 {len(lines)} 行）")
                end_line = self.get_int_arg(args, "endLine", start_line)
                if end_line < start_line:
                    # 反过来 range 会是空的：一行都不删却照样回"文件已修改"（空操作报成功）
                    return self.error(
                        f"endLine({end_line}) 不能小于 startLine({start_line})，"
                        "一行都没删（不谎报成功）")
                # 【必须夹取，和 replace 分支一样】模型常写 endLine=9999 表示"删到末尾"，
                # 不夹就 `del lines[9998]` 抛 IndexError → 整个删除失败、报"参数错误"
                end_line = min(end_line, len(lines))
                for i in range(end_line, start_line - 1, -1):
                    del lines[i - 1]

            elif operation_low == "append":
                # 实测模型会写 operation=append，以前只回"未知操作类型: append"，白跑一轮
                if args.get("content") is None:
                    return self.error("append 操作需要 content 参数（要追加的内容）")
                # 【直接拼在原文末尾】原来走 lines.append("") + sep.join：每追加一次都凭空
                # 多一个空行（"a\nb\n" 追加 "c" → "a\nb\n\nc"），与 append_file
                # （直接写字节、不加分隔行）也对不上。追加就是字节接字节。
                appended = original_text + str(args.get("content"))
                gate = intercept(self.name, str(path), original_text, appended)
                if gate is not None:
                    return gate
                write_text_preserving_charset(file_path, appended)
                return self.success(f"文件已修改: {path} (操作: {operation})")

            else:
                return self.error(
                    f"未知操作类型: {operation}"
                    "。支持 replace / insert / delete / append（想直接追加也可以用 append_file）")

            # 【末尾换行必须补回来】read_text_lines 会把末尾那个空串 pop 掉，
            # 只 join 不补的话，以换行结尾的文件被任意改一次就永久丢掉末尾换行
            # （git 会显示 "\ No newline at end of file"）。
            new_text = _to_file_text("\n".join(lines), sep, had_trailing)
            gate = intercept(self.name, str(path), original_text, new_text)
            if gate is not None:
                return gate
            # 按文件原本的编码 + 原本的换行风格写回
            write_text_preserving_charset(file_path, new_text)
            return self.success(f"文件已修改: {path} (操作: {operation})")

        except OSError as e:
            return self.error(f"修改文件失败: {e}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"参数错误: {e}")


def _count_occurrences(haystack: str, needle: str) -> int:
    """按原文替换时数一下替换了几处（Java: `countOccurrences`，非重叠计数）。"""
    if not needle:
        return 0
    n = 0
    i = haystack.find(needle)
    while i >= 0:
        n += 1
        i = haystack.find(needle, i + len(needle))
    return n


def _to_file_text(lf_text: str, sep: str, had_trailing: bool) -> str:
    """把 **LF 形式**的正文转回文件原本的分隔符，并按原样补回末尾换行。

    【两件事都不能省】
    1. `read_text_lines` 把 `\\r` 剥掉、末尾空串 pop 掉了，只 join 写回会把 CRLF 文件
       变成 LF、以换行结尾的文件丢掉那个换行（git 直接显示 "\\ No newline at end of file"）；
    2. 删光所有行时空串不能补换行 —— 那会写出一个只含一个换行的"非空文件"。
    """
    text = lf_text.replace("\r\n", "\n").replace("\n", sep)
    if had_trailing and text and not text.endswith("\n"):
        text += sep
    return text


def _read_lines_with_encoding(path: Path, encoding: str) -> list[str]:
    """按调用方声明的 encoding 严格解行；没声明/不认识/解不开就退回容错读。

    【为什么要有这条退路】read_file 的 encoding 参数是"模型的声明"，不是文件的事实：
    声明错了（或文件其实不是那个编码）时，硬按声明解会把整个文件读成乱码/抛异常 ——
    那比"没生效"更糟。所以严格解码成功才用它，LookupError/UnicodeDecodeError 都退回
    decode_text 的三级容错（UTF-8 → GBK → 替换），最差也和没有这个参数时一样。
    """
    name = (encoding or "").strip().lower().replace("_", "-")
    if name in ("", "utf-8", "utf8"):
        return read_text_lines(path)          # 默认口径，别为它多读一遍文件
    try:
        text = path.read_bytes().decode(name)
    except (LookupError, UnicodeDecodeError):
        return read_text_lines(path)
    text = _strip_leading_bom(text)
    lines = text.split("\n")
    lines = [ln[:-1] if ln.endswith("\r") else ln for ln in lines]
    if lines and lines[-1] == "":
        lines.pop()
    return lines


# ========================================================================
# 原模块 lionbox/tools/file/file_move.py
# ========================================================================
"""`move_file` —— 移动或重命名文件/目录。

【契约来源】`core/plugin/tool/file/FileMoveTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。
"""


import errno
import shutil
from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileMoveTool(ToolPlugin):
    """文件移动/重命名工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.move"

    @property
    def name(self) -> str:
        return "move_file"

    @property
    def description(self) -> str:
        return "移动或重命名文件/目录"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "source": {"type": "string", "description": "源路径"},
                "target": {"type": "string", "description": "目标路径"},
            },
            "required": ["source", "target"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            # 参数别名：模型常写 src/from，只认 source 会白报一次"缺少必需参数"
            merged = dict(args)
            if "source" not in merged:
                for alias in ("src", "from", "path", "oldPath"):
                    if merged.get(alias) is not None:
                        merged["source"] = merged[alias]
                        break
            if "target" not in merged:
                for alias in ("dest", "destination", "to", "newPath"):
                    if merged.get(alias) is not None:
                        merged["target"] = merged[alias]
                        break

            source = self.resolve_path(self.get_required_string_arg(merged, "source"))
            target = self.resolve_path(self.get_required_string_arg(merged, "target"))

            source_path = Path(source)
            target_path = Path(target)

            if not source_path.exists():
                return self.error(f"源路径不存在: {source}")

            if target_path.parent != Path(""):
                target_path.parent.mkdir(parents=True, exist_ok=True)

            # 【目标已存在且是目录时必须先说清楚】os.replace 对"目标是目录"必然失败，
            # 退到 shutil.move 的语义是"搬进目录里"（真实落点是 target/<源文件名>），
            # 而返回文案照旧写 "source -> target" —— 调用方按文案去找文件会找不到。
            # Java 的 REPLACE_EXISTING 此时抛 DirectoryNotEmptyException 直接报错，这里对齐：
            # 先拒绝，把真实落点告诉调用方，别先斩后奏。
            if target_path.is_dir():
                return self.error(
                    f"目标已存在且是目录: {target}"
                    f"（要移动到目录里就写完整落点 {target.rstrip('/\\') + os.sep + source_path.name}；"
                    "或者把 target 写成一个文件名）")

            # Java: Files.move(source, target, REPLACE_EXISTING) —— 同盘是原子改名，
            # 目标已存在就替换（目录被替换时要求它为空，非空会报 DirectoryNotEmptyException）。
            # Python 的 os.replace 语义一致；**只有跨盘（EXDEV）**才退到 shutil.move ——
            # 其它失败（权限、目标是目录、被占用）原来也无脑兜底，会把"没搬成"报成"已移动"。
            try:
                source_path.replace(target_path)
            except OSError as e:
                cross_device = (getattr(e, "errno", None) == errno.EXDEV
                                or getattr(e, "winerror", None) == 17)   # ERROR_NOT_SAME_DEVICE
                if not cross_device:
                    raise
                shutil.move(str(source_path), str(target_path))

            return self.success(f"已移动: {source} -> {target}")

        except OSError as e:
            return self.error(f"移动失败: {e}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"参数错误: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_read.py
# ========================================================================
"""`read_file` —— 读取指定路径的文件内容。

【契约来源】`core/plugin/tool/file/FileReadTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**（用编译产物核对过）。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileReadTool(ToolPlugin):
    """读取指定路径的文件内容，支持文本文件和二进制文件信息。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.read"

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "读取指定路径的文件内容"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "encoding": {"type": "string", "description": "文件编码", "default": "UTF-8"},
                "offset": {"type": "integer", "description": "起始行号（从1开始）", "default": 1},
                "limit": {"type": "integer", "description": "读取行数限制", "default": 1000},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            offset = self.get_int_arg(args, "offset", 1)
            limit = self.get_int_arg(args, "limit", 1000)
            # schema 里声明了 encoding（还带 default），execute 却从头到尾没读过它 ——
            # 模型传 encoding="utf-16"/"gb18030" 会被静默忽略，读出来的内容和它声明的
            # 编码毫无关系。这里真的按它解一次（解不开再退回三级容错，别把读文件变硬失败）。
            encoding = self.get_string_arg(args, "encoding", "") or ""

            file_path = Path(path)
            if not file_path.exists():
                return self.error(f"文件不存在: {path}{similar_path_hint(str(path), self.current_workspace())}")

            if file_path.is_dir():
                # 【实测】模型常把目录当文件读，原来回 ❌"不是普通文件"，它得再跑一轮。
                # 直接把目录列出来，等于这一轮就把事办了。
                out = [f"这是目录，不是文件；下面是它的内容: {path}"]
                names = (sorted_children(file_path) or [])[:200]
                for p in names:
                    out.append(("[DIR]  " if p.is_dir() else "[FILE] ") + p.name)
                if not names:
                    out.append("（空目录）")
                out.append("（要看某个文件就 read_file 它的完整路径；看整棵树用 directory_tree）")
                return self.success("\n".join(out) + "\n")

            if not file_path.is_file():
                return self.error(f"不是普通文件: {path}（可能是设备/管道文件）")

            lines = _read_lines_with_encoding(file_path, encoding)
            if limit < 1:
                # limit 传 0 或者负数时，下面一行都取不到，然后会掉进"（空文件）"的兜底 ——
                # 一个非空文件被说成空的，模型会据此判断"文件是空的"。
                return self.error(
                    f"limit 必须是 >= 1 的整数（当前: {limit}）；不传就是默认 1000 行")

            start = max(0, offset - 1)
            # 【实测】原来是 int end = Math.min(lines.size(), start + limit)：
            # 超大数字（"9999999999"）会让 start + limit 溢出成负数，于是 end < start、
            # 一个非空文件被报成"（空文件）"。Python 没有整数溢出，夹一下就行。
            end = min(len(lines), start + limit)

            parts = [f"{i + 1:>4} | {lines[i]}\n" for i in range(start, end)]
            result = "".join(parts)
            if not result:
                # 【同上的症状】原文案一律说"（空文件）"：offset 超出行数（或者文件真为空）
                # 都这么说，模型分不清"文件是空的"和"我要的那一段没有"。分开报。
                result = "（空文件）" if not lines else (
                    f"（文件不是空的：共 {len(lines)} 行，但 offset={offset} 起没有内容了；"
                    "把 offset 调小再读）")
            return self.success(result)

        except OSError as e:
            return self.error(f"读取文件失败: {e}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"参数错误: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_search.py
# ========================================================================
"""`search_in_files` —— 在文件中搜索文本或正则表达式。

【契约来源】`core/plugin/tool/file/FileSearchTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【三处必须对齐 Java 的细节】
1. 文本模式是**不区分大小写**的（`Pattern.quote(pattern), CASE_INSENSITIVE`），
   正则模式是区分大小写的。别自作主张给两边都加 flag。
2. Java 的 `CASE_INSENSITIVE` 默认只折 ASCII（要 `UNICODE_CASE` 才折 Unicode），
   所以这里用 `re.ASCII | re.IGNORECASE`；只用 `re.IGNORECASE` 会把 `CAFÉ` 也匹配上。
3. 结果行 `.trim()` 过 —— Java 的 `String.trim()` 只去 <= U+0020，见 `_common.java_trim`。
"""


import re
from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolPlugin, ToolResult, tool


@tool
class FileSearchTool(ToolPlugin):
    """文件内容搜索工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_SEARCH 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.search"

    @property
    def name(self) -> str:
        return "search_in_files"

    @property
    def description(self) -> str:
        return "在文件中搜索文本或正则表达式"

    @property
    def category(self) -> str:
        return "FILE_SEARCH"

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "搜索目录"},
                "pattern": {"type": "string", "description": "搜索模式（文本或正则）"},
                "filePattern": {"type": "string", "description": "文件名匹配模式", "default": "*"},
                "useRegex": {"type": "boolean", "description": "是否使用正则表达式", "default": False},
                "maxResults": {"type": "integer", "description": "最大结果数", "default": 50},
            },
            "required": ["path", "pattern"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            pattern = self.get_required_string_arg(args, "pattern")
            file_pattern = self.get_string_arg(args, "filePattern", "*")
            use_regex = self.get_bool_arg(args, "useRegex", False)
            max_results = self.get_int_arg(args, "maxResults", 50)

            search_dir = Path(path)
            if not search_dir.exists():
                return self.error(f"路径不存在: {path}")

            search_re = (re.compile(pattern) if use_regex
                         else re.compile(re.escape(pattern), re.IGNORECASE | re.ASCII))

            results: list[str] = []
            for candidate in walk_files(search_dir, 10):
                if len(results) >= max_results:
                    break
                if not glob_matches(file_pattern, candidate.name):
                    continue
                try:
                    lines = read_text_lines(candidate)
                except OSError:
                    continue
                try:
                    relative = str(candidate.relative_to(search_dir))
                except ValueError:
                    continue
                for i, line in enumerate(lines):
                    if search_re.search(line):
                        results.append(f"{relative}:{i + 1}: {java_trim(line)}")
                        if len(results) >= max_results:
                            break

            if not results:
                return self.success("未找到匹配结果")

            return self.success(
                f"找到 {len(results)} 个匹配:\n" + "".join(f"{r}\n" for r in results))

        except re.error as e:
            return self.error(f"搜索失败: {e}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"搜索失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_touch.py
# ========================================================================
"""`create_file` —— 创建空文件。

【契约来源】`core/plugin/tool/file/FileTouchTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【存在性判断必须排在 intercept 之前】原来的顺序是"先 intercept(…, "") 登记待审改动，
再 createFile"：文件已存在时 createFile 抛 FileAlreadyExistsException，被 catch 成
"文件已存在"回给模型 —— 但那条 newContent="" 的待审改动**已经登记了**。
用户点「通过并写入」时 ChangeReview 会把空串写进去，**原文件内容被清空**。
这是默认路径（人工审核默认开启）上的数据丢失，所以这里的顺序不能动。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileTouchTool(ToolPlugin):
    """创建空文件工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.touch"

    @property
    def name(self) -> str:
        return "create_file"

    @property
    def description(self) -> str:
        return "创建空文件"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            file_path = Path(path)

            # 【判断存在必须排在 intercept 之前】见模块 docstring：顺序反了会清空原文件
            if file_path.exists():
                return self.success(f"文件已存在，未做任何改动: {path}")

            if file_path.parent != Path(""):
                file_path.parent.mkdir(parents=True, exist_ok=True)
            gate = intercept(self.name, str(path), None, "")
            if gate is not None:
                return gate
            # Java: Files.createFile —— 存在就抛 FileAlreadyExistsException
            file_path.touch(exist_ok=False)
            return self.success(f"文件已创建: {path}")
        except FileExistsError:
            return self.success(f"文件已存在: {args.get('path')}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"创建文件失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/file/file_tree.py
# ========================================================================
"""`directory_tree` —— 以树形结构展示目录。

【契约来源】`core/plugin/tool/file/FileTreeTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【递归语义】Java 是 `depth <= 0 就 return`，每进一层目录 depth-1：
所以 maxDepth=3 时能看到"根 → 子 → 孙"这一层的目录名，但孙目录里面不再展开。
目录名后面补 `/`；连线用 `├── ` / `└── `，缩进用 `│   ` / `    `（都是 4 字符宽）。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class FileTreeTool(ToolPlugin):
    """目录树工具。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.tree"

    @property
    def name(self) -> str:
        return "directory_tree"

    @property
    def description(self) -> str:
        return "以树形结构展示目录"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "目录路径"},
                "maxDepth": {"type": "integer", "description": "最大深度", "default": 3},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            max_depth = self.get_int_arg(args, "maxDepth", 3)
            parts: list[str] = []
            _build_tree(Path(path), "", max_depth, parts)
            return self.success("".join(parts))
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"生成目录树失败: {e}")


def _build_tree(directory: Path, prefix: str, depth: int, out: list[str]) -> None:
    if depth <= 0:
        return
    entries = sorted_children(directory)
    if entries is None:
        return
    for i, entry in enumerate(entries):
        is_last = i == len(entries) - 1
        out.append(prefix + ("└── " if is_last else "├── ") + entry.name)
        if entry.is_dir():
            out.append("/\n")
            _build_tree(entry, prefix + ("    " if is_last else "│   "), depth - 1, out)
        else:
            out.append("\n")


# ========================================================================
# 原模块 lionbox/tools/file/file_wc.py
# ========================================================================
"""`word_count` —— 统计文件行数、字数、字节数。

【契约来源】`core/plugin/tool/file/FileWcTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【修掉的两个毛病，别改回去】
1. **行数和 line_count 必须一致**：原来用 `content.chars().filter(c=='\n').count() + 1`，
   空文件算 1 行、以换行结尾的文件比 line_count 多 1 行；`"".split("\\s+").length`
   又把空文件算成 1 个词。同一个文件两个工具给出不同答案。
   现在行数复用 `read_text_lines`，字数用 `count_words`（空/纯空白 = **0** 个词）。
2. **二进制判断不能是死代码**：原注释说"不是合法文本时 readTextFile 会抛"，
   但 `decode_text` 是三级容错的（UTF-8 → GBK → 替换），**它不会抛**，
   那个 catch 永远进不去 —— 图片、exe 也会被统计出一个"看着挺正常"的假行数。
   现在按字节真判（`looks_binary`）。

【目录】传进来是目录就去遍历累加：能解码成文本的文件把行数/字数加上，
二进制文件**只算字节**（原来它会给总数添上一堆凭空的"1 行 1 词"）。
"""


import re
from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

# Java 的 `String.split("\\s+")` 里 `\s` 只认 ASCII 空白（[ \t\n\x0B\f\r]），
# Python 默认的 `\s` 还认 U+3000/NBSP 这些 Unicode 空白 —— 差一个全角空格结论就不同。
_WHITESPACE_SPLIT = re.compile(r"\s+", re.ASCII)


def count_words(content: str | None) -> int:
    """按空白切词；空文件/纯空白是 **0** 个词（`"".split(...)` 得到 1，那是错的）。"""
    text = java_trim(content or "")
    return 0 if not text else len(_WHITESPACE_SPLIT.split(text))


@tool
class FileWcTool(ToolPlugin):
    """文件统计工具（行数、字数、字节数）。"""

    minimal_mode = True          # Java: ToolCategory.FILE_OPERATION 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.wc"

    @property
    def name(self) -> str:
        return "word_count"

    @property
    def description(self) -> str:
        return "统计文件行数、字数、字节数"

    @property
    def category(self) -> str:
        return ToolCategory.FILE_OPERATION

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            target = Path(path)

            # 实测：模型把目录当文件传进来，原来只回"统计失败: <路径>"（异常 message 是空的），
            # 等于什么都没说。它想要的就是"这个目录里有多少东西"，那就真的去数。
            if target.is_dir():
                return self.success(_directory_stats(target))

            if not target.exists():
                return self.error(f"文件不存在: {path}")

            raw = target.read_bytes()
            size = len(raw)
            if looks_binary(raw):
                # 【这是原来的死代码位置】现在按字节真判：二进制就说清楚，不编数字。
                return self.success(
                    f"字节数: {size}\n（这个文件看着是二进制（含 NUL 或大量控制字符），"
                    "行数/字数没法准确统计；可以 file_info 看类型，或 read_file 看前面一段）")

            # 【和 line_count 对齐】同一个文件两个工具的答案必须一样
            lines = len(read_text_lines(target))
            words = count_words(decode_text(raw))
            return self.success(f"行数: {lines}\n字数: {words}\n字节数: {size}")

        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"统计失败: {e}")


def _directory_stats(directory: Path) -> str:
    """目录累计统计：把能解码成文本的文件一个个加起来（二进制文件只算字节）。"""
    files = 0
    lines = 0
    words = 0
    size = 0
    binary = 0
    # 与 line_count 的目录分支同口径：统计不设层数上限（默认 10 层会静默漏数深处的文件）
    for candidate in walk_files(directory, WALK_UNLIMITED_DEPTH):
        try:
            raw = candidate.read_bytes()
            size += len(raw)
            files += 1
            if looks_binary(raw):
                # 二进制只算字节：原来它会掉进 readTextFile 的"假成功"里
                binary += 1
                continue
            # 行数用 read_text_lines（和 line_count 同一套语义），字数用 count_words
            lines += len(read_text_lines(candidate))
            words += count_words(decode_text(raw))
        except OSError:
            binary += 1
    out = (f"这是目录，已按**目录累计**统计: {directory}\n"
           f"文件数: {files}\n行数: {lines}\n字数: {words}\n字节数: {size}")
    if binary > 0:
        out += f"\n（其中 {binary} 个是二进制/读不出来，只算了字节数）"
    return out


# ========================================================================
# 原模块 lionbox/tools/file/file_write.py
# ========================================================================
"""`write_file` —— 创建或覆盖写入指定路径的文件内容。

【契约来源】`core/plugin/tool/file/FileWriteTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import ToolPlugin, ToolResult, tool


@tool
class FileWriteTool(ToolPlugin):
    """创建或覆盖写入指定路径的文件内容。"""

    minimal_mode = True          # Java: ToolCategory.FILE_MODIFY 在 MINIMAL 下开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.file.write"

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return "创建或覆盖写入指定路径的文件内容"

    @property
    def category(self) -> str:
        return "FILE_MODIFY"

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "文件路径"},
                "content": {"type": "string", "description": "文件内容"},
            },
            "required": ["path", "content"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            content = self.get_required_string_arg(args, "content")

            file_path = Path(path)
            # 人工审核（开着的话）：先把改动登记成待审，别落盘
            gate = intercept(self.name, str(path),
                             read_text_file(file_path) if file_path.is_file() else None,
                             content)
            if gate is not None:
                return gate

            # 自动创建父目录
            if file_path.parent != Path(""):
                file_path.parent.mkdir(parents=True, exist_ok=True)

            # 覆盖已有文件时保留它原来的编码（新文件用 UTF-8）。
            # 【回显必须是真实写字节数】len(content) 是**字符数**：中文在 utf-8 下 3 字节/
            # 字符、gbk 下 2 字节/字符，拿它当"字节数"报，调用方拿 file_info 的 st_size
            # 一并对账永远对不上。
            data = content.encode(charset_of(file_path), "replace")
            file_path.write_bytes(data)
            return self.success(f"文件已写入: {path} ({len(data)}字节)")

        except OSError as e:
            return self.error(f"写入文件失败: {e}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"参数错误: {e}")


# ========================================================================
# 原模块 lionbox/tools/file.py
# ========================================================================
"""file 工具包（18 个，与 Java 的 `core/plugin/tool/file` 包一一对应）。

显式登记：每个模块在自己的 `@tool` 装饰器里登记工具类，`__init__` 只做"按名字导入"，
不做目录扫描（见 PORTING.md 一.3：扫描会拖慢启动且顺序不确定）。

  - `FileAppendTool`     append_file         向文件末尾追加内容
  - `FileChmodTool`      change_permissions  修改文件权限
  - `FileCopyTool`       copy_file           复制文件或目录到目标路径
  - `FileDeleteTool`     delete_file         删除指定路径的文件或空目录
  - `FileGlobTool`       glob_files          使用glob模式匹配文件路径
  - `FileHeadTailTool`   head_tail_file      查看文件头部或尾部N行
  - `FileInfoTool`       file_info           查看文件详细信息（大小、修改时间等）
  - `FileLineCountTool`  line_count          统计文件行数
  - `FileListTool`       list_directory      列出目录下的文件和子目录
  - `FileMkdirTool`      create_directory    创建目录（含父目录）
  - `FileModifyTool`     modify_file         修改文件内容，支持替换、插入、删除行
  - `FileMoveTool`       move_file           移动或重命名文件/目录
  - `FileReadTool`       read_file           读取指定路径的文件内容
  - `FileSearchTool`     search_in_files     在文件中搜索文本或正则表达式
  - `FileTouchTool`      create_file         创建空文件
  - `FileTreeTool`       directory_tree      以树形结构展示目录
  - `FileWcTool`         word_count          统计文件行数、字数、字节数
  - `FileWriteTool`      write_file          创建或覆盖写入指定路径的文件内容

`_common.py` 是这批工具共用的底层助手（容错编解码 / 二进制判据 / 遍历 / glob），
`_gate.py` 是改动人工审核闸门的接线点 —— 两者都**不是工具**，所以没有 `@tool` 登记。
"""



__all__ = [
    "FileAppendTool",
    "FileChmodTool",
    "FileCopyTool",
    "FileDeleteTool",
    "FileGlobTool",
    "FileHeadTailTool",
    "FileInfoTool",
    "FileLineCountTool",
    "FileListTool",
    "FileMkdirTool",
    "FileModifyTool",
    "FileMoveTool",
    "FileReadTool",
    "FileSearchTool",
    "FileTouchTool",
    "FileTreeTool",
    "FileWcTool",
    "FileWriteTool",
]


# ========================================================================
# 原模块 lionbox/tools/context/context_prune.py
# ========================================================================
"""`context_prune` —— 裁剪本会话的上下文。

【契约来源】`core/plugin/tool/context/ContextPruneTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【语义】"保留后面这几条，前面的删掉"：唯一的必填参数是 `keep_last`，其余一律删。
裁剪是**真的删**（从会话历史里移除并落盘），不是只影响这一次请求。

【两个保护】
1. 不越过工具调用的配对边界（不会删掉 assistant(tool_calls) 却留下它的 tool 结果）；
2. 至少保留最近 `MIN_KEEP` 条，且永远不动系统提示。删掉哪几条会在返回值里列出来。

【接线】`ConversationHistory` 在 `lionbox.sessions` 里（P2 单元）。这里沿用 `_gate` / `ask_user`
那套**显式接线点**：`set_history(...)` 挂上；没挂就返回明确失败，不吞异常。
"""


from typing import Any, Protocol

from lionbox.plugins.base import ToolPlugin, ToolResult, tool

#: 最少保留几条：把最后两条（一般是"用户提问 + 模型回答"）删了就什么都记不住了
MIN_KEEP = 2


class PruneResult(Protocol):
    """`ConversationHistory.PruneResult` 的同形结构。"""

    @property
    def total(self) -> int: ...
    @property
    def removed(self) -> int: ...
    @property
    def kept(self) -> int: ...
    @property
    def preview(self) -> list[str]: ...


class History(Protocol):
    """`ConversationHistory` 的同形接口。"""

    def prune_history(self, session_id: str, keep: int, dry_run: bool) -> PruneResult: ...


HISTORY: History | None = None
"""当前挂上的会话历史；None = 还没接线。"""


def set_history(history: History | None) -> None:
    """挂上/摘掉会话历史。接线方在启动时调一次。"""
    global HISTORY
    HISTORY = history


@tool
class ContextPruneTool(ToolPlugin):
    """让 Agent 自己裁剪上下文的工具。"""

    minimal_mode = False         # Java: ToolCategory.OTHER 在 MINIMAL 下不开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.context.prune"

    @property
    def name(self) -> str:
        return "context_prune"

    @property
    def description(self) -> str:
        return ("裁剪本会话的上下文：保留最近 keep_last 条消息，把它之前的全部删掉（真删，落盘）。"
                "用在「前面的探查已经没用了、但上下文快满」的时候：比如方案已定，"
                "之前翻文件、试错的过程都可以扔。别拿它当压缩用 —— 塞不下时会自动压缩。"
                "想先看看会删掉什么，用 dry_run=true。")

    @property
    def category(self) -> str:
        return "OTHER"

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "keep_last": {
                    "type": "integer",
                    "description": f"保留最近几条消息（至少 {MIN_KEEP}），更早的全部删除",
                },
                "reason": {
                    "type": "string",
                    "description": "为什么这些可以删（一句话，记进日志）",
                },
                "dry_run": {
                    "type": "boolean",
                    "description": "true = 只报告会删掉什么，不真删（默认 false）",
                },
            },
            "required": ["keep_last"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            keep = self.get_int_arg(args, "keep_last", -1)
            if keep < MIN_KEEP:
                return self.error(
                    f"keep_last 至少是 {MIN_KEEP}（把最后两条也删了就什么都不记得了）")
            dry_run = self.get_bool_arg(args, "dry_run", False)
            reason = self.get_string_arg(args, "reason", "")
            session_id = _current_session_id()
            if not session_id:
                return self.error("拿不到当前会话 id，无法裁剪")
            if HISTORY is None:
                return self.error("会话历史还没接线（lionbox 里需要先 set_history）")

            result = HISTORY.prune_history(session_id, keep, dry_run)
            if result.total == 0:
                return self.success("这个会话还没有历史消息，没什么可裁剪的。")
            if result.removed == 0:
                return self.success(
                    f"当前只有 {result.total} 条消息，不需要裁剪"
                    f"（保留最近 {keep} 条时没有更早的可以删）。")

            out = [f"{'【试算】' if dry_run else ''}已裁剪 {result.removed} 条早期消息，"
                   f"保留最近 {result.kept} 条。\n", "删掉的是：\n"]
            for line in result.preview:
                out.append(f"  - {line}\n")
            if reason.strip():
                out.append(f"（理由：{reason}）")
            if dry_run:
                out.append("\n要真的删掉，把 dry_run 去掉再调一次。")
            return self.success("".join(out))
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"裁剪上下文失败: {e}")


def _current_session_id() -> str | None:
    """当前会话 id（Java: `SessionContext.get()`）。拿不到就返回 None。

    【原来的写法读错了地方】`from ...sessions import context as session_context` 拿到的是
    **模块对象**，而那个模块里只有类 `SessionContext`，没有模块级的 `get()` ——
    两次 getattr 全部落空、直接返回 None。结果是本工具永远报
    "拿不到当前会话 id"（`_check_context_review.py` 抓到的就是这个）。
    真实实现是 `lionbox.sessions.SessionContext`（与 AgentLoop 用的是同一份 thread-local）。
    """
    try:
        from lionbox.sessions import SessionContext
    except ImportError:
        return None
    try:
        value = SessionContext.get()
    except Exception:               # noqa: BLE001 - 会话模块没就绪时按"没有会话"处理
        return None
    text = "" if value is None else str(value).strip()
    return text or None


# ========================================================================
# 原模块 lionbox/tools/context/context_window.py
# ========================================================================
"""`context_window` —— 调整本会话的上下文窗口大小（token）。

【契约来源】`core/plugin/tool/context/ContextWindowTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【默认窗口 16K 是为了省预填充】本机模型 256K 全开时每一轮都要把整个前缀重算一遍。
但"够不够用"只有干活的模型自己知道，所以给它自己调的权力，而且**立刻生效**。

【接线】`ContextBudget` 在 `lionbox.agent` 里（P4 单元）。这里沿用 `_gate` 那套
**显式接线点**：`set_budget(...)` 挂上；没挂就返回明确失败，不吞异常。
"""


from typing import Any, Protocol

from lionbox.plugins.base import ToolPlugin, ToolResult, tool

#: 下限：再小连系统提示 + 工具定义都放不下，压缩会原地打转
MIN_TOKENS = 4096
#: 上限：本机模型原生 256K，但不允许一步开到顶（留出 75% 的余量给"下一轮还要追加"）
MAX_TOKENS = 196_608


class Budget(Protocol):
    """`ContextBudget` 的同形接口。"""

    def set(self, session_id: str | None, tokens: int) -> int: ...
    def default_limit(self) -> int: ...


BUDGET: Budget | None = None
"""当前挂上的上下文预算；None = 还没接线。"""


def set_budget(budget: Budget | None) -> None:
    """挂上/摘掉上下文预算。接线方在启动时调一次。"""
    global BUDGET
    BUDGET = budget


@tool
class ContextWindowTool(ToolPlugin):
    """让 Agent 自己调上下文窗口的工具。"""

    minimal_mode = False         # Java: ToolCategory.OTHER 在 MINIMAL 下不开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.context.window"

    @property
    def name(self) -> str:
        return "context_window"

    @property
    def description(self) -> str:
        return ("调整本会话的上下文窗口大小（token），立即生效。默认 16K。"
                "只有在 16K 真的装不下（比如要通读大文件、跨多个模块改代码）时才调大；"
                "任务做完必须调回 16384，否则每一轮都要多算预填充。"
                "tokens=0 表示不设限（用模型窗口的 75%）。")

    @property
    def category(self) -> str:
        return "OTHER"

    @property
    def permission(self) -> str:
        return "WORKSPACE_WRITE"

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "tokens": {
                    "type": "integer",
                    "description": "新的窗口大小（token）。16384 = 默认；调大用于大项目；0 = 不设限",
                },
                "reason": {
                    "type": "string",
                    "description": "为什么需要调（一句话，会记进日志，方便事后看这笔开销值不值）",
                },
            },
            "required": ["tokens"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            tokens = self.get_int_arg(args, "tokens", -1)
            if tokens < 0:
                return self.error("tokens 必须是 0 或正整数（0 = 不设限）")
            if tokens != 0 and tokens < MIN_TOKENS:
                return self.error(
                    f"太小了：窗口至少 {MIN_TOKENS} token，"
                    "再小连系统提示和工具定义都放不下，会陷入反复压缩。想省就用 16384。")
            if tokens > MAX_TOKENS:
                return self.error(
                    f"太大了：最多 {MAX_TOKENS} token（本机模型原生 256K，"
                    "但要留出余量给下一轮追加的内容）")
            if BUDGET is None:
                # 显式失败而不是假装成功：预算还没接线（见模块 docstring）
                return self.error("上下文预算还没接线（lionbox 里需要先 set_budget）")

            session_id = _current_session_id__tools_context_context_window()
            reason = self.get_string_arg(args, "reason", "")
            now = BUDGET.set(session_id, tokens)

            out = [f"上下文窗口已改为 {_describe(now)}，下一次模型调用就会用新窗口。"]
            if now == 0:
                out.append("（0 = 不设限，按模型窗口的 75% 走）")
            default_limit = BUDGET.default_limit()
            if now > default_limit and now != 0:
                out.append(
                    f"【别忘了】这件事做完就把窗口调回 {default_limit}"
                    f"（再调一次 context_window，tokens={default_limit}）"
                    "—— 窗口越大，每一轮的预填充越贵。")
            return self.success("".join(out))
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"调窗口失败: {e}")


def _describe(tokens: int) -> str:
    """Java 的 `describe`：整 KB 显示成 N K（N token），否则只报 token 数。"""
    if tokens == 0:
        return "不设限"
    if tokens % 1024 == 0:
        return f"{tokens // 1024}K（{tokens} token）"
    return f"{tokens} token"


def _current_session_id__tools_context_context_window() -> str | None:
    """当前会话 id（Java: `SessionContext.get()`）。拿不到就返回 None。

    【原来的写法读错了地方】`from ...sessions import context as session_context` 拿到的是
    **模块对象**，而那个模块里只有类 `SessionContext`，没有模块级的 `get()` ——
    两次 getattr 全部落空、直接返回 None。结果是本工具永远报
    "拿不到当前会话 id"（`_check_context_review.py` 抓到的就是这个）。
    真实实现是 `lionbox.sessions.SessionContext`（与 AgentLoop 用的是同一份 thread-local）。
    """
    try:
        from lionbox.sessions import SessionContext
    except ImportError:
        return None
    try:
        value = SessionContext.get()
    except Exception:               # noqa: BLE001 - 会话模块没就绪时按"没有会话"处理
        return None
    text = "" if value is None else str(value).strip()
    return text or None


# ========================================================================
# 原模块 lionbox/tools/context.py
# ========================================================================
"""context 工具包（2 个，与 Java 的 `core/plugin/tool/context` 包一一对应）。

显式登记：每个模块在自己的 `@tool` 装饰器里登记工具类，`__init__` 只做"按名字导入"，
不做目录扫描（见 PORTING.md 一.3）。

  - `ContextPruneTool`   context_prune   裁剪本会话的上下文（真删、落盘）
  - `ContextWindowTool`  context_window  调整本会话的上下文窗口大小（token）

两个的 `ToolCategory` 都是 `OTHER`，极简模式下不开放；`getRequiredPermission()`
都是 `WORKSPACE_WRITE`（会动会话数据，不是只读）。

两者都需要接线：`context_prune` 要会话历史（`set_history`），
`context_window` 要上下文预算（`set_budget`）—— 没接线时如实返回失败，不假装成功。
"""



__all__ = [
    "ContextPruneTool",
    "ContextWindowTool",
]


# ========================================================================
# 原模块 lionbox/tools/code/base64.py
# ========================================================================
"""Base64 编解码工具（对应 Java `core/plugin/tool/code/Base64Tool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False —— Java 里类别是 OTHER，极简模式不开放。

【实测过的行为，照抄】
1. 编解码写死 UTF-8。Java 侧原来用平台默认编码，启动参数带 `-Dfile.encoding=GBK`
   时"中文"编出来的 base64 跟标准工具/别的机器完全不一样，用户拿去解码是乱码。
2. 失败一律返回 `ToolResult.fail("Base64处理失败: …")`，不抛异常出去（Java 的 catch 包住整段，
   连"缺少必需参数"也走这个前缀）。
3. 解码得到的字节按 UTF-8 **容错**解码：Java 的 `new String(bytes, UTF_8)` 遇到非法序列
   替换成 U+FFFD 而不报错，Python 的 bytes.decode 默认会抛，所以这里用 errors="replace"。

【扩展（不改变上面任何行为）】除 Java 的 input/action 外，额外认 `file`：给了 file 就读文件
字节（对齐"编码工具要支持文本或文件两种输入"）。不传 file 时与 Java 完全一致。
"""


import base64 as _base64
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class Base64Tool(ToolPlugin):
    """Base64编码/解码"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.base64"

    @property
    def name(self) -> str:
        return "base64"

    @property
    def description(self) -> str:
        return "Base64编码/解码"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "输入内容"},
                "action": {"type": "string", "description": "encode/decode"},
            },
            "required": ["input", "action"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            action = self.get_required_string_arg(args, "action")
            file_arg = str(args.get("file") or args.get("path") or "").strip()
            if file_arg:
                return self._execute_file(action, file_arg)

            text = self.get_required_string_arg(args, "input")
            if action == "encode":
                return self.success(_base64.b64encode(text.encode("utf-8")).decode("ascii"))
            if action == "decode":
                return self.success(_decode_to_text(text))
            return self.error("未知操作: " + action)
        except Exception as e:      # 与 Java 一样，整段一个 catch：错误前缀统一
            return self.error("Base64处理失败: " + str(e))

    def _execute_file(self, action: str, file_arg: str) -> ToolResult:
        """扩展路径：以文件为输入（Java 没有这个分支，加了不影响原行为）。"""
        path = self.resolve_path(file_arg)
        if not path.is_file():
            return self.error("Base64处理失败: 文件不存在: " + str(path))
        data = path.read_bytes()
        if action == "encode":
            return self.success(_base64.b64encode(data).decode("ascii"))
        if action == "decode":
            return self.success(_decode_to_text(data.decode("ascii", errors="replace")))
        return self.error("未知操作: " + action)


def _decode_to_text(text: str) -> str:
    """标准 base64 解码 → UTF-8 容错文本。

    Java 用的是 `Base64.getDecoder()`（严格的标准字母表），Python 侧加 `validate=True`
    与之对齐：非法字符要报错，而不是被悄悄忽略。末尾填充按 Java 的行为补上 ——
    Java 的 decoder 接受**省略填充**的输入（"abc" 能解出 2 字节），Python 的 b64decode
    默认会报 "Incorrect padding"，不补就会"Java 成功、Python 失败"。
    """
    padded = text + "=" * (-len(text) % 4)
    raw = _base64.b64decode(padded, validate=True)
    return raw.decode("utf-8", errors="replace")


# ========================================================================
# 原模块 lionbox/tools/code/cron.py
# ========================================================================
"""Cron 表达式解析工具（对应 Java `core/plugin/tool/code/CronTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【行为对齐】Java 是 `expr.split("\\s+")` 后按"5 段还是 6 段"决定秒/分/时/日/月/周的位置，
不做语义校验（不判断 */5、MON-FRI 这类写法是否合法）。这里照抄同一套动作与输出文案，
连 `split` 的边界语义都对齐：Java 会丢掉末尾空串，这里也丢。
"""


import re
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class CronTool(ToolPlugin):
    """解析Cron表达式"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.cron"

    @property
    def name(self) -> str:
        return "cron_parse"

    @property
    def description(self) -> str:
        return "解析Cron表达式"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "expression": {"type": "string", "description": "Cron表达式"},
            },
            "required": ["expression"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            expr = self.get_required_string_arg(args, "expression")
        except ValueError as e:
            return self.error(str(e))

        parts = re.split(r"\s+", expr)
        while parts and parts[-1] == "":      # Java 的 split 丢末尾空串
            parts.pop()

        if len(parts) < 5 or len(parts) > 6:
            return self.error("无效的Cron表达式，需要5或6个字段")

        six = len(parts) > 5
        return self.success(
            f"Cron表达式: {expr}\n"
            f"秒: {parts[0] if six else '0'}\n"
            f"分: {parts[1] if six else parts[0]}\n"
            f"时: {parts[2] if six else parts[1]}\n"
            f"日: {parts[3] if six else parts[2]}\n"
            f"月: {parts[4] if six else parts[3]}\n"
            f"周: {parts[5] if six else parts[4]}")


# ========================================================================
# 原模块 lionbox/tools/code/diff.py
# ========================================================================
"""文本差异比较工具（对应 Java `core/plugin/tool/code/DiffTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【行为对齐】Java 是按行号**逐行对位**比较（不是 LCS diff）：
`String.split("\\n")` 会丢掉末尾的空串，所以这里也照 Java 的语义切行，
否则 "a\\n" 与 "a" 在 Java 里算"完全相同"、在 Python 里会被判成第 2 行不同。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class DiffTool(ToolPlugin):
    """比较两段文本的差异"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.diff"

    @property
    def name(self) -> str:
        return "diff_text"

    @property
    def description(self) -> str:
        return "比较两段文本的差异"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text1": {"type": "string", "description": "文本1"},
                "text2": {"type": "string", "description": "文本2"},
            },
            "required": ["text1", "text2"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            text1 = self.get_required_string_arg(args, "text1")
            text2 = self.get_required_string_arg(args, "text2")
        except ValueError as e:
            return self.error(str(e))

        lines1 = _java_split_lines(text1)
        lines2 = _java_split_lines(text2)

        out: list[str] = []
        for i in range(max(len(lines1), len(lines2))):
            l1 = lines1[i] if i < len(lines1) else ""
            l2 = lines2[i] if i < len(lines2) else ""
            if l1 != l2:
                out.append(f"行{i + 1}:\n  - {l1}\n  + {l2}\n")
        return self.success("".join(out) if out else "文本完全相同")


def _java_split_lines(text: str) -> list[str]:
    """Java `text.split("\\n")`：切分后**丢掉所有末尾空串**（"a\\n" → ["a"]）。"""
    parts = text.split("\n")
    while len(parts) > 1 and parts[-1] == "":
        parts.pop()
    return parts


# ========================================================================
# 原模块 lionbox/tools/code/escape.py
# ========================================================================
"""字符串转义工具（对应 Java `core/plugin/tool/code/EscapeTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的坑，照抄修法】真机日志里模型把**要转义的文本**塞进了 `target`（这个词太像"目标字符串"），
`input` 随手写成 "test"，于是拿到一句看不懂的"未知目标"。Java 侧的修法这里一条不落：
  1. `input` 支持别名 text/value/data/string/content/source/str；
  2. 识别得出"目标名写在 input 里"时自动互换；
  3. 目标名不认识时不再报错，而是按 html 处理并在正文里说明；
  4. 目标是 html / xml / java / json / url / regex / shell。

url 的编解码手写了 Java `URLEncoder`/`URLDecoder` 的规则（空格→`+`、保留 `.-*_`、
`~` 要转义），Python 的 `quote_plus` 在 `*`/`~` 上与 Java 不一致，直接用会出现两边输出不同。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 支持的转义目标（顺序与 Java 的 List.of 一致 —— 它出现在"未知目标"的提示正文里）
TARGETS = ("html", "xml", "java", "json", "url", "regex", "shell")


@tool
class EscapeTool(ToolPlugin):
    """字符串转义/反转义"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.escape"

    @property
    def name(self) -> str:
        return "escape_string"

    @property
    def description(self) -> str:
        return "字符串转义/反转义（html/json/java/url/regex/shell）"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "要转义的文本（放这里！不是 target）"},
                "action": {"type": "string", "description": "escape / unescape"},
                "target": {"type": "string", "description":
                           "转到哪种格式：html / xml / java / json / url / regex / shell，默认 html",
                           "default": "html"},
            },
            "required": ["input", "action"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        merged = dict(args)
        # input 的别名：模型常写 text / value / data / string / content
        for alias in ("text", "value", "data", "string", "content", "source", "str"):
            if "input" not in merged and merged.get(alias) is not None:
                merged["input"] = merged[alias]

        raw_action = "" if merged.get("action") is None else str(merged.get("action"))
        action = raw_action.lower().strip()
        if action.startswith("un"):
            action = "unescape"
        elif action != "escape":
            action = "escape"

        raw_target = "" if merged.get("target") is None else str(merged.get("target"))
        # 注意：target 缺省（没传）时是 html；传了但内容是空串时仍走"未知目标"的提示分支，
        # 这与 Java 的 `a.get("target") == null ? "html" : String.valueOf(...)` 完全一致
        target = "html" if merged.get("target") is None else raw_target.lower().strip()
        text = None if merged.get("input") is None else str(merged.get("input"))

        # 模型把目标名写进了 input、把正文写进了 target：换回来
        if target not in TARGETS and text is not None and text.lower().strip() in TARGETS:
            text, target = target, text.lower().strip()

        if text is None or text.strip() == "":
            return self.error("缺少必需参数: input" + self._required_hint())

        note = ""
        if target not in TARGETS:
            note = ("（target 只能是 " + " / ".join(TARGETS)
                    + " 之一，要转义的文本放在 input 里；本次按 html 处理）\n")
            target = "html"
        return self.success(note + _convert(target, action, text))

    def _required_hint(self) -> str:
        """把必填参数连说明一起回给模型（对齐 Java 的 requiredParamsHint）。"""
        schema = self.parameters_schema()
        required = schema.get("required") or []
        if not required:
            return ""
        props = schema.get("properties") or {}
        items = []
        for key in required:
            desc = str((props.get(key) or {}).get("description", ""))
            items.append(f"{key}（{desc}）")
        return "。本工具必填参数：" + "、".join(items)


def _convert(target: str, action: str, text: str) -> str:
    un = action == "unescape"
    if target in ("html", "xml"):
        if un:
            # 【&amp; 必须**最后**换】反转义是转义的逆运算：转义时第一步就是 `& → &amp;`
            # （见下面 escape 分支），所以还原时 `&amp;` 要最后处理。放在最前面会把
            # 正文里本来就有的字面量 `&lt;`（被正确转义成 `&amp;lt;`）先拆成 `&lt;`、
            # 第二步又当成实体换成 `<` —— escape→unescape 往返必错。
            return (text.replace("&lt;", "<").replace("&gt;", ">")
                    .replace("&quot;", "\"").replace("&amp;", "&"))
        return (text.replace("&", "&amp;").replace("<", "&lt;")
                .replace(">", "&gt;").replace("\"", "&quot;"))
    if target in ("java", "json"):
        if un:
            # 【不能逐条串行 replace】转义（下面 escape）第一步是 `\\ → \\\\`：字面量
            # `\n`（反斜杠+n）被转成 `\\n`（3 字符），串行规则会先在它的第 2 位命中
            # `\\n → 换行`，得到 `\<换行>`，最后 `\\\\ → \\` 又无从折叠 —— 往返必错。
            # 这里单趟从左到右扫描，和转义互为逆运算；不认识的转义原样保留。
            return _unescape_c_style(text)
        return (text.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n")
                .replace("\r", "\\r").replace("\t", "\\t"))
    if target == "url":
        try:
            return _java_url_decode(text) if un else _java_url_encode(text)
        except Exception as e:
            return "URL 处理失败: " + str(e)
    if target == "regex":
        # Java Pattern.quote：\Q … \E 原样包起来
        return text if un else "\\Q" + text + "\\E"
    if target == "shell":
        if un:
            return text.replace("'\\''", "'")
        return "'" + text.replace("'", "'\\''") + "'"
    return text


#: java/json 反转义的映射（与 `_convert` 里 escape 的 5 种一一对应，别少也别多）
_C_UNESCAPE = {"n": "\n", "t": "\t", "r": "\r", "\"": "\"", "\\": "\\"}


def _unescape_c_style(text: str) -> str:
    """单趟从左到右解 `\\n \\t \\r \\" \\\\`；不认识的转义（如 `\\x`）原样保留。

    【为什么不能串行 replace】见 `_convert` 里 java/json 分支的注释：转义先把 `\\`
    翻成 `\\\\`，反转义若按规则表逐条替换，字面量 `\\n` 会在错的位置先命中 `\\n → 换行`，
    escape→unescape 往返就不回来了。单趟扫描才是转义的真正逆运算。
    """
    out: list[str] = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "\\" and i + 1 < n and text[i + 1] in _C_UNESCAPE:
            out.append(_C_UNESCAPE[text[i + 1]])
            i += 2
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _java_url_encode(text: str) -> str:
    """Java `URLEncoder.encode(text, UTF_8)`：保留 a-z A-Z 0-9 . - * _，空格变 +。"""
    out: list[str] = []
    for byte in text.encode("utf-8"):
        ch = chr(byte)
        if ("a" <= ch <= "z") or ("A" <= ch <= "Z") or ("0" <= ch <= "9") or ch in ".-*_":
            out.append(ch)
        elif ch == " ":
            out.append("+")
        else:
            out.append("%%%02X" % byte)
    return "".join(out)


def _java_url_decode(text: str) -> str:
    """Java `URLDecoder.decode(text, UTF_8)`：+ 变空格，非法 %转义抛异常（同 Java）。"""
    raw = bytearray()
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch == "+":
            raw.append(0x20)
            i += 1
        elif ch == "%":
            pair = text[i + 1:i + 3]
            if len(pair) < 2:
                raise ValueError("URLDecoder: Incomplete trailing escape (%) pattern")
            if not all(c in "0123456789abcdefABCDEF" for c in pair):
                raise ValueError("URLDecoder: Illegal hex characters in escape (%) pattern - "
                                 + text[i:i + 3])
            raw.append(int(pair, 16))
            i += 3
        else:
            raw.extend(ch.encode("utf-8"))
            i += 1
    return raw.decode("utf-8", errors="replace")


# ========================================================================
# 原模块 lionbox/tools/code/format.py
# ========================================================================
"""代码空白规整工具（对应 Java `core/plugin/tool/code/CodeFormatTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差 ——
描述里的"不做语法级重排、不是任何语言的格式化器"是**故意留下的能力边界**：
Java 侧原来描述写着"格式化代码（缩进、换行等）"、schema 里还挂着一个从头到尾没被读过的
`language` 参数，模型把压成一行的 JS/JSON 丢进来指望它排版，拿回原样后以为工具坏了、反复重试。
所以这里的 language 参数也**不能加回来**。minimal_mode = False（Java 类别 OTHER）。

【实现的三个动作】制表符 → 4 空格、去行尾空白、连续空行压成一行；换行先统一成 \\n。
结果是整段代码本身（没有前后缀说明），可以直接拿去覆盖文件。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 制表符按几列展开（Java/前端社区最通用的 4）
INDENT = "    "


@tool
class CodeFormatTool(ToolPlugin):
    """规整代码空白"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.format"

    @property
    def name(self) -> str:
        return "format_code"

    @property
    def description(self) -> str:
        return ("规整代码空白：制表符缩进统一成4空格、去掉行尾空白、连续空行压成一行、统一换行符；"
                "不做语法级重排（不会改缩进层级、不会折行），不是任何语言的格式化器")

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "code": {"type": "string", "description": "代码内容"},
            },
            "required": ["code"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            code = self.get_required_string_arg(args, "code")
        except ValueError as e:
            return self.error(str(e))

        # 统一换行：CRLF 混在里面会让每一行末尾挂一个 \r，后面的行尾空白判断和输出都会带着它
        text = code.replace("\r\n", "\n").replace("\r", "\n")

        # 末尾那个空元素（文件以换行结尾时的产物）先摘掉，否则它会被当成"一个多余的空行"，
        # 结果凭空多出一个空行 —— 与 Java 的 split("\n", -1) + 摘末尾 完全同一套动作
        lines = text.split("\n")
        if lines and lines[-1] == "":
            lines.pop()

        out: list[str] = []
        last_blank = False
        for line in lines:
            fixed = line.replace("\t", INDENT) if "\t" in line else line
            trimmed = _strip_trailing(fixed)
            if not trimmed:
                if last_blank:
                    continue        # 连续空行只留一行
                last_blank = True
            else:
                last_blank = False
            out.append(trimmed)
        body = "".join(line + "\n" for line in out)
        return self.success(body)


def _strip_trailing(line: str) -> str:
    """去行尾空白（空格和制表符；制表符可能已经被展开，这里再兜一次）。"""
    return line.rstrip(" \t")


# ========================================================================
# 原模块 lionbox/tools/code/hash.py
# ========================================================================
"""哈希计算工具（对应 Java `core/plugin/tool/code/HashTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的行为，照抄】
1. 输入写死 UTF-8。Java 侧原来用 `input.getBytes()`（平台默认编码），
   带 `-Dfile.encoding=GBK` 启动时同一个字符串算出来的哈希和 md5sum/sha256sum
   对不上，用户会以为文件被改过。
2. 输出格式 `"{algorithm}: {hex小写}"`，algorithm 用**调用方原样传的字符串**
   （Java 就是 `algorithm + ": " + hex`，不做归一化回显）。
3. 算法名走 MessageDigest 的宽松命名（MD5 / SHA-1 / SHA-256 / sha256 都认），
   不认识时报 `哈希计算失败: {algorithm} MessageDigest not available`（Java 的异常原文形状）。

【扩展（不改变上面任何行为）】额外认 `file`（读文件字节算哈希，流式，不整块进内存）
和 `encoding`（hex=默认 / base64）。两个都不传时与 Java 完全一致。
"""


import base64 as _base64
import hashlib
from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 算法名 → hashlib 名称。Java 的 MessageDigest 认连字符写法，这里做等价归一。
_ALGORITHMS = {
    "md5": "md5",
    "sha": "sha1",
    "sha1": "sha1",
    "sha224": "sha224",
    "sha256": "sha256",
    "sha384": "sha384",
    "sha512": "sha512",
    "sha512/224": "sha512_224",
    "sha512/256": "sha512_256",
    "sha3-224": "sha3_224",
    "sha3-256": "sha3_256",
    "sha3-384": "sha3_384",
    "sha3-512": "sha3_512",
    "blake2b": "blake2b",
    "blake2s": "blake2s",
    "sm3": "sm3",
}

_CHUNK = 1 << 20


@tool
class HashTool(ToolPlugin):
    """计算字符串的MD5/SHA1/SHA256哈希值"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.hash"

    @property
    def name(self) -> str:
        return "hash"

    @property
    def description(self) -> str:
        return "计算字符串的MD5/SHA1/SHA256哈希值"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "输入内容"},
                "algorithm": {"type": "string", "description": "算法：MD5/SHA-1/SHA-256",
                              "default": "SHA-256"},
            },
            "required": ["input"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            algorithm = self.get_string_arg(args, "algorithm", "SHA-256")
            file_arg = str(args.get("file") or args.get("path") or "").strip()
            encoding = self.get_string_arg(args, "encoding", "hex").strip().lower() or "hex"

            digest = _new_digest(algorithm)
            if digest is None:
                # Java 的 NoSuchAlgorithmException 原文形状
                return self.error("哈希计算失败: " + algorithm + " MessageDigest not available")

            if file_arg:
                path = self.resolve_path(file_arg)
                if not path.is_file():
                    return self.error("哈希计算失败: 文件不存在: " + str(path))
                size = _feed_file(digest, path)
                tail = f"\n文件: {path}（{size} 字节）"
            else:
                text = self.get_required_string_arg(args, "input")
                digest.update(text.encode("utf-8"))
                tail = ""

            raw = digest.digest()
            if encoding == "base64":
                out = _base64.b64encode(raw).decode("ascii")
            elif encoding == "hex":
                out = raw.hex()
            else:
                return self.error("哈希计算失败: 不支持的输出编码: " + encoding
                                  + "（支持 hex / base64）")
            return self.success(algorithm + ": " + out + tail)
        except Exception as e:
            return self.error("哈希计算失败: " + str(e))


def _new_digest(algorithm: str):
    """按 Java MessageDigest 的命名规则找算法；找不到返回 None。"""
    key = str(algorithm or "").strip().lower()
    if key in _ALGORITHMS:
        name = _ALGORITHMS[key]
    else:
        flat = key.replace("-", "")
        if flat in _ALGORITHMS:
            name = _ALGORITHMS[flat]
        else:
            name = key.replace("/", "_")
    try:
        return hashlib.new(name)
    except (ValueError, TypeError):
        return None


def _feed_file(digest, path: Path) -> int:
    """流式喂文件，避免把大文件整块读进内存。返回字节数。"""
    total = 0
    with path.open("rb") as fh:
        while True:
            block = fh.read(_CHUNK)
            if not block:
                break
            total += len(block)
            digest.update(block)
    return total


# ========================================================================
# 原模块 lionbox/tools/code/json.py
# ========================================================================
"""JSON 格式化/验证/压缩工具（对应 Java `core/plugin/tool/code/JsonTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【为什么要自己写序列化】Java 用的是 Jackson 的 `writerWithDefaultPrettyPrinter()`：
  1. 键值分隔是 `" : "`（冒号两边都有空格），缩进 2 空格；
  2. 数组是**行内**的 `[ 1, 2 ]`（`DefaultPrettyPrinter` 的数组缩进器是 FixedSpaceIndenter），
     只有对象才换行；空对象/空数组写作 `{ }` / `[ ]`；
  3. 中文原样输出（不转成 \\uXXXX），键顺序保留输入顺序。
Python 的 `json.dumps(indent=2)` 这三点全都不同，会让"同一个输入在两版里格式不一样"，
所以这里按 Jackson 的实际输出实现（对照 Java 侧实测输出逐项核对过）。
"""


import json as _json
import os
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class JsonTool(ToolPlugin):
    """格式化、验证、压缩JSON"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.json"

    @property
    def name(self) -> str:
        return "json_format"

    @property
    def description(self) -> str:
        return "格式化、验证、压缩JSON"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "JSON字符串"},
                "action": {"type": "string", "description": "format/minify/validate",
                           "default": "format"},
            },
            "required": ["input"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            text = self.get_required_string_arg(args, "input")
            action = self.get_string_arg(args, "action", "format")

            if action == "validate":
                _parse(text)
                return self.success("JSON格式有效")
            if action == "format":
                return self.success(_dump(_parse(text), pretty=True))
            if action == "minify":
                return self.success(_dump(_parse(text), pretty=False))
            return self.error("未知操作: " + action)
        except Exception as e:
            return self.error("JSON处理失败: " + str(e))


def _parse(text: str) -> Any:
    """严格解析：NaN / Infinity 这类非标准常量按 Jackson 的默认策略拒绝。"""
    return _json.loads(text, parse_constant=_reject_constant)


def _reject_constant(name: str) -> Any:
    raise ValueError(f"非标准 JSON 常量 {name}（Jackson 默认不允许 NaN/Infinity）")


def _dump(value: Any, pretty: bool, depth: int = 0) -> str:
    """按 Jackson 的形状输出。depth 只统计**对象**层数（数组是行内的，不计层）。"""
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return _json.dumps(value, ensure_ascii=False)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        return _java_double(value)
    if isinstance(value, dict):
        if not value:
            return "{ }" if pretty else "{}"
        if not pretty:
            return "{" + ",".join(
                _json.dumps(str(k), ensure_ascii=False) + ":" + _dump(v, False, depth + 1)
                for k, v in value.items()) + "}"
        # Jackson 的 DefaultIndenter 用的是 SYSTEM_LINEFEED：Windows 上是 CRLF
        body = ("," + os.linesep).join(
            "  " * (depth + 1) + _json.dumps(str(k), ensure_ascii=False) + " : "
            + _dump(v, True, depth + 1)
            for k, v in value.items())
        return "{" + os.linesep + body + os.linesep + "  " * depth + "}"
    if isinstance(value, (list, tuple)):
        if not value:
            return "[ ]" if pretty else "[]"
        items = [_dump(v, pretty, depth) for v in value]
        return "[ " + ", ".join(items) + " ]" if pretty else "[" + ",".join(items) + "]"
    return _json.dumps(str(value), ensure_ascii=False)


def _java_double(v: float) -> str:
    """对齐 Java `Double.toString` 的写法：一定带小数点，指数用大写 E 且没有 '+'。"""
    if v != v or v in (float("inf"), float("-inf")):
        return '"' + repr(v).replace("inf", "Infinity") + '"'
    text = repr(v)
    if "e" in text or "E" in text:
        mantissa, _, exponent = text.replace("E", "e").partition("e")
        if "." not in mantissa:
            mantissa += ".0"
        return mantissa + "E" + str(int(exponent))
    if "." not in text:
        text += ".0"
    return text


# ========================================================================
# 原模块 lionbox/tools/code/markdown.py
# ========================================================================
"""Markdown 渲染工具（对应 Java `core/plugin/tool/code/MarkdownTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的两个坑，照抄修法】
1. 标题正则必须按行匹配（Java 的 `Pattern.MULTILINE` ↔ Python 的 `re.M`），
   否则只有"整篇恰好一行 # 标题"才碰巧生效，多行 Markdown 一个标题都转不出来。
2. 先做 HTML 转义再转换：`markdown="<script>alert(1)</script>"` 原来会被原样塞进这份
   "HTML 预览"里，谁贴进页面就是实打实的 XSS。

转换顺序与 Java 完全一致：h3 → h2 → h1 → ** → * → `code` → 换行变 <br>。
"""


import re
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

_H3 = re.compile(r"^### (.*)$", re.MULTILINE)
_H2 = re.compile(r"^## (.*)$", re.MULTILINE)
_H1 = re.compile(r"^# (.*)$", re.MULTILINE)


@tool
class MarkdownTool(ToolPlugin):
    """Markdown转HTML预览"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.markdown"

    @property
    def name(self) -> str:
        return "markdown_render"

    @property
    def description(self) -> str:
        return "Markdown转HTML预览"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "markdown": {"type": "string", "description": "Markdown内容"},
            },
            "required": ["markdown"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            md = self.get_required_string_arg(args, "markdown")
        except ValueError as e:
            return self.error(str(e))

        html = escape_html(md)
        html = _H3.sub(r"<h3>\1</h3>", html)
        html = _H2.sub(r"<h2>\1</h2>", html)
        html = _H1.sub(r"<h1>\1</h1>", html)
        # 行内记号：** 要比 * 先换（和 Java 同样的顺序）
        html = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", html)
        html = re.sub(r"\*(.*?)\*", r"<em>\1</em>", html)
        html = re.sub(r"`([^`]+)`", r"<code>\1</code>", html)
        html = html.replace("\n", "<br>")
        return self.success(html)


def escape_html(text: str) -> str:
    """转义 HTML 元字符：& 必须先换，否则后面换出来的 &lt; 会被二次转义成 &amp;lt;。"""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


# ========================================================================
# 原模块 lionbox/tools/code/number.py
# ========================================================================
"""进制转换工具（对应 Java `core/plugin/tool/code/NumberTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的坑，照抄修法】用户日志里模型给的是**进制名**：
`number_convert(value=255, fromBase=dec, toBase=hex)` —— Java 侧原来直接
`((Number) arguments.get("fromBase")).intValue()`，一句 ClassCastException 就把工具废了。
所以这里也自己认进制名（dec/hex/bin/oct、十进制…），并且**不硬转 Number**。

数值解析按 Java `Long.parseLong(v, radix)` 的语义来：64 位有符号、不接受下划线、
越界要报错（Python 的 int() 是任意精度且容忍 "1_0"，直接用会出现"Java 报错、Python 静默成功"）。
"""


import re
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

_DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz"
_DECIMAL_ONLY = re.compile(r"^[+-]?\d+$")

_BASE_NAMES = {
    "dec": 10, "decimal": 10, "denary": 10, "10进制": 10, "十进制": 10,
    "hex": 16, "hexadecimal": 16, "16进制": 16, "十六进制": 16,
    "bin": 2, "binary": 2, "2进制": 2, "二进制": 2,
    "oct": 8, "octal": 8, "8进制": 8, "八进制": 8,
}

LONG_MIN = -(2 ** 63)
LONG_MAX = 2 ** 63 - 1


@tool
class NumberTool(ToolPlugin):
    """进制转换"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.number"

    @property
    def name(self) -> str:
        return "number_convert"

    @property
    def description(self) -> str:
        return "进制转换（dec/hex/bin/oct 或 10/16/2/8）"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "value": {"type": "string", "description": "要转换的数值，如 255"},
                "fromBase": {"type": "string",
                             "description": "源进制：10/16/2/8，也认 dec/hex/bin/oct",
                             "default": "10"},
                "toBase": {"type": "string",
                           "description": "目标进制：10/16/2/8，也认 dec/hex/bin/oct",
                           "default": "16"},
            },
            "required": ["value", "fromBase", "toBase"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            value = self.get_required_string_arg(args, "value").strip()
        except ValueError as e:
            # Java 里 IllegalArgumentException 落到泛化 catch → 前缀同样是"转换失败: "
            return self.error("转换失败: " + str(e))
        try:
            from_base = parse_base(args.get("fromBase"), 10)
            to_base = parse_base(args.get("toBase"), 16)
            if from_base < 2 or from_base > 36 or to_base < 2 or to_base > 36:
                return self.error(
                    f"进制必须在 2-36 之间（收到 fromBase={args.get('fromBase')}, "
                    f"toBase={args.get('toBase')}）；也可以直接写 dec/hex/bin/oct")

            digits = value
            negative = digits.startswith("-")
            if negative or digits.startswith("+"):
                digits = digits[1:]
            if digits.startswith(("0x", "0X")):
                digits = digits[2:]
                from_base = 16
            elif digits.startswith(("0b", "0B")):
                digits = digits[2:]
                from_base = 2
            elif digits.startswith(("0o", "0O")):
                digits = digits[2:]
                from_base = 8

            decimal = _parse_long(digits, from_base, negative)
        except ValueError:
            return self.error("转换失败: " + str(args.get("value")) + " 不是合法的 "
                              + str(args.get("fromBase")) + " 进制数字")
        except Exception as e:
            return self.error("转换失败: " + str(e))

        out = _to_base(decimal, to_base).upper()
        return self.success(f"{value}（{base_name(from_base)}） = {out}（{base_name(to_base)}）"
                            f"\n十进制: {decimal}")


def parse_base(raw: Any, fallback: int) -> int:
    """认 "10" / "dec" / "hex" / "bin" / "oct" / "decimal" / "十进制"…（对齐 Java parseBase）。"""
    if raw is None:
        return fallback
    text = str(raw).strip().lower()
    if text == "":
        return fallback
    if text in _BASE_NAMES:
        return _BASE_NAMES[text]
    if _DECIMAL_ONLY.match(text):
        return int(text)
    return fallback


def base_name(base: int) -> str:
    return {2: "2进制", 8: "8进制", 10: "10进制", 16: "16进制"}.get(base, f"{base}进制")


def _parse_long(digits: str, radix: int, negative: bool) -> int:
    """Java `Long.parseLong(digits, radix)`：大小写不敏感、拒绝下划线、越界报错。"""
    if digits == "" or "_" in digits:
        raise ValueError("NumberFormatException")
    value = 0
    for ch in digits.lower():
        digit = _DIGITS.find(ch)
        if digit < 0 or digit >= radix:
            raise ValueError("NumberFormatException")
        value = value * radix + digit
        if value > LONG_MAX + 1:
            raise ValueError("NumberFormatException")
    if negative:
        value = -value
    if value < LONG_MIN or value > LONG_MAX:
        raise ValueError("NumberFormatException")
    return value


def _to_base(value: int, base: int) -> str:
    """Java `Long.toString(value, base)`（超出 2-36 的进制调用方已经挡掉）。"""
    if value == 0:
        return "0"
    negative = value < 0
    rest = abs(value)
    digits: list[str] = []
    while rest:
        rest, rem = divmod(rest, base)
        digits.append(_DIGITS[rem])
    return ("-" if negative else "") + "".join(reversed(digits))


# ========================================================================
# 原模块 lionbox/tools/code/regex.py
# ========================================================================
"""正则表达式测试工具（对应 Java `core/plugin/tool/code/RegexTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的坑，照抄修法】
1. 结果**必须**截断：Java 侧原来 `while (m.find())` 有多少收多少，pattern="." 配 100KB 文本
   会生成约 10 万行结果一次性灌进模型上下文（几 MB），这一轮对话直接废掉。
   这里沿用 MAX_MATCHES = 200，超了就明说被截断。
2. 超时保护：Python 的 `re` 没有引擎级超时（Java 侧另有超时保护），
   所以这里做了两道：编译前拒绝"嵌套量词"这类会指数级回溯的写法（直接返回失败并说明怎么改写），
   执行中还有一道墙钟预算，超了就停下并如实标注。宁可明确报错，也不要让一个正则把服务挂死。
"""


import re
import time
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 最多回多少条匹配（与 Java 的 MAX_MATCHES 一致）
MAX_MATCHES = 200

#: 匹配阶段的墙钟预算（秒）：超了就停止收集并标注
TIME_BUDGET_SECONDS = 10.0


@tool
class RegexTool(ToolPlugin):
    """测试正则表达式匹配"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.regex"

    @property
    def name(self) -> str:
        return "regex_test"

    @property
    def description(self) -> str:
        return "测试正则表达式匹配"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pattern": {"type": "string", "description": "正则表达式"},
                "input": {"type": "string", "description": "测试文本"},
                "flags": {"type": "string", "description": "标志：i=忽略大小写", "default": ""},
            },
            "required": ["pattern", "input"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            pattern = self.get_required_string_arg(args, "pattern")
            text = self.get_required_string_arg(args, "input")
            flags = self.get_string_arg(args, "flags", "")

            risky = find_nested_quantifier(pattern)
            if risky is not None:
                return self.error(
                    "正则表达式可能有灾难性回溯风险（嵌套量词 " + risky + "），已拒绝执行："
                    "Python 侧没有引擎级超时。请改写，例如把 (.+)+ 换成 .+、"
                    "把 (\\w+)* 换成 [\\w]*，或用更具体的字符集限定重复范围。")

            flag = re.IGNORECASE if "i" in flags else 0
            compiled = re.compile(pattern, flag)
            matches: list[str] = []
            truncated = False
            timed_out = False
            started = time.monotonic()
            for m in compiled.finditer(text):
                if len(matches) >= MAX_MATCHES:
                    truncated = True        # 达到上限就停：剩下的不再收集，只报一句"还有更多"
                    break
                if time.monotonic() - started > TIME_BUDGET_SECONDS:
                    timed_out = True
                    break
                matches.append(f"位置[{m.start()},{m.end()}]: '{m.group()}'")

            if not matches:
                if timed_out:
                    return self.error(
                        f"正则匹配超过 {TIME_BUDGET_SECONDS:.0f} 秒被中止（文本太长或表达式太慢）："
                        "请把 pattern 写得更具体，或先在小段文本上验证。")
                return self.success("无匹配结果")

            if truncated:
                head = f"匹配结果（只列出前 {len(matches)} 条，后面还有更多）:\n"
            else:
                head = f"匹配结果（共 {len(matches)} 条）:\n"
            body = "".join(match + "\n" for match in matches)
            if truncated:
                body += ("（结果已截断：还有更多匹配没列出来。要看全部就把 pattern 写得更具体，"
                         "或者先用更小的 input 验证正则）\n")
            if timed_out:
                body += (f"（匹配超时：已花 {TIME_BUDGET_SECONDS:.0f} 秒，后面的匹配没有继续收集）\n")
            return self.success(head + body)
        except Exception as e:
            return self.error("正则表达式错误: " + str(e))


def find_nested_quantifier(pattern: str) -> str | None:
    """找出"被量词修饰的组里还含无界量词"的写法（经典指数级回溯），返回那段文本。

    只认这一种形态（例如 `(a+)+`、`(.*)*`、`(\\d+){2,}`），不做过度拦截：
    误报会让本来能跑的正则用不了，所以宁可只挡最确定的一类。
    """
    stack: list[int] = []
    i = 0
    n = len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "[":
            i += 1
            while i < n and pattern[i] != "]":
                i += 2 if pattern[i] == "\\" else 1
            i += 1
            continue
        if ch == "(":
            stack.append(i)
            i += 1
            continue
        if ch == ")":
            if not stack:
                i += 1
                continue
            start = stack.pop()
            end = i
            if _has_unbounded_quantifier(pattern, start + 1, end) and _quantifier_at(pattern, end + 1):
                return pattern[start:end + 1] + _quantifier_at(pattern, end + 1)
            i += 1
            continue
        i += 1
    return None


def _has_unbounded_quantifier(pattern: str, start: int, end: int) -> bool:
    i = start
    while i < end:
        ch = pattern[i]
        if ch == "\\":
            i += 2
            continue
        if ch == "[":
            i += 1
            while i < end and pattern[i] != "]":
                i += 2 if pattern[i] == "\\" else 1
            i += 1
            continue
        if ch in "*+":
            return True
        if ch == "{" and _quantifier_at(pattern, i):
            return True
        i += 1
    return False


def _quantifier_at(pattern: str, i: int) -> str:
    """位置 i 上是不是"无界量词"（*、+、{m,}）；是就返回它的文本。"""
    if i >= len(pattern):
        return ""
    ch = pattern[i]
    if ch in "*+":
        return ch
    if ch == "{":
        close = pattern.find("}", i)
        if close < 0:
            return ""
        body = pattern[i + 1:close]
        if body.endswith(",") and body[:-1].isdigit():
            return pattern[i:close + 1]
    return ""


# ========================================================================
# 原模块 lionbox/tools/code/string.py
# ========================================================================
"""字符串处理工具（对应 Java `core/plugin/tool/code/StringTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的两个坑，照抄修法】
1. 大小写转换不带区域设置：Java 是 `Locale.ROOT`（土耳其语 JVM 下 "file".toUpperCase() 会变成
   "FİLE"、'I'.toLowerCase() 变成 'ı'，工具的大小写转换和 action 归一都会出错）。
   Python 的 `str.upper()/lower()` 本身就是语言无关的，天然对齐。
2. action 别名归一：模型实测写过 uppercase / to_upper / lowercase / to_lower / len / strip /
   翻转 等 8 种写法，Java 侧全部认了下来（认下来比让它反复试划算），这里照抄同一张别名表。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: action 别名表（键已小写、已 trim）—— 与 Java 的 switch 一一对应
_ALIASES = {
    "uppercase": "upper", "to_upper": "upper", "to_uppercase": "upper",
    "upcase": "upper", "大写": "upper",
    "lowercase": "lower", "to_lower": "lower", "to_lowercase": "lower",
    "downcase": "lower", "小写": "lower",
    "strip": "trim", "去除空格": "trim",
    "len": "length", "size": "length", "长度": "length",
    "revert": "reverse", "翻转": "reverse", "反转": "reverse",
}


@tool
class StringTool(ToolPlugin):
    """字符串处理：大小写转换、trim、长度等"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.string"

    @property
    def name(self) -> str:
        return "string_utils"

    @property
    def description(self) -> str:
        return "字符串处理：大小写转换、trim、长度等"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "输入字符串"},
                "action": {"type": "string", "description":
                           "只支持这几个：upper / lower / trim / length / reverse"},
            },
            "required": ["input", "action"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            text = self.get_required_string_arg(args, "input")
            action = self.get_required_string_arg(args, "action").lower().strip()
        except ValueError as e:
            return self.error(str(e))

        action = _ALIASES.get(action, action)

        if action == "upper":
            return self.success(text.upper())
        if action == "lower":
            return self.success(text.lower())
        if action == "trim":
            return self.success(_java_trim(text))
        if action == "length":
            return self.success("长度: " + str(len(text)))
        if action == "reverse":
            return self.success(text[::-1])
        return self.error(
            "未知操作: " + action + "。本工具只支持：upper、lower、trim、length、reverse")


def _java_trim(text: str) -> str:
    """Java 的 `String.trim()` 只去 <= U+0020 的首尾字符（Python 的 strip 去得更多）。"""
    start, end = 0, len(text)
    while start < end and text[start] <= " ":
        start += 1
    while end > start and text[end - 1] <= " ":
        end -= 1
    return text[start:end]


# ========================================================================
# 原模块 lionbox/tools/code/timestamp.py
# ========================================================================
"""时间工具（对应 Java `core/plugin/tool/code/TimestampTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的坑，照抄修法】模型传 `format=%Y-%m-%d %H:%M:%S`（strftime 风格），Java 侧直接把它
当 `DateTimeFormatter` 模式用，输出成了 `%2026-%58-%29 %12:%9:%2` 这种乱码。所以：
  1. 先认 strftime 记号（%Y %m %d %H %M %S %s %p %A %a %B %b %j %e %F %T %R %D %n %t %%），
     逐个翻译成 Java 模式；已经是 Java 模式（yyyy/MM/dd…）就原样用；
  2. 也认 unix/epoch/iso/date/time/full 这些口语别名；
  3. **不认识的记号要报错**（原来是 `s.replace("%", "")` 一刀删掉，"%s" 变成字面量 "s"
     还不报错，模型根本不知道格式写错了），报错里把支持的记号列全；
  4. `%s`（unix 秒）在 Java 模式里没有对应记号，用占位记号先切开、格式化时把秒数填回去 ——
     这里照抄同一套动作。
另外 Python 侧自己实现了 Java 模式的渲染（yyyy/MM/dd/HH/mm/ss/E/MMM… + 单引号字面量），
因为标准库的 strftime 在 Windows 上不支持 %-d 这类"不补零"写法，会静默输出错的结果。

【扩展（不改变上面任何行为）】额外认 `timezone`/`tz`（时区，默认跟随系统，与 Java 一致）
与 `parse`/`input`（把一个已存在的时间戳解析出来，支持 unix 秒/毫秒、ISO 8601、常见写法）。
不传这两个参数时输出与 Java 完全一致。
"""


import re
from datetime import datetime, timedelta, timezone, tzinfo
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

DEFAULT_FORMAT = "yyyy-MM-dd HH:mm:ss"

#: `%s`（unix 秒）的占位记号（同 Java 的 EPOCH_SECONDS）
EPOCH_SECONDS = "\u0001"

#: 支持的 strftime 记号（报错时列给模型看，省得它一个个试）
SUPPORTED_TOKENS = "%Y %y %m %d %H %I %M %S %s %p %A %a %B %b %j %e %F %T %R %D %n %t %%"

_ALIASES__tools_code_timestamp = {
    "unix": DEFAULT_FORMAT, "epoch": DEFAULT_FORMAT, "timestamp": DEFAULT_FORMAT,
    "iso": "yyyy-MM-dd'T'HH:mm:ss", "iso8601": "yyyy-MM-dd'T'HH:mm:ss",
    "iso-8601": "yyyy-MM-dd'T'HH:mm:ss",
    "date": "yyyy-MM-dd", "time": "HH:mm:ss",
    "full": DEFAULT_FORMAT, "datetime": DEFAULT_FORMAT,
}

_STRFTIME = {
    "Y": "yyyy", "y": "yy", "m": "MM", "d": "dd", "H": "HH", "I": "hh", "M": "mm",
    "S": "ss", "s": EPOCH_SECONDS, "p": "a", "A": "EEEE", "a": "EEE", "B": "MMMM",
    "b": "MMM", "j": "DDD", "e": "d", "F": "yyyy-MM-dd", "T": "HH:mm:ss", "R": "HH:mm",
    "D": "MM/dd/yy", "n": "\n", "t": "\t", "%": "%",
}

_MONTHS_SHORT = ("Jan", "Feb", "Mar", "Apr", "May", "Jun",
                 "Jul", "Aug", "Sep", "Oct", "Nov", "Dec")
_MONTHS_FULL = ("January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December")
_DAYS_SHORT = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
_DAYS_FULL = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
              "Saturday", "Sunday")

#: 常见时区的固定偏移（Python 在 Windows 上没有系统 tz 数据库，装了 tzdata 才认 IANA 名字；
#: 没有 tzdata 时用这张表兜底，避免"时区参数一填就报错"）
_FIXED_ZONES = {
    "utc": 0, "gmt": 0, "z": 0,
    "asia/shanghai": 8, "asia/chongqing": 8, "asia/hong_kong": 8, "asia/singapore": 8,
    "asia/taipei": 8, "asia/tokyo": 9, "asia/seoul": 9, "asia/bangkok": 7,
    "asia/kolkata": 5.5, "asia/dubai": 4, "europe/moscow": 3, "europe/london": 0,
    "europe/paris": 1, "europe/berlin": 1, "america/new_york": -5,
    "america/chicago": -6, "america/denver": -7, "america/los_angeles": -8,
    "australia/sydney": 10, "pacific/auckland": 12,
}


@tool
class TimestampTool(ToolPlugin):
    """获取当前时间"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.timestamp"

    @property
    def name(self) -> str:
        return "timestamp"

    @property
    def description(self) -> str:
        return "获取当前时间（支持 yyyy-MM-dd HH:mm:ss 或 %Y-%m-%d 两种写法）"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "format": {"type": "string", "description":
                           "时间格式：Java 模式 yyyy-MM-dd HH:mm:ss，或 strftime 风格 "
                           "%Y-%m-%d %H:%M:%S（%s = unix 秒）",
                           "default": DEFAULT_FORMAT},
            },
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        raw = self.get_string_arg(args, "format", DEFAULT_FORMAT)

        tz_raw = str(args.get("timezone") or args.get("tz") or "").strip()
        try:
            zone = _resolve_zone(tz_raw)
        except ValueError as e:
            return self.error(str(e))

        parse_raw = args.get("parse") if args.get("parse") is not None else args.get("input")
        if parse_raw is not None and str(parse_raw).strip() != "":
            try:
                moment = _parse_moment(str(parse_raw).strip(), zone)
            except ValueError as e:
                return self.error(str(e))
        else:
            moment = datetime.now(timezone.utc).astimezone(zone)

        epoch = int(moment.timestamp())
        local = moment.astimezone(zone)
        try:
            formatted = _format(_normalize(raw), local, epoch)
        except ValueError as e:
            return self.error(
                f"时间格式无法识别: {raw}。{e}。Java 模式例：yyyy-MM-dd HH:mm:ss；"
                "strftime 记号例：%Y-%m-%d %H:%M:%S；本工具支持的 strftime 记号："
                + SUPPORTED_TOKENS
                + "。要原样输出字母（比如 ISO 里那个 T）得用单引号包住：%Y-%m-%d'T'%H:%M:%S")

        head = "解析结果: " if parse_raw is not None and str(parse_raw).strip() != "" \
            else "当前时间: "
        return self.success(f"{head}{formatted}"
                            f"\nUnix时间戳: {epoch}"
                            f"\nISO格式: {_instant_text(moment)}")


# --------------------------------------------------------------------------
# 格式：strftime → Java 模式 → 渲染
# --------------------------------------------------------------------------


def _normalize(raw: str) -> str:
    """把 strftime / 口语别名统一成 Java 的 DateTimeFormatter 模式（对齐 Java normalize）。"""
    if raw is None or raw.strip() == "":
        return DEFAULT_FORMAT
    text = raw.strip()
    alias = _ALIASES__tools_code_timestamp.get(text.lower())
    if alias is not None:
        return alias
    if "%" not in text:
        return text

    out: list[str] = []
    i = 0
    while i < len(text):
        ch = text[i]
        if ch != "%":
            out.append(ch)
            i += 1
            continue
        if i + 1 >= len(text):
            raise ValueError("格式结尾多了一个 %（strftime 记号后面必须跟字母，例如 %Y）")
        token = text[i + 1]
        if token not in _STRFTIME:
            raise ValueError(f"不支持的 strftime 记号 %{token}（支持的：{SUPPORTED_TOKENS}）")
        out.append(_STRFTIME[token])
        i += 2
    return "".join(out)


def _format(pattern: str, moment: datetime, epoch_second: int) -> str:
    """按翻译好的 Java 模式格式化；`%s`（epoch 秒）的位置直接填秒数（同 Java）。"""
    out: list[str] = []
    rest = pattern
    while True:
        at = rest.find(EPOCH_SECONDS)
        if at < 0:
            out.append(_format_part(rest, moment))
            return "".join(out)
        out.append(_format_part(rest[:at], moment))
        out.append(str(epoch_second))
        rest = rest[at + len(EPOCH_SECONDS):]


def _format_part(pattern: str, moment: datetime) -> str:
    if pattern == "":
        return ""
    out: list[str] = []
    i = 0
    n = len(pattern)
    while i < n:
        ch = pattern[i]
        if ch == "'":
            if i + 1 < n and pattern[i + 1] == "'":
                out.append("'")
                i += 2
                continue
            end = pattern.find("'", i + 1)
            if end < 0:
                raise ValueError("模式里的单引号没有配对（要输出单引号请写两个 ''）")
            out.append(pattern[i + 1:end])
            i = end + 1
            continue
        if not ch.isalpha():
            out.append(ch)
            i += 1
            continue
        j = i
        while j < n and pattern[j] == ch:
            j += 1
        count = j - i
        out.append(_render_letter(ch, count, moment))
        i = j
    return "".join(out)


def _render_letter(letter: str, count: int, moment: datetime) -> str:
    """一个 Java 模式字母 → 文本。认不出的字母按 Java 的行为报错。"""
    if letter in ("y", "Y", "u"):
        if count == 2:
            return f"{moment.year % 100:02d}"
        if count == 1:
            return str(moment.year)
        return str(moment.year).rjust(count, "0")
    if letter in ("M", "L"):
        if count == 1:
            return str(moment.month)
        if count == 2:
            return f"{moment.month:02d}"
        if count == 3:
            return _locale_text(moment, "%b", _MONTHS_SHORT[moment.month - 1])
        if count == 4:
            return _locale_text(moment, "%B", _MONTHS_FULL[moment.month - 1])
        return _locale_text(moment, "%B", _MONTHS_FULL[moment.month - 1])[0]
    if letter == "d":
        return str(moment.day) if count == 1 else f"{moment.day:02d}"
    if letter == "D":
        day_of_year = moment.timetuple().tm_yday
        return str(day_of_year).rjust(min(count, 3), "0")
    if letter == "E":
        return _locale_text(moment, "%a" if count <= 3 else "%A",
                            _DAYS_SHORT[moment.weekday()] if count <= 3
                            else _DAYS_FULL[moment.weekday()])
    if letter == "H":
        return str(moment.hour) if count == 1 else f"{moment.hour:02d}"
    if letter == "h":
        hour = moment.hour % 12 or 12
        return str(hour) if count == 1 else f"{hour:02d}"
    if letter == "m":
        return str(moment.minute) if count == 1 else f"{moment.minute:02d}"
    if letter == "s":
        return str(moment.second) if count == 1 else f"{moment.second:02d}"
    if letter == "S":
        return str(moment.microsecond).rjust(6, "0")[:count]
    if letter == "a":
        return "AM" if moment.hour < 12 else "PM"
    raise ValueError("Unknown pattern letter: " + letter)


_locale_ready = False


def _locale_text(moment: datetime, fmt: str, fallback: str) -> str:
    """星期/月份的名字跟随系统区域 —— Java 的 DateTimeFormatter 用的是默认 Locale，
    中文机器上 EEEE 出来就是"星期六"（实测），所以这里也走系统区域，拿不到再退回英文。"""
    global _locale_ready
    if not _locale_ready:
        _locale_ready = True
        try:
            import locale as _locale
            _locale.setlocale(_locale.LC_TIME, "")
        except Exception:
            pass
    try:
        text = moment.strftime(fmt)
        return text if text else fallback
    except Exception:
        return fallback


# --------------------------------------------------------------------------
# 时区与时间戳解析（扩展能力）
# --------------------------------------------------------------------------


def _resolve_zone(raw: str) -> tzinfo:
    if raw == "" or raw.lower() in ("local", "system", "default"):
        return datetime.now().astimezone().tzinfo or timezone.utc
    text = raw.strip()
    offset = re.fullmatch(r"([+-])(\d{1,2})(?::?(\d{2}))?", text)
    if offset:
        sign = -1 if offset.group(1) == "-" else 1
        hours = int(offset.group(2))
        minutes = int(offset.group(3) or 0)
        return timezone(sign * timedelta(hours=hours, minutes=minutes))
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(text)
    except Exception:
        pass
    fixed = _FIXED_ZONES.get(text.lower())
    if fixed is not None:
        return timezone(timedelta(hours=fixed))
    raise ValueError("时区无法识别: " + raw + "（可用 UTC、Asia/Shanghai 这类名字，"
                     "或 +08:00 这样的偏移）")


def _parse_moment(raw: str, zone: tzinfo) -> datetime:
    """支持 unix 秒/毫秒、ISO 8601、常见的 "YYYY-MM-DD HH:MM:SS" 写法。"""
    text = raw.strip()
    if re.fullmatch(r"-?\d{10}", text):
        return datetime.fromtimestamp(int(text), tz=timezone.utc)
    if re.fullmatch(r"-?\d{13}", text):
        return datetime.fromtimestamp(int(text) / 1000, tz=timezone.utc)
    if re.fullmatch(r"-?\d+(\.\d+)?", text):
        return datetime.fromtimestamp(float(text), tz=timezone.utc)

    iso = text.replace("Z", "+00:00").replace("z", "+00:00")
    try:
        parsed = datetime.fromisoformat(iso)
        return parsed.replace(tzinfo=zone) if parsed.tzinfo is None else parsed
    except ValueError:
        pass
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M",
                "%Y/%m/%d %H:%M:%S", "%Y/%m/%d", "%Y-%m-%d", "%Y%m%d%H%M%S", "%Y%m%d"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=zone)
        except ValueError:
            continue
    raise ValueError("时间戳无法解析: " + raw + "（支持 unix 秒/毫秒、ISO 8601、"
                     "YYYY-MM-DD HH:MM:SS、YYYY-MM-DD 等写法）")


def _instant_text(moment: datetime) -> str:
    """对齐 Java `Instant.toString()`：UTC、秒必写、小数部分按 0/3/6 位、结尾 Z。"""
    utc = moment.astimezone(timezone.utc)
    base = utc.strftime("%Y-%m-%dT%H:%M:%S")
    micro = utc.microsecond
    if micro == 0:
        fraction = ""
    elif micro % 1000 == 0:
        fraction = f".{micro // 1000:03d}"
    else:
        fraction = f".{micro:06d}"
    return base + fraction + "Z"


# ========================================================================
# 原模块 lionbox/tools/code/uuid.py
# ========================================================================
"""UUID 生成工具（对应 Java `core/plugin/tool/code/UuidTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差 ——
注意 Java 的 schema 里**没有** "required"（count 可省略，默认 1），这里也不加。
minimal_mode = False（Java 类别 OTHER）。

【实测过的两个坑，照抄修法】
1. count 没有上限时 count=10000000 会拼出约 370MB 的字符串，堆直接打满 ——
   Java 侧上线 MAX_COUNT=1000，超了就截断**并且明说**（"已截断"那行不能省：
   不然模型以为拿到了 1000 万个，拿着这个数字继续往下算）。
2. count 传 0/负数原来循环一次都不跑、返回空字符串**还算成功** —— "空成功"比报错更坑，
   现在直接返回失败，并把当前值写进消息。
"""


import uuid as _uuid
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 一次最多生成多少个（与 Java 的 MAX_COUNT 一致）
MAX_COUNT = 1000


@tool
class UuidTool(ToolPlugin):
    """生成UUID"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.uuid"

    @property
    def name(self) -> str:
        return "generate_uuid"

    @property
    def description(self) -> str:
        return "生成UUID"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "count": {"type": "integer", "description": f"生成数量（1-{MAX_COUNT}）",
                          "default": 1},
            },
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        count = self.get_int_arg(args, "count", 1)
        if count < 1:
            return self.error(f"count 必须是 >= 1 的整数（当前: {count}）")
        clamped = count > MAX_COUNT
        n = MAX_COUNT if clamped else count

        out = "\n".join(str(_uuid.uuid4()) for _ in range(n))
        if clamped:
            out += f"\n（已截断：一次最多生成 {MAX_COUNT} 个，你要求的是 {count} 个）"
        return self.success(out)


# ========================================================================
# 原模块 lionbox/tools/code/yaml.py
# ========================================================================
"""YAML 校验/格式化/压缩工具（对应 Java `core/plugin/tool/code/YamlTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 OTHER）。

【实测过的坑，照抄修法】Java 侧这个工具**以前是个假的**：输入原样回显、连 action 都不读，
`action="validate"` 在一份明显写坏的 YAML 上也回"成功"，模型据此认为配置没问题 ——
谎报成功比报错危险得多。所以这里也必须**真解析**：
  * 语法错误要带"第几行第几列 + 问题 + 出错那行"；
  * 多文档（k8s 那种一个文件几个 `---`）是合法的，不能判成坏文件；
  * 空文档返回"YAML语法有效（空文档：整个输入没有任何内容）"。

【零第三方依赖】PORTING.md 硬约束：不许引入 PyYAML。这里的解析器/生成器是自己写的，
覆盖配置文件的常见写法：块映射/块序列（含紧凑 `- key: v`）、流式 `{}`/`[]`、
单双引号标量、块标量 `|`/`>`（含 `-`/`+` 与显式缩进）、锚点/别名与 `<<` 合并键、
`---`/`...` 多文档、注释。生成器按 Java 侧 SnakeYAML 2.4 的**实际输出**对齐
（缩进 2、序列不额外缩进、空集合写 `{}`/`[]`、中文原样、80 列不折行、
format=块式、minify=流式单行）—— 每条都拿真 SnakeYAML 跑过对照。
有意不做的：自定义标签（`!!str` 以外的 `!foo`）、锚点的复杂嵌套语法、时间戳类型
（日期一律按字符串处理，不会像 Java 那样还原成 `!!timestamp`）。
"""


import re
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


class YamlSyntaxError(Exception):
    """带位置的语法错误：行/列是 0 基（与 SnakeYAML 的 Mark 一致），展示时 +1。"""

    def __init__(self, problem: str, line: int | None = None, col: int = 0,
                 snippet: str | None = None) -> None:
        super().__init__(problem)
        self.problem = problem
        self.line = line
        self.col = col
        self.snippet = snippet

    def describe(self) -> str:
        out: list[str] = []
        if self.line is not None:
            out.append(f"第 {self.line + 1} 行第 {self.col + 1} 列：")
        out.append(self.problem)
        if self.snippet is not None:
            out.append("\n    " + self.snippet + "\n    " + " " * self.col + "^")
        return "".join(out)


@tool
class YamlTool(ToolPlugin):
    """YAML校验/格式化/压缩"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.code.yaml"

    @property
    def name(self) -> str:
        return "yaml_process"

    @property
    def description(self) -> str:
        return "YAML校验/格式化/压缩（真解析，语法错误会报出行列）"

    @property
    def category(self) -> str:
        return ToolCategory.CODE

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "input": {"type": "string", "description": "YAML内容"},
                "action": {"type": "string", "description":
                           "validate=只校验语法 / format=规范化缩进 / minify=压成单行流式",
                           "default": "format"},
            },
            "required": ["input"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            text = self.get_required_string_arg(args, "input")
        except ValueError as e:
            return self.error(str(e))

        action = normalize_action(self.get_string_arg(args, "action", "format"))
        if action is None:
            return self.error("未知操作: " + self.get_string_arg(args, "action", "")
                              + "。支持：validate（只校验语法）、format（格式化）、"
                                "minify（压缩成单行）")

        try:
            docs = load_all(text)
        except YamlSyntaxError as e:
            return self.error("YAML语法错误: " + e.describe())
        except Exception as e:
            return self.error("YAML解析失败: " + str(e))

        if not docs:
            return self.success("YAML语法有效（空文档：整个输入没有任何内容）")
        if action == "validate":
            return self.success(f"YAML语法有效（{len(docs)} 个文档，顶层是 "
                                f"{type_name(docs[0])}）")
        return self.success(dump(docs, action == "minify"))


def normalize_action(raw: str) -> str | None:
    """把口语化的 action 归一；认不出来的返回 None（调用方报错，而不是默默当 format）。"""
    if raw is None or raw.strip() == "":
        return "format"
    value = raw.strip().lower()
    if value in ("format", "pretty", "beautify", "格式化"):
        return "format"
    if value in ("validate", "check", "verify", "lint", "校验", "验证"):
        return "validate"
    if value in ("minify", "min", "compact", "compress", "压缩"):
        return "minify"
    return None


def type_name(value: Any) -> str:
    """对齐 Java 的 typeName（顶层类型的中文说明）。"""
    if value is None:
        return "空（null）"
    if isinstance(value, dict):
        return f"映射(Map，{len(value)} 个键)"
    if isinstance(value, list):
        return f"列表(List，{len(value)} 项)"
    if isinstance(value, str):
        return "字符串"
    if isinstance(value, bool):
        return "Boolean"
    if isinstance(value, int):
        return "Integer"
    if isinstance(value, float):
        return "Double"
    return type(value).__name__


# ==========================================================================
# 一、解析
# ==========================================================================

_NULL_WORDS = {"", "~", "null", "Null", "NULL"}
_TRUE_WORDS = {"true", "True", "TRUE", "yes", "Yes", "YES", "on", "On", "ON"}
_FALSE_WORDS = {"false", "False", "FALSE", "no", "No", "NO", "off", "Off", "OFF"}
_INT_RE = re.compile(r"^[-+]?(0b[01_]+|0x[0-9a-fA-F_]+|0o[0-7_]+|0[0-7_]+|[0-9][0-9_]*)$")
_FLOAT_RE = re.compile(r"^[-+]?(\.[0-9]+|[0-9][0-9_]*(\.[0-9_]*)?)([eE][-+]?[0-9]+)?$")
_SPECIAL_FLOAT = {"inf", "+inf", "-inf", "nan", ".inf", "+.inf", "-.inf", ".nan",
                  ".Inf", ".INF", ".NaN", ".NAN"}
_TIMESTAMP_RE = re.compile(r"^\d{4}-\d{2}-\d{2}([Tt ].*)?$")
_DOC_START = re.compile(r"^---(\s+(.*))?$")
_DOC_END = re.compile(r"^\.\.\.(\s+(.*))?$")
_KEY_RE = re.compile(r"^(\"(?:[^\"\\]|\\.)*\"|'(?:[^']|'')*'|[^:#]*?)\s*:(\s|$)")


def load_all(text: str) -> list[Any]:
    """解析整个输入，返回文档列表（与 SnakeYAML 的 `loadAll` 语义对齐）。"""
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    chunks = _split_documents(lines)
    anchors: dict[str, Any] = {}
    docs: list[Any] = []
    for entries, explicit in chunks:
        significant = [e for e in entries if _content(e[1]) != ""]
        if not significant:
            if explicit:
                docs.append(None)      # `---` 后面什么都没有 → 一个 null 文档
            continue
        parser = _ChunkParser(entries, anchors)
        docs.append(parser.parse_document())
    return docs


def _split_documents(lines: list[str]) -> list[tuple[list[tuple[int, str]], bool]]:
    chunks: list[tuple[list[tuple[int, str]], bool]] = []
    current: list[tuple[int, str]] | None = None
    explicit = False
    for no, raw in enumerate(lines):
        start = _DOC_START.match(raw)
        if start:
            current = []
            explicit = True
            chunks.append((current, True))
            body = (start.group(2) or "").strip()
            if body and not body.startswith("#"):
                current.append((no, body))
            continue
        if _DOC_END.match(raw):
            current = None
            explicit = False
            continue
        if current is None:
            current = []
            explicit = False
            chunks.append((current, False))
        current.append((no, raw))
    return chunks


def _content(raw: str) -> str:
    """去掉缩进与行尾注释后的内容（注释只在"前面是空白"时才算注释）。"""
    stripped = raw.lstrip(" ")
    if stripped.startswith("#"):
        return ""
    out: list[str] = []
    quote = ""
    i = 0
    while i < len(stripped):
        ch = stripped[i]
        if quote:
            out.append(ch)
            if ch == "\\" and quote == "\"" and i + 1 < len(stripped):
                out.append(stripped[i + 1])
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
            out.append(ch)
            i += 1
            continue
        if ch == "#" and (i == 0 or stripped[i - 1] in " \t"):
            break
        out.append(ch)
        i += 1
    return "".join(out).rstrip()


def _indent_of(raw: str, no: int) -> int:
    i = 0
    while i < len(raw) and raw[i] == " ":
        i += 1
    if i < len(raw) and raw[i] == "\t":
        raise YamlSyntaxError(
            "found character '\\t(TAB)' that cannot start any token. "
            "(Do not use \\t(TAB) for indentation)", no, 0, raw)
    return i


class _Sig:
    """一行有效内容。"""

    __slots__ = ("no", "indent", "content", "raw")

    def __init__(self, no: int, indent: int, content: str, raw: str) -> None:
        self.no = no
        self.indent = indent
        self.content = content
        self.raw = raw


class _ChunkParser:
    def __init__(self, entries: list[tuple[int, str]], anchors: dict[str, Any]) -> None:
        self.entries = entries
        self.i = 0
        self.anchors = anchors

    # ---- 行游标 ----
    def _peek(self) -> _Sig | None:
        while self.i < len(self.entries):
            no, raw = self.entries[self.i]
            content = _content(raw)
            if content == "":
                self.i += 1
                continue
            return _Sig(no, _indent_of(raw, no), content, raw)
        return None

    def _take(self) -> _Sig:
        sig = self._peek()
        if sig is None:
            raise YamlSyntaxError("意外的输入结尾")
        self.i += 1
        return sig

    # ---- 文档 ----
    def parse_document(self) -> Any:
        sig = self._peek()
        if sig is None:
            return None
        value = self._parse_node(sig.indent)
        rest = self._peek()
        if rest is not None:
            raise YamlSyntaxError("could not find expected ':'", rest.no,
                                  rest.indent, rest.raw)
        return value

    def _parse_node(self, indent: int) -> Any:
        sig = self._peek()
        if sig is None or sig.indent < indent:
            return None
        if sig.indent > indent:
            raise YamlSyntaxError("mapping values are not allowed here", sig.no,
                                  sig.indent, sig.raw)
        if _is_seq_item(sig.content):
            return self._parse_sequence(sig.indent)
        if _looks_like_mapping(sig.content):
            return self._parse_mapping(sig.indent)
        self.i += 1
        # parent_indent 传 indent-1：多行普通标量的续行只要不浅于本行就能折叠
        # （`a:\n  b\n  c` 在 SnakeYAML 里是 {a: "b c"}，续行与首行同缩进是合法的）
        return self._parse_inline(sig.content, sig.no, sig.indent, sig.indent - 1)

    # ---- 映射 ----
    def _parse_mapping(self, indent: int, first: _Sig | None = None) -> dict[str, Any]:
        result: dict[str, Any] = {}
        pending = first
        while True:
            injected = pending is not None
            sig = pending if injected else self._peek()
            pending = None
            if sig is None or sig.indent < indent:
                break
            if sig.indent > indent:
                raise _bad_indent(sig)
            if _is_seq_item(sig.content):
                break
            match = _KEY_RE.match(sig.content)
            if not match:
                raise YamlSyntaxError("could not find expected ':'", sig.no,
                                      sig.indent, sig.raw)
            if not injected:
                self.i += 1
            raw_key = match.group(1).strip()
            key = _parse_key(raw_key)
            rest = sig.content[match.end():].strip()
            value = self._parse_value(rest, indent, sig.no)
            if key == "<<":
                _merge(result, value)
            else:
                result[key] = value
        return result

    # ---- 序列 ----
    def _parse_sequence(self, indent: int, first: _Sig | None = None) -> list[Any]:
        items: list[Any] = []
        pending = first
        while True:
            injected = pending is not None
            sig = pending if injected else self._peek()
            pending = None
            if sig is None or sig.indent < indent:
                break
            if sig.indent > indent:
                raise _bad_indent(sig)
            if not _is_seq_item(sig.content):
                # 同缩进的下一行不是 "- " 项 → 这个序列到此为止，交回外层块
                # （k8s 那种 ports/env 兄弟键就长这样，不能当成错误）
                break
            if not injected:
                self.i += 1
            body = sig.content[1:]
            offset = len(body) - len(body.lstrip(" "))
            rest = body.lstrip(" ")
            col = sig.indent + 1 + offset
            if rest == "":
                nxt = self._peek()
                if nxt is not None and (nxt.indent > indent
                                        or (nxt.indent == indent and _is_seq_item(nxt.content))):
                    items.append(self._parse_node(nxt.indent))
                else:
                    items.append(None)
                continue
            if _is_seq_item(rest):
                items.append(self._parse_sequence(col, _Sig(sig.no, col, rest, sig.raw)))
                continue
            if _looks_like_mapping(rest):
                items.append(self._parse_mapping(col, _Sig(sig.no, col, rest, sig.raw)))
                continue
            items.append(self._parse_inline(rest, sig.no, col, indent))
        return items

    # ---- 值 ----
    def _parse_value(self, rest: str, indent: int, no: int) -> Any:
        if rest == "":
            nxt = self._peek()
            if nxt is None:
                return None
            if nxt.indent > indent or (nxt.indent == indent and _is_seq_item(nxt.content)):
                return self._parse_node(nxt.indent)
            return None
        return self._parse_inline(rest, no, indent + 1, indent)

    def _parse_inline(self, text: str, no: int, col: int, parent_indent: int) -> Any:
        text = text.strip()
        anchor = None
        if text.startswith("&"):
            name, _, remainder = text[1:].partition(" ")
            anchor = name.strip()
            text = remainder.strip()
            if text == "":
                nxt = self._peek()
                value = self._parse_node(nxt.indent) if nxt is not None else None
                self.anchors[anchor] = value
                return value
        if text.startswith("*"):
            name = text[1:].strip()
            if name not in self.anchors:
                raise YamlSyntaxError("undefined alias '" + name + "'", no, col, None)
            return _deep_copy(self.anchors[name])
        if text.startswith("|") or text.startswith(">"):
            value = self._parse_block_scalar(text, no, parent_indent)
        elif text.startswith("!!"):
            tag, _, remainder = text.partition(" ")
            value = _apply_tag(tag, remainder.strip(), no, col)
        elif text[0] in "{[":
            value = self._parse_flow(text, no, col)
        else:
            value = self._parse_scalar_text(text, no, col, parent_indent)
        if anchor:
            self.anchors[anchor] = value
        return value

    def _parse_flow(self, text: str, no: int, col: int) -> Any:
        """流式集合可能跨行：先把括号配平，再交给流式解析器。"""
        buffer = text
        while _brackets_open(buffer):
            nxt = self._peek()
            if nxt is None:
                break
            self.i += 1
            buffer += " " + nxt.content
        try:
            return _FlowParser(buffer, no, col).parse()
        except YamlSyntaxError as e:
            if "<stream end>" in e.problem:
                # SnakeYAML 把"流没配平"的位置报在输入结尾那一行（行号 +1、第 1 列）
                last = no
                for entry_no, raw in self.entries:
                    if raw.strip() != "":
                        last = entry_no
                raise YamlSyntaxError(e.problem, last + 1, 0, "") from None
            raise
        except Exception as e:
            raise YamlSyntaxError(str(e), no, col, None) from None

    def _parse_scalar_text(self, text: str, no: int, col: int, parent_indent: int) -> Any:
        if text[0] in "\"'":
            value, remainder = _read_quoted(text, no, col)
            if remainder.strip() != "":
                raise YamlSyntaxError("mapping values are not allowed here", no, col, None)
            return value
        if _KEY_RE.match(text) and not text.startswith(("http://", "https://")):
            raise _bad_indent(_Sig(no, col, text, text))
        _reject_stray_colon(text, no, col)
        lines = [text]
        # 多行普通标量：后续更深缩进、且不是新键/新项的行按空格折叠
        while True:
            nxt = self._peek()
            if nxt is None or nxt.indent <= parent_indent or _is_seq_item(nxt.content):
                break
            if _looks_like_mapping(nxt.content):
                break
            self.i += 1
            lines.append(nxt.content)
        if len(lines) == 1:
            return _resolve_scalar(text)
        return _resolve_scalar(" ".join(lines))

    def _parse_block_scalar(self, header: str, no: int, parent_indent: int) -> str:
        style = header[0]
        chomp = ""
        explicit = None
        for ch in header[1:]:
            if ch in "+-":
                chomp = ch
            elif ch.isdigit():
                explicit = int(ch)
            else:
                raise YamlSyntaxError(
                    f"expected chomping or indentation indicators, but found '{ch}'",
                    no, parent_indent, None)
        lines: list[str] = []
        block_indent = parent_indent + explicit if explicit else None
        parent = parent_indent
        while self.i < len(self.entries):
            raw_no, raw = self.entries[self.i]
            if _content(raw) == "" and raw.strip() == "":
                lines.append("")
                self.i += 1
                continue
            ind = _indent_of(raw, raw_no)
            if ind <= parent:
                break
            if block_indent is None:
                block_indent = ind
            lines.append(raw[block_indent:] if len(raw) > block_indent else "")
            self.i += 1
        trailing = 0
        while lines and lines[-1] == "":
            lines.pop()
            trailing += 1
        if style == ">":
            folded = ""
            for idx, line in enumerate(lines):
                if idx > 0:
                    folded += "\n" if (line == "" or lines[idx - 1] == "") else " "
                folded += line
            body = folded
        else:
            body = "\n".join(lines)
        if body == "":
            content = ""
        else:
            content = body + "\n"
        if chomp == "-":
            content = content.rstrip("\n")
        elif chomp == "+":
            content += "\n" * trailing
        return content


def _is_seq_item(content: str) -> bool:
    return content.startswith("- ") or content == "-" or content.startswith("-\t")


def _bad_indent(sig: _Sig) -> YamlSyntaxError:
    """缩进不对齐：像 SnakeYAML 一样把位置指到那一行的冒号上（没有冒号就指行首）。"""
    colon = sig.content.find(":")
    col = sig.indent + (colon if colon >= 0 else 0)
    return YamlSyntaxError("mapping values are not allowed here", sig.no, col, sig.raw)


def _looks_like_mapping(content: str) -> bool:
    if content.startswith(("http://", "https://")):
        return False
    if content.startswith(("{", "[")):
        return False        # 流式集合不是块映射（"{a: 1}" 里那个冒号不算键分隔）
    return _KEY_RE.match(content) is not None


def _reject_stray_colon(text: str, no: int, col: int) -> None:
    quote = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\" and quote == "\"":
                i += 2
                continue
            if ch == quote:
                quote = ""
            i += 1
            continue
        if ch in "\"'":
            quote = ch
        elif ch == ":" and i + 1 < len(text) and text[i + 1] == " ":
            raise YamlSyntaxError("mapping values are not allowed here", no, col + i, None)
        i += 1


def _brackets_open(text: str) -> bool:
    depth = 0
    quote = ""
    i = 0
    while i < len(text):
        ch = text[i]
        if quote:
            if ch == "\\" and quote == "\"":
                i += 2
                continue
            if ch == quote:
                quote = ""
        elif ch in "\"'":
            quote = ch
        elif ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
        i += 1
    return depth > 0


def _read_quoted(text: str, no: int, col: int) -> tuple[str, str]:
    quote = text[0]
    out: list[str] = []
    i = 1
    while i < len(text):
        ch = text[i]
        if quote == "'":
            if ch == "'":
                if i + 1 < len(text) and text[i + 1] == "'":
                    out.append("'")
                    i += 2
                    continue
                return "".join(out), text[i + 1:]
            out.append(ch)
            i += 1
            continue
        if ch == "\\":
            if i + 1 >= len(text):
                break
            esc = text[i + 1]
            simple = {"n": "\n", "t": "\t", "r": "\r", "0": "\0", "a": "\a", "b": "\b",
                      "f": "\f", "v": "\v", "e": "\x1b", "\\": "\\", "\"": "\"",
                      "/": "/", " ": " ", "N": "\u0085", "_": "\u00a0",
                      "L": "\u2028", "P": "\u2029"}
            if esc in simple:
                out.append(simple[esc])
                i += 2
                continue
            if esc in "xuU":
                width = {"x": 2, "u": 4, "U": 8}[esc]
                digits = text[i + 2:i + 2 + width]
                if len(digits) == width and all(c in "0123456789abcdefABCDEF" for c in digits):
                    out.append(chr(int(digits, 16)))
                    i += 2 + width
                    continue
                raise YamlSyntaxError("expected escape sequence of " + str(width)
                                      + " hexadecimal numbers", no, col, None)
            raise YamlSyntaxError("found unknown escape character '" + esc + "'", no, col, None)
        if ch == quote:
            return "".join(out), text[i + 1:]
        out.append(ch)
        i += 1
    raise YamlSyntaxError("found unexpected end of stream", no, col, None)


def _apply_tag(tag: str, text: str, no: int, col: int) -> Any:
    name = tag[2:].lower()
    if name == "str":
        if text[:1] in "\"'":
            value, _ = _read_quoted(text, no, col)
            return value
        return _content(text)
    if name == "null":
        return None
    if name == "bool":
        return text.strip().lower() in ("true", "yes", "on", "1")
    if name == "int":
        return int(text.strip(), 0)
    if name == "float":
        return float(text.strip())
    raise YamlSyntaxError("不支持的 YAML 标签: " + tag, no, col, None)


def _parse_key(raw: str) -> Any:
    """键按 YAML 规则解析出**原生类型**（1 是整数、true 是布尔），生成时才不会乱加引号。"""
    if raw[:1] in "\"'":
        value, _ = _read_quoted(raw, 0, 0)
        return value
    return _resolve_scalar(raw)


def _resolve_scalar(text: str) -> Any:
    """按 YAML 1.1 的解析规则（SnakeYAML 用的那套）推断类型。"""
    if text in _NULL_WORDS:
        return None
    if text in _TRUE_WORDS:
        return True
    if text in _FALSE_WORDS:
        return False
    if _INT_RE.match(text):
        body = text.replace("_", "")
        sign = -1 if body.startswith("-") else 1
        digits = body.lstrip("+-")
        if digits.startswith(("0b", "0B")):
            return sign * int(digits[2:], 2)
        if digits.startswith(("0x", "0X")):
            return sign * int(digits[2:], 16)
        if digits.startswith(("0o", "0O")):
            return sign * int(digits[2:], 8)
        if len(digits) > 1 and digits.startswith("0") and digits[1:].isalnum() \
                and all(c in "01234567_" for c in digits[1:]):
            # 【只有整串都是八进制数字才按八进制】_INT_RE 的兜底分支 `[0-9][0-9_]*`
            # 会把 "09"、"09123456789" 也认成整数（首字符是 0 就行），直接
            # int("09", 8) 抛 ValueError → 合法 YAML（port: 09、工号/电话）被判语法错误。
            # 08/09 这种 SnakeYAML 是按**十进制**解析的，这里回退到下面的十进制分支。
            return sign * int(digits, 8)
        return int(body, 10)
    if text in _SPECIAL_FLOAT:
        low = text.lower()
        if "nan" in low:
            return float("nan")
        return float("-inf") if low.startswith("-") else float("inf")
    if _FLOAT_RE.match(text):
        return float(text.replace("_", ""))
    return text


class _FlowParser:
    """流式集合解析器：`{a: 1, b: [1, 2]}` / `[1, 'x']`。"""

    def __init__(self, text: str, no: int, col: int) -> None:
        self.text = text
        self.pos = 0
        self.no = no
        self.col = col

    def parse(self) -> Any:
        value = self._value()
        self._skip_ws()
        if self.pos < len(self.text):
            raise YamlSyntaxError(
                "expected ',' or ']', but got " + repr(self.text[self.pos]), self.no, self.col, None)
        return value

    def _skip_ws(self) -> None:
        while self.pos < len(self.text) and self.text[self.pos] in " \t":
            self.pos += 1

    def _value(self) -> Any:
        self._skip_ws()
        if self.pos >= len(self.text):
            raise YamlSyntaxError("expected a value, but got <stream end>", self.no, self.col, None)
        ch = self.text[self.pos]
        if ch == "{":
            return self._mapping()
        if ch == "[":
            return self._sequence()
        if ch in "\"'":
            value, remainder = _read_quoted(self.text[self.pos:], self.no, self.col)
            consumed = len(self.text) - self.pos - len(remainder)
            self.pos += consumed
            return value
        return self._plain()

    def _plain(self) -> Any:
        start = self.pos
        quote = ""
        depth = 0
        while self.pos < len(self.text):
            ch = self.text[self.pos]
            if quote:
                if ch == "\\" and quote == "\"":
                    self.pos += 2
                    continue
                if ch == quote:
                    quote = ""
            elif ch in "\"'":
                quote = ch
            elif ch in "{[":
                depth += 1
            elif ch in "}]":
                if depth == 0:
                    break
                depth -= 1
            elif ch == "," and depth == 0:
                break
            elif ch == ":" and depth == 0 and self.pos + 1 < len(self.text) \
                    and self.text[self.pos + 1] in " \t":
                break
            self.pos += 1
        return _resolve_scalar(self.text[start:self.pos].strip())

    def _mapping(self) -> dict[str, Any]:
        self.pos += 1     # '{'
        result: dict[str, Any] = {}
        while True:
            self._skip_ws()
            if self.pos >= len(self.text):
                raise YamlSyntaxError("expected ',' or '}', but got <stream end>",
                                      self.no, self.col, None)
            if self.text[self.pos] == "}":
                self.pos += 1
                return result
            key = self._key()
            self._skip_ws()
            if self.pos >= len(self.text) or self.text[self.pos] != ":":
                raise YamlSyntaxError("expected ':' but got <stream end>",
                                      self.no, self.col, None)
            self.pos += 1
            value = self._value()
            if key == "<<":
                _merge(result, value)
            else:
                result[key] = value
            self._skip_ws()
            if self.pos < len(self.text) and self.text[self.pos] == ",":
                self.pos += 1
                continue
            if self.pos < len(self.text) and self.text[self.pos] == "}":
                self.pos += 1
                return result
            raise YamlSyntaxError("expected ',' or '}', but got <stream end>",
                                  self.no, self.col, None)

    def _key(self) -> str:
        self._skip_ws()
        if self.pos < len(self.text) and self.text[self.pos] in "\"'":
            value, remainder = _read_quoted(self.text[self.pos:], self.no, self.col)
            self.pos += len(self.text) - self.pos - len(remainder)
            return value
        start = self.pos
        while self.pos < len(self.text) and self.text[self.pos] != ":":
            self.pos += 1
        return _parse_key(self.text[start:self.pos].strip())

    def _sequence(self) -> list[Any]:
        self.pos += 1     # '['
        items: list[Any] = []
        while True:
            self._skip_ws()
            if self.pos >= len(self.text):
                raise YamlSyntaxError("expected ',' or ']', but got <stream end>",
                                      self.no, self.col, None)
            if self.text[self.pos] == "]":
                self.pos += 1
                return items
            items.append(self._value())
            self._skip_ws()
            if self.pos < len(self.text) and self.text[self.pos] == ",":
                self.pos += 1
                continue
            if self.pos < len(self.text) and self.text[self.pos] == "]":
                self.pos += 1
                return items
            raise YamlSyntaxError("expected ',' or ']', but got <stream end>",
                                  self.no, self.col, None)


def _merge(target: dict[str, Any], value: Any) -> None:
    """`<<` 合并键：已有的键优先（与 SnakeYAML 的 merge 语义一致）。"""
    sources = value if isinstance(value, list) else [value]
    for source in sources:
        if isinstance(source, dict):
            for key, item in source.items():
                target.setdefault(key, item)


def _deep_copy(value: Any) -> Any:
    if isinstance(value, dict):
        return {k: _deep_copy(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_deep_copy(v) for v in value]
    return value


# ==========================================================================
# 二、生成（按 SnakeYAML 2.4 的实际输出对齐）
# ==========================================================================

_PLAIN_BAD_FIRST = set("-?:,[]{}#&*!|>'\"%@`")
_ESCAPES = {"\\": "\\\\", "\"": "\\\"", "\n": "\\n", "\t": "\\t", "\r": "\\r",
            "\0": "\\0", "\a": "\\a", "\b": "\\b", "\f": "\\f", "\v": "\\v",
            "\x1b": "\\e"}


def dump(docs: list[Any], minify: bool) -> str:
    """dumpAll + 去掉末尾一个换行（与 Java 侧 YamlTool.dump 同一套动作）。"""
    chunks: list[str] = []
    for index, doc in enumerate(docs):
        body = _emit_flow(doc) if minify else _emit_block(doc, 0)
        if index > 0:
            body = ("--- " + body) if minify else ("---\n" + body)
        chunks.append(body + "\n")
    text = "".join(chunks)
    return text[:-1] if text.endswith("\n") else text


def _emit_block(value: Any, indent: int) -> str:
    if isinstance(value, dict):
        return _emit_block_map(value, indent) if value else "{}"
    if isinstance(value, list):
        return _emit_block_seq(value, indent) if value else "[]"
    return _block_scalar(value, indent)


def _emit_block_map(value: dict[Any, Any], indent: int) -> str:
    lines = []
    for key, item in value.items():
        lines.append(" " * indent + _emit_key(key) + ":" + _emit_block_child(item, indent))
    return "\n".join(lines)


def _emit_block_child(value: Any, indent: int) -> str:
    if isinstance(value, dict):
        return " {}" if not value else "\n" + _emit_block_map(value, indent + 2)
    if isinstance(value, list):
        return " []" if not value else "\n" + _emit_block_seq(value, indent)
    return " " + _block_scalar(value, indent)


def _emit_block_seq(items: list[Any], indent: int) -> str:
    lines = []
    for item in items:
        if isinstance(item, dict) and item:
            body = _emit_block_map(item, indent + 2).split("\n")
            body[0] = " " * indent + "- " + body[0][indent + 2:]
            lines.append("\n".join(body))
        elif isinstance(item, list) and item:
            body = _emit_block_seq(item, indent + 2).split("\n")
            body[0] = " " * indent + "- " + body[0][indent + 2:]
            lines.append("\n".join(body))
        elif isinstance(item, dict):
            lines.append(" " * indent + "- {}")
        elif isinstance(item, list):
            lines.append(" " * indent + "- []")
        else:
            lines.append(" " * indent + "- " + _block_scalar(item, indent))
    return "\n".join(lines)


def _block_scalar(value: Any, indent: int) -> str:
    if isinstance(value, str) and "\n" in value and _literal_ok(value):
        return _literal_block(value, indent)
    return _scalar_text(value, flow=False)


def _literal_ok(text: str) -> bool:
    if "\t" in text:
        return False
    body = text[:-1] if text.endswith("\n") else text
    for line in body.split("\n"):
        if line != line.rstrip() or line.startswith(" "):
            return False
        if any(ord(ch) < 0x20 for ch in line):
            return False
    return True


def _literal_block(text: str, indent: int) -> str:
    if text.endswith("\n\n"):
        indicator, body = "|+", text[:-1]
    elif text.endswith("\n"):
        indicator, body = "|", text[:-1]
    else:
        indicator, body = "|-", text
    pad = " " * (indent + 2)
    lines = [pad + line if line else "" for line in body.split("\n")]
    return indicator + "\n" + "\n".join(lines)


def _emit_flow(value: Any) -> str:
    if isinstance(value, dict):
        if not value:
            return "{}"
        return "{" + ", ".join(
            _emit_key(k, flow=True) + ": " + _emit_flow(v) for k, v in value.items()) + "}"
    if isinstance(value, list):
        if not value:
            return "[]"
        return "[" + ", ".join(_emit_flow(v) for v in value) + "]"
    return _scalar_text(value, flow=True)


def _emit_key(key: Any, flow: bool = False) -> str:
    if key is None:
        return "null"
    if key is True:
        return "true"
    if key is False:
        return "false"
    if isinstance(key, (int, float)):
        return _scalar_text(key, flow=flow)
    return _scalar_text(str(key), flow=flow)


def _scalar_text(value: Any, flow: bool) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, float):
        if value != value:
            return ".nan"
        if value == float("inf"):
            return ".inf"
        if value == float("-inf"):
            return "-.inf"
        text = repr(value)
        return text if "." in text or "e" in text or "E" in text else text + ".0"
    text = str(value)
    if _needs_quote(text, flow):
        if _can_double_quote(text):
            return _double_quote(text)
        return "'" + text.replace("'", "''") + "'"
    return text


def _needs_quote(text: str, flow: bool) -> bool:
    if text == "":
        return True
    if text != text.strip():
        return True
    if any(ord(ch) < 0x20 for ch in text):
        return True
    if _resolves_elsewhere(text):
        return True
    if ": " in text or text.endswith(":") or " #" in text:
        return True
    if flow and any(ch in ",[]{}:" for ch in text):
        return True
    first = text[0]
    if first in "-?:":
        return len(text) == 1 or text[1] in " \t"
    return first in _PLAIN_BAD_FIRST


def _can_double_quote(text: str) -> bool:
    for ch in text:
        code = ord(ch)
        if code < 0x20 or ch in "\\\"":
            return True
        if 0x7F <= code <= 0x9F or code in (0x2028, 0x2029):
            return True
    return False


def _resolves_elsewhere(text: str) -> bool:
    """这些字符串不加引号会被读成别的类型（SnakeYAML 就是这么引起来的）。"""
    if text in _NULL_WORDS or text in _TRUE_WORDS or text in _FALSE_WORDS:
        return True
    if text in _SPECIAL_FLOAT:
        return True
    if _INT_RE.match(text) or _FLOAT_RE.match(text):
        return True
    return _TIMESTAMP_RE.match(text) is not None


def _double_quote(text: str) -> str:
    out = ['"']
    for ch in text:
        if ch in _ESCAPES:
            out.append(_ESCAPES[ch])
        elif ord(ch) < 0x20 or 0x7F <= ord(ch) <= 0x9F or ord(ch) in (0x2028, 0x2029):
            out.append("\\x%02x" % ord(ch) if ord(ch) < 0x100 else "\\u%04x" % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


# ========================================================================
# 原模块 lionbox/tools/code.py
# ========================================================================
"""编解码类工具（对应 Java 包 `core/plugin/tool/code`，14 个工具）。

【显式登记，不做目录扫描】导入本包即把 14 个工具类通过 `@tool` 登记进
`lionbox.plugins.base.TOOL_CLASSES`；启动路径上不会去遍历文件系统（PORTING.md 硬约束）。

id / name / description / parameters_schema 与 Java 版逐字一致；
minimal_mode 对齐 Java 的 `AbstractToolPlugin.isAvailableInMode(MINIMAL)`：
这一批在 Java 里类别都是 `OTHER`，不属于"文件类 + shell 类"，所以极简模式一律不开放。
"""



__all__ = [
    "Base64Tool",
    "CodeFormatTool",
    "CronTool",
    "DiffTool",
    "EscapeTool",
    "HashTool",
    "JsonTool",
    "MarkdownTool",
    "NumberTool",
    "RegexTool",
    "StringTool",
    "TimestampTool",
    "UuidTool",
    "YamlTool",
]


# ========================================================================
# 原模块 lionbox/tools/git/_git.py
# ========================================================================
"""git 工具共用的底座。

【契约来源】逐项对照 Java 版 `AbstractToolPlugin`：
  - `gitExecutable()`        → `executable()`
  - `gitEnv(ProcessBuilder)` → `env()`
  - `drainAndWait(...)`      → `run(...)` / `run_checked(...)`
  - `isEmptyRepository(dir)` → `is_empty_repository(dir)`
  - `checkGitDirectory(…)`   → `check_directory(…)`
  - `gitHint(exception)`     → `hint(text)`

【为什么这些必须抽出来共用】Java 版那几条注释记录的都是实测踩过的坑，
一条都不能在移植时丢掉：

1. **不能直接写 `git`**：Lion Code 是从开始菜单/注册表拉起来的 GUI 程序，PATH 常常比
   用户终端里的短，`ProcessBuilder("git")` 可能找不到；用户也可能用的是便携版 Git。
   所以按 `GIT_EXE` → PATH → 常见安装位置 的顺序找。
2. **绝不等凭据**：`git remote show origin` 会去连远端，要凭据时 git 会交互式等输入，
   工具就永远挂在那里（Java 侧实测卡了 3 分多钟）。装上 `GIT_TERMINAL_PROMPT=0` 等
   几个变量后，git 遇到需要凭据就直接失败返回。
3. **边读边等，不能"先等再读"**：`waitFor(30s)` → `readAllBytes()` 会变成有界缓冲区死锁 ——
   子进程输出写满 OS 管道（约 4-8KB，几百行 diff 就到了）就阻塞在 write 上永不退出。
   `subprocess.run` 内部就是并发排空，所以这里用它，而不是 `Popen.wait()` + `read()`。
4. **超时必须能强杀**：`git add` 超时后若丢掉进程引用，那个进程会一直攥着 `.git/index.lock`，
   后面的 commit 全部失败。`subprocess.run(timeout=…)` 会 kill 并 wait 干净。
5. **中文路径与输出编码**：git 在 Windows 上按控制台代码页输出，中文文件名要按 UTF-8 解；
   严格解不出来再退 GBK，最后才是替换字符（`decode_text`）。
"""


import os
import shutil
import subprocess
import sys
from pathlib import Path

#: git 命令的输出编码：UTF-8 → GBK → 替换字符（与 Java 版 decodeText 同一顺序）
_GIT_DECODE_ORDER = ("utf-8", "gbk")

#: `is_empty_repository` 的探测超时（秒），对应 Java 的 drainAndWait(p, 10, …)
_EMPTY_REPO_TIMEOUT = 10

_cached_executable: str | None = None


def executable() -> str:
    """找到 git 可执行文件：`GIT_EXE` → PATH → 常见安装位置 → 交给 PATH。"""
    global _cached_executable
    if _cached_executable is not None:
        return _cached_executable

    from_env = os.environ.get("GIT_EXE", "").strip()
    if from_env and Path(from_env).is_file():
        _cached_executable = from_env
        return _cached_executable

    candidates = [
        r"C:\Program Files\Git\cmd\git.exe",
        r"C:\Program Files (x86)\Git\cmd\git.exe",
        r"C:\Program Files\Git\bin\git.exe",
    ]
    local = os.environ.get("LOCALAPPDATA")
    if local:
        candidates.append(str(Path(local) / "Programs" / "Git" / "cmd" / "git.exe"))
    for candidate in candidates:
        if Path(candidate).is_file():
            _cached_executable = candidate
            return _cached_executable

    found = shutil.which("git")            # PATH 里能问到就用它（非 Windows 上基本都走这里）
    _cached_executable = found or "git"
    return _cached_executable


def env() -> dict[str, str]:
    """给 git 的进程加上"绝不等凭据"的环境（见模块头注释第 2 条）。"""
    full = dict(os.environ)
    full.update({
        "GIT_TERMINAL_PROMPT": "0",
        "GIT_ASKPASS": "echo",
        "SSH_ASKPASS": "echo",
        "GCM_INTERACTIVE": "never",
        "GIT_OPTIONAL_LOCKS": "0",
    })
    return full


def decode_text__tools_git__git(raw: bytes) -> str:
    """按 UTF-8 → GBK → 替换字符 的顺序解码命令输出。

    【注意】`bytes.decode("utf-8")` 默认不抛异常（非法字节变 U+FFFD），拿它当"先试 UTF-8"
    用会把 GBK 输出解成乱码却看不出错。所以必须用严格模式：真抛了才说明不是 UTF-8。
    """
    for encoding in _GIT_DECODE_ORDER:
        try:
            return raw.decode(encoding)
        except (UnicodeDecodeError, LookupError):
            continue
    return raw.decode("utf-8", errors="replace")


def run(args: list[str], cwd: str | Path | None,
        timeout: int) -> tuple[int, str] | None:
    """在 `cwd` 里跑一条 git 命令，返回 `(exit_code, 合并输出)`；超时返回 `None`。

    超时时进程已被强杀并回收（见模块头注释第 4 条），调用方据此给出可读提示。

    起不来时（目录不存在、没装 git、没权限）抛 `OSError`：调用方按 Java 版的
    老路径接住它 → `error("…失败: " + 原始消息 + hint(消息))`，也就是模型能照着改的提示。
    """
    try:
        completed = subprocess.run(
            [executable(), *args],
            cwd=str(cwd) if cwd else None,
            env=env(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,          # 与 Java 的 redirectErrorStream(true) 一致
            timeout=timeout,
            creationflags=(0x08000000 if sys.platform == "win32" else 0),
        )
    except subprocess.TimeoutExpired:
        # 【这里必须接】subprocess.run 超时是 **kill + raise**，从不返回 None ——
        # 不接的话文档里"超时返回 None"和 13 处 `result is None` 分支全是恒假死代码，
        # 超时会一路冒到最外层 except，模型看到的是英文
        # "Command '[…]' timed out after 30 seconds"，写好的中文提示永远出不来。
        # 进程已被 subprocess.run 杀干净并回收，直接按契约返回 None 即可。
        return None
    return completed.returncode, decode_text__tools_git__git(completed.stdout or b"")


def hint(text: str) -> str:
    """把 git 相关异常翻译成"能照着做"的提示（对应 Java 的 `gitHint`）。

    Java 侧实测：在还没建的目录里跑 git，模型看到 `CreateProcess error=267, 目录名称无效`，
    据此得出"本机没装 git"的错误结论，后面一连串 git 工具都不敢用了。
    """
    message = text or ""
    if "267" in message or "目录名称无效" in message or "Invalid directory" in message \
            or "The directory name is invalid" in message:
        return ("。这次操作的**目录不存在**（不是没装 git）：先用 create_directory 建目录，"
                "或者直接用 git_init（它会自动建）")
    if 'Cannot run program "git"' in message or "CreateProcess error=2," in message \
            or "找不到指定的文件" in message or "No such file or directory" in message:
        return ("。没找到 git 可执行文件：装一个 Git for Windows，"
                "或用 GIT_EXE 环境变量指定 git.exe 的路径")
    return ""


def check_directory(path: str | Path) -> str | None:
    """跑 git 命令前的目录检查：目录不存在时给出能照着做的错误（对应 `checkGitDirectory`）。"""
    if not Path(path).is_dir():
        return ("目录不存在: " + str(path) + "（先用 create_directory 建目录，或直接 git_init 建仓库；"
                "git 命令必须在真实存在的目录里执行）")
    return None


def is_empty_repository(directory: str | Path) -> bool:
    """这个仓库是不是"空仓库"（初始化过、但还没有任何提交）。

    判据：`git rev-parse --verify HEAD` 失败 —— 没有提交时 HEAD 指向不存在的 master，
    所以 `git branch <名字>` 会报 `fatal: not a valid object name: 'master'`。
    认识这个状态，工具才能改成做真正有用的事（checkout -b）。
    """
    try:
        result = run(["rev-parse", "--verify", "HEAD"], directory, _EMPTY_REPO_TIMEOUT)
    except Exception:                      # noqa: BLE001 —— 探测失败一律当"非空仓库"，与 Java 一致
        return False
    if result is None:
        return False                       # 超时（run 已强杀）
    return result[0] != 0


# ========================================================================
# 原模块 lionbox/tools/git/git_branch.py
# ========================================================================
"""Git 分支管理工具（Java: core/plugin/tool/git/GitBranchTool.java）。

两个实测坑都保住：
  - **空仓库**（还没有任何提交）里 `git branch foo` 只回
    "fatal: not a valid object name: 'master'"（master 还不存在，新分支没有可指向的提交）。
    空仓库下唯一有意义的做法是 `checkout -b`（建好并切过去），这里代它做掉。
  - 模型"把工具试一遍"时会重复建同名分支、或删一个它刚删过的分支，
    这两件事的结果本来就已经是它想要的，直接当成功回。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_GIT_TIMEOUT = 30
_BRANCH_PROBE_TIMEOUT = 15        # 对应 Java 的 drainAndWait(p, 15, UTF_8)


@tool
class GitBranchTool(ToolPlugin):
    """查看、创建、切换 Git 分支。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.branch"

    @property
    def name(self) -> str:
        return "git_branch"

    @property
    def description(self) -> str:
        return "查看、创建、切换Git分支"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        # Java 的 GitBranchTool 没有覆盖 getRequiredPermission() → 基类默认 WORKSPACE_WRITE
        # （create/checkout/delete 都在动仓库）。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "仓库路径"},
                "action": {"type": "string", "description": "list/create/checkout/delete"},
                "branch": {"type": "string", "description": "分支名"},
            },
            "required": ["path", "action"],
        }

    def branch_exists(self, directory: str, branch: str) -> bool:
        """本地有没有这个分支（`git branch --list <名字>` 输出非空就是有）。"""
        try:
            result = _git.run(["branch", "--list", branch], directory, _BRANCH_PROBE_TIMEOUT)
        except Exception:                              # noqa: BLE001 —— 与 Java 一致：问不出来当没有
            return False
        if result is None:
            return False                               # 超时（已强杀）：当成"没这个分支"
        # 【退出码也要看】非仓库目录里这条命令 exit=128、stderr 是 "fatal: not a git
        # repository"（stderr 已合并到 result[1]），只看"输出非空"会把 fatal 当成
        # "分支已存在" → create 直接回"分支已存在，无需重复创建"，仓库根本没动。
        return result[0] == 0 and bool(result[1].strip())

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            action = self.get_required_string_arg(args, "action").strip().lower()
            branch = self.get_string_arg(args, "branch", "") or ""

            dir_error = _git.check_directory(path)
            if dir_error is not None:
                return self.error(dir_error)
            if not branch.strip():
                branch = self.get_string_arg(args, "name", "") or ""

            if action in ("create", "checkout"):
                if not branch.strip():
                    return self.error("缺少分支名：action=" + action
                                      + " 要带 branch 参数（例如 branch=dev）")
                if _git.is_empty_repository(path):
                    result = _git.run(["checkout", "-b", branch], path, _GIT_TIMEOUT)
                    if result is None:
                        return self.error("git 命令超时（30 秒没返回）")
                    exit_code, output = result
                    if exit_code == 0:
                        return self.success(
                            "仓库还没有任何提交，已直接创建并切换到分支 " + branch
                            + "（空仓库里 git branch 建不出分支，所以用 checkout -b；"
                            + "git_commit 一次之后再 git_branch list 就能看到它）\n" + output)
                    return self.error("创建分支失败（退出码 " + str(exit_code) + "）:\n" + output)

            if action == "create" and self.branch_exists(path, branch):
                return self.success("分支已存在，无需重复创建: " + branch)
            if action == "delete" and not self.branch_exists(path, branch):
                return self.success("分支本来就不存在（无需删除）: " + branch)

            if action == "list":
                command = ["branch", "-a"]
            elif action == "create":
                command = ["branch", branch]
            elif action == "checkout":
                command = ["checkout", branch]
            elif action == "delete":
                command = ["branch", "-d", branch]
            else:
                return self.error("未知操作: " + action + "（支持 list / create / checkout / delete）")

            result = _git.run(command, path, _GIT_TIMEOUT)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据。"
                                  "远程操作用 -n 只看本地配置，或先确认网络/凭据。")
            # 【必须看退出码】checkout 一个不存在的分支（pathspec 'typo' did not match）、
            # branch -d 删未合并分支（not fully merged）、非仓库目录（fatal: not a git
            # repository）全是 exit!=0 —— 原来这里一律 self.success，模型以为已切换/已删除，
            # 后续步骤全建立在假状态上（同文件 git_log 早就写了这条，这里补齐）。
            exit_code, output = result
            if exit_code != 0:
                if "not a git repository" in output:
                    return self.error("这不是 git 仓库（先 git_init）:\n" + output)
                return self.error("git " + " ".join(command)
                                  + " 失败（退出码 " + str(exit_code) + "）:\n" + output)
            return self.success(output if output else "操作完成")
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git分支操作失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_commit.py
# ========================================================================
"""Git提交工具（Java: core/plugin/tool/git/GitCommitTool.java）。

先 `git add -A`（addAll 默认 true）再 `git commit -m <message>`。
两个实测坑都在这里保住：
  - add 那一步也必须带 gitEnv + 排空输出 + 超时强杀，否则超时后进程会攥着
    `.git/index.lock`，后面的 commit 直接失败；
  - 机器上没配 user.name/user.email 时 commit 会报 "Please tell me who you are"，
    所以带一组本地兜底身份，不让用户先手动配置。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_GIT_TIMEOUT__tools_git_git_commit = 30


@tool
class GitCommitTool(ToolPlugin):
    """暂存并提交更改。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.commit"

    @property
    def name(self) -> str:
        return "git_commit"

    @property
    def description(self) -> str:
        return "Git暂存并提交更改"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        # 与 Java 一致：GitCommitTool 没有覆盖 getRequiredPermission()，取 AbstractToolPlugin
        # 的默认值 WORKSPACE_WRITE。这里显式写出来 —— Python 基类的默认值是 READ_ONLY，
        # 不写就会把"提交"标成只读。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Git仓库路径"},
                "message": {"type": "string", "description": "提交信息"},
                "addAll": {"type": "boolean", "description": "是否暂存所有更改", "default": True},
            },
            "required": ["path", "message"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            message = self.get_required_string_arg(args, "message")
            # 【键不存在 = true，显式给了 false 才是 false】与 Java 的
            # `!arguments.containsKey("addAll") || getBoolArg(…)` 同语义。
            add_all = args.get("addAll") is None or self.get_bool_arg(args, "addAll", False)

            if add_all:
                added = _git.run(["add", "-A"], path, _GIT_TIMEOUT__tools_git_git_commit)
                if added is None:
                    return self.error(
                        "git add 超时（30 秒没返回），已终止；请检查是否有文件被占用或索引被锁。")

            result = _git.run(
                ["-c", "user.name=Lion Code Agent",
                 "-c", "user.email=agent@lionbox.local",
                 "commit", "-m", message],
                path, _GIT_TIMEOUT__tools_git_git_commit)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据")

            exit_code, output = result
            if exit_code == 0:
                return self.success("提交成功:\n" + output)
            # "没有改动"不是错误：报成错误会让模型以为参数写错了、反复重试（用户那次连试三次）。
            if ("nothing to commit" in output or "no changes added" in output
                    or "nothing added to commit" in output):
                return self.success("（没有需要提交的改动：工作区是干净的，不用再试）")
            if "not a git repository" in output:
                return self.error("这不是 git 仓库（先 git_init）:\n" + output)
            return self.error("提交失败:\n" + output)
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git提交失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_diff.py
# ========================================================================
"""Git差异查看工具（Java: core/plugin/tool/git/GitDiffTool.java）。

【坑】文件路径必须放在 `--` 后面。直接当位置参数传的话 git 会把它当成 revision
去解析，实测报 `fatal: ambiguous argument 'x.txt'` —— 用户那次 git_diff 就是这么失败的。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_GIT_TIMEOUT__tools_git_git_diff = 30


@tool
class GitDiffTool(ToolPlugin):
    """查看 Git 文件差异。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.diff"

    @property
    def name(self) -> str:
        return "git_diff"

    @property
    def description(self) -> str:
        return "查看Git文件差异"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Git仓库路径"},
                "file": {"type": "string", "description": "指定文件（可选，会自动放到 -- 后面）"},
                "rev": {"type": "string", "description": "版本/范围（可选），如 HEAD~1、main..dev"},
                "cached": {"type": "boolean", "description": "查看暂存区差异", "default": False},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            file = self.get_string_arg(args, "file", "") or ""
            cached = self.get_bool_arg(args, "cached", False)
            rev = self.get_string_arg(args, "rev", "") or ""

            command = ["diff"]
            if cached:
                command.append("--cached")
            if rev.strip():
                command.append(rev)        # 例如 HEAD~1 或 main..dev
            if file.strip():
                command.append("--")       # 见模块头注释：文件路径必须在 -- 后面
                command.append(file)

            result = _git.run(command, path, _GIT_TIMEOUT__tools_git_git_diff)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据。"
                                  "远程操作用 -n 只看本地配置，或先确认网络/凭据。")
            # 【必须看退出码】rev 写错时 git diff 是 exit=128 + "fatal: ambiguous
            # argument 'xyz'"，非仓库目录同样是 128 —— 原来把这段 fatal 文本当"差异内容"
            # success 吐回去，模型会照着分析一段根本不是 diff 的报错文本。
            exit_code, output = result
            if exit_code != 0:
                # 已知文案按**小写**比对：git 对 `diff` 在非仓库里回的是
                # "warning: Not a git repository"（大写 N）+ 退出码 129，
                # 只匹配小写会漏掉、退化成一句没有指向的"失败"。
                low = output.lower()
                if "ambiguous argument" in low:
                    return self.error("rev 没解析出来（写错了？例如 HEAD~1 / main..dev）:\n"
                                      + output)
                if "not a git repository" in low:
                    return self.error("这不是 git 仓库（先 git_init）:\n" + output)
                return self.error("git diff 失败（退出码 " + str(exit_code) + "）:\n" + output)
            return self.success(output if output else "（无差异）")
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git差异获取失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_init.py
# ========================================================================
"""Git初始化工具（Java: core/plugin/tool/git/GitInitTool.java）。

【实测】模型会直接 git_init 到一个还不存在的目录（.git_test），结果 ProcessBuilder 报
error=267 目录名称无效，它还以为是"没装 git"。git init 到新目录本来就是正常用法，
所以这里直接 `mkdir -p` 建出来。
"""


from pathlib import Path
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_GIT_TIMEOUT__tools_git_git_init = 30


@tool
class GitInitTool(ToolPlugin):
    """初始化 Git 仓库。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.init"

    @property
    def name(self) -> str:
        return "git_init"

    @property
    def description(self) -> str:
        return "初始化Git仓库"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        # Java 的 GitInitTool 没有覆盖 getRequiredPermission() → 取基类默认 WORKSPACE_WRITE。
        # 它在目标目录里写 .git/，显式写出来才不会在 Python 侧被默认成只读。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "目录路径"},
                "bare": {"type": "boolean", "description": "是否创建裸仓库", "default": False},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            bare = self.get_bool_arg(args, "bare", False)
            Path(path).mkdir(parents=True, exist_ok=True)   # 对应 Java 的 Files.createDirectories

            command = ["init", "--bare"] if bare else ["init"]
            result = _git.run(command, path, _GIT_TIMEOUT__tools_git_git_init)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据。"
                                  "远程操作用 -n 只看本地配置，或先确认网络/凭据。")
            # 【退出码不能丢】目录只读/被占用/已有损坏的 .git 时 init 会 exit!=0，
            # 原来照样拼上 "Git仓库已初始化:\n<fatal...>" —— 明确的谎报成功。
            exit_code, output = result
            if exit_code != 0:
                return self.error("Git初始化失败（退出码 " + str(exit_code) + "）:\n"
                                  + output + _git.hint(output))
            return self.success("Git仓库已初始化:\n" + output)
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git初始化失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_log.py
# ========================================================================
"""Git日志查看工具（Java: core/plugin/tool/git/GitLogTool.java）。

【坑】必须看退出码，不能把 git 的 fatal 当成功吐回去：空仓库会回一句
"fatal: your current branch 'master' does not have any commits yet"，
模型看不懂就反复重试（用户那次连试了三次）。这里按已知的 fatal 文案分流。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_GIT_TIMEOUT__tools_git_git_log = 30


@tool
class GitLogTool(ToolPlugin):
    """查看 Git 提交历史。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.log"

    @property
    def name(self) -> str:
        return "git_log"

    @property
    def description(self) -> str:
        return "查看Git提交历史"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Git仓库路径"},
                "count": {"type": "integer", "description": "显示条数", "default": 20},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            count = self.get_int_arg(args, "count", 20)

            result = _git.run(["log", "--oneline", "-" + str(count)], path, _GIT_TIMEOUT__tools_git_git_log)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据。"
                                  "远程操作用 -n 只看本地配置，或先确认网络/凭据。")

            exit_code, output = result
            output = output.strip()
            if exit_code != 0:
                if ("does not have any commits" in output or "unknown revision" in output
                        or "bad default revision" in output):
                    return self.success("（这个仓库还没有任何提交：先 create_file 建个文件，再 git_commit）")
                if "not a git repository" in output:
                    return self.error("这不是 git 仓库：" + str(path) + "（先 git_init，path 指向工作区目录）")
                return self.error("git log 失败:\n" + output)
            return self.success(output if output else "（无提交记录）")
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git日志获取失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_remote.py
# ========================================================================
"""Git Remote 管理工具（Java: core/plugin/tool/git/GitRemoteTool.java）。

不是只读：remote add / set-url / remove 都在写 `.git/config`
（只读工作区里也能把 origin 改指别处）→ 与 Java 一样要 WORKSPACE_WRITE。

两个实测坑：
  - `remote show` 必须带 `-n`（只读本地配置，不联网）：不加时 git 会去连远端、等凭据卡死；
  - name 经常被漏传（实测就是这么失败的），add 时按"有没有远程"推一个出来，
    别为了个名字把整件事卡住。
"""


import re
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_GIT_TIMEOUT__tools_git_git_remote = 30
_REMOTE_PROBE_TIMEOUT = 10        # 对应 Java 的 drainAndWait(p, 10, UTF_8)


@tool
class GitRemoteTool(ToolPlugin):
    """查看和管理 Git 远程仓库。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.remote"

    @property
    def name(self) -> str:
        return "git_remote"

    @property
    def description(self) -> str:
        return "查看和管理Git远程仓库"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        # 不是只读：remote add / set-url / remove 都在写 .git/config（只读工作区里也能把
        # origin 改指别处）—— 与 Java 的 getRequiredPermission() = WORKSPACE_WRITE 一致。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "仓库路径"},
                "action": {"type": "string",
                           "description": "list / show / add / remove / get-url / set-url"},
                "name": {"type": "string", "description": "远程名（add/remove/show 用，如 origin）"},
                "url": {"type": "string", "description": "仓库地址（add 用）"},
            },
            "required": ["path", "action"],
        }

    def infer_remote_name(self, repo_path: str, url: str) -> str:
        """猜一个远程名：没配过远程就叫 origin，否则用地址里的仓库名（去掉 .git）。"""
        try:
            result = _git.run(["remote"], repo_path, _REMOTE_PROBE_TIMEOUT)
            if result is not None and not result[1].strip():
                return "origin"                # 一个远程都没有 → 惯例就是 origin
        except Exception:                      # noqa: BLE001 —— 问不出来就按仓库名猜
            pass
        base = re.sub(r"[#?].*$", "", url)
        base = re.sub(r"/+$", "", base)
        index = max(base.rfind("/"), base.rfind(":"))
        if 0 <= index < len(base) - 1:
            base = base[index + 1:]
        base = re.sub(r"\.git$", "", base).strip()
        return base or "origin"

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            action = self.get_required_string_arg(args, "action")
            name = (self.get_string_arg(args, "name", "") or "").strip()
            url = (self.get_string_arg(args, "url", "") or "").strip()

            if action in ("list", "ls"):
                command = ["remote", "-v"]
            elif action == "show":
                # -n：只读本地配置，不联网。实测不加 -n 时 git 会去连远端、等凭据卡死。
                command = ["remote", "show", "-n", name or "origin"]
            elif action == "add":
                if not url:
                    return self.error("add 操作至少要给 url（仓库地址），例如 "
                                      "{\"action\":\"add\",\"url\":\"https://github.com/you/repo.git\"}"
                                      "；name 可以不给，会自动取 origin 或仓库名")
                if not name:
                    name = self.infer_remote_name(path, url)
                command = ["remote", "add", name, url]
            elif action in ("get-url", "geturl", "url"):
                command = ["remote", "get-url", name or "origin"]
            elif action in ("set-url", "seturl"):
                if not url:
                    return self.error("set-url 操作需要 url 参数")
                command = ["remote", "set-url", name or "origin", url]
            elif action in ("remove", "rm", "delete"):
                if not name:
                    return self.error("remove 操作需要 name（要删掉的远程名）")
                command = ["remote", "remove", name]
            else:
                return self.error("未知操作: " + action
                                  + "。支持 list / show / add / remove / get-url / set-url"
                                  + "（add/set-url 需要 url，其余需要 name）")

            result = _git.run(command, path, _GIT_TIMEOUT__tools_git_git_remote)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据。"
                                  "远程操作用 -n 只看本地配置，或先确认网络/凭据。")

            # 【退出码不能丢】remote add 重复加（error: remote origin already exists.）、
            # remove 不存在的远程、非仓库目录（fatal）全是 exit!=0 而 stderr 已合并进
            # output —— 原来"有输出就 success"，等于把 error 文本当成功结果还给模型。
            exit_code, raw_output = result
            output = raw_output.strip()
            if exit_code != 0:
                if "not a git repository" in output:
                    return self.error("这不是 git 仓库（先 git_init）:\n" + output)
                return self.error("git remote " + action
                                  + " 失败（退出码 " + str(exit_code) + "）:\n" + output)
            if output:
                return self.success(output)
            # 没输出 != 失败：git remote add / set-url / remove 成功时本来就不打印任何东西。
            # 以前这里一律回"（无远程仓库）"，add 成功看着也像没加上。
            if action == "add":
                return self.success("已添加远程 " + name + " → " + url + "（git 成功时本来就没有输出）")
            if action in ("set-url", "seturl"):
                return self.success("已把远程 " + name + " 的地址改成 " + url)
            if action in ("remove", "rm"):
                return self.success("已删除远程 " + name)
            if action in ("list", "ls"):
                return self.success("（这个仓库没有配置任何远程）")
            return self.success("（git 没有输出，命令已执行）")
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git remote操作失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_reset.py
# ========================================================================
"""git reset 工具（Java: core/plugin/tool/git/GitResetTool.java）。

补这个工具的原因：用户实跑时模型明确调用了 `git_reset`，而我们没有
（只回了"未找到工具: git_reset"）。reset 是撤销暂存/回退提交的常用操作，
缺了它模型只能用 execute_command 拼命令，容易写错。

危险度由审批策略决定（工具 id 是 tool.git.reset）：`--hard` 会丢改动，
这里在返回内容里也明确写出来。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_RESET_TIMEOUT = 60        # 对应 Java 的 drainAndWait(process, 60, UTF_8)
_MODES = ("soft", "mixed", "hard", "keep", "merge")


@tool
class GitResetTool(ToolPlugin):
    """撤销暂存 / 回退提交。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.reset"

    @property
    def name(self) -> str:
        return "git_reset"

    @property
    def description(self) -> str:
        return "撤销暂存/回退提交（--soft/--mixed/--hard，可选 ref）"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        # Java 的 GitResetTool 没有覆盖 getRequiredPermission() → 基类默认 WORKSPACE_WRITE。
        # 危险度由审批策略决定（工具 id 是 tool.git.reset），不靠这里的等级。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Git仓库路径"},
                "mode": {"type": "string",
                         "description": "soft（只移动 HEAD，改动留在暂存区）/ mixed（默认，改动留在工作区）/ hard（丢弃改动）",
                         "default": "mixed"},
                "ref": {"type": "string", "description": "回退到哪个提交，默认 HEAD"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            dir_error = _git.check_directory(path)
            if dir_error is not None:
                return self.error(dir_error)

            mode = (self.get_string_arg(args, "mode", "mixed") or "mixed").lower().strip()
            mode = mode.replace("-", "")               # 模型可能写成 --hard / -hard
            if mode not in _MODES:
                return self.error("未知模式: " + mode + "。只能是 soft / mixed / hard")

            ref = self.get_string_arg(args, "ref", "HEAD") or ""
            if not ref.strip():
                ref = "HEAD"

            command = ["reset", "--" + mode]
            if ref != "HEAD":
                command.append(ref)

            result = _git.run(command, path, _RESET_TIMEOUT)
            if result is None:
                return self.error("git 命令超时（60 秒没返回）：多半在等网络或凭据")

            code, output = result
            head = ("git reset --" + mode + ("" if ref == "HEAD" else " " + ref)
                    + "（退出码 " + str(code) + "）")
            if code != 0:
                return self.error(head + "\n" + output + _git.hint(output))
            warn = "\n注意：--hard 已丢弃工作区改动。" if mode == "hard" else ""
            return self.success(head + "\n" + (output if output.strip() else "（无输出）") + warn)
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("git reset 失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_stash.py
# ========================================================================
"""Git Stash 工具（Java: core/plugin/tool/git/GitStashTool.java）。

action 支持 push/pop/list/drop/apply，另收一批模型爱写的别名
（save/stash/create/store/push_stash → push 等）。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

_GIT_TIMEOUT__tools_git_git_stash = 30

#: action 别名 → 真实子命令（与 Java 的 switch 表达式逐个对应）
_ALIASES__tools_git_git_stash = {
    "save": "push", "stash": "push", "create": "push", "store": "push", "push_stash": "push",
    "restore": "pop", "unstash": "pop", "pop_stash": "pop",
    "ls": "list", "show": "list", "status": "list",
}


@tool
class GitStashTool(ToolPlugin):
    """Git stash 操作（保存/恢复/列出/删除）。"""

    minimal_mode = False

    @property
    def id(self) -> str:
        return "tool.git.stash"

    @property
    def name(self) -> str:
        return "git_stash"

    @property
    def description(self) -> str:
        return "Git stash操作（保存/恢复/列出/删除）"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        # Java 的 GitStashTool 没有覆盖 getRequiredPermission() → 基类默认 WORKSPACE_WRITE
        # （stash push/pop 会改工作区文件）。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "仓库路径"},
                "action": {"type": "string",
                           "description": "push/pop/list/drop/apply（save 等于 push）"},
                "message": {"type": "string", "description": "stash消息"},
            },
            "required": ["path", "action"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            action = self.get_required_string_arg(args, "action").lower().strip()
            action = _ALIASES__tools_git_git_stash.get(action, action)          # 别名：save/stash/create 都是 push
            message = self.get_string_arg(args, "message", "") or ""

            if action == "push":
                command = ["stash", "push", "-m", message] if message else ["stash", "push"]
            elif action in ("pop", "list", "drop", "apply"):
                command = ["stash", action]
            else:
                return self.error("未知操作: " + action)

            result = _git.run(command, path, _GIT_TIMEOUT__tools_git_git_stash)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据。"
                                  "远程操作用 -n 只看本地配置，或先确认网络/凭据。")
            # 【退出码不能丢】stash pop 撞冲突（CONFLICT / local changes would be
            # overwritten）、空栈上 drop/apply/pop（No stash entries found）全是 exit!=0，
            # 原来一律 self.success —— 模型以为改动已恢复/暂存已删，工作区其实没动。
            exit_code, output = result
            if exit_code != 0:
                if "No stash entries found" in output or "No stash entries" in output:
                    return self.error("没有可执行的 stash（栈是空的）:\n" + output)
                if "CONFLICT" in output or "would be overwritten" in output:
                    return self.error("stash " + action + " 有冲突（退出码 "
                                      + str(exit_code) + "，改动没有完整恢复，先看下面的输出）:\n"
                                      + output)
                return self.error("git stash " + action
                                  + " 失败（退出码 " + str(exit_code) + "）:\n" + output)
            return self.success(output if output else "操作完成")
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git stash操作失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git/git_status.py
# ========================================================================
"""Git状态查看工具（Java: core/plugin/tool/git/GitStatusTool.java）。"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool
from lionbox.tools.git import _git

#: 单条 git 命令的超时（秒），对应 Java 的 drainAndWait(process, 30, UTF_8)
_GIT_TIMEOUT__tools_git_git_status = 30


@tool
class GitStatusTool(ToolPlugin):
    """查看 Git 仓库状态：`git status --short`。"""

    minimal_mode = False        # GIT 类工具在极简模式下一律不开放（Java: isAvailableInMode(MINIMAL)）

    @property
    def id(self) -> str:
        return "tool.git.status"

    @property
    def name(self) -> str:
        return "git_status"

    @property
    def description(self) -> str:
        return "查看Git仓库状态"

    @property
    def category(self) -> str:
        return ToolCategory.GIT

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Git仓库路径"},
            },
            "required": ["path"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        return self.runGitCommand(args, "status", "--short")

    def runGitCommand(self, args: dict[str, Any], *command: str) -> ToolResult:
        """对应 Java 的 `runGitCommand(arguments, gitExecutable(), …)`。"""
        try:
            path = self.resolve_path(self.get_required_string_arg(args, "path"))
            result = _git.run(list(command), path, _GIT_TIMEOUT__tools_git_git_status)
            if result is None:
                return self.error("git 命令超时（30 秒没返回）：多半在等网络或凭据")
            # 【退出码不能丢】非仓库目录里 git status --short 是 exit=128 +
            # "fatal: not a git repository"，原来这句 fatal 被当"状态文本" success 吐回去，
            # 模型会把它读成"仓库没改动"（同文件 git_log 对同一文案做了分流，这里对齐）。
            exit_code, output = result
            if exit_code != 0:
                if "not a git repository" in output:
                    return self.error("这不是 git 仓库（先 git_init，path 指向工作区目录）:\n"
                                      + output)
                return self.error("git status 失败（退出码 " + str(exit_code) + "）:\n" + output)
            return self.success(output if output else "（无变更）")
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("Git命令执行失败: " + str(exc) + _git.hint(str(exc)))


# ========================================================================
# 原模块 lionbox/tools/git.py
# ========================================================================
"""git 工具包（9 个，与 Java 的 `core/plugin/tool/git` 包一一对应）。

显式登记：每个模块在自己的 `@tool` 装饰器里登记工具类，`__init__` 只做"按名字导入"，
不做目录扫描（见 PORTING.md 一.3：扫描会拖慢启动且顺序不确定）。
"""



__all__ = [
    "GitBranchTool",
    "GitCommitTool",
    "GitDiffTool",
    "GitInitTool",
    "GitLogTool",
    "GitRemoteTool",
    "GitResetTool",
    "GitStashTool",
    "GitStatusTool",
]


# ========================================================================
# 原模块 lionbox/tools/shell/persistent_shell.py
# ========================================================================
"""常驻 Shell 会话（"持续运行的终端"）—— Java: `core/plugin/tool/shell/PersistentShell.java`。

**这个文件不是工具**（Java 里它是 `@Component` 而不是 ToolPlugin），所以没有 `@tool` 登记。
它管的是 `execute_command` 怎么跑。

【为什么要有它】以前 `execute_command` 是"一条命令起一个进程"：`cd` 是白做的、
`$env:X=1` 下一轮就没、函数/别名更留不下来；用户看到的现象是"这不是终端，它每次都新开一个"。
现在改成：**同一个工作区共用一个长期活着的 PowerShell 进程**，命令从它的 stdin 递进去，
`cd`、变量、函数、别名都真的会留在下一次调用里（跟真人开的终端一样）。

【协议】Java 版同款，三个坑都在这里解决：

1. **多行脚本**：PowerShell 5.1 的 `-Command -` 是**按行**读 stdin 的，直接喂
   `if (...) {` 换行 `}` 会被拆散、卡住。所以命令先做 UTF-8 Base64，整条作为一行 ASCII
   送进去（`[Convert]::FromBase64String` 再 `Invoke-Expression`），多行脚本就当成一整段执行。
2. **中文乱码**：PS 5.1 的 stdin/stdout 走的是**系统 ANSI/OEM 代码页**（中文机器 = GBK），
   用 UTF-8 写命令进去，中文路径在进去之前就已经乱了。Base64 全程 ASCII，从根上绕过；
   输出侧在会话建立时设一次 `[Console]::OutputEncoding = UTF8`。
3. **哪一段输出属于哪条命令**：每条命令跑完由 shell 自己打一行唯一哨兵
   （`__LIONBOX_DONE_<随机>__ ok=… code=… cwd=…`），读到哨兵就收工。
   哨兵放在 try/catch 的**两个分支**里，命令抛异常也会打出来，不会把调用方吊死。

【退出码哨兵】`$LASTEXITCODE` 只有**原生命令**（git/python…）才会写，纯 cmdlet 命令
（echo hi、Get-ChildItem）根本不碰它 —— 而会话是长期活着的，于是它会把上一条命令的
退出码留下来报上去：先 `git status`（非仓库 → 128），再 `echo hi`，工具就报
"命令以退出码 128 结束"，一条成功的命令被判成失败。所以每条命令开跑前先 `$LASTEXITCODE = 0`。

【超时】命令卡住（等输入、死循环）时不能只杀子进程 —— 那样这个会话本身也废了。
现在的做法是连**整个 shell 会话一起杀掉并重建**，并在结果里明确告诉模型"终端被重启了，
之前 cd 的目录和变量没了"，它下一轮就不会接着用不存在的状态。

【输出上限】`max_output_bytes` 只约束"一次 run 往回带多少"，管不住内存：命令结束、
下一条命令还没来时，一条 `type huge.log` 的输出会整份堆在堆里（这软件跟着本地模型跑，
机器本来就不宽裕）。所以读取侧的缓冲区按配置值的 4 倍封顶，且**超限只丢不停** ——
不读的话 shell 的输出管道满了，它自己就卡在 write 上，后面所有命令都别想跑。
"""


import base64
import shutil
import subprocess
import sys
import threading
import time
from collections import deque
from pathlib import Path

#: 哨兵前缀；后面拼一段随机数，避免和命令自身的输出撞车
MARK = "__LIONBOX_DONE_"

#: 会话建立握手超时（秒）
STARTUP_TIMEOUT = 20

#: 命令没给超时时的兜底（与 Java 的 `timeoutSec <= 0 ? 300 : timeoutSec` 一致）
DEFAULT_TIMEOUT_SECONDS = 300

#: 一条命令最多带回多少字节的默认值；与 Java 的 PluginSettings.DEFAULT_MAX_OUTPUT_BYTES 一致
DEFAULT_MAX_OUTPUT_BYTES = 200_000

#: 输出编码设置（会话第一条命令）
INIT = ("[Console]::OutputEncoding=[System.Text.Encoding]::UTF8; "
        "$OutputEncoding=[System.Text.Encoding]::UTF8; "
        "$PSDefaultParameterValues['Out-File:Encoding']='utf8'")

#: 会话空闲多久之后回收（秒）；10 分钟没命令就把进程关掉，别白占内存
IDLE_TIMEOUT_SECONDS = 10 * 60

#: 空闲回收器多久扫一遍（秒）
REAP_INTERVAL_SECONDS = 60

#: 读取侧缓冲区封顶 = 输出上限 × 这个倍数。
#: 留 4 倍余量：截断是按字节记账的，缓冲区卡得跟上限一样紧，截断逻辑就看不到
#: "超限的那一行"，"输出已截断"的提示会变成一句空话。
QUEUE_CAP_FACTOR = 4

#: 缓冲区封顶的绝对上限（字符）：用户在设置里填个天文数字也不至于把堆吃满
QUEUE_CAP_MAX_CHARS = 8_000_000

#: 保留多少条"控制行"（哨兵行/错误行）。它们不参与封顶丢弃，只留最近这些避免无限增长：
#: 一条命令最多打两条（try 分支一条、catch 分支一条），24 条足够覆盖极端情况。
_CONTROL_MAX = 24
_CONTROL_KEEP = 4

#: 巡检步长（秒）/ 巡检间隔（秒）：等待哨兵时既不能忙等，也不能反应太慢
_POLL_STEP_SECONDS = 0.2
_POLL_SLICE_SECONDS = 0.05

#: 读取线程读多大一块（字符）
_READ_CHUNK_CHARS = 65536

#: 没有创建工作区时用的会话键（与 Java 的 `key == null ? "default" : key` 一致）
DEFAULT_KEY = "default"


class RunResult:
    """一次命令执行的结果（字段与 Java 的 `record RunResult` 对齐）。

    output    命令输出（已去掉哨兵行；stdout 与 stderr 合并，跟真终端一样）
    exit_code 退出码（拿不到时为 None）
    ok        shell 报的 `$?`
    cwd       执行完之后终端所在目录
    timed_out 是否超时（此时 shell 已被重启）
    restarted 是否重启过 shell（超时/被 exit 杀掉）
    error_text 致命错误（非 None 时调用方直接当失败返回）
    truncated 输出是否因为超过上限被截断
    """

    __slots__ = ("output", "exit_code", "ok", "cwd", "timed_out", "restarted",
                 "error_text", "truncated")

    def __init__(self, output: str = "", exit_code: int | None = None, ok: bool = False,
                 cwd: str | None = None, timed_out: bool = False, restarted: bool = False,
                 error_text: str | None = None, truncated: bool = False) -> None:
        self.output = output
        self.exit_code = exit_code
        self.ok = ok
        self.cwd = cwd
        self.timed_out = timed_out
        self.restarted = restarted
        self.error_text = error_text
        self.truncated = truncated

    def __repr__(self) -> str:
        return (f"RunResult(ok={self.ok}, exit_code={self.exit_code}, cwd={self.cwd!r}, "
                f"timed_out={self.timed_out}, restarted={self.restarted}, "
                f"truncated={self.truncated}, output={self.output[:40]!r})")


class _Session:
    """单个常驻会话：一个长期活着的 shell 进程 + 一个读线程 + 一个有上限的输出缓冲区。"""

    def __init__(self, process: subprocess.Popen, shell_name: str) -> None:
        self.process = process
        self.shell_name = shell_name
        self.cwd: str | None = None
        self.last_used = time.monotonic()
        self.cap_chars = _queue_cap_chars(0)      # 每条命令开始时按当前设置重算
        self.dead = False                         # 进程已退出 / 已被回收
        self.broken = False                       # 输出到了上限还没见到换行，缓冲区已截断

        self._lines: deque[str] = deque()         # 收下的输出行
        self._chars = 0                           # 这些行一共多少字符
        self._control: list[str] = []             # 哨兵行/错误行：**永远不丢**（见 _trim_locked）
        self._scan_pos = 0                        # 主线程已经扫到哪（避免重复扫描）
        self._cond = threading.Condition()
        #: 一次 run 的执行锁（begin → send → 等哨兵 整段持有，见 PersistentShell._exec）
        self.exec_lock = threading.Lock()

        self._reader = threading.Thread(target=self._read_loop, name="lionbox-shell-reader",
                                        daemon=True)
        self._reader.start()

    # ---- 读取侧 ----
    def _read_loop(self) -> None:
        stdout = self.process.stdout
        try:
            while True:
                # 【读取方式是最容易踩坑的一处，实测确认过两点】
                #  1) 不能用 `read(n)`：文本流的 `read(n)` 会一直阻塞到**凑满 n 个字符**或 EOF
                #     才返回。常驻终端是"问一句答一句"的交互，命令输出的那几行永远凑不满 64KB，
                #     哨兵就永远到不了主线程 —— 表现是连握手都超时。
                #  2) 也不能用 `read1(n)`：Windows 上子进程管道是原始 FileIO，
                #     `_io.FileIO` 没有 `read1`，`TextIOWrapper` 也就没有 → AttributeError，
                #     读线程直接死掉（表现是"终端进程已退出"但其实进程还活着）。
                # 所以用 `read(1)`：有数据就立刻返回一个字符，没有就阻塞等（不忙等）。
                # 攒够一块（或读到换行）再进缓冲区，避免逐字符加锁。
                chunk = stdout.read(1)
                if not chunk:
                    break
                while len(chunk) < _READ_CHUNK_CHARS:
                    more = stdout.read(1)
                    if not more:
                        break
                    chunk += more
                    if more == "\n":
                        break
                with self._cond:
                    self._lines.append(chunk)
                    self._chars += len(chunk)
                    # 【哨兵行/错误行永远放行】缓冲区封顶会从头丢行，而哨兵是**最后**到的：
                    # 一条输出几兆的命令（`type huge.log`）会把封顶顶穿，如果哨兵也被丢掉，
                    # 主线程就永远等不到"命令结束"——表现是那条命令白等到超时、终端被重启。
                    # Java 版就是靠 `boolean control = line.contains(MARK) || …` 这一条挡住的。
                    # 丢了控制行 = 命令永远不结束，所以这里只"丢"普通输出、绝不"停"读取。
                    if MARK in chunk or chunk.startswith("__LIONBOX_ERR__"):
                        self._control.append(chunk)
                        if len(self._control) > _CONTROL_MAX:
                            del self._control[:-_CONTROL_KEEP]
                    self._trim_locked()
                    self._cond.notify_all()
        except Exception:                          # noqa: BLE001 —— 进程被强杀时管道会提前断开
            pass
        finally:
            with self._cond:
                self.dead = True
                self._cond.notify_all()

    def _trim_locked(self) -> None:
        """缓冲区封顶：只丢不停（见模块头注释的"输出上限"）。"""
        dropped = 0
        while self._chars > self.cap_chars and len(self._lines) > 1:
            head = self._lines.popleft()
            self._chars -= len(head)
            dropped += len(head)
        if dropped:
            self._scan_pos = max(0, self._scan_pos - dropped)
            self.broken = True

    # ---- 主线程用 ----
    def begin(self, cap_chars: int) -> None:
        """开始一条新命令：丢掉上一条命令残留的输出，并把缓冲计数清零。

        【计数必须一起清零】否则一条超大输出的命令把计数顶到上限之后，
        这个会话后面每条命令都收不到任何输出行（表现是"终端哑了"）。
        """
        with self._cond:
            self._lines.clear()
            self._chars = 0
            self._scan_pos = 0
            self._control.clear()
            self.broken = False
            self.cap_chars = cap_chars
            self.last_used = time.monotonic()

    def send(self, line: str) -> None:
        assert self.process.stdin is not None
        self.process.stdin.write(line + "\n")
        self.process.stdin.flush()

    def scan_for(self, token: str) -> tuple[list[str], str] | None:
        """扫到哨兵就返回 `(本次新到的输出行, 哨兵尾巴)`。

        只扫上次之后新到的数据；缓冲区被截断时 `_scan_pos` 会跟着回退，
        所以最多重扫一遍幸存的行，哨兵不会丢。

        【为什么按**行**返回，而不是返回一大坨 head】上限记账必须是"一行一行地累加、
        超了才停"：如果把整段输出一次交给调用方去判断，一段比上限大得多的输出会被整体
        丢掉 —— 表现是"明明有几十 KB 输出，工具却说没有输出"（实测踩过）。按行给，
        调用方就能一直收到正好塞满上限为止，剩下的丢掉并标 truncated。

        【为什么还要看 `_control`】缓冲区封顶会把老行丢掉，而哨兵是最后到的。
        控制行单独留了一份（见 `_read_loop`），所以哪怕普通输出已经被丢光，
        哨兵照样找得到 —— 与 Java 版"控制行永远放行"是同一条保证。
        """
        with self._cond:
            found_tail: str | None = None

            def take(from_pos: int, to_pos: int) -> list[str]:
                """把 [from_pos, to_pos) 里**完整的行**取出来（不完整的留在扫描位之后）。"""
                nonlocal found_tail
                text = data[from_pos:to_pos] if from_pos < to_pos else ""
                if not text:
                    return []
                index = text.find(token)
                if index >= 0:
                    found_tail = text[index + len(token):].strip()
                    text = text[:index]
                last_newline = text.rfind("\n")
                if last_newline < 0:
                    return []
                out = text[:last_newline].split("\n")
                self._scan_pos = from_pos + last_newline + 1
                return out

            data = "".join(self._lines)
            start = min(self._scan_pos, len(data))
            index = data.find(token, start)
            if index >= 0:
                lines = take(start, len(data))
                tail = found_tail if found_tail is not None else data[index + len(token):].strip()
                self._control.clear()
                self.last_used = time.monotonic()
                return lines, tail

            for line in self._control:
                index = line.find(token)
                if index >= 0:
                    lines = take(start, len(data))
                    self._control.clear()
                    self.last_used = time.monotonic()
                    return lines, line[index + len(token):].strip()

            lines = take(start, len(data))
            if lines:
                self.last_used = time.monotonic()
                return lines, ""
            return None

    def wait_tick(self, timeout: float) -> None:
        with self._cond:
            self._cond.wait(timeout)

    def overflowed(self) -> bool:
        """缓冲区被顶穿、并且**连哨兵都没留住** —— 这才是真的没救了。

        控制行在的话说明命令已经结束、哨兵马上就到，不该把它当"输出失控"杀掉。
        """
        with self._cond:
            return self.broken and not self._control

    def is_alive(self) -> bool:
        return not self.dead and self.process.poll() is None

    def destroy(self) -> None:
        """强杀 shell 进程并收掉读线程（幂等）。"""
        self.dead = True
        reader, self._reader = self._reader, None
        try:
            self.process.kill()
        except Exception:                          # noqa: BLE001 —— 已经死了
            pass
        try:
            self.process.wait(timeout=5)
        except Exception:                          # noqa: BLE001 —— 杀不掉也不该把调用方带走
            pass
        if reader is not None and reader is not threading.current_thread():
            reader.join(timeout=2)
        with self._cond:
            self._lines.clear()
            self._control.clear()
            self._chars = 0
            self._cond.notify_all()                # 叫醒还在等哨兵的主线程


def _queue_cap_chars(max_output_bytes: int) -> int:
    """输出缓冲区最多攒多少字符（0 = 不限制 → 按默认值算，缓冲区必须有上限）。"""
    base = max_output_bytes if max_output_bytes > 0 else DEFAULT_MAX_OUTPUT_BYTES
    return int(min(base * QUEUE_CAP_FACTOR, QUEUE_CAP_MAX_CHARS))


def shell_executable() -> str:
    """有 PowerShell 7（pwsh）就用它；没有就用系统自带的 Windows PowerShell 5.1。"""
    if not is_windows__tools_shell_persistent_shell():
        return "sh"
    probe = shutil.which("pwsh")
    if probe:
        try:
            # 【必须带 NO_WINDOW】Lion Code 是 GUI 进程，CreateProcess 一个控制台程序会
            # 新开控制台窗口（_start_process / run_background 都带了这个 flag，唯独这次
            # 探测没带 → 装了 pwsh 的机器第一次用终端会闪一下黑框，用户当成 bug）。
            completed = subprocess.run(
                [probe, "-NoLogo", "-NoProfile", "-Command", "exit 0"],
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5,
                creationflags=NO_WINDOW)
            if completed.returncode == 0:
                return probe
        except Exception:                          # noqa: BLE001 —— 没有 pwsh，继续用 powershell
            pass
    return "powershell"


def is_windows__tools_shell_persistent_shell() -> bool:
    return sys.platform == "win32"


#: 子进程不弹控制台窗口（Lion Code 是 GUI 程序，弹黑框会被用户当成 bug）
NO_WINDOW = 0x08000000 if sys.platform == "win32" else 0


def build_payload(command: str, workdir: str | None, token: str) -> str:
    """组装要送进 shell 的脚本（PowerShell 版）。

    哨兵放进 try/catch 的**两个分支**里：命令正常结束在 try 里打，抛出终止性错误在 catch 里打。
    这样无论命令怎么炸，调用方都能收到哨兵，不会白等到超时。
    """
    lines = ["try {"]
    if workdir:
        lines.append("Set-Location -LiteralPath '" + workdir.replace("'", "''") + "'")
    lines.append("$global:LASTEXITCODE = 0")
    lines.append(command)
    lines.append('Write-Output ("' + token + ' ok=$? code=$LASTEXITCODE cwd=" + (Get-Location).Path)')
    lines.append("} catch {")
    lines.append('Write-Output ("__LIONBOX_ERR__" + $_.Exception.Message)')
    lines.append('Write-Output ("' + token + ' ok=False code=$LASTEXITCODE cwd=" + (Get-Location).Path)')
    lines.append("}")
    return "\n".join(lines)


def build_payload_sh(command: str, workdir: str | None, token: str) -> str:
    """类 Unix 的同一套协议：`$?` / `pwd` 用 sh 的等价物。

    【注意】哨兵行里带的是 `cwd=`，所以 `pwd` 要用 `pwd -P`（解析符号链接后的物理路径，
    与 PowerShell 的 `(Get-Location).Path` 语义一致）。
    """
    lines = []
    if workdir:
        lines.append("cd " + _sh_quote(workdir) + " || true")
    lines.append(command)
    lines.append("__lc=$?")
    # 【哨兵必须是 printf 的**一个**参数】POSIX printf 在参数多于格式符时会**重复使用
    # 格式串**：`printf '%s\n' tok " ok=" True " code=0…"` 输出 4 行，协议要求的单行
    # "<token> ok=… code=… cwd=…" 就碎了 —— 扫描侧拿到的 tail 里没有 "ok=True"，
    # 每条命令都会被报成失败。所以把几段拼成一个词：单引号放 token（无须展开），
    # 双引号放要展开的 `$?`/`$(pwd)`，相邻引号在 shell 里会拼成同一个参数。
    lines.append("printf '%s\\n' " + _sh_quote(token)
                 + '" ok=' + "$([ $__lc -eq 0 ] && echo True || echo False)"
                 + ' code=$__lc cwd=$(pwd -P)"')
    return "\n".join(lines)


def _sh_quote(text: str) -> str:
    return "'" + text.replace("'", "'\\''") + "'"


def encode_line(key: str, payload: str) -> str:
    """Base64 成**一行 ASCII** 再交给 `Invoke-Expression`（见模块头注释第 1、2 条）。"""
    b64 = base64.b64encode(payload.encode("utf-8")).decode("ascii")
    return ("$__lionbox_c=[Text.Encoding]::UTF8.GetString([Convert]::FromBase64String('" + b64
            + "')); Invoke-Expression $__lionbox_c")


def parse_code(tail: str) -> int | None:
    """从哨兵尾部解析 `code=`（拿不到返回 None）。"""
    index = tail.find("code=")
    if index < 0:
        return None
    rest = tail[index + 5:].strip()
    end = 0
    while end < len(rest) and (rest[end].isdigit() or rest[end] == "-"):
        end += 1
    if end == 0:
        return None
    try:
        return int(rest[:end])
    except ValueError:
        return None


def parse_cwd(tail: str) -> str | None:
    """从哨兵尾部解析 `cwd=`（永远放在最后，所以中文/带空格路径也取得回来）。"""
    index = tail.find("cwd=")
    if index < 0:
        return None
    cwd = tail[index + 4:].strip()
    return cwd or None


def _strip_trailing_newlines(text: str) -> str:
    return text.rstrip("\r\n")


class PersistentShell:
    """常驻终端：工作区 → 会话（同一个工作区 = 同一个终端）。"""

    def __init__(self) -> None:
        self._sessions: dict[str, _Session] = {}
        self._lock = threading.RLock()
        self._shell_name: str | None = None
        self._closed = False
        self._reaper = threading.Thread(target=self._reap_loop, name="lionbox-shell-reaper",
                                        daemon=True)
        self._reaper.start()

    # ---- 对外接口 ----
    def run(self, key: str | None, command: str, workdir: str | None,
            timeout_sec: int = 0, max_output_bytes: int = 0) -> RunResult:
        """在常驻会话里执行一条命令。

        key             会话键（用工作区路径；同一个工作区 = 同一个终端）
        command         已经翻译过的命令（Unix 写法 → PowerShell 写法在调用方完成）
        workdir         这条命令要求的目录（None = 沿用终端当前目录）
        timeout_sec     超时秒数（<=0 用默认 300）
        max_output_bytes 最多带回多少字节（<=0 表示不限制）
        """
        session_key = key if key and key.strip() else DEFAULT_KEY
        timeout = timeout_sec if timeout_sec > 0 else DEFAULT_TIMEOUT_SECONDS
        if self._closed:
            return RunResult(error_text="常驻终端已关闭（应用正在退出）")
        try:
            session = self._acquire(session_key)
        except Exception as exc:                   # noqa: BLE001 —— 起不来就报"无法启动常驻终端"
            return RunResult(error_text="无法启动常驻终端: " + str(exc))
        return self._exec(session, session_key, command, workdir, timeout, max_output_bytes)

    def close(self, key: str | None) -> bool:
        """关掉某个工作区的终端（用户主动要求重开时用）。"""
        session_key = key if key and key.strip() else DEFAULT_KEY
        with self._lock:
            session = self._sessions.pop(session_key, None)
        if session is None:
            return False
        session.destroy()
        return True

    def active_shells(self) -> list[str]:
        """当前活着的终端有哪些（诊断用）。"""
        with self._lock:
            return list(self._sessions)

    def shutdown(self) -> None:
        """应用退出：先停回收器，再关掉所有会话。"""
        self._closed = True
        with self._lock:
            sessions = list(self._sessions.values())
            self._sessions.clear()
        for session in sessions:
            session.destroy()

    # ---- 会话管理 ----
    def _acquire(self, key: str) -> _Session:
        now = time.monotonic()
        with self._lock:
            existing = self._sessions.get(key)
            if existing is not None:
                if existing.is_alive() and now - existing.last_used < IDLE_TIMEOUT_SECONDS:
                    return existing
                self._sessions.pop(key, None)
                existing.destroy()

            created = _Session(self._start_process(key), self._shell_name or "shell")
            self._sessions[key] = created

        # 握手：确认这个 shell 真的能收命令（不然第一条真命令会白等到超时）。
        # 顺手把输出编码设成 UTF-8，中文路径/中文输出才不会变成乱码。
        hello = self._exec(created, key, INIT, None, STARTUP_TIMEOUT, 0)
        if hello.error_text is not None or not hello.ok:
            with self._lock:
                self._sessions.pop(key, None)
            created.destroy()
            raise OSError(hello.error_text if hello.error_text is not None
                          else "终端启动后没有回应（" + created.shell_name + "）")
        return created

    def _start_process(self, key: str) -> subprocess.Popen:
        shell = self._shell_name = self._shell_name or shell_executable()
        if is_windows__tools_shell_persistent_shell():
            command = [shell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", "-"]
        else:
            command = [shell]
        cwd: str | None = None
        if key == DEFAULT_KEY:
            home = Path.home()
            cwd = str(home) if home.is_dir() else None
        elif Path(key).is_dir():
            cwd = key
        return subprocess.Popen(
            command,
            cwd=cwd,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
            text=True, encoding="utf-8", errors="replace", bufsize=1,
            creationflags=NO_WINDOW,
        )

    # ---- 真正执行：写命令 → 等哨兵 → 收输出 ----
    def _exec(self, session: _Session, session_key: str, command: str,
              workdir: str | None, timeout: int, max_output_bytes: int) -> RunResult:
        """执行一条命令：**同一会话整段串行**（begin → send → 等哨兵 持锁）。

        【为什么必须串行】工具执行跑在线程池里，两个调用方可能拿到同一个会话：
        B 线程的 begin() 会清空 A 正在读的缓冲/扫描位，A、B 的输出与哨兵交错，
        谁先到的哨兵都会被对方 scan_for 收走（控制行只认 token 前缀、不认归属）——
        先等的一方永远等不到自己的 token，白等到 deadline 后连终端一起被杀，
        另一方立刻看到"终端进程已退出"。_acquire 还可能把刚建、握手还没做完的会话
        交给第二个调用者，两条命令直接交错执行。锁在这里一并解决这两件事。
        """
        with session.exec_lock:
            return self._exec_locked(session, session_key, command, workdir,
                                     timeout, max_output_bytes)

    def _exec_locked(self, session: _Session, session_key: str, command: str,
                     workdir: str | None, timeout: int, max_output_bytes: int) -> RunResult:
        token = MARK + format(int(time.time() * 1_000_000) & 0xFFFFFFFF, "x") + "__"
        if is_windows__tools_shell_persistent_shell():
            line = encode_line(session_key, build_payload(command, workdir, token))
        else:
            line = build_payload_sh(command, workdir, token)

        session.begin(_queue_cap_chars(max_output_bytes))
        try:
            session.send(line)
        except Exception as exc:                   # noqa: BLE001 —— 写不进去说明会话废了
            with self._lock:
                self._sessions.pop(session_key, None)
            session.destroy()
            return RunResult(error_text="终端会话已失效（写入失败），已重启: " + str(exc),
                             restarted=True)

        collected: list[str] = []
        collected_bytes = 0
        truncated = False
        deadline = time.monotonic() + timeout
        while True:
            # 命令还在跑 → 每条输出/每次轮询都给会话续期（空闲回收器别把长命令连终端一起杀掉）
            session.last_used = time.monotonic()

            if session.overflowed():
                # 输出把读取侧的缓冲区顶穿了、而且连哨兵都没留住（命令还在往外吐）：
                # 这个 shell 的输出管道满了它会卡在 write 上，与其吊死不如连终端一起重启。
                # 【已经收到的那部分要带回去】不能白丢：模型至少能看到开头，知道命令确实跑过。
                with self._lock:
                    self._sessions.pop(session_key, None)
                session.destroy()
                return RunResult(output=_strip_trailing_newlines("\n".join(collected)),
                                 timed_out=True, restarted=True, truncated=True,
                                 error_text=("终端输出超过上限（"
                                             + str(_queue_cap_chars(max_output_bytes))
                                             + " 字符）仍未结束，**输出已截断**，已强制重启终端；"
                                             "命令可能产出了超长的一行（例如二进制文件、无换行的日志）。"))

            found = session.scan_for(token)
            if found is not None:
                lines, tail = found
                # 一行一行地累加：到上限就停（但**继续把行读掉**，不读的话这个 shell 的
                # 输出会一直堆在管道里，它自己就卡在 write 上），并标记"被截断了"。
                for text_line in lines:
                    line_bytes = len(text_line.encode("utf-8")) + 1
                    if max_output_bytes > 0 and collected_bytes + line_bytes > max_output_bytes:
                        truncated = True
                        continue
                    collected.append(text_line)
                    collected_bytes += line_bytes
                if not tail:
                    continue                        # 只是有新输出，命令还没结束
                ok = "ok=True" in tail
                code = parse_code(tail)
                cwd = parse_cwd(tail)
                if cwd is not None:
                    session.cwd = cwd
                session.last_used = time.monotonic()
                text = _strip_trailing_newlines("\n".join(collected))
                if text.startswith("__LIONBOX_ERR__"):
                    text = text[len("__LIONBOX_ERR__"):].strip()
                return RunResult(output=text, exit_code=code, ok=ok, cwd=cwd,
                                 truncated=truncated)

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                # 命令卡住：整个会话一起杀，重建一个干净终端
                with self._lock:
                    self._sessions.pop(session_key, None)
                session.destroy()
                # 【必须按行 join】collected 的元素是不含换行的输出行，
                # 这里用 "".join 会把 "line1line2line3" 黏成一行（超时/终端退出两条路径），
                # 模型拿到的"已收到的输出"完全不可读，排障线索作废。
                return RunResult(output=_strip_trailing_newlines("\n".join(collected)),
                                 timed_out=True, restarted=True, truncated=truncated,
                                 error_text=("命令执行超时（" + str(timeout) + "秒），已强制重启终端"
                                             "（超时通常是在等输入，例如 pause/read-host/set /p）"))
            if not session.is_alive():
                with self._lock:
                    self._sessions.pop(session_key, None)
                return RunResult(output=_strip_trailing_newlines("\n".join(collected)),
                                 restarted=True, truncated=truncated,
                                 error_text=("终端进程已退出（命令里可能有 exit）—— "
                                             "下次调用会自动重开一个终端"))
            session.wait_tick(min(remaining, _POLL_STEP_SECONDS))

    # ---- 空闲回收 ----
    def _reap_loop(self) -> None:
        """空闲会话回收器：每分钟扫一遍。

        【为什么要有它】`IDLE_TIMEOUT_SECONDS` 那句注释写着"10 分钟没命令就把进程关掉"，
        但 Java 版的检查只在 `acquire` 里做 —— 也就是**下一条命令**来的时候才回收。
        用户不再对着这个工作区敲命令时，那个 shell 进程就一直驻留着。守护线程 + 只读会话表，
        开销可以忽略。整个循环包在 try 里：定时任务是"抛一次异常就再也不跑"的。
        """
        while not self._closed:
            time.sleep(REAP_INTERVAL_SECONDS)
            try:
                self._reap_idle()
            except Exception:                      # noqa: BLE001 —— 回收失败不能把回收器带走
                pass

    def _reap_idle(self) -> None:
        """把"进程已死"或"闲着超过 IDLE_TIMEOUT_SECONDS"的会话收掉。

        判据和 `_acquire` 里的一致；先摘出名单再逐个 destroy（不要在持锁时 kill 进程）。
        """
        now = time.monotonic()
        with self._lock:
            stale = [key for key, session in self._sessions.items()
                     if not session.is_alive() or now - session.last_used >= IDLE_TIMEOUT_SECONDS]
        for key in stale:
            with self._lock:
                session = self._sessions.pop(key, None)
            if session is not None:
                session.destroy()


# ========================================================================
# 原模块 lionbox/tools/shell/shell_background.py
# ========================================================================
"""后台 Shell 执行工具 —— Java: `core/plugin/tool/shell/ShellBackgroundTool.java`。

【会话隔离】Java 版这两张表是 **static** 的（`static final Map<String, Process> backgroundProcesses`），
于是"某个会话启动的后台进程"和"另一个会话的后台进程"混在同一个表里：不带 pid 的
`stop_background` 会看到别的会话的进程，报"有多个后台进程在跑"。Python 版按**工作区**
分表（`_TABLES[workspace] = {pid: process}`），每个会话只看得见自己起的进程 ——
既保留 Java 的行为语义（同一工作区共享），又不串到别人的会话里去。

【两个实测坑】
  1) 原来走 `cmd /c`，与 execute_command 的 PowerShell 不一致：模型写 ps 语法或 Unix 别名时
     直接失败。现在与常驻终端同一套（Windows: PowerShell，类 Unix: sh）。
  2) workdir 直接按相对路径开会按**软件自己的**工作目录解析，不是工作区 —— 相对目录必然
     "目录不存在"，所以先 resolve_path + 检查。

【必须排空输出】原来没人读子进程的 stdout/stderr：后台命令输出一多就把管道缓冲区写满，
子进程**卡死**在写上面（表现是"后台任务永远不结束"）。这里开两个守护线程读掉，
并留最后 50 行方便排查。
"""


import subprocess
import threading
import uuid
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 每个后台进程留多少行输出尾巴（排查线索）
_TAIL_LINES = 50

#: 工作区 → {pid: Popen} / {pid: [行]}（见模块头注释的"会话隔离"）
_TABLES: dict[str, dict[str, subprocess.Popen]] = {}
_TAILS: dict[str, dict[str, list[str]]] = {}
_TABLES_LOCK = threading.RLock()

#: 工作区 → 已被 stop_background 停掉的 pid 集合。
#:
#: 【为什么需要】kill() 之后进程不会**立刻**从进程表里消失（Windows 上尤其明显），
#: 所以马上再停一次同一个 pid 时，`poll()` 还是 None、它已经不在表里了 ——
#: 会报"未找到进程"，而用户/模型要的只是"它别在跑"。记一笔"这个 pid 是我停的"，
#: 第二次调用就能照 Java 的语义回"已经结束了，不用再停"。
_STOPPED: dict[str, set[str]] = {}
_STOPPED_LIMIT = 200


def table(key: str) -> dict[str, subprocess.Popen]:
    """某个工作区的后台进程表（含已结束、尚未回收的）。"""
    with _TABLES_LOCK:
        return _TABLES.setdefault(key, {})


def tails(key: str) -> dict[str, list[str]]:
    """某个工作区的输出尾巴表。"""
    with _TABLES_LOCK:
        return _TAILS.setdefault(key, {})


def drain(stream: Any, tail: list[str]) -> None:
    """把子进程的输出读掉（丢弃 + 留最后 50 行），不读的话管道满了会把子进程堵死。

    【为什么这里要自己解码】调用方按**字节**收管道（不能用 encoding="utf-8" 的 text 模式：
    PS 5.1 写的是 GBK 字节，会被解成 U+FFFD 乱码）。解码退路与 read_text 一致：
    UTF-8 严格 → GBK → 替换，中文机器上的中文输出才留得住。
    """
    def reader() -> None:
        try:
            for line in stream:
                text = decode_text(line) if isinstance(line, (bytes, bytearray)) else line
                with _TABLES_LOCK:
                    tail.append(text.rstrip("\r\n"))
                    if len(tail) > _TAIL_LINES:
                        del tail[0]
        except Exception:                          # noqa: BLE001 —— 进程结束了
            pass

    threading.Thread(target=reader, name="lionbox-bg-drain", daemon=True).start()


def reap_finished(key: str) -> list[str]:
    """把已经结束的后台进程从表里清掉，返回这次清掉的 pid。

    【实测】两条后台命令都正常跑完之后，不带 pid 的 `stop_background` 会回
    "有多个后台进程在跑，指定要停哪个：…" —— 列出来的全是**已经退出**的进程，
    于是它一个也停不了（用户看到的是"后台任务清不掉"）。所以判断"有几个在跑"之前先扫一遍。
    """
    finished: list[str] = []
    with _TABLES_LOCK:
        processes = _TABLES.setdefault(key, {})
        for pid in list(processes):
            if processes[pid].poll() is not None:
                processes.pop(pid, None)
                _TAILS.setdefault(key, {}).pop(pid, None)
                finished.append(pid)
    return finished


def forget(key: str, pid: str) -> subprocess.Popen | None:
    """从表里摘掉一个 pid 并把它的输出尾巴一起清掉。"""
    with _TABLES_LOCK:
        process = _TABLES.setdefault(key, {}).pop(pid, None)
        _TAILS.setdefault(key, {}).pop(pid, None)
        if process is not None:
            stopped = _STOPPED.setdefault(key, set())
            stopped.add(pid)
            while len(stopped) > _STOPPED_LIMIT:
                stopped.pop()
    return process


def was_stopped(key: str, pid: str) -> bool:
    """这个 pid 是不是已经被 stop_background 停过了（见 `_STOPPED` 的注释）。"""
    with _TABLES_LOCK:
        return pid in _STOPPED.get(key, set())


def shutdown() -> None:
    """应用退出时把还在跑的后台进程一起收掉。

    这些进程是我们起的，不杀就会活过整个应用（用户关掉软件后任务管理器里还留着它），
    而且这两张表是模块级的，进程重启之后也没人再管它们。
    """
    with _TABLES_LOCK:
        pending = [proc for processes in _TABLES.values() for proc in processes.values()]
        _TABLES.clear()
        _TAILS.clear()
        _STOPPED.clear()
    for process in pending:
        try:
            if process.poll() is None:
                process.kill()
        except Exception:                          # noqa: BLE001 —— 已经死了
            pass


@tool
class ShellBackgroundTool(ToolPlugin):
    """在后台执行长时间运行的命令。"""

    minimal_mode = True         # SHELL 类工具极简模式也开放

    def __init__(self, workspace=None) -> None:
        super().__init__(workspace)
    @property
    def key(self) -> str:
        """后台进程登记表的键：**当前会话的工作区**（不是构造期那个）。

        后台进程按工作区分组登记；用构造期的 `self.workspace`（`load_all()` 没传工作区时
        退化成进程 CWD）会让"在这个会话里起的进程"和"在那个会话里查/停的进程"对不上，
        也会把仓库根目录当成用户的工作区。见 `ToolPlugin.current_workspace()`。
        """
        return str(self.current_workspace())

    @property
    def id(self) -> str:
        return "tool.shell.background"

    @property
    def name(self) -> str:
        return "run_background"

    @property
    def description(self) -> str:
        return "在后台执行长时间运行的命令"

    @property
    def category(self) -> str:
        return ToolCategory.SHELL

    @property
    def permission(self) -> str:
        # 与 Java 一致：ShellBackgroundTool 没有覆盖 getRequiredPermission()，
        # 取 AbstractToolPlugin 的默认值 WORKSPACE_WRITE。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "命令"},
                "workdir": {"type": "string", "description": "工作目录"},
            },
            "required": ["command"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            command = self.get_required_string_arg(args, "command")
            workdir = self.get_string_arg(args, "workdir", "") or ""

            directory: str | None = None
            if workdir.strip():
                resolved = self.resolve_path(workdir)
                directory = str(resolved)
                if not resolved.is_dir():
                    return self.error("工作目录不存在: " + directory
                                      + "（先 create_directory 建出来，或去掉 workdir 用工作区根目录）")
            else:
                directory = self.key

            if is_windows__tools_shell_persistent_shell():
                argv = ["powershell", "-NoLogo", "-NoProfile", "-NonInteractive",
                        "-Command", command]
            else:
                argv = ["sh", "-c", command]

            # 【不能用 text=True + encoding="utf-8"】PS 5.1 子进程按系统 ANSI/OEM 代码页
            # （中文机器 = CP936/GBK）往管道写字节，utf-8 + errors="replace" 会把中文输出
            # 全解成 U+FFFD 乱码（"留最后 50 行方便排查"拿到的是废文本）。
            # 这里按字节收，drain 里走 UTF-8 → GBK → 替换 的退路（同 read_text/git 输出）。
            process = subprocess.Popen(
                argv,
                cwd=directory,
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                creationflags=NO_WINDOW,
            )

            tail: list[str] = []
            drain(process.stdout, tail)
            drain(process.stderr, tail)

            pid = uuid.uuid4().hex[:8]
            table(self.key)[pid] = process
            tails(self.key)[pid] = tail

            return self.success("后台进程已启动，PID: " + pid
                                + "\n工作目录: " + (directory if directory else "(继承)")
                                + "\n使用 stop_background 工具停止")
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("启动后台进程失败: " + str(exc))


# ========================================================================
# 原模块 lionbox/tools/shell/terminal_limits.py
# ========================================================================
"""终端插件的限制值（Java: `core/plugin/TerminalPlugin.java` + `PluginSettings`）。

【为什么放在这个包里】Java 版里"一条命令最长跑多久、最多带回多少字节"是用户在
**终端插件**的设置面板里改的，`ShellExecuteTool` 通过注入的 `TerminalPlugin` 读它：

    int timeout = terminalPlugin.clampTimeout(requested);
    int maxOutputBytes = terminalPlugin.maxOutputBytes();

端口时的约束是"只改 tools/shell 下的文件"，而终端插件属于 `lionbox/plugin/*`，
所以这里先按 Java 的默认值与语义落一份等价实现（默认 300 秒 / 200000 字节，
取小不取大）。等终端插件本体移植过来，把 `TerminalLimits` 的实现换成
"转读它的设置"即可 —— `ShellExecuteTool` 的调用点一个字都不用动。
"""


import json
import os
from pathlib import Path
from typing import Any

#: 与 Java `PluginSettings.DEFAULT_MAX_COMMAND_SECONDS` 一致：
#: Java 注释写明"ShellExecuteTool 在模型没给 timeout 时传 300，PersistentShell.run
#: 对非正数也回落 300"，所以 300 就是"保持现在的行为"。
DEFAULT_MAX_COMMAND_SECONDS = 300

#: 与 Java `PluginSettings.DEFAULT_MAX_OUTPUT_BYTES` 一致（≈200KB）。
#: 老版本完全不限，但一条 `type huge.log` 就能把 8k 上下文的本地模型冲得失忆。
DEFAULT_MAX_OUTPUT_BYTES__tools_shell_terminal_limits = 200_000

#: 终端设置所在的配置区（Java: `settings.intOf("terminal", …)`）
SETTINGS_SECTION = "terminal"

#: 设置文件名（Java: PluginPaths.settingsFile() → ~/.lioncode/plugins/settings.json）
_SETTINGS_FILE = Path(os.environ.get("LIONCODE_HOME", str(Path.home() / ".lioncode"))) \
    / "plugins" / "settings.json"


def _int_or(value: Any, default: int) -> int:
    if isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return default


class TerminalLimits:
    """终端插件的限制值：每次现读，改了设置下一条命令就生效（Java 的"不做字段缓存"）。"""

    def __init__(self, settings_file: Path | None = None) -> None:
        self._settings_file = settings_file or _SETTINGS_FILE
        self._cache: tuple[float, dict[str, Any]] | None = None

    def _section(self) -> dict[str, Any]:
        """读 `terminal` 段；文件没改就复用上次的结果（按 mtime 判）。"""
        try:
            mtime = self._settings_file.stat().st_mtime
        except OSError:
            return {}
        if self._cache is not None and self._cache[0] == mtime:
            return self._cache[1]
        try:
            raw_bytes = self._settings_file.read_bytes()
            # 【必须自己剥 BOM】这个文件是 Java 侧写的，实测用户机器上带 UTF-8 BOM
            # （记事本/"PowerShell Set-Content -Encoding UTF8" 都会写 BOM）。
            # json.loads 遇到开头的 \ufeff 直接抛 JSONDecodeError → 设置读不出来、
            # 悄悄退回默认值，表现是"我在设置里改了上限怎么没用"。
            # Java 侧 `Files.readString` + Jackson 能吃掉它，Python 这边要自己剥。
            text = raw_bytes.decode("utf-8", errors="replace")
            if text.startswith("\ufeff"):
                text = text[1:]
            raw = json.loads(text)
            section = raw.get(SETTINGS_SECTION) if isinstance(raw, dict) else None
        except (OSError, ValueError):
            return {}
        result = section if isinstance(section, dict) else {}
        self._cache = (mtime, result)
        return result

    def max_command_seconds(self) -> int:
        """一条命令最多跑多少秒（0 或负数没有意义，回落默认值）。"""
        value = _int_or(self._section().get("maxCommandSeconds"), DEFAULT_MAX_COMMAND_SECONDS)
        return value if value > 0 else DEFAULT_MAX_COMMAND_SECONDS

    def max_output_bytes(self) -> int:
        """一条命令最多带回多少字节（0 = 不限制）。"""
        return max(_int_or(self._section().get("maxOutputBytes"), DEFAULT_MAX_OUTPUT_BYTES__tools_shell_terminal_limits), 0)

    def clamp_timeout(self, requested_seconds: int | None) -> int:
        """把工具请求的超时和插件上限取小值。

        取小不取大：模型自己写的 `timeout` 只是它的"期望"，插件的上限是用户的"规定"。
        规定优先，否则模型写个 99999 就把限制绕过去了。
        """
        limit = self.max_command_seconds()
        if requested_seconds is None or requested_seconds <= 0:
            return limit
        return min(requested_seconds, limit)


# ========================================================================
# 原模块 lionbox/tools/shell/shell_execute.py
# ========================================================================
"""Shell 命令执行工具（常驻终端）—— Java: `core/plugin/tool/shell/ShellExecuteTool.java`。

它不是"每条命令起一个进程"，而是把这个工作区的一个**长期活着的 PowerShell** 当终端用：
命令流里 `cd`、变量、函数都会留到下一次调用（实现见 `PersistentShell`）。
所以模型可以像人在终端里一样一条条往下做，而不是每条命令都在一个全新的、
忘了刚才做过什么的进程里跑。

【谁说了算】模型给的 timeout 只是它的"期望"，用户在终端插件里设的上限是"规定"。
取小值 —— 否则模型随手写个 99999 就把用户设的限制绕过去了。
"""


import re
import threading
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: Unix 写法 → PowerShell 等价写法（与 Java 的 unixToPowerShell 逐条对应）
_UNIX_TO_PS: tuple[tuple[str, str], ...] = (
    (r"\bll\b", "ls -Force"),                                              # ll → 列全部文件
    (r"\bls\s+-[a-zA-Z]*l[a-zA-Z]*(\s|$)", r"ls -Force\1"),                # ls -la / ls -l / ls -al
    (r"\bls\s+-a(\s|$)", r"ls -Force\1"),                                  # ls -a
    (r"\brm\s+-rf\b", "Remove-Item -Recurse -Force"),                      # rm -rf
    (r"\brm\s+-fr\b", "Remove-Item -Recurse -Force"),                      # rm -fr
    (r"\brm\s+-r\b", "Remove-Item -Recurse"),                              # rm -r
    (r"\brm\s+-f\b", "Remove-Item -Force"),                                # rm -f
    (r"\bcp\s+-r\b", "Copy-Item -Recurse"),                                # cp -r
    (r"\bmv\s+-f\b", "Move-Item -Force"),                                  # mv -f
    (r"\bmkdir\s+-p\b", "New-Item -ItemType Directory -Force"),            # mkdir -p
    (r"\bmkdir\s+-p\s+", "New-Item -ItemType Directory -Force -Path "),    # mkdir -p <目录>
    (r"\bgrep\b", "Select-String"),
    (r"\btouch\b", "New-Item -ItemType File -Force"),
    (r"\bwhich\b", "Get-Command"),
    (r"\bps\s+aux\b", "Get-Process"),
    (r"\bhead\s+-n\s+(\d+)\s+", r"Get-Content -TotalCount \1 "),           # head -n 5 file
    (r"\btail\s+-n\s+(\d+)\s+", r"Get-Content -Tail \1 "),                 # tail -n 5 file
)

#: 用了 cmd 的 `/x` 风格开关时，哪些命令名说明这是 cmd 语法
_CMD_SWITCH_COMMANDS = ("rmdir", "rd", "del", "erase", "copy", "move", "xcopy",
                        "robocopy", "attrib", "icacls", "net")

#: cmd 独占的命令名（PowerShell 里没有同名 cmdlet 或语义完全不同）
_CMD_BUILTINS = ("dir", "type", "findstr", "tasklist", "taskkill", "where", "ver", "set")


def unix_to_powershell(command: str) -> str:
    """把常见的 Unix 写法翻成 PowerShell 等价写法。

    【实测】模型写 `echo hello && ls -la`，PowerShell 报
    "Get-ChildItem : 找不到与参数名称"la"匹配的参数"。这类 Unix 开关在 PowerShell 里
    **永远不可能合法**，所以按模式翻译是安全的（只翻确定的几种，不做通用猜测）。
    """
    if not command or not command.strip():
        return command
    c = command
    for pattern, replacement in _UNIX_TO_PS:
        c = re.sub(pattern, replacement, c)
    return c


def looks_like_cmd(command: str) -> bool:
    """这条命令像不像 cmd 语法。

    判据：用了 cmd 的内置命令 + `/x` 风格开关（`rmdir /s /q`、`del /f`、`xcopy /e`…），
    或者 cmd 独占的命令名（`dir`、`type`、`findstr`、`tasklist`、`taskkill`）。

    【命令名后面只能是空白或结尾】本机 execute_command 走的是 **PowerShell**，
    用 `\b` 判词边界会把 `Set-Content`、`Where-Object`、`Set-Item` 这些 cmdlet 的前缀
    （`set`/`where` 后面紧跟 `-`，`\b` 照样成立）当成 cmd 语法送进 `cmd /c`，
    合法命令必然失败（exit 9009）。裸 `set x=1` / `where.exe git` 才是 cmd。
    """
    if not command or not command.strip():
        return False
    c = command.strip().lower()
    slash_switch = re.search(r"\s/[a-z](\s|$)", c) is not None
    if slash_switch:
        for name in _CMD_SWITCH_COMMANDS:
            if re.search(r"\b" + name + r"\b", c):
                return True
    return re.match(r"^(" + "|".join(_CMD_BUILTINS) + r")(?:\s|$)", c) is not None


@tool
class ShellExecuteTool(ToolPlugin):
    """在常驻终端里执行命令。"""

    minimal_mode = True         # SHELL 类工具极简模式也开放（Java: isAvailableInMode(MINIMAL)）

    def __init__(self, workspace=None, shell: PersistentShell | None = None,
                 terminal: TerminalLimits | None = None) -> None:
        super().__init__(workspace)
        self._terminal = terminal or TerminalLimits()
        self._shell = shell
        self._shell_lock = threading.Lock()

    @property
    def id(self) -> str:
        return "tool.shell.execute"

    @property
    def name(self) -> str:
        return "execute_command"

    @property
    def description(self) -> str:
        return ("在常驻终端里执行命令（同一工作区共用一个持续运行的 PowerShell 会话，"
                "cd、变量、函数会保留到下一次调用）")

    @property
    def category(self) -> str:
        return ToolCategory.SHELL

    @property
    def permission(self) -> str:
        # 工具本身是"执行命令"，但 shell 既能读也能写，与 Java 的默认值保持一致
        # （ShellExecuteTool 没有覆盖 getRequiredPermission()）。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "command": {"type": "string", "description": "要执行的命令"},
                "workdir": {"type": "string",
                            "description": "工作目录（可选；给了就先切过去，之后的命令留在这个目录）"},
                "timeout": {"type": "integer", "description": "超时秒数", "default": 60},
            },
            "required": ["command"],
        }

    @property
    def shell(self) -> PersistentShell:
        """整个进程共用一个常驻终端管理器（Java 里它是 Spring 单例 `@Component`）。"""
        if self._shell is None:
            with self._shell_lock:
                if self._shell is None:
                    self._shell = _shared_shell()
        return self._shell

    def on_abandoned(self) -> None:
        """上层因超时**放弃**这次调用时被调用：把当前工作区的常驻终端关掉。

        【为什么必须关】`python` 线程杀不掉，主循环的 `cancel_futures` 只能取消排队中的任务 ——
        正在跑的 `Start-Sleep -Seconds 300` 会**一直占着那个常驻终端**（终端是"一个工作区一个
        长驻进程"），于是下一条 `execute_command` 排队等同一个终端、同样超时。
        用户看到的现象就是"卡住的命令把终端堵死了，之后什么都跑不了"。

        关掉之后下一次调用会重开一个干净终端（`close()` 会把会话从表里摘掉并杀掉进程）。
        这也是 Java `PersistentShell` 在超时时的做法（"已强制重启终端"）。
        """
        try:
            self.shell.close(str(self.current_workspace()))
        except Exception:                     # noqa: BLE001 清理失败不该影响"已超时"这个结论
            pass
    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            command = self.get_required_string_arg(args, "command")
            workdir = self.get_string_arg(args, "workdir", "") or ""

            # 模型给的是"期望"，终端插件里的上限是"规定" —— 取小值（见模块头注释）
            requested = self.get_int_arg(args, "timeout", 0)
            timeout = self._terminal.clamp_timeout(requested)
            max_output_bytes = self._terminal.max_output_bytes()

            # 目标目录先解析+检查，别把不存在的目录塞进终端（那只会回一句看不懂的报错）
            directory: str | None = None
            if workdir.strip():
                resolved = self.resolve_path(workdir)
                directory = str(resolved)
                if not resolved.is_dir():
                    return self.error("工作目录不存在: " + directory
                                      + "（先 create_directory 建出来，或检查路径）")

            prepared = command
            if is_windows__tools_shell_persistent_shell():
                # 【实测】模型两种写法都会用：
                #   ls -la            → PowerShell 别名，用 cmd 会报"不是内部或外部命令"
                #   rmdir /s /q xxx   → cmd 开关，用 PowerShell 会报"找不到与参数名称/q匹配的参数"
                # 所以按写法分流：带 cmd 风格开关的交给 `cmd /c`（在常驻终端里跑，不另起 shell），
                # 其余按 PowerShell 走，并把 Unix 写法翻译过来。
                if looks_like_cmd(prepared):
                    prepared = "cmd /c '" + prepared.replace("'", "''") + "'"
                else:
                    # PowerShell 5.1 不认 `&&`：模型很爱写 `ls && pwd`，换成 `;`
                    prepared = unix_to_powershell(prepared).replace("&&", ";")

            result = self.shell.run(str(self.current_workspace()), prepared, directory,
                                    timeout, max_output_bytes)
            if result.error_text is not None:
                # 【已经收到的输出不能白丢】致命错误（超时/输出失控/终端退出）之前命令
                # 往往已经吐了一部分，那是模型判断"命令到底跑到哪一步"的唯一线索。
                if result.output:
                    return self.error(result.error_text + "\n已收到的输出:\n" + result.output)
                return self.error(result.error_text)

            out: list[str] = []
            if result.output:
                out.append("输出:\n" + result.output + "\n")
            else:
                out.append("（这条命令没有输出）\n")
            # 【必须明确告诉模型"被截断了"】不提示的话它会把"没看到"当成"不存在"，
            # 然后基于不完整的信息下结论（"日志里没有报错"）。说清了它才知道换个更精确的查法。
            if result.truncated:
                out.append("⚠ 输出已截断：这条命令的输出超过了终端设置的上限（"
                           + str(max_output_bytes)
                           + " 字节），后面的内容没有带回来。要看全就用更精确的命令"
                           + "（例如 Select-String 过滤、Get-Content -TotalCount 只看前几行），"
                           + "或在设置 → 插件 → 终端里调大「最大输出字节数」。\n")
            if result.cwd is not None:
                out.append("当前目录: " + result.cwd + "\n")
            code = result.exit_code
            out.append("退出码: " + str(code if code is not None else (0 if result.ok else 1)))

            if result.ok and (code is None or code == 0):
                return self.success("".join(out))

            # 【实测】退出码非 0 但明明有输出时（例如 git 在非仓库目录报 128、grep 没匹配到），
            # 一律写成"执行失败"会让模型以为命令根本没跑。这里把"有没有输出"说清楚，
            # 常见的 128 / 1 再补一句提示，它下一轮就能改对。
            fail: list[str] = []
            # 退出码是 0 也可能是失败：PersistentShell 每条命令前把 $LASTEXITCODE 归零（哨兵），
            # 所以 code=0 且 $? = False 表示这是条纯 cmdlet 命令、真正的失败原因在输出里。
            # 这时写成"命令以退出码 0 结束"会被模型读成"成功了"。
            if not result.ok and code == 0:
                fail.append("命令失败（PowerShell 报 $?=False，没跑原生命令所以没有退出码）")
            else:
                fail.append("命令以退出码 " + (str(code) if code is not None else "非0") + " 结束")
            fail.append("（没有任何输出）" if not result.output else "（**有输出**，见下）")
            if code == 128:
                fail.append("；128 是 git 的 fatal：多半是当前目录不是 git 仓库"
                            "（先 git_init，或用 path 指定仓库目录）")
            fail.append("\n")
            fail.append("".join(out))
            return self.error("".join(fail))
        except Exception as exc:                       # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("命令执行异常: " + str(exc))


#: 进程级共享的常驻终端（Java 里 PersistentShell 是单例，所有工作区共用一个实例、各有各的会话）
_SHARED_SHELL: PersistentShell | None = None
_SHARED_SHELL_LOCK = threading.Lock()


def _shared_shell() -> PersistentShell:
    global _SHARED_SHELL
    with _SHARED_SHELL_LOCK:
        if _SHARED_SHELL is None:
            _SHARED_SHELL = PersistentShell()
        return _SHARED_SHELL


# ========================================================================
# 原模块 lionbox/tools/shell/shell_stop.py
# ========================================================================
"""停止后台进程工具 —— Java: `core/plugin/tool/shell/ShellStopTool.java`。

【实测】模型常想"把后台的东西停掉"，但手上没有 pid（上一轮 run_background 的返回值
它没记住），于是编一个 id 传进来 → 必然 ❌。所以允许不给 pid：这个工作区只有一个在跑
就直接停它（这才是它真正想要的），多个就把名单回给它挑。
"""


from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class ShellStopTool(ToolPlugin):
    """停止后台运行的进程。"""

    minimal_mode = True         # SHELL 类工具极简模式也开放

    def __init__(self, workspace=None) -> None:
        super().__init__(workspace)
    @property
    def key(self) -> str:
        """后台进程登记表的键：**当前会话的工作区**（不是构造期那个）。

        后台进程按工作区分组登记；用构造期的 `self.workspace`（`load_all()` 没传工作区时
        退化成进程 CWD）会让"在这个会话里起的进程"和"在那个会话里查/停的进程"对不上，
        也会把仓库根目录当成用户的工作区。见 `ToolPlugin.current_workspace()`。
        """
        return str(self.current_workspace())

    @property
    def id(self) -> str:
        return "tool.shell.stop"

    @property
    def name(self) -> str:
        return "stop_background"

    @property
    def description(self) -> str:
        return "停止后台运行的进程"

    @property
    def category(self) -> str:
        return ToolCategory.SHELL

    @property
    def permission(self) -> str:
        # 与 Java 一致：ShellStopTool 没有覆盖 getRequiredPermission()，取基类默认值。
        return PermissionLevel.WORKSPACE_WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "pid": {"type": "string",
                        "description": "进程ID（省略则停掉最近启动的那个后台进程）"},
            },
            "required": [],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            # 【实测】两条后台命令正常跑完之后，不带 pid 的 stop_background 会回
            # "有多个后台进程在跑，指定要停哪个" —— 名单里全是已经退出的进程，于是它谁也停不了。
            # 先按"还活着吗"把死进程从表里清掉，再判断"现在有几个在跑"。
            finished = reap_finished(self.key)
            pid = self.get_string_arg(args, "pid", "") or ""

            # 【实测】模型常常没有 pid（上一轮 run_background 的返回值它没记住）：
            # 只有一个在跑就直接停它；多个就把名单回给它挑。
            if not pid.strip() or pid.strip().lower() == "null":
                ids = list(table(self.key))
                if not ids:
                    return self.error("当前没有在跑的后台进程（run_background 启动后会返回 pid）")
                if len(ids) > 1:
                    return self.error("有多个后台进程在跑，指定要停哪个：pid=" + " / ".join(ids))
                pid = ids[0]

            if pid in finished or was_stopped(self.key, pid):
                # 它自己已经跑完了（或者上一条 stop_background 刚把它停掉）——
                # 用户/模型要的就是"它别在跑"，直接当成功回，别报"未找到进程"
                # （那会让人以为还得再想办法）。
                return self.success("这个后台进程已经自己结束了，不用再停: " + pid)

            process = forget(self.key, pid)
            if process is None:
                # 实测模型会拿一个自己编的 pid 来停（a7472d31）。
                # 把当前真在跑的后台进程 id 列出来，它下一轮就能用对。
                alive = list(table(self.key))
                if not alive:
                    return self.error("未找到进程: " + pid
                                      + "（当前没有在跑的后台进程；先用 run_background 启动，"
                                        "它会返回 pid）")
                return self.error("未找到进程: " + pid
                                  + "（当前在跑的后台进程: " + ", ".join(alive) + "）")

            try:
                process.kill()
            except Exception:                      # noqa: BLE001 —— 刚好自己退出了也算停住了
                pass
            return self.success("进程已停止: " + pid)
        except Exception as exc:                   # noqa: BLE001 —— 与 Java catch(Exception) 对齐
            return self.error("停止进程失败: " + str(exc))


# ========================================================================
# 原模块 lionbox/tools/shell.py
# ========================================================================
"""shell 工具包（3 个工具 + 1 个常驻终端插件，与 Java 的 `core/plugin/tool/shell` 包一一对应）。

  - `PersistentShell`   常驻终端插件（Java 的 `@Component PersistentShell`），**不是工具**，
                        所以这里没有 `@tool` 登记；
  - `ShellExecuteTool`  execute_command  跑在常驻终端里
  - `ShellBackgroundTool` run_background 后台进程
  - `ShellStopTool`     stop_background  停止后台进程
"""



__all__ = [
    "PersistentShell",
    "RunResult",
    "ShellBackgroundTool",
    "ShellExecuteTool",
    "ShellStopTool",
    "TerminalLimits",
]


# ========================================================================
# 原模块 lionbox/tools/system/ask_user.py
# ========================================================================
"""`ask_user` —— 向用户提问并等待回答。

【契约来源】`core/plugin/tool/system/AskUserTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【怎么接进去】Java 里它依赖 `UserQuestionService`（提问服务）和 `SoundNotifier`（提问音效），
两者都在 `core/question`、`core/sound` 包里 —— 按分工不归这次移植建。
所以这里照 `_gate` 那套做法留**显式接线点**：`set_question_service(...)` / `set_sound_notifier(...)`，
启动时由接线方挂上；没挂就返回一句明确失败（PORTING.md 第四条：不许吞异常、不许假装成功）。

【超时的两条规矩（都是实测踩出来的）】
- 下限 30 秒：实测模型传 `timeoutSeconds=5`，人根本来不及答，它自己连着试了 8 次全部超时。
  提问是给人答的，不是给机器答的。
- 上限 300 秒（`MAX_TIMEOUT`）。
"""


import re
from typing import Any, Callable, Protocol

from lionbox.plugins.base import PermissionLevel, ToolPlugin, ToolResult, tool

MAX_TIMEOUT = 300
MIN_TIMEOUT = 30
DEFAULT_TIMEOUT_SECONDS__tools_system_ask_user = 300

#: 选项最多给几个：太多了界面也没法看
MAX_OPTIONS = 8

#: 逗号分隔的兼容切分（包含中文逗号、顿号、竖线）
_OPTION_SPLIT = re.compile("[,，、|]")


class QuestionResult(Protocol):
    """`UserQuestionService.Result` 的同形结构：status + answer/text。"""

    status: str      # ANSWERED / TIMEOUT / CANCELLED
    answer: str
    text: str


QuestionService = Callable[[str, str, list[str], int], QuestionResult]
"""`questionService.ask(sessionId, question, options, timeout)` 的可调用形式。

【两种形状都要认】Java 侧 `AskUserTool` 注入的是 `UserQuestionService` **对象**，
调的是 `service.ask(...)`；本模块原来的接线契约写成了"可调用对象"，于是装配方
（`assembly._hook_ask_user` / `wiring.wire_tool_hooks`）把真实对象挂上去之后，
`QUESTION_SERVICE(...)` 直接抛 `'UserQuestionService' object is not callable`
（`_check_ask_user.py` 抓到的就是这个）。真实实现是对象形态，所以下面统一用
`_ask()` 取用：有 `ask()` 就调它，否则当成可调用对象 —— 接线方不用猜。"""


def _ask(service: Any, session_id: str, question: str,
         options: list[str], timeout: int) -> QuestionResult:
    """调用提问服务（兼容"对象 + ask()"与"可调用对象"两种形状）。"""
    ask = getattr(service, "ask", None)
    if callable(ask):
        return ask(session_id, question, options, timeout)
    return service(session_id, question, options, timeout)


QUESTION_SERVICE: QuestionService | None = None
"""当前挂上的提问服务；None = 还没接线。"""

SOUND_NOTIFIER: Callable[[str], None] | None = None
"""当前挂上的音效通知；None = 不响（Java 里由 SoundNotifier 播 QUESTION）。"""


def set_question_service(service: QuestionService | None) -> None:
    """挂上/摘掉提问服务。接线方在启动时调一次。"""
    global QUESTION_SERVICE
    QUESTION_SERVICE = service


def set_sound_notifier(notifier: Callable[[str], None] | None) -> None:
    """挂上/摘掉音效通知（kind 传 `"QUESTION"`）。"""
    global SOUND_NOTIFIER
    SOUND_NOTIFIER = notifier


@tool
class AskUserTool(ToolPlugin):
    """向用户提问并等待回答的工具。"""

    minimal_mode = False         # Java: ToolCategory.OTHER 在 MINIMAL 下不开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.system.ask_user"

    @property
    def name(self) -> str:
        return "ask_user"

    @property
    def description(self) -> str:
        return ("向用户提问并等待回答。当信息不足、需求含糊或要执行不可逆操作时先问清楚，"
                "不要靠猜。能自己从工作区查到的信息不要问。")

    @property
    def category(self) -> str:
        return "OTHER"

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "要问用户的问题，尽量具体、一次问清一件事",
                },
                "options": {
                    "type": "array",
                    "description": "可选项（可选）。给了的话界面上会显示成按钮，用户点一下就行；"
                                   "不给就是自由输入",
                    "items": {"type": "string"},
                },
                "timeoutSeconds": {
                    "type": "integer",
                    "description": "最多等多少秒（可选，默认 300，最少 30 —— 人答题需要时间，别填几秒）",
                },
            },
            "required": ["question"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            question = self.get_required_string_arg(args, "question")
        except ValueError:
            # Java 这里把 base 的报错整句换掉，只留这一句
            return self.error("缺少必填参数：question（要问用户的问题）")

        session_id = _current_session_id__tools_system_ask_user()
        if not session_id:
            # 理论上不会发生：AgentLoop 执行工具前一定会设置会话上下文
            return self.error("当前不在会话上下文里，无法向用户提问")

        if QUESTION_SERVICE is None:
            # 显式失败而不是假装成功：提问服务还没接线（见模块 docstring）
            return self.error("提问服务还没接线（lionbox 里需要先 set_question_service）")

        options = _read_options(args)
        timeout = _read_timeout(args)

        # 提问音效：让用户不用盯着屏幕也知道"它在问我"
        if SOUND_NOTIFIER is not None:
            SOUND_NOTIFIER("QUESTION")

        result = _ask(QUESTION_SERVICE, session_id, question, options, timeout)
        status = result.status
        if status == "ANSWERED":
            return self.success(f"用户回答：{result.answer}")
        if status in ("TIMEOUT", "CANCELLED"):
            return self.success(result.text)
        return self.error(f"未知的提问状态: {status}")


def _current_session_id__tools_system_ask_user() -> str | None:
    """当前会话 id（Java: `SessionContext.get()`）。

    【原来的写法读错了地方】`from ...sessions import context as session_context` 拿到的是
    **模块对象**，而那个模块里只有类 `SessionContext`，没有模块级的 `get()` ——
    两次 getattr 全部落空、直接返回 None。于是工具永远回
    "当前不在会话上下文里，无法向用户提问"（`_check_ask_user.py` 抓到的就是这个）。
    真实实现是 `lionbox.sessions.SessionContext`（与 AgentLoop 用的是同一份 thread-local）。
    """
    try:
        from lionbox.sessions import SessionContext
    except ImportError:
        return None
    try:
        value = SessionContext.get()
    except Exception:               # noqa: BLE001 - 会话模块没就绪时按"没有会话"处理
        return None
    text = "" if value is None else str(value).strip()
    return text or None


def _read_options(args: dict[str, Any]) -> list[str]:
    """读 options：既支持数组，也兼容前端/模型传过来的逗号分隔字符串。"""
    raw = args.get("options")
    out: list[str] = []
    if isinstance(raw, (list, tuple)):
        for item in raw:
            if item is not None and str(item).strip():
                out.append(str(item).strip())
    elif isinstance(raw, str) and raw.strip():
        for part in _OPTION_SPLIT.split(raw):
            if part.strip():
                out.append(part.strip())
    return out[:MAX_OPTIONS]


def _read_timeout(args: dict[str, Any]) -> int:
    """读 timeoutSeconds，夹到 [MIN_TIMEOUT, MAX_TIMEOUT]（传了乱七八糟的东西用默认值）。"""
    raw = args.get("timeoutSeconds")
    timeout = DEFAULT_TIMEOUT_SECONDS__tools_system_ask_user
    if isinstance(raw, bool):
        timeout = DEFAULT_TIMEOUT_SECONDS__tools_system_ask_user
    elif isinstance(raw, (int, float)):
        timeout = int(raw)
    elif isinstance(raw, str):
        try:
            timeout = int(raw.strip())
        except ValueError:
            timeout = DEFAULT_TIMEOUT_SECONDS__tools_system_ask_user
    if timeout <= 0:
        timeout = DEFAULT_TIMEOUT_SECONDS__tools_system_ask_user
    return min(max(timeout, MIN_TIMEOUT), MAX_TIMEOUT)


# ========================================================================
# 原模块 lionbox/tools/system/env_var.py
# ========================================================================
"""`get_env` —— 查看环境变量。

【契约来源】`core/plugin/tool/system/EnvVarTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。
"""


import os
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolPlugin, ToolResult, tool


@tool
class EnvVarTool(ToolPlugin):
    """环境变量查看工具。"""

    minimal_mode = False         # Java: ToolCategory.OTHER 在 MINIMAL 下不开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.system.env"

    @property
    def name(self) -> str:
        return "get_env"

    @property
    def description(self) -> str:
        return "查看环境变量"

    @property
    def category(self) -> str:
        return "OTHER"

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        # Java 的 Map.of(type, properties) 里**没有 required**，别补上
        return {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "变量名（可选，不填返回全部）"},
            },
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            name = self.get_string_arg(args, "name", "") or None
            if name is not None:
                value = os.environ.get(name)
                # Java 的 System.getenv 在 Windows 上大小写不敏感，Python 的 os.environ 也是
                return self.success(f"{name}={value if value is not None else '（未设置）'}")
            out = "".join(f"{k}={v}\n" for k, v in os.environ.items())
            return self.success(out)
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"读取环境变量失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/system/system_info.py
# ========================================================================
"""`system_info` —— 获取系统运行时信息。

【契约来源】`core/plugin/tool/system/SystemInfoTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【字段映射】Java 用 JVM 的 Runtime/MemoryMXBean/RuntimeMXBean；Python 没有 JVM，
按同样含义映射：
  操作系统      -> `platform.system()`（Java `os.name`，Windows 上两者都是 "Windows"）
  版本          -> `platform.release()`（Java `os.version`）
  Java版本      -> `platform.python_version()`（**字段名照抄 Java 不动**：它进的是模型
                   看到的文本，改名会让"两边同一接口逐字段一致"的回归断言对不上）
  可用处理器     -> `os.cpu_count()`
  最大内存/已用/空闲 -> 没有 JVM 堆这回事，用**进程自身**的常驻内存按同样三项输出：
                   最大内存给机器物理内存、已用给本进程 RSS、空闲 = 最大 - 已用
  运行时间       -> 本进程已运行秒数
"""


import os
import platform
import sys
import time
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolPlugin, ToolResult, tool

_STARTED_AT = time.monotonic()
_MB = 1024 * 1024


@tool
class SystemInfoTool(ToolPlugin):
    """系统信息工具。"""

    minimal_mode = False         # Java: ToolCategory.OTHER 在 MINIMAL 下不开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.system.info"

    @property
    def name(self) -> str:
        return "system_info"

    @property
    def description(self) -> str:
        return "获取系统运行时信息"

    @property
    def category(self) -> str:
        return "OTHER"

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        # Java 的 Map.of("type", "object", "properties", Map.of()) —— 没有 required
        return {"type": "object", "properties": {}}

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            max_mem = _total_memory_bytes()
            used_mem = _resident_bytes()
            free_mem = max(0, max_mem - used_mem) if max_mem > 0 else 0
            return self.success(
                f"操作系统: {platform.system()} {platform.release()}\n"
                f"Java版本: {platform.python_version()}\n"
                f"可用处理器: {os.cpu_count() or 0}\n"
                f"最大内存: {max_mem // _MB} MB\n"
                f"已用内存: {used_mem // _MB} MB\n"
                f"空闲内存: {free_mem // _MB} MB\n"
                f"运行时间: {int(time.monotonic() - _STARTED_AT)} 秒")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"获取系统信息失败: {e}")


def _total_memory_bytes() -> int:
    """机器物理内存（Java 那边是 JVM 的 `Runtime.maxMemory()`）。

    `os.sysconf` 只有 POSIX 有，Windows 上得问 `GlobalMemoryStatusEx`。
    两条路都取不到就报 0（不编数字）。
    """
    try:
        return os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")
    except (AttributeError, ValueError, OSError):
        pass
    if os.name == "nt":
        try:
            import ctypes

            class _MemoryStatusEx(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = _MemoryStatusEx()
            status.dwLength = ctypes.sizeof(status)
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            kernel32.GlobalMemoryStatusEx.argtypes = [ctypes.POINTER(_MemoryStatusEx)]
            kernel32.GlobalMemoryStatusEx.restype = ctypes.c_int
            if kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.ullTotalPhys)
        except Exception:           # noqa: BLE001 - 取不到就报 0
            return 0
    return 0


def _resident_bytes() -> int:
    """本进程的常驻内存（Java 那边是 `totalMemory() - freeMemory()`）。

    只用标准库：Windows 走 `psapi.GetProcessMemoryInfo` 的 WorkingSetSize，
    其他平台退回 `resource.getrusage` 的峰值 RSS。取不到就报 0，不编数字。
    """
    if os.name == "nt":
        try:
            import ctypes
            from ctypes import wintypes

            class _ProcessMemoryCounters(ctypes.Structure):
                _fields_ = [
                    ("cb", wintypes.DWORD),
                    ("PageFaultCount", wintypes.DWORD),
                    ("PeakWorkingSetSize", ctypes.c_size_t),
                    ("WorkingSetSize", ctypes.c_size_t),
                    ("QuotaPeakPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaPeakNonPagedPoolUsage", ctypes.c_size_t),
                    ("QuotaNonPagedPoolUsage", ctypes.c_size_t),
                    ("PagefileUsage", ctypes.c_size_t),
                    ("PeakPagefileUsage", ctypes.c_size_t),
                ]

            counters = _ProcessMemoryCounters()
            counters.cb = ctypes.sizeof(counters)
            kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
            psapi = ctypes.WinDLL("psapi", use_last_error=True)
            kernel32.GetCurrentProcess.restype = wintypes.HANDLE
            psapi.GetProcessMemoryInfo.argtypes = [
                wintypes.HANDLE, ctypes.POINTER(_ProcessMemoryCounters), wintypes.DWORD]
            psapi.GetProcessMemoryInfo.restype = wintypes.BOOL
            handle = kernel32.GetCurrentProcess()
            if psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
                return int(counters.WorkingSetSize)
            return 0
        except Exception:           # noqa: BLE001 - 取不到就报 0，不编数字
            return 0
    try:
        import resource

        usage = resource.getrusage(resource.RUSAGE_SELF)
        # Linux 的 ru_maxrss 是 KB，macOS 是字节
        return int(usage.ru_maxrss) * (1 if sys.platform == "darwin" else 1024)
    except Exception:               # noqa: BLE001
        return 0


# ========================================================================
# 原模块 lionbox/tools/system/working_dir.py
# ========================================================================
"""`working_directory` —— 获取或设置当前工作目录。

【契约来源】`core/plugin/tool/system/WorkingDirTool.java` 逐行对照。
id / name / description / parameters_schema 与 Java 版**逐字一致**。

【只读】Java 的实现只返回 `System.getProperty("user.dir")`，**没有**设置功能
（描述里那句"或设置"是历史遗留）。这里照抄实现，不多做：
schema 里没有参数，`execute` 一律返回当前目录。
"""


import os
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolPlugin, ToolResult, tool


@tool
class WorkingDirTool(ToolPlugin):
    """工作目录工具。"""

    minimal_mode = False         # Java: ToolCategory.OTHER 在 MINIMAL 下不开放

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.system.cwd"

    @property
    def name(self) -> str:
        return "working_directory"

    @property
    def description(self) -> str:
        return "获取或设置当前工作目录"

    @property
    def category(self) -> str:
        return "OTHER"

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        # Java 的 Map.of("type", "object", "properties", Map.of()) —— 没有 required
        return {"type": "object", "properties": {}}

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            return self.success(f"当前工作目录: {os.getcwd()}")
        except Exception as e:      # noqa: BLE001 - 与 Java 的 catch(Exception) 对齐
            return self.error(f"获取工作目录失败: {e}")


# ========================================================================
# 原模块 lionbox/tools/system.py
# ========================================================================
"""system 工具包（4 个，与 Java 的 `core/plugin/tool/system` 包一一对应）。

显式登记：每个模块在自己的 `@tool` 装饰器里登记工具类，`__init__` 只做"按名字导入"，
不做目录扫描（见 PORTING.md 一.3）。

  - `AskUserTool`     ask_user           向用户提问并等待回答（需要接线提问服务）
  - `EnvVarTool`      get_env            查看环境变量
  - `SystemInfoTool`  system_info        获取系统运行时信息
  - `WorkingDirTool`  working_directory  获取或设置当前工作目录

这四个的 `ToolCategory` 都是 `OTHER`，所以极简模式下**都不开放**
（Java `isAvailableInMode(MINIMAL)` 实测返回 false）。
"""



__all__ = [
    "AskUserTool",
    "EnvVarTool",
    "SystemInfoTool",
    "WorkingDirTool",
]


# ========================================================================
# 原模块 lionbox/tools/web/dns_lookup.py
# ========================================================================
"""DNS 查询工具（对应 Java `core/plugin/tool/web/DnsLookupTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 WEB_SEARCH，极简模式不开放）。

【行为对齐】Java 用 `InetAddress.getAllByName` 拿到**全部**地址（IPv4 + IPv6）逐个输出，
这里用 `socket.getaddrinfo` 做同样的事，并按出现顺序去重（同一个地址被解析出多条记录时
Java 也只列一次实际返回的地址列表）。
"""


import socket
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool


@tool
class DnsLookupTool(ToolPlugin):
    """DNS域名解析查询"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.web.dns"

    @property
    def name(self) -> str:
        return "dns_lookup"

    @property
    def description(self) -> str:
        return "DNS域名解析查询"

    @property
    def category(self) -> str:
        return ToolCategory.WEB

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "hostname": {"type": "string", "description": "主机名"},
            },
            "required": ["hostname"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            hostname = self.get_required_string_arg(args, "hostname")
            infos = socket.getaddrinfo(hostname, None, proto=socket.IPPROTO_TCP)
            seen: list[str] = []
            for info in infos:
                address = _java_ip_text(info[4][0])
                if address not in seen:
                    seen.append(address)
            out = ["域名: " + hostname]
            out.extend("IP: " + address for address in seen)
            return self.success("\n".join(out) + "\n")
        except Exception as e:
            return self.error("DNS查询失败: " + str(e))


def _java_ip_text(address: str) -> str:
    """IPv6 按 Java `InetAddress.getHostAddress()` 的写法展开（不做 :: 压缩）。

    实测同一台机器：Java 输出 `0:0:0:0:0:0:0:1`，Python 默认输出 `::1` —— 同一个地址，
    但文本不一样会让"两边同一接口逐字段一致"的对照过不去，所以这里按 Java 的格式展开。
    """
    if ":" not in address:
        return address
    try:
        packed = socket.inet_pton(socket.AF_INET6, address)
    except OSError:
        return address
    groups = [format(int.from_bytes(packed[i:i + 2], "big"), "x") for i in range(0, 16, 2)]
    return ":".join(groups)


# ========================================================================
# 原模块 lionbox/tools/web/download_file.py
# ========================================================================
"""文件下载工具（对应 Java `core/plugin/tool/web/DownloadTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 WEB_SEARCH）；
权限对齐 Java 基类默认的 WORKSPACE_WRITE → `PermissionLevel.WRITE`（要往工作区写文件）。

【行为对齐 + 移植要求的两处加固】
1. 与 Java 一致的：相对路径按工作区解析（resolvePath）、父目录自动创建、
   非 2xx 返回 `下载失败: HTTP {code}`（不假装成功）、成功文案 `文件已下载: {路径} ({n}字节)`。
2. 【移植要求】Java 是"整块读进内存再写"（大文件会打满内存），这里改成
   **边下边写临时文件 + 落盘改名**：
     * 先写 `<目标>.part`，下完再 `os.replace` 成正式文件 —— 中途失败不会留下半个"正式文件"；
     * 目标已存在时照 Java 的语义**覆盖**，但会在结果里说明一句（不然用户以为没动）；
     * `.part` 还在且非空时用 `Range: bytes=N-` 续传（服务器无视 Range 返回 200 时自动从头重下）；
     * 大小上限 200MB（Java 没有上限），超了就中止并说明。
"""


import os
import urllib.error
import urllib.request
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 连接 10s / 读 120s（与 Java 的 OkHttp 配置一致；urllib 只有一个超时，取读超时）
TIMEOUT = 120

#: 单个文件最多下多大（防"下一个 4GB 镜像把内存/磁盘打满"）
MAX_DOWNLOAD_BYTES = 200 * 1024 * 1024

_CHUNK__tools_web_download_file = 1 << 16


@tool
class DownloadTool(ToolPlugin):
    """从URL下载文件"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.web.download"

    @property
    def name(self) -> str:
        return "download_file"

    @property
    def description(self) -> str:
        return "从URL下载文件"

    @property
    def category(self) -> str:
        return ToolCategory.WEB

    @property
    def permission(self) -> str:
        return PermissionLevel.WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "下载URL"},
                "savePath": {"type": "string", "description": "保存路径"},
            },
            "required": ["url", "savePath"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            url = self.get_required_string_arg(args, "url")
            save_path = self.get_required_string_arg(args, "savePath")
        except ValueError as e:
            return self.error("下载失败: " + str(e))

        target = self.resolve_path(save_path)
        part = target.with_name(target.name + ".part")
        existed = target.is_file()
        resume_from = part.stat().st_size if part.is_file() else 0

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            headers = {"Accept-Encoding": "identity"}
            if resume_from > 0:
                headers["Range"] = f"bytes={resume_from}-"
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
                status = response.status
                appending = status == 206 and resume_from > 0
                if status == 206 and resume_from > 0 and not _range_matches(response, resume_from):
                    appending = False
                mode = "ab" if appending else "wb"
                written = 0
                with part.open(mode) as fh:
                    while True:
                        block = response.read(_CHUNK__tools_web_download_file)
                        if not block:
                            break
                        written += len(block)
                        if written > MAX_DOWNLOAD_BYTES:
                            fh.close()
                            return self.error(
                                f"下载失败: 文件超过 "
                                f"{MAX_DOWNLOAD_BYTES // (1024 * 1024)}MB 上限已中止"
                                f"（临时文件已保留：{part.name}）")
                        fh.write(block)
            os.replace(part, target)
            size = target.stat().st_size
        except urllib.error.HTTPError as e:
            return self.error("下载失败: HTTP " + str(e.code))
        except Exception as e:
            hint = f"\n（临时文件已保留：{part}，重试会从断点继续）" if part.is_file() else ""
            return self.error("下载失败: " + str(e) + hint)

        notes = ""
        if existed:
            notes += "\n（目标位置原来就有同名文件，已覆盖）"
        if resume_from > 0:
            notes += f"\n（断点续传：从 {resume_from} 字节处接着下载）"
        return self.success(f"文件已下载: {target} ({size}字节){notes}")


def _range_matches(response, resume_from: int) -> bool:
    """服务器回的 Content-Range 起点要和我们请求的一致，否则不能接着写。"""
    content_range = response.headers.get("Content-Range") or ""
    if "/" not in content_range:
        return True
    start = content_range.split(" ", 1)[-1].split("-", 1)[0].strip()
    try:
        return int(start) == resume_from
    except ValueError:
        return True


# ========================================================================
# 原模块 lionbox/tools/web/http_get.py
# ========================================================================
"""HTTP GET 工具（对应 Java `core/plugin/tool/web/HttpGetTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差 ——
注意 id 是 `tool.http.get`（**不是** tool.web.get，Java 就是这样）；
minimal_mode = False（Java 类别 WEB_SEARCH）。

【实测过的行为，照抄】
1. 必须带浏览器 UA：不少站点对没有 UA 的请求直接不响应（连接挂到超时）。
   Java 侧 OkHttp 还默认带 `Accept-Encoding: gzip` 并自动解压，这里也照做。
2. **非 2xx 不是异常**：OkHttp 不会为 4xx/5xx 抛异常，Java 侧就把状态码和响应体一起返回给模型。
   Python 的 urllib 会抛 HTTPError，所以要显式接住、把响应体读出来 ——
   否则模型只能看到"请求失败"，看不到站点到底说了什么。
3. 超时与大小上限：Java 是连接 15s / 读 30s；`timeout` 参数在 Java 里只声明没被用，
   这里让它真的生效（默认 30，与 schema 一致）。响应体读取设了上限，
   防止一个超大页面把内存打满（超了就截断并说明）。
"""


import urllib.error
import urllib.request
import zlib
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 带浏览器 UA：不少站点对无 UA 的请求直接不响应（连接挂到超时）
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

#: 响应体最多读多少字节（Java 侧 OkHttp 是无上限的；这里按移植要求加一道闸）
MAX_BODY_BYTES = 5 * 1024 * 1024

DEFAULT_TIMEOUT = 30


@tool
class HttpGetTool(ToolPlugin):
    """发送HTTP GET请求"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.http.get"

    @property
    def name(self) -> str:
        return "http_get"

    @property
    def description(self) -> str:
        return "发送HTTP GET请求"

    @property
    def category(self) -> str:
        return ToolCategory.WEB

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "请求URL"},
                "timeout": {"type": "integer", "description": "超时秒数", "default": 30},
            },
            "required": ["url"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            url = self.get_required_string_arg(args, "url")
            timeout = self.get_int_arg(args, "timeout", DEFAULT_TIMEOUT)
        except ValueError as e:
            return self.error("HTTP请求失败: " + str(e))
        request = urllib.request.Request(url, headers={
            "User-Agent": UA,
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate",
        })
        try:
            with urllib.request.urlopen(request, timeout=max(1, timeout)) as response:
                body = read_body(response)
                return self.success(f"HTTP {response.status}\n{body}")
        except urllib.error.HTTPError as e:
            # 非 2xx：状态码 + 响应体片段一起给模型（Java 侧就是这个行为）
            body = read_body(e)
            return self.success(f"HTTP {e.code}\n{body}")
        except Exception as e:
            return self.error("HTTP请求失败: " + str(e))


def _inflate_partial(raw: bytes, wbits: int) -> bytes:
    """把压缩流**分块**解出来；流被读取上限截断时，能解多少算多少。

    【为什么不能 `gzip.decompress` + `except: pass`】它遇到半截流直接抛，pass 之后
    压缩字节原样进解码器 → 返回一堆乱码还报成功。分块解压在截断时能保住已解出的前半段，
    真正的坏流返回空串，由调用方如实报"解压失败"。
    """
    dec = zlib.decompressobj(wbits)
    out = b""
    pos = 0
    try:
        while pos < len(raw):
            out += dec.decompress(raw[pos:pos + 65536])
            pos += 65536
        out += dec.flush()
    except (zlib.error, ValueError, EOFError):
        return out              # 流不完整/坏了：已解出的部分就是能给的全部
    return out


def read_body(response) -> str:
    """按 Content-Encoding 解压、按 Content-Type 的 charset 解码，并限制读取上限。

    【顺序不能反：先解压、后截断】压缩流必须完整才解得开，原来是"读 5MB → 截断 →
    再解压"，半截 gzip 必然解压失败并被 `except: pass` 吞掉，最后把 gzip 字节当 UTF-8
    解码返回乱码。读取上限记的是**原始字节**（防大响应打爆内存），解压结果再按同一上限
    截断（防压缩炸弹），解压失败则如实说明，不装作成功。
    """
    raw = response.read(MAX_BODY_BYTES + 1)
    read_overflow = len(raw) > MAX_BODY_BYTES
    encoding = (response.headers.get("Content-Encoding") or "").lower()
    note = ""
    if "gzip" in encoding:
        data = _inflate_partial(raw, zlib.MAX_WBITS | 16)
        if not data and raw:
            note = "\n（响应体解压失败：不是合法的 gzip，或超过了读取上限）"
    elif "deflate" in encoding:
        data = _inflate_partial(raw, zlib.MAX_WBITS)
        if not data and raw:
            data = _inflate_partial(raw, -zlib.MAX_WBITS)     # 少数站点发不带头的裸 deflate
        if not data and raw:
            note = "\n（响应体解压失败：不是合法的 deflate，或超过了读取上限）"
    else:
        data = raw
    truncated = read_overflow or len(data) > MAX_BODY_BYTES
    if truncated:
        data = data[:MAX_BODY_BYTES]
    text = decode_text__tools_web_http_get(data, response.headers.get("Content-Type"))
    if truncated:
        text += f"\n...(内容超过 {MAX_BODY_BYTES // (1024 * 1024)}MB 已截断)"
    if note:
        text += note
    return text


def decode_text__tools_web_http_get(raw: bytes, content_type: str | None) -> str:
    """Content-Type 里带 charset 就按它解，否则按 UTF-8（同 OkHttp 的 `body().string()`）。"""
    charset = "utf-8"
    if content_type and "charset=" in content_type.lower():
        charset = content_type.lower().split("charset=", 1)[1].split(";")[0].strip().strip('"')
    try:
        return raw.decode(charset, errors="replace")
    except LookupError:
        return raw.decode("utf-8", errors="replace")


# ========================================================================
# 原模块 lionbox/tools/web/fetch_url.py
# ========================================================================
"""URL 内容抓取工具（对应 Java `core/plugin/tool/web/UrlFetchTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 WEB_SEARCH）。

【实测过的坑，照抄修法】Java 侧原来 8s 连接 / 15s 读、而且**不带 User-Agent**：
不少站点对没有 UA 的请求直接不响应（连接挂着直到超时），用户那一跑就是
"http_get 能用、fetch_url 超时"。修法（这里全部照抄）：
  1. 带浏览器 UA + Accept + Accept-Language；
  2. 连接 15s / 读 30s；
  3. **失败重试一次**（网络抖动很常见），但非 2xx 不重试 —— 那是有确定答复的；
  4. 非 2xx 也把状态码和响应体给模型，并附一句"站点可能要求登录/被墙/需要换 UA"；
  5. maxLength 截断（默认 10000），截了要说 `...(截断)`；
  6. 两条路都失败时给出可执行的建议（改用 http_get 或 web_search）。
另外加了响应体读取上限，防止一个超大页面把内存打满。
"""


import urllib.error
import urllib.request
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 带浏览器 UA（同上：没有 UA 的请求很多站点直接不响应）
UA__tools_web_fetch_url = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

TIMEOUT__tools_web_fetch_url = 30
DEFAULT_MAX_LENGTH = 10000


@tool
class UrlFetchTool(ToolPlugin):
    """抓取URL内容"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.web.fetch"

    @property
    def name(self) -> str:
        return "fetch_url"

    @property
    def description(self) -> str:
        return "抓取URL内容"

    @property
    def category(self) -> str:
        return ToolCategory.WEB

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "URL"},
                "maxLength": {"type": "integer", "description": "最大内容长度",
                              "default": 10000},
            },
            "required": ["url"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            url = self.get_required_string_arg(args, "url")
            max_length = self.get_int_arg(args, "maxLength", DEFAULT_MAX_LENGTH)
        except ValueError as e:
            return self.error("抓取失败: " + str(e))
        if max_length < 0:
            max_length = 0

        request = urllib.request.Request(url, headers={
            "User-Agent": UA__tools_web_fetch_url,
            "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
        })

        last: Exception | None = None
        for attempt in (1, 2):        # 失败重试一次（网络抖动很常见）
            try:
                with urllib.request.urlopen(request, timeout=TIMEOUT__tools_web_fetch_url) as response:
                    body = _body(response)
                    head = f"HTTP {response.status}（第 {attempt} 次尝试）\n"
                    return self.success(head + _cut(body, max_length))
            except urllib.error.HTTPError as e:
                # 非 2xx：不重试，把状态码 + 响应体一起给模型（Java 侧就是这个行为）
                head = (f"HTTP {e.code}（第 {attempt} 次尝试）\n"
                        "（非 2xx：站点可能要求登录/被墙/需要换 UA）\n")
                return self.success(head + _cut(_body(e), max_length))
            except Exception as e:
                last = e
        return self.error("抓取失败（重试过 1 次）: "
                          + ("未知原因" if last is None else str(last))
                          + "\n可以改用 http_get（同样的 GET，超时设置不同）或 web_search "
                            "搜这个地址。")


def _body(response) -> str:
    # 统一走 read_body：原来这里是"先截 5MB 再解压"（半截 gzip 必失败 → 乱码），
    # 而且只认 gzip 不认 deflate（我们声明的是 "gzip, deflate"）。见 read_body 的注释。
    return read_body(response)


def _cut(body: str, max_length: int) -> str:
    if len(body) > max_length:
        return body[:max_length] + "\n...(截断)"
    return body


# ========================================================================
# 原模块 lionbox/tools/web/headless_browser.py
# ========================================================================
"""无头浏览器（对应 Java `core/plugin/tool/web/HeadlessBrowser.java`）。

【这不是一个工具】Java 里它是 `@Component` 的**辅助类**（没有 id/name/execute），
被 `WebSearchTool` 注入使用；所以这里也不加 `@tool`，类名保持 `HeadlessBrowser`。
（Java 包下 8 个 `.java` 文件里，只有 7 个是工具，这一个不是。）

【为什么走浏览器而不是搜索 API】用户明确要求"网络搜索改成用无头浏览器搜，不要 api" ——
不要密钥、不要注册、不要配额、不用管某家 API 哪天改条款。
实现走 Chrome/Edge 自带的 `--dump-dom`：一次调用一个进程，跑完自己退出，
比连 CDP/WebSocket 省事，也不会留下常驻进程。

【实测过的两个坑，照抄修法】
1. stdout 必须一边读一边等：`--dump-dom` 把整页 DOM 打到 stdout，写满了没人读浏览器就卡死；
   Java 用读线程，Python 用 `communicate()`（它内部就是并发排空两条管道）。
2. stderr 也得抽干：Edge 一启动就往 stderr 写一堆日志（实测 5KB+），管道写满它就永远不退出；
   这里同样交给 communicate。
找不到浏览器时 `available()` 为 False，调用方自己去退到"直接抓 HTML"那条路。
想指定浏览器：环境变量 `LIONBOX_BROWSER=<可执行文件路径>`。
"""


import os
import shutil
import subprocess
import sys
import tempfile

#: 页面里 JS 跑多久（毫秒）再 dump —— 给结果页留足渲染时间
VIRTUAL_BUDGET_MS = 6000


class HeadlessBrowser:
    """用系统里已经装好的 Edge / Chrome 打开页面，把「渲染后的 DOM」抓回来。"""

    def __init__(self) -> None:
        found = ""
        env = (os.environ.get("LIONBOX_BROWSER") or "").strip()
        if env and os.path.isfile(env):
            found = env
        if not found:
            for path in self._candidates():
                if os.path.isfile(path):
                    found = path
                    break
        if not found:
            for name in ("msedge", "chrome", "chromium"):
                path = shutil.which(name)
                if path:
                    found = path
                    break
        self._exe = found
        self._why = "" if found else "没找到 Edge/Chrome（设环境变量 LIONBOX_BROWSER=<路径> 可指定）"

    @staticmethod
    def _candidates() -> list[str]:
        home = os.path.expanduser("~")
        return [
            r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            os.path.join(home, r"AppData\Local\Google\Chrome\Application\chrome.exe"),
        ]

    def available(self) -> bool:
        return bool(self._exe)

    def exe_path(self) -> str:
        """浏览器可执行文件路径（没装就是空串），给工具结果里如实说明用。"""
        return self._exe

    def unavailable_reason(self) -> str:
        """没找到浏览器时的原因，写给用户看。"""
        return self._why

    def dump_dom(self, url: str, timeout_seconds: int) -> str | None:
        """打开 url 并返回**渲染后**的 DOM（含执行完的 JS）。

        返回 None 的情形：浏览器没装、超时、页面空白 —— 由调用方决定退路。
        """
        if not self._exe or not url or url.strip() == "":
            return None
        profile = None
        proc = None
        try:
            profile = tempfile.mkdtemp(prefix="lionbox-headless-")
            command = [
                self._exe,
                "--headless=new",
                "--disable-gpu",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                "--disable-sync",
                "--disable-background-networking",
                "--mute-audio",
                "--hide-scrollbars",
                "--user-data-dir=" + profile,
                "--virtual-time-budget=" + str(VIRTUAL_BUDGET_MS),
                "--dump-dom",
                url,
            ]
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.DEVNULL)
            try:
                out, _err = proc.communicate(timeout=max(5, int(timeout_seconds)))
            except subprocess.TimeoutExpired:
                self._kill_tree(proc)
                try:
                    out, _err = proc.communicate(timeout=5)
                except Exception:
                    out = b""
            html = self._decode(out)
            if html is None or html.strip() == "":
                return None
            return html
        except Exception:
            return None
        finally:
            if proc is not None and proc.poll() is None:
                self._kill_tree(proc)
            self._delete_quietly(profile)

    # ------------------------------------------------------------------

    @staticmethod
    def _kill_tree(proc: subprocess.Popen) -> None:
        """连子进程一起收掉（浏览器会 fork 一堆渲染进程，只 kill 父进程会留一堆僵尸）。"""
        try:
            if sys.platform == "win32":
                subprocess.run(["taskkill", "/F", "/T", "/PID", str(proc.pid)],
                               capture_output=True, timeout=10)
            else:
                proc.kill()
        except Exception:
            pass
        try:
            proc.kill()
        except Exception:
            pass

    @staticmethod
    def _decode(raw: bytes | None) -> str | None:
        """DOM 是 UTF-8；万一不是（老机器代码页），退到 GBK / Latin-1，绝不因为编码丢结果。"""
        if not raw:
            return None
        try:
            return raw.decode("utf-8")
        except Exception:
            pass
        try:
            return raw.decode("gbk", errors="replace")
        except Exception:
            return raw.decode("latin-1", errors="replace")

    @staticmethod
    def _delete_quietly(path: str | None) -> None:
        if not path:
            return
        shutil.rmtree(path, ignore_errors=True)


# ========================================================================
# 原模块 lionbox/tools/web/http_post.py
# ========================================================================
"""HTTP POST 工具（对应 Java `core/plugin/tool/web/HttpPostTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差
（id 是 `tool.http.post`）；minimal_mode = False（Java 类别 WEB_SEARCH）。

【行为对齐】
1. Java 没覆盖 getRequiredPermission → 用基类默认的 WORKSPACE_WRITE，
   Python 这边对应 `PermissionLevel.WRITE`。
2. OkHttp 对 4xx/5xx **不抛异常**，Java 侧照样把 "HTTP 500" + 响应体当成功返回；
   这里接住 urllib 的 HTTPError 做同样的事（否则非 2xx 就只剩一句报错）。
3. 内容类型默认 application/json，请求体按 UTF-8 发送（OkHttp 的 MediaType 默认也是 UTF-8）。
4. 同 http_get：连接 8s / 读 15s（Java 的 OkHttp 配置），并加了响应体大小上限。
"""


import urllib.error
import urllib.request
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: Java 侧是 OkHttp，它自己带这个 UA；这里对齐，避免两边站点行为不一致
UA__tools_web_http_post = "okhttp/4.12.0"

DEFAULT_TIMEOUT__tools_web_http_post = 15


@tool
class HttpPostTool(ToolPlugin):
    """发送HTTP POST请求"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.http.post"

    @property
    def name(self) -> str:
        return "http_post"

    @property
    def description(self) -> str:
        return "发送HTTP POST请求"

    @property
    def category(self) -> str:
        return ToolCategory.WEB

    @property
    def permission(self) -> str:
        return PermissionLevel.WRITE

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "url": {"type": "string", "description": "请求URL"},
                "body": {"type": "string", "description": "请求体"},
                "contentType": {"type": "string", "description": "内容类型",
                                "default": "application/json"},
            },
            "required": ["url", "body"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            url = self.get_required_string_arg(args, "url")
            body = self.get_required_string_arg(args, "body")
            content_type = self.get_string_arg(args, "contentType", "application/json")
        except ValueError as e:
            return self.error("HTTP请求失败: " + str(e))

        # OkHttp 的 RequestBody.create(String, MediaType) 在没有 charset 时会补一句
        # "; charset=utf-8"（正文按 UTF-8 编码）—— 实测 Java 发出的头就是
        # "application/json; charset=utf-8"，这里对齐，免得两边站点看到的请求不一样。
        if content_type and "charset=" not in content_type.lower():
            content_type = content_type + "; charset=utf-8"

        request = urllib.request.Request(
            url, data=body.encode("utf-8"), method="POST",
            headers={"Content-Type": content_type, "User-Agent": UA__tools_web_http_post,
                     "Accept-Encoding": "gzip, deflate"})
        try:
            with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT__tools_web_http_post) as response:
                return self.success(f"HTTP {response.status}\n{_body__tools_web_http_post(response)}")
        except urllib.error.HTTPError as e:
            return self.success(f"HTTP {e.code}\n{_body__tools_web_http_post(e)}")
        except Exception as e:
            return self.error("HTTP请求失败: " + str(e))


def _body__tools_web_http_post(response) -> str:
    # 【必须解压】请求头里主动声明了 `Accept-Encoding: gzip, deflate`，服务端照做返回
    # 压缩体，而 urllib **不会**自动解压 —— 原来这里直接把 gzip 字节当 UTF-8 解码，
    # 返回乱码还报成功。复用 http_get 的 read_body（解压 + charset + 上限一套全有）。
    return read_body(response)


# ========================================================================
# 原模块 lionbox/tools/web/translate.py
# ========================================================================
"""文本翻译工具（对应 Java `core/plugin/tool/web/TranslateTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False（Java 类别 WEB_SEARCH）。

【行为对齐】Java 侧以前是个占位实现（只会回"需要配置翻译API密钥"，等于不能用），
现在走 MyMemory 的公开接口：**不要密钥、不要注册**。修法与细节照抄：
  1. 单次约 500 字符上限，按 450 字符分段（CHUNK），尽量在换行/句号/！处切开，不切断句子；
  2. 源语言没给或给了 auto 时按文本猜（有中文 → zh-CN，否则 en）；
  3. 某一段翻不动时：如果前面已经翻好了就把已翻好的给出去并标注"只翻好了一部分"，
     一段都没翻好则**如实报错**（不假装成功）；
  4. 接口返回里取 responseData.translatedText，空/缺失都算这一段失败。
"""


import json as _json
import urllib.parse
import urllib.request
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

#: 免费接口单次大概 500 字符，留点余量分段
CHUNK = 450

TIMEOUT__tools_web_translate = 25
UA__tools_web_translate = "Lion Code/1.3 (translate tool)"


@tool
class TranslateTool(ToolPlugin):
    """文本翻译"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.web.translate"

    @property
    def name(self) -> str:
        return "translate"

    @property
    def description(self) -> str:
        return "文本翻译（免密钥，走公开接口；也可用它把中文译成英文再搜）"

    @property
    def category(self) -> str:
        return ToolCategory.WEB

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "text": {"type": "string", "description": "待翻译文本"},
                "from": {"type": "string", "description": "源语言，默认 auto",
                         "default": "auto"},
                "to": {"type": "string", "description": "目标语言，默认 zh", "default": "zh"},
            },
            "required": ["text"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            text = self.get_required_string_arg(args, "text")
        except ValueError as e:
            return self.error(str(e))

        to = self.get_string_arg(args, "to", "zh")
        source = self.get_string_arg(args, "from", "auto")
        if to is None or to.strip() == "":
            to = "zh"
        if source is None or source.strip() == "" or source.lower() == "auto":
            source = _guess_source(text, to)

        pieces: list[str] = []
        done = 0
        for chunk in _split(text, CHUNK):
            piece = _translate_chunk(chunk, source, to)
            if piece is None:
                if not pieces:
                    return self.error(
                        "翻译没成功（免费接口没响应或超时）。可以先试短一点的一段，"
                        f"或直接把原文交给模型自己翻。原文长度 {len(text)} 字符。")
                break        # 部分成功：把已经翻好的给出去，并标注
            pieces.append(piece)
            done += 1
        if not pieces:
            return self.error("翻译没成功（没拿到内容）。")
        tail = "\n（注：只翻好了前面一部分，原文较长）" if done * CHUNK < len(text) else ""
        return self.success(f"{source} → {to}：\n" + "".join(pieces) + tail)


def _translate_chunk(chunk: str, source: str, to: str) -> str | None:
    """交给免费接口翻一段；失败返回 None（调用方决定是报错还是部分成功）。"""
    try:
        url = ("https://api.mymemory.translated.net/get?q="
               + urllib.parse.quote_plus(chunk)
               + "&langpair=" + urllib.parse.quote_plus(source + "|" + to))
        request = urllib.request.Request(url, headers={"User-Agent": UA__tools_web_translate})
        with urllib.request.urlopen(request, timeout=TIMEOUT__tools_web_translate) as response:
            body = decode_text__tools_web_http_get(response.read(1 << 20), response.headers.get("Content-Type"))
        data = _json.loads(body).get("responseData") or {}
        translated = data.get("translatedText")
        if not isinstance(translated, str) or translated.strip() == "":
            return None
        return translated
    except Exception:
        return None


def _guess_source(text: str, to: str) -> str:
    """目标语言不是中文、原文里又有中文 → 当成 zh；否则原文按英文处理。

    【原来这里是个恒等三元】`return "en" if to.startswith("zh") else "en"` 两支一样，
    条件纯属死代码（docstring 承诺的"英中互相猜"根本没实现）。现在只留事实：
    没有中文字符的原文一律当英文原文 —— 目标是不是中文都不影响"原文是什么语言"。
    """
    if any(0x4E00 <= ord(ch) <= 0x9FFF or 0x3400 <= ord(ch) <= 0x4DBF for ch in text):
        return "zh-CN"
    return "en"


def _split(text: str, size: int) -> list[str]:
    """按段落/句子切块，尽量不把一句话切断（与 Java 的分段规则一致）。"""
    if len(text) <= size:
        return [text]
    parts: list[str] = []
    start = 0
    while start < len(text):
        end = min(len(text), start + size)
        if end < len(text):
            cut = max(text.rfind("\n", start, end + 1),
                      text.rfind("\u3002", start, end + 1),
                      text.rfind(".", start, end + 1),
                      text.rfind("\uff01", start, end + 1))
            if cut > start + size // 2:
                end = cut + 1
        parts.append(text[start:end])
        start = end
    return parts


# ========================================================================
# 原模块 lionbox/tools/web/web_search.py
# ========================================================================
"""网络搜索工具（对应 Java `core/plugin/tool/web/WebSearchTool.java`）。

【逐字一致的契约】id/name/description/parameters_schema 与 Java 一字不差；
minimal_mode = False —— Java 侧**特意删掉了**"搜索工具永远可用"的老特例
（原来极简模式里还能调 web_search，用户一眼就看出模式没生效），现在交给基类按
"模式 + 类别"统一判断：极简模式下它根本不在工具清单里。

【两条腿走路】
  1. 首选无头浏览器（HeadlessBrowser，用 `--dump-dom` 拿渲染后的 DOM）；
  2. 浏览器没装/打不开时，退到直接用 HTTP 抓同一个结果页（Bing 的结果页是服务端渲染的，
     直接抓也拿得到），并在结果里**如实说明**走的哪条路。
默认引擎 cn.bing.com（国内能直连）；也可指定 duckduckgo / google / baidu。

【实测过的坑，照抄修法】
1. fetch/parse/format 整段用 try 包住：结果页里一个 `&#99999999999;`（整数溢出）
   或半个 `%`（URL 解码）就能让模型看到"工具执行异常"，看起来像工具坏了 ——
   现在这一个引擎失败就记一笔、换下一个，两个都不行再回一条正常的搜索失败提示。
2. 链接是跳转包装：Bing 的 `ck/a?...&u=a1<base64url>`、DDG 的 `uddg=`、Google 的 `/url?q=`
   都要解回真地址，解不开就原样返回（一条脏链接不该毁掉整次搜索）。
"""


import base64 as _base64
import re
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

from lionbox.plugins.base import PermissionLevel, ToolCategory, ToolPlugin, ToolResult, tool

UA__tools_web_web_search = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/124.0 Safari/537.36")

TIMEOUT__tools_web_web_search = 25
DEFAULT_MAX_RESULTS = 5
MAX_RESULTS_LIMIT = 20

#: 浏览器要建 profile，冷启动慢，超时给宽一点
BROWSER_TIMEOUT = 45

_browser: HeadlessBrowser | None = None


def browser() -> HeadlessBrowser:
    """进程内单例：构造会去探几个固定路径，不该在每个工具实例里重复做。"""
    global _browser
    if _browser is None:
        _browser = HeadlessBrowser()
    return _browser


@tool
class WebSearchTool(ToolPlugin):
    """用无头浏览器在互联网上搜索"""

    minimal_mode = False

    @property
    def id(self) -> str:  # noqa: A003
        return "tool.web.search"

    @property
    def name(self) -> str:
        return "web_search"

    @property
    def description(self) -> str:
        return "用无头浏览器（Edge/Chrome）在互联网上搜索，返回标题/链接/摘要；不需要任何 API 密钥"

    @property
    def category(self) -> str:
        return ToolCategory.WEB

    @property
    def permission(self) -> str:
        return PermissionLevel.READ_ONLY

    def parameters_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "搜索关键词"},
                "maxResults": {"type": "integer", "description": "最多返回几条",
                               "default": 5},
                "engine": {"type": "string", "description":
                           "搜索引擎：bing（默认，国内可直连）/ duckduckgo / google / baidu"},
            },
            "required": ["query"],
        }

    def execute(self, args: dict[str, Any]) -> ToolResult:
        try:
            query = self.get_required_string_arg(args, "query")
        except ValueError as e:
            return self.error(str(e))

        max_results = _max_results(args.get("maxResults"))
        engine = self.get_string_arg(args, "engine", "bing")
        if engine is None or engine.strip() == "":
            engine = "bing"
        engine = engine.strip().lower()

        tried: list[str] = []
        order = (["bing", "duckduckgo"] if engine.startswith("bing")
                 else [engine, "bing"])
        for candidate in order:
            try:
                page = _fetch(_search_url(candidate, query))
                hits = _parse__tools_web_web_search(candidate, page.html, max_results)
                tried.append(f"{candidate}：{page.how}（解析到 {len(hits)} 条）")
                if hits:
                    return self.success(_format__tools_web_web_search(query, candidate, page.how, hits))
            except Exception as e:
                tried.append(f"{candidate}：结果页解析失败（{e}）")
        return self.error(f"没搜到结果（{query}）。尝试过 → " + "；".join(tried)
                          + "\n建议：换个更短的关键词；或用 fetch_url 直接打开某个具体网址。")


# ==========================================================================
# 抓页面
# ==========================================================================


class _Page:
    __slots__ = ("html", "how")

    def __init__(self, html: str | None, how: str) -> None:
        self.html = html
        self.how = how


def _fetch(url: str) -> _Page:
    """抓页面：优先无头浏览器，失败退到 HTTP 直取。"""
    dom = browser().dump_dom(url, BROWSER_TIMEOUT)
    if dom is not None and len(dom) > 400:
        return _Page(dom, "无头浏览器 " + _short_name(browser().exe_path()))
    why = "浏览器没拿到内容" if browser().available() else browser().unavailable_reason()
    via_http = _http_get(url)
    if via_http is not None and len(via_http) > 400:
        return _Page(via_http, f"HTTP 直取（{why}）")
    return _Page(None, f"两条路都没成功（{why}）")


def _http_get(url: str) -> str | None:
    request = urllib.request.Request(url, headers={
        "User-Agent": UA__tools_web_web_search,
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
    })
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT__tools_web_web_search) as response:
            # 结果页常常是 gzip/deflate 压缩的（实测 cn.bing.com 就是），
            # 直接按文本解会得到一堆乱码、解析必然 0 条 —— 统一走 http_get 里的解压+解码。
            return read_body(response)
    except urllib.error.HTTPError as e:
        try:
            return read_body(e)
        except Exception:
            return None
    except Exception:
        return None


def _search_url(engine: str, query: str) -> str:
    encoded = urllib.parse.quote_plus(query)
    if engine in ("duckduckgo", "ddg"):
        return "https://html.duckduckgo.com/html/?q=" + encoded
    if engine == "google":
        return "https://www.google.com/search?num=20&q=" + encoded
    if engine == "baidu":
        return "https://www.baidu.com/s?wd=" + encoded
    return "https://cn.bing.com/search?q=" + encoded


def _short_name(path: str) -> str:
    if not path or path.strip() == "":
        return "未找到"
    return re.split(r"[\\/]", path)[-1]


# ==========================================================================
# 解析
# ==========================================================================


class _Hit:
    __slots__ = ("title", "url", "snippet")

    def __init__(self, title: str, url: str, snippet: str) -> None:
        self.title = title
        self.url = url
        self.snippet = snippet


def _parse__tools_web_web_search(engine: str, html: str | None, max_results: int) -> list[_Hit]:
    if not html or html.strip() == "":
        return []
    if engine in ("duckduckgo", "ddg"):
        return _parse_duckduckgo(html, max_results)
    if engine == "google":
        return _parse_google(html, max_results)
    if engine == "baidu":
        return _parse_baidu(html, max_results)
    return _parse_bing(html, max_results)


def _parse_bing(html: str, max_results: int) -> list[_Hit]:
    out: list[_Hit] = []
    blocks = re.findall(r'(?s)<li[^>]*class="[^"]*\bb_algo\b[^"]*"[^>]*>(.*?)</li>', html)
    for block in blocks:
        if len(out) >= max_results:
            break
        link = re.search(r'(?s)<h2[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', block)
        if not link:
            continue
        url = _clean_bing_url(link.group(1))
        title = _text(link.group(2))
        snippet = ""
        para = re.search(r"(?s)<p[^>]*>(.*?)</p>", block)
        if para:
            snippet = _text(para.group(1))
        if title.strip() != "" and url.startswith("http"):
            out.append(_Hit(title, url, snippet))
    return out


def _parse_duckduckgo(html: str, max_results: int) -> list[_Hit]:
    out: list[_Hit] = []
    snippets = [_text(m) for m in re.findall(
        r'(?s)<a[^>]*class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</a>', html)]
    links = re.findall(
        r'(?s)<a[^>]*class="[^"]*result__a[^"]*"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html)
    # 【摘要按下标配对，不按"已接受的结果数"】snippets 与 links 是按页面顺序各自抓的
    # 两份列表；用 len(out) 当下标，一旦某条链接被下面的条件跳过，后面每条结果都会
    # 配上**前一条**的摘要（张冠李戴）。按链接在页面里的位置 i 取才对得上。
    for i, (href, inner) in enumerate(links):
        if len(out) >= max_results:
            break
        url = _decode_ddg_url(href)
        title = _text(inner)
        if title.strip() != "" and url.startswith("http"):
            out.append(_Hit(title, url, snippets[i] if i < len(snippets) else ""))
    return out


def _parse_baidu(html: str, max_results: int) -> list[_Hit]:
    out: list[_Hit] = []
    for href, inner in re.findall(
            r'(?s)<h3[^>]*>\s*<a[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html):
        if len(out) >= max_results:
            break
        title = _text(inner)
        if title.strip() != "":
            out.append(_Hit(title, href, ""))
    return out


def _parse_google(html: str, max_results: int) -> list[_Hit]:
    out: list[_Hit] = []
    for href, inner in re.findall(
            r'(?s)<a[^>]*href="(/url\?q=[^"]+|https?://[^"]+)"[^>]*>\s*<h3[^>]*>(.*?)</h3>',
            html):
        if len(out) >= max_results:
            break
        url = _decode_google_url(href)
        title = _text(inner)
        if title.strip() != "" and url.startswith("http"):
            out.append(_Hit(title, url, ""))
    return out


# ---- 链接还原 ----

def _clean_bing_url(href: str | None) -> str:
    """Bing 的链接常常是 ck/a?...&u=a1<base64url>，要解回真地址。"""
    if href is None:
        return ""
    text = href.replace("&amp;", "&")
    at = text.find("&u=a1")
    if "bing.com/ck/a" in text and at >= 0:
        payload = text[at + 5:]
        amp = payload.find("&")
        if amp > 0:
            payload = payload[:amp]
        try:
            padded = payload + "=" * (-len(payload) % 4)
            return _base64.urlsafe_b64decode(padded).decode("utf-8", errors="replace")
        except Exception:
            return text
    return text


def _decode_ddg_url(href: str | None) -> str:
    """DuckDuckGo 的链接是 //duckduckgo.com/l/?uddg=<urlencoded>。"""
    if href is None:
        return ""
    text = href.replace("&amp;", "&")
    at = text.find("uddg=")
    if at >= 0:
        encoded = text[at + 5:]
        amp = encoded.find("&")
        if amp > 0:
            encoded = encoded[:amp]
        return _url_decode(encoded)
    return "https:" + text if text.startswith("//") else text


def _decode_google_url(href: str | None) -> str:
    text = "" if href is None else href.replace("&amp;", "&")
    if text.startswith("/url?q="):
        query = text[7:]
        amp = query.find("&")
        if amp > 0:
            query = query[:amp]
        return _url_decode(query)
    return text


def _url_decode(encoded: str) -> str:
    """解不开就原样返回：一条链接脏了不该毁掉整次搜索（Java 侧实测踩过）。"""
    for match in re.finditer("%", encoded):
        pair = encoded[match.start() + 1:match.start() + 3]
        if len(pair) < 2 or not all(ch in "0123456789abcdefABCDEF" for ch in pair):
            return encoded
    return urllib.parse.unquote_plus(encoded)


def _text(fragment: str | None) -> str:
    """去标签 + 还原常见实体。"""
    if fragment is None:
        return ""
    text = re.sub(r"(?s)<script.*?</script>", " ", fragment)
    text = re.sub(r"(?s)<style.*?</style>", " ", text)
    text = re.sub(r"<[^>]+>", " ", text)
    for entity, value in (("&nbsp;", " "), ("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                          ("&quot;", "\""), ("&#39;", "'"), ("&apos;", "'"),
                          ("&hellip;", "\u2026"), ("&mdash;", "\u2014")):
        text = text.replace(entity, value)

    def replace_numeric(match: re.Match[str]) -> str:
        # 结果页里出现过 &#99999999999;（10 位数字）：Java 侧 parseInt 直接溢出，
        # 异常一路冒出 execute。认不出的实体原样留着就行，不能让一个字符毁掉整次搜索。
        try:
            code = int(match.group(1))
        except ValueError:
            return match.group(0)
        if 0 < code <= 0x10FFFF and not 0xD800 <= code <= 0xDFFF:
            return chr(code)
        return match.group(0)

    text = re.sub(r"&#(\d+);", replace_numeric, text)
    return re.sub(r"\s+", " ", text).strip()


# ==========================================================================
# 组装结果
# ==========================================================================


def _max_results(raw: Any) -> int:
    """与 Java 一致：数字或数字字符串都认，范围夹到 1-20，认不出用默认 5。"""
    try:
        if isinstance(raw, bool):
            return DEFAULT_MAX_RESULTS
        if isinstance(raw, (int, float)):
            return max(1, min(MAX_RESULTS_LIMIT, int(raw)))
        if isinstance(raw, str) and raw.strip() != "":
            return max(1, min(MAX_RESULTS_LIMIT, int(raw.strip())))
    except Exception:
        return DEFAULT_MAX_RESULTS
    return DEFAULT_MAX_RESULTS


def _format__tools_web_web_search(query: str, engine: str, how: str, hits: list[_Hit]) -> str:
    lines = [f"搜索「{query}」—— 引擎 {engine}，方式：{how}",
             f"共 {len(hits)} 条结果："]
    for index, hit in enumerate(hits, start=1):
        lines.append("")
        lines.append(f"{index}. {hit.title}")
        lines.append("   " + hit.url)
        if hit.snippet.strip() != "":
            snippet = hit.snippet if len(hit.snippet) <= 300 else hit.snippet[:300] + "\u2026"
            lines.append("   " + snippet)
    return "\n".join(lines) + "\n"


# ========================================================================
# 原模块 lionbox/tools/web.py
# ========================================================================
"""网络类工具（对应 Java 包 `core/plugin/tool/web`）。

【显式登记，不做目录扫描】导入本包即把 7 个工具类通过 `@tool` 登记进
`lionbox.plugins.base.TOOL_CLASSES`。

注意 Java 包下 8 个 `.java` 文件里只有 **7 个是工具**：
`HeadlessBrowser` 是 `@Component` 的辅助类（没有 id/name/execute，被 web_search 注入使用），
所以本包也把它按辅助类移植（`headless_browser.py`，类名保持 `HeadlessBrowser`，不加 `@tool`）。

id / name / description / parameters_schema 与 Java 版逐字一致（注意 http 两个工具的 id 前缀是
`tool.http.*`，不是 `tool.web.*` —— Java 就是如此）；
minimal_mode 对齐 `isAvailableInMode(MINIMAL)`：这一批在 Java 里类别都是 WEB_SEARCH，
不属于"文件类 + shell 类"，所以极简模式一律不开放。
"""



__all__ = [
    "DnsLookupTool",
    "DownloadTool",
    "HeadlessBrowser",
    "HttpGetTool",
    "HttpPostTool",
    "TranslateTool",
    "UrlFetchTool",
    "WebSearchTool",
]


# ============================================================================
# 【第二批工具：原 工具集.py —— 第一批补全的 18 个真实现】
#
# 原来放在独立模块里（只改 build_registry 两行来注册，风险最小 ✓），
# 现按用户要求合并进本文件（一个文件）。
#
# 合并时改过的名字（都因为与其它批/本文件原有符号同名 ✗）：
#   · DEFAULT_TIMEOUT      → DEFAULT_EXEC_TIMEOUT
#       本文件 L9416 附近已有 DEFAULT_TIMEOUT ✗ 直接搬会**静默改掉原有行为** ✓
#   · build_tools(NS)      → _build_batch1(NS)
#       本文件末尾的 build_tools(NS) 统一调三批 ✓
#
# 其余内容**原样搬运**（注释与"为什么这么写"的记录一并保留 ✓）
# ============================================================================


# -*- coding: utf-8 -*-
r"""工具补全：把提示词里**广告出去但没有实现**的工具做成真实现。

【为什么单独一个文件】main.py 是 1.1 MB 的内联引擎。新增工具写在独立模块里、
只改 build_registry 两行来注册，风险最小，也方便逐批测。

【盘点结论（实测）】
  A 广告出去 57 个（TOOL_PROMPT_HINTS 57 + 别名表正名 55）
  B 实际注册 8 个
  C 其中仍是桩：execute_command（只回显 "$ "）、move_file（只查参数）、
              context_window（"窗口 = None"）、web_search（"搜索结果"）
  A − B = **49 个广告了但没注册** —— 模型喊了只会得到"未找到工具"

【本模块补齐（第一批：编码 Agent 最常用的 18 个）】
  execute_command / search_in_files / glob_files / line_count / word_count /
  file_info / directory_tree / modify_file / create_file / append_file /
  delete_file / copy_file / move_file / create_directory / system_info /
  timestamp / working_directory / fetch_url

【约定】
  · 路径一律走 `self.resolve_path()`（沙箱的工作区约束，别绕过去）
  · 权限照 `PermissionLevel` 声明，要不要确认交给权限层
  · 危险命令在权限层之外**再挡一道**（灾难性命令没有"确认一下"的余地）
  · 失败要**说清为什么**，别返回空字符串（模型会以为成功继续瞎调）
"""

import datetime
import hashlib
import os
import platform
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

MAX_OUTPUT = 60_000
MAX_HITS = 200
MAX_ENTRIES = 500
DEFAULT_EXEC_TIMEOUT = 60

#: 灾难性命令：直接拒绝（这类没有"确认一下"的余地）
_FORBIDDEN = (
    r"\bformat\s+[a-z]:",
    r"rm\s+-rf?\s+[/\\](\s|$)",
    r"Remove-Item\s+[^|]*-Recurse[^|]*\b[a-z]:\\?\s*$",
    r"\bmkfs(\.\w+)?\b",
    r"\bdiskpart\b",
    r"\bshutdown\b",
    r"\breboot\b",
    r"cipher\s+/w",
)


def _truncate(text: str, limit: int = MAX_OUTPUT) -> str:
    if len(text) <= limit:
        return text
    return (text[:limit] + "\n…（输出共 " + format(len(text), ",")
            + " 字符，已截断到前 " + format(limit, ",") + "）")


def _fmt_bytes(n: int) -> str:
    v = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if v < 1024 or unit == "GB":
            return (f"{int(v)}{unit}" if unit == "B" else f"{v:.1f}{unit}")
        v /= 1024.0
    return f"{int(v)}B"


def _is_forbidden(cmd: str) -> str:
    low = cmd.lower()
    for pat in _FORBIDDEN:
        if re.search(pat, low, re.IGNORECASE):
            return pat
    return ""


def _kill_tree_and_reap(p) -> tuple[bytes, bytes]:
    """超时后**连子孙进程一起杀**并收掉管道，返回已经收到的那部分输出。

    【两件事缺一不可】
    1. `taskkill /F /T /PID`：kill/terminate 只作用于直接子进程，Windows 上
       powershell 拉起来的 node/npm/服务器都是孙进程，不 /T 全部存活 —— 报"已终止"
       却还在占端口/占 CPU；
    2. 杀完必须**再收一次管道**（communicate）：攥着 stdout 句柄的漏网进程会让管道
       永远等不到 EOF，表现是"超时之后这条命令还是卡着不返回"，工作线程一直泄漏。
    类 Unix 这里只杀直接子进程（没有预先建进程组，杀不了整棵树），能收多少收多少。
    """
    if os.name == "nt":
        try:
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(p.pid)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=15, creationflags=NO_WINDOW)
        except Exception:                              # noqa: BLE001 —— taskkill 失败就退回普通 kill
            try:
                p.kill()
            except Exception:                          # noqa: BLE001 —— 已经死了
                pass
    else:
        try:
            p.kill()
        except Exception:                              # noqa: BLE001 —— 已经死了
            pass
    try:
        return p.communicate(timeout=10)
    except Exception:                                  # noqa: BLE001 —— 漏网进程还攥着管道，别无限等
        try:
            p.kill()
        except Exception:                              # noqa: BLE001
            pass
        return b"", b""


def _build_batch1(NS: dict) -> list:
    """用调用方传进来的基类造出工具类清单（避免与 main.py 循环导入）。

    :param NS: 需含 ToolPlugin / ToolResult / PermissionLevel / ToolCategory
    """
    ToolPlugin = NS["ToolPlugin"]
    ToolResult = NS["ToolResult"]
    PermissionLevel = NS["PermissionLevel"]
    ToolCategory = NS["ToolCategory"]
    out: list = []

    def tool(cls):
        out.append(cls)
        return cls

    # ────────────────────────────── 执行命令 ⭐ ──────────────────────────────
    @tool
    class ExecuteCommandTool(ToolPlugin):
        """执行 shell 命令（本机是 Windows，走 PowerShell）。"""
        minimal_mode = True

        @property
        def id(self): return "tool.shell.execute"

        @property
        def name(self): return "execute_command"

        @property
        def description(self):
            return (
                "执行命令并拿到输出（装了什么、跑测试、用 git 等都用它）。\n"
                "用法：\n"
                "- 本机是 **Windows + PowerShell**：没有 `which`（用 **`where.exe 名字`** —— 裸 `where` 是 PowerShell 的 Where-Object 别名，什么都不输出）、"
                "没有 `python3`（用 `python`）、**不要用 `&&` / `||`**"
                "（PS 5.1 不认，用 `A; if ($?) { B }`）。\n"
                "- 一条 command 只做一件相关的事；互不相关的拆成多个调用，一轮里一起发。\n"
                "- 命令输出会被收走并截断，**不要用 `2>&1` / `2>/dev/null`**。\n"
                "- 非零退出码会如实报给你（不是失败就别假装成功）。\n"
                "- 危险命令（格式化、递归删根目录等）会被直接拒绝。\n"
                "- 长驻进程（服务器、watch）用 run_background，别在这里等它。\n"
                "- 可选 timeout（秒，默认 60）；超时会杀掉进程并如实报告。"
            )

        @property
        def category(self): return ToolCategory.SHELL

        @property
        def permission(self): return PermissionLevel.EXECUTE

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"command": {"type": "string"},
                                   "timeout": {"type": "number"}},
                    "required": ["command"]}

        def execute(self, args):
            cmd = str(args.get("command") or "").strip()
            if not cmd:
                return ToolResult.fail("缺少 command 参数")
            bad = _is_forbidden(cmd)
            if bad:
                return ToolResult.fail(
                    "拒绝执行：这条命令属于灾难性操作（匹配 " + bad + "）。"
                    "如果确实需要，请人工在终端里执行。")
            try:
                timeout = float(args.get("timeout") or DEFAULT_EXEC_TIMEOUT)
            except (TypeError, ValueError):
                timeout = DEFAULT_EXEC_TIMEOUT
            timeout = max(1.0, min(timeout, 600.0))

            if os.name == "nt":
                argv = ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd]
            else:
                argv = ["/bin/sh", "-c", cmd]
            cwd = None
            try:
                cwd = str(self.resolve_path("."))
            except Exception:                              # noqa: BLE001
                cwd = None
            t0 = __import__("time").time()

            def dec(b):
                for enc in ("utf-8", "gbk", "mbcs" if os.name == "nt" else "utf-8"):
                    try:
                        return b.decode(enc)
                    except (UnicodeDecodeError, LookupError):
                        continue
                return b.decode("utf-8", "replace")

            try:
                # 【用 Popen 而不是 subprocess.run】超时后要拿自己的 pid 去连**进程树**
                # 一起杀：subprocess.run 只 kill 直接子进程 powershell，它拉起来的
                # node/npm/服务器在 Windows 上全部存活，返回的"已被终止"是假话
                # （对照本文件 HeadlessBrowser._kill_tree 的 taskkill /F /T）。
                p = subprocess.Popen(argv, cwd=cwd, shell=False,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except FileNotFoundError as e:
                return ToolResult.fail("找不到解释器: " + str(e))
            except OSError as e:
                return ToolResult.fail("启动失败: " + type(e).__name__ + ": " + str(e))
            try:
                out_bytes, err_bytes = p.communicate(timeout=timeout)
            except subprocess.TimeoutExpired:
                out_bytes, err_bytes = _kill_tree_and_reap(p)
                dt = __import__("time").time() - t0
                partial = []
                if (out_bytes or b"").strip():
                    partial.append("已收到的输出:\n" + dec(out_bytes).rstrip())
                if (err_bytes or b"").strip():
                    partial.append("已收到的 stderr:\n" + dec(err_bytes).rstrip())
                return ToolResult.fail(
                    f"命令超时（{timeout:.0f}s）已被终止（含它拉起的子进程）：{cmd}\n"
                    + ("".join(seg + "\n" for seg in partial))
                    + f"（耗时 {dt:.1f}s；要跑长时间任务请用 run_background）")
            dt = __import__("time").time() - t0

            stdout = dec(out_bytes or b"")
            stderr = dec(err_bytes or b"")
            parts = []
            if p.returncode != 0:
                parts.append(f"[退出码 {p.returncode}] 命令没有成功（耗时 {dt:.1f}s）")
            else:
                parts.append(f"[退出码 0] 成功（耗时 {dt:.1f}s）")
            if stdout.strip():
                parts.append("stdout:\n" + stdout.rstrip())
            if stderr.strip():
                parts.append("stderr:\n" + stderr.rstrip())
            if not stdout.strip() and not stderr.strip():
                parts.append("（命令没有任何输出）")
            body = _truncate("\n".join(parts))
            return ToolResult.ok(body) if p.returncode == 0 else ToolResult.fail(body)

    # ────────────────────────────── 搜索 / 遍历 ──────────────────────────────
    @tool
    class SearchInFilesTool(ToolPlugin):
        """按内容搜索文件。"""
        minimal_mode = True

        @property
        def id(self): return "tool.file.search"

        @property
        def name(self): return "search_in_files"

        @property
        def description(self):
            return (
                "在文件内容里搜字符串/正则（不知道在哪个文件里时用它）。\n"
                "用法：\n"
                "- `pattern` 必填；`path` 默认当前目录；`glob` 限定文件名（如 `*.py`）。\n"
                "- `regex: true` 时按正则解释 pattern。\n"
                "- 返回 `文件:行号: 内容`，最多 200 条；要读上下文再用 read_file / head_tail_file。\n"
                "- **不要**用它列目录（用 list_directory / directory_tree）。"
            )

        @property
        def category(self): return ToolCategory.FILE_SEARCH

        @property
        def permission(self): return PermissionLevel.READ_ONLY

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"pattern": {"type": "string"},
                                   "path": {"type": "string"},
                                   "glob": {"type": "string"},
                                   "regex": {"type": "boolean"}},
                    "required": ["pattern"]}

        def execute(self, args):
            pat = str(args.get("pattern") or "")
            if not pat:
                return ToolResult.fail("缺少 pattern 参数")
            rx = None
            if args.get("regex"):
                try:
                    rx = re.compile(pat)
                except re.error as e:
                    return ToolResult.fail("正则不合法: " + str(e))
            try:
                root = self.resolve_path(str(args.get("path") or "."))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            if not root.exists():
                return ToolResult.fail("路径不存在: " + str(root))
            g = str(args.get("glob") or "").strip()
            files = [root] if root.is_file() else [p for p in root.rglob("*") if p.is_file()]
            hits, scanned = [], 0
            for f in files:
                if g and not (f.match(g) or fnmatch.fnmatch(f.name, g)):
                    continue
                try:
                    if f.stat().st_size > 4_000_000:
                        continue
                    text = f.read_bytes().decode("utf-8", "replace")
                except OSError:
                    continue
                scanned += 1
                for i, line in enumerate(text.splitlines(), 1):
                    if (rx.search(line) if rx else (pat in line)):
                        hits.append(f"{f}:{i}: {line.strip()[:200]}")
                        if len(hits) >= MAX_HITS:
                            break
                if len(hits) >= MAX_HITS:
                    break
            if not hits:
                return ToolResult.ok(f"没找到匹配（扫了 {scanned} 个文件）。"
                                     "换个关键词，或确认 path/glob 是否正确。")
            head = f"找到 {len(hits)} 条" + ("（已达上限，可能还有）" if len(hits) >= MAX_HITS else "")
            return ToolResult.ok(_truncate(head + ":\n" + "\n".join(hits)))

    @tool
    class GlobFilesTool(ToolPlugin):
        """按文件名/路径匹配找文件。"""
        minimal_mode = True

        @property
        def id(self): return "tool.file.glob"

        @property
        def name(self): return "glob_files"

        @property
        def description(self):
            return (
                "按名字找文件（只知道文件名或后缀时用它）。\n"
                "用法：\n"
                "- `pattern` 支持 `**`（如 `**/*.py`、`src/**/*.ts`）。\n"
                "- 按内容找用 search_in_files；看目录结构用 directory_tree。\n"
                "- 返回相对路径，最多 500 条。"
            )

        @property
        def category(self): return ToolCategory.FILE_SEARCH

        @property
        def permission(self): return PermissionLevel.READ_ONLY

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"pattern": {"type": "string"},
                                   "path": {"type": "string"}},
                    "required": ["pattern"]}

        def execute(self, args):
            pat = str(args.get("pattern") or "").strip()
            if not pat:
                return ToolResult.fail("缺少 pattern 参数")
            try:
                root = self.resolve_path(str(args.get("path") or "."))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            if not root.exists():
                return ToolResult.fail("路径不存在: " + str(root))
            try:
                found = [p for p in root.glob(pat)][:MAX_ENTRIES]
            except (ValueError, OSError) as e:
                return ToolResult.fail("匹配失败: " + type(e).__name__ + ": " + str(e))
            if not found:
                return ToolResult.ok("没有匹配的文件（pattern=" + pat + "）。")
            rels = sorted({str(p.relative_to(root)) if p.is_relative_to(root) else str(p)
                           for p in found})
            return ToolResult.ok(f"匹配 {len(rels)} 个:\n" + "\n".join(rels))

    @tool
    class DirectoryTreeTool(ToolPlugin):
        """按树形列出目录结构。"""

        @property
        def id(self): return "tool.file.tree"

        @property
        def name(self): return "directory_tree"

        @property
        def description(self):
            return (
                "树形展示目录结构（了解项目布局时用它）。\n"
                "用法：\n"
                "- `maxDepth` 默认 2；**别一下开到很深**（大仓库会吃掉上下文）。\n"
                "- 只看一层用 list_directory；找特定文件用 glob_files。\n"
                "- 默认跳过 .git / node_modules / __pycache__ 等噪音目录。"
            )

        @property
        def category(self): return ToolCategory.FILE_OPERATION

        @property
        def permission(self): return PermissionLevel.READ_ONLY

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"path": {"type": "string"},
                                   "maxDepth": {"type": "number"}},
                    "required": []}

        SKIP = {".git", "node_modules", "__pycache__", ".venv", ".pytest_cache",
                "dist", "build", ".idea", ".mypy_cache"}

        def execute(self, args):
            try:
                root = self.resolve_path(str(args.get("path") or "."))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            if not root.is_dir():
                return ToolResult.fail("不是目录: " + str(root))
            try:
                depth = int(args.get("maxDepth") or 2)
            except (TypeError, ValueError):
                depth = 2
            depth = max(1, min(depth, 6))
            lines, count = [str(root)], 0

            def walk(d: Path, level: int, prefix: str):
                nonlocal count
                if level > depth or count >= MAX_ENTRIES:
                    return
                try:
                    kids = sorted(d.iterdir(), key=lambda p: (p.is_file(), p.name.lower()))
                except OSError:
                    return
                for p in kids:
                    if p.name in self.SKIP or count >= MAX_ENTRIES:
                        continue
                    count += 1
                    lines.append(prefix + ("[目录] " if p.is_dir() else "") + p.name)
                    if p.is_dir():
                        walk(p, level + 1, prefix + "    ")
            walk(root, 1, "  ")
            tail = "" if count < MAX_ENTRIES else f"\n…（已达 {MAX_ENTRIES} 条上限）"
            return ToolResult.ok(_truncate("\n".join(lines) + tail))

    # ────────────────────────────── 统计 / 元信息 ──────────────────────────────
    def _stat_tool(name, id_, desc, fn, is_read=True):
        @tool
        class _T(ToolPlugin):
            @property
            def id(self): return id_
            @property
            def name(self): return name
            @property
            def description(self): return desc
            @property
            def category(self): return ToolCategory.FILE_OPERATION
            @property
            def permission(self):
                return PermissionLevel.READ_ONLY if is_read else PermissionLevel.WRITE
            def parameters_schema(self):
                return {"type": "object", "properties": {"path": {"type": "string"}},
                        "required": ["path"]}
            def execute(self, args):
                if not args.get("path"):
                    return ToolResult.fail("缺少 path 参数")
                try:
                    p = self.resolve_path(str(args["path"]))
                except Exception as e:                     # noqa: BLE001
                    return ToolResult.fail("路径无法解析: " + str(e))
                return fn(self, p)
        _T.__name__ = name + "Tool"
        return _T

    def _do_line_count(self, p):
        if not p.is_file():
            return ToolResult.fail("不是文件: " + str(p))
        try:
            text = p.read_bytes().decode("utf-8", "replace")
        except OSError as e:
            return ToolResult.fail("读不了: " + str(e))
        lines = text.splitlines()
        return ToolResult.ok(f"{p}\n行数 {len(lines)}（其中空行 "
                             f"{sum(1 for x in lines if not x.strip())}）")

    def _do_word_count(self, p):
        if not p.is_file():
            return ToolResult.fail("不是文件: " + str(p))
        try:
            text = p.read_bytes().decode("utf-8", "replace")
        except OSError as e:
            return ToolResult.fail("读不了: " + str(e))
        words = text.split()
        return ToolResult.ok(f"{p}\n词数 {len(words)}，字符（含空白）{len(text)}，"
                             f"字符（不含空白）{len(text) - sum(1 for c in text if c.isspace())}")

    def _do_file_info(self, p):
        if not p.exists():
            return ToolResult.fail("不存在: " + str(p))
        try:
            st = p.stat()
        except OSError as e:
            return ToolResult.fail("取不到信息: " + str(e))
        kind = "目录" if p.is_dir() else ("文件" if p.is_file() else "其它")
        mt = datetime.datetime.fromtimestamp(st.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
        size = "" if p.is_dir() else f"\n大小 {_fmt_bytes(st.st_size)}（{st.st_size} 字节）"
        extra = ""
        if p.is_file():
            try:
                # 【只读需要的那 2MB】原来 `p.read_bytes()[:2_000_000]` 是把**整个文件**
                # 读进内存再切片 —— GB 级文件为了算个"前 2MB"哈希瞬时吃掉等量内存。
                with open(p, "rb") as fh:
                    h = hashlib.sha256(fh.read(2_000_000)).hexdigest()[:16]
                extra = f"\nsha256(前2MB) {h}"
            except OSError:
                pass
        return ToolResult.ok(f"{p}\n类型 {kind}{size}\n修改时间 {mt}{extra}")

    _stat_tool("line_count", "tool.file.linecount",
               "数文件行数（用户问「多少行」时用它）。空行数也一并给出。",
               _do_line_count)
    _stat_tool("word_count", "tool.file.wordcount",
               "数文件的词数/字符数。",
               _do_word_count)
    _stat_tool("file_info", "tool.file.info",
               "看文件/目录的元信息（类型、大小、修改时间、哈希）。\n"
               "要看内容用 read_file；要列目录用 list_directory。",
               _do_file_info)

    # ────────────────────────────── 写操作 ──────────────────────────────
    @tool
    class ModifyFileTool(ToolPlugin):
        """把文件里的一段文本精确替换掉。"""
        minimal_mode = True

        @property
        def id(self): return "tool.file.modify"

        @property
        def name(self): return "modify_file"

        @property
        def description(self):
            return (
                "把文件里的一段文本替换成新文本（改代码的主力工具）。\n"
                "用法：\n"
                "- 必填 `path` `old` `new`；`old` 必须**在文件里原样存在**"
                "（包括缩进），否则会明确报错而不会乱写。\n"
                "- 先 read_file 看清楚原文再改；`old` 给太短容易匹配到多处"
                "（会报「找到 N 处」，让你给更长的上下文）。\n"
                "- 整文件重写用 write_file；追加用 append_file。\n"
                "- 改完会告诉你替换了几处。"
            )

        @property
        def category(self): return ToolCategory.FILE_MODIFY

        @property
        def permission(self): return PermissionLevel.WRITE

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"path": {"type": "string"},
                                   "old": {"type": "string"},
                                   "new": {"type": "string"},
                                   "count": {"type": "number"}},
                    "required": ["path", "old", "new"]}

        def execute(self, args):
            for k in ("path", "old", "new"):
                if k not in args:
                    return ToolResult.fail("缺少参数: " + k)
            try:
                p = self.resolve_path(str(args["path"]))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            if not p.is_file():
                return ToolResult.fail("不是文件（不存在或为目录）: " + str(p))
            old, new = str(args["old"]), str(args["new"])
            if old == "":
                return ToolResult.fail("old 不能为空")
            try:
                text = p.read_bytes().decode("utf-8")
            except UnicodeDecodeError:
                return ToolResult.fail("这不是 UTF-8 文本文件，改不了: " + str(p))
            except OSError as e:
                return ToolResult.fail("读不了: " + str(e))
            n = text.count(old)
            if n == 0:
                return ToolResult.fail(
                    "在文件里找不到 old 那段原文（一处都没有）—— 没有做任何修改。\n"
                    "请先用 read_file 看准确切内容（注意缩进与换行），再重试。")
            want = args.get("count")
            if want is not None:
                try:
                    want = int(want)
                except (TypeError, ValueError):
                    want = None
            # 【count 的 0/负数不能当"全部"】CPython 实测：'aaa'.replace('a','b',0) 不替换、
            # 'aaa'.replace('a','b',-3) 替换全部。原代码 `want if want else -1` 把 0 换成 -1
            # → 用户要"0 处"却改了整个文件；负数还会报"替换了 -3 处"。
            if want == 0:
                return ToolResult.ok(f"已修改 {p}\n替换了 0 处（count=0，按你的要求没有改动文件）")
            if want is not None and want < 0:
                return ToolResult.fail(f"count 必须是 >= 1 的整数（你给的是 {want}）—— 没有做任何修改")
            if want is None and n > 1:
                return ToolResult.fail(
                    f"old 在文件里出现了 {n} 处，无法确定要改哪一处 —— 没有做任何修改。\n"
                    "请把 old 给长一点（带上前后几行或独特上下文），或用 count 指定处数。")
            # want=None（没传）只可能在 n==1 时走到这里：全量替换 == 替换这 1 处
            replaced = text.replace(old, new, -1 if want is None else want)
            try:
                p.write_bytes(replaced.encode("utf-8"))
            except OSError as e:
                return ToolResult.fail("写不了: " + str(e))
            done = n if not want else min(want, n)
            return ToolResult.ok(f"已修改 {p}\n替换了 {done} 处")

    @tool
    class CreateFileTool(ToolPlugin):
        """新建文件（已存在则不覆盖）。"""

        @property
        def id(self): return "tool.file.create"

        @property
        def name(self): return "create_file"

        @property
        def description(self):
            return (
                "新建文件（**已存在会失败，不会覆盖** —— 这是有意的保护）。\n"
                "用法：\n"
                "- 可选 `content`；不给她就建空文件。\n"
                "- 覆盖已有文件用 write_file；改一部分用 modify_file；追加用 append_file。"
            )

        @property
        def category(self): return ToolCategory.FILE_MODIFY

        @property
        def permission(self): return PermissionLevel.WRITE

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"path": {"type": "string"},
                                   "content": {"type": "string"}},
                    "required": ["path"]}

        def execute(self, args):
            if not args.get("path"):
                return ToolResult.fail("缺少 path 参数")
            try:
                p = self.resolve_path(str(args["path"]))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            if p.exists():
                return ToolResult.fail(
                    "文件已存在，没有覆盖: " + str(p) + "（要覆盖用 write_file，要改用 modify_file）")
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_bytes(str(args.get("content") or "").encode("utf-8"))
            except OSError as e:
                return ToolResult.fail("建不了: " + type(e).__name__ + ": " + str(e))
            return ToolResult.ok("已新建 " + str(p))

    @tool
    class AppendFileTool(ToolPlugin):
        """在文件末尾追加内容。"""

        @property
        def id(self): return "tool.file.append"

        @property
        def name(self): return "append_file"

        @property
        def description(self):
            return ("在文件末尾追加内容（文件不存在会新建）。\n"
                    "要改中间的一段用 modify_file，不要用本工具拼接。")

        @property
        def category(self): return ToolCategory.FILE_MODIFY

        @property
        def permission(self): return PermissionLevel.WRITE

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"path": {"type": "string"},
                                   "content": {"type": "string"}},
                    "required": ["path", "content"]}

        def execute(self, args):
            if not args.get("path"):
                return ToolResult.fail("缺少 path 参数")
            if "content" not in args:
                return ToolResult.fail("缺少 content 参数")
            try:
                p = self.resolve_path(str(args["path"]))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            try:
                p.parent.mkdir(parents=True, exist_ok=True)
                with open(p, "ab") as fh:
                    fh.write(str(args["content"]).encode("utf-8"))
            except OSError as e:
                return ToolResult.fail("追加失败: " + str(e))
            return ToolResult.ok("已追加到 " + str(p))

    @tool
    class DeleteFileTool(ToolPlugin):
        """删除文件或空目录（危险操作）。"""

        @property
        def id(self): return "tool.file.delete"

        @property
        def name(self): return "delete_file"

        @property
        def description(self):
            return (
                "删除文件（危险，需要授权）。\n"
                "用法：\n"
                "- **只能删文件或空目录**；非空目录会被拒绝（避免误删一整棵树）。\n"
                "- 删之前先确认路径（file_info / list_directory）；不确定就不要删。\n"
                "- 用户没明确要求删除时，**不要**主动删任何东西。"
            )

        @property
        def category(self): return ToolCategory.FILE_MODIFY

        @property
        def permission(self): return PermissionLevel.DANGEROUS

        def parameters_schema(self):
            return {"type": "object", "properties": {"path": {"type": "string"}},
                    "required": ["path"]}

        def execute(self, args):
            if not args.get("path"):
                return ToolResult.fail("缺少 path 参数")
            try:
                p = self.resolve_path(str(args["path"]))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            if not p.exists():
                return ToolResult.fail("不存在: " + str(p))
            try:
                if p.is_dir():
                    kids = list(p.iterdir())
                    if kids:
                        return ToolResult.fail(
                            f"这是非空目录（{len(kids)} 项），拒绝删除: {p}\n"
                            "确实要删整棵树的话，请人工在终端里操作。")
                    p.rmdir()
                else:
                    p.unlink()
            except OSError as e:
                return ToolResult.fail("删不掉: " + type(e).__name__ + ": " + str(e))
            return ToolResult.ok("已删除 " + str(p))

    def _copy_move(name, id_, desc, move: bool):
        @tool
        class _T(ToolPlugin):
            @property
            def id(self): return id_
            @property
            def name(self): return name
            @property
            def description(self): return desc
            @property
            def category(self): return ToolCategory.FILE_MODIFY
            @property
            def permission(self):
                return PermissionLevel.DANGEROUS if move else PermissionLevel.WRITE
            def parameters_schema(self):
                return {"type": "object",
                        "properties": {"source": {"type": "string"},
                                       "target": {"type": "string"},
                                       "path": {"type": "string"},
                                       "destination": {"type": "string"}},
                        "required": []}
            def execute(self, args):
                src = args.get("source") or args.get("path") or args.get("src")
                dst = args.get("target") or args.get("destination") or args.get("dest")
                if not src or not dst:
                    return ToolResult.fail("需要 source 和 target 两个参数")
                try:
                    s = self.resolve_path(str(src))
                    d = self.resolve_path(str(dst))
                except Exception as e:                     # noqa: BLE001
                    return ToolResult.fail("路径无法解析: " + str(e))
                if not s.exists():
                    return ToolResult.fail("源不存在: " + str(s))
                if d.exists():
                    return ToolResult.fail("目标已存在，没有覆盖: " + str(d))
                try:
                    d.parent.mkdir(parents=True, exist_ok=True)
                    if move:
                        shutil.move(str(s), str(d))
                    else:
                        shutil.copytree(str(s), str(d)) if s.is_dir() \
                            else shutil.copy2(str(s), str(d))
                except OSError as e:
                    return ToolResult.fail("操作失败: " + type(e).__name__ + ": " + str(e))
                return ToolResult.ok(("已移动 " if move else "已复制 ") + f"{s} → {d}")
        _T.__name__ = name + "Tool"
        return _T

    _copy_move("copy_file", "tool.file.copy",
               "复制文件或目录（目标已存在会拒绝，不覆盖）。", move=False)
    _copy_move("move_file", "tool.file.move",
               "移动/重命名文件或目录（危险，需要授权；目标已存在会拒绝）。", move=True)

    @tool
    class CreateDirectoryTool(ToolPlugin):
        """新建目录。"""

        @property
        def id(self): return "tool.file.mkdir"

        @property
        def name(self): return "create_directory"

        @property
        def description(self):
            return ("新建目录（父目录会自动创建；已存在不算错）。")

        @property
        def category(self): return ToolCategory.FILE_MODIFY

        @property
        def permission(self): return PermissionLevel.WRITE

        def parameters_schema(self):
            return {"type": "object", "properties": {"path": {"type": "string"}},
                    "required": ["path"]}

        def execute(self, args):
            if not args.get("path"):
                return ToolResult.fail("缺少 path 参数")
            try:
                p = self.resolve_path(str(args["path"]))
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("路径无法解析: " + str(e))
            try:
                p.mkdir(parents=True, exist_ok=True)
            except OSError as e:
                return ToolResult.fail("建不了: " + type(e).__name__ + ": " + str(e))
            return ToolResult.ok("目录已就绪 " + str(p))

    # ────────────────────────────── 系统 / 杂项 ──────────────────────────────
    @tool
    class SystemInfoTool(ToolPlugin):
        """看这台机器的配置。"""
        minimal_mode = True

        @property
        def id(self): return "tool.system.info"

        @property
        def name(self): return "system_info"

        @property
        def description(self):
            return ("看本机配置（CPU、内存、操作系统、Python 版本）。\n"
                    "用户问「什么配置/多少内存/什么系统」时用它 —— **不要靠猜**。")

        @property
        def category(self): return ToolCategory.SYSTEM

        @property
        def permission(self): return PermissionLevel.READ_ONLY

        def parameters_schema(self):
            return {"type": "object", "properties": {}, "required": []}

        def execute(self, args):
            info = [f"系统 {platform.system()} {platform.release()}（{platform.machine()}）",
                    f"Python {platform.python_version()} @ {sys.executable}"]
            try:
                if os.name == "nt":
                    import ctypes

                    class MEMORYSTATUSEX(ctypes.Structure):
                        _fields_ = [("dwLength", ctypes.c_ulong),
                                    ("dwMemoryLoad", ctypes.c_ulong),
                                    ("ullTotalPhys", ctypes.c_ulonglong),
                                    ("ullAvailPhys", ctypes.c_ulonglong),
                                    ("ullTotalPageFile", ctypes.c_ulonglong),
                                    ("ullAvailPageFile", ctypes.c_ulonglong),
                                    ("ullTotalVirtual", ctypes.c_ulonglong),
                                    ("ullAvailVirtual", ctypes.c_ulonglong),
                                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
                    st = MEMORYSTATUSEX()
                    st.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                    if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(st)):
                        info.append("内存 共 " + _fmt_bytes(st.ullTotalPhys)
                                    + "，可用 " + _fmt_bytes(st.ullAvailPhys)
                                    + f"（占用 {st.dwMemoryLoad}%）")
                    info.append("CPU 逻辑核 " + str(os.cpu_count()))
                    info.append("CPU " + (os.environ.get("PROCESSOR_IDENTIFIER") or "未知"))
                else:
                    info.append("CPU 逻辑核 " + str(os.cpu_count()))
                    if hasattr(os, "sysconf"):
                        try:
                            info.append("内存 共 " + _fmt_bytes(
                                os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES")))
                        except (ValueError, OSError, AttributeError):
                            pass
            except Exception as e:                         # noqa: BLE001
                info.append("（部分信息取不到: " + type(e).__name__ + "）")
            info.append("工作目录 " + os.getcwd())
            return ToolResult.ok("\n".join(info))

    @tool
    class TimestampTool(ToolPlugin):
        """看当前时间。"""
        minimal_mode = True

        @property
        def id(self): return "tool.system.timestamp"

        @property
        def name(self): return "timestamp"

        @property
        def description(self):
            return ("拿当前日期时间（用户问「现在几点/今天几号」时用它，别猜）。")

        @property
        def category(self): return ToolCategory.SYSTEM

        @property
        def permission(self): return PermissionLevel.READ_ONLY

        def parameters_schema(self):
            return {"type": "object", "properties": {}, "required": []}

        def execute(self, args):
            now = datetime.datetime.now()
            return ToolResult.ok(now.strftime("%Y-%m-%d %H:%M:%S")
                                 + f"（{now.strftime('%A')}，本地时区，UTC"
                                 + datetime.datetime.now().astimezone().strftime("%z") + "）")

    @tool
    class WorkingDirectoryTool(ToolPlugin):
        """看当前工作目录。"""

        @property
        def id(self): return "tool.system.cwd"

        @property
        def name(self): return "working_directory"

        @property
        def description(self):
            return ("看当前工作目录（不确定自己在哪个目录时用它）。")

        @property
        def category(self): return ToolCategory.SYSTEM

        @property
        def permission(self): return PermissionLevel.READ_ONLY

        def parameters_schema(self):
            return {"type": "object", "properties": {}, "required": []}

        def execute(self, args):
            lines = ["进程目录 " + os.getcwd()]
            try:
                lines.append("工作区 " + str(self.resolve_path(".")))
            except Exception as e:                         # noqa: BLE001
                lines.append("工作区取不到: " + type(e).__name__)
            return ToolResult.ok("\n".join(lines))

    @tool
    class ContextWindowTool(ToolPlugin):
        """看/设上下文窗口。"""

        @property
        def id(self): return "tool.context.window"

        @property
        def name(self): return "context_window"

        @property
        def description(self):
            return ("查当前上下文窗口上限（用户问「上下文多大/还剩多少」时用它）。\n"
                    "设上限请用 /context-limit 命令，不在这里改。")

        @property
        def category(self): return ToolCategory.CONTEXT

        @property
        def permission(self): return PermissionLevel.READ_ONLY

        def parameters_schema(self):
            return {"type": "object", "properties": {}, "required": []}

        def execute(self, args):
            info = []
            for attr in ("context_limit", "max_context", "context_window"):
                v = getattr(self, attr, None)
                if v:
                    info.append(f"{attr} = {v}")
            env = os.environ.get("LION_CONTEXT_LIMIT")
            if env:
                info.append("LION_CONTEXT_LIMIT = " + env)
            # 【这里原来是一句死代码】`import 沙箱` 的结果既没接收也没用上，注释却写着
            # "用后端已有的预算设施" —— 预算从来就没读到过。现在真的去问后端要
            # （和 context_prune 同一个入口），拿不到就保持下面这句如实说明。
            try:
                backend = NS.get("api")
                snapshot = backend.budget().snapshot("") if hasattr(backend, "budget") else None
                if snapshot:
                    info.append(f"预算快照: {snapshot}")
            except Exception:                              # noqa: BLE001
                pass                                       # 拿不到就走下面的"如实说"分支
            if not info:
                return ToolResult.ok(
                    "本工具拿不到窗口数值（后端未把预算暴露给工具层）。"
                    "默认 16384，可用 /context-limit 命令调整。")
            return ToolResult.ok("\n".join(info))

    @tool
    class FetchUrlTool(ToolPlugin):
        """抓取一个网址的内容。"""

        @property
        def id(self): return "tool.web.fetch"

        @property
        def name(self): return "fetch_url"

        @property
        def description(self):
            return ("抓取指定 URL 的文本内容（已知确切网址时用它）。\n"
                    "用法：\n"
                    "- 只知道要查什么、不知道网址，用 web_search。\n"
                    "- 返回会被截断（默认前 20000 字符）。\n"
                    "- 网络不通/超时会**如实报错**，不要据此编内容。")

        @property
        def category(self): return ToolCategory.WEB

        @property
        def permission(self): return PermissionLevel.EXECUTE

        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"url": {"type": "string"},
                                   "maxChars": {"type": "number"}},
                    "required": ["url"]}

        def execute(self, args):
            url = str(args.get("url") or "").strip()
            if not url:
                return ToolResult.fail("缺少 url 参数")
            if not re.match(r"^https?://", url, re.IGNORECASE):
                return ToolResult.fail("只支持 http/https 网址: " + url)
            try:
                limit = int(args.get("maxChars") or 20_000)
            except (TypeError, ValueError):
                limit = 20_000
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (compatible; LionCode/1.0)"})
            try:
                with urllib.request.urlopen(req, timeout=30) as r:
                    raw = r.read(4_000_000)
                    ctype = r.headers.get("Content-Type", "")
            except urllib.error.HTTPError as e:
                return ToolResult.fail(f"HTTP {e.code} {e.reason}（{url}）")
            except urllib.error.URLError as e:
                return ToolResult.fail("网络不通: " + str(e.reason) + "（" + url + "）")
            except Exception as e:                         # noqa: BLE001
                return ToolResult.fail("抓取失败: " + type(e).__name__ + ": " + str(e))
            text = raw.decode("utf-8", "replace")
            if "html" in ctype.lower():
                text = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", text)
                text = re.sub(r"(?s)<[^>]+>", " ", text)
                text = re.sub(r"[ \t\r\f\v]+", " ", text)
                text = re.sub(r"\n\s*\n+", "\n\n", text).strip()
            return ToolResult.ok(_truncate(text, limit) if len(text) > limit else text)
    # ── 权限等级覆盖（本次修正）──────────────────────────────────────────

    # 【为什么需要】核查发现 20 个工具没声明 permission（属性是 None，不是基类

    # 默认值），而权限门禁判的是 `required == PermissionLevel.READ_ONLY` ——

    # None 不成立，于是在**只读工作区**里连 base64/hash/json_format 这类纯计算

    # 都被拦；git_status/diff/log/branch 又错标成 EXECUTE。这里按名字统一纠正，

    # 一处收口、便于复查（不改各工具类本身，避免散落 24 处）。

    _LEVEL_OVERRIDE = {}

    for _n in ['base64', 'hash', 'generate_uuid', 'escape_string', 'string_utils', 'regex_test', 'number_convert', 'diff_text', 'json_format', 'yaml_process', 'cron_parse', 'format_code', 'markdown_render', 'translate', 'dns_lookup', 'get_env', 'http_get', 'ask_user', 'working_directory', 'context_window', 'system_info', 'timestamp', 'git_status', 'git_diff', 'git_log', 'git_branch']:

        _LEVEL_OVERRIDE[_n] = PermissionLevel.READ_ONLY

    for _n in ['git_add', 'git_commit', 'git_stash', 'git_init', 'git_remote', 'context_prune']:

        _LEVEL_OVERRIDE[_n] = PermissionLevel.WRITE

    for _n in ['delete_file', 'move_file', 'change_permissions', 'git_reset']:

        _LEVEL_OVERRIDE[_n] = PermissionLevel.DANGEROUS

    for _c in out:

        # 【类上取 name 拿到的是 property 对象】工具类把 name 定义成 @property，
        # `getattr(类, "name")` 返回 property 本身、不是字符串 —— 拿它当 key 查
        # _LEVEL_OVERRIDE 永远查不到，这段权限覆盖从来没生效过（现网没炸只因为
        # main.py build_registry 又在**实例**上做了一遍；走 register_extra 这条路
        # 就没人兜底）。按 fget 求值取出真正的名字（见 _tool_class_name）。
        _lv = _LEVEL_OVERRIDE.get(_tool_class_name(_c))

        if _lv is not None:

            _c.permission = property(lambda self, _v=_lv: _v)

    return out

def _tool_class_name(cls) -> str | None:
    """取工具**类**的 name 字符串（取不到返回 None，调用方按"不认识这个工具"处理）。

    `getattr(cls, "name")` 对 @property 类返回的是 property 对象本身，不能当 key 用；
    这些 getter 都只返回常量，所以直接拿 fget 求值即可。真读 self 的 getter（不存在于
    本文件，但保险起见）会抛异常 —— 按取不到处理，退回"不做覆盖"，不会比修复前更差。
    """
    prop = cls.__dict__.get("name") if isinstance(cls, type) else None
    if prop is None:
        prop = getattr(cls, "name", None)
    if isinstance(prop, property) and prop.fget is not None:
        try:
            value = prop.fget(None)
        except Exception:                              # noqa: BLE001
            return None
        return value if isinstance(value, str) else None
    return prop if isinstance(prop, str) else None

def register_extra(reg, NS: dict) -> int:
    """把本模块的工具注册进 reg（同名会覆盖桩实现）。返回注册个数。"""
    ws = getattr(reg, "workspace", None)
    n = 0
    for cls in build_tools(NS):
        try:
            reg.register(cls(ws) if ws is not None else cls(Path.cwd()))
            n += 1
        except Exception as e:                         # noqa: BLE001
            # 【不能静默吞】单个工具构造/注册失败原来被 continue 掉：外层只看到 n 变小，
            # 模型侧只表现为"未找到工具"，一行日志都没有，查都没法查。
            print(f"[工具] 注册 {getattr(cls, '__name__', cls)} 失败: "
                  f"{type(e).__name__}: {e}")
    return n


# ============================================================================
# 【第三批工具：原 工具集2.py —— 第二批补全的 33 个（git9 / 网络4 /
#   编码文本8 / 格式数据6 / 进程2 / 杂项4）】
#
# 合并时改过的名字（都因为同名 ✗）：
#   · MAX_OUTPUT  → MAX_OUTPUT_B2    （第一批已有 MAX_OUTPUT ✓ 语义相同但值可能不同，
#                                     保守起见不合并常量，避免悄悄改变某一批的截断阈值 ✓）
#   · _truncate   → _truncate_b2     （同上）
#   · build_tools(NS) → _build_batch2(NS)
# 其余原样搬运 ✓
# ============================================================================


# -*- coding: utf-8 -*-
r"""工具补全 第二批：把**剩下 33 个广告名**全部做成真实现。

【盘点（脚本从代码取的权威名单，不是猜）】
  A 广告 57 个 = 别名表正名 55 ∪ TOOL_PROMPT_HINTS 57
  B 已注册 24 个（第一批 工具集.py ✓）
  缺 33 个 —— 本模块补齐：
    git 类(9)   git_status git_diff git_log git_commit git_branch git_init
                git_remote git_reset git_stash
    网络类(4)   http_get http_post download_file dns_lookup
    编码文本(8) base64 hash generate_uuid escape_string string_utils
                regex_test number_convert diff_text
    格式数据(6) json_format yaml_process cron_parse format_code markdown_render translate
    进程类(2)   run_background stop_background
    杂项(4)     get_env context_prune ask_user change_permissions

【三条硬约定（照第一批）】
  · 路径走 `self.resolve_path()`（沙箱的工作区约束，不绕过去）
  · 权限用 `PermissionLevel` 声明，确不确认交给权限层
  · **失败必须说清为什么** —— 别返回空字符串，模型会以为成功然后继续瞎调
    （这正是本会话"工具是空壳 → 模型反复瞎试"的根源）

【本机环境（实测，写死在这里的原因见下）】
  · Windows + PowerShell；**裸 `where` 是 `Where-Object` 的别名，什么都不输出** ✗
    → 一律 `where.exe` ✓（这批工具自己调 subprocess，不经过 shell，无此问题）
  · `git` / `python` / `node` 都在 PATH ✓；`uv` `ollama` `go` `rg` **没装** ✓
  · **HTTPS 到 github 不通**（只 SSH 通）→ 网络类工具**实测可达性后再决定行为**，
    不可达时**如实报错**（不是假装成功）
"""

import base64 as _b64
import datetime
import difflib
import hashlib as _hash
# fnmatch：search_in_files 的 glob 过滤要用（漏 import 的话只要文件树里有一个
# 不匹配 glob 的文件，`fnmatch.fnmatch(...)` 就被求值 → NameError → 整个工具炸）
import fnmatch
import json
import os
import re
import socket
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
import uuid as _uuid
from pathlib import Path

MAX_OUTPUT_B2 = 60_000
_UA = {"User-Agent": "lion-code-tool/1.0"}

#: batch2  HTTP 通道的读取上限（与 web 版 MAX_BODY_BYTES 同一档：5MB）
_HTTP_MAX_B2 = 5 * 1024 * 1024


def _truncate_b2(text: str, limit: int = MAX_OUTPUT_B2) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n…（共 {len(text)} 字符，已截断到前 {limit}）"


def _int_b2(value, default: int) -> int:
    """安全取整（拿不到就用默认值），不让乱值把整次工具调用炸成"工具执行异常"。

    【为什么必须兜】schema 写的是 number，但模型经常给字符串：timeout="60s"、
    limit="10.5"、count="3" —— 裸 `int(...)` 抛 ValueError 会一路冒出 execute，
    模型看到的是"工具执行异常"而不是"参数不对"。bool 是 int 的子类，显式排除。
    """
    if value is None or isinstance(value, bool):
        return default
    if isinstance(value, int):
        return value
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        try:
            return int(float(str(value).strip()))      # "10.5" 这种还能救回来
        except (TypeError, ValueError):
            return default


def _run(cmd: list[str], cwd: str, timeout: int = 60) -> tuple[int, str]:
    """跑一个**不经 shell** 的命令（列表参数，天然免疫引号/分隔符问题）。"""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
        out = (p.stdout or "") + (("\n[stderr]\n" + p.stderr) if p.stderr else "")
        return p.returncode, _truncate_b2(out.strip())
    except FileNotFoundError:
        return 127, f"命令不存在：{cmd[0]}（本机可能没装；用 where.exe {cmd[0]} 确认）"
    except subprocess.TimeoutExpired:
        return 124, f"超时（{timeout}s）已终止：{' '.join(cmd)}"
    except Exception as e:                                  # noqa: BLE001
        return 1, f"{type(e).__name__}: {e}"


def _http(url: str, data: bytes | None = None, timeout: int = 30,
          headers: dict | None = None) -> tuple[bool, str]:
    """统一的 HTTP 通道（http/https）；失败**如实返回原因**。"""
    if not re.match(r"^https?://", url or ""):
        return False, "只支持 http/https"
    req = urllib.request.Request(url, data=data, headers={**_UA, **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            # 【读取必须有上限】原来 `r.read()` 是整个响应无上限进内存（同文件 web 版
            # http_get 专门加了 5MB 的闸），给一个 GB 级地址就是内存打爆。
            # 本通道没声明 Accept-Encoding，服务端一般回明文，按明文截断即可。
            raw = r.read(_HTTP_MAX_B2 + 1)
            truncated = len(raw) > _HTTP_MAX_B2
            if truncated:
                raw = raw[:_HTTP_MAX_B2]
            ctype = r.headers.get("Content-Type", "")
            if "text" in ctype or "json" in ctype or "xml" in ctype:
                text = raw.decode("utf-8", "replace")
                if truncated:
                    text += f"\n…（响应体超过 {_HTTP_MAX_B2 // (1024 * 1024)}MB 已截断）"
                return True, _truncate_b2(text)
            return True, f"[{ctype or 'binary'}] {len(raw)} 字节（非文本，未展开）"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return False, f"连不上：{e.reason}（本机 HTTPS 对部分站点不通，属已知环境限制）"
    except Exception as e:                                  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def _build_batch2(NS: dict) -> list:
    """用调用方传进来的基类造工具类清单（避免与 main.py 循环导入）。

    :param NS: 需含 ToolPlugin / ToolResult / PermissionLevel / ToolCategory
    """
    ToolPlugin = NS["ToolPlugin"]
    ToolResult = NS["ToolResult"]
    PermissionLevel = NS["PermissionLevel"]
    ToolCategory = NS["ToolCategory"]

    # 分类名做防御式取用：不同版本枚举取值可能不同，取不到就退回 SHELL
    CAT_SHELL = getattr(ToolCategory, "SHELL", None)
    # ToolCategory 只有 FILE_OPERATION/FILE_MODIFY/FILE_SEARCH，**没有** "FILE" ——
    # 拿不到就恒退回 SHELL，hash/diff_text 的类别会错标成 SHELL（/api/plugins 按类别
    # 分组与极简模式判定都跟着错）。按真实存在的成员名取。
    CAT_FILE = getattr(ToolCategory, "FILE_OPERATION", CAT_SHELL)
    CAT_NET = getattr(ToolCategory, "NETWORK", getattr(ToolCategory, "WEB", CAT_SHELL))
    CAT_OTHER = getattr(ToolCategory, "OTHER", CAT_SHELL)
    # PermissionLevel 只有 READ_ONLY/WRITE/WORKSPACE_WRITE/EXECUTE/DANGEROUS，**没有**
    # "READ" —— getattr 到 None 时这 20 个纯计算工具的 permission 是 None，权限门禁
    # 判 `required == READ_ONLY` 恒为 False，只读工作区里全被拦（取不到就该退回 READ_ONLY）。
    LV_READ = getattr(PermissionLevel, "READ", PermissionLevel.READ_ONLY)
    LV_WRITE = getattr(PermissionLevel, "WRITE", None)
    LV_EXEC = getattr(PermissionLevel, "EXECUTE", None)

    out: list = []

    def tool(cls):
        out.append(cls)
        return cls

    def git_tool(name, ident, desc, params, build_args):
        """git 类工具的公共壳：统一处理"不是仓库"与"git 不存在"。"""
        @tool
        class _Git(ToolPlugin):
            @property
            def id(self): return ident
            @property
            def name(self): return name
            @property
            def description(self): return desc
            @property
            def category(self): return CAT_SHELL
            @property
            def permission(self): return LV_EXEC
            def parameters_schema(self): return {"type": "object", "properties": params,
                                                 "required": []}
            def execute(self, args):
                cwd = str(self.resolve_path(args.get("path") or "."))
                # 【防呆 · 血的教训】目标路径存在但是**文件**时直接拒绝。
                # 曾经发生过：有人以 path="main.py" 调 git 类工具，而预检
                # `git rev-parse --is-inside-work-tree` 对**外层仓库的子目录**会通过
                # （main.py/ 若已被建成目录，它就在外层工作树里 → rc=0），
                # 于是 git init 真的在里面跑起来，把 1.1 MB 的 main.py 覆盖成一个空仓库。
                # 这条守卫对所有走这个壳的 git 工具生效。
                if os.path.isfile(cwd):
                    return ToolResult.fail(
                        f"目标路径是一个**文件**，不是目录：{cwd}\n"
                        "（拒绝执行：把文件当仓库目录会破坏它。要操作这个文件请用 read_file / modify_file）")
                rc, _ = _run(["git", "rev-parse", "--is-inside-work-tree"], cwd, 20)
                if rc != 0:
                    return ToolResult.fail(
                        f"当前目录不是 git 仓库：{cwd}\n"
                        "（要用 git_init 初始化，或把 path 指向仓库目录）")
                argv = build_args(args)
                if isinstance(argv, str):                  # 参数校验失败
                    return ToolResult.fail(argv)
                rc, text = _run(["git"] + argv, cwd, _int_b2(args.get("timeout"), 60))
                body = text or "(无输出)"
                if rc != 0:
                    return ToolResult.fail(f"git {' '.join(argv)} 退出码 {rc}：\n{body}")
                return ToolResult.ok(body)
        _Git.__name__ = name + "_tool"
        return _Git

    # ───────────────────────────── git 类（9） ─────────────────────────────
    P_PATH = {"path": {"type": "string", "description": "仓库目录，默认当前目录"},
              "timeout": {"type": "number"}}

    git_tool("git_status", "tool.git.status",
             "看仓库当前状态（分支 + 改动清单）。用户问'改了哪些文件/有没有未提交'就用它。",
             P_PATH, lambda a: ["status", "--short", "--branch"])

    git_tool("git_diff", "tool.git.diff",
             "看改动内容。默认看工作区未暂存的改动；staged=true 看已暂存的。"
             "只想知道改了哪些文件、不需要内容时用 git_status（更快）。",
             {**P_PATH, "staged": {"type": "boolean"}, "file": {"type": "string"}},
             lambda a: (["diff", "--cached"] if a.get("staged") else ["diff"])
                       + ([str(a["file"])] if a.get("file") else []))

    git_tool("git_log", "tool.git.log",
             "看提交历史（默认最近 20 条，一行一条）。想看某文件的改动用 git_diff 配 file。",
             {**P_PATH, "limit": {"type": "number"}},
             # limit 乱值/0/负数都不能让整次调用炸掉或拼出 `git log -0`：兜成 >=1
             lambda a: ["log", "-" + str(max(1, _int_b2(a.get("limit"), 20) or 20)),
                        "--oneline", "--decorate"])

    def _commit_args(a):
        msg = str(a.get("message") or "").strip()
        if not msg:
            return "缺少 message 参数（提交必须写提交信息）"
        return ["commit", "-m", msg]

    @tool
    class GitCommitTool(ToolPlugin):
        """git 提交（**两步：先 add -A，再 commit**）。"""
        @property
        def id(self): return "tool.git.commit"
        @property
        def name(self): return "git_commit"
        @property
        def description(self):
            return ("提交改动。默认先把所有改动 `add -A` 再提交（add_all=false 只提交已暂存的）。\n"
                    "空暂存区会**如实报\"没有可提交的改动\"**，不会假装成功。\n"
                    "失败时把 git 的原话带回来，不吞掉。")
        @property
        def category(self): return CAT_SHELL
        @property
        def permission(self): return LV_EXEC
        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"path": {"type": "string"},
                                   "message": {"type": "string"},
                                   "add_all": {"type": "boolean"},
                                   "timeout": {"type": "number"}},
                    "required": ["message"]}
        def execute(self, args):
            cwd = str(self.resolve_path(args.get("path") or "."))
            rc, _ = _run(["git", "rev-parse", "--is-inside-work-tree"], cwd, 20)
            if rc != 0:
                return ToolResult.fail(f"当前目录不是 git 仓库：{cwd}")
            msg = str(args.get("message") or "").strip()
            if not msg:
                return ToolResult.fail("缺少 message 参数（提交必须写提交信息）")
            # 第一步：暂存（可关）。**这一步以前漏了** —— 那时 build_args 只返回
            # ["add","-A"]，而公共外壳只跑一条命令，于是"提交"实际只做了 add，
            # 工具却回报成功（自测抓到的：git_commit 之后 git_log 里没有那条提交）。
            if args.get("add_all") is not False:
                rc, text = _run(["git", "add", "-A"], cwd, 60)
                if rc != 0:
                    return ToolResult.fail(f"git add -A 失败（退出码 {rc}）：\n{text}")
            # 第二步：提交
            rc, text = _run(["git", "commit", "-m", msg], cwd,
                            _int_b2(args.get("timeout"), 60))
            if rc != 0:
                low = (text or "").lower()
                if "nothing to commit" in low or "no changes added" in low:
                    return ToolResult.fail("没有可提交的改动（暂存区是空的）")
                return ToolResult.fail(f"git commit 失败（退出码 {rc}）：\n{text or '(无输出)'}")
            return ToolResult.ok(text or f"已提交：{msg}")

    git_tool("git_branch", "tool.git.branch",
             "列出分支（当前分支带 *）。不切换分支。",
             P_PATH, lambda a: ["branch", "-a", "-vv"])

    # 【git_init 必须独立实现，不能走公共壳】两个原因：
    #   ① 公共壳开头就验"是不是仓库"，而 init 的对象**本来就不是**仓库 → 永远跑不通；
    #   ② 更要命的是那句预检对"外层仓库的子目录"会**通过**（rc=0），
    #      于是 git_init 会在一个子目录里再 init 一次 —— 实测就是这条把 main.py 覆盖了：
    #      有人以 path="main.py" 调它，main.py 被建成目录后落在外层工作树里 →
    #      预检通过 → git init 在里面跑 → 源文件变成一个空仓库 ✗
    @tool
    class _GitInit(ToolPlugin):
        @property
        def id(self): return "tool.git.init"
        @property
        def name(self): return "git_init"
        @property
        def description(self): return (
            "把一个**目录**初始化成 git 仓库（git init）。"
            "目标已存在且是仓库时会如实说明；**目标是文件时拒绝执行**。")
        @property
        def category(self): return CAT_SHELL
        @property
        def permission(self): return LV_EXEC
        def parameters_schema(self):
            return {"type": "object", "properties": P_PATH, "required": []}

        def execute(self, args):
            p = Path(str(self.resolve_path(args.get("path") or ".")))
            # ① 目标是文件 → 拒绝（这是那次事故的形态）
            if p.is_file():
                return ToolResult.fail(
                    f"目标是一个**文件**而不是目录：{p}\n"
                    "（拒绝执行：git init 会把它变成目录并覆盖内容）")
            # ② 已存在且已是仓库 → 如实说明，不重复 init
            if p.is_dir():
                rc, _ = _run(["git", "-C", str(p), "rev-parse", "--git-dir"], str(p), 20)
                if rc == 0:
                    return ToolResult.ok(f"已经是 git 仓库了，无需初始化：{p}")
            else:
                # ③ 不存在 → 这才是 init 的正常用法：建目录再 init
                try:
                    p.mkdir(parents=True, exist_ok=True)
                except OSError as e:
                    return ToolResult.fail(f"建目录失败：{p}（{type(e).__name__}: {e}）")
            rc, text = _run(["git", "init"], str(p), _int_b2(args.get("timeout"), 60))
            if rc != 0:
                return ToolResult.fail(f"git init 失败（退出码 {rc}）：\n{text or '(无输出)'}")
            return ToolResult.ok(text or f"已初始化：{p}")

    git_tool("git_remote", "tool.git.remote",
             "看/加远端。不带参数列出远端；带 name+url 则添加。",
             {**P_PATH, "name": {"type": "string"}, "url": {"type": "string"}},
             lambda a: (["remote", "-v"] if not a.get("name")
                        else (["remote", "add", str(a["name"]), str(a["url"])]
                              if a.get("url") else "加远端要同时给 name 和 url")))

    def _reset_args(a):
        mode = str(a.get("mode") or "--mixed")
        if mode not in ("--soft", "--mixed"):
            return ("git_reset 只允许 --soft / --mixed；"
                    "--hard 会丢改动，已被拒绝（要丢弃改动请自己在终端确认后操作）")
        return ["reset", mode, str(a.get("target") or "HEAD")]
    git_tool("git_reset", "tool.git.reset",
             "撤销提交但保留改动（默认 --mixed）。**不允许 --hard**（会丢改动，已拦）。",
             {**P_PATH, "mode": {"type": "string"}, "target": {"type": "string"}},
             _reset_args)

    git_tool("git_stash", "tool.git.stash",
             "暂存/恢复未提交改动。action: list（默认）/ push / pop。",
             {**P_PATH, "action": {"type": "string"}},
             lambda a: ({"list": ["stash", "list"], "push": ["stash", "push"],
                         "pop": ["stash", "pop"]}.get(str(a.get("action") or "list"))
                        or "action 只能是 list / push / pop"))

    # ───────────────────────────── 网络类（4） ─────────────────────────────
    @tool
    class HttpGetTool(ToolPlugin):
        """抓取 URL 内容（只读）。"""
        @property
        def id(self): return "tool.net.http_get"
        @property
        def name(self): return "http_get"
        @property
        def description(self):
            return ("GET 一个 http/https 地址并返回内容（文本展开、非文本报大小）。\n"
                    "本机 HTTPS 对部分站点不通，连不上会**如实报错**（不是空结果）。\n"
                    "只想抓网页正文时用 fetch_url；这个更偏裸接口调用。")
        @property
        def category(self): return CAT_NET
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"url": {"type": "string"},
                                                     "timeout": {"type": "number"}},
                    "required": ["url"]}
        def execute(self, args):
            url = str(args.get("url") or "").strip()
            if not url:
                return ToolResult.fail("缺少 url 参数")
            ok, text = _http(url, timeout=_int_b2(args.get("timeout"), 30))
            return ToolResult.ok(text) if ok else ToolResult.fail(text)

    @tool
    class HttpPostTool(ToolPlugin):
        """向 URL POST（JSON 或表单）。"""
        @property
        def id(self): return "tool.net.http_post"
        @property
        def name(self): return "http_post"
        @property
        def description(self):
            return ("POST 请求。body 给字符串原样发；给对象则按 JSON 发。\n"
                    "失败会如实报 HTTP 状态与原因。")
        @property
        def category(self): return CAT_NET
        @property
        def permission(self): return LV_EXEC
        def parameters_schema(self):
            return {"type": "object", "properties": {"url": {"type": "string"},
                                                     "body": {}, "timeout": {"type": "number"}},
                    "required": ["url"]}
        def execute(self, args):
            url = str(args.get("url") or "").strip()
            if not url:
                return ToolResult.fail("缺少 url 参数")
            body = args.get("body")
            if isinstance(body, (dict, list)):
                data = json.dumps(body, ensure_ascii=False).encode("utf-8")
                hdrs = {"Content-Type": "application/json"}
            elif isinstance(body, str):
                data = body.encode("utf-8")
                hdrs = {"Content-Type": "text/plain; charset=utf-8"}
            else:
                data, hdrs = b"", {}
            ok, text = _http(url, data=data, headers=hdrs,
                             timeout=_int_b2(args.get("timeout"), 30))
            return ToolResult.ok(text) if ok else ToolResult.fail(text)

    @tool
    class DownloadFileTool(ToolPlugin):
        """下载文件到本地（真落盘）。"""
        @property
        def id(self): return "tool.net.download"
        @property
        def name(self): return "download_file"
        @property
        def description(self):
            return ("把 URL 下载到本地路径，返回**真实字节数**。\n"
                    "目标目录不存在会自动建；下载失败不会留下半个文件（会删掉）。")
        @property
        def category(self): return CAT_NET
        @property
        def permission(self): return LV_WRITE
        def parameters_schema(self):
            return {"type": "object", "properties": {"url": {"type": "string"},
                                                     "path": {"type": "string"},
                                                     "timeout": {"type": "number"}},
                    "required": ["url", "path"]}
        def execute(self, args):
            url = str(args.get("url") or "").strip()
            if not url or not args.get("path"):
                return ToolResult.fail("需要 url 与 path 两个参数")
            dest = self.resolve_path(str(args["path"]))
            # 【目标已存在就拒绝】与 move_file / copy_file / create_file 保持同一策略 ✓
            # footgun 审计实测：原来会**静默覆盖**（27 字节的已有文件被 29506 字节的下载
            # 内容顶掉 ✗ 而返回只说"已下载" ✗）—— 下载覆盖是最没必要的破坏 ✓。
            if dest.exists():
                return ToolResult.fail("目标已存在，没有覆盖: " + str(dest)
                                       + "（要覆盖请先 delete_file 或换个路径）")
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not re.match(r"^https?://", url):
                return ToolResult.fail("只支持 http/https")
            try:
                req = urllib.request.Request(url, headers=_UA)
                with urllib.request.urlopen(req, timeout=_int_b2(args.get("timeout"), 60)) as r, \
                        open(dest, "wb") as fh:
                    n = 0
                    while True:
                        chunk = r.read(65536)
                        if not chunk:
                            break
                        fh.write(chunk)
                        n += len(chunk)
                return ToolResult.ok(f"已下载 {n} 字节 → {dest}")
            except Exception as e:                          # noqa: BLE001
                if dest.exists():
                    try:
                        dest.unlink()                       # 别留半个文件
                    except OSError:
                        pass
                return ToolResult.fail(f"下载失败（{type(e).__name__}）：{e}")

    @tool
    class DnsLookupTool(ToolPlugin):
        """域名解析（本地就能做，不依赖外网 HTTP）。"""
        @property
        def id(self): return "tool.net.dns"
        @property
        def name(self): return "dns_lookup"
        @property
        def description(self):
            return ("把域名解析成 IP（socket.getaddrinfo，走本机 DNS）。\n"
                    "解析不了会如实报错——这**不代表**该站点 HTTP 可达/不可达。")
        @property
        def category(self): return CAT_NET
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"host": {"type": "string"}},
                    "required": ["host"]}
        def execute(self, args):
            host = str(args.get("host") or "").strip()
            if not host:
                return ToolResult.fail("缺少 host 参数")
            try:
                infos = socket.getaddrinfo(host, None)
                ips = sorted({i[4][0] for i in infos})
                return ToolResult.ok(f"{host} → " + ", ".join(ips))
            except socket.gaierror as e:
                return ToolResult.fail(f"解析失败：{e}（域名可能不存在，或本机 DNS 不可用）")

    # ───────────────────────── 编码 / 文本 / 数据（14） ─────────────────────────
    @tool
    class Base64Tool(ToolPlugin):
        """base64 编解码。"""
        @property
        def id(self): return "tool.text.base64"
        @property
        def name(self): return "base64"
        @property
        def description(self):
            return ("base64 编码或解码。mode=encode（默认）/ decode。\n"
                    "decode 遇到非法 base64 会如实报错（不会给你一堆乱码）。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "mode": {"type": "string"}},
                    "required": ["text"]}
        def execute(self, args):
            text = str(args.get("text") or "")
            if not text and args.get("text") is None:
                return ToolResult.fail("缺少 text 参数")
            mode = str(args.get("mode") or "encode").lower()
            try:
                if mode.startswith("dec"):
                    return ToolResult.ok(_b64.b64decode(text, validate=True)
                                         .decode("utf-8", "replace"))
                return ToolResult.ok(_b64.b64encode(text.encode("utf-8")).decode())
            except Exception as e:                          # noqa: BLE001
                return ToolResult.fail(f"{mode} 失败：{type(e).__name__}: {e}")

    @tool
    class HashTool(ToolPlugin):
        """算哈希（文件或字符串）。"""
        @property
        def id(self): return "tool.text.hash"
        @property
        def name(self): return "hash"
        @property
        def description(self):
            return ("算哈希。给 path 则算文件（大文件也流式读完），给 text 则算字符串。\n"
                    "algo 默认 sha256，可选 md5 / sha1 / sha512。")
        @property
        def category(self): return CAT_FILE
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"path": {"type": "string"},
                                                     "text": {"type": "string"},
                                                     "algo": {"type": "string"}},
                    "required": []}
        def execute(self, args):
            algo = str(args.get("algo") or "sha256").lower()
            if algo not in ("md5", "sha1", "sha256", "sha512"):
                return ToolResult.fail("algo 只能是 md5 / sha1 / sha256 / sha512")
            if args.get("path"):
                p = self.resolve_path(str(args["path"]))
                if not p.is_file():
                    return ToolResult.fail(f"不是文件：{p}")
                h = _hash.new(algo)
                with open(p, "rb") as fh:
                    for chunk in iter(lambda: fh.read(1 << 20), b""):
                        h.update(chunk)
                return ToolResult.ok(f"{algo}({p.name}) = {h.hexdigest()}")
            if args.get("text") is not None:
                h = _hash.new(algo)
                h.update(str(args["text"]).encode("utf-8"))
                return ToolResult.ok(f"{algo}(text) = {h.hexdigest()}")
            return ToolResult.fail("至少给 path 或 text 之一")

    @tool
    class UuidTool(ToolPlugin):
        """生成 UUID。"""
        @property
        def id(self): return "tool.text.uuid"
        @property
        def name(self): return "generate_uuid"
        @property
        def description(self):
            return "生成 UUID（默认 1 个，count 可指定个数，最多 100）。version 1 或 4。"
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"count": {"type": "number"},
                                                     "version": {"type": "number"}},
                    "required": []}
        def execute(self, args):
            # count/version 乱值（"abc"）原来直接抛 ValueError → "工具执行异常"，
            # 这里兜成默认值（uuid 一次一个、version 4）
            n = max(1, min(100, _int_b2(args.get("count"), 1)))
            v = _int_b2(args.get("version"), 4)
            gen = _uuid.uuid1 if v == 1 else _uuid.uuid4
            return ToolResult.ok("\n".join(str(gen()) for _ in range(n)))

    @tool
    class EscapeStringTool(ToolPlugin):
        """转义/反转义字符串。"""
        @property
        def id(self): return "tool.text.escape"
        @property
        def name(self): return "escape_string"
        @property
        def description(self):
            return ("按目标环境转义：json（默认）/ url / html / regex / shell_ps。\n"
                    "mode=unescape 则反向。用于把一段文本塞进别的语法里。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "kind": {"type": "string"},
                                                     "mode": {"type": "string"}},
                    "required": ["text"]}
        def execute(self, args):
            text = str(args.get("text") or "")
            kind = str(args.get("kind") or "json").lower()
            un = str(args.get("mode") or "escape").lower().startswith("un")
            try:
                if kind == "json":
                    return ToolResult.ok(json.dumps(text, ensure_ascii=False)[1:-1] if not un
                                         else json.loads('"' + text + '"'))
                if kind == "url":
                    return ToolResult.ok(urllib.parse.unquote(text) if un
                                         else urllib.parse.quote(text, safe=""))
                if kind == "html":
                    import html
                    return ToolResult.ok(html.unescape(text) if un else html.escape(text))
                if kind == "regex":
                    return ToolResult.ok(re.escape(text) if not un
                                         else text.replace("\\", ""))
                if kind == "shell_ps":
                    return ToolResult.ok(text.replace("'", "''") if not un
                                         else text.replace("''", "'"))
                return ToolResult.fail("kind 只能是 json / url / html / regex / shell_ps")
            except Exception as e:                          # noqa: BLE001
                return ToolResult.fail(f"转义失败：{type(e).__name__}: {e}")

    @tool
    class StringUtilsTool(ToolPlugin):
        """字符串统计与变换。"""
        @property
        def id(self): return "tool.text.string_utils"
        @property
        def name(self): return "string_utils"
        @property
        def description(self):
            return ("对一段文本做统计或变换。op：stats（默认）/ upper / lower / trim / "
                    "snake / camel / kebab / reverse / unique_lines / sort_lines。\n"
                    "stats 给字符数、词数、行数、最长行。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "op": {"type": "string"}},
                    "required": ["text"]}
        def execute(self, args):
            t = str(args.get("text") or "")
            op = str(args.get("op") or "stats").lower()
            words = re.findall(r"\S+", t)
            lines = t.splitlines()
            if op == "stats":
                longest = max(lines, key=len) if lines else ""
                return ToolResult.ok(
                    f"字符 {len(t)} · 词 {len(words)} · 行 {len(lines)} · "
                    f"最长行 {len(longest)} 字符")
            if op == "upper":   return ToolResult.ok(t.upper())
            if op == "lower":   return ToolResult.ok(t.lower())
            if op == "trim":    return ToolResult.ok(t.strip())
            if op == "reverse": return ToolResult.ok(t[::-1])
            if op == "snake":
                return ToolResult.ok(re.sub(r"(?<!^)(?=[A-Z])", "_", t).replace("-", "_").lower())
            if op == "kebab":
                return ToolResult.ok(re.sub(r"(?<!^)(?=[A-Z])", "-", t).replace("_", "-").lower())
            if op == "camel":
                parts = re.split(r"[_\-\s]+", t)
                return ToolResult.ok(parts[0].lower() + "".join(p.title() for p in parts[1:]))
            if op == "unique_lines":
                seen, out2 = set(), []
                for ln in lines:
                    if ln not in seen:
                        seen.add(ln)
                        out2.append(ln)
                return ToolResult.ok("\n".join(out2))
            if op == "sort_lines":
                return ToolResult.ok("\n".join(sorted(lines)))
            return ToolResult.fail("op 不支持：" + op)

    @tool
    class RegexTestTool(ToolPlugin):
        """正则测试（真跑，给匹配位置）。"""
        @property
        def id(self): return "tool.text.regex"
        @property
        def name(self): return "regex_test"
        @property
        def description(self):
            return ("用 pattern 在 text 上跑正则，返回**所有匹配**（含分组与位置）。\n"
                    "flags 可给 i / m / s。写正则前先在这里验证，比在代码里试快。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"pattern": {"type": "string"},
                                                     "text": {"type": "string"},
                                                     "flags": {"type": "string"}},
                    "required": ["pattern", "text"]}
        def execute(self, args):
            pat = str(args.get("pattern") or "")
            if not pat:
                return ToolResult.fail("缺少 pattern")
            f = 0
            for ch in str(args.get("flags") or ""):
                f |= {"i": re.I, "m": re.M, "s": re.S}.get(ch, 0)
            try:
                rx = re.compile(pat, f)
            except re.error as e:
                return ToolResult.fail(f"正则非法：{e}")
            ms = list(rx.finditer(str(args.get("text") or "")))
            if not ms:
                return ToolResult.ok("没有匹配（0 处）")
            rows = [f"共 {len(ms)} 处："]
            for i, mo in enumerate(ms[:100], 1):
                g = mo.groups()
                rows.append(f"  {i}. [{mo.start()}:{mo.end()}] {mo.group(0)!r}"
                            + (f"  分组={g}" if g else ""))
            if len(ms) > 100:
                rows.append(f"  …（还有 {len(ms) - 100} 处未列）")
            return ToolResult.ok("\n".join(rows))

    @tool
    class NumberConvertTool(ToolPlugin):
        """进制转换。"""
        @property
        def id(self): return "tool.text.number"
        @property
        def name(self): return "number_convert"
        @property
        def description(self):
            return ("进制转换：给 value 与 from_base（默认 10）、to_base（默认 16）。\n"
                    "也支持 to_base=bin/oct/hex/dec 这种写法。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"value": {"type": "string"},
                                                     "from_base": {}, "to_base": {}},
                    "required": ["value"]}
        def execute(self, args):
            names = {"bin": 2, "oct": 8, "dec": 10, "hex": 16}
            # 【from_base/to_base 的 int() 必须在 try 里】fb="0x16" 这种 names 表之外的
            # 字符串在**取值那一步**就抛 ValueError，原来它在 try 之外 → 整次调用变成
            # "工具执行异常"，而本该走下面"按 N 进制解析失败"的可读报错分支。
            try:
                fb = args.get("from_base") or 10
                tb = args.get("to_base") or 16
                if isinstance(fb, str):
                    fb = names.get(fb.lower(), None) or int(fb)
                if isinstance(tb, str):
                    tb = names.get(tb.lower(), None) or int(tb)
                fb, tb = int(fb), int(tb)
            except (TypeError, ValueError):
                return ToolResult.fail(
                    "from_base/to_base 必须是 2-36 的数字，或 bin/oct/dec/hex（你给的: "
                    f"from_base={args.get('from_base')!r}, to_base={args.get('to_base')!r}）")
            if not (2 <= fb <= 36):
                return ToolResult.fail(f"from_base 只能是 2~36（你给的是 {fb}）")
            raw = str(args.get("value") or "").strip().replace("_", "")
            try:
                n = int(raw, fb)
            except ValueError as e:
                return ToolResult.fail(f"按 {fb} 进制解析失败：{e}")
            if not (2 <= tb <= 36):
                return ToolResult.fail("to_base 只能是 2~36")
            builtin = {2: format(n, "b"), 8: format(n, "o"), 10: str(n), 16: format(n, "x")}
            shown = builtin.get(tb) or _to_base(n, tb)
            return ToolResult.ok(f"{raw}(base{fb}) = {shown}（base{tb}）")

    def _to_base(n: int, base: int) -> str:
        digits, sign, out2 = "0123456789abcdefghijklmnopqrstuvwxyz", "", ""
        if n < 0:
            sign, n = "-", -n
        while n:
            out2 = digits[n % base] + out2
            n //= base
        return sign + (out2 or "0")

    @tool
    class DiffTextTool(ToolPlugin):
        """比较两段文本/两个文件的差异。"""
        @property
        def id(self): return "tool.text.diff"
        @property
        def name(self): return "diff_text"
        @property
        def description(self):
            return ("比较两段文本或两个文件的差异（统一 diff 格式）。\n"
                    "给 a/b 两个路径，或 a_text/b_text 两段字符串。\n"
                    "只看文件有没有变用 git_status；要看具体改了哪几行用这个。")
        @property
        def category(self): return CAT_FILE
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"a": {"type": "string"}, "b": {"type": "string"},
                                   "a_text": {"type": "string"}, "b_text": {"type": "string"}},
                    "required": []}
        def execute(self, args):
            def side(path_key, text_key):
                if args.get(path_key):
                    p = self.resolve_path(str(args[path_key]))
                    if not p.is_file():
                        return None, f"不是文件：{p}"
                    return p.read_text(encoding="utf-8", errors="replace").splitlines(), None
                if args.get(text_key) is not None:
                    return str(args[text_key]).splitlines(), None
                return None, f"缺少 {path_key} 或 {text_key}"
            la, err = side("a", "a_text")
            if err:
                return ToolResult.fail(err)
            lb, err = side("b", "b_text")
            if err:
                return ToolResult.fail(err)
            d = list(difflib.unified_diff(la, lb, "a", "b", lineterm="", n=2))
            return ToolResult.ok("\n".join(d) if d else "两段内容完全一致（无差异）")

    @tool
    class JsonFormatTool(ToolPlugin):
        """JSON 校验 / 美化 / 压缩 / 取值。"""
        @property
        def id(self): return "tool.data.json"
        @property
        def name(self): return "json_format"
        @property
        def description(self):
            return ("JSON 工具。给 text 或 path。op：format（默认，美化 2 空格）/ minify / "
                    "validate / keys（列顶层键）。\n"
                    "解析失败会**指出具体位置**，不是只说一句'非法'。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "path": {"type": "string"},
                                                     "op": {"type": "string"}},
                    "required": []}
        def execute(self, args):
            if args.get("path"):
                p = self.resolve_path(str(args["path"]))
                if not p.is_file():
                    return ToolResult.fail(f"不是文件：{p}")
                raw = p.read_text(encoding="utf-8", errors="replace")
            elif args.get("text") is not None:
                raw = str(args["text"])
            else:
                return ToolResult.fail("至少给 text 或 path")
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as e:
                lines = raw.splitlines()
                bad = lines[e.lineno - 1] if 0 < e.lineno <= len(lines) else ""
                return ToolResult.fail(
                    f"JSON 非法：第 {e.lineno} 行第 {e.colno} 列 —— {e.msg}\n    {bad.strip()[:120]}")
            op = str(args.get("op") or "format").lower()
            if op == "validate":
                return ToolResult.ok(f"合法 JSON：顶层是 {type(obj).__name__}，"
                                     f"{len(obj)} 个成员" if isinstance(obj, (dict, list))
                                     else f"合法 JSON：{type(obj).__name__}")
            if op == "minify":
                return ToolResult.ok(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))
            if op == "keys":
                if not isinstance(obj, dict):
                    return ToolResult.ok(f"顶层不是对象，是 {type(obj).__name__}")
                return ToolResult.ok("\n".join(f"{k}: {type(v).__name__}" for k, v in obj.items()))
            return ToolResult.ok(_truncate_b2(json.dumps(obj, ensure_ascii=False, indent=2)))

    @tool
    class YamlProcessTool(ToolPlugin):
        """YAML 校验（有 PyYAML 就完整解析，没有就做缩进/制表符等结构检查）。"""
        @property
        def id(self): return "tool.data.yaml"
        @property
        def name(self): return "yaml_process"
        @property
        def description(self):
            return ("校验 YAML 文档。**没有 PyYAML 时会如实说明只做了结构检查**，"
                    "不会假装解析过。\n给 text 或 path。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "path": {"type": "string"}},
                    "required": []}
        def execute(self, args):
            if args.get("path"):
                p = self.resolve_path(str(args["path"]))
                if not p.is_file():
                    return ToolResult.fail(f"不是文件：{p}")
                raw = p.read_text(encoding="utf-8", errors="replace")
            elif args.get("text") is not None:
                raw = str(args["text"])
            else:
                return ToolResult.fail("至少给 text 或 path")
            try:
                import yaml                                    # type: ignore
                obj = yaml.safe_load(raw)
                return ToolResult.ok(f"PyYAML 解析成功：顶层 {type(obj).__name__}"
                                     + (f"，{len(obj)} 个键" if isinstance(obj, dict) else ""))
            except ImportError:
                problems = []
                for i, ln in enumerate(raw.splitlines(), 1):
                    if "\t" in ln:
                        problems.append(f"第 {i} 行含制表符（YAML 不允许缩进用 tab）")
                    if ln.rstrip() != ln and ln.strip() and not ln.lstrip().startswith("#"):
                        problems.append(f"第 {i} 行有多余行尾空格")
                return ToolResult.ok(
                    "本机没装 PyYAML —— **只做了结构检查**（不代表已完整校验）：\n"
                    + ("\n".join(problems[:20]) if problems else "未发现 tab 缩进/行尾空格问题"))
            except Exception as e:                              # noqa: BLE001
                return ToolResult.fail(f"YAML 非法：{type(e).__name__}: {e}")

    @tool
    class CronParseTool(ToolPlugin):
        """解析 cron 表达式，说明它什么时候跑。"""
        @property
        def id(self): return "tool.data.cron"
        @property
        def name(self): return "cron_parse"
        @property
        def description(self):
            return ("解析 5 段 cron 表达式（分 时 日 月 周），逐段说明含义。\n"
                    "**只做解释，不预测下次执行时间**（那要完整调度器，这里不假装）。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"expression": {"type": "string"}},
                    "required": ["expression"]}
        def execute(self, args):
            expr = str(args.get("expression") or "").strip()
            parts = expr.split()
            if len(parts) != 5:
                return ToolResult.fail(f"需要 5 段（分 时 日 月 周），你给了 {len(parts)} 段：{expr!r}")
            names = ("分钟", "小时", "日", "月", "星期")
            special = {"*": "每一", "*/": "每隔 ", "-": "范围", ",": "多个",
                       "?": "不指定"}
            rows = [f"表达式 {expr}："]
            for n, seg in zip(names, parts):
                hint = next((v for k, v in special.items() if seg.startswith(k)), "")
                rows.append(f"  {n}：{seg}" + (f"（{hint}）" if hint else ""))
            return ToolResult.ok("\n".join(rows))

    @tool
    class FormatCodeTool(ToolPlugin):
        """格式化代码/JSON（**只支持能确定做对的格式**）。"""
        @property
        def id(self): return "tool.text.format"
        @property
        def name(self): return "format_code"
        @property
        def description(self):
            return ("格式化。**目前只支持 json**（用标准库，结果一定对）。\n"
                    "其它语言本机没有可靠的格式化器 —— 会**如实拒绝**，"
                    "而不是随便缩进了事（那会改坏代码）。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "path": {"type": "string"},
                                                     "language": {"type": "string"}},
                    "required": []}
        def execute(self, args):
            # 【恒等三元 + None.endswith 都修掉】原来两支都是 "json"（条件纯属死代码），
            # 而且 args.get("path", "") 在键**存在但值是 null** 时返回 None
            # （默认值只在键缺失时生效）→ None.endswith 抛 AttributeError。
            path = args.get("path")
            if not args.get("language") and isinstance(path, str) and path.lower().endswith(".json"):
                lang = "json"
            else:
                lang = str(args.get("language") or "json").lower()
            if lang not in ("json", "jsonc"):
                return ToolResult.fail(
                    f"format_code 目前只支持 json（你给的是 {lang}）——\n"
                    "其它语言本机没有可靠的格式化器，硬做会改坏代码，所以选择如实拒绝。\n"
                    "如果确实需要，可以先装对应工具再让我用 execute_command 调用它。")
            # 【不要在这里 new 一个别的工具类】`JsonFormatTool(self)` 是错的 ——
            # 那些类要的是 NS（含 ToolPlugin/ToolResult/…），传 self 会在运行时炸。
            # 所以把 JSON 美化的逻辑就地写一遍（就三行）。
            if args.get("path"):
                p = self.resolve_path(str(args["path"]))
                if not p.is_file():
                    return ToolResult.fail(f"不是文件：{p}")
                raw = p.read_text(encoding="utf-8", errors="replace")
            elif args.get("text") is not None:
                raw = str(args["text"])
            else:
                return ToolResult.fail("至少给 text 或 path")
            try:
                obj = json.loads(raw)
            except json.JSONDecodeError as e:
                return ToolResult.fail(f"JSON 非法：第 {e.lineno} 行第 {e.colno} 列 —— {e.msg}")
            return ToolResult.ok(_truncate_b2(json.dumps(obj, ensure_ascii=False, indent=2)))

    @tool
    class MarkdownRenderTool(ToolPlugin):
        """把 Markdown 渲染成纯文本（去标记）。"""
        @property
        def id(self): return "tool.text.markdown"
        @property
        def name(self): return "markdown_render"
        @property
        def description(self):
            return ("把 Markdown 转成**纯文本**（去 #、*、链接语法等），用于终端阅读。\n"
                    "**不是** HTML 渲染器（本机没有渲染依赖，不假装）。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "path": {"type": "string"}},
                    "required": []}
        def execute(self, args):
            if args.get("path"):
                p = self.resolve_path(str(args["path"]))
                if not p.is_file():
                    return ToolResult.fail(f"不是文件：{p}")
                raw = p.read_text(encoding="utf-8", errors="replace")
            elif args.get("text") is not None:
                raw = str(args["text"])
            else:
                return ToolResult.fail("至少给 text 或 path")
            t = raw
            t = re.sub(r"```.*?```", lambda m: re.sub(r"^```\w*\n?", "", m.group(0)).rstrip("`"),
                       t, flags=re.S)
            t = re.sub(r"`([^`]+)`", r"\1", t)
            t = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"[图: \1]", t)
            t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1 (\2)", t)
            t = re.sub(r"^\s{0,3}#{1,6}\s*", "", t, flags=re.M)
            t = re.sub(r"(\*\*|__)(.*?)\1", r"\2", t)
            t = re.sub(r"(\*|_)(.*?)\1", r"\2", t)
            t = re.sub(r"^\s*[-*+]\s+", "· ", t, flags=re.M)
            return ToolResult.ok(_truncate_b2(t.strip()))

    @tool
    class TranslateTool(ToolPlugin):
        """翻译（需要联网服务；不可达时如实说明）。"""
        @property
        def id(self): return "tool.text.translate"
        @property
        def name(self): return "translate"
        @property
        def description(self):
            return ("翻译文本。**本机 HTTPS 对多数外部站点不通** —— 连不上会如实报错，"
                    "不会把原文当译文返回。\n可选 endpoint 指定自建翻译服务"
                    "（应接受 POST JSON {text,to} 并返回 {text}）。")
        @property
        def category(self): return CAT_NET
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"text": {"type": "string"},
                                                     "to": {"type": "string"},
                                                     "endpoint": {"type": "string"}},
                    "required": ["text"]}
        def execute(self, args):
            text = str(args.get("text") or "")
            if not text:
                return ToolResult.fail("缺少 text 参数")
            endpoint = str(args.get("endpoint") or "").strip()
            if not endpoint:
                return ToolResult.fail(
                    "translate 需要一个可用的翻译服务 endpoint ——\n"
                    "本机 HTTPS 对外基本不通（实测连 github 都是 Connection reset），"
                    "所以没有内置默认服务。\n"
                    "用法：translate(text=..., to=\"zh\", endpoint=\"http://<你的服务>/translate\")，"
                    "该服务应接受 POST JSON {text, to} 并返回 {text: \"译文\"}。")
            ok, out = _http(endpoint, data=json.dumps({"text": text, "to": args.get("to") or "zh"}
                                                      ).encode("utf-8"),
                            headers={"Content-Type": "application/json"})
            if not ok:
                return ToolResult.fail(f"翻译服务不可达：{out}")
            try:
                return ToolResult.ok(str(json.loads(out).get("text") or out))
            except Exception:                               # noqa: BLE001
                return ToolResult.ok(out)

    # ───────────────────────── 进程类（2） ─────────────────────────
    @tool
    class RunBackgroundTool(ToolPlugin):
        """后台跑长驻进程。"""
        @property
        def id(self): return "tool.shell.background"
        @property
        def name(self): return "run_background"
        @property
        def description(self):
            return ("把长驻进程（服务器、watch、npm run dev）放后台跑，立刻返回 PID。\n"
                    "输出落到 `.lbcheck/bg-<pid>.log`，之后可以用 read_file 看。\n"
                    "**不要在 execute_command 里等长驻进程**（会超时被杀）。")
        @property
        def category(self): return CAT_SHELL
        @property
        def permission(self): return LV_EXEC
        def parameters_schema(self):
            return {"type": "object", "properties": {"command": {"type": "string"},
                                                     "cwd": {"type": "string"}},
                    "required": ["command"]}
        def execute(self, args):
            cmd = str(args.get("command") or "").strip()
            if not cmd:
                return ToolResult.fail("缺少 command 参数")
            cwd = str(self.resolve_path(args.get("cwd") or "."))
            logdir = Path(cwd) / ".lbcheck"
            try:
                logdir.mkdir(parents=True, exist_ok=True)
            except OSError:
                logdir = Path(cwd)
            # 【工具说明承诺了日志文件，就必须真的落盘】原来 stdout/stderr 接 DEVNULL：
            # `.lbcheck/bg-<pid>.log` 从没被创建过，模型按说明去 read_file 必然"文件不存在"，
            # 进程起挂了也没有任何日志可查。文件名要 pid → 只能先把进程起来再开日志，
            # stdout/stderr 合并成一条管道（stderr=STDOUT），由一个守护线程边读边写。
            try:
                if os.name == "nt":
                    # 【别再带 DETACHED_PROCESS(0x8)】实测：powershell 带 0x8 时
                    # stdout 永远不往管道里写（进程活着、日志一直空），带它是因为以前
                    # 输出接 DEVNULL 根本没人看。现在日志要落盘，只留 CREATE_NO_WINDOW
                    # （0x08000000，GUI 不弹黑框）—— 实测这样输出立刻流进管道。
                    p = subprocess.Popen(["powershell", "-NoProfile", "-Command", cmd],
                                         cwd=cwd, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT,
                                         creationflags=0x08000000)
                else:
                    p = subprocess.Popen(["sh", "-c", cmd], cwd=cwd,
                                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            except Exception as e:                          # noqa: BLE001
                return ToolResult.fail(f"起不来：{type(e).__name__}: {e}")

            log_path = logdir / f"bg-{p.pid}.log"
            log_note = ""
            fh = None
            try:
                fh = open(log_path, "wb")
            except OSError as e:
                # 日志建不了也**必须照样把管道读干**：没人读的话输出一多，
                # 子进程会卡死在 write 上（"后台任务永远不结束"那个坑）。
                log_note = f"\n（日志文件创建失败：{type(e).__name__}: {e}，输出会被丢弃）"

            def _pump() -> None:
                try:
                    # 必须用 read1（有就用）：BufferedReader.read(n) 会**凑满 n 字节**才返回，
                    # 输出不满 64KB 时管道没人读 → 子进程卡在 write 上。
                    reader = getattr(p.stdout, "read1", p.stdout.read)
                    while True:
                        chunk = reader(65536)
                        if not chunk:
                            break
                        if fh is not None:
                            fh.write(chunk)
                            # 【必须立刻 flush】文件对象默认带 8KB 缓冲，不 flush 的话
                            # "边跑边 read_file 看日志"永远读到空文件（进程还没退出，
                            # finally 里的 close 还没发生）——工具的承诺就落空了。
                            fh.flush()
                except Exception:                          # noqa: BLE001
                    pass
                finally:
                    try:
                        p.stdout.close()
                    except Exception:                      # noqa: BLE001
                        pass
                    if fh is not None:
                        try:
                            fh.close()
                        except Exception:                  # noqa: BLE001
                            pass

            threading.Thread(target=_pump, name="lionbox-bg-log", daemon=True).start()

            _BG[p.pid] = {"cmd": cmd, "cwd": cwd, "proc": p}
            return ToolResult.ok(
                f"已在后台启动，PID {p.pid}\n命令：{cmd}\n工作目录：{cwd}\n"
                f"输出日志：{log_path}{log_note}\n"
                f"（要停它用 stop_background(pid={p.pid})）")

    @tool
    class StopBackgroundTool(ToolPlugin):
        """停掉后台进程。"""
        @property
        def id(self): return "tool.shell.bgstop"
        @property
        def name(self): return "stop_background"
        @property
        def description(self):
            return ("停掉 run_background 起的进程。pid 省略则停**本会话起的全部**。\n"
                    "只停自己起的（不会去杀别人/系统的进程）。")
        @property
        def category(self): return CAT_SHELL
        @property
        def permission(self): return LV_EXEC
        def parameters_schema(self):
            return {"type": "object", "properties": {"pid": {"type": "number"}}, "required": []}
        def execute(self, args):
            pid = args.get("pid")
            if pid not in (None, "", False):
                try:
                    targets = [int(pid)]
                except (TypeError, ValueError):
                    # pid 乱值（"abc"）原来直接抛 ValueError → "工具执行异常"，
                    # 这里如实说清楚：一个进程也没停
                    return ToolResult.fail(f"pid 必须是数字（你给的是 {pid!r}）—— 没有停任何进程")
            else:
                targets = list(_BG.keys())
            if not targets:
                return ToolResult.ok("没有本会话起的后台进程")
            rows = []
            for tp in targets:
                rec = _BG.get(tp)
                if not rec:
                    rows.append(f"PID {tp}：不是本会话起的，**不动它**")
                    continue
                rows.append(_stop_one(tp, rec))
                _BG.pop(tp, None)
            return ToolResult.ok("\n".join(rows))

    # ───────────────────────── 杂项（4） ─────────────────────────
    @tool
    class GetEnvTool(ToolPlugin):
        """读环境变量 / 看关键路径。"""
        @property
        def id(self): return "tool.sys.env"
        @property
        def name(self): return "get_env"
        @property
        def description(self):
            return ("不带 name：列出关键环境变量与系统路径（cwd、临时目录、PATH 条目数等）。\n"
                    "带 name：返回该变量的值（不存在会明确说'未设置'）。\n"
                    "**不会打印含 KEY/TOKEN/SECRET/PASSWORD 的值**（只显示已设置与否）。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {"name": {"type": "string"}}, "required": []}
        def execute(self, args):
            name = str(args.get("name") or "").strip()
            secret = re.search(r"KEY|TOKEN|SECRET|PASSWORD|PASSWD|CREDENTIAL", name, re.I)
            if name:
                if name not in os.environ:
                    return ToolResult.fail(f"环境变量未设置：{name}")
                if secret:
                    return ToolResult.ok(f"{name} 已设置（值疑似敏感，共 {len(os.environ[name])} 字符，不显示）")
                return ToolResult.ok(f"{name} = {os.environ[name]}")
            rows = [f"cwd            = {os.getcwd()}",
                    f"OS             = {sys.platform} ({os.name})",
                    f"Python         = {sys.version.split()[0]}",
                    f"TEMP           = {os.environ.get('TEMP', '(未设置)')}",
                    f"PATH 条目数    = {len(os.environ.get('PATH', '').split(os.pathsep))}",
                    f"环境变量总数   = {len(os.environ)}"]
            interesting = [k for k in os.environ
                           if re.match(r"^(MIMOCODE|LION|LIONBOX|PYTHON|NODE|BUN|GIT)", k, re.I)]
            if interesting:
                rows.append("相关变量：" + ", ".join(sorted(interesting)[:20]))
            return ToolResult.ok("\n".join(rows))

    @tool
    class ContextPruneTool(ToolPlugin):
        """看当前上下文占用（**给出建议，不擅自删历史**）。"""
        @property
        def id(self): return "tool.context.prune"
        @property
        def name(self): return "context_prune"
        @property
        def description(self):
            return ("查看当前会话的上下文占用与预算，并给出建议。\n"
                    "**不会自己删历史** —— 真正压缩由 AgentLoop/后端在做"
                    "（这里只报告，避免模型自作主张丢上下文）。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {}, "required": []}
        def execute(self, args):
            rows = ["上下文压缩由后端/AgentLoop 统一处理；这里是只读报告："]
            try:
                b = NS.get("api")
                snap = b.budget().snapshot("") if b and hasattr(b, "budget") else None
                if snap:
                    rows.append(f"预算快照：{snap}")
            except Exception as e:                          # noqa: BLE001
                rows.append(f"（拿不到预算快照：{type(e).__name__}）")
            rows.append("建议：单个工具输出过大时，用 head_tail_file / search_in_files "
                        "缩小读入量，而不是反复整文件读。")
            return ToolResult.ok("\n".join(rows))

    @tool
    class AskUserTool(ToolPlugin):
        """向用户提问（**循环级**：由 AgentLoop 负责真的呈现问题）。"""
        @property
        def id(self): return "tool.ux.ask"
        @property
        def name(self): return "ask_user"
        @property
        def description(self):
            return ("当**缺关键信息且猜不出来**时，向用户提问（而不是瞎猜）。\n"
                    "**注意**：这个工具只把问题交回给上层；真正的提问 UI 由客户端呈现。\n"
                    "只在真的卡住时用 —— 能从代码/文件里查到答案的，先自己查。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object",
                    "properties": {"question": {"type": "string"},
                                   "options": {"type": "array", "items": {"type": "string"}}},
                    "required": ["question"]}
        def execute(self, args):
            # 【不许谎报"已把问题交给用户"】这个实现原来只是把问题原样回一句
            # "已把问题交给用户：…（等待用户回答）"，却**没有任何呈现/接线调用** ——
            # 问题根本没到用户眼前，模型却在原地等一个永远不会来的回答（对话空转）。
            # 改成走本模块真正接线过的那个 ask_user（走 QUESTION_SERVICE，本文件
            # `set_question_service` 挂的那个）：没接线它会如实报错，接线了就真的阻塞
            # 等用户回答 —— 无论哪种，返回文案都是**实际发生的事**。
            real = globals().get("AskUserTool")
            if not isinstance(real, type):
                return ToolResult.fail(
                    "ask_user 没有可用的提问实现 —— 问题**没有**呈现给用户，"
                    "不要假定用户已收到；换个方式继续或让用户手动输入。")
            return real.execute(self, args)

    @tool
    class ChangePermissionsTool(ToolPlugin):
        """查看/申请权限（**不能自己提权**）。"""
        @property
        def id(self): return "tool.sec.perms"
        @property
        def name(self): return "change_permissions"
        @property
        def description(self):
            return ("查看当前权限策略（只读）。\n"
                    "**工具不能给自己提权** —— 权限变更必须由用户在设置里做，"
                    "所以这里只报告，不会修改任何策略。")
        @property
        def category(self): return CAT_OTHER
        @property
        def permission(self): return LV_READ
        def parameters_schema(self):
            return {"type": "object", "properties": {}, "required": []}
        def execute(self, args):
            rows = ["权限变更必须由用户在设置里完成；工具侧只读报告："]
            try:
                cfg = NS.get("api")
                if cfg and hasattr(cfg, "cfg"):
                    mode = cfg.cfg.get("toolCallMode", "?")
                    rows.append(f"当前 toolCallMode = {mode}")
            except Exception as e:                          # noqa: BLE001
                rows.append(f"（读配置失败：{type(e).__name__}）")
            rows.append("如果某操作被权限层拒绝：请让用户在设置里放行，或改用不需要该权限的做法。")
            return ToolResult.ok("\n".join(rows))
    # ── 权限等级覆盖（本次修正）──────────────────────────────────────────

    # 【为什么需要】核查发现 20 个工具没声明 permission（属性是 None，不是基类

    # 默认值），而权限门禁判的是 `required == PermissionLevel.READ_ONLY` ——

    # None 不成立，于是在**只读工作区**里连 base64/hash/json_format 这类纯计算

    # 都被拦；git_status/diff/log/branch 又错标成 EXECUTE。这里按名字统一纠正，

    # 一处收口、便于复查（不改各工具类本身，避免散落 24 处）。

    _LEVEL_OVERRIDE = {}

    for _n in ['base64', 'hash', 'generate_uuid', 'escape_string', 'string_utils', 'regex_test', 'number_convert', 'diff_text', 'json_format', 'yaml_process', 'cron_parse', 'format_code', 'markdown_render', 'translate', 'dns_lookup', 'get_env', 'http_get', 'ask_user', 'working_directory', 'context_window', 'system_info', 'timestamp', 'git_status', 'git_diff', 'git_log', 'git_branch']:

        _LEVEL_OVERRIDE[_n] = PermissionLevel.READ_ONLY

    for _n in ['git_add', 'git_commit', 'git_stash', 'git_init', 'git_remote', 'context_prune']:

        _LEVEL_OVERRIDE[_n] = PermissionLevel.WRITE

    for _n in ['delete_file', 'move_file', 'change_permissions', 'git_reset']:

        _LEVEL_OVERRIDE[_n] = PermissionLevel.DANGEROUS

    for _c in out:

        # 同 _build_batch1 里那段：类上的 name 是 @property，getattr 拿到的是 property
        # 对象，拿它查表永远不命中（死代码）。按 fget 求值取真名，见 _tool_class_name。
        _lv = _LEVEL_OVERRIDE.get(_tool_class_name(_c))

        if _lv is not None:

            _c.permission = property(lambda self, _v=_lv: _v)

    return out

#: run_background 起的进程表（进程内有效；stop 只动这里面的）
_BG: dict = {}


def _stop_one(tp, rec: dict) -> str:
    """停掉一个后台进程，返回如实的一行结果。

    【为什么不能只 `proc.terminate()`】run_background 起的是 powershell，命令里的
    node/npm/服务器全是它的**孙进程**：只杀直接子进程，孙进程在 Windows 上全部存活，
    却回报"已终止"（模型据此认为任务停了，实际还在占端口/占 CPU）。对照本文件
    HeadlessBrowser._kill_tree 的做法：`taskkill /F /T /PID`（/T = 连进程树一起杀）。
    """
    proc = rec["proc"]
    try:
        if os.name == "nt":
            subprocess.run(["taskkill", "/F", "/T", "/PID", str(tp)],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                           timeout=15, creationflags=NO_WINDOW)
        else:
            proc.terminate()
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        return f"PID {tp}：发了终止信号但 5 秒内还没退出，**可能还活着**（{rec['cmd'][:60]}）"
    except Exception as e:                                  # noqa: BLE001
        return f"PID {tp}：终止失败 {type(e).__name__}: {e}"
    return f"PID {tp}：已终止（连子进程；{rec['cmd'][:60]}）"


# ============================================================================
# 【统一入口】三批工具一次性产出
#
# main.py 的 build_registry 只需要这一处调用 ✓（原来要 import 两个模块、跑两个循环 ✗）
# NS 由调用方传入 main.py 的 globals() ✓ —— 沿用原约定：**不从 main 反向 import** ✗
# （那会循环导入 ✓）
# ============================================================================
def build_tools(NS: dict) -> list:
    """产出本文件里全部工具类（原有 + 第一批 + 第二批）。

    :param NS: 需含 ToolPlugin / ToolResult / PermissionLevel / ToolCategory
    """
    out: list = []
    for _builder in (_build_batch1, _build_batch2):
        got = _builder(NS)
        if isinstance(got, list):
            out.extend(got)
    return out
