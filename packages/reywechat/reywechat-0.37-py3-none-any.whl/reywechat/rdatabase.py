# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time    : 2023-10-23 20:55:58
@Author  : Rey
@Contact : reyxbo@163.com
@Explain : Database methods.
"""


from reytool.rdatabase import RDatabase as RRDatabase

from .rclient import MsgParams
from .rwechat import RWeChat


__all__ = (
    "RDatabase",
)


class RDatabase(object):
    """
    Rey's `database` type.
    """


    def __init__(
        self,
        rwechat: RWeChat,
        rrdatabase: RRDatabase
    ) -> None:
        """
        Build `database` instance.

        Parameters
        ----------
        rwechat : `RClient` instance.
        rrdatabase : RRDatabase instance.
        """

        # Set attribute.
        self.rwechat = rwechat
        self.rrdatabase = rrdatabase


    def update_message_type(self) -> None:
        """
        Update table `message_type`.
        """

        # Get data.
        type_dict = self.rwechat.rclient.get_type_dict()
        data = [
            {
                "type": type_,
                "description": description
            }
            for type_, description in type_dict.items()
        ]

        # Insert and update.
        self.rrdatabase.execute_insert(
            ("wechat", "message_type"),
            data,
            "update"
        )


    def build(self) -> None:
        """
        Check and build all standard databases and tables.
        """

        # Set parameter.

        ## Database.
        databases = [
            {
                "database": "wechat"
            }
        ]

        ## Table.
        tables = [

            ### "message_receive".
            {
                "path": ("wechat", "message_receive"),
                "fields": [
                    {
                        "name": "id",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL AUTO_INCREMENT",
                        "comment": "Message ID.",
                    },
                    {
                        "name": "uuid",
                        "type_": "bigint unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message UUID.",
                    },
                    {
                        "name": "time",
                        "type_": "datetime",
                        "constraint": "NOT NULL",
                        "comment": "Message receive time.",
                    },
                    {
                        "name": "room",
                        "type_": "char(20)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message room ID.",
                    },
                    {
                        "name": "sender",
                        "type_": "varchar(19)",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message sender ID.",
                    },
                    {
                        "name": "type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type.",
                    },
                    {
                        "name": "content",
                        "type_": "text",
                        "constraint": "CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL",
                        "comment": "Message content.",
                    },
                    {
                        "name": "xml",
                        "type_": "text",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message XML content.",
                    },
                    {
                        "name": "file",
                        "type_": "mediumint unsigned",
                        "constraint": "DEFAULT NULL",
                        "comment": "Message file ID.",
                    },
                    {
                        "name": "receiver",
                        "type_": "varchar(19)",
                        "constraint": "NOT NULL",
                        "comment": "Message receiver ID.",
                    }
                ],
                "primary": "id",
                "comment": "Message receive table."
            },

            ### "message_type".
            {
                "path": ("wechat", "message_type"),
                "fields": [
                    {
                        "name": "type",
                        "type_": "int unsigned",
                        "constraint": "NOT NULL",
                        "comment": "Message type.",
                    },
                    {
                        "name": "description",
                        "type_": "varchar(200)",
                        "constraint": "NOT NULL",
                        "comment": "Message type description.",
                    }
                ],
                "primary": "type",
                "comment": "Message type table."
            },
        ]

        # Build.
        self.rrdatabase.build(databases, tables)

        ## File.
        self.rrdatabase.file()

        # Insert.
        self.update_message_type()


    def to_message_receive(self) -> None:
        """
        Write message parameters to table `message_receive`.
        """


        # Define.
        def handler_db_message_receive(message: MsgParams) -> None:
            """
            Message handler, write message parameters to table `message_receive`.

            Parameters
            ----------
            message : Message parameters.
            """

            # Upload file.
            if message["file"] is None:
                file_id = None
            else:
                file_id = self.rrdatabase.file.upload(
                    message["file"],
                    uploader="WeChat"
                )

            # Generate data.
            data = {
                "uuid": message["uuid"],
                "room": message["room"],
                "sender": message["sender"],
                "type": message["type"],
                "content": message["content"],
                "xml": message["xml"],
                "file": file_id,
                "receiver": self.rwechat.rclient.client.self_wxid
            }
            kwdata = {
                "time": ":NOW()"
            }

            self.rrdatabase.execute_insert(
                ("wechat", "message_receive"),
                data,
                **kwdata
            )

        # Add handler.
        self.rwechat.rreceive.add_handler(handler_db_message_receive)


    def to_all(self) -> None:
        """
        To all database tables.
        """

        # Check and build.
        self.build()

        # Use "message_receive".
        self.to_message_receive()


    __call__ = to_all