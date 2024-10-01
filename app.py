from flask import Flask
import os
import db
from models import Book
from routes.index import index_bp
from routes.request import request_bp

app = Flask(__name__)

if not os.path.isfile('books.db'):
    db.connect()

# the db multiple times
if not os.path.isfile('books.db'):
    db.connect()

# register the blueprints
app.register_blueprint(index_bp)
app.register_blueprint(request_bp)



if __name__ == '__main__':
    port = int(os.environ.get("PORT", 4444))
    app.run(host='0.0.0.0', port=port)

