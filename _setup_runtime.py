# -*- coding: utf-8 -*-
r"""拉 llama.cpp 的 Windows Vulkan 版，解到 <仓库>/runtime-vulkan/。

【为什么需要它】本地模型（`lion-merged-IQ4_XS.gguf`）要靠 llama.cpp 的
`llama-server.exe` 跑起来，后端只认这个位置：

    <app-root>/runtime-vulkan/llama-server.exe     （源码里的 RUNTIME_EXE_REL）

而后端自己的下载源没实现 —— `POST /api/runtime/local/download` 回的是
"下载源解析将在 P2 实现"，所以首次部署得由这个脚本从 llama.cpp 官方
Releases 取一份。运行时二进制不进仓库（31.8 MB），要用就跑一次：

    python _setup_runtime.py

【两个坑】
1. 用 releases 列表而不是 `/latest`：`latest` 现在返回 v0.5.0（只带
   nightly-tag.txt），llama.cpp 的构建包挂在 b#### 流水号下。
2. 后端启动必须带 `--app-root=<仓库根>`，否则它会在 `<仓库>/python/`
   下找模型和运行时（旧布局），模型会被判为"未安装"并触发重复下载。
"""
from __future__ import annotations

import io
import json
import os
import sys
import urllib.request
import zipfile

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(ROOT, "runtime-vulkan")
API = "https://api.github.com/repos/ggml-org/llama.cpp/releases?per_page=30"


def get(url: str, timeout: float = 60.0) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "lion-code-setup"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def main() -> int:
    print("[1/3] 查询 llama.cpp Release 列表 …", flush=True)
    try:
        rels = json.loads(get(API).decode("utf-8"))
    except Exception as e:                                # noqa: BLE001
        print(f"  查询失败: {type(e).__name__}: {e}")
        print("  手动下载：https://github.com/ggml-org/llama.cpp/releases")
        print(f"  选 *-bin-win-vulkan-x64.zip，解到 {DEST}")
        return 1
    if isinstance(rels, dict):
        rels = [rels]

    pick = None
    for want in ("bin-win-vulkan-x64", "bin-win-cpu-x64"):
        for rel in rels:
            for a in (rel.get("assets") or []):
                n = str(a.get("name", ""))
                if want in n and n.endswith(".zip"):
                    pick = (a, rel.get("tag_name", "?"))
                    break
            if pick:
                break
        if pick:
            break

    if not pick:
        print("  最近的 Release 里没找到 Windows 包，可选：")
        seen = 0
        for rel in rels[:6]:
            for a in (rel.get("assets") or []):
                n = str(a.get("name", ""))
                if "win" in n and n.endswith(".zip") and seen < 20:
                    print(f"    {rel.get('tag_name')}  {n}")
                    seen += 1
        return 1

    asset, tag = pick
    name = asset["name"]
    url = asset["browser_download_url"]
    size = asset.get("size", 0)
    print(f"[2/3] 下载 {tag} / {name}（{size / 1048576:.1f} MB）…", flush=True)
    try:
        data = get(url, timeout=1800)
    except Exception as e:                                # noqa: BLE001
        print(f"  下载失败: {type(e).__name__}: {e}")
        return 1
    print(f"      收到 {len(data) / 1048576:.1f} MB", flush=True)

    print(f"[3/3] 解压到 {DEST} …", flush=True)
    os.makedirs(DEST, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        members = [m for m in z.namelist() if not m.endswith("/")]
        # 压缩包内有目录层级，摊平到 DEST（llama-server.exe 要能直接在根）
        for m in members:
            base = os.path.basename(m)
            if not base:
                continue
            with z.open(m) as src, open(os.path.join(DEST, base), "wb") as dst:
                dst.write(src.read())
        print(f"      解出 {len(members)} 个文件", flush=True)

    exe = os.path.join(DEST, "llama-server.exe")
    if os.path.isfile(exe):
        print(f"✓ 就绪: {exe}", flush=True)
        return 0
    print("✗ 解压后没看到 llama-server.exe，目录内容：", flush=True)
    for f in os.listdir(DEST)[:20]:
        print("    " + f)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())