from util import ray
from .hittable import hittable, hit_record
from util import *
from .material import material
from .aabb import aabb
from util import point3, vec3
from .interval import interval


class triangle(hittable):
    """Triangle primitive using three vertices."""

    def __init__(self, v0: point3, v1: point3, v2: point3, mat: material):
        """
        Create a triangle from three vertices.
        Vertices should be specified in counter-clockwise order when viewed from the front.
        """
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.mat = mat

        # Compute edges
        self.edge1 = v1 - v0
        self.edge2 = v2 - v0

        # Compute normal (counter-clockwise winding)
        n = vec3.cross(self.edge1, self.edge2)
        self.normal = n.unit_vector()

        self.set_bounding_box()

    def set_bounding_box(self):
        # Find min and max for each axis across the three vertices
        min_x = min(self.v0.x, self.v1.x, self.v2.x)
        max_x = max(self.v0.x, self.v1.x, self.v2.x)

        min_y = min(self.v0.y, self.v1.y, self.v2.y)
        max_y = max(self.v0.y, self.v1.y, self.v2.y)

        min_z = min(self.v0.z, self.v1.z, self.v2.z)
        max_z = max(self.v0.z, self.v1.z, self.v2.z)

        self.bbox = aabb.from_points(
            point3(min_x, min_y, min_z),
            point3(max_x, max_y, max_z)
        )
        # Pad for planar triangles
        self.bbox._pad_to_minimums()

    def bounding_box(self):
        return self.bbox

    def hit(self, r: ray, ray_t: interval, rec: hit_record) -> bool:
        """
        Ray-triangle intersection using Moller-Trumbore algorithm.
        """
        epsilon = 1e-8

        # Compute determinant
        h = vec3.cross(r.direction, self.edge2)
        det = vec3.dot(self.edge1, h)

        # Ray is parallel to triangle
        if abs(det) < epsilon:
            return False

        inv_det = 1.0 / det

        # Compute u parameter
        s = r.origin - self.v0
        u = inv_det * vec3.dot(s, h)

        if u < 0.0 or u > 1.0:
            return False

        # Compute v parameter
        q = vec3.cross(s, self.edge1)
        v = inv_det * vec3.dot(r.direction, q)

        if v < 0.0 or u + v > 1.0:
            return False

        # Compute t
        t = inv_det * vec3.dot(self.edge2, q)

        if not ray_t.contains(t):
            return False

        # We have a valid intersection
        rec.t = t
        rec.p = r.at(t)
        rec.set_face_normal(r, self.normal)
        rec.material = self.mat

        # Set barycentric coordinates as texture coordinates
        rec.u = u
        rec.v = v

        return True
