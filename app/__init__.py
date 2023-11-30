# app/__init__.py
from flask import Flask

app = Flask(__name__)

from app import user_routes
from app import login_routes
from app import messages_routes

if __name__ == '__main__':
    app.run(debug=True)
