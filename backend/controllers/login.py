from flask.views import MethodView
from flask import request, jsonify
from helpers.crypt import Crypt
from validators.client_val import ClientLogin
from db.cloudant.cloudant_manager import CloudantManager

client_schema = ClientLogin()
cm = CloudantManager()
crypt = Crypt()


class Login(MethodView):
    def post(self):
        try:
            # Se reciben los datos y se validan
            client_login = request.get_json()
            errors = client_schema.validate(client_login)
            if errors:
                return jsonify({'st': errors}), 403
            # Se conecta a la db y se agrega el doc
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            docs = cm.get_query_by(my_db, client_login['email'], 'email')
            if docs != []:
                doc = docs[0]
                password_msg = crypt.check_hash(
                    client_login['password'], doc['doc']['password'])
                disconnect = cm.disconnect_db('cafe_db')
                if password_msg:
                    return jsonify({'st': 'ok'}), 200
                else:
                    return jsonify({'st': 'pass'}), 403
            return jsonify({'st': 'email'}), 403
        except:
            return jsonify({"st": "error"}), 403

            
