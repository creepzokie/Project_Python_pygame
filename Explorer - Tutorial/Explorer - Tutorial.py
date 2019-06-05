"""
    Game Name : Explorer - Tutorial
    Game Maker : Jung Hae Jin
    Created Date : 2019.5.28
    Description : Explore it. Don't bump into the wall.
"""

# import part
import sys
from random import randint
import pygame
from pygame.locals import QUIT, Rect, KEYDOWN, K_SPACE, K_r, K_s
import time

# Window Size(fixed number)
Window_Size_x = 1024
Window_Size_y = 768

# Initial Setting of pygame windows
pygame.init()
pygame.key.set_repeat(1, 10) # (delay = 1ms, interval = 10ms)
Window_Surface = pygame.display.set_mode((Window_Size_x, Window_Size_y))
pygame.display.set_caption("Explorer - Tutorial")
FPS_Clock = pygame.time.Clock()

def main():
    """
    Main Routine
    """
    # 1. set variable
    
    # 1-1. Game User's Status
    Game_User_Status_Round = 1
    Game_Round_Font = pygame.font.SysFont("Arial Black", 20)
    Game_User_Status_GameStart = False
    Game_Image_GameStart = pygame.image.load("Dot_GameStart.png")
    Game_User_Status_KeyInput_S = False
    Game_User_Status_GameOver = False
    Game_Image_GameOver = pygame.image.load("Dot_GameOver.png")
    Game_User_Status_KeyInput_R = False
    
    # 1-2. Game BackGrounds Setting
    Game_BG_Walls_Width = 8     # Wall's Width
    # Wall's RGB
    Game_BG_Walls_R = 0
    Game_BG_Walls_G = 0
    Game_BG_Walls_B = 0
    Game_BG_Holes_Height = 400  # Hole's Height
    # Hole's RGB
    Game_BG_Holes_R = 254
    Game_BG_Holes_G = 254
    Game_BG_Holes_B = 254
    RGB_Count = 0               # Hole's White and Black Change Count
    # The Number of Walls
    Game_BG_Walls_Num = Window_Size_x // Game_BG_Walls_Width
    # The slope of Walls will increase when the game round be increased
    Game_BG_Walls_slope = 1
    Game_BG_Walls_TurnCount = 0     # The number of Turning points
    # The Generation of initial holes
    Game_BG_Holes = []
    for x_position in range(Game_BG_Walls_Num):
        Game_BG_Holes.append(Rect(x_position * Game_BG_Walls_Width,
                                  (Window_Size_y - Game_BG_Holes_Height) // 2,
                                  Game_BG_Walls_Width, Game_BG_Holes_Height))
    
    # 1-3. Game User's Plane Setting
    Game_Plane_position_x = 24
    Game_Plane_position_y = Window_Size_y / 2
    Game_Plane_velocity_y = 0
    
    # 1-4. Game Score UI Setting
    Game_Score_number = 0
    Game_Score_font = pygame.font.SysFont("Arial Black", 20)
    
    # 1-5. Game Plane UI Setting
    Game_Image_Plane = pygame.image.load("Dot_Plane2.png")
    Game_Image_PlaneFly = pygame.image.load("Dot_Plane2_Fly.png")
    Game_Image_PlaneBang = pygame.image.load("Dot_Effect_Bang1.png")
    
    # 2. Main Loop
    while True:
        Game_User_Status_Keydown_Spacebar = False   # Initialize key input data
        # 2-1. Key Input Event
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    Game_User_Status_Keydown_Spacebar = True
                if event.key == K_s and Game_User_Status_GameStart == False:
                    Game_User_Status_KeyInput_S = True
                if event.key == K_r and \
                Game_User_Status_GameStart == True and \
                Game_User_Status_GameOver == True:
                    Game_User_Status_KeyInput_R = True
        
        # 2-2. Game Playing
        if Game_User_Status_GameStart == False and \
        Game_User_Status_KeyInput_S == True:
            Game_User_Status_GameStart = True
            Game_User_Status_KeyInput_S = False
            time.sleep(3)
            continue
        elif Game_User_Status_GameStart == True and \
        Game_User_Status_GameOver == False:
            Game_Score_number += 1  # Increase Score by FPS
            # User's Plane Control
            if Game_User_Status_Keydown_Spacebar == True:
                Game_Plane_velocity_y -= 1                  # Go Up
            else:
                Game_Plane_velocity_y += 1                  # Go Down
            Game_Plane_position_y += Game_Plane_velocity_y
            
            # Generaion of Holes
            Game_BG_HoleEdge = Game_BG_Holes[-1].copy()     # The last hole
            # Turning the hole by slope which is given
            # Wall's Slope must be plus at start
            Game_BG_HoleTurn = Game_BG_HoleEdge.move(0, Game_BG_Walls_slope)
            
            # Turning the hole's shape
            if Game_BG_Walls_TurnCount == 0:
                TurnPoint = 0     # Initial Turning Point
            # Holes must not be out of window
            if Game_BG_HoleTurn.top <= 0 + TurnPoint or \
            Game_BG_HoleTurn.bottom >= Window_Size_y - TurnPoint:
                # When the Slope is plus value
                if Game_BG_Walls_slope > 0:
                    # Turn the Slope into minus random value
                    Game_BG_Walls_slope = -randint(0 + Game_User_Status_Round,
                                                   3 + Game_User_Status_Round)
                # When the Slope is minus value
                else:
                    # Turn the Slope into plus random value
                    Game_BG_Walls_slope = randint(0 + Game_User_Status_Round,
                                                  3 + Game_User_Status_Round)
                # Hole is getting smaller over time
                if Game_BG_Walls_TurnCount < Game_BG_Holes_Height - 300:
                    Game_BG_HoleEdge.inflate_ip(0, -1)
                elif Game_BG_Walls_TurnCount < Game_BG_Holes_Height - 250:
                    Game_BG_HoleEdge.inflate_ip(0, -2)
                # Count the turning points
                Game_BG_Walls_TurnCount += 1
                if Game_BG_Walls_TurnCount >= Game_BG_Holes_Height - 250:
                    Game_User_Status_Round = 6
                elif Game_BG_Walls_TurnCount >= Game_BG_Holes_Height - 300:
                    Game_User_Status_Round = 5
                elif Game_BG_Walls_TurnCount >= Game_BG_Holes_Height - 340:
                    Game_User_Status_Round = 4
                elif Game_BG_Walls_TurnCount >= Game_BG_Holes_Height - 370:
                    Game_User_Status_Round = 3
                elif Game_BG_Walls_TurnCount >= Game_BG_Holes_Height - 390:
                    Game_User_Status_Round = 2
                # Set the turning points change by game round
                TurnPoint = Game_User_Status_Round * 5
            
            # Generate new holes at the end of Holes List
            Game_BG_HoleEdge.move_ip(8, Game_BG_Walls_slope)
            Game_BG_Holes.append(Game_BG_HoleEdge)
            # Delete the hole at the start of Holes List
            del Game_BG_Holes[0]
            # Move all holes to the left
            Game_BG_Holes = [x.move(-8, 0) for x in Game_BG_Holes]

            # The condition of game over
            if Game_BG_Holes[4].top > Game_Plane_position_y + 4 or \
            Game_BG_Holes[4].bottom < Game_Plane_position_y + 28:
                Game_User_Status_GameOver = True
        
        elif Game_User_Status_GameOver == True and \
        Game_User_Status_KeyInput_R == True:
            Game_User_Status_Round = 1
            Game_User_Status_GameStart = True
            Game_User_Status_GameOver = False
            Game_User_Status_KeyInput_R = False
            Game_BG_Walls_R = 255
            Game_BG_Walls_G = 255
            Game_BG_Walls_B = 255
            Game_BG_Holes_R = 254
            Game_BG_Holes_G = 254
            Game_BG_Holes_B = 254
            RGB_Count = 0
            Game_Plane_position_y = Window_Size_y / 2
            Game_Plane_velocity_y = 0
            Game_Score_number = 0
            for x_position in range(Game_BG_Walls_Num):
                Game_BG_Holes.append(Rect(x_position * Game_BG_Walls_Width,
                                          (Window_Size_y - Game_BG_Holes_Height)
                                          // 2, Game_BG_Walls_Width,
                                          Game_BG_Holes_Height))
                del Game_BG_Holes[0]
            Game_BG_Walls_slope = 1
            Game_BG_Walls_TurnCount = 0
            time.sleep(3)
            continue

        # 3. Window UI Setting
        # Walls' Color will change by Game Round
        if Game_User_Status_Round == 1:
            Game_BG_Walls_R = 136
            Game_BG_Walls_G = 159
            Game_BG_Walls_B = 249
        elif Game_User_Status_Round == 2:
            Game_BG_Walls_R = 175
            Game_BG_Walls_G = 253
            Game_BG_Walls_B = 232
        elif Game_User_Status_Round == 3:
            Game_BG_Walls_R = 229
            Game_BG_Walls_G = 236
            Game_BG_Walls_B = 120
        elif Game_User_Status_Round == 4:
            Game_BG_Walls_R = 255
            Game_BG_Walls_G = 195
            Game_BG_Walls_B = 51
        elif Game_User_Status_Round == 5:
            Game_BG_Walls_R = 150
            Game_BG_Walls_G = 0
            Game_BG_Walls_B = 0
        elif Game_User_Status_Round == 6:
            Game_BG_Walls_R = 0
            Game_BG_Walls_G = 0
            Game_BG_Walls_B = 0
        Window_Surface.fill((Game_BG_Walls_R,
                             Game_BG_Walls_G,
                             Game_BG_Walls_B))
        
        if Game_User_Status_GameStart == True:
            if Game_BG_Holes_R >= 0 and Game_BG_Holes_R < 255 and \
            RGB_Count == 0:
                Game_BG_Holes_R += 1
                Game_BG_Holes_G += 1
                Game_BG_Holes_B += 1
                if Game_BG_Holes_R == 255:
                    RGB_Count = 1
            elif Game_BG_Holes_R <= 255 and Game_BG_Holes_R > 0 and \
            RGB_Count == 1:
                Game_BG_Holes_R -= 1
                Game_BG_Holes_G -= 1
                Game_BG_Holes_B -= 1
                if Game_BG_Holes_R == 0:
                    RGB_Count = 0
        for hole in Game_BG_Holes:
            pygame.draw.rect(Window_Surface,
                             (Game_BG_Holes_R,
                              Game_BG_Holes_G,
                              Game_BG_Holes_B),
                             hole)       # Hole's Color will change cyclically

        # Player's Plane UI Setting
        if Game_User_Status_Keydown_Spacebar == True:
            Window_Surface.blit(Game_Image_PlaneFly,
                                (Game_Plane_position_x, Game_Plane_position_y))
        else:
            Window_Surface.blit(Game_Image_Plane,
                                (Game_Plane_position_x, Game_Plane_position_y))
        # Player's Score UI Setting
        Game_Iamge_Score = Game_Score_font.render("Your Score : {}"
                                                  .format(Game_Score_number),
                                                  True,
                                                  (255 - Game_BG_Walls_R,
                                                   255 - Game_BG_Walls_G,
                                                   255 - Game_BG_Walls_B))
        Window_Surface.blit(Game_Iamge_Score, (Window_Size_x / 2 - 100, 20))
        # Player's Round UI Setting
        if Game_User_Status_Round <= 5:
            Game_Iamge_Round = Game_Round_Font.render("Stage : {}"
                                                      .format(Game_User_Status_Round),
                                                      True,
                                                      (255 - Game_BG_Walls_R,
                                                       255 - Game_BG_Walls_G,
                                                       255 - Game_BG_Walls_B))
        else:
            Game_Iamge_Round = Game_Round_Font.render("Stage : Ultimate",
                                                      True,
                                                      (255 - Game_BG_Walls_R,
                                                       255 - Game_BG_Walls_G,
                                                       255 - Game_BG_Walls_B))
        Window_Surface.blit(Game_Iamge_Round, (Window_Size_x / 2 - 43, 50))
        if Game_User_Status_GameStart == False:
            Window_Surface.blit(Game_Image_GameStart,
                                (Window_Size_x // 2 - 300,
                                 Window_Size_y // 2 - 150))
        # Player's GameOver UI Setting
        if Game_User_Status_GameOver == True:
            Window_Surface.blit(Game_Image_PlaneBang,
                                (Game_Plane_position_x - 9,
                                 Game_Plane_position_y - 9))
            Window_Surface.blit(Game_Image_GameOver,
                                (Window_Size_x // 2 - 200,
                                 Window_Size_y // 2 - 100))
        
        pygame.display.update()
        FPS_Clock.tick(30)
        
if __name__ == "__main__":
    main()
                    
    