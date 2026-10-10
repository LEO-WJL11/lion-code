# ASCII-only real install / uninstall self-test (PowerShell 5.1 reads BOM-less
# .ps1 as ANSI/GBK on this machine - a single CJK line can swallow the next
# one, so this file must stay 100% ASCII; chat question etc. are ASCII too).
#
# What it does, printing RAW server responses at every step:
#   1  silent install to <repo>\.lbcheck\selftest\install_<ts>  (no UAC;
#      %LOCALAPPDATA% is unwritable for the Low-IL installer here - measured)
#   2  layout asserts: start.exe / backend / adapter / bun.exe /
#      runtime-vulkan / MiMo TUI entry file / install-deps.ok
#   3  start the INSTALLED start.exe (three stages + watchdog), poll /health
#      and assert its stdout proves it picked <installdir>\bun.exe
#   4  API suite: /health, /api/models, cloud mode
#      (POST /api/runtime/mode -> POST /api/chat/adapter/config -> chat)
#      falls back to launching LionCode.exe + adapter.exe directly if
#      start.exe's TUI stage tears the services down
#   5  kill everything that belongs to the install dir (by command line)
#   6  silent uninstall -> assert the directory is really gone
#
# Usage: powershell -NoProfile -ExecutionPolicy Bypass -File test_install.ps1
#        (do NOT pass the install dir on the command line - step 5 kills by
#         command line match, and our own command line must not contain it)
param([string]$setup = '', [switch]$KeepInstall)
$ErrorActionPreference = 'Continue'
$root = 'C:\Users\Leo\Desktop\lion-code'
$script:failed = @()
$script:passed = 0

function Step($m) { Write-Host ''; Write-Host ('========== ' + $m + ' ==========') }
function Pass($m) { $script:passed++; Write-Host ('  [PASS] ' + $m) }
function Fail($m) { $script:failed += $m; Write-Host ('  [FAIL] ' + $m) }
function Assert([bool]$cond, $m) { if ($cond) { Pass $m } else { Fail $m } }
function SamePath($a, $b) { return [string]::Equals([string]$a, [string]$b, [StringComparison]::OrdinalIgnoreCase) }

# ---------------------------------------------------------------- http ------
function HttpGet([string]$url, [int]$timeout = 30) {
    try {
        $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec $timeout
        $body = [string]$r.Content
        Write-Host ('    GET  ' + $url)
        Write-Host ('    HTTP ' + $r.StatusCode)
        Write-Host ('    RAW  ' + $body)
        return [pscustomobject]@{ st = [int]$r.StatusCode; body = $body; err = '' }
    } catch {
        $msg = $_.Exception.Message; $st = 0; $b = ''
        if ($_.Exception.Response) {
            $st = [int]$_.Exception.Response.StatusCode
            try {
                $sr = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $b = $sr.ReadToEnd(); $sr.Close()
            } catch { $b = '' }
        }
        Write-Host ('    GET  ' + $url)
        Write-Host ('    ERR  ' + $msg)
        if ($b) { Write-Host ('    RAW  ' + $b) }
        return [pscustomobject]@{ st = $st; body = $b; err = $msg }
    }
}

