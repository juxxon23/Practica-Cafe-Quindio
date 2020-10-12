from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Client(db.Model):
    __tablename__ = "Client"

    id_c = db.Column(db.String(10), primary_key=True, nullable=False)
    name_c = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(128), nullable=False)
    role_c = db.Column(db.String(2), db.ForeignKey('Role.id_r'))
    favorite_c = db.relationship(
        'Favorite', backref='client_fav', lazy='dynamic', foreign_keys='Favorite.id_c')
    bill_c = db.relationship(
        'Bill', backref='client_bill', lazy='dynamic', foreign_keys='Bill.id_c')

    def __init__(self, id_c, name_c, email, phone, password, role_c):
        self.id_c = id_c
        self.name_c = name_c
        self.email = email
        self.phone = phone
        self.password = password
        self.role_c = role_c


class Product(db.Model):
    __tablename__ = "Product"

    id_p = db.Column(db.String(2), primary_key=True, nullable=False)
    name_p = db.Column(db.String(40), nullable=False)
    bio_p = db.Column(db.String(200))
    appearance_p = db.relationship(
        'Appearance', backref='category', lazy='dynamic', foreign_keys='Appearance.id_p')

    def __init__(self, id_p, name_p, bio_p, role_p):
        self.id_p = id_p
        self.name_p = name_p
        self.bio_p = bio_p
        self.role_p = role_p


class Appearance(db.Model):
    __tablename__ = "Appearance"

    id_a = db.Column(db.String(2), primary_key=True, nullable=False)
    name_a = db.Column(db.String(40), nullable=False)
    bio_a = db.Column(db.String(200))
    price = db.Column(db.Float(), nullable=False)
    id_p = db.Column(db.String(2), db.ForeignKey('Product.id_p'))
    role_a = db.Column(db.String(2), db.ForeignKey('Role.id_r'))
    favorite_a = db.relationship(
        'Favorite', backref='appearance_fav', lazy='dynamic', foreign_keys='Favorite.id_a')
    bill_a = db.relationship(
        'Bill', backref='appearance_bill', lazy='dynamic', foreign_keys='Bill.id_a')

    def __init__(self, id_a, name_a, bio_a, price, id_p, role_a):
        self.id_a = id_a
        self.name_a = name_a
        self.bio_a = bio_a
        self.price = price
        self.id_p = id_p
        self.role_a = role_a


class Favorite(db.Model):
    __tablename__ = "Favorite"

    id_f = db.Column(db.String(2), primary_key=True, nullable=False)
    id_c = db.Column(db.String(10), db.ForeignKey('Client.id_c'))
    id_a = db.Column(db.String(2), db.ForeignKey('Appearance.id_a'))
    role_f = db.Column(db.String(2), db.ForeignKey('Role.id_r'))

    def __init__(self, id_f, id_c, id_a, role_f):
        self.id_f = id_f
        self.id_c = id_c
        self.id_a = id_a
        self.role_f = role_f


class Bill(db.Model):
    __tablename__ = "Bill"

    id_b = db.Column(db.String(5), primary_key=True, nullable=False)
    id_c = db.Column(db.String(10), db.ForeignKey('Client.id_c'))
    id_a = db.Column(db.String(2), db.ForeignKey('Appearance.id_a'))
    quantity = db.Column(db.Integer, nullable=False)
    total = db.Column(db.Float(), nullable=False)
    date_b = db.Column(db.DateTime, nullable=False)
    role_b = db.Column(db.String(2), db.ForeignKey('Role.id_r'))

    def __init__(self, id_b, id_c, id_a, quantity, total, date_b, role_b):
        self.id_b = id_b
        self.id_c = id_c
        self.id_a = id_a
        self.quantity = quantity
        self.total = total
        self.date_b = date_b
        self.role_b = role_b


class History(db.Model):
    __tablename__ = "History"

    id_h = db.Column(db.String(2), primary_key=True, nullable=False)
    id_b = db.Column(db.String(5), db.ForeignKey('Bill.id_b'))
    role_h = db.Column(db.String(2), db.ForeignKey('Role.id_r'))

    def __init(self, id_h, id_b, role_h):
        self.id_h = id_h
        self.id_b = id_b
        self.role_h = role_h


class Role(db.Model):
    __tablename__ = "Role"

    id_r = db.Column(db.String(2), primary_key=True, nullable=False)
    name_r = db.Column(db.String(10), nullable=False)
    id_c = db.relationship(
        'Client', backref='role_cli', lazy='dynamic', foreign_keys='Client.role_c')
    id_a = db.relationship(
        'Appearance', backref='role_app', lazy='dynamic', foreign_keys='Appearance.role_a')
    id_f = db.relationship(
        'Favorite', backref='role_fav', lazy='dynamic', foreign_keys='Favorite.role_f')
    id_b = db.relationship(
        'Bill', backref='role_bil', lazy='dynamic', foreign_keys='Bill.role_b')
    id_h = db.relationship(
        'History', backref='role_his', lazy='dynamic', foreign_keys='History.role_h')

    def __init(self, id_r, name_r):
        self.id_r = id_r
        self.name_r = name_r
