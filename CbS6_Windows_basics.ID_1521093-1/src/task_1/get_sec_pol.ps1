# 1. Admin Check
if (-NOT ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole] "Administrator")) {
    Write-Warning "Error: Run as Administrator!"
    Exit
}

# 2. Files
$OutputFile = "secpol.txt"
$TempFile = "$env:TEMP\temp_policy.inf"

# 3. Export
secedit /export /cfg $TempFile /quiet

# 4. Save to file
Get-Content $TempFile | Out-File -FilePath $OutputFile -Encoding UTF8

# 5. Cleanup
if (Test-Path $TempFile) { Remove-Item $TempFile }

Write-Host "Success! File $OutputFile created." -ForegroundColor Cyan