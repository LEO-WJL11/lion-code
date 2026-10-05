# 🦁 Lion Code（Lion-Code Agent Harness）

**本地优先的 AI 编程 Agent**：后端是纯 Python 3.15 单机运行，界面是用 **Ink（React for CLIs）**
写的终端界面，模型跑在你自己机器上 —— 代码和数据不出本机。

配套模型（本机默认用的那个）：**[lion-models1 @ ModelScope](https://modelscope.cn/models/lionnezha/lion-models)**
—— 9B、Qwen3.5 架构、按 Agent 工具调用微调，三档 GGUF 量化（Q8_0 / Q4_K_M / IQ4_XS）。
首次使用自动下载，装完不用配环境。

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.15-blue.svg)](https://www.python.org/)
[![依赖](https://img.shields.io/badge/第三方依赖-0-green.svg)](#-项目结构)

---

## 🚀 怎么运行

**双击仓库根目录的 `启动LionCode.cmd`** —— 这是最省事的方式（会开一个控制台窗口跑界面）。

命令行也行：

```bash
python main.py                 # 终端界面（默认）
python main.py --backend-only  # 只起 HTTP 后端，不起界面（调接口 / 跑自动化用）
```

> ⚠️ **界面需要"真终端"（TTY）**。PyCharm 的 Run 窗口、管道、输出重定向都**没有 TTY**，
> Ink 的光标控制在那儿会变成一堆乱字，看起来就像"只是个 python 终端"。
> 所以：
> - 在 PyCharm 里 Run 时，程序会**自动新开一个 Windows Terminal 窗口**把界面放进去跑；
> - 或者直接双击 `启动LionCode.cmd`；
> - 或者在 Windows Terminal / PowerShell 里执行 `python main.py`。

界面依赖只装一次（Node 20+）：

```bash
cd tui
npm install                    # 装 ink / react / ink-text-input，约 40 个包
```

缺 node 或没装依赖时，程序会直接告诉你去 `tui/` 跑一次 `npm install` ——
**界面只有 Ink 这一个实现**（不做第二套，免得两套界面两套行为）。

CLI 里能用 `/help` 看全部命令。常用几个：

```
/new [名字]          开新会话          /mode local|custom   本地模型 / 云端
/key <APIKey>        填云端 Key（走小米 MiMo）
/endpoint <URL> [模型]  任意 OpenAI 兼容端点
/tools               按分组看全部工具   /approvals auto      全部工具免确认
/panel               开关右侧面板      /status              当前状态
```

界面长这样（对齐 MiMo Code：标签栏 + 用户消息框 + 工具分组 + 底部输入框与状态栏 + 右侧面板）：

```
 MC | Lion Code · 询问可调用的工具                                            Lion Code 1.5.46
 ─────────────────────────────────────────────────┬──────────────────────
  ╭───────────────────────────────────────────╮   │ Context
  ▌你能调用什么工具                            │   │ ≈24,691 tokens
  ╰───────────────────────────────────────────╯   │ 2% used
                                                  │ limit 1.05M
  + Thought: 385ms                                │ 49 t/s
                                                  │ $0.00 spent
  我可以调用以下工具：                             │
                                                  │ 工作目录
  文件操作                                         │ ~
   - Read - 读取文件或目录内容                     │
   - Write - 创建或覆盖文件                        │ LSP
   - Edit - 精确替换文件中的字符串                  │ 未接入 LSP 子系统
  终端                                            │
   - Bash - 执行 shell 命令                        │ ~/
                                                  │ ● Lion Code 1.5.46
 ╭───────────────────────────────────────────╮    │
 │▌ 我看这个项目的整体结构                     │    │
 │  Build · MiMo-V2.6-Flash · high           │    │
 ╰───────────────────────────────────────────╯    │
 ─────────────────────────────────────────────────┴──────────────────────
 24.7K/944K (3%) · $0.00   回车 发送   / 唤起命令   Ctrl+P 面板   Ctrl+C 中断
```

本仓库自带 Python 3.15 运行环境，无需另装：

| 位置 | 用途 |
|---|---|
| `.pythons/315/` | Python 3.15.0rc3 本体（官方免安装完整版） |
| `.venv/` | 虚拟环境（**Python 侧第三方依赖为 0**，只用标准库） |

PyCharm 里把解释器指到 `.venv\Scripts\python.exe` 即可。

## 📁 项目结构

**后端 6 个 Python 文件 + 前端 1 个 Ink 应用**：

| 文件 | 行数 | 职责 |
|---|---|---|
| `main.py` | 24,193 | 决策循环、HTTP 服务、会话、事件、模型、上下文 + **主程序入口**（负责起后端并拉起 Ink 界面） |
| `工具.py` | 10,475 | 全部工具（文件 / 搜索 / Git / Shell / 网页 …）与工具注册表 |
| `插件管理.py` | 5,094 | 插件宿主、插件契约、插件开发、团队、自动化 |
| `技能.py` | 1,684 | 技能仓库（4 个内置技能） |
| `权限.py` | 818 | 授权策略、审批档位、改动审核 |
| `沙箱.py` | 494 | 工作区上下文与路径沙箱 |
| `tui/app.js` | ~900 | **Ink（React for CLIs）终端界面** —— 只做渲染，数据全走 `/api/*` |

另有 `skills/`（内置技能源，4 个）、`docs/_archive/`（重构前全量快照，回退用）。

> **历史说明**：下面的安装包 / VS Code 扩展 / Spring Boot 章节是 **Java 版时期**的文档，
> 对应的 `installer/`、`extensions/`、`dist/` 目录与 Java 源码已在纯 Python 移植后移除，
> 保留在此仅供追溯。当前版本没有安装包，直接 `python main.py` 运行。

---

## ⬇️ 下载与安装（三分钟）—— Java 版时期

**去哪里下**：这个仓库的 **`installer/release/`** 文件夹里，就一个文件：

> ### 👉 [`installer/release/LionBox-Setup-1.5.4.exe`](https://github.com/LEO-WJL11/lion-code/blob/main/installer/release/LionBox-Setup-1.5.4.exe)

打开那个页面后点右上角的 **Download**（或直接点这个直链：
[1.5.4 直链下载](https://github.com/LEO-WJL11/lion-code/raw/main/installer/release/LionBox-Setup-1.5.4.exe)），
大小 **74 MB**。仓库里没有别的东西需要下 —— 模型权重不在这里，首次使用时自动下（见下）。

**怎么装**：

1. **右键安装包 → 「以管理员身份运行」** —— 这一步是必须的：
   不加管理员权限安装会**报权限错误**（写文件/装 VS Code 插件那几步会失败）；
2. 如果 Windows 弹出蓝色的"已保护你的电脑"（SmartScreen）：点 **更多信息 → 仍要运行**
   —— 安装包没有买代码签名，这一步是正常的，不是有毒；
3. 接着弹 UAC 询问时点「是」，然后一路下一步；
4. 安装快结束时它会**自动把 VS Code 插件也装上**（自己找 `code` 命令；
   找不到就跳过，不影响本体使用）。

**装完怎么开始用**：

| 你想在哪用 | 怎么做 |
| --- | --- |
| **在 VS Code 里**（推荐） | 打开 VS Code → 打开你的项目文件夹 → **最右边那一栏**就是「Lion Code Agent」，直接在里面说话就行（第一次可能要把 VS Code 重开一下让插件生效） |
| 在浏览器里 | 开始菜单启动 Lion Code（或桌面快捷方式），然后开 `http://127.0.0.1:8080` |

**第一次会先下模型**：如果安装目录里还没有权重，助手会自动从 ModelScope 下载
`lion-merged-Q8_0.gguf`（**8.87 GB，只下一次**，界面上能看到进度）。
网慢就先干别的，下完再聊；想离线部署就把 `.gguf` 手动放进安装目录，程序优先用本地文件。

**卸载**：Windows 设置 → 应用 → Lion Code 卸载（或开始菜单里的卸载项）。
VS Code 插件会一起卸掉；你的会话和工作区数据保留。

---

## 📁 这个仓库里东西都在哪

| 想看/想要的 | 去这里 |
| --- | --- |
| **后端全部代码**（6 个文件） | 根目录 `main.py`、`工具.py`、`插件管理.py`、`技能.py`、`权限.py`、`沙箱.py` |
| **界面** | 就在 `main.py` 里（终端 CLI），没有独立前端文件 |
| 内置技能（通用 skill 格式，可以自己加） | `skills/` —— 每个子目录一个技能（有 `SKILL.md`） |
| 运行环境 | `.pythons/315/`（Python 本体）、`.venv/`（虚拟环境） |
| 改动前的快照（回退用） | `docs/_archive/` —— 含内联前的 186 个模块、40 个回归套件、Java 源码 |
| 模型权重 | 根目录 `lion-merged-IQ4_XS.gguf`（首次自动下；也可以只放 ModelScope 那份） |

> **历史说明**：本文档下面的「安装包 / VS Code 插件 / 出包脚本」章节是 **Java 与桌面版时期**留下的，
> 对应的 `installer/`、`extensions/`、`dist/`、`tools/checks/`、`python/lionbox/` 都已移除
> （`tools/checks/` 与旧引擎在 `docs/_archive/重构前全量快照.zip` 里）。当前版本没有安装包，
> `python main.py` 就是全部。

模型权重**不在这个仓库**（太大），在 ModelScope：
**[lionnezha/lion-models](https://modelscope.cn/models/lionnezha/lion-models)**。

## 装什么（就一个包）

**`installer/release/LionBox-Setup-1.5.4.exe`**（74 MB）= 后端 + WebUI + llama.cpp 运行时（Vulkan）+ 精简 JRE +
内置技能 + **VS Code 插件**。装完：

- **VS Code 右侧栏**（secondary sidebar）多出 **Lion Code Agent** 面板 —— 不用跳出去，
  在编辑器里就能让 Agent 干活；卸载时插件跟着卸掉；
- 想用完整界面：开始菜单启动 Lion Code，浏览器打开 `http://127.0.0.1:8080`；
- 首次用到本地模型时自动从 ModelScope 下载权重（默认 Q8_0，8.87 GB，**只下一次**）；
  离线部署就把 `.gguf` 放进安装目录，程序优先用本地文件。

## 在编辑器里怎么干活

| 能力 | 说明 |
| --- | --- |
| 工作区 = 打开的文件夹 | 插件把当前文件夹交给后端建工作区；换文件夹就换工作区、自动开新会话 |
| `@` 引用单个文件 | 只把这一个文件读进上下文（窗口默认 16K，省着用）；也支持 `@history:` 引用历史对话 |
| **AI 改的文件要你先点通过** | 改文件的工具先攒成待审改动，面板里看 diff，点「通过并写入」才落盘；点「打回」写理由，模型按理由重写 —— 相当于作业签字 |
| 暂停 / 继续 / 停止 | 长任务跑到一半可以叫停 |
| 看得见每一步 | 对话里实时显示正在调用的工具名和结果 |

## 一切皆插件（71 个 / 9 类）

运行时核心保持薄，能力都挂在插件上：**能热插拔、能在设置里逐项开关、能自己写**。
（下面的数字取自运行中的 `/api/plugins`，不是手写的。）

| 类别 | 数量 | 干什么 |
| --- | --- | --- |
| BASE_TOOL | 22 | 极简模式下可用的基础工具：读写文件、列目录、跑命令、搜内容 |
| ADVANCED_TOOL | 36 | 标准模式追加：Git、网络、代码与文本处理等 |
| SKILL | 4 | 技能包（通用 skill 格式：介绍 + 何时用 + 正文），可自己放进 `skills/` |
| TERMINAL | 1 | 常驻终端：每条命令最长跑多久、最多回多少内容，用户可配 |
| AGENT_LOOP | 1 | 大循环：最多几轮、单工具等多久、一轮派几个工具 |
| SUBAGENT | 2 | 子智能体：递归层级、数量上限、用哪个模型 |
| AGENT_TEAM | 2 | 智能体团队：每个成员用什么模式、负责什么 |
| APPROVAL_REVIEW | 2 | 自动授权审查（让另一个模型先判该不该放行）+ **改动人工审核** |
| AUTOMATION | 1 | 自动化任务：按时间或周期在会话里自动执行 |

设置里只有一个「插件管理」页：每类插件的开关 + **该插件自己的参数就在它那一行下面**，
还有插件开发模式（生成骨架 → 改代码 → 重新加载，不用重启）。

## 上下文是钱，所以默认 16K

本机模型原生 256K，但**每一条消息都要把整个前缀重新预填充一遍** —— 窗口开多大就多算多少。
所以默认窗口收到 **16K**，另外给模型两个工具自己管：

- `context_window` —— 真的不够时调大，**干完必须调回来**（约束写在系统提示里）；
- `context_prune` —— 前面那些探查过程没用了，自己删掉（真删，保留最近几条）。

两者都按会话记，界面上也能手动改（输入框下面那个「窗口 16K」）。

## 验证到什么程度

- **39 个回归套件，0 失败**（`python tools/checks/_run_all_checks.py`）：工具调用、上下文、
  插件系统、会话、UI/接口、技能、`@` 引用、终端限制、压缩与裁剪……
- **真装真卸**：安装包装到临时目录 → 用装出来的自带 JRE 起服务 → 断言页面/接口 → 卸载
  （`tools/release/_verify_154_single.py`，其中包含"VS Code 里到底有没有装上插件"这一条）；
- 插件系统的行为用例是"真跑"：派子智能体、团队分头干活、审查 DENY/ALLOW、自动化到点投递、
  一轮最多几个工具、改动通过/打回 —— 不是看代码里有没有函数名。

## 先说清楚这个项目不吹什么

旧的 README 里写着"超越某某"、"HumanEval 70% vs 50%"这类话。**那些删了** ——
没法验证的对比没有信息量。下面每一条都能在仓库里找到对应的代码或用例；
**做不到的事写在最后的「已知限制」里**，而不是藏起来。

## 已知限制

- **本机 4bit 模型的工具选择准确率有限**：实测"第一次就选对工具"约 43% → 66.7%；
  harness 保证的是**调用格式合法（30/30）、选错了能纠正、多轮下来最终选对 93.3%**。
  要更高就得换更大的权重或云端模型。
- **慢**：Q8 权重 + Intel Arc 核显约 **10.9 token/s**，一条复杂任务几分钟很正常。
- **没有代码签名**：Windows SmartScreen 首次运行会拦一下（"更多信息 → 仍要运行"）。
- **Windows 为主**：安装包、常驻终端、VS Code 插件都是按 Windows 验证的。
- **模型权重不随包发布**（8.87 GB），首次使用要联网下载。
- 自动装 VS Code 插件认几个常见安装位置；装在别处就手动装（VSIX 在安装目录里）。

## 配套模型

| | |
| --- | --- |
| 模型 | **lion-models1**（9B，Qwen3.5 架构，32 层混合线性注意力） |
| 地址 | **https://modelscope.cn/models/lionnezha/lion-models** |
| 量化 | Q8_0 8.87 GB（推荐）/ Q4_K_M 5.24 GB / IQ4_XS 4.87 GB |
| 怎么来 | Qwen3.5-9B 底座 + 4.9 万条 Agent 工具调用数据 QLoRA 微调（核显笔记本上做的），合并后量化 |
| 换别的 | 也支持任意 OpenAI 兼容端点（本地或云端），设置 → 模型来源 里切 |

这个模型和 harness 是**配套设计**的：模型按文本工具调用约定微调，harness 两种通道都认；
系统提示里教的"一轮可以给多个互不依赖的调用、干完活要收尾"，也是 harness 真正支持的语义。
模型卡片（下载、校验、llama.cpp 参数、速度）见仓库里的 [`README-模型.md`](README-模型.md)。

## 自己跑

```bat
:: 仓库自带 Python 3.15 与 .venv，第三方依赖为 0，不需要 pip install
.venv\Scripts\python.exe main.py                 :: 终端界面（默认）
.venv\Scripts\python.exe main.py --backend-only  :: 只要后端，然后开 http://localhost:8080
```

## 技术栈

Python 3.15 后端（**只用标准库**：`http.server` + 手写路由 / SSE，Python 侧第三方依赖为 0），
前端是 **Ink（React for CLIs）** 写的终端界面（`tui/`，依赖 node_modules，`npm install` 一次）；
本地推理走 llama.cpp（`llama-server`，OpenAI 兼容，端口 8788），也可以切到云端
（内置小米 MiMo 的默认端点）。

```
main.py           决策循环、HTTP 服务、会话、事件、模型、上下文 + 主程序入口（起后端 + 拉起 Ink）
工具.py            全部工具（file/ search/ git/ shell/ web/ …）与工具注册表
插件管理.py         插件宿主与契约、插件开发、团队、自动化
技能.py            技能仓库
权限.py            授权策略、审批档位、改动审核
沙箱.py            工作区上下文与路径沙箱
tui/              Ink 前端（app.js + package.json；node_modules 需自己 npm install）
skills/           内置技能源（4 个）
docs/_archive/    改动前快照（回退用：内联前的 186 个模块、40 个回归套件、Java 源码）
```

> **前后端怎么分工**：Python 侧负责全部能力（模型、工具、审批、会话、事件），
> 并且已经被 40 个回归套件验证过 —— 路由 114/114、业务插件 71/71、与原版结果完全一致
> （37 通过 / 1 失败 / 2 跳过）。Ink 前端只做渲染与交互，**走的是同一套 `/api/*`**，
> 所以换界面不会影响已验证的行为。

## 主要接口

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/api/chat` | 发消息（Agent 干活） |
| GET | `/api/plugins` | 插件清单（含类别与开关状态） |
| GET/POST | `/api/context` | 看 / 改上下文窗口 |
| GET | `/api/changes` | 待人工审核的改动 |
| GET | `/api/skills` | 技能清单 |
| GET | `/api/sessions` | 会话列表 |

## 许可

[MIT](LICENSE)。

## 致谢

- [llama.cpp](https://github.com/ggml-org/llama.cpp) —— 本地推理运行时
- [Qwen](https://github.com/QwenLM/Qwen) —— 底座模型架构
- [DeepSeek-Harness](https://github.com/deepseek-ai/dsh)、[Claude Code](https://github.com/anthropics/claude-code)
  —— Agent 循环、工具调用与事件溯源的思路参考
