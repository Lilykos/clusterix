from flask.ext.script import Manager
from clusterix import app


manager = Manager(app)

if __name__ == '__main__':
    manager.run()

# @manager.option('-f', '--file', dest='xml_file', default=None,
#                 help='Parse the database from xml.')
# def parse_xml(xml_file):
#     """Parse an xml file and retrieve the database."""
#     parse(xml_file)
#
#
# @manager.command
# def cluster():
#     """Cluster the existing data."""
#     BlockClusterer.cluster_data()
