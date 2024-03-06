import pygame

def sign(x):
    """Returns the sign of x, 1 if x is positive, -1 if x is negative, 0 if x is 0"""
    return x and (1, -1)[x<0]


def fade_colour(start: tuple[int, int, int], end: tuple[int, int, int], delta: float) -> tuple[int, int, int]:
    """Shifts a colour by delta amount from start to end"""
    new_colour = tuple()
    for i in range(3):
        change = end[i] - start[i]
        if abs(change) > delta:
            new_colour += (start[i] + sign(change)*delta,)
        else:
            new_colour += (end[i],)
    return new_colour


def load_image(path: str, size: tuple[int, int]) -> pygame.surface.Surface:
    image = pygame.image.load(path)
    try:
        image = pygame.transform.smoothscale(image, size)
    except ValueError:
        image = pygame.transform.scale(image, size)
    return image


def sort_dictionary(dictionary, key=lambda x: x, reverse=False):
    return {k: v for k, v in sorted(dictionary.items(), key=key, reverse=reverse)}
