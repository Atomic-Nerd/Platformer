import random
import pygame

from pygame import mixer
from Levels import LevelsGrid
from Levels import CheckpointCoords

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
mixer.init()

screen_width = 1000
screen_height = 600

player_width = 30
player_height = 60

cubewidth = 40

window = pygame.display.set_mode((screen_width,screen_height))

clock = pygame.time.Clock()
fps = 60

#------------- FONT -------------#

font = pygame.font.SysFont('8bitwondernominal', 40, True)

#---------- BACKGROUND ----------#

BACKGROUND_PNG = pygame.image.load("Images/Background/background.png")

#--------- TEXT SPRITES ---------#

COLLECTALLCOINS_PNG = pygame.image.load("Images/Text/collectallcoins.png")

#--------- GAME SPRITES ---------#

BORDER_PNG = pygame.image.load("Images/Map_Sprites/border.png")
DIRT_PNG = pygame.image.load("Images/Map_Sprites/dirt.png")
GRASS_PNG = pygame.image.load("Images/Map_Sprites/grass.png")
ARROWRIGHT_PNG = pygame.image.load("Images/Map_Sprites/arrowright.png")
ARROWLEFT_PNG = pygame.image.load("Images/Map_Sprites/arrowleft.png")

FULLHEART_PNG = pygame.image.load("Images/Map_Sprites/fullheart.png")
EMPTYHEART_PNG = pygame.image.load("Images/Map_Sprites/emptyheart.png")

CLOSEDDOORBOTTOM_PNG = pygame.image.load("Images/Map_Sprites/closeddoorbottom.png")
CLOSEDDOORTOP_PNG = pygame.image.load("Images/Map_Sprites/closeddoortop.png")

OPENDOORBOTTOM_PNG = pygame.image.load("Images/Map_Sprites/opendoorbottom.png")
OPENDOORTOP_PNG = pygame.image.load("Images/Map_Sprites/opendoortop.png")

COIN_PNG = pygame.image.load("Images/Map_Sprites/coin.png")

LAVA_PNG = pygame.image.load("Images/Map_Sprites/lava.png")
LAVAWHOLE_PNG = pygame.image.load("Images/Map_Sprites/lavawhole.png")

LEVERLEFT_PNG = pygame.image.load("Images/Map_Sprites/leverleft.png")
LEVERRIGHT_PNG = pygame.image.load("Images/Map_Sprites/leverright.png")

#---------- GAME SOUNDS ---------#

LAVA_WAV = pygame.mixer.Sound("Sounds/lava.wav")
OPENDOOR_WAV = pygame.mixer.Sound("Sounds/opendoor.wav")
JUMP_WAV = pygame.mixer.Sound("Sounds/jump.wav")
COIN_WAV = pygame.mixer.Sound("Sounds/coin.wav")
ERROR_WAV = pygame.mixer.Sound("Sounds/error.wav")
NEXTLEVEL_WAV = pygame.mixer.Sound("Sounds/nextlevel.wav")
MENUTICK_WAV = pygame.mixer.Sound("Sounds/menutick.wav")
MENUSELECT_WAV = pygame.mixer.Sound("Sounds/menuselect.wav")

#------------ MUSIC -------------#

pygame.mixer.music.load("Sounds/music.wav")

#---------- GRID CODES ----------#

GRIDECODES = {
    1 : BORDER_PNG,
    2 : DIRT_PNG,
    3 : GRASS_PNG,
    4 : ARROWRIGHT_PNG,
    5 : ARROWLEFT_PNG,
    6 : CLOSEDDOORBOTTOM_PNG,
    7 : CLOSEDDOORTOP_PNG,
    8 : LAVAWHOLE_PNG,
    9 : LAVA_PNG,
    10 : COIN_PNG,
    11 : LEVERLEFT_PNG,
    12 : LEVERRIGHT_PNG
}

#------------ TILES -------------#

TILEBLOCKS = [1,2,3]

tile_list = []

#------------ PLAYER ------------#

