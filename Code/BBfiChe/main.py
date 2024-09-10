import engine
import engine_main
import engine_audio
import engine_resources
from engine_resources import FontResource
import engine_nodes
import engine_io
import engine_draw
from engine_nodes import CameraNode,Sprite2DNode, Text2DNode
import engine_resources
from engine_math import Vector2, Vector3
from engine_io import rumble
import time
import framebuf

camera = CameraNode(Vector3(64,64,0))
engine.fps_limit(60)



fb = engine_draw.front_fb()
splash_image = engine_resources.TextureResource('/Games/TinyFlight/assets/splash_screen.bmp')



# yellow = (255, 236, 0)
green = (0, 255, 0)

# Game loop
running = True
alpha = 0  # Initial alpha value for the second image
fade_in = False  # Flag to control fading in


font = FontResource(r'/system/assets/outrunner_outline.bmp')


# Arr loc
#arrowx = 23
#arrowy = 23

# rec loc

single_loc = ((128 // 2) + 10) #74
multi_loc = ((128 // 2) + 25)
Setting_loc = ((128 // 2) + 40)

page = 0

# Add a 3-second delay before starting the fade-in process
time.sleep(3)
fade_in = True

# Initial rectangle position
rect_y = single_loc

def page_0():
    single_text = Text2DNode(Vector2(64,64),font,'SINGLEPLAYER', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
    multi_text = Text2DNode(Vector2(64,80),font,'MULTIPLAYER', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
    help_text = Text2DNode(Vector2(64,96),font,'HELP', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
    quit_text = Text2DNode(Vector2(64,112),font,'QUIT', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)

def page_1():
    single_text = Text2DNode(Vector2(64,64),font,'Stonks', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
    multi_text = Text2DNode(Vector2(64,80),font,'Test', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
    help_text = Text2DNode(Vector2(64,96),font,'HELP', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
    quit_text = Text2DNode(Vector2(64,112),font,'QUIT', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)

def page_2():
    pass

def page_3():
    pass

def page_4():
    pass

def page_5():
    pass

arrow_x = 1
arrow_y = 76

intensity = 15

thing = 0

picsel = 0
fps = 240
framecounter = 0

rumbleFrames = 0
def rumble(frames, intensity):
    global rumbleFrames
    engine_io.rumble(intensity)
    rumbleFrames = frames

def color(r,g,b):
    rgb565 = ((r & 0xF8) << 8) | ((g & 0xFC) << 3) | (b >> 3)
    return rgb565

# makeing a frame buffer every frame works but its a bit slower
def makeFrameBuf(imagePath):
    image = engine_resources.TextureResource(imagePath)
    return framebuf.FrameBuffer(image.data, image.width, image.height, framebuf.RGB565)

arrow = makeFrameBuf('/Games/TinyFlight/assets/arrow.bmp')

# draw the splash_image as a background save like 8 fps
engine_draw.set_background(splash_image)

# make nodes once it was very slow cause you were making new nodes every frame
single_text = Text2DNode(Vector2(64,64),font,'SINGLEPLAYER', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
multi_text = Text2DNode(Vector2(64,80),font,'MULTIPLAYER', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
help_text = Text2DNode(Vector2(64,96),font,'HELP', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)
quit_text = Text2DNode(Vector2(64,112),font,'QUIT', 0, Vector2(1.0, 1.0), 1.0, 1, 1, color(0,255,0), 127)

def kill_all_nodes():
    global single_text, multi_text, help_text, quit_test
    single_text.mark_destroy_all()
    multi_text.mark_destroy_all()
    help_text.mark_destroy_all()
    quit_text.mark_destroy_all()

def button_press_check(mode):
    # page defs
    # NOTE: ALL MENUS WILL HAVE A BACK OPTION.
    # 0 - Main Menu: SinglePlayer, Multiplayer, Help, Quit
    # 1 - Single Player Screen options: Free Flight, Target Practice, Missions, Back
    # 2 - Free flight start screen
    # 3 - Target Practice screen options: Weapons selection screen, Do targets shoot Back? Y/N
    # 4 - Missions screen options: Missions/achivements and their progress
    # 5 - Multiplayer Screen: PVP Missions, COOP Missions, Waiting for connection then when connection is established show a play button.
    # 6 - PVP missions screen: Shows all Missions/Achivements and their progress.
    # 7 - COOP Missions screen: Shows all Missions/Achivements and their progress.
    # 8 - Start Multiplayer after valid connection: Connecting and starting in [countdown timer of 10 sec]
    # 9 - Help Screen: Credits button, Description of the game, how to use controls, ect.
    # 10 - Credits Screen: Credits to UnRedKnown for Physics/research mechanics, TheBoredKid For taking every drop out of his life to make a 3D engine, and BBfiChe for making the Main Menu.
    
    global page
    print("Button A/B Has been Pressed!!!!")
    kill_all_nodes()
    if mode == True:
        if page == 0:
            if arrow_y == 58:
                page = 1
                
                page_1()
            if arrow_y == 74:
                page = 5
            if arrow_y == 90:
                page = 9

    if mode == False:
        if page == 0:
            pass
    
    
        


while running:
    
    if engine.tick():
        print(engine.get_running_fps())
        
        if engine_io.UP.is_just_pressed and arrow_y != 60:
            arrow_y -= 16 
            rumble(12, 0.3)
            print("Rectangle moved Up")
        if engine_io.DOWN.is_just_pressed and  arrow_y != 108:
            arrow_y += 16  
            rumble(12, 0.3)
            print("rectangle moved Down")

        if rumbleFrames > 0:
            rumbleFrames -= 1
        if rumbleFrames == 0:
            engine_io.rumble(0)
        
        if engine_io.A.is_just_pressed:
            button_press_check(True)
            
        if engine_io.B.is_just_pressed:
            button_press_check(False)
                
        # the color that is set here is the colorkey change it if the background changes
        fb.blit(arrow,arrow_x , arrow_y, color(255,255,255))
