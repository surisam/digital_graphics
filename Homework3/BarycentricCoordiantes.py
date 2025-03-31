import pygame
import numpy as np

# Pygame 초기화
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Barycentric Coordinates Visualization")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GRAY = (180, 180, 180)

# 점 저장 (삼각형 꼭짓점)
triangle_pts = [(200, 400), (600, 400), (400, 200)]
clicked_pts = []

clock = pygame.time.Clock()
screen.fill(WHITE)

def barycentric_coordinates(p, a, b, c):
    """점 P의 Barycentric 좌표 계산"""
    mat = np.array([
        [a[0], b[0], c[0]],
        [a[1], b[1], c[1]],
        [1, 1, 1]
    ])
    p_vec = np.array([p[0], p[1], 1])
    
    # Cramer's rule을 사용하여 가중치(λ) 계산
    try:
        lambda_vals = np.linalg.solve(mat, p_vec)
        return lambda_vals
    except np.linalg.LinAlgError:
        return None

def draw_barycentric_triangle():
    """삼각형과 내부 보간 점들을 그림"""
    # 삼각형 내부 색칠
    pygame.draw.polygon(screen, GRAY, triangle_pts)

    # 삼각형 외곽선
    pygame.draw.polygon(screen, BLACK, triangle_pts, 2)

    # 삼각형 꼭짓점 표시
    font = pygame.font.Font(None, 30)
    for i, pt in enumerate(triangle_pts):
        pygame.draw.circle(screen, BLUE, pt, 5)
        screen.blit(font.render(f"P{i}", True, BLACK), (pt[0] + 10, pt[1] - 10))

    # 사용자가 찍은 점 그리기
    for pt in clicked_pts:
        pygame.draw.circle(screen, RED, pt, 5)
        lambdas = barycentric_coordinates(pt, *triangle_pts)
        if lambdas is not None:
            lambda_text = f"({lambdas[0]:.2f}, {lambdas[1]:.2f}, {lambdas[2]:.2f})"
            screen.blit(font.render(lambda_text, True, BLACK), (pt[0] + 10, pt[1] - 10))

done = False
while not done:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(clicked_pts) < 5:
                clicked_pts.append(pygame.mouse.get_pos())

    draw_barycentric_triangle()
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
