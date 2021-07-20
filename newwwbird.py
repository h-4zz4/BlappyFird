print('BlappyFird, by h_4zz4 on github')
try:
    import pygame
    from pygame.locals import *
except:
    print('You do not have the pygame module installed. You can do this by typing "pip install pygame" in the CMD command line,\nand checking that python is installed to PATH')
try:
    import keyboard
except:
    print('You do not have the keyboard module installed. You can do this by typing "pip install keyboard" in the CMD command line,\nand checking that python is installed to PATH')
import random

from pygame.version import PygameVersion

'''
gaming time
github: h_4zz4
'''

clock = pygame.time.Clock()
win = pygame.display.set_mode((300,600))
hardMode = False
filepath = (__file__)
filepath = (filepath[:len(filepath) - 12] + 'assets/')
bird1 = pygame.image.load(filepath + 'bird1.png')
bird2 = pygame.image.load(filepath + 'bird2.png')
bird3 = pygame.image.load(filepath + 'bird3.png')
icon = pygame.image.load(filepath + 'birdicon.png')
pipeFaceUp = pygame.image.load(filepath + 'pipe.png')
g = pygame.image.load(filepath + 'ground.png')
title = pygame.image.load(filepath + 'title.png')
gameOver = pygame.image.load(filepath + 'gameover.png')
pressSpace = pygame.image.load(filepath + 'spacebar.png')
num0 = pygame.image.load(filepath + '0.png')
num1 = pygame.image.load(filepath + '1.png')
num2 = pygame.image.load(filepath + '2.png')
num3 = pygame.image.load(filepath + '3.png')
num4 = pygame.image.load(filepath + '4.png')
num5 = pygame.image.load(filepath + '5.png')
num6 = pygame.image.load(filepath + '6.png')
num7 = pygame.image.load(filepath + '7.png')
num8 = pygame.image.load(filepath + '8.png')
num9 = pygame.image.load(filepath + '9.png')
hard = pygame.image.load(filepath + 'hard.png')

pygame.display.set_caption('Blappy Fird')
pygame.display.set_icon(icon)

pipeFaceDown = pygame.transform.rotate(pipeFaceUp, 180)
bg = pygame.image.load(filepath + 'bg.png')
bird1 = pygame.transform.scale(bird1, (51, 36))
bird2 = pygame.transform.scale(bird2, (51, 36))
bird3 = pygame.transform.scale(bird3, (51, 36))
gameOver = pygame.transform.scale(gameOver, (200, 40))
title = pygame.transform.scale(title, (180, 50))
pressSpace = pygame.transform.scale(pressSpace, (128, 128))
hard = pygame.transform.scale(hard, (175,17))
birds = [bird1, bird2, bird3]
numbers = [num0, num1, num2, num3, num4, num5, num6, num7, num8, num9]

pygame.mixer.init()
jumpSound = pygame.mixer.Sound(filepath + 'wing.wav')
pointSound = pygame.mixer.Sound(filepath + 'point.wav')

x = 500
y = 250
x2 = 500
y2 = -375

vel = 0
tick_counter = 0
currentbird = 1
height = 0
score = 0
templateVariable = 0
bestscore = 0
rotation = 0
pipeGap = 25

canPause = True
enableScore = True
isTitle = True

