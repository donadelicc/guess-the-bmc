from flask import Flask, g, jsonify, session
from bmc_game.routes import bmc_game_bp
from auth.routes import auth_bp
from util.db import connect_to_db
from datetime import timedelta


app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.permanent_session_lifetime = timedelta(minutes=30)  # Sett sesjonsvarighet til 30 minutter

# Registrer Blueprint som kombinerer både spill- og BMC-ruter
app.register_blueprint(bmc_game_bp)
# Registrer Blueprint for autentisering
app.register_blueprint(auth_bp)

@app.before_request
def make_session_permanent():
    session.permanent = True

# Oppretter tilkoblingen og lagrer den i Flask g variabel (global objekt for hver request)
@app.before_request
def before_request():
    if 'db_conn' not in g:
        g.db_conn = connect_to_db()

@app.teardown_request
def teardown_request(exception):
    db_conn = g.pop('db_conn', None)
    if db_conn is not None:
        db_conn.close()
        
@app.route('/debug_session')
def debug_session():
    return jsonify(dict(session))

if __name__ == '__main__':
    app.run(debug=True)
