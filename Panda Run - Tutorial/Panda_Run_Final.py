"""
    Game Name : Panda Run - Tutorial
    Game Maker : Jung Hae Jin
    Created Date : 2019.7.9
    Description : Run and run. Don't bump into the obstacle.
"""
import sys
from random import randint
import pygame
from pygame.locals import QUIT, KEYDOWN, KEYUP, \
    K_LEFT, K_RIGHT
import math

# Window Size(fixed number)
Window_Xsize = 1024
Window_Ysize = 768
degree40_to_radian = math.radians(40)

# Initial Setting of pygame windows
pygame.init()
Window_Surface = pygame.display.set_mode((Window_Xsize, Window_Ysize))
pygame.display.set_caption("Panda Run - Tutorial")
Game_Image_GameIcon = pygame.image.load("Panda_Run_IconImage.png")
pygame.display.set_icon(Game_Image_GameIcon)
FPS_Clock = pygame.time.Clock()

def main():
    """
        Main Routine
    """
    # 1. set variable
    
    # 1-1. Game User's Status
    Game_Player_Status_GameOver = False
    Game_Player_Status_PassObs = 0
    Game_Player_Score = 0
    Game_Player_Speed = 5
    Game_Player_XPos = 0
    # 1-2. Game Obstacle's Status
    Game_Obstacle_Status = []
    
    # 2. setting
    
    # 2-1. Game Image Setting
    Game_Image_Player_Stand = pygame.image.load("stand.png")
    Game_Image_Player_Move1 = pygame.image.load("move_1.png")
    Game_Image_Player_Move2 = pygame.image.load("move_2.png")
    Game_Image_Obstacle = pygame.image.load("obstacle.png")
    Game_Image_BG = pygame.image.load("background.png")
    # 2-2. Game System Setting
    Game_Sys_KeyInput_Frame = 0
    Game_Sys_keyInput_Count = 2
    Game_Sys_Move_Frame = 0
    Game_Sys_Move_Count = 5
    Game_Sys_Move_Mode = False
    # 2-3. Game Font Setting
    Game_Font_ScoreFont = pygame.font.SysFont(None, 54)
    Game_Font_SystemFont = pygame.font.SysFont(None, 72)
    # 2-4. Game Message Setting
    Game_Msg_GameOver = Game_Font_SystemFont.render("GAME OVER!!",\
                                        True, (0, 255, 225))
    Game_Msg_rect = Game_Msg_GameOver.get_rect()
    Game_Msg_rect.center = (Window_Xsize // 2, Window_Ysize // 2)

    # 2-5. Game Obstacle Setting
    obs_count = 0
    for obs_count in range(1, 17):
        Game_Obstacle_Status.append({"randpos" : [randint(-1, 1)],
                                     "count" : [obs_count*100],
                                     "pos" : [0, 0, 0]
        })

    # 3. Main Loop
    while True:
        # 3-1. Key Input Event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not Game_Player_Status_GameOver:
                    if event.key == K_LEFT:
                        if not Game_Player_XPos == -270:
                            if Game_Sys_KeyInput_Frame % Game_Sys_keyInput_Count == 0:
                                Game_Player_XPos -= 270
                                Game_Sys_KeyInput_Frame = 0
                            Game_Sys_KeyInput_Frame += 1
                    elif event.key == K_RIGHT:
                        if not Game_Player_XPos == 270:
                            if Game_Sys_KeyInput_Frame % Game_Sys_keyInput_Count == 0:
                                Game_Player_XPos += 270
                                Game_Sys_KeyInput_Frame = 0
                            Game_Sys_KeyInput_Frame += 1
            elif event.type == KEYUP:
                if not Game_Player_Status_GameOver:
                    Game_Sys_KeyInput_Frame = 0

        # 3-2. Game Playing
        if not Game_Player_Status_GameOver:
            Game_Player_Score = 10 * Game_Player_Status_PassObs
            Game_Sys_Move_Frame += 1
            if Game_Player_Status_PassObs > 0 and\
            Game_Player_Status_PassObs % 5 == 0:
                Game_Player_Speed += 0.01

            for Obstacle in Game_Obstacle_Status:
                if Obstacle["count"][0] < 1600:
                    if Game_Player_Status_PassObs // 5 > 4:
                        Obstacle["count"][0] += 5
                    else:
                        Obstacle["count"][0] += 1 + Game_Player_Status_PassObs // 5
                else:
                    if Obstacle["pos"][2] < Window_Ysize // 2:
                        if Obstacle["randpos"][0] == -1:
                            Obstacle["pos"][0] = -5 - Obstacle["pos"][2] *\
                            math.tan(degree40_to_radian)
                        elif Obstacle["randpos"][0] == 0:
                            Obstacle["pos"][0] = -5 - Obstacle["pos"][2] *\
                            math.tan(degree40_to_radian)
                            Obstacle["pos"][1] = 5 + Obstacle["pos"][2] *\
                            math.tan(degree40_to_radian)
                        elif Obstacle["randpos"][0] == 1:
                            Obstacle["pos"][1] = 5 + Obstacle["pos"][2] *\
                            math.tan(degree40_to_radian)
                        Obstacle["pos"][2] += Game_Player_Speed
                        if (abs(Obstacle["pos"][0] - Game_Player_XPos) < 64 or\
                            abs(Obstacle["pos"][1] - Game_Player_XPos) < 64) and\
                            Obstacle["pos"][2] > Window_Ysize // 2 - 55 and\
                            Obstacle["pos"][2] < Window_Ysize // 2 - 40:
                                Game_Player_Status_GameOver = True
                    else:
                        before_obs1st = Obstacle["randpos"][0]
                        while True:
                            Obstacle["randpos"][0] = randint(-1, 1)
                            rand_num = Obstacle["randpos"][0]
                            if rand_num != before_obs1st and\
                            abs(rand_num - before_obs1st) <= 1:
                                break
                        Obstacle["pos"][0] = 0
                        Obstacle["pos"][1] = 0
                        Obstacle["pos"][2] = 0
                        Game_Player_Status_PassObs += 1
                        Obstacle["count"][0] = 0

        # 4. Window UI Setting
        Window_Surface.fill((255, 255, 255))

        Window_Surface.blit(Game_Image_BG, (0, 0))
        
        for Obstacle in Game_Obstacle_Status:
            if Obstacle["count"][0] >= 1600:
                obs1_xpos = Obstacle["pos"][0]
                obs2_xpos = Obstacle["pos"][1]
                obs_ypos = Obstacle["pos"][2]
                size = 0.2 + 2.8 * obs_ypos / (Window_Ysize // 2)
                Obs1_size_up = pygame.transform.rotozoom(Game_Image_Obstacle,
                                                         0, size)
                Obs2_size_up = pygame.transform.rotozoom(Game_Image_Obstacle,
                                                         0, size)
                Window_Surface.blit(Obs1_size_up,
                             (Window_Xsize // 2 - size*32 + obs1_xpos,
                              Window_Ysize // 3 + obs_ypos * size / 3 + 20))
                Window_Surface.blit(Obs2_size_up,
                             (Window_Xsize // 2 - size*32 + obs2_xpos,
                              Window_Ysize // 3 + obs_ypos * size / 3 + 20))

        if Game_Player_Status_GameOver:
            Window_Surface.blit(Game_Image_Player_Stand,
                         (Window_Xsize // 2 - 48 + Game_Player_XPos,
                          Window_Ysize - (96 + 50)))
            Window_Surface.blit(Game_Msg_GameOver, Game_Msg_rect)
            pygame.mixer.music.stop()
        else:
            if Game_Sys_Move_Mode == False:
                Window_Surface.blit(Game_Image_Player_Move1,
                             (Window_Xsize // 2 - 48 + Game_Player_XPos,
                             Window_Ysize - (96 + 50)))
                if Game_Sys_Move_Frame % Game_Sys_Move_Count == 0:
                    Game_Sys_Move_Mode = True
                    Game_Sys_Move_Frame = 0
            elif Game_Sys_Move_Mode == True:
                Window_Surface.blit(Game_Image_Player_Move2,
                                    (Window_Xsize // 2 - 48 + Game_Player_XPos,
                                    Window_Ysize - (96 + 50)))
                if Game_Sys_Move_Frame % Game_Sys_Move_Count == 0:
                    Game_Sys_Move_Mode = False
                    Game_Sys_Move_Frame = 0

        score_str = "Score : " + str(Game_Player_Score).zfill(6)
        score_image = Game_Font_ScoreFont.render(score_str, True, (0, 0, 0))
        Window_Surface.blit(score_image, (700, 30))

        pygame.display.update()
        FPS_Clock.tick(20)

if __name__ == '__main__':
    main()
