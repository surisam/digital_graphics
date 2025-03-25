import pygame
import numpy as np

# Pygame 초기 설정
width, height = 800, 600
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Affine Combination Visualization")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# 점 저장 리스트
pts = []
clock = pygame.time.Clock()
screen.fill(WHITE)

def affine_combination(c0, c1, lamb):
    """Affine Combination 공식을 적용하여 중간 보간점 계산"""
    return (1 - lamb) * np.array(c0) + lamb * np.array(c1)

def draw_affine_combination():
    """Affine Combination을 적용하여 보간점을 표시"""
    if len(pts) < 2:
        return

    c0, c1 = pts[0], pts[1]
    
    # 두 점을 직선으로 연결
    pygame.draw.line(screen, BLACK, c0, c1, 2)

    # 원래 점 표시
    pygame.draw.circle(screen, BLUE, c0, 5)  # C0
    pygame.draw.circle(screen, BLUE, c1, 5)  # C1
    font = pygame.font.Font(None, 30)
    screen.blit(font.render("C0", True, BLACK), (c0[0] - 20, c0[1] - 20))
    screen.blit(font.render("C1", True, BLACK), (c1[0] + 10, c1[1] - 20))

    # 중간 보간점 계산 (λ = 0.5, 1, 1.5)
    for lamb, label in zip([0.5, 1, 1.5], ["0.5", "1", "1.5"]):
        mid_point = affine_combination(c0, c1, lamb)
        mid_point = tuple(map(int, mid_point))  # 정수 좌표 변환
        pygame.draw.circle(screen, RED, mid_point, 5)
        screen.blit(font.render(label, True, BLACK), (mid_point[0] + 5, mid_point[1] - 10))

done = False
while not done:
    screen.fill(WHITE)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if len(pts) < 2:
                pts.append(pygame.mouse.get_pos())

    draw_affine_combination()
    
    pygame.display.update()
    clock.tick(30)

pygame.quit()
