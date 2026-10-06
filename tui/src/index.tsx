/**
 * Lion Code 终端界面 —— OpenTUI + SolidJS
 *
 * 【为什么是这套】它和 MiMo Code 的前端是同款技术栈（@opentui/core + @opentui/solid
 * + solid-js）。OpenTUI 靠 Bun 的原生 FFI 渲染（Node 下会报 "native FFI is not
 * available for this runtime"），所以必须用 bun 跑，不能用 node。
 *
 * 【它只做界面】所有能力都在 Python 后端（main.py 起的 HTTP 服务）：
 *   POST /api/workspaces → POST /api/sessions → SSE POST /api/chat/stream
 * SSE 帧形状：{type: TEXT|TOOL_CALL|DONE|ERROR, content, toolName, finished}
 */
import { render, useKeyboard, useTerminalDimensions } from "@opentui/solid"
import { createCliRenderer, RGBA, TextAttributes } from "@opentui/core"
import { For, createSignal, onMount } from "solid-js"

// ─────────────────────────────────────────── 命令行参数
const argv = process.argv.slice(2)
const arg = (name: string, dflt: string) => {
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i]
    if (a.startsWith(`--${name}=`)) return a.slice(name.length + 3)
    if (a === `--${name}` && argv[i + 1]) return argv[i + 1]
  }
  return dflt
}
const PORT = Number(arg("port", "8080"))
const WORKSPACE = arg("workspace", process.cwd())
const SELFTEST = argv.includes("--selftest")

// ─────────────────────────────────────────── 配色
// 直接取自 MiMo Code 的默认主题 context/theme/mimocode.json（dark 档）：
//   近黑底 + 橙色主色，蓝色只用于小标题 —— 这是它整套界面的辨识度所在。
const C = {
  bg: RGBA.fromHex("#0a0a0a"),          // darkStep1  background
  panel: RGBA.fromHex("#141414"),       // darkStep2  backgroundPanel
  element: RGBA.fromHex("#1e1e1e"),     // darkStep3  backgroundElement
  border: RGBA.fromHex("#484848"),      // darkStep7  border
  borderSubtle: RGBA.fromHex("#3c3c3c"),// darkStep6  borderSubtle
  text: RGBA.fromHex("#eeeeee"),        // darkStep12 text
  gray: RGBA.fromHex("#808080"),        // darkStep11 textMuted
  primary: RGBA.fromHex("#FF6A00"),     // darkStep9  primary（标志性橙）
  secondary: RGBA.fromHex("#FF8A3C"),   // darkSecondary
  accent: RGBA.fromHex("#818CF8"),      // darkAccent（小标题/关键字）
  err: RGBA.fromHex("#FB7185"),         // darkRed
  warn: RGBA.fromHex("#FBBF24"),        // darkOrange
  ok: RGBA.fromHex("#FF6A00"),          // darkGreen 在这套主题里就是橙色
  title: RGBA.fromHex("#FF6A00"),
  user: RGBA.fromHex("#FF6A00"),
  amber: RGBA.fromHex("#e5c07b"),       // darkYellow
  bar: RGBA.fromHex("#141414"),
}
const THINK = ["Pondering", "Noodling", "Percolating", "Musing", "Herding", "Crunching", "Simmering", "Smooshing"]

// ─────────────────────────────────────────── 后端调用
const base = () => `http://127.0.0.1:${PORT}`

async function jget(path: string): Promise<any> {
  try {
    const r = await fetch(base() + path)
    return await r.json()
  } catch (e) {
    return { success: false, message: String((e as Error)?.message || e) }
  }
}
async function jpost(path: string, body?: unknown): Promise<any> {
  try {
    const r = await fetch(base() + path, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: body === undefined ? undefined : JSON.stringify(body),
    })
    return await r.json()
  } catch (e) {
    return { success: false, message: String((e as Error)?.message || e) }
  }
}

/** 读 SSE：按行切，只认 `data:` 前缀，`[DONE]` 结束。 */
async function stream(body: unknown, onFrame: (f: any) => void, signal: AbortSignal) {
  const res = await fetch(base() + "/api/chat/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    signal,
  })
  if (!res.body) throw new Error(`后端没有返回流（HTTP ${res.status}）`)
  const reader = res.body.getReader()
  const dec = new TextDecoder()
  let buf = ""
  for (;;) {
    const { done, value } = await reader.read()
    if (done) break
    buf += dec.decode(value, { stream: true })
    let nl = 0
    while ((nl = buf.indexOf("\n")) >= 0) {
      const line = buf.slice(0, nl).trim()
      buf = buf.slice(nl + 1)
      if (!line.startsWith("data:")) continue
      const raw = line.slice(5).trim()
      if (!raw || raw === "[DONE]") continue
      try {
        onFrame(JSON.parse(raw))
      } catch {
        /* 半截帧，丢掉 */
      }
    }
  }
}

