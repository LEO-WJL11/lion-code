; trivial sanity installer: does a plain Inno build even run on this machine?
[Setup]
AppName=LbTrivial
AppVersion=1.0
DefaultDirName={tmp}\lbtrivial_dest
PrivilegesRequired=lowest
DisableProgramGroupPage=yes
OutputDir=output
OutputBaseFilename=LbTrivial-Setup
Compression=lzma
[Files]
Source: "payload\StartLionCode.cmd"; DestDir: "{app}"; Flags: ignoreversion
