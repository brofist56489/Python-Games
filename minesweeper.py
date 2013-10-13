import pygame
from pygame.locals import *
import time as _time
import random, math
color_black = (0,0,0)

UNCLICKED = 0
CLICKED = 1
MINE = 2
FLAG = 3
NUMBER_START = 10

LEVEL_CLEAR = 1
LEVEL_MINE = 2

HAPPY_FACE = 4
SAD_FACE = 5
NEUTRAL_FACE = 6

try:
    MINES = int(input("How many mines? "))
except EOFError as e:
    MINES = 20

try:
    LEVEL_SIZE = int(input("Level size? "))
except EOFError as e:
    LEVEL_SIZE = 15

screen_size = (LEVEL_SIZE * 32, LEVEL_SIZE * 32 + 32)
color_black = (0,0,0)

class Game():

    def __init__(self):
        self.score = 0
        self.mines_remaining = MINES

        self.level_width = LEVEL_SIZE
        self.level_height = LEVEL_SIZE
        
        self.newgame()
        
        #Makes the unclicked surface
        self.unclicked_surface = pygame.Surface((32, 32))
        pxarray = pygame.PixelArray(self.unclicked_surface)
        pxarray[::1] = 0xAFAFAF
        pxarray[::1, :4] = 0x5F5F5F
        pxarray[:4, ::1] = 0x5F5F5F

        #Makes the clicked surface
        self.clicked_surface = pygame.Surface((32, 32))
        pxarray = pygame.PixelArray(self.clicked_surface)
        pxarray[::1] = 0x7F7F7F
        pxarray[::1, :4] = 0x5F5F5F
        pxarray[:4, ::1] = 0x5F5F5F

        #Makes the mine surface
        self.mine_surface = self.clicked_surface.copy()
        pxarray = pygame.PixelArray(self.mine_surface)
        for y in range(-14, 14):
            for x in range(-14, 14):
                d = x**2+y**2
                if d >= 14**2: continue
                pxarray[x + 16, y + 16] = 0x1F1F1F

        #Makes the flag surface
        self.flag_surface = pygame.Surface((32, 32))
        pxarray = pygame.PixelArray(self.flag_surface)
        pxarray[::1] = 0xAFAFAF
        pxarray[::1, :4] = 0x5F5F5F
        pxarray[:4, ::1] = 0x5F5F5F
        pxarray[6:4, 6::1] = 0x4F4F4F
        pxarray[8:25, 6:20] = 0xFF0000
        
        #Makes the face surface
        self.face_surface = pygame.Surface((32, 32))
        pxarray = pygame.PixelArray(self.face_surface)
        pxarray[::1] = 0
        for y in range(-16, 16):
            for x in range(-16, 16):
                d = x*x+y*y
                if d >= 15**2: continue
                pxarray[x + 16, y + 16] = 0xFFFF00
        
        #Makes the smiley face surface
        self.smiley_surface = self.face_surface.copy()
        pxarray = pygame.PixelArray(self.smiley_surface)
        pxarray[8:12, 8:12] = 0
        pxarray[20:24, 8:12] = 0
        pxarray[8:12, 20:24] = 0
        pxarray[12:16, 24:28] = 0
        pxarray[16:20, 24:28] = 0
        pxarray[20:24, 20:24] = 0
        
        #Makes the sad face surface
        self.sad_surface = self.face_surface.copy()
        pxarray = pygame.PixelArray(self.sad_surface)
        pxarray[8:12, 8:12] = 0
        pxarray[20:24, 8:12] = 0
        pxarray[8:12, 24:28] = 0
        pxarray[12:16, 20:24] = 0
        pxarray[16:20, 20:24] = 0
        pxarray[20:24, 24:28] = 0
        
        #Makes the neutral face surface
        self.neutral_surface = self.face_surface.copy()
        pxarray = pygame.PixelArray(self.neutral_surface)
        pxarray[8:12, 8:12] = 0
        pxarray[20:24, 8:12] = 0
        pxarray[8:12, 20:24] = 0
        pxarray[12:16, 20:24] = 0
        pxarray[16:20, 20:24] = 0
        pxarray[20:24, 20:24] = 0
        
        self.surfaces = {
            UNCLICKED : self.unclicked_surface,
            CLICKED : self.clicked_surface,
            MINE : self.mine_surface,
            FLAG : self.flag_surface,
            HAPPY_FACE : self.smiley_surface,
            SAD_FACE : self.sad_surface,
            NEUTRAL_FACE : self.neutral_surface
            }
        
        self.number_colors = {
            1 : (0, 0, 255),
            2 : (0, 255, 0),
            3 : (0, 128, 128),
            4 : (128, 0, 0),
            5 : (200, 0, 0),
            6 : (255, 0, 0),
            7 : (128, 0, 128),
            8 : (0, 0, 0)
            }
        
        pygame.init()
        self.number_font = pygame.font.SysFont("Lucidia Console, Sans-Serif", 48)
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("Minesweeper")

        self.events = {}
        self.pastEvents = {}
        self.quit = False
    
    def newgame(self):
        self.level = []
        self.world = []
        for l in range(0, self.level_width):
            self.level.append([])
            self.world.append([])

        self.mine_positions = []
        r = random.Random()
        for i in range(0, self.mines_remaining, 1):
            hasFound = False
            while not hasFound:
                pos = (r.randint(0, self.level_width - 1), r.randint(0, self.level_height - 1))
                if not pos in self.mine_positions:
                    self.mine_positions.append(pos)
                    hasFound = True

        for y in range(self.level_height):
            for x in range(self.level_width):
                self.level[x].append(LEVEL_CLEAR)
                self.world[x].append(UNCLICKED)
        for p in self.mine_positions: self.level[p[0]][p[1]] = LEVEL_MINE
        
        for y in range(self.level_height):
            for x in range(self.level_width):
                if self.level[x][y] != LEVEL_MINE:
                    a = self.countTiles(x, y, self.level, LEVEL_MINE)
                    if a != 0:
                        self.level[x][y] = a + 10
                        
        self.flags_remaining = self.mines_remaining
        self.timer = 0
        self.current_face = NEUTRAL_FACE
        self.gameover = False
        self.started = False
        self.won = False
        return    
        
    def update(self):
        self.events = {'keys': pygame.key.get_pressed(),
                      'mousePos': pygame.mouse.get_pos(),
                      'mousePressed': pygame.mouse.get_pressed()
		}
        
        self.won = self.detectWin()
        if self.won:
            self.gameover = True
            self.current_face = HAPPY_FACE
		
        if self.events['mousePressed'][0] and self.pastEvents['mousePressed'][0] == 0:
            if Rect(self.events['mousePos'][0], self.events['mousePos'][1], 1, 1).colliderect(Rect((screen_size[0] / 2) - 16, self.level_height * 32, 32, 32)):
                self.newgame()
            if self.gameover: return
            if self.events['mousePos'][0] < 0 or self.events['mousePos'][1] < 0 or self.events['mousePos'][0] >= self.level_width << 5 or self.events['mousePos'][1] >= self.level_height << 5:
                return
                
            if not self.started: self.started = True
            tx = self.events['mousePos'][0] >> 5
            ty = self.events['mousePos'][1] >> 5
            if self.level[tx][ty] == LEVEL_MINE and self.world[tx][ty] != FLAG:
                self.gameover = True
                self.current_face = SAD_FACE
            if self.world[tx][ty] == UNCLICKED and not self.level[tx][ty] > NUMBER_START:
                self.findSpan(tx, ty)
            if self.level[tx][ty] > NUMBER_START and self.world[tx][ty] != FLAG:
                self.world[tx][ty] = self.level[tx][ty]
            
        if self.events['mousePressed'][2] and self.pastEvents['mousePressed'][2] == 0:
            if self.events['mousePos'][0] < 0 or self.events['mousePos'][1] < 0 or self.events['mousePos'][0] >= self.level_width << 5 or self.events['mousePos'][1] >= self.level_height << 5:
                return
            if self.gameover: return
            tx = self.events['mousePos'][0] >> 5
            ty = self.events['mousePos'][1] >> 5
            if self.world[tx][ty] == UNCLICKED:
                if self.flags_remaining >= 1:
                    self.world[tx][ty] = FLAG
                    self.flags_remaining -= 1
                
            elif self.world[tx][ty] == FLAG:
                self.world[tx][ty] = UNCLICKED
                self.flags_remaining += 1
                
        self.pastEvents = self.events
        return
        
    def countTiles(self, tx, ty, l, t):
        count = 0
        
        if tx >= 1:
            if l[tx-1][ty-0] == t: count += 1
        if ty >= 1:
            if l[tx-0][ty-1] == t: count += 1
        if tx < self.level_width - 1:
            if l[tx+1][ty-0] == t: count += 1
        if ty < self.level_height - 1:
            if l[tx-0][ty+1] == t: count += 1
        if tx >= 1 and ty >= 1:
            if l[tx-1][ty-1] == t: count += 1
        if tx >= 1 and ty < self.level_height - 1:
            if l[tx-1][ty+1] == t: count += 1
        if tx < self.level_width - 1 and ty >= 1:
            if l[tx+1][ty-1] == t: count += 1
        if tx < self.level_width - 1 and ty < self.level_height - 1:
            if l[tx+1][ty+1] == t: count += 1
        return count
        
    def findSpan(self, tx, ty):
        checkTiles = [(tx, ty)]
        checkedTiles = []
        for t in checkTiles:
            if not t in checkedTiles:
                self.world[t[0]][t[1]] = CLICKED
                checkedTiles.append(t)
            else:
                continue
            for x in range(t[0] - 1, t[0] + 2):
                for y in range(t[1] - 1, t[1] + 2):
                    if x == t[0] and y == t[1]: continue
                    if x < 0 or x >= self.level_width or y < 0 or y >= self.level_height: continue
                    if self.level[x][y] > NUMBER_START:
                        self.world[x][y] = self.level[x][y]
                        continue
                    if self.level[x][y] == LEVEL_CLEAR and not self.world[x][y] == FLAG:
                        checkTiles.append((x, y))
        return
        
    def detectWin(self):
        won = True
        for m in self.mine_positions:
            if not self.world[m[0]][m[1]] == FLAG:
                won = False
        won2 = True
        for y in range(0, self.level_height):
            for x in range(0, self.level_width):
                if self.world[x][y] == CLICKED or self.world[x][y] > NUMBER_START: continue
                if (self.world[x][y] == UNCLICKED or self.world[x][y] == FLAG) and self.level[x][y] == LEVEL_MINE:
                    pass
                else:
                    won2 = False
        return won | won2
    def draw(self):
        self.screen.fill(color_black)

        for y in range(0, self.level_height):
            for x in range(0, self.level_width):
                if self.world[x][y] > NUMBER_START:
                    self.screen.blit(self.surfaces[CLICKED], [x << 5, y << 5])
                    self.screen.blit(self.number_font.render(str(self.world[x][y] % 10), 0, self.number_colors[self.world[x][y] % 10]), [(x << 5) + 8, (y << 5) + 3])
                    continue 
                self.screen.blit(self.surfaces[self.world[x][y]], [x << 5, y << 5])
        
        self.screen.blit(self.surfaces[self.current_face], [(screen_size[0] / 2) - 16, self.level_height * 32])
        
        self.screen.blit(self.number_font.render(str(self.flags_remaining), 0, (0xCF, 0, 0)), [(screen_size[0] / 4) - len(str(self.flags_remaining)) * 16, self.level_height << 5])
        self.screen.blit(self.number_font.render(str(self.timer), 0, (0xCF, 0, 0)), [(3 * screen_size[0] / 4) - len(str(self.timer)) * 16 + 16, self.level_height << 5])
        pygame.display.flip()
        return
    def mainLoop(self):
        lastTime = int(round(_time.time() * 1000000000))
        nsPerTick = 1000000000.0/30.0
        delta = 0.0
        ticks, frames = 0, 0
        lastTimer = int(round(_time.time() * 1000))
        
        while not self.quit:
            now = int(round(_time.time() * 1000000000))
            delta += (now - lastTime) / nsPerTick
            lastTime = now
            shouldRender = False
            for event in pygame.event.get():
                if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                    self.quit = True

            while delta >= 1:
                self.update()
                ticks += 1
                shouldRender = True
                delta -= 1

            if self.gameover:
                if self.won:
                    for p in self.mine_positions: self.world[p[0]][p[1]] = FLAG
                else:
                    for y in range(0, self.level_height):
                        for x in range(0, self.level_width):
                            if self.world[x][y] == FLAG and self.level[x][y] == LEVEL_MINE: continue
                            self.world[x][y] = self.level[x][y]

            if shouldRender:
                self.draw()
                frames += 1

            if int(round(_time.time() * 1000)) - lastTimer >= 1000:
                message = str(ticks) + " tps, " + str(frames) + " fps";
                lastTimer = int(round(_time.time() * 1000))
                frames = ticks = 0
                if self.started and not self.gameover:
                    self.timer += 1

            if self.quit:
                pygame.quit()
        return
if __name__ == '__main__':
    game = Game()
    game.mainLoop()