import olog
import os
from pathlib import Path
import pytest


RECORDED_URL = "https://localhost:8181/Olog"
# Only required if we are re-recording for VCR.
url = os.environ.get('OLOG_URL', RECORDED_URL)
user = os.environ.get('OLOG_USER', 'olog-user')
admin = os.environ.get('OLOG_ADMIN', 'olog-admin')
password = os.environ.get('OLOG_PASSWORD', '1234')

user_cli = olog.Client(url, user, password)
admin_cli = olog.Client(url, admin, password)


# Various test parameters
LOGBOOK_NAME = 'Operations'
LOG_ID = 1


def test_list_logbooks():
    expected = {'logbook': [{'id': 2,
                             'name': 'Electronics Maintenance',
                             'owner': None,
                             'state': 'Active'},
                            {'id': 4,
                             'name': 'LOTO',
                             'owner': None,
                             'state': 'Active'},
                            {'id': 3,
                             'name': 'Mechanical Technicians',
                             'owner': None,
                             'state': 'Active'},
                            {'id': 1,
                             'name': 'Operations',
                             'owner': None,
                             'state': 'Active'}]}
    actual = user_cli.list_logbooks()
    assert actual == expected


def test_get_logbook():
    expected = {'id': 1,
                'name': LOGBOOK_NAME,
                'owner': None,
                'state': 'Active'}
    actual = user_cli.get_logbook(name=LOGBOOK_NAME)
    assert actual == expected


def test_create_logbook():
    expected = {'id': 12,
                'name': 'Test',
                'owner': 'test',
                'state': 'Active'}
    actual = admin_cli.put_logbook({'name': 'Test', 'owner': 'test'})
    expected.pop('id')
    actual.pop('id')
    assert actual == expected
    admin_cli.delete_logbook('Test')
