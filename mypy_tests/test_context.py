import zmq

ctx = zmq.Context.instance()
s = ctx.socket(zmq.PUSH)
c = Context.instance()
c2 = zmq.sugar.Context.instance()
ctx = zmq.Context.instance()

ctx2 = zmq.Context()
ctx2.shadow_pyczmq(123)
s = ctx.socket(zmq.PUSH)
s.send(b"buf")
