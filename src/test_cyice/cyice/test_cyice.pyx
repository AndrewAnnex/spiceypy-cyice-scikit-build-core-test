# cython: language_level = 3
# cython: embedsignature = True
# cython: c_string_type = unicode
# cython: c_string_encoding = ascii
# cython: cdivision = True
# cython: profile = False
# cython: linetrace = False
# cython: warn.unused = True
# cython: warn.maybe_uninitialized = True
# cython: warn.multiple_declarators = True
# cython: show_performance_hints = True
# cython: always_allow_keywords = False
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_9_API_VERSION


from libc.stdlib cimport malloc, free
from libc.string cimport memcpy, strlen
from cython cimport boundscheck, wraparound, ufunc, memoryview
from cython.parallel import prange
from cpython.float cimport PyFloat_Check
from cpython.unicode cimport PyUnicode_DecodeUTF8
from cpython.bool       cimport PyBool_Check
from cpython.tuple      cimport PyTuple_GET_SIZE


import numpy as np
cimport numpy as np
np.import_array()

DEF _default_len_out = 256

DEF TIMELEN = 64

DEF SHORTLEN = 32
DEF EXPLAINLEN = 128
DEF LONGLEN = 2048
DEF TRACELEN = 256


from .test_cyice cimport *


def b1900():
    """
    Return the Julian Date corresponding to Besselian Date 1900.0.

    https://naif.jpl.nasa.gov/pub/naif/toolkit_docs/C/cspice/b1900_c.html

    :return: The Julian Date corresponding to Besselian Date 1900.0.
    """
    return b1900_c()