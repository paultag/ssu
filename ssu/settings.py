from pupa.settings import *


DATABASES['production'] = DATABASES['default']


DATABASES['untrusted'] = dj_database_url.parse(os.environ.get(
    'UNTRUSTED_DATABASE_URL',
    'postgres://pupa:pupa@localhost/untrusted_opencivicdata'
))

DATABASES['default'] = DATABASES['untrusted']
