from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    # Proves Phase 2 (SSM Parameter Store) is working
    db_pass = os.environ.get('DB_PASSWORD', 'Not Found')
    status = "Successfully Injected" if db_pass != 'Not Found' else "Missing"
    return f"<h1>AgileOps CI/CD Pipeline Successful!</h1><p>Zero-Trust DB Secret Status: {status}</p>"

@app.route('/health')
def health():
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
