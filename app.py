from flask import Flask, render_template, request, jsonify
import random
import json

from util.db import upload_bmc, get_bmc, get_all_company_names


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# Henter BMC-data fra PostgreSQL
@app.route('/get_bmc', methods=['GET'])
def get_bmc_route():
    # Hent alle selskapsnavn fra PostgreSQL
    company_names = get_all_company_names()

    if not company_names:
        return jsonify({"error": "No companies found in the database"}), 404

    # Velg et tilfeldig selskap
    company = random.choice(company_names)
    
    # Hent BMC-data for det valgte selskapet
    data = get_bmc(company)
    if data:
        return jsonify({"company": company, "bmc": data[company]})
    else:
        return jsonify({"error": f"No data found for {company}"}), 404

@app.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    guess = data['guess']
    correct_company = data['correct_company']
    if guess.lower() == correct_company.lower():
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong", "correct_company": correct_company})

@app.route('/stats', methods=['GET'])
def show_stats():
    score = request.args.get('score')
    total_time = request.args.get('time')
    TPBM = request.args.get('TPBM')
    
    return render_template('stats.html', score=score, total_time=total_time, TPBM=TPBM)


# Laster opp ny BMC-data til PostgreSQL
@app.route('/add_bmc', methods=['POST'])
def add_bmc():
    data = request.get_json()

    new_bmc = {
        "company_name": data['company_name'],
        "key_partners": data['key_partners'],
        "key_activities": data['key_activities'],
        "key_resources": data['key_resources'],
        "value_proposition": data['value_proposition'],
        "customer_relationships": data['customer_relationships'],
        "channels": data['channels'],
        "customer_segments": data['customer_segments'],
        "cost_structure": data['cost_structure'],
        "revenue_streams": data['revenue_streams']
    }

    # Bruk upload_bmc-funksjonen fra postgres.py for å lagre data i PostgreSQL
    upload_bmc(new_bmc)

    return jsonify({"success": True})


# Returnerer skjema for å legge til BMC-data
@app.route('/add_bmc', methods=['GET'])
def add_bmc_page():
    return render_template('add_bmc.html')

if __name__ == '__main__':
    app.run(debug=True)
