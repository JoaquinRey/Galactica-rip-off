import numpy
import pygame
from random import randint
import time

pygame.font.init()
#a matric which provides the spawn of enemies
placement = []
#the movement speed of the player
MOVEMENTSPEED = 1
#laser speed along y coord
LASERYSPEED = 2
#laser speed when diagonal
LASERXSPEED = 2
#constant colors
white = (255,255,255)
black= (0,0,0)
#size of the display
width = 600 
height = 600
Screen = pygame.display.set_mode((width, height))
screenThing = pygame.image.load(r'images\space.jpg')
ship1 = pygame.image.load(r'images\ship.png')
ship2 = pygame.image.load(r'images\ship.png')
ship3 = pygame.image.load(r'images\ship.png')
Screen.fill(white)
game = True
#speed of the Enemy lasers
ELSpeed = 1
score = 0
ships = 3
sprites = {}
#wave is the amount of change the shots are shot at each wave
wave = 1.5
#potato is how often they shoot laser beams
potato = 2000
#enemy lasers
ELasers = []
#enemy direction of travel
eDir = 'l'
#list used for spawning enemies
enemies = []
#list for spawning lasers
laserC = []
secondsHeld = 0
#EX and EY are the displacement of the enemy spawns
EX = 0
EY = 0
#PX and PY are the player's coords
PX = 270
PY = 470
playerModel = pygame.image.load(r'images\ship.png')
position = playerModel.get_rect()
myfont = pygame.font.SysFont('Comic Sans MS', 30)


class player:

    def __init__(self):
        self.lives = 3
        self.dir = None
        if (self.dir == 'a') or (self.dir == 'aw') or (self.dir == 'sa') or (self.dir == 'd') or (self.dir == 'wd') or (self.dir == 'ds'):
            player.hitbox = pygame.Rect(PX,PY,100,100)
        if (self.dir == None) or (self.dir == 's') or (self.dir == 'w'):
            player.hitbox = pygame.Rect(PX,PY,50,100)
            
    def move(self):
        global PX
        global PY
        secondsHeld = 0
        self.movementSpeed = numpy.tanh(secondsHeld) * MOVEMENTSPEED        
        while self.dir == 'wd':
            if PY > 250:
                PY -= MOVEMENTSPEED
            if PX < 525:
                PX += MOVEMENTSPEED
            getEvents()
            live()
        while self.dir == 'ds':           
            if PY < 525:
                PY += MOVEMENTSPEED
            if PX < 525:
                PX += MOVEMENTSPEED
            getEvents()
            live()           
        while self.dir == 'sa':            
            if PX > 0:
                PX -= MOVEMENTSPEED
            if PY < 525:
                PY += MOVEMENTSPEED
            getEvents()
            live()           
        while self.dir == 'aw':          
            if PX > 0:
                PX -= MOVEMENTSPEED
            if PY > 250:
                PY -= MOVEMENTSPEED
            getEvents()
            live()          
        while self.dir == 'w':           
            if PY > 250:
                PY -= MOVEMENTSPEED
            getEvents()   
            live()  
        while self.dir == 'd':           
            if PX < 525:
                PX += MOVEMENTSPEED
            getEvents()
            live()           
        while self.dir == 's':           
            if PY < 525:
                PY += MOVEMENTSPEED
            getEvents()
            live()            
        while self.dir == 'a':           
            if PX > 0:
                PX -= MOVEMENTSPEED
            getEvents()
            live()            
        if self.dir == None:
            pass
