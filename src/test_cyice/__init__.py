import sys
import ctypes
import importlib.resources
from pathlib import Path

# Import the compiled Cython extension
from .test_cyice import b1900

def _load_cspice():
    """Locate and load the bundled CSPICE shared library via ctypes."""
    if sys.platform.startswith("win"):
        libname = "cspice.dll"
    elif sys.platform == "darwin":
        libname = "libcspice.dylib"
    else:
        libname = "libcspice.so"

    try:
        with importlib.resources.path("test_cyice", libname) as libpath:
            return ctypes.CDLL(str(libpath))
    except FileNotFoundError as e:
        raise RuntimeError(f"Bundled CSPICE shared library not found: {libname}") from e

# # Expose a ctypes handle
ctypes_cspice = _load_cspice()
