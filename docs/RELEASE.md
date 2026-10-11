# 发布清单（RELEASE）—— 给下一个照着做的人

> 快照时间：**2026-10-11 17:1x**（本文件里的哈希 / 大小 / 测试条数都是这个时间点**实算**的）。
> 写这份文档时**没有改任何源码**（`main.py` / `工具.py` / `mimo适配.py` / `_start_mimo.py` /
> `提示词.py` / `权限.py` / `沙箱.py` / `MiMo-Code-main/**` 全程只读）。

---

## 0. 版本号怎么定（别自己发明）

| 位置 | 值 | 语义 |
| --- | --- | --- |
| `main.py:3303` `VERSION` | **1.5.46** | **产品版本**：界面标题栏、`/status` 显示的就是它 |
| `mimo适配.py:48` `VERSION` | **1.5.46** | 适配层，必须与 `main.py` 一致 |
| `installer\LionCode.iss:31` `AppVersion` | 1.0.0 | **安装包侧**的编号，只决定文件名 `LionCode-Setup-1.0.0.exe` |
| 仓库根 `VERSION` | 1.5.46 | 本次发布加的单行标记，**改版本时四处一起改**（改 `VERSION` 之前先改 `main.py`） |

**结论：这一版叫 1.5.46**（沿用代码里已有的 `VERSION`，不是新发明的号）。
发版时若只改了代码没改 `VERSION`，以 `main.py` 为准。

---

## 1. 一键流水线：`.lbcheck\rebuild_all.ps1`（7 段）

```bat
powershell -NoProfile -ExecutionPolicy Bypass -File .lbcheck\rebuild_all.ps1
```

**开头先做的环境准备**（脚本 1–17 行）：`TEMP/TMP/TMPDIR` → `.lbcheck\tmp`、
`PYTHONUTF8=0`、`NUITKA_CACHE_DIR` → `.lbcheck\nuitka-cache`、清掉 `PYTHONIOENCODING`。

| 段 | 做什么（读自脚本实际内容） | 产物 / 判据 |
| --- | --- | --- |
| **Stage 1** | `Nuitka rebuild (16 threads)`：循环调 `build_one.ps1` 编 3 个程序。适配层源码按**通配符** `mimo*.py` 取（不能在无 BOM 的 ps1 里写中文文件名字面量 —— 会按 GBK 解成乱码，Nuitka 找不到文件） | `.lbcheck\snk_main\main.dist\LionCode.exe`、`.lbcheck\build_out\mimo适配.dist\adapter.exe`、`.lbcheck\build_out\_start_mimo.dist\start.exe`；末尾打印 `compile failures: N` |
| **Stage 2** | 逐个 `Test-Path` 上面 3 个 exe，打印 MB 与修改时间（`build_one.ps1` 打印的路径不可信，所以要这一步） | 3 个都在 → 继续；缺一个 → `exit 1` 中止 |
| **Stage 3** | `Inno Setup 6 build (threads=16)`：调 `installer\build_installer.ps1 -threads 16`（内部：staging → 校验 stage → `ISCC.exe /DLZMA_THREADS=16`） | `installer\output\LionCode-Setup-1.0.0.exe`（**183.3 MB**）。⚠️ 这一段的成败判定有缺陷 → 见第 4 节待办 ① |
| **Stage 4** | 列 `installer\output` 下最新 4 个 exe（名字 + MB + 时间） | 人工核对：要发的那个是不是刚生成的 |
| **Stage 4.5** | 起开发栈（`final_gate.py` 需要 `:18080` 后端 / `:8791` 适配层）：已在跑就跳过；端口被别的东西占着就 `exit 3`（**绝不杀用户的进程**）；否则开真实终端跑 `启动MiMo界面.cmd` 并轮询 100 s | `:18080=1 :8791=1 bun>=1` → 继续；起不来 `exit 4` |
| **Stage 5** | 跑验收门 `.lbcheck\final_gate.py`，只回显最后 26 行 + `gate exit=N` | `gate=0` 才算过 |
| **Stage 6** | 真装真卸 `installer\test_install.ps1`（用 **18090/8793**，与正在用的 18080/8791 不冲突）。`$env:LB_SKIP_INSTALL_TEST=1` 可跳过 | 打印 `PASS|FAIL|ALL CHECKS|passed:|failed:` 末 22 行 + `install-test exit=N` |
| 收尾 | `==== PIPELINE DONE ====` + `gate=<n>` | 两者都要 0 |

