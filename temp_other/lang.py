from langid import classify
from stemming.porter2 import stem
from nltk import word_tokenize
from nltk.corpus import stopwords

from clusterix.utils.lang import strip_accents_from_str


def detect_language(affiliation_str):
    """
    Detects the language of the affiliation string.

    :param affiliation_str: The original affiliation string.
    :type affiliation_str: str

    :return: A dictionary with the original string, the stripped of accents string and lang details.
    :rtype: dict
    """
    lang_id = classify(affiliation_str)
    flat = {
        'raw_string': strip_accents_from_str(affiliation_str),
        'raw_string_unicode': affiliation_str,
        'language': lang_id[0]
    }
    return flat


def preprocess_text(affiliation_dict):
    """
    Stems and removes stopwords from certain affiliation fields.

    :param affiliation_dict: The processed affiliation dict.
    :type affiliation_dict: dict

    :return: The affiliation dict, stemmed and without stopwords
    :rtype: dict
    """
    stop = stopwords.words('english') \
        if affiliation_dict['language'] == 'en' \
        else stopwords.words()

    for key in ['institution', 'department', 'laboratory']:
        sentence = word_tokenize(affiliation_dict[key].lower())
        words = [word for word in sentence if (word not in stop and word.isalnum())]

        affiliation_dict.update({
            key: ' '.join(stem(word) for word in words)
        })

    return affiliation_dict


##########################
# Very specific functions
# (to be moved later)
##########################
def remove_ampersand(affiliation_str):
    return affiliation_str.replace('&', ',')