"""
    Implementation of multiformat protocols, according to the `Multiformats <https://multiformats.io/>`_ specifications.

    Suggested usage:

    >>> from multiformats import *

    The above will import the following names:

    .. code-block:: python

        varint, multicodec, multibase, multihash, multiaddr, CID

    The first five are modules implementing homonymous specifications,
    while :class:`~multiformats.cid.CID` is a class for Content IDentifiers.
"""

__version__ = "0.2.1"

from . import multiaddr, multibase, multicodec, multihash, varint
from .cid import CID

__all__ = [
    "varint",
    "multicodec",
    "multibase",
    "multihash",
    "multiaddr",
    "CID",
]
