# REELS SEM APARECER - instalador para Windows (PowerShell).
#
#   irm https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/main/instalar.ps1 | iex
#
# O que ele faz:
#   1. Confere se o Git para Windows esta instalado (ele traz o "Git Bash", que a skill e o Claude Code usam para
#      rodar os comandos). Se faltar, instala pelo winget (o Windows pede a sua confirmacao).
#   2. Chama o instalador principal (instalar.sh), que baixa a skill para a pasta .claude\skills do seu usuario e poe
#      todo o resto DENTRO dela. Nada mais e instalado no sistema.
# Pode rodar de novo quantas vezes quiser. (Sem acentos de proposito: o PowerShell antigo le este arquivo em outra codificacao.)

$ErrorActionPreference = "Stop"
$ramo = if ($env:RSA_RAMO) { $env:RSA_RAMO } else { "main" }

function Find-GitBash {
  $candidatos = @(
    (Join-Path $env:ProgramFiles "Git\bin\bash.exe"),
    (Join-Path $env:LOCALAPPDATA "Programs\Git\bin\bash.exe")
  )
  if (${env:ProgramFiles(x86)}) { $candidatos += (Join-Path ${env:ProgramFiles(x86)} "Git\bin\bash.exe") }
  $git = Get-Command git.exe -ErrorAction SilentlyContinue
  if ($git) { $candidatos += (Join-Path (Split-Path (Split-Path $git.Source)) "bin\bash.exe") }
  foreach ($c in $candidatos) { if ($c -and (Test-Path $c)) { return $c } }
  return $null
}

$bash = Find-GitBash
if (-not $bash) {
  Write-Host ""
  Write-Host "Falta o Git para Windows. Instalando pelo winget (o Windows pode pedir a sua confirmacao)..."
  if (Get-Command winget.exe -ErrorAction SilentlyContinue) {
    winget install --id Git.Git -e --source winget --accept-package-agreements --accept-source-agreements
  }
  $bash = Find-GitBash
  if (-not $bash) {
    Write-Host ""
    Write-Host "Nao consegui instalar o Git sozinho. Faca assim:"
    Write-Host "  1. Abra https://git-scm.com/download/win e baixe o instalador."
    Write-Host "  2. Instale clicando em Next ate o fim (as opcoes padrao servem)."
    Write-Host "  3. Feche e abra o PowerShell e cole este comando de novo."
    if ($MyInvocation.MyCommand.Path) { exit 3 } else { return }
  }
}

Write-Host "Git Bash: $bash"
$env:RSA_RAMO = $ramo
& $bash -lc "curl -fsSL https://raw.githubusercontent.com/Felpborges/reels-sem-aparecer/$ramo/instalar.sh | bash"
$codigo = $LASTEXITCODE
if ($codigo -eq 0) {
  Write-Host ""
  Write-Host "Feche e abra o Claude Code para os atalhos /reel-... aparecerem."
}
# rodando de um arquivo (testes) devolve o codigo; colado no PowerShell (irm | iex) nao fecha a janela da pessoa
if ($MyInvocation.MyCommand.Path) { exit $codigo }
