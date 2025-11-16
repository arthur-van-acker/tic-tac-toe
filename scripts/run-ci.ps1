param(
    [string]$Python = "python",
    [switch]$SkipEditableInstall
)

$ErrorActionPreference = "Stop"

function Invoke-Step {
    param(
        [string]$Label,
        [scriptblock]$Operation
    )

    Write-Host "`n>>> $Label" -ForegroundColor Cyan
    & $Operation
}

function Invoke-PythonModule {
    param(
        [string]$Module,
        [string[]]$Arguments = @()
    )

    & $Python -m $Module @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command '$Python -m $Module $Arguments' failed with exit code $LASTEXITCODE"
    }
}

Write-Host "Running local CI checks with $Python" -ForegroundColor Green

if (-not $SkipEditableInstall) {
    Invoke-Step -Label "Installing project in editable mode" -Operation {
        Invoke-PythonModule -Module pip -Arguments @("install", "-e", ".")
    }
}

Invoke-Step -Label "Tox lint/type/test matrix" -Operation {
    Invoke-PythonModule -Module tox -Arguments @("-e", "lint,type,py313")
}

Write-Host "`nAll local CI checks completed successfully." -ForegroundColor Green
