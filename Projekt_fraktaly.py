import pygame
import numpy as np
import Mandelbrot
import Juliaova_mnoz

WIDTH, HEIGHT = 800, 800


# Legenda na obrazovce
def legend(screen: pygame.Surface):

    font: pygame.font.Font = pygame.font.SysFont("Arial", 14)

    text: list[str] = [
        "Ukončení: ESC",
        "Reset zobrazení: R",
        "Změna fraktálu: Q",
        "Změna barevného režimu: M",
        "Počet iterací: šipky nahoru/dolů",
        "Změna parametru Julia:",
        " - W/S: změna realné části",
        " - A/D: změna imaginární části",
        "Přibližování/oddálení: kolečko myši"
    ]
    y: int = 10
    for t in text:
        label: pygame.surface.Surface = font.render(t, True, (0, 0, 0))
        screen.blit(label, (10, y))
        y: int = y + 15


# Převod dat na RGB obraz
def na_rgb(data: np.ndarray, max_iter: int, color_mode: int) -> np.ndarray:
    h: int = data.shape[0]
    w: int = data.shape[1]
    img = np.zeros((h, w, 3), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            v = data[i, j]

            color = color_map(v, max_iter, color_mode)

            img[i, j] = color

    return img


# Zbarvení fraktálů
def color_map(value: int, max_iter: int, color_mode: int) -> tuple[int, int, int]:
    t: float = value / max_iter

    if color_mode == 0:  # Zelené zbravení
        return (int(255 - (255 * t)), int(255 - (100 * t)), int(255 - (255 * t)))

    elif color_mode == 1:  # Červené zbravení
        return (int(255 - (100 * t)), int(255 - (255 * t)), int(255 - (255 * t)))

    elif color_mode == 2:  # Modré zbarvení
        return (int(255 - (255 * t)), int(255 - (240 * t)), int(255 - (100 * t)))

    else:  # Černé zbarvení
        v = int((255 - (255 * t)))
        return (v, v, v)


# Hlavní funkce
def main():
    # Inicializace programu
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Vizualizace fraktálů")

    # Počáteční nastavení zobrazení
    xmin: float = -2
    xmax: float = 1
    ymin: float = -1.5
    ymax: float = 1.5
    max_iter: int = 100

    mode: str = "mandelbrot"
    c: complex = -0.7 + 0.27015j
    color_mode: int = 0

    running: bool = True

    # Funkce pro vykreslení fraktálu
    def render():
        if mode == "mandelbrot":
            data = Mandelbrot.mandelbrot_pg(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, max_iter)
        else:
            data = Juliaova_mnoz.julia(xmin, xmax, ymin, ymax, WIDTH, HEIGHT, max_iter, c.real, c.imag)

        rgb: np.ndarray = na_rgb(data, max_iter, color_mode)
        surf: pygame.Surface = pygame.surfarray.make_surface(rgb.swapaxes(0, 1))
        screen.blit(surf, (0, 0))
        legend(screen)
        pygame.display.flip()

    render()

    while running:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            # Zoom pomocí kolečka myši
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    mx: int = pygame.mouse.get_pos()[0]
                    my: int = pygame.mouse.get_pos()[1]

                    zx: float = xmin + (xmax - xmin) * mx / WIDTH
                    zy: float = ymin + (ymax - ymin) * my / HEIGHT

                    scale: float = 0.5
                    dx: float = (xmax - xmin) * scale
                    dy: float = (ymax - ymin) * scale

                    xmin, xmax = zx - dx / 2, zx + dx / 2
                    ymin, ymax = zy - dy / 2, zy + dy / 2

                    render()

                elif event.button == 5:
                    mx: int = pygame.mouse.get_pos()[0]
                    my: int = pygame.mouse.get_pos()[1]

                    zx: float = xmin + (xmax - xmin) * mx / WIDTH
                    zy: float = ymin + (ymax - ymin) * my / HEIGHT

                    scale: float = 0.5
                    dx: float = (xmax - xmin) * scale
                    dy: float = (ymax - ymin) * scale

                    xmin: float = zx - dx * 2
                    xmax: float = zx + dx * 2
                    ymin: float = zy - dy * 2
                    ymax: float = zy + dy * 2
                    render()

            # Ovládání
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP:
                    max_iter: int = max_iter + 50
                    render()

                elif event.key == pygame.K_DOWN:
                    max_iter: int = max(50, max_iter - 50)
                    render()

                elif event.key == pygame.K_q:
                    if mode == "mandelbrot":
                        mode: str = "julia"
                        xmin: float = -1.5
                        xmax: float = 1.5
                        ymin: float = -1.5
                        ymax: float = 1.5
                    else:
                        mode: str = "mandelbrot"
                        xmin: float = -2
                        xmax: float = 1
                        ymin: float = -1.5
                        ymax: float = 1.5
                    render()

                elif event.key == pygame.K_r and mode == "mandelbrot":
                    xmin: float = -2
                    xmax: float = 1
                    ymin: float = -1.5
                    ymax: float = 1.5
                    render()

                elif event.key == pygame.K_r and mode == "julia":
                    xmin: float = -1.5
                    xmax: float = 1.5
                    ymin: float = -1.5
                    ymax: float = 1.5
                    render()

                # změna parametru Julia
                elif event.key == pygame.K_a and mode == "julia":
                    c: complex = c + (-0.01 + 0j)
                    render()
                elif event.key == pygame.K_d and mode == "julia":
                    c: complex = c + (0.01 + 0j)
                    render()
                elif event.key == pygame.K_w and mode == "julia":
                    c: complex = c + (0 + 0.01j)
                    render()
                elif event.key == pygame.K_s and mode == "julia":
                    c: complex = c + (0 - 0.01j)
                    render()

                # Změna barevného režimu
                elif event.key == pygame.K_m:
                    color_mode: int = (color_mode + 1) % 4
                    render()

                # Ukončení programu
                elif event.key == pygame.K_ESCAPE:
                    running: bool = False
                    pygame.quit()

    pygame.quit()


if __name__ == "__main__":
    main()
