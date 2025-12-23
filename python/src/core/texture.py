
from abc import ABC, abstractmethod
from util import color, point3


class texture(ABC):
    @abstractmethod
    def value(self, u: float, v: float, p: point3) -> color:
        pass

class solid_color(texture):
    
    @classmethod
    def from_color(cls, albedo: color) -> "solid_color":
        instance = cls()
        instance.albedo = albedo
        return instance

    @classmethod
    def from_rgb(cls, red: float, green: float, blue: float) -> "solid_color":
        instance = cls()
        instance.albedo = color(red, green, blue)
        return instance

    def value(self, u: float, v: float, p: point3) -> color:
        return self.albedo