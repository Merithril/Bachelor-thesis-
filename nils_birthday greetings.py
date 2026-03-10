"""
  Birthday greetings for Nils.
   """

import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("OO Geburtstagsanimation")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 48, bold=True)
small_font = pygame.font.SysFont("Arial", 24)


class CakeLayer:
    def __init__(self, y, width, height, layer_idx):
        self.y = y
        self.width = width
        self.height = height
        self.idx = layer_idx
        self.color = [(255, 180, 180), (255, 140, 140), (255, 100, 100)][layer_idx % 3]
        self.cream_color = (255, 255, 220)
        self.visible = False

    def show(self):
        self.visible = True

    def update(self, dt):
        pass  # Statisch nach Aufbau

    def draw(self, screen):
        if not self.visible: return

        rect = pygame.Rect(400 - self.width // 2, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
        cream_rect = rect.inflate(-12, -20)
        pygame.draw.rect(screen, self.cream_color, cream_rect)
        pygame.draw.circle(screen, self.color, (int(rect.left + 20), int(rect.centery)), 20)
        pygame.draw.circle(screen, self.color, (int(rect.right - 20), int(rect.centery)), 20)


class Candle:
    def __init__(self, x, y_base):
        self.x = x
        self.y_base = y_base
        self.flame_offset = 0

    def update(self, dt, global_time):
        self.flame_offset = math.sin(global_time * 10) * 1.5

    def draw(self, screen):
        # Kerze
        pygame.draw.rect(screen, (240, 200, 100), (self.x - 2, self.y_base - 65, 4, 65))
        pygame.draw.circle(screen, (100, 50, 0), (int(self.x), self.y_base - 68), 2)
        # Flamme
        flame_y = self.y_base - 72 + self.flame_offset
        pygame.draw.ellipse(screen, (255, 180, 50), (self.x - 4, flame_y, 8, 7))


class ConfettiParticle:
    def __init__(self):
        self.x = random.randint(-20, 820)
        self.y = random.randint(-50, -10)
        self.color = random.choice([(255, 100, 150), (150, 255, 150), (150, 150, 255), (255, 255, 100)])
        self.size = random.randint(4, 9)
        self.sway_speed = random.uniform(-90, 90)
        self.fall_speed = 180
        self.rotation = 0
        self.dead = False

    def update(self, dt):
        self.x += self.sway_speed * dt
        self.y += self.fall_speed
        self.sway_speed += random.uniform(-120, 120) * dt
        self.fall_speed += 60 * dt
        self.rotation += 3 * dt

        if self.y > 650:
            self.dead = True

    def draw(self, screen):
        surf = pygame.Surface((self.size * 2.2, self.size * 2.2), pygame.SRCALPHA)
        points = [[self.size, 0], [self.size * 2.2, self.size * 1.1], [0, self.size * 2.2]]
        pygame.draw.polygon(surf, self.color, points)
        rotated = pygame.transform.rotate(surf, math.sin(self.y * 0.12) * 60)
        screen.blit(rotated, (self.x - self.size, self.y - self.size))


class BirthdayScene:
    def __init__(self):
        self.time = 0
        self.cake_layers = []
        self.candles = []
        self.confetti = []
        self.text_alpha = 0
        self.font = font
        self.small_font = small_font

        # Kuchen schichten initialisieren (unsichtbar)
        base_y = 520
        layer_h = 85
        for i in range(3):
            scale = 1.0 - (i * 0.12)
            y = base_y - (i * layer_h)
            width = int(220 * scale)
            self.cake_layers.append(CakeLayer(y, width, layer_h, i))

        # Setup fertig
        self.setup_candles()

    def setup_candles(self):
        # Kerzen werden später positioniert
        pass

    def update(self, dt):
        self.time += dt

        # Kuchen schichtweise sichtbar machen (0-3s)
        progress = min(self.time / 3.0, 1.0)
        num_visible = int(progress * 3) + 1
        for i in range(len(self.cake_layers)):
            self.cake_layers[i].visible = i < num_visible

        # Kerzen positionieren wenn Top-Schicht sichtbar
        if self.cake_layers[0].visible:
            top_layer = self.cake_layers[0]
            candle_base_y = top_layer.y - 15
            if not self.candles:
                for j in range(6):
                    cx = 400 - 75 + j * 27
                    self.candles.append(Candle(cx, candle_base_y))

        # Konfetti spawn
        if self.time > 1.5 and len(self.confetti) < 150:
            self.confetti.append(ConfettiParticle())

        # Alle Objekte updaten
        for layer in self.cake_layers:
            layer.update(dt)
        for candle in self.candles:
            candle.update(dt, self.time)
        self.confetti = [p for p in self.confetti if not p.dead]
        for particle in self.confetti:
            particle.update(dt)

        # Text fade
        if self.time > 4:
            self.text_alpha = min(255, self.text_alpha + 150 * dt)

    def draw(self, screen):
        screen.fill((15, 15, 35))

        # Kuchen
        for layer in self.cake_layers:
            layer.draw(screen)

        # Kerzen
        for candle in self.candles:
            candle.draw(screen)

        # Konfetti
        for particle in self.confetti:
            particle.draw(screen)

        # Text
        if self.text_alpha > 0:
            text_surf = self.font.render("Alles Gute zum Geburtstag!", True, (255, 255, 220))
            text_surf.set_alpha(int(self.text_alpha))
            tw, th = text_surf.get_size()
            screen.blit(text_surf, (400 - tw // 2, 150))

        # Info
        info = self.small_font.render("ESC Beenden | OO-Klassen | Auto 12s", True, (200, 200, 255))
        screen.blit(info, (10, 570))


# Hauptprogramm
scene = BirthdayScene()
running = True
while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False

    scene.update(dt)
    scene.draw(screen)
    pygame.display.flip()

    if scene.time > 12:
        running = False

pygame.quit()
