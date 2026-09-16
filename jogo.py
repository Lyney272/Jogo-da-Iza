import pygame
import json
import os
import time
import random
import math

# ============================================================
# CAPI CARE
# Virtual Capybara Pet
# Python + Pygame
# ============================================================

pygame.init()
pygame.mixer.init()

# ------------------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------------------

WIDTH = 1100
HEIGHT = 700
FPS = 60

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CapiCare 🦫🎀")

CLOCK = pygame.time.Clock()

SAVE_FILE = "pet_save.json"

# Cores
CREAM = (255, 248, 235)
WHITE = (255, 255, 255)
DARK = (76, 61, 57)

PINK = (245, 166, 190)
LIGHT_PINK = (255, 214, 225)

GREEN = (151, 205, 157)
LIGHT_GREEN = (205, 235, 195)

BLUE = (157, 204, 235)
LIGHT_BLUE = (214, 239, 250)

YELLOW = (250, 214, 119)
LIGHT_YELLOW = (255, 239, 183)

BROWN = (163, 111, 72)
DARK_BROWN = (104, 68, 48)
LIGHT_BROWN = (196, 143, 98)

SHADOW = (220, 198, 181)

# ------------------------------------------------------------
# FONTES
# ------------------------------------------------------------

FONT_BIG = pygame.font.SysFont("arialrounded", 42, bold=True)
FONT_TITLE = pygame.font.SysFont("arialrounded", 30, bold=True)
FONT = pygame.font.SysFont("arialrounded", 23, bold=True)
FONT_SMALL = pygame.font.SysFont("arialrounded", 18)

# ------------------------------------------------------------
# FUNÇÕES AUXILIARES
# ------------------------------------------------------------


def draw_text(surface, text, font, color, x, y, center=False):
    image = font.render(text, True, color)

    if center:
        rect = image.get_rect(center=(x, y))
    else:
        rect = image.get_rect(topleft=(x, y))

    surface.blit(image, rect)


def rounded_rect(surface, color, rect, radius=20):
    pygame.draw.rect(surface, color, rect, border_radius=radius)


def clamp(value, minimum=0, maximum=100):
    return max(minimum, min(maximum, value))


# ------------------------------------------------------------
# PARTÍCULAS
# ------------------------------------------------------------

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

        self.vx = random.uniform(-2.5, 2.5)
        self.vy = random.uniform(-4.5, -1)

        self.life = random.uniform(0.8, 1.5)
        self.max_life = self.life

        self.size = random.randint(4, 9)

    def update(self, dt):
        self.x += self.vx
        self.y += self.vy

        self.vy += 5 * dt
        self.life -= dt

    def draw(self, surface):
        if self.life <= 0:
            return

        alpha = int(255 * (self.life / self.max_life))

        particle_surface = pygame.Surface(
            (self.size * 2, self.size * 2),
            pygame.SRCALPHA
        )

        pygame.draw.circle(
            particle_surface,
            (*self.color, alpha),
            (self.size, self.size),
            self.size
        )

        surface.blit(
            particle_surface,
            (self.x - self.size, self.y - self.size)
        )


# ------------------------------------------------------------
# BOTÃO
# ------------------------------------------------------------

class Button:
    def __init__(self, x, y, width, height, text, color):
        self.rect = pygame.Rect(x, y, width, height)

        self.text = text
        self.color = color

        self.hover = False
        self.pressed = False

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)

    def clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and self.rect.collidepoint(event.pos):
                self.pressed = True
                return True

        return False

    def draw(self, surface):
        color = self.color

        if self.hover:
            color = tuple(min(255, c + 15) for c in color)

        offset = 3 if self.pressed else 0

        # sombra
        pygame.draw.rect(
            surface,
            SHADOW,
            self.rect.move(0, 6),
            border_radius=18
        )

        pygame.draw.rect(
            surface,
            color,
            self.rect.move(0, offset),
            border_radius=18
        )

        draw_text(
            surface,
            self.text,
            FONT,
            DARK,
            self.rect.centerx,
            self.rect.centery + offset,
            center=True
        )

        self.pressed = False


# ------------------------------------------------------------
# CAPIVARA
# ------------------------------------------------------------

