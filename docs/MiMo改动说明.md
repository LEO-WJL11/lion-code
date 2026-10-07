# MiMo 源码改动说明（`MiMo-Code-main/`）

## 这份东西为什么存在

`MiMo-Code-main/` 是**从上游下载的第三方源码**（`github.com/XiaomiMiMo/MiMo-Code` ✓），
它被 `.gitignore` 排除在仓库之外 ✗ —— 但我们对它做了 **80 处改动**（品牌、命令精简、
侧栏会话列表、插件、i18n 加固、退出画面、工作区对话框…）。

⇒ **换机器 / 重新下载 MiMo 源码后，这些改动会全部丢失** ✗
⇒ 所以改动被固化成补丁，用脚本一键重放 ✓

```
docs/mimo-changes.patch      改动本体（git 格式，80 个文件块，其中 3 个是新文件）
_patch_mimo.py               一键重放脚本（逐条报告 · 幂等 · 冲突不动文件）
```

## 怎么用

```bash
# ① 先把 MiMo 源码放到仓库内，目录名必须是 MiMo-Code-main
#    （脚本要求目标在 git 仓库里，见下方"两个坑"）

# ② 看会改什么（不动文件）
python _patch_mimo.py --dry-run

# ③ 真打
python _patch_mimo.py

# ④ 装依赖（--ignore-scripts 必需）
cd MiMo-Code-main && bun install --ignore-scripts && cd ..
```

幂等 ✓：已打过会直接说「已经是打过补丁的状态 ✓ 无需再动 ✓」。

## ⚠️ 两个坑（都实测踩过）

**① 别按版本号认源码** ✗

| 你可能会拉的 | 结构 | 对不对 |
|---|---|---|
| tag `v0.1.15` | `packages/opencode` | ✗ **错的基线** |
| **`main` 分支** | `packages/cli` | ✓ 正确 |

两边 `@mimo-ai/*` 都是 `0.1.15` ✗ —— **版本号一样、结构完全不同** ✓。
`packages/cli` 是上游 `chore(repo): rename packages/opencode to packages/cli` 之后才有的 ✓。

**② `git apply` 有两个"假成功"** ✗

```
· 在 git 仓库**之外**执行 → 每个文件报 `Skipped patch` 但**返回 0** ✗
· 在仓库内但目标不在仓库顶层 → 路径按**仓库顶层**解析 ✗
  （会去改仓库根的同名路径，然后报"已改"、其实没动 ✓）
```

`_patch_mimo.py` 对这两条都做了处理 ✓（拒绝 + 显式 `--directory=`），
并且**打完再做一次反向校验** ✓ —— 不信任 `git apply` 的退出码 ✗。

## 改动家族（80 个文件）

| 类别 | 主要文件 |
|---|---|
| **品牌** | `cli/logo.ts`（块状 art）、`cli/ui.ts`（wordmark）、`i18n/*.ts`（7 个语言）、`routes/session/index.tsx`（终端标题）、`script/publish.ts`、`session/goal.ts`（喂给模型的提示词 ✗ 不改模型会自称 Mimo Code ✓） |
| **命令精简** | `cmd/tui/app.tsx`（30→17）、`cmd/tui/routes/session/index.tsx`（14→11）—— 删掉没适配的自带命令 ✓ |
| **新增命令** | `/workspace`（新建）、`/workspaces`（选择）、`util/win-folder-picker.ts`（Windows 原生文件夹窗口） |
| **侧栏会话列表** | `routes/session/sidebar.tsx`（直接渲染，**绕开插件运行时** ✓ + 点选 + `Delete` 两段确认） |
| **插件** | `feature-plugins/sidebar/sessions.tsx`（新增）、`plugin/internal.ts`（**停用**它以免两份列表 ✗） |
| **i18n 加固** | `context/language.tsx` —— `t()` 非字符串返回 `""`，防 `path[0]` 崩溃 ✓ |
| **退出画面** | `ui.ts` 的 `logo()` 加 `shape` 参数 + `routes/session/index.tsx` 用窄体（82→46 列，原来会折行 ✓） |
| **崩溃修复** | `component/dialog-workspace-create.tsx`（`/experimental/workspace/adaptor` 必须返回数组 ✓）、`feature-plugins/home/tips-view.tsx` |

### ★ 最容易漏的一处

`routes/session/sidebar.tsx` 里品牌被**拆成两个标签** ✗：

```tsx
<b>Open</b><span style={{fg: theme.text}}><b>Code</b></span>     ← 拼出 "OpenCode"
```

**按整词搜索永远搜不到** ✗ —— 这一处排查了很多轮才定位 ✓。
补丁里已显式包含它 ✓，但**手工改动时务必注意同样的拆分写法** ✓。

## 无法自动重放的部分

- `MiMo-Code-main/node_modules/**` ✗ —— 依赖要 `bun install --ignore-scripts` 重新装 ✓
  （`--ignore-scripts` 是必需的：`tree-sitter-powershell` 等原生模块要 node-gyp，
  在 Windows 上会因 EPERM 失败 ✓）
- 工作区里的 `packages/*/node_modules` 残留副本 ✗ —— 装完若报
  `Cannot find module 'drizzle-orm/sqlite-core'`，删掉那 4 个目录即可 ✓
  （它们会挡住根目录的完整依赖 ✓）

## 补丁是怎么生成的（可复现）

```
① 稀疏克隆正确的基线（只取我们用到的包）
   git clone --depth 1 --filter=blob:none --sparse git@github.com:XiaomiMiMo/MiMo-Code.git <dir>
   git -C <dir> sparse-checkout set packages/cli packages/plugin packages/sdk packages/shared
② 与 MiMo-Code-main/ 逐文件比对（**先归一化行尾** ✗ 否则每个文件都"不同" ✓）
   我们这份是 Windows 下载的 CRLF ✗，上游 git 里是 LF ✓
③ 用临时 git 仓库生成补丁：先提交 pristine → 再覆盖成我们的 → git diff
   （不要用 `git diff --no-index` ✗ 它会输出绝对路径、含反斜杠时还加引号转义 ✓）
```

验证方式：拿一份 pristine 打一遍 → 与 `MiMo-Code-main/` 逐字节比对 →
**1933 个文件全部一致** ✓（归一化行尾后 ✓）。