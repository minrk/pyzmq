"""ZAP Authenticator integrated with the asyncio IO loop.

.. versionadded:: 15.2
"""

# Copyright (C) PyZMQ Developers
# Distributed under the terms of the Modified BSD License.

import asyncio
import warnings
from typing import Any, Optional

import zmq
from zmq.asyncio import Poller

from .base import Authenticator


class AsyncioAuthenticator(Authenticator):
    """ZAP authentication for use in the asyncio IO loop"""

    __poller: Optional[Poller]
    __task: Any
    _async_socket: Optional["zmq.asyncio.Socket"]

    def __init__(
        self,
        context: Optional["zmq.Context"] = None,
        loop: Any = None,
        encoding: str = 'utf-8',
        log: Any = None,
    ):
        super().__init__(context, encoding, log)
        if loop is not None:
            warnings.warn(
                f"{self.__class__.__name__}(loop) is deprecated and ignored",
                DeprecationWarning,
                stacklevel=2,
            )
        self.__poller = None
        self.__task = None

    async def __handle_zap(self) -> None:
        while self.__poller is not None:
            events = await self.__poller.poll(timeout=100)
            if self._async_socket and self._async_socket in dict(events):
                msg = self.zap_socket.recv_multipart()
                await self.handle_zap_message(msg)
                # we just used the underlying zap_socket
                # we need to poke the async wrapper to ensure events
                # are handled
                self._async_socket._schedule_remaining_events()
            else:
                self.log.debug("nothing to handle")

    def start(self) -> None:
        """Start ZAP authentication"""
        super().start()
        self._async_socket = zmq.asyncio.Socket.from_socket(self.zap_socket)
        self.__poller = Poller()
        self.__poller.register(self._async_socket, zmq.POLLIN)
        self.__task = asyncio.ensure_future(self.__handle_zap())

    def stop(self) -> None:
        """Stop ZAP authentication"""
        if self.__task:
            self.log.info("Canceling task!")
            self.__task.cancel()
        if self.__poller and self._async_socket:
            self.__poller.unregister(self._async_socket)
            self.__poller = None
            self._async_socket.close()
            self._async_socket = None
            # accessing .closed ensures the object knows it's closed
            # and doesn't re-raise on garbage collection
            # assert self.zap_socket.closed
            self.zap_socket = None  # type: ignore
        super().stop()


__all__ = ["AsyncioAuthenticator"]
