import pygame
import math
from mathutils import Vec3

MAX_RAY_DEPTH = 3

WIDTH = 320
HEIGHT = 240

BACKGROUND_COLOUR = Vec3(0,0,0)

scene_objects = []

class Material:
    surface_colour = Vec3(1.0,1.0,1.0)
    emission_colour = Vec3(0.0,0.0,0.0)
    
    def is_light(self):
        return self.emission_colour.magnitude() > 0.0

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
    
def get_intersecting_object(origin, direction):
    tnear = float("inf")
    scene_object_index = -1
    
    for idx,scene_object in enumerate(scene_objects):
        is_intersecting, t0, t1 = scene_object.intersect(origin, direction)
        if is_intersecting:
            if t0 < 0.0:
                t0 = t1
            if t0 < tnear:
                tnear = t0
                scene_object_index = idx
    
    return scene_object_index, tnear

def trace(origin, direction, depth):

    idx, tnear = get_intersecting_object(origin, direction)

    if idx == -1:
        return BACKGROUND_COLOUR
    
    bias = -0.01
    
    phit = origin + direction*(tnear + bias)
    nhit = (phit - scene_objects[idx].pos).normalize()
    
    surface_colour = Vec3(0,0,0)
    if scene_objects[idx].material.is_light():
        light_intensity = 1.0/tnear
        
        if light_intensity > 1.0: light_intensity = 1.0
        if light_intensity < 0.0: light_intensity = 0.0
        
        return scene_objects[idx].material.surface_colour * scene_objects[idx].material.emission_colour * (1.0/tnear)
    
    for current_idx, scene_object in enumerate(scene_objects):
        if scene_object.material.is_light():
            light_dir = scene_object.pos - phit
            light_dist = light_dir.magnitude()
            light_dir = light_dir.normalize()
            
            shadow_ray_idx, tnear = get_intersecting_object(phit, light_dir)
            if shadow_ray_idx == current_idx:
                object_colour = scene_objects[idx].material.surface_colour
                light_colour = scene_objects[shadow_ray_idx].material.emission_colour
                
                light_intensity = nhit.dot(light_dir)*(1.0/light_dist)
                
                if light_intensity > 1.0: light_intensity = 1.0
                if light_intensity < 0.0: light_intensity = 0.0
                
                surface_colour += (object_colour*light_colour)*light_intensity
    
    return surface_colour

sphere_material = Material()
sphere_material.surface_colour = Vec3(1.0,1.0,1.0)

scene_objects.append(Sphere(Vec3(-10,0,-100), 5, sphere_material))
scene_objects.append(Sphere(Vec3(10,0,-100),5,sphere_material))
scene_objects.append(Sphere(Vec3(0,0,-80), 5,sphere_material))
scene_objects.append(Sphere(Vec3(0,0,-150), 50,sphere_material))

light_material = Material()
light_material.emission_colour = Vec3(50.0,0.0,0.0)
light_material.surface_colour = Vec3(1.0,1.0,1.0)

scene_objects.append(Sphere(Vec3(10,-10,-50),2,light_material))

pygame.init()
game_display = pygame.display.set_mode((WIDTH,HEIGHT))

def render(width,height,fov):
    aspect_ratio = width / float(height)
    angle = math.tan(math.radians(fov / 2.0))
    inv_width = 1.0 / width
    inv_height = 1.0 / height

    for y in range(height):
        for x in range(width):
            xx = (2 * ((x + 0.5) * inv_width) - 1) * angle * aspect_ratio
            yy = (1 - 2 * ((y + 0.5) * inv_height)) * angle

            ray = Vec3(xx, yy, -1).normalize()
            
            rgb = trace(Vec3(0,0,0), ray, 0)
            
            rgb = rgb.clamp(0.0, 1.0)

            game_display.set_at((x,y), (int(rgb.x * 255), int(rgb.y * 255), int(rgb.z * 255)))

pygame_quitted = False

clock = pygame.time.Clock()

running = True
while running:
    clock.tick(5)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    render(WIDTH,HEIGHT,30)
    pygame.display.flip()
    
    x+= 1.0

pygame.quit()

