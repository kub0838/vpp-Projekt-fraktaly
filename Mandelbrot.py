import numpy as np
import numba


@numba.njit(parallel=True)
def mandelbrot_pg(xmin: float, xmax: float, ymin: float, ymax: float, w: int, h: int, max_iter: int) -> np.ndarray:
    img: np.ndarray = np.zeros((h, w))
    for i in numba.prange(h):
        for j in numba.prange(w):
            x: float = xmin + (xmax - xmin) * j / w
            y: float = ymin + (ymax - ymin) * i / h

            c: complex = x + 1j * y
            z: complex = 0j

            for k in numba.prange(max_iter):
                z = z * z + c
                if abs(z) > 2:
                    img[i, j] = k
                    break
            else:
                img[i, j] = max_iter
    return img
    
