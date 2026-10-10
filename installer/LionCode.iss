; ==========================================================================
; Lion Code - Inno Setup script
;
; NOTE on encoding: this file contains Chinese comments on purpose - .iss is
; NOT a .ps1, PowerShell 5.1 never reads it, so the GBK/UTF-8 trap does not
; apply here. Every *path* referenced below is nevertheless pure ASCII,
; because installer\build_installer.ps1 first stages the whole payload into
;   ..\.lbcheck\stage\
; That also sidesteps the Chinese source directory name
; (".lbcheck\build_out\mimo适配.dist") and keeps codepage surprises out of
; the compile step entirely.
;
; node_modules strategy (see report): Plan B - shipped PRE-PACKED as
; node_modules.7z (7za -snh: hardlink dedup, -snl: junctions not followed)
; plus relink-nm.cmd; install_deps.cmd extracts it during [Run].
; Plan A ("bun install at install time") was proven viable once (rc=0, 6.9 s,
; 1042 packages) but the same command later failed environment-wide with
; 380-470 "ENOENT ... failed to symlink" errors under every variable we could
; isolate (cache warm/cold, frozen on/off, 3 TEMP targets, clean trees, the
; shell where it had succeeded). Shipping the proven tree removes the network
; dependency and that failure mode entirely.
; ==========================================================================

#ifndef LZMA_THREADS
  #define LZMA_THREADS "16"
#endif

