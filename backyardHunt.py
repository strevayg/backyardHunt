######################################################
#   File: backyardHunt
#   Purpose: Implementing a game of collection to satisfy
#       CS118 group project requirements 
#   Authors: Gabby, Rae, and Nakia 
#   Resources:
#       Link used to implement consisted character movement with key holds
#           https://www.pygame.org/docs/ref/key.html#:~:text=Using%20bitwise%20operators%20you%20can%20test%20if%20specific%20modifier%20keys%20are%20pressed.&text=Create%20a%20bitmask%20of%20the,to%20impose%20on%20your%20program.&text=When%20the%20keyboard%20repeat%20is,KEYDOWN%20events.
#       Link used to help understand a lot of the pygame rendering of fonts
#           https://www.pygame.org/docs/ref/font.html#pygame.font.Font
#       Link used to understand pygame 
#           https://www.youtube.com/watch?v=AY9MnQ4x3zk
######################################################

import pygame
import random
from sys import exit #used to completely quit game
import characterClass as CC #seperate file with character class

# Start the game to display things, has to be first or wont work
pygame.init()

######################################################
#   Variables used in the program 
######################################################

#used to determine one style/size of text display
screenTextLook0 = pygame.font.SysFont('Comic Sans MS', 60) 
screenTextLook1 = pygame.font.SysFont('Comic Sans MS', 30) 
screenTextLook2 = pygame.font.SysFont('Comic Sans MS', 20) 
 
# Rectangles used 2 see if we should display text based on where character
# is on the screen (ie over the bones? then display the collect text)
# Last one is over the hole rectangle
textDisplayList = [
    #[x mins],[x maxs],[y mins],[y maxs]
    [0,400,760,759,320], 
    [80,540,850,850,500], 
    [0,220,480,45,500], 
    [50,310,550,125,560]
]
# Init text stuff for startup menu 
screenText1 = screenTextLook0.render("How to Win", False, 'Black')
screenText2 = screenTextLook1.render(
    "* Collect bones, one at a time, in the correct color order", 
    False, 
    'Black')
screenText6 = screenTextLook1.render(
    "* Collection order is random!",
    False,
    'Black')
screenText3 = screenTextLook1.render(
    "* Deposit at the hole",
    False,
    'Black')
screenText4 = screenTextLook1.render(
    "Press 'D' to play as a dog or press 'C' to play as a Cat!",
    False,
    'Black')
screenText5 = screenTextLook1.render(
    "* Bone colors to collect: red, yellow, and blue",
    False,
    'Black')
screenText7 = screenTextLook1.render(
    "* Use AWSD or arrow keys to move",
    False,
    'Black')

# By just having this line you only see for a second or so bc its one frame
#hence the loop to continuously display
screen = pygame.display.set_mode((952,608)) #dimension of the background image 
backgroundPhoto = pygame.image.load('background.png') #background photo of game
bonePhoto = pygame.image.load('bone.png') #bones in the game
redBonePhoto = pygame.image.load('redBone.png')
yellowBonePhoto = pygame.image.load('yellowBone.png')
blueBonePhoto = pygame.image.load('blueBone.png')
# Set the size for the redBonePhoto
DFLT_IMG_SZ = (50, 49)
# Scale the image to your needed size
redBonePhoto = pygame.transform.scale(redBonePhoto, DFLT_IMG_SZ)
yellowBonePhoto = pygame.transform.scale(yellowBonePhoto, DFLT_IMG_SZ)
blueBonePhoto = pygame.transform.scale(blueBonePhoto, DFLT_IMG_SZ)
# Where bones will be placed on screen
boneList = [
    [5,5], [820,500], [820,75],[450,250]
]
isCollectedRed = False 
isCollectedYellow = False 
isCollectedBlue = False 

# Used to know which right bone actually should display a colored bone later
randomNumber = random.randint(1, 2) + 1
if randomNumber == 2:
    randomNumberIs2 = True
else:
    randomNumberIs2 = False

# Possible combinations    
winningOrder = [
    ['red', 'yellow', 'blue'],
    ['red', 'blue', 'yellow'],
    ['yellow', 'red', 'blue'],
    ['yellow', 'blue', 'red'],
    ['blue', 'red', 'yellow'],
    ['blue', 'yellow', 'red']
]

#random order of collection 
randomIndex = random.randint(0,5)
colorList = winningOrder[randomIndex]
print(colorList)

