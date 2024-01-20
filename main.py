import pygame

BOMB = pygame.image.load("assets/bomb.png")
pygame.font.init()
FONT = pygame.font.SysFont("Lucinda", 32)

class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.bomb = Bomb(400, 300)

    def run(self):
        while self.running:
            self.update()
            self.handle_events()
            self.draw()
            self.clock.tick(60)

    def update(self):
        self.bomb.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
    def draw(self):
        self.screen.fill((64, 64, 64))
        self.bomb.draw(self.screen)
        pygame.display.flip()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BOMB
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.size = 200
        self.growing = True

        self.letters = ""

    def update(self):
        self.update_size()
        self.image = pygame.transform.scale(BOMB, (self.size, self.size))
        self.rect = self.image.get_rect(center=self.rect.center)

    def update_size(self):
        if self.growing:
            self.size += 1
        else:
            self.size -= 1
        if self.size > 300:
            self.growing = False
        if self.size < 200:
            self.growing = True

    def draw(self, screen):
        self.image.blit(FONT.render(self.letters, True, (255, 255, 255)), (0, 0))
        screen.blit(self.image, self.rect)


if __name__ == "__main__":
    pygame.init()
    UI().run()
    pygame.quit()
