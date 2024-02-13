import pygame
from pygame.locals import *
import random
import time

pygame.init()
(W,H) = (1200,800)
screen = pygame.display.set_mode((W,H),FULLSCREEN)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
DARK_BLUE = (24,27,56)
PASTEL_PURPLE = (234,214,255)
PASTEL_ORANGE = (255,255,204)
PASTEL_CYAN = (163,255,255)
PASTEL_BLUE = (158,158,255)
RAINBOW = [(255,127,127),(255,127,191),(255,127,255),(191,127,255),(127,127,255),(127,191,255),(127,255,255),(127,255,191),(127,255,127),(191,255,127),(255,255,127),(255,191,127)]
FONT = 'data/fonts/Arial'
TITLE = '凸包を構築するソフト'
pygame.display.set_caption('凸包')

initial = True
build = False

BACKGROUND = DARK_BLUE
BUTTON_COLOR1 = PASTEL_CYAN
BUTTON_COLOR2 = PASTEL_BLUE

point_num = 1000
point_radius = 5
edge_color = YELLOW

EPS = 1e-9

def Std():
    screen.fill(BACKGROUND)
    pygame.time.wait(0)

def Quit():
    pygame.quit()

def QuitStd():
    for event in pygame.event.get(): 
        if event.type == QUIT:
            Quit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                Quit()
            if event.key == K_q:
                Quit()

# 参考 : https://github.com/bioerrorlog/CellForRest_Pygame

#ここから
def Text(text,font,size,color,center_x,center_y):
    Font = pygame.font.Font(font, size)
    Surf = Font.render(text, True, color)
    Rect = Surf.get_rect()
    Rect.center = (center_x,center_y)
    screen.blit(Surf,Rect)

def DrawButton(msg,size,color,x,y,w,h,action = None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen,BUTTON_COLOR2,Rect(x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen,BUTTON_COLOR1,Rect(x,y,w,h))

    Text(msg,FONT,size,color,(x+(w/2)),(y+(h/2)))
#ここまで

def Toggle():
    global initial
    global build
    initial ^= 1
    build ^= 1

def Initial():
    while initial:
        Std()
        Text(TITLE,FONT,100,RAINBOW[-2],W / 2,H / 2)
        DrawButton("Start",20,BLACK,W/4,H/4*3,100,50,Toggle)
        DrawButton("Quit",20,BLACK,W - W/4,H/4*3,100,50,Quit)

        pygame.display.update() 

        QuitStd()

def GeneratePoints():
    history = set()
    ret = []

    x_lower = int(W / 10)
    x_upper = int(W / 10 * 9)
    y_lower = int(H / 10)
    y_upper = int(H / 10 * 9)

    for repeat in range(point_num):
        while True:
            x = random.randint(x_lower,x_upper)
            y = random.randint(y_lower,y_upper)

            if (x,y) in history:
                continue

            history.add((x,y))
            ret.append((x,y))
            break



    return ret

def Vector(lhs,rhs):
    (x1,y1) = lhs
    (x2,y2) = rhs
    return (x2 - x1,y2 - y1)

def Cross(lhs,rhs):
    (x1,y1) = lhs
    (x2,y2) = rhs
    return x1 * y2 - x2 * y1

def Build():
    Points = GeneratePoints()
    assert(len(Points) == point_num)
    Points.sort()

    start_time = time.time()
    first_display_time = 2
    build_start = 3
    assert(first_display_time < build_start)

    building_lower = True
    complete = False
    ConvexHull = []
    current_id = 0
    lower_size = 0

    edges = []
    edge_width = 3
    while True:
        if not build:
            break
        Std()

        current_time = time.time()
        elapsed_time = current_time - start_time

        rate = elapsed_time / first_display_time
        iterate = int(point_num * min(rate,1))

        for i in range(iterate):
            (x,y) = Points[i]
            point_color = RAINBOW[i % len(RAINBOW)]
            pygame.draw.circle(screen,point_color,(x,y),point_radius)

        if elapsed_time >= build_start:
            if not complete:
                if current_id == point_num:
                    building_lower = False
                    lower_size = len(ConvexHull)
                    current_id -= 2

                if building_lower:
                    if len(ConvexHull) >= 2 and Cross(Vector(ConvexHull[-1],ConvexHull[-2]),Vector(Points[current_id],ConvexHull[-1])) < EPS:
                        ConvexHull.pop(-1)
                        edges.pop(-1)
                    else:
                        ConvexHull.append(Points[current_id])
                        if len(ConvexHull) >= 2:
                            edges.append((ConvexHull[-2],ConvexHull[-1]))
                        current_id += 1
                else:
                    if len(ConvexHull) >= lower_size + 1 and Cross(Vector(ConvexHull[-1],ConvexHull[-2]),Vector(Points[current_id],ConvexHull[-1])) < EPS:
                        ConvexHull.pop(-1)
                        edges.pop(-1)
                    else:
                        ConvexHull.append(Points[current_id])
                        if len(ConvexHull) >= 2:
                            edges.append((ConvexHull[-2],ConvexHull[-1]))
                        current_id -= 1
                        if current_id == -1:
                            complete = True

            for (lhs,rhs) in edges:
                pygame.draw.line(screen,edge_color,lhs,rhs,edge_width)

        if complete:
            Text('完成!',FONT,70,YELLOW,W / 2,H / 2)
            DrawButton('タイトルに戻る',30,BLACK,W / 2 - 150,H / 16 * 9,300,80,Toggle)

        pygame.display.update()
        QuitStd()

def main():
    while True:
        Std()

        while initial:
            Initial()

        while build:
            Build()

        pygame.display.update()

        QuitStd()

if __name__ == "__main__":
    main()
