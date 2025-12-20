
from abc import ABC, abstractmethod
from util import Ray, color, random_unit_vector, reflect
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.hittable import hit_record

class material(ABC):
    @abstractmethod
    def scatter(self, r_in: Ray, rec: 'hit_record', attenuation: color, scattered: Ray) -> bool:
        return False

class lambertian(material):
    def __init__(self, albedo: color):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: 'hit_record', attenuation: color, scattered: Ray) -> bool:
        scatter_direction = rec.normal + random_unit_vector()
        if scatter_direction.near_zero():
            scatter_direction = rec.normal

        scattered.origin = rec.p
        scattered.direction = scatter_direction
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True
    
class metal(material):
    def __init__(self, albedo: color):
        self.albedo = albedo

    def scatter(self, r_in: Ray, rec: 'hit_record', attenuation: color, scattered: Ray) -> bool:
        scatter_direction = reflect(r_in.direction, rec.normal)
        scattered.origin = rec.p
        scattered.direction = scatter_direction
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True