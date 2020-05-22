import asyncio
from collections import OrderedDict
from datetime import datetime

from httpx import AsyncClient

__all__ = ['Client']


def ensure_time(time):
    if isinstance(time, datetime):
        return time.isoformat(sep=' ', timespec='milliseconds')
    else:
        d = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
        return d.isoformat(sep=' ', timespec='milliseconds')


class Client:
    def __init__(self, url, user, password):
        """
        url : string
            base URL, such as ``'https://some_host:port/Olog'``
        user : string
        password : string
        """
        if not url.endswith('/'):
            url += '/'
        self._session = AsyncClient(base_url=url, auth=(user, password))

    # Logbooks
    async def aget_logbooks(self):
        async with self._session as api:
            res = await api.get('logbooks')
        res.raise_for_status()
        return res.json()

    def get_logbooks(self):
        return asyncio.run(self.aget_logbooks())

    async def aget_logbook(self, name):
        # Logbooks have an integer id, but this REST endpoint expects the
        # *name*.  It does not accept an id.
        async with self._session as api:
            res = await api.get(f'logbooks/{name}')
        res.raise_for_status()
        return res.json()

    def get_logbook(self, name):
        return asyncio.run(self.aget_logbook(name))

    async def aput_logbooks(self, logbooks):
        async with self._session as api:
            res = await api.put('logbooks', json=logbooks)
        res.raise_for_status()

    def put_logbooks(self, logbooks):
        return asyncio.run(self.aput_logbooks(logbooks))

    async def aput_logbook(self, logbook):
        async with self._session as api:
            res = await api.put(f'logbooks/{logbook["name"]}',  json=logbook)
            logbook_from_server = res.json()
            logbook_from_server.pop('owner')
            logbook.pop('owner')
        if (not res.raise_for_status()) and (logbook != logbook_from_server):
            raise ValueError("No http error was raised but server doesn't \
                             successfully put logbook you want")

    def put_logbook(self, logbook):
        return asyncio.run(self.aput_logbook(logbook))

    # Logs

    async def aget_logs(self, desc=None, fuzzy=None, phrase=None, owner=None,
                        start=None, end=None, includeevents=None,
                        logbooks=None, tags=None, properties=None):
        if start is not None:
            start = ensure_time(start)
        if end is not None:
            end = ensure_time(end)
        params = dict(desc=desc, fuzzy=fuzzy, phrase=phrase, owner=owner,
                      start=start, end=end, includeevents=includeevents,
                      logbooks=logbooks, tags=tags, properties=properties)
        params = {k: v for k, v in params.items() if v is not None}
        async with self._session as api:
            res = await api.get('logs', params=params)
        res.raise_for_status()
        return res.json()

    def get_logs(self, desc=None, fuzzy=None, phrase=None, owner=None,
                 start=None, end=None, includeevents=None,
                 logbooks=None, tags=None, properties=None):
        """
        desc : a list of str
            A list of keywords which are present in the log entry description

        fuzzy : str
            Allow fuzzy searches

        phrase: str
            Finds log entries with the exact same word/s

        owner: str
            Finds log entries with the given owner

        start : class 'datetime.datetime'
            Search for log entries created after given time instant

        end : class 'datetime.datetime'
            Search for log entries created before the given time instant

        includeevents : class 'datetime.datetime'
            A flag to include log event times when

        tags : str
            Search for log entries with at least one of the given tags

        logbooks : str
            Search for log entries with at least one of the given logbooks
        """
        return asyncio.run(self.aget_logs(desc, fuzzy, phrase, owner,
                                          start, end, includeevents,
                                          logbooks, tags))

    async def aget_log(self, id):
        async with self._session as api:
            res = await api.get(f'logs/{id}')
        res.raise_for_status()
        return res.json()

    def get_log(self, id):
        return asyncio.run(self.aget_log(id))

    # Attachments
    async def aget_attachment(self, id, filename):
        async with self._session as api:
            res = await api.get(f'logs/attachments/{id}/{filename}')
        return res.content

    def get_attachment(self, id, filename):
        return asyncio.run(self.aget_attachment(id, filename))

    async def apost_attachment(self, id, files):
        async with self._session as api:
            res = await api.post(f'logs/attachments/{id}', files=files)
        res.raise_for_status()

    def post_attachment(self, id, files):
        return asyncio.run(self.apost_attachment(id, files))

    # Tags
    async def aget_tags(self):
        async with self._session as api:
            res = await api.get('tags')
        res.raise_for_status()
        return res.json()

    def get_tags(self):
        return asyncio.run(self.aget_tags())

    async def aget_tag(self, name):
        async with self._session as api:
            res = await api.get(f'tags/{name}')
        res.raise_for_status()
        return res.json()

    def get_tag(self, name):
        return asyncio.run(self.aget_tag(name))

    async def aput_tags(self, tags):
        async with self._session as api:
            res = await api.put('tags', json=tags)
        res.raise_for_status()

    def put_tags(self, tags):
        return asyncio.run(self.aput_tags(tags))

    async def aput_tag(self, tag):
        async with self._session as api:
            res = await api.put(f'tags/{tag["name"]}',  json=tag)
        if (not res.raise_for_status()) and (tag != res.json()):
            raise ValueError("No http error was raised \
                             but server doesn't successfully put tag you want")

    def put_tag(self, tag):
        return asyncio.run(self.aput_tag(tag))

    # Properties
    async def aget_properties(self):
        async with self._session as api:
            res = await api.get('properties')
        res.raise_for_status()
        return res.json()

    def get_properties(self):
        return asyncio.run(self.aget_properties())

    async def aget_property(self, name):
        async with self._session as api:
            res = await api.get(f'properties/{name}')
        res.raise_for_status()
        return res.json()

    def get_property(self, name):
        return asyncio.run(self.aget_property(name))

    async def aput_properties(self, properties):
        async with self._session as api:
            res = await api.put('properties', json=properties)
        res.raise_for_status()

    def put_properties(self, properties):
        return asyncio.run(self.aput_properties(properties))

    async def aput_property(self, property):
        async with self._session as api:
            res = await api.put(f'properties/{property["name"]}',
                                json=property)
            property_from_server = res.json()
            property_from_server.pop('owner')
            property.pop('owner')
            property['attributes'] = sorted(property['attributes'],
                                            key=lambda d: d['name'])
        if (not res.raise_for_status()) and \
           (OrderedDict(property) != property_from_server):
            raise ValueError("No http error was raised but server \
                             doesn't successfully put property you want")

    def put_property(self, property):
        return asyncio.run(self.aput_property(property))
