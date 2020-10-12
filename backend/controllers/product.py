from flask.views import MethodView
from marshmallow import validate
from validators.product_val import Product
from db.cloudant.cloudant_manager import CloudantManager
from flask import jsonify, request
from helpers.db_parser import DBP
from db.postgresql.postgresql_manager import PostgresqlManager
from db.postgresql.model import Client

cm = CloudantManager()
product_schema = Product()
my_dbp = DBP()
pm = PostgresqlManager()


class Product(MethodView):
    # Lista de productos
    def get(self):
        try:
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            sdb = my_dbp.sync(my_db, cm)
            products = cm.get_query_by(my_db, '2', 'role')
            for i in range(len(products)):
                products[i] = {
                    'name_a': products[i]['doc']['name_a'],
                    'bio_a': products[i]['doc']['bio_a'],
                    'price': products[i]['doc']['price'],
                    'id_p': products[i]['doc']['id_p'],
                }
            disconnect = cm.disconnect_db("cafe-db")
            return jsonify({'products': products, 'sync':sdb}), 200
        except:
            return jsonify({'st': 'error'}), 403
        finally:
            pass

    # agregar producto
    def post(self):
        try:
            product_register = request.get_json()
            product_register['role'] = '2'
            errors = product_schema.validate()####
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
            return jsonify({"st": "error"}), 403
        finally:
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
