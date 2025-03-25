import pygame
import numpy as np

# Pygame 초기화
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Polynomial Interpolation Visualization")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (180, 180, 180)
GREEN = (0, 255, 0)

# 점 리스트 (C0, C1, C2)
control_pts = [(200, 400), (400, 200), (600, 400)]  # 기본적으로 세 점이 존재
clock = pygame.time.Clock()
screen.fill(WHITE)

def linear_interpolation(p1, p2, t):
    """두 점을 선형 보간하여 중간 점 계산"""
    return (1 - t) * np.array(p1) + t * np.array(p2)

def quadratic_interpolation(p0, p1, p2, t):
    """2차 보간식 적용"""
    q01 = linear_interpolation(p0, p1, t)
    q11 = linear_interpolation(p1, p2, t)
    return linear_interpolation(q01, q11, t)

def draw_interpolation():
    """보간 과정 및 곡선을 그림"""
    screen.fill(WHITE)

    # 기본 제어점 그리기
    font = pygame.font.Font(None, 30)
    for i, pt in enumerate(control_pts):
        pygame.draw.circle(screen, BLUE, pt, 5)
        screen.blit(font.render(f"C{i}", True, BLACK), (pt[0] + 10, pt[1] - 10))

    # 직선 연결 (C0-C1, C1-C2)
    pygame.draw.line(screen, BLACK, control_pts[0], control_pts[1], 2)
    pygame.draw.line(screen, BLACK, control_pts[1], control_pts[2], 2)

    # 1차 보간 선과 보간 점 그리기
    for t in [0.5, 1.5]:
        q01 = linear_interpolation(control_pts[0], control_pts[1], t / 2)
        q11 = linear_interpolation(control_pts[1], control_pts[2], t / 2)
        pygame.draw.circle(screen, RED, q01.astype(int), 5)
        pygame.draw.circle(screen, RED, q11.astype(int), 5)
        pygame.draw.line(screen, BLACK, q01, q11, 1)

    # 2차 보간 곡선 그리기
    curve_pts = [quadratic_interpolation(control_pts[0], control_pts[1], control_pts[2], t) for t in np.linspace(0, 1, 100)]
    for i in range(len(curve_pts) - 1):
        pygame.draw.line(screen, GREEN, curve_pts[i], curve_pts[i+1], 2)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    draw_interpolation()
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
