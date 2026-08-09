$ErrorActionPreference = 'Stop'

$projectRoot = Split-Path -Parent $PSScriptRoot
$dataDirectory = Join-Path $PSScriptRoot 'data'
$fixturePath = Join-Path $dataDirectory 'site-data.json'
$archivePath = Join-Path $PSScriptRoot 'site-transfer.tar.gz'

New-Item -ItemType Directory -Force -Path $dataDirectory | Out-Null

Push-Location $projectRoot
try {
    $env:PYTHONUTF8 = '1'
    python manage.py dumpdata `
        --settings=config.settings.local `
        --exclude contenttypes `
        --exclude auth.permission `
        --exclude admin.logentry `
        --exclude sessions.session `
        --exclude axes `
        --exclude thumbnail `
        --exclude advertising.adimpression `
        --indent 2 `
        --output $fixturePath

    tar -czf $archivePath deployment/data/site-data.json media
}
finally {
    Pop-Location
}

Write-Host "Production transfer archive created: $archivePath"
Write-Host "It contains the database fixture and uploaded media. Keep it private."
