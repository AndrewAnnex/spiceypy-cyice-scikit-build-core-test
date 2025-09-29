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
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_9_API_VERSION


cdef extern from "SpiceUsr.h" nogil:
    ctypedef char SpiceChar
    ctypedef int SpiceInt
    ctypedef double SpiceDouble
    ctypedef const char ConstSpiceChar
    ctypedef const int ConstSpiceInt
    ctypedef const double ConstSpiceDouble

    # Bool
    ctypedef enum SpiceBoolean:
        SPICEFALSE = 0
        SPICETRUE  = 1
    # const SpiceBoolean
    ctypedef const SpiceBoolean ConstSpiceBoolean

    cdef SpiceDouble b1900_c()