import sys

from flask.ext.script import Manager
from clusterix import app


# manager = Manager(app)

if __name__ == '__main__':
    sys.setrecursionlimit(10000)  # Overflow if we don't do that
    # manager.run()
    app.run(threaded=True)