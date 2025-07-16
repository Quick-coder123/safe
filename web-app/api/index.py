from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import json
import os
from datetime import datetime, timedelta
import uuid

app = Flask(__name__, static_folder='public', template_folder='public')
CORS(app)

# Тарифи (точно як в оригіналі)
RATES = {
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

# Файли для зберігання даних (замість БД для простоти на Vercel)
CLIENTS_FILE = '/tmp/clients.json'
RENTALS_FILE = '/tmp/rentals.json'

def load_data(filename, default=[]):
    """Завантаження даних з файлу"""
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return default
    return default

def save_data(filename, data):
    """Збереження даних у файл"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except:
        return False

def get_daily_rate(category, days):
    """Отримання денної ставки"""
    for rate_range in RATES["dailyRates"]:
        if "1-30" in rate_range["term"] and days <= 30:
            return rate_range["rates"].get(category, 0)
        elif "31-90" in rate_range["term"] and 31 <= days <= 90:
            return rate_range["rates"].get(category, 0)
        elif "91-180" in rate_range["term"] and 91 <= days <= 180:
            return rate_range["rates"].get(category, 0)
        elif "181-365" in rate_range["term"] and 181 <= days <= 365:
            return rate_range["rates"].get(category, 0)
    return 0

def get_insurance_cost(days):
    """Отримання вартості страхування"""
    for rate in RATES["insuranceRates"]:
        if "1-90" in rate["term"] and days <= 90:
            return rate["cost"]
        elif "91-180" in rate["term"] and 91 <= days <= 180:
            return rate["cost"]
        elif "181-270" in rate["term"] and 181 <= days <= 270:
            return rate["cost"]
        elif "271-365" in rate["term"] and 271 <= days <= 365:
            return rate["cost"]
    return 0

@app.route('/')
def index():
    """Головна сторінка"""
    return render_template('index.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    """API для розрахунку вартості"""
    try:
        data = request.get_json()
        
        category = data.get('category', '1 категорія')
        days = int(data.get('days', 30))
        coverage = data.get('coverage', False)
        attorney_count = int(data.get('attorney_count', 0))
        penalty = float(data.get('penalty', 0))
        start_date = data.get('start_date', datetime.now().strftime('%Y-%m-%d'))
        
        # Розрахунки
        daily_rate = get_daily_rate(category, days)
        rent_cost = daily_rate * days
        coverage_cost = get_insurance_cost(days) if coverage else 0
        attorney_cost = attorney_count * RATES["attorneyTariff"]
        total_cost = rent_cost + coverage_cost + attorney_cost + penalty
        
        # Розрахунок дати закінчення
        start_dt = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = (start_dt + timedelta(days=days-1)).strftime('%Y-%m-%d')
        
        return jsonify({
            'success': True,
            'result': {
                'category': category,
                'days': days,
                'start_date': start_date,
                'end_date': end_date,
                'daily_rate': daily_rate,
                'rent_cost': rent_cost,
                'coverage_cost': coverage_cost,
                'attorney_cost': attorney_cost,
                'penalty_cost': penalty,
                'total_cost': total_cost
            }
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/clients', methods=['GET'])
def get_clients():
    """Отримати список клієнтів"""
    clients = load_data(CLIENTS_FILE, [])
    return jsonify({'success': True, 'clients': clients})

@app.route('/api/clients', methods=['POST'])
def add_client():
    """Додати нового клієнта"""
    try:
        data = request.get_json()
        
        client = {
            'id': str(uuid.uuid4()),
            'name': data.get('name', ''),
            'ipn': data.get('ipn', ''),
            'iban': data.get('iban', ''),
            'phone': data.get('phone', ''),
            'email': data.get('email', ''),
            'created_at': datetime.now().isoformat()
        }
        
        clients = load_data(CLIENTS_FILE, [])
        clients.append(client)
        
        if save_data(CLIENTS_FILE, clients):
            return jsonify({'success': True, 'client': client})
        else:
            return jsonify({'success': False, 'error': 'Не вдалося зберегти клієнта'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/rentals', methods=['POST'])
def save_rental():
    """Зберегти розрахунок оренди"""
    try:
        data = request.get_json()
        
        rental = {
            'id': str(uuid.uuid4()),
            'client_id': data.get('client_id', ''),
            'category': data.get('category', ''),
            'contract_type': data.get('contract_type', ''),
            'coverage': data.get('coverage', False),
            'start_date': data.get('start_date', ''),
            'end_date': data.get('end_date', ''),
            'days': data.get('days', 0),
            'rent_cost': data.get('rent_cost', 0),
            'coverage_cost': data.get('coverage_cost', 0),
            'attorney_cost': data.get('attorney_cost', 0),
            'penalty_cost': data.get('penalty_cost', 0),
            'total_cost': data.get('total_cost', 0),
            'created_at': datetime.now().isoformat()
        }
        
        rentals = load_data(RENTALS_FILE, [])
        rentals.append(rental)
        
        if save_data(RENTALS_FILE, rentals):
            return jsonify({'success': True, 'rental': rental})
        else:
            return jsonify({'success': False, 'error': 'Не вдалося зберегти розрахунок'}), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 400

@app.route('/api/rates', methods=['GET'])
def get_rates():
    """Отримати тарифи"""
    return jsonify({'success': True, 'rates': RATES})

if __name__ == '__main__':
    app.run(debug=True)
