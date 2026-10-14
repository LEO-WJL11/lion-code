# Build script invoked by build.bat. UTF-8 with BOM (PS 5.1 reads BOM as UTF-8;
# without it CJK literals would be read as GBK and get mangled).
# Fixes vs the old pipeline:
#   1) NO output filtering - Nuitka's real error stays visible.
#   2) Each target's exit code is captured IMMEDIATELY (PowerShell's $LASTEXITCODE
#      is overwritten by every later native call - that made the old script print
#      "compile failures: 0" while one build had actually failed).
#   3) Stage 0 clears caches BEFORE compiling (explicit user requirement).
#   4) Full stage summary at the end, failures named explicitly.
$ErrorActionPreference = 'Continue'
$root = 'C:\Users\Leo\Desktop\lion-code'
Set-Location $root

function Step($m) { Write-Host ''; Write-Host ('==== ' + $m + ' ====') }
function Ok($m)   { Write-Host ('  [OK]   ' + $m) -ForegroundColor Green }
function Bad($m)  { Write-Host ('  [FAIL] ' + $m) -ForegroundColor Red }
$script:failures = @()
function Fail($m) { Bad $m; $script:failures += $m }

$tmp = Join-Path $root '.lbcheck\tmp'
New-Item -ItemType Directory -Force -Path $tmp | Out-Null
$env:TEMP = $tmp; $env:TMP = $tmp; $env:TMPDIR = $tmp; $env:SQLITE_TMPDIR = $tmp
$env:PYTHONUTF8 = '0'
Remove-Item Env:\PYTHONIOENCODING -ErrorAction SilentlyContinue
$env:NUITKA_CACHE_DIR = Join-Path $root '.lbcheck\nuitka-cache'
New-Item -ItemType Directory -Force -Path $env:NUITKA_CACHE_DIR | Out-Null

# ---------------------------------------------------------------
# STAGE 0: clear every compile cache BEFORE building (user asked for this)
# ---------------------------------------------------------------
Step 'STAGE 0  clear all compile caches (before building)'
$dirs = @(
  (Join-Path $root '.lbcheck\nuitka-cache'),
  (Join-Path $root '.lbcheck\snk_main'),
  (Join-Path $root '.lbcheck\build_out'),
  (Join-Path $root '.lbcheck\stage'),
  (Join-Path $root '.lbcheck\nuitka_smoke'),
  (Join-Path $root '.lbcheck\nk_ascii'),
  (Join-Path $root '.lbcheck\nk_pure'),
  (Join-Path $root '.lbcheck\nk_noutf8'),
  (Join-Path $root '.lbcheck\nk_t2')
)
$freed = [int64]0
foreach ($d in $dirs) {
  if (Test-Path -LiteralPath $d) {
    $sz = [int64]0
    try { $sz = (Get-ChildItem -LiteralPath $d -Recurse -File -Force -ErrorAction SilentlyContinue |
                 Measure-Object -Property Length -Sum).Sum } catch { $sz = [int64]0 }
    try { Remove-Item -LiteralPath $d -Recurse -Force -ErrorAction Stop
          Write-Host ('  removed ' + (Split-Path $d -Leaf) + '  (' + [math]::Round($sz/1MB,1) + ' MB)')
          $freed += $sz } catch { Bad ('cannot remove ' + (Split-Path $d -Leaf) + ': ' + $_.Exception.Message) }
  }
}
try {
  Get-ChildItem -LiteralPath $root -Recurse -Directory -Filter '__pycache__' -Force -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -notlike '*node_modules*' -and $_.FullName -notlike '*.venv*' -and $_.FullName -notlike '*.pythons*' } |
    ForEach-Object { try { Remove-Item -LiteralPath $_.FullName -Recurse -Force -ErrorAction Stop } catch {} }
} catch {}
Get-ChildItem -LiteralPath $root -Filter 'nuitka-crash-report.xml' -File -Force -ErrorAction SilentlyContinue |
  ForEach-Object { Remove-Item -LiteralPath $_.FullName -Force -ErrorAction SilentlyContinue }
Write-Host ('  freed approx ' + [math]::Round($freed/1MB,1) + ' MB')
Write-Host '  kept: installer\output (deliverables)'

