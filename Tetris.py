import pygame
from pygame.locals import *
import time as _time

from random import Random

screen_size = (480, 640)
color_black = (0,0,0)

CLEAR = 0
TILE = 1
TILE_COLOR_OFFSET = 9

LEVEL_WIDTH = 10
LEVEL_HEIGHT = 20

SHAPES = {
    "L" : ("X---",
           "X---",
           "XX--",
           "--XX")
    }

class Game:

    def __init__(self):
        pygame.init()

        self.level = []
        for i in range(0, LEVEL_WIDTH):
            self.level.append([])

        for y in range(0, LEVEL_HEIGHT):
            for x in range(0, LEVEL_WIDTH):
                self.level[x].append(0)

        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("PyGame testing")
        self.clock = pygame.time.Clock()
        
        self.tile_colors = {
            0 : (0, 0, 0),
            1 : (255, 255, 255),
            2 : (100, 100, 100),
            3 : (255, 0, 0),
            4 : (0, 255, 0),
            5 : (0, 0, 255),
            6 : (255, 255, 0),
            7 : (255, 0, 255),
            8 : (0, 255, 255),
            9 : (240, 90, 30)
        }

        self.quit = False
    def update(self):
        key = pygame.key.get_pressed()
        
        return

    def draw(self):
        self.screen.fill(color_black)

        for y in range(0, LEVEL_HEIGHT):
            for x in range(0, LEVEL_WIDTH):
                if self.level[x][y] == 0: continue
                pygame.draw.rect(self.screen, self.tile_colors[self.level[x][y].value - TILE_COLOR_OFFSET], Rect(x << 5, y << 5, 32, 32))

        Shape(None, "L", 11).draw(self.screen)

        pygame.display.flip()
        return

    def mainLoop(self):
        lastTime = int(round(_time.time() * 1000000000))
        nsPerTick = 1000000000.0/60.0
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
            
            if shouldRender:
                self.draw()
                frames += 1

            if int(round(_time.time() * 1000)) - lastTimer >= 1000:
                message = str(ticks) + " tps, " + str(frames) + " fps";
                pygame.display.set_caption(message)
                lastTimer = int(round(_time.time() * 1000))
                frames = ticks = 0

            if self.quit:
                pygame.quit()
        return


class Shape:
    def __init__(self, l, s, c):
        self.level = l
        self.tiles = []
        self.color = c
        
        for i in range(0, 4):
            self.tiles.append([])
        for i in range(0, 16):
            self.tiles[i % 4].append(0)

        for y in range(0, 4):
            for x in range(0, 4):
                if SHAPES[s][y][x] == "X":
                    self.tiles[x][y] = self.color

    def draw(self, screen):
        for y in range(0, 4):
            for x in range(0, 4):
                if self.tiles[x][y] ==  self.color:
                    pygame.draw.rect(screen, (255, 255, 255), Rect(x << 5, y << 5, 32, 32))

if __name__ == '__main__':
    game = Game()
    game.mainLoop()
