import pygame
import socket

HOST = '192.168.178.129'
PORT = 5555
player_img = pygame.image.load("spaceship/R.png")
player_width, player_height = 50, 50
player_img = pygame.transform.scale(player_img, (player_width, player_height))


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

pygame.init()

width, height = 500, 500
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

player_x, player_y = 250, 250
player_width, player_height = 50, 50
player_color = (0, 255, 0)
player_vel = 20

clock = pygame.time.Clock()


def send_movement(key):
    message = f"MOVE:{key}"
    client.send(message.encode())


def redraw_window(x, y):
    win.fill((255, 255, 255))
    win.blit(player_img, (x,y))
    pygame.display.update()

def main():
    run = True
    global player_x, player_y
    while run:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if player_y - player_vel > 0:
                        player_y -= player_vel
                        send_movement("UP")
                elif event.key == pygame.K_DOWN:
                    if player_y + player_vel < height - player_height:
                        player_y += player_vel
                        send_movement("DOWN")
                elif event.key == pygame.K_LEFT:
                    if player_x - player_vel > 0:
                        player_x -= player_vel
                        send_movement("LEFT")
                elif event.key == pygame.K_RIGHT:
                    if player_x + player_vel < width - player_width:
                        player_x += player_vel
                        send_movement("RIGHT")
                elif event.key == pygame.K_SPACE:
                    player_x += player_vel
                    send_movement("SPACE")

        redraw_window(player_x, player_y)

    client.close()


if __name__ == "__main__":
    main()
