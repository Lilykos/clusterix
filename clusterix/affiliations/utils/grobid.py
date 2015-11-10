from requests import post
from clusterix.config import Config


def get_grobid_affiliation_xml(affiliation_dict):
    """
    Make a request to the specified GROBID endpoint, to get the affiliation details.

    :param affiliation_dict: The affiliation dict.
    :type affiliation_dict: dict

    :return: A dict with the raw strings and the GROBID xml.
    :rtype: dict
    """
    res = post(Config.GROBID_ENDPOINT,
               Config.GROBID_AFF_PREFIX + affiliation_dict['raw_string'])

    if res.status_code == 200:
        affiliation_dict.update({
            'grobid_xml': res.content
        })

        return affiliation_dict

    return None