class enemy:

    def __init__(self, tier, x, y):
        self.tier = tier
        self.x = x + EX
        self.y = y + EY
        self.origenX = self.x
        self.origenY = self.y
        self.model = pygame.image.load(r'images\Enemy0' + str(tier) + '.png')
        self.hitbox = pygame.Rect(self.x,self.y,50,50)
        sprites[self.model] = (f'{x},{y}') 
    
    def takeDamage(self):
        self.model = pygame.image.load(r'images\Enemy0' + str(self.tier) + '.png')
    def move(self):
        global eDir
        if eDir == 'l':
            if ((abs(self.x - self.origenX)) <= 50):
                self.x -= 1
            if ((abs(self.x - self.origenX)) > 50):
                eDir = 'r'
                self.x += 1
        elif eDir == 'r':
            if ((abs(self.x - self.origenX)) <= 50):
                self.x += 1
            if ((abs(self.x - self.origenX)) > 50):
                eDir = 'l'
                self.x -= 1
    def uninstall(self):
        global score
        score += 50 * self.tier
        enemies.remove(self)

class laserBeam:

    def __init__(self):

        self.dir = player.dir
        if (self.dir == None) or (self.dir == 's') or (self.dir == 'w'):
            self.x = PX+22
            self.y = PY-15
            self.model = pygame.image.load(r'images\laserBeam.png')
            self.hitbox = pygame.Rect(self.x,self.y,4,20)
        if (self.dir == 'a') or (self.dir == 'aw') or (self.dir == 'sa'):
            self.x = PX+15
            self.y = PY-15
            self.model = pygame.image.load(r'images\laserBeamA.png')
            self.hitbox = pygame.Rect(self.x,self.y,15,20)
        if (self.dir == 'd') or (self.dir == 'wd') or (self.dir == 'ds'):
            self.x = PX+70
            self.y = PY-15
            self.model = pygame.image.load(r'images\laserBeamD.png')
            self.hitbox = pygame.Rect(self.x,self.y,15,20)

        #dlaserS.append(self.model)
    def move(self):
        if (self.dir == None) or (self.dir == 's') or (self.dir == 'w'):
            self.y -= LASERYSPEED
        if (self.dir == 'a') or (self.dir == 'aw') or (self.dir == 'sa'):
            self.y -= LASERXSPEED
            self.x -= LASERXSPEED
        if (self.dir == 'd') or (self.dir == 'wd') or (self.dir == 'ds'):
            self.y -= LASERXSPEED
            self.x += LASERXSPEED

    def uninstall(self):
        self.x = 1000
        self.y = 1000

class ELaser:
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.model = pygame.image.load(r'images\ELaser.png')
        self.hitbox = pygame.Rect(self.x,self.y,4,20)

    def move(self):
        self.y += int(ELSpeed)
    
    def uninstall(self):
        global game
        ELasers.remove(self)
        if player.lives > 1:
            player.lives -= 1
        else:
            game = False

#checks to see if there are collisions
def checkCollide():
    for laser in laserC:
        if laser.model == pygame.image.load(r'images\laserBeam.png'):
            laser.hitbox = pygame.Rect(laser.x,laser.y,4,20)
        else:
            laser.hitbox = pygame.Rect(laser.x,laser.y,15,20)
        for enemy in enemies:
            enemy.hitbox = pygame.Rect(enemy.x,enemy.y,50,50)
            if (pygame.Rect.colliderect(laser.hitbox,enemy.hitbox)):
                laser.uninstall()
                enemy.uninstall()
    for Elaser in ELasers:
        Elaser.hitbox = pygame.Rect(Elaser.x,Elaser.y,4,20)
        if (player.dir == 'a') or (player.dir == 'aw') or (player.dir == 'sa') or (player.dir == 'd') or (player.dir == 'wd') or (player.dir == 'ds'):
            player.hitbox = pygame.Rect(PX,PY,100,100)
        if (player.dir == None) or (player.dir == 's') or (player.dir == 'w'):
            player.hitbox = pygame.Rect(PX,PY,50,100)
        
        if (pygame.Rect.colliderect(Elaser.hitbox,player.hitbox)):      
            Elaser.uninstall()
