from flask.views import MethodView
from flask import request, jsonify
from marshmallow import validate
from validators.client import ClientSignin
from helpers.cloudant_manager import cloudantManager

user_schema= ClientSignin()
cm= cloudantManager()

class Signin(MethodView):

    def post(self):
        try:
            # Se reciben los datos y se validan
            client_signin= request.get_json()
            errors= ClientSignin.validate(ClientSignin)
            if errors:
                return jsonify({"st":errors}),403
            # Se conecta a la db y se agrega el doc
            cm.connect_service()
            my_db= cm.connect_db('test-db')
            doc_msg= cm.add_doc(my_db, client_signin)
            if doc_msg == "ok":
                return jsonify({"st":"ok"}),200
            elif doc_msg == "error":
                return jsonify({"st":"error"}),403
        except:
            return jsonify({"st":"error"})
        finally:
            disconnect = cm.disconnect_db("test-db")