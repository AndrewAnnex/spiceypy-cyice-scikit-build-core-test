import sys
import ctypes
import importlib.resources
from pathlib import Path

# Import the compiled Cython extension
from .test_cyice import b1900

def _load_cspice():
    """Locate and load the bundled CSPICE shared library via ctypes."""
    match sys.platform:
        case p if p.startswith("win"):
            libname = "cspice.dll"
        case "darwin":
            libname = "libcspice.dylib"
        case "emscripten":
            libname = "libcspice.wasm"
        case _:
            libname = "libcspice.so"
    try:
            libpath = Path(__file__).parent / libname
            if not libpath.exists():
                    raise RuntimeError(f"Bundled CSPICE shared library not found: {libname}")
            return ctypes.CDLL(str(libpath))

    except FileNotFoundError as e:
        raise RuntimeError(f"Bundled CSPICE shared library not found: {libname}") from e

# # Expose a ctypes handle
ctypes_cspice = _load_cspice()
