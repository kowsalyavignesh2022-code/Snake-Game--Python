import pygame
import time
import random
import mysql.connector

mydb=mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="gameleaderboard"

)
mycursor=mydb.cursor()

pygame.init()
state="welcome"
state="menu"
width=600
height=400

black=(0,0,0)
white=(255,255,255)

blocksize=30
foodsize=30
snakespeed=4

window=pygame.display.set_mode((width,height))
pygame.display.set_caption('SNAKE GAME')

welcome_image=pygame.image.load("welcome3d.png")
welcomeimage=pygame.transform.scale(welcome_image,(width,height))

home_image=pygame.image.load("home.png")
homeimage=pygame.transform.scale(home_image,(width,height))

name_image=pygame.image.load("namescreen.png")
nameimage=pygame.transform.scale(name_image,(width,height))

back_ground=pygame.image.load("gamescreen1_1.png")
background=pygame.transform.scale(back_ground,(width,height))

head_images={"right":pygame.transform.scale(pygame.image.load("snake_transparent _head_right.png"),
                                            (blocksize,blocksize)),
             "left":pygame.transform.scale(pygame.image.load("snake_transparent_head_left.png"),
                                            (blocksize,blocksize)),
             "up":pygame.transform.scale(pygame.image.load("snake_transparent_head_up.png"),
                                            (blocksize,blocksize)),
             "down":pygame.transform.scale(pygame.image.load("snake_transparent_head_down.png"),
                                            (blocksize,blocksize)),} 
body_images={"right":pygame.transform.scale(pygame.image.load("snake_transparent _body_right.png"),
                                            (blocksize,blocksize)),
             "left":pygame.transform.scale(pygame.image.load("snake_transparent _body_left.png"),
                                            (blocksize,blocksize)),
             "up":pygame.transform.scale(pygame.image.load("snake_transparent _body_up.png"),
                                            (blocksize,blocksize)),
             "down":pygame.transform.scale(pygame.image.load("snake_transparent _body_down.png"),
                                            (blocksize,blocksize)),} 
tail_images={"right":pygame.transform.scale(pygame.image.load("snake_transparent_tail_right.png"),
                                            (blocksize,blocksize)),
             "left":pygame.transform.scale(pygame.image.load("snake_transparent_tail_left.png"),
                                            (blocksize,blocksize)),
             "up":pygame.transform.scale(pygame.image.load("snake_transparent_tail_up.png"),
                                            (blocksize,blocksize)),
             "down":pygame.transform.scale(pygame.image.load("snake_transparent_tail_down.png"),
                                            (blocksize,blocksize)),} 
food_image=pygame.image.load("apple.png")
foodimage=pygame.transform.scale(food_image,(foodsize,foodsize))

speaker_on=pygame.image.load("speaker_on.png")
speaker_on_image=pygame.transform.scale(speaker_on,(50,50))

speaker_off=pygame.image.load("speaker_off.png")
speaker_off_image=pygame.transform.scale(speaker_off,(50,50))
pause_image=pygame.image.load("pauseimage.png")
pauseimage=pygame.transform.scale(pause_image,(width,height))
quit_image=pygame.image.load("quit_screen.png")
quitimage=pygame.transform.scale(quit_image,(width,height))
sure_image=pygame.image.load("sure_image.png")
sureimage=pygame.transform.scale(sure_image,(width,height))
overimage=pygame.image.load("gameover_image.png")
over_image=pygame.transform.scale(overimage,(width,height))

clock=pygame.time.Clock()

font=pygame.font.SysFont(None,35)

def welcome():
    running=True
    while running:

        window.blit(welcomeimage,(0,0))

        start_rect=pygame.Rect(230,300,200,100)
        pygame.display.update()
        
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    running=False

                elif event.type==pygame.KEYDOWN:
                    running=False
def menu():
    running=True
    while running:
        window.blit(homeimage,(0,0))
        
        start_rect=pygame.Rect(210,130,180,60)
        
        exit_rect=pygame.Rect(210,200,180,60)


        pygame.display.update()
        
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                  running=False
                elif exit_rect.collidepoint(event.pos):
                   pygame.quit()
                   quit()
def nameboard():
    font=pygame.font.SysFont(None,30)
    inputbox=pygame.Rect(195,170,10,10)
    text=''
    submit_rect=pygame.Rect(210,240,200,60)

    running=True
    while running:
        window.blit(nameimage,(0,0))
        text_surface=font.render(text,True,white)
        window.blit(text_surface,(inputbox.x,inputbox.y))
        pygame.display.update()
        
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_BACKSPACE:
                    text=text[:-1]
                else:
                    text+=event.unicode

            elif event.type==pygame.MOUSEBUTTONDOWN:
                if submit_rect.collidepoint(event.pos):
                  running=False
    return text
               
            
def savescore(playername,score):
    sql="INSERT INTO leaderboard(playername,score)VALUES(%s,%s)"
    val=(playername,score)
    mycursor.execute(sql,val)
    mydb.commit()
    print("score inserted")


def draw_snake(snakelist,directions):
    for i,segment in enumerate (snakelist):
          x,y=segment
          direction=directions[i]

          if i==len(snakelist)-1:
             window.blit(head_images[direction],(x,y))
          elif i==0:
               window.blit(tail_images[direction],(x,y))
          else:
             
              window.blit(body_images[direction],(x,y))
  
