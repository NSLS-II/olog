import os
from datetime import date, datetime
from pathlib import Path

import pytest
import vcr as _vcr

from olog.httpx_client import Client
from olog.util import UncaughtServerError, ensure_time

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


RECORDED_URL = "http://10.0.137.22:8080/Olog"
# Only required if we are re-recording for VCR.
url = os.environ.get('OLOG_URL', RECORDED_URL)
user = os.environ.get('OLOG_USER', 'olog-logs')
password = os.environ.get('OLOG_PASSWORD', '')
cli = Client(url, user, password)


# Various test parameters
LOG_ID = 1

LOGBOOKS = [{'name': 'Operations', 'owner': 'olog-logs', 'state': 'Active'},
            {'name': 'TEST', 'owner': 'olog-logs', 'state': 'Active'}]
LOGBOOK = {'name': 'Operations', 'owner': 'olog-logs', 'state': 'Active'}
INVALID_LOGBOOK = {'name': 'Operations', 'owner': 'invalid_name',
                   'state': 'Active'}
LOGBOOK_NAME = 'Operations'

PROPS = [{'name': 'Ticket',
          'owner': 'olog-logs',
          'state': 'Active',
          'attributes': [{'name': 'url', 'value': None, 'state': 'Active'},
                         {'name': 'id', 'value': None, 'state': 'Active'}]},
         {'name': 'TEST',
          'owner': 'olog-logs',
          'state': 'Active',
          'attributes': [{'name': 'url', 'value': None, 'state': 'Active'},
                         {'name': 'id', 'value': None, 'state': 'Active'}]}]
PROPERTY = {'name': 'Ticket',
            'owner': 'olog-logs',
            'state': 'Active',
            'attributes': [{'name': 'url', 'value': None, 'state': 'Active'},
                           {'name': 'id', 'value': None, 'state': 'Active'}]}
PROPERTY_ATTRIBUTES = {'url': None, 'id': None}
INVALID_PROPERTY = {'name': 'Ticket',
                    'owner': 'invalid_name',
                    'state': 'Active',
                    'attributes': [{'name': 'url', 'value': None,
                                    'state': 'Active'},
                                   {'name': 'id', 'value': None,
                                    'state': 'Active'}]}
PROPERTY_NAME = 'Ticket'

TAG_NAMES = ['Fault', 'TEST']
TAG = {'name': 'Fault', 'state': 'Active'}
TAG_NAME = 'Fault'

ATTACHMENT_FILE = {'file': open('README.md', 'rb'),
                   'filename': (None, 'test'),
                   'fileMetadataDescription': (None, 'This is a attachment')}
ATTACHMENT_NAME = ATTACHMENT_FILE['filename'][1]

DATETIME_OBJ = datetime(2015, 1, 1, 0, 0, 0)
DATETIME_START = '2015-01-01 00:00:00.000123'
DATETIME_END = '2020-01-01 00:00:00.000123'

TIME_INPUTS = [
        DATETIME_OBJ,
        DATETIME_START,
        '2015-01-01 00:00:00.000123',
        '2015-01-01 00:00:00',
        '2015-01-01 00:00',
        '2015-01-01 00',
        '2015-01-01',
        '2015-01',
        '2015',
        date(2015, 1, 1),
        1420070400.0,
        1420070400]


@vcr.use_cassette()
def test_get_logbooks():
    cli.get_logbooks()


@vcr.use_cassette()
def test_get_logbook():
    cli.get_logbook(LOGBOOK_NAME)


@vcr.use_cassette()
def test_put_logbooks():
    cli.put_logbooks(LOGBOOKS)


@vcr.use_cassette()
def test_put_logbook():
    cli.put_logbook(LOGBOOK)
    with pytest.raises(ValueError):
        cli.put_logbook(INVALID_LOGBOOK)


@vcr.use_cassette()
def test_put_logbook_with_error():
    # extra verification that everything worked correctly.
    # vcr will return a wrong logbook because the recorded
    # response has been manually edited to be inconsistent
    # with the request to exercise this code path
    with pytest.raises(UncaughtServerError):
        cli.put_logbook(LOGBOOK)


def test_get_logs_by_keyword_only_arguments():
    with pytest.raises(TypeError):
        cli.get_logs(LOGBOOK_NAME)


@vcr.use_cassette()
def test_get_logs_by_logbooks():
    logs = cli.get_logs(logbooks=LOGBOOK_NAME)
    for log in logs:
        assert LOGBOOK_NAME == log['logbooks'][0]['name']


@vcr.use_cassette()
def test_get_logs_by_time():
    cli.get_logs(start=DATETIME_START, end=DATETIME_END)


@vcr.use_cassette()
def test_get_log():
    assert LOG_ID == cli.get_log(LOG_ID)['id']


@vcr.use_cassette()
def test_get_attachment():
    cli.get_attachment(LOG_ID, ATTACHMENT_NAME)


@vcr.use_cassette()
def test_post_attachment():
    cli.post_attachment(1, ATTACHMENT_FILE)


@vcr.use_cassette()
def test_get_tags():
    cli.get_tags()


@vcr.use_cassette()
def test_get_tag():
    assert TAG == cli.get_tag(TAG_NAME)


@vcr.use_cassette()
def test_put_tags():
    cli.put_tags(TAG_NAMES)


@vcr.use_cassette()
def test_put_tag():
    cli.put_tag(TAG_NAME)


@vcr.use_cassette()
def test_get_properties():
    cli.get_properties()


@vcr.use_cassette()
def test_get_property():
    cli.get_property(PROPERTY_NAME)


@vcr.use_cassette()
def test_put_properties():
    cli.put_properties(PROPS)


@vcr.use_cassette()
def test_put_property():
    cli.put_property(PROPERTY_NAME, PROPERTY_ATTRIBUTES)


@vcr.use_cassette()
def test_put_property_with_error():
    # vcr will return a wrong property because the recorded
    # response has been manually edited to be inconsistent
    # with the request to exercise this code path
    with pytest.raises(UncaughtServerError):
        cli.put_property(PROPERTY_NAME, PROPERTY)


def test_ensure_time():
    for time in TIME_INPUTS[:-2]:
        assert '2015-01-01 00:00:00.000' == ensure_time(time)
    for time in TIME_INPUTS[-2:]:
        # fromtimestamp() return local time. In this test case, timestamp and
        # datetime given match in GMT which is +5 hours comparing to UTC.
        # The code below will calculate the  diff(hours) between where the
        # code being execuated and GMT. Then correct it in assert.
        local = datetime.fromtimestamp(0).hour
        diff = local - 24 if local > 12 else local
        assert '2015-01-01 00:00:00.000' == ensure_time(time - diff*3600)
    with pytest.raises(ValueError):
        ensure_time('ABC')
