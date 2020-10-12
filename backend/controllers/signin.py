from flask.views import MethodView
from flask import request, jsonify
from marshmallow import validate
from helpers.crypt import Crypt
from validators.client_val import ClientSignin
from db.cloudant.cloudant_manager import CloudantManager

client_schema = ClientSignin()
cm = CloudantManager()
crypt = Crypt()

class Signin(MethodView):
    def post(self):
        try:
            # Se reciben los datos y se validan
            client_signin = request.get_json()
            client_signin['role'] = "1"
            errors = client_schema.validate(client_signin)
            if errors:
                return jsonify({"st": errors}), 403
            # Se conecta a la db y se agrega el doc
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            # Se encripta la contrasena y se agrega el documento
            client_signin['password'] = crypt.hash_string(client_signin['password'])
            doc_msg = cm.add_doc(my_db, client_signin)
            if doc_msg == "ok":
                return jsonify({"st": "ok"}), 200
            elif doc_msg == "error":
                print("elif")
                return jsonify({"st": "error"}), 403
        except:
            return jsonify({"st": "error"}), 403
        finally:
            disconnect = cm.disconnect_db("cafe-db")
