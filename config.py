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

def connect():
    return psycopg2.connect(**db_config)