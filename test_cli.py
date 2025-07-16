#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CLI версія калькулятора сейфу для тестування функціональності
"""

import sqlite3
from datetime import datetime, timedelta

class SafeCalculatorCLI:
    """CLI версія калькулятора"""
    
    def __init__(self):
        self.rates = {
            "dailyRates": [
                {"term": "1-30 днів", "rates": {"1 категорія": 39, "2 категорія": 51, "3 категорія": 63, "4 категорія": 63, "5 категорія": 63}},
                {"term": "31-90 днів", "rates": {"1 категорія": 25, "2 категорія": 26, "3 категорія": 28, "4 категорія": 35, "5 категорія": 43}},
                {"term": "91-180 днів", "rates": {"1 категорія": 22, "2 категорія": 24, "3 категорія": 26, "4 категорія": 33, "5 категорія": 41}},
                {"term": "181-365 днів", "rates": {"1 категорія": 20, "2 категорія": 22, "3 категорія": 24, "4 категорія": 29, "5 категорія": 40}}
            ],
            "insuranceRates": [
                {"term": "1-90 днів", "cost": 285},
                {"term": "91-180 днів", "cost": 370},
                {"term": "181-270 днів", "cost": 430},
                {"term": "271-365 днів", "cost": 550}
            ],
            "attorneyTariff": 300
        }
    
    def get_daily_rate(self, category: str, days: int) -> float:
        """Отримання денної ставки"""
        for rate_range in self.rates["dailyRates"]:
            if "1-30" in rate_range["term"] and days <= 30:
                return rate_range["rates"].get(category, 0)
            elif "31-90" in rate_range["term"] and 31 <= days <= 90:
                return rate_range["rates"].get(category, 0)
            elif "91-180" in rate_range["term"] and 91 <= days <= 180:
                return rate_range["rates"].get(category, 0)
            elif "181-365" in rate_range["term"] and 181 <= days <= 365:
                return rate_range["rates"].get(category, 0)
        return 0
    
    def get_insurance_cost(self, days: int) -> float:
        """Отримання вартості страхування"""
        for rate in self.rates["insuranceRates"]:
            if "1-90" in rate["term"] and days <= 90:
                return rate["cost"]
            elif "91-180" in rate["term"] and 91 <= days <= 180:
                return rate["cost"]
            elif "181-270" in rate["term"] and 181 <= days <= 270:
                return rate["cost"]
            elif "271-365" in rate["term"] and 271 <= days <= 365:
                return rate["cost"]
        return 0
    
    def calculate(self, category: str, days: int, coverage: bool = False, attorney_count: int = 0, penalty: float = 0.0):
        """Розрахунок вартості"""
        
        # Розрахунок вартості оренди
        daily_rate = self.get_daily_rate(category, days)
        rent_cost = daily_rate * days
        
        # Розрахунок страхування
        coverage_cost = self.get_insurance_cost(days) if coverage else 0
        
        # Розрахунок довіреностей
        attorney_cost = attorney_count * self.rates["attorneyTariff"]
        
        # Загальна сума
        total_cost = rent_cost + coverage_cost + attorney_cost + penalty
        
        return {
            'category': category,
            'days': days,
            'daily_rate': daily_rate,
            'rent_cost': rent_cost,
            'coverage_cost': coverage_cost,
            'attorney_cost': attorney_cost,
            'penalty_cost': penalty,
            'total_cost': total_cost
        }
    
    def show_clients(self):
        """Показати всіх клієнтів"""
        conn = sqlite3.connect('safe_calculator.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT name, ipn, phone, email FROM clients ORDER BY name')
        clients = cursor.fetchall()
        
        if clients:
            print("\n📋 СПИСОК КЛІЄНТІВ:")
            print("-" * 60)
            for i, (name, ipn, phone, email) in enumerate(clients, 1):
                print(f"{i:2}. {name}")
                print(f"    ІПН: {ipn or 'не вказано'}")
                print(f"    Тел: {phone or 'не вказано'}")
                print(f"    Email: {email or 'не вказано'}")
                print()
        else:
            print("\n📋 Клієнтів не знайдено")
        
        conn.close()
    
    def demo_calculations(self):
        """Демонстраційні розрахунки"""
        print("\n🧮 ДЕМОНСТРАЦІЙНІ РОЗРАХУНКИ:")
        print("=" * 50)
        
        test_cases = [
            {"category": "1 категорія", "days": 30, "coverage": True, "attorney": 1, "penalty": 0},
            {"category": "3 категорія", "days": 90, "coverage": False, "attorney": 2, "penalty": 150},
            {"category": "5 категорія", "days": 180, "coverage": True, "attorney": 0, "penalty": 0},
            {"category": "2 категорія", "days": 365, "coverage": True, "attorney": 3, "penalty": 500}
        ]
        
        for i, test in enumerate(test_cases, 1):
            print(f"\n{i}. Розрахунок #{i}")
            print("-" * 30)
            
            result = self.calculate(
                test["category"], 
                test["days"], 
                test["coverage"], 
                test["attorney"], 
                test["penalty"]
            )
            
            print(f"Категорія сейфу: {result['category']}")
            print(f"Термін оренди: {result['days']} днів")
            print(f"Денна ставка: {result['daily_rate']} грн/день")
            print(f"Страхування: {'Так' if test['coverage'] else 'Ні'}")
            print(f"Довіреності: {test['attorney']} шт")
            print(f"Штраф: {test['penalty']} грн")
            print()
            print(f"💰 РОЗРАХУНОК:")
            print(f"  Оренда: {result['rent_cost']:.2f} грн")
            print(f"  Страхування: {result['coverage_cost']:.2f} грн")
            print(f"  Довіреності: {result['attorney_cost']:.2f} грн")
            print(f"  Штраф: {result['penalty_cost']:.2f} грн")
            print(f"  ВСЬОГО: {result['total_cost']:.2f} грн")

def main():
    """Головна функція"""
    print("🔐 КАЛЬКУЛЯТОР ОРЕНДИ СЕЙФУ - CLI ТЕСТ")
    print("=" * 50)
    
    calc = SafeCalculatorCLI()
    
    # Показати клієнтів
    calc.show_clients()
    
    # Демонстраційні розрахунки
    calc.demo_calculations()
    
    print("\n✅ CLI тест завершено!")
    print("Для запуску GUI версії використайте: python safe_calculator.py")

if __name__ == "__main__":
    main()
