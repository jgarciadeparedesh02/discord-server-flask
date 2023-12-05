# app/notifications.py
from flask import jsonify, request
from psycopg2.extras import RealDictCursor
from config import connect
from app import app
import re

# Obtener los mensajes de los chats de un usuario por su ID creados en los últimos 30 segundos
@app.route('/users/<int:user_id>/notifications', methods=['GET'])
def get_user_notifications(user_id):
    conn = connect()

    # Consulta para obtener los chats del usuario por su ID con los nombres de usuario
    query = '''
        SELECT tc.id, tu1.id as user1_id, tu2.id as user2_id, tu1.username as user1_username, tu2.username as user2_username, tc.createdAt, tc.updatedAt
        FROM tellmedam_chat tc
        INNER JOIN tellmedam_user tu1 ON tc.idUser1 = tu1.id
        INNER JOIN tellmedam_user tu2 ON tc.idUser2 = tu2.id
        WHERE (tu1.id = %s OR tu2.id = %s)
        AND tc.updatedAt > NOW() - INTERVAL '30 seconds';
    '''

    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute(query, (user_id, user_id))
        user_chats = cursor.fetchall()

    conn.close()

    return jsonify(user_chats)
