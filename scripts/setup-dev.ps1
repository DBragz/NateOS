Param(
	[string]$OutputDir = "outputs"
)

Write-Host "[NateOS] Ensuring output directory: $OutputDir"
if (-not (Test-Path $OutputDir)) { New-Item -ItemType Directory -Path $OutputDir | Out-Null }

Write-Host "[NateOS] Creating docs and scripts folders if missing"
@("docs","scripts") | ForEach-Object { if (-not (Test-Path $_)) { New-Item -ItemType Directory -Path $_ | Out-Null } }

Write-Host "[NateOS] BMAD config expected at bmad/bmm/config.yaml"
if (-not (Test-Path "bmad/bmm/config.yaml")) {
	New-Item -ItemType Directory -Path "bmad/bmm" -Force | Out-Null
	@(
		"user_name: Nate",
		"communication_language: English",
		"output_folder: $OutputDir"
	) | Set-Content -Path "bmad/bmm/config.yaml"
	Write-Host "[NateOS] Created default BMAD config."
}

Write-Host "[NateOS] Dev setup complete."
