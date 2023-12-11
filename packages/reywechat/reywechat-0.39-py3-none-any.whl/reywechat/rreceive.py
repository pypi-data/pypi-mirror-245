# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-26 11:18:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Receive methods.
"""


from __future__ import annotations
from typing import Any, List, Optional, Callable, Union
from os.path import (
    abspath as os_abspath,
    exists as os_exists,
    join as os_join
)
from queue import Queue
from socket import socket
from json import loads as josn_loads
from reytool.rcomm import listen_socket
from reytool.ros import RFile, RFolder
from reytool.rtime import sleep
from reytool.rwrap import wrap_thread, wrap_wait, wrap_exc
from reytool.rmultitask import RThreadPool

from .rwechat import RWeChat


__all__ = (
    "RReceive",
)


Message = {
}

callback_host = "127.0.0.1"
callback_port = 19089


# class RReceive_(object):
#     """
#     Rey's `receive` type.
#     """


#     def __init__(
#         self,
#         rwechat: RWeChat,
#         max_receiver: int,
#         timeout : Optional[float]
#     ) -> None:
#         """
#         Build `receive` instance.

#         Parameters
#         ----------
#         rwechat : `RClient` instance.
#         max_receiver : Maximum number of receivers.
#         timeout : File receive timeout seconds.
#             - `None` : Infinite time.
#             - `float` : Use this value.
#         """

#         # Set attribute.
#         self.rwechat = rwechat
#         self.timeout = timeout
#         self.handlers: List[Callable[[MsgParams], Any]] = []
#         self.queue: Queue[MsgParams] = Queue()
#         self.started: Optional[bool] = False
#         self.cache_path = os_abspath("cache")

#         # Receiver.
#         self._create_receiver(max_receiver)

#         # Add handler.
#         self.handlers.append(self.handler_file)
#         self.handlers.append(self.rwechat.rlog.handler_log_receive)


#     @wrap_thread
#     def _create_receiver(
#         self,
#         max_receiver: int
#     ) -> None:
#         """
#         Create receiver, it will get message parameters from receive queue, and handle.

#         Parameters
#         ----------
#         max_receiver : Maximum number of receivers.
#         """


#         # Define.
#         def handlers(message: MsgParams) -> None:
#             """
#             Handlers.

#             Parameters
#             ----------
#             message : Message parameters.
#             """

#             # Handle.
#             for handler in self.handlers:
#                 wrap_exc(
#                     handler,
#                     message,
#                     _handler=self.rwechat.rlog.rrlog.log
#                 )

#             ## Put.
#             self.queue.put(message)


#         # Thread pool.
#         thread_pool = RThreadPool(
#             handlers,
#             _max_workers=max_receiver
#         )

#         # Loop.
#         while True:

#             ## Stop.
#             if self.started is False:
#                 sleep(0.1)
#                 continue

#             ## End.
#             elif self.started is None:
#                 break

#             ## Submit.
#             message = self.rwechat.rclient.receive()
#             thread_pool(message)


#     def handler_file(self, message: MsgParams) -> None:
#         """
#         File handler, decrypt image, and add file path attribute to message instance.

#         Parameters
#         ----------
#         message : Message parameters.
#         """


#         # Get file path.

#         ## Image.
#         if message["type"] == 3:
#             file_path = message["thumbnail"]

#         ## Video.
#         elif message["type"] == 43:
#             file_path = message["thumbnail"]

#         ## File.
#         elif message["type"] == 49:
#             file_path = message["extra"]

#         ## Other.
#         else:
#             return

#         # Wait.
#         wrap_wait(
#             os_exists,
#             file_path,
#             _interval = 0.05,
#             _timeout=self.timeout
#         )

#         # Decrypt.
#         rfile = RFile(file_path)
#         if rfile.suffix == ".dat":
#             file_name = str(message["uuid"])
#             save_path = os_join(self.cache_path, file_name)

#             ## Decrypt.
#             success = self.rwechat.rclient.client.decrypt_image(file_path, save_path)
#             if not success:
#                 raise AssertionError("image file decrypt fail")

#             ## Get path.
#             pattern = "^%s." % file_name
#             rfolder = RFolder(self.cache_path)
#             file_path = rfolder.search(pattern)

#         # Set attribute
#         message["file"] = file_path


#     def start(self) -> None:
#         """
#         Start receiver.
#         """

#         # Start.
#         self.started = True


#     def stop(self) -> None:
#         """
#         Stop receiver.
#         """

#         # Stop.
#         self.started = False


#     def end(self) -> None:
#         """
#         End receiver.
#         """

#         # End.
#         self.started = None


#     def add_handler(
#         self,
#         method: Callable[[MsgParams], Any]
#     ) -> None:
#         """
#         Add method message handler.

#         Parameters
#         ----------
#         method : Handle method, enter parameter is the message parameters.
#         """

#         # Add.
#         self.handlers.append(method)


#     def receive(
#         self,
#         timeout: Optional[float] = None
#     ) -> MsgParams:
#         """
#         Receive one message.

#         Parameters
#         ----------
#         timeout : Number of timeout seconds.

#         Returns
#         -------
#         Message parameters.
#         """

#         # Receive.
#         message: MsgParams = self.queue.get(timeout=timeout)

#         return message


#     __del__ = receive


#     __del__ = end


class RReceive(object):
    """
    Rey's `receive` type.
    """


    def __init__(
        self,
        rwechat: RWeChat
    ) -> None:
        """
        Build `receive` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.queue: Queue[bytes] = Queue()
        self.handlers: List[Callable[[Message], Any]] = []


    @wrap_thread
    def _start_callback(self) -> None:
        """
        Start callback socket.
        """


        # Define.
        def put_queue(data: bytes) -> None:
            """
            Put data into queue.

            Parameters
            ----------
            data : Socket receive data.
            """

            # Put.
            self.queue.put(data)


        # Listen socket.
        listen_socket(
            callback_host,
            callback_port,
            put_queue
        )


    @wrap_thread
    def _start_receiver(
        self,
        max_receiver: int
    ) -> None:
        """
        Create receiver, it will get message parameters from receive queue, and handle.

        Parameters
        ----------
        max_receiver : Maximum number of receivers.
        """


        # Define.
        def handlers(message: Message) -> None:
            """
            Handlers.

            Parameters
            ----------
            message : Message parameters.
            """

            # Handle.
            for handler in self.handlers:
                wrap_exc(
                    handler,
                    message,
                    _handler=self.rwechat.rlog.rrlog.log
                )

            ## Put.
            self.queue.put(message)


        # Thread pool.
        thread_pool = RThreadPool(
            handlers,
            _max_workers=max_receiver
        )

        # Loop.
        while True:

            ## Stop.
            if self.started is False:
                sleep(0.1)
                continue

            ## End.
            elif self.started is None:
                break

            ## Submit.
            message = self.rwechat.rclient.receive()
            thread_pool(message)