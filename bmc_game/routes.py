from flask import Blueprint, render_template, request, jsonify, g, session, redirect, url_for
from util.db import get_bmc, get_all_company_names, upload_bmc
from functools import wraps

bmc_game_bp = Blueprint('bmc_game', __name__)

@bmc_game_bp.route('/')
def index():
    return render_template('index.html')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Sjekk om brukeren er enten logget inn som bruker eller gjest
        if 'user_id' not in session and 'guest' not in session:
            return redirect(url_for('auth.login'))  # Send til innloggingssiden hvis ikke logget inn
        return f(*args, **kwargs)
    return decorated_function


# Bruk login_required på spillruten
@bmc_game_bp.route('/start_game', methods=['GET'])
@login_required
def start_game():
    username = session.get('username', 'Guest')  # Hent brukernavnet fra session
    return render_template('index.html', username=username)  # Pass brukernavnet til template


# Rute for å hente BMC-data
@bmc_game_bp.route('/get_bmc', methods=['GET'])
def get_bmc_route():
    connection = g.db_conn
    data = get_bmc(connection)
    
    if data:
        company_name, bmc_data = list(data.items())[0]
        return jsonify({"company": company_name, "bmc": bmc_data})
    else:
        return jsonify({"error": "No data found"}), 404

# Rute for å laste opp ny BMC-data
@bmc_game_bp.route('/add_bmc', methods=['POST'])
def add_bmc():
    connection = g.db_conn
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

    upload_bmc(new_bmc, connection)
    return jsonify({"success": True})

# Rute for å vise BMC-lastesiden
@bmc_game_bp.route('/add_bmc', methods=['GET'])
def add_bmc_page():
    return render_template('add_bmc.html')

# Rute for å sjekke svaret på et gjett
@bmc_game_bp.route('/check_answer', methods=['POST'])
def check_answer():
    data = request.get_json()
    guess = data['guess']
    correct_company = data['correct_company']
    
    if guess.lower() == correct_company.lower():
        return jsonify({"result": "correct"})
    else:
        return jsonify({"result": "wrong", "correct_company": correct_company})

# Rute for å vise statistikk
@bmc_game_bp.route('/stats', methods=['GET'])
def show_stats():
    score = request.args.get('score')
    total_time = request.args.get('time')
    TPBM = request.args.get('TPBM')
    
    return render_template('stats.html', score=score, total_time=total_time, TPBM=TPBM)
