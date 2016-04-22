import sys
from flask.ext.script import Manager, Server
from clusterix import app

manager = Manager(app)
manager.add_command('runserver', Server(use_debugger=True))
if __name__ == '__main__':
    sys.setrecursionlimit(10000)  # Overflow if we don't do that
    manager.run()