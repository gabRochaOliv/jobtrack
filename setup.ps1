# =============================================================
# JobTrack - Setup automatico (Python + venv + Django + banco)
# Uso: .\setup.ps1
# =============================================================

$ErrorActionPreference = "Stop"

function Write-Step($msg) { Write-Host "`n==> $msg" -ForegroundColor Cyan }
function Write-OK($msg)   { Write-Host "    $msg" -ForegroundColor Green }
function Write-Warn($msg) { Write-Host "    $msg" -ForegroundColor Yellow }
function Write-Err($msg)  { Write-Host "    $msg" -ForegroundColor Red }

Write-Host "`n================================================" -ForegroundColor Magenta
Write-Host "  JobTrack - Setup automatico" -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Magenta

# -------------------------------------------------------------
# Passo 0: desativar venv atual se estiver ativo
# -------------------------------------------------------------
if ($env:VIRTUAL_ENV) {
    Write-Step "Desativando ambiente virtual atual"
    try { & deactivate } catch { }
}

# -------------------------------------------------------------
# Passo 1: Procurar Python 3.10+ no sistema
# -------------------------------------------------------------
Write-Step "Procurando Python 3.10 ou superior"

$pythonExe = $null
$candidates = @("3.13", "3.12", "3.11", "3.10")

foreach ($v in $candidates) {
    $out = & py "-$v" --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $pythonExe = "py -$v"
        Write-OK "Encontrado: $out (via '$pythonExe')"
        break
    }
}

# -------------------------------------------------------------
# Passo 2: Se nao achou, instalar via winget
# -------------------------------------------------------------
if (-not $pythonExe) {
    Write-Warn "Nenhum Python 3.10+ encontrado."
    Write-Step "Verificando winget (gerenciador de pacotes do Windows)"

    $wingetOk = $false
    try { & winget --version | Out-Null; $wingetOk = ($LASTEXITCODE -eq 0) } catch { }

    if (-not $wingetOk) {
        Write-Err "winget nao esta disponivel neste Windows."
        Write-Err "Baixe o Python 3.12 manualmente em: https://www.python.org/downloads/"
        Write-Err "No instalador, marque 'Add python.exe to PATH', instale e rode .\setup.ps1 de novo."
        exit 1
    }

    Write-OK "winget disponivel. Instalando Python 3.12 (vai pedir confirmacao do Windows)..."
    winget install -e --id Python.Python.3.12 --accept-source-agreements --accept-package-agreements --scope user

    if ($LASTEXITCODE -ne 0) {
        Write-Err "Falha na instalacao via winget. Instale manualmente."
        exit 1
    }

    # Atualiza PATH da sessao atual
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path", "User")

    # Tenta de novo
    $out = & py "-3.12" --version 2>$null
    if ($LASTEXITCODE -eq 0) {
        $pythonExe = "py -3.12"
        Write-OK "Instalado: $out"
    } else {
        Write-Err "Python 3.12 instalado mas 'py -3.12' nao foi encontrado nesta sessao."
        Write-Err "FECHE este terminal, abra um novo, e rode .\setup.ps1 novamente."
        exit 1
    }
}

# -------------------------------------------------------------
# Passo 3: Remover .venv antigo (se tiver Python < 3.10)
# -------------------------------------------------------------
if (Test-Path ".venv") {
    Write-Step "Removendo ambiente virtual antigo (.venv)"
    Remove-Item -Recurse -Force .venv
    Write-OK "Removido."
}

# -------------------------------------------------------------
# Passo 4: Criar venv novo
# -------------------------------------------------------------
Write-Step "Criando novo ambiente virtual com Python 3.12"
Invoke-Expression "$pythonExe -m venv .venv"
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Err "Falha ao criar .venv"
    exit 1
}
Write-OK "Ambiente virtual criado em .venv"

$venvPy = ".\.venv\Scripts\python.exe"

# -------------------------------------------------------------
# Passo 5: Instalar dependencias
# -------------------------------------------------------------
Write-Step "Atualizando pip"
& $venvPy -m pip install --upgrade pip --quiet

Write-Step "Instalando Django (pode levar 30s)"
& $venvPy -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { Write-Err "Falha ao instalar dependencias"; exit 1 }
Write-OK "Django instalado."

# -------------------------------------------------------------
# Passo 6: Migrar banco
# -------------------------------------------------------------
Write-Step "Criando banco de dados SQLite"
& $venvPy manage.py makemigrations candidaturas
& $venvPy manage.py migrate
Write-OK "Banco de dados pronto (db.sqlite3)"

# -------------------------------------------------------------
# Pronto
# -------------------------------------------------------------
Write-Host "`n================================================" -ForegroundColor Green
Write-Host "  TUDO PRONTO!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "`nPara subir o servidor, rode:" -ForegroundColor White
Write-Host "    .\.venv\Scripts\activate" -ForegroundColor Yellow
Write-Host "    python manage.py runserver" -ForegroundColor Yellow
Write-Host "`nOu num comando so:" -ForegroundColor White
Write-Host "    .\.venv\Scripts\python.exe manage.py runserver" -ForegroundColor Yellow
Write-Host "`nDepois abra no navegador: http://127.0.0.1:8000`n" -ForegroundColor White
