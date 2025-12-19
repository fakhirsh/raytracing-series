import sys
from core import hittable, hit_record, interval
from util import point3, vec3, color, write_color, Ray, random_on_hemisphere
from random import random

class camera:
    aspect_ratio = 1.0
    img_width = 100
    samples_per_pixel = 10

    def __init__(self):
        pass

    def initialize(self):
        # Calculate the image height, and ensure that it's at least 1.
        self.img_height = 1 if int(self.img_width / self.aspect_ratio) < 1 else int(self.img_width / self.aspect_ratio)
        self.center = point3(0, 0, 0)
        
        self.pixel_samples_scale = 1.0 / self.samples_per_pixel

        focal_length = 1.0

        # Viewport widths less than one are ok since they are real valued.
        viewport_height = 2.0
        viewport_width = viewport_height * (self.img_width / self.img_height)
        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        viewport_u = vec3(viewport_width, 0, 0)
        viewport_v = vec3(0, -viewport_height, 0)
        # Calculate the horizontal and vertical delta vectors from pixel to pixel.
        self.delta_u = viewport_u / self.img_width
        self.delta_v = viewport_v / self.img_height
        # Calculate the location of the upper left pixel.
        viewport_upper_left = self.center - vec3(0, 0, focal_length) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.delta_u + self.delta_v)

    def ray_color(self, ray: Ray, world: hittable) -> color:
        rec = hit_record()
        if world.hit(ray, interval(0.001, float('inf')), rec):
            direction = random_on_hemisphere(rec.normal)
            return 0.5 * self.ray_color(Ray(rec.p, rec.normal + direction), world)
        
        unit_dir = ray.direction.unit_vector()
        a = 0.5 * (unit_dir.y + 1.0)
        return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)

    def sample_square(self) -> vec3:
        return vec3(random() - 0.5, random() - 0.5, 0)

    def get_ray(self, w: int, h: int) -> Ray:
        offset = self.sample_square()
        psample = self.pixel00_loc \
                    + (w + offset.x) * self.delta_u \
                    + (h + offset.y) * self.delta_v
        ray_origin = self.center
        ray_direction = psample - ray_origin
        return Ray(ray_origin, ray_direction)

    def render(self, world: hittable):
        self.initialize()

        print(f"P3\n{self.img_width} {self.img_height}\n255")
        for h in range(self.img_height):
            # Progress indicator: print to stderr and flush
            sys.stderr.write(f"\rScanlines remaining: {self.img_height - h} ")
            sys.stderr.flush()
            
            for w in range(self.img_width):
                
                pcolor = color(0,0,0)
                for s in range(self.samples_per_pixel):
                    r = self.get_ray(w, h)
                    pcolor += self.ray_color(r, world)
                
                write_color(self.pixel_samples_scale * pcolor)

        # Clear the progress line after completion
        sys.stderr.write("\r" + " " * 30 + "\r")
        sys.stderr.flush()

        print("Done.", file=sys.stderr)
