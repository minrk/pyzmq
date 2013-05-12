# -*- coding: utf-8 -*-
"""Module holding utility and convenience functions for the event monitoring facility.
"""

#-----------------------------------------------------------------------------
#  Copyright (c) 2013 Guido Goldstein
#
#  This file is part of pyzmq
#
#  Distributed under the terms of the New BSD License.  The full license is in
#  the file COPYING.BSD, distributed as part of this software.
#-----------------------------------------------------------------------------

import struct
import zmq

def parse_monitor_message(msg):
    """Helper to parse event messages.
    
    Requires libzmq ≥ 3.3
    
    Event messages are always two frames:
    
    First frame is
      16 bit event id
      32 bit event value
    
    *NO padding*
    
    Second frame is endpoint as string
    
    Returns
    -------
    
    dict with keys:
    
    event: the event ID
    value: the event mask (match with ZMQ_EVENT_*)
    endpoint: the event endpoint (always defined, but empty if not applicable)
    """
    if (len(msg) != 2) or (len(msg[0]) != 6):
        raise ValueError("Invalid event message format: %s" % msg)
    ret = {}
    ret['event'], ret['value'] = struct.unpack("=hi", msg[0])
    ret['endpoint'] = msg[1].decode('ascii')
    return ret
