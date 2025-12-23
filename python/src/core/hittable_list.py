from util import Ray
from .aabb import aabb
from .hittable import hittable, hit_record
from .interval import interval

class hittable_list(hittable):
    
    def __init__(self):
        self.objects = []
        self.bbox = aabb.from_intervals(interval.empty, interval.empty, interval.empty)

    def clear(self):
        self.objects = []

    def add(self, obj: hittable):
        self.objects.append(obj)
        self.bbox = aabb.from_aabbs(self.bbox, obj.bounding_box())

    def bounding_box(self) -> aabb:
        return self.bbox

    def hit(self, r: Ray, ray_t: interval, rec: hit_record) -> bool:
        temp_rec = hit_record()
        hit_anything = False
        closest_so_far = ray_t.max

        for obj in self.objects:
            if obj.hit(r, interval.from_floats(ray_t.min, closest_so_far), temp_rec):
                hit_anything = True
                closest_so_far = temp_rec.t
                rec.copy_from(temp_rec)

        return hit_anything