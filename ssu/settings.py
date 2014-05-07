from pupa.settings import *


DATABASES['production'] = DATABASES['default']


DATABASES['untrusted'] = os.environ.get(
    'UNTRUSTED_DATABASE_URL',
    'postgres://pupa:pupa@localhost/untrusted_opencivicdata'
)

DATABASES['default'] = DATABASES['untrusted']
