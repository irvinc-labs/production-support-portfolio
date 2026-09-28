import http.server
import random
import logging
import os

# Create a secure path inside the restricted user's home folder
log_directory = "/home/appuser"
if not os.path.exists(log_directory):
    # Fallback to local path if running outside Docker on your laptop
    log_file_path = "app_production.log"
else:
    log_file_path = os.path.join(log_directory, "app_production.log")

# Setup enterprise-style logging format using the patched safe path
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class ProductionMockApp(http.server.BaseHTTPRequestHandler):
    
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "UP", "database": "CONNECTED"}')
            logging.info("Health check endpoint hit - Status: 200 OK")
            
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
    # Dynamic port binding so Render can inject its own port configuration smoothly
    port = int(os.environ.get("PORT", 8080))
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, ProductionMockApp)
    print(f"=== [AU/NZ Support Portfolio App] Running on port {port} ===")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
        httpd.server_close()