class Player():
    def __init__(self, x, y, speed):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f'Images/Player_Sprites/guy{num}.png')
            img_right = pygame.transform.scale(img_right, (player_width, player_height))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.vel_y = 0
        self.jumped = False
        self.direction = "R"
        self.landed = True
        self.health = 3

    def atcheckpoint(self,level):

        if CheckpointCoords[level][1]+40 > self.rect.y > CheckpointCoords[level][1]:
            if CheckpointCoords[level][0] < self.rect.x < CheckpointCoords[level][0]+40:
                return True

        return False

    def nearcheckpoint(self,level):

        if CheckpointCoords[level][1]+40 > self.rect.y > CheckpointCoords[level][1]:
            if CheckpointCoords[level][0]-40 < self.rect.x < CheckpointCoords[level][0]+40:
                window.blit(OPENDOORTOP_PNG, (CheckpointCoords[level][0], CheckpointCoords[level][1]))
                window.blit(OPENDOORBOTTOM_PNG, (CheckpointCoords[level][0], CheckpointCoords[level][1] + 40))
                return True

        return False

    def drawhealth(self):

        gap = 10
        first_gap = 50

        first_empty_gap = 146

        for i in range(self.health):
            window.blit(FULLHEART_PNG, (first_gap+ 38*i+gap*i, first_gap))

        for i in range(3-self.health):
            window.blit(EMPTYHEART_PNG, (first_empty_gap-38*i-gap*i, first_gap))

    def update(self,drawhitbox,level):

        key = pygame.key.get_pressed()

        dx = 0
        dy = 0

        walk_cooldown = 10

        if key[pygame.K_0]:
            print (self.rect.x, self.rect.y)
        if key[pygame.K_SPACE] and self.jumped == False and self.landed == True:
            if playsound: JUMP_WAV.play()
            self.vel_y = -15
            self.landed = False
            self.jumped = True
        if not(key[pygame.K_SPACE]):
            self.jumped = False
        if key[pygame.K_a] or key[pygame.K_LEFT]:
            self.direction = "L"
            self.counter += 1
            dx -= self.speed
        if key[pygame.K_d] or key[pygame.K_RIGHT]:
            self.direction = "R"
            self.counter += 1
            dx += self.speed
        if key[pygame.K_a] == False and key[pygame.K_LEFT] == False and key[pygame.K_d] == False and key[pygame.K_RIGHT] == False:
            self.index = 0
            self.counter = 0
            if self.direction == "R":
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]

        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            if self.direction == "R":
                self.image = self.images_right[self.index]
            else:
                self.image = self.images_left[self.index]

        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y

        for tile in tile_list:
            if tile.colliderect(self.rect.x + dx, self.rect.y, player_width, player_height):
                dx = 0
            if tile.colliderect(self.rect.x, self.rect.y + dy, player_width, player_height):
                if self.vel_y < 0:
                    dy = tile.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.landed = True
                    dy = tile.top - self.rect.bottom
                    self.vel_y = 0

        for tile in lava_list:
            if tile.colliderect(self.rect.x, self.rect.y + dy-20, player_width, player_height):
                if playsound:
                    LAVA_WAV.play()
                player.takedamage()


        for i in range(len(coin_list)):
            tile = coin_list[i]
            if tile.colliderect(self.rect.x, self.rect.y, player_width, player_height):
                if playsound: COIN_WAV.play()
                LevelsGrid[level][coin_coords[i][0]][coin_coords[i][1]] = 0
                coin_coords.pop(i)
                coin_list.pop(i)
                break

        self.rect.x += dx
        self.rect.y += dy

        window.blit(self.image, self.rect)
        if drawhitbox:
            pygame.draw.rect(window, (255, 255, 255), self.rect, 2)

    def takedamage(self):

        player.health -= 1
        if player.health > 0:
            player.rect.x = 45
            player.rect.y = screen_height - player_height - 80
        else:
            outoflives()

player = Player(45, screen_height-player_height-80, 4)

def fadenextlevel():
    fade = pygame.Surface((screen_width,screen_height))
    fade.fill((0,0,0))
    if playsound: NEXTLEVEL_WAV.play()
    for alpha in range(75):
        fade.set_alpha(alpha)
        window.blit(fade,(0,0))
        pygame.display.update()
        pygame.time.delay(20)

def outoflives():
    main_menu()

def drawgrid(LevelsGrid,level,drawhitbox, newlevel):

    global tile_list
    global lava_list
    global coin_list
    global coin_coords

    if newlevel:
        tile_list = []
        lava_list = []
        coin_list = []
        coin_coords = []

    window.blit(BACKGROUND_PNG, (0,0))

    for row in range(15):
        for coloumn in range(25):
            if LevelsGrid[level][row][coloumn] != 0:
                img = GRIDECODES[LevelsGrid[level][row][coloumn]]
                img_rect = img.get_rect()
                img_rect.x = coloumn*cubewidth
                img_rect.y = row*cubewidth

                window.blit(img,(img_rect.x,img_rect.y))

                if LevelsGrid[level][row][coloumn] in TILEBLOCKS:
                    if newlevel:
                        tile_list.append(img_rect)
                    if drawhitbox:
                        pygame.draw.rect(window,(255,255,255),(coloumn*cubewidth,row*cubewidth,cubewidth,cubewidth),1)

                if LevelsGrid[level][row][coloumn] == 10:
                    if newlevel:
                        coin_coords.append([row,coloumn])
                        coin_list.append(img_rect)
                    if drawhitbox:
                        pygame.draw.rect(window,(255,255,255),(coloumn*cubewidth,row*cubewidth+15,cubewidth,cubewidth),1)

                if LevelsGrid[level][row][coloumn] == 9:
                    if newlevel:
                        lava_list.append(img_rect)
                    if drawhitbox:
                        pygame.draw.rect(window,(255,255,255),(coloumn*cubewidth,row*cubewidth+15,cubewidth,cubewidth),1)
    return False

