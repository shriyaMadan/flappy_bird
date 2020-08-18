import pygame, random, sys

pygame.mixer.pre_init(frequency=44100, size=16, channels=1, buffer=512)
pygame.init()

#setting display window
display_width = 576
display_height = 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('flappy bird')
game_font = pygame.font.Font('04B_19.ttf', 40)
clock = pygame.time.Clock()
crashed = False


def bgSetting():
    bgImg = pygame.image.load('assets/background-day.png').convert()
    im_width, im_height = bgImg.get_size()
    bgImg = pygame.transform.scale(bgImg, (display_width, display_height))
    gameDisplay.blit(bgImg, (0, 0))

def floorSetting():
    floorImg = pygame.image.load('assets/base.png').convert()
    floorImg = pygame.transform.scale2x(floorImg)
    gameDisplay.blit(floorImg, (floor_x_pos, 500))
    gameDisplay.blit(floorImg, (floor_x_pos + display_width, 500))
floor_x_pos = 0

#bird_surface = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
#bird_surface = pygame.transform.scale2x(bird_surface)
#bird_rect = bird_surface.get_rect(center=(100, 300))

#pipe
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE,1200)
pipe_height = [400, 300, 200]

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (600,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (600,random_pipe_pos-200))
    return top_pipe, bottom_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if(pipe.bottom>=600):
            gameDisplay.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            gameDisplay.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            return False
    if bird_rect.top<=-100 or bird_rect.bottom>= 500:
            return False
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement*3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))
    return new_bird, new_bird_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface= game_font.render(str(int(score)),True, (255,255,255))
        score_rect = score_surface.get_rect(center=(288 ,100))
        gameDisplay.blit(score_surface, score_rect)
    if game_state=='game_over':
        score_surface = game_font.render(
            f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        gameDisplay.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}',True,(255,255,255))
        high_score_rect = high_score_surface.get_rect(center=(288, 450))
        gameDisplay.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if(score>high_score):
        high_score = score
    return high_score

#game variables
gravity = 0.25
bird_movement = 0
game_active = True
score=0
high_score = 0

#bird
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
bird_frames = [bird_downflap,bird_midflap,bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (100, 300))

BIRDFLAP = pygame.USEREVENT+1
pygame.time.set_timer(BIRDFLAP,200)

game_over_surface = pygame.image.load('assets/message.png').convert_alpha()
game_over_rect = game_over_surface.get_rect(center=(288,300))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 100

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (100, 300)
                bird_movement=0
                score = 0
        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
        if event.type == BIRDFLAP:
            if(bird_index<2):
                bird_index +=1
            else:
                bird_index=0
            bird_surface, bird_rect = bird_animation()
           

    bgSetting()

    if game_active:
        #bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += int(bird_movement)

        gameDisplay.blit(rotated_bird, bird_rect)
        game_active = check_collision(pipe_list)    

        #pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)
        
        score+= 0.01
        score_sound_countdown -= 1
        if score_sound_countdown<=0:
            score_sound.play()
            score_sound_countdown = 100
        score_display('main_game')
    else:
        gameDisplay.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')



    #floor
    floor_x_pos -= 1
    floorSetting()
    if floor_x_pos <= -576:
	    floor_x_pos = 0
        
    pygame.display.update()
    clock.tick(60)

pygame.quit()
quit()
