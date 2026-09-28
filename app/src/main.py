import http.server
import random
import logging

# This sets up our digital notebook (the log file)
logging.basicConfig(
    filename='app_production.log',
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ProductionMockApp(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        pass # This keeps our main screen clean

    def do_GET(self):
        # The Health Room
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "UP", "database": "CONNECTED"}')
            logging.info("Health check endpoint hit - Status: 200 OK")
            
        # The Checkout Room (programmed to break 20% of the time)
        elif self.path == '/checkout':
            if random.random() < 0.20:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"error": "Internal Server Error"}')
                logging.error("CRITICAL: Payment gateway timeout - HTTP 504 Gateway Timeout from local provider.")
            else:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"status": "SUCCESS", "transaction_id": "TXN-AU-9923"}')
                logging.info("User checkout transaction processed successfully.")
        else:
            self.send_response(404)
            self.end_headers()

if __name__ == '__main__':
    server_address = ('0.0.0.0', 8080)
    httpd = http.server.HTTPServer(server_address, ProductionMockApp)
    print("=== [AU/NZ Support Portfolio App] Running on http://localhost:8080 ===")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        httpd.server_close()
