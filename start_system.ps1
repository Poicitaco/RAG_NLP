param(
    [int]$BackendPort = 8000,
    [int]$FrontendPort = 3000,
    [string]$HostAddress = "127.0.0.1",
    [switch]$OpenBrowser,
    [switch]$NoWarmup,
    [switch]$Stop,
    [switch]$Restart
)

$ErrorActionPreference = "Stop"

function Write-Step {
    param([string]$Message)
    Write-Host "`n==> $Message" -ForegroundColor Cyan
}

function Write-Ok {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Warn {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Get-PortProcessId {
    param([int]$Port)
    $conn = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue |
        Select-Object -First 1
    if ($conn) {
        return [int]$conn.OwningProcess
    }
    return $null
}

function Stop-PortProcess {
    param(
        [int]$Port,
        [string]$Name
    )
    $pidOnPort = Get-PortProcessId -Port $Port
    if ($pidOnPort) {
        Write-Warn "$Name dang chay tren port $Port, dung PID $pidOnPort"
        Stop-Process -Id $pidOnPort -Force
        Start-Sleep -Seconds 2
        Write-Ok "Da dung $Name tren port $Port"
    }
}

function Wait-HttpOk {
    param(
        [string]$Url,
        [int]$TimeoutSeconds = 60
    )
    $deadline = (Get-Date).AddSeconds($TimeoutSeconds)
    $lastError = ""
    while ((Get-Date) -lt $deadline) {
        try {
            $response = Invoke-WebRequest -Uri $Url -UseBasicParsing -TimeoutSec 5
            if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) {
                return $true
            }
        } catch {
            $lastError = $_.Exception.Message
        }
        Start-Sleep -Seconds 2
    }
    throw "Khong goi duoc $Url sau $TimeoutSeconds giay. Loi cuoi: $lastError"
}

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendPython = Join-Path $Root ".venv\Scripts\python.exe"
$FrontendDir = Join-Path $Root "frontend-next"
$LogsDir = Join-Path $Root "logs"
$FrontendEnv = Join-Path $FrontendDir ".env.local"
$BackendLog = Join-Path $LogsDir "run_backend_8000.log"
$BackendErr = Join-Path $LogsDir "run_backend_8000.err.log"
$FrontendLog = Join-Path $LogsDir "run_frontend_3000.log"
$FrontendErr = Join-Path $LogsDir "run_frontend_3000.err.log"

if (!(Test-Path $LogsDir)) {
    New-Item -ItemType Directory -Path $LogsDir | Out-Null
}

if ($Stop -or $Restart) {
    Write-Step "Dung cac server dang chay neu co"
    Stop-PortProcess -Port $FrontendPort -Name "frontend"
    Stop-PortProcess -Port $BackendPort -Name "backend"
    if ($Stop -and !$Restart) {
        Write-Ok "Da dung he thong"
        exit 0
    }
}

Write-Step "Kiem tra moi truong"
if (!(Test-Path $BackendPython)) {
    throw "Khong thay Python venv tai $BackendPython. Hay tao/cai .venv truoc."
}
if (!(Test-Path $FrontendDir)) {
    throw "Khong thay thu muc frontend-next tai $FrontendDir"
}
if (!(Test-Path (Join-Path $FrontendDir "node_modules"))) {
    throw "Chua co frontend-next\node_modules. Hay chay: cd frontend-next; npm install"
}

$npm = Get-Command npm.cmd -ErrorAction SilentlyContinue
if (!$npm) {
    throw "Khong thay npm.cmd trong PATH"
}
Write-Ok "Moi truong co .venv va node_modules"

Write-Step "Dong bo cau hinh frontend API"
$apiUrl = "http://localhost:$BackendPort/api/v1"
"NEXT_PUBLIC_API_URL=$apiUrl" | Set-Content -Path $FrontendEnv -Encoding UTF8
Write-Ok "frontend-next/.env.local -> NEXT_PUBLIC_API_URL=$apiUrl"

Write-Step "Khoi dong backend"
$backendPid = Get-PortProcessId -Port $BackendPort
if ($backendPid) {
    Write-Warn "Backend port $BackendPort da co process PID $backendPid, giu nguyen"
} else {
    $backendArgs = @(
        "-m", "uvicorn",
        "backend.main:app",
        "--host", $HostAddress,
        "--port", "$BackendPort"
    )
    $backend = Start-Process `
        -FilePath $BackendPython `
        -ArgumentList $backendArgs `
        -WorkingDirectory $Root `
        -RedirectStandardOutput $BackendLog `
        -RedirectStandardError $BackendErr `
        -WindowStyle Hidden `
        -PassThru
    Write-Ok "Backend started PID $($backend.Id)"
}

Write-Step "Khoi dong frontend"
$frontendPid = Get-PortProcessId -Port $FrontendPort
if ($frontendPid) {
    Write-Warn "Frontend port $FrontendPort da co process PID $frontendPid, giu nguyen"
} else {
    $frontendArgs = @(
        "run", "dev", "--",
        "--hostname", $HostAddress,
        "--port", "$FrontendPort"
    )
    $frontend = Start-Process `
        -FilePath $npm.Source `
        -ArgumentList $frontendArgs `
        -WorkingDirectory $FrontendDir `
        -RedirectStandardOutput $FrontendLog `
        -RedirectStandardError $FrontendErr `
        -WindowStyle Hidden `
        -PassThru
    Write-Ok "Frontend started PID $($frontend.Id)"
}

Write-Step "Health check"
$backendHealthUrl = "http://$HostAddress`:$BackendPort/health"
$frontendUrl = "http://$HostAddress`:$FrontendPort/"
Wait-HttpOk -Url $backendHealthUrl -TimeoutSeconds 90 | Out-Null
Write-Ok "Backend healthy: $backendHealthUrl"
Wait-HttpOk -Url $frontendUrl -TimeoutSeconds 90 | Out-Null
Write-Ok "Frontend ready: $frontendUrl"

if (!$NoWarmup) {
    Write-Step "Warm-up backend chat pipeline"
    $warmupBody = @{
        message = "Toi bi dau dau nen uong thuoc gi?"
        session_id = "startup-warmup"
    } | ConvertTo-Json
    try {
        Invoke-RestMethod `
            -Uri "http://$HostAddress`:$BackendPort/api/v1/chat/" `
            -Method Post `
            -Body $warmupBody `
            -ContentType "application/json" `
            -TimeoutSec 120 | Out-Null
        Write-Ok "Backend chat pipeline warmed up"
    } catch {
        Write-Warn "Warm-up khong thanh cong: $($_.Exception.Message)"
    }
}

Write-Host ""
Write-Host "SafeRAG Pharma dang chay:" -ForegroundColor Green
Write-Host "  Frontend: $frontendUrl"
Write-Host "  Backend : http://$HostAddress`:$BackendPort"
Write-Host "  Docs    : http://$HostAddress`:$BackendPort/docs"
Write-Host ""
Write-Host "Log files:"
Write-Host "  Backend stdout : $BackendLog"
Write-Host "  Backend stderr : $BackendErr"
Write-Host "  Frontend stdout: $FrontendLog"
Write-Host "  Frontend stderr: $FrontendErr"
Write-Host ""
Write-Host "Dung he thong: .\start_system.ps1 -Stop"
Write-Host "Restart     : .\start_system.ps1 -Restart"
Write-Host "Bo warm-up  : .\start_system.ps1 -NoWarmup"

if ($OpenBrowser) {
    Start-Process $frontendUrl
}
