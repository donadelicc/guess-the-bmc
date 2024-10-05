from flask import Blueprint, jsonify, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from util.db import connect_to_db

auth_bp = Blueprint('auth', __name__)

# Rute for registrering av ny bruker
@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = connect_to_db()
        cursor = connection.cursor()

        # Sjekk om brukernavnet allerede eksisterer
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        
        # Hashe passordet og lagre brukeren i databasen
        password_hash = generate_password_hash(password)
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", (username, password_hash))
        connection.commit()
        cursor.close()
        connection.close()
        
        flash('User registered successfully')
        return redirect(url_for('auth.login'))

    return render_template('register.html')

# Rute for innlogging av bruker
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        connection = connect_to_db()
        cursor = connection.cursor()

        # Søk etter brukeren i databasen
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and check_password_hash(user['password_hash'], password):
            # Brukeren er autentisert
            session['user_id'] = user['id']
            session['username'] = user['username']
            return redirect(url_for('bmc_game.index'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

# Rute for gjestelogging
@auth_bp.route('/guest', methods=['POST'])
def guest_login():
    guest_username = request.json.get('username')

    if not guest_username or len(guest_username.strip()) == 0:
        return jsonify({"message": "Invalid guest username"}), 400

    # Lagre gjestens brukernavn i session
    session['guest'] = True
    session['username'] = guest_username.strip()  # Fjern mellomrom før lagring

    return jsonify({"message": "Guest logged in"}), 200


# Rute for å logge ut brukeren
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for('auth.login'))
