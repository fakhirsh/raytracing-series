
from util import *
from core import *
from math import sqrt

#------------------------------------------------------------------------



def main():
    
    # World setup
    world = hittable_list()
    world.add(Sphere(point3(0, 0, -1), 0.5))
    world.add(Sphere(point3(0, -100.5, -1), 100))

    cam = camera()
    cam.aspect_ratio = 16.0 / 9.0
    cam.img_width = 400
    cam.samples_per_pixel = 10

    cam.render(world)

    #------------------------------------------------------------------------

if __name__ == "__main__":
    main()