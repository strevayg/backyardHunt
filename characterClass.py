######################################################
#   File: characterClass 
#   Purpose: Implementing class for character used in backyardHunt file
#   Authors: Gabby 
#   Resources:
#       Link used to implement character movement with key presses from awsd or arrow keys 
#           https://pythonprogramming.altervista.org/how-to-move-player-in-pygame-with-keys/
######################################################

import pygame 

# Character class that inits the starting position of the character
class Character:
    def __init__(self, characterAnimation):
        """ Initializes character object used for game 
            Parameters: None
            Returns: Initialized character object """
        # positioning
        self.x = 242
        self.y = 448
        self.velocity = 0 #init movement
        self.pos = self.x, self.y
        self.goingRight = True
        self.characterAnimation = characterAnimation
        self.currentFrame = 0
        self.currentImage = self.characterAnimation[0][0]
        self.direction = 'down'
        # Load image file [104 × 49]
        self.DFLT_IMG_SZ = (150, 150)
        self.characterPhoto = pygame.image.load(self.currentImage)
        self.characterPhoto = pygame.transform.scale(self.characterPhoto, self.DFLT_IMG_SZ)

        # Puts characterPhoto at 242,448 
        # x,y on screen from the middle of the bottom of the image 
        self.characterRect = \
            self.characterPhoto.get_rect(midbottom = (242,448))
        self.lastUpdated = 0
        self.delayUpdate = 0
        self.lastIndex = 0


    def update(self):
        """ movement data to change x & y accordingly to update position
            Parameters: N/A
            Returns: Updated character rectangle based on wanted movement """
        self.characterRect.topleft = (self.x, self.y)

    def draw(self, display):
        """ display character to screen
            Parameters: display
            Returns: Updated character display """
        display.blit(self.characterPhoto,self.characterRect)


    def animate(self):
        isDown = False
        now = pygame.time.get_ticks()
        if self.direction in ['left','right','up']:
            if now - self.lastUpdated > 100:
                    self.lastUpdated = now
                    # wrap around mod 4 bc length of the animations
                    self.currentFrame = (self.currentFrame + 1) % 8
                    if self.direction in ['left','right']:
                            isDown = False
                            self.currentImage = self.characterAnimation[0][self.currentFrame]
                            self.lastIndex = 0
                    else:
                        isDown = False
                        self.currentFrame = (self.currentFrame + 1) % 6
                        self.currentImage = self.characterAnimation[1][self.currentFrame]
                        self.lastIndex = 1
        elif self.direction == 'down':
            isDown = True
            if now - self.lastUpdated > 50:
                self.currentFrame = (self.currentFrame + 1) % 6
                self.currentImage = self.characterAnimation[1][self.currentFrame]
                self.lastIndex = 1
        else: #upkey
            self.currentImage = self.characterAnimation[0][0]

        self.characterPhoto = pygame.image.load(self.currentImage)
        self.characterPhoto = pygame.transform.scale(self.characterPhoto, self.DFLT_IMG_SZ)
        if (not self.goingRight):
            self.characterPhoto = pygame.transform.flip(self.characterPhoto, True, False)
            if self.direction == 'down':
                self.characterPhoto = pygame.transform.rotate(self.characterPhoto, 65)
        elif (self.direction == 'down'):
            self.characterPhoto = pygame.transform.rotate(self.characterPhoto, -65)
        else:
            pass




    def move(self, direction1):
        """collect movement data to change x & y accordingly to update position
            Parameters: direction: string 
            Returns: Updated character x or y value based on wanted movement """
        self.direction = direction1 
       #CREATE LIST WITH THE CAT AND DOG POSITIONS AND THEN TRAVERSE THROUGH TO CREATE "ANIMATIONS"
        if self.direction == "left":
            self.goingRight = False
            # Keep character in frame completely (dont let off screen)
            if self.x -10 < 0:
                self.x = 0
            else:
                self.x -= 10

        elif self.direction == "right":
            self.goingRight = True
            # Keep character in frame completely
            # 845 was the right max x value 
            if self.x + 10 > 845:
                self.x = 845
            else:
                self.x += 10

        elif self.direction == "up":
             # Keep character in frame completely
            if self.y - 10 < 0:
                self.y = 0
            else:
                self.y -= 10

        elif self.direction == "down":
            #keep character in frame completely
            # 560 was the right max y value 
            if self.y + 10 > 480:
                self.y = 480 
            else:
                self.y += 10
        else: #do nothing
            pass
        self.animate()