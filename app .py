from flask import Flask, request, jsonify, render_template
import pandas as pd
from datetime import datetime

app = Flask(__name__)

# Load data
tenants = pd.read_csv('tenants.csv')
payments = pd.read_csv('payments.csv')

@app.route('/')
def home():
    return render_template('login.html')

@app.route('/login', methods=['GET'])
def login():
    user_id = request.args.get('user_id')
    role = request.args.get('role')

    if role == 'landlord':
        return render_template('landlord.html',
                               tenants=tenants.to_dict(orient='records'),
                               payments=payments.to_dict(orient='records'))
    elif role == 'tenant':
        try:
            tenant_id = int(user_id)
            tenant_data = tenants[tenants['tenant_id'] == tenant_id].iloc[0]
            tenant_payments = payments[payments['tenant_id'] == tenant_id].to_dict(orient='records')
            return render_template('tenant.html',
                                   tenant=tenant_data,
                                   payments=tenant_payments)
        except:
            return "Tenant not found or invalid ID", 404
    else:
        return "Invalid role", 400

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
