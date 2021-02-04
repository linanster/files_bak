SECRET_KEY = "youdonotknowme"
SQLALCHEMY_TRACK_MODIFICATIONS = False
# DEBUG = False

SQLALCHEMY_BINDS = {
    'sqlite_todo': 'sqlite:///../sqlite/todo.sqlite3',
}

