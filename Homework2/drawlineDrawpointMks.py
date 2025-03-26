"""
HW2 - Implement drawLine using drawPoint only
+ 마우스 클릭 또는 키보드(SPACE) 입력으로 점 추가
"""

import pygame
from sys import exit
import numpy as np

# 화면 설정
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)

background_image_filename = 'image/curve_pattern.png'
background = pygame.image.load(background_image_filename).convert()
width, height = background.get_size()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("HW2: drawLine + Mouse/Key input")

# 색상 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 변수 초기화
pts = []
count = 0
screen.fill(WHITE)
clock = pygame.time.Clock()

def drawPoint(pt, color=GREEN, thick=3):
    pygame.draw.circle(screen, color, pt, thick)

def drawLine(pt0, pt1, color=GREEN, thick=3):
    p0 = np.array(pt0)
    p1 = np.array(pt1)
    steps = 100
    for i in range(steps + 1):
        t = i / steps
        p = (1 - t) * p0 + t * p1
        drawPoint(p.astype(int), color, thick)

def drawPolylines(color=GREEN, thick=3):
    if count < 2:
        return
    for i in range(count - 1):
        drawLine(pts[i], pts[i + 1], color, thick)

# 상태 변수
done = False
pressed = 0
margin = 6
old_pressed = 0
old_button1 = 0

while not done:
    time_passed = clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            pressed = -1

        elif event.type == pygame.MOUSEBUTTONUP:
            pressed = 1

        elif event.type == pygame.KEYDOWN:
            # 스페이스바를 누르면 현재 마우스 위치에 점 추가
            if event.key == pygame.K_SPACE:
                x, y = pygame.mouse.get_pos()
                pt = [x, y]
                pts.append(pt)
                count += 1
                pygame.draw.rect(screen, BLUE, (pt[0]-margin, pt[1]-margin, 2*margin, 2*margin), 5)
                print(f"[KEY] len:{len(pts)}  ⌨️ SPACE key pressed — point added at ({x}, {y})")

    # 마우스 상태 읽기
    button1, button2, button3 = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()
    pt = [x, y]
    pygame.draw.circle(screen, RED, pt, 0)

    if old_pressed == -1 and pressed == 1 and old_button1 == 1 and button1 == 0:
        pts.append(pt)
        count += 1
        pygame.draw.rect(screen, BLUE, (pt[0]-margin, pt[1]-margin, 2*margin, 2*margin), 5)
        print(f"[MOUSE] len:{len(pts)}  🖱️ mouse clicked at ({x}, {y})")
    else:
        print(f"len:{len(pts)}  mouse at ({x},{y})")

    if len(pts) > 1:
        drawPolylines(GREEN, 1)

    pygame.display.update()
    old_button1 = button1
    old_pressed = pressed

pygame.quit()
