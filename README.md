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

Start a development Olog server with Docker:

```
docker pull mrakitin/olog-mysql-db:latest
docker pull mrakitin/olog-server:latest
docker run -d --name=olog-mysql-db -e MYSQL_USER=olog_user -e MYSQL_ROOT_PASSWORD=password -e MYSQL_PASSWORD=password -e MYSQL_DATABASE=olog mrakitin/olog-mysql-db:latest
docker run -d --name=olog-server -p 4848:4848 -p 8181:8181 --link olog-mysql-db mrakitin/olog-server:latest asadmin --user=admin --passwordfile=/tmp/glassfishpwd start-domain -v
```

Wait at least 60 seconds for the server to start. Then, before running the
Python tests, we suggest checking that the server is up using ``curl``:

```
curl -H "Content-Type: application/json" -H "Accept: application/json" -X GET --insecure https://localhost:8181/Olog/resources/logbooks
```

(As we understand it, the ``--insecure`` flag is unfortunately necessary because
Olog assumes it is being deployed without valid SSL certificates. We, the
developers of this Python REST API wrapper, have flagged that issue to the
developers of Olog server.)

Run the tests:

```
pytest test_olog.py
```

Finally, to clean up docker when finished:

```
docker stop olog-server olog-mysql-db && docker rm olog-server olog-mysql-db
```

## References

This is based on
[official Olog web service API documentation](https://github.com/Olog/olog-service/raw/master/doc/Release%20Notes%20and%20Manuals.docx)
(a .docx file).
