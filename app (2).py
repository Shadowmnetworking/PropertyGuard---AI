from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Simulated tenant and payment database
tenants = pd.read_csv('tenants.csv')
payments = pd.read_csv('payments.csv')

@app.route('/')
def dashboard():
    return render_template('dashboard.html', tenants=tenants.to_dict(orient='records'))

@app.route('/api/tenants', methods=['GET'])
def get_tenants():
    return jsonify(tenants.to_dict(orient='records'))

@app.route('/api/payments', methods=['GET'])
def get_payments():
    return jsonify(payments.to_dict(orient='records'))

@app.route('/api/payments', methods=['POST'])
def add_payment():
    data = request.json
    new_payment = {
        "tenant_id": data["tenant_id"],
        "amount": data["amount"],
        "date": datetime.now().strftime('%Y-%m-%d')
    }
    global payments
    payments = payments.append(new_payment, ignore_index=True)
    payments.to_csv('payments.csv', index=False)
    return jsonify({"message": "Payment recorded"}), 201

if __name__ == '__main__':
    app.run(debug=True)