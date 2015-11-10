from lxml import etree
from bs4 import SoupStrainer, BeautifulSoup

from processing import process_affiliation


def parse(xml_file):
    """
    Parse an xml file, get the affiliations and start the processing.

    :param xml_file: The xml file path.
    :type xml_file: str
    """
    affiliation_elements = []

    for tag in [100, 700]:
        # We need to parse the xml as a string to strip the accents ourselves
        # because the built-in bs4 parser creates unicode / utf-8 problems
        tree = etree.parse(xml_file)
        xml = etree.tostring(tree.getroot())

        restrict = SoupStrainer('datafield', {'tag': tag})
        soup = BeautifulSoup(xml, 'lxml', parse_only=restrict)

        affiliation_elements += soup.findAll('subfield', {'code': 'v'})

    affiliations = [a.text for a in affiliation_elements]

    for affiliation in affiliations:
        process_affiliation(affiliation)