def pausegame():
    paused=True
    while paused:

        resume_rect=pygame.Rect(170,110,270,60)
        replay_rect=pygame.Rect(170,190,270,60)
        exit_rect=pygame.Rect(170,280,270,60)
        for event in pygame.event.get(): 
              
              if event.type==pygame.QUIT:
                pygame.quit()
                quit()
              elif event.type==pygame.MOUSEBUTTONDOWN:
                 if resume_rect.collidepoint(event.pos):
                    paused=False
                 elif replay_rect.collidepoint(event.pos):
                     game_loop()
                 elif exit_rect.collidepoint(event.pos):
                     pygame.quit()
                     quit()
                    
              elif event.type==pygame.KEYDOWN:
                 if event.key==pygame.K_RETURN:
                       paused=False
        window.blit(pauseimage,(0,0))
        pygame.display.update()
def quitgame():
    running=True
    while running:

        quit_rect=pygame.Rect(110,240,170,40)
        resume_rect=pygame.Rect(320,250,170,40)
        for event in pygame.event.get(): 
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    quit()
                elif resume_rect.collidepoint(event.pos):
                    running=False

                
        window.blit(quit_image,(0,0))
        pygame.display.update()
                
    

def game_loop():
    gameover=False
    gameclose=False
    

    x=width/2
    y=height/2

    x_change=0
    y_change=0

    current_direction="right"
    snake_directions=[]

    snakelist=[]
    snake_length=1

    score=0
    score_font=pygame.font.SysFont(None,25)
    score_font_big=pygame.font.SysFont(None,40)


    speaker_rect=pygame.Rect(480,1,50,50)
    music_on=True
    bite_sound=pygame.mixer.Sound("cartoon_gulp.wav")
    
   
    pause_rect=pygame.Rect(530,10,25,25)
    exit_rect=pygame.Rect(570,10,25,25)
    playagain_rect=pygame.Rect(180,320,250,50)
    quit_rect=pygame.Rect(550,10,30,30)
    grid_size=blocksize

    food_x=random.randint(0,(width-grid_size)//grid_size)*grid_size
    food_y=random.randint(0,(height-grid_size)//grid_size)*grid_size

    while not gameover:
             
             for event in pygame.event.get():
                

                if event.type==pygame.QUIT:
                    gameover=True

                elif event.type==pygame.MOUSEBUTTONDOWN:
                 
                 if pause_rect.collidepoint(event.pos):
                   pausegame()
                 elif speaker_rect.collidepoint(event.pos):
                     if music_on:
                         pygame.mixer.music.pause()
                         music_on=False
                     else:
                         pygame.mixer.music.unpause()
                         music_on=True
                     
                 elif exit_rect.collidepoint(event.pos):
                     quitgame()

                if event.type==pygame.KEYDOWN:


                    if event.key==pygame.K_LEFT and x_change==0:
                        x_change=-blocksize
                        y_change=0
                        current_direction="left"

                    elif event.key==pygame.K_RIGHT and x_change==0:
                        x_change=blocksize
                        y_change=0
                        current_direction="right"

                        

                    elif event.key==pygame.K_UP and y_change==0:
                        x_change=0
                        y_change=-blocksize
                        current_direction="up"


                    elif event.key==pygame.K_DOWN and y_change==0:
                        x_change=0
                        y_change=blocksize
                        current_direction="down"

             x+=x_change
             y+=y_change

             if x>=width or x<0 or y>=height or y<0:
                gameclose=True

             window.blit(background,(0,0))
            
                        
             window.blit(foodimage,(food_x,food_y))

             snake_head=[x,y]
             snakelist.append(snake_head)
             snake_directions.append(current_direction)

             if len(snakelist)>snake_length:
                del snakelist[0]
                del snake_directions[0]
            
             for segment in snakelist[:-1]:
                if segment==snake_head:
                    gameclose=True
             
             draw_snake(snakelist,snake_directions)
             if music_on:
                 window.blit(speaker_on,(480,0))
             else:
                 window.blit(speaker_off,(480,0))

             score_surface=score_font.render(str(score),True,(white))
             window.blit(score_surface,(83,8))

             pygame.display.update()

             
             if abs(x-food_x)<foodsize and abs(y-food_y)<foodsize:
                food_x=random.randint(0,(width-grid_size)//grid_size)*grid_size
                food_y=random.randint(0,(height-grid_size)//grid_size)*grid_size
                if music_on:
                    bite_sound.play()
 
                snake_length+=1
                score+=4

             score_saved=False

             while gameclose:
                
                window.blit(over_image,(0,0))
                score_surface=score_font_big.render(str(score),True,(101,67,33))
                window.blit(score_surface,(290,278))
                if not score_saved:
                 savescore(playername,score)
                 score_saved=True

              
                pygame.display.update()

                for event in pygame.event.get():
                   
                    
                   if event.type==pygame.MOUSEBUTTONDOWN:
                 
                     if playagain_rect.collidepoint(event.pos):
                         game_loop()
                     elif quit_rect.collidepoint(event.pos):
                         pygame.quit()
                         quit()


                   elif event.type==pygame.KEYDOWN:

                        if event.key==pygame.K_q:
                            gameover=True
                            gameclose=False

                        elif event.key==pygame.K_c:
                            game_loop()

             clock.tick(snakespeed)
    pygame.quit()
    quit()
welcome()
menu()
playername=nameboard()

game_loop()





            



