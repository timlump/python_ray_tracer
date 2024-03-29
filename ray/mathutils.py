import math

class Vec3:

    def __init__(self, x, y, z):
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __add__(self, other):
        if type(other) is Vec3:    
            return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            return Vec3(self.x + other, self.y + other, self.z + other)

    def __sub__(self, other):
        if type(other) is Vec3:
            return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            return Vec3(self.x - other, self.y - other, self.z - other)

    def __mul__(self, other):
        if type(other) is Vec3:    
            return Vec3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            return Vec3(self.x * other, self.y * other, self.z * other)

    def __div__(self, other):
        if type(other) is Vec3:
            return Vec3(self.x / other.x, self.y / other.y, self.z / other.z)
        else:
            return Vec3(self.x / other, self.y / other, self.z / other)

    def __getitem__(self, item):
        if item == 0:
            return self.x
        elif item == 1:
            return self.y
        elif item == 2:
            return self.z
        else:
             raise IndexError("Index should be between 0 and 2")

    def __setitem__(self, key, value):
        if key == 0:
            self.x = value
        elif key == 1:
            self.y = value
        elif key == 2:
            self.z = value
        else:
            raise IndexError("Index should be between 0 and 2")

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) +" z: " + str(self.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z*other.z

    def cross(self, other):
        cx = self.y * other.z - self.z * other.y
        cy = self.z * other.x - self.x * other.z
        cz = self.x * other.y - self.y * other.x
        return Vec3(cx,cy,cz)

    def magnitude(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def normalize(self):
        mag = self.magnitude()
        return Vec3(self.x / mag, self.y / mag, self.z / mag)
    
    def clamp(self, min_value, max_value):
        
        result = Vec3(self.x, self.y, self.z)
        
        if result.x > max_value : result.x = max_value
        if result.y > max_value : result.y = max_value
        if result.z > max_value : result.z = max_value
            
        if result.x < min_value : result.x = min_value
        if result.y < min_value : result.y = min_value
        if result.z < min_value : result.z = min_value
        
        return result