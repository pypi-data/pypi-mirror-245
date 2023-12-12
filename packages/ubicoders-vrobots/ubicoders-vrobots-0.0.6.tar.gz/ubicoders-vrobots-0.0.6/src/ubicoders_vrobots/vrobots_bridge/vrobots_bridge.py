import time
from websockets.server import serve
import asyncio
import websockets
import threading
import asyncio
from ..messages.multirotor_generated import FB_MultirotorMsgAll
from ..messages.helicopter_generated import FB_HeliMsgAll
from ..messages.imu_generated import FB_IMUMsgAll


WebSocketList = []


class NamedWebsocket:
    def __init__(self, name, ws) -> None:
        self.ws = ws
        self.name = name
        self.msg = None

    def handle_new_msg(self, name, ws):
        if name is None or self.name != name:
            return
        self.handle_dup(ws)

    def handle_dup(self, ws):
        if self.validate_dup(ws) is True:
            return
        else:
            self.ws.close()
            self.ws = ws

    def validate_dup(self, ws):
        if self.ws is ws:
            return True
        else:
            return False

    def remove(self):
        WebSocketList.remove(self)


def get_name_from_msg(msg):
    # Heli msg
    if FB_HeliMsgAll.FB_HeliMsgAllBufferHasIdentifier(msg, 0) is True:
        heli_all = FB_HeliMsgAll.GetRootAs(msg, 0)
        name = heli_all.Sender().decode("utf-8")
        msg_type = heli_all.MsgType()
        return [name, msg_type]

    # Multirotor msg
    if FB_MultirotorMsgAll.FB_MultirotorMsgAllBufferHasIdentifier(msg, 0) is True:
        mr_all = FB_MultirotorMsgAll.GetRootAs(msg, 0)
        name = mr_all.Sender().decode("utf-8")
        msg_type = mr_all.MsgType()
        return [name, msg_type]
    

    # Multirotor msg
    if FB_IMUMsgAll.FB_IMUMsgAllBufferHasIdentifier(msg, 0) is True:
        imu0_all = FB_IMUMsgAll.GetRootAs(msg, 0)
        name = imu0_all.Sender().decode("utf-8")
        msg_type = imu0_all.MsgType()
        return [name, msg_type]

    return None


def upsert_ws_list(name, ws):
    # check if ws_list has name
    for named_ws in WebSocketList:
        if named_ws.name == name:
            named_ws.handle_new_msg(name, ws)
            return

    # if new, push
    named_ws = NamedWebsocket(name, ws)
    WebSocketList.append(named_ws)
    named_ws.handle_new_msg(name, ws)


def remove_ws_list(name):
    for named_ws in WebSocketList:
        if named_ws.name == name:
            named_ws.remove()
            return


async def echo(websocket):
    print("Client connected")
    name = None
    try:
        async for message in websocket:
            # print(message)
            # await websocket.send("hi there")
            result = get_name_from_msg(message)
            # print(result)
            if result is None:
                continue

            name = result[0]
            msg_type = result[1]

            if msg_type == 0:
                continue

            upsert_ws_list(name, websocket)

            # print(len(WebSocketList))
            for named_ws in WebSocketList:
                # print(named_ws.name)
                if named_ws.name == name:
                    continue
                # print(len(WebSocketList))
                # print(f"send to {named_ws.name}, msg: {message}")
                await named_ws.ws.send(message)

    except Exception as e:
        print(f"Error while processing message: {message}")
        print(e)
    finally:
        print(f"Client disconnected")
        remove_ws_list(name)


def run_bridge_server():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    print("simulator server running @ 12740")
    start_server = websockets.serve(echo, "0.0.0.0", 12740)

    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
    loop.run_until_complete(start_server)
    loop.run_forever()


class BridgeModule:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(BridgeModule, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.stopFlag = False
        self.thread = None
        self.value = 1

    def start(self):
        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.stopFlag = True
        self.thread.join()

    def loop(self):
        while self.stopFlag == False:
            run_bridge_server()


BRIDGE = BridgeModule()


async def main():
    async with serve(echo, "localhost", 12740):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    run_bridge_server()  # run without gui
