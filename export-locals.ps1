# RUN like: `. .\import-locals.ps1`

$envFilePath = ".\.env"

if (Test-Path $envFilePath) {
    Write-Host "Loading environment variables from $envFilePath"

    Get-Content $envFilePath | ForEach-Object {
        if ($_ -notmatch '^\s*#' -and $_ -match '^\s*(\w+)\s*=\s*(.+)$') {
            $key = $matches[1]
            $value = $matches[2].Trim('"')  # Remove surrounding quotes if any
            [System.Environment]::SetEnvironmentVariable($key, $value, "Process")
            Write-Host "Set $key"
        }
    }

    Write-Host "Environment variables loaded successfully."
} else {
    Write-Error ".env file not found at $envFilePath"
}