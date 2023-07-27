from main import speak
from configs import Configs
import serial
import pygame
import sys

arduino = serial.Serial('COM14', 9600)
pygame.init()

if speak():

    # Defina as dimensões da janela (tamanho da imagem)

    # Crie a janela
    window = pygame.display.set_mode((Configs.window_width, Configs.window_height))
    pygame.display.set_caption('Assistente Holográfica')

    # Loop principal
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Preencha o fundo da janela com uma cor ou imagem, se desejar
        window.fill((255, 255, 255))  # Cor branca como exemplo

        # Desenhe a imagem da assistente na janela
        window.blit(Configs.assistant_image, (200, 200))  # Posição (0, 0) como exemplo

        # Atualize a tela
        pygame.display.flip()




