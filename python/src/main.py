
from core.material import *
from scenes import vol1_final_scene
from util import *
from core import *
import cProfile
import pstats

#------------------------------------------------------------------------

def main():
    world = vol1_final_scene()

    cam = camera()

    cam.aspect_ratio = 16.0 / 9.0
    cam.img_width = 200
    cam.samples_per_pixel = 20
    cam.max_depth = 10

    cam.vfov = 20
    cam.lookfrom = point3(13, 2, 3)
    cam.lookat = point3(0, 0, 0)
    cam.vup = vec3(0, 1, 0)

    cam.defocus_angle = 0.6
    cam.focus_distance = 10.0

    cam.render(world)

    #------------------------------------------------------------------------

if __name__ == "__main__":
    profiler = cProfile.Profile()
    profiler.enable()

    main()

    profiler.disable()

    # Save profile data to file for visualization tools
    profiler.dump_stats('profile_output.prof')

    # Print profiling results to console
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')

    print("\n" + "="*80)
    print("PROFILING RESULTS - Top 30 functions by cumulative time")
    print("="*80)
    stats.print_stats(30)

    print("\n" + "="*80)
    print("PROFILING RESULTS - Top 30 functions by total time")
    print("="*80)
    stats.sort_stats('tottime')
    stats.print_stats(30)