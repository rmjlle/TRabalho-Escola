import os
import random
import pygame

pygame.init()

# Configurações Globais
SCREEN_HEIGHT = 1000
SCREEN_WIDTH = 1500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Game Modificado")

# Cores
WHITE = (255, 255, 255)

# Carregamento e redimensionamento das imagens
# Carregamento e redimensionamento das imagens
BG = pygame.image.load(os.path.join("Assets/Other", "RUA 8.png"))
BG = pygame.transform.scale(BG, (SCREEN_WIDTH * 15, SCREEN_HEIGHT))

# Aumentando o tamanho do dinossauro e dos obstáculos em 30%
RUNNING = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "KartMax1.png")), (98, 60)),
           pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "KartMax2.png")), (98, 60))]
JUMPING = pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "MAXJUMP.png")), (99, 87))
DUCKING = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "MAXDUCK.png")), (99, 53)),
           pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "MAXDUCK.png")), (99, 53))]
DYING = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Dino", "DeadMax.png")), (104, 48))]

# Aumentando o tamanho dos obstáculos em 30%
SMALL_CACTUS = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "Lixo.png")), (60, 104))]
LARGE_CACTUS = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Cactus", "penus.png")), (61, 77))]
BIRD = [pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")), (236/2, 236/2)),
        pygame.transform.scale(pygame.image.load(os.path.join("Assets/Bird", "Bird1.png")), (236/2, 236/2))]


