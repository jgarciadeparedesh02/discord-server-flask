# app/chat_routes.py
from flask import jsonify, request
from psycopg2.extras import RealDictCursor
from config import connect
from app import app

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