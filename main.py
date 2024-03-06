import pygame
import json
import random
from utils import fade_colour, load_image
import leaderboard_handler

BOMB = load_image("assets/bomb.png", (250, 250))
BIG_BOMB = load_image("assets/bomb.png", (500, 500))
FULL_HEART = load_image("assets/full_heart.png", (100, 100))
EMPTY_HEART = load_image("assets/empty_heart.png", (100, 100))
pygame.font.init()
FONT = pygame.font.SysFont("Lucinda", 52)
LETTERS = "abcdefghijklmnopqrstuvwxyz"

DEFAULT_BACKGROUND = (64, 64, 64)
MILD_RED = (128, DEFAULT_BACKGROUND[1], DEFAULT_BACKGROUND[2])
BRIGHT_RED = (255, DEFAULT_BACKGROUND[1], DEFAULT_BACKGROUND[2])
MILD_GREEN = (DEFAULT_BACKGROUND[0], 128, DEFAULT_BACKGROUND[2])
BLUE = (DEFAULT_BACKGROUND[0], DEFAULT_BACKGROUND[1], 255)
TEXT_COLOUR = (255, 255, 255)

with open("words_per_syllable.json", "r") as f:
    WORDS_PER_SYLLABLE = json.load(f)
SYLLABLES = list(WORDS_PER_SYLLABLE.keys())
with open("words.txt", "r") as f:
    VALID_WORDS = set(map(lambda x: x.strip(), f.readlines()))


class Scene:
    def __init__(self, return_values={}):
        self.running = True
        self.bg_color = DEFAULT_BACKGROUND
        self.previous_return_values = return_values
        self.return_values = {}
        self.call_scene_change = False

    def update(self, dt):
        self.bg_color = fade_colour(self.bg_color, DEFAULT_BACKGROUND, 3)

    def handle_events(self):
        pass

    def draw(self, screen):
        screen.fill(self.bg_color)
        

class StartScene(Scene):
    def __init__(self, return_values={}):
        super().__init__(return_values)
        self.bomb = Bomb(440, 200, 400)
        self.title = FONT.render("Word Bomb", True, (TEXT_COLOUR))
        self.title_rect = self.title.get_rect(center=(380, 280))
        self.instructions = FONT.render("Press any key to start", True, (TEXT_COLOUR))
        self.instructions_rect = self.instructions.get_rect(center=(400, 500))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                self.call_scene_change = True
        
    def draw(self, screen):
        super().draw(screen)
        self.bomb.draw(screen)
        screen.blit(self.title, self.title_rect)
        screen.blit(self.instructions, self.instructions_rect)
        pygame.display.flip()


class PlayingScene(Scene):
    def __init__(self, return_values={}):
        super().__init__(return_values)
        self.bomb = Bomb(425, 225, 250)
        self.difficulty = 4000
        self.reset_prompt()
        self.current_word = ""
        self.used_words = set()
        self.ms_on_current_prompt = 0
        self.health = 3

    def update(self, dt):
        super().update(dt)
        self.ms_on_current_prompt += dt
        if self.ms_on_current_prompt > 10000:
            self.bg_color = BRIGHT_RED
            self.health -= 1
            self.ms_on_current_prompt = 0
            self.current_word = ""
            self.reset_prompt()
            if self.health <= 0:
                self.game_over()
        self.bomb.update()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            
            if event.type == pygame.KEYDOWN:
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

    def draw(self, screen):
        screen.fill(self.bg_color)
        self.bomb.draw(screen)
        current_word = FONT.render(self.current_word.upper(), True, (TEXT_COLOUR))
        current_word_rect = current_word.get_rect(center=(400, 500))
        screen.blit(current_word, current_word_rect)
        for i in range(3):
            if i < self.health:
                screen.blit(FULL_HEART, (200 + i * 150, 25))
            else:
                screen.blit(EMPTY_HEART, (200 + i * 150, 25))

        pygame.display.flip()

    def attempt_to_submit(self):
        if self.prompt.lower() in self.current_word and self.current_word not in self.used_words and self.current_word in VALID_WORDS:
            self.used_words.add(self.current_word)
            self.current_word = ""
            self.difficulty -= 20
            self.ms_on_current_prompt = 0
            self.bg_color = MILD_GREEN
            self.reset_prompt()
        else:
            self.bg_color = MILD_RED

    def reset_prompt(self):
        self.prompt = get_random_syallable(self.difficulty)
        self.bomb.update_letters(self.prompt)

    def game_over(self):
        words = 0
        letters = 0
        for word in self.used_words:
            words += 1
            letters += len(word)
        self.return_values = {"words": words, "letters": letters}
        self.call_scene_change = True


