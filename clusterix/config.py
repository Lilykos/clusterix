"""App configuration"""

# GROBID specific
GROBID_ENDPOINT = 'http://inspire-grobid.cern.ch:8080/processAffiliations'
GROBID_AFF_PREFIX = 'affiliations='

# DB info
DATABASE = '{drivername}://{username}:{password}@{host}:{port}/{database}'.format(
    drivername='postgres',
    host='localhost',
    port='5432',
    username='db',
    password='db',
    database='affiliations_db'
)

# Temp folders
TEMP_FILE_PATH = 'temp_input/'
TEMP_MODULE_PATH = 'temp_modules/'
