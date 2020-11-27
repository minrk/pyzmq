from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize

import numpy
import zmq

# print(f"library={zmq.get_library()}")
print(f"library_dirs={zmq.get_library_dirs()}")
print(f"includes={zmq.get_includes()}")

extensions = [
    Extension(
        "cyzmq_example",
        ["cyzmq.pyx"],
        include_dirs=zmq.get_includes() + [numpy.get_include()],
        # libraries=[zmq.get_library()],
        extra_objects=[zmq.get_bundled_libzmq()],
        library_dirs=zmq.get_library_dirs(),
    )
]
setup(name="cython-zmq-example", ext_modules=cythonize(extensions))
