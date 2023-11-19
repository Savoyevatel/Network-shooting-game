import pygame
import sys
from network import Network

filename = "spaceship/R.png"
white = (255, 255, 255)
green = (0, 255, 0)
red = (255, 0, 0)
yellow = (255, 255, 0)

class Bullet:
    def __init__(self, startx, starty):
        self.x = startx
        self.y = starty
        self.velocity = 5
        self.damage = 1
        self.image = pygame.image.load(spaceship/bullet.png")
        self.image = pygame.transform.scale(self.image, (10, 10))  # Adjust size as needed

    def move(self):
        self.y -= self.velocity

    def draw(self, g):
        g.blit(self.image, (self.x, self.y))


class Player:
    width = height = 50

    def __init__(self, startx, starty, canvas, multi):
        self.x = startx
        self.y = starty
        self.multi = multi
        self.max_health = 100
        self.health = self.max_health
        self.health_percentage = 1.0
        self.velocity = 2
        self.image = pygame.image.load(filename)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        if multi == 2:
            self.image = pygame.transform.rotate(self.image, 180)
        self.bullets = []
        self.canvas = canvas

    def draw(self, g):
        g.blit(self.image, (self.x, self.y))

    def move(self, dirn):
        if dirn == 0:
            self.x += self.velocity
        elif dirn == 1:
            self.x -= self.velocity
        elif dirn == 2:
            self.y -= self.velocity
        else:
            self.y += self.velocity

    def get_hurt(self, damage):
        # Decrease player's health
        self.health -= damage  # Adjust the amount based on your requirements
        if self.health <= 0:
            self.health = 0
        self.health_percentage = self.health/self.max_health

    def shoot(self):
        bullet = Bullet(self.x + self.width // 2, self.y)
        self.bullets.append(bullet)

    def move_bullets(self):
        for bullet in self.bullets:
            bullet.move()
            if bullet.y < 0:
                self.bullets.remove(bullet)

    def draw_bullets(self, g):
        for bullet in self.bullets:
            bullet.draw(g)

    def get_health_percentage(self):
        max_health = 100
        current_health = 80
        return current_health / max_health

    def draw_health_bar(self, surf):
        health_pct = self.get_health_percentage()
        self.canvas.draw_player_health(surf, self.x, self.y - 30, self.health_percentage)


class Game:

    def __init__(self, w, h):
        self.net = Network()
        self.width = w
        self.height = h
        self.canvas = Canvas(self.width, self.height, "Testing...")
        self.player = Player(50, 50, self.canvas,1)
        self.player2 = Player(100, 100, self.canvas,2)


    def run(self):
        clock = pygame.time.Clock()
        run = True
        while run:
            clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.K_ESCAPE:
                    run = False

            keys = pygame.key.get_pressed()

            if keys[pygame.K_RIGHT]:
                if self.player.x <= self.width - self.player.velocity:
                    self.player.move(0)

            if keys[pygame.K_LEFT]:
                if self.player.x >= self.player.velocity:
                    self.player.move(1)

            if keys[pygame.K_UP]:
                if self.player.y >= self.player.velocity:
                    self.player.move(2)

            if keys[pygame.K_DOWN]:
                if self.player.y <= self.height - self.player.velocity:
                    self.player.move(3)

            if keys[pygame.K_SPACE]:
                self.player.shoot()

            for bullet in self.player.bullets:
                bullet.move()
                if bullet.y < 0:
                    self.player.bullets.remove(bullet)
                elif (
                        self.player2.x < bullet.x < self.player2.x + self.player2.width
                        and self.player2.y < bullet.y < self.player2.y + self.player2.height
                ):
                    # Bullet hit player2, decrease player2's health
                    self.player2.get_hurt(bullet.damage)
                    self.player.bullets.remove(bullet)

                # Send Network Stuff
            self.player2.x, self.player2.y = self.parse_data(self.send_data())

            # Update Canvas
            self.canvas.draw_background()
            self.player.draw(self.canvas.get_canvas())
            self.player.draw_bullets(self.canvas.get_canvas())
            self.player.draw_health_bar(self.canvas.get_canvas())
            self.player2.draw(self.canvas.get_canvas())
            self.player2.draw_health_bar(self.canvas.get_canvas())
            self.player2.draw_bullets(self.canvas.get_canvas())

            self.canvas.update()


        pygame.quit()

    def send_data(self):
        data = str(self.net.id) + ":" + str(self.player.x) + "," + str(self.player.y)
        reply = self.net.send(data)
        return reply

    @staticmethod
    def parse_data(data):
        try:
            d = data.split(":")[1].split(",")
            return int(d[0]), int(d[1])
        except:
            return 0,0

class Canvas:
    def __init__(self, w, h, name="None"):
        self.width = w
        self.height = h
        self.screen = pygame.display.set_mode((w, h))
        pygame.display.set_caption(name)

    def draw_player_health(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 20
        fill = pct * BAR_LENGTH
        outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
        if pct > 0.6:
            color = (0, 255, 0)  # Green
        elif pct > 0.3:
            color = (255, 255, 0)  # Yellow
        else:
            color = (255, 0, 0)  # Red
        pygame.draw.rect(surf, color, fill_rect)
        pygame.draw.rect(surf, (255, 255, 255), outline_rect, 2) #white


    @staticmethod
    def update():
        pygame.display.update()

    def draw_text(self, text, size, x, y):
        pygame.font.init()
        font = pygame.font.SysFont("comicsans", size)
        render = font.render(text, 1, (0, 0, 0))

        self.screen.blit(render, (x, y))

    def get_canvas(self):
        return self.screen

    def draw_background(self):
        self.screen.fill((0, 0, 0))


if __name__ == "__main__":
    pygame.init()
    game = Game(1800, 1600)
    game.run()
    sys.exit()
