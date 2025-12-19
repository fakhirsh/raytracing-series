from .vec3 import vec3

class Ray:
    def __init__(self, origin: vec3, direction: vec3):
        self._origin = origin
        self._dir = direction

    @property
    def origin(self) -> vec3:
        return self._origin

    @property
    def direction(self) -> vec3:
        return self._dir

    def at(self, t: float) -> vec3:
        return self.origin + t * self.direction