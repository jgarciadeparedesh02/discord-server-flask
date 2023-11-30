from flask import Flask, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os

load_dotenv()
db_config = {
    'dbname': 'verceldb',
    'user': 'default',
    'password': 'bP6OiTzwm1sn',
    'host': 'ep-white-smoke-91737562-pooler.us-east-1.postgres.vercel-storage.com',
    'port': '5432',
    'sslmode': 'require'
}

app = Flask(__name__)

# Conexión a la base de datos
def connect():
    return psycopg2.connect(**db_config)

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
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tellmedam_user (username, email, password, photoUrl) VALUES (%s, %s, %s, %s) RETURNING *;',
                       (new_user['username'], new_user['email'], new_user['password'], new_user['photoUrl']))
        created_user = cursor.fetchone()
    conn.commit()
    conn.close()
    return jsonify(created_user)

# Obtener todos los chats
@app.route('/chats', methods=['GET'])
def get_chats():
    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_chat;')
        chats = cursor.fetchall()
    conn.close()
    return jsonify(chats)

# Obtener un chat por ID
@app.route('/chats/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_chat WHERE id = %s;', (chat_id,))
        chat = cursor.fetchone()
    conn.close()
    return jsonify(chat)

# Crear un nuevo chat
@app.route('/chats', methods=['POST'])
def create_chat():
    new_chat = request.get_json()
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tellmedam_chat (idUser1, idUser2, createdAt, updatedAt) VALUES (%s, %s, %s, %s) RETURNING *;',
                       (new_chat['idUser1'], new_chat['idUser2'], new_chat.get('createdAt'), new_chat.get('updatedAt')))
        created_chat = cursor.fetchone()
    conn.commit()
    conn.close()
    return jsonify(created_chat)

# Obtener todos los mensajes
@app.route('/messages', methods=['GET'])
def get_messages():
    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_message;')
        messages = cursor.fetchall()
    conn.close()
    return jsonify(messages)

# Obtener un mensaje por ID
@app.route('/messages/<int:message_id>', methods=['GET'])
def get_message(message_id):
    conn = connect()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_message WHERE id = %s;', (message_id,))
        message = cursor.fetchone()
    conn.close()
    return jsonify(message)

# Crear un nuevo mensaje
@app.route('/messages', methods=['POST'])
def create_message():
    new_message = request.get_json()
    conn = connect()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tellmedam_message (idSender, content, createdAt, receivedAt, chatId) VALUES (%s, %s, %s, %s, %s) RETURNING *;',
                       (new_message['idSender'], new_message['content'], new_message.get('createdAt'), new_message.get('receivedAt'), new_message['chatId']))
        created_message = cursor.fetchone()
    conn.commit()
    conn.close()
    return jsonify(created_message)

if __name__ == '__main__':
    app.run(debug=True)