import numpy as np
import numba


@numba.njit(parallel=True)
def mandelbrot_pg(xmin, xmax, ymin, ymax, w, h, max_iter):
    img = np.zeros((h, w))
    for i in range(h):
        for j in range(w):
            x = xmin + (xmax - xmin) * j / w
            y = ymin + (ymax - ymin) * i / h

            c = x + 1j * y
            z = 0j

            for k in range(max_iter):
                z = z * z + c
                if abs(z) > 2:
                    img[i, j] = k
                    break
            else:
                img[i, j] = max_iter
    return img
