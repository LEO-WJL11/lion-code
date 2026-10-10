// Lion Code 终端界面 —— Ink（React for CLIs）
//
// 外观对齐 MiMo Code：
//   · 顶部标签栏（整行铺底色）
//   · 用户消息：左侧强调条 + 圆角框
//   · `+ Thought: 385ms` 折叠思考耗时
//   · 工具调用按分类成组：` - Read - main.py`（工具名琥珀色）
//   · 输入框：左强调条 + 框内 `Build · <模型> · <档位>`
//   · 底部整条状态栏：`24.7K/944K (3%) · $0.00  回车 发送 …`
//   · 右侧固定面板：Context / 工作目录 / LSP / cwd / 版本号
//
// 后端是 Python（`main.py --backend-only`），这里只做界面，走同一套 /api/* 接口。
// 【不用 JSX】用 `h = React.createElement` 直接写，省掉转译步骤 —— `node app.js` 就能跑。

import React, {useState, useEffect, useRef, useCallback, useMemo} from 'react';
import {render, Box, Text, Static, useInput, useStdout, useApp} from 'ink';
import TextInput from 'ink-text-input';
import fs from 'node:fs';
import {Readable} from 'node:stream';

const h = React.createElement;
const DBG = process.env.LIONBOX_TUI_DEBUG || '';
const dbg = (msg) => { if (DBG) { try { fs.appendFileSync(DBG, msg + '\n'); } catch { /* 忽略 */ } } };

// ─────────────────────────────────────────── 配色
const C = {
  text: '#e6e6e6',
  title: '#ffffff',
  amber: '#e5b567',
  userbar: '#ff7a5c',
  accent: '#7aa2f7',
  think: '#d7a65f',
  gray: '#8a8a8a',
  faint: '#4a4a4a',
  ok: '#9ece6a',
  err: '#f7768e',
  barBg: '#262626',
  tabBg: '#262626',
};

// Claude Code 那种"思考中"的俏皮词轮播（忙的时候显示在输入框位置）
const THINK_WORDS = [
  'Pondering', 'Noodling', 'Percolating', 'Musing', 'Herding', 'Crunching',
  'Simmering', 'Puttering', 'Vibing', 'Smooshing', 'Wrangling', 'Churning',
];

// ─────────────────────────────────────────── 工具分组（Claude Code 不画分组标题，这里只用来归类）
const GROUPS = [
  ['文件操作', ['read', 'write', 'edit', 'append', 'glob', 'grep', 'find', 'search_in',
                'list_dir', 'delete', 'move', 'copy', 'mkdir', 'chmod', 'patch',
                'head_tail', 'line_count', 'file_info', 'create_file', 'download']],
  ['终端', ['execute_command', 'run_command', 'shell', 'terminal', 'bash']],
  ['任务与代理', ['task', 'todo', 'spawn', 'agent', 'team', 'subagent', 'actor']],
  ['记忆与历史', ['memory', 'history', 'skill', 'context', 'recall']],
  ['调度与交互', ['cron', 'automation', 'question', 'ask_user', 'approval']],
  ['网络', ['web', 'fetch', 'http']],
];

const SHORT = {
  read_file: 'Read', write_file: 'Write', modify_file: 'Edit', append_file: 'Append',
  glob_files: 'Glob', search_in_files: 'Grep', list_directory: 'List',
  head_tail_file: 'HeadTail', read_multiple_files: 'ReadMany', create_file: 'Create',
  delete_file: 'Delete', move_file: 'Move', copy_file: 'Copy', file_info: 'Stat',
  line_count: 'LineCount', download_file: 'Download', create_directory: 'Mkdir',
  execute_command: 'Bash', run_command: 'Bash', web_search: 'WebSearch',
  fetch_url: 'WebFetch', http_get: 'HttpGet', http_post: 'HttpPost',
  skill_load: 'Skill', ask_user: 'Question', agent_spawn: 'Actor',
  agent_team_run: 'Actor', agent_team: 'Team', agent_loop: 'Loop',
  context_window: 'Context', context_prune: 'Prune', cron_parse: 'Cron',
  approval_review: 'Review', subagent: 'Subagent', terminal: 'Terminal',
};

function groupOf(name) {
  const low = String(name || '').toLowerCase();
  for (const [g, keys] of GROUPS) if (keys.some((k) => low.includes(k))) return g;
  return '其它';
}

function pretty(name) {
  if (SHORT[name]) return SHORT[name];
  return String(name || 'tool').split('_').map((s) => s.charAt(0).toUpperCase() + s.slice(1)).join('');
}

// 从工具入参里挑一个最能说明问题的值：Read 的 path、Bash 的 command、Grep 的 pattern…
// Claude Code 的写法就是 `⏺ Read(README.md)` —— 括号里只放这一个关键参数。
function argOf(raw) {
  const s = String(raw == null ? '' : raw).trim();
  if (!s) return '';
  if (s.startsWith('{')) {
    try {
      const o = JSON.parse(s);
      for (const k of ['path', 'file_path', 'command', 'pattern', 'query', 'url',
                       'name', 'id', 'sessionId', 'providerId']) {
        if (o[k] !== undefined && o[k] !== null && String(o[k]) !== '') return String(o[k]);
      }
      const first = Object.values(o).find((v) => v !== null && v !== undefined && v !== '');
      return first === undefined ? '' : String(first);
    } catch { /* 不是完整 JSON（流式截断），按原文用 */ }
  }
  return s;
}

