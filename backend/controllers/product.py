from flask.views import MethodView
#from validators.product import ProductRegister
from db.cloudant.cloudant_manager import CloudantManager
from flask import jsonify, request

cm = CloudantManager()

class Product(MethodView):
    # Lista de productos
    def get(self):
        try:
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            products = cm.get_query_by(my_db, 'product', 'role')
            for i in range(len(products)):
                products[i] = {
                    'name_a': products[i]['doc']['name_a'],
                    'bio_a': products[i]['doc']['bio_a'],
                    'price': products[i]['doc']['price'],
                    'id_p': products[i]['doc']['id_p'],
                }
            return jsonify({'products':products}), 200
        except:
            return jsonify({'st':'error'}), 403
        finally:
            disconnect = cm.disconnect_db('cafe-db')
        
    # agregar producto
    def post(self):
        try:
            product_register = request.get_json()
            product_register['role'] = 'product' 
            cm.connect_service()
            my_db = cm.connect_db('cafe-db')
            doc_msg = cm.add_doc(my_db, product_register)
            if doc_msg == "ok":
                return jsonify({"st": "ok"}), 200
            elif doc_msg == "error":
                print("elif")
                return jsonify({"st": "error"}), 403
        except:
            return jsonify({"st": "error"}), 403
        finally:
            disconnect = cm.disconnect_db("cafe-db")

        
