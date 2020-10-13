from flask.views import MethodView
from validators.product_val import ProductRegister, ProductUpdate
from db.cloudant.cloudant_manager import CloudantManager
from flask import jsonify, request
from helpers.db_parser import DBP
from db.postgresql.postgresql_manager import PostgresqlManager

cm = CloudantManager()
product_schema = ProductRegister()
update_schema = ProductUpdate()
my_dbp = DBP()
pm = PostgresqlManager()


class Product(MethodView):
    # Lista de productos
    def get(self):
        try:
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            sdb = my_dbp.sync(my_db, cm)
            products = cm.get_query_by(my_db, '2', 'role_a')
            for i in range(len(products)):
                products[i] = {
                    'name_a': products[i]['doc']['name_a'],
                    'bio_a': products[i]['doc']['bio_a'],
                    'price': products[i]['doc']['price'],
                    'id_p': products[i]['doc']['id_p'],
                }
            disconnect = cm.disconnect_db("cafe-db")
            return jsonify({'products': products, 'sync': sdb}), 200
        except:
            return jsonify({'st': 'error'}), 403

    # agregar producto
    def post(self):
        try:
            product_register = request.get_json()
            product_register['role_a'] = '2'
            errors = product_schema.validate()
            if errors:
                return jsonify({'st': errors}), 403
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            sdb = my_dbp.sync(my_db, cm)
            doc_msg = cm.add_doc(my_db, product_register)
            disconnect = cm.disconnect_db("cafe-db")
            if doc_msg == "ok":
                return jsonify({"st": "ok", "sync": sdb}), 200
            elif doc_msg == "error":
                print("elif")
                return jsonify({"st": "error", "sync": sdb}), 403
        except:
            # Falta agregar respaldo postgresql
            return jsonify({"st": "error"}), 403

    # Actualizar producto
    def put(self):
        try:
            # Se obtiene el json y se extraen las variables
            # change_key y change_value, estas serviran como
            # una especie de indice para realizar busquedas
            product_change = request.get_json()
            key_item = product_change['change_key']
            value_item = product_change['change_value']
            product_change.pop('change_key')
            product_change.pop('change_value')
            errors = update_schema.validate(product_change)
            if errors:
                return jsonify({'st': errors}), 403
            # Conexion y actualizacion
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            sdb = my_dbp.sync(my_db, cm)
            doc_msg = cm.update_doc(
                my_db, key_item, value_item, product_change)
            disconnect = cm.disconnect_db("cafe-db")
            if doc_msg == "ok":
                return jsonify({"st": "ok", "sync": sdb}), 200
            elif doc_msg == "error":
                return jsonify({"st": "error", "sync": sdb}), 403
        except:
            # Falta agregar respaldo postgresql
            return jsonify({"st": "error"}), 403


    # Eliminar producto
    def delete(self):
        pass


"""
new_client = Client(
        id_c=product_register['id'],
        name_c=product_register['name_c'],
        email=product_register['email'],
        phone=product_register['phone'],
        password=product_register['password'],
        role_c=product_register['role'])
message = pm.add(new_client)
print(message)
return message
"""
