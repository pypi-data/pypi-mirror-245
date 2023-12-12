import flatbuffers
from ..messages.multirotor_generated import *
from .mr_msgs_helper import MultirotorGroundTruth
from ..vrobots_client.clientutils import VirtualRobot, System


class Multirotor(VirtualRobot):
    def __init__(self) -> None:
        self.ground_truth = MultirotorGroundTruth(None)
        self.pwm = [900, 900, 900, 900]

    def set_pwm(self, m0, m1, m2, m3):
        self.pwm = [m0, m1, m2, m3]

    def pack_setup(self):
        builder = flatbuffers.Builder(512)
        sender = builder.CreateString("python")
        FB_MultirotorMsgAllStart(builder)
        FB_MultirotorMsgAllAddSender(builder, sender)
        FB_MultirotorMsgAllAddMsgType(builder, 4)
        FB_MultirotorMsgAllAddCmdReset(builder, 1)
        os = FB_MultirotorMsgAllEnd(builder)
        builder.Finish(os, b"MLRT")
        return builder.Output()

    def pack(self):  # FB_MultirotorMsgAll
        builder = flatbuffers.Builder(512)
        sender = builder.CreateString("python")

        FB_Vect16MsgStart(builder)
        FB_Vect16MsgAddM0(builder, self.pwm[0])
        FB_Vect16MsgAddM1(builder, self.pwm[1])
        FB_Vect16MsgAddM2(builder, self.pwm[2])
        FB_Vect16MsgAddM3(builder, self.pwm[3])
        vec16_os = FB_ActuatorsMsgEnd(builder)

        FB_ActuatorsMsgStart(builder)
        FB_ActuatorsMsgAddPwm(builder, vec16_os)
        actuator_os = FB_ActuatorsMsgEnd(builder)

        FB_MultirotorMsgAllStart(builder)
        FB_MultirotorMsgAllAddSender(builder, sender)
        FB_MultirotorMsgAllAddMsgType(builder, 4)
        FB_MultirotorMsgAllAddCmdControl(builder, actuator_os)
        os = FB_MultirotorMsgAllEnd(builder)
        builder.Finish(os, b"MLRT")
        return builder.Output()

    def unpack(self, msg):  # FB_MultirotorMsgAll
        objdata = FB_MultirotorMsgAllT.InitFromPackedBuf(msg, 0)
        self.ground_truth = MultirotorGroundTruth(objdata.groundTruth)
        ## TODO onboard pid params


# ===============================================================================
# dev code
# ===============================================================================

mr = Multirotor()


class UbicodersMain:
    def __init__(self) -> None:
        pass

    def setup(self):
        # mr.mass = 2 kg
        pass

    def loop(self):
        gt = mr.ground_truth
        print(gt)

        mr.set_pwm(m0=1500, m1=1500, m2=1501, m3=1501)


if __name__ == "__main__":
    sys = System(mr, UbicodersMain())
    sys.start()
