#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/13 10:17
# @Author  : jw
import json


class Msg1:

    def __init__(self, src):
        self.src = src

    def __str__(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class SubMessage(Msg1):
    mode = "pub_sub"
    action = "sub"

    def __init__(self, src, topic):
        super().__init__(src)
        if topic is None:
            topic = []
        self.topic = topic


class PubMessage(Msg1):
    def __init__(self, src, topic: str, code=200, msg="success", error="", data=None):
        super().__init__(src)
        self.topic = topic
        self.code = code
        self.msg = msg
        self.error = error
        self.data = data or []
        self.mode = "pub_sub"
        self.action = "pub"

    def dumps(self):
        return json.dumps(self.__dict__, ensure_ascii=False)


class ReqMessage(Msg1):
    """
    客户端请求的消息结构
    """
    mode = "req_res"
    action = "req"

    def __init__(self, src, command, args=None, kwargs=None):
        super().__init__(src)
        self.command = command
        self.args = args if args is not None else []
        self.kwargs = kwargs if kwargs is not None else {}


class ResMessage:
    """
    服务端响应的消息结构
    """

    def __init__(self, src="", code=200, msg="success", data=None):
        self.src = src
        self.code = code
        self.msg = msg
        if data:
            self.data = data
        self.mode = "req_res"
        self.action = "res"

    def dumps(self):
        return json.dumps(self.__dict__, ensure_ascii=False)
