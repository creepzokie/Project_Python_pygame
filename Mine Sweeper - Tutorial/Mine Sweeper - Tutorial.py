"""
    Game Name : Mine Sweeper
    Game Maker : Jung Hae Jin
    Created Date : 2019.6.5
    Description : Find all Mine.
"""

# import part
import sys
from math import floor
from random import randint
import pygame
from pygame.locals import QUIT, MOUSEBUTTONDOWN

# Game Field Size
Game_Field_Width = 20
Game_Field_Height = 15

# Game Field Setting
Game_Field_Block_Size = 30
Game_Field_Block_Mines_Num = 50
Game_Field_Block_Status_Empty = 0
Game_Field_Block_Status_Mine = 1
Game_Field_Block_Status_Opened = 2
Game_Field_Flag_posList = []

# Game Player Status Setting
Game_Player_Status_OpenBlockCount = 0
Game_Player_Status_BlockCheckList = [[0 for _ in range(Game_Field_Width)]
                                     for _ in range(Game_Field_Height)]

# Game Window Icon
Game_Image_GameIcon = pygame.image.load("Mine_Sweeper_Icon_BigSize.png")

# Window Size(fixed Number)
Window_xsize = Game_Field_Block_Size * Game_Field_Width
Window_ysize = Game_Field_Block_Size * Game_Field_Height

# Initial Setting of pygame windows
pygame.init()
Window_Surface = pygame.display.set_mode([Window_xsize, Window_ysize])
pygame.display.set_caption("Mine Sweeper - Tutorial")
pygame.display.set_icon(Game_Image_GameIcon)
FPS_Clock = pygame.time.Clock()

"""
    Functions definition
    which are used in game
"""

""" Return the number of bombs in around blocks """
def Num_Mines(field, x_position, y_position):
    Mines_Count = 0
    for Yoffset in range(-1, 2):        # -1, 0, 1
        for Xoffset in range(-1, 2):    # -1, 0, 1
            Xposition = x_position + Xoffset
            Yposition = y_position + Yoffset
            # Don't count position out of range
            if 0 <= Xposition < Game_Field_Width and \
                0 <= Yposition < Game_Field_Height and \
                field[Yposition][Xposition] == Game_Field_Block_Status_Mine:
                Mines_Count += 1
    return Mines_Count

""" Open the Block """
def Open_Block(field, x_position, y_position):
    global Game_Player_Status_OpenBlockCount    # To save the num of opened block
    # if block is checked, get out of the function
    if Game_Player_Status_BlockCheckList[y_position][x_position]:
        return
    # Change stauts into 'checked'
    Game_Player_Status_BlockCheckList[y_position][x_position] = True
    
    for Yoffset in range(-1, 2):        # -1, 0, 1
        for Xoffset in range(-1, 2):    # -1, 0, 1
            Xposition = x_position + Xoffset
            Yposition = y_position + Yoffset
            # Don't count position out of range
            if 0 <= Xposition < Game_Field_Width and \
                0 <= Yposition < Game_Field_Height and \
                field[Yposition][Xposition] == Game_Field_Block_Status_Empty:
                # change the status of block
                field[Yposition][Xposition] = Game_Field_Block_Status_Opened
                # count the num of opened block
                Game_Player_Status_OpenBlockCount += 1
                # check Bomb
                Count = Num_Mines(field, Xposition, Yposition)
                # if not have bomb and not clicked block, then execute func again
                if Count == 0 and \
                    not (Xposition == x_position and Yposition == y_position):
                    Open_Block(field, Xposition, Yposition)

