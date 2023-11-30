# app/user_routes.py
from flask import jsonify, request
from psycopg2.extras import RealDictCursor
from config import connect
from app import app

# Obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT id, username, email, photourl FROM tellmedam_user;')
        users = cursor.fetchall()
    conn.close()
    return jsonify(users)

# Obtener un usuario por ID
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT id, username, email, photourl FROM tellmedam_user WHERE id = %s;', (user_id,))
        user = cursor.fetchone()
    conn.close()
    return jsonify(user)

# Crear un nuevo usuario
@app.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    conn = connect()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_user WHERE username = %s OR email = %s;', (new_user['username'], new_user['email']))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Ya existe un usuario con el mismo username o email'}), 400

    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tellmedam_user (username, email, password) VALUES (%s, %s, %s) RETURNING *;',
                       (new_user['username'], new_user['email'], new_user['password']))
        created_user = cursor.fetchone()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT id, username, email, photourl FROM tellmedam_user WHERE username = %s OR email = %s;', (new_user['username'], new_user['email']))
        created_user = cursor.fetchone()

    conn.commit()
    conn.close()

    return jsonify(created_user)

# Obtener los chats de un usuario
@app.route('/users/<int:user_id>/chats', methods=['GET'])
def get_user_chats(user_id):
    conn = connect()

    # Consulta para obtener los chats del usuario por su ID con los nombres de usuario
    query = '''
        SELECT tc.id, tu1.id as user1_id, tu2.id as user2_id, tu1.username as user1_username, tu2.username as user2_username, tc.createdAt, tc.updatedAt
        FROM tellmedam_chat tc
        INNER JOIN tellmedam_user tu1 ON tc.idUser1 = tu1.id
        INNER JOIN tellmedam_user tu2 ON tc.idUser2 = tu2.id
        WHERE tu1.id = %s OR tu2.id = %s;
    '''

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (user_id, user_id))
        user_chats = cursor.fetchall()

    conn.close()

    return jsonify(user_chats)