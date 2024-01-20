import pygame

class Scene:
    def __init__(self, size):
        self.display = pygame.Surface(size)
        self.size = size
        self.objects = []

    def add(self, obj):
        self.objects.append(obj)

    def update(self):
        for obj in self.objects:
            obj.update()

    def draw(self, screen):
        screen.blit(self.display, (0, 0))
        for obj in self.objects:
            obj.draw(self.display)
