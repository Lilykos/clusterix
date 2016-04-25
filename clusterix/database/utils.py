from sklearn.externals.joblib import Parallel, delayed

from whoosh.analysis import StemmingAnalyzer, CharsetFilter, StandardAnalyzer
from whoosh.lang import stopwords
from whoosh.support.charset import accent_map
from whoosh.fields import TEXT, NUMERIC
"""
Some regexes for consideration:
split camel case (needs finditer)
    regex = r'(?<=[A-Z])(?=[A-Z][a-z])|(?<=[^A-Z])(?=[A-Z])|(?<=[A-Za-z])(?=[^A-Za-z])'
does not return 's (but returns numbers)
    regex = r"[\w][\w]*'?\w?"
"""

stop = stopwords.stoplists['en']
REGEX = r'\b[^\d\W]+\b'

analyzer = StemmingAnalyzer(expression=REGEX,
                            stoplist=stop,
                            minsize=1) | CharsetFilter(accent_map)

vocab_analyzer = StandardAnalyzer(expression=REGEX,
                                  stoplist=stop,
                                  minsize=3) | CharsetFilter(accent_map)


def get_whoosh_fields(dtypes):
    """
    Returns a dict of field-type mappings for whoosh schema use.
    From: 'Character': 'object'
    To: 'Character': TEXT(stored=True)
    """
    mapping = {}
    for key in dtypes.keys():
        if dtypes[key] == 'object':
            mapping[key] = TEXT(stored=True)
        else:
            mapping[key] = NUMERIC(stored=True)

    return mapping


def get_processed(data, dtypes):
    """
    Process the input using Whoosh analysers, returns a list of dicts.
    Example:
    - CSV                       |   - Results:
    Name,Job,City               |   [{u'City': u'pari', u'Job': u'softwar dev', u'Name': u'john'}]
    John,Software Dev.,Paris    |
    """
    parallel = Parallel(n_jobs=-1, backend='multiprocessing', verbose=1)
    return parallel(delayed(_process)(data[i], i, dtypes) for i in data.keys())


def _process(item, i, dtypes):
    """Process a single item, to be used in parallel."""
    # log_info('Processing item: {}'.format(i))
    data = {}

    for field in item.keys():
        if dtypes[field] == 'object':
            processed = ' '.join([token.text for token in analyzer(item[field])])
            data[field] = processed if processed != '' else u'NaN'
        else:
            data[field] = float(item[field])

    return data


def get_vocabulary(documents):
    """
    Process the vocabulary using Whoosh, returns a vocabulary list.
    Example:
        [['Chicago', 'Software engineering', 'Dreams to go to australia one day!'],
         ['New York City', 'Painting outdoor spaces', 'Own a farm at the woods!']]
    Results:
        [u'chicago software engineering dreams go australia one day',
         u'new york city painting outdoor spaces farm woods']
    """
    parallel = Parallel(n_jobs=-1, backend='multiprocessing', verbose=1)
    return parallel(delayed(_process_vocabulary)(doc) for doc in documents)


def _process_vocabulary(doc):
    row_str = ' '.join(map(unicode, doc))
    return ' '.join([token.text for token in vocab_analyzer(row_str)])



