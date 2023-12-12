import json
from ..messages.imu_generated import FB_Vec3MsgT, FB_Vec4MsgT, FB_IMUGroundTruthMsgT,FB_IMUSensorMsgT, FB_IMUMsgAllT


class IMUVec3(FB_Vec3MsgT):
    def __init__(self, instance):
        super().__init__()
        if instance == None:
            self.x = 0
            self.y = 0
            self.z = 0
            return
        self.x = instance.x
        self.y = instance.y
        self.z = instance.z

    def get_dict_data(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)

class IMUVec4(FB_Vec4MsgT):
    def __init__(self, instance):
        super().__init__()
        if instance == None:
            self.x = 0
            self.y = 0
            self.z = 0
            self.w = 0
            return
        self.x = instance.x
        self.y = instance.y
        self.z = instance.z
        self.w = instance.w

    def get_dict_data(self):
        return {
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "w": self.w,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)


class IMU_GT():
    def __init__(self, instance: FB_IMUGroundTruthMsgT):
        super().__init__()
        if instance == None:
            self.euler = IMUVec3(None) # deg per second
            self.ang_vel = IMUVec3(None) # rad per second
            return
        self.euler = IMUVec3(instance.euler)
        self.ang_vel = IMUVec3(instance.angVel)

    def get_dict_data(self):
        return {
            "euler": self.euler.get_dict_data(),
            "ang_vel": self.ang_vel.get_dict_data(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)

class IMU_Sensor():
    def __init__(self, instance:FB_IMUSensorMsgT):
        super().__init__()
        if instance == None:
            self.acc = IMUVec3(None)
            self.gyro = IMUVec3(None)
            self.mag = IMUVec3(None)
            return
        self.acc = IMUVec3(instance.acc)
        self.gyro = IMUVec3(instance.gyro)
        self.mag = IMUVec3(instance.mag)
    
    def get_dict_data(self):
        return {
            "acc": self.acc.get_dict_data(),
            "gyro": self.gyro.get_dict_data(),
            "mag": self.mag.get_dict_data(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)

class IMU_All():
    def __init__(self, instance:FB_IMUMsgAllT):
        super().__init__()
        if instance == None:
            self.gt = IMU_GT(None)
            self.imu = IMU_Sensor(None)
            return
        self.gt = IMU_GT(instance.gt)
        self.imu = IMU_Sensor(instance.imu)
    
    def get_dict_data(self):
        return {
            "gt": self.gt.get_dict_data(),
            "imu": self.imu.get_dict_data(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)

