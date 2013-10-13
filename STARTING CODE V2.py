import pygame
from pygame.locals import *
import time as _time
screen_size = (640, 480)
color_black = (0,0,0)


class Game:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("PyGame testing")
        self.clock = pygame.time.Clock()
        
        self.quit = False
    def update(self):
        key = pygame.key.get_pressed()
        
        return

    def draw(self):
        self.screen.fill(color_black)
        
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

if __name__ == '__main__':
    game = Game()
    game.mainLoop()
