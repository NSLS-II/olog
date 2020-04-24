from datetime import datetime
import requests
import requests.auth


__all__ = ['Client']

headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}


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
        url = f'{self._url}/logbooks'
        res = self._session.get(url, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def get_logbook(self, name):
        # Logbooks have an integer id, but this REST endpoint expects the
        # *name*.  It does not accept an id.
        url = f'{self._url}/logbooks/{name}'
        res = self._session.get(url, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def delete_logbook(self, name):
        # Logbooks have an integer id, but this REST endpoint expects the
        # *name*.  It does not accept an id.
        url = f'{self._url}/logbooks/{name}'
        res = self._session.delete(url, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def post_logbook(self, logbook):
        """
        Create a logbook.
        """
        url = f'{self._url}/logbooks'
        res = self._session.post(url, data=logbook, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def put_logbook(self, logbook):
        """
        Create or update a logbook (mathced by name).
        """
        url = f'{self._url}/logbooks/{logbook["name"]}'
        res = self._session.put(url, json=logbook)
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
        url = f'{self._url}/logs'
        res = self._session.get(url, params=params, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def get_log(self, id):
        url = f'{self._url}/logs/{id}'
        res = self._session.get(url, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def put_log(self, log):
        """
        Create or update a log (mathced by name).
        """
        url = f'{self._url}/logs'
        res = self._session.put(url, json=log, **self._kwargs)
        res.raise_for_status()
        return res.json()

    def attach(self, filename, logid):
        """
        Attach a file to a log with a specified logid.
        """
        import mimetypes

        import requests
        from requests_toolbelt.multipart.encoder import MultipartEncoder

        m = MultipartEncoder(
                    fields={'file': open(filename, 'rb'),
                            'filename': filename,
                            'fileMetadataDescription': 'text/plain',
                            }
                        )

        files = {'file': (filename,
                          open(filename, 'rb'),
                          mimetypes.guess_type(filename)[0],
                          )}
        # res = self._session.post(url, files=files, **self._kwargs)
        # data = {'file': open(filename, 'rb'),
        #         'filename': filename,
        #         'fileMetadataDescription': 'text/plain',
        #         }

        url = f'{self._url}/logs/attachments/{logid}'
        kwargs = self._kwargs
        headers = kwargs['headers']
        kwargs.pop('headers')
        print(kwargs)
        headers.update({'Content-Type': 'multipart/form-data'})
        files = {filename: open(filename, 'rb')}

        res = self._session.post(url, files=files, headers=headers, **kwargs)
        res.raise_for_status()

        return res.json()
