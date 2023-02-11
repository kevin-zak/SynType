import pygame, os
from menu import Menu
class Game():
    def __init__(self):
        pygame.init()


        

        # Display Settings
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



        # Text Locations
        self.input_startx = self.DISPLAY_W / 2.0 
        self.input_starty = 200

        #Some colors
        self.GREEN = (100, 255, 50)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)


        #Game Status
        self.running, self.playing = True, False
        self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.input_lines = []
        self.curr_line = ""

    def game_loop(self):
        while self.playing:
            # Check for keypresses..
            self.check_events()
            
            self.display.fill(self.WHITE)
            self.drawPannels()
            
            self.window.blit(self.display,(0,0))


            pygame.display.update()
            self.reset_keys()





    def drawPannels(self):
        y = 200
        x = 0
        for line in self.lines:
            if line[0] == '\t':
                x = 150
            else:
                x=100
            self.draw_code(line, 30, x, y)
            y+=50
        y = 200
        for line in self.input_lines:
            if(len(line) == 0):
                continue
            if line[0] == '\t':
                x = self.input_startx+150
            else:
                x = self.input_startx+100
            self.draw_code(line, 30, x, y)
            y+=50
        if(len(self.curr_line) > 0 and self.curr_line[0] == '\t'):
            x = self.input_startx+150
        else:
            x = self.input_startx+100
        self.draw_code(self.curr_line, 30, x, y)
        

    

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                    # If in progress of game... Move to new line
                    self.input_lines += [self.curr_line]
                    self.curr_line = ""
                    
                elif event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                    #Check if at beginning of line...
                    if len(self.curr_line) > 0:
                        self.curr_line = self.curr_line[:-1]
                    else:
                        if(len(self.input_lines) > 0):
                            self.curr_line = self.input_lines[-1]
                            self.input_lines.pop()
                        else:
                            self.curr_line = ""
                
                elif event.key == pygame.K_ESCAPE:
                    self.shutdown()

                elif event.key == pygame.K_TAB:
                    # Has to add to current line of text...
                    self.curr_line += "\t"

                else: # Add keypress
                    try:
                        self.curr_line += event.unicode
                    except:
                        pass
    
    def reset_keys(self):
        self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False


    def draw_code(self, text, size, x, y):
        font = pygame.font.Font(os.path.join("assets", "MonoLight.ttf"), size) 
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x,y)
        self.display.blit(text_surface, text_rect)

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