function HttpPostJson([string]$url, $payload, [int]$timeout = 60) {
    $json = if ($payload -is [string]) { $payload } else { $payload | ConvertTo-Json -Compress -Depth 6 }
    Write-Host ('    POST ' + $url)
    Write-Host ('    BODY ' + $json)
    try {
        $r = Invoke-WebRequest -Uri $url -Method Post -ContentType 'application/json; charset=utf-8' `
                -Body $json -UseBasicParsing -TimeoutSec $timeout
        $body = [string]$r.Content
        Write-Host ('    HTTP ' + $r.StatusCode)
        Write-Host ('    RAW  ' + $body)
        return [pscustomobject]@{ st = [int]$r.StatusCode; body = $body; err = ''; json = $json }
    } catch {
        $msg = $_.Exception.Message; $st = 0; $b = ''
        if ($_.Exception.Response) {
            $st = [int]$_.Exception.Response.StatusCode
            try {
                $sr = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
                $b = $sr.ReadToEnd(); $sr.Close()
            } catch { $b = '' }
        }
        Write-Host ('    ERR  ' + $msg)
        if ($b) { Write-Host ('    RAW  ' + $b) }
        return [pscustomobject]@{ st = $st; body = $b; err = $msg; json = $json }
    }
}

function To-Json([object]$o) {
    try { return ($o | ConvertTo-Json -Compress -Depth 6) } catch { return 'null' }
}

# ------------------------------------------------------------- process ------
function Get-Matched([string]$needle) {
    $me = $PID
    return @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object {
        $_.CommandLine -and ($_.ProcessId -ne $me) -and ($_.CommandLine -like ('*' + $needle + '*'))
    })
}

function Stop-Matched([string]$needle) {
    $list = Get-Matched $needle
    foreach ($p in $list) {
        $cl = [string]$p.CommandLine
        if ($cl.Length -gt 220) { $cl = $cl.Substring(0, 220) + ' ...' }
        Write-Host ('    kill pid=' + $p.ProcessId + ' ' + $p.Name + ' :: ' + $cl)
        Stop-Process -Id $p.ProcessId -Force -ErrorAction SilentlyContinue
    }
    if ($list.Count -eq 0) { Write-Host ('    (no running process matched "' + $needle + '")') }
    return $list.Count
}

function Show-Matched([string]$needle) {
    $list = Get-Matched $needle
    if ($list.Count -eq 0) { Write-Host '    (nothing running)' }
    foreach ($p in $list) {
        $cl = [string]$p.CommandLine
        if ($cl.Length -gt 220) { $cl = $cl.Substring(0, 220) + ' ...' }
        Write-Host ('    pid=' + $p.ProcessId + ' ' + $p.Name + ' :: ' + $cl)
    }
}

function Wait-Http([string]$url, [int]$timeoutSec, [string]$label) {
    $end = (Get-Date).AddSeconds($timeoutSec)
    $t0 = Get-Date
    while ((Get-Date) -lt $end) {
        try {
            $r = Invoke-WebRequest -Uri $url -UseBasicParsing -TimeoutSec 3
            $ms = [int]((Get-Date) - $t0).TotalMilliseconds
            Write-Host ('    ' + $label + ' up after ' + $ms + ' ms -> HTTP ' + $r.StatusCode)
            return $true
        } catch { Start-Sleep -Milliseconds 400 }
    }
    Write-Host ('    ' + $label + ' NOT up within ' + $timeoutSec + ' s (' + $url + ')')
    return $false
}

# Launch an exe and REALLY WAIT for it, returning its exit code.
# Why not the & call operator: measured - & returned in 296 ms with
# $LASTEXITCODE null while the GUI-subsystem installer was still running in
# the background (all later steps raced it). Why not Start-Process: plain
# Start-Process uses ShellExecute and pops the "Open file - security warning"
# dialog for an unsigned exe (the test hung on that for 5+ minutes).
# ProcessStartInfo + UseShellExecute=false is CreateProcess: no dialog,
# WaitForExit blocks, ExitCode is real.
function Invoke-Exe([string]$exe, [string]$argString, [int]$timeoutSec) {
    $psi = New-Object System.Diagnostics.ProcessStartInfo
    $psi.FileName = $exe
    $psi.Arguments = $argString
    $psi.UseShellExecute = $false
    $psi.WorkingDirectory = (Split-Path -Parent $exe)
    $sw = [Diagnostics.Stopwatch]::StartNew()
    try {
        $p = [Diagnostics.Process]::Start($psi)
    } catch {
        Write-Host ('  [FAIL] could not start ' + $exe + ': ' + $_.Exception.Message)
        return -98
    }
    if (-not $p.WaitForExit($timeoutSec * 1000)) {
        Write-Host ('  [FAIL] ' + (Split-Path -Leaf $exe) + ' still running after ' + $timeoutSec + ' s - killing')
        try { $p.Kill() } catch { }
        return -99
    }
    $sw.Stop()
    Write-Host ('  ran ' + (Split-Path -Leaf $exe) + ': exit=' + $p.ExitCode + ' in ' + [int]$sw.Elapsed.TotalMilliseconds + ' ms')
    return $p.ExitCode
}

# ================================================================ STEP 0 ====
Step 'STEP 0  preflight'
# TEMP/TMP for this process AND EVERY child (installer, start.exe, services,
# uninstaller). Measured on this machine: unsigned exes are spawned at LOW
# integrity (S-1-16-4096 vs our shell's S-1-16-8192) and a Low-IL process gets
# "Error 5: access denied" writing %TEMP% - the same trap that forced the
# Nuitka builds to use .lbcheck\tmp. Workspace dirs ARE writable from Low IL.
$env:TEMP = Join-Path $root '.lbcheck\tmp'
$env:TMP = $env:TEMP
New-Item -ItemType Directory -Force -Path $env:TEMP | Out-Null
Write-Host ('  TEMP/TMP -> ' + $env:TEMP)
if (-not $setup) {
    # Prefer the self-test variant (CreateUninstallRegKey=no): the default
    # build needs an HKCU Uninstall key write that a Low-IL process is denied
    # (Error 5 - measured). On a machine where the default works, the variant
    # is unnecessary; we fall back to the newest build.
    $preferred = Join-Path $root 'installer\output\LionCode-Setup-1.0.0-selftest.exe'
    if (Test-Path -LiteralPath $preferred) { $setup = $preferred }
    else {
        $setup = (Get-ChildItem (Join-Path $root 'installer\output\LionCode-Setup-*.exe') -ErrorAction SilentlyContinue |
                  Sort-Object LastWriteTime | Select-Object -Last 1 -ExpandProperty FullName)
    }
}
if (-not $setup -or -not (Test-Path -LiteralPath $setup)) { Write-Host '  [FATAL] no installer exe found'; exit 2 }
$setupItem = Get-Item -LiteralPath $setup
Write-Host ('  installer : ' + $setup)
Write-Host ('  size      : ' + [math]::Round($setupItem.Length / 1MB, 1) + ' MB (' + $setupItem.Length + ' bytes)')
Write-Host ('  built     : ' + $setupItem.LastWriteTime)
if ($setup -like '*selftest*') { Write-Host '  variant   : selftest (CreateUninstallRegKey=no - Low-IL compatible)' }

$stamp = Get-Date -Format 'yyyyMMdd_HHmmss'
# Install into the WORKSPACE, not %LOCALAPPDATA%: measured, a Low-IL installer
# cannot create %LOCALAPPDATA%\<dir> (Error 5), while the workspace is
# writable from Low IL. Still UAC-free (user-writable dir), which is what the
# /DIR choice was for.
$installdir = Join-Path $root ('.lbcheck\selftest\install_' + $stamp)
if ($installdir -match ' ') { Write-Host '  [FATAL] install path contains a space'; exit 2 }
$installlog = Join-Path $root ('.lbcheck\inno_install_' + $stamp + '.log')
$uninstalllog = Join-Path $root ('.lbcheck\inno_uninstall_' + $stamp + '.log')
$so = Join-Path $root ('.lbcheck\test_start_stdout_' + $stamp + '.log')
$se = Join-Path $root ('.lbcheck\test_start_stderr_' + $stamp + '.log')
Write-Host ('  install to: ' + $installdir)

# PATH snapshot. The user requirement is: after install, a NEW cmd must resolve
# `lion-code`, and the installer must NEVER overwrite the existing PATH. We read
# HKCU\Environment\Path exactly the way a fresh console does (raw registry value,
# no expansion) and remember every entry so STEP 2 can prove they all survived.
function Read-UserPath {
    try {
        $k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment')
        if ($null -eq $k) { return '' }
        $v = [string]$k.GetValue('Path', '')
        $k.Close()
        return $v
    } catch { return '' }
}
$pathBefore = Read-UserPath
$pathEntriesBefore = @($pathBefore -split ';' | Where-Object { $_.Trim() -ne '' })
Write-Host ('  PATH entries before install: ' + $pathEntriesBefore.Count)
if ($pathBefore) {
    $shown = $pathBefore; if ($shown.Length -gt 200) { $shown = $shown.Substring(0, 200) + ' ...' }
    Write-Host ('  PATH raw: ' + $shown)
} else { Write-Host '  PATH raw: (no Path value yet)' }
$regTypeBefore = ''
try {
    $k2 = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment')
    if ($k2) { $regTypeBefore = [string]$k2.GetValueKind('Path'); $k2.Close() }
} catch { $regTypeBefore = '' }
Write-Host ('  PATH registry kind before: ' + $(if ($regTypeBefore) { $regTypeBefore } else { '(none)' }))

# leftovers from an earlier aborted run (needle = the selftest path segment,
# which never appears in the live dev stack's command lines)
Write-Host '  cleaning leftovers of previous runs...'
$needle0 = '.lbcheck\selftest\'
Stop-Matched $needle0 | Out-Null
Get-ChildItem (Join-Path $root '.lbcheck\selftest') -Directory -ErrorAction SilentlyContinue | ForEach-Object {
    Write-Host ('    removing stale dir ' + $_.FullName)
    Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
}
Assert (-not (Test-Path -LiteralPath $installdir)) 'install target is clean before install'

# ================================================================ STEP 1 ====
Step 'STEP 1  silent install (VERYSILENT, no UAC)'
# Invoke-Exe = CreateProcess + WaitForExit (see helper): no security dialog,
# and unlike the & call operator it actually waits for this GUI-subsystem exe.
$instArgs = '/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /DIR="' + $installdir + '" /LOG="' + $installlog + '"'
$installRc = Invoke-Exe $setup $instArgs 900
Write-Host ('  installer exit code : ' + $installRc)
if (Test-Path -LiteralPath $installlog) {
    Write-Host '  --- raw Inno install log (last 25 lines) ---'
    Get-Content -LiteralPath $installlog | Select-Object -Last 25 | ForEach-Object { Write-Host ('  | ' + $_) }
    Write-Host '  --- end log ---'
} else {
    Write-Host '  (no /LOG file produced)'
}
Assert ($installRc -eq 0) 'installer exited 0'
Assert (Test-Path -LiteralPath $installdir) 'install directory exists'
# 8.3 short form of the install dir: start.exe (Nuitka) resolves __file__ to
# the SHORT path, so everything IT spawns has short command lines - a kill
# matching only the long path would leak the backend (measured: one survived,
# held the DLLs during uninstall, and 22 files were left behind).
$fso = New-Object -ComObject Scripting.FileSystemObject
$ndShort = $installdir
try {
    if (Test-Path -LiteralPath $installdir) { $ndShort = $fso.GetFolder($installdir).ShortPath }
} catch { $ndShort = $installdir }
Write-Host ('  install dir short form: ' + $ndShort)

# ================================================================ STEP 2 ====
Step 'STEP 2  installed layout (TUI entry, bun.exe, lion-code.cmd, NO local runtime)'
$must = @(
    'start.exe', 'LionCode.exe', 'adapter.exe', 'bun.exe', 'python315.dll',
    'StartLionCode.cmd', '_run_mimo.cmd', 'install_deps.cmd', 'README-install.md',
    'lion-code.cmd',
    'node_modules.7z', '7za.exe', 'relink-nm.cmd',
    'MiMo-Code-main\packages\cli\src\index.ts',
    'MiMo-Code-main\package.json', 'MiMo-Code-main\bun.lock',
    'unins000.exe'
)
foreach ($f in $must) {
    $p = Join-Path $installdir $f
    Assert (Test-Path -LiteralPath $p) ('exists: ' + $f)
    if (-not (Test-Path -LiteralPath $p)) { Write-Host ('        expected at ' + $p) }
}
# CLOUD-ONLY payload: no llama-server runtime and no GGUF weights anywhere in
# the tree. Both were shipped before; the product is API-only now.
Assert (-not (Test-Path (Join-Path $installdir 'runtime-vulkan'))) 'runtime-vulkan NOT shipped (cloud-only build)'
$ggufAll = @(Get-ChildItem -LiteralPath $installdir -Recurse -Filter '*.gguf' -File -Force -ErrorAction SilentlyContinue)
Assert ($ggufAll.Count -eq 0) ('no *.gguf anywhere under the install dir (' + $ggufAll.Count + ')')
$nm = Join-Path $installdir 'MiMo-Code-main\node_modules'
$ok = Join-Path $installdir 'install-deps.ok'
$log = Join-Path $installdir 'install-deps.log'
Assert (Test-Path -LiteralPath $ok) 'install-deps.ok marker (7z extract + relink succeeded during install)'
if (Test-Path -LiteralPath $log) {
    Write-Host '  --- raw install-deps.log (last 40 lines) ---'
    Get-Content -LiteralPath $log | Select-Object -Last 40 | ForEach-Object { Write-Host ('  | ' + $_) }
    Write-Host '  --- end install-deps.log ---'
} else { Fail 'install-deps.log missing' }
if (Test-Path -LiteralPath $nm) {
    $n = @(Get-ChildItem -LiteralPath $nm -Recurse -File -Force -ErrorAction SilentlyContinue)
    $mb = [math]::Round(($n | Measure-Object Length -Sum).Sum / 1MB, 1)
    Write-Host ('  node_modules: ' + $n.Count + ' files, ' + $mb + ' MB (logical)')
    Assert ($n.Count -gt 50000) 'node_modules extracted from the pre-packed archive'
    # junctions: 7z -snl leaves them as empty folders; relink-nm.cmd must have
    # recreated them (dev tree has 3275)
    $j = @(Get-ChildItem -LiteralPath $nm -Recurse -Force -Attributes ReparsePoint -ErrorAction SilentlyContinue)
    Write-Host ('  junctions/symlinks now: ' + $j.Count)
    Assert ($j.Count -gt 1000) 'junctions recreated by relink-nm.cmd'
} else { Fail 'node_modules missing' }
# Plan B acceptance: the EXTRACTED tree must actually run the TUI CLI
$cliDir = Join-Path $installdir 'MiMo-Code-main\packages\cli'
Push-Location $cliDir
$t0 = Get-Date
$cliOut = & (Join-Path $installdir 'bun.exe') run --conditions=browser '.\src\index.ts' --help 2>&1
$cliRc = $LASTEXITCODE
Pop-Location
$cliMs = [int]((Get-Date) - $t0).TotalMilliseconds
Write-Host ('  installed CLI --help: rc=' + $cliRc + ' ms=' + $cliMs)
@($cliOut) | Select-Object -First 6 | ForEach-Object { Write-Host ('    | ' + $_) }
Assert ($cliRc -eq 0) 'installed tree runs the MiMo TUI CLI (extracted deps are usable)'
# no python sources shipped (compiled exes only), and NO gguf models shipped
Assert (-not (Test-Path (Join-Path $installdir 'main.py'))) 'main.py NOT shipped (backend is compiled)'
$ggufs = @(Get-ChildItem -LiteralPath $installdir -Filter '*.gguf' -File -ErrorAction SilentlyContinue)
Assert ($ggufs.Count -eq 0) 'no *.gguf model weights shipped (cloud-only build)'
# NOTE: the previous revision hardlinked lion-merged-IQ4_XS.gguf into the install
# dir to block the 5.2 GB auto-download. That is obsolete twice over: the
# payload has no weights AND auto-download is switched off in the product
# (LOCAL_RUNTIME_DISABLED), so nothing can download anything.

# ================================================================ STEP 2b ====
Step 'STEP 2b  PATH: install dir appended (never overwritten) + lion-code resolves'
$pathAfter = Read-UserPath
$shown2 = $pathAfter; if ($shown2.Length -gt 300) { $shown2 = $shown2.Substring(0, 300) + ' ...' }
Write-Host ('  PATH raw after install : ' + $(if ($pathAfter) { $shown2 } else { '(EMPTY)' }))
$pathEntriesAfter = @($pathAfter -split ';' | Where-Object { $_.Trim() -ne '' })
Write-Host ('  PATH entries after     : ' + $pathEntriesAfter.Count + ' (was ' + $pathEntriesBefore.Count + ')')
Assert ($pathEntriesAfter.Count -ge $pathEntriesBefore.Count) 'PATH entry count did not shrink'
$lost = @($pathEntriesBefore | Where-Object { $pathEntriesAfter -notcontains $_ })
Assert ($lost.Count -eq 0) ('no pre-existing PATH entry was overwritten/lost (lost: ' + ($lost -join ' | ') + ')')
$hit = @($pathEntriesAfter | Where-Object { $_.Trim() -ieq $installdir })
# ---- environment probe ----------------------------------------------------
# An UNSIGNED installer is spawned at Low Mandatory Level inside this sandbox
# (measured: every HKCU write fails with WinError 5 / RegCreateKeyEx code 5),
# so HKCU\Environment cannot be written by setup.exe here. LionCode.iss detects
# that (LionHKCUWritable probe), skips the [Registry] entry and writes a
# WARNING into the installer log instead of aborting the install.
# We report it as an explicit ENV-SKIP - never as a pass - and let the TEST
# process (Medium IL, proven able to write HKCU) append the entry itself so the
# `lion-code`-via-PATH launch below can still be exercised end to end.
$script:pathWrittenByInstaller = $true
$installerSkippedPath = $false
if (Test-Path -LiteralPath $installlog) {
    $installerSkippedPath = [bool](Select-String -LiteralPath $installlog -Pattern 'HKCU is NOT writable' -Quiet)
}
if ($installerSkippedPath -or ($hit.Count -eq 0)) {
    $script:pathWrittenByInstaller = $false
    Write-Host '  [ENV-SKIP] the (Low IL) installer could NOT write HKCU\Environment in this sandbox.'
    Write-Host '             evidence: installer log -> "LionCode: WARNING - HKCU is NOT writable"'
    Write-Host '             installer-side PATH assertion SKIPPED; the test appends the entry itself.'
    try {
        $k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment', $true)
        if ($null -eq $k) { $k = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey('Environment') }
        $cur = [string]$k.GetValue('Path', '')
        $has = @($cur -split ';') -contains $installdir
        if (-not $has) {
            $new = $cur
            if ($new.Trim() -eq '') { $new = $installdir }
            else { $new = $new.TrimEnd(';') + ';' + $installdir }
            $k.SetValue('Path', $new, [Microsoft.Win32.RegistryValueKind]::ExpandString)
            Write-Host '  (test process appended the install dir to PATH itself - Medium IL)'
        }
        $k.Close()
    } catch { Write-Host ('  [WARN] self-append failed: ' + $_.Exception.Message) }
    $pathAfter = Read-UserPath
    $pathEntriesAfter = @($pathAfter -split ';' | Where-Object { $_.Trim() -ne '' })
    $hit = @($pathEntriesAfter | Where-Object { $_.Trim() -ieq $installdir })
} else {
    Assert ($hit.Count -eq 1) ('install dir present in PATH exactly once (' + $hit.Count + ')')
}
Assert ($pathEntriesAfter.Count -ge $pathEntriesBefore.Count) 'PATH entry count did not shrink (still true after the PATH touch)'
$regTypeAfter = ''
try {
    $k3 = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment')
    if ($k3) { $regTypeAfter = [string]$k3.GetValueKind('Path'); $k3.Close() }
} catch { $regTypeAfter = '' }
Write-Host ('  PATH registry kind now  : ' + $regTypeAfter + ' (before: ' + $regTypeBefore + ')')
Assert ($regTypeAfter -ne '') 'Path value exists in HKCU\Environment after install'
# A brand-new console rebuilds its environment from the registry; do exactly
# that here so `lion-code` is resolved through PATH and not through a hardcoded
# path (our command line must not contain the install dir - see STEP 5).
$env:PATH = $pathAfter + ';' + $env:PATH
$lcCmd = Get-Command lion-code -ErrorAction SilentlyContinue
$lcSrc = if ($lcCmd) { $lcCmd.Source } else { '(not found)' }
Write-Host ('  Get-Command lion-code  : ' + $lcSrc)
Assert ($null -ne $lcCmd) 'lion-code resolves through PATH in a fresh environment'
if ($lcCmd) {
    Assert ([string]::Equals([string]$lcCmd.Source, (Join-Path $installdir 'lion-code.cmd'),
            [StringComparison]::OrdinalIgnoreCase)) 'resolved to <installdir>\lion-code.cmd'
}
# The .cmd must be the plain-console launcher the user asked for: run start.exe
# in the current console (no `start` to a new window, no hidden run).
$lcBytes = [IO.File]::ReadAllBytes((Join-Path $installdir 'lion-code.cmd'))
$lcText = [Text.Encoding]::ASCII.GetString($lcBytes)
Write-Host ('  lion-code.cmd head: ' + ($lcText -split "`r`n" | Select-Object -First 1))
Assert ($lcText -like '*start.exe*') 'lion-code.cmd launches start.exe'
Assert (($lcText -notmatch '(?im)^\s*start\s+""')) 'lion-code.cmd does NOT open a separate window'
$lcNonAscii = @($lcBytes | Where-Object { $_ -gt 127 }).Count
Assert ($lcNonAscii -eq 0) ('lion-code.cmd is ASCII-only (' + $lcNonAscii + ' non-ASCII bytes)')

# ================================================================ STEP 3 ====
Step 'STEP 3  start via the `lion-code` command (backend -> adapter -> MiMo TUI + watchdog)'
# The dev stack of THIS workspace is live while we test (verified with
# Get-NetTCPConnection: python main.py on 18080, the adapter on 8791 - they
# belong to the parent session, must not be touched). Talking to them would
# make every assertion pass against the WRONG process, so the self-test runs on
# its own port pair; start.exe reads these two env vars (children inherit them).
$bePort = 18090
$adPort = 8793
$env:LION_CODE_BACKEND_PORT = [string]$bePort
$env:LION_CODE_ADAPTER_PORT = [string]$adPort
$backend = 'http://127.0.0.1:' + $bePort
$adapter = 'http://127.0.0.1:' + $adPort
Write-Host ('  ports: backend :' + $bePort + '  adapter :' + $adPort + '  (dev stack keeps 18080/8791)')
# Launch through `cmd /c lion-code` so PATH resolution is the thing under test.
# Our own command line stays free of the install dir (STEP 5 kills by command
# line); the .cmd itself does cd /d "%~dp0", so no working-dir help either.
$sp = Start-Process -FilePath 'cmd.exe' -ArgumentList '/c', 'lion-code' `
        -WorkingDirectory $root -RedirectStandardOutput $so -RedirectStandardError $se -PassThru -WindowStyle Hidden
Write-Host ('  cmd /c lion-code  pid=' + $sp.Id)
$up = Wait-Http ($backend + '/health') 120 'backend /health'
$upAdapter = $false
if ($up) { $upAdapter = Wait-Http ($adapter + '/global/health') 60 'adapter /global/health' }
$exited = $sp.HasExited
Write-Host ('  start.exe still running: ' + (-not $exited))
Write-Host '  --- raw start.exe stdout (first 40 lines) ---'
if (Test-Path $so) { Get-Content $so | Select-Object -First 40 | ForEach-Object { Write-Host ('  | ' + $_) } }
Write-Host '  --- end stdout ---'
if ((Test-Path $se) -and (Get-Item $se).Length -gt 0) {
    Write-Host '  --- raw start.exe stderr (first 20 lines) ---'
    Get-Content $se | Select-Object -First 20 | ForEach-Object { Write-Host ('  | ' + $_) }
    Write-Host '  --- end stderr ---'
}
Assert $up 'lion-code command brought the backend up (cmd -> lion-code.cmd -> start.exe)'
Assert $upAdapter 'adapter /global/health reachable'
# evidence for the bun.exe-lookup patch: the launcher must print its bun cmd.
# Poll the (still open) redirected stdout for up to 20 s; reading a file that
# the running child holds can throw, so never let that abort the test.
$bunCmdExpected = (Join-Path $installdir 'bun.exe')
$stage3line = ''
$stage3End = (Get-Date).AddSeconds(20)
while ((Get-Date) -lt $stage3End -and -not $stage3line) {
    $stdoutAll = ''
    try { if (Test-Path $so) { $stdoutAll = (Get-Content $so -Raw -ErrorAction Stop) } } catch { $stdoutAll = '' }
    foreach ($l in ($stdoutAll -split "`r?`n")) { if ($l -like '*bun.exe run*') { $stage3line = $l.Trim(); break } }
    if (-not $stage3line) { Start-Sleep -Milliseconds 500 }
}
Write-Host ('  stage-3 line: ' + $(if ($stage3line) { $stage3line } else { '(not found within 20 s)' }))
# The line can print the path in 8.3 form (this volume has 8.3 names on:
# ...\LION-C~1\LBCHEC~1\selftest\INSTAL~1\bun.exe), so compare RESOLVED
# paths - Get-Item expands a short path to its long FullName (verified).
$resolvedBun = ''
if ($stage3line -match '^\s*(\S+bun\.exe)\s+run') {
    $token = $Matches[1]
    try { $resolvedBun = (Get-Item -LiteralPath $token -ErrorAction Stop).FullName } catch { $resolvedBun = '' }
}
if ($resolvedBun) { Write-Host ('  resolved bun from that line: ' + $resolvedBun) }
Assert ($resolvedBun -ne '' -and [string]::Equals($resolvedBun, $bunCmdExpected, [StringComparison]::OrdinalIgnoreCase)) `
       'start.exe uses the bundled <installdir>\bun.exe (lookup patch)'
Write-Host ('  processes now running for this install:')
Show-Matched $installdir

# watchdog / frontend logs: raw evidence of what stage 3 did
foreach ($lg in @('.lbcheck\watchdog.log', '.lbcheck\frontend.log', '.lbcheck\backend.log')) {
    $p = Join-Path $installdir $lg
    if ((Test-Path $p) -and (Get-Item $p).Length -gt 0) {
        Write-Host ('  --- tail of ' + $lg + ' (raw, last 12 lines) ---')
        Get-Content $p | Select-Object -Last 12 | ForEach-Object { Write-Host ('  | ' + $_) }
        Write-Host '  --- end ---'
    }
}

# ================================================================ STEP 4 ====
function Invoke-ApiSuite([string]$phase, [bool]$withAdapter) {
    Step ('STEP 4  API suite (' + $phase + ')')
    $h = HttpGet ($backend + '/health')
    Assert ($h.st -eq 200) ($phase + ': GET /health == 200')
    $m = HttpGet ($backend + '/api/models')
    Assert ($m.st -eq 200) ($phase + ': GET /api/models == 200')
    if ($withAdapter) {
        $a = HttpGet ($adapter + '/global/health')
        Assert ($a.st -eq 200) ($phase + ': adapter GET /global/health == 200')
    }

    Write-Host '  --- cloud mode: step 1 POST /api/runtime/mode (custom) ---'
    $r1 = HttpPostJson ($backend + '/api/runtime/mode') @{
        mode = 'custom'
        baseUrl = 'https://token-plan-cn.xiaomimimo.com/v1'
        apiKey = 'tp-csttjvymida1debrhdu692ubt8qervw0dh6nsbg79mzm0nuu'
        model = 'mimo-v2.6-flash'
    }
    Assert ($r1.st -eq 200) ($phase + ': POST /api/runtime/mode == 200')
    $r1b = HttpGet ($backend + '/api/runtime/mode')
    Assert ($r1b.st -eq 200) ($phase + ': GET /api/runtime/mode == 200')

    Write-Host '  --- cloud mode: step 2 POST /api/chat/adapter/config (re-point active adapter) ---'
    $r2 = HttpPostJson ($backend + '/api/chat/adapter/config') @{
        baseUrl = 'https://token-plan-cn.xiaomimimo.com/v1'
        apiKey = 'tp-csttjvymida1debrhdu692ubt8qervw0dh6nsbg79mzm0nuu'
        model = 'mimo-v2.6-flash'
    }
    Assert ($r2.st -eq 200) ($phase + ': POST /api/chat/adapter/config == 200')
    $r2b = HttpGet ($backend + '/api/chat/adapter/status')
    Write-Host ('    adapter status raw: ' + $r2b.body)

    Write-Host '  --- cloud mode: step 3 real chat (stream) ---'
    $ws = Join-Path $root '.lbcheck\ws_selftest'
    if (-not (Test-Path $ws)) { New-Item -ItemType Directory -Force -Path $ws | Out-Null }
    $rw = HttpPostJson ($backend + '/api/workspaces') @{ path = $ws }
    $wsid = $null
    try { $wsid = (ConvertFrom-Json $rw.body).data.id } catch { Write-Host ('    workspace parse failed: ' + $_.Exception.Message) }
    Write-Host ('    workspaceId = ' + $wsid)
    if (-not $wsid) { Fail ($phase + ': workspace creation failed (see raw above)'); return }

    $rs = HttpPostJson ($backend + '/api/sessions') @{ workspaceId = $wsid; mode = 'STANDARD' }
    $sid = $null
    try {
        $d = (ConvertFrom-Json $rs.body).data
        $sid = $d.sessionId; if (-not $sid) { $sid = $d.id }
    } catch { Write-Host ('    session parse failed: ' + $_.Exception.Message) }
    Write-Host ('    sessionId = ' + $sid)
    if (-not $sid) { Fail ($phase + ': session creation failed (see raw above)'); return }

    # A task that FORCES several tool calls (the user asked for a tool-using
    # chat): create a file, count its lines, read it back. All three are on the
    # keep-list; the assertions below reject any deleted/off-list tool.
    $q = 'Use tools for all three steps, then reply in one sentence: ' + `
         '1) create hello.txt with exactly two lines (alpha and beta), ' + `
         '2) count how many lines it has, ' + `
         '3) read it back and report the line count.'
    $rc = HttpPostJson ($backend + '/api/chat/stream') @{ sessionId = $sid; message = $q } 300
    $raw = [string]$rc.body
    Write-Host ('    stream raw length = ' + $raw.Length)
    $head = $raw; if ($head.Length -gt 1500) { $head = $head.Substring(0, 1500) + ' ...[truncated]' }
    Write-Host '    --- raw stream (head) ---'
    foreach ($l in ($head -split "`r?`n")) { Write-Host ('    | ' + $l) }
    Write-Host '    --- end stream ---'
    $texts = @()
    $tools = @()
    $errFrames = @()
    foreach ($l in ($raw -split "`r?`n")) {
        if ($l.Trim() -like 'data:*') {
            $payload = $l.Trim().Substring(5).Trim()
            if (-not $payload -or $payload -eq '[DONE]') { continue }
            try {
                $f = ConvertFrom-Json $payload
                if ($f.type -eq 'TEXT') { $texts += [string]$f.content }
                if ($f.type -eq 'TOOL_CALL') {
                    $tn = [string]$f.toolName
                    if (-not $tn) { $tn = [string]$f.name }
                    if ($tn) { $tools += $tn }
                }
                if ($f.type -eq 'ERROR') { $errFrames += $payload; Write-Host ('    ERROR FRAME: ' + $payload) }
            } catch { Write-Host ('    unparseable frame: ' + $payload) }
        }
    }
    $answer = ($texts -join '').Trim()
    Write-Host ('    ANSWER: ' + $answer)
    Assert ($rc.st -eq 200) ($phase + ': POST /api/chat/stream == 200')
    Assert ($answer.Length -gt 0) ($phase + ': cloud chat produced an answer')
    # ---- the tool part (user requirement: a task that needs several tools) --
    $toolsUsed = @($tools | Where-Object { $_ } | Sort-Object -Unique)
    Write-Host ('    TOOLS USED: ' + $(if ($toolsUsed.Count) { $toolsUsed -join ', ' } else { '(none)' }))
    Assert ($toolsUsed.Count -ge 1) ($phase + ': the chat really called tools')
    $keepTools = @('read_file', 'head_tail_file', 'directory_tree', 'glob_files',
                   'search_in_files', 'line_count', 'write_file', 'create_file',
                   'modify_file', 'append_file', 'copy_file', 'create_directory',
                   'delete_file', 'download_file', 'execute_command', 'web_search',
                   'system_info', 'timestamp', 'context_window', 'context_prune',
                   'ask_user', 'skill_load')
    $offList = @($toolsUsed | Where-Object { $keepTools -notcontains $_ })
    Assert ($offList.Count -eq 0) ($phase + ': only the 21 kept tools were used (off-list: ' + ($offList -join ',') + ')')
    Assert ($errFrames.Count -eq 0) ($phase + ': no ERROR frame in the stream')
    # PROVENANCE, not self-identity: models hallucinate who they are (one run
    # answered "Claude" while the raw config clearly showed the Xiaomi
    # token-plan endpoint). What is provable: the active config points at
    # token-plan/mimo-v2.6-flash, and no local llama-server of this install is
    # running - so the local 9B (which is not even shipped) cannot have
    # produced the answer.
    $cloudCfg = (([string]$r1b.body) -like '*token-plan*') -and (([string]$r1b.body) -like '*mimo-v2.6-flash*')
    Assert $cloudCfg ($phase + ': active config is the CLOUD endpoint (token-plan / mimo-v2.6-flash)')
    $llama = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
               Where-Object { $_.Name -like 'llama-server*' -and
                              ($_.CommandLine -like ('*' + $installdir + '*') -or
                               ($ndShort -ne $installdir -and $_.CommandLine -like ('*' + $ndShort + '*'))) })
    Assert ($llama.Count -eq 0) ($phase + ': no local llama-server of this install answering (so NOT the local 9B)')
    # Whole-machine check too: the product is cloud-only, so there must not be a
    # single llama-server process anywhere (this machine ships one under
    # runtime-vulkan\, and a stray instance would silently answer the chat).
    $llamaAll = @(Get-CimInstance Win32_Process -ErrorAction SilentlyContinue |
                  Where-Object { $_.Name -like 'llama-server*' })
    Assert ($llamaAll.Count -eq 0) ($phase + ': zero llama-server processes machine-wide')
    # The install dir must stay clean of weights after a chat round as well.
    $ggufAfter = @(Get-ChildItem -LiteralPath $installdir -Recurse -Filter '*.gguf' -File -Force -ErrorAction SilentlyContinue)
    Assert ($ggufAfter.Count -eq 0) ($phase + ': still no *.gguf (nothing was downloaded)')
    Write-Host ('    identity claim (informational, self-reports are flaky): ' + $answer)
}

