#!/usr/bin/env python
# -*- coding: utf-8 -*-
r"""一键把本项目对 MiMo 源码的改动重放到一份新的 MiMo-Code-main 上。

【为什么需要它】
`MiMo-Code-main/` 是**从上游下载的第三方源码**，被 .gitignore 排除在仓库之外 ✗ ——
但我们对它做了 80 处改动（品牌、命令精简、侧栏会话列表、插件、i18n 加固、退出画面、
工作区对话框…）。⇒ **换机器 / 重新下载 MiMo 源码后，这些改动会全部丢失** ✗。
这个脚本把它们一次性打回去 ✓。

【补丁从哪来】`docs/mimo-changes.patch`
由「上游 pristine」与「我们改过的源码」**逐字节对比**生成（不是凭记忆手写锚点 ✗）。
上游 = `github.com/XiaomiMiMo/MiMo-Code` 的 **main 分支**。
⚠️ **别按版本号认源码** ✗：tag `v0.1.15` 的结构是 `packages/opencode`，
而 `packages/cli` 是后来 `chore(repo): rename packages/opencode to packages/cli` 才有的 ✓；
两边 `@mimo-ai/*` 都是 0.1.15 ✓ —— 结构不对就是错的基线 ✓。

【怎么用】
    python _patch_mimo.py                 # 打补丁（幂等：已打过会说"已是最新"）
    python _patch_mimo.py --dry-run       # 只看会改什么，不动文件
    python _patch_mimo.py --root <目录>    # 指定仓库根（默认脚本所在目录；测试用）

【⚠️ 一个阴险的坑（本脚本已处理）】
`git apply` **在 git 仓库之外**会把每个文件都报成 `Skipped patch '...'` ✓
**并且返回 exit 0** ✗ —— 看起来"成功了"，实际一个字节都没改 ✓✓（实测踩到 ✓）。
所以本脚本**先确认目标在 git 仓库里** ✓，否则直接报错退出 ✓；
并且**打完再做一次反向校验** ✓ 确认真的是打上了 ✓ 不信任 exit code ✗。

【设计取舍】
· 整份补丁一次 apply（不逐块切 ✗）—— 实测逐块从 stdin 喂过去会被 Skip ✓
  · 冲突**逐文件报**：解析 git 的 `error: patch failed: <file>:<line>` 输出 ✓
· **幂等**：正向 `--check` 失败 + 反向 `--check` 成功 ⇒ 已打过 ✓
· **冲突不覆盖**：正反向都失败 ⇒ 报冲突并**不动任何文件** ✗（绝不静默覆盖手改内容 ✓）
"""
from __future__ import annotations

import argparse
import io
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PATCH = os.path.join(HERE, "docs", "mimo-changes.patch")
TARGET_REL = "MiMo-Code-main"


def git(args: list[str], cwd: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True,
                          encoding="utf-8", errors="replace")


def patch_files(text: str) -> list[str]:
    """补丁里涉及的文件（去掉 MiMo-Code-main/ 前缀，便于阅读）。"""
    out = []
    for line in text.split("\n"):
        m = re.match(r"diff --git a/(\S+) b/(\S+)", line)
        if m:
            out.append(m.group(2).replace(TARGET_REL + "/", ""))
    return out


