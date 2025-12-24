
from abc import ABC, abstractmethod
import math
from .interval import interval
from util.rtw_image import rtw_image
from util import color, point3
from .perlin import perlin


class texture(ABC):
    @abstractmethod
    def value(self, u: float, v: float, p: point3) -> color:
        pass
    
#----------------------------------------------------------------------------------

class solid_color(texture):
    
    @classmethod
    def from_color(cls, albedo: color) -> "solid_color":
        instance = cls()
        instance.albedo = albedo
        return instance

    @classmethod
    def from_rgb(cls, red: float, green: float, blue: float) -> "solid_color":
        instance = cls()
        instance.albedo = color(red, green, blue)
        return instance

    def value(self, u: float, v: float, p: point3) -> color:
        return self.albedo
    
#----------------------------------------------------------------------------------

class checker_texture(texture):

    @classmethod
    def from_textures(cls, scale: float, even: texture, odd: texture) -> "checker_texture":
        instance = cls()
        instance.inv_scale = 1.0 / scale
        instance.even = even
        instance.odd = odd
        return instance

    @classmethod
    def from_colors(cls, scale: float, c1: color, c2: color) -> "checker_texture":
        return cls.from_textures(scale, solid_color.from_color(c1), solid_color.from_color(c2))

    def value(self, u: float, v: float, p: point3) -> color:
        x_integer = math.floor(self.inv_scale * p.x)
        y_integer = math.floor(self.inv_scale * p.y)
        z_integer = math.floor(self.inv_scale * p.z)

        is_even = (x_integer + y_integer + z_integer) % 2 == 0

        return self.even.value(u, v, p) if is_even else self.odd.value(u, v, p)
    
#----------------------------------------------------------------------------------

class image_texture(texture):
    def __init__(self, filename: str):
        self.image = rtw_image.from_file(filename)
    
    def value(self, u: float, v: float, p: point3) -> color:
        # If we have no texture data, return solid cyan as a debugging aid
        
        if self.image.height() <= 0:
            return color(0, 1, 1)
        
        # Clamp input texture coordinates to [0,1] x [1,0]
        u = interval.from_floats(0, 1).clamp(u)
        v = 1.0 - interval.from_floats(0, 1).clamp(v)  # Flip V to image coordinates
        
        i = int(u * self.image.width())
        j = int(v * self.image.height())
        
        # Use float version directly to avoid the 1/255 scaling
        r, g, b = self.image.pixel_data_float(i, j)
        return color(r, g, b)
    
#----------------------------------------------------------------------------------

class noise_texture(texture):
    def __init__(self, scale: float = 1.0):
        self.noise = perlin()
        self.scale = scale
    
    def value(self, u: float, v: float, p: point3) -> color:
        return color(.5, .5, .5) * (1 + math.sin(self.scale * p.z + 10 * self.noise.turb(p, 7)))