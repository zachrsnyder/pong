import pygame
import random
from operator import add, mul
from math import sqrt, sin, cos

class Circle:
    def __init__(self, radius, center, direction, velocity, color):
        self.radius = radius
        self.center = center
        self.direction = direction
        self.velocity = velocity
        self.color = color

    def getRadius(self):
        return self.radius
    def getCenter(self):
        return self.center
    def getDirection(self):
        return self.direction
    def getVelocity(self):
        return self.velocity
    def getFrameChange(self):
        return list(map(lambda x: x * self.getVelocity(), self.direction))
    def getColor(self):
        return self.color
    
    def changeRadius(self, radius):
        self.radius = radius
    def changeCenter(self, center):
        self.center = center
    def changeDirection(self, direction):
        self.direction = direction
    def changeVelocity(self, velocity):
        self.velocity = velocity
    def changeColor(self, color):
        self.color = color
    

SCREEN_HEIGHT, SCREEN_WIDTH = 600, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 15, 70
WIN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
WIN_BACKGROUND = pygame.Rect(0,0,SCREEN_WIDTH,SCREEN_HEIGHT)
pygame.display.set_caption("Pong")
pygame.font.init()
FONT = pygame.font.Font(None, 36)
VELOCITY = 6
FPS = 60
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (255, 165, 0)
BLUE = (0,0,255)
BALL_RADIUS = 10
BLUE_LOSE = pygame.USEREVENT + 1
ORANGE_LOSE = pygame.USEREVENT + 2
PI = 3.14


def decideBall():
    if random.randint(0,99) % 2:
        return [-1,0]
    else:
        return [1,0]

def leftMovement(keys_pressed, player1):
    if keys_pressed[pygame.K_w] and player1.top > 0:
        player1.top -= VELOCITY
    if keys_pressed[pygame.K_s] and player1.top + PLAYER_HEIGHT < SCREEN_HEIGHT:
        player1.top += VELOCITY 

def rightMovement(keys_pressed, player2):
    if keys_pressed[pygame.K_UP] and player2.top > 0:
        player2.top -= VELOCITY
    if keys_pressed[pygame.K_DOWN] and player2.top + PLAYER_HEIGHT < SCREEN_HEIGHT:
        player2.top += VELOCITY

def clamp(n, min, max): 
    if n < min: 
        return min
    elif n > max: 
        return max
    else: 
        return n 
    
def displayWinner(text, color):
    surface = FONT.render(text, True, color)
    text_box = surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    #WIN.fill((0,0,0))
    WIN.blit(surface, text_box)
    pygame.display.flip()

    pygame.time.delay(2000)

    
def checkTermination(ball):
    ball_center = ball.getCenter()
    if ball_center[0] - BALL_RADIUS <= 0:
        displayWinner("Blue Wins!", BLUE)
        pygame.event.post(pygame.event.Event(ORANGE_LOSE))
        return True
    elif ball_center[0] + BALL_RADIUS >= SCREEN_WIDTH:
        displayWinner("Orange Wins!", ORANGE)
        pygame.event.post(pygame.event.Event(BLUE_LOSE))
        return True
    
    return False




