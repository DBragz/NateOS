Param(
	[string]$Python = "python"
)

Write-Host "[NateOS] Launching Desktop GUI (Tkinter)"
Write-Host "[NateOS] Ensure the API is running: ./scripts/run-web-gui.ps1"

# Detect Python base prefix to locate Tcl/Tk
try {
	$prefix = & $Python -c "import sys; print(sys.base_prefix)"
	if ($LASTEXITCODE -eq 0 -and $prefix) {
		$tclDir = Join-Path $prefix "tcl\tcl8.6"
		$tkDir = Join-Path $prefix "tcl\tk8.6"
		$dllDir = Join-Path $prefix "DLLs"

		if (-not $env:TCL_LIBRARY -and (Test-Path $tclDir)) {
			$env:TCL_LIBRARY = $tclDir
			Write-Host "[NateOS] Set TCL_LIBRARY=$tclDir"
		}
		if (-not $env:TK_LIBRARY -and (Test-Path $tkDir)) {
			$env:TK_LIBRARY = $tkDir
			Write-Host "[NateOS] Set TK_LIBRARY=$tkDir"
		}
		if (Test-Path $dllDir -and ($env:PATH -notlike "*$dllDir*")) {
			$env:PATH = "$dllDir;$env:PATH"
			Write-Host "[NateOS] Prepending $dllDir to PATH"
		}
	}
} catch { }

& $Python "src/mgmt/desktop/app.py"
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
