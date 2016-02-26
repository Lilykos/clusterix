from pyexpat import ExpatError


def flatten_dict(dictionary, l_key='', separator=':'):
    """
    Flattens a dictionary using a specified separator to provide an XPath-like
    data structure. The flattening happens up to the first level of lists.

    :param dictionary: The dict to be flattened.
    :type dictionary: dict

    :param l_key: The left key used for flattening (not to be used externally).
    :type l_key: str

    :param separator: The separator for the flattened keys.
    :type separator: str

    :return: A flattened dictionary (up to the first level, lists are not flattened).
    :rtype: dict
    """
    flat = {}
    for r_key, val in dictionary.items():
        key = l_key + r_key

        # If it is a dict, recursion to flatten it
        if isinstance(val, dict):
            flat.update(flatten_dict(val, l_key=key+separator))
        else:
            flat[key] = val
    return flat


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
    Maps the flattened affiliation dictionary to a new data model, that will be used for clusterers.

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