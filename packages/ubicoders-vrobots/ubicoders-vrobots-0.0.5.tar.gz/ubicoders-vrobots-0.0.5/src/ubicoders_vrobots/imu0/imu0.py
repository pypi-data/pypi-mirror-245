import flatbuffers
from ..messages.imu_generated import *
from ..vrobots_client.clientutils import VirtualRobot, System
from ..imu0.imu0_msgs_helper import IMU_All


class IMU0(VirtualRobot):
    def __init__(self) -> None:
        self.force = 0
        self.states = None

    def set_force(self, f):
        self.force = f

    def pack_setup(self):
        return self.pack()

    def pack(self):  # FB_MultirotorMsgAll
        builder = flatbuffers.Builder(512)
        sender = builder.CreateString("python")
        FB_IMUMsgAllStart(builder)        
        FB_IMUMsgAllAddSender(builder, sender)
        FB_IMUMsgAllAddMsgType(builder, 1)
        os = FB_IMUMsgAllEnd(builder)
        builder.Finish(os, b"IMU0")
        return builder.Output()

    def unpack(self, msg):  # FB_MultirotorMsgAll
        objdata = FB_IMUMsgAllT.InitFromPackedBuf(msg, 0)
        self.data  = IMU_All(objdata)       


# ===============================================================================
# dev code
# ===============================================================================

imu0 = IMU0()


class UbicodersMain:
    def __init__(self) -> None:
        pass

    def setup(self):
        # mr.mass = 2 kg
        pass

    def loop(self):
        sim_data = imu0.data
        euler = sim_data.gt.euler
        print("euler: ", euler) # deg per second
        ang_vel = sim_data.gt.ang_vel
        print("ang_vel: ", ang_vel) # rad per second

        imu = sim_data.imu
        acc = imu.acc
        print("acc: ", acc)
        gyro = imu.gyro
        print("gyro: ", gyro)
        mag = imu.mag
        print("mag: ", mag)



if __name__ == "__main__":
    sys = System(imu0, UbicodersMain())
    sys.start()