def pause():

    loop = True
    cursor_index = 1

    while loop:

        pygame.draw.rect(window,(0,0,0),(100,100,800,400))
        pygame.draw.rect(window,(255,255,255),(110,110,780,380),4)
        drawtext("Pause",400,150)
        drawtext("Back",400,350)
        drawtext("*",350,350)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    loop = False
                    if playsound: MENUSELECT_WAV.play()
                if event.key == pygame.K_RETURN:
                    if playsound: MENUSELECT_WAV.play()
                    loop = False

        pygame.display.update()


def drawtext(string,x,y):

    text_surface = font.render(string, True, (255,255,255))
    window.blit(text_surface, (x,y))

def draw_main_menu(cursor_location,cursor_locations):

    window.fill((0,0,0))
    drawtext("Main Menu", 300,200)
    drawtext("Play", 250,350)
    drawtext("Options", 250,400)
    drawtext("Credits", 250,450)
    cursor_y = cursor_locations[cursor_location]
    drawtext("*", 200, cursor_y)
    pygame.display.update()

def options():

    global playsound

    index = 0
    loop = True
    if playsound == True:
        onoff = "on"
    else:
        onoff = "off"

    while loop:

        window.fill((0, 0, 0))
        drawtext("Options", 300, 200)
        drawtext("Main Menu", 250, 450)
        drawtext(f"Sound {onoff}",275, 300)

        if index == 0:
            drawtext("*", 200, 450)
        else:
            drawtext("*", 225, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if playsound: MENUSELECT_WAV.play()
                    if index == 0:
                        loop = False
                    else:
                        if onoff == "on":
                            onoff = "off"
                            playsound = False
                        else:
                            onoff = "on"
                            playsound = True

                if event.key == pygame.K_w and index != 1:
                    if playsound: MENUSELECT_WAV.play()
                    index += 1
                if event.key == pygame.K_s and index != 0:
                    if playsound: MENUSELECT_WAV.play()
                    index -= 1

        pygame.display.update()


def credits():

    window.fill((0,0,0))
    drawtext("Credits", 300,200)
    drawtext("Me LOL", 300,280)

    drawtext("Main Menu", 250, 450)
    drawtext("*", 200, 450)

    pygame.display.update()

    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if playsound: MENUSELECT_WAV.play()
                    loop = False


def main_menu():

    global playsound

    mainmenu = True
    cursor_index = 0
    cursor_locations = [350,400,450]
    playsound = True

    while mainmenu:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w and cursor_index > 0:
                    if playsound: MENUTICK_WAV.play()
                    cursor_index -= 1
                if event.key == pygame.K_s and cursor_index < 2:
                    if playsound: MENUTICK_WAV.play()
                    cursor_index += 1
                if event.key == pygame.K_RETURN:
                    if playsound: MENUSELECT_WAV.play()
                    if cursor_index == 0:
                        mainmenu = False
                    elif cursor_index == 1:
                        options()
                    elif cursor_index == 2:
                        credits()

        draw_main_menu(cursor_index,cursor_locations)

    main()

def main():
    clock.tick(fps)

    player.health = 3

    run = True
    drawhitbox = False

    if playsound: pygame.mixer.music.play(-1,0)

    level = 0
    newlevel = True

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause()

        newlevel = drawgrid(LevelsGrid,level,drawhitbox,newlevel)
        AtDoor = player.nearcheckpoint(level)

        if AtDoor:
            if replay:
                replay = False
                if playsound: OPENDOOR_WAV.play()
            if player.atcheckpoint(level):
                if len(coin_list) == 0:
                    fadenextlevel()
                    level += 1
                    newlevel = True
                    player.rect.x = 45
                    player.rect.y = screen_height-player_height-80
                else:
                    if replay2:
                        if playsound: ERROR_WAV.play()
                        replay2 = False
                    window.blit(COLLECTALLCOINS_PNG,(150,250))
                    pygame.display.update()
            else:
                replay2 = True
        else:
            replay = True

        player.update(drawhitbox, level)
        player.drawhealth()

        pygame.display.update()

main_menu()