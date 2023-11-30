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