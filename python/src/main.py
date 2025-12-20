
from core.material import *
from util import *
from core import *
from math import sqrt, cos, pi

#------------------------------------------------------------------------

def main():
    
    # World setup
    world = hittable_list()

    material_ground = lambertian(color(0.8, 0.8, 0.0))
    material_center = lambertian(color(0.1, 0.2, 0.5))
    material_left   = dielectric(1.5)
    material_bubble = dielectric(1.0/1.5)
    material_right  = metal(color(0.8, 0.6, 0.2), 1.0)

    world.add(Sphere(point3( 0.0, -100.5, -1), 100, material_ground))
    world.add(Sphere(point3( 0.0, 0.0, -1.2), 0.5,  material_center))
    world.add(Sphere(point3(-1.0, 0.0, -1.0), 0.5,  material_left))
    world.add(Sphere(point3(-1.0, 0.0, -1.0), 0.4,  material_bubble))
    world.add(Sphere(point3( 1.0, 0.0, -1.0), 0.5,  material_right))
    # world.add(KleinBottle(point3(0.0, 0.0, -1.0), 0.5, metal(color(0.7, 0.3, 0.3)), u_steps=5, v_steps=5))

    # R = cos(pi / 4)
    # material_left = lambertian(color(0, 0, 1))
    # material_right = lambertian(color(1, 0, 0))

    # world.add(Sphere(point3(-R, 0, -1), R, material_left))
    # world.add(Sphere(point3(R, 0, -1), R, material_right))

    cam = camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.img_width = 400
    cam.samples_per_pixel = 50
    cam.max_depth = 10
    
    cam.vfov = 20.0
    cam.lookfrom = point3(-2,2,1)
    cam.lookat = point3(0,0,-1)
    cam.vup = vec3(0,1,0)

    cam.render(world)

    #------------------------------------------------------------------------

if __name__ == "__main__":
    main()