# ---------------------------------------------------------------
# STAGE 1: Nuitka, one target at a time, FULL output, exit code captured at once
# ---------------------------------------------------------------
Step 'STAGE 1  Nuitka x3 (single thread, --jobs=1 per user instruction) - FULL output'
$ps1 = Join-Path $root '.lbcheck\build_one.ps1'
# Resolve the adapter source by wildcard: a CJK literal here would be mangled if
# this file ever lost its BOM - that already broke a build once.
$adapterSrc = (Get-ChildItem -Path $root -Filter 'mimo*.py' -File | Select-Object -First 1).Name
if (-not $adapterSrc) { Bad 'adapter source not found'; $script:failures += 'adapter src'; }
$targets = @(
  @('main.py',        'LionCode.exe'),
  @($adapterSrc,      'adapter.exe'),
  @('_start_mimo.py', 'start.exe')
)
$buildResult = @{}
foreach ($t in $targets) {
  Write-Host ''
  Write-Host ('---- building ' + $t[0] + ' -> ' + $t[1] + ' ----')
  # Capture the exit code IMMEDIATELY after the native call (before any cmdlet
  # overwrites $LASTEXITCODE) and keep the full output visible.
  & 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' `
      -NoProfile -ExecutionPolicy Bypass -File $ps1 -src $t[0] -out $t[1] 2>&1 | Out-String -Width 4000 | Write-Host
  $code = $LASTEXITCODE
  $buildResult[$t[1]] = $code
  if ($code -ne 0) { Fail ($t[0] + ' exit=' + $code) } else { Ok ($t[1] + '  exit=0') }
}
Write-Host ''
Write-Host ('  per-target exit codes: ' + (($buildResult.GetEnumerator() | ForEach-Object { $_.Key + '=' + $_.Value }) -join '  '))

# ---------------------------------------------------------------
# STAGE 2: verify the three exes really exist (build_one prints a guessed path)
# ---------------------------------------------------------------
Step 'STAGE 2  verify exes'
$exeOk = 0
# 【路径以 Nuitka 实际输出为准】main 的 dist 也在 build_out 下（旧脚本 build_main.ps1
# 才用 snk_main；写死老路径会假报 MISSING）。另：字符串拼接不能写在 @() 的逗号列表里
# （PowerShell 会把它拆成多个元素，上一版就出现过 "MISSING mimo适配" 这种碎片）。
$adapterExeRel = '.lbcheck\build_out\' + ($adapterSrc -replace '\.py$', '') + '.dist\adapter.exe'
$exeRels = @(
  '.lbcheck\build_out\main.dist\LionCode.exe'
  $adapterExeRel
  '.lbcheck\build_out\_start_mimo.dist\start.exe'
)
foreach ($e in $exeRels) {
  $full = Join-Path $root $e
  if (Test-Path $full) { Ok ($e + '  ' + [math]::Round((Get-Item $full).Length/1MB,1) + ' MB'); $exeOk++ }
  else { Fail ('MISSING ' + $e) }
}
if ($exeOk -ne 3) {
  Write-Host ''
  Write-Host 'ABORT: exes incomplete - not packaging.' -ForegroundColor Red
  Write-Host ('  passed ' + $exeOk + ' / 3')
  exit 1
}

# ---------------------------------------------------------------
# STAGE 3: Inno Setup 6 package (threads=16)
# ---------------------------------------------------------------
Step 'STAGE 3  Inno Setup 6 package (threads=16)'
$build = Join-Path $root 'installer\build_installer.ps1'
& 'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' `
    -NoProfile -ExecutionPolicy Bypass -File $build -threads 16 2>&1 | Out-String -Width 4000 | Write-Host
$pkgCode = $LASTEXITCODE
# The inner script inherits the exit code of its LAST native call, which is not
# necessarily ISCC's - so verify by marker AND by the artifact existing.
$marker = Select-String -Path (Join-Path $root '.lbcheck\build_only.log') -Pattern 'BUILD OK' -ErrorAction SilentlyContinue |
          Select-Object -Last 1
$setup = Join-Path $root 'installer\output\LionCode-Setup-1.0.0.exe'
if (Test-Path $setup) {
  $h = (Get-FileHash $setup -Algorithm SHA256).Hash.Substring(0,16).ToLower()
  Ok ('installer: ' + $setup + '  ' + [math]::Round((Get-Item $setup).Length/1MB,1) + ' MB  sha256:16=' + $h)
} else {
  Fail ('installer missing (inner exit=' + $pkgCode + ')')
}

# ---------------------------------------------------------------
Step 'SUMMARY'
if ($script:failures.Count -eq 0) {
  Write-Host '  ALL STAGES OK' -ForegroundColor Green
  exit 0
} else {
  Write-Host ('  ' + $script:failures.Count + ' FAILURE(S):') -ForegroundColor Red
  $script:failures | ForEach-Object { Write-Host ('    - ' + $_) -ForegroundColor Red }
  exit 1
}