> **编码铁律**：`.ps1` 必须**纯 ASCII 或带 UTF-8 BOM**。PS 5.1 在本机把无 BOM 文件按 GBK 读，
> 中文注释会**吞掉后面的行**（这个 bug 之前烧掉过几小时：`$tmp` 恒 null → TEMP 被清空 → LNK1104）。
> `.cmd` 同理：cmd.exe 按控制台代码页（GBK）解析，且必须是 CRLF。

---

## 2. 验收门

### 2.1 `.lbcheck\final_gate.py` —— **26 项断言**

跑法：`python .lbcheck\final_gate.py`（需要 Stage 4.5 的开发栈在跑）。分 7 段：

| 段 | 项数 | 断言什么 |
| --- | --- | --- |
| ① 编译 | 5 | `main.py` / `工具.py` / `mimo适配.py` / `_start_mimo.py` / `提示词.py` `py_compile` rc=0 |
| ② 工具与提示词 | 7 | 注册工具数==21、`TOOL_PROMPT_HINTS`==21、提示词不广告已删工具、别名表不指向已删工具、系统提示词含工作区目录、含权限策略、不引用 `list_directory`/`git_status`/`move_file`/`working_directory` |
| ③ 云端-only | 3 | `mode=custom`、`baseUrl` 含 `token-plan` 且 `model=mimo-v2.6-flash`、全机 `llama-server` 进程数==0 |
| ④ 云端端到端 | 3 | 真发一条会话消息：调了工具且**只用保留的 21 个**、回答有真实值且无 ERROR 帧、回答无 `<function` 残留 |
| ⑤ 编译产物 | 3 | 3 个 exe 存在（打印 MB） |
| ⑥ 安装包 + `lion-code` | 4 | `installer\output` 有 setup exe、`.iss` 有 `lion-code` 入口、PATH 用 `{olddata}` 追加、**staging 实际内容** `runtime-vulkan=无` + `*.gguf=0` |
| ⑦ 自带测试 | 1 | `run_tests.py` rc=0 且 `失败 0` |

**26 = 5+7+3+3+3+4+1**。⑥ 段还有一条「`lion-code` 在 PATH 上」是**条件项**：本机没装时打
`[INFO]` 不计分，装了才变成 PASS ⇒ 总数可能显示 27。全 PASS 才允许关机。

### 2.2 `installer\test_install.ps1` —— **63 条**

静态看是 **49 条 `Assert` 语句**（`Select-String '^\s*Assert\s'`），
按「必需文件清单循环」与「两个阶段（`lion-code` / 直接 exe 兜底）各跑一遍 API suite」展开后
**实测 63 PASS / 0 FAIL**。它做的是：静默装到 `.lbcheck\selftest\install_<ts>`（不弹 UAC）
→ 断言布局（`start.exe` / `LionCode.exe` / `adapter.exe` / `bun.exe` / `install-deps.ok` /
**`runtime-vulkan` 不存在** / **全树 0 个 `.gguf`** / **不带 `main.py`**）
→ 起装出来的 `start.exe` 轮询 `/health`
→ PATH 断言（**没覆盖旧值**、安装目录**恰好出现 1 次**、`lion-code` 能解析到
`<安装目录>\lion-code.cmd`、`lion-code.cmd` 纯 ASCII）
→ 云端三步 `mode` → `adapter/config` → 真聊天（要真调工具、只能用保留清单、0 ERROR 帧、
配置确实在 token-plan / mimo-v2.6-flash、**全机 0 个 llama-server**、聊天后仍 0 个 `.gguf`）
→ 杀掉属于安装目录的进程 → 静默卸载 → 断言目录真没了。

> 脚本里**内嵌了一个真实的云端 key**（`installer\test_install.ps1:502/512`）——
> 它已经在 git 里了。**换 key 或撤销该 token 时别忘了这两个位置**；文档里一律用 `<你的 key>`。

---

## 3. 发布前必查（逐条打勾）

- [ ] **编译 0 错**：① 段 5 个 `py_compile` 全 0；Stage 1 `compile failures: 0`
- [ ] **225 全绿**：`python .lbcheck\run_tests.py` → `合计 225 用例，失败 0 → 全部通过 ✓`
      （7 套：parser 56 / alias 42 / main_loop 39 / guard 30 / context 20 / approval 8 / change_review 30）
