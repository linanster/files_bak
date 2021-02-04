from datetime import datetime
from app import db

class MyBaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, nullable=False, autoincrement=True, primary_key=True)
    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False
    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except Exception as e:
            print(e)
            return False

class Todo(MyBaseModel):
    __bind_key__ = 'sqlite_todo'
    __tablename__ = 'todo'
    content = db.Column(db.String(100))
    time = db.Column(db.DateTime)
    status = db.Column(db.Integer)
    def __init__(self, content, time=datetime.now(), status=0):
        self.content = content
        self.time = time
        self.status = status

