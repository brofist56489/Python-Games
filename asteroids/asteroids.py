import pygame
from pygame.locals import *
import time as _time

import math
from random import Random
screen_size = (640, 480)
color_black = (0,0,0)

ASTEROID_COLORS = [(255, 255, 255), (255, 0, 0), (0, 255, 0), (255, 255, 0), (0, 0, 255), (255, 0, 255)]

class Game:

    def __init__(self):
        pygame.init()
        
        self.shipTexture = pygame.image.load("ship.png")
        pxarray = pygame.PixelArray(self.shipTexture)
        
        for y in range(0, 16):
            for x in range(0, 16):
                if pxarray[x, y] == -1 or pxarray[x, y] == 0xFFFFFFFF:
                    pxarray[x, y] = (255, 255, 0)
        
        self.newGame()
    
        self.screen = pygame.display.set_mode((screen_size[0], screen_size[1] + 48))
        pygame.display.set_caption("Asteroids")
        self.clock = pygame.time.Clock()
        self.key = pygame.key.get_pressed()
        self.pastKey = self.key
        
        self.scoreFont = pygame.font.SysFont("Lucidia console, Sans-Serif", 48)
        
        self.quit = False
        
    def newGame(self):
        self.ship = Ship(self)
        self.score = 0
        self.shipsLeft = 10
        self.waveNumber = 0
    
        self.newWave()
        return
        
    def newWave(self):
        self.bullets = []
        self.asteroids = []
        self.waveNumber += 1
        
        self.waveSpawnDelay = 300
        return
        
    def makeAsteroids(self):
        tx = self.ship.x
        ty = self.ship.y
        r = Random()
        
        for i in range(0, self.waveNumber + 3):
            a = r.randint(0, 360) * (math.pi / 180)
            d = 300
            self.asteroids.append(Asteroid(tx + math.cos(a) * d, ty + math.sin(a) * d, 2, a, 2))
        return
        
    def update(self):
        self.tickCount += 1
        self.key = pygame.key.get_pressed()
        
        if self.waveSpawnDelay != -1:
            self.waveSpawnDelay -= 1
        if self.waveSpawnDelay == 0:
            self.waveSpawnDelay -= 1
            self.makeAsteroids()
        
        if len(self.asteroids) == 0 and self.waveSpawnDelay == -1:
            self.newWave()
        
        if self.ship != None:
            self.ship.update(self)
        else:
            if self.key[K_SPACE] and not self.pastKey[K_SPACE] and self.shipsLeft >= 1:
                self.shipsLeft -= 1
                self.ship = Ship(self)
                
        for b in self.bullets:
            b.update(self)
        for a in self.asteroids:
            a.update(self)
            if self.ship == None: continue
            if Circle(a.x + 16 * a.size, a.y + 16 * a.size, 16 * a.size).intersects(Circle(self.ship.x + 8, self.ship.y + 8, 6)):
                self.ship.die(self)
                a.split(self)
        
        self.pastKey = self.key
        return

    def draw(self):
        self.screen.fill(color_black)
        
        for b in self.bullets:
            b.draw(self.screen)
        for a in self.asteroids:
            a.draw(self.screen)
        if self.ship != None:
            self.ship.draw(self.screen)
        else:
            if self.shipsLeft >= 1:
                self.screen.blit(self.scoreFont.render("Press space to respawn", 10, (255, 0, 0)), [screen_size[0] / 2 - (21 * 8), screen_size[1] / 2 - 16])
            else:
                self.screen.blit(self.scoreFont.render("Game over", 10, (255, 0, 0)), [screen_size[0] / 2 - (9 * 8), screen_size[1] / 2 - 16])               
        
        pygame.draw.rect(self.screen, (0, 0, 0), Rect(0, screen_size[1], screen_size[0], 48))
        
        self.screen.blit(self.scoreFont.render("Score: " + str(self.score), 0, (255, 255, 255)), [0, screen_size[1] + 8])
        
        message = "Wave: " + str(self.waveNumber)
        self.screen.blit(self.scoreFont.render(message, 0, (255, 255, 255)), [screen_size[0] - len(message) * 24, screen_size[1] + 8])
        
        for s in range(0, self.shipsLeft):
            self.screen.blit(self.shipTexture, [(screen_size[0] / 2) - ((self.shipsLeft / 2 - s) * 18), screen_size[1] + 16])
         
        pygame.display.flip()
        return

    def mainLoop(self):
        lastTime = int(round(_time.time() * 1000000000))
        nsPerTick = 1000000000.0/60.0
        delta = 0.0
        ticks, frames = 0, 0
        lastTimer = int(round(_time.time() * 1000))
        
        self.tickCount = 0
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
                lastTimer = int(round(_time.time() * 1000))
                frames = ticks = 0

            if self.quit:
                pygame.quit()
        return

