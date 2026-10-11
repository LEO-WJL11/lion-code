# Changelog — Lion Code

按「用户能感知到的变化」记，不罗列内部提交；做不到的事写进 **已知问题**，不藏。
版本号沿用 `main.py` / `mimo适配.py` 里的 `VERSION`（界面标题栏显示的就是它）。

## [1.5.46] — 2026-10-11 — 云端版首发（可发布状态）

> 安装包文件名里的 `1.0.0` 是 Inno Setup 侧的 `AppVersion`（`installer\LionCode.iss`），
> **不是产品版本号**。产品版本 = **1.5.46**，两者并行、别混。

### 这一版最大的变化：只走云端，不再带本地模型

- **本地运行时整条链路停用**：安装包**不带** `runtime-vulkan`（`llama-server`）、**不带**任何
  `*.gguf` 权重。装完不会在后台拉起 llama-server，也不会偷偷下 5 GB 模型。
- 想切回本地会被**明确拒绝并说明原因**（`本地模式已停用（本产品为云端 API 版）`），
  不是静默失败。
- 出厂已内置端点与模型：`https://api.xiaomimimo.com/v1` + `mimo-v2.6-flash` ——
  **你只差一个 API Key**（见下面「云端接入」）。

### 可以双击安装了：`LionCode-Setup-1.0.0.exe`（183.3 MB）

- 三个程序都用 Nuitka 编成原生 exe：`LionCode.exe` 26.6 MB / `adapter.exe` 7.9 MB /
  `start.exe` 7.4 MB（`--jobs=16`）。
- 装完在 **cmd 里敲 `lion-code` 就能启动**（安装器把安装目录追加进用户 PATH，
  `{olddata}` 追加不覆盖已有 PATH，并广播 `WM_SETTINGCHANGE`）。
- 打包用 **Inno Setup 6**（ISCC 6.7.3），`LZMANumBlockThreads=16`：
  实测 16 线程 **10.5 s** vs 单线程 **36.5 s**。
- 卸载：设置 → 应用 → Lion Code（或 `unins000.exe /VERYSILENT /NORESTART`），
  卸载时会先把安装目录从 PATH 里摘掉。

### 工具从 57 个砍到 21 个

砍掉的（`list_directory` / `move_file` / `git_*` 9 个 / `fetch_url` / `http_get` /
`translate` / `regex_test` / `word_count` / `file_info` …）**提示词和别名表同时清干净**
—— 模型喊一个不存在的工具名，不会再被归一化到空壳上白跑一轮。

留下的 21 个（取自 `main.py` 的 `TOOL_PROMPT_HINTS` 真实文本）：

| 工具 | 干什么 |
| --- | --- |
| `read_file` | 读文件内容（已知路径时用；传目录会失败） |
| `head_tail_file` | 看文件开头/结尾 N 行（大日志省上下文，`tail=true` 看结尾） |
| `line_count` | 统计行数（给目录会递归累计） |
| `directory_tree` | 画目录树 —— 看结构、列目录都用它 |
| `glob_files` | 按名字/后缀找文件（`**/*.java` 这种） |
| `search_in_files` | 在**文件内容**里搜文本或正则 |
| `create_file` | 只创建**空**文件 |
| `write_file` | 新建文件并写入内容（也用于整体覆盖） |
| `append_file` | 往文件末尾追加内容 |
| `modify_file` | 改已有文件的一小部分：替换 / 插入 / 删除行 |
| `copy_file` | 复制文件或目录（移动改名 = copy + delete） |
| `delete_file` | 删除文件或空目录 |
| `create_directory` | 创建目录（含父目录） |
| `download_file` | 把 URL 上的文件下载到本地 |
| `execute_command` | 执行命令（git / 构建 / 测试 / 装依赖）；环境是 Windows + PowerShell |
| `system_info` | 系统信息（CPU、内存、操作系统） |
| `timestamp` | 当前时间 |
| `web_search` | 联网搜索（默认 `cn.bing.com`，可指定 duckduckgo / google / baidu） |
| `context_window` | 调整本会话上下文窗口（默认 16K，做完立刻调回 16384） |
| `context_prune` | 删掉本会话前面已经没用的历史消息（真删，只留最近几条） |
| `ask_user` | 需要用户做选择或补充信息时提问 |

另外**技能插件注册的 `skill_load`** 仍在（按 id 取回某个技能的完整指令）——
它由插件系统提供，不在上面 21 个之内，所以清单是 **21 个内置 + 插件的 `skill_load`**。

### 云端接入（配置步骤）

**方式 A —— 界面里的命令（最省事）**：自带 Ink 界面里

```
/key <你的 key>                一步到位：切云端 + 填 key + 推给适配器（走小米 MiMo）
/endpoint <URL> [模型]          换成任意 OpenAI 兼容端点
/mode custom                    手动切到云端模式（会自动带出厂端点）
```

**方式 B —— HTTP 两步（任何界面都能用，安装版推荐）**：

```powershell
# ① 写模式与端点
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:18080/api/runtime/mode `
  -ContentType 'application/json' -Body '{
    "mode": "custom",
    "baseUrl": "https://api.xiaomimimo.com/v1",
    "apiKey": "<你的 key>",
    "model": "mimo-v2.6-flash"
  }'

