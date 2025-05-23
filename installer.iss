[Setup]
AppName=DrawHelper
AppVersion=2.0
DefaultDirName={userappdata}\DrawHelper
DefaultGroupName=DrawHelper
OutputDir=dist_installer
OutputBaseFilename=DrawHelperSetup
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\DrawHelper\*"; DestDir: "{app}"; Flags: recursesubdirs createallsubdirs

[Icons]
Name: "{autoprograms}\DrawHelper"; Filename: "{app}\DrawHelper.exe"
Name: "{userdesktop}\DrawHelper"; Filename: "{app}\DrawHelper.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Создать ярлык на рабочем столе"; GroupDescription: "Дополнительные задачи:"

[UninstallDelete]
Name: "{app}"; Type: filesandordirs
