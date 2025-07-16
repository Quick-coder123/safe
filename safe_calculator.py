#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Калькулятор оренди індивідуального сейфу
Спрощена Python версія з GUI на tkinter
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional
import sqlite3
import uuid

@dataclass
class Client:
    """Клас для зберігання даних клієнта"""
    id: str
    name: str
    ipn: str = ""
    iban: str = ""
    phone: str = ""
    email: str = ""
    created_at: str = ""

@dataclass
class SafeRental:
    """Клас для зберігання даних оренди сейфу"""
    id: str
    client_id: str
    category: str
    contract_type: str
    coverage: str
    start_date: str
    end_date: str
    days: int
    rent_cost: float
    coverage_cost: float
    attorney_cost: float
    penalty_cost: float
    total_cost: float
    created_at: str

class SafeCalculatorDB:
    """Клас для роботи з локальною SQLite базою даних"""
    
    def __init__(self, db_path: str = "safe_calculator.db"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Ініціалізація бази даних"""
        conn = sqlite3.connect(self.db_path)
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
    
    def add_client(self, client: Client) -> bool:
        """Додати клієнта"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO clients (id, name, ipn, iban, phone, email, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (client.id, client.name, client.ipn, client.iban, 
                  client.phone, client.email, client.created_at))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Помилка додавання клієнта: {e}")
            return False
    
    def get_clients(self) -> List[Client]:
        """Отримати список всіх клієнтів"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM clients ORDER BY name')
        rows = cursor.fetchall()
        
        clients = []
        for row in rows:
            clients.append(Client(
                id=row[0], name=row[1], ipn=row[2], iban=row[3],
                phone=row[4], email=row[5], created_at=row[6]
            ))
        
        conn.close()
        return clients
    
    def add_rental(self, rental: SafeRental) -> bool:
        """Додати запис оренди"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO rentals (id, client_id, category, contract_type, coverage,
                                   start_date, end_date, days, rent_cost, coverage_cost,
                                   attorney_cost, penalty_cost, total_cost, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (rental.id, rental.client_id, rental.category, rental.contract_type,
                  rental.coverage, rental.start_date, rental.end_date, rental.days,
                  rental.rent_cost, rental.coverage_cost, rental.attorney_cost,
                  rental.penalty_cost, rental.total_cost, rental.created_at))
            
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print(f"Помилка додавання оренди: {e}")
            return False

