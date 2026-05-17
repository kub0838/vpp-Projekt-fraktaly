import numpy as np
import numba


@numba.njit(parallel=True)
def julia(xmin, xmax, ymin, ymax, w, h, max_iter, cr, ci):
    img = np.zeros((h, w))
    c = cr + ci * 1j

    for i in range(h):
        for j in range(w):
            x = xmin + (xmax - xmin) * j / w
            y = ymin + (ymax - ymin) * i / h

            z = x + 1j * y

            for k in range(max_iter):
                z = z * z + c
                if abs(z) > 2:
                    img[i, j] = k
                    break
            else:
                img[i, j] = max_iter
    return img