[Setup]
AppId={{5E6F7A8B-1C2D-4E3F-8A9B-0C1D2E3F4A5B}
AppName=Lion Code
AppVersion=1.0.0
AppPublisher=Lion Code
VersionInfoVersion=1.0.0.0
VersionInfoProductVersion=1.0.0
; lowest = no UAC: installs into {localappdata}\Programs by default, which is
; also what makes the silent self-test install/uninstall deterministic.
PrivilegesRequired=lowest
DefaultDirName={autopf}\LionCode
DisableProgramGroupPage=yes
UsePreviousAppDir=no
UsePreviousGroup=no
WizardStyle=modern
ArchitecturesAllowed=x64compatible
; double-click entry is a .cmd that opens Windows Terminal (the TUI needs a
; real console; see installer\payload\StartLionCode.cmd)
OutputDir=output
OutputBaseFilename=LionCode-Setup-1.0.0
; Inno itself is single-threaded at the command-line level (ISCC /? has no
; parallel option), but the LZMA2 compressor supports block-parallel
; compression: LZMANumBlockThreads is a documented [Setup] directive
; (shipped changelog: "Increased the maximum value of ... LZMANumBlockThreads
; from 32 to 256"). build_installer.ps1 measures threads=1 vs threads=16.
Compression=lzma2/max
SolidCompression=yes
LZMANumBlockThreads={#LZMA_THREADS}
; ---------------------------------------------------------------------------
; Self-test variant (build_installer.ps1 -SelfTest) drops the uninstall
; registry entry. WHY, measured on this machine: unsigned exes are spawned at
; LOW integrity (setup process IL=S-1-16-4096 vs our shell's S-1-16-8192 -
; bun.exe, signed, comes out Medium; python.exe, unsigned, comes out Low), and
; a Low-IL process gets "Error 5: access denied" creating
; HKCU\...\Uninstall\<App>_is1 (and directories under %LOCALAPPDATA%). The
; default build keeps the entry so a normal machine shows it in Settings >
; Apps; the variant installs to a Low-writable directory instead and is
; uninstalled via unins000.exe / the Start-Menu shortcut.
; ---------------------------------------------------------------------------
#ifdef SELFTEST_NO_REGKEY
CreateUninstallRegKey=no
#endif
UninstallDisplayIcon={app}\LionCode.exe
UninstallDisplayName=Lion Code
InfoBeforeFile=README-install.md
SetupLogging=yes

[Tasks]
Name: "desktopicon"; Description: "Create a &desktop shortcut"; GroupDescription: "Additional icons:"

[Files]
; whole staged payload, one line: 3 Nuitka dists flattened (all DLL name
; collisions verified byte-identical), bun.exe, runtime-vulkan, MiMo source
; WITHOUT node_modules, launchers, skills, README-install.md
Source: "..\.lbcheck\stage\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Run]
; Plan B - no network needed: node_modules ships pre-packed (7za -snh -snl)
; and install_deps.cmd extracts it + recreates the junctions. Output goes to
; {app}\install-deps.log, ok marker {app}\install-deps.ok (test_install.ps1
; asserts both). ~60k files to unpack: roughly 30-90 s.
; NOTE the doubled quotes: Inno's own docs use Parameters: "/C ""{app}\x.cmd"""
; - a single quote pair gave "Mismatched or misplaced quotes" at compile time.
Filename: "{cmd}"; Parameters: "/C ""{app}\install_deps.cmd"""; Flags: runhidden waituntilterminated; StatusMsg: "Extracting MiMo TUI dependencies (offline, about 30-90 seconds)..."

[UninstallRun]
; ---------------------------------------------------------------------------
; The node_modules trees must go BEFORE Inno starts deleting the [Files] tree.
; Why: MiMo's workspace packages each have their own node_modules full of
; JUNCTIONS; Inno's recursive delete walks into them and then fails with
; error 145 (directory not empty) - measured 976 "Failed to delete directory"
; lines and 1014 leftover items when they were only listed under
; [UninstallDelete] (which runs AFTER the [Files] pass). cmd's `rmdir /s /q`
; removes a junction as a reparse point without following it, so it clears the
; tree in one go; the [UninstallDelete] entries stay as a fallback.
; ---------------------------------------------------------------------------
Filename: "{cmd}"; Parameters: "/C rmdir /s /q ""{app}\MiMo-Code-main\node_modules"""; Flags: runhidden waituntilterminated
Filename: "{cmd}"; Parameters: "/C rmdir /s /q ""{app}\MiMo-Code-main\packages\cli\node_modules"""; Flags: runhidden waituntilterminated
Filename: "{cmd}"; Parameters: "/C rmdir /s /q ""{app}\MiMo-Code-main\packages\plugin\node_modules"""; Flags: runhidden waituntilterminated
Filename: "{cmd}"; Parameters: "/C rmdir /s /q ""{app}\MiMo-Code-main\packages\sdk\node_modules"""; Flags: runhidden waituntilterminated
Filename: "{cmd}"; Parameters: "/C rmdir /s /q ""{app}\MiMo-Code-main\packages\shared\node_modules"""; Flags: runhidden waituntilterminated

[Icons]
Name: "{autoprograms}\Lion Code"; Filename: "{app}\StartLionCode.cmd"; WorkingDir: "{app}"; IconFilename: "{app}\LionCode.exe"; Comment: "Start Lion Code (backend + adapter + MiMo TUI)"
Name: "{autodesktop}\Lion Code"; Filename: "{app}\StartLionCode.cmd"; WorkingDir: "{app}"; IconFilename: "{app}\LionCode.exe"; Comment: "Start Lion Code (backend + adapter + MiMo TUI)"; Tasks: desktopicon

; ---------------------------------------------------------------------------
; "lion-code" must work from a plain cmd prompt after install (user request).
;   1) {app}\lion-code.cmd does the actual work (ships in [Files] through the
;      staged payload) and runs start.exe IN THE CURRENT CONSOLE - the MiMo TUI
;      pokes the console mode through FFI, so neither a new window nor a
;      hidden run is acceptable.
;   2) This entry appends {app} to the USER PATH in HKCU\Environment.
;      NEVER overwrite: {olddata} keeps whatever was there, and the two Check
;      functions below make the entries mutually exclusive (append only when a
;      PATH already exists and the dir is not in it yet; write a bare value
;      only when no PATH value exists at all).
;      Verified on Inno Setup 6.7.3: {olddata} + Check is the documented way.
;      Guarded by LionHKCUWritable(): on a machine where HKCU cannot be written
;      the Check returns False, so Inno SKIPS the entry instead of aborting the
;      whole install. MEASURED here: an unsigned installer runs at Low
;      Mandatory Level inside this sandbox and every HKCU write fails with
;      RegCreateKeyEx code 5 - without the guard that rolled the install back
;      (exit 5) after the files were already copied.
; ---------------------------------------------------------------------------
[Registry]
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{app}"; Check: LionPathMissing
Root: HKCU; Subkey: "Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{olddata};{app}"; Check: LionPathNeedsAppend

[UninstallDelete]
; node_modules as extracted by install_deps.cmd (7z output, junctions, ...)
Type: filesandordirs; Name: "{app}\MiMo-Code-main\node_modules"
; bun-era safety net (a run once left 16 dirs behind: error 145 = not empty).
; NOTE: a middle wildcard (packages\*\node_modules) did NOT match anything in
; the real self-test, so the four workspace packages are listed explicitly.
Type: filesandordirs; Name: "{app}\MiMo-Code-main\packages\cli\node_modules"
Type: filesandordirs; Name: "{app}\MiMo-Code-main\packages\plugin\node_modules"
Type: filesandordirs; Name: "{app}\MiMo-Code-main\packages\sdk\node_modules"
Type: filesandordirs; Name: "{app}\MiMo-Code-main\packages\shared\node_modules"
Type: filesandordirs; Name: "{app}\.lbcheck"
Type: filesandordirs; Name: "{app}\tmp"
Type: files; Name: "{app}\install-deps.log"
Type: files; Name: "{app}\install-deps.ok"
Type: files; Name: "{app}\relink-nm.done"
; NOTE: runtime junk lives under {app} on purpose - a Low-IL process cannot
; create %LOCALAPPDATA%\LionCode\* (measured Error 5), and keeping it in
; {app} also makes the uninstaller self-contained.
; last: only removed when nothing else is left
Type: dirifempty; Name: "{app}"

[Code]
{ Pascal Script needs the declaration BEFORE the first use; the helper block
  (PATH readers + WM_SETTINGCHANGE broadcast) lives further down, so forward it. }
procedure LionRefreshEnvironment(); forward;

{ Make a failed dependency extraction VISIBLE in non-silent installs instead of
  leaving the user with a TUI that silently does not start. Backend/adapter
  still work without node_modules, so this is a warning, not a hard failure. }
procedure CurStepChanged(CurStep: TSetupStep);
begin
  if CurStep = ssPostInstall then
    LionRefreshEnvironment();
  if CurStep = ssDone then
    if not WizardSilent then
      if not FileExists(ExpandConstant('{app}\install-deps.ok')) then
        MsgBox('MiMo TUI dependencies could not be extracted (see log).' + #13#10
               + #13#10
               + 'The Lion Code backend and adapter still work.' + #13#10
               + 'To retry:' + #13#10
               + ExpandConstant('{app}\install_deps.cmd') + #13#10 + #13#10
               + 'Log: ' + ExpandConstant('{app}\install-deps.log'),
               mbError, MB_OK);
end;

{ ===========================================================================
  PATH handling (HKCU\Environment). Measured on this machine:
  - Never overwrite: the olddata directive keeps the existing value, and the
    two Check functions make "bare value" and "append" mutually exclusive, so a
    user who already has a PATH never loses it.
  - A freshly opened cmd.exe only sees the new PATH after WM_SETTINGCHANGE is
    broadcast (the shell caches its environment); we broadcast it after the
    install AND after the uninstall. Explorer / Windows Terminal pick it up
    from there, so a NEW terminal gets lion-code. An already-running terminal
    keeps its old environment by design - tell the user to reopen it.
  Syntax below verified by compiling with Inno Setup 6.7.3:
    external 'SendMessageTimeoutA@user32.dll stdcall'  compiles fine,
    RegWriteExpandStringData does NOT exist in 6 -> RegWriteStringValue (REG_SZ).
  NOTE: do NOT put brace pairs (like the app constant) inside a [Code] comment:
  Pascal Script closes the comment at the first closing brace - measured as
  "'BEGIN' expected" pointing into this comment.
  =========================================================================== }

function LionReadUserPath(var s: String): Boolean;
begin
  Result := RegQueryStringValue(HKCU, 'Environment', 'Path', s);
  if not Result then
    s := '';
end;

{ Can this process write HKCU at all? Probed once and cached.
  The probe creates and immediately removes its own subkey, so a successful
  probe leaves nothing behind and a failed one never created anything.
  WHY: an unsigned installer runs at Low Mandatory Level inside this sandbox
  (measured: every HKCU write -> RegCreateKeyEx code 5) and a Registry entry
  that cannot be written makes Inno abort + roll back the entire install.
  Skipping the entry and saying so in the log is the honest, non-fatal
  behaviour. (Never start a [Code] comment line with something in brackets:
  the ISCC section scanner reads it as a section tag - measured "Invalid
  section tag".)
  NOTE the encoding of gHKCUProbe: Inno zero-initialises globals, so 0 has to
  mean "not probed yet" (a -1 sentinel would read as "already probed, no"). }
var
  gHKCUProbe: Integer;

function LionHKCUWritable(): Boolean;
begin
  if gHKCUProbe = 0 then begin
    if RegWriteStringValue(HKCU, 'Software\LionCodeInstallerProbe', 'v', '1') then begin
      RegDeleteKeyIncludingSubkeys(HKCU, 'Software\LionCodeInstallerProbe');
      gHKCUProbe := 1;
      Log('LionCode: HKCU is writable, the user PATH will be updated.');
    end else begin
      gHKCUProbe := 2;
      Log('LionCode: WARNING - HKCU is NOT writable from this process (Low '
        + 'Mandatory Level / locked-down profile). The user PATH was NOT '
        + 'updated; add the install dir to PATH manually.');
    end;
  end;
  Result := (gHKCUProbe = 1);
end;

function LionPathMissing(): Boolean;
var
  p: String;
begin
  Result := False;
  if not LionHKCUWritable() then
    Exit;
  LionReadUserPath(p);
  Result := (Trim(p) = '');
end;

function LionPathNeedsAppend(): Boolean;
var
  p: String;
begin
  Result := False;
  if not LionHKCUWritable() then
    Exit;
  LionReadUserPath(p);
  Result := (Trim(p) <> '') and
            (Pos(Lowercase(ExpandConstant('{app}')), Lowercase(p)) = 0);
end;

function LionSendMessageTimeout(hWnd: LongWord; Msg: LongWord; wParam: LongInt;
  lParam: String; fuFlags: LongWord; uTimeout: LongWord;
  var lpdwResult: LongWord): LongWord;
  external 'SendMessageTimeoutA@user32.dll stdcall';

procedure LionRefreshEnvironment();
var
  flags, res: LongWord;
begin
  flags := 2; { SMTO_ABORTIFHUNG }
  res := 0;
  LionSendMessageTimeout(HWND_BROADCAST, $001A, 0, 'Environment', flags, 5000, res);
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  p, appLower, outp: String;
  parts: TStringList;
  i: Integer;
begin
  if CurUninstallStep = usUninstall then begin
    { Remove the install dir from the user PATH BEFORE it disappears, otherwise
      the "no install dir left in PATH" test fails and the user keeps a
      dangling entry. (No brace pairs in this comment - see the note above.) }
    if RegQueryStringValue(HKCU, 'Environment', 'Path', p) then begin
      appLower := Lowercase(ExpandConstant('{app}'));
      parts := TStringList.Create;
      try
        parts.StrictDelimiter := True;
        parts.Delimiter := ';';
        parts.DelimitedText := p;
        for i := parts.Count - 1 downto 0 do
          if Lowercase(Trim(parts[i])) = appLower then
            parts.Delete(i);
        outp := '';
        for i := 0 to parts.Count - 1 do begin
          if Trim(parts[i]) = '' then
            Continue;
          if outp = '' then
            outp := parts[i]
          else
            outp := outp + ';' + parts[i];
        end;
        RegWriteStringValue(HKCU, 'Environment', 'Path', outp);
      finally
        parts.Free;
      end;
    end;
    if not LionHKCUWritable() then
      Log('LionCode: WARNING - uninstall could not clean the user PATH '
        + '(HKCU not writable); the entry may be left behind.');
  end;
  if (CurUninstallStep = usUninstall) or (CurUninstallStep = usPostUninstall) then
    LionRefreshEnvironment();
end;