randomIndex = random.randint(0,5) # Which list w/in WinningOrder 2 use 
colors = 'noneYet'
colorsIndex = 0
index = 0 # Used to see if done for collection
randomIndex = random.randint(0,5) # Which list w/in WinningOrder 2 use 
# red, yellow, blue true or false basically
noRepeatCollections = [1,1,1]

# Arrays for character animation and initalization 
#   Indexes 0-1 are for Dog: Right, Left 
#   Indexes 2-3 are for Cat: Right, Left 

characterAnimationD = [
    [
        'characterR_Dog0.png',
        'characterR_Dog1.png',
        'characterR_Dog2.png',
        'characterR_Dog0.png',
        'characterR_Dog1.png',
        'characterR_Dog2.png',
        'characterR_Dog1.png',
        'characterR_Dog2.png'
    ],
    [
        'characterR_Dog0.png',
        'characterR_Dog1.png',
        'characterR_Dog2.png',
        'characterR_Dog0.png',
        'characterR_Dog1.png',
        'characterR_Dog2.png'
    ]
]
characterAnimationC = [
    [
        'characterR_Cat0.png',
        'characterR_Cat1.png',
        'characterR_Cat1.png',
        'characterR_Cat1.png',
        'characterR_Cat2.png',
        'characterR_Cat2.png',
        'characterR_Cat2.png',
        'characterR_Cat0.png'
    ],
    [
        "characterUpR_Cat0.png",
        "characterUpR_Cat1.png",
        "characterUpR_Cat1.png",
        "characterUpR_Cat2.png",
        "characterUpR_Cat2.png",
        "characterUpR_Cat0.png" 

    ]
]

isDogCharacter = True 
movement = 'UPKEY'
######################################################
# Start game stuff
######################################################
clock = pygame.time.Clock() #Init game clock
screen.fill('white') # Fill background with white
pygame.display.set_caption("Backyard Hunt")

# Start initial menu display with rules/explanation
gamePlay = True
stopProgram = True
while(gamePlay):
    screen.blit(screenText1,(300, 30))
    screen.blit(screenText2,(100, 150))
    screen.blit(screenText6,(100, 215))
    screen.blit(screenText5,(100, 280))
    screen.blit(screenText3,(100, 345))
    screen.blit(screenText7,(100, 410))
    screen.blit(screenText4,(85, 500))

    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  # Quit gameplay
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d or pygame.K_c:
                gamePlay = False
                if event.key == pygame.K_c:
                    isDogCharacter = False
    pygame.display.update()
    clock.tick(60)  # 60 times per second

screen.fill('#458a21') # Will fill background with green of grass 
# Write over old values for the actual game needs of the text 
screenText1 = screenTextLook1.render("Collect/Drop?", False, 'Black')
screenText2 = screenTextLook2.render("Press 'X'", False, 'Black')
screenText3 = screenTextLook1.render("Drop?", False, 'Black')
screenText4 = screenTextLook2.render("Press 'X'", False, 'Black')

if isDogCharacter:
    character = CC.Character(characterAnimationD) # Dog
else:
    character = CC.Character(characterAnimationC) # Cat 

