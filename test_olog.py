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


url = os.environ['OLOG_URL']
user = os.environ['OLOG_USER']
password = os.environ['OLOG_PASSWORD']
cli = olog.Client(url, user, password)


# Various test parameters
LOGBOOK_NAME = 'Operations'
LOG_ID = 1


@vcr.use_cassette()
def test_list_logbooks():
    cli.list_logbooks()


@vcr.use_cassette()
def test_get_logbook():
    cli.get_logbook(LOGBOOK_NAME)


@vcr.use_cassette()
def test_list_logs_by_logbook():
    cli.list_logs(logbook=LOGBOOK_NAME)


@vcr.use_cassette()
def test_get_log():
    cli.get_log(LOG_ID)
