import numpy as np
import numba


@numba.njit(parallel=True)
def julia(xmin: float, xmax: float, ymin: float, ymax: float, w: int, h: int, max_iter: int, cr: float, ci: float) -> np.ndarray:
    img: np.ndarray = np.zeros((h, w))
    c: complex = cr + ci * 1j

    for i in range(h):
        for j in range(w):
            x: float = xmin + (xmax - xmin) * j / w
            y: float = ymin + (ymax - ymin) * i / h

            z: complex = x + 1j * y

            for k in range(max_iter):
                z = z * z + c
                if abs(z) > 2:
                    img[i, j] = k
                    break
            else:
                img[i, j] = max_iter
    return img