#displays all the images
def live():
    pygame.event.pump()
    newWave()
    textsurface = myfont.render(f'Score: {score}', False, (255, 255, 255))
    Screen.blit(screenThing,(0,0))
    Screen.blit(playerModel,(PX,PY))
    if player.lives >= 1:
        Screen.blit(ship1,(10,500))
    if player.lives >= 2:
        Screen.blit(ship2,(50,500))
    if player.lives == 3:
        Screen.blit(ship3,(90,500))
    Screen.blit(textsurface, (0,0)) 
    for enemy in enemies:
        Screen.blit(enemy.model, (enemy.x,enemy.y))
        enemy.takeDamage()
        enemy.move()
        value = randint(0,potato)
        if value == 1:
            ELasers.append(ELaser(enemy.x,enemy.y))
    for laser in laserC:
        Screen.blit(laser.model,(laser.x,laser.y))
        laser.move()
        if (laser.x <= -50) or (laser.x >= 650) or (laser.y <= -50):
            laserC.remove(laser)
    for laser in ELasers:
        if (laser.y > 700):
            ELasers.remove(laser)
        Screen.blit(laser.model,(laser.x,laser.y))
        laser.move()
    checkCollide()
    pygame.display.update()

#checks for inputs
def getEvents():
    global playerModel
    for event in pygame.event.get() :
        # if event object type is QUIT
        # then quitting the pyame
        # and program both.
        if event.type == pygame.QUIT :       
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  
                #summon a laser
                laserC.append(laserBeam())

            #determines which direction the player moves
        if event.type == pygame.KEYUP:
            player.dir = None
            playerModel = pygame.image.load(r'images\ship.png')
        if pygame.key.get_pressed()[pygame.K_w] and pygame.key.get_pressed()[pygame.K_d]:
            player.dir = 'wd'
            playerModel = pygame.image.load(r'images\shipRIGHTTILTFORWARD.png')
        if pygame.key.get_pressed()[pygame.K_d] and pygame.key.get_pressed()[pygame.K_s]:
            player.dir = 'ds'
            playerModel = pygame.image.load(r'images\shipRIGHTTILT.png')
        if pygame.key.get_pressed()[pygame.K_s]and pygame.key.get_pressed()[pygame.K_a]:
            player.dir = 'sa'
            playerModel = pygame.image.load(r'images\shipLEFTTILT.png')
        if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed()[pygame.K_w]:
            player.dir = 'aw'
            playerModel = pygame.image.load(r'images\shipLEFTTILTFORWARD.png')
        if pygame.key.get_pressed()[pygame.K_w] and pygame.key.get_pressed().count(1) == 1:
            player.dir = 'w'
            playerModel = pygame.image.load(r'images\shipForward.png')
        if pygame.key.get_pressed()[pygame.K_s] and pygame.key.get_pressed().count(1) == 1:
            player.dir = 's'
            playerModel = pygame.image.load(r'images\ship.png')
        if pygame.key.get_pressed()[pygame.K_d] and pygame.key.get_pressed().count(1) == 1:
            player.dir = 'd'
            playerModel = pygame.image.load(r'images\shipRIGHTTILT.png')
        if pygame.key.get_pressed()[pygame.K_a] and pygame.key.get_pressed().count(1) == 1:
            player.dir = 'a'
            playerModel = pygame.image.load(r'images\shipLEFTTILT.png')

def newWave():
    global potato
    global wave
    global ELSpeed

    if len(enemies) == 0:
        for i in range(5):
            enemies.append(enemy(3,100*i+70,50))
        for i in range(5):
            enemies.append(enemy(2,100*i+70,100))
        for i in range(5):
            enemies.append(enemy(1,100*i+70,150))
        if potato > 50:
            potato -= 50
        ELSpeed = ELSpeed + 0.5
#runs the game
def RunGame():
# conditional loop
    global PY
    global PX
    while game==True :
        live()
        #blits the images on the screen
        getEvents()  
        player.move()
        pygame.display.update()


player = player()

RunGame()

