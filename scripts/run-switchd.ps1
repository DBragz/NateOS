Param(
	[string]$Python = "python"
)

Write-Host "[NateOS] Running switchd"
& $Python "src/switchd/switchd.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