# Start main game 
gamePlay = True
while gamePlay and stopProgram:
    # Draw everything
    screen.blit(backgroundPhoto, (0, 0))
    #no black border for character, sets transparancy 
    screen.set_colorkey((0, 0, 0)) 
    for i in range(4):
        screen.blit(bonePhoto, boneList[i])
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()  
            gamePlay = False
        elif event.type == pygame.KEYDOWN:
            #pygame.key.set_repeat(50, 50)
            if event.key in (pygame.K_LEFT, pygame.K_a):
                movement = 'left'
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                movement = 'right'
            elif event.key in (pygame.K_UP, pygame.K_w):
                movement = 'up'
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                movement = 'down'
            elif event.key == pygame.K_q:
                gamePlay = False # Dont want to play anymore
        elif event.type == pygame.KEYUP:
                movement = 'UPKEY'


        # Key press for 'X' only if character is over a bone
        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            # Check if the character is over any of the bone regions
            # If over a bone rectangle then can collect the bone
            for i in range(5):
                if textDisplayList[0][i] <= character.x <= textDisplayList[1][i] \
                    and textDisplayList[2][i] <= character.y <= textDisplayList[3][i]:
                        for j in range(3):
                            # textDisplayList[0][0] -> are we at top left bone?
                            # textDisplayList[0][1] -> are we at middle of the screen bone? 
                            # textDisplayList[0][2 or 3]are we at bottom far right or high far right?
                            # different per gameplay based off randomNumber
                            if textDisplayList[0][i] == textDisplayList[0][j]:
                                # Which index of the randomized list is 1 and collect that bone color
                                #   How we decide which photo is which bone from the randomized list per play 
                                #   2nd & 3rd arguments make sure you cant collect when  holding another color
                                #   Fourth argument is so you cant pick up a bone color you already deposited 
                                for k in range(3):
                                    # The actual random bone placement is 2 but on index 3
                                    if randomNumberIs2 and k == 3: 
                                        break
                                    if colorList[j] == colorList[k]:
                                        #colorsIndex = k #used to see which one you have collected 
                                        if colorList[k] == 'red' and not isCollectedBlue and not isCollectedYellow and noRepeatCollections[0]:
                                            isCollectedRed = not isCollectedRed
                                            colors = 'red'
                                            break
                                        elif colorList[k] == 'yellow' and not isCollectedBlue and not isCollectedRed and noRepeatCollections[1]:
                                            isCollectedYellow = not isCollectedYellow
                                            colors = 'yellow'
                                            break
                                        elif colorList[k] == 'blue' and not isCollectedRed and not isCollectedYellow and noRepeatCollections[2]:
                                            isCollectedBlue = not isCollectedBlue
                                            colors = 'blue'
                                            break
                        # Are we at hole? and can deposit?
                        if textDisplayList[0][i] == textDisplayList[0][4]:
                            if index < 3:
                                # If you have the correct one you can deposit it
                                if winningOrder[randomIndex][index] == colors:
                                    # Switch the state if they can deposit 
                                    match colors:
                                        case 'red':
                                            if isCollectedRed and noRepeatCollections[0]:
                                                noRepeatCollections[0] = 0
                                                isCollectedRed = not isCollectedRed
                                                index += 1 # Increment because properly collected 
                                            else:
                                                pass
                                        case 'yellow':
                                            if isCollectedYellow and noRepeatCollections[1]:
                                                noRepeatCollections[1] = 0
                                                isCollectedYellow = not isCollectedYellow
                                                index += 1 # Increment because properly collected 
                                            else:
                                                pass
                                        case 'blue':
                                            if isCollectedBlue and noRepeatCollections[2]:
                                                noRepeatCollections[2] = 0
                                                isCollectedBlue = not isCollectedBlue
                                                index += 1 # Increment because properly collected 
                                            else:
                                                pass
                                    if index >= 3:
                                        gamePlay = False
                                        index = "winner"
                            break
                        # Do nothing for last/other bone, dont allow for anything to be collected 
                        else:
                            pass

    character.move(movement)
    # Update character position
    character.update()

    # Game is over!
    if index == "winner":
        screenText1 = screenTextLook1.render("WINNER!!", False, 'Black')
        screen.blit(screenText1, (390, 200))                   

    # Display Collect message if character is over a bone
    for i in range(5):
        if textDisplayList[0][i] <= character.x <= textDisplayList[1][i] \
            and textDisplayList[2][i] <= character.y <= textDisplayList[3][i]:
            # Need this so the colored bone shows not just for a split second 
            # pygame.key.set_repeat() 
            if i >= 4:
                screen.blit(screenText3, (420, 5))  # Display Deposit?
                screen.blit(screenText4, (422, 40))  # Display Press 'X'
            else:
                screen.blit(screenText1, (370, 5))  # Display Collect/Drop?
                screen.blit(screenText2, (422, 40))  # Display Press 'X'
    
    # Show red bone if collected
    if isCollectedRed and noRepeatCollections[0]:
        screen.blit(redBonePhoto, (5, 550))  # Display redBone
    if isCollectedYellow and noRepeatCollections[1]:
        screen.blit(yellowBonePhoto, (5, 550))  # Display yellowBone
    if isCollectedBlue and noRepeatCollections[2]:
       screen.blit(blueBonePhoto, (5, 550))  # Display blueBone

    # Update the display
    character.draw(screen)
    pygame.display.update()
    clock.tick(35)  # 60 times per second

# Essentially a pausing function, will delay the game for 3000 milliseconds
pygame.time.wait(3000)  # Pauses execution for 3 seconds                  
pygame.quit()
exit()  # Quit gameplay
