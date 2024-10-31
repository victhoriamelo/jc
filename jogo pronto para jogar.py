import pygame
import time
import random

from pygame.constants import K_RCTRL

# Inicializando o Pygame
pygame.init()

# Cores
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
ORANGE = pygame.Color(255,140,0)
BLUE = pygame.Color(0, 0, 255)
YELLOW = pygame.Color(255, 255, 0)
PURPLE = pygame.Color(148,0,211)
PINK = pygame.Color(255, 105, 180)
GREEN = pygame.Color(50,205,50)
MAGENTA = pygame.Color(139,0,139)
LILAC = pygame.Color(200, 150, 220)
CYAN = pygame.Color(176,224,230)

# Dimensões da tela
WIDTH = 600
HEIGHT = 400
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobrinha")

# Configurações da cobrinha
snake_block = 10

snake_speed = 15

# Fonte para a pontuação
font_style = pygame.font.SysFont("bahnschrift", 25)

def mostrar_pontuacao(score):
    value = font_style.render("Score: " + str(score), True, WHITE)
    SCREEN.blit(value, [0, 0])

def desenhar_botao(cor, x, y, largura, altura, texto):
    pygame.draw.rect(SCREEN, cor, [x, y, largura, altura])
    texto_botao = font_style.render(texto, True, BLACK)
    SCREEN.blit(texto_botao, [x + (largura - texto_botao.get_width()) / 2, y + (altura - texto_botao.get_height()) / 2])

def escolher_cor():
    cor_escolhida = None

    while cor_escolhida is None:
        SCREEN.fill(PURPLE)
        mensagem = font_style.render("Escolha a cor da cobrinha:", True, WHITE)
        SCREEN.blit(mensagem, [WIDTH / 6, HEIGHT / 6])

        # Desenhar os botões
        desenhar_botao(WHITE, WIDTH / 6, HEIGHT / 2 - 100, 100, 50, "Branco")
        desenhar_botao(LILAC, WIDTH / 6 + 150, HEIGHT / 2 - 100, 100, 50, "Lilás")
        desenhar_botao(GREEN, WIDTH / 6 + 300, HEIGHT / 2 - 100, 100, 50, "Verde")
        desenhar_botao(BLUE, WIDTH / 6, HEIGHT / 2, 100, 50, "Azul")
        desenhar_botao(YELLOW, WIDTH / 6 + 150, HEIGHT / 2, 100, 50, "Amarelo")
        desenhar_botao(ORANGE, WIDTH / 6 + 300, HEIGHT / 2, 100, 50, "Laranja")
        desenhar_botao(PINK, WIDTH / 6 + 150, HEIGHT / 2 + 100, 100, 50, "Rosa")
        desenhar_botao(MAGENTA, WIDTH / 6 + 300, HEIGHT / 2 + 100, 100, 50, "Magenta")
        desenhar_botao(CYAN, WIDTH / 6, HEIGHT / 2 + 100, 100, 50, "Ciano")
        
        pygame.display.update()

        # Verificar cliques nos botões
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                if WIDTH / 6 <= mouse_x <= WIDTH / 6 + 100 and HEIGHT / 2 - 100 <= mouse_y <= HEIGHT / 2 - 50:
                    cor_escolhida = WHITE
                elif WIDTH / 6 + 150 <= mouse_x <= WIDTH / 6 + 250 and HEIGHT / 2 - 100 <= mouse_y <= HEIGHT / 2 - 50:
                    cor_escolhida = LILAC
                elif WIDTH / 6 + 300 <= mouse_x <= WIDTH / 6 + 400 and HEIGHT / 2 - 100 <= mouse_y <= HEIGHT / 2 - 50:
                    cor_escolhida = GREEN
                elif WIDTH / 6 <= mouse_x <= WIDTH / 6 + 100 and HEIGHT / 2 <= mouse_y <= HEIGHT / 2 + 50:
                    cor_escolhida = BLUE
                elif WIDTH / 6 + 150 <= mouse_x <= WIDTH / 6 + 250 and HEIGHT / 2 <= mouse_y <= HEIGHT / 2 + 50:
                    cor_escolhida = YELLOW
                elif WIDTH / 6 + 300 <= mouse_x <= WIDTH / 6 + 400 and HEIGHT / 2 <= mouse_y <= HEIGHT / 2 + 50:
                    cor_escolhida = ORANGE
                elif WIDTH / 6 + 150 <= mouse_x <= WIDTH / 6 + 250 and HEIGHT / 2 + 100 <= mouse_y <= HEIGHT / 2 + 150:
                    cor_escolhida = PINK
                elif WIDTH / 6 + 300 <= mouse_x <= WIDTH / 6 + 400 and HEIGHT / 2 + 100 <= mouse_y <= HEIGHT / 2 + 150:
                    cor_escolhida = MAGENTA
                elif WIDTH / 6 <= mouse_x <= WIDTH / 6 + 100 and HEIGHT / 2 + 100 <= mouse_y <= HEIGHT / 2 + 150:
                    cor_escolhida = CYAN

    return cor_escolhida

def game_loop():
    game_over = False
    game_close = False

    # Chama a função para escolher a cor da cobrinha
    snake_color = escolher_cor()

    x1 = WIDTH / 2
    y1 = HEIGHT / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    fruit_x = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
    fruit_y = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0

    while not game_over:

        while game_close:
            SCREEN.fill(PURPLE)
            # Fontes diferentes para o Game Over e para a instrução
            game_over_font = pygame.font.SysFont("bahnschrift", 70)  # Fonte maior para o "Game Over"
            instruction_font = pygame.font.SysFont("bahnschrift", 25)  # Fonte menor para a instrução

            # Mensagem de "Game Over"
            mensagem_game_over = game_over_font.render("Game Over!", True, RED)
            mensagem_instrucao = instruction_font.render("Pressione a tecla Enter para jogar novamente.", True, WHITE)

            # Posição centralizada para o "Game Over"
            mensagem_game_over_rect = mensagem_game_over.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
            SCREEN.blit(mensagem_game_over, mensagem_game_over_rect)

            # Posição centralizada para a instrução, logo abaixo do "Game Over"
            mensagem_instrucao_rect = mensagem_instrucao.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
            SCREEN.blit(mensagem_instrucao, mensagem_instrucao_rect)

            # Mostrar pontuação
            mostrar_pontuacao(length_of_snake - 1)

            # Atualizar a tela
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_KP_ENTER:
                        game_loop()
                         
                  
                    
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        SCREEN.fill(PURPLE)

        pygame.draw.rect(SCREEN, RED, [fruit_x, fruit_y, snake_block, snake_block])

        snake_head = []
        snake_head.append(x1)
        snake_head.append(y1)
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        for segment in snake_list:
            pygame.draw.rect(SCREEN, snake_color, [segment[0], segment[1], snake_block, snake_block])

        mostrar_pontuacao(length_of_snake - 1)

        pygame.display.update()

        if x1 == fruit_x and y1 == fruit_y:
            fruit_x = round(random.randrange(0, WIDTH - snake_block) / 10.0) * 10.0
            fruit_y = round(random.randrange(0, HEIGHT - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        pygame.time.Clock().tick(snake_speed)

    pygame.quit()
    quit()

game_loop()