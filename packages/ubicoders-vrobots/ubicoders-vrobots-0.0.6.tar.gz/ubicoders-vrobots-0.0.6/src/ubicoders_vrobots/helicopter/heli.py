import flatbuffers
from ..messages.helicopter_generated import *
from .heli_msgs_helper import HelicopterStates
from ..vrobots_client.clientutils import VirtualRobot, System


class Helicopter(VirtualRobot):
    def __init__(self) -> None:
        self.force = 0
        self.states = None

    def set_force(self, f):
        self.force = f

    def pack_setup(self):
        return self.pack()

    def pack(self):  # FB_MultirotorMsgAll
        builder = flatbuffers.Builder(512)
        FB_HeliInputMsgStart(builder)
        FB_HeliInputMsgAddForce(builder, self.force)
        cmd_input = FB_HeliInputMsgEnd(builder)
        sender = builder.CreateString("python")
        FB_HeliMsgAllStart(builder)
        FB_HeliMsgAllAddSender(builder, sender)
        FB_HeliMsgAllAddCmdInput(builder, cmd_input)
        FB_HeliMsgAllAddMsgType(builder, 1)
        os = FB_HeliMsgAllEnd(builder)
        builder.Finish(os, b"HELI")
        return builder.Output()

    def unpack(self, msg):  # FB_MultirotorMsgAll
        objdata = FB_HeliMsgAllT.InitFromPackedBuf(msg, 0)
        self.states = HelicopterStates(objdata.states)
        ## TODO onboard pid params


# ===============================================================================
# dev code
# ===============================================================================

heli = Helicopter()


class UbicodersMain:
    def __init__(self) -> None:
        pass

    def setup(self):
        # mr.mass = 2 kg
        pass

    def loop(self):
        if heli.states == None:
            return

        kp = 5
        kd = 10

        error = 5 - heli.states.pos.z

        heli.set_force(15 + error * kp - heli.states.vel.z * kd)


if __name__ == "__main__":
    sys = System(heli, UbicodersMain())
    sys.start()
