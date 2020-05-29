from ._version import get_versions
from .httpx_client import Client

__all__ = ['Client']


__version__ = get_versions()['version']
del get_versions
