@echo off
rem Скрипт запуску калькулятора оренди сейфу для Windows

echo 🔐 Калькулятор оренди індивідуального сейфу
echo ============================================

rem Перевірка наявності Python
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo ✅ Python знайдено
    python safe_calculator.py
) else (
    echo ❌ Python не знайдено!
    echo Будь ласка, встановіть Python 3.8 або новіший
    echo https://www.python.org/downloads/
    pause
)
