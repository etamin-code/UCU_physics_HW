import numpy as np

from atoms import Cell
from vectors import Vector


def projection(val: float, axes: float, vector: Vector) -> float:
    return val * (axes / np.sqrt(vector.x ** 2 +
                                 vector.y ** 2 +
                                 vector.z ** 2))


def lj_force(r, epsilon, sigma) -> float:
    return 48 * epsilon * np.power(sigma, 12) / np.power(r, 13) \
           - 24 * epsilon * np.power(sigma, 6) / np.power(r, 7)


def find_pos(cell: Cell, dt: float, box_size: Vector) -> Vector:
    new_coords = cell.coordinates + cell.speed * dt + cell.force / cell.mass * (
            dt * dt * 0.5)
    for i in range(3):
        if new_coords[i] < 0:
            new_coords.set_value(i, new_coords[i] + box_size[i])
        if new_coords[i] > box_size[i]:
            new_coords.set_value(i, new_coords[i] - box_size[i])
    return new_coords



def find_velo(cell: Cell, dt: float) -> Vector:
    return cell.speed + cell.force / cell.mass * dt


def find_force(cell_1: Cell, cell_2: Cell, holo_coord=None) -> Vector:
    if holo_coord is not None:
        vr = cell_1.coordinates - holo_coord
    else:
        vr = cell_1.coordinates - cell_2.coordinates
    r = abs(vr)  # absolute distance between cells
    abs_force = lj_force(r, Cell.epsilon, Cell.sigma)
    return Vector(
        projection(abs_force, vr.x, vr),
        projection(abs_force, vr.y, vr),
        projection(abs_force, vr.z, vr)
    )


def get_lj_u(cell_1: Cell, cell_2: Cell):
    vr = cell_1.coordinates - cell_2.coordinates
    r = abs(vr)
    return 4 * cell_1.epsilon * (np.power(cell_1.sigma / r, 12)  - np.power(cell_1.sigma / r, 6))
