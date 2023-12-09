# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-22 22:50:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Send methods.
"""


from typing import Tuple, Dict, Optional
from threading import Thread
from queue import Queue
from reytool.rsystem import check_most_one, check_least_one, check_file_found
from reytool.rtime import sleep
from reytool.rwrap import wrap_thread
from reytool.rnumber import randn
from reytool.rrequest import get_file_send_time

from .rwechat import RWeChat


__all__ = (
    "RSend",
)


class RSend(object):
    """
    Rey's `send` type.
    """


    def __init__(
        self,
        rwechat: RWeChat,
        bandwidth: float
    ) -> None:
        """
        Build `send` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        bandwidth : Upload bandwidth, impact send interval, unit Mpbs.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.bandwidth = bandwidth
        self.queue: Queue[Tuple[str, Dict]] = Queue()
        self.started: Optional[bool] = False

        # Sender.
        self.sender: Thread = self._create_sender()


    def get_interval(
        self,
        plan: Tuple[str, Dict],
        minimum: float = 0.8,
        maximum: float = 1.2,
    ) -> float:
        """
        Get message send interval time, unit seconds.

        Parameters
        ----------
        plan : Plan message type and message parameters.
            - `Parameter has key 'file' and is not None` : Calculate file send time, but not less than random seconds.
            - `Other` : Calculate random seconds.

        minimum : Random minimum seconds.
        maximum : Random maximum seconds.

        Returns
        -------
        Send interval seconds.
        """

        # Get parameters.
        type_, params = plan

        # Random.
        seconds = randn(minimum, maximum, precision=2)

        # File.
        if type_ == "file":
            file_seconds = get_file_send_time(params["file"], self.bandwidth)
            if file_seconds > seconds:
                seconds = file_seconds

        return seconds


    @wrap_thread
    def _create_sender(self) -> None:
        """
        Create sender, it will get message parameters from send queue and send.
        """

        # Loop.
        while True:

            ## Stop.
            if self.started is False:
                sleep(0.1)
                continue

            ## End.
            elif self.started is None:
                break

            ## Start.
            plan = self.queue.get()
            type_, params = plan
            if type_ == "text":
                self.rwechat.rclient.send_text(**params, check=False)
            elif type_ == "file":
                self.rwechat.rclient.send_file(**params, check=False)

            ## Interval.
            seconds = self.get_interval(plan)
            sleep(seconds)


    def start(self) -> None:
        """
        Start sender.
        """

        # Start.
        self.started = True


    def stop(self) -> None:
        """
        Stop sender.
        """

        # Stop.
        self.started = False


    def end(self) -> None:
        """
        End sender.
        """

        # End.
        self.started = None


    def send(
        self,
        receiver: str,
        text: Optional[str] = None,
        ats: Optional[str] = None,
        file: Optional[str] = None,
        timeout: Optional[float] = None
    ) -> None:
        """
        Queue add plan, waiting send text or file message.

        Parameters
        ----------
        receiver : WeChat user ID or room ID.
        text : Text message content. Conflict with parameter 'file'.
        ats : User ID to '@' of text message content, comma interval. Can only be use when parameter 'receiver' is room ID.
            - `None` : Not use '@'.
            - `str` : Use '@', parameter 'text' must have with ID same quantity '@' symbols.

        file : File message path. Conflict with parameter 'text'.
        timeout : Number of timeout seconds.

        Examples
        --------
        Send text.
        >>> receiver = 'uid_or_rid'
        >>> rclient.send(receiver, 'Hello!')

        Send text and '@'.
        >>> receiver = 'rid'
        >>> ats = ('uid1', 'uid2')
        >>> rclient.send(receiver, '@uname1 @uname2 Hello!', ats)

        Send file.
        >>> file = 'file_path'
        >>> rclient.send(receiver, file=file)
        """

        # Check.
        check_most_one(text, file)
        check_least_one(text, file)

        ## Text.
        if text is not None:
            if ats is not None:

                ### ID type.
                if "@chatroom" not in receiver:
                    raise ValueError("when using parameter 'ats', parameter 'receiver' must be room ID.")

                ### Count "@" symbol.
                comma_n = ats.count(",")
                at_n = text.count("@")
                if at_n < comma_n:
                    raise ValueError("when using parameter 'ats', parameter 'text' must have with ID same quantity '@' symbols")

        ## File.
        elif file is not None:

            ### Found.
            check_file_found(file)

        # Generate plan.

        ## Text.
        if text is not None:
            plan = (
                "text",
                {
                    "receiver": receiver,
                    "text": text,
                    "ats": ats
                }
            )

        elif file is not None:
            plan = (
                "file",
                {
                    "receiver": receiver,
                    "file": file
                }
            )

        # Add plan.
        self.queue.put(plan, timeout=timeout)


    __call__ = send


    __del__ = end