class SafeCalculatorApp:
    """Основний клас додатку калькулятора сейфу"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор оренди індивідуального сейфу")
        self.root.geometry("1000x700")
        self.root.configure(bg='#f0f0f0')
        
        # База даних
        self.db = SafeCalculatorDB()
        
        # Тарифи (спрощена структура)
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
            "attorneyTariff": 300,
            "packetTariff": 30,
            "depositAmount": 3000
        }
        
        self.create_widgets()
        self.load_clients()
    
    def create_widgets(self):
        """Створення інтерфейсу"""
        # Створення notebook для вкладок
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Вкладка калькулятора
        self.calculator_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calculator_frame, text="Калькулятор")
        
        # Вкладка клієнтів
        self.clients_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.clients_frame, text="Клієнти")
        
        self.create_calculator_tab()
        self.create_clients_tab()
    
    def create_calculator_tab(self):
        """Створення вкладки калькулятора"""
        # Основний фрейм з прокруткою
        canvas = tk.Canvas(self.calculator_frame, bg='#f0f0f0')
        scrollbar = ttk.Scrollbar(self.calculator_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Заголовок
        title_label = tk.Label(scrollable_frame, text="Калькулятор оренди індивідуального сейфу", 
                              font=('Arial', 16, 'bold'), bg='#f0f0f0')
        title_label.pack(pady=10)
        
        # Фрейм для форми
        form_frame = ttk.LabelFrame(scrollable_frame, text="Параметри оренди", padding="20")
        form_frame.pack(fill='x', padx=20, pady=10)
        
        # Категорія сейфу
        ttk.Label(form_frame, text="Категорія сейфу:").grid(row=0, column=0, sticky='w', pady=5)
        self.category_var = tk.StringVar(value="1 категорія")
        self.category_combo = ttk.Combobox(form_frame, textvariable=self.category_var, 
                                          values=["1 категорія", "2 категорія", "3 категорія", "4 категорія", "5 категорія"],
                                          state="readonly", width=20)
        self.category_combo.grid(row=0, column=1, sticky='w', padx=(10,0), pady=5)
        
        # Тип договору
        ttk.Label(form_frame, text="Тип договору:").grid(row=1, column=0, sticky='w', pady=5)
        self.contract_var = tk.StringVar(value="Новий")
        self.contract_combo = ttk.Combobox(form_frame, textvariable=self.contract_var,
                                          values=["Новий", "Пролонгація"], state="readonly", width=20)
        self.contract_combo.grid(row=1, column=1, sticky='w', padx=(10,0), pady=5)
        
        # Страхування
        ttk.Label(form_frame, text="Страхування:").grid(row=2, column=0, sticky='w', pady=5)
        self.coverage_var = tk.StringVar(value="Ні")
        self.coverage_combo = ttk.Combobox(form_frame, textvariable=self.coverage_var,
                                          values=["Так", "Ні"], state="readonly", width=20)
        self.coverage_combo.grid(row=2, column=1, sticky='w', padx=(10,0), pady=5)
        
        # Кількість днів
        ttk.Label(form_frame, text="Кількість днів:").grid(row=3, column=0, sticky='w', pady=5)
        self.days_var = tk.StringVar(value="30")
        self.days_entry = ttk.Entry(form_frame, textvariable=self.days_var, width=20)
        self.days_entry.grid(row=3, column=1, sticky='w', padx=(10,0), pady=5)
        self.days_entry.bind('<KeyRelease>', self.on_days_change)
        
        # Дата початку
        ttk.Label(form_frame, text="Дата початку:").grid(row=4, column=0, sticky='w', pady=5)
        self.start_date_var = tk.StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        self.start_date_entry = ttk.Entry(form_frame, textvariable=self.start_date_var, width=20)
        self.start_date_entry.grid(row=4, column=1, sticky='w', padx=(10,0), pady=5)
        self.start_date_entry.bind('<KeyRelease>', self.on_date_change)
        
        # Дата закінчення (автоматично розраховується)
        ttk.Label(form_frame, text="Дата закінчення:").grid(row=5, column=0, sticky='w', pady=5)
        self.end_date_var = tk.StringVar()
        self.end_date_label = ttk.Label(form_frame, textvariable=self.end_date_var, font=('Arial', 10, 'bold'))
        self.end_date_label.grid(row=5, column=1, sticky='w', padx=(10,0), pady=5)
        
        # Кількість довіреностей
        ttk.Label(form_frame, text="Кількість довіреностей:").grid(row=6, column=0, sticky='w', pady=5)
        self.attorney_var = tk.StringVar(value="0")
        self.attorney_spinbox = ttk.Spinbox(form_frame, from_=0, to=10, textvariable=self.attorney_var, width=20)
        self.attorney_spinbox.grid(row=6, column=1, sticky='w', padx=(10,0), pady=5)
        
        # Сума штрафу
        ttk.Label(form_frame, text="Сума штрафу (грн):").grid(row=7, column=0, sticky='w', pady=5)
        self.penalty_var = tk.StringVar(value="0")
        self.penalty_entry = ttk.Entry(form_frame, textvariable=self.penalty_var, width=20)
        self.penalty_entry.grid(row=7, column=1, sticky='w', padx=(10,0), pady=5)
        
        # Кнопка розрахунку
        calc_button = ttk.Button(form_frame, text="Розрахувати", command=self.calculate)
        calc_button.grid(row=8, column=0, columnspan=2, pady=20)
        
        # Фрейм результатів
        result_frame = ttk.LabelFrame(scrollable_frame, text="Результати розрахунку", padding="20")
        result_frame.pack(fill='x', padx=20, pady=10)
        
        # Результати
        ttk.Label(result_frame, text="Вартість оренди:").grid(row=0, column=0, sticky='w', pady=5)
        self.rent_cost_var = tk.StringVar(value="0.00 грн")
        ttk.Label(result_frame, textvariable=self.rent_cost_var, font=('Arial', 10, 'bold')).grid(row=0, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Label(result_frame, text="Вартість страхування:").grid(row=1, column=0, sticky='w', pady=5)
        self.coverage_cost_var = tk.StringVar(value="0.00 грн")
        ttk.Label(result_frame, textvariable=self.coverage_cost_var, font=('Arial', 10, 'bold')).grid(row=1, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Label(result_frame, text="Вартість довіреностей:").grid(row=2, column=0, sticky='w', pady=5)
        self.attorney_cost_var = tk.StringVar(value="0.00 грн")
        ttk.Label(result_frame, textvariable=self.attorney_cost_var, font=('Arial', 10, 'bold')).grid(row=2, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Label(result_frame, text="Сума штрафу:").grid(row=3, column=0, sticky='w', pady=5)
        self.penalty_cost_var = tk.StringVar(value="0.00 грн")
        ttk.Label(result_frame, textvariable=self.penalty_cost_var, font=('Arial', 10, 'bold')).grid(row=3, column=1, sticky='w', padx=(10,0), pady=5)
        
        # Загальна сума
        ttk.Label(result_frame, text="ЗАГАЛЬНА СУМА:", font=('Arial', 12, 'bold')).grid(row=4, column=0, sticky='w', pady=10)
        self.total_cost_var = tk.StringVar(value="0.00 грн")
        ttk.Label(result_frame, textvariable=self.total_cost_var, font=('Arial', 14, 'bold'), foreground='red').grid(row=4, column=1, sticky='w', padx=(10,0), pady=10)
        
        # Кнопки дій
        action_frame = ttk.Frame(scrollable_frame)
        action_frame.pack(fill='x', padx=20, pady=10)
        
        ttk.Button(action_frame, text="Зберегти розрахунок", command=self.save_calculation).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Генерувати звіт", command=self.generate_report).pack(side='left', padx=5)
        ttk.Button(action_frame, text="Очистити форму", command=self.clear_form).pack(side='left', padx=5)
        
        # Налаштування canvas
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Початковий розрахунок
        self.calculate()
    
    def create_clients_tab(self):
        """Створення вкладки клієнтів"""
        # Фрейм для додавання клієнта
        add_frame = ttk.LabelFrame(self.clients_frame, text="Додати нового клієнта", padding="20")
        add_frame.pack(fill='x', padx=20, pady=10)
        
        # Поля для клієнта
        ttk.Label(add_frame, text="ПІБ *:").grid(row=0, column=0, sticky='w', pady=5)
        self.client_name_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.client_name_var, width=30).grid(row=0, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Label(add_frame, text="ІПН:").grid(row=1, column=0, sticky='w', pady=5)
        self.client_ipn_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.client_ipn_var, width=30).grid(row=1, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Label(add_frame, text="IBAN:").grid(row=2, column=0, sticky='w', pady=5)
        self.client_iban_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.client_iban_var, width=30).grid(row=2, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Label(add_frame, text="Телефон:").grid(row=3, column=0, sticky='w', pady=5)
        self.client_phone_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.client_phone_var, width=30).grid(row=3, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Label(add_frame, text="Email:").grid(row=4, column=0, sticky='w', pady=5)
        self.client_email_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.client_email_var, width=30).grid(row=4, column=1, sticky='w', padx=(10,0), pady=5)
        
        ttk.Button(add_frame, text="Додати клієнта", command=self.add_client).grid(row=5, column=0, columnspan=2, pady=20)
        
        # Список клієнтів
        list_frame = ttk.LabelFrame(self.clients_frame, text="Список клієнтів", padding="20")
        list_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview для відображення клієнтів
        columns = ('ПІБ', 'ІПН', 'IBAN', 'Телефон', 'Email')
        self.clients_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        for col in columns:
            self.clients_tree.heading(col, text=col)
            self.clients_tree.column(col, width=150)
        
        # Scrollbar для списку клієнтів
        clients_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.clients_tree.yview)
        self.clients_tree.configure(yscrollcommand=clients_scrollbar.set)
        
        self.clients_tree.pack(side="left", fill="both", expand=True)
        clients_scrollbar.pack(side="right", fill="y")
    
    def on_days_change(self, event=None):
        """Обробник зміни кількості днів"""
        self.calculate_end_date()
        self.calculate()
    
    def on_date_change(self, event=None):
        """Обробник зміни дати початку"""
        self.calculate_end_date()
        self.calculate()
    
    def calculate_end_date(self):
        """Розрахунок дати закінчення"""
        try:
            start_date = datetime.strptime(self.start_date_var.get(), "%Y-%m-%d")
            days = int(self.days_var.get())
            end_date = start_date + timedelta(days=days-1)
            self.end_date_var.set(end_date.strftime("%Y-%m-%d"))
        except:
            self.end_date_var.set("Невірний формат")
    
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
    
    def calculate(self):
        """Основний розрахунок"""
        try:
            # Отримання значень
            category = self.category_var.get()
            days = int(self.days_var.get())
            coverage = self.coverage_var.get() == "Так"
            attorney_count = int(self.attorney_var.get())
            penalty = float(self.penalty_var.get())
            
            # Розрахунок вартості оренди
            daily_rate = self.get_daily_rate(category, days)
            rent_cost = daily_rate * days
            
            # Розрахунок страхування
            coverage_cost = self.get_insurance_cost(days) if coverage else 0
            
            # Розрахунок довіреностей
            attorney_cost = attorney_count * self.rates["attorneyTariff"]
            
            # Загальна сума
            total_cost = rent_cost + coverage_cost + attorney_cost + penalty
            
            # Оновлення інтерфейсу
            self.rent_cost_var.set(f"{rent_cost:.2f} грн")
            self.coverage_cost_var.set(f"{coverage_cost:.2f} грн")
            self.attorney_cost_var.set(f"{attorney_cost:.2f} грн")
            self.penalty_cost_var.set(f"{penalty:.2f} грн")
            self.total_cost_var.set(f"{total_cost:.2f} грн")
            
            # Розрахунок дати закінчення
            self.calculate_end_date()
            
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка розрахунку: {e}")
    
    def add_client(self):
        """Додавання нового клієнта"""
        name = self.client_name_var.get().strip()
        if not name:
            messagebox.showerror("Помилка", "ПІБ клієнта є обов'язковим полем!")
            return
        
        client = Client(
            id=str(uuid.uuid4()),
            name=name,
            ipn=self.client_ipn_var.get().strip(),
            iban=self.client_iban_var.get().strip(),
            phone=self.client_phone_var.get().strip(),
            email=self.client_email_var.get().strip(),
            created_at=datetime.now().isoformat()
        )
        
        if self.db.add_client(client):
            messagebox.showinfo("Успіх", "Клієнта успішно додано!")
            self.clear_client_form()
            self.load_clients()
        else:
            messagebox.showerror("Помилка", "Не вдалося додати клієнта!")
    
    def clear_client_form(self):
        """Очищення форми клієнта"""
        self.client_name_var.set("")
        self.client_ipn_var.set("")
        self.client_iban_var.set("")
        self.client_phone_var.set("")
        self.client_email_var.set("")
    
    def load_clients(self):
        """Завантаження списку клієнтів"""
        # Очищення поточного списку
        for item in self.clients_tree.get_children():
            self.clients_tree.delete(item)
        
        # Завантаження клієнтів з бази
        clients = self.db.get_clients()
        for client in clients:
            self.clients_tree.insert('', 'end', values=(
                client.name, client.ipn, client.iban, 
                client.phone, client.email
            ))
    
    def save_calculation(self):
        """Збереження розрахунку"""
        try:
            # Вибір клієнта (спрощено - можна розширити)
            clients = self.db.get_clients()
            if not clients:
                messagebox.showwarning("Увага", "Спочатку додайте клієнта у вкладці 'Клієнти'!")
                return
            
            # Простий вибір першого клієнта (можна розширити)
            client = clients[0]
            
            rental = SafeRental(
                id=str(uuid.uuid4()),
                client_id=client.id,
                category=self.category_var.get(),
                contract_type=self.contract_var.get(),
                coverage=self.coverage_var.get(),
                start_date=self.start_date_var.get(),
                end_date=self.end_date_var.get(),
                days=int(self.days_var.get()),
                rent_cost=float(self.rent_cost_var.get().replace(' грн', '')),
                coverage_cost=float(self.coverage_cost_var.get().replace(' грн', '')),
                attorney_cost=float(self.attorney_cost_var.get().replace(' грн', '')),
                penalty_cost=float(self.penalty_cost_var.get().replace(' грн', '')),
                total_cost=float(self.total_cost_var.get().replace(' грн', '')),
                created_at=datetime.now().isoformat()
            )
            
            if self.db.add_rental(rental):
                messagebox.showinfo("Успіх", "Розрахунок збережено!")
            else:
                messagebox.showerror("Помилка", "Не вдалося зберегти розрахунок!")
                
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка збереження: {e}")
    
    def generate_report(self):
        """Генерація звіту"""
        try:
            report_text = f"""
