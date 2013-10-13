import pygame
from pygame.locals import *
import time as _time
screen_size = (640, 480)
color_black = (0,0,0)


class Game:

    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(screen_size)
        pygame.display.set_caption("PyGame testing")
        self.clock = pygame.time.Clock()
        
        self.screen = Screen(6)

        self.quit = False
    def update(self):
        key = pygame.key.get_pressed()
        
        return

    def draw(self):
        self.screen.fill(0xff)

        self.screen.draw_circle(50, 50, 25, 0xff00)
        for i in range(0, int(640 / 6), 1):
            self.screen.place_pixel(i, i, 0xff0000)

        self.screen.draw_to_display(self.display)
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
            shouldRender = True
            
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

class Screen:
    def __init__(self, scale):
        
        self.width = screen_size[0]
        self.height = screen_size[1]
        self.text = pygame.Surface((self.width, self.height))
        self.pixels = pygame.PixelArray(self.text)
        self.scale = scale
        return

    def place_pixel(self, x, y, c):
        scale = self.scale
        x *= scale
        y *= scale
        x2 = x + scale
        y2 = y + scale
        if x < 0 or y < 0 or x >= self.width or y >= self.height: return
        self.pixels[x:x2, y:y2] = c
        return

    def fill(self, c):
        self.pixels[::1] = c
        return

    def draw_circle(self, xp, yp, r, c):
        for y in range(-r, r, 1):
            for x in range(-r, r, 1):
                d = x * x + y * y
                if(d >= r * r): continue

                self.place_pixel(xp + x, yp + y, c)
        return

    def draw_to_display(self, display):
        self.pixels = None
        display.blit(self.text, [0, 0])
        self.pixels = pygame.PixelArray(self.text)
        return

if __name__ == '__main__':
    game = Game()
    game.mainLoop()
