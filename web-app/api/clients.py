from http.server import BaseHTTPRequestHandler
import json

# Простий in-memory storage для демо (в продакшені використовуйте справжню БД)
clients_storage = []

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

    def do_GET(self):
        try:
            # Повернення списку клієнтів
            result = {'success': True, 'clients': clients_storage}
            self._set_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))

    def do_POST(self):
        try:
            # Додавання нового клієнта
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            import uuid
            from datetime import datetime
            
            client = {
                'id': str(uuid.uuid4()),
                'name': data.get('name', ''),
                'ipn': data.get('ipn', ''),
                'iban': data.get('iban', ''),
                'phone': data.get('phone', ''),
                'email': data.get('email', ''),
                'created_at': datetime.now().isoformat()
            }
            
            clients_storage.append(client)
            
            result = {'success': True, 'client': client}
            self._set_headers()
            self.wfile.write(json.dumps(result, ensure_ascii=False).encode('utf-8'))
            
        except Exception as e:
            self._set_headers(500)
            self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode('utf-8'))
