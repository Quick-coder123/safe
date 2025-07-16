#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для додавання тестових даних до калькулятора сейфу
"""

import sqlite3
import uuid
from datetime import datetime

def create_demo_data():
    """Створення демонстраційних даних"""
    
    # Підключення до бази даних
    conn = sqlite3.connect('safe_calculator.db')
    cursor = conn.cursor()
    
    # Тестові клієнти
    demo_clients = [
        {
            'id': str(uuid.uuid4()),
            'name': 'Іванов Іван Іванович',
            'ipn': '1234567890',
            'iban': 'UA123456789012345678901234567',
            'phone': '+380501234567',
            'email': 'ivanov@example.com',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Петренко Петро Петрович',
            'ipn': '0987654321',
            'iban': 'UA987654321098765432109876543',
            'phone': '+380679876543',
            'email': 'petrenko@example.com',
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'name': 'Сидоренко Марія Олександрівна',
            'ipn': '5555555555',
            'iban': 'UA555555555555555555555555555',
            'phone': '+380631111111',
            'email': 'sidorenko@example.com',
            'created_at': datetime.now().isoformat()
        }
    ]
    
    # Додавання клієнтів
    for client in demo_clients:
        cursor.execute('''
            INSERT OR REPLACE INTO clients (id, name, ipn, iban, phone, email, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (client['id'], client['name'], client['ipn'], client['iban'], 
              client['phone'], client['email'], client['created_at']))
    
    print(f"✅ Додано {len(demo_clients)} тестових клієнтів")
    
    # Тестові розрахунки оренди
    demo_rentals = [
        {
            'id': str(uuid.uuid4()),
            'client_id': demo_clients[0]['id'],
            'category': '1 категорія',
            'contract_type': 'Новий',
            'coverage': 'Так',
            'start_date': '2024-01-15',
            'end_date': '2024-02-14',
            'days': 30,
            'rent_cost': 1170.0,  # 39 * 30
            'coverage_cost': 285.0,
            'attorney_cost': 300.0,
            'penalty_cost': 0.0,
            'total_cost': 1755.0,
            'created_at': datetime.now().isoformat()
        },
        {
            'id': str(uuid.uuid4()),
            'client_id': demo_clients[1]['id'],
            'category': '3 категорія',
            'contract_type': 'Пролонгація',
            'coverage': 'Ні',
            'start_date': '2024-02-01',
            'end_date': '2024-04-30',
            'days': 90,
            'rent_cost': 2520.0,  # 28 * 90
            'coverage_cost': 0.0,
            'attorney_cost': 600.0,  # 2 довіреності
            'penalty_cost': 150.0,
            'total_cost': 3270.0,
            'created_at': datetime.now().isoformat()
        }
    ]
    
    # Додавання розрахунків
    for rental in demo_rentals:
        cursor.execute('''
            INSERT OR REPLACE INTO rentals (id, client_id, category, contract_type, coverage,
                                          start_date, end_date, days, rent_cost, coverage_cost,
                                          attorney_cost, penalty_cost, total_cost, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (rental['id'], rental['client_id'], rental['category'], rental['contract_type'],
              rental['coverage'], rental['start_date'], rental['end_date'], rental['days'],
              rental['rent_cost'], rental['coverage_cost'], rental['attorney_cost'],
              rental['penalty_cost'], rental['total_cost'], rental['created_at']))
    
    print(f"✅ Додано {len(demo_rentals)} тестових розрахунків")
    
    conn.commit()
    conn.close()
    
    print("\n🎉 Демонстраційні дані успішно створено!")
    print("Тепер можете запустити калькулятор: python safe_calculator.py")

if __name__ == "__main__":
    print("🔧 Створення демонстраційних даних...")
    create_demo_data()
