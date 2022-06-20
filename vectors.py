from numpy import sqrt


class Vector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __abs__(self):
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, constant):
        self.x *= constant
        self.y *= constant
        self.z *= constant
        return self

    def __truediv__(self, constant):
        return Vector(self.x / constant, self.y / constant, self.z / constant)

    def __neg__(self):
        self.y = -self.y
        self.y = -self.y
        self.z = -self.z
        return self

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def __iadd__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z)

    def copy(self):
        return Vector(self.x, self.y, self.z)

    def __hash__(self):
        return hash(self.z + self.y + self.z)

    def __getitem__(self, index):
        if index < 0 or index > 2:
            print(f"index {index} is out of bond")
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        return self.z

    def __iter__(self):
        return [self[0], self[1], self[2]]

    def set_value(self, index, value):
        if index < 0  or index > 2:
            print("out of bonds")
            return -1
        if index == 0:
            self.x = value
        if index == 1:
            self.y = value
        if index == 2:
            self.z = value

