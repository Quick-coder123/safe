#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт ініціалізації бази даних без GUI
"""

import sqlite3

def init_database():
    """Ініціалізація бази даних"""
    conn = sqlite3.connect('safe_calculator.db')
    cursor = conn.cursor()
    
    # Таблиця клієнтів
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            ipn TEXT,
            iban TEXT,
            phone TEXT,
            email TEXT,
            created_at TEXT
        )
    ''')
    
    # Таблиця оренди сейфів
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS rentals (
            id TEXT PRIMARY KEY,
            client_id TEXT,
            category TEXT,
            contract_type TEXT,
            coverage TEXT,
            start_date TEXT,
            end_date TEXT,
            days INTEGER,
            rent_cost REAL,
            coverage_cost REAL,
            attorney_cost REAL,
            penalty_cost REAL,
            total_cost REAL,
            created_at TEXT,
            FOREIGN KEY (client_id) REFERENCES clients (id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✅ База даних ініціалізована")

if __name__ == "__main__":
    init_database()
