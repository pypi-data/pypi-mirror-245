from typing import List, Union

import numpy as np

__author__ = "Alberto Abarzua"


def rad2degree(angle: float) -> float:
    return (180 / np.pi) * angle


def degree2rad(angle: float) -> float:
    return (np.pi / 180) * angle


def allclose(
    a: Union[float, int, List[Union[float, int]]],
    b: Union[float, int, List[Union[float, int]]],
    rtol: float = 1e-03,
    atol: float = 1e-03,
) -> bool:
    a_array = np.array(a)
    b_array = np.array(b)
    return np.allclose(a_array, b_array, rtol=rtol, atol=atol)


def x_rotation_matrix(angle: float) -> np.ndarray:
    """Creates a rotation matrix using angle about the X axis.

    Args:
        angle (float): angle that must be in radians

    Returns:
        np.array: 3x3 transformation matrix using angle
    """
    r = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
    return r


def y_rotation_matrix(angle: float) -> np.ndarray:
    """Creates a rotation matrix using angle about the Y axis.

    Args:
         angle (float): angle that must be in radians

     Returns:
         np.array: 3x3 transformation matrix using angle
    """
    r = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
    return r


def z_rotation_matrix(angle: float) -> np.ndarray:
    """Creates a rotation matrix using angle about the Z axis.

    Args:
        angle (float): angle that must be in radians

    Returns:
       np.array: 3x3 transformation matrix using angle
    """
    r = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])
    return r


def transformation_matrix(R: np.ndarray, D: np.ndarray) -> np.ndarray:
    """Create a 4x4 homogeneous transformation matrix from a 3x3 rotation matrix and a 3D
    translation vector.

    Args:
        R (np.ndarray): A 3x3 rotation matrix.
        D (np.ndarray): A 1D array of size 3 representing the translation along the x, y,
        and z axes.

    Returns:
        np.ndarray: A 4x4 homogeneous transformation matrix.

    Raises:
        ValueError: If `R` is not a 3x3 matrix, or `D` is not a 1D array of size 3.
    """
    if R.shape != (3, 3) or D.shape != (3,):
        raise ValueError("R must be a 3x3 matrix and D must be a 1D array of size 3.")

    return np.block([[R, D.reshape(-1, 1)], [0, 0, 0, 1]])  # reshape the D vector to column vector


def extract_euler_angles(R: np.ndarray) -> list[float]:
    """Extract Euler angles (roll, pitch, yaw) from a given rotation matrix.

    Args:
        R (np.ndarray): A 3x3 rotation matrix.

    Returns:
        list[float]: The three Euler angles (roll, pitch, yaw) obtained from the rotation
        matrix in radians.

    Raises:
        ValueError: If `R` is not a 3x3 matrix.
    """
    if R.shape != (3, 3):
        raise ValueError("R must be a 3x3 matrix.")

    if R[2, 0] != 1 and R[2, 0] != -1:
        roll = np.arctan2(R[2, 1], R[2, 2])

        pitch = -np.arcsin(R[2, 0])

        yaw = np.arctan2(R[1, 0], R[0, 0])

        return [float(roll), float(pitch), float(yaw)]
    else:
        yaw = 0
        if R[2, 0] == -1:
            pitch = np.pi / 2.0
            roll = np.arctan2(R[0, 1], R[0, 2])
        else:
            pitch = -np.pi / 2.0
            roll = np.arctan2(-R[0, 1], -R[0, 2])

        return [float(roll), float(pitch), float(yaw)]


def create_rotation_matrix_from_euler_angles(roll: float, pitch: float, yaw: float) -> np.ndarray:
    """Create a 3x3 rotation matrix from three Euler angles (roll, pitch, yaw).

    Args:
        roll (float): Roll (x-Euler angle) in radians.
        pitch (float): Pitch (y-Euler angle) in radians.
        yaw (float): Yaw (z-Euler angle) in radians.

    Returns:
        np.ndarray: 3x3 rotation matrix.
    """
    return z_rotation_matrix(yaw) @ y_rotation_matrix(pitch) @ x_rotation_matrix(roll)


def nearest_by_2pi_ref(angle: float, ref: float) -> float:
    """Find the nearest angle to 'ref' that is a multiple of 2π away from 'angle' in any direction.

    Args:
        angle (float): The starting angle in radians.
        ref (float): The reference angle in radians.

    Returns:
        float: The nearest angle to 'ref' that is a multiple of 2π away from 'angle' in any direction.
    """
    try:
        n = round((ref - angle) / (2 * np.pi))
        return angle + n * 2 * np.pi
    except Exception:
        return angle
