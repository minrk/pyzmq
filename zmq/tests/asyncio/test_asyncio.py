"""Test asyncio support"""

try:
    from ._test_asyncio import TestAsyncIOSocket, TestAsyncioAuthentication # noqa
except SyntaxError:
    pass
