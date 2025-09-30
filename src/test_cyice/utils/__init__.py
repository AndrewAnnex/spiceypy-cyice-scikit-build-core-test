import os
import sys
import logging
import ctypes
from ctypes.util import find_library
from pathlib import Path

if os.environ.get("CSPICE_LOGLEVEL"):
    logging.basicConfig(level=os.environ["CSPICE_LOGLEVEL"].upper())

logger = logging.getLogger(__name__)


def load_cspice():
    """
    Load the CSPICE shared library with priority:
      1. Explicit environment override (CSPICE_SHARED_LIB).
      2. System/conda install (via ctypes.util.find_library).
      3. Fallback to library file in the same folder as this script.

    Notes:
        - If the shared library is missing or corrupted, raises RuntimeError.
    """

    def _try_load(path: str, desc: str):
        try:
            return ctypes.CDLL(path, mode=ctypes.RTLD_GLOBAL)
        except OSError as e:
            logger.debug(f"Failed to load CSPICE {desc} at {path}: {e}")
            return None

    # 1. User override
    override = os.environ.get("CSPICE_SHARED_LIB")
    if override:
        logger.info(f"Using override from CSPICE_SHARED_LIB: {override}")
        lib = _try_load(override, "override")
        if lib:
            return lib

    # 2. System/conda install
    libpath = find_library("cspice")
    if libpath:
        logger.info(f"Using system/conda library via find_library: {libpath}")
        lib = _try_load(libpath, "system/conda")
        if lib:
            return lib
    else:
        logger.debug("find_library('cspice') returned None")

    # 3. Fallback per host
    match sys.platform:
        case p if p.startswith("win"):
            shared_name = "cspice.dll"
        case "darwin":
            shared_name = "libcspice.dylib"
        case "emscripten":
            shared_name = "libcspice.wasm"
        case _:
            shared_name = "libcspice.so"

    relpath = Path(__file__).resolve().parent / shared_name
    if relpath.exists():
        logger.info(f"Using fallback library next to module: {relpath}")
        lib = _try_load(str(relpath), "fallback")
        if lib:
            return lib

    msg = (
        "Could not locate or load CSPICE shared library. "
        "Set CSPICE_SHARED_LIB to override detection."
    )
    logger.error(msg)
    raise RuntimeError(msg)

# usage
ctypes_cspice = load_cspice()