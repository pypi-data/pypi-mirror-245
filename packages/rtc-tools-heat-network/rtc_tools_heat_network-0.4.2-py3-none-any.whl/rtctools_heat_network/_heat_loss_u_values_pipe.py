import math
from typing import List, Tuple, Union

import numpy as np


def heat_loss_u_values_pipe(
    inner_diameter: float,
    insulation_thicknesses: Union[float, List[float], np.ndarray] = None,
    conductivities_insulation: Union[float, List[float], np.ndarray] = 0.033,
    conductivity_subsoil: float = 2.3,
    depth: float = 1.0,
    h_surface: float = 15.4,
    pipe_distance: float = None,
    neighbour: bool = True,
) -> Tuple[float, float]:
    """
    Calculate the U_1 and U_2 heat loss values for a pipe based for either
    single- or multi-layer insulation. The heat loss calculation for two parallel pipes in the
    ground is based on the literature of Benny Böhm:
        - Original reference (paid article): B. Bohm, On transient heat losses from buried district
        heating pipes, International Journal of Energy Research 24, 1311 (2000))
        - Used in Master's degree: Jort de Boer, Optimization of a District Heating Network with the
        focus on heat loss, TU Delft Mechanical, Maritime and Materials Engineering, 2018,
        http://resolver.tudelft.nl/uuid:7be9fcdd-49e4-4e0c-b36c-69d8b713a874 (access to pdf)

    If the `insulation_thicknesses` is provided as a list, the length should be
    equal to the length of `conductivities_insulation`. If both are floats, a
    single layer of insulation is assumed.

    :inner_diameter:            Inner diameter of the pipes [m]
    :insulation_thicknesses:    Thicknesses of the insulation [m]
                                Default of None means a thickness of 0.5 * inner diameter.
    :conductivities_insulation: Thermal conductivities of the insulation layers [W/m/K]
    :conductivity_subsoil:      Subsoil thermal conductivity [W/m/K]
    :h_surface:                 Heat transfer coefficient at surface [W/m^2/K]
    :param depth:               Depth of outer top of the pipeline [m]
    :param pipe_distance:       Distance between pipeline feed and return pipeline centers [m].
                                Default of None means 2 * outer diameter

    :return: U-values (U_1 / U_2) for heat losses of pipes [W/(m*K)]
    """

    if insulation_thicknesses is None:
        insulation_thicknesses = 0.5 * inner_diameter

    if not isinstance(insulation_thicknesses, type(conductivities_insulation)):
        raise Exception("Insulation thicknesses and conductivities should have the same type.")

    if hasattr(insulation_thicknesses, "__iter__"):
        if not len(insulation_thicknesses) == len(conductivities_insulation):
            raise Exception(
                "Number of insulation thicknesses should match number of conductivities"
            )
        insulation_thicknesses = np.array(insulation_thicknesses)
        conductivities_insulation = np.array(conductivities_insulation)
    else:
        insulation_thicknesses = np.array([insulation_thicknesses])
        conductivities_insulation = np.array([conductivities_insulation])

    diam_inner = inner_diameter
    diam_outer = diam_inner + 2 * sum(insulation_thicknesses)
    if pipe_distance is None:
        pipe_distance = 2 * diam_outer
    depth_center = depth + 0.5 * diam_outer

    # NOTE: We neglect the heat resistance due to convection inside the pipe,
    # i.e. we assume perfect mixing, or that this resistance is much lower
    # than the resistance of the outer insulation layers.

    # Heat resistance of the subsoil
    r_subsoil = 1 / (2 * math.pi * conductivity_subsoil) * math.log(4.0 * depth_center / diam_outer)

    # Heat resistance due to insulation
    outer_diameters = diam_inner + 2.0 * np.cumsum(insulation_thicknesses)
    inner_diameters = np.array([inner_diameter, *outer_diameters[:-1]])
    r_ins = sum(
        np.log(outer_diameters / inner_diameters) / (2.0 * math.pi * conductivities_insulation)
    )

    # Heat resistance due to neighboring pipeline
    r_m = (
        1
        / (4 * math.pi * conductivity_subsoil)
        * math.log(1 + (2 * depth_center / pipe_distance) ** 2)
    )

    if neighbour:
        u_1 = (r_subsoil + r_ins) / ((r_subsoil + r_ins) ** 2 - r_m**2)
        u_2 = r_m / ((r_subsoil + r_ins) ** 2 - r_m**2)
    else:
        u_1 = 1 / (r_subsoil + r_ins)
        u_2 = 0

    return u_1, u_2
