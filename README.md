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
             os.environ['USER'],
             os.environ['PASSWORD'])
```

Use the methods on the Client. For example:

```
cli.list_logbooks()
```

## Running Tests

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

If tests are added or changed in a way that alters the requests that they
issue, the tests will need to be re-run with an Olog server.

```
cp .env.example .env
# Fill auth information into .env file. Then:
source .env
rm -rf cassettes/*
py.test test_olog.py
```

## References

This is based on
[official Olog web service API documentation](https://github.com/Olog/olog-service/raw/master/doc/Release%20Notes%20and%20Manuals.docx)
(a .docx file).
