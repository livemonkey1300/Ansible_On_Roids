#!powershell
# This file is part of Ansible
# WANT_JSON
# POWERSHELL_COMMON
$data = Get-ChildItem -Directory -Exclude Public -Path C:\Users | Select-Object -Property Name
$result = New-Object psobject @{
users = $data
changed = $false
};
Exit-Json $result;
