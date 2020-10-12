from db.postgresql.model import Role

role_client = Role(id_r='1', name_r='client')
role_appearance = Role(id_r='2', name_r='product')
role_favorite = Role(id_r='3', name_r='favorite')
role_bill = Role(id_r='4', name_r='bill')
role_history = Role(id_r='5', name_r='history')

role = [role_client, role_appearance,
        role_favorite, role_bill, role_history]
