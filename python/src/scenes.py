from core.material import *
from util import *
from core import *
from math import sqrt, cos, pi
import random

def vol1_final_scene() -> hittable_list:
    world = hittable_list()

    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(Sphere(point3(0, -1000, 0), 1000, ground_material))

    for a in range(-11, 11):
        for b in range(-11, 11):
            choose_mat = random.uniform(0, 1)
            center = point3(a + 0.9 * random.uniform(0, 1), 0.2, b + 0.9 * random.uniform(0, 1))

            if (center - point3(4, 0.2, 0)).length() > 0.9:
                sphere_material = None

                if choose_mat < 0.8:
                    # diffuse
                    albedo = color.random() * color.random()
                    sphere_material = lambertian(albedo)
                    world.add(Sphere(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = color.random(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(Sphere(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = dielectric(1.5)
                    world.add(Sphere(center, 0.2, sphere_material))

    material1 = dielectric(1.5)
    world.add(Sphere(point3(0, 1, 0), 1.0, material1))

    material2 = lambertian(color(0.4, 0.2, 0.1))
    world.add(Sphere(point3(-4, 1, 0), 1.0, material2))

    material3 = metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere(point3(4, 1, 0), 1.0, material3))

    return world