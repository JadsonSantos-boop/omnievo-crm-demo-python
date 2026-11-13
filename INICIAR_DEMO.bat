@echo off
title OMNIEVO CRM - Sistema de Demonstracao B2B
color 0b
chcp 65001 >nul
cls

echo =========================================================================
echo               OMNIEVO CRM - AMBIENTE DE DEMONSTRACAO B2B
echo          Cosmeticos, Dermocosmeticos e Linha Estetica Comercial
echo =========================================================================
echo.
echo [1/3] Verificando ambiente Python...

python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERRO] Python nao foi localizado neste computador.
    echo Por favor, instale o Python 3.10+ em https://www.python.org/downloads/
    echo e certifique-se de marcar a opcao "Add Python to PATH".
    echo.
    pause
    exit /b
)

echo [2/3] Verificando dependencias essenciais (Streamlit, Pandas, Plotly)...
python -c "import streamlit, pandas, plotly" >nul 2>&1
if %errorlevel% neq 0 (
    echo Instalando pacotes necessarios automaticamente...
    python -m pip install -r requirements.txt
)

echo [3/3] Iniciando o Omnievo CRM de Demonstracao...
echo.
echo =========================================================================
echo   SUCESSO! O sistema abrira automaticamente no seu navegador padrao.
echo   URL Local: http://localhost:8501
echo   Para encerrar a apresentacao, basta fechar esta janela preta.
echo =========================================================================
echo.

cd /d "%~dp0"
python -m streamlit run app.py --server.headless false --server.port 8501

pause
