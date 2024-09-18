from flask import Flask, render_template, request, jsonify
import random
import json

app = Flask(__name__)

# Lese JSON-data fra en fil
with open('data/bmc.json', 'r') as file:
    bmc_data = json.load(file)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_bmc', methods=['GET'])
def get_bmc():
    company = random.choice(list(bmc_data.keys()))
    data = bmc_data[company]
    return jsonify({"company": company, "bmc": data})

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


@app.route('/add_bmc', methods=['POST'])
def add_bmc():
    data = request.get_json()

    new_bmc = {
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

    # Legg til den nye BMC i ditt eksisterende bmc_data
    bmc_data[data['company_name']] = new_bmc

    # Du må også lagre denne endringen til fil, slik at den vedvarer
    with open('data/bmc.json', 'w') as file:
        json.dump(bmc_data, file, indent=4)

    return jsonify({"success": True})


@app.route('/add_bmc', methods=['GET'])
def add_bmc_page():
    return render_template('add_bmc.html')


if __name__ == '__main__':
    app.run(debug=True)
