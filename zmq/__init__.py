"""Python bindings for 0MQ."""

# Copyright (C) PyZMQ Developers
# Distributed under the terms of the Modified BSD License.

# load bundled libzmq, if there is one:

def _load_libzmq():
    """load bundled libzmq if there is one"""
    import sys, platform, os

    dlopen = hasattr(sys, 'getdlopenflags')  # unix-only
    # RTLD flags are added to os in Python 3
    # get values from os because ctypes values are WRONG on pypy
    PYPY = platform.python_implementation().lower() == 'pypy'

    if dlopen:
        import ctypes

        dlflags = sys.getdlopenflags()
        # set RTLD_GLOBAL, unset RTLD_LOCAL
        flags = ctypes.RTLD_GLOBAL | dlflags
        # ctypes.RTLD_LOCAL is 0 on pypy, which is *wrong*
        flags &= ~getattr(os, 'RTLD_LOCAL', 4)
        # pypy on darwin needs RTLD_LAZY for some reason
        if PYPY and sys.platform == 'darwin':
            flags |= getattr(os, 'RTLD_LAZY', 1)
            flags &= ~getattr(os, 'RTLD_NOW', 2)
        sys.setdlopenflags(flags)
    try:
        from . import libzmq
    except ImportError:
        # raise on failure to load if libzmq is present
        from importlib.util import find_spec

        if find_spec(".libzmq", "zmq"):
            # found libzmq, but failed to load it!
            # raise instead of silently moving on
            raise
    else:
        # store libzmq as zmq._libzmq for backward-compat
        globals()['_libzmq'] = libzmq
        if PYPY:
            # should already have been imported above, so reimporting is as cheap as checking
            import ctypes

            # some versions of pypy (5.3 < ? < 5.8) needs explicit CDLL load for some reason,
            # otherwise symbols won't be globally available
            # do this unconditionally because it should be harmless (?)
            ctypes.CDLL(libzmq.__file__, ctypes.RTLD_GLOBAL)
    finally:
        if dlopen:
            sys.setdlopenflags(dlflags)


_load_libzmq()


# zmq top-level imports

from zmq import backend
from zmq.backend import *
from zmq import sugar
from zmq.sugar import *


def get_includes():
    """Return a list of directories to include for linking against pyzmq with cython."""
    from os.path import join, dirname, abspath, pardir, exists

    base = dirname(__file__)
    parent = abspath(join(base, pardir))
    includes = [parent] + [join(parent, base, subdir) for subdir in ('utils',)]
    if exists(join(parent, base, 'include')):
        includes.append(join(parent, base, 'include'))
    return includes


def get_library_dirs():
    """Return a list of directories used to link against pyzmq's bundled libzmq."""
    from os.path import join, dirname, abspath, pardir, exists

    base = dirname(__file__)
    parent = abspath(join(base, pardir))
    lib_dirs = [join(parent, base)]
    # include auditwheel/delocate bundle dirs
    for lib_subdir in ["pyzmq.libs", ".libs", ".dylibs"]:
        lib_dir = join(base, lib_subdir)
        if exists(lib_dir):
            lib_dirs.append(lib_dir)
    return lib_dirs


def get_bundled_libzmq():
    """Return the library name of libzmq to link against

    If libzmq is bundled, a full path will be given
    """
    import glob
    import os

    # if libzmq is bundled as an Extension,
    # return its full path
    try:
        return libzmq.__file__
    except NameError:
        pass

    # find bundled libzmq
    # e.g. .libs/libzmq-abc123.so.5
    # or .dylibs/libzmq.5.dylib
    for d in get_library_dirs():
        for blob in ("libzmq*.so*", "libzmq*.dylib"):
            matches = glob.glob(os.path.join(d, blob))
            if matches:
                return matches[0]
                return f":{os.path.basename(matches[0])}"

    if os.name == "nt":
        return "libzmq"
    else:
        return "zmq"


COPY_THRESHOLD = 65536
__all__ = ['get_includes', 'get_library_dirs', 'get_library', 'COPY_THRESHOLD'] + sugar.__all__ + backend.__all__
