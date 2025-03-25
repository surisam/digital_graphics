import pygame
import numpy as np

width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height), 0, 32)
pygame.display.set_caption("Lagrange Curve")

WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pts = []
count = 0
screen.fill(WHITE)
clock = pygame.time.Clock()

def lagrange_interpolation(x, px, py):
    """라그랑주 다항식 보간법을 사용하여 y 값을 계산"""
    n = len(px)
    y = 0
    for i in range(n):
        term = py[i]
        for j in range(n):
            if i != j:
                term *= (x - px[j]) / (px[i] - px[j])
        y += term
    return y

def draw_curve(color=GREEN, thick=2):
    """라그랑주 보간법을 이용한 곡선 그리기"""
    if len(pts) < 2:
        return
    
    px = np.array([p[0] for p in pts])
    py = np.array([p[1] for p in pts])
    
    x_vals = np.linspace(min(px), max(px), 100)  # 100개의 x값 생성
    y_vals = [lagrange_interpolation(x, px, py) for x in x_vals]  # y값 계산

    for i in range(len(x_vals) - 1):
        pygame.draw.line(screen, color, (x_vals[i], y_vals[i]), (x_vals[i+1], y_vals[i+1]), thick)

done = False
while not done:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            pts.append((x, y))
            count += 1
            pygame.draw.circle(screen, BLUE, (x, y), 5)  # 점 찍기

    screen.fill(WHITE)  # 화면 초기화
    for pt in pts:
        pygame.draw.circle(screen, BLUE, pt, 5)  # 점 유지

    if len(pts) > 1:
        draw_curve(GREEN, 2)  # 곡선 그리기

    pygame.display.update()

pygame.quit()
