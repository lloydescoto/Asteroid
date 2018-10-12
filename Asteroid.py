import pygame
import random
pygame.init()
pygame.mixer.init()

vec = pygame.math.Vector2
WIDTH = 1000
HEIGHT = 600
FPS = 60
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Asteriods")
rocketSound = pygame.mixer.Sound("Rocket-SoundBible.wav")
def makeTextObjects(text,font):
    textSurf = font.render(text,True,(255,255,255))
    return textSurf, textSurf.get_rect()
def instructionMessage(text):
    smallFont = pygame.font.SysFont("Arial",50)
    textSurf, textRect = makeTextObjects(text,smallFont)
    textRect.center = (WIDTH/2,(HEIGHT/2)-200)
    screen.blit(textSurf,textRect)
def scoreMessage(text):
    smallFont = pygame.font.SysFont("Arial",30)
    textSurf, textRect = makeTextObjects(text,smallFont)
    textRect.center = (70,30)
    screen.blit(textSurf,textRect)
def gameoverMessage(text):
    largeFont = pygame.font.SysFont("Arial",70)
    textSurf, textRect = makeTextObjects(text,largeFont)
    textRect.center = (WIDTH/2,HEIGHT/2)
    screen.blit(textSurf,textRect)
class Rocket(pygame.sprite.Sprite):
    images = []
    moving = []
    movingCounter = 1
    score = 0
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = self.images[0]
        self.original = self.image
        self.position = vec(WIDTH/2,HEIGHT/2)
        self.rect = self.image.get_rect(center=self.position)
        self.acceleration = vec(0,-0.2)
        self.velocity = vec(0,0)
        self.angle_speed = 0
        self.angle = 0
    def update(self):
        keypress = pygame.key.get_pressed()
        if keypress[pygame.K_LEFT]:
            rocketSound.play()
            self.angle_speed = -1
            self.image = self.images[1]
            self.original = self.image
            rocket.rotate()
        if keypress[pygame.K_RIGHT]:
            rocketSound.play()
            self.angle_speed = 1
            self.image = self.images[2]
            self.original = self.image
            rocket.rotate()
        if keypress[pygame.K_UP]:
            rocketSound.play()
            self.velocity += self.acceleration
            self.image = self.moving[self.movingCounter]
            self.movingCounter = (self.movingCounter + 1) % len(self.moving)
            self.original = self.image
            rocket.rotate()
        if keypress[pygame.K_DOWN]:
            rocketSound.play()
            self.velocity -= self.acceleration
            self.image = self.moving[self.movingCounter]
            self.movingCounter = (self.movingCounter + 1) % len(self.moving)
            self.original = self.image
            rocket.rotate()
        if self.velocity.length() > 9:
            self.velocity.scale_to_length(9)
        if self.velocity.length() == 0:
            self.image = self.images[0]
            self.original = self.image
            rocket.rotate()
        self.position += self.velocity
        self.rect.center = self.position
    def rotate(self):
        self.acceleration.rotate_ip(self.angle_speed)
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle -= 360
        if self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.original,-self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
    def warp(self):
        if self.position.x > WIDTH:
            self.position.x = 0
        if self.position.x < 0:
            self.position.x = WIDTH
        if self.position.y > HEIGHT:
            self.position.y = 0
        if self.position.y < 0:
            self.position.y = HEIGHT
class Asteriod(pygame.sprite.Sprite):
    lives = 1
    direction = "None"
    def __init__(self):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.image = pygame.image.load("asteroid.png")
        self.original = self.image
        self.rect = self.image.get_rect()
        self.indicator = random.randrange(1,5)
        if self.indicator == 1:
            self.direction = "North"
        if self.indicator == 2:
            self.direction = "South"
        if self.indicator == 3:
            self.direction = "West"
        if self.indicator == 4:
            self.direction = "East"
        if self.direction == "North":
            self.rect.y = 0
            self.rect.x = random.randrange(0,WIDTH)
        if self.direction == "South":
            self.rect.y = HEIGHT
            self.rect.x = random.randrange(0,WIDTH)
        if self.direction == "West":
            self.rect.x = 0
            self.rect.y = random.randrange(0,HEIGHT)
        if self.direction == "East":
            self.rect.x = WIDTH
            self.rect.y = random.randrange(0,HEIGHT)
        self.angle_speed = 1
        self.angle = 0
    def update(self):
        if self.direction == "North":
            self.rect.y += 3
        if self.direction == "South":
            self.rect.y -= 3
        if self.direction == "West":
            self.rect.x += 3
        if self.direction == "East":
            self.rect.x -= 3
        if self.rect.x > WIDTH:
            self.rect.x = 0
        if self.rect.y > HEIGHT:
            self.rect.y = 0
        if self.rect.x < 0:
            self.rect.x = WIDTH
        if self.rect.y < 0:
            self.rect.y = HEIGHT
        self.angle += self.angle_speed
        if self.angle > 360:
            self.angle = 0
        if self.angle < 0:
            self.angle = 360
        self.image = pygame.transform.rotate(self.original,-self.angle)
class Background(pygame.sprite.Sprite):
    def __init__(self,background_image,location):
        pygame.sprite.Sprite.__init__(self)
        self.image = background_image
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
Rocket.images.append(pygame.image.load("rocket1.png"))
Rocket.images.append(pygame.image.load("rocket2a.png"))
Rocket.images.append(pygame.image.load("rocket2b.png"))
Rocket.moving.append(Rocket.images[1])
Rocket.moving.append(Rocket.images[2])
space = pygame.image.load("stars.png")
clock = pygame.time.Clock()
keepGoing = True
allSprite = pygame.sprite.RenderUpdates()
asteriods = pygame.sprite.Group()
Rocket.containers = allSprite
Asteriod.containers = allSprite, asteriods
rocket = Rocket()
background = Background(space,[0,0])
while keepGoing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepGoing = False
    screen.fill((0,0,0))
    screen.blit(background.image,background.rect)
    if rocket.score == 5:
        allSprite.empty()
        gameoverMessage("Game Over")
    else:
        rocket.warp()
        if random.randrange(0,100) < 3:
            asteriods.add(Asteriod())
        instructionMessage("[Arrow Keys to Move]")
        scoreMessage("Collision : " + str(rocket.score))
        allSprite.update()
        allSprite.draw(screen)
        for meteor in pygame.sprite.spritecollide(rocket,asteriods,0):
            meteor.image = pygame.image.load("redasteroid.png")
            meteor.original = meteor.image
            meteor.lives = 0
        rocket.score = 0
        for meteor in asteriods:
            if meteor.lives == 0:
                rocket.score += 1
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()