# pylint: disable=unused-import
import os

# support DVCX_ aliases for DQL_ env vars
for key in list(os.environ.keys()):
    if key.startswith("DVCX_"):
        dql_key = f"DQL_{key[5:]}"
        os.environ.setdefault(dql_key, os.environ[key])

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "UNKNOWN"
