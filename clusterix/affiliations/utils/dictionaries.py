from pyexpat import ExpatError

import xmltodict

from ..utils.database import save_broken_affiliation
from clusterix.utils.dictionaries import flatten_dict


def flatten_affiliation_dict(affiliation_dict):
    """
    Parse the xml from GROBID into a dictionary, and then flatten it,in order to make the process of mapping easier.
    If the affiliation cannot be parsed correctly, it is saved in the database, on the table specified by the model.

    :param affiliation_dict: The affiliation dict.
    :type affiliation_dict: dict

    :return: The flattened affiliation dict.
    :rtype: tuple
    """
    try:
        xml_to_dict = xmltodict.parse(affiliation_dict['grobid_xml'])
        flat = flatten_dict(xml_to_dict)

        flat.update({
            'raw_string': affiliation_dict['raw_string'],
            'raw_string_unicode': affiliation_dict['raw_string_unicode'],
            'grobid_xml': affiliation_dict['grobid_xml'],
            'language': affiliation_dict['language']
        })
        return flat
    except ExpatError:
        save_broken_affiliation(affiliation_dict)
        return None


def map_affiliation(affiliation_dict):
    """
    Maps the flattened affiliation dictionary to a new data model, that will be used for clustering.

    :param affiliation_dict: The affiliation dictionary which will be simplified.
    :type affiliation_dict: dict

    :return: The new, mapped dictionary.
    :rtype: dict
    """
    DEFAULT = ''

    def _get_organization(key):
        """
        Get the organization based on the key (department, lab, institution).
        Handles cases of multiple organizations with the same key.
        """
        orgs = affiliation_dict.get('affiliation:orgName', DEFAULT)
        if orgs:
            return ' '.join(org['#text'] for org in orgs if org['@type'] == key)
        else:
            return affiliation_dict.get('affiliation:orgName:#text', DEFAULT) \
                if affiliation_dict.get('affiliation:orgName:@type') == key \
                else DEFAULT

    def _get_field(key):
        """ Get the address attribute based on the given key."""
        return affiliation_dict.get(key, DEFAULT)

    def _get_country():
        """ Get the country, handles for the observed cases."""
        country = affiliation_dict.get('affiliation:address:country:#text', DEFAULT)
        return country \
            if country \
            else affiliation_dict.get('affiliation:address:country', DEFAULT)

    # Use the internal functions to create the new mapped item
    final = {
        # Address Info
        'country':      _get_country(),
        'country_code': _get_field('affiliation:address:country:@key'),
        'post_box':     _get_field('affiliation:address:postBox'),
        'post_code':    _get_field('affiliation:address:postCode'),
        'region':       _get_field('affiliation:address:region'),
        'settlement':   _get_field('affiliation:address:settlement'),

        # Organization Info
        'institution':  _get_organization('institution'),
        'department':   _get_organization('department'),
        'laboratory':   _get_organization('laboratory'),

        # Keep the original info as well
        'raw_string': affiliation_dict['raw_string'],
        'raw_string_unicode': affiliation_dict['raw_string_unicode'],
        'grobid_xml': affiliation_dict['grobid_xml'],
        'language': affiliation_dict['language']
    }

    return final