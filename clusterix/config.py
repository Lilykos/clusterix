"""App configuration"""

# DB info
DATABASE = '{drivername}://{username}:{password}@{host}:{port}/{database}'.format(
    drivername='postgres',
    host='localhost',
    port='5432',
    username='db',
    password='db',
    database='clusterix'
)

# Temp folders
TEMP_FILE_PATH = 'temp_input/'
TEMP_MODULE_PATH = 'temp_modules/'
