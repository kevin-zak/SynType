import pygame, os
from menu import Menu
class Game():
    def __init__(self):
        pygame.init()

        self.running, self.playing = True, False
        self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 1600, 900
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption('SynType')

        # specific game values, language, code segment, lines, etc.
        self.language = "C++"
        self.segment = 'assets/C++/1.txt'
        self.lines = open(self.segment).read().split('\n')
        print(self.lines)

        # Menu Object
        self.curr_menu = Menu(self)


        # Set Font
        #self.font = pygame.font.Font(os.path.join("assets", "ABCfont.ttf"), 16)

        #Some colors
        self.GREEN = (100, 255, 50)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)

    def game_loop(self):
        while self.playing:
            self.check_events()
            
            self.display.fill(self.WHITE)
            self.draw_text("In Typing Game...", 20, 100, 100)
            self.window.blit(self.display,(0,0))
            pygame.display.update()
            self.reset_keys()



    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_RIGHT:
                    self.RIGHT_KEY = True
                if event.key == pygame.K_LEFT:
                    self.LEFT_KEY = True
                if event.key == pygame.K_ESCAPE:
                    self.shutdown()
    
    def reset_keys(self):
        self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False


    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(os.path.join("assets", "ABCfont.ttf"), size) 
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def shutdown(self):
        self.running, self.playing = False, False
        self.curr_menu.run_display = False

# Typing game and Syntax game will inherit from this