import math
from random import *
from util.vec3 import vec3
from util import point3

class perlin:
    point_count = 256
    def __init__(self):
        self.randvec = [vec3.random(-1, 1) for _ in range(self.point_count)]
        
        self.perm_x = [0] * self.point_count
        self.perm_y = [0] * self.point_count
        self.perm_z = [0] * self.point_count
        
        self._perlin_generate_perm(self.perm_x)
        self._perlin_generate_perm(self.perm_y)
        self._perlin_generate_perm(self.perm_z)

    def noise(self, p: point3) -> float:
        u = p.x - math.floor(p.x)
        v = p.y - math.floor(p.y)
        w = p.z - math.floor(p.z)

        i = int(math.floor(p.x))
        j = int(math.floor(p.y))
        k = int(math.floor(p.z))

        c = [
            [[vec3(0, 0, 0), vec3(0, 0, 0)], [vec3(0, 0, 0), vec3(0, 0, 0)]],
            [[vec3(0, 0, 0), vec3(0, 0, 0)], [vec3(0, 0, 0), vec3(0, 0, 0)]]
        ]

        for di in range(2):
            for dj in range(2):
                for dk in range(2):
                    c[di][dj][dk] = self.randvec[
                        self.perm_x[(i + di) & 255] ^
                        self.perm_y[(j + dj) & 255] ^
                        self.perm_z[(k + dk) & 255]
                    ]

        return self._perlin_interp(c, u, v, w)

    @staticmethod
    def _perlin_generate_perm(p: list[int]) -> None:
        for i in range(perlin.point_count):
            p[i] = i
        
        perlin._permute(p, perlin.point_count)
        
    @staticmethod
    def _permute(p: list[int], n: int) -> None:
        for i in range(n-1, 0, -1):
            target = randint(0, i)
            p[i], p[target] = p[target], p[i]
      
    @staticmethod
    def _perlin_interp(c: list[list[list[vec3]]], u: float, v: float, w: float) -> float:
        uu = u * u * (3 - 2 * u)
        vv = v * v * (3 - 2 * v)
        ww = w * w * (3 - 2 * w)      
        accum = 0.0

        for i in range(2):
            for j in range(2):
                for k in range(2):
                    weight_v = vec3(u - i, v - j, w - k)
                    accum +=  (i*uu + (1-i)*(1-uu)) \
                            * (j*vv + (1-j)*(1-vv)) \
                            * (k*ww + (1-k)*(1-ww)) \
                            * c[i][j][k].dot(weight_v)
        return accum
    
    def turb(self, p: point3, depth: int = 7) -> float:
        accum = 0.0
        temp_p = p.copy()
        weight = 1.0

        for _ in range(depth):
            accum += weight * self.noise(temp_p)
            weight *= 0.5
            temp_p = temp_p * 2.0

        return abs(accum)