def ballMovement(player1, player2, ball):
    if checkTermination(ball):
        return Circle(BALL_RADIUS, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], decideBall(), VELOCITY, WHITE)
    next_frame = list(map(add, ball.getCenter(), ball.getFrameChange()))
    direction = ball.getDirection()
    center = ball.getCenter()
    radius = ball.getRadius()
    velocity = ball.getVelocity()


    if next_frame[1] < radius:
        t = abs((radius - center[1]) / direction[1])
        center = list(map(add, list(map(lambda x: x * t, direction)), center))
        remainder = velocity - t
        direction = list(map(mul, [1, -1], direction))
        center = list(map(add, list(map(lambda x: x * remainder, direction)), center))
        return Circle(radius, center, direction, velocity, ball.getColor())


    if next_frame[1] > SCREEN_HEIGHT - radius:
        t = abs((SCREEN_HEIGHT - radius - center[1]) / direction[1])
        center = list(map(add, list(map(lambda x: x * t, direction)), center))
        remainder = velocity - t
        direction = list(map(mul, [1, -1], direction))
        center = list(map(add, list(map(lambda x: x * remainder, direction)), center))
        return Circle(radius, center, direction, velocity, ball.getColor())
    

    if next_frame[0] < SCREEN_WIDTH * .15:
           
        N_x = next_frame[0] - clamp(next_frame[0], player1.left, player1.left + PLAYER_WIDTH)
        N_y = next_frame[1] - clamp(next_frame[1], player1.top, player1.top + PLAYER_HEIGHT)
        N_mag = sqrt((N_x ** 2) + (N_y ** 2))
        direction = ball.getDirection()
        center = ball.getCenter()
        if N_mag < BALL_RADIUS and direction[0] < 0:
            print(ball.getVelocity())
            print(N_mag)

            overlap = BALL_RADIUS - N_mag
            if N_mag == 0:
                next_frame = [center[0] + ((-1) * (overlap)), center[1] + ((-1) * (overlap))]
            else:
                next_frame = [center[0] + ((-1) * (N_x / N_mag) * (overlap)), center[1] + ((-1) * (N_y / N_mag) * (overlap))]
            radians = clamp(((PI * (next_frame[1] - player1.top)) / PLAYER_HEIGHT) , PI/4, (3 * PI)/4)
            direction = [sin(radians), (-1) * cos(radians)]
            leftover_velocity = VELOCITY - sqrt((next_frame[0] - center[0]) ** 2 + (next_frame[1] - center[1]) ** 2)
            next_frame = [next_frame[0] + (leftover_velocity * sin(radians)), next_frame[1] + (leftover_velocity * (-1) * cos(radians))]
            return Circle(BALL_RADIUS, next_frame, direction, velocity, ORANGE) 



    elif next_frame[0] > SCREEN_WIDTH * .85:
            
        N_x = next_frame[0] - clamp(next_frame[0], player2.left, player2.left + PLAYER_WIDTH)
        N_y = next_frame[1] - clamp(next_frame[1], player2.top, player2.top + PLAYER_HEIGHT)
        N_mag = sqrt((N_x ** 2) + (N_y ** 2))
        direction = ball.getDirection()
        center = ball.getCenter()

        if N_mag < BALL_RADIUS and direction[0] > 0:            
            overlap = BALL_RADIUS - N_mag
            if N_mag == 0:
                next_frame = [center[0] + ((-1) * (overlap)), center[1] + ((-1) * (overlap))]
            else:
                next_frame = [center[0] + ((-1) * (N_x / N_mag) * (overlap)), center[1] + ((-1) * (N_y / N_mag) * (overlap))]
            radians = clamp(((PI * (next_frame[1] - player2.top)) / PLAYER_HEIGHT) , PI/4, (3 * PI)/4)
            direction = [(-1) * sin(radians), (-1) * cos(radians)]
            leftover_velocity = VELOCITY - sqrt((next_frame[0] - center[0]) ** 2 + (next_frame[1] - center[1]) ** 2)
            next_frame = [next_frame[0] + (leftover_velocity * (-1) * sin(radians)), next_frame[1] + (leftover_velocity * (-1) * cos(radians))]
            return Circle(BALL_RADIUS, next_frame, direction, velocity, BLUE)
        

    ball.changeCenter(next_frame)
    return(ball)
        

    



        

        
        
    
        
         
        
        


def drawWindow(player1, player2, ball, player1_lives, player2_lives):
    pygame.draw.rect(WIN, (0,0,0), WIN_BACKGROUND)
    pygame.draw.rect(WIN, ORANGE, player1)
    pygame.draw.rect(WIN, BLUE, player2)
    pygame.draw.circle(WIN, ball.getColor(), ball.getCenter(), BALL_RADIUS)
    center = list(map(add, ball.getCenter(), list(map(lambda x: x * (ball.getRadius() * 2), ball.getDirection()))))
    pygame.draw.circle(WIN, (255,0,0), center, 2)
    player1_text = "Lives: " + str(player1_lives)
    player2_text = "Lives: " + str(player2_lives)
    player_one_score = FONT.render(player1_text, True, WHITE)
    player_two_score = FONT.render(player2_text, True, WHITE)
    player_one_box = player_one_score.get_rect()
    player_one_box.topleft = (5,5)
    player_two_box = player_two_score.get_rect()
    player_two_box.topleft = (SCREEN_WIDTH - 100, 5)
    WIN.blit(player_one_score, player_one_box)
    WIN.blit(player_two_score, player_two_box)
    pygame.display.flip()


def main():
    run = True
    clock = pygame.time.Clock()
    player1 = pygame.Rect(5, (SCREEN_HEIGHT // 2) - (PLAYER_HEIGHT // 2) ,PLAYER_WIDTH,PLAYER_HEIGHT)
    player2 = pygame.Rect(SCREEN_WIDTH - 5 - PLAYER_WIDTH, (SCREEN_HEIGHT // 2) - (PLAYER_HEIGHT // 2), PLAYER_WIDTH, PLAYER_HEIGHT)
    player1_lives = 5
    player2_lives = 5
    ball_center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]
    direction_vector = decideBall()
    velocity = VELOCITY
    game_ball = Circle(BALL_RADIUS, ball_center, direction_vector, velocity, WHITE)
    while run:
        clock.tick(FPS)
        game_ball.changeVelocity(game_ball.getVelocity() + 0.001)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            
            if event.type == ORANGE_LOSE:
                player1_lives -= 1
                if player1_lives == 0:
                    run = False
                
            
            if event.type == BLUE_LOSE:
                player2_lives -= 1
                if player2_lives == 0:
                    run = False



        keys_pressed = pygame.key.get_pressed()
        leftMovement(keys_pressed, player1)
        rightMovement(keys_pressed, player2)
        game_ball = ballMovement(player1, player2, game_ball)
        drawWindow(player1, player2, game_ball, player1_lives, player2_lives)

    pygame.quit()

main()




