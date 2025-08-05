#define MyAppVersion "1.0.5"

[Setup]
AppName=Image to Text
AppVersion={#MyAppVersion}
DefaultDirName={autopf}\Image to Text
DefaultGroupName=Image to Text
OutputBaseFilename=installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main\Image to Text.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\main\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Image to Text"; Filename: "{app}\Image to Text.exe"
Name: "{group}\Uninstall Image to Text"; Filename: "{uninstallexe}"