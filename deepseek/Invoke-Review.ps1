[CmdletBinding()]
param(
 [Parameter(Mandatory)][string]$TaskFile,
 [Parameter(Mandatory)][string[]]$InputFiles,
 [string]$Name='review',
 [int]$TimeoutSeconds=900,
 [ValidateSet('low','medium','high')][string]$ReasoningEffort='medium'
)
$ErrorActionPreference='Stop'
$harnessRoot='F:\DeepSeekHarness'
$safeName=$Name -replace '[^a-zA-Z0-9_-]','-'
$stamp=[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff')
$job=Join-Path $harnessRoot ('Jobs\'+$stamp+'-'+$safeName)
New-Item -ItemType Directory -Path (Join-Path $job 'inputs') -Force|Out-Null
$manifest=@();$index=0
foreach($file in $InputFiles){
 $source=(Resolve-Path -LiteralPath $file).Path
 if(![IO.File]::Exists($source)){throw 'Only explicit input files are accepted.'}
 if($source -match '(?i)(api[-_]?key|credential|\.env(?:\.|$)|secret|\.dpapi$)'){throw 'Credentials must never be staged as research inputs.'}
 $destination=Join-Path $job ('inputs\'+('{0:D3}-' -f $index)+[IO.Path]::GetFileName($source))
 Copy-Item -LiteralPath $source -Destination $destination
 $manifest+=@{file=[IO.Path]::GetFileName($destination);sha256=(Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash;bytes=(Get-Item -LiteralPath $destination).Length}
 $index++
}
$manifest|ConvertTo-Json -Depth 4|Set-Content -LiteralPath (Join-Path $job 'inputs.json') -Encoding utf8
$task=[IO.File]::ReadAllText((Resolve-Path -LiteralPath $TaskFile).Path)
$task+="`n`nStaged input files (read each completely):`n"+($manifest|ConvertTo-Json -Depth 4)
$task+="`nUse only these staged inputs and public sources explicitly requested by the task. Never inspect credentials, unrelated paths, or production project files. Return findings in your final response; do not write any files."
$stagedTask=Join-Path $job 'task.md'
[IO.File]::WriteAllText($stagedTask,$task,[Text.UTF8Encoding]::new($false))
& (Join-Path $harnessRoot 'Invoke-DeepSeek.ps1') -Mode Run -TaskFile $stagedTask -JobDirectory $job -TimeoutSeconds $TimeoutSeconds -ReasoningEffort $ReasoningEffort
foreach($item in $manifest){
 $destination=Join-Path $job ('inputs\'+$item.file)
 if((Get-FileHash -LiteralPath $destination -Algorithm SHA256).Hash -ne $item.sha256){throw 'Staged input changed during review.'}
}
Write-Output ('Review outputs: '+$job)
