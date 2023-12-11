from dataclasses import dataclass

import numpy as np
from numpy.typing import ArrayLike
import ovito

from .modifier import particle_reduction_modifier


# modifier for getting total displacement of each type
total_displacement_modifier = particle_reduction_modifier(
    particle_property='Displacement',
    reducer=lambda x: np.sum(x, axis=0)
)


@dataclass
class OnsagerMatrix:
    """
    Container object storing Onsager matrix info
    """

    time_series: ArrayLike
    matrix: ArrayLike
    time: ArrayLike
    num_types: int

    def __getitem__(self, item):
        """
        Let user index object like a numpy array
        :param item: Ellipses or tuple
        :return: Full matrix or individual ij element
        :raise: ValueError if user tries to subscript object with a non-Ellipses or non-tuple object
        """

        if item is Ellipsis:
            return self.matrix
        elif type(item) is tuple and len(item) == 2:
            return self.matrix[item]
        else:
            raise ValueError('OnsagerMatrix instance only subscriptable with Ellipses or length-two indices')


def get_onsager_matrix(
        dump_file: str,
        num_trajectories: int,
        timestep: float = 1.0e-3,
        transient_time: float = 0.0
) -> OnsagerMatrix:
    """
    Function for getting the Onsager matrix
    :param dump_file: input LAMMPS-style dump file
    :param num_trajectories: number of trajectories to splice simulation into
    :param timestep: physical timestep (in units of ps for metal unit simulations), defaults to 0.001 ps = 1.0 fs
    :param transient_time: physical transient time, lets user exclude the beginning part of the trajectory
                           if unspecified, assume user wants to use full trajectory
    :return: OnsagerMatrix object with all information necessary to plot and access ij elements
    """

    # import file as pipeline object, get types and number of unique types from first frame
    pipeline = ovito.io.import_file(dump_file)
    data = pipeline.compute(0)
    types = data.particles['Particle Type'][...]
    num_types = len(set(types))

    # add displacement and total displacement modifier
    pipeline.modifiers.append(ovito.modifiers.CalculateDisplacementsModifier())
    pipeline.modifiers.append(total_displacement_modifier)

    # store number of frames and the truncated number of frames
    # if splitting trajectory into num_trajectories frames, need to make sure we only store K steps
    # where K is a multiple of num_trajectories
    num_frames = pipeline.source.num_frames
    truncated_num_frames = num_frames // num_trajectories * num_trajectories
    total_displacement_time_series = np.zeros((num_types, truncated_num_frames, 3))
    time = np.zeros(num_frames // num_trajectories)

    # get total displacements and time from pipeline
    for frame in np.arange(truncated_num_frames, dtype=int):

        data = pipeline.compute(frame)
        for i in np.arange(num_types, dtype=int):
            total_displacement = data.attributes[f'Total displacement {i + 1:.0f}']
            total_displacement_time_series[i, frame, :] = total_displacement
        if frame < num_frames // num_trajectories:
            time[frame] = data.attributes['Timestep'] * timestep

    # default transient_index to 0, find the appropriate transient index according to user's input transient time
    # if transient time is provided
    transient_index = 0
    if transient_time != 0:
        for i, t in enumerate(time):
            if t > transient_time:
                break
            transient_index = i

    # initialize time series R_i(t)\cdot R_j(t) for each sample
    average_square_displacement_time_series = np.zeros((num_types, num_types, num_frames // num_trajectories))

    # initialize matrix
    onsager_matrix = np.zeros((num_types, num_types))

    # loop through types
    for i in np.arange(num_types, dtype=int):
        for j in np.arange(i, num_types, dtype=int):

            # grab R_i(t) and R_j(t)
            total_displacement_first_type = total_displacement_time_series[i, :, :]
            total_displacement_second_type = total_displacement_time_series[j, :, :]

            # split arrays into num_trajectories trajectories
            first_windows = np.array((np.split(total_displacement_first_type, num_trajectories, axis=0)))
            second_windows = np.array((np.split(total_displacement_second_type, num_trajectories, axis=0)))

            # zero out all windows, i.e. first timestep for window should have zero vector
            # need to stack to pad the lost axis
            first_windows = first_windows - np.stack(
                [first_windows[:, 0, :]] * (truncated_num_frames // num_trajectories),
                axis=1
            )
            second_windows = second_windows - np.stack(
                [second_windows[:, 0, :]] * (truncated_num_frames // num_trajectories),
                axis=1
            )

            # perform dot product over dimension axis, i.e. last axis
            # w = window index, t = timestep index, d = dimension index
            square_displacement = np.einsum(
                'wtd,wtd->wt',
                first_windows,
                second_windows
            )

            # average over window index
            msd_time_series = np.mean(square_displacement, axis=0)
            average_square_displacement_time_series[i, j, :] = msd_time_series
            average_square_displacement_time_series[j, i, :] = msd_time_series

            # then, do linear regression on time series after transient time to get coefficient
            non_transient_time = time[transient_index:]
            non_transient_square_displacement = msd_time_series[transient_index:]
            coefficient_matrix = np.vstack([non_transient_time, np.ones(non_transient_time.shape)]).T
            slope, intercept = np.linalg.lstsq(coefficient_matrix, non_transient_square_displacement, rcond=None)[0]
            onsager_matrix[i, j] = slope / 6.0
            onsager_matrix[j, i] = slope / 6.0

    return OnsagerMatrix(
        time_series=average_square_displacement_time_series,
        matrix=onsager_matrix,
        time=time,
        num_types=num_types
    )
