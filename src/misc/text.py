from sklearn.feature_extraction.text import HashingVectorizer, TfidfVectorizer, CountVectorizer
from sklearn.externals.joblib import Parallel, delayed
from whoosh.analysis import StemmingAnalyzer, CharsetFilter
from whoosh.support.charset import accent_map
from ..config import logger, log, stopwords
from ..utils import load_df

TOKEN_PATTERN = r'\b\w+\b'  # Keeps single letter attrs
STEM_REGEX = r'\b[^\d\W]+\b'

stop = lambda attrs: stopwords if attrs['stopwords'] else None
norm = lambda attrs: None if attrs['norm'] == 'none' else attrs['norm']
join_by_cluster = lambda cl, df, tc: ' '.join(df[df.clx_cluster == cl][tc].apply(' '.join, axis=1).values)

analyzer = StemmingAnalyzer(expression=STEM_REGEX, minsize=1) | CharsetFilter(accent_map)


def get_vectorizer(attrs):
    """Returna a vectorizer with the user options."""
    stop_ = stop(attrs)
    norm_ = norm(attrs)
    features = int(attrs['featureNumber'])
    vectorizers = {
        'hashing': HashingVectorizer(n_features=features, non_negative=True, norm=norm_, stop_words=stop_),
        'tfidf': TfidfVectorizer(max_features=features, norm=norm_, token_pattern=TOKEN_PATTERN, stop_words=stop_),
        'count': CountVectorizer(max_features=features, token_pattern=TOKEN_PATTERN, stop_words=stop_)
    }

    logger.info('- Vectorizer created: {}'.format(attrs['vectorizer']))
    return vectorizers[attrs['vectorizer']]


@log('- TF-IDF scoring started.')
def tfidf(attrs, clusters=None):
    """
    Returns the TF-IDF scores of words, separated by cluster in the form of:
    {
        '0':[{'term': 'x', 'score': y}, {'term': 'x', 'score': y}, ...],
        '1': [...]
    }
    """
    df = load_df()
    text_columns = list(df.select_dtypes(include=['object']).columns)
    attrs['vectorizer'] = 'tfidf'  # monkey-patch to use the API

    # Only get tfidf in text attributes
    if not text_columns:
        return

    # Consider each cluster a document, so get the text from each cluster separately
    # If an cluster list is given, get results for those clusters
    if not clusters:
        clusters = df.clx_cluster.unique()

    text_by_cluster = [join_by_cluster(cluster, df, text_columns) for cluster in clusters]

    # Feature matrix
    vec = get_vectorizer(attrs)
    tfidf_matrix = vec.fit_transform(text_by_cluster).toarray()
    feature_names = vec.get_feature_names()

    # Get the top 10 TF-IDF scores for each cluster
    tfidf_by_cluster = {}
    for cluster, doc in zip(clusters, tfidf_matrix):
        max_10_indices = doc.argsort()[-10:][::-1]
        tfidf_by_cluster[str(cluster)] = [{'term': feature_names[i], 'score': doc[i]}
                                          for i in max_10_indices]
    return tfidf_by_cluster


@log('- Stemming started')
def stem_text_input(text):
    """Stem the text corpus."""
    parallel = Parallel(n_jobs=-1, backend='multiprocessing', verbose=1)
    return parallel(delayed(_stem)(row) for row in text)


def _stem(row):
    """Process a single item, to be used in parallel."""
    return ' '.join([token.text for token in analyzer(row)])
