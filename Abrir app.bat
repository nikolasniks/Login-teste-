@echo off
rem Abre o app com dois cliques. Na primeira vez, prepara o ambiente Python sozinho.
title Abrindo o app...
cd /d "%~dp0Janela_login\Projeto"

if exist ".venv\Scripts\pythonw.exe" goto abrir

echo Preparando o ambiente pela primeira vez (leva 1 ou 2 minutos)...
set "UV=uv"
where uv >nul 2>nul || set "UV=%USERPROFILE%\.local\bin\uv.exe"
if exist "%UV%" goto com_uv
where uv >nul 2>nul && goto com_uv

rem Sem o uv: usa o Python instalado no Windows
py -3 -m venv .venv || python -m venv .venv || goto sem_python
".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto erro
goto abrir

:com_uv
"%UV%" venv .venv --python 3.13 || goto erro
"%UV%" pip install --python ".venv\Scripts\python.exe" -r requirements.txt || goto erro

:abrir
rem pythonw: abre so a janela do app, sem a tela preta do terminal
start "" ".venv\Scripts\pythonw.exe" src\main.py
exit /b 0

:sem_python
echo.
echo Nao encontrei o Python nem o uv neste computador.
echo Instale o Python 3.13 em https://www.python.org/downloads/ e abra este arquivo de novo.
pause
exit /b 1

:erro
echo.
echo Algo deu errado ao preparar o ambiente. Veja a mensagem acima.
pause
exit /b 1