class Bird():
    def __init__(self,x,y,vel,tick_counter, currentbird, height, score, rotation):
        self.x = x
        self.y = y
        self.vel = vel
        self.tick_counter = tick_counter
        self.currentbird = currentbird
        self.height = height
        self.score = score
        self.rotation = rotation
    def jump(self):
        self.tick_counter = 0
        self.height = self.y
    def move(self):
        self.tick_counter += 1
        if self.tick_counter < 6:
            self.y -= 6
        elif self.tick_counter < 10:
            self.y -= 4
        elif self.tick_counter < 16:
            self.y -= 2
        elif self.tick_counter < 20:
            self.y -= 1
        elif self.tick_counter < 23:
            self.y += 1
        elif self.tick_counter < 26:
            self.y += 2
        elif self.tick_counter < 28:
            self.y += 3
        elif self.tick_counter < 35:
            self.y += 4
        elif self.tick_counter < 45:
            self.y += 6
        else:
            self.y += 7  #i know it's janky but this works well
    def draw(self, win):
        if self.tick_counter % 5 == 0:#fix this \\ did i fix it? i cant even remember
            if self.currentbird < 3:
                self.currentbird += 1
            else:
                self.currentbird = 1
        z = self.y
        self.rotation = 45 - (self.tick_counter*2)
        if self.rotation > 20:
            act_rotation = 45
        elif self.rotation < -90:
            self.rotation = -90
            act_rotation = -90
        else:
            act_rotation = self.rotation
        rotated_image = pygame.transform.rotate(birds[self.currentbird-1], self.rotation)   
        new_rect = rotated_image.get_rect(center = birds[self.currentbird-1].get_rect(topleft = (120, self.y)).center)
        win.blit(rotated_image, new_rect.topleft) #inspired by Rabbid76 on StackOverflow
        #                                          github-h_4zz4
    def die(self, win, pipeFunc):
        win.blit(bg, (0, -50))
        pipeFunc.move(win)
        win.blit(g, (0, 550))
        rotated_image = pygame.transform.rotate(birds[self.currentbird-1], self.rotation)   
        new_rect = rotated_image.get_rect(center = birds[self.currentbird-1].get_rect(topleft = (120, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        win.blit(gameOver, (50, 100))
        win.blit(pressSpace, ((150-64), 350))
        pygame.display.update()
        keyboard.wait('space')
        pipe.reset()
        self.y = 150
    def collisionDraw(self,win,piperect1,piperect2, pipeFunc): #soon to be obsolete!
        birdRect = pygame.draw.rect(win,(0,0,0), (120,self.y, 51,36))
        if birdRect.colliderect(piperect1) == True or birdRect.colliderect(piperect2) or self.y > 550 - 36 or self.y < - 20:
            birdd.die(win, pipeFunc)
class Pipes():
    def __init__(self, x, y, tv, x2,y2, score, bestscore, enableScore, pipeGap):
        self.x = x
        self.x2 = x2
        self.y2 = y2
        self.y = y
        self.win = win
        self.tv = tv
        self.score = score
        self.bestscore = score
        self.enableScore = enableScore
        self.scoreArray = []
        self.bestScoreArray = []
        self.pipeGap = pipeGap
    def move(self, win):
        self.x -= 2
        if self.x < (-72):
            self.x = 300
            randnum = random.randint(100, 500)
            self.y = randnum
            self.y2 = randnum - (600 + self.pipeGap)
            self.enableScore = True
        if self.x < 100 and self.enableScore == True:
            self.scoreArray = []
            pointSound.play()
            self.score += 1
            self.enableScore = False
            for c in str(self.score):
                self.scoreArray.append(numbers[int(c)])             # ((16*int(c))+10,5))
        if self.score > self.bestscore:
            self.bestscore = self.score
            self.bestScoreArray = []
            for ch in str(self.bestscore):
                self.bestScoreArray.append(numbers[int(ch)])
        win.blit(pipeFaceUp,(self.x,self.y))
        win.blit(pipeFaceDown,(self.x, self.y2))
        zzz = 0
        yyy = 0
        for entry in self.scoreArray:
            win.blit(self.scoreArray[zzz], ((24*int(zzz))+10, 5))
            zzz += 1
        for entryy in self.bestScoreArray:
            win.blit(self.bestScoreArray[yyy], ((24*int(yyy))+10, 45))
            yyy += 1
        font = pygame.font.SysFont("verdana", 32)
    def pcollisionDraw(self,win,birdd, pipeFunc):
        upfPipeRect = pygame.draw.rect(win,(0,0,100), (self.x, self.y, 72, 500))
        downfPipeRect = pygame.draw.rect(win,(0,100,0), (self.x, self.y2, 72, 500))
        birdd.collisionDraw(self.win, upfPipeRect, downfPipeRect, pipeFunc)
    def reset(self):
        self.x = 500
        self.y = 250
        self.y2 = -365
        self.score = 0
        self.enableScore = True
        self.scoreArray = [num0]
class Ground():
    def __init__(self, x, win):
        self.x = x
    def moveDraw(self,birdd):
        win.blit(g, (self.x, 550))
        self.x -= 2
        if self.x <= -24:
            self.x = 0
        
birdd = Bird(x,y, vel, tick_counter, currentbird, height,score,rotation)
pipe = Pipes(x,y,templateVariable, x2, y2, score, bestscore, enableScore, pipeGap)
ground = Ground(templateVariable, win)
pygame.init()
pygame.mixer.init()
win.blit(bg, (0, -50))
while True:
    if hardMode == True:
        win.blit(hard, (150, 10))
    pipe.move(win)
    birdd.move()
    birdd.draw(win)
    ground.moveDraw(birdd)
    if isTitle == True:
        win.blit(title, (60, 100))
        win.blit(pressSpace, ((150-64), 350))
        pygame.display.update()
        isTitle = False
        keyboard.wait('space')
    keys = pygame.key.get_pressed()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                jumpSound.play()
                birdd.jump()
            elif event.key == K_ESCAPE:
                pygame.quit()
                break
            if event.key == K_b and canPause == True:
                canPause = False
                keyboard.wait('b')
            else:
                canPause = True
            if event.key == K_h:
                hardMode = True
                s = pygame.Surface((1000,1000)) 
                s.set_alpha(160)              
                s.fill((255,0,0))            
        if event.type == pygame.MOUSEBUTTONDOWN:
            birdd.jump()
    pygame.display.update()
    pipe.pcollisionDraw(win, birdd, pipe)
    win.blit(bg, (0,-50))
    if hardMode == True:
        win.blit(s, (0,0))
# github: h_4zz4
# i'm aware that this code is awful, i just find the game fun :)