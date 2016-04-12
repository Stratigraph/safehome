
from . import _md5 as md5
from tablib import formats

formats.available += (md5,)
