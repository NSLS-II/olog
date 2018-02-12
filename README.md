# pyolog2

This is intended to be a simpler Python client to the Olog. It has one class,
``Client``, with methods corresponding to each command in Olog's REST API.

It includes automated tests that can be run without an Olog server, relying on
previously recorded requests and responses in the source tree. (See later
section for details.)

**It is not currently anywhere near feature-complete.**

## Installation

```
git clone https://github.com/NSLS-II/pyolog2
cd pyolog2
pip install -r requirements.txt
pip install .
```

Or, for a development installation:

```
pip install -r requirements.txt
pip install -r test-requirements.txt
pip install -e .
```

## Usage

Instantiate a Client. We recommend passing authentication info through
environment variables.

```python
from olog import Client
import os

cli = Client(os.eniron['OLOG_URL'],
             os.environ['OLOG_USER'],
             os.environ['OLOG_PASSWORD'])
```

Use the methods on the Client. For example:

```
cli.list_logbooks()
```

## Running Tests

### Simple case: without an Olog server

The tests can be run *without an Olog server*. The source tree contains
serialized requests and responses that were captured during test execution
against a real Olog server. (Authentication information has been filtered out.)
If the requests issued during any test differ from those that were issued during
the capture, the tests will fail. See
[VCR documentation](https://vcrpy.readthedocs.io) for details on this technique.

Run tests:

```
py.test test_olog.py
```

### General case: with an Olog server

If tests are added or changed in a way that alters the requests that they
issue, the tests will need to be re-run with an Olog server.

Start a development Olog server with Docker:

```
git clone https://github.com/lnls-sirius/docker-olog-compose
cd docker-olog-compose
docker-compose up
```

Wait several minutes, and then test with curl:

```
curl -H "Content-Type: application/json" -H "Accept: application/json" -X GET --insecure https://localhost:8181/Olog/resources/logbooks
```

(As we understand it, the ``--insecure`` flag is unfortunately necessary because
Olog assumes it is being deployed without valid SSL certificates. We, the
developers of this Python REST API wrapper, have flagged that issue to the
developers of Olog server.)

Clear the recorded requests and responses and run the tests.

```
rm -rf cassettes/*
```

And finally, run the tests, same as in the simple case:

```
py.test test_olog.py
```

## References

This is based on
[official Olog web service API documentation](https://github.com/Olog/olog-service/raw/master/doc/Release%20Notes%20and%20Manuals.docx)
(a .docx file).
