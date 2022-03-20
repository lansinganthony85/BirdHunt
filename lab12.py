import pygame
import random

# Anthony Lansing
# BirdHunt Game
# A DuckHunt like game where random amounts of birds go across the screen
# and you try to shoot as many as you can for points

# initialize global constants
WIDTH, HEIGHT = 960, 610 #the dimensions of the display which is half of the pixel dimensions of the BG
STAGE = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60

#starting positions
STARTX = WIDTH/2
STARTY = HEIGHT/2

#Scaler to keep the images at a relatively decent size compared to the display
SCALER = 6

#Speeds
PLAYER_SPEED = 6
BIRD_SPEED = 4

#COLORS
WHITE = (255, 255, 255)

#IMAGES
BG = pygame.transform.scale(pygame.image.load('prairie_background.png'), (WIDTH,HEIGHT))
BIRD_LEFT = pygame.transform.scale(pygame.image.load("bird_left3.png"), (WIDTH/6, HEIGHT/6))
BIRD_RIGHT = pygame.transform.scale(pygame.image.load("bird_right3.png"), (WIDTH/6, HEIGHT/6))
CROSSHAIRS = pygame.transform.scale(pygame.image.load("crosshairs.png"), (WIDTH/6, HEIGHT/6))
EXPLOSION = pygame.transform.scale(pygame.image.load("explosion.png"), (WIDTH/6, HEIGHT/6))
DOT = pygame.image.load("shoot_dot.png")

#initialize a variable to determine how often birds are created
BIRD_OCCUR = 100

#function that redraws the display each round
def redraw(player, kill_dot, left_birds, right_birds,score, counter):
    STAGE.blit(BG, (0,0))

    for bird in left_birds:
        STAGE.blit(BIRD_LEFT, (bird.x, bird.y))
    for bird in right_birds:
        STAGE.blit(BIRD_RIGHT, (bird.x, bird.y))

    STAGE.blit(CROSSHAIRS, (player.x, player.y))

    #place the DOT image in the center of the crosshairs for drawing to screen
    kill_dot.x, kill_dot.y = (player.x + player.width/2), (player.y + player.height/2)
    STAGE.blit(DOT, (kill_dot.x, kill_dot.y))

    refresh_score(score)
    update_timer(counter)
    pygame.display.update()

#function to create a bird coming from the right of the display
def create_right_birds():
    y_pos = random.randint(0, HEIGHT)
    return BIRD_RIGHT.get_rect(center=(WIDTH, y_pos))

#function to create a bird coming from the left of the display
def create_left_birds():
    y_pos = random.randint(0, HEIGHT)
    return BIRD_LEFT.get_rect(center=(0, y_pos))

#function to draw an explosion at a bird's location when shot
def draw_explosion(bird):
    STAGE.blit(EXPLOSION, (bird.x, bird.y))
    pygame.display.update()

#function to draw the current score to the display
def refresh_score(score):
    my_font = pygame.font.SysFont(("arial", "helvetica"), 32, bold=True)
    score_text = my_font.render(f"SCORE: {score}", True, WHITE)
    STAGE.blit(score_text, (10, 10))

#function to draw the current timer to the display
def update_timer(counter):
    my_font = pygame.font.SysFont(("arial", "helvetica"), 32, bold=True)
    counter_text = my_font.render(f'TIME LEFT: {counter}', True, WHITE)
    STAGE.blit(counter_text, (WIDTH-counter_text.get_width(), 10))

#when the time is up, this function puts game over on the screen with the score
def game_over(score):
    my_font = pygame.font.SysFont(("arial", "helvetica"), 64, bold=True)
    go_text = my_font.render(f"GAME OVER", True, WHITE)
    score_text = my_font.render(f"SCORE: {score}", True, WHITE)
    STAGE.blit(go_text, (WIDTH/2 - go_text.get_width(), HEIGHT/2 - go_text.get_height()))
    STAGE.blit(score_text, (WIDTH/2, HEIGHT/2))
    pygame.display.update()

#the main function
def main():
    pygame.init()
    pygame.display.set_caption('BirdHunt')
    pygame.display.set_icon(pygame.transform.scale(BIRD_RIGHT, (32,30))) #take an image, scale down, and set as icon

    #initialize the mixer for using sounds
    pygame.mixer.init()

    #load the gun shot sound effect
    GUN_SHOT = pygame.mixer.Sound("gun_shot.wav")

    #initialize two lists to hold birds
    left_birds = []
    right_birds = []

    #create player and kill_dot
    #the kill_dot is separate from crosshairs and is the actual device used to shoot birds
    #so more accuracy is required
    player = CROSSHAIRS.get_rect(center=(WIDTH/2, HEIGHT/2))
    kill_dot = DOT.get_rect(center=(WIDTH/2, HEIGHT/2))

    counter = 30 #counter is for 30 seconds
    score = 0 #score initialized to 0

    #create a USEREVENT to keep track when 1000 milliseconds have passed
    pygame.time.set_timer(pygame.USEREVENT, 1000)

    keep_playing = True
    while keep_playing:
        CLOCK.tick(FPS)

        #listen for the closing of the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit() #just quit pygame when 'x' is pressed
            if event.type == pygame.USEREVENT:
                counter -= 1 #timer goes down by 1
                if counter < 0:
                    #when time is up, display the game over text and wait 5 seconds
                    keep_playing = False
                    game_over(score)
                    pygame.time.delay(5000)
        
        # randomly generate birds
        if random.randint(1, BIRD_OCCUR) == BIRD_OCCUR:
            left_birds.append(create_left_birds())
        if random.randint(1, BIRD_OCCUR) == BIRD_OCCUR:
            right_birds.append(create_right_birds())
        
        #get the entire keyboard state as a list
        keys_pressed = pygame.key.get_pressed()

        #play the gun shot sound when SPACE is pressed
        if keys_pressed[pygame.K_SPACE]:
            pygame.mixer.Sound.play(GUN_SHOT)

        #move the birds
        for bird in left_birds:
            if bird.x < WIDTH:
                bird.x += BIRD_SPEED
                #check if bird has been shot and display explosion if yes
                if bird.colliderect(kill_dot) and keys_pressed[pygame.K_SPACE]:
                    draw_explosion(bird)
                    left_birds.remove(bird)
                    score += 1
            else:
                left_birds.remove(bird)
        for bird in right_birds:
            if bird.x > 0:
                bird.x -= BIRD_SPEED
                #check if bird has been shot and display explosion if yes
                if bird.colliderect(kill_dot) and keys_pressed[pygame.K_SPACE]:
                    draw_explosion(bird)
                    right_birds.remove(bird)
                    score += 1
            else:
                right_birds.remove(bird)
        
        #move the crosshairs around
        if keys_pressed[pygame.K_UP]:
            player.y -= PLAYER_SPEED
        if keys_pressed[pygame.K_DOWN]:
            player.y += PLAYER_SPEED
        if keys_pressed[pygame.K_LEFT]:
            player.x -= PLAYER_SPEED
        if keys_pressed[pygame.K_RIGHT]:
            player.x += PLAYER_SPEED
        
        #check for player wall collision
        if player.y < 0:
            player.y = 0
        if player.y > HEIGHT-player.height: #take into account that height of screen is slightly off display
            player.y = (HEIGHT - player.height)
        if player.x < 0:
            player.x = 0
        if player.x > WIDTH-player.width:
            player.x = (WIDTH - player.width)
        
        #redraw the display
        redraw(player, kill_dot, left_birds, right_birds, score, counter)        
        
    pygame.quit()

#run main if not imported as module
if __name__ == '__main__':
    main()