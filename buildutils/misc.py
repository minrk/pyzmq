"""Detect zmq version"""
#-----------------------------------------------------------------------------
#  Copyright (C) 2012 Min Ragan-Kelley
#
#  This file is part of pyzmq
#
#  Distributed under the terms of the New BSD License.  The full license is in
#  the file COPYING.BSD, distributed as part of this software.
#-----------------------------------------------------------------------------

def customize_mingw(cc):
    # strip -mno-cygwin from mingw32 ()
    for cmd in [cc.compiler, cc.compiler_cxx, cc.compiler_so]:
        if '-mno-cygwin' in cmd:
            cmd.remove('-mno-cygwin')

__all__ = ['customize_mingw']