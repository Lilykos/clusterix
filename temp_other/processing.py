from temp_other.database.models import InputItem
# from ..database.utils.database import save_affiliation


def examine_country_attrs(affiliation):
    """
    Filter the country of the affiliation dict and replace some specific strings that cause
    errors, in the country code and other fields.

    :param affiliation: The affiliation dictionary which examined for possible mistakes.
    :type affiliation: dict

    :return: The new (hopefully fixed) database dict.
    :rtype: dict
    """
    DEFAULT = ''

    def _find_second_last(text, pattern):
        return text.rfind(pattern, 0, text.rfind(pattern))

    country = affiliation.get('affiliation:address:country', DEFAULT)
    if country:
        raw_string = affiliation['raw_string']

        if country in ['US', 'United States of America']:
            process_affiliation(raw_string.replace(country, 'USA'))
        elif country == 'Saudia Arabia':
            process_affiliation(raw_string.replace(country, 'Saudi Arabia'))
        elif country == 'I. R. Iran':
            process_affiliation(raw_string.replace(country, 'Iran'))
        else:
            countries = [c.strip() for c in country.split(',')]

            # We need to make sure we found a result that can be parsed,
            # or else there is the danger of an endless loop
            if len(countries) == 2:
                i = _find_second_last(raw_string, countries[0])
                raw_string = raw_string[:i] + raw_string[i+len(countries[0]):]
                process_affiliation(raw_string)

        # Important! It returns None to stop the current processing workflow.
        # The process_affiliation method will start a new one, with the fixed string.
        return None
    else:
        return affiliation


def process_affiliation(affiliation_str):
    """
    Process the original affiliation string, through defined steps, and return the final dictionary or None,
    depending on whether a step failed or not.

    :param affiliation_str: The affiliation raw string
    :type affiliation_str: str
    :return: The processed dictionary of the affiliation.
    :rtype: dict
    """
    if not InputItem.query.filter_by(raw_string=affiliation_str).first():
        return

        # return (
        #     affiliation_str > maybe             # break if None
        #     | remove_ampersand
        #     | detect_language                   # translate if not english text
        #     | get_grobid_affiliation_xml        # get GROBID affiliation
        #     | flatten_affiliation_dict          # flatten the dictionary
        #     | examine_country_attrs             # do some pattern matching for faulty countries
        #     | map_affiliation                   # map to the new data model
        #     | preprocess_text                   # map to the new data model
        #     | save_affiliation                  # save to db
        # )
