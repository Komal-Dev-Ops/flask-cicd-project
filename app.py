from flask import Flask, render_template, jsonify
import os

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "message": "Flask app is running!"})

@app.route('/api/info')
def app_info():
    return jsonify({
        "app_name": "Flask CI/CD Demo",
        "version": "1.0.0",
        "environment": os.getenv('FLASK_ENV', 'production')
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.getenv('FLASK_ENV') == 'development')
