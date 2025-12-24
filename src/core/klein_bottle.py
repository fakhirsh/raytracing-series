import math
from core.material import material
from util import vec3, point3, dot, Ray
from .hittable import hittable, hit_record
from .interval import interval

class KleinBottle(hittable):
    """
    Klein bottle implementation using figure-8 immersion parametric equations.

    Parametric equations (0 <= u < 2π, 0 <= v < 2π):
    x = (a + b*cos(u/2)*sin(v) - b*sin(u/2)*sin(2*v)) * cos(u)
    y = (a + b*cos(u/2)*sin(v) - b*sin(u/2)*sin(2*v)) * sin(u)
    z = b*sin(u/2)*sin(v) + b*cos(u/2)*sin(2*v)

    where a and b control the size and shape.
    """

    def __init__(self, center: point3, scale: float, mat: material, u_steps: int = 10, v_steps: int = 10):
        """
        Initialize Klein bottle.

        Args:
            center: Center position of the Klein bottle
            scale: Overall scale factor
            mat: Material for the surface
            u_steps: Number of subdivisions in u direction (higher = more accurate but slower)
            v_steps: Number of subdivisions in v direction (higher = more accurate but slower)
        """
        self.center = center
        self.scale = scale
        self.material = mat
        self.u_steps = u_steps
        self.v_steps = v_steps

        # Klein bottle parameters
        self.a = 2.0  # Major radius
        self.b = 1.0  # Minor radius

        # Pre-compute tessellation mesh for performance
        self._precompute_mesh()

    def _precompute_mesh(self):
        """Pre-compute tessellation mesh (vertices and normals) for performance."""
        du = (2.0 * math.pi) / self.u_steps
        dv = (2.0 * math.pi) / self.v_steps

        # Pre-compute all vertices in local coordinates
        self.vertices = []
        for i in range(self.u_steps + 1):
            row = []
            for j in range(self.v_steps + 1):
                u = i * du
                v = j * dv
                row.append(self._parametric_point_local(u, v))
            self.vertices.append(row)

        # Pre-compute normals at quad centers for better quality
        self.normals = []
        for i in range(self.u_steps):
            row = []
            for j in range(self.v_steps):
                u_mid = (i + 0.5) * du
                v_mid = (j + 0.5) * dv
                row.append(self._parametric_normal_local(u_mid, v_mid))
            self.normals.append(row)

    def _parametric_point_local(self, u: float, v: float) -> vec3:
        """Compute point on Klein bottle surface in local coordinates (no translation/scale)."""
        cos_u = math.cos(u)
        sin_u = math.sin(u)
        cos_u_half = math.cos(u / 2.0)
        sin_u_half = math.sin(u / 2.0)
        sin_v = math.sin(v)
        sin_2v = math.sin(2.0 * v)

        r = self.a + self.b * cos_u_half * sin_v - self.b * sin_u_half * sin_2v

        x = r * cos_u
        y = r * sin_u
        z = self.b * sin_u_half * sin_v + self.b * cos_u_half * sin_2v

        return vec3(x, y, z)

    def parametric_point(self, u: float, v: float) -> point3:
        """Compute point on Klein bottle surface given parameters u, v."""
        local_point = self._parametric_point_local(u, v)
        return self.center + self.scale * local_point

    def _parametric_normal_local(self, u: float, v: float) -> vec3:
        """Compute approximate normal in local coordinates using numerical derivatives."""
        epsilon = 0.001

        # Compute partial derivatives using central differences
        pu = (self._parametric_point_local(u + epsilon, v) - self._parametric_point_local(u - epsilon, v)) / (2.0 * epsilon)
        pv = (self._parametric_point_local(u, v + epsilon) - self._parametric_point_local(u, v - epsilon)) / (2.0 * epsilon)

        # Normal is cross product of partial derivatives
        normal = pu.cross(pv)
        return normal.unit_vector()

    def parametric_normal(self, u: float, v: float) -> vec3:
        """Compute approximate normal at parameter point (u, v) using numerical derivatives."""
        # For transformed geometry, normal direction stays the same (assuming uniform scaling)
        return self._parametric_normal_local(u, v)

    def hit(self, r: Ray, ray_t: interval, rec: hit_record) -> bool:
        """
        Ray-Klein bottle intersection using pre-computed tessellated mesh.
        This uses cached vertices and normals for performance.
        """
        closest_t = ray_t.max
        hit_anything = False

        # Check intersection with pre-computed tessellated surface
        for i in range(self.u_steps):
            for j in range(self.v_steps):
                # Get pre-computed vertices and transform to world space
                p00 = self.center + self.scale * self.vertices[i][j]
                p10 = self.center + self.scale * self.vertices[i + 1][j]
                p11 = self.center + self.scale * self.vertices[i + 1][j + 1]
                p01 = self.center + self.scale * self.vertices[i][j + 1]

                # Get pre-computed normal for this quad
                normal = self.normals[i][j]

                # Split quad into two triangles and test both
                # Triangle 1: p00, p10, p11
                t = self._intersect_triangle(r, p00, p10, p11, ray_t.min, closest_t)
                if t is not None and t < closest_t:
                    closest_t = t
                    rec.t = t
                    rec.p = r.at(t)
                    rec.set_face_normal(r, normal)
                    rec.material = self.material
                    hit_anything = True

                # Triangle 2: p00, p11, p01
                t = self._intersect_triangle(r, p00, p11, p01, ray_t.min, closest_t)
                if t is not None and t < closest_t:
                    closest_t = t
                    rec.t = t
                    rec.p = r.at(t)
                    rec.set_face_normal(r, normal)
                    rec.material = self.material
                    hit_anything = True

        return hit_anything

    def _intersect_triangle(self, ray: Ray, v0: point3, v1: point3, v2: point3,
                           t_min: float, t_max: float) -> float:
        """
        Möller-Trumbore ray-triangle intersection algorithm.
        Returns t value if intersection exists within [t_min, t_max], None otherwise.
        """
        epsilon = 1e-8

        edge1 = v1 - v0
        edge2 = v2 - v0
        h = ray.direction.cross(edge2)
        a = dot(edge1, h)

        # Ray is parallel to triangle
        if abs(a) < epsilon:
            return None

        f = 1.0 / a
        s = ray.origin - v0
        u = f * dot(s, h)

        if u < 0.0 or u > 1.0:
            return None

        q = s.cross(edge1)
        v = f * dot(ray.direction, q)

        if v < 0.0 or u + v > 1.0:
            return None

        # Compute t
        t = f * dot(edge2, q)

        if t > t_min and t < t_max:
            return t

        return None