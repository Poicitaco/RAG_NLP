$ErrorActionPreference = "Stop"

$conn = Get-NetTCPConnection -LocalPort 8000 -State Listen -ErrorAction SilentlyContinue | Select-Object -First 1
if ($conn) {
    Stop-Process -Id $conn.OwningProcess -Force
}

$backend = Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000" -PassThru -WindowStyle Hidden

Write-Host "Waiting for backend to be ready..."
Start-Sleep -Seconds 10

Write-Host "Running API test script..."
.\.venv\Scripts\python.exe test_api.py

Write-Host "Stopping backend..."
Stop-Process -Id $backend.Id -Force
Write-Host "Done"
