import pygame
import json
import random


def load_image(path: str, size: tuple[int, int]) -> pygame.surface.Surface:
    image = pygame.image.load(path)
    try:
        image = pygame.transform.smoothscale(image, size)
    except ValueError:
        image = pygame.transform.scale(image, size)
    return image


BOMB = load_image("assets/bomb.png", (250, 250))
FULL_HEART = load_image("assets/full_heart.png", (100, 100))
EMPTY_HEART = load_image("assets/empty_heart.png", (100, 100))
pygame.font.init()
FONT = pygame.font.SysFont("Lucinda", 52)
LETTERS = "abcdefghijklmnopqrstuvwxyz"

with open("words_per_syllable.json", "r") as f:
    WORDS_PER_SYLLABLE = json.load(f)
SYLLABLES = list(WORDS_PER_SYLLABLE.keys())
with open("words.txt", "r") as f:
    VALID_WORDS = set(map(lambda x: x.strip(), f.readlines()))

class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.bomb = Bomb(425, 225)
        self.difficulty = 4000
        self.reset_prompt()
        self.current_word = ""
        self.used_words = set()
        self.ms_on_current_prompt = 0
        self.health = 3
        

    def run(self):
        while self.running:
            dt = self.clock.tick(60)
            self.update(dt)
            self.handle_events()
            self.draw()

    def update(self, dt):
        self.ms_on_current_prompt += dt
        if self.ms_on_current_prompt > 10000:
            self.health -= 1
            self.ms_on_current_prompt = 0
            self.current_word = ""
            self.reset_prompt()
        self.bomb.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                ch = event.unicode
                if ch in LETTERS:
                    self.current_word += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.current_word = ""
                    else:
                        self.current_word = self.current_word[:-1]
                elif event.key == pygame.K_RETURN:
                    self.attempt_to_submit()

    def attempt_to_submit(self):
        if self.prompt.lower() in self.current_word and self.current_word not in self.used_words and self.current_word in VALID_WORDS:
            self.used_words.add(self.current_word)
            self.current_word = ""
            self.difficulty -= 20
            self.ms_on_current_prompt = 0
            self.reset_prompt()
        
    def draw(self):
        self.screen.fill((64, 64, 64))
        self.bomb.draw(self.screen)
        current_word = FONT.render(self.current_word.upper(), True, (255, 255, 255))
        current_word_rect = current_word.get_rect(center=(400, 500))
        self.screen.blit(current_word, current_word_rect)
        for i in range(3):
            if i < self.health:
                self.screen.blit(FULL_HEART, (200 + i * 150, 25))
            else:
                self.screen.blit(EMPTY_HEART, (200 + i * 150, 25))

        pygame.display.flip()

    def reset_prompt(self):
        self.prompt = get_random_syallable(self.difficulty)
        self.bomb.update_letters(self.prompt)


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
