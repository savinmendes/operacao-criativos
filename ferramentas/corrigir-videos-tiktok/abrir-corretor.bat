@echo off
rem Abre o corretor de video no navegador.
rem Deixe esta janela aberta enquanto usa: e ela que roda o ffmpeg.
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
"C:\Users\PICHAU\AppData\Local\Programs\Python\Python312\python.exe" "%~dp0servidor.py"
echo.
echo O corretor foi encerrado.
pause
