"""hocam bu final ödevinde çocukken oynadığım dxball oyununu python kullanarak yapmak istedim,
kendimi yeterince gelistirebilirsem oyunu daha da genisletip belki mobil versiyonunu yapabilirim.

not: oyunu bitirdim, bu kadar basit bir oyunun bu kadar vaktimi almasını beklemedim, daha cok sey katacaktım
(patlama ve ses efektleri, poweruplar vb.) simdilik bu kadarının yeterli oldugunu düsünüyorum, sayenizde
pythonda ilk oyunumu yaptım hocam, tesekkürler
"""


import pygame
from pygame.locals import *#bir kac error alıyodum (cözemedim) yardım aldım, ne yaptıgını anlayamadım :D

pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("DxBall: Emre")

#font
font = pygame.font.SysFont('Constantia', 30)

#renkler (renkleri gecen dönem sizden aldıgım dersteki coolors sitesinden aldım, cok kullanıslı oldu)
bg = (234, 218, 184)#arkaplan

block_red = (242, 85, 96)
block_green = (86, 174, 87)
block_blue = (69, 177, 232)

paddle_col = (142, 135, 123)
paddle_outline = (100, 100, 100)
text_col = (78, 81, 139)

#degiskenler
cols = 6
rows = 6
clock = pygame.time.Clock()
fps = 60 #oyun daha soft gözüksün diye böyle bir cözüm buldum internette (kasıyor gibi gözüküyordu)
live_ball = False
game_over = 0


#ekrana text yazdırma
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class wall():
    def __init__(self):
        self.width = screen_width // cols
        self.height = 50

    def create_wall(self):
        self.blocks = []
        block_individual = []
        for row in range(rows):
            block_row = []
            for col in range(cols):
                block_x = col * self.width
                block_y = row * self.height
                rect = pygame.Rect(block_x, block_y, self.width, self.height)
                if row < 2:
                    strength = 3
                elif row < 4:
                    strength = 2
                elif row < 6:
                    strength = 1
                block_individual = [rect, strength]
                block_row.append(block_individual)
            self.blocks.append(block_row)

    def draw_wall(self):
        for row in self.blocks:
            for block in row:
                #blockların dayanıklık atadım, seviyesine göre renk atadım
                if block[1] == 3:
                    block_col = block_blue
                elif block[1] == 2:
                    block_col = block_green
                elif block[1] == 1:
                    block_col = block_red
                pygame.draw.rect(screen, block_col, block[0])
                pygame.draw.rect(screen, bg, (block[0]), 2)

#paddle (cubuk)
class paddle():
    def __init__(self):
        self.reset()

    def move(self):#cubugun hareket etmesi icin (aslında mouse ile hareket ettirecektim ama bir kac bug oldu)
        self.direction = 0
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
            self.direction = -1
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
            self.direction = 1

    def draw(self):
        pygame.draw.rect(screen, paddle_col, self.rect)
        pygame.draw.rect(screen, paddle_outline, self.rect, 3)

    def reset(self):
        self.height = 20
        self.width = int(screen_width / cols)
        self.x = int((screen_width / 2) - (self.width / 2))#ortada baslaması icin
        self.y = screen_height - (self.height * 2)
        self.speed = 10
        self.rect = Rect(self.x, self.y, self.width, self.height)
        self.direction = 0


#top
class game_ball():
    def __init__(self, x, y):
        self.reset(x, y)

    def move(self):

        collision_thresh = 5

        wall_destroyed = 1
        row_count = 0
        for row in wall.blocks:
            item_count = 0
            for item in row:
                if self.rect.colliderect(item[0]):
                    if abs(self.rect.bottom - item[0].top) < collision_thresh and self.speed_y > 0:
                        self.speed_y *= -1
                    if abs(self.rect.top - item[0].bottom) < collision_thresh and self.speed_y < 0:
                        self.speed_y *= -1
                    if abs(self.rect.right - item[0].left) < collision_thresh and self.speed_x > 0:
                        self.speed_x *= -1
                    if abs(self.rect.left - item[0].right) < collision_thresh and self.speed_x < 0:
                        self.speed_x *= -1
                    #top carpınca dayanıklılık azalıyor
                    if wall.blocks[row_count][item_count][1] > 1:
                        wall.blocks[row_count][item_count][1] -= 1
                    else:
                        wall.blocks[row_count][item_count][0] = (0, 0, 0, 0)

                if wall.blocks[row_count][item_count][0] != (0, 0, 0, 0):
                    wall_destroyed = 0
                item_count += 1
            row_count += 1
        if wall_destroyed == 1:
            self.game_over = 1

        if self.rect.left < 0 or self.rect.right > screen_width:
            self.speed_x *= -1

        if self.rect.top < 0:
            self.speed_y *= -1
        if self.rect.bottom > screen_height:
            self.game_over = -1

        if self.rect.colliderect(player_paddle):
            if abs(self.rect.bottom - player_paddle.rect.top) < collision_thresh and self.speed_y > 0:
                self.speed_y *= -1
                self.speed_x += player_paddle.direction
                if self.speed_x > self.speed_max:
                    self.speed_x = self.speed_max
                elif self.speed_x < 0 and self.speed_x < -self.speed_max:
                    self.speed_x = -self.speed_max
            else:
                self.speed_x *= -1

        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        return self.game_over

    def draw(self):
        pygame.draw.circle(screen, paddle_col, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad)
        pygame.draw.circle(screen, paddle_outline, (self.rect.x + self.ball_rad, self.rect.y + self.ball_rad),
                           self.ball_rad, 3)

    def reset(self, x, y):
        self.ball_rad = 10
        self.x = x - self.ball_rad
        self.y = y
        self.rect = Rect(self.x, self.y, self.ball_rad * 2, self.ball_rad * 2)
        self.speed_x = 4
        self.speed_y = -4
        self.speed_max = 5
        self.game_over = 0


wall = wall()
wall.create_wall()

player_paddle = paddle()

ball = game_ball(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)

run = True
while run:#oyunun döngüsü

    clock.tick(fps)

    screen.fill(bg)

    wall.draw_wall()
    player_paddle.draw()
    ball.draw()

    if live_ball:
        player_paddle.move()
        game_over = ball.move()
        if game_over != 0:
            live_ball = False

    if not live_ball:
        if game_over == 0:
            draw_text("BASLAMAK ICIN TIKLA", font, text_col, 100, screen_height // 2 + 100)
        elif game_over == 1:
            draw_text("KAZANDIN!", font, text_col, 240, screen_height // 2 + 50)
            draw_text("TEKRAR BASLAMAK ICIN TIKLA", font, text_col, 100, screen_height // 2 + 100)
        elif game_over == -1:
            draw_text("KAYBETTIN!", font, text_col, 240, screen_height // 2 + 50)
            draw_text("TEKRAR BASLAMAK ICIN TIKLA", font, text_col, 100, screen_height // 2 + 100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and live_ball == False:
            live_ball = True
            ball.reset(player_paddle.x + (player_paddle.width // 2), player_paddle.y - player_paddle.height)
            player_paddle.reset()
            wall.create_wall()

    pygame.display.update()

pygame.quit()
