from flask_script import Manager, Server
from Problem1 import app

manager = Manager(app)
manager.add_command('runserver', Server(host='127.0.0.1', port=6015, use_debugger=True))

@manager.command
def hello():
    print "hello"

@manager.shell
def make_shell_context():
    return dict(app=app)

if __name__ == '__main__':
   manager.run()

 
