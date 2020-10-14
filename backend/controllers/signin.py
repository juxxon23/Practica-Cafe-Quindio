from flask.views import MethodView
from flask import request, jsonify
from helpers.crypt import Crypt
from validators.client_val import ClientSignin
from db.cloudant.cloudant_manager import CloudantManager
from db.postgresql.model import Client
from db.postgresql.postgresql_manager import PostgresqlManager
import random

client_schema = ClientSignin()
cm = CloudantManager()
pm = PostgresqlManager()
crypt = Crypt()


class Signin(MethodView):
    def post(self):
        client_signin = request.get_json()
        client_signin['role_c'] = "1"
        errors = client_schema.validate(client_signin)
        if errors:
            return jsonify({"st": errors}), 403
        try:
            # Se conecta a la db y se agrega el doc
            conn = cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            if my_db == "error":
                raise Exception
            docs = cm.get_query_by(my_db, client_signin['email'], 'email')
            if docs != []:
                doc = docs[0]
                if client_signin['email'] == doc['doc']['email']:
                    return jsonify({"st": "existe"})

            # Se encripta la contrasena y se agrega el documento
            client_signin['password'] = crypt.hash_string(
                client_signin['password'])
            doc_msg = cm.add_doc(my_db, client_signin)
            disconnect = cm.disconnect_db("cafe-db")
            if doc_msg == "ok":
                return jsonify({"st": "ok"}), 200
            elif doc_msg == "error":
                return jsonify({"st": "error"}), 403
        except:
            new_client = Client(
                id_c=random.randint(0,1000000000),
                name_c=client_signin['name_c'],
                email=client_signin['email'],
                phone=client_signin['phone'],
                password=crypt.hash_string(client_signin['password']),
                role_c=client_signin['role_c'])
            msg = pm.add(new_client)
            return jsonify({"st": "local"}), 200

