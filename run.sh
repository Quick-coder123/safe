#!/bin/bash
# Скрипт запуску калькулятора оренди сейфу

echo "🔐 Калькулятор оренди індивідуального сейфу"
echo "============================================"

# Перевірка наявності Python
if command -v python3 &> /dev/null; then
    echo "✅ Python3 знайдено"
    python3 safe_calculator.py
elif command -v python &> /dev/null; then
    echo "✅ Python знайдено"
    python safe_calculator.py
else
    echo "❌ Python не знайдено!"
    echo "Будь ласка, встановіть Python 3.8 або новіший"
    echo "https://www.python.org/downloads/"
    exit 1
fi
