from db.postgresql.model import Client, Product, Appearance
from db.postgresql.model import Favorite, Bill, History
from db.postgresql.postgresql_manager import PostgresqlManager

pm = PostgresqlManager()


class DBP:
    def sync(self, my_db, cm):
        try:
            # Sincronizacion de la tabla Client
            client_temp = pm.get_all(Client)
            if client_temp != []:
                for client in client_temp:
                    client_nosql = {
                        'name_c': client.name_c,
                        'email': client.email,
                        'phone': client.phone,
                        'password': client.password,
                        'role_c': '1'
                    }
                    msg = cm.add_doc(my_db, client_nosql)
                    client_del = pm.delete(client)
            print('Sincronizacion 1 completada')

            # Sincronizacion de la tabla Appearance
            appearance_temp = pm.get_all(Appearance)
            if appearance_temp != []:
                for appearance in appearance_temp:
                    appearance_nosql = {
                        'name_a': appearance.name_a,
                        'bio_a': appearance.bio_a,
                        'price': appearance.price,
                        'id_p': appearance.id_p,
                        'role_a': '2'
                    }
                    msg = cm.add_doc(my_db, appearance_nosql)
                    appearance_del = pm.delete(appearance)
            print('Sincronizacion 2 completada')

            # Sincronizacion de la tabla Product
            product_temp = pm.get_all(Product)
            if product_temp != []:
                for product in product_temp:
                    product_nosql = {
                        'name_p': product.name_p,
                        'bio_p': product.bio_p,
                    }
                    msg = cm.add_doc(my_db, product_nosql)
                    product_del = pm.delete(product)
            print('Sincronizacion product completada')

            # Sincronizacion de la tabla Favorite
            favorite_temp = pm.get_all(Favorite)
            if favorite_temp != []:
                for favorite in favorite_temp:
                    favorite_nosql = {
                        'id_f': favorite.id_f,
                        'id_c': favorite.id_c,
                        'id_a': favorite.id_a,
                        'role_f': '3'
                    }
                    msg = cm.add_doc(my_db, favorite_nosql)
                    favorite_del = pm.delete(favorite)
            print('Sincronizacion 3 completada')

            # Sincronizacion de la tabla Bill
            bill_temp = pm.get_all(Bill)
            if bill_temp != []:
                for bill in bill_temp:
                    bill_nosql = {
                        'id_b': bill.id_b,
                        'id_c': bill.id_c,
                        'id_a': bill.id_a,
                        'quantity': bill.quantity,
                        'total': bill.total,
                        'role_b': '5'
                    }
                    msg = cm.add_doc(my_db, bill_nosql)
                    bill_del = pm.delete(bill)
            print('Sincronizacion 4 completada')

            # Sincronizacion de la tabla History
            history_temp = pm.get_all(History)
            if history_temp != []:
                for history in history_temp:
                    history_nosql = {
                        'id_h': history.id_h,
                        'id_b': history.id_b,
                        'role_h': '6'
                    }
                    msg = cm.add_doc(my_db, history_nosql)
                    history_del = pm.delete(history)
            print('Sincronizacion 5 completada')
            return 'ok'
        except:
            return 'error'
