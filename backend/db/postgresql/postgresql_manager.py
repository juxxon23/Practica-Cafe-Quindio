from model import db
from sqlalchemy.exc import SQLAlchemyError


class PostgresqlManager:
    def add(self, *args):
        try:
            for new in args:
                db.session.add(new)
                db.session.commit()
            return 'ok'
        except SQLAlchemyError as e:
            return e
        except:
            return 'error'

    def update(self):
        try:
            db.session.commit()
            return 'ok'
        except SQLAlchemyError as e:
            return e
        except:
            return 'error'

    def delete(self, id_del):
        try:
            db.session.delete(id_del)
            db.session.commit()
            return 'ok'
        except SQLAlchemyError as e:
            return e
        except:
            return 'error'