// `⏺ Read(README.md)` + 结果行 `  ⎿  Read 3 lines`（Claude Code 的两个标志性形状）
const callSpans = (name, detail, room) => [
  S('  ⏺ ', C.ok),
  S(pretty(name), C.text, {bold: true}),
  S(`(${cut(argOf(detail), Math.max(8, room - 20))})`, C.gray),
];

const resultSpans = (text, bad, room) => {
  const first = String(text == null ? '' : text).split('\n').find((l) => l.trim()) || '完成';
  return [S('    ⎿  ', bad ? C.err : C.gray),
          S(cut(first.trim(), Math.max(8, room - 10)), bad ? C.err : C.gray)];
};

const wid = (s) => [...String(s)].reduce(
  (n, ch) => n + (/[\u1100-\u115F\u2E80-\uA4CF\uAC00-\uD7A3\uF900-\uFAFF\uFE30-\uFE4F\uFF00-\uFF60\uFFE0-\uFFE6]/.test(ch) ? 2 : 1), 0);
const cut = (s, n) => {
  s = String(s ?? '');
  if (wid(s) <= n) return s;
  let out = '', w = 0;
  for (const ch of s) { const cw = wid(ch); if (w + cw > n - 1) break; out += ch; w += cw; }
  return out + '…';
};
const pad = (s, n) => s + ' '.repeat(Math.max(0, n - wid(s)));
const wrap = (s, n) => {
  const lines = [];
  for (const raw of String(s ?? '').split('\n')) {
    let cur = '', w = 0;
    for (const ch of raw) {
      const cw = wid(ch);
      if (w + cw > n) { lines.push(cur); cur = ''; w = 0; }
      cur += ch; w += cw;
    }
    lines.push(cur);
  }
  return lines;
};

// 一行 = 若干 span，这样"工具名琥珀色 + 说明灰色"能在一行内混排
const S = (t, c, extra) => ({t: String(t ?? ''), c: c || C.text, ...(extra || {})});

// ─────────────────────────────────────────── HTTP + SSE
const base = (port) => `http://127.0.0.1:${port}`;

async function jget(port, path) {
  try {
    const r = await fetch(base(port) + path);
    return await r.json();
  } catch (e) {
    return {success: false, message: String(e && e.message || e)};
  }
}

async function jpost(port, path, body, method) {
  try {
    const r = await fetch(base(port) + path, {
      method: method || 'POST',
      headers: {'Content-Type': 'application/json'},
      body: body === undefined ? undefined : JSON.stringify(body),
    });
    const txt = await r.text();
    try { return JSON.parse(txt); } catch { return {success: r.ok, raw: txt}; }
  } catch (e) {
    return {success: false, message: String(e && e.message || e)};
  }
}

// 【切换端点后必须再推一次适配器】`/api/runtime/mode` 只写配置；
// 活跃适配器的 baseUrl 是装配时固化进去的，光改配置它不会跟着变 ——
// 实测现象就是"端点改成功了，请求照样打到 127.0.0.1:8788（积极拒绝）"。
// `POST /api/chat/adapter/config` 是唯一能真正推给适配器的入口
// （它那边拿得到 ApiContext → AdapterManager → adapter.update_config）。
async function pushAdapter(port, baseUrl, apiKey, model) {
  return jpost(port, '/api/chat/adapter/config', {
    adapterType: 'OPENAI_COMPATIBLE',
    ...(baseUrl ? {baseUrl} : {}),
    ...(apiKey ? {apiKey} : {}),
    ...(model ? {model} : {}),
  });
}

async function runStream(port, body, onFrame, signal) {
  const r = await fetch(base(port) + '/api/chat/stream', {
    method: 'POST',
    headers: {'Content-Type': 'application/json', Accept: 'text/event-stream'},
    body: JSON.stringify(body),
    signal,
  });
  if (!r.body) return;
  const reader = r.body.getReader();
  const dec = new TextDecoder();
  let buf = '';
  for (;;) {
    const {done, value} = await reader.read();
    if (done) break;
    buf += dec.decode(value, {stream: true});
    let i;
    while ((i = buf.indexOf('\n\n')) >= 0) {
      const frame = buf.slice(0, i);
      buf = buf.slice(i + 2);
      for (const ln of frame.split('\n')) {
        const s = ln.trim();
        if (!s.startsWith('data:')) continue;
        try { onFrame(JSON.parse(s.slice(5).trim())); } catch { /* 忽略坏帧 */ }
      }
    }
  }
}

// ─────────────────────────────────────────── 非 TTY 输入通道
// 被管道喂输入时 Ink 的 raw mode 不可用（setRawMode 会抛），所以不用 useInput，
// 而是把 stdin 的每一行喂进同一个提交通道 —— 这样自动化测试和脚本化调用都能跑。
const feedQ = [];
const feedWait = [];
function feed(line) {
  if (feedWait.length) feedWait.shift()(line);
  else feedQ.push(line);
}
function nextLine() {
  return new Promise((res) => (feedQ.length ? res(feedQ.shift()) : feedWait.push(res)));
}

