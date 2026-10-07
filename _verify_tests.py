# -*- coding: utf-8 -*-
r"""验收脚本：跑 main.py 自带的 7 套测试。

【收集器必须收 *a】各套件的 check() 形态不统一：`check(msg, cond)` 与
`check(msg, cond, extra)` 都有 ✗ 写死两个参数会让后续套件抛 TypeError 提前中止
（本项目已因此误判过一次：4 套被截断，看着像"套件本身有问题"）。
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
import pathlib
import sys
import tempfile
import traceback

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = r"C:\Users\Leo\Desktop\lion-code"


def main() -> int:
    spec = importlib.util.spec_from_file_location("lionbox_main", ROOT + r"\main.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["lionbox_main"] = mod
    spec.loader.exec_module(mod)

    results = []

    def run(label, fn):
        got = []

        def _check(*a, **kw):
            msg = str(a[0]) if a else str(kw.get("msg", ""))
            cond = bool(a[1]) if len(a) > 1 else bool(kw.get("cond", False))
            got.append((msg, cond))

        mod.check = _check
        err = None
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                fn()
        except Exception:                                  # noqa: BLE001
            err = traceback.format_exc()
        bad = [m for m, ok in got if not ok]
        results.append((label, got))
        print(f"  {'✓' if not bad and not err else '✗'} {label:26s} 用例 {len(got):3d}  失败 {len(bad)}")
        for m in bad[:6]:
            print("        ✗ " + m)
        if err:
            print("        异常: " + err.strip().split("\n")[-1][:140])
        return not bad and not err

    work = tempfile.mkdtemp(prefix="lb-verify-")
    print("=" * 68)
    ok = True
    ok &= run("run_parser_samples", mod.run_parser_samples)
    ok &= run("run_alias_tables", mod.run_alias_tables)
    ok &= run("run_main_loop", lambda: mod.run_main_loop(pathlib.Path(work)))
    ok &= run("run_guard", mod.run_guard)
    ok &= run("run_context", mod.run_context)
    ok &= run("run_approval", mod.run_approval)
    ok &= run("run_change_review", lambda: mod.run_change_review(pathlib.Path(work)))
    print("=" * 68)
    total = sum(len(c) for _, c in results)
    failed = sum(1 for _, c in results for _, v in c if not v)
    print(f"合计 {total} 用例，失败 {failed} → " + ("全部通过 ✓" if ok else "有失败 ✗"))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())