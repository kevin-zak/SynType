import pygame, os
from menu import Menu
import time, random
class Game():
    def __init__(self):
        pygame.init()

        # Display Settings
        self.DISPLAY_W, self.DISPLAY_H = 1600, 900
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        pygame.display.set_caption('SynType')
        
        #Some colors
        self.GREEN = (100, 255, 50)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.BORDER_COLOR = self.BLACK

        # specific game values, language, code segment, lines, etc.
        self.language = "C++"
        self.newGame()
        # self.segment = 'assets/C++/1.txt'
        # self.seg_seg_lines = open(self.segment).read().split('\n')

        # Menu Object
        self.curr_menu = Menu(self)

        # Text Locations
        self.input_startx = self.DISPLAY_W / 2.0 
        self.input_starty = 200
        self.cursor_x = 900
        self.cursor_y = 100

        #Some colors
        self.GREEN = (100, 255, 50)
        self.BLACK = (0,0,0)
        self.WHITE = (255,255,255)
        self.RED = (255, 100, 50)
        self.BORDER_COLOR = self.BLACK

        #Game Status
        self.running, self.playing = True, False
        self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.input_lines = []
        self.curr_line = ""
        self.error = False
        self.done = False

    def newGame(self):
        self.segment = os.path.join("assets/" + self.language, (random.choice(os.listdir(os.path.join("assets", self.language)))))
        self.seg_lines = open(self.segment).read().split('\n')
        self.input_lines = []
        self.curr_line = ""
        self.done = False
        self.error = False
        self.BORDER_COLOR = self.BLACK

    def game_loop(self):
        while self.playing:
            # Check for keypresses..
            self.check_events()
            
            self.display.fill(self.WHITE)
            
            self.drawPannels()

            self.window.blit(self.display,(0,0))

            self.drawBorder()
            pygame.display.update()
            self.reset_keys()
        

    def drawBorder(self):
        #draw midline
        pygame.draw.line(self.window, self.BORDER_COLOR, (self.DISPLAY_W/2,0), (self.DISPLAY_W/2,self.DISPLAY_H), 5)

        #draw border
        pygame.draw.line(self.window, self.BORDER_COLOR, (0,0), (self.DISPLAY_W,0), 10)
        pygame.draw.line(self.window, self.BORDER_COLOR, (0,0), (0,self.DISPLAY_H), 10)
        pygame.draw.line(self.window, self.BORDER_COLOR, (self.DISPLAY_W,self.DISPLAY_H), (self.DISPLAY_W,0), 15)
        pygame.draw.line(self.window, self.BORDER_COLOR, (self.DISPLAY_W,self.DISPLAY_H), (0,self.DISPLAY_H), 15)
        self.drawCursor(self.cursor_x, self.cursor_y)


    def drawPannels(self):
        y = 200
        for line in self.seg_lines:
            x = 100
            for char in line:
                if char == '\t':
                    x+=50
                else:
                    break
            self.draw_code(line, 30, x, y, True)
            y+=50
        y = 200
        for ind, line in enumerate(self.input_lines):
            if(len(line) == 0):
                continue
            self.check_error(line, ind)
            x = self.input_startx+100
            for char in line:
                if char == '\t':
                    x+=50
                else:
                    break
            self.draw_code(line, 30, x, y, False)
            y+=50
        x = self.input_startx+100
        for char in self.curr_line:
            if char == '\t':
                x+=50
            else:
                break
        self.check_error(self.curr_line, len(self.input_lines))
        self.draw_code(self.curr_line, 30, x, y, False)
        

    def drawCursor(self, x, y):
        if time.time() % 1 > 0.5:
            return
        x_coord = x
        y_coord = y
        pygame.draw.line(self.window, self.BLACK, (x_coord, y_coord - 15), (x_coord, y_coord+15), 3)

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True

                    if not self.done:
                        self.input_lines += [self.curr_line]
                        self.curr_line = ""
                    
                    
                    if(len(self.input_lines) == len(self.seg_lines)):
                        # Check correctness
                        if(self.input_lines == self.seg_lines):
                            self.BORDER_COLOR = self.GREEN
                            
                        else:
                            self.BORDER_COLOR = self.RED
                        self.done = True
                        
                        self.drawBorder()
                        pygame.display.update()
                        time.sleep(3)
                        self.newGame()

                        break
                    

                    
                    
                elif event.key == pygame.K_BACKSPACE and not self.done:
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
                    ##self.done = True
                    ##self.playing = False


                elif event.key == pygame.K_TAB:
                    # Has to add to current line of text...
                    self.curr_line += "\t"

                elif not self.done: # Add keypress
                    try:
                        self.curr_line += event.unicode
                    except:
                        pass
    
    def reset_keys(self):
        self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False


    def draw_code(self, text, size, x, y, isSeg):
        font = pygame.font.Font(os.path.join("assets", "MonoLight.ttf"), size) 
        if(self.error and not isSeg):
            text_surface = font.render(text, True, self.RED)
        else:
            text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.midleft = (x,y)
        self.cursor_x = text_rect.midright[0]
        self.cursor_y = text_rect.midright[1]
        self.display.blit(text_surface, text_rect)


    def check_error(self, line, segInd):
        if len(self.input_lines) < len(self.seg_lines):
            if len(line)>0 and line != self.seg_lines[segInd][:len(line)]:
                self.error = True
            else:
                self.error = False
        
    

    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(os.path.join("assets", "ABCfont.ttf"), size) 
        text_surface = font.render(text, True, self.BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def shutdown(self):
        self.running, self.playing = False, False
        self.curr_menu.run_display = False
