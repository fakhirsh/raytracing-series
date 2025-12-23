from core.material import *
from util import *
from core import *
from math import sqrt, cos, pi
import random

def vol1_sec95() -> hittable_list:
    ground_material = lambertian(color(0.5, 0.5, 0.5))
    shpere_material = lambertian(color(0.8, 0.3, 0.3))
    world = hittable_list()
    obj = Sphere.stationary(point3(0,0,-1), 0.5, shpere_material)
    world.add(obj)
    obj = Sphere.stationary(point3(0,-100.5,-1), 100, ground_material)
    world.add(obj)
    return world

def vol1_final_scene() -> hittable_list:
    world = hittable_list()

    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(Sphere.stationary(point3(0, -1000, 0), 1000, ground_material))

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
                    center2 = center + vec3(0, random.uniform(0, 0.5), 0)
                    world.add(Sphere.stationary(center, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = color.random(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(Sphere.stationary(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = dielectric(1.5)
                    world.add(Sphere.stationary(center, 0.2, sphere_material))
    material1 = dielectric(1.5)
    world.add(Sphere.stationary(point3(0, 1, 0), 1.0, material1))

    material2 = lambertian(color(0.4, 0.2, 0.1))
    world.add(Sphere.stationary(point3(-4, 1, 0), 1.0, material2))

    material3 = metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere.stationary(point3(4, 1, 0), 1.0, material3))

    return world


def vol2_sec26_scene() -> hittable_list:
    world = hittable_list()

    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(Sphere.stationary(point3(0, -1000, 0), 1000, ground_material))

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
                    center2 = center + vec3(0, random.uniform(0, 0.5), 0)
                    world.add(Sphere.moving(center, center2, 0.2, sphere_material))
                elif choose_mat < 0.95:
                    # metal
                    albedo = color.random(0.5, 1)
                    fuzz = random.uniform(0, 0.5)
                    sphere_material = metal(albedo, fuzz)
                    world.add(Sphere.stationary(center, 0.2, sphere_material))
                else:
                    # glass
                    sphere_material = dielectric(1.5)
                    world.add(Sphere.stationary(center, 0.2, sphere_material))

    material1 = dielectric(1.5)
    world.add(Sphere.stationary(point3(0, 1, 0), 1.0, material1))

    material2 = lambertian(color(0.4, 0.2, 0.1))
    world.add(Sphere.stationary(point3(-4, 1, 0), 1.0, material2))

    material3 = metal(color(0.7, 0.6, 0.5), 0.0)
    world.add(Sphere.stationary(point3(4, 1, 0), 1.0, material3))

    return world


def vol2_sec26_scene_simple() -> hittable_list:
    world = hittable_list()

    # Ground
    ground_material = lambertian(color(0.5, 0.5, 0.5))
    world.add(Sphere.stationary(point3(0, -1000, 0), 1000, ground_material))

    # Moving diffuse sphere (left)
    moving_material = lambertian(color(0.8, 0.3, 0.3))
    center1 = point3(-2, 0.5, 0)
    center2 = center1 + vec3(0, 0.3, 0)
    world.add(Sphere.moving(center1, center2, 0.5, moving_material))

    # Static glass sphere (center)
    glass_material = dielectric(1.5)
    world.add(Sphere.stationary(point3(0, 0.5, 0), 0.5, glass_material))

    # Static metal sphere (right)
    metal_material = metal(color(0.7, 0.6, 0.5), 0.1)
    world.add(Sphere.stationary(point3(2, 0.5, 0), 0.5, metal_material))

    # Moving diffuse sphere (behind)
    moving_material2 = lambertian(color(0.3, 0.3, 0.8))
    center3 = point3(0, 0.3, -2)
    center4 = center3 + vec3(0, 0.4, 0)
    world.add(Sphere.moving(center3, center4, 0.3, moving_material2))

    # Additional moving diffuse sphere (front left)
    moving_material3 = lambertian(color(0.3, 0.8, 0.3))
    center5 = point3(-1, 0.3, 1)
    center6 = center5 + vec3(0, 0.4, 0)
    world.add(Sphere.moving(center5, center6, 0.3, moving_material3))

    # Additional moving diffuse sphere (front right)
    moving_material4 = lambertian(color(0.8, 0.8, 0.3))
    center7 = point3(1, 0.3, 1.5)
    center8 = center7 + vec3(0, 0.35, 0)
    world.add(Sphere.moving(center7, center8, 0.3, moving_material4))

    # Static glass sphere (smaller, right side)
    glass_material2 = dielectric(1.5)
    world.add(Sphere.stationary(point3(3, 0.3, -1), 0.3, glass_material2))

    # Static metal sphere (left side, shiny)
    metal_material2 = metal(color(0.9, 0.9, 0.9), 0.0)
    world.add(Sphere.stationary(point3(-3, 0.4, -0.5), 0.4, metal_material2))

    # Static metal sphere (back, bronze-ish)
    metal_material3 = metal(color(0.8, 0.5, 0.3), 0.3)
    world.add(Sphere.stationary(point3(0.5, 0.3, -3), 0.3, metal_material3))

    # Moving diffuse sphere (far left)
    moving_material5 = lambertian(color(0.7, 0.3, 0.7))
    center9 = point3(-3.5, 0.25, 1)
    center10 = center9 + vec3(0, 0.25, 0)
    world.add(Sphere.moving(center9, center10, 0.25, moving_material5))

    return world
