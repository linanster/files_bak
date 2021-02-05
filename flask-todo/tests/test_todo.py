import unittest
from app import app
from app.models import Todo

class TodoTestCase(unittest.TestCase):

    def setUp(self):
        print('==set up==')
        self.app = app.test_client()

    def tearDown(self):
        print('==tear down==')
        todos  = Todo.query.filter(Todo.content == "iamtest").all()
        for todo in todos:
            todo.delete()

    def test_index(self):
        print('==test index==')
        rv = self.app.get('/')
        assert "Todo" in rv.data.decode()

    def test_todo(self):
        print('==test todo==')
        self.app.post('/add', data = dict(content="iamtest"))
        todo  = Todo.query.filter(Todo.content == "iamtest").first_or_404()
        assert todo is not None
