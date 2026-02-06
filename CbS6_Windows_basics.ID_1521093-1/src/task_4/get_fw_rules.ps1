# get_fw_rules.ps1

# Список имен наших правил для фильтрации
$MyRules = @("Block_http_conn", "Allow_rdp_conn", "Block_ftp_conn", "Block_ping_conn")

# Получаем правила и выбираем нужные свойства
Get-NetFirewallRule | Where-Object { $MyRules -contains $_.DisplayName } | ForEach-Object {
    $Filter = $_ | Get-NetFirewallPortFilter
    [PSCustomObject]@{
        Name        = $_.DisplayName
        Enabled     = $_.Enabled
        Protocol    = $Filter.Protocol
        LocalPort   = $Filter.LocalPort
        RemotePort  = $Filter.RemotePort
        Action      = $_.Action
        Profile     = $_.Profile
    }
} | Format-Table -AutoSize | Out-File -FilePath "result.txt" -Encoding UTF8

Write-Host "Success! Results saved to result.txt" -ForegroundColor Cyan