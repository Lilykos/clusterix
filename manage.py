from flask.ext.script import Manager
from clusterix import app
from clusterix.affiliations.xml_parser import parse
from clusterix.clustering.clusters import cluster_data

manager = Manager(app)


@manager.option('-f', '--file', dest='xml_file', default=None,
                help='Parse the affiliations from xml.')
def parse_xml(xml_file):
    """Parse an xml file and retrieve the affiliations."""
    parse(xml_file)


@manager.command
def cluster():
    """Cluster the existing data."""
    cluster_data()


if __name__ == '__main__':
    manager.run()