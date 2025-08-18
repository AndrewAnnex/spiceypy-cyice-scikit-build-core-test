import ctypes
import pytest
import test_cyice

def test_b1900_cython():
    # Call the Cython wrapper
    val = test_cyice.b1900()
    assert abs(val - -36525.0) < 1e-8  # expected CSPICE value

def test_b1900_ctypes():
    # Call directly from the bundled shared lib via ctypes
    lib = test_cyice.ctypes_cspice 
    lib.b1900.restype = ctypes.c_double
    val = lib.b1900()
    assert abs(val - -36525.0) < 1e-8

def test_consistency():
    # Ensure both approaches agree
    cython_val = test_cyice.b1900()
    lib = test_cyice.ctypes_cspice 
    lib.b1900.restype = ctypes.c_double
    ctypes_val = lib.b1900()
    assert abs(cython_val - ctypes_val) < 1e-12
