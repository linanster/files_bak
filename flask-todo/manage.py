from app import app
from app.models import Todo
from flask_script import Manager

manager = Manager(app)

@manager.command
def createdb():
    from app import db
    db.create_all(bind='sqlite_todo')

@manager.command
def deletedb():
    from app import db
    db.drop_all(bind='sqlite_todo')

@manager.command
def savedb():
    todo = Todo(content='study flask')
    todo.save()

if __name__ == '__main__':
    manager.run()