class Ship(object):
    def __init__(self, g):
        self.angle = 0.0
        self.movementAngle = 0.0
        self.speed = 0.0
        self.x = screen_size[0] / 2
        self.y = screen_size[1] / 2
        self.originalTexture = g.shipTexture
        return
        
    def checkKey(self, g):
        if g.key[K_UP] or g.key[K_w]:
            self.speed += .5
            self.movementAngle = self.angle
        if g.key[K_LEFT] or g.key[K_a]:
            self.angle -= 5
        if g.key[K_RIGHT] or g.key[K_d]:
            self.angle += 5
        
        if g.key[K_SPACE] and not g.pastKey[K_SPACE]:
            g.bullets.append(Bullet(self.x, self.y, self.angle, self.speed + 5))
        
        if g.key[K_DOWN] or g.key[K_s]:
            self.speed -= .1
        
        if self.speed > 8: self.speed = 8
        if self.speed < 0: self.speed = 0
        
        if self.angle < 0: self.angle = 360 + self.angle
        if self.angle > 360: self.angle -= 360
        return     
    
    def update(self, g):
        self.checkKey(g)
        if self.speed != 0:
            ax = math.cos(self.movementAngle * (math.pi / 180)) * self.speed
            ay = math.sin(self.movementAngle * (math.pi / 180)) * self.speed
            self.x += ax
            self.y += ay
            
        if self.x < 0: self.x += screen_size[0]
        if self.y < 0: self.y += screen_size[1]
        if self.x >= screen_size[0]: self.x -= screen_size[0]
        if self.y >= screen_size[1]: self.y -= screen_size[1]
        
        self.speed -= .10
        if self.speed < 0: self.speed = 0
        return
        
    def die(self, g):
        g.ship = None
        return
        
    def draw(self, screen):
        t = pygame.transform.rotate(self.originalTexture, 360 - self.angle)
    
        screen.blit(t, [self.x, self.y])
        
        render2nd = False
        x2 = self.x
        y2 = self.y
        if self.x >= screen_size[0] - 16:
            render2nd = True
            x2 -= screen_size[0]
        if self.y >= screen_size[1] - 16:
            render2nd = True
            y2 -= screen_size[1]
        if render2nd:
            screen.blit(t, [x2, y2])
        return

class Bullet(object):
    def __init__(self, x, y, a, s):
        self.x = x
        self.y = y
        self.angle = a * (math.pi / 180)
        self.speed = s
        self.texture = pygame.Surface((4, 4))
        self.dist = screen_size[0]
        pxarray = pygame.PixelArray(self.texture)
        pxarray[::1] = 0xFFFFFF
        return
        
    def update(self, g):
        if self.speed != 0:
            px = self.x
            py = self.y
            ax = math.cos(self.angle) * self.speed
            ay = math.sin(self.angle) * self.speed
            self.x += ax
            self.y += ay
            self.dist -= math.sqrt((self.x - px)**2 + (self.y - py)**2)
        if self.x < 0: self.x += screen_size[0]
        if self.y < 0: self.y += screen_size[1]
        if self.x >= screen_size[0]: self.x -= screen_size[0]
        if self.y >= screen_size[1]: self.y -= screen_size[1]
        
        shouldRemove = False
        if self.dist <= 0:
            shouldRemove = True
            
        for a in g.asteroids:
            if Circle(a.x + 16 * a.size, a.y + 16 * a. size, 16 * a.size).intersects(Circle(self.x + 2, self.y + 2, 2)):
                a.split(g)
                shouldRemove = True
        
        if shouldRemove:
            del g.bullets[g.bullets.index(self)]
        return
        
    def draw(self, screen):
        screen.blit(self.texture, [self.x, self.y])
        return

class Asteroid(object):
    def __init__(self, x, y, size, a, speed):
        self.x = x
        self.y = y
        self.size = size
        self.angle = a
        self.speed = speed
        self.color = Random().choice(ASTEROID_COLORS)
        self.texture = pygame.image.load("asteroid.png").convert_alpha()
        px = pygame.PixelArray(self.texture)
        for y in range(self.texture.get_height()):
            for x in range(self.texture.get_width()):
                if(px[x, y] in [0xffffffff, -1]):
                    px[x, y] = self.color
        px = None
        self.texture = pygame.transform.scale(self.texture, [int(32 * self.size), int(32 * self.size)])
        return
        
    def update(self, g):
        if self.speed != 0:
            ax = math.cos(self.angle) * self.speed
            ay = math.sin(self.angle) * self.speed
            self.x += ax
            self.y += ay
        
        if self.x < 0: self.x += screen_size[0]
        if self.y < 0: self.y += screen_size[1]
        if self.x >= screen_size[0]: self.x -= screen_size[0]
        if self.y >= screen_size[1]: self.y -= screen_size[1]
        return
        
    def split(self, g):
        r = Random()
        if not self.size == .5:
            g.asteroids.append(Asteroid(self.x, self.y, self.size / 2, r.randint(0, 360) * (math.pi / 180), self.speed * 1.3))
            g.asteroids.append(Asteroid(self.x + 32 * (self.size / 2), self.y + 32 * (self.size / 2), self.size / 2, r.randint(0, 360) * (math.pi / 180), self.speed * 1.3))

        g.score += 10
        del g.asteroids[g.asteroids.index(self)]
        
        return
        
    def draw(self, screen):
        screen.blit(self.texture, [self.x, self.y])
        render2nd = False
        x2 = self.x
        y2 = self.y
        if self.x >= screen_size[0] - 32 * self.size:
            render2nd = True
            x2 -= screen_size[0]
        if self.y >= screen_size[1] - 32 * self.size:
            render2nd = True
            y2 -= screen_size[1]
        if render2nd:
            screen.blit(self.texture, [x2, y2])
        return

class Circle():
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r
        return
        
    def intersects(self, c):
        d = (self.x - c.x)**2 + (self.y - c.y)**2
        r = (self.r + c.r)**2
        if (d <= r):
            return True
        else:
            return False
            
if __name__ == '__main__':
    game = Game()
    game.mainLoop()

