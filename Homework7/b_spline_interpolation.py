import pygame
import numpy as np

# 화면 설정
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cubic B-spline Curve")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

pts = []
screen.fill(WHITE)
clock = pygame.time.Clock()

def cubic_b_spline(t, p0, p1, p2, p3):
    """4개 점으로 이루어진 Cubic B-spline 곡선 점 계산"""
    t2 = t * t
    t3 = t2 * t
    b0 = (-t3 + 3*t2 - 3*t + 1) / 6.0
    b1 = (3*t3 - 6*t2 + 4) / 6.0
    b2 = (-3*t3 + 3*t2 + 3*t + 1) / 6.0
    b3 = t3 / 6.0
    return b0 * p0 + b1 * p1 + b2 * p2 + b3 * p3

def draw_b_spline(pts, color=GREEN, thick=2):
    if len(pts) < 4:
        return
    
    for i in range(len(pts) - 3):
        p0 = np.array(pts[i], dtype=float)
        p1 = np.array(pts[i+1], dtype=float)
        p2 = np.array(pts[i+2], dtype=float)
        p3 = np.array(pts[i+3], dtype=float)

        curve = [cubic_b_spline(t, p0, p1, p2, p3) for t in np.linspace(0, 1, 30)]
        
        for j in range(len(curve) - 1):
            pygame.draw.line(screen, color, curve[j], curve[j + 1], thick)

# 메인 루프
done = False
while not done:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            pts.append((x, y))

    screen.fill(WHITE)

    # 제어점 그리기
    for pt in pts:
        pygame.draw.circle(screen, BLUE, pt, 5)

    # 제어선
    if len(pts) >= 2:
        pygame.draw.lines(screen, RED, False, pts, 1)

    # 곡선 그리기
    draw_b_spline(pts, GREEN, 2)

    pygame.display.update()

pygame.quit()
