import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os

load_dotenv()

db_config = {
    'dbname': os.getenv('POSTGRES_DATABASE'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'host': os.getenv('POSTGRES_HOST'),
    'port': '5432',
    'sslmode': 'require' 
}
# Añadir el prefijo 'tellmedam_' a los nombres de las tablas
prefix = 'tellmedam_'
table_users = f'{prefix}users'
table_messages = f'{prefix}messages'
table_chats = f'{prefix}chats'

# Consulta SQL para crear la tabla de usuarios
sql_user_create_table = sql.SQL("""
    CREATE TABLE {} (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password VARCHAR(255) NOT NULL,
        photoUrl VARCHAR(255) DEFAULT '/placeholder.png',
        chats UUID[]
    )
""").format(sql.Identifier(table_users))

# Consulta SQL para crear la tabla de mensajes
sql_message_create_table = sql.SQL("""
    CREATE TABLE {} (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        createdAt TIMESTAMPTZ DEFAULT current_timestamp,
        updatedAt TIMESTAMPTZ DEFAULT current_timestamp,
        name VARCHAR(255),
        category VARCHAR(255),
        chatId UUID REFERENCES {}(id)
    )
""").format(sql.Identifier(table_messages), sql.Identifier(table_chats))

# Consulta SQL para crear la tabla de chats
sql_chat_create_table = sql.SQL("""
    CREATE TABLE {} (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
        createdAt TIMESTAMPTZ DEFAULT current_timestamp,
        updatedAt TIMESTAMPTZ DEFAULT current_timestamp,
        users UUID[],
        messages UUID[]
    )
""").format(sql.Identifier(table_chats))

# Conexión a PostgreSQL
try:
    connection = psycopg2.connect(**db_config)
    cursor = connection.cursor()

    # Crear la tabla de usuarios
    cursor.execute(sql_user_create_table)

    # Crear la tabla de mensajes
    cursor.execute(sql_message_create_table)

    # Crear la tabla de chats
    cursor.execute(sql_chat_create_table)

    connection.commit()

    print(f"Tablas '{table_users}', '{table_messages}' y '{table_chats}' creadas correctamente.")

except Exception as e:
    print(f"Error: {e}")

finally:
    cursor.close()
    connection.close()