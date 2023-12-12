#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2023/11/2 9:01
# @Author  : jw
import asyncio
import logging.config
import threading

import websockets
from websockets.server import serve
from typing import Callable, Coroutine
from websockets.legacy.server import WebSocketServerProtocol
from jw_ws.msg import *


class ClientInfo:
    def __init__(self, client_id, ws):
        self.client_id = client_id
        self.ws: WebSocketServerProtocol = ws
        self.topics = []

    def set_topics(self, topics):
        self.topics = topics


class AsyncWS:
    # 客户端列表
    clients: {str: ClientInfo} = {}

    # serving
    _serving: bool = False

    __Req_RES = "req_res"
    __Pub_Sub = "pub_sub"

    __all_command_handle = {}

    __topic_callback = {}

    __actions = ["pub", "sub", "req", "res"]

    def __init__(self, host="127.0.0.1", port=13254, max_client=2000, logger=None):
        if not logger:
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger("async_ws")
        else:
            self.logger = logger
        self.host = host
        self.port = port
        if max_client < 0:
            max_client = 10
        self.max_client = max_client

    async def __Serve(self):

        stop = asyncio.Future()
        async with serve(self.__run_ws, self.host, self.port) as s:
            self._serving = True
            await stop
            await s.wait_closed()

    async def __run_ws(self, websocket: WebSocketServerProtocol, path):
        """
        入口
        :param websocket:
        :return:
        """

        # 校验客户端数量
        if self.client_limit():
            self.logger.info("maximum client connection limit")
            await websocket.send(self.make_response(400, "客户端超出限制"))
            return

        # 用户名密码认证
        if not await self.auth():
            print("no auth")
            return

        # 校验token
        if not await self.token():
            print("no token")
            return

        # 保存客户端
        client_id = websocket.id
        self.append_client(client_id, websocket)
        self.logger.info("ws client identity: %s(%s)", client_id, websocket.remote_address)

        # 处理消息
        try:
            await self.__handle_msg(client_id, websocket)
        except Exception as e:
            self.logger.error("收到异常：%s", e)
            await websocket.close()
        finally:
            await websocket.wait_closed()
            self.logger.info("client is closed: %s", client_id)
            self.logger.info("current clients num: %s", len(self.clients))
            if client_id != "":
                self.clients.pop(client_id, "")
            self.logger.info("new clients num: %s", len(self.clients))

    async def __handle_msg(self, client_id, websocket: WebSocketServerProtocol):
        """
        处理消息
        :return:
        """

        async for message in websocket:
            ws_msg, err = self.valid_message(message)
            if err != "":
                self.logger.warning("msg valid fail:%s", err)
                res = self.make_response(404, err)
                await websocket.send(res)
                continue

            self.logger.info("recv client(%s) msg: %s", client_id, ws_msg)

            mode = ws_msg.mode
            if mode == self.__Pub_Sub:
                if ws_msg.action == "sub":
                    # 保存订阅者信息
                    cli_info = self.clients.get(client_id)
                    cli_info.set_topics(ws_msg.topic)
                    res = self.make_response(200, f"sub{ws_msg.topic}ok")
                    await websocket.send(res)
                    continue
                elif ws_msg.action == "pub":
                    # 取出topic
                    topic = ws_msg.topic
                    # 响应发布者
                    res = self.make_response(200, f"pub {topic} msg ok")
                    await websocket.send(res)

                    if len(self.clients) == 0:
                        continue

                    # 将消息发布到订阅了该topic的客户端
                    self.pub_topic_sync(topic, ws_msg)

                    # 如果该topic有会调函数，那么执行, 将回调的消息发给所有客户端
                    fn = self.get_topic_callback(topic)
                    if isinstance(fn, Callable):
                        callback_msg = fn()
                        if callback_msg:
                            self.pub_topic_sync(topic, callback_msg)
                    continue

            elif mode == self.__Req_RES:
                command = ws_msg.command

                # 根据不同的command找到不同的处理函数
                fn = self.get_cmd_handle(command)
                if hasattr(fn, '__call__'):
                    await fn(ws_msg, websocket)
                else:
                    res = self.make_response(404, "消息指令未找到")
                    await websocket.send(res)
            else:
                res = self.make_response(404, "消息模式未找到")
                await websocket.send(res)
                continue

    def client_limit(self) -> bool:
        """
        限制连接数量
        :return:
        """
        return len(self.clients) > self.max_client - 1

    @staticmethod
    def make_response(code=200, msg="success", data=None):
        res = {
            "code": code,
            "msg": msg
        }
        if data is not None:
            res["data"] = data

        return json.dumps(res, ensure_ascii=False)

    async def auth(self):
        """
        用户名密码
        :return:
        """
        return True

    async def token(self):
        """
        校验token
        :return:
        """
        return True

    def valid_message(self, req_msg) -> (Msg1, str):
        """
        校验消息
        :return:
        """
        try:
            message = json.loads(req_msg)
            src = message.get("src")
            if src == "":
                return None, "src 不能为空"

            action = message.get("action")
            if action not in self.__actions:
                return None, f"action 不在允许的列表{self.__actions}"

            # 根据不同的消息类型，反序列化不同的消息
            mode = message.get("mode")
            if mode == ReqMessage.mode:
                command = message.get("command")
                args = message.get("args")
                kwargs = message.get("kwargs")
                if command == "":
                    return None, "command 不能为空"
                ws_msg = ReqMessage(src=src, command=command, args=args, kwargs=kwargs)

            elif action == "sub":
                topics = message.get("topic")
                if not isinstance(topics, list):
                    return None, "订阅的topic 格式不正确"
                ws_msg = SubMessage(src=src, topic=topics)

            elif action == "pub":
                topics = message.get("topic")
                code = message.get("code")
                msg = message.get("msg")
                error = message.get("error")
                data = message.get("data")
                if not isinstance(topics, str):
                    return None, "发布的topic 格式不正确"
                ws_msg = PubMessage(src=src, topic=topics, code=code, msg=msg, error=error, data=data)

            else:
                return None, "不支持的消息模式"

        except Exception as e:
            return None, e.__str__()

        return ws_msg, ""

    def run_async_ws(self):
        if self._serving:
            self.logger.warning("not multi Serve")
            return
        asyncio.run(self.__Serve())

    def get_clients(self):
        for k, v in self.clients.items():
            if v.ws:
                yield v.ws

    def get_pub_clients(self, topic):
        for k, v in self.clients.items():
            if topic in v.topics:
                if v.ws:
                    yield v.ws

    def pub_topic_sync(self, topic, pub_msg: PubMessage):
        """
        同步发送消息给所有客户端
        :return:
        """

        # 同步方式
        websockets.broadcast(self.get_pub_clients(topic), pub_msg.dumps())

    def send_all_sync(self, res_msg: ResMessage):
        """
        同步发送消息给所有客户端
        :return:
        """

        # 同步方式
        websockets.broadcast(self.get_clients(), res_msg.dumps())

    def send_all_async(self, res_msg: ResMessage):
        """
        异步发送消息给所有客户端
        :return:
        """

        def send(loop, msg):
            task = loop.create_task(self.__send_all(msg))
            loop.run_until_complete(task)

        new_loop = asyncio.new_event_loop()

        t = threading.Thread(target=send, args=(new_loop, res_msg))
        t.start()
        t.join()

    def send_some(self, res_msg: ResMessage):
        """
        异步发送消息给某类客户端：比如前端front、后端agent、后端monitor、后端control
        :return:
        """
        loop = asyncio.get_event_loop()
        c1 = loop.create_task(self.__send_some(res_msg))
        loop.run_until_complete(c1)

    async def __send_all(self, res_msg: ResMessage):
        self.logger.debug("call send msg to all(%s) ws client...", len(self.clients))
        try:
            if len(self.clients) == 0:
                return
            for ws in self.get_clients():
                if ws:
                    await ws.send(res_msg.dumps())
            return
        except websockets.ConnectionClosed:
            self.logger.info("the client is closed")
        return

    async def __send_some(self, res_msg: ResMessage):
        # self.logger.info("call send msg to some(%s) ws client...", len(self.clients))
        # for k, v in self.clients.items():
        #     if v.ws
        #     if v.ws:
        #         await v.ws.send(res_msg.dumps())
        pass

    def append_client(self, client_id, ws):
        cli_info = ClientInfo(client_id=client_id, ws=ws)

        self.clients[cli_info.client_id] = cli_info

    def add_command_handle(self, command, func: Callable[[ReqMessage, WebSocketServerProtocol], Coroutine]):
        """
        注册指令的处理函数
        :param command: 指令名称
        :param func: 该指令对应的处理函数
        :return:
        """
        t_command = command.upper()
        self.__all_command_handle[t_command] = func

    def registry_topic_callback(self, topic, fn):
        """
        订阅到的topic的回调
        :return:
        """
        self.__topic_callback[topic] = fn
        pass

    def get_cmd_handle(self, command):
        t_command = command.upper()
        return self.__all_command_handle.get(t_command, None)

    def get_topic_callback(self, topic):
        return self.__topic_callback.get(topic, None)
