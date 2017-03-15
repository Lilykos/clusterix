import logging
import sys


# Algorithm templates
algorithm_paths = {
    'kmeans':       'algorithms/kmeans.html',
    'hcluster':     'algorithms/hcluster.html',
    'meanshift':    'algorithms/meanshift.html',
    'dbscan':       'algorithms/dbscan.html'
}

# App configuration
TEMP_PATH = 'temp/'
CLUSTERER_PATH = 'temp/clusterer.pkl'
DATAFRAME_PATH = 'temp/dataframe.pkl'
DECOMPOSITION_MODEL_PATH = 'temp/{}.pkl'
X_PATH = 'temp/X.npy'

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself',
             'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself',
             'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these',
             'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do',
             'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
             'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
             'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
             'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each',
             'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than',
             'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']

# Logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s - %(levelname)s\t%(message)s',
                    datefmt='(%Y-%m-%d %H:%M:%S)')
logger = logging


def log(msg):
    """Logger decorator."""
    def decorator(func):
        def wrapper(*args):
            logger.info(msg)
            return func(*args)
        return wrapper
    return decorator
