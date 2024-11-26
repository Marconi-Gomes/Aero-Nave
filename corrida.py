import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Definindo as cores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Tamanho da tela
SCREEN_WIDTH = 1366
SCREEN_HEIGHT = 768

# Definindo o display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Jogo de Nave 2D")

# Definindo o relógio
clock = pygame.time.Clock()

# Carregar as imagens
nave_imagem = pygame.image.load(r'c:\Users\marco\Desktop\Corrida\Sprite\Nave.png')
nave_imagem = pygame.transform.scale(nave_imagem, (50, 100))

obstaculo_imagem = pygame.image.load(r'c:\Users\marco\Desktop\Corrida\Sprite\Meteorio.png')
obstaculo_imagem = pygame.transform.scale(obstaculo_imagem, (50, 100))

# Carregar a imagem de fundo (espaço)
fundo_imagem = pygame.image.load(r'c:\Users\marco\Desktop\Corrida\Sprite\espaço.jpg')
fundo_imagem = pygame.transform.scale(fundo_imagem, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregar a imagem de fundo da tela de fim de jogo
fundo_fim_jogo_imagem = pygame.image.load(r'c:\Users\marco\Desktop\Corrida\Sprite\perdeu.png')
fundo_fim_jogo_imagem = pygame.transform.scale(fundo_fim_jogo_imagem, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Carregar a imagem de fundo do menu
fundo_menu_imagem = pygame.image.load(r'c:\Users\marco\Desktop\Corrida\Sprite\mENU.png')
fundo_menu_imagem = pygame.transform.scale(fundo_menu_imagem, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Redimensiona para a tela inteira

# Carregar o som de fundo do jogo
pygame.mixer.music.load(r'c:\Users\marco\Desktop\Corrida\Music\Musica de invasão.mp3')  # Som de fundo do jogo
pygame.mixer.music.set_volume(0.5)  # Define o volume do som (0.0 a 1.0)

# Carregar o som do menu
som_menu = pygame.mixer.Sound(r'c:\Users\marco\Desktop\Corrida\Music\Musica menu Dark.mp3')  # Som de fundo do menu

# Carregar o som do tiro
som_tiro = pygame.mixer.Sound(r'c:\Users\marco\Desktop\Corrida\Music\Tiro.mp3')  # Som do tiro

# Função para desenhar o botão
def desenhar_botao(texto, x, y, largura, altura):
    fonte = pygame.font.SysFont(None, 50)
    texto_renderizado = fonte.render(texto, True, (255, 255, 255))  # Texto em branco
    pygame.draw.rect(screen, RED, (x, y, largura, altura))  # Botão vermelho
    screen.blit(texto_renderizado, (x + (largura - texto_renderizado.get_width()) // 2, y + (altura - texto_renderizado.get_height()) // 2))

# Função para verificar se o botão foi pressionado
def verificar_clique_botao(x, y, largura, altura, pos_mouse):
    if x < pos_mouse[0] < x + largura and y < pos_mouse[1] < y + altura:
        return True
    return False

# Função do menu inicial
def menu():
    menu_ativo = True
    som_menu.play(-1)  # Toca a música do menu em loop
    while menu_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()

                # Verifica se clicou no botão "Iniciar Jogo"
                if verificar_clique_botao(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3, 250, 70, pos_mouse):
                    som_menu.stop()  # Para a música do menu
                    menu_ativo = False
                    return True  # Indica que o jogador quer iniciar o jogo

                # Verifica se clicou no botão "Sair"
                if verificar_clique_botao(SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 100, 250, 70, pos_mouse):
                    som_menu.stop()  # Para a música do menu
                    pygame.quit()  # Fecha o Pygame e o jogo
                    quit()

        # Preencher a tela com a imagem de fundo do menu
        screen.blit(fundo_menu_imagem, (0, 0))  # Desenha o fundo do menu

        # Desenhar os botões
        desenhar_botao('Iniciar Jogo', SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3, 250, 70)
        desenhar_botao('Sair', SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 100, 250, 70)

        # Atualizar a tela
        pygame.display.update()

# Definindo a classe da Nave
class Nave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.largura = 50
        self.altura = 100
        self.velocidade = 5

    def desenhar(self):
        screen.blit(nave_imagem, (self.x, self.y))  # Desenha a imagem da nave

    def mover(self, direcao):
        if direcao == "esquerda" and self.x > 0:  # Verifica se a nave está dentro da borda esquerda
            self.x -= self.velocidade
        elif direcao == "direita" and self.x < SCREEN_WIDTH - self.largura:  # Verifica se a nave está dentro da borda direita
            self.x += self.velocidade
        elif direcao == "cima" and self.y > 0:  # Verifica se a nave está dentro da borda superior
            self.y -= self.velocidade
        elif direcao == "baixo" and self.y < SCREEN_HEIGHT - self.altura:  # Verifica se a nave está dentro da borda inferior
            self.y += self.velocidade


# Definindo a classe do Tiro
class Tiro:
    def __init__(self, x, y):
        self.x = x + 20  # Ajuste para que o tiro saia da posição correta (do meio da nave)
        self.y = y
        self.largura = 10
        self.altura = 20
        self.velocidade = 7  # A velocidade do tiro

    def mover(self):
        self.y -= self.velocidade  # Move o tiro para cima

    def desenhar(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.largura, self.altura))  # Desenha o tiro

    def checar_colisao(self, obstaculos):
        for obs in obstaculos:
            if self.x < obs[0] + 50 and self.x + self.largura > obs[0] and self.y < obs[1] + 50 and self.y + self.altura > obs[1]:
                obstaculos.remove(obs)  # Remove o obstáculo atingido
                return True  # Colisão detectada
        return False  # Nenhuma colisão

# Função principal do jogo
def jogo():
    global pontuacao
    pygame.mixer.music.stop()  # Para a música do menu
    pygame.mixer.music.play(-1)  # Toca a música do jogo em loop
    nave = Nave(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 100)
    direcao = None
    obstaculos = []
    tiros = []
    pontuacao = 0
    tempo_inicial = time.time()  # Marca o tempo inicial do jogo
    jogo_ativo = True
    ultimo_tiro = time.time()  # Para controlar o tempo entre disparos

    while jogo_ativo:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                jogo_ativo = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT:
                    direcao = "esquerda"
                if evento.key == pygame.K_RIGHT:
                    direcao = "direita"
                if evento.key == pygame.K_UP:
                    direcao = "cima"  # Movimento para frente
                if evento.key == pygame.K_DOWN:
                    direcao = "baixo"  # Movimento para trás
                if evento.key == pygame.K_SPACE and time.time() - ultimo_tiro >= 1:  # Agora o intervalo é 1 segundo
                    tiros.append(Tiro(nave.x, nave.y))  # Adiciona um novo tiro
                    som_tiro.play()  # Toca o som do tiro
                    ultimo_tiro = time.time()  # Atualiza o tempo do último disparo
            if evento.type == pygame.KEYUP:
                if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT or evento.key == pygame.K_UP or evento.key == pygame.K_DOWN:
                    direcao = None

        # Atualizar a posição da nave
        if direcao:
            nave.mover(direcao)

        # Criando obstáculos
        if random.randint(1, 20) == 1:
            obstaculos.append([random.randint(0, SCREEN_WIDTH - 50), -50])

        # Atualizando a posição dos obstáculos
        for obs in obstaculos:
            obs[1] += 5

        # Remover obstáculos que saíram da tela
        obstaculos = [obs for obs in obstaculos if obs[1] < SCREEN_HEIGHT]

        # Verificando colisões com obstáculos
        for obs in obstaculos[:]:
            if nave.x < obs[0] + 50 and nave.x + 50 > obs[0] and nave.y < obs[1] + 50 and nave.y + 100 > obs[1]:
                jogo_ativo = False  # Fim de jogo quando a nave colide com o obstáculo

        # Atualizando a pontuação
        tempo_atual = time.time()
        tempo_decorrido = int(tempo_atual - tempo_inicial)

        # A cada segundo que passa, o jogador ganha pontos
        if tempo_decorrido > 0:
            pontuacao += 1  # Aumenta a pontuação continuamente

        # Preencher o fundo da tela com a imagem de fundo do jogo
        screen.blit(fundo_imagem, (0, 0))

        # Desenhar a nave
        nave.desenhar()

        # Desenhar obstáculos
        for obs in obstaculos:
            screen.blit(obstaculo_imagem, (obs[0], obs[1]))  # Desenha os obstáculos

        # Mover e desenhar os tiros
        for tiro in tiros[:]:
            tiro.mover()
            tiro.desenhar()
            if tiro.y < 0:  # Remove tiros que saíram da tela
                tiros.remove(tiro)
            elif tiro.checar_colisao(obstaculos):  # Verifica se o tiro atingiu um obstáculo
                tiros.remove(tiro)  # Remove o tiro após atingir um obstáculo

        # Exibir pontuação na parte superior esquerda
        font = pygame.font.SysFont(None, 35)
        texto_pontuacao = font.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
        screen.blit(texto_pontuacao, (10, 10))  # Ajustado para a parte superior esquerda

        # Exibir tempo de jogo na parte superior esquerda
        texto_tempo = font.render(f'Tempo: {tempo_decorrido}s', True, (255, 255, 255))
        screen.blit(texto_tempo, (10, 50))  # Abaixo da pontuação

        # Atualizar a tela
        pygame.display.update()

        # Controlar a taxa de quadros por segundo
        clock.tick(60)

    # Fim de jogo: exibir fundo de "Fim de Jogo"
    screen.blit(fundo_fim_jogo_imagem, (0, 0))  # Exibe a imagem de fundo do "fim de jogo"

    # Exibir a pontuação final
    font = pygame.font.SysFont(None, 55)
    mensagem = font.render(f'PONTUAÇÃO: {pontuacao}', True, (0, 0, 0))
    screen.blit(mensagem, [SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3])

    # Exibir botão "Tentar outra vez" no canto superior direito
    botao_x = SCREEN_WIDTH - 320  # Posição à direita
    botao_y = 20  # Posição no topo
    botao_largura = 300
    botao_altura = 70
    desenhar_botao('Tentar outra vez', botao_x, botao_y, botao_largura, botao_altura)


    pygame.display.update()

    # Esperar o clique no botão para reiniciar o jogo
    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False
            if evento.type == pygame.MOUSEBUTTONDOWN:
                pos_mouse = pygame.mouse.get_pos()
                if verificar_clique_botao(botao_x, botao_y, botao_largura, botao_altura, pos_mouse):
                    return True  # Reiniciar o jogo
    return False

# Função para rodar o jogo
def main():
    menu_ativo = menu()
    while menu_ativo:
        menu_ativo = jogo()

# Iniciar o jogo
if __name__ == "__main__":
    main()
