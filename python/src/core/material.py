
from abc import ABC, abstractmethod
from random import random
from util import Ray, color, random_unit_vector, reflect, refract
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
    def __init__(self, albedo: color, fuzz: float):
        self.albedo = albedo
        self.fuzz = fuzz if fuzz < 1.0 else 1.0

    def scatter(self, r_in: Ray, rec: 'hit_record', attenuation: color, scattered: Ray) -> bool:
        scatter_direction = reflect(r_in.direction, rec.normal) + self.fuzz * random_unit_vector()
        scattered.origin = rec.p
        scattered.direction = scatter_direction
        attenuation.x = self.albedo.x
        attenuation.y = self.albedo.y
        attenuation.z = self.albedo.z
        return True
    
class dielectric(material):
    def __init__(self, index_of_refraction: float):
        self.ir = index_of_refraction

    def scatter(self, r_in: Ray, rec: 'hit_record', attenuation: color, scattered: Ray) -> bool:
        attenuation.x = 1.0
        attenuation.y = 1.0
        attenuation.z = 1.0

        refraction_ratio = (1.0 / self.ir) if rec.front_face else self.ir

        unit_direction = r_in.direction.unit_vector()
        cos_theta = min(-unit_direction.dot(rec.normal), 1.0)
        sin_theta = (1.0 - cos_theta * cos_theta) ** 0.5

        cannot_refract = refraction_ratio * sin_theta > 1.0
        direction = None

        if cannot_refract or self._reflectance(cos_theta, refraction_ratio) > random():
            direction = reflect(unit_direction, rec.normal)
        else:
            direction = refract(unit_direction, rec.normal, refraction_ratio)

        scattered.origin = rec.p
        scattered.direction = direction
        return True
    
    def _reflectance(self, cosine: float, ref_idx: float) -> float:
        r0 = (1 - ref_idx) / (1 + ref_idx)
        r0 = r0 * r0
        return r0 + (1 - r0) * ((1 - cosine) ** 5)