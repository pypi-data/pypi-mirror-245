from ..messages.multirotor_generated import *
import json


class MRVector16(FB_Vect16MsgT):
    def __init__(self, instance):
        super().__init__()
        if instance == None:
            self.m0 = 0
            self.m1 = 0
            self.m2 = 0
            self.m3 = 0
            return
        self.m0 = instance.m0
        self.m1 = instance.m1
        self.m2 = instance.m2
        self.m3 = instance.m3

    def get_dict_data(self):
        return {
            "m0": self.m0,
            "m1": self.m1,
            "m2": self.m2,
            "m3": self.m3,
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)


class MRVector3(FB_Vec3MsgT):
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


class MultirotorStates(FB_StatesMsgT):
    def __init__(self, instance):
        super().__init__()
        if instance == None:
            self.position = MRVector3(None)
            self.linearVelocity = MRVector3(None)
            self.eulerAngles = MRVector3(None)
            self.angularVelocity = MRVector3(None)
            return
        self.position = MRVector3(instance.position)
        self.linearVelocity = MRVector3(instance.linearVelocity)
        self.eulerAngles = MRVector3(instance.eulerAngles)
        self.angularVelocity = MRVector3(instance.angularVelocity)

    def get_dict_data(self):
        return {
            "position": self.position.get_dict_data(),
            "linearVelocity": self.linearVelocity.get_dict_data(),
            "eulerAngles": self.eulerAngles.get_dict_data(),
            "angularVelocity": self.angularVelocity.get_dict_data(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)


class MultirotorSensors:
    def __init__(self, instance):
        super().__init__()
        if instance == None:
            self.acc = MRVector3(None)
            self.gyro = MRVector3(None)
            self.mag = MRVector3(None)
            return
        self.acc = MRVector3(instance.acc)
        self.gyro = MRVector3(instance.gyro)
        self.mag = MRVector3(instance.mag)

    def get_dict_data(self):
        return {
            "acc": self.acc.get_dict_data(),
            "gyro": self.gyro.get_dict_data(),
            "mag": self.mag.get_dict_data(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)


class MultirotorActuators:
    def __init__(self, instance):
        super().__init__()
        if instance == None:
            self.pwm = MRVector16(None)
            return
        self.pwm = MRVector16(instance.pwm)

    def get_dict_data(self):
        return {"pwm": self.pwm.get_dict_data()}

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)


class MultirotorGroundTruth:
    def __init__(self, groundTruth) -> None:
        if groundTruth == None:
            self.states = MultirotorStates(None)
            self.sensors = MultirotorSensors(None)
            self.actuators = MultirotorActuators(None)
            return
        self.states = MultirotorStates(groundTruth.states)
        self.sensors = MultirotorSensors(groundTruth.sensors)
        self.actuators = MultirotorActuators(groundTruth.actuators)

    def get_dict_data(self):
        return {
            "states": self.states.get_dict_data(),
            "sensors": self.sensors.get_dict_data(),
            "actuators": self.actuators.get_dict_data(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)