// ─────────────────────────────────────────── 行模型
type Span = { t: string; c: RGBA; bold?: boolean }
type Line = Span[]
const S = (t: string, c: RGBA, bold = false): Span => ({ t, c, bold })
const cut = (s: string, n: number) => (s.length > n ? s.slice(0, n - 1) + "…" : s)
/** 全角算 2 格的宽度（中文对齐用） */
const wid = (s: string) => [...s].reduce((n, ch) => n + (/[\u1100-\u115F\u2E80-\uA4CF\uAC00-\uD7A3\uF900-\uFAFF\uFE30-\uFE6F\uFF00-\uFF60\uFFE0-\uFFE6]/.test(ch) ? 2 : 1), 0)
const pad = (s: string, n: number) => s + " ".repeat(Math.max(0, n - wid(s)))
function wrap(s: string, width: number): string[] {
  const out: string[] = []
  for (const para of String(s).split("\n")) {
    let cur = ""
    for (const ch of para) {
      if (wid(cur) + wid(ch) > width) {
        out.push(cur)
        cur = ""
      }
      cur += ch
    }
    out.push(cur)
  }
  return out
}

// ─────────────────────────────────────────── 界面
function App() {
  const dims = useTerminalDimensions()
  const [lines, setLines] = createSignal<Line[]>([])
  const [input, setInput] = createSignal("")
  const [stream_, setStream] = createSignal("")
  const [busy, setBusy] = createSignal(false)
  const [tick, setTick] = createSignal(0)
  const [model, setModel] = createSignal("默认模型")
  const [session, setSession] = createSignal("新会话")
  const [port, setPort] = createSignal("")
  const [stats, setStats] = createSignal({ tokens: 0, limit: 16384, spent: 0 })
  const [scroll, setScroll] = createSignal(0)

  // 尺寸兜底：拿不到终端尺寸时不能让它变 NaN（NaN 传给布局会把渲染炸掉）
  const W = () => {
    const d: any = dims()
    const w = Number(d?.width)
    return Number.isFinite(w) && w > 20 ? w : 80
  }
  const H = () => {
    const d: any = dims()
    const hh = Number(d?.height)
    return Number.isFinite(hh) && hh > 6 ? hh : 24
  }

  let sid = ""
  let abort: AbortController | null = null

  const say = (...ls: Line[]) => setLines((v) => [...v, ...ls])
  const sayText = (t: string, c = C.text, indent = "  ") => say(wrap(indent + t, Math.max(20, W() - 2)).map((l) => [S(l, c)]))

  
  const refresh = async () => {
    const ctx = (await jget("/api/context")).context || {}
    const m = (await jget("/api/runtime/mode")).data || {}
    setStats({ tokens: Number(ctx.tokensUsed || 0), limit: Number(ctx.sessionLimit || 16384), spent: Number(ctx.costUsd || 0) })
    if (m.model) setModel(String(m.model))
    const s = (await jget("/api/sessions")).data || []
    if (Array.isArray(s) && s.length) setSession(String(s[s.length - 1].name || s[s.length - 1].id || "会话"))
  }

  const ensureSession = async () => {
    if (sid) return sid
    const ws = await jpost("/api/workspaces", { path: WORKSPACE })
    const wid_ = ws?.data?.id || (await jget("/api/workspaces/default"))?.data?.id
    const made = await jpost("/api/sessions", { workspaceId: wid_, mode: "STANDARD" })
    sid = String(made?.data?.id || made?.data?.sessionId || "")
    if (made?.data?.name) setSession(String(made.data.name))
    return sid
  }

  const send = async (text: string) => {
    sayText("▌ " + text, C.title, "")
    setBusy(true)
    setStream("")
    abort = new AbortController()
    let acc = ""
    try {
      const s = await ensureSession()
      await stream({ sessionId: s, message: text, thinkingLevel: "HIGH" }, (f) => {
        const type = String(f.type || "").toUpperCase()
        if (type === "TEXT") {
          acc += String(f.content || "")
          setStream(acc)
        } else if (type === "TOOL_CALL") {
          if (acc) {
            say(...wrap(acc, W() - 4).map((l) => [S("  " + l, C.text)]))
            acc = ""
            setStream("")
          }
          const name = String(f.toolName || "tool")
          const detail = String(f.content || "")
          say([S("  ⏺ ", C.ok), S(name, C.text, true), S(detail ? `(${cut(detail, 50)})` : "()", C.gray)])
        } else if (type === "ERROR") {
          say([S("  ✗ " + cut(String(f.content || "未知错误"), W() - 6), C.err)])
        }
      }, abort.signal)
      if (acc) say(...wrap(acc, W() - 4).map((l) => [S("  " + l, C.text)]))
    } catch (e) {
      if ((e as Error)?.name !== "AbortError") say([S("  ✗ " + cut(String((e as Error)?.message || e), W() - 6), C.err)])
    }
    setStream("")
    setBusy(false)
    abort = null
    refresh()
  }

  const doCommand = async (raw: string): Promise<boolean> => {
    const [cmd, ...rest] = raw.trim().split(/\s+/)
    const a = rest.join(" ")
    switch (cmd) {
      case "/help":
        say([S("  命令", C.title, true)])
        for (const [k, v] of [["/new", "开新会话"], ["/sessions", "列出会话"], ["/status", "状态"], ["/tools", "工具清单"],
                              ["/skills", "技能清单"], ["/plugins", "插件清单"], ["/mode local|custom", "模型来源"],
                              ["/clear", "清屏"], ["/exit", "退出"]] as [string, string][]) {
          say([S("  " + pad(k, 22), C.amber), S(v, C.gray)])
        }
        return true
      case "/new": {
        sid = ""
        await ensureSession()
        say([S("  ✓ 新会话", C.ok)])
        return true
      }
      case "/sessions": {
        const list = (await jget("/api/sessions")).data || []
        say([S("  会话", C.title, true)])
        for (const s of list.slice(-12)) say([S("  " + cut(String(s.id || ""), 12), C.gray), S("  " + cut(String(s.name || ""), 40), C.text)])
        return true
      }
      case "/status":
        await refresh()
        say([S("  状态", C.title, true)])
        for (const [k, v] of [["模型", model()], ["会话", session()], ["工作区", WORKSPACE],
                              ["上下文", `${stats().tokens}/${stats().limit}`], ["后端", `127.0.0.1:${PORT}`]] as [string, string][]) {
          say([S("  " + pad(k, 8), C.gray), S(v, C.text)])
        }
        return true
      case "/tools": {
        const t = (await jget("/api/tools")).data || []
        say([S(`  工具 ${Array.isArray(t) ? t.length : 0} 个`, C.title, true)])
        for (const x of (Array.isArray(t) ? t : []).slice(0, 40)) say([S("  " + cut(String(x.name || x.id || x), 34), C.amber)])
        return true
      }
      case "/skills": {
        const t = (await jget("/api/skills")).data || []
        say([S("  技能", C.title, true)])
        for (const x of (Array.isArray(t) ? t : [])) say([S("  " + cut(String(x.name || x.id || x), 34), C.amber)])
        return true
      }
      case "/plugins": {
        const t = (await jget("/api/plugins")).data || []
        say([S(`  插件 ${Array.isArray(t) ? t.length : 0} 个`, C.title, true)])
        for (const x of (Array.isArray(t) ? t : []).slice(0, 40)) say([S("  " + cut(String(x.name || x.id || x), 40), C.text)])
        return true
      }
      case "/mode": {
        const out = await jpost("/api/runtime/mode", { mode: a || "local" })
        say([S(out.success ? `  ✓ 模型来源 = ${a || "local"}` : "  ✗ " + (out.message || ""), out.success ? C.ok : C.err)])
        return true
      }
      case "/clear":
        setLines([])
        return true
      case "/exit":
      case "/quit":
        return false
      default:
        say([S("  ✗ 未知命令: " + cmd + "（/help 看命令）", C.err)])
        return true
    }
  }

  const submit = async () => {
    const text = input().trim()
    if (!text || busy()) return
    setInput("")
    if (text.startsWith("/")) {
      const keep = await doCommand(text)
      if (!keep) process.exit(0)
      return
    }
    await send(text)
  }

  useKeyboard((key: any) => {
    if (key?.ctrl && key?.name === "c") {
      if (busy() && abort) {
        abort.abort()
        jpost("/api/chat/control/stop", { sessionId: sid })
        say([S("  ✓ 已中断", C.ok)])
      } else {
        process.exit(0)
      }
      return
    }
    if (busy()) return
    if (key?.name === "return" || key?.name === "enter") return void submit()
    if (key?.name === "backspace") return setInput((v) => v.slice(0, -1))
    if (key?.name === "pageup") return setScroll((s) => s + 5)
    if (key?.name === "pagedown") return setScroll((s) => Math.max(0, s - 5))
    const seq = String(key?.sequence || "")
    if (!key?.ctrl && !key?.meta && seq.length === 1 && seq >= " ") setInput((v) => v + seq)
  })

  onMount(() => {
    // 思考词轮播：定时器只建一次，且只在忙时推进。
    // （原来放在组件顶层 —— 每次渲染都新建一个，既泄漏又和 Solid 的更新队列打架）
    setInterval(() => { if (busy()) setTick((t) => t + 1) }, 700)
    void (async () => {
      const rv = await jget("/api/runtime/version")
      const ver = rv?.data?.version || "1.5.46"
      say([S("  Lion Code", C.title, true), S(`  ${ver}`, C.gray)])
      say([S("  输入 /help 看命令 · Ctrl+C 退出 · 回车发送", C.gray)])
      await refresh()
      say([S("", C.text)])
    })()
  })

  const bodyH = () => Math.max(2, H() - 6)
  const visible = () => {
    const all = lines()
    const end = Math.max(0, all.length - scroll())
    return all.slice(Math.max(0, end - bodyH()), end)
  }
  const pct = () => (stats().limit ? Math.round((stats().tokens / stats().limit) * 100) : 0)
  const kNum = (n: number) => (n >= 1000 ? (n / 1000).toFixed(1) + "K" : String(n))

  return (
    <box flexDirection="column" width={W()} height={H()} backgroundColor={C.bg}>
      {/* 顶部标题栏 */}
      <box height={1} backgroundColor={C.bar} paddingLeft={1}>
        <text fg={C.text} attributes={TextAttributes.BOLD}>{`Lion Code · ${cut(session(), 40)}`}</text>
        <text fg={C.gray}>{`  ${cut(model(), 28)}`}</text>
      </box>

      {/* 对话区 */}
      <box flexGrow={1} flexDirection="column" overflow="hidden">
        <For each={visible()}>
          {(line) => (
            <box flexDirection="row">
              <For each={line}>
                {(sp) => <text fg={sp.c} attributes={sp.bold ? TextAttributes.BOLD : undefined}>{sp.t}</text>}
              </For>
            </box>
          )}
        </For>
        <For each={stream() ? wrap(stream(), W() - 4) : []}>
          {(l) => <text fg={C.text}>{`  ${l}`}</text>}
        </For>
      </box>

      {/* 输入框 */}
      <box backgroundColor={C.panel} paddingLeft={1} paddingRight={1} flexDirection="row">
        <text fg={busy() ? C.accent : C.user}>{"▌ "}</text>
        {busy() ? (
          <text fg={C.accent}>{`✻ ${THINK[tick() % THINK.length]}…`}</text>
        ) : (
          <text fg={input() ? C.text : C.gray}>{input() || "问点什么，或 /help 看命令"}</text>
        )}
        {busy() ? <text fg={C.gray}>{"   (esc to interrupt)"}</text> : null}
      </box>

      {/* 底部状态栏 */}
      <box height={1} backgroundColor={C.bar} paddingLeft={1}>
        <text fg={C.text}>{` ${kNum(stats().tokens)}/${kNum(stats().limit)} (${pct()}%) · $${stats().spent.toFixed(2)}`}</text>
        <text fg={C.gray}>{`${busy() ? "   esc to interrupt" : "   回车 发送   / 命令   Ctrl+C 退出"}`}</text>
      </box>
    </box>
  )
}

// ─────────────────────────────────────────── 启动
if (SELFTEST) {
  // 无 TTY 环境（CI / 我这边的验证）不能建渲染器，只验数据通路
  const ping = async () => {
    const v = await jget("/api/runtime/version")
    const m = await jget("/api/runtime/mode")
    const ws = await jpost("/api/workspaces", { path: WORKSPACE })
    const wid = ws?.data?.id
    const made = await jpost("/api/sessions", { workspaceId: wid, mode: "STANDARD" })
    const sid = made?.data?.id || made?.data?.sessionId
    console.log(`  版本: ${v?.data?.version}`)
    console.log(`  模型: ${m?.data?.model}`)
    console.log(`  工作区: ${wid}`)
    console.log(`  会话: ${sid}`)
    console.log(`  SSE   : ${sid ? "已建会话，可推流" : "建会话失败"}`)
    process.exit(0)
  }
  await ping()
} else {
  const renderer = await createCliRenderer({ exitOnCtrlC: false })
  await render(() => <App />, renderer)
}