КАЛЬКУЛЯТОР ОРЕНДИ ІНДИВІДУАЛЬНОГО СЕЙФУ
========================================

Дата розрахунку: {datetime.now().strftime("%Y-%m-%d %H:%M")}

ПАРАМЕТРИ ОРЕНДИ:
Категорія сейфу: {self.category_var.get()}
Тип договору: {self.contract_var.get()}
Страхування: {self.coverage_var.get()}
Період оренди: {self.days_var.get()} днів
Дата початку: {self.start_date_var.get()}
Дата закінчення: {self.end_date_var.get()}
Кількість довіреностей: {self.attorney_var.get()}
Сума штрафу: {self.penalty_var.get()} грн

РОЗРАХУНОК ВАРТОСТІ:
Вартість оренди: {self.rent_cost_var.get()}
Вартість страхування: {self.coverage_cost_var.get()}
Вартість довіреностей: {self.attorney_cost_var.get()}
Сума штрафу: {self.penalty_cost_var.get()}

ЗАГАЛЬНА СУМА: {self.total_cost_var.get()}
"""
            
            # Збереження в файл
            file_path = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Зберегти звіт"
            )
            
            if file_path:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(report_text)
                messagebox.showinfo("Успіх", f"Звіт збережено: {file_path}")
                
        except Exception as e:
            messagebox.showerror("Помилка", f"Помилка генерації звіту: {e}")
    
    def clear_form(self):
        """Очищення форми"""
        self.category_var.set("1 категорія")
        self.contract_var.set("Новий")
        self.coverage_var.set("Ні")
        self.days_var.set("30")
        self.start_date_var.set(datetime.now().strftime("%Y-%m-%d"))
        self.attorney_var.set("0")
        self.penalty_var.set("0")
        self.calculate()
    
    def run(self):
        """Запуск додатку"""
        self.root.mainloop()

if __name__ == "__main__":
    app = SafeCalculatorApp()
    app.run()
