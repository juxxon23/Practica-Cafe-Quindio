from flask import Flask
from routes import client

app = Flask(__name__)

# Client routes
app.add_url_rule(client['signin'], view_func=client['view_func_signin'])
app.add_url_rule(client['login'], view_func=client['view_func_login'])