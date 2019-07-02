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
    def __init__(self, pos, material = None):
        self.pos = pos
        if material == None:
            self.material = Material()
        else:
            self.material = material

    def intersect(self, ray_origin, ray_dir):
        return False, float("inf"),float("inf")

class Sphere(SceneObject):
    def __init__(self, pos, radius, material = None):
        SceneObject.__init__(self, pos, material)
        self.radius = radius
        self.radius2 = radius*radius
        

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
    
    phit = origin + direction*tnear
    nhit = (phit - intersected_object.pos).normalize()
    
    surface_colour = (0,0,0)
    
    for scene_object in scene_objects:
        if scene_object.material.emission_colour[0] > 0:
            light_dir = (scene_object.pos - phit).normalize()
            surface_colour = tuple( int(nhit.dot(light_dir)*x) for x in intersected_object.material.surface_colour)

    return surface_colour

sphere_material1 = Material()
sphere_material1.surface_colour = (255,0,0)
scene_objects.append(Sphere(Vec3(-10,0,-100), 5, sphere_material1))

sphere_material2 = Material()
sphere_material2.surface_colour = (0,255,0)
scene_objects.append(Sphere(Vec3(10,0,-100),5,sphere_material2))

light_material = Material()
light_material.emission_colour = (255,255,255)
light_material.surface_colour = (0,0,0)
scene_objects.append(Sphere(Vec3(20,20,-50),5,light_material))

count = 0

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
            
    filename = "sequence/result_" + str(count) + ".png"
    print(filename)
    img.save(filename)

for x in range(20):
    scene_objects[2].pos.x = -60.0 + 120.0*(x/20.0)
    render(640,480,30)
    count += 1

