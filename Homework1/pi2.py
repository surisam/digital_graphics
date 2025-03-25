import pygame
import numpy as np

# Pygame 초기화
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Polynomial Interpolation - Click to Add Points")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 클릭한 점 리스트
clicked_pts = []

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

    font = pygame.font.Font(None, 30)

    # 클릭된 점이 3개 미만이면 점만 그림
    for pt in clicked_pts:
        pygame.draw.circle(screen, BLUE, pt, 5)

    if len(clicked_pts) == 3:
        p0, p1, p2 = clicked_pts

        # 기본 점 라벨 추가
        for i, pt in enumerate(clicked_pts):
            screen.blit(font.render(f"C{i}", True, BLACK), (pt[0] + 10, pt[1] - 10))

        # 1차 보간 선과 중간 점 그리기
        for t in [0.5, 1.5]:
            q01 = linear_interpolation(p0, p1, t / 2)
            q11 = linear_interpolation(p1, p2, t / 2)
            pygame.draw.circle(screen, RED, q01.astype(int), 5)
            pygame.draw.circle(screen, RED, q11.astype(int), 5)
            pygame.draw.line(screen, BLACK, q01, q11, 1)

        # 최종 2차 보간 곡선 그리기
        curve_pts = [quadratic_interpolation(p0, p1, p2, t) for t in np.linspace(0, 1, 100)]
        for i in range(len(curve_pts) - 1):
            pygame.draw.line(screen, GREEN, curve_pts[i], curve_pts[i+1], 2)

done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(clicked_pts) < 3:
                clicked_pts.append(pygame.mouse.get_pos())

            # 점이 3개가 되면 자동으로 다시 그림
            if len(clicked_pts) == 3:
                draw_interpolation()

    pygame.display.update()
    clock.tick(30)

pygame.quit()