class EnterNameScene(Scene):
    def __init__(self, return_values={}):
        super().__init__(return_values)
        self.bg_color = BRIGHT_RED
        self.you_scored = FONT.render("You scored:", True, (TEXT_COLOUR))
        self.you_scored_rect = self.you_scored.get_rect(center=(400, 100))
        self.words = FONT.render(f"Words: {return_values['words']}", True, (TEXT_COLOUR))
        self.words_rect = self.words.get_rect(center=(200, 200))
        self.letters = FONT.render(f"Letters: {return_values['letters']}", True, (TEXT_COLOUR))
        self.letters_rect = self.letters.get_rect(center=(600, 200))

        self.instructions = FONT.render("Enter your name", True, (TEXT_COLOUR))
        self.instructions_rect = self.instructions.get_rect(center=(400, 300))
        self.name = ""
        self.name_text = FONT.render(self.name, True, (TEXT_COLOUR))
        self.name_rect = self.name_text.get_rect(center=(400, 400))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.name:
                        self.submit()
                elif event.key == pygame.K_BACKSPACE:
                    if pygame.key.get_mods() & pygame.KMOD_CTRL:
                        self.name = ""
                    else:
                        self.name = self.name[:-1]
                else:
                    self.name += event.unicode
        
    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.you_scored, self.you_scored_rect)
        screen.blit(self.words, self.words_rect)
        screen.blit(self.letters, self.letters_rect)
        screen.blit(self.instructions, self.instructions_rect)
        self.name_text = FONT.render(self.name, True, (TEXT_COLOUR))
        self.name_rect = self.name_text.get_rect(center=(400, 400))
        screen.blit(self.name_text, self.name_rect)
        pygame.display.flip()
    
    def submit(self):
        words = self.previous_return_values["words"]
        letters = self.previous_return_values["letters"]
        self.return_values = {"words": words, "letters": letters, "name": self.name}
        high_score = leaderboard_handler.update_leaderboard(self.name, words, letters)
        self.return_values["high_score"] = high_score
        self.call_scene_change = True


class LeaderboardScene(Scene):
    def __init__(self, return_values={}):
        super().__init__(return_values)
        self.leaderboard = leaderboard_handler.open_leaderboard()
        self.title = FONT.render("Leaderboard", True, (TEXT_COLOUR))
        self.title_rect = self.title.get_rect(center=(400, 100))
        self.words = FONT.render("Words", True, (TEXT_COLOUR))
        self.words_rect = self.words.get_rect(center=(250, 200))
        self.letters = FONT.render("Letters", True, (TEXT_COLOUR))
        self.letters_rect = self.letters.get_rect(center=(550, 200))
        self.high_score = return_values["high_score"]
        self.username = return_values["name"]
        if self.high_score:
            self.bg_color = BLUE

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.title, self.title_rect)
        screen.blit(self.words, self.words_rect)
        screen.blit(self.letters, self.letters_rect)

        for i, leaderboard in enumerate((self.leaderboard["words"], self.leaderboard["letters"])):
            for j, (name, score) in list(enumerate(leaderboard.items()))[:5]:
                if name == self.username:
                    colour = BLUE
                else:
                    colour = TEXT_COLOUR
                row_text = FONT.render(f"{name}: {score}", True, (colour))
                row_rect = row_text.get_rect(center=(250 + 300*i, 250 + j * 50))
                screen.blit(row_text, row_rect)

        if self.high_score:
            high_score_text = FONT.render("New High Score!", True, (TEXT_COLOUR))
            high_score_rect = high_score_text.get_rect(center=(400, 500))
            screen.blit(high_score_text, high_score_rect)
        pygame.display.flip()


SCENES = [StartScene, PlayingScene, EnterNameScene, LeaderboardScene]


class UI:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.clock = pygame.time.Clock()
        self.running = True
        self.scene_number = 0
        self.scene = SCENES[self.scene_number]()

    def run(self):
        while self.running:
            dt = self.clock.tick(60)
            self.scene.update(dt)
            self.scene.handle_events()
            self.scene.draw(self.screen)
            self.check_scene_change()

    def check_scene_change(self):
        if not self.scene.running:
            self.running = False
            return
        if self.scene.call_scene_change:
            return_values = self.scene.return_values
            self.scene_number += 1
            self.scene = SCENES[self.scene_number](return_values)
        

class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        super().__init__()
        self.IMAGE = load_image("assets/bomb.png", (size, size))
        self.image = self.IMAGE.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.update_letters("")

    def update(self):
        pass

    def draw(self, screen):
        self.image = self.IMAGE.copy()
        self.image.blit(self.letters, self.letter_rect)
        screen.blit(self.image, self.rect)

    def update_letters(self, letters):
        self.letters = FONT.render(letters, True, (TEXT_COLOUR))
        self.letter_rect = self.letters.get_rect(center=(77, 165))


def get_random_syallable(min_words=0):
    potential_syllables = list(filter(lambda x: WORDS_PER_SYLLABLE[x] >= min_words, SYLLABLES))
    return random.choice(potential_syllables).upper()


if __name__ == "__main__":
    pygame.init()
    UI().run()
    pygame.quit()
