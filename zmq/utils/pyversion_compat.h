#include "Python.h"

// default to Python's own target Windows version(s)
// override by setting WINVER, _WIN32_WINNT, (maybe also NTDDI_VERSION?) macros
#ifdef Py_WINVER
  #ifndef WINVER
    #error "this should happen!"
    #define WINVER Py_WINVER
  #endif
  #ifndef _WIN32_WINNT
    #define _WIN32_WINNT Py_WINVER
  #endif
#endif


#if PY_VERSION_HEX < 0x02070000
    #define PyMemoryView_FromBuffer(info) (PyErr_SetString(PyExc_NotImplementedError, \
                    "new buffer interface is not available"), (PyObject *)NULL)
    #define PyMemoryView_FromObject(object)     (PyErr_SetString(PyExc_NotImplementedError, \
                                        "new buffer interface is not available"), (PyObject *)NULL)
#endif

#if PY_VERSION_HEX >= 0x03000000
    // for buffers
    #define Py_END_OF_BUFFER ((Py_ssize_t) 0)

    #define PyObject_CheckReadBuffer(object) (0)

    #define PyBuffer_FromMemory(ptr, s) (PyErr_SetString(PyExc_NotImplementedError, \
                            "old buffer interface is not available"), (PyObject *)NULL)
    #define PyBuffer_FromReadWriteMemory(ptr, s) (PyErr_SetString(PyExc_NotImplementedError, \
                            "old buffer interface is not available"), (PyObject *)NULL)
    #define PyBuffer_FromObject(object, offset, size)  (PyErr_SetString(PyExc_NotImplementedError, \
                            "old buffer interface is not available"), (PyObject *)NULL)
    #define PyBuffer_FromReadWriteObject(object, offset, size)  (PyErr_SetString(PyExc_NotImplementedError, \
                            "old buffer interface is not available"), (PyObject *)NULL)

#endif
