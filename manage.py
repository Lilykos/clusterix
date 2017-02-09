from flask_script import Manager, Server
from src import app
from src.config import logger

manager = Manager(app)
manager.add_command('runserver', Server(use_debugger=True))
if __name__ == '__main__':
    logger.info(
        """
          ___ _   _   _ ___ _____ ___ ___ _____  __
         / __| | | | | / __|_   _| __| _ \_ _\ \/ /
        | (__| |_| |_| \__ \ | | | _||   /| | >  <
         \___|____\___/|___/ |_| |___|_|_\___/_/\_\\

        """)
    manager.run()
