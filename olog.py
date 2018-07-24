from datetime import datetime
import json
import requests
import requests.auth


__all__ = ['Client']

headers = {'content-type': 'application/json', 'accept': 'application/json'}


class Client:
    def __init__(self, url, user, password):
        """
        url : string
            base URL, such as ``'https://some_host:port/Olog'``
        user : string
        password : string
        """
        if url.endswith('/'):
            url = url[:-1]
        auth = requests.auth.HTTPBasicAuth(user, password)
        self._url = url
        self._session = requests.Session()
        # I have requested that working certificates be properly configured on
        # the server. This is unfortunately a necessary workaround for now....
        self._session.verify = False
        self._kwargs = dict(headers=headers, auth=auth)  # for every request

    def list_logbooks(self):
        url = f'{self._url}/resources/logbooks'
        res = self._session.get(url, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def get_logbook(self, name):
        # Logbooks have an integer id, but this REST endpoint expects the
        # *name*.  It does not accept an id.
        url = f'{self._url}/resources/logbooks/{name}'
        res = self._session.get(url, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def delete_logbook(self, name):
        # Logbooks have an integer id, but this REST endpoint expects the
        # *name*.  It does not accept an id.
        url = f'{self._url}/resources/logbooks/{name}'
        res = self._session.delete(url, **self._kwargs)
        res.raise_for_status()
        # Remove .json() below since it returns
        # "JSONDecodeError: Expecting value: line 1 column 1 (char 0)"
        return res

    def post_logbook(self, logbook):
        """
        # TODO: check what it does, cannot create a logbook with the method
        Create a logbook.
        """
        url = f'{self._url}/resources/logbooks'
        res = self._session.post(url, data=logbook, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def put_logbook(self, logbook):
        """
        Create or update a logbook (matched by name).
        """
        url = f'{self._url}/resources/logbooks/{logbook["name"]}'
        res = self._session.put(url, json=logbook, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def list_logs(self, logbook=None, tag=None, componentType=None,
                  start=None, end=None,
                  search=None,
                  **params):
        if isinstance(start, datetime):
            start = start.timestamp()
        if isinstance(end, datetime):
            end = end.timestamp()
        params.update(dict(logbook=logbook,
                           tag=tag,
                           componentType=componentType,
                           search=search,
                           start=start,
                           end=end))
        url = f'{self._url}/resources/logs'
        res = self._session.get(url, params=params, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def get_log(self, id):
        url = f'{self._url}/resources/logs/{id}'
        res = self._session.get(url, **self._kwargs)
        res.raise_for_status()
        return res.json()