"""
    Main Routine
"""
def main():
    # Font setting
    smallfont = pygame.font.SysFont("Berlin Sans FB Demi", 24, True)
    largefont = pygame.font.SysFont(None, 72, True)
    # Game message setting
    Game_Msg_Clear = largefont.render("CLEAR!", True, (0, 255, 0))
    Game_Msg_ClearRect = Game_Msg_Clear.get_rect()
    Game_Msg_ClearRect.center = (Window_xsize // 2, Window_ysize // 2)
    Game_Msg_GameOver = largefont.render("Game OVER!", True, (255, 0, 0))
    Game_Msg_GameOverRect = Game_Msg_GameOver.get_rect()
    Game_Msg_GameOverRect.center = (Window_xsize // 2, Window_ysize // 2)
    # Game image setting
    Game_Image_Mine = pygame.image.load("Mine.png")
    Game_Image_MineBang = pygame.image.load("Mine_Bang.png")
    Game_Image_MineFlag = pygame.image.load("Dot_Flag.png")
    # Game player status setting
    Game_Player_Status_SetFlag = [[0 for _ in range(Game_Field_Width)]
                                  for _ in range(Game_Field_Height)]
    Game_Player_Status_GameClear = False
    Game_Player_Status_GameOver = False
    # Block field setting
    field = [[Game_Field_Block_Status_Empty for Xposition in range(Game_Field_Width)]
              for Yposition in range(Game_Field_Height)]
    
    # Set Bomb
    Set_Mine_count = 0
    while Set_Mine_count < Game_Field_Block_Mines_Num:
        Xposition = randint(0, Game_Field_Width - 1)
        Yposition = randint(0, Game_Field_Height - 1)
        if field[Yposition][Xposition] == Game_Field_Block_Status_Empty:
            field[Yposition][Xposition] = Game_Field_Block_Status_Mine
            Set_Mine_count += 1
    # Main loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            # open block
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and \
            not Game_Player_Status_GameOver:
                Xposition = floor(event.pos[0] / Game_Field_Block_Size)
                Yposition = floor(event.pos[1] / Game_Field_Block_Size)
                # game over option
                if field[Yposition][Xposition] == Game_Field_Block_Status_Mine:
                    Game_Player_Status_GameOver = True
                # block open option
                else:
                    Open_Block(field, Xposition, Yposition)
            # flag set option
            if event.type == MOUSEBUTTONDOWN and event.button == 3 and \
            not Game_Player_Status_GameOver:
                Flag_Xpos = floor(event.pos[0] / Game_Field_Block_Size)
                Flag_Ypos = floor(event.pos[1] / Game_Field_Block_Size)
                if not field[Flag_Ypos][Flag_Xpos] == Game_Field_Block_Status_Opened:
                    # set flag
                    if Game_Player_Status_SetFlag[Flag_Ypos][Flag_Xpos] == 0:
                        Game_Player_Status_SetFlag[Flag_Ypos][Flag_Xpos] = 1
                        Game_Field_Flag_posList.append((Flag_Xpos *
                                                        Game_Field_Block_Size,
                                                        Flag_Ypos *
                                                        Game_Field_Block_Size))
                    # get rid of flag
                    elif Game_Player_Status_SetFlag[Flag_Ypos][Flag_Xpos] == 1:
                        Game_Player_Status_SetFlag[Flag_Ypos][Flag_Xpos] = 0
                        Game_Field_Flag_posList.remove((Flag_Xpos *
                                                        Game_Field_Block_Size,
                                                        Flag_Ypos *
                                                        Game_Field_Block_Size))
                
        # Window Setting
        Window_Surface.fill((0, 0, 0))
        for Yposition in range(Game_Field_Height):
            for Xposition in range(Game_Field_Width):
                Game_Field_Blocks = field[Yposition][Xposition]
                Game_Field_BlockRect = (Xposition * Game_Field_Block_Size,
                                        Yposition * Game_Field_Block_Size,
                                        Game_Field_Block_Size,
                                        Game_Field_Block_Size)
                # not opened block setting
                if Game_Field_Blocks == Game_Field_Block_Status_Empty or \
                Game_Field_Blocks == Game_Field_Block_Status_Mine:
                    pygame.draw.rect(Window_Surface, (192, 192, 192),
                                     Game_Field_BlockRect)
                    # draw bomb bang image
                    if Game_Player_Status_GameOver == True and \
                    Game_Field_Blocks == Game_Field_Block_Status_Mine:
                        Window_Surface.blit(Game_Image_MineBang,
                                            (Xposition * Game_Field_Block_Size,
                                             Yposition * Game_Field_Block_Size))
                # bomb's num image setting
                elif Game_Field_Blocks == Game_Field_Block_Status_Opened:
                    Mine_Count = Num_Mines(field, Xposition, Yposition)
                    if Mine_Count > 0:
                        if Mine_Count == 1:
                            Game_Image_MineNum = smallfont.render(
                            "{}".format(Mine_Count), True, (70, 255, 255))
                        elif Mine_Count == 2:
                            Game_Image_MineNum = smallfont.render(
                            "{}".format(Mine_Count), True, (80, 255, 175))
                        elif Mine_Count == 3:
                            Game_Image_MineNum = smallfont.render(
                            "{}".format(Mine_Count), True, (255, 255, 0))
                        elif Mine_Count == 4:
                            Game_Image_MineNum = smallfont.render(
                            "{}".format(Mine_Count), True, (255, 128, 128))
                        else:
                            Game_Image_MineNum = smallfont.render(
                            "{}".format(Mine_Count), True, (255, 50, 255))
                        Window_Surface.blit(Game_Image_MineNum,
                                            (Xposition * Game_Field_Block_Size + 10,
                                            Yposition * Game_Field_Block_Size))
        # Set Flag
        for Flag_pos in Game_Field_Flag_posList:
            Flag_pos_toList = list(Flag_pos)
            Flag_Xpos = Flag_pos_toList[0] // Game_Field_Block_Size
            Flag_Ypos = Flag_pos_toList[1] // Game_Field_Block_Size
            if not (field[Flag_Ypos][Flag_Xpos] == Game_Field_Block_Status_Opened):
                if not Game_Player_Status_GameClear:
                    if not Game_Player_Status_GameOver:
                        Window_Surface.blit(Game_Image_MineFlag, Flag_pos)
                else:
                    Window_Surface.blit(Game_Image_Mine, Flag_pos)
        
        # Set Vertical and Horizontal lines
        for Vertical_line_count in range(0, Window_xsize, Game_Field_Block_Size):
            pygame.draw.line(Window_Surface, (100, 100, 100),
                             (Vertical_line_count, 0),
                             (Vertical_line_count, Window_ysize))
        for Horizontal_line_count in range(0, Window_ysize, Game_Field_Block_Size):
            pygame.draw.line(Window_Surface, (100, 100, 100),
                             (0, Horizontal_line_count),
                             (Window_xsize, Horizontal_line_count))
        
        # Set Game Clear and Over
        if Game_Player_Status_OpenBlockCount == Game_Field_Width *\
        Game_Field_Height - Game_Field_Block_Mines_Num:
            Game_Player_Status_GameClear = True
            Window_Surface.blit(Game_Msg_Clear, Game_Msg_ClearRect.topleft)
        elif Game_Player_Status_GameOver == True:
            Window_Surface.blit(Game_Msg_GameOver, Game_Msg_GameOverRect.topleft)
        
        pygame.display.update()
        FPS_Clock.tick(15)

if __name__ == "__main__":
    main()