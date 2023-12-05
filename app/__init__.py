# app/__init__.py
import os
from flask import Flask, abort, send_file, send_from_directory, url_for

app = Flask(__name__, static_url_path='/static')

@app.route('/images/<filename>', methods=['GET'])
def get_image(filename):
    file_path = os.path.join('../static/imgs', filename)
    return send_file(file_path)

from app import user_routes
from app import login_routes
from app import messages_routes
from app import notifications_routes
from app import chat_routes

if __name__ == '__main__':
    app.run(debug=True)
