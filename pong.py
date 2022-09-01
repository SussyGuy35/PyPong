import pygame, sys, random,os
try:
    import pyi_splash
    pyi_splash.update_text('UI Loaded ...')
    pyi_splash.close()
except:
    print("Not using pyinstaller splash screen")
#Tạo hàm
def ball_movement():
    global ball_hsp, ball_vsp, player_score, opponent_score, score_time, player_spd, player2_spd,opponent_spd, scr_height
    
    ball.centerx += ball_hsp
    ball.centery += ball_vsp

    if ball.top <= 0 and ball_vsp<=0:
        ball_vsp *= -1
        pygame.mixer.Sound.play(pong_sfx)
    elif ball.bottom>=scr_height and ball_vsp >= 0:
        ball_vsp *= -1
        pygame.mixer.Sound.play(pong_sfx)

    if ball.left+ball_hsp <= 0:
        player_score+=1
        pygame.mixer.Sound.play(score_sfx)
        score_time  = pygame.time.get_ticks()
    if ball.right+ball_hsp>=scr_width:
        opponent_score+=1
        pygame.mixer.Sound.play(score_sfx)
        score_time  = pygame.time.get_ticks()

    if ball.colliderect(player) and ball_hsp >0:
        pygame.mixer.Sound.play(pong_sfx)
        if abs(ball.right - player.left)<10:
            ball_hsp=(ball_hsp*-1)+0.25
            ball_vsp += player_spd*0.5
        elif abs(ball.bottom - player.top)<10 and ball_vsp >0:
            ball_vsp *=-1    
        elif abs(ball.top - player.bottom)<10 and ball_vsp <0:
            ball_vsp *=-1       
    if ball.colliderect(opponent) and ball_hsp<0:
        pygame.mixer.Sound.play(pong_sfx)
        if abs(ball.left - opponent.right)<10:
            ball_hsp=(ball_hsp*-1)+0.25
            if not two_player:
                if opponent.top > 0 and opponent.bottom < scr_height:
                    ball_vsp += ((ball.centery - opponent.centery)*opponent_spd)*0.5
            elif two_player:
                ball_vsp += player2_spd*0.5    
        elif abs(ball.bottom - opponent.top)<10 and ball_vsp >0:
            ball_vsp *=-1    
        elif abs(ball.top - opponent.bottom)<10 and ball_vsp <0:
            ball_vsp *=-1    
def player_movement():
    global player_spd
    player_spd = (keys[pygame.K_DOWN]-keys[pygame.K_UP])*7
    player.y+= player_spd
    if player.top <= 0:
        player.top = 0
        player_spd = 0
    if player.bottom >= scr_height:
        player.bottom = scr_height
        player_spd = 0
def player2_movement():
    global player2_spd
    player2_spd = (keys[pygame.K_s]-keys[pygame.K_w])*7
    opponent.y+= player2_spd
    if opponent.top <= 0:
        opponent.top = 0
        player2_spd = 0
    if opponent.bottom >= scr_height:
        opponent.bottom = scr_height
        player2_spd = 0
def opponent_ai():
    global opponent_spd
    opponent.centery += (ball.centery - opponent.centery)*opponent_spd
    if opponent.top <= 0:
        opponent.top = 0
    if opponent.bottom >= scr_height:
        opponent.bottom = scr_height 
def ball_start():
    global ball_hsp, ball_vsp, opponent_spd, score_time, white, scr_width, scr_height

    current_time = pygame.time.get_ticks()
    ball.center = (scr_width/2,scr_height/2)
    
    if current_time - score_time < 700:
        number_three = game_font.render("3",True,white)
        screen.blit(number_three, (scr_width/2 - 6, scr_height/2+35))
    if 700<current_time - score_time < 1400:
        number_two = game_font.render("2",True,white)
        screen.blit(number_two, (scr_width/2 - 6, scr_height/2+35))    
    if 1400<current_time - score_time < 2100:
        number_one = game_font.render("1",True,white)
        screen.blit(number_one, (scr_width/2 - 6, scr_height/2+35))

    if current_time - score_time < 2100:
        ball_hsp, ball_vsp = 0, 0
    else:
        ball_hsp = random.choice((4,-4,5,-5,6,-6))
        ball_vsp = random.choice((4,-4,5,-5))
        opponent_spd = random.choice((0.15,0.2))
        score_time = None
def check_game_restart():
    global player_score, opponent_score, score_time, scr_height
    if player_score == 10 or opponent_score == 10:
        ball_start()
        player_score = 0
        opponent_score = 0 
        player.centery = scr_height/2   
        opponent.centery = scr_height/2 
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
        output_path = os.path.join(base_path, relative_path)
    except Exception:
        output_path = relative_path

    return output_path
# chuẩn bị
pygame.mixer.pre_init(44100,-16,2,512)
pygame.init()
scr_width = 1000
scr_height = 600
screen = pygame.display.set_mode((scr_width,scr_height))
pygame.display.set_caption('Pong')

icon = pygame.image.load(resource_path('data/icon.ico'))

pygame.display.set_icon(icon)
clock = pygame.time.Clock()
# tạo biến
    #Framerate
gamespeed = 60
    # Tạo hitbox lmao
ball = pygame.Rect(scr_width/2-10, scr_height/2-10,20,20)
player = pygame.Rect(scr_width-15, scr_height/2-60,10,120)
opponent = pygame.Rect(5, scr_height/2-60,10,120)
    #Tạo màu
bg_color = pygame.Color('grey12')
white = (255,255,255)
line_col = (105,105,105)
    #bruh
ball_hsp = random.choice((-4,-5,-6))
ball_vsp = random.choice((4,-4))   
player_spd = 0
player2_spd = 0
opponent_spd = random.choice((0.15,0.2))
two_player = False

    # Chữ lmao
player_score = 0
opponent_score = 0    

game_font = pygame.font.Font(resource_path("data/font.ttf"),20) 
       
    #Timer
score_time = True   
    # Sfx

pong_sfx = pygame.mixer.Sound(resource_path("data/pong.ogg"))
score_sfx = pygame.mixer.Sound(resource_path("data/score.ogg"))

# vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                if two_player == True:
                    two_player = False
                elif two_player == False:
                    two_player = True                                                   
    # Lấy input
    keys = pygame.key.get_pressed()
    #game logic
    ball_movement()
    player_movement()
    if not two_player:
        opponent_ai()
    else :
        player2_movement()    
    check_game_restart()

    #Đồ họa
    screen.fill(bg_color)
    pygame.draw.aaline(screen,line_col,(scr_width/2,0),(scr_width/2,scr_height))
    pygame.draw.rect(screen,white,player)
    pygame.draw.rect(screen,white,opponent)
    pygame.draw.ellipse(screen,white,ball)
    
    if score_time:
        ball_start()


    player_text = game_font.render(f"{player_score}",True,white)
    screen.blit(player_text,(525,300))
    opponent_text = game_font.render(f"{opponent_score}",True,white)
    screen.blit(opponent_text,(465,300))

    pygame.display.flip()
    clock.tick(gamespeed)