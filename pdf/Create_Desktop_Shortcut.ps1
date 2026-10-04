$desktopPath = [System.Environment]::GetFolderPath('Desktop')
$targetScript = "c:\Users\Anuj1\Downloads\Jules Apt\Launch_Aptimizer_Desktop.bat"
$iconPath = "c:\Users\Anuj1\Downloads\Jules Apt\frontend\public\favicon.ico"
$shortcutPath = Join-Path $desktopPath "Aptimizer Civil AI.lnk"

$WScriptShell = New-Object -ComObject WScript.Shell
$Shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$Shortcut.TargetPath = $targetScript
$Shortcut.WorkingDirectory = "c:\Users\Anuj1\Downloads\Jules Apt"
$Shortcut.Description = "Aptimizer Civil AI & Architectural Design Suite"
if (Test-Path $iconPath) {
    $Shortcut.IconLocation = $iconPath
}
$Shortcut.Save()

Write-Host "Created Desktop Shortcut at: $shortcutPath" -ForegroundColor Green
