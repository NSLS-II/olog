import asyncio

from httpx import AsyncClient

from .util import (UncaughtServerError, ensure_name, ensure_time,
                   simplify_attr, simplify_logbook)


class Client:
    def __init__(self, url, user, password):
        '''A Python client of olog service

        Parameters
        ----------
        url : str
            base URL, such as ``'https://some_host:port/Olog'``
        user : string
            Your olog service username
        password : str
            Your olog service password
        '''
        if not url.endswith('/'):
            url += '/'
        self.user = user
        self._session = AsyncClient(base_url=url, auth=(self.user, password))

    # Logbooks
    async def aget_logbooks(self):
        async with self._session as api:
            res = await api.get('logbooks')
        res.raise_for_status()
        logbooks = list()
        for i in res.json():
            logbooks.append(simplify_logbook(i))
        return logbooks

    def get_logbooks(self):
        '''
        Returns
        -------
        logbooks : list
            Each element is a logbook dict.

        Examples
        --------
        >>>cli.get_logbooks()
        [{'DAMA': {'owner': 'olog-logs', 'state': 'Active'}},
         {'Operations': {'owner': 'olog-logs', 'state': 'Active'}}]

        '''
        return asyncio.run(self.aget_logbooks())

    async def aget_logbook(self, name):
        # Logbooks have an integer id, but this REST endpoint expects the
        # *name*.  It does not accept an id.
        async with self._session as api:
            res = await api.get(f'logbooks/{name}')
        res.raise_for_status()
        return simplify_logbook(res.json())

    def get_logbook(self, name):
        '''
        Parameters
        ----------
        name : str
            name of logbook

        Returns
        -------
        logbook : dict
            Each element is a logbook dict.

        Examples
        --------
        >>>cli.get_logbook("TEST')
        {'TEST': {'owner': 'olog-logs', 'state': 'Active'}}

        '''
        return asyncio.run(self.aget_logbook(name))

    async def aput_logbooks(self, names):
        logbooks = [{'name': name, 'owner': self.user} for name in names]
        async with self._session as api:
            res = await api.put('logbooks', json=logbooks)
        res.raise_for_status()

    def put_logbooks(self, logbooks):
        '''
        Parameters
        ----------
        logbooks : list
            Each element is a str of logbook name.

        Examples
        --------
        >>>cli.put_logbooks(['TEST0', 'TEST1'])

        '''
        return asyncio.run(self.aput_logbooks(logbooks))

    async def aput_logbook(self, name):
        logbook = {'name': name, 'owner': self.user}
        async with self._session as api:
            res = await api.put(f'logbooks/name',  json=logbook)
        res.raise_for_status()
        # The server returned OK. Its response contains a copy of what it
        # inserted into its database. We can compare it with our submission for
        # extra verification that everything worked correctly.
        logbook_from_server = res.json()
        logbook_from_server.pop('state')
        if logbook != logbook_from_server:
            raise UncaughtServerError(f"No http error was raised but server \
                                      doesn't successfully put logbook you \
                                      want. Server put {res.json()} while you \
                                      are tring to put {logbook}.")
        return simplify_logbook(res.json())

    def put_logbook(self, name):
        '''
        Parameters
        ----------
        logbook : str
            logbook name.

        Returns
        -------
        logbook : dict
            A dict map logbook name to a nested dict of owner and state informations.

        Examples
        --------
        >>>cli.put_logbook('TEST')
        {'TEST': {'owner': 'admin', 'state': 'Active'}}

        '''
        return asyncio.run(self.aput_logbook(name))

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

    def get_logs(self, *, desc=None, fuzzy=None, phrase=None, owner=None,
                 start=None, end=None, includeevents=None,
                 logbooks=None, tags=None, properties=None):
        '''
        Parameters
        ----------
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

        Returns
        -------
        logs : list of logs

        Examples
        --------
        >>>cli.get_logs(logbooks='Operations')
        '''
        return asyncio.run(self.aget_logs(desc, fuzzy, phrase, owner,
                                          start, end, includeevents,
                                          logbooks, tags))

    async def aget_log(self, id):
        async with self._session as api:
            res = await api.get(f'logs/{id}')
        res.raise_for_status()
        return res.json()

    def get_log(self, id):
        '''
        Parameters
        ----------
        id : int
            id number of log

        Returns
        -------
        log : dict

        Examples
        --------
        >>>cli.get_log(1)
        '''
        return asyncio.run(self.aget_log(id))

    # Attachments
    async def aget_attachment(self, id, filename):
        async with self._session as api:
            res = await api.get(f'logs/attachments/{id}/{filename}')
        return res.content

    def get_attachment(self, id, filename):
        '''Get attachemnt file based on log id and filename

        Parameters
        ----------
        id : int
            id number of log
        filename : str
            name of file

        Returns
        -------
        content : content of httpx return

        Examples
        --------
        >>>cli.get_attachment(1, 'test')
        '''
        return asyncio.run(self.aget_attachment(id, filename))

    async def apost_attachment(self, id, files):
        async with self._session as api:
            res = await api.post(f'logs/attachments/{id}', files=files)
        res.raise_for_status()

    def post_attachment(self, id, files):
        '''
        Parameters
        ----------
        id : int
            id number of log
        files : dict
            files dictionary including filename, file obj and meta data.

        Examples
        --------
        >>> files = {'file': open('<FILE>','rb'), 'filename': (None, '<FILENAME>'),
        'fileMetadataDescription': (None, 'This is a attachment file')}
        >>>cli.post_attachment(3, files)
        '''
        return asyncio.run(self.apost_attachment(id, files))

    # Tags
    async def aget_tags(self):
        async with self._session as api:
            res = await api.get('tags')
        res.raise_for_status()
        return res.json()

    def get_tags(self):
        '''
        Returns
        -------
        tags : list
            A list of tag dict

        Examples
        --------
        >>>cli.get_tags()
        '''
        return asyncio.run(self.aget_tags())

    async def aget_tag(self, name):
        async with self._session as api:
            res = await api.get(f'tags/{name}')
        res.raise_for_status()
        return res.json()

    def get_tag(self, name):
        '''
        Parameters
        ----------
        name : str
            Name of tag.

        Returns
        -------
        tag : dict
            A tag dict.

        Examples
        --------
        >>>cli.get_tag('TEST')
        '''
        return asyncio.run(self.aget_tag(name))

    async def aput_tags(self, names):
        async with self._session as api:
            res = await api.put('tags', json=[{'name': n} for n in names])
        res.raise_for_status()

    def put_tags(self, names):
        '''
        Parameters
        ----------

        names : list
            List of names

        Examples
        --------
        >>>cli.put_tags(['TEST0', 'TEST1'])
        '''
        return asyncio.run(self.aput_tags(names))

    async def aput_tag(self, name):
        async with self._session as api:
            res = await api.put(f'tags/{name}', json={'name': name})
        res.raise_for_status()
        return res.json()

    def put_tag(self, name):
        '''
        Parameters
        ----------
        name : str
            Name of tag

        Returns
        -------
        tag : dict
            The tag dict with automatically added state

        Examples
        --------
        >>>cli.put_tag('TEST')
        {'name': 'TEST1', 'state': 'Active'}
        '''
        return asyncio.run(self.aput_tag(name))

    # Properties
    async def aget_properties(self):
        async with self._session as api:
            res = await api.get('properties')
        res.raise_for_status()
        properties = list()
        for i in res.json():
            properties.append(simplify_attr(i))
        return properties

    def get_properties(self):
        '''
        Returns
        -------
        properties : list
            A list of property dict

        Examples
        --------
        >>>cli.get_properties()
        '''
        return asyncio.run(self.aget_properties())

    async def aget_property(self, name):
        async with self._session as api:
            res = await api.get(f'properties/{name}')
        res.raise_for_status()
        return simplify_attr(res.json())

    def get_property(self, name):
        '''
        Parameters
        ----------
        name : str
            Name of property.

        Returns
        -------
        property : dict
            A property dict.

        Examples
        --------
        >>>cli.get_property('TEST')
        '''
        return asyncio.run(self.aget_property(name))

    async def aput_properties(self, named_attributes):
        properties = list()
        for name, attributes in named_attributes.items():
            attr_value = [{'name': ensure_name(name), 'value': value} for name, value in attributes.items()]
            properties.append(dict({'name': name,
                                    'owner': self.user,
                                    'attributes': attr_value}))
        async with self._session as api:
            res = await api.put('properties', json=properties)
        res.raise_for_status()

    def put_properties(self, named_attributes):
        '''
        Parameters
        ----------

        named_attributes : dict
            Each element is a pair of {<name>: <attributes>, ...}. <attributes> is dict
            of <key: value> pair.

        Examples
        --------
        >>>cli.put_properties({'TEST0': {'id': None, 'url': None}, 'TEST1':{'id': None, 'url': None}})
        '''
        return asyncio.run(self.aput_properties(named_attributes))

    async def aput_property(self, name, attributes):
        name = ensure_name(name)
        monitor_list = [name for name, value in attributes.items()
                        if isinstance(value, int) or isinstance(value, float)]
        print('monitor_list')
        print(monitor_list)
        attr_value = [{'name': ensure_name(name), 'value': value} for name, value in attributes.items()]
        property = dict({'name': name,
                         'owner': self.user,
                         'attributes': attr_value})
        async with self._session as api:
            res = await api.put(f'properties/{property["name"]}',
                                json=property)
        res.raise_for_status()
        # The server returned OK. Its response contains a copy of what it
        # inserted into its database. We can compare it with our submission for
        # extra verification that everything worked correctly.
        property_from_server = res.json()
        property_cp = property.copy()
        for e in property_from_server['attributes']:
            e.pop('state')
        property_from_server.pop('state')
        # property_cp['attributes'] = sorted(property_cp['attributes'], key=lambda d: d['name'])
        # Looks server doesn't return sorted attributes
        for i in property_cp['attributes']:
            if i['name'] in monitor_list:
                i['value'] = str(i['value'])
        if property_cp != property_from_server:
            raise UncaughtServerError("No http error was raised but server doesn't successfully put property" \
                                      f"you want.Server puts {property_from_server} while you are tring to put" \
                                      f"{property_cp}.")
        return simplify_attr(res.json())

    def put_property(self, name, attributes):
        '''
        Parameters
        ----------
        name : str
            Name of property
        attributes : dict
            Mappings of name to value.

        Returns
        -------
        property : dict
            The property dict with automatically added state and owner.

        Examples
        --------
        >>>cli.put_property('TEST', {'id': 1, 'url': None})
        '''
        return asyncio.run(self.aput_property(name, attributes))
