Set-Location -Path $PSScriptRoot

if ($args.Count -eq 0) {
    $mode = "single"
} else {
    $mode = $args[0]
}

switch ($mode) {
    "single" {
        Write-Host "Run test in one thread (default)"
        uv run pytest -v --tb=short -n 1
    }
    "three" {
        Write-Host "Run tests in three threads"
        uv run pytest -v --tb=short -n 3
    }
    default {
        Write-Host "Error incorrect mode: '$mode'"
        Write-Host "Press any key"
        $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

Write-Host ""
Write-Host "Press any key"
$Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
