import ctypes
import pytest
import test_cyice

def test_b1900_cython():
    # Call the Cython wrapper
    val = test_cyice.b1900()
    assert val == pytest.approx(2415020.31352)

def test_b1900_ctypes():
    # Call directly from the bundled shared lib via ctypes
    lib = test_cyice.ctypes_cspice 
    lib.b1900_c.restype = ctypes.c_double
    val = lib.b1900_c()
    assert val == pytest.approx(2415020.31352)

def test_consistency():
    # Ensure both approaches agree
    cython_val = test_cyice.b1900()
    lib = test_cyice.ctypes_cspice 
    lib.b1900_c.restype = ctypes.c_double
    ctypes_val = lib.b1900_c()
    assert abs(cython_val - ctypes_val) == pytest.approx(0)
