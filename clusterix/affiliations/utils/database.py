from ..models import db, Affiliation, BrokenAffiliation

# TODO : FIX THE RETURN STATEMENTS HERE. IT DOES NOT NEED TO RETURN SOMETHING


def save_affiliation(aff):
    """
    Save the affiliation in the db.

    :param aff: The affiliation dictionary.
    :type aff: dict
    :return: The same dictionary
    """
    affiliation = Affiliation(aff['country'], aff['country_code'], aff['post_box'], aff['post_code'], aff['region'],
                              aff['settlement'], aff['institution'], aff['department'], aff['laboratory'],
                              aff['raw_string'], aff['raw_string_unicode'], aff['grobid_xml'], aff['language'])
    db.session.add(affiliation)
    db.session.commit()

    return aff


def save_broken_affiliation(aff):
    """
    Save the affiliation in the db (for the faulty affiliations).

    :param aff: The affiliation dictionary.
    :type aff: dict
    :return: The same dictionary
    """
    affiliation = BrokenAffiliation(aff['raw_string'], aff['raw_string_unicode'], aff['grobid_xml'])
    db.session.add(affiliation)
    db.session.commit()