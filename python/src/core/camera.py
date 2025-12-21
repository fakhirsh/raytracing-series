import math
import sys
from core import hittable, hit_record, interval
from util import point3, vec3, color, write_color, Ray, degrees_to_radians, dot, cross, normalize, random_in_unit_disk
from random import random

class camera:
    aspect_ratio = 1.0
    img_width = 100
    samples_per_pixel = 10
    max_depth = 10
    vfov = 90
    lookfrom = point3(0,0,0)
    lookat = point3(0,0,-1)
    vup = vec3(0,1,0)

    defocus_angle = 0.0
    focus_distance = 10.0

    def __init__(self):
        pass

    def initialize(self):
        # Calculate the image height, and ensure that it's at least 1.
        self.img_height = 1 if int(self.img_width / self.aspect_ratio) < 1 else int(self.img_width / self.aspect_ratio)
        self.center = point3(0, 0, 0)
        
        self.pixel_samples_scale = 1.0 / self.samples_per_pixel

        self.center = self.lookfrom
        # focal_length = (self.lookfrom - self.lookat).length()
        # Viewport widths less than one are ok since they are real valued.
        theta = degrees_to_radians(self.vfov)
        h = math.tan(theta / 2)
        viewport_height = 2.0 * h * self.focus_distance
        viewport_width = viewport_height * (self.img_width / self.img_height)

        w = normalize(self.lookfrom - self.lookat)
        u = normalize(cross(self.vup, w))
        v = cross(w, u)

        # Calculate the vectors across the horizontal and down the vertical viewport edges.
        viewport_u = viewport_width * u
        viewport_v = viewport_height * -v

        # Calculate the horizontal and vertical delta vectors from pixel to pixel.
        self.delta_u = viewport_u / self.img_width
        self.delta_v = viewport_v / self.img_height
        # Calculate the location of the upper left pixel.
        viewport_upper_left = self.center - (self.focus_distance * w) - viewport_u / 2 - viewport_v / 2
        self.pixel00_loc = viewport_upper_left + 0.5 * (self.delta_u + self.delta_v)

        defocus_radius = self.focus_distance * math.tan(degrees_to_radians(self.defocus_angle) / 2)
        self.defocus_disk_u = defocus_radius * u
        self.defocus_disk_v = defocus_radius * v

    def ray_color(self, ray: Ray, depth: int, world: hittable) -> color:
        if depth <= 0:
            return color(0, 0, 0)
        
        rec = hit_record()
        if world.hit(ray, interval(0.001, float('inf')), rec):
            scattered = Ray(point3(0,0,0), vec3(0,0,0))
            attenuation = color(0,0,0)
            if rec.material.scatter(ray, rec, attenuation, scattered):
                return attenuation * self.ray_color(scattered, depth - 1, world)
            return color(0,0,0)
        
        unit_dir = ray.direction.unit_vector()
        a = 0.5 * (unit_dir.y + 1.0)
        return (1.0 - a) * color(1.0, 1.0, 1.0) + a * color(0.5, 0.7, 1.0)

    def sample_square(self) -> vec3:
        return vec3(random() - 0.5, random() - 0.5, 0)

    def defocus_disk_sample(self) -> point3:
        p = random_in_unit_disk()
        return self.center + p.x * self.defocus_disk_u + p.y * self.defocus_disk_v

    def get_ray(self, w: int, h: int) -> Ray:
        offset = self.sample_square()
        psample = self.pixel00_loc \
                    + (w + offset.x) * self.delta_u \
                    + (h + offset.y) * self.delta_v
        ray_origin = self.center if self.defocus_angle <= 0.0 else self.defocus_disk_sample()
        ray_direction = psample - ray_origin
        ray_time = random()  # Time can be used for motion blur; here we just use a random time in [0,1)
        return Ray(ray_origin, ray_direction, ray_time)

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
                    pcolor += self.ray_color(r, self.max_depth, world)
                
                write_color(self.pixel_samples_scale * pcolor)

        # Clear the progress line after completion
        sys.stderr.write("\r" + " " * 30 + "\r")
        sys.stderr.flush()

        print("Done.", file=sys.stderr)
