import json
from ..messages.helicopter_generated import FB_Vec3MsgT, FB_HeliStatesMsgT


class HeliVector3(FB_Vec3MsgT):
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


class HelicopterStates(FB_HeliStatesMsgT):
    def __init__(self, instance):
        super().__init__()
        if instance == None:
            self.pos = HeliVector3(None)
            self.vel = HeliVector3(None)
            return
        self.pos = HeliVector3(instance.pos)
        self.vel = HeliVector3(instance.vel)

    def get_dict_data(self):
        return {
            "pos": self.pos.get_dict_data(),
            "vel": self.vel.get_dict_data(),
        }

    def __str__(self) -> str:
        return json.dumps(self.get_dict_data(), indent=4, sort_keys=True)
