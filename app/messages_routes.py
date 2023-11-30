# app/chat_routes.py
from flask import jsonify, request
from psycopg2.extras import RealDictCursor
from config import connect
from app import app

@app.route('/chats/<int:chat_id>/messages', methods=['GET'])
def get_chat_messages(chat_id):
    conn = connect()

    # Consulta para obtener los mensajes de un chat por su ID
    query = '''
        SELECT tm.id, tm.idSender, tm.content, tm.createdAt, tm.receivedAt
        FROM tellmedam_message tm
        WHERE tm.chatId = %s;
    '''

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (chat_id,))
        chat_messages = cursor.fetchall()

    conn.close()

    return jsonify(chat_messages)

@app.route('/chats/<int:chat_id>/messages', methods=['POST'])
def add_message(chat_id):
    data = request.get_json()

    id_sender = data.get('idSender')
    content = data.get('content')

    conn = connect()
    with conn.cursor() as cursor:
        # Consulta SQL para insertar un nuevo mensaje
        sql_insert_message = """
            INSERT INTO tellmedam_message (idSender, content, chatId)
            VALUES (%s, %s, %s) RETURNING *;
        """
        cursor.execute(sql_insert_message, (id_sender, content, chat_id))
        created_message = cursor.fetchone()

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        print(type(created_message))
        cursor.execute('SELECT id, idSender, content, chatId FROM tellmedam_message WHERE chatId = %s and idSender = %s and content = %s;', (chat_id, id_sender, content))
        created_message = cursor.fetchone()
    conn.commit()
    conn.close()

    return jsonify(created_message)