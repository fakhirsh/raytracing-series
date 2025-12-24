from .vec3 import vec3

class Ray:
    def __init__(self, origin: vec3, direction: vec3, tm: float = 0.0):
        self._origin = origin
        self._dir = direction
        self._time = tm

    @property
    def origin(self) -> vec3:
        return self._origin
    
    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float):
        self._time = value

    @origin.setter
    def origin(self, value: vec3):
        self._origin = value

    @property
    def direction(self) -> vec3:
        return self._dir

    @direction.setter
    def direction(self, value: vec3):
        self._dir = value

    def at(self, t: float) -> vec3:
        return self.origin + t * self.direction