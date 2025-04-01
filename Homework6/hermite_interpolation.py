import pygame
import numpy as np

# 설정
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Cubic Hermite Interpolation - Multi Points")

# 색상
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

pts = []
screen.fill(WHITE)
clock = pygame.time.Clock()

def hermite(t, P0, P1, m0, m1):
    """Cubic Hermite 보간 함수"""
    h00 = 2 * t**3 - 3 * t**2 + 1
    h10 = t**3 - 2 * t**2 + t
    h01 = -2 * t**3 + 3 * t**2
    h11 = t**3 - t**2
    return h00 * P0 + h10 * m0 + h01 * P1 + h11 * m1

def compute_tangents(pts):
    """중앙차분 방식으로 각 점의 접선 벡터 계산"""
    n = len(pts)
    tangents = []
    for i in range(n):
        if i == 0:
            tangent = np.array(pts[1]) - np.array(pts[0])
        elif i == n - 1:
            tangent = np.array(pts[-1]) - np.array(pts[-2])
        else:
            tangent = (np.array(pts[i + 1]) - np.array(pts[i - 1])) * 0.5
        tangents.append(tangent)
    return tangents

def draw_hermite_spline(pts, color=GREEN, thick=2):
    if len(pts) < 2:
        return

    tangents = compute_tangents(pts)
    
    for i in range(len(pts) - 1):
        P0 = np.array(pts[i], dtype=float)
        P1 = np.array(pts[i + 1], dtype=float)
        m0 = tangents[i]
        m1 = tangents[i + 1]

        curve = [hermite(t, P0, P1, m0, m1) for t in np.linspace(0, 1, 30)]
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

    # 점 그리기
    for pt in pts:
        pygame.draw.circle(screen, BLUE, pt, 5)

    # 보간 곡선 그리기
    if len(pts) >= 2:
        draw_hermite_spline(pts)

    pygame.display.update()

pygame.quit()
