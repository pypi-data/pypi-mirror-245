# 消息

## 模式

mode是一级指令，分为两种模式(mode)：

- 请求-响应模式(req_res)：对话模式，客户端发一条，服务端回复一条，当然也可以进行多轮对话
- 发布-订阅模式(pub_sub)：发布订阅模式，服务端和客户端都是对等的，都可以进行发布和订阅，只需要指定了发布的主题和订阅的主题，就能收到

## 动作

action是二级指令，从属于模式下，对应分别为2种动作：

- req_res：req、res
- pub_sub：pub、sub

## 发布消息格式

这条消息最终会被订阅了该topic的订阅端收到

```json
{
  "mode": "pub_sub",
  "action": "pub",
  "src": "agent",
  "topic": "user",
  "code": 200,
  "msg": "添加了一个用户",
  "data": [
    {
      "name": "jw",
      "age": 110
    }
  ]
}
```

## 订阅的消息格式

客户端建立ws连接之后，可以手动发送一条订阅消息，表示自己订阅这些topic

```json
{
  "mode": "pub_sub",
  "action": "sub",
  "src": "front",
  "topic": [
    "user",
    "order"
  ]
}
```

## 客户端主动请求

建立ws连接之后，客户端主动发送消息，需要携带command，比如`add_user`、`taskStats`、`images`...等。服务端会回应数据。

如果需要传参数，则按照下面格式
参数：

- args：[1, 2,3]
- kwargs: {"name":"jw","id":1}

```json
{
  "mode": "req_res",
  "action": "req",
  "src": "front",
  "command": "add_user|images|del_user|web|restartProcess",
  "args": [
    1,
    2
  ],
  "kwargs": {
    "name": "jw",
    "id": 1
  }
}
```

## 服务端被动响应

### 成功

```json
{
  "src": "control",
  "code": 200,
  "msg": "success",
  "data": [
    {
      "img1": "/path/1"
    }
  ],
  "mode": "req_res",
  "action": "res"
}
```

### 失败

```json
{
  "src": "control",
  "code": 404,
  "msg": "没查到",
  "data": [],
  "mode": "req_res",
  "action": "res"
}
```

# 使用示例：

## 编写指令的响应

```python
from websockets.legacy.server import WebSocketServerProtocol

import logging

import threading

from jw_ws.server import AsyncWS
from jw_ws.msg import *


async def web(req_msg: ReqMessage, websocket: WebSocketServerProtocol):
    """
    心跳消息
    :param req_msg:
    :param websocket:
    :return:
    """
    # 组装消息，只要是json格式即可
    res = ResMessage(src="control", code=200, msg="success")
    # 发送给该客户端
    await websocket.send(res.dumps())
    # 禁止执行此类代码
    # time.sleep(10)

    # 如果需要进行多轮对话，那么可以继续send、recv
    # await websocket.recv()
    # await websocket.send()
    # await websocket.recv()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("example")

    ws = AsyncWS(host="0.0.0.0", port=18887)

    t1 = threading.Thread(target=ws.run_async_ws)
    t1.daemon = True
    t1.start()

    ws.add_command_handle("web", web)
```

## 发布消息

只要订阅端和发布端按照规定的消息格式来交互，那么服务端无需要改代码，即可实现消息订阅。

还有一种场景，订阅端收到了发布的消息之后，服务端还想处理该消息，比如多发几条消息，那么就可以通过主题回调来实现。

```python
def user_callback():
    print("user topic 回调函数")
    return PubMessage(src="agent", code=200, topic="user", data=["hahaha", "xixixi"])


ws.registry_topic_callback("user", fn=user_callback)
```

## 广播消息

会将消息发送给所有客户端。

```python
from jw_ws.server import AsyncWS
from jw_ws.msg import *
import threading

if __name__ == '__main__':
    ws = AsyncWS(host="0.0.0.0", port=18887)

    t1 = threading.Thread(target=ws.run_async_ws)
    t1.daemon = True
    t1.start()

    msg = ResMessage(src="control", data={"name": "jw", "num": n})
    ws.send_all_async(msg)
    ws.send_all_sync(msg)
```

