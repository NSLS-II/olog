import olog
import os
from pathlib import Path
import pytest
import vcr as _vcr


# This stashes Olog server responses in JSON files (one per test)
# so that an actual server does not have to be running.
# Authentication 
cassette_library_dir = str(Path(__file__).parent / Path('cassettes'))
vcr = _vcr.VCR(
    serializer='json',
    cassette_library_dir=cassette_library_dir,
    record_mode='once',
    match_on=['uri', 'method'],
    filter_headers=['authorization']
)


RECORDED_URL = "https://localhost:9992/Olog"
# Only required if we are re-recording for VCR.
url = os.environ.get('OLOG_URL', RECORDED_URL)
user = os.environ.get('OLOG_USER', 'olog-user')
password = os.environ.get('OLOG_PASSWORD', '1234')
cli = olog.Client(url, user, password)


# Various test parameters
LOGBOOK_NAME = 'Operations'
LOG_ID = 1


@vcr.use_cassette()
def test_list_logbooks():
    expected = {'logbook': [{'id': 2,
       'logs': None,
       'name': 'Electronics Maintenance',
       'owner': None,
       'state': 'Active'},
      {'id': 4, 'logs': None, 'name': 'LOTO', 'owner': None, 'state': 'Active'},
      {'id': 3,
       'logs': None,
       'name': 'Mechanical Technicians',
       'owner': None,
       'state': 'Active'},
      {'id': 1,
       'logs': None,
       'name': 'Operations',
       'owner': None,
       'state': 'Active'}]}
    actual = cli.list_logbooks()
    assert actual == expected


@vcr.use_cassette()
def test_get_logbook():
    cli.get_logbook(LOGBOOK_NAME)


@vcr.use_cassette()
def test_list_logs_by_logbook():
    cli.list_logs(logbook=LOGBOOK_NAME)


@vcr.use_cassette()
def test_get_log():
    cli.get_log(LOG_ID)
