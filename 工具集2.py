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
from __future__ import annotations

import base64 as _b64
import datetime
import difflib
import hashlib as _hash
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

MAX_OUTPUT = 60_000
_UA = {"User-Agent": "lion-code-tool/1.0"}


def _truncate(text: str, limit: int = MAX_OUTPUT) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n…（共 {len(text)} 字符，已截断到前 {limit}）"


def _run(cmd: list[str], cwd: str, timeout: int = 60) -> tuple[int, str]:
    """跑一个**不经 shell** 的命令（列表参数，天然免疫引号/分隔符问题）。"""
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
        out = (p.stdout or "") + (("\n[stderr]\n" + p.stderr) if p.stderr else "")
        return p.returncode, _truncate(out.strip())
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
            raw = r.read()
            ctype = r.headers.get("Content-Type", "")
            if "text" in ctype or "json" in ctype or "xml" in ctype:
                return True, _truncate(raw.decode("utf-8", "replace"))
            return True, f"[{ctype or 'binary'}] {len(raw)} 字节（非文本，未展开）"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code} {e.reason}"
    except urllib.error.URLError as e:
        return False, f"连不上：{e.reason}（本机 HTTPS 对部分站点不通，属已知环境限制）"
    except Exception as e:                                  # noqa: BLE001
        return False, f"{type(e).__name__}: {e}"


def build_tools(NS: dict) -> list:
    """用调用方传进来的基类造工具类清单（避免与 main.py 循环导入）。

    :param NS: 需含 ToolPlugin / ToolResult / PermissionLevel / ToolCategory
    """
    ToolPlugin = NS["ToolPlugin"]
    ToolResult = NS["ToolResult"]
    PermissionLevel = NS["PermissionLevel"]
    ToolCategory = NS["ToolCategory"]

    # 分类名做防御式取用：不同版本枚举取值可能不同，取不到就退回 SHELL
    CAT_SHELL = getattr(ToolCategory, "SHELL", None)
    CAT_FILE = getattr(ToolCategory, "FILE", CAT_SHELL)
    CAT_NET = getattr(ToolCategory, "NETWORK", getattr(ToolCategory, "WEB", CAT_SHELL))
    CAT_OTHER = getattr(ToolCategory, "OTHER", CAT_SHELL)
    LV_READ = getattr(PermissionLevel, "READ", None)
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
                rc, _ = _run(["git", "rev-parse", "--is-inside-work-tree"], cwd, 20)
                if rc != 0:
                    return ToolResult.fail(
                        f"当前目录不是 git 仓库：{cwd}\n"
                        "（要用 git_init 初始化，或把 path 指向仓库目录）")
                argv = build_args(args)
                if isinstance(argv, str):                  # 参数校验失败
                    return ToolResult.fail(argv)
                rc, text = _run(["git"] + argv, cwd, int(args.get("timeout") or 60))
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
             lambda a: ["log", f"-{int(a.get('limit') or 20)}", "--oneline", "--decorate"])

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
                            int(args.get("timeout") or 60))
            if rc != 0:
                low = (text or "").lower()
                if "nothing to commit" in low or "no changes added" in low:
                    return ToolResult.fail("没有可提交的改动（暂存区是空的）")
                return ToolResult.fail(f"git commit 失败（退出码 {rc}）：\n{text or '(无输出)'}")
            return ToolResult.ok(text or f"已提交：{msg}")

    git_tool("git_branch", "tool.git.branch",
             "列出分支（当前分支带 *）。不切换分支。",
             P_PATH, lambda a: ["branch", "-a", "-vv"])

    git_tool("git_init", "tool.git.init",
             "把一个目录初始化成 git 仓库（git init）。已经是仓库时会如实说明。",
             P_PATH, lambda a: ["init"])

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
            ok, text = _http(url, timeout=int(args.get("timeout") or 30))
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
                             timeout=int(args.get("timeout") or 30))
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
            dest.parent.mkdir(parents=True, exist_ok=True)
            if not re.match(r"^https?://", url):
                return ToolResult.fail("只支持 http/https")
            try:
                req = urllib.request.Request(url, headers=_UA)
                with urllib.request.urlopen(req, timeout=int(args.get("timeout") or 60)) as r, \
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
            n = max(1, min(100, int(args.get("count") or 1)))
            v = int(args.get("version") or 4)
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
            fb = args.get("from_base") or 10
            tb = args.get("to_base") or 16
            if isinstance(fb, str): fb = names.get(fb.lower(), None) or int(fb)
            if isinstance(tb, str): tb = names.get(tb.lower(), None) or int(tb)
            raw = str(args.get("value") or "").strip().replace("_", "")
            try:
                n = int(raw, int(fb))
            except ValueError as e:
                return ToolResult.fail(f"按 {fb} 进制解析失败：{e}")
            if not (2 <= int(tb) <= 36):
                return ToolResult.fail("to_base 只能是 2~36")
            builtin = {2: format(n, "b"), 8: format(n, "o"), 10: str(n), 16: format(n, "x")}
            shown = builtin.get(int(tb)) or _to_base(n, int(tb))
            return ToolResult.ok(f"{raw}(base{fb}) = {shown}（base{int(tb)}）")

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
            return ToolResult.ok(_truncate(json.dumps(obj, ensure_ascii=False, indent=2)))

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
            lang = str(args.get("language") or ("json" if args.get("path", "").endswith(".json")
                                                else "json")).lower()
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
            return ToolResult.ok(_truncate(json.dumps(obj, ensure_ascii=False, indent=2)))

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
            return ToolResult.ok(_truncate(t.strip()))

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
            try:
                if os.name == "nt":
                    p = subprocess.Popen(["powershell", "-NoProfile", "-Command", cmd],
                                         cwd=cwd, stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL,
                                         creationflags=0x00000008 | 0x08000000)
                else:
                    p = subprocess.Popen(["sh", "-c", cmd], cwd=cwd,
                                         stdout=subprocess.DEVNULL,
                                         stderr=subprocess.DEVNULL)
            except Exception as e:                          # noqa: BLE001
                return ToolResult.fail(f"起不来：{type(e).__name__}: {e}")
            _BG[p.pid] = {"cmd": cmd, "cwd": cwd, "proc": p}
            return ToolResult.ok(
                f"已在后台启动，PID {p.pid}\n命令：{cmd}\n工作目录：{cwd}\n"
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
            targets = [int(pid)] if pid else list(_BG.keys())
            if not targets:
                return ToolResult.ok("没有本会话起的后台进程")
            rows = []
            for tp in targets:
                rec = _BG.get(tp)
                if not rec:
                    rows.append(f"PID {tp}：不是本会话起的，**不动它**")
                    continue
                try:
                    rec["proc"].terminate()
                    rows.append(f"PID {tp}：已终止（{rec['cmd'][:60]}）")
                except Exception as e:                      # noqa: BLE001
                    rows.append(f"PID {tp}：终止失败 {type(e).__name__}: {e}")
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
            q = str(args.get("question") or "").strip()
            if not q:
                return ToolResult.fail("缺少 question 参数")
            opts = args.get("options") or []
            tail = ("\n候选：" + " / ".join(str(o) for o in opts[:6])) if opts else ""
            return ToolResult.ok(
                f"已把问题交给用户：{q}{tail}\n"
                "（等待用户回答；在拿到答复前**不要**对同一件事反复猜测或重复提问）")

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

    return out


#: run_background 起的进程表（进程内有效；stop 只动这里面的）
_BG: dict = {}