# ② 推给当前适配器（只做①是不够的：活跃适配器的 baseUrl 是装配时固化的，
#    不推就会出现"端点改成功了、请求照样打到 127.0.0.1:8788"）
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:18080/api/chat/adapter/config `
  -ContentType 'application/json' -Body '{
    "baseUrl": "https://api.xiaomimimo.com/v1",
    "apiKey": "<你的 key>",
    "model": "mimo-v2.6-flash"
  }'
```

> ⚠️ **文档里不写真实 key**：上面 `<你的 key>` 是占位符。key 落在
> `%USERPROFILE%\.lioncode\app-config.json`，**别把它贴进 issue / 截图 / 仓库**。

- 换模型：界面里跑 **`/models`**（或 `Ctrl+X M`）打开模型选择；
  它读的是后端 `GET /api/models`（真去请求 `{baseUrl}/models`）。
- 看当前生效配置：`GET /api/runtime/mode`；适配器状态：`GET /api/chat/adapter/status`。

### 常用命令（MiMo 界面 = 默认界面 / 安装版）

| 命令 | 作用 |
| --- | --- |
| `/help` | 全部命令 |
| `/new`、`/sessions` | 新会话、会话列表 |
| `/models` | 切换模型（`Ctrl+X M`） |
| `/workspace`、`/workspaces` | 新建工作区、切换工作区 |
| `/context-limit`、`/compact` | 看/改上下文上限、压缩历史 |
| `/agents`、`/mcps`、`/status` | 子代理、MCP、当前状态 |
| `/themes`、`/language`、`/exit` | 主题、语言、退出 |

### 已知问题（逐条如实）

1. **安装时可能写不了 PATH（本机沙箱特有）**：本机的沙箱把未签名 exe 降到
   **Low 完整性级别** → HKCU 写不进 → 安装器**跳过 PATH 写入并在日志里写明**
   （`LionCode: WARNING - HKCU is NOT writable …`），不会因为注册表写不进而整包回滚。
   **正常机器上是 Medium 级别，PATH 由安装器真实写入 ✓**。遇到跳过时按日志提示
   手动把安装目录加进 PATH 即可。
2. **旧终端看不到新 PATH**：安装器广播了 `WM_SETTINGCHANGE`，但**已经开着的 cmd 是
   安装前的环境快照** —— 必须**开新窗口**才认 `lion-code`（这条踩过，见 README）。
3. **`opentui.dll` 段错误**：上游渲染层 bug，本机已积累 **17 份崩溃报告**，治不了。
   缓解是**崩溃出声**（提交 `0f2fba9`）：界面崩了不再停在冻结黑屏，会明确打印
   「界面进程崩溃了… 直接重新打开本程序即可，数据没有损坏」并指到 `frontend.log`。
   **处理办法：重开程序**。
4. **`web_search` 走 `cn.bing.com` + 兜底**：默认引擎 Bing CN（国内可直连），
   搜不到时按 `bing → duckduckgo` 兜底，也可显式指定 `baidu` / `google`。
   结果页是抓 HTML 解析的，**搜索引擎改版就可能失灵**。
5. **`translate` 已不在工具清单里**：它依赖的免费 HTTPS 翻译接口在**本机对部分 HTTPS
   站点直连不通**，要自己配 endpoint 才能用；这一版已把它从注册表移除 ——
   需要翻译请自己用 `execute_command` 调工具（或恢复该工具并配好 endpoint）。
6. **Inno Setup 7 是 Non-commercial 许可**：ISCC 7 的横幅标着
   "Non-commercial use only"，**商用要买许可**。当前打包用的是 **Inno Setup 6**，
   换 7 之前先看许可。
7. **本机网络对部分 HTTPS 站点不通**：不是产品逻辑问题，是这台机器的出网环境 ——
   表现为个别端点/下载源连不上，换网络或换 endpoint 即可。
8. **没有代码签名**：SmartScreen 首次运行会拦一下（更多信息 → 仍要运行），
   安装包里的 exe 也是未签名的（这正是本机被降级到 Low IL 的原因，见第 1 条）。

### 验证状态（这一版发出去时的实测）

- 自带测试 **225 条全绿**（`.lbcheck\run_tests.py`，7 套：解析 56 / 别名 42 / 主循环 39 /
  审批 30 / 上下文 20 / 授权 8 / 改动审核 30）。
- 真装真卸 **63/0**（`installer\test_install.ps1`：静默装 → 起三段 → 云端聊天走工具 →
  零 llama-server → 零 `.gguf` → 卸干净）。
- 5 个源文件 `py_compile` 0 错；验收门 `.lbcheck\final_gate.py` **26 项 PASS**。
- 另有一轮验证出现 **4 条 FAIL**，定位为**旧安装残留的 PATH 条目遮蔽**造成的环境问题
  （不是产品断言失败）—— 复跑前先把旧安装目录从 PATH 里清掉。

发布流程与打包细节见 [`docs/RELEASE.md`](docs/RELEASE.md)。
