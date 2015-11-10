class Config():
    """App configuration"""
    GROBID_ENDPOINT = 'http://inspire-grobid.cern.ch:8080/processAffiliations'
    GROBID_AFF_PREFIX = 'affiliations='

    DATABASE = '{drivername}://{username}:{password}@{host}:{port}/{database}'.format(
        drivername='postgres',
        host='localhost',
        port='5432',
        username='db',
        password='db',
        database='affiliations_db'
    )

    def __init__(self):
        pass
