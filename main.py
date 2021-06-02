# Import library for keyboard, mouse inputs and display
import sys

import pygame

# Initializes library pygame and pygames font
pygame.init()
pygame.font.init()

# Defines colours used
red = (218, 86, 72)
green = (66, 151, 71)
blue = (65, 80, 214)

# Defines the size of the window
screenWidth = 1200
screenHeigh = 800

# Defines how many bricks there will be.
cols = 6
rows = 6

# Game variables
playing = False
mainMenu = True
controlSelect = False
gameOver = 0
score = 0
useMouse = None


# Creates the Bricks
class Bricks:
    def __init__(self):
        # Sets the width and height of each brick
        self.width = screenWidth // cols
        self.height = 50

        # Stores each brick
        self.bricks = []

        # Stores bricks in the row
        self.eachBrick = []

    # Creates the bricks
    def createBricks(self):
        # For each row
        for row in range(rows):
            # Stores each row
            brickRow = []
            # For each collum
            for col in range(cols):
                # Sets the X and Y value of the top left of each brick
                brickX = col * self.width
                brickY = row * self.height
                # Draws the bricks
                Rect = pygame.Rect(brickX, brickY, self.width, self.height)
                # Checks if the row is of the first third of the rows
                if row < rows // 3:
                    # Sets the brick heath to 3
                    health = 3
                # Checks if the row is of the first third of the rows
                elif row < (rows // 3) * 2:
                    # Sets the brick heath to 2
                    health = 2
                # Checks if the row is of the first third of the rows
                elif row < (rows // 3) * 3:
                    # Sets the brick heath to 1
                    health = 1
                # Stores the brick and health in a list
                eachBrick = [Rect, health]
                # Adds the brick and brick health to the row
                brickRow.append(eachBrick)
            # Adds the row to the bricks list
            self.bricks.append(brickRow)

    # Shows the bricks
    def showBricks(self):
        # For each row in the bricks list
        for row in self.bricks:
            # For each brick in the row
            for brick in row:
                # Checks the heath of the bricks
                if brick[1] == 3:
                    # Sets the brick colour
                    brickColour = red
                # Checks the heath of the bricks
                elif brick[1] == 2:
                    # Sets the brick colour
                    brickColour = green
                # Checks the heath of the bricks
                elif brick[1] == 1:
                    # Sets the brick colour
                    brickColour = blue
                # Draws the bricks
                pygame.draw.rect(canvas, brickColour, brick[0])
                # Draws the bricks border
                pygame.draw.rect(canvas, (0, 0, 0), (brick[0]), 1)


# Creates Paddle
class Paddle:
    def __init__(self):
        # Sets the width and height of the paddle
        self.height = 20
        self.width = screenWidth // cols

        # Sets the x and y position of the paddle
        self.x = (screenWidth // 2) - (self.width // 2)
        self.y = screenHeigh - (self.height * 2)

        # Defines the rectangle
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Sets the direction and speed of the brick
        self.direction = 0
        self.speed = 10

        # Saves the old mouse x pos for use later
        self.oldMouseX = 0

    # Allows you to move the paddle with your keyboard
    def keyboardmove(self):
        # Resets the saved direction of the paddle
        self.direction = 0

        # Sets pressed key in a variable
        key = pygame.key.get_pressed()

        # Checks if you push the left arrow key
        if key[pygame.K_LEFT] and self.rect.left > 0:
            # Moves the paddle
            self.rect.x -= self.speed
            # Sets the direction of the paddle
            self.direction = -1

        # Checks if you push the left arrow key
        if key[pygame.K_RIGHT] and self.rect.right < screenWidth:
            # Moves the paddle
            self.rect.x += self.speed

            # Sets the direction of the paddle
            self.direction = 1

    # Allows you to move the paddle with your mouse
    def mouseMove(self):
        # Resets the save direction of the mouse
        self.direction = 0
        # Gets the mouse pos tuple and convert it to the variables mouseX and mouseY
        mouseX, mouseY = pygame.mouse.get_pos()
        # Check if the mouseX position is greater than the old mouseX position
        if mouseX > self.oldMouseX:
            # Sets the direction to right
            self.direction = 1
        # Check if the mouseX position is less than the old mouseX position
        if mouseX < self.oldMouseX:
            # Sets the direction to left
            self.direction = 1
        # Move the paddle to the mouseX position
        self.rect.x = mouseX - self.rect.width / 2
        # Save the old mouseX
        self.oldMouseX = mouseX

    # Draws the paddle
    def show(self):
        pygame.draw.rect(canvas, red, self.rect)


# Creates the ball
class Ball:
    # When ball is called require a x and y value
    def __init__(self, x, y):
        # Sets the balls radius
        self.radius = 10
        # Sets the X and Y coordinates of the ball
        self.x = x - self.radius
        self.y = y
        # Defines the balls hit-box
        self.rect = pygame.Rect(self.x, self.y, self.radius * 2, self.radius * 2)
        # Sets the speed and the max speed of the ball.
        self.speedX = 4
        self.speedY = -4
        self.maxSpeed = 5
        # Sets how a game over happened
        self.gameOver = 0

    # Moves the ball
    def move(self):
        # Allows the score to be set
        global score
        # Defines the hit threshold
        threshold = 5
        # Resets the brickDestroyed variable
        bricksDestroyed = True
        # Creates the row counter
        rowC = 0
        # For each row in bricks list
        for row in bricks.bricks:
            # Creates the item counter
            itemC = 0
            # For each item in the row
            for item in row:
                # Checks if the ball collides with a brick
                if self.rect.colliderect(item[0]):
                    # Checks if the ball collides with the top of the brick
                    if abs(self.rect.bottom - item[0].top) < threshold and self.speedY > 0:
                        # Moves the ball in the opposite y direction
                        self.speedY *= -1
                    # Checks if the ball collides with the bottom of the brick
                    if abs(self.rect.top - item[0].bottom) < threshold and self.speedY < 0:
                        # Moves the ball in the opposite y direction
                        self.speedY *= -1
                    # Checks if the ball collides with the left of the brick
                    if abs(self.rect.right - item[0].left) < threshold and self.speedX > 0:
                        # Moves the ball in the opposite x direction
                        self.speedX *= -1
                    # Checks if the ball collides with the right of the brick
                    if abs(self.rect.left - item[0].right) < threshold and self.speedX < 0:
                        # Moves the ball in the opposite x direction
                        self.speedX *= -1
                    # adds 10 to the score
                    score += 10
                    # Checks if the health of the brick is greater than 1
                    if bricks.bricks[rowC][itemC][1] > 1:
                        # Lowers the health of the bricks
                        bricks.bricks[rowC][itemC][1] -= 1
                    # If the heath is not greater than 1
                    else:
                        # Make the brick invisible and moves it off screen.
                        bricks.bricks[rowC][itemC][0] = (-100, -100, 0, 0)

                # Checks if the there are bricks left
                if bricks.bricks[rowC][itemC][0] != (-100, -100, 0, 0):
                    # Sets bricks destroyed to be false
                    bricksDestroyed = False
                # Adds 1 to the item Counter
                itemC += 1
            # Adds 1 to the row counter
            rowC += 1

        # Checks if all bricks are destroyed
        if bricksDestroyed:
            # Sets gameOver
            self.gameOver = 1
        # Checks if the ball collide with the left or right side of the screen
        if self.rect.left < 0 or self.rect.right > screenWidth:
            # Reverse the balls x direction
            self.speedX *= -1
        # Checks if the ball collide with the top of the screen
        if self.rect.top < 0:
            # Reverse the balls Y direction
            self.speedY *= -1
        # Checks if the ball collide with the bottom of the screen
        if self.rect.bottom > screenHeigh:
            # Sets gameOver to state that you lost
            self.gameOver = -1

        # Checks if the ball collides with the paddle
        if self.rect.colliderect(paddle):
            # Checks if the paddle collides with the top of the paddle
            if abs(self.rect.bottom - paddle.rect.top) < threshold and self.speedY > 0:
                # Reverse the y direction
                self.speedY *= -1
                # Increases the X speed of the ball
                self.speedX += paddle.direction
                # Checks if the X speed of the ball is greater then the max speed
                if self.speedX > self.maxSpeed:
                    # Sets the X speed of the ball to the max speed
                    self.speedX = self.maxSpeed
                # Checks if the x speed is less then 0 and if the x speed is less than negative the max speed
                elif self.speedX < 0 and self.speedX < -self.maxSpeed:
                    # Sets the X speed to the negative of the max speed
                    self.speedX = -self.maxSpeed
            # Checks if it does not collide with the top of the paddle
            else:
                # Reverse the x speed
                self.speedX *= -1

        # Moves the ball the amount of the current ball speed
        self.rect.x += self.speedX
        self.rect.y += self.speedY

        # Returns the game over state
        return self.gameOver

    # Lets you draw the ball
    def show(self):
        # Draws the ball
        pygame.draw.circle(canvas, red, (self.rect.x + self.radius, self.rect.y + self.radius), self.radius)


# Creates the menu
class Menus:
    def __init__(self):
        # Sets the title font
        self.titleF = pygame.font.Font("ARIAL.TTF", 100)
        # Sets the rest if the buttons font
        self.font = pygame.font.Font("ARIAL.TTF", 45)
        # Creates a rectangle the size of the each label to check if it gets clicked in the game loop
        self.play = pygame.Rect(screenWidth / 2 - 88 / 2, screenHeigh - 100, 88, 51)
        self.mouse = pygame.Rect(screenWidth / 2 - 135 / 2, screenHeigh - 250, 135, 51)
        self.keyboard = pygame.Rect(screenWidth / 2 - 198 / 2, screenHeigh - 150, 198, 51)
        self.keepPlaying = pygame.Rect(screenWidth / 2 - 181 / 2, screenHeigh - 250, 181, 51)
        self.toMenu = pygame.Rect(screenWidth / 2 - 277 / 2, screenHeigh - 150, 277, 51)

    # Shows the Main Menu
    def Main(self):
        # Shows the title
        title = self.titleF.render("Breakout", False, red)
        canvas.blit(title, (screenWidth / 2 - title.get_rect().width / 2, 25))
        # Shows the play button
        play = self.font.render("Play", False, green)
        canvas.blit(play, (self.play.x, self.play.y))

    # Shows the controls menu
    def Controls(self):
        # Shows the title
        title = self.titleF.render("Controller select", False, blue)
        canvas.blit(title, (screenWidth / 2 - title.get_rect().width / 2, 25))
        # Shows the mouse button
        mouse = self.font.render("Mouse", False, green)
        canvas.blit(mouse, (self.mouse.x, self.mouse.y))
        # Shows the keyboard button
        keyboard = self.font.render("KeyBoard", False, green)
        canvas.blit(keyboard, (self.keyboard.x, self.keyboard.y))

    # Shows the win menu
    def Win(self):
        # Shows the title
        title = self.titleF.render("You Win!", False, green)
        canvas.blit(title, (screenWidth / 2 - title.get_rect().width / 2, 25))
        # Shows the continue button
        keepPlaying = self.font.render("Continue", False, blue)
        canvas.blit(keepPlaying, (self.keepPlaying.x, self.keepPlaying.y))
        # Shows the back to menu button
        toMenu = self.font.render("Back to menu", False, blue)
        canvas.blit(toMenu, (self.toMenu.x, self.toMenu.y))


# Initializes the bricks, the paddle, the ball, and the menus
bricks = Bricks()
bricks.createBricks()
paddle = Paddle()
ball = Ball(paddle.x + (paddle.width // 2), paddle.y - paddle.height)
menu = Menus()

# Sets the font and the font size
font = pygame.font.Font("ErbosDraco1StOpenNbpRegular-l5wX.ttf", 30)

# Creates the window and sets a display name.
canvas = pygame.display.set_mode((screenWidth, screenHeigh))
pygame.display.set_caption("Creative Task 2")

# Sets the running state to be true
run = True
# While run is true or the main game loop
while run:
    # Sets the background colour to be black
    canvas.fill((35, 37, 39))
    # print(pygame.mouse.get_pos())
    # Checks if you are in the main menu
    if mainMenu:
        menu.Main()
    if controlSelect:
        menu.Controls()
    # Checks if you are playing
    if playing:
        # Shows the bricks
        bricks.showBricks()
        # Shows the paddle
        paddle.show()
        # shows the ball
        ball.show()
        # Shows the score
        label = font.render(str(score), False, (255, 255, 255))
        canvas.blit(label, (12, screenHeigh - 42))
        # Allows the ball to move and gets the gameOver variable from ball.move
        gameOver = ball.move()
        # Checks if you are using the mouse
        if useMouse:
            # Allows the paddle to be moved by your mouse
            paddle.mouseMove()
        # If you aren't using your mouse
        else:
            # Allows the paddle to be moved by your keyboard
            paddle.keyboardmove()

    # Checks if you won
    if gameOver == 1:
        # Ends the game
        playing = False
        # Open the win menu
        menu.Win()
    # Checks if you lost
    if gameOver == -1:
        # Ends the game
        playing = False
    # Gets the mouse position
    pos = pygame.mouse.get_pos()
    # For each event in pygame
    for e in pygame.event.get():
        # Checks if the event is a quit
        if e.type == pygame.QUIT:
            # Stops the game loop
            run = False
        # Checks if you click your mouse
        if e.type == pygame.MOUSEBUTTONDOWN:
            # Checks if you click the play button and you are in the main menu
            if menu.play.collidepoint(pos) and mainMenu:
                # Sets that you are in the control select menu
                controlSelect = True
                # Sets that you are not in the main menu
                mainMenu = False

            # Checks if you click the mouse button and you are in the controller select menu
            if menu.mouse.collidepoint(pos) and controlSelect:
                # Takes you out of the controller select menu
                controlSelect = False
                # Takes you in to the game
                playing = True
                # Sets that you are using mouse controls
                useMouse = True
            # Checks if you click the keyboard button and you are in the controller select menu
            if menu.keyboard.collidepoint(pos) and controlSelect:
                # Takes you out of the controller select menu
                controlSelect = False
                # Takes you in to the game
                playing = True
                # Sets that you are not using mouse controls
                useMouse = False
            # Checks if you click Continue or Reset
            if menu.keepPlaying.collidepoint(pos):
                # Checks if you won
                if gameOver == 1:
                    # Moves the ball the its starting position
                    ball.rect.x = ball.x
                    ball.rect.y = ball.y
                    # Starts playing the game
                    playing = True
                    # Sets game to not be over
                    gameOver = 0
                    ball.gameOver = 0
                    # Deletes old bricks
                    bricks.bricks.clear()
                    # Creates new bricks
                    bricks.createBricks()
            # Checks if you click back to menu and if gameOver is not 1
            if menu.toMenu.collidepoint(pos) and gameOver != 0:
                # Moves the ball the its starting position
                ball.rect.x = ball.x
                ball.rect.y = ball.y
                # Bring you back to the menu
                mainMenu = True
                # Sets game to not be over
                gameOver = 0
                ball.gameOver = 0
                # Resets the score
                score = 0
                # Deletes old bricks
                bricks.bricks.clear()
                # Creates new bricks
                bricks.createBricks()

    # Updates the canvas
    pygame.display.update()

    # Limits the frames per second to 60
    pygame.time.Clock().tick(60)

# Exits the game
pygame.QUIT
# End of program.