# Classe do Dinossauro
class Dinosaur:
    X_POS = 0
    Y_POS = 693
    Y_POS_DUCK = 700
    Y_POS_DEAD = 730
    JUMP_VEL = 8.5

    def __init__(self):
        self.duck_img = DUCKING
        self.run_img = RUNNING
        self.jump_img = JUMPING
        self.dead_img = DYING

        self.dino_duck = False
        self.dino_run = True
        self.dino_jump = False
        self.dino_dead = False

        self.step_index = 0
        self.jump_vel = self.JUMP_VEL
        self.image = self.run_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS

    def update(self, userInput):
        if self.dino_dead:
            self.dead()
        elif self.dino_duck:
            self.duck()
        elif self.dino_run:
            self.run()
        elif self.dino_jump:
            self.jump()

        if self.step_index >= 10:
            self.step_index = 0

        if userInput[pygame.K_SPACE] and not self.dino_jump and not self.dino_dead:
            self.dino_duck = False
            self.dino_run = False
            self.dino_jump = True
        elif userInput[pygame.K_DOWN] and not self.dino_jump and not self.dino_dead:
            self.dino_duck = True
            self.dino_run = False
            self.dino_jump = False
        elif not (self.dino_jump or userInput[pygame.K_DOWN]):
            self.dino_duck = False
            self.dino_run = True
            self.dino_jump = False

    def duck(self):
        self.image = self.duck_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DUCK
        self.step_index += 1

    def run(self):
        self.image = self.run_img[self.step_index // 5]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index += 1

    def jump(self):
        self.image = self.jump_img
        if self.dino_jump:
            self.dino_rect.y -= self.jump_vel * 4
            self.jump_vel -= 0.8
        if self.jump_vel < -self.JUMP_VEL:
            self.dino_jump = False
            self.jump_vel = self.JUMP_VEL

    def dead(self):
        self.image = self.dead_img[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS_DEAD

    def draw(self, SCREEN):
        SCREEN.blit(self.image, (self.dino_rect.x, self.dino_rect.y))


# Classe dos Obstáculos
class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image[self.type].get_rect()
        self.rect.x = SCREEN_WIDTH

    def update(self):
        global obstacles
        self.rect.x -= game_speed
        if self.rect.x < -self.rect.width:
            obstacles.pop()

    def draw(self, SCREEN):
        SCREEN.blit(self.image[self.type], self.rect)

    def check_proximity(self, dino):
    # Checa se o retângulo do obstáculo colide com o retângulo do dinossauro
        return self.rect.colliderect(dino.dino_rect)


class SmallCactus(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 670


class LargeCactus(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        self.rect.y = 680


class Bird(Obstacle):
    def __init__(self, image):
        self.type = 0
        super().__init__(image, self.type)
        
        # Define a posição y do pássaro de forma fixa ou aleatória acima de 689 pixels
        self.rect.y = random.choice([570, 550, 560])  # Alturas altas o suficiente para passar por cima do dinossauro agachado
        self.index = 0
        self.rotation_angle = 0  # Ângulo inicial de rotação

    def draw(self, SCREEN): 
        # Incrementa o ângulo de rotação a cada frame
        self.rotation_angle = (self.rotation_angle + 1) % 360  # Gira um grau a cada frame, reseta a 0 após 360 graus
        
        # Alterna entre as imagens do pássaro para animação e aplica rotação
        current_image = self.image[self.index // 5]
        rotated_image = pygame.transform.rotate(current_image, self.rotation_angle)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)  # Centraliza a rotação
        
        # Exibe a imagem rotacionada na tela
        SCREEN.blit(rotated_image, rotated_rect)
        
        # Atualiza o índice para a animação do pássaro
        self.index += 1
        if self.index >= 10:
            self.index = 0


# Função Principal do Jogo
def main():
    global game_speed, x_pos_bg, y_pos_bg, points, obstacles, run, start_time
    run = True
    clock = pygame.time.Clock()
    player = Dinosaur()
    game_speed = 30  # Velocidade inicial
    x_pos_bg = -100
    y_pos_bg = 0 
    points = 0
    obstacles = []
    death_count = 0
    start_time = pygame.time.get_ticks()

    while run:
        SCREEN.fill(WHITE)

        # Movimento do fundo (efeito de paralaxe)
        x_pos_bg -= game_speed // 2  # A velocidade do fundo é a metade da velocidade do jogo
        SCREEN.blit(BG, (x_pos_bg, y_pos_bg))  # Fundo
        SCREEN.blit(BG, (x_pos_bg + SCREEN_WIDTH * 15, y_pos_bg))  # Fundo adicional para criar o loop

        if x_pos_bg <= -SCREEN_WIDTH * 15:  # Reseta a posição do fundo
            x_pos_bg = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        userInput = pygame.key.get_pressed()
        player.update(userInput)

        if len(obstacles) == 0:
            if random.randint(0, 2) == 0:
                obstacles.append(SmallCactus(SMALL_CACTUS))
            elif random.randint(0, 2) == 1:
                obstacles.append(LargeCactus(LARGE_CACTUS))
            elif random.randint(0, 2) == 2:
                obstacles.append(Bird(BIRD))
        
        for obstacle in obstacles:
            obstacle.update()
            obstacle.draw(SCREEN)
            if obstacle.check_proximity(player):
                player.dino_dead = True
                menu(death_count)
                return  # Encerra o loop principal ao morrer

        player.draw(SCREEN)

        # Atualiza os pontos e aumenta a velocidade do jogo
        points = (pygame.time.get_ticks() - start_time) // 100
        if points % 100 == 0 and points != 0:  # Aumenta a velocidade a cada 100 pontos
            game_speed += 1

        font = pygame.font.Font('freesansbold.ttf', 20)
        text = font.render(f"Pontos: {points}", True, (0, 0, 0))
        SCREEN.blit(text, (900, 50))

        clock.tick(30)
        pygame.display.update()


# Função para exibir o Menu
def menu(death_count):
    global points
    run = True
    while run:
        SCREEN.fill(WHITE)
        font = pygame.font.Font('freesansbold.ttf', 30)

        if death_count == 0:
            text = font.render("Pressione qualquer tecla para iniciar", True, (0, 0, 0))
        else:
            text = font.render("If my moomma had balls, she would have been my dad", True, (0, 0, 0))
            score = font.render("Teus Pontos: {points}", True, (0, 0, 0))
            scoreRect = score.get_rect()
            scoreRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            SCREEN.blit(score, scoreRect)

        textRect = text.get_rect()
        textRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        SCREEN.blit(text, textRect)
        SCREEN.blit(RUNNING[0], (SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 - 140))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                main()


menu(death_count=0)
