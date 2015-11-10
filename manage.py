from flask.ext.script import Manager
from clusterix import app
from clusterix.affiliations.xml_parser import parse

manager = Manager(app)


@manager.command
@manager.option('-f', '--file', dest='xml_file', default=None,
                help='Parse the affiliations from xml.')
def parse_xml(xml_file):
    """
    Parse an xml file and get the affiliations.
    Implementation depends on the file structure.

    :param xml_file: The xml file path.
    :type xml_file: str
    """
    parse(xml_file)


if __name__ == '__main__':
    manager.run()