# 注意事项

使用的是websockets库的async模式，也就是异步非阻塞模式。
编写指令回复的逻辑的时候，不能使用阻塞的代码，否则整个ws服务会被阻塞住，无法接收新的连接，以及其余客户端的消息也会阻塞住。

比如`time.sleep(10)`。而应该使用`asyncio.sleep(3)`。

Python的asyncio还在逐步完善，像数据库或者文件IO，cpu计算密集型，如果一定要执行阻塞逻辑，那么可以通过开线程使用，这样就不会阻塞了。例子如下：

```python
from websockets.legacy.server import WebSocketServerProtocol
import concurrent.futures
from jw_ws.msg import *
import asyncio


def blocking_io():
    # 文件io
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)


def cpu_bound():
    # cpu计算
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))


async def images(req_msg: ReqMessage, websocket: WebSocketServerProtocol):
    # 异步执行阻塞函数：比如文件IO、数据库查询、网络IO等

    # 获取当前事件循环
    running_lop = asyncio.get_running_loop()
    print("current running loop...", running_lop)

    # 文件IO
    with concurrent.futures.ThreadPoolExecutor() as pool:
        result = await running_lop.run_in_executor(
            pool, blocking_io)
        print('同步调用的结果:', result)

    # cpu密集型
    with concurrent.futures.ProcessPoolExecutor() as pool:
        result = await running_lop.run_in_executor(
            pool, cpu_bound)
        print('同步调用的结果', result)

    # 等待调用完成
    print("同步调用完成")
```

如果是网络请求，比如之前的一键重启，可以通过`aiohttp`库
```python
import aiohttp
import json
import asyncio

async def restart_container(index: int, url: str):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(timeout=timeout) as session:
        try:
            async with session.post(url) as resp:
                return resp.status
        except Exception as e:
            print("send restart container error: ", e)
            return -1


async def restart_progress(server):
    """
    发送重启进度
    """
    # 要重启的服务名称列表
    # restart_items = config["restart"]["agent"] + config["restart"]["vision"] + config["restart"]["camera"]
    # 要重启的服务数量
    restart_nums = 3
    progress = 0

    # 重启次数
    restart_num = 0
    # 错误次数
    wrong_restart_num = 0

    def call_back(task):
        nonlocal wrong_restart_num
        nonlocal restart_num
        res_code = task.result()
        if res_code == 204 or res_code == 200:
            pass
        else:
            wrong_restart_num += 1
        restart_num += 1

    loop = asyncio.get_event_loop()

    for items in range(1, 4):
        restart_url = "https://www.baidu.com"
        # 创建3个任务对象
        job = loop.create_task(restart_container(index=items, url=restart_url))
        job.add_done_callback(call_back)

    print("task1....")
    print("task2....")
    while True:
        if restart_num == restart_nums:
            break
        if int(restart_num / restart_nums * 100) > progress:
            progress = int(restart_num / restart_nums * 100)
        if progress < 99:
            progress += 1
        if 0 <= progress <= 30:
            msg = "软件重启中"
        elif 31 <= progress <= 70:
            msg = "视觉重启中"
        elif 71 <= progress <= 99:
            msg = "相机重启中"
        else:
            msg = "error"
        data = {"command": "restartProcess", "process": progress, "code": 200, "msg": msg}
        await server.send(json.dumps(data, ensure_ascii=False))
        await asyncio.sleep(1)

    if wrong_restart_num == 0:
        data = {"command": "restartProcess", "process": 100, "code": 200, "msg": "重启成功"}
    else:
        data = {"command": "restartProcess", "process": progress, "code": 200, "msg": "重启失败"}
    await server.send(json.dumps(data, ensure_ascii=False))

async def restartProcess(req_msg, websocket):
    data = {"command": "restartProcess", "process": 0, "code": 200, "msg": "软件开始重启"}
    await websocket.send(json.dumps(data, ensure_ascii=False))
    await restart_progress(websocket)
```