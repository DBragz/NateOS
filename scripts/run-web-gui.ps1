Param(
	[string]$Python = "python",
	[int]$Port = 8080
)

Write-Host "[NateOS] Starting Web Management GUI on port $Port"
Write-Host "[NateOS] Access the GUI at: http://localhost:$Port/static/index.html"
Write-Host "[NateOS] API will be available at: http://localhost:$Port/api"

$env:PORT = $Port
& $Python "src/mgmt/web/api.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