- [ ] **验收门 26/26**：`final_gate.py` `gate=0`
- [ ] **包 sha256 记录**：`Get-FileHash installer\output\LionCode-Setup-1.0.0.exe -Algorithm SHA256`
      —— 本次 `b9ebea5da2fdcec0…`（与 `build_only.log` 里的 `sha256:16=B9EBEA5DA2FDCEC0` 一致 ✓）
- [ ] **真装真卸 63/0**：`test_install.ps1` 的 `ALL CHECKS`
- [ ] **云端口径**：装出来的包必须 0 `llama-server` + 0 `.gguf` + `runtime-vulkan` 不在
- [ ] **已知限制没有新增**：对照 `CHANGELOG.md` 的 8 条「已知问题」，多出来的一条都不许悄悄存在
- [ ] **PATH 提示没被删**：README 里「新窗口才认 PATH」那一条必须还在（用户踩过）
- [ ] **提交只用精确路径**：`git add CHANGELOG.md README.md docs/RELEASE.md VERSION` ——
      ⛔ **绝不 `git add -A`**（工作树里有别的代理正在改 `mimo适配.py`，还有大量未跟踪临时目录）
- [ ] **安装包产物不入库**：`installer/output/` 已 gitignore（提交 `ae30b50`），别再把 183 MB 塞进去
- [ ] push 由用户统一做 —— **发版流程只提交、不 push**

### 已知的两处待办（如实，不粉饰）

**① 流水线判 ISCC 退出码的方式有缺陷 → 会误报 `package FAILED`**

- 现状：`rebuild_all.ps1:63` 用 `if ($LASTEXITCODE -ne 0) { 'package FAILED'; exit 1 }`
  判 Stage 3 成败。这个 `$LASTEXITCODE` 来自**内层那个 `powershell.exe`**，
  而 `-File` 方式下内层脚本的退出码会**继承它最后执行的那条命令**，不一定是 ISCC 的返回值。
- **正确做法**：认 `build_installer.ps1:171` 打印的 **`BUILD OK: <路径>`** 标记
  —— 它只在 `ISCC rc=0` **且** 产物文件真实存在时才打印（166 行 `rc≠0 或文件不在 → exit 1`）。
- **实测**：单独跑打包是好的 —— `.lbcheck\build_only.log:2200` 起：
  `ISCC exit=0 elapsed=9.9 s` → `BUILD OK: …\LionCode-Setup-1.0.0.exe`
  → `size=183.3 MB (192209011 bytes) sha256:16=B9EBEA5DA2FDCEC0`。
  **所以流水线报 FAILED 时，先去 `installer\output` 看产物时间戳和 `BUILD OK`，别急着重编。**

**② `opentui.dll` 段错误（上游 bug，治不了）**

- 本机已积累 **17 份崩溃报告**，全部落在 **opentui.dll** 原生层（`_start_mimo.py:288/442`）。
- 现有缓解是**崩溃出声**（提交 **`0f2fba9`**）：前端非 0 退出且日志判定为崩溃时，
  打印横幅「界面进程崩溃了（不是你的操作有问题）… 直接重新打开本程序即可 ✓ 数据没有损坏」
  并指到 `frontend.log` —— 不再让用户盯着冻结黑屏等。
- 用户侧处置：**重开程序**。上游修好前不要在文档里承诺「不会崩」。

---

## 4. 只读盘点（本快照实算）

### 4.1 `git log --oneline -15`

