from flask.views import MethodView
from validators.product_val import ProductRegister, ProductGeneral
from db.cloudant.cloudant_manager import CloudantManager
from flask import jsonify, request
from helpers.db_parser import DBP
from db.postgresql.postgresql_manager import PostgresqlManager
from db.postgresql.model import Appearance
import random

cm = CloudantManager()
product_schema = ProductRegister()
general_schema = ProductGeneral()
my_dbp = DBP()
pm = PostgresqlManager()


class Product(MethodView):
    # Lista de productos
    def get(self):
        try:
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            print(my_db)
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
            
            return jsonify({'st':'ok'})
        except:
            return jsonify({'st': 'error'}), 403

    # agregar producto
    def post(self):
        product_register = request.get_json()
        product_register['role_a'] = '2'
        errors = product_schema.validate()
        if errors:
            return jsonify({'st': errors}), 403
        try:
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            if my_db == "error":
                raise Exception
            sdb = my_dbp.sync(my_db, cm)
            doc_msg = cm.add_doc(my_db, product_register)
            disconnect = cm.disconnect_db("cafe-db")
            if doc_msg == "ok":
                return jsonify({"st": "ok", "sync": sdb}), 200
            elif doc_msg == "error":
                return jsonify({"st": "error", "sync": sdb}), 403
        except:
            new_product = Product(
                id_a = random.randint(0, 99),
                name_a = product_register['name_a'],
                bio_a = product_register['bio_a'],
                price = product_register['price'],
                id_p = product_register['id_p'],
                role_a = product_register['role_a'])
            msg = pm.add(new_product)
            return jsonify({"st": "local"}), 200

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
            errors = general_schema.validate(product_change)
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
            return jsonify({"st": "error"}), 403


    # Eliminar producto
    def delete(self):
        try:
            product_del = request.get_json()
            key_del = product_del['del_key']
            value_del = product_del['del_value']
            product_del.pop('del_key')
            product_del.pop('del_value')
            errors = general_schema.validate(product_del)
            if errrors:
                return jsonify({'st':errors})
        except:
            pass
