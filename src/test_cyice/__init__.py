import os
import sys
import logging
import ctypes
from ctypes.util import find_library
from pathlib import Path

if os.environ.get("CSPICE_LOGLEVEL"):
    logging.basicConfig(level=os.environ["CSPICE_LOGLEVEL"].upper())

logger = logging.getLogger(__name__)

# import the spice libray
from .utils import ctypes_cspice

# Import the compiled Cython extension
from .test_cyice import *