```
c784d15 perf(installer): 解压并行 + junction 并行重建 + 进度文案改成实测值
0f2fba9 fix(launcher): 前端崩溃时出声 —— 别再让用户盯着冻结黑屏等
16c722f fix(adapter): GlobalEvent 按事件主体带 directory+workspace，会话带 workspaceID（选完工作区后 useEvent 全丢事件/黑屏的配套修复）
c0b8214 fix(adapter): 事件缺 workspace 键 → 选完工作区后实时事件 100% 被丢（黑屏根因）
ae30b50 chore(prompt): 清掉提示词里对已删工具的历史注记 + 安装包产物不入库
42094b0 test(installer): 真装真卸自测改到云端口径 —— PATH / lion-code / 21 工具 / 无 llama-server
04f2936 build(installer): Inno Setup 6 + `lion-code` 命令 + 云端 payload（去掉 runtime-vulkan）
0dcae06 refactor(cloud): 只要云端 API —— 本地运行时整条链路停用（接口保留、明确拒绝）
bd16b91 refactor(tools): 工具从 57 个砍到 21 个 —— 注册表/提示词/别名表三处同步
cdbd020 fix(workspace): 切换工作区后界面显示不变 —— 三层根因全修
eec8054 fix(llm): 429 限流退避重试 + 消掉重复的"模型调用失败:"前缀
8cad024 fix(llm): tools 被双重包装成 60 个 name:null —— 云端 400 "Param Incorrect" 致发消息无响应
119e82f fix(launcher): 修我上一轮引入的回归 —— rc 初始 1 成功路径不置 0，导致 TUI 从未真正启动
e94807f fix(adapter): 最后 2 片补审的 2 条 —— titleSource 枚举外值致侧栏标题永不更新 / 非有限 token 值掐断连接
c6f990d fix(adapter): 清单外实证 fatal —— /provider 模型缺 limit/providerID/api，overflow.ts:81 裸读导致状态对话框修完 tokens 仍崩
```

（`c784d15` 是本快照的 HEAD；`git status` 里 `mimo适配.py` 处于**已修改未提交**状态 ——
那是另一个代理正在做的消息 id 修复，**别碰、别 add**。）

### 4.2 三个 exe + 安装包（实算，`Get-FileHash -Algorithm SHA256`）

| 文件 | 字节 | MB | sha256 前 16 位 |
| --- | ---: | ---: | --- |
| `.lbcheck\snk_main\main.dist\LionCode.exe` | 27,919,360 | 26.6 | `f67eb5a6f50015c9` |
| `.lbcheck\build_out\mimo适配.dist\adapter.exe` | 8,278,016 | 7.9 | `25ea12d6d4c43d51` |
| `.lbcheck\build_out\_start_mimo.dist\start.exe` | 7,803,392 | 7.4 | `49e964ae89438b69` |
| `installer\output\LionCode-Setup-1.0.0.exe` | 192,209,011 | **183.3** | `b9ebea5da2fdcec0` |

配套数据（来自 `build_only.log`）：payload **296.5 MB / 2083 文件**，压缩比 **0.618**，
ISCC **9.9 s**（`LZMANumBlockThreads=16`；单线程对比 36.5 s）。

### 4.3 自带测试（`.lbcheck\run_tests.py`，本轮实跑）

```
✓ run_parser_samples        56 用例  失败 0
✓ run_alias_tables          42 用例  失败 0
✓ run_main_loop             39 用例  失败 0
✓ run_guard                 30 用例  失败 0
✓ run_context               20 用例  失败 0
✓ run_approval               8 用例  失败 0
✓ run_change_review         30 用例  失败 0
合计 225 用例，失败 0 → 全部通过 ✓     [exit code: 0]
```

### 4.4 工具清单来源（免得下次手编）

```bat
:: 需要 sys.path + chdir 到仓库根（main.py 有同目录导入）
python -c "import os,sys,pathlib;R=r'C:\Users\Leo\Desktop\lion-code';sys.path.insert(0,R);os.chdir(R);import main;print(len(main.TOOL_PROMPT_HINTS));print(sorted(main.build_registry(pathlib.Path(R)) and {d.name for d in main.build_registry(pathlib.Path(R)).all()}))"
```

实算结果：注册表 **21 个** = `append_file, ask_user, context_prune, context_window, copy_file,
create_directory, create_file, delete_file, directory_tree, download_file, execute_command,
glob_files, head_tail_file, line_count, modify_file, read_file, search_in_files, system_info,
timestamp, web_search, write_file`；`TOOL_PROMPT_HINTS` 同样 21 条（内容见 `CHANGELOG.md` 的表）。
另有插件 `技能.py` 注册的 **`skill_load`**（不在 21 之内）。

### 4.5 已知的环境性 4 条 FAIL

有 一轮验证出现 4 条 FAIL，定位是**旧安装残留的 PATH 条目遮蔽**（环境问题，非产品断言失败）：
复跑前先把旧安装目录从用户 PATH 里清掉，或换新窗口再跑。