def conflicts_from(stderr: str) -> list[str]:
    """从 git apply 的报错里抠出冲突文件（`error: patch failed: <file>:<line>`）。"""
    seen, out = set(), []
    for line in (stderr or "").split("\n"):
        m = re.search(r"patch failed: ([^:]+):\d+", line)
        if m:
            f = m.group(1).replace(TARGET_REL + "/", "")
            if f not in seen:
                seen.add(f)
                out.append(f)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="重放本项目对 MiMo 源码的改动")
    ap.add_argument("--dry-run", action="store_true", help="只报告，不修改文件")
    ap.add_argument("--root", default=HERE, help="仓库根目录（默认脚本所在目录）")
    ap.add_argument("--patch", default=DEFAULT_PATCH, help="补丁文件路径")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    print(f"仓库根 : {root}")
    print(f"补丁   : {os.path.relpath(args.patch, root)}")

    if not os.path.isfile(args.patch):
        print(f"\n✗ 找不到补丁文件：{args.patch}")
        print("  （它应该在仓库里；新克隆的仓库确认 docs/mimo-changes.patch 存在 ✓）")
        return 1
    if not os.path.isdir(os.path.join(root, TARGET_REL)):
        print(f"\n✗ 找不到目标目录：{TARGET_REL}/")
        print(f"  请先把 MiMo 源码下载/解压成 {root}\\{TARGET_REL}\\（目录名要保持一致 ✓）")
        print("  上游：git@github.com:XiaomiMiMo/MiMo-Code.git （main 分支 ✓ 不是 v0.1.15 ✗）")
        return 1
    if git(["--version"], root).returncode != 0:
        print("\n✗ 本机没有 git —— 补丁靠 `git apply` 应用，没有它没法安全地打 ✗")
        print("  装好 git 再跑 ✓（80 处改动别手工逐条改：必漏 ✗）")
        return 1

    # 【必须先确认在 git 仓库里】仓库外 git apply 会全 Skip 且 exit 0 ✗（见文件头）
    inside = git(["rev-parse", "--is-inside-work-tree"], root)
    if inside.returncode != 0 or "true" not in (inside.stdout or ""):
        print("\n✗ 当前目录**不在 git 仓库里** —— 不能这么打 ✗")
        print("  原因：仓库外 `git apply` 会把每个文件都报成 `Skipped patch` 并**返回 0** ✓")
        print("  看起来成功、其实一个字节没改 ✗（实测踩过 ✓）")
        print("  做法：把 MiMo 源码放在本仓库内（保持 MiMo-Code-main/ 这个名字 ✓）再跑 ✓")
        return 1

    # 【路径基准：git 认的是"仓库顶层"，不是我们传的 --root】✗
    # 实测：pristine 放在 <仓库>/.lbcheck/realtest/MiMo-Code-main 时，
    # git 会去改**仓库顶层**的同名路径（那里已经是打过补丁的 ✓）→ 报"已改"、实际没动 ✗✓。
    # 修法：算出 root 相对仓库顶层的偏移，用 `--directory=<偏移>` 告诉 git ✓。
    top = git(["rev-parse", "--show-toplevel"], root)
    repo_top = (top.stdout or "").strip()
    dir_arg: list[str] = []
    if repo_top:
        rel = os.path.relpath(root, repo_top).replace("\\", "/")
        if rel not in (".", ""):
            dir_arg = [f"--directory={rel}"]
            print(f"路径前缀: --directory={rel}   （git 以仓库顶层为基准 ✓ 实测必须显式给 ✗）")

    text = io.open(args.patch, encoding="utf-8").read()
    names = patch_files(text)
    print(f"条目   : {len(names)} 个文件" + ("   模式: dry-run（不改文件 ✓）" if args.dry_run else ""))
    print("=" * 74)

    fwd = git(["apply", "-p1", *dir_arg, "--check", args.patch], root)
    if fwd.returncode == 0:
        # 可以正向打 ⇒ 还没打过 ✓
        if args.dry_run:
            for n in names:
                print("  将修改  " + n)
            print("=" * 74)
            print(f"汇总：将修改 {len(names)} 个文件（dry-run，未改动 ✓）")
            return 0
        print(f"  准备应用 {len(names)} 个文件的改动 …")
        ap_ = git(["apply", "-p1", *dir_arg, args.patch], root)
        # 【不信任 exit code】用反向检查确认真的打上了 ✓（仓库外的 Skip 陷阱就是 exit 0 ✗）
        rev = git(["apply", "-p1", *dir_arg, "--check", "--reverse", args.patch], root)
        if ap_.returncode == 0 and rev.returncode == 0:
            for n in names:
                print("  ✓ 已改  " + n)
            print("=" * 74)
            print(f"汇总：已修改 {len(names)} 个文件 ✓（反向校验通过 → 确实落盘了 ✓）")
            print("\n下一步：cd MiMo-Code-main && bun install --ignore-scripts")
            print("  （`--ignore-scripts` 是必需的 ✗：tree-sitter-powershell 等原生模块要 node-gyp，")
            print("    在 Windows 上会因 EPERM 失败 ✓）")
            return 0
        print(f"  ✗ 应用未生效（apply rc={ap_.returncode}, reverse-check rc={rev.returncode}）")
        print("    " + (ap_.stderr or "").strip()[:400])
        return 1

    # 正向打不上 ⇒ 要么已打过，要么真冲突 ✓
    rev = git(["apply", "-p1", *dir_arg, "--check", "--reverse", args.patch], root)
    print("=" * 74)
    if rev.returncode == 0:
        print("这份 MiMo 源码**已经是打过补丁的状态** ✓ 无需再动 ✓")
        print(f"（反向校验通过：{len(names)} 个文件都符合『已应用』的样子 ✓）")
        return 0

    bad = conflicts_from(fwd.stderr)
    print(f"✗ 有 {len(bad) or '若干'} 个文件对不上 —— **没有改动任何文件** ✗")
    for b in bad[:25]:
        print("    ✗ " + b)
    if len(bad) > 25:
        print(f"    …另有 {len(bad) - 25} 个")
    print("\n【为什么】这份 MiMo 源码的版本/内容与补丁的基线不同 ✗（多半是拉错了版本 ✓）。")
    print("  基线是上游 main 分支 ✓ —— 注意 tag v0.1.15 的结构是 packages/opencode，")
    print("  和我们对不上（packages/cli 是后来改名才有的 ✓）。")
    print("\n【怎么处理】")
    print("  · 首选：按上面的说明重新拉一份**正确的**源码，再跑本脚本 ✓")
    print("  · 这些文件**不要**手工覆盖 ✗ —— 会丢掉别人可能已经改过的内容 ✓")
    print("  · 若确认这些文件是你自己改的（不是我们要的改动），可先备份再对齐 ✓")
    if fwd.stderr:
        print("\ngit 的原始报错（前 300 字）：")
        print("  " + fwd.stderr.strip().replace("\n", "\n  ")[:300])
    return 1


if __name__ == "__main__":
    raise SystemExit(main())