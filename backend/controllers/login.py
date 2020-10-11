from flask.views import MethodView
from flask import request, jsonify
from marshmallow import validate
from validators.client import ClientLogin
from db.cloudantManager import CloudantManager

client_schema = ClientLogin()
cm = CloudantManager()

class Login(MethodView):
    def post(self):
        try:
            # Se reciben los datos y se validan
            client_schema = request.get_json()
            errors = client_schema.validate(client_schema)
            if errors:
                return jsonify({"st":errors}),403
            # Se conecta a la db y se agrega el doc
            cm.connect_service()
            my_db = cm.connect_db('test-db')
            docs = cm.get_all_docs(my_db)
            for doc in docs:
                if doc['doc']['email'] == client_schema['email']:
                    if doc['doc']['password'] == client_schema['password']:
                        return jsonify({'st':'ok'}),200
                    else:
                        return jsonify({'st':'pass'}),403
            return jsonify({'st':'email'}),403
        except:
            return jsonify({"st":"error"}), 403
        finally:
            disconnect = cm.disconnect_db('test_db')
