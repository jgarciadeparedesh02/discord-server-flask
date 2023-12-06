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

    print('Try new_chat: ', new_chat)

    if 'user1_id' not in new_chat or 'user2_id' not in new_chat:
        return jsonify({'error': 'Campos incompletos'}), 400
    if new_chat['user1_id'] == new_chat['user2_id']:
        return jsonify({'error': 'Campos incompletos'}), 400
    
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute('SELECT * FROM tellmedam_chat WHERE idUser1 = %s AND idUser2 = %s;', (new_chat['user1_id'], new_chat['user2_id']))
        existing_chat = cursor.fetchone()
    if existing_chat:
        return jsonify({'error': 'Ya existe un chat entre estos dos usuarios'}), 400

    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO tellmedam_chat (idUser1, idUser2) VALUES (%s, %s) RETURNING *;',
                       (new_chat['user1_id'], new_chat['user2_id']))
        created_chat = cursor.fetchone()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        query = '''
            SELECT tc.id, tu1.id as user1_id, tu2.id as user2_id, tu1.username as user1_username, tu2.username as user2_username, tc.createdAt, tc.updatedAt
            FROM tellmedam_chat tc
            INNER JOIN tellmedam_user tu1 ON tc.idUser1 = tu1.id
            INNER JOIN tellmedam_user tu2 ON tc.idUser2 = tu2.id
            WHERE tu1.id = %s AND tu2.id = %s;
        '''
        cursor.execute(query, (new_chat['user1_id'], new_chat['user2_id']))
        created_chat = cursor.fetchone()

    conn.commit()
    conn.close()
    return jsonify(created_chat)