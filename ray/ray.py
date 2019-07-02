import math
from mathutils import Vec3

from PIL import Image

MAX_RAY_DEPTH = 3

BACKGROUND_COLOUR = (0,0,0)

scene_objects = []

class Material:
    surface_colour = (255,255,255)
    emission_colour = (0,0,0)

class SceneObject:
    def __init__(self, pos):
        self.pos = pos

    def intersect(self, ray_origin, ray_dir):
        return False, float("inf"),float("inf")

class Sphere(SceneObject):
    def __init__(self, pos, radius, material = None):
        SceneObject.__init__(self, pos)
        self.radius = radius
        self.radius2 = radius*radius
        if material == None:
            self.material = Material()

    def intersect(self, ray_origin, ray_dir):
        t0 = float("inf")
        t1 = float("inf")

        L = self.pos - ray_origin
        tca = L.dot(ray_dir)
        d2 = L.dot(L) - tca*tca
        if d2 > self.radius2:
            return False, t0, t1
        thc = math.sqrt(self.radius2 - d2)
        t0 = tca - thc
        t1 = tca + thc

        if t0 > t1:
            temp = t0
            t0 = t1
            t1 = temp

        if t0 < 0:
            t0 = t1
            if t0 < 0:
                return False, t0, t1

        return True, t0, t1

def trace(origin, direction, depth):
    tnear = float("inf")

    intersected_object = None

    for scene_object in scene_objects:
        is_intersecting, t0, t1 = scene_object.intersect(origin, direction)
        if is_intersecting:
            if t0 < 0.0:
                t0 = t1
            if t0 < tnear:
                tnear = t0
                intersected_object = scene_object

    if intersected_object == None:
        return BACKGROUND_COLOUR

    surface_colour = intersected_object.material.surface_colour

    return surface_colour

scene_objects.append(Sphere(Vec3(0,0,-100),5))

def render(width,height,fov):
    aspect_ratio = width / float(height)
    angle = math.tan(math.radians(fov / 2.0))
    inv_width = 1.0 / width
    inv_height = 1.0 / height

    img = Image.new('RGB', (width, height), "black")
    pixels = img.load()

    for y in range(height):
        for x in range(width):
            xx = (2 * ((x + 0.5) * inv_width) - 1) * angle * aspect_ratio
            yy = (1 - 2 * ((y + 0.5) * inv_height)) * angle

            ray = Vec3(xx, yy, -1).normalize()

            pixels[x,y] = trace(Vec3(0,0,0), ray, 0)

    img.save('result.png')

render(320,240,30)

