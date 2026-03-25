$FilePath = Join-Path $PSScriptRoot "tmp.txt"
$random = Get-Random -Minimum 0 -Maximum 101
$random | Out-File -FilePath $FilePath -Encoding UTF8
