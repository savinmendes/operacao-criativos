@echo off
rem Eleva sozinho e roda o conserto da pilha Bluetooth.
rem Clique duplo. Vai aparecer o aviso do Windows pedindo permissao de administrador.

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Pedindo permissao de administrador...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0consertar-bluetooth.ps1"
