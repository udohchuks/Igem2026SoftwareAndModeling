$ErrorActionPreference = 'Stop'

$sourcePath = Join-Path $PSScriptRoot 'overview-process-draft.svg'
$outputPath = Join-Path $PSScriptRoot 'overview-process-draft-embedded.svg'
$svg = [System.IO.File]::ReadAllText($sourcePath)

$imageNames = @(
    'overview-stage-01-leachant-web.png',
    'overview-stage-02-leaching-web.png',
    'overview-stage-03-golb-capture-web.png',
    'overview-stage-04-thiourea-release-web.png',
    'overview-stage-05-metallic-gold-web.png'
)

foreach ($imageName in $imageNames) {
    $imagePath = Join-Path $PSScriptRoot $imageName
    $encoded = [Convert]::ToBase64String([System.IO.File]::ReadAllBytes($imagePath))
    $dataUri = "data:image/png;base64,$encoded"
    $svg = $svg.Replace("href=`"$imageName`"", "href=`"$dataUri`"")
}

[System.IO.File]::WriteAllText($outputPath, $svg, [System.Text.UTF8Encoding]::new($false))
