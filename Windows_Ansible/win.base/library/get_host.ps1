#!powershell
# This file is part of Ansible
# WANT_JSON
# POWERSHELL_COMMON
$data = Get-Host | Select Version
$win = Get-WindowsFeature -Name AD*, Web* | Select Name , Installed , InstallState
$result = New-Object psobject @{
get_features = $win
get_host_version = $data
changed = $false
};
Exit-Json $result;
