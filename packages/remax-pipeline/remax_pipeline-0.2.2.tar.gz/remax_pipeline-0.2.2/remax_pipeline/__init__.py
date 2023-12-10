from . import _version

__version__ = _version.get_versions()["version"]


from .db import initialize_database