# Lion Code 安装说明（随安装包附带）

双击 `StartLionCode.cmd`（或开始菜单 / 桌面的 **Lion Code** 快捷方式）即可启动。
它会打开一个终端窗口，按顺序拉起三段：**后端 :18080 → MiMo 接口适配层 :8791 → MiMo TUI**，
并带看门狗（后端/适配层崩了会自动拉起）。

## 模型有两种用法（安装包**不带**任何模型权重）

| 模式 | 怎么用 | 需要什么 |
| --- | --- | --- |
| **云端**（默认推荐） | 界面里 `/mode custom` + `/key <APIKey>`，或后端 `POST /api/runtime/mode`；本项目已端到端验证云端 `mimo-v2.6-flash` | 联网 + 云端 token |
| **本地 GGUF**（可选） | 把 `lion-merged-*.gguf`（4.87 GB 起）放进安装目录，`/mode local`；没有权重时后端会自动下载 Q8_0（8.87 GB） | 无需联网（权重就位后）；`runtime-vulkan\llama-server.exe` 已随包安装 |

## 首次安装**不需要**联网

MiMo TUI 的依赖（`MiMo-Code-main\node_modules`）以预压缩包 `node_modules.7z`
随安装包提供，安装结束时由 `install_deps.cmd` 解开并重建目录链接：

- 成功：安装目录下出现 `install-deps.ok`，日志在 `install-deps.log`（约 30–90 秒）
- 失败：**后端与适配层照常可用**（它们是编译好的 exe，不依赖 node_modules），
  只有第三段 MiMo TUI 起不来；重跑安装目录里的 `install_deps.cmd` 即可补齐

> 为什么不是安装时 `bun install`：本机实测 bun 的链接阶段在各种组合下
> （冷/热缓存、frozen 开关、三种 TEMP、干净目录）都报几百个
> `ENOENT ... failed to symlink`，同一命令早上还能成功、之后环境性失败。
> 预打包直接恢复**已验证可用**的依赖树，且安装完全离线。

## 日志 / 数据在哪

- 运行日志：`<安装目录>\.lbcheck\`（`watchdog.log`、`backend.log`、`adapter.log`、`frontend.log`）
  —— 安装目录不可写时自动回退到 `%LOCALAPPDATA%\LionCode\data\`
- 会话与配置（真正持久化的）：`%USERPROFILE%\.lioncode\`，与安装位置无关
- 依赖包压缩档与临时目录：`<安装目录>\node_modules.7z`、`<安装目录>\tmp\`
  （放在安装目录内：低完整性进程也能写，且卸载时一并删除）

## 卸载

控制面板 / 设置里卸载 **Lion Code**（或运行 `<安装目录>\unins000.exe`），
静默卸载：`unins000.exe /VERYSILENT /NORESTART`。
卸载会连同安装目录内的 `node_modules`、运行日志一起删掉。
