# pip install tornado
import os

import tornado.ioloop
import tornado.web
import tornado.websocket
from tornado.options import define, options, parse_command_line
from tornado.web import url

# 定义运行参数
define('port', default=8000, type=int)
define('debug', default=True, type=bool)

# 项目根路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print('BASE_DIR', BASE_DIR)
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# 1.登录
class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('login.html')
    def post(self):
        auth_users = ['user1', 'user2']
        username = self.get_argument('username')
        password = self.get_argument('password')
        print('==username==', username)
        if username in auth_users:
            print('==login success==')
            self.set_secure_cookie('username', username, expires_days=1)
            self.redirect(self.reverse_url('chat'))
        else:
            print('==login failed==')
            self.redirect(self.reverse_url('login'))

# 2. 聊天
class ChatHandler(tornado.web.RequestHandler):
    def get(self):
        username = self.get_secure_cookie('username').decode()
        self.render('chat.html', username=username)

# 3. 聊天服务器WebSocket
class MessageHandler(tornado.websocket.WebSocketHandler):
    # 聊天室所有用户
    online_users = []
    # 当用户连接时自动调用
    def open(self, *args, **kwargs):
        print('open')
        # 把登录的用户添加至online_users中， self指新用户
        self.online_users.append(self)
    # 接收用户发送过来的消息
    def on_message(self, message):
        print('on_message')
        # 群发接受到的消息
        username = self.get_secure_cookie('username').decode()
        for user in self.online_users:
            user.write_message('[{}]: {}'.format(username, message))

    # 关闭： 当用户退出聊天室时自动调用
    def on_close(self):
        print('on_close')
        # 把登出用户删除
        self.online_users.remove(self)


def make_app():
    return tornado.web.Application(
        handlers = [
            url(r'/chat/index/', LoginHandler, name='login'),
            url(r'/chat/chatroom/', ChatHandler, name='chat'),
            # 聊天服务器websocket
            url(r'/chat/messageserver/', MessageHandler, name='message'),
        ],
        debug = options.debug,
        template_path = os.path.join(BASE_DIR, 'templates'),
        cookie_secret = 'abc123',
    )

if __name__ == '__main__':
    parse_command_line()
    app = make_app()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
