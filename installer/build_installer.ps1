# ASCII-only Inno build script (PowerShell 5.1 reads BOM-less .ps1 as ANSI/GBK
# on this machine; a single CJK comment can swallow the next line -> variables
# silently null. Keep this file 100% ASCII. Same rule for every .cmd in payload\.
#
# What it does:
#   1. stages the whole payload into .lbcheck\stage\   (ALL ASCII paths - the
#      adapter dist dir name contains Chinese, and node_modules must NOT be
#      staged: 131452 hardlinks would be expanded by the file copier)
#   2. verifies the stage (required files, .cmd is ASCII+CRLF, sizes)
#   3. runs ISCC.exe with timing, /DLZMA_THREADS=<n> for the thread comparison
#
# Usage:  build_installer.ps1 [-threads 16] [-tag name] [-SkipStage] [-SelfTest]
#         -SelfTest adds /DSELFTEST_NO_REGKEY=1 (see LionCode.iss: this sandbox
#         runs unsigned exes at Low IL, where the HKCU Uninstall key is
#         unwritable -> the self-test installer skips that one entry).
param([string]$threads = '16', [string]$tag = '', [switch]$SkipStage, [switch]$SelfTest)
$ErrorActionPreference = 'Continue'

$root  = 'C:\Users\Leo\Desktop\lion-code'
$stage = Join-Path $root '.lbcheck\stage'
$iss   = Join-Path $root 'installer\LionCode.iss'
# Inno Setup 6 (the user asked for 6 explicitly; 7 is installed too but unused).
$iscc  = 'C:\Users\Leo\AppData\Local\Programs\Inno Setup 6\ISCC.exe'
$fail  = 0
function Step($m) { Write-Host ('--- ' + $m) }
function Bad($m)  { Write-Host ('  [FAIL] ' + $m); $script:fail++ }

if (-not (Test-Path $iscc)) { Write-Host 'ISCC.exe missing'; exit 2 }

