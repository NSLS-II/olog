# pyolog2

This is Python client of the new rewritten
[Olog](https://olog-es.readthedocs.io/en/latest/). It has one class,
``Client``, with methods corresponding to each command in Olog's REST API.

It includes automated tests that can be run without an Olog server, relying on
previously recorded requests and responses in the source tree. (See later
section for details.)

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
pip install -r requirements-dev.txt
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
cli.get_logbooks()
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
pytest test_olog.py
```

### General case: with an Olog server

"TO DO: Document how to stand up a new Olog server for testing."

## References

[Official Olog web service API documentation](https://olog-es.readthedocs.io/en/latest/).

[Archived Olog web service API documentation](https://github.com/Olog/olog-service/raw/master/doc/Release%20Notes%20and%20Manuals.docx)(a .docx file).
