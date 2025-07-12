import sys
import pygame

BG_COLOR = (0, 0, 0)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


def show_start_screen(game):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    title = font.render('Invaders', True, (255, 255, 255))
    instructions = [
        'Setas esquerda e direita para mover',
        'Barra de espaço para atirar',
        'Q para sair do jogo',
        'Pressione ENTER para começar',
    ]
    rendered_instructions = [
        small_font.render(text, True, (200, 200, 200)) for text in instructions
    ]

    while True:
        game.screen.fill(BG_COLOR)
        game.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))

        for i, line in enumerate(rendered_instructions):
            game.screen.blit(
                line, line.get_rect(center=(SCREEN_WIDTH // 2, 250 + i * 40))
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
                elif event.key == pygame.K_q:
                    sys.exit()


def show_game_over_screen(game):
    font = pygame.font.SysFont(None, 48)
    small_font = pygame.font.SysFont(None, 32)

    title = font.render('Game Over', True, (255, 0, 0))
    final_score = small_font.render(
        f'Pontuação Final: {game.score}', True, (255, 255, 255)
    )
    instructions = ['Pressione R para reiniciar', 'Pressione Q para sair']
    rendered_instructions = [
        small_font.render(text, True, (200, 200, 200)) for text in instructions
    ]

    while True:
        game.screen.fill(BG_COLOR)
        game.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 150)))
        game.screen.blit(
            final_score, final_score.get_rect(center=(SCREEN_WIDTH // 2, 220))
        )

        for i, line in enumerate(rendered_instructions):
            game.screen.blit(
                line, line.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 40))
            )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                elif event.key == pygame.K_q:
                    sys.exit()