class Capybara:

    def __init__(self):
        self.name = "Capi"

        self.hunger = 85
        self.hygiene = 85
        self.energy = 100
        self.fun = 85

        self.sleeping = False
        self.tired = False

        self.sleep_start = None

        self.last_update = time.time()
        self.last_sleep = time.time()

        self.expression = "happy"

        self.animation_time = 0

    # --------------------------------------------------------
    # ATUALIZAÇÃO
    # --------------------------------------------------------

    def update(self):

        current = time.time()
        elapsed = current - self.last_update

        self.last_update = current

        if self.sleeping:
            self.energy = clamp(
                self.energy + elapsed * 8
            )

            if self.energy >= 100:
                self.energy = 100
                self.sleeping = False
                self.tired = False
                self.last_sleep = current

            return

        # Necessidades diminuindo
        self.hunger = clamp(
            self.hunger - elapsed * 0.45
        )

        self.hygiene = clamp(
            self.hygiene - elapsed * 0.20
        )

        self.fun = clamp(
            self.fun - elapsed * 0.12
        )

        self.energy = clamp(
            self.energy - elapsed * 0.12
        )

        # Depois de 10 minutos:
        if current - self.last_sleep >= 600:
            self.tired = True

        # Se estiver muito cansada
        if self.energy <= 15:
            self.tired = True

        # Expressão
        if self.sleeping:
            self.expression = "sleeping"

        elif self.tired:
            self.expression = "tired"

        elif self.hunger < 25:
            self.expression = "hungry"

        elif self.hygiene < 25:
            self.expression = "dirty"

        elif self.fun > 70:
            self.expression = "happy"

        else:
            self.expression = "normal"

        self.animation_time += elapsed

    # --------------------------------------------------------
    # AÇÕES
    # --------------------------------------------------------

    def eat(self):

        if self.tired or self.sleeping:
            return False

        self.hunger = clamp(self.hunger + 30)
        self.fun = clamp(self.fun + 5)

        self.expression = "happy"

        return True

    def bath(self):

        if self.sleeping:
            return False

        self.hygiene = 100
        self.fun = clamp(self.fun + 8)

        self.expression = "happy"

        return True

    def play(self):

        if self.tired or self.sleeping:
            return False

        if self.energy < 20:
            self.tired = True
            return False

        self.fun = clamp(self.fun + 30)
        self.energy = clamp(self.energy - 20)
        self.hunger = clamp(self.hunger - 8)

        self.expression = "happy"

        return True

    def sleep(self):

        if self.sleeping:
            return

        self.sleeping = True
        self.tired = False
        self.expression = "sleeping"

        self.sleep_start = time.time()

    # --------------------------------------------------------
    # SAVE
    # --------------------------------------------------------

    def save(self):

        data = {
            "name": self.name,
            "hunger": self.hunger,
            "hygiene": self.hygiene,
            "energy": self.energy,
            "fun": self.fun,
            "last_sleep": self.last_sleep
        }

        with open(SAVE_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # --------------------------------------------------------
    # LOAD
    # --------------------------------------------------------

    def load(self):

        if not os.path.exists(SAVE_FILE):
            return

        try:

            with open(SAVE_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.name = data.get("name", "Capi")

            self.hunger = data.get("hunger", 85)
            self.hygiene = data.get("hygiene", 85)
            self.energy = data.get("energy", 100)
            self.fun = data.get("fun", 85)

            self.last_sleep = data.get(
                "last_sleep",
                time.time()
            )

        except Exception:
            pass


# ------------------------------------------------------------
# DESENHO DA CAPIVARA
# ------------------------------------------------------------

def draw_capybara(surface, x, y, capy):

    bob = math.sin(capy.animation_time * 3) * 5

    if capy.sleeping:
        bob = math.sin(capy.animation_time * 2) * 2

    x = int(x)
    y = int(y + bob)

    # sombra
    pygame.draw.ellipse(
        surface,
        (190, 171, 153),
        (x - 120, y + 135, 240, 35)
    )

    # corpo
    pygame.draw.ellipse(
        surface,
        BROWN,
        (x - 105, y - 10, 210, 160)
    )

    # cabeça
    pygame.draw.ellipse(
        surface,
        LIGHT_BROWN,
        (x - 100, y - 100, 200, 155)
    )

    # orelhas
    pygame.draw.circle(
        surface,
        DARK_BROWN,
        (x - 70, y - 78),
        22
    )

    pygame.draw.circle(
        surface,
        DARK_BROWN,
        (x + 70, y - 78),
        22
    )

    pygame.draw.circle(
        surface,
        LIGHT_BROWN,
        (x - 70, y - 78),
        13
    )

    pygame.draw.circle(
        surface,
        LIGHT_BROWN,
        (x + 70, y - 78),
        13
    )

    # focinho
    pygame.draw.ellipse(
        surface,
        (210, 163, 119),
        (x - 70, y - 30, 140, 85)
    )

    # olhos
    if capy.sleeping or capy.expression == "sleeping":

        pygame.draw.arc(
            surface,
            DARK,
            (x - 65, y - 25, 35, 20),
            0,
            math.pi,
            4
        )

        pygame.draw.arc(
            surface,
            DARK,
            (x + 30, y - 25, 35, 20),
            0,
            math.pi,
            4
        )

    else:

        pygame.draw.ellipse(
            surface,
            DARK,
            (x - 62, y - 30, 30, 38)
        )

        pygame.draw.ellipse(
            surface,
            DARK,
            (x + 32, y - 30, 30, 38)
        )

        # brilho
        pygame.draw.circle(
            surface,
            WHITE,
            (x - 53, y - 18),
            7
        )

        pygame.draw.circle(
            surface,
            WHITE,
            (x + 41, y - 18),
            7
        )

    # nariz
    pygame.draw.ellipse(
        surface,
        DARK_BROWN,
        (x - 24, y + 5, 48, 28)
    )

    # boca
    pygame.draw.arc(
        surface,
        DARK_BROWN,
        (x - 30, y + 15, 60, 35),
        0,
        math.pi,
        3
    )

    # bochechas
    if capy.expression == "happy":
        pygame.draw.circle(
            surface,
            (240, 145, 157),
            (x - 75, y + 5),
            13
        )

        pygame.draw.circle(
            surface,
            (240, 145, 157),
            (x + 75, y + 5),
            13
        )

    # patas
    pygame.draw.ellipse(
        surface,
        LIGHT_BROWN,
        (x - 75, y + 100, 55, 45)
    )

    pygame.draw.ellipse(
        surface,
        LIGHT_BROWN,
        (x + 20, y + 100, 55, 45)
    )

    # --------------------------------------------------------
    # LACINHO 🎀
    # --------------------------------------------------------

    bow_y = y - 108

    # laço esquerdo
    pygame.draw.ellipse(
        surface,
        PINK,
        (x - 55, bow_y - 20, 60, 45)
    )

    # laço direito
    pygame.draw.ellipse(
        surface,
        PINK,
        (x - 5, bow_y - 20, 60, 45)
    )

    # centro
    pygame.draw.circle(
        surface,
        (231, 119, 153),
        (x, bow_y),
        17
    )

    # brilho
    pygame.draw.circle(
        surface,
        LIGHT_PINK,
        (x - 5, bow_y - 5),
        5
    )

    # --------------------------------------------------------
    # INDICADORES DE EMOÇÃO
    # --------------------------------------------------------

    if capy.expression == "hungry":

        draw_text(
            surface,
            "Estou com fome...",
            FONT_SMALL,
            DARK,
            x,
            y + 190,
            center=True
        )

    elif capy.expression == "tired":

        draw_text(
            surface,
            "Estou cansada... 💤",
            FONT_SMALL,
            DARK,
            x,
            y + 190,
            center=True
        )

    elif capy.expression == "dirty":

        draw_text(
            surface,
            "Um banho seria ótimo!",
            FONT_SMALL,
            DARK,
            x,
            y + 190,
            center=True
        )

    elif capy.sleeping:

        draw_text(
            surface,
            "Z z z...",
            FONT_TITLE,
            DARK,
            x + 110,
            y - 90,
            center=True
        )


# ------------------------------------------------------------
# FUNDO
# ------------------------------------------------------------

def draw_background(surface, mode="garden"):

    if mode == "garden":

        surface.fill((225, 245, 218))

        # céu
        pygame.draw.rect(
            surface,
            (191, 226, 242),
            (0, 0, WIDTH, 220)
        )

        # nuvens
        for cx, cy in [(130, 90), (750, 80), (950, 130)]:

            pygame.draw.circle(
                surface,
                WHITE,
                (cx, cy),
                30
            )

            pygame.draw.circle(
                surface,
                WHITE,
                (cx + 30, cy + 5),
                25
            )

            pygame.draw.circle(
                surface,
                WHITE,
                (cx - 30, cy + 7),
                23
            )

        # chão
        pygame.draw.rect(
            surface,
            (164, 210, 145),
            (0, 220, WIDTH, 480)
        )

        # flores
        for _ in range(25):

            x = random.randint(0, WIDTH)
            y = random.randint(260, HEIGHT)

            pygame.draw.circle(
                surface,
                random.choice([
                    (255, 232, 151),
                    (255, 190, 205),
                    WHITE
                ]),
                (x, y),
                5
            )

    elif mode == "bathroom":

        surface.fill((210, 239, 245))

        # azulejos
        for x in range(0, WIDTH, 70):
            for y in range(0, HEIGHT, 70):

                pygame.draw.rect(
                    surface,
                    (190, 225, 233),
                    (x, y, 68, 68),
                    2
                )

        # piso
        pygame.draw.rect(
            surface,
            (230, 244, 240),
            (0, 500, WIDTH, 200)
        )

    elif mode == "bedroom":

        surface.fill((242, 220, 229))

        # parede
        pygame.draw.rect(
            surface,
            (249, 229, 236),
            (0, 0, WIDTH, 500)
        )

        # piso
        pygame.draw.rect(
            surface,
            (211, 174, 160),
            (0, 500, WIDTH, 200)
        )

        # tapete
        pygame.draw.ellipse(
            surface,
            (247, 196, 213),
            (330, 480, 440, 130)
        )

        # cama
        pygame.draw.rect(
            surface,
            (167, 117, 91),
            (690, 300, 300, 190),
            border_radius=25
        )

        pygame.draw.rect(
            surface,
            (255, 239, 244),
            (710, 315, 260, 115),
            border_radius=20
        )

        pygame.draw.rect(
            surface,
            (244, 177, 201),
            (700, 410, 280, 70),
            border_radius=20
        )


# ------------------------------------------------------------
# BARRA DE STATUS
# ------------------------------------------------------------

def draw_status_bar(
    surface,
    x,
    y,
    label,
    value,
    color,
    icon
):

    draw_text(
        surface,
        f"{icon} {label}",
        FONT_SMALL,
        DARK,
        x,
        y
    )

    bar_x = x
    bar_y = y + 27

    width = 190
    height = 17

    rounded_rect(
        surface,
        (230, 220, 215),
        (bar_x, bar_y, width, height),
        10
    )

    rounded_rect(
        surface,
        color,
        (
            bar_x,
            bar_y,
            int(width * (value / 100)),
            height
        ),
        10
    )

    draw_text(
        surface,
        f"{int(value)}%",
        FONT_SMALL,
        DARK,
        bar_x + width + 8,
        bar_y - 3
    )


# ------------------------------------------------------------
# JOGO
# ------------------------------------------------------------

class Game:

    def __init__(self):

        self.capybara = Capybara()
        self.capybara.load()

        self.running = True

        self.scene = "garden"

        self.particles = []

        self.message = ""
        self.message_timer = 0

        # Botões
        self.eat_button = Button(
            50, 585, 220, 70,
            "🍎 Alimentar",
            LIGHT_YELLOW
        )

        self.bath_button = Button(
            290, 585, 220, 70,
            "🛁 Dar banho",
            LIGHT_BLUE
        )

        self.sleep_button = Button(
            530, 585, 220, 70,
            "💤 Dormir",
            LIGHT_PINK
        )

        self.play_button = Button(
            770, 585, 280, 70,
            "⚽ Brincar",
            LIGHT_GREEN
        )

        self.auto_save_timer = 0

    # --------------------------------------------------------
    # PARTÍCULAS
    # --------------------------------------------------------

    def create_particles(self, color):

        for _ in range(20):

            self.particles.append(
                Particle(
                    WIDTH // 2 + random.randint(-100, 100),
                    400,
                    color
                )
            )

    # --------------------------------------------------------
    # MENSAGEM
    # --------------------------------------------------------

    def show_message(self, text):

        self.message = text
        self.message_timer = 2.5

    # --------------------------------------------------------
    # AÇÕES
    # --------------------------------------------------------

    def eat(self):

        if self.capybara.tired:

            self.show_message(
                "😴 A Capi está cansada! Ela precisa dormir."
            )
            return

        if self.capybara.eat():

            self.scene = "garden"

            self.create_particles(
                (255, 197, 94)
            )

            self.show_message(
                "🍎 Nhac! A Capi adorou a comida!"
            )

    def bath(self):

        if self.capybara.bath():

            self.scene = "bathroom"

            self.create_particles(
                (155, 218, 240)
            )

            self.show_message(
                "🛁 A Capi ficou limpinha!"
            )

    def sleep(self):

        self.scene = "bedroom"

        self.capybara.sleep()

        self.show_message(
            "💤 Boa noite, Capi..."
        )

    def play(self):

        if self.capybara.tired:

            self.show_message(
                "😴 A Capi está cansada demais para brincar."
            )
            return

        if self.capybara.play():

            self.scene = "garden"

            self.create_particles(
                (255, 160, 194)
            )

            self.show_message(
                "⚽ Uhuu! A Capi se divertiu!"
            )

    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if self.eat_button.clicked(event):
                self.eat()

            elif self.bath_button.clicked(event):
                self.bath()

            elif self.sleep_button.clicked(event):
                self.sleep()

            elif self.play_button.clicked(event):
                self.play()

    # --------------------------------------------------------
    # UPDATE
    # --------------------------------------------------------

    def update(self, dt):

        self.capybara.update()

        mouse_pos = pygame.mouse.get_pos()

        self.eat_button.update(mouse_pos)
        self.bath_button.update(mouse_pos)
        self.sleep_button.update(mouse_pos)
        self.play_button.update(mouse_pos)

        # partículas
        for particle in self.particles:
            particle.update(dt)

        self.particles = [
            p for p in self.particles
            if p.life > 0
        ]

        # mensagem
        if self.message_timer > 0:

            self.message_timer -= dt

        # autosave
        self.auto_save_timer += dt

        if self.auto_save_timer >= 10:

            self.capybara.save()
            self.auto_save_timer = 0

    # --------------------------------------------------------
    # DESENHO
    # --------------------------------------------------------

    def draw(self):

        draw_background(
            SCREEN,
            self.scene
        )

        # ----------------------------------------------------
        # PAINEL SUPERIOR
        # ----------------------------------------------------

        rounded_rect(
            SCREEN,
            (255, 251, 246),
            (25, 20, 1050, 135),
            28
        )

        draw_text(
            SCREEN,
            "CapiCare",
            FONT_BIG,
            DARK,
            50,
            35
        )

        draw_text(
            SCREEN,
            f"🦫 {self.capybara.name}",
            FONT,
            DARK,
            52,
            92
        )

        # status
        draw_status_bar(
            SCREEN,
            300,
            35,
            "Fome",
            self.capybara.hunger,
            (244, 184, 95),
            "🍎"
        )

        draw_status_bar(
            SCREEN,
            550,
            35,
            "Higiene",
            self.capybara.hygiene,
            (117, 190, 230),
            "🛁"
        )

        draw_status_bar(
            SCREEN,
            800,
            35,
            "Energia",
            self.capybara.energy,
            (238, 175, 207),
            "⚡"
        )

        # diversão embaixo
        draw_status_bar(
            SCREEN,
            300,
            92,
            "Diversão",
            self.capybara.fun,
            (142, 202, 146),
            "❤️"
        )

        # ----------------------------------------------------
        # CAPIVARA
        # ----------------------------------------------------

        draw_capybara(
            SCREEN,
            WIDTH // 2,
            350,
            self.capybara
        )

        # ----------------------------------------------------
        # ALERTA DE CANSAÇO
        # ----------------------------------------------------

        if self.capybara.tired and not self.capybara.sleeping:

            rounded_rect(
                SCREEN,
                (255, 235, 240),
                (345, 165, 410, 55),
                25
            )

            draw_text(
                SCREEN,
                "💤 Sua capivara precisa dormir!",
                FONT,
                DARK,
                550,
                192,
                center=True
            )

        # ----------------------------------------------------
        # PARTÍCULAS
        # ----------------------------------------------------

        for particle in self.particles:
            particle.draw(SCREEN)

        # ----------------------------------------------------
        # MENSAGEM
        # ----------------------------------------------------

        if self.message_timer > 0:

            rounded_rect(
                SCREEN,
                WHITE,
                (270, 500, 560, 60),
                25
            )

            draw_text(
                SCREEN,
                self.message,
                FONT_SMALL,
                DARK,
                550,
                530,
                center=True
            )

        # ----------------------------------------------------
        # BOTÕES
        # ----------------------------------------------------

        self.eat_button.draw(SCREEN)
        self.bath_button.draw(SCREEN)
        self.sleep_button.draw(SCREEN)
        self.play_button.draw(SCREEN)

        pygame.display.flip()

    # --------------------------------------------------------
    # LOOP
    # --------------------------------------------------------

    def run(self):

        while self.running:

            dt = CLOCK.tick(FPS) / 1000

            self.handle_events()
            self.update(dt)
            self.draw()

        self.capybara.save()

        pygame.quit()


# ============================================================
# INICIAR
# ============================================================

if __name__ == "__main__":

    game = Game()
    game.run()


