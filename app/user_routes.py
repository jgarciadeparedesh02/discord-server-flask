# app/user_routes.py
from flask import jsonify, request
from psycopg2.extras import RealDictCursor
from config import connect
from app import app
import re

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

    if 'username' not in new_user or 'email' not in new_user or 'password' not in new_user:
        return jsonify({'error': 'Campos incompletos'}), 400

    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', new_user['email']):
        return jsonify({'error': 'Formato de correo electrónico inválido'}), 400

    if len(new_user['password']) < 8:
        return jsonify({'error': 'La contraseña debe tener al menos 8 caracteres'}), 400

    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', new_user['password']):
        return jsonify({'error': 'La contraseña debe contener al menos un caracter especial'}), 400

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_user WHERE username = %s OR email = %s;', (new_user['username'], new_user['email']))
        existing_user = cursor.fetchone()

        if existing_user:
            return jsonify({'error': 'Ya existe un usuario con el mismo username o email'}), 400

    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tellmedam_user (username, email, password, photourl) VALUES (%s, %s, %s, %s) RETURNING *;',
                       (new_user['username'], new_user['email'], new_user['password'], "https://discord-server-flask.vercel.app/images/default-image.jpg"))
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

# Actualizar un usuario
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.get_json()
    conn = connect()

    # Check id exists
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_user WHERE id = %s;', (user_id,))
        user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404


    if 'username' not in updated_user or 'email' not in updated_user or 'password' not in updated_user:
        return jsonify({'error': 'Campos incompletos'}), 400
    
    if 'photourl' not in updated_user:
        updated_user['photourl'] = "https://discord-server-flask.vercel.app/images/default-image.jpg"

    with conn.cursor() as cursor:
        cursor.execute('UPDATE tellmedam_user SET username = %s, email = %s, password = %s, photourl = %s WHERE id = %s RETURNING *;',
                       (updated_user['username'], updated_user['email'], updated_user['password'], updated_user['photourl'], user_id))

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT id, username, email, photourl FROM tellmedam_user WHERE username = %s OR email = %s;', (updated_user['username'], updated_user['email']))
        updated_user = cursor.fetchone()

    conn.commit()
    conn.close()

    return jsonify(updated_user)

# Eliminar un usuario
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = connect()

    # Check id exists
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT id, username, email, photourl FROM tellmedam_user WHERE id = %s;', (user_id,))
        user = cursor.fetchone()
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    # Delete all messages from chats where idUser1 or idUser2 is user_id
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM tellmedam_message WHERE chatId IN (SELECT id FROM tellmedam_chat WHERE idUser1 = %s OR idUser2 = %s);', (user_id, user_id))

    conn.commit()

    # Delete all messages from user
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM tellmedam_message WHERE idSender = %s;', (user_id,))

    conn.commit()

    # Delete all chats from user
    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM tellmedam_chat WHERE idUser1 = %s OR idUser2 = %s;', (user_id, user_id))

    conn.commit()

    with conn.cursor() as cursor:
        cursor.execute('DELETE FROM tellmedam_user WHERE id = %s RETURNING *;', (user_id,))

    conn.commit()
    conn.close()

    return jsonify(user)