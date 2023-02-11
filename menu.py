import pygame

class Menu():

    def __init__(self, game):
        self.state = "Game 1"
        self.game = game
        self.leftx = self.game.DISPLAY_W * 1.0 / 4.0
        self.rightx = self.game.DISPLAY_W * 3.0 / 4.0
        self.starty = self.game.DISPLAY_H * 3.0 / 5.0
        self.run_display = True
        self.cursor_rect = pygame.Rect(0,0,20,20)
        self.offset = -100
        self.cursor_rect.midtop = (self.leftx, self.starty+self.offset)

    def draw_cursor(self):
        self.game.draw_text("^^^", 20, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

    def display_menu(self):
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.GREEN)
            self.game.draw_text("Welcome to SynType!", 150, self.game.DISPLAY_W/2, self.game.DISPLAY_H/10)
            self.game.draw_text("Game 1", 50, self.leftx, self.starty)
            self.game.draw_text("Game 2", 50, self.rightx, self.starty)
            self.draw_cursor()
            self.blit_screen()


    def move_cursor(self):
        if self.game.RIGHT_KEY or self.game.LEFT_KEY:
            if self.state == "Game 1":
                self.cursor_rect.midtop = (self.rightx, self.starty + self.offset)
                self.state = "Game 2"
            elif self.state == "Game 2":
                self.cursor_rect.midtop = (self.leftx, self.starty + self.offset)
                self.state = "Game 1"
        
    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Game 1":
                self.game.playing1 = True
            elif self.state == "Game 2":
                self.game.playing2 = True

            # Once a game has been started, don't display menu anymore
            self.run_display = False