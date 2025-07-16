from http.server import BaseHTTPRequestHandler
import json
import urllib.parse
from datetime import datetime, timedelta

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

class handler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        try:
            # Парсинг URL для визначення endpoint
            path = self.path
            
            if path == '/api/calculate':
                # Читання тіла запиту
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode('utf-8'))
                
                # Обробка розрахунку
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
                
                result = {
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
                }
                
                self._set_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
                
            else:
                # Невідомий endpoint
                self._set_headers(404)
                self.wfile.write(json.dumps({'success': False, 'error': 'Endpoint not found'}).encode('utf-8'))
                
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))

    def do_GET(self):
        try:
            if self.path == '/api/rates':
                # Повернення тарифів
                result = {'success': True, 'rates': RATES}
                self._set_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            else:
                # Невідомий endpoint
                self._set_headers(404)
                self.wfile.write(json.dumps({'success': False, 'error': 'Endpoint not found'}).encode('utf-8'))
                
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
