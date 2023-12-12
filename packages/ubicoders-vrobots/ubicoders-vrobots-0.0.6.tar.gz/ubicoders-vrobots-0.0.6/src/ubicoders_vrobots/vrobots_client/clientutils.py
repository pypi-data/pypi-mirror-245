from abc import ABC, abstractmethod
import websocket
import time
import flatbuffers
import _thread


class WebsocketClient:
    def __init__(self, robot) -> None:
        self.robot = robot

        def on_message(ws, message):
            # print("message recieved")
            # print(message)
            self.robot.unpack(message)

        def on_error(ws, error):
            print(error)

        def on_close(ws, close_status_code, close_msg):
            print("### closed ###")

        def on_open(ws):
            print("Opened connection")

            ## setup and send setup message
            self.robot.setup()
            ws.send(self.robot.pack_setup(), opcode=0x2)

            def _update_loop(*args):
                while True:
                    time.sleep(0.02)  # 50 hz
                    self.robot.loop()
                    ws.send(self.robot.pack(), opcode=0x2)
                    # ws.send("hello server")

            _thread.start_new_thread(_update_loop, ())

        self.ws = websocket.WebSocketApp(
            "ws://localhost:12740",
            on_open=on_open,
            on_close=on_close,
            on_error=on_error,
            on_message=on_message,
        )

    def start(self):
        self.ws.run_forever()


class VirtualRobot(ABC):
    def __init__(self) -> None:
        self.setup = None
        self.loop = None

    @abstractmethod
    def pack_setup(self):
        pass

    @abstractmethod
    def pack(self):
        pass

    @abstractmethod
    def unpack(self):
        pass


class System:
    def __init__(
        self, robot, ubicoders_main_obj, duration=5, stop_condition=None
    ) -> None:
        self.robot = robot
        self.robot.setup = ubicoders_main_obj.setup
        self.robot.loop = ubicoders_main_obj.loop
        self.ws = WebsocketClient(self.robot)

    def start(self):
        self.ws.start()


if __name__ == "__main__":
    sys = System()