# ---- 1. stage --------------------------------------------------------------
if (-not $SkipStage) {
    $sw = [Diagnostics.Stopwatch]::StartNew()
    if (Test-Path $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
    New-Item -ItemType Directory -Force -Path $stage | Out-Null

    # Resolve every freshly built exe by SEARCH: the adapter's dist dir name
    # contains NON-ASCII characters, and PS 5.1 reads this BOM-less script as
    # GBK -> a literal non-ASCII path here decodes to garbage and the copy dies.
    # (Nuitka names the dist dir after the SOURCE file, not the output name:
    #  main.py -> main.dist, <adapter src>.dist, _start_mimo.py ->
    #  _start_mimo.dist -- so never hardcode the dir name.)
    $buildOut = Join-Path $root '.lbcheck\build_out'
    $mainExe = (Get-ChildItem -LiteralPath $buildOut -Recurse -Filter 'LionCode.exe' -File -ErrorAction SilentlyContinue |
                Select-Object -First 1)
    $adapterExe = (Get-ChildItem -LiteralPath $buildOut -Recurse -Filter 'adapter.exe' -File -ErrorAction SilentlyContinue |
                   Select-Object -First 1).FullName
    $startExe = (Get-ChildItem -LiteralPath $buildOut -Recurse -Filter 'start.exe' -File -ErrorAction SilentlyContinue |
                 Select-Object -First 1).FullName
    if (-not $mainExe)   { Bad 'LionCode.exe not found under .lbcheck\build_out' }
    if (-not $adapterExe) { Bad 'adapter.exe not found under .lbcheck\build_out' }
    if (-not $startExe)  { Bad 'start.exe not found under .lbcheck\build_out' }
    $mainDist = ''
    if ($mainExe) { $mainDist = $mainExe.Directory.FullName }

    # The CLOUD-ONLY build ships NO local runtime: runtime-vulkan (llama-server)
    # and every *.gguf are deliberately absent. Only ONE python dist goes in
    # wholesale: main.dist is a byte-identical superset of the other two dists'
    # runtime files (every name collision hashes equal - verified), so
    # adapter/start contribute their .exe only.
    $srcs = @()
    if ($mainDist) { $srcs += @{ from = $mainDist; to = $stage; excl = @() } }
    $srcs += @(
        # MiMo sources WITHOUT node_modules - the deps ship pre-packed below
        @{ from = (Join-Path $root 'MiMo-Code-main'); to = (Join-Path $stage 'MiMo-Code-main'); excl = @('node_modules') },
        @{ from = (Join-Path $root 'skills'); to = (Join-Path $stage 'skills'); excl = @() },
        @{ from = (Join-Path $root 'installer\payload'); to = $stage; excl = @() }
    )
    foreach ($s in $srcs) {
        if (-not (Test-Path -LiteralPath $s.from)) { Bad ('missing source: ' + $s.from); continue }
        $rx = @('/E', '/NFL', '/NDL', '/NJH', '/NJS', '/R:1', '/W:1', '/NP')
        foreach ($e in $s.excl) { $rx += '/XD'; $rx += $e }
        # robocopy is a NATIVE exe: PowerShell hands switches to it verbatim,
        # so do NOT write -LiteralPath (it would be passed as a path -> rc=16
        # fatal). Positional source/dest only, switches as plain strings.
        robocopy $s.from $s.to @rx | Out-Null
        $rc = $LASTEXITCODE
        if ($rc -ge 8) { Bad ('robocopy failed rc=' + $rc + ' ' + $s.from) }
        else { Write-Host ('  robocopy rc=' + $rc + ' <- ' + $s.from) }
    }
    if ($adapterExe) { Copy-Item -LiteralPath $adapterExe (Join-Path $stage 'adapter.exe') -Force }
    Copy-Item -LiteralPath $startExe (Join-Path $stage 'start.exe') -Force
    Copy-Item -LiteralPath 'C:\Users\Leo\AppData\Roaming\npm\node_modules\bun\bin\bun.exe' (Join-Path $stage 'bun.exe') -Force
    Copy-Item -LiteralPath (Join-Path $root 'installer\README-install.md') (Join-Path $stage 'README-install.md') -Force
    # Plan B payload: pre-packed node_modules + x64 7za + junction relink script
    # (pack_nm.ps1 produced all three from the proven dev tree)
    $planB = @(
        @{ from = (Join-Path $root '.lbcheck\node_modules.7z'); to = (Join-Path $stage 'node_modules.7z') },
        @{ from = (Join-Path $root '.lbcheck\7zextra\x64\7za.exe');  to = (Join-Path $stage '7za.exe') },
        @{ from = (Join-Path $root '.lbcheck\7zextra\x64\7za.dll');  to = (Join-Path $stage '7za.dll') },
        @{ from = (Join-Path $root '.lbcheck\7zextra\x64\7zxa.dll'); to = (Join-Path $stage '7zxa.dll') },
        @{ from = (Join-Path $root '.lbcheck\relink-nm.cmd');        to = (Join-Path $stage 'relink-nm.cmd') }
    )
    foreach ($f in $planB) {
        if (Test-Path -LiteralPath $f.from) { Copy-Item -LiteralPath $f.from $f.to -Force }
        else { Bad ('plan B file missing: ' + $f.from) }
    }
    $sw.Stop()
    Write-Host ('STAGE done in ' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + ' s')
}

# ---- 2. verify stage -------------------------------------------------------
Step 'verify stage'
$required = @(
    'LionCode.exe', 'adapter.exe', 'start.exe', 'bun.exe', 'python315.dll',
    'StartLionCode.cmd', '_run_mimo.cmd', 'install_deps.cmd', 'README-install.md',
    'lion-code.cmd',
    'node_modules.7z', '7za.exe', 'relink-nm.cmd',
    'MiMo-Code-main\package.json', 'MiMo-Code-main\bun.lock',
    'MiMo-Code-main\packages\cli\src\index.ts'
)
foreach ($r in $required) {
    if (-not (Test-Path (Join-Path $stage $r))) { Bad ('stage missing: ' + $r) }
}
# CLOUD-ONLY payload: no llama-server, no GGUF weights. Ship any of them and
# the package is wrong (and 5 GB bigger) - fail loudly instead of shipping it.
if (Test-Path (Join-Path $stage 'runtime-vulkan')) { Bad 'runtime-vulkan must NOT be staged (cloud-only build)' }
$gguf = @(Get-ChildItem -LiteralPath $stage -Recurse -Filter '*.gguf' -File -ErrorAction SilentlyContinue)
if ($gguf.Count -gt 0) { Bad ($gguf.Count + ' .gguf weight(s) staged: ' + ($gguf[0].FullName)) }
foreach ($c in @('StartLionCode.cmd', '_run_mimo.cmd', 'install_deps.cmd', 'relink-nm.cmd', 'lion-code.cmd')) {
    $bytes = [IO.File]::ReadAllBytes((Join-Path $stage $c))
    $nonAscii = ($bytes | Where-Object { $_ -gt 127 }).Count
    $lfOnly = 0
    for ($i = 0; $i -lt $bytes.Length; $i++) { if ($bytes[$i] -eq 10) { if ($i -eq 0 -or $bytes[$i-1] -ne 13) { $lfOnly++ } } }
    if ($nonAscii -gt 0) { Bad ($c + ' has ' + $nonAscii + ' non-ASCII bytes') }
    if ($lfOnly -gt 0)   { Bad ($c + ' has ' + $lfOnly + ' LF-only line endings (need CRLF)') }
    if ($nonAscii -eq 0 -and $lfOnly -eq 0) { Write-Host ('  [OK] ' + $c + ' ASCII+CRLF') }
}
$st = Get-ChildItem -LiteralPath $stage -Recurse -File -Force
$stMB = [math]::Round(($st | Measure-Object Length -Sum).Sum / 1MB, 1)
Write-Host ('  stage: ' + $st.Count + ' files, ' + $stMB + ' MB')
if (Test-Path (Join-Path $stage 'MiMo-Code-main\node_modules')) { Bad 'node_modules leaked into stage' }
if ($fail -gt 0) { Write-Host ('STAGE VERIFICATION FAILED: ' + $fail + ' problem(s)'); exit 1 }

# ---- 3. compile ------------------------------------------------------------
$name = 'LionCode-Setup-1.0.0'
if ($SelfTest) { $name = $name + '-selftest' }
elseif ($tag) { $name = $name + '-' + $tag }
Step ('ISCC threads=' + $threads + ' out=' + $name + '.exe')
$isccArgs = @("/DLZMA_THREADS=$threads", "/F$name")
if ($SelfTest) {
    $isccArgs += '/DSELFTEST_NO_REGKEY=1'
    Write-Host '  (self-test variant: CreateUninstallRegKey=no, see LionCode.iss)'
}
$sw = [Diagnostics.Stopwatch]::StartNew()
# /F sets the output BASE filename (OutputDir stays "output" from the .iss);
# /D sets an ISPP define - that is how the LZMA thread count is varied.
$out = & $iscc @isccArgs $iss 2>&1 | ForEach-Object { $_.ToString() }
$rc = $LASTEXITCODE
$sw.Stop()
$out | ForEach-Object { Write-Host ('  | ' + $_) }
Write-Host ('ISCC exit=' + $rc + ' elapsed=' + [math]::Round($sw.Elapsed.TotalSeconds, 1) + ' s')
$exe = Join-Path $root ('installer\output\' + $name + '.exe')
if ($rc -ne 0 -or -not (Test-Path $exe)) {
    Write-Host 'BUILD FAILED; exe=' + $exe
    exit 1
}
$size = (Get-Item $exe).Length
$sha = (Get-FileHash $exe -Algorithm SHA256).Hash.Substring(0, 16)
Write-Host ('BUILD OK: ' + $exe)
Write-Host ('  size=' + [math]::Round($size / 1MB, 1) + ' MB  (' + $size + ' bytes)  sha256:16=' + $sha)
Write-Host ('  payload=' + $stMB + ' MB in ' + $st.Count + ' files  ratio=' + [math]::Round($size / ($stMB * 1MB), 3))
exit 0
