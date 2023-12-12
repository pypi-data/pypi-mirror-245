"""Gear testing suite and utilities"""
import logging

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

try:
    import unittest # noqa: F401

    import pytest # noqa: F401
except (ImportError, ModuleNotFoundError):
    raise RuntimeError("Need to have pytest and unittest installed to use this module.")

from .files import *
from .gears import *
from .hierarchy import *
from .sdk import *
from .utils import *
