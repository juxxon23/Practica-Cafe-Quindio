from flask.views import MethodView
from flask import request, jsonify
from marshmallow import validate
from helpers.crypt import Crypt
from validators.client_val import ClientSignin
from db.cloudant.cloudant_manager import CloudantManager
<<<<<<< HEAD

client_schema = ClientSignin()
cm = CloudantManager()
crypt = Crypt()

=======

user_schema = ClientSignin()
cm = CloudantManager()
>>>>>>> eb47fae85c2885803c5c18e653929ba64227deb6

class Signin(MethodView):
    def post(self):
        try:
            # Se reciben los datos y se validan
            client_signin = request.get_json()
<<<<<<< HEAD
            errors = client_schema.validate(client_signin)
=======
            errors = ClientSignin.validate(client_signin)
>>>>>>> eb47fae85c2885803c5c18e653929ba64227deb6
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
            print("except")
            return jsonify({"st": "error"})
        finally:
            disconnect = cm.disconnect_db("cafe-db")
