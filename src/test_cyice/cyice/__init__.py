try:
    from ..utils import ctypes_cspice
except ImportError:  # fallback if executed outside package context
    from test_cyice.utils import ctypes_cspice

from .test_cyice import *