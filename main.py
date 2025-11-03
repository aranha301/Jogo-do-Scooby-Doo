import pygame
import random

pygame.init()

LARGURA, ALTURA = 800, 600

TELA = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Fuja dos monstros com o Scooby Doo")

RELOGIO = pygame.time.Clock()

PRETO = (250, 250, 250)
AZUL = (70, 45, 120)

# ------------------------------  CRIAR AS CLASSES AQUI   -------------------------------------------------
class Personagem():
    def __init__(self):
        self.x = 100
        self.y = 500
        self.altura = 50
        self.largura =50
        self.vel_x = 0
        self.vel_y = 0
        self.no_chao = True
        self.gravidade = 0.5
        self.forca_pulo = 22
        self.velocidade_andar = 5
        self.sprite = pygame.image.load("SD.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

    def pular(self):
        if self.no_chao == True:
            self.vel_y = -self.forca_pulo
            self.no_chao = False
    
    def andar(self,direção):
        if direção == "esquerda":
            self.vel_x = -self.velocidade_andar
        elif direção == "direita":
            self.vel_x = self.velocidade_andar

    def parar(self):
        self.vel_x = 0

    def atualizar(self):
        self.vel_y += self.gravidade
        self.y += self.vel_y
        self.x += self.vel_x
        if self.y + self.altura >= 550:
            self.y = 550 - self.altura
            self.vel_y = 0
            self.no_chao = True
        if self.x + self.largura > 800:
            self.x = 800 - self.largura
        if self.x < 0:
            self.x = 0

    def desenhar(self,tela):
        tela.blit(self.sprite, (self.x, self.y))

class Moeda():
    def __init__(self):
            self.altura = 50
            self.largura =50
            self.x = random.randint(60, 520 - self.largura)
            self.y = random.randint(60, 520 - self.altura)
            self.sprite = pygame.image.load("Biscoito Scooby.png").convert_alpha()
            self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))

    def desenhar(self,tela):
         tela.blit(self.sprite, (self.x, self.y))

class Player(Personagem):
    def __init__(self):
        super().__init__()
        self.vida = 100
        self.pontos = 0
        self.vivo = True
    
    def morrer(self):
        self.vivo = False

    def tomar_dano(self, dano):
        self.vida -= dano       
        if self.vida <= 0:
            self.morrer()

    def ganhar_pontos(self, pontos):
        self.pontos += pontos

class Inimigo(Personagem):
    def __init__(self, alvo: Personagem, posicao_x = None):
        super().__init__()
        self.alvo = alvo
        self.x = posicao_x if posicao_x is not None else random.randint(0, LARGURA - self.largura)
        self.sprite = pygame.image.load("New Piskel.png").convert_alpha()
        self.sprite = pygame.transform.scale(self.sprite, (self.largura, self.altura))
        self.velocidade_andar = 2

    def atualizar(self):
        distancia = self.alvo.x - self.x
        if abs(distancia) > 15:
            if(distancia) > 0:
                self.andar('direita')
            else:
                self.andar('esquerda')
            super().atualizar()

    

# ---------------------------------------------------------------------------------------------------------
ultimo_spawn_inimigo = pygame.time.get_ticks()
intervalo_spawn = 500


rodando = True
jogador = Player()
inimigos = [Inimigo(jogador) for _ in range(1)]  # AULA DE HERANÇA, IGNORAR
moedas = [Moeda() for _ in range(5)]
pontos = 0
vida = 100

while rodando:
    RELOGIO.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE:
                #Fazer o jogador pular
                jogador.pular()
    keys = pygame.key.get_pressed()
    if jogador.vivo:  # AULA DE HERANÇA, IGNORAR (Player)
        if keys[pygame.K_LEFT]:
        # Fazer o jogador andar 
            jogador.andar("esquerda")
        elif keys[pygame.K_RIGHT]:
        # Fazer o jogador andar 
            jogador.andar("direita")
        else:
        # Fazer o jogador parar 
            jogador.parar()
    # Atualizar o jogador
    jogador.atualizar()

    jogador_hitbox = pygame.Rect(jogador.x, jogador.y, jogador.largura, jogador.altura) 
    TELA.fill(PRETO)
    
    # LOOP DE INIMIGOS - AULA DE HERANÇA, IGNORAR
    for inimigo in inimigos:
         inimigo.atualizar()
         inimigo.desenhar(TELA)

         inimigo_hitbox = pygame.Rect(inimigo.x, inimigo.y, inimigo.largura, inimigo.altura)
         if jogador.vivo and jogador_hitbox.colliderect(inimigo_hitbox):
             jogador.tomar_dano(1)

    fonte = pygame.font.SysFont(None, 30)
    texto_vida = fonte.render(f"Vida: {jogador.vida}", True, (255, 0, 0))  # AULA DE HERANÇA, IGNORAR
    texto_pontos = fonte.render(f"Pontos: {jogador.pontos}", True, (0, 0, 0))  # AULA DE HERANÇA, IGNORAR
    texto_vida = fonte.render(f"Vida: {vida}", True, (255, 0, 0))
    texto_pontos = fonte.render(f"Pontos: {pontos}", True, (0, 0, 0))
    TELA.blit(texto_vida, (10, 10))
    TELA.blit(texto_pontos, (10, 40))
    jogador.desenhar(TELA)
    
    for moeda in moedas[:]:
        moeda.desenhar(TELA)
        moeda_hitbox = pygame.Rect(moeda.x, moeda.y, moeda.largura, moeda.altura)
        if jogador_hitbox.colliderect(moeda_hitbox):
            jogador.ganhar_pontos(10)  # AULA DE HERANÇA, IGNORAR
            pontos += 10  # Versão sem herança
            moedas.remove(moeda)
    
    if len(moedas) < 5:
        moedas.append(Moeda())
    
    # SPAWN DE INIMIGOS - AULA DE HERANÇA, IGNORAR
    tempo_atual = pygame.time.get_ticks()
    if tempo_atual - ultimo_spawn_inimigo >= intervalo_spawn and len(inimigos) < 50:
         inimigos.append(Inimigo(jogador))
         ultimo_spawn_inimigo = tempo_atual

    if jogador.pontos >= 200:  # AULA DE HERANÇA, IGNORAR
        if pontos >= 200:  # Versão sem herança
            TELA.fill(PRETO)
            fonte_grande = pygame.font.SysFont(None, 60)
            texto_vitoria = fonte_grande.render("Você ganhou!!! Fugiu dos monstros", True, (0, 200, 0))
            texto_rect = texto_vitoria.get_rect(center=(LARGURA // 2, ALTURA // 2))
            TELA.blit(texto_vitoria, texto_rect)
            pygame.display.update()
            pygame.time.delay(5000)
            rodando = False
    
    if jogador.vida <= 0:  # AULA DE HERANÇA, IGNORAR
        
            TELA.fill(PRETO)
            fonte_grande = pygame.font.SysFont(None, 60)
            texto_vitoria = fonte_grande.render("Oh não, os monstros te pegeram", True, (255, 0, 0))
            texto_rect = texto_vitoria.get_rect(center=(LARGURA // 2, ALTURA // 2))
            TELA.blit(texto_vitoria, texto_rect)
            pygame.display.update()
            pygame.time.delay(5000)
            rodando = False

    pygame.draw.rect(TELA, (0, 255, 0), (0, 550, LARGURA, 50))
    pygame.display.update()

pygame.quit()