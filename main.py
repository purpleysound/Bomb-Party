import pygame
import json
import random

BOMB = pygame.transform.smoothscale(pygame.image.load("assets/bomb.png"), (250, 250))
pygame.font.init()
FONT = pygame.font.SysFont("Lucinda", 52)

with open("words_per_syllable.json", "r") as f:
    WORDS_PER_SYLLABLE = json.load(f)
SYLLABLES = list(WORDS_PER_SYLLABLE.keys())


class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.bomb = Bomb(425, 225)

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
            elif event.type == pygame.KEYDOWN:
                self.bomb.update_letters(get_random_syallable(1000))
        
    def draw(self):
        self.screen.fill((64, 64, 64))
        self.bomb.draw(self.screen)
        pygame.display.flip()


class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = BOMB.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.update_letters("")


    def update(self):
        pass

    def draw(self, screen):
        self.image = BOMB.copy()
        self.image.blit(self.letters, self.letter_rect)
        screen.blit(self.image, self.rect)

    def update_letters(self, letters):
        self.letters = FONT.render(letters, True, (255, 255, 255))
        self.letter_rect = self.letters.get_rect(center=(77, 165))


def get_random_syallable(min_words=0):
    potential_syllables = list(filter(lambda x: WORDS_PER_SYLLABLE[x] >= min_words, SYLLABLES))
    return random.choice(potential_syllables).upper()


if __name__ == "__main__":
    pygame.init()
    UI().run()
    pygame.quit()
