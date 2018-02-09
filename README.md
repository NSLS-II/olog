# pyolog2

This is intended to be a simpler Python client to the Olog. It has one class,
``Client``, with methods corresponding to each command in Olog's REST API.

**It is not currently anywhere near feature-complete, and it needs tests.**

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

Instantiate a Client:

```python
from olog import Client

URL = 'https://<HOST>:<PORT>/Olog'
USER = ...
PASSWORD = ...
cli = Client(URL, USER, PASSWORD)
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
the capture, the tests will fail.

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