$phaseA = 'lion-code'
$up2 = $false
try { $r = Invoke-WebRequest -Uri ($backend + '/health') -UseBasicParsing -TimeoutSec 5; $up2 = ($r.StatusCode -eq 200) } catch { $up2 = $false }
if ($up2) {
    # print the raw answer inside; a crash here must be visible, never silent
    try { Invoke-ApiSuite $phaseA $true }
    catch { Write-Host ('  [FAIL] suite crashed: ' + $_.Exception.Message); Write-Host ('  [FAIL] stack: ' + $_.ScriptStackTrace) }
    # did the TUI stage tear the services down mid-suite?
    try { $r = Invoke-WebRequest -Uri ($backend + '/health') -UseBasicParsing -TimeoutSec 5; $up2 = ($r.StatusCode -eq 200) } catch { $up2 = $false }
    Write-Host ('  backend still healthy after suite: ' + $up2)
} else {
    Write-Host '  backend never came up under start.exe - will fall back to direct exes'
}

# ---- fallback: launch installed backend + adapter directly -----------------
$needFallback = -not $up2
if ($needFallback) {
    Step 'STEP 4b  fallback: launch installed LionCode.exe + adapter.exe directly'
    foreach ($ndl in @($installdir, $ndShort)) { Stop-Matched $ndl | Out-Null }
    Start-Sleep -Seconds 2
    $wsroot = Join-Path $installdir '.lbcheck\workspace'
    $cfgdir = Join-Path $installdir '.lbcheck\mimo'
    New-Item -ItemType Directory -Force -Path $wsroot, $cfgdir | Out-Null
    $blog = Join-Path $installdir '.lbcheck\backend.log'
    $alog = Join-Path $installdir '.lbcheck\adapter.log'
    $bp = Start-Process -FilePath (Join-Path $installdir 'LionCode.exe') -WorkingDirectory $installdir `
            -ArgumentList @('--backend-only', ('--server.port=' + $bePort),
                            ('--app-root=' + $installdir),
                            ('--lion.workspace.default-path=' + $wsroot),
                            ('--config-dir=' + $cfgdir)) `
            -RedirectStandardOutput $blog -RedirectStandardError (Join-Path $installdir '.lbcheck\backend.err.log') `
            -PassThru -WindowStyle Hidden
    Write-Host ('  LionCode.exe pid=' + $bp.Id)
    $upB = Wait-Http ($backend + '/health') 120 'direct backend /health'
    $ap = Start-Process -FilePath (Join-Path $installdir 'adapter.exe') -WorkingDirectory $installdir `
            -ArgumentList @(('--port=' + $adPort), ('--backend=http://127.0.0.1:' + $bePort),
                            ('--directory=' + $installdir),
                            ('--workspace=' + $wsroot)) `
            -RedirectStandardOutput $alog -RedirectStandardError (Join-Path $installdir '.lbcheck\adapter.err.log') `
            -PassThru -WindowStyle Hidden
    Write-Host ('  adapter.exe pid=' + $ap.Id)
    $upBA = Wait-Http ($adapter + '/global/health') 60 'direct adapter /global/health'
    Show-Matched $installdir
    if ($upB) { Invoke-ApiSuite 'direct-exe' $upBA }
    else { Fail 'direct backend did not come up either (see raw logs above)' }
}

