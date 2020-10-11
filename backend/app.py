from flask import Flask
from flask_cors import CORS
from routes import client
from db.postgresql.model import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/Cafe-db'
CORS(app, support_credentials=True)
db.init_app(app)

# Client routes
app.add_url_rule(client['signin'], view_func=client['view_func_signin'])
app.add_url_rule(client['login'], view_func=client['view_func_login'])