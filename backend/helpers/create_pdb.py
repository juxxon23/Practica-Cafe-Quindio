from flask import Flask
from db.postgresql.model import db
from db.postgresql.postgresql_manager import PostgresqlManager
from db.postgresql.data import role


def create_app():
    data_manager = PostgresqlManager()
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:1234@localhost:5432/Cafe-db'
    with app.app_context():
        db.init_app(app)
        db.create_all()
        for rol in role:
            msg = data_manager.add(rol)
    return app
