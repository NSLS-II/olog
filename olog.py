from httpx import AsyncClient
import asyncio


__all__ = ['Client']


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
            return res.json()

    def put_logbooks(self, logbooks):
        return asyncio.run(self.aput_logbooks(logbooks))

    async def aput_logbook(self, logbook):
        async with self._session as api:
            name = logbook['name']
            res = await api.put(f'logbooks/{name}',  json=logbook)
            res.raise_for_status()
            return res.json()

    def put_logbook(self, logbook):
        return asyncio.run(self.aput_logbook(logbook))

    # Logs
    async def aget_logs(self, **params):
        async with self._session as api:
            res = await api.get('logs', params=params)
            res.raise_for_status()
            return res.json()

    def get_logs(self, **params):
        return asyncio.run(self.aget_logs(**params))

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
            return res.status_code

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
            return res.json()

    def put_tags(self, tags):
        return asyncio.run(self.aput_tags(tags))

    async def aput_tag(self, tag):
        async with self._session as api:
            name = tag['name']
            res = await api.put(f'tags/{name}',  json=tag)
            res.raise_for_status()
            return res.json()

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
            return res.json()

    def put_properties(self, properties):
        return asyncio.run(self.aput_properties(properties))

    async def aput_property(self, property):
        async with self._session as api:
            name = property['name']
            res = await api.put(f'properties/{name}',  json=property)
            res.raise_for_status()
            return res.json()

    def put_property(self, property):
        return asyncio.run(self.aput_property(property))
