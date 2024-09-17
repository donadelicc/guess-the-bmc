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
    score = request.args.get('score', 0)
    total_time = request.args.get('time', '00:00')
    return render_template('stats.html', score=score, total_time=total_time)

if __name__ == '__main__':
    app.run(debug=True)
