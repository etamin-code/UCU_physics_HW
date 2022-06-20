from typing import Tuple
from vectors import Vector
from numpy import pi, exp
from random import randint, random


class Cell:
    mass = 1
    sigma = 1
    epsilon = 1
    kB = 1
    r_max = 2.5 * sigma

    def __init__(self, xyz: Tuple[float, float, float],
                 sxyz: Tuple[float, float, float] = (-1, -1, -1),
                 T: float = 273):
        self.coordinates: Vector = Vector(*xyz)
        self.T = T
        if sxyz == (-1, -1, -1):
            self.speed = self.generate_maxvell_velo()
        else:
            self.speed: Vector = Vector(*sxyz)
        self.force: Vector = Vector(0, 0, 0)
        self.analytic_force: Vector

    def __copy__(self):
        return Cell(self.coordinates.copy(), self.speed.copy())

    def __eq__(self, other):
        return self.coordinates == other.coordinates

    def __hash__(self):
        return hash(self.coordinates)

    def generate_maxvell_velo(self):
        m = self.mass
        kB = self.kB
        T = self.T
        avg_v = (2 * kB * T / m) ** 0.5
        max_pdf = m/(2*pi*kB*T)**1.5 * 4*pi * avg_v**2 * exp(-m*avg_v**2/(2*kB*T))
        while True:
            v = avg_v * exp(randint(0, 100) / 50)
            pdf = m/(2*pi*kB*T)**1.5 * 4*pi * v**2 * exp(-m*v**2/(2*kB*T))
            if random() < pdf / max_pdf:
                break
        v_x, v_y, v_z = random() * 2 - 1, random() * 2 - 1, random() * 2 - 1
        norm = (v_x ** 2 + v_y ** 2 + v_z ** 2) ** 0.5
        v_x, v_y, v_z = v * v_x / norm, v * v_y / norm, v * v_z / norm
        return Vector(v_x, v_y, v_z)


    def distance(self, other):
        return abs(other.coordinates - self.coordinates)


    def holographic_distance(self, other, box_size):
        coords = self.coordinates
        other_coords = other.coordinates
        holo_x, holo_y, holo_z = other_coords.x, other_coords.y, other_coords.z

        cur_dif = abs(other_coords.x - coords.x)
        if coords.x > other_coords.x:
            new_holo = other_coords.x + box_size.x
            if abs(new_holo - coords.x) < cur_dif:
                holo_x = new_holo
        else:
            new_holo = other_coords.x - box_size.x
            if abs(new_holo - coords.x) < cur_dif:
                holo_x = new_holo

        cur_dif = abs(other_coords.y - coords.y)
        if coords.y > other_coords.y:
            new_holo = other_coords.y + box_size.y
            if abs(new_holo - coords.y) < cur_dif:
                holo_y = new_holo
        else:
            new_holo = other_coords.y - box_size.y
            if abs(new_holo - coords.y) < cur_dif:
                holo_y = new_holo

        cur_dif = abs(other_coords.z - coords.z)

        if coords.z > other_coords.z:
            new_holo = other_coords.z + box_size.z
            if abs(new_holo - coords.z) < cur_dif:
                holo_z = new_holo
        else:
            new_holo = other_coords.z - box_size.z
            if abs(new_holo - coords.z) < cur_dif:
                holo_z = new_holo

        holo_coord = Vector(holo_x, holo_y, holo_z)
        return abs(holo_coord - coords), holo_coord
