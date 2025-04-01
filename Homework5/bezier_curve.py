import pygame
import numpy as np

# 기본 설정
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cubic Bézier Curve")

# 색상 정의
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 점 저장 리스트
pts = []
screen.fill(WHITE)
clock = pygame.time.Clock()

def cubic_bezier(t, P0, P1, P2, P3):
    """3차 베지에 보간 함수"""
    return ((1 - t)**3) * P0 + \
           3 * ((1 - t)**2) * t * P1 + \
           3 * (1 - t) * t**2 * P2 + \
           t**3 * P3

def draw_bezier_curve(color=GREEN, thick=2):
    if len(pts) != 4:
        return
    
    P0, P1, P2, P3 = [np.array(p, dtype=float) for p in pts]
    
    bezier_points = [cubic_bezier(t, P0, P1, P2, P3) for t in np.linspace(0, 1, 100)]

    for i in range(len(bezier_points) - 1):
        start = bezier_points[i]
        end = bezier_points[i + 1]
        pygame.draw.line(screen, color, start, end, thick)

# 메인 루프
done = False
while not done:
    clock.tick(30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(pts) < 4:
                x, y = pygame.mouse.get_pos()
                pts.append((x, y))

    screen.fill(WHITE)

    # 점 그리기
    for pt in pts:
        pygame.draw.circle(screen, BLUE, pt, 5)
    
    # 제어선 그리기
    if len(pts) >= 2:
        pygame.draw.lines(screen, RED, False, pts, 1)
    
    # 곡선 그리기
    if len(pts) == 4:
        draw_bezier_curve(GREEN, 2)

    pygame.display.update()

pygame.quit()
