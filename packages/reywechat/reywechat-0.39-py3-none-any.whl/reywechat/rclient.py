# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-17 20:27:16
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Client methods.
"""


from __future__ import annotations
from typing import Any, Dict, Optional, Literal, Union
from reytool.rcomm import request as reytool_request
from reytool.rdll import inject_dll
from reytool.rsystem import search_process
from reytool.ros import find_relpath

from .rwechat import RWeChat


__all__ = (
    "RClient",
)


client_api_port = 19088


class RClient(object):
    """
    Rey's `client` type.
    """


    def __init__(
        self,
        rwechat: RWeChat
    ) -> None:
        """
        Build `client` instance.

        Parameters
        ----------
        rwechat : `RWeChat` instance.
        """

        # Start.
        self.start_api()

        # Set attribute.
        self.rwechat = rwechat
        self.account_info = self.get_account_info()


    def start_api(self) -> None:
        """
        Start client control API.
        """

        # Check client.
        result = self.check_client()
        if not result:
            raise Exception("WeChat client not started")

        # Check start.
        result = self.check_api()
        if result: return

        # Inject DLL.
        self.inject_dll()

        # Check api.
        result = self.check_api()
        if not result:
            raise Exception("WeChat client API failed to start")


    def check_client(self) -> bool:
        """
        Check if the client is started.

        Returns
        -------
        Check result.
        """

        # Search.
        processes = search_process(name="WeChat.exe")

        # Check.
        if processes == []:
            return False
        else:
            return True


    def check_api(self) -> bool:
        """
        Check if the client API is started.
        """

        # Search.
        processes = search_process(port=client_api_port)

        # Check.
        if processes == []:
            return False
        process = processes[0]
        with process.oneshot():
            process_name = process.name()
        if process_name != "WeChat.exe":
            return False

        ## Check request.
        result = self.check_login()
        if not result:
            return False

        return True


    def inject_dll(self) -> None:
        """
        Inject DLL file of start API into the WeChat client process.
        """

        # Get parameter.
        dll_file_relpath = r".\data\client_api.dll"
        dll_file_path = find_relpath(__file__, dll_file_relpath)

        # Inject.
        processes = search_process(name="WeChat.exe")
        process = processes[0]
        inject_dll(
            process.pid,
            dll_file_path
        )


    def request(
        self,
        api: str,
        data: Optional[Dict] = None
    ) -> Dict[
        Literal["code", "message", "data"],
        Any
    ]:
        """
        Request client API.

        Parameters
        ----------
        api : API name.
        data : Request data.

        Returns
        -------
        Response content.
            - `code` : Response code.
            - `message` : Response message.
            - `data` : Response data.
        """

        # Get parameter.
        url = f"http://127.0.0.1:{client_api_port}/api/{api}"
        if data is None:
            data = {}

        # Request.
        response = reytool_request(
            url,
            json=data,
            method="post",
            check=True
        )

        # Extract.
        response_data = response.json()
        data = {
            "code": response_data["code"],
            "message": response_data["msg"],
            "data": response_data["data"]
        }

        return response_data


    def check_login(self) -> bool:
        """
        Check if the client is logged in.

        Returns
        -------
        Check result.
        """

        # Get parameter.
        api = "checkLogin"

        # Request.
        response = self.request(api)

        # Check.
        if response["code"] == 1:
            return True
        elif response["code"] == 0:
            return False


    def get_account_info(
        self
    ) -> Dict[
        Literal[
            "id",
            "account",
            "name",
            "mobile",
            "signature",
            "country",
            "province",
            "city",
            "head_image",
            "account_data_path",
            "wechat_data_path",
            "decrypt_key"
        ],
        Optional[str]
    ]:
        """
        Get login account information.

        Returns
        -------
        Login user account information.
            - `Key 'id'` : ID, cannot change.
            - `Key 'account' : Account, can change.
            - `Key 'name' : Account name.
            - `Key 'mobile' : Bind phone number.
            - `Key 'signature' : Personal signature.
            - `Key 'country' : Country.
            - `Key 'province' : Province.
            - `Key 'city' : City.
            - `Key 'head_image' : Head image URL.
            - `Key 'account_data_path' : Current account data save path.
            - `Key 'wechat_data_path' : WeChat data save path.
            - `Key 'decrypt_key' : Database decrypt key.
        """

        # Get parameter.
        api = "userInfo"

        # Request.
        response = self.request(api)

        # Extract.
        data = response["data"]
        info = {
            "id": data["wxid"],
            "account": data["account"],
            "name": data["name"],
            "mobile": data["mobile"],
            "signature": data["signature"],
            "country": data["country"],
            "province": data["province"],
            "city": data["city"],
            "head_image": data["headImage"],
            "account_data_path": data["currentDataPath"],
            "wechat_data_path": data["dataSavePath"],
            "decrypt_key": data["dbKey"]
        }
        info = {
            key: (
                None
                if value == ""
                else value
            )
            for key, value in info.items()
        }

        return info


    def hook_message(
        self,
        host: str,
        port: Union[str, int],
        timeout: float
    ) -> None:
        """
        Hook the message, and send the message to the TCP protocol request.

        Parameters
        ----------
        host : Request host.
        port : Request port.
        timeout : Request timeout seconds.
        """

        # Get parameter.
        api = "hookSyncMsg"
        port = str(port)
        timeout = str(int(timeout * 1000))

        # Request.
        data = {
            "ip": host,
            "port": port,
            "timeout": timeout,
            "enableHttp": "0"
        }
        response = self.request(api, data)

        # Check.
        if response["code"] != 0:
            raise Exception("hook message fail")


    def unhook_message(self) -> None:
        """
        Unhook the message.
        """

        # Get parameter.
        api = "unhookSyncMsg"

        # Request.
        response = self.request(api)

        # Check.
        if response["code"] != 0:
            raise Exception("unhook message fail")