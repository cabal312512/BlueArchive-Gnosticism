[CmdletBinding()]
param(
 [Parameter(Mandatory)][string]$JobDirectory,
 [Parameter(Mandatory)][string]$Feedback,
 [ValidateSet('low','medium','high')][string]$ReasoningEffort='medium'
)
$ErrorActionPreference='Stop'
$job=(Resolve-Path -LiteralPath $JobDirectory).Path
$allowed=[IO.Path]::GetFullPath('F:\DeepSeekHarness\Jobs')+'\'
if(!$job.StartsWith($allowed,[StringComparison]::OrdinalIgnoreCase)){throw 'Use an existing independent harness job.'}
$log=Get-ChildItem -LiteralPath $job -Filter '*.run.stdout.log'|Sort-Object Name|Select-Object -Last 1
if(!$log){throw 'No prior run in this job.'}
$session=[IO.File]::ReadLines($log.FullName)|ForEach-Object{try{$_|ConvertFrom-Json}catch{}}|Where-Object type -eq 'session'|Select-Object -First 1
if(!$session.sessionId){throw 'No resumable session ID found.'}
$task=Join-Path $job ('followup-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss-fff')+'.md')
[IO.File]::WriteAllText($task,$Feedback+"`nContinue the existing report only. Remain read-only. Return findings; never edit project documents.",[Text.UTF8Encoding]::new($false))
& F:\DeepSeekHarness\Invoke-DeepSeek.ps1 -Mode Run -TaskFile $task -JobDirectory $job -SessionId $session.sessionId -ReasoningEffort $ReasoningEffort
