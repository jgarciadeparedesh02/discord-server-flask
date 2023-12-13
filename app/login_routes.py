# app/login_routes.py
from flask import jsonify, request
from psycopg2.extras import RealDictCursor
from config import connect, disconnect
from app import app

@app.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()

    if 'email' not in login_data or 'password' not in login_data:
        return jsonify({'error': 'Credenciales incompletas'}), 400

    email = login_data['email']
    password = login_data['password']

    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_user WHERE email = %s AND password = %s;',
                       (email, password))
        user = cursor.fetchone()

        disconnect(conn)
        if user:
            return jsonify(user)
        else:
            return jsonify({'error': 'Credenciales incorrectas'}), 401
