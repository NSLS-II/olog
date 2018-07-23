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
                            {'id': 4,
                             'logs': None, 'name': 'LOTO',
                             'owner': None, 'state': 'Active'},
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
    expected = {'id': 1,
                'logs': None,
                'name': 'Operations',
                'owner': None,
                'state': 'Active'}
    actual = cli.get_logbook(name=LOGBOOK_NAME)
    assert actual == expected


@vcr.use_cassette()
def test_list_logs_by_logbook():
    expected = {'attachments': [],
                'createdDate': 1487609015000,
                'description': 'd\t\n\nCause:\nnull\n\nRepair:\nnull\n\nCorrective:\nnull',
                'id': 21,
                'level': 'Problem',
                'logbooks': [{'id': 1,
                              'logs': None,
                              'name': 'Operations',
                              'owner': None,
                              'state': 'Active'}],
                'modifiedDate': 1487609015000,
                'owner': 'olog-user',
                'properties': [{'attributes': {'Area': 'Global',
                                               'Assign': 'Controls',
                                               'BeamState': 'False',
                                               'Contact': 'Kunal Shroff<shroffk@bnl.gov>',
                                               'Device': 'M01',
                                               'System': 'Diagnostics',
                                               'TimeOccoured': '2017-02-20T16:43:23.408Z'},
                                'groupingNum': 0,
                                'id': 1,
                                'logs': None,
                                'name': 'fault'}],
                'source': '130.199.219.79',
                'state': 'Active',
                'tags': [],
                'version': '1'}
    actual = cli.list_logs(logbook=LOGBOOK_NAME)
    assert actual[0] == expected


@vcr.use_cassette()
def test_get_log():
    expected = {'attachments': [],
                'createdDate': 1459083898000,
                'description': 'Creating the first simple entry.\nInstructions for creating log entries\nusername: olog-user\npassword: 1234\n\n?????',
                'id': 1,
                'level': 'Info',
                'logbooks': [{'id': 1,
                              'logs': None,
                              'name': 'Operations',
                              'owner': None,
                              'state': 'Active'}],
                'modifiedDate': 1459083898000,
                'owner': 'olog-user',
                'properties': [],
                'source': '127.0.0.1',
                'state': 'Active',
                'tags': [],
                'version': '1'}
    actual = cli.get_log(LOG_ID)
    assert actual == expected