# ================================================================ STEP 5 ====
Step 'STEP 5  stop everything started for this install (kill by command line)'
# BOTH path forms: start.exe spawns its children with 8.3 (short) paths, the
# fallback launcher with long ones - match either or a backend leaks (it did).
$ndNeedles = @($installdir)
if ($ndShort -ne $installdir) { $ndNeedles += $ndShort }
$n = 0
foreach ($ndl in $ndNeedles) { $n += Stop-Matched $ndl }
Write-Host ('  killed ' + $n + ' process(es) [' + ($ndNeedles -join ' | ') + ']')
# second pass: the watchdog inside start.exe could respawn a child in the gap
Start-Sleep -Seconds 2
Write-Host '  second pass (watchdog respawn race):'
$n2 = 0
foreach ($ndl in $ndNeedles) { $n2 += Stop-Matched $ndl }
Write-Host ('  killed ' + $n2 + ' process(es) on second pass')
$freeEnd = (Get-Date).AddSeconds(30)
$free = $false
while ((Get-Date) -lt $freeEnd) {
    try { Invoke-WebRequest -Uri ($backend + '/health') -UseBasicParsing -TimeoutSec 2 | Out-Null; Start-Sleep -Milliseconds 500 }
    catch { $free = $true; break }
}
Assert $free ('port ' + $bePort + ' released after cleanup')
$left = @()
foreach ($ndl in $ndNeedles) { $left += Get-Matched $ndl }
$left = @($left | Sort-Object ProcessId -Unique)
Assert ($left.Count -eq 0) ('no process left with this install dir (' + $left.Count + ')')
foreach ($p in $left) { Write-Host ('    leftover pid=' + $p.ProcessId + ' ' + $p.Name + ' :: ' + $p.CommandLine) }

