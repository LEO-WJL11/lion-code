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
from __future__ import annotations

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
DEFAULT_TIMEOUT = 60

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


def build_tools(NS: dict) -> list:
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
                "- 本机是 **Windows + PowerShell**：没有 `which`（用 `where 名字`）、"
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
                timeout = float(args.get("timeout") or DEFAULT_TIMEOUT)
            except (TypeError, ValueError):
                timeout = DEFAULT_TIMEOUT
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
            try:
                p = subprocess.run(argv, capture_output=True, cwd=cwd,
                                   timeout=timeout, shell=False)
            except subprocess.TimeoutExpired:
                return ToolResult.fail(
                    f"命令超时（{timeout:.0f}s）已被终止：{cmd}\n"
                    "（要跑长时间任务请用 run_background）")
            except FileNotFoundError as e:
                return ToolResult.fail("找不到解释器: " + str(e))
            except OSError as e:
                return ToolResult.fail("启动失败: " + type(e).__name__ + ": " + str(e))
            dt = __import__("time").time() - t0

            def dec(b):
                for enc in ("utf-8", "gbk", "mbcs" if os.name == "nt" else "utf-8"):
                    try:
                        return b.decode(enc)
                    except (UnicodeDecodeError, LookupError):
                        continue
                return b.decode("utf-8", "replace")

            stdout = dec(p.stdout or b"")
            stderr = dec(p.stderr or b"")
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
                h = hashlib.sha256(p.read_bytes()[:2_000_000]).hexdigest()[:16]
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
            if want is None and n > 1:
                return ToolResult.fail(
                    f"old 在文件里出现了 {n} 处，无法确定要改哪一处 —— 没有做任何修改。\n"
                    "请把 old 给长一点（带上前后几行或独特上下文），或用 count 指定处数。")
            replaced = text.replace(old, new, want if want else -1)
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
            # 用后端已有的预算设施（拿不到就如实说，别编数字）
            try:
                import 沙箱  # noqa: F401
            except Exception:                              # noqa: BLE001
                pass
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

    return out


def register_extra(reg, NS: dict) -> int:
    """把本模块的工具注册进 reg（同名会覆盖桩实现）。返回注册个数。"""
    ws = getattr(reg, "workspace", None)
    n = 0
    for cls in build_tools(NS):
        try:
            reg.register(cls(ws) if ws is not None else cls(Path.cwd()))
            n += 1
        except Exception:                                  # noqa: BLE001
            continue
    return n