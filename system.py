from typing import Set

from atoms import Cell
from find_forces import find_force, find_velo, find_pos, get_lj_u
from vectors import Vector


class System:
    def __init__(self, cells: Set[Cell], step: float, size: Vector):
        self.size = size
        self.cells: Set[Cell] = cells
        self.step = step
        self.epoch = 0
        self.U = {self.epoch: 0}
        self.U[self.epoch] = self.get_U()
        self.K = {self.epoch: 0}
        self.K[self.epoch] = self.get_K()

        self.W = {self.epoch: self.U[self.epoch] + self.K[self.epoch]}


    def update_coordinates(self, elem: Cell):
        elem.coordinates = find_pos(elem, self.step, self.size)

    def update_velocity(self, elem: Cell):

        elem.speed = find_velo(elem, self.step)

    def update_forces(self):

        element: Cell
        element1: Cell
        element2: Cell
        for element in self.cells:
            element.force = Vector(.0, .0, .0)

        for element1 in self.cells:
            for element2 in self.cells:
                if element1 == element2:
                    continue
                if element2.distance(element1) <= element2.r_max:
                    force = find_force(element1, element2)
                    element1.force += force

                else:
                    dist, holo_coord = element2.holographic_distance(element1, self.size)
                    if dist <= element2.r_max:
                        force = find_force(element1, element2, holo_coord)
                        element1.force += force


    def next_period_step(self):
        """
        Update the forces projections in cells
        """
        self.epoch += 1
        self.update_forces()
        element: Cell
        for element in self.cells:
            self.update_coordinates(element)
            self.update_velocity(element)
        self.U[self.epoch] = self.get_U()
        self.K[self.epoch] = self.get_K()
        self.W[self.epoch] = self.U[self.epoch] + self.K[self.epoch]

    def get_U(self):
        if self.epoch in self.U:
            return self.U[self.epoch]
        U = 0
        cells_list = list(self.cells)
        for i in range(len(cells_list) - 1):
            for j in range(i+1, len(cells_list)):
                U += get_lj_u(cells_list[i], cells_list[j])
        return U

    def get_K(self):
        if self.epoch in self.K:
            return self.K[self.epoch]
        K = 0
        for cell in self.cells:
            K += cell.mass * abs(cell.speed) ** 2 / 2
        return K