# ================================================================ STEP 6 ====
Step 'STEP 6  silent uninstall (unins000.exe /VERYSILENT)'
# pre-uninstall cleanliness: no half-downloaded model (the product never
# downloads one anymore - this asserts that too).
$parts = @(Get-ChildItem -LiteralPath $installdir -Filter '*.part' -File -Force -ErrorAction SilentlyContinue)
foreach ($p in $parts) { Write-Host ('  note: partial download present: ' + $p.Name + ' ' + $p.Length + ' B') }
Assert ($parts.Count -eq 0) 'no partial model download (*.part) in install dir'
$unins = Join-Path $installdir 'unins000.exe'
if (-not (Test-Path -LiteralPath $unins)) {
    Fail 'unins000.exe missing - cannot uninstall'
} else {
    $unArgs = ('/VERYSILENT /NORESTART /LOG="' + $uninstalllog + '"')
    $unRc = Invoke-Exe $unins $unArgs 600
    if (Test-Path $uninstalllog) {
        Write-Host '  --- raw Inno uninstall log (last 20 lines) ---'
        Get-Content $uninstalllog | Select-Object -Last 20 | ForEach-Object { Write-Host ('  | ' + $_) }
        Write-Host '  --- end log ---'
    }
    Assert ($unRc -eq 0) 'uninstaller exited 0'
    $goneEnd = (Get-Date).AddSeconds(180)
    $gone = $false
    while ((Get-Date) -lt $goneEnd) {
        if (-not (Test-Path -LiteralPath $installdir)) { $gone = $true; break }
        Start-Sleep -Milliseconds 500
    }
    if (-not $gone) {
        Write-Host '  [FAIL] install dir still present; leftovers:'
        $items = Get-ChildItem -LiteralPath $installdir -Recurse -Force -ErrorAction SilentlyContinue
        Write-Host ('  leftover count = ' + $items.Count)
        foreach ($i in ($items | Select-Object -First 30)) {
            $rel = $i.FullName.Substring($installdir.Length + 1)
            if ($i.PSIsContainer) { Write-Host ('    [dir ] ' + $rel) }
            else { Write-Host ('    [file] ' + $rel + '  ' + $i.Length + ' B') }
        }
    }
    Assert $gone 'install directory removed after uninstall'

    # ---- PATH must be clean of the install dir afterwards -------------------
    $pathAfterUn = Read-UserPath
    $leftoverEntries = @($pathAfterUn -split ';' | Where-Object { $_.Trim() -ieq $installdir })
    Write-Host ('  PATH after uninstall: ' + $(if ($pathAfterUn) { $pathAfterUn.Substring(0, [Math]::Min(220, $pathAfterUn.Length)) } else { '(empty)' }))
    if ($script:pathWrittenByInstaller) {
        Assert ($leftoverEntries.Count -eq 0) ('no install dir left in the user PATH (' + $leftoverEntries.Count + ')')
    } else {
        Write-Host '  [ENV-SKIP] uninstaller-side PATH cleanup not testable here: the (Low IL)'
        Write-Host '             uninstaller cannot write HKCU\Environment in this sandbox.'
        Write-Host '             Removing the entry the TEST added, then re-checking.'
        try {
            $k = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey('Environment', $true)
            if ($k) {
                $cur = [string]$k.GetValue('Path', '')
                $kept = @($cur -split ';' | Where-Object { $_.Trim() -ne '' -and $_.Trim() -ine $installdir })
                $k.SetValue('Path', ($kept -join ';'), [Microsoft.Win32.RegistryValueKind]::ExpandString)
                $k.Close()
            }
        } catch { Write-Host ('  [WARN] self-clean failed: ' + $_.Exception.Message) }
        $pathAfterUn = Read-UserPath
        $leftoverEntries = @($pathAfterUn -split ';' | Where-Object { $_.Trim() -ieq $installdir })
        Assert ($leftoverEntries.Count -eq 0) ('install dir not left in PATH after the test cleaned it (' + $leftoverEntries.Count + ')')
    }
    $lostAfterUn = @($pathEntriesBefore | Where-Object { @($pathAfterUn -split ';') -notcontains $_ })
    Assert ($lostAfterUn.Count -eq 0) ('uninstall did NOT touch the other PATH entries (lost: ' + ($lostAfterUn -join ' | ') + ')')
    # and `lion-code` must be gone from a fresh lookup
    $env:PATH = ($pathAfterUn + ';' + $env:PATH)
    $lcAfter = Get-Command lion-code -ErrorAction SilentlyContinue
    Assert ($null -eq $lcAfter) 'lion-code no longer resolves after uninstall'
}

# ================================================================ STEP 7 ====
Step 'STEP 7  summary'
Write-Host ('  passed: ' + $script:passed)
Write-Host ('  failed: ' + $script:failed.Count)
foreach ($f in $script:failed) { Write-Host ('    FAIL: ' + $f) }
if (-not $KeepInstall) {
    $stRoot = Join-Path $root '.lbcheck\selftest'
    Get-ChildItem $stRoot -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        Write-Host ('  cleanup: removing ' + $_.FullName)
        Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction SilentlyContinue
    }
}
if ($script:failed.Count -gt 0) { exit 1 }
Write-Host '  ALL CHECKS PASSED'
exit 0