// ─────────────────────────────────────────── 界面
function App({port, workspace}) {
  const {exit} = useApp();
  const {stdout} = useStdout();
  const [cols, setCols] = useState(stdout.columns || 100);
  const [rows, setRows] = useState(stdout.rows || 30);
  const [lines, setLines] = useState([]);        // 已经定稿的对话行（span 数组）
  const [stream, setStream] = useState(null);    // 正在流的那一段文本
  const [busy, setBusy] = useState(false);
  const [word, setWord] = useState(0);            // 思考词轮播（Claude Code 那种）
  const [thinking, setThinking] = useState(0);   // 已等待毫秒（转圈用）
  const [input, setInput] = useState('');
  const [prompt, setPrompt] = useState(null);    // 正在问用户（ask_user / 改动审核）
  const [scroll, setScroll] = useState(0);       // 0 = 贴底
  const [status, setStatus] = useState('就绪');
  const [session, setSession] = useState(null);
  const [sessionName, setSessionName] = useState('新会话');
  const [stats, setStats] = useState({tokens: 0, limit: 16384, tps: 0, spent: 0});
  const [model, setModel] = useState('默认模型');
  const [provider, setProvider] = useState('local');
  const [level, setLevel] = useState('high');
  const [version, setVersion] = useState('1.5.46');
  const [showSide, setShowSide] = useState(true);

  const busyRef = useRef(false);
  const sessionRef = useRef(null);
  const abortRef = useRef(null);
  const lastEventMs = useRef(0);
  const seenEvents = useRef(new Set());
  const groupRef = useRef(null);
  const toolSeq = useRef({});
  const renderedTools = useRef(new Set());
  const pendingQueue = useRef([]);               // 待处理的"提问"（一次只显示一个）
  const mainWRef = useRef(80);                   // 主栏宽度（喂给画框/折行用）

  // 终端尺寸变化
  useEffect(() => {
    const on = () => { setCols(stdout.columns || 100); setRows(stdout.rows || 30); };
    stdout.on('resize', on);
    return () => stdout.off('resize', on);
  }, [stdout]);

  const push = useCallback((...ls) => {
    setLines((prev) => [...prev, ...ls]);
  }, []);
  // 按主栏宽度折行再入列 —— 不折的话 Ink 会自己折，续行会顶到最左边，很难看
  const pushText = useCallback((text, indent = '') => {
    const w = Math.max(20, mainWRef.current - 4 - indent.length);
    push(...wrap(text, w).map((l) => [S(indent + l, C.gray)]));
  }, [push]);

  // ── 启动：版本 / 上下文 / 模型来源
  useEffect(() => {
    (async () => {
      const rv = await jget(port, '/api/runtime/version');
      if (rv && rv.data && rv.data.version) setVersion(String(rv.data.version));
      // 开场横幅：跟对话一起滚进回滚缓冲（不做常驻顶栏 —— 常驻元素必须留在
      // Ink 的动态区里，而动态区越小越稳）。
      push([],
        [S('  Lion Code · 终端版 AI 编程 Agent', C.title, {bold: true})],
        [S('  输入 /help 看命令 · Esc/Ctrl+C 中断当前任务 · /exit 退出', C.gray)]);
      await refreshStats();
      const local = (await jget(port, '/api/runtime/local')).data || {};
      // 【云端 API 版】本地模型已停用：不再提示"把 llama.cpp 放回去"那条路 ——
      // 留一个点了没反应的入口比没有入口更糟。只说云端怎么配。
      if (local.disabled) {
        pushText('· 云端 API 版：本地模型已停用（不下载权重、不拉起 llama-server）。', '  ');
        pushText('  配云端：/key <你的APIKey>（默认走小米 MiMo），或 /endpoint <URL>', '  ');
      } else if (!(local.modelInstalled && local.runtimeInstalled)) {
        pushText('! 本地模型还没就绪，直接提问会失败。两条路：', '  ');
        pushText('1) 把 llama.cpp 运行时放回 python/runtime-vulkan/（模型权重已在仓库里）', '  ');
        pushText('2) 用云端：/key <你的APIKey>（默认走小米 MiMo），或 /endpoint <URL>', '  ');
      }
    })();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const refreshStats = useCallback(async () => {
    const ctx = (await jget(port, '/api/context')).context || {};
    const mode = (await jget(port, '/api/runtime/mode')).data || {};
    if (mode.mode || mode.providerMode) setProvider(String(mode.mode || mode.providerMode));
    if (mode.model) setModel(String(mode.model));
    let tokens = 0;
    const sid = sessionRef.current;
    if (sid) {
      const hist = (await jget(port, `/api/sessions/${sid}/history`)).data || [];
      tokens = Math.round(hist.reduce((n, m) => n + String(m.content || '').length, 0) / 2.4);
    }
    setStats((s) => ({...s, tokens, limit: Number(ctx.sessionLimit) || s.limit}));
  }, [port]);

  const ensureSession = useCallback(async (name) => {
    if (sessionRef.current) {
      if (name) {
        await jpost(port, `/api/sessions/${sessionRef.current}/name`, {name}, 'PUT');
        setSessionName(name);
      }
      return sessionRef.current;
    }
    let sid = null;
    const ws = await jpost(port, '/api/workspaces', {path: workspace});
    if (ws.data && ws.data.id) sid = ws.data.id;
    if (!sid) {
      const d = (await jget(port, '/api/workspaces/default')).data || {};
      sid = d.id || d.workspaceId;
    }
    if (!sid) return null;
    const made = await jpost(port, '/api/sessions', {workspaceId: sid, mode: 'STANDARD'});
    const id = made.data && (made.data.id || made.data.sessionId);
    if (!id) return null;
    sessionRef.current = id;
    setSession(id);
    lastEventMs.current = 0;
    seenEvents.current = new Set();
    if (name) {
      await jpost(port, `/api/sessions/${id}/name`, {name}, 'PUT');
      setSessionName(name);
    } else {
      setSessionName(id.slice(0, 8));
    }
    return id;
  }, [port, workspace]);

  // ── 工具事件（比流式块更细：调用/完成/失败）
  const pollEvents = useCallback(async () => {
    const sid = sessionRef.current;
    if (!sid) return;
    const res = await jget(port, `/api/events/${sid}?after=${lastEventMs.current}`);
    for (const ev of (res.data || [])) {
      const key = String(ev.eventId || ev.id || '');
      if (key && seenEvents.current.has(key)) continue;
      if (key) seenEvents.current.add(key);
      if (Number(ev.timestamp) > lastEventMs.current) lastEventMs.current = Number(ev.timestamp);
      const type = String(ev.type || '').toUpperCase();
      if (!type.includes('TOOL')) continue;
      const data = ev.data && typeof ev.data === 'object' ? ev.data : {};
      const name = String(data.toolName || data.name || 'tool');
      if (type.includes('START') || type.includes('CALL')) {
        if (!renderedTools.current.has(name)) {
          renderedTools.current.add(name);
          push(callSpans(name, data.args || data.input || '', mainWRef.current));
        }
      } else if (type.includes('FAIL') || type.includes('ERROR')) {
        push(resultSpans(ev.summary || '失败', true, mainWRef.current));
      } else if (/END|COMPLETE|FINISH|RESULT/.test(type)) {
        push(resultSpans(ev.summary || '完成', false, mainWRef.current));
      }
    }
  }, [port, cols, push]);

  // 忙的时候轮播思考词（Claude Code 的 ✻ Pondering… 效果）
  useEffect(() => {
    if (!busy) return undefined;
    const t = setInterval(() => setWord((w) => w + 1), 700);
    return () => clearInterval(t);
  }, [busy]);

  // ── 后端在问问题（ask_user）
  const pollQuestion = useCallback(async () => {
    const sid = sessionRef.current;
    if (!sid) return;
    const res = await jget(port, `/api/questions/pending?sessionId=${encodeURIComponent(sid)}`);
    const q = res.data;
    if (!q || typeof q !== 'object') return;
    const id = q.id || q.questionId;
    if (pendingQueue.current.some((p) => p.id === id)) return;
    pendingQueue.current.push({
      kind: 'question', id,
      text: String(q.question || q.text || ''),
      options: q.options || [],
    });
  }, [port]);

  // ── 等待放行的改动
  const pollChanges = useCallback(async () => {
    const res = await jget(port, '/api/changes');
    if (!res.enabled) return;
    for (const ch of (res.changes || [])) {
      const id = ch.id;
      if (pendingQueue.current.some((p) => p.id === id)) continue;
      pendingQueue.current.push({
        kind: 'change', id,
        text: String(ch.path || ch.filePath || ''),
        diff: String(ch.diff || ch.patch || ''),
      });
    }
  }, [port]);

  // ── 提问/改动：串行地弹给用户
  useEffect(() => {
    if (prompt || busy || !lines.length) return;
    const next = pendingQueue.current.shift();
    if (next) setPrompt(next);
  }, [lines, busy, prompt]);

  // ── 发一条消息
  const send = useCallback(async (text) => {
    const sid = await ensureSession();
    if (!sid) { push([S('✗ 建会话失败', C.err)]); return; }
    // 用户消息：左侧强调条 + 圆角框（参考图第一块就是它）
    // 宽度要对齐：上边框 = ╭ + bw 个 ─ + ╮（bw+2 列），
    // 所以正文行 = ▌ + 正文补齐到 bw + │ = bw+2 ✓ 差一列边框就会歪。
    const bw = Math.max(20, mainWRef.current - 6);
    const body = wrap(text, bw);
    push([],
      [S('╭' + '─'.repeat(bw) + '╮', C.faint)],
      ...body.map((l) => [S('▌', C.userbar), S(pad(l, bw), C.text), S('│', C.faint)]),
      [S('╰' + '─'.repeat(bw) + '╯', C.faint)]);
    busyRef.current = true;
    setBusy(true);
    setStatus('生成中');
    groupRef.current = null;
    renderedTools.current = new Set();
    toolSeq.current = {};
    const ctrl = new AbortController();
    abortRef.current = ctrl;
    const t0 = Date.now();
    let sawThought = false;
    let acc = '';
    try {
      await runStream(port, {
        sessionId: sid, message: text, thinkingLevel: level.toUpperCase(),
        ...(model && model !== '默认模型' ? {model} : {}),
      }, (frame) => {
        const type = String(frame.type || '').toUpperCase();
        if (type === 'TEXT') {
          if (!sawThought) {
            sawThought = true;
            push([S(`+ Thought: ${Date.now() - t0}ms`, C.think)]);
          }
          acc += String(frame.content || '');
          setStream(acc);
        } else if (type === 'TOOL_CALL') {
          if (!sawThought) {
            sawThought = true;
            push([S(`+ Thought: ${Date.now() - t0}ms`, C.think)]);
          }
          const name = String(frame.toolName || 'tool');
          const detail = String(frame.content || '');
          toolSeq.current[name] = (toolSeq.current[name] || 0) + 1;
          const out = [];
          if (toolSeq.current[name] % 2 === 1) {
            out.push(callSpans(name, detail, mainWRef.current));
            renderedTools.current.add(name);
          } else {
            out.push(resultSpans(detail, false, mainWRef.current));
          }
          if (acc) { push(...wrap(acc, Math.max(20, mainWRef.current - 4)).map((l) => [S('  ' + l, C.text)])); acc = ''; setStream(null); }
          push(...out);
        } else if (type === 'ERROR') {
          pushText('✗ ' + String(frame.content || '未知错误'), '');
        }
      }, ctrl.signal);
    } catch (e) {
      if (!(e && e.name === 'AbortError')) pushText('✗ ' + String(e && e.message || e), '');
    }
    if (acc) push(...wrap(acc, Math.max(20, mainWRef.current - 4)).map((l) => [S('  ' + l, C.text)]));
    setStream(null);
    busyRef.current = false;
    setBusy(false);
    setStatus('就绪');
    abortRef.current = null;
    await refreshStats();
    const secs = Math.max(0.01, (Date.now() - t0) / 1000);
    setStats((s) => ({...s, tps: Math.round(s.tokens / secs)}));
  }, [port, cols, level, model, ensureSession, push, refreshStats]);

  // ── 斜杠命令
  const handleCommand = useCallback(async (raw) => {
    const [cmd, ...rest] = raw.trim().split(/\s+/);
    const arg = rest.join(' ');
    const say = (...ls) => push(...ls);
    switch (cmd) {
      case '/exit': case '/quit': exit(); return true;
      case '/help': {
        const items = [
          ['/new [名字]', '开一个新会话'], ['/sessions', '列出会话'],
          ['/use <id前缀>', '切换会话'], ['/history', '打印历史'],
          ['/mode local|custom', '切换模型来源'], ['/key <APIKey>', '填云端 Key（MiMo）'],
          ['/endpoint <URL> [模型]', '任意 OpenAI 兼容端点'], ['/model <名字>', '指定模型'],
          ['/level low|medium|high|max', '思考档位'], ['/ctx <数字>', '上下文窗口'],
          ['/tools', '按分组看工具'], ['/skills', '技能清单'],
          ['/approvals [auto|confirm]', '审批档位'], ['/changes', '待放行的改动'],
          ['/plugins', '插件清单'], ['/status', '状态'], ['/stop', '中断当前任务'],
          ['/panel', '开关右侧面板'], ['/clear', '清屏'], ['/exit', '退出'],
        ];
        say([S('命令', C.title, {bold: true})]);
        for (const [n, d] of items) say([S(' ' + pad(n, 28), C.accent), S(d, C.gray)]);
        return true;
      }
      case '/tools': {
        const list = (await jget(port, '/api/plugins')).data || [];
        const byGroup = {};
        for (const p of list) {
          const kind = String(p.kind || '');
          if (!/TOOL/.test(kind)) continue;
          const name = String(p.name || p.id || '');
          if (!name) continue;
          (byGroup[groupOf(name)] = byGroup[groupOf(name)] || []).push([name, String(p.description || '')]);
        }
        for (const [g] of GROUPS.concat([['其它', []]])) {
          const items = byGroup[g] || [];
          if (!items.length) continue;
          say([], [S(g, C.title, {bold: true})]);
          for (const [name, desc] of items) {
            say([S(' - ', C.gray), S(pretty(name), C.amber), S(' - ' + cut(desc, cols - 30), C.gray)]);
          }
        }
        return true;
      }
      case '/panel': {
        const p = stats.limit ? Math.round((stats.tokens / stats.limit) * 100) : 0;
        say([S('状态', C.title, {bold: true})]);
        for (const [k, v] of [
          ['Context', `≈${stats.tokens.toLocaleString()} tokens · ${p}% used · limit ${stats.limit}`],
          ['速度', `${stats.tps} t/s · $${stats.spent.toFixed(2)} spent`],
          ['工作目录', workspace],
          ['LSP', '未接入 LSP 子系统'],
          ['cwd', process.cwd()],
          ['版本', `Lion Code ${version}`],
        ]) {
          say([S(' ' + pad(k, 10), C.gray), S(String(v), C.text)]);
        }
        return true;
      }
      case '/clear': setLines([]); return true;
      case '/new': { sessionRef.current = null; setSession(null); setSessionName(arg || '新会话');
        await ensureSession(arg || undefined); say([S('✓ 新会话 ' + (sessionRef.current || ''), C.ok)]); return true; }
      case '/sessions': {
        const list = (await jget(port, '/api/sessions')).data || [];
        if (!list.length) say([S('(没有会话)', C.gray)]);
        for (const s of list) say([S((String(s.id) === String(sessionRef.current) ? '* ' : '  ') +
          String(s.id).slice(0, 8) + '  ' + (s.name || '(未命名)'), C.gray)]);
        return true;
      }
      case '/use': {
        const list = (await jget(port, '/api/sessions')).data || [];
        const hit = list.filter((s) => String(s.id).startsWith(arg));
        if (hit.length !== 1) say([S(`✗ 匹配到 ${hit.length} 个会话`, C.err)]);
        else { sessionRef.current = String(hit[0].id); setSession(hit[0].id);
          setSessionName(hit[0].name || ''); lastEventMs.current = 0; seenEvents.current = new Set();
          say([S('✓ 已切到 ' + hit[0].id, C.ok)]); }
        return true;
      }
      case '/history': {
        const sid = sessionRef.current; if (!sid) return true;
        const hist = (await jget(port, `/api/sessions/${sid}/history`)).data || [];
        for (const m of hist) say([S(`[${m.role}] ` + cut(String(m.content || '').replace(/\n/g, ' '), cols - 16), C.gray)]);
        return true;
      }
      case '/mode': {
        if (arg !== 'local' && arg !== 'custom') { say([S('用法：/mode local|custom', C.gray)]); return true; }
        const body = {mode: arg};
        if (arg === 'custom') { body.baseUrl = 'https://api.xiaomimimo.com/v1'; body.model = model === '默认模型' ? 'mimo-v2.6-flash' : model; }
        const out = await jpost(port, '/api/runtime/mode', body);
        if (out.success && arg === 'custom') {
          await pushAdapter(port, body.baseUrl, '', body.model);
        }
        say([S(out.success ? '✓ 模型来源 = ' + arg : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
        await refreshStats(); return true;
      }
      case '/key': {
        const out = await jpost(port, '/api/runtime/mode', {
          mode: 'custom', apiKey: arg, baseUrl: 'https://api.xiaomimimo.com/v1',
          model: model === '默认模型' ? 'mimo-v2.6-flash' : model});
        if (out.success) {
          await pushAdapter(port, 'https://api.xiaomimimo.com/v1', arg,
            model === '默认模型' ? 'mimo-v2.6-flash' : model);
        }
        say([S(out.success ? '✓ Key 已保存（走 MiMo）' : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
        await refreshStats(); return true;
      }
      case '/endpoint': {
        const [url, m] = arg.split(/\s+/);
        if (!url) { say([S('用法：/endpoint http://host:port/v1 [模型]', C.gray)]); return true; }
        const out = await jpost(port, '/api/runtime/mode', {mode: 'custom', baseUrl: url, model: m || 'local'});
        if (out.success) {
          setModel(m || 'local');
          const pushed = await pushAdapter(port, url, '', m || 'local');
          if (!pushed.success) say([S('  （适配器未能重指：' + (pushed.message || '') + '）', C.gray)]);
        }
        say([S(out.success ? `✓ 端点 = ${url}` : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
        await refreshStats(); return true;
      }
      case '/model': setModel(arg || '默认模型'); say([S('✓ 模型 = ' + (arg || '默认'), C.ok)]); return true;
      case '/level': {
        if (!/^(low|medium|high|max)$/i.test(arg)) { say([S('用法：/level low|medium|high|max', C.gray)]); return true; }
        setLevel(arg.toLowerCase()); say([S('✓ 档位 = ' + arg.toLowerCase(), C.ok)]); return true;
      }
      case '/ctx': {
        if (/^\d+$/.test(arg)) { const out = await jpost(port, '/api/context', {sessionLimit: Number(arg)});
          say([S(out.success ? `✓ 上下文 = ${arg}` : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
          await refreshStats(); }
        else say([S('当前 ' + stats.limit, C.gray)]);
        return true;
      }
      case '/skills': {
        const r = await jget(port, '/api/skills');
        for (const s of (r.skills || [])) say([S(`${s.id}  ${s.displayName || s.name}  `, C.gray),
          S(cut(String(s.description || ''), cols - 40), C.gray)]);
        return true;
      }
      case '/approvals': {
        if (arg === 'auto' || arg === 'confirm') {
          const data = (await jget(port, '/api/approvals')).data || [];
          const out = await jpost(port, '/api/approvals', {policies: data.map((d) => ({
            toolId: d.toolId, policy: arg === 'auto' ? 'AUTO_APPROVE' : 'CONFIRM'}))});
          say([S(out.success ? `✓ 全部工具 = ${arg}` : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
          return true;
        }
        const data = (await jget(port, '/api/approvals')).data || [];
        const cnt = data.reduce((m, d) => (m[d.policy] = (m[d.policy] || 0) + 1, m), {});
        say([S(Object.entries(cnt).map(([k, v]) => `${k}: ${v}`).join('，') || '(空)', C.gray)]);
        return true;
      }
      case '/changes': { const r = await jget(port, '/api/changes');
        say([S(`待放行 ${r.pendingCount || 0} 个`, C.gray)]); await pollChanges(); return true; }
      case '/plugins': {
        const list = (await jget(port, '/api/plugins')).data || [];
        say([S(`共 ${list.length} 个插件`, C.gray)]);
        for (const p of list.slice(0, 24)) say([S(`  ${p.id}  ${p.name}  ${p.kind || ''}`, C.gray)]);
        return true;
      }
      case '/status': {
        const local = (await jget(port, '/api/runtime/local')).data || {};
        say([S('状态', C.title, {bold: true})]);
        for (const [k, v] of [
          ['后端', base(port)], ['会话', sessionName], ['工作区', workspace],
          ['模型', `${model} · 来源 ${provider} · 档位 ${level}`],
          ['本地模型', local.disabled ? '已停用（云端 API 版）' : String(local.phase || '未知')],
          ['上下文', String(stats.limit)],
        ]) say([S(' ' + pad(k, 10), C.gray), S(String(v), C.text)]);
        return true;
      }
      case '/stop': {
        if (sessionRef.current) {
          await jpost(port, '/api/chat/control/stop', {sessionId: sessionRef.current});
          if (abortRef.current) abortRef.current.abort();
          say([S('✓ 已请求中断', C.ok)]);
        }
        return true;
      }
      default:
        if (raw.startsWith('/')) { say([S(`✗ 没有这个命令：${cmd}（/help 看全部）`, C.err)]); return true; }
        return false;
    }
  }, [port, cols, model, level, stats.limit, sessionName, workspace, provider, exit, push,
      ensureSession, refreshStats, pollChanges]);

  // ── 输入提交
  const onSubmit = useCallback(async (value) => {
    const text = value.trim();
    setInput('');
    setScroll(0);
    if (!text) return;
    if (prompt) {
      if (prompt.kind === 'question') {
        let ans = text;
        if (prompt.options && /^\d+$/.test(text)) {
          const i = Number(text) - 1;
          if (prompt.options[i] !== undefined) ans = String(prompt.options[i]);
        }
        const out = await jpost(port, '/api/questions/answer', {questionId: prompt.id, answer: ans});
        push([S(out.success ? '✓ 已回答' : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
      } else if (prompt.kind === 'change') {
        const low = text.toLowerCase();
        if (low === 'y') {
          const out = await jpost(port, `/api/changes/${prompt.id}/approve`);
          push([S(out.success ? '✓ 已通过' : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
        } else if (low === 'n') {
          const out = await jpost(port, `/api/changes/${prompt.id}/reject`, {reason: text || '用户打回'});
          push([S(out.success ? '✓ 已打回' : '✗ ' + (out.message || ''), out.success ? C.ok : C.err)]);
        } else {
          push([S('已跳过（/changes 再看）', C.gray)]);
        }
      }
      setPrompt(null);
      return;
    }
    if (text.startsWith('/')) { await handleCommand(text); return; }
    await send(text);
  }, [prompt, port, push, handleCommand, send]);

  // ── 非 TTY：把 stdin 每一行喂进提交通道
  // 【只注册一次】依赖写成空数组：onSubmit 每次渲染都会换新函数，若把它列进依赖，
  // effect 会重建消费者 —— 旧的那个已经把行领走了却因为 alive=false 直接丢弃，
  // 于是命令全部消失（实测就是这个现象）。用 ref 拿最新处理函数，消费者只建一次。
  const submitRef = useRef(onSubmit);
  submitRef.current = onSubmit;
  useEffect(() => {
    dbg('effect: mount');
    // 【不要用 alive 标志】组件被卸载时旧消费者若把行丢掉，命令就凭空消失了
    // （实测过）。这里无论挂载与否都照常处理：卸载后 setState 是空操作，无害。
    (async () => {
      for (;;) {
        const line = await nextLine();
        dbg('effect: got ' + JSON.stringify(line));
        try { await submitRef.current(line); } catch (e) { dbg('consume-error: ' + e); }
      }
    })();
    return () => dbg('consumer cleanup（组件卸载）');
  }, []);

  // ── 快捷键
  useInput((ch, key) => {
    // Claude Code 的 `esc to interrupt`
    if (key.escape) {
      if (busyRef.current && sessionRef.current) {
        jpost(port, '/api/chat/control/stop', {sessionId: sessionRef.current});
        if (abortRef.current) abortRef.current.abort();
        push([S('✓ 已请求中断', C.ok)]);
      }
      return;
    }
    if (key.ctrl && ch === 'c') {
      if (busyRef.current && sessionRef.current) {
        jpost(port, '/api/chat/control/stop', {sessionId: sessionRef.current});
        if (abortRef.current) abortRef.current.abort();
        push([S('✓ 已请求中断', C.ok)]);
      } else {
        exit();
      }
      return;
    }
    if (key.ctrl && ch === 'p') { handleCommand('/panel'); return; }
    if (key.ctrl && ch === 'l') { setLines([]); return; }
  }, {isActive: Boolean(process.stdin.isTTY)});

  // ── 布局
  // 【为什么不能铺满整屏】Ink 是"打印 → 光标上移 N 行 → 重绘"：动态区一旦等于
  // 终端高度，终端就会滚动，Ink 的上移行数全部错位 → 满屏花屏。这就是"界面不能用"。
  // 正确姿势（Claude Code 也是这样）：对话内容走 <Static>，只打印一次、永不重绘，
  // 自然滚进终端回滚缓冲；底部只留输入框 + 状态栏这一小块动态区。
  const mainW = Math.max(40, cols - 4);
  mainWRef.current = mainW;

  const pct = stats.limit ? Math.round((stats.tokens / stats.limit) * 100) : 0;
  const kNum = (n) => (n >= 1000 ? (n / 1000).toFixed(1) + 'K' : String(n));

  const keyHint = busy
    ? 'esc to interrupt'
    : (prompt
      ? (prompt.kind === 'question' ? '输入回答后回车' : 'y 通过 / n 打回 / 直接回车跳过')
      : '回车 发送   / 唤起命令   Ctrl+P 状态   Ctrl+C 退出');

  const renderSpans = (spans, key) => h(Text, {key}, ...spans.map((sp, j) =>
    h(Text, {key: j, color: sp.c, bold: sp.bold, dimColor: sp.dim}, sp.t)));

  return h(Box, {flexDirection: 'column'},
    // ① 已定稿的对话：<Static> 只打印一次，之后永不重绘 → 滚进终端回滚缓冲，
    //    用终端自己的滚动条就能往回看（不需要自己实现视口）。
    h(Static, {items: lines}, (item, i) => renderSpans(item, i)),
    // ② 正在流式输出的那一段：动态区，但只保留最后几行，不让它把屏幕顶满
    stream
      ? h(Box, {flexDirection: 'column'},
        ...wrap(stream, mainW).slice(-6).map((l, i) =>
          h(Text, {key: i, color: C.text}, '  ' + l)))
      : null,
    // ③ 输入框（Claude Code 那种左强调条 + 圆角，框内一行状态）
    h(Box, {flexDirection: 'column', borderStyle: 'round', borderColor: C.faint,
            paddingX: 1},
          h(Box, null,
            h(Text, {color: prompt ? C.userbar : C.accent}, '▌ '),
            busy
              ? h(Text, null,
                h(Text, {color: C.accent},
                  `✻ ${THINK_WORDS[word % THINK_WORDS.length]}…`),
                h(Text, {color: C.gray}, '   (esc to interrupt)'))
              : (interactive
                ? h(TextInput, {
                  value: input, onChange: setInput, onSubmit,
                  placeholder: prompt
                    ? (prompt.kind === 'question' ? cut(prompt.text, 60) : `${cut(prompt.text, 40)}  [y/n]`)
                    : '问点什么，或 /help 看命令',
                })
                : h(Text, {color: input ? C.text : C.gray},
                  input || (prompt ? '（等待回答）' : '（非交互）')))),
          h(Text, {color: C.gray}, `  Build · ${cut(model, 40)} · ${level}`)),
    // 底部状态栏
    h(Box, {width: cols, backgroundColor: C.barBg, paddingX: 1},
      h(Text, {color: C.text}, ` ${kNum(stats.tokens)}/${kNum(stats.limit)} (${pct}%) · $${stats.spent.toFixed(2)}`),
      h(Box, {flexGrow: 1}),
      h(Text, {color: C.gray}, keyHint + ' ')));
}

// ─────────────────────────────────────────── 入口
const argv = process.argv.slice(2);
let port = 8080;
let workspace = process.cwd();
let scriptFile = '';
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (a.startsWith('--port=')) port = Number(a.slice(7));
  else if (a === '--port' && argv[i + 1]) port = Number(argv[++i]);
  else if (a.startsWith('--workspace=')) workspace = a.slice(12);
  else if (a.startsWith('--script=')) scriptFile = a.slice(9);
  else if (a === '--script' && argv[i + 1]) scriptFile = argv[++i];
}

// Ink 在 stdin 走到 EOF 时会自己卸载。管道/重定向喂输入的场景必然踩到，
// `--script` 模式也跑不掉（继承来的 stdin 本来就是空的、立刻 EOF）。
// 解法：非交互场景给 Ink 一个**永不结束的假 stdin**，真输入走我们自己的通道。
// 【必须补齐 TTY 接口】Ink 的 App 在 effect 里会调 `stdin.setRawMode(false)` 和
// `stdin.unref()`；普通 Readable 没有这两个方法 → effect 抛异常 → React 把整棵树卸载
// （实测：push 被调用但 setLines 的 updater 永远不执行，界面像死了一样）。
const fakeStdin = new Readable({read() { /* 永远不产出、也永远不结束 */ }});
fakeStdin.isTTY = false;
fakeStdin.setRawMode = () => {};
fakeStdin.unref = () => {};
fakeStdin.ref = () => {};
const inkInput = process.stdin.isTTY ? process.stdin : fakeStdin;

// 【非交互模式不能渲染 TextInput】`ink-text-input` 内部是 `useInput(..., {isActive: focus})`，
// focus 默认 true → Ink 会调 `setRawMode(true)`；非 TTY 下这句直接抛
// "Raw mode is not supported" → React 卸载整棵树（实测：界面画出来但永远不更新）。
// 非交互时输入从 `--script` / stdin 通道来，界面上用一行文本代替输入框即可。
const interactive = Boolean(process.stdin.isTTY);

// 自动化：命令从文件读，经同一个通道喂进去，进程按自己的节奏活着
if (scriptFile) {
  const cmds = fs.readFileSync(scriptFile, 'utf8').split(/\r?\n/).filter((l) => l.trim() !== '');
  render(h(App, {port, workspace}), {stdin: inkInput});
  (async () => {
    await new Promise((r) => setTimeout(r, 800));          // 等首帧与统计就绪
    for (const line of cmds) {
      dbg('script: ' + JSON.stringify(line));
      feed(line);
      await new Promise((r) => setTimeout(r, 900));
    }
    await new Promise((r) => setTimeout(r, 2500));         // 留时间把最后一帧画完
    process.exit(0);
  })();
} else if (!process.stdin.isTTY) {
  const {default: readline} = await import('node:readline');
  render(h(App, {port, workspace}), {stdin: fakeStdin});
  const rl = readline.createInterface({input: process.stdin});
  rl.on('line', (line) => feed(line));
  rl.on('close', () => setTimeout(() => process.exit(0), 1500));
} else {
  render(h(App, {port, workspace}));
}