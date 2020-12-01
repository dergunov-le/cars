import pygame as pg
import random
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
try:
    with open('record.txt', 'x') as f:
        f.write(str(0))
except BaseException:
    pass

SIZE = WIDTH, HEIGHT = 800, 600
GREY = (128, 128, 128)
GREEN = (0, 128, 0)
WHITE = (200, 200, 200)
block = False
block2 = False
car_accident = 0
scr1 = True
rgb = [0, 250, 0]
level = 40
count = [0]

pg.init()
pg.display.set_caption('Rally')
screen = pg.display.set_mode(SIZE)

FPS = 120
clock = pg.time.Clock()

cars = [pg.image.load('Image/car1.png'), pg.image.load('Image/car2.png'),
        pg.image.load('Image/car3.png')]
sound_car_accident = pg.mixer.Sound('Image/udar.wav')
sound_canister = pg.mixer.Sound('Image/canister.wav')
font = pg.font.Font(None, 32)
button_start = pg.image.load('Image/start_button.png')
button_start_rect = button_start.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
button_stop = pg.image.load('Image/stop_button.png')
button_stop_rect = button_stop.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))

fuel_image = pg.image.load('Image/fuel.png')
canister_image = pg.image.load('Image/canister.png')
water_image = pg.image.load('Image/water.png')

user_event = pg.USEREVENT + 1
pg.time.set_timer(user_event, random.randrange(7000, 27001, 5000))


class Player(pg.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pg.image.load('Image/car4.png')
        self.orig_image = self.image
        self.angle = 0
        self.speed = 2
        self.acceleration = 0.02
        self.x, self.y = WIDTH // 2, HEIGHT // 2
        self.rect = self.image.get_rect()
        self.position = pg.math.Vector2(self.x, self.y)
        self.velocity = pg.math.Vector2()

    def update(self):
        self.image = pg.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.position += self.velocity
        self.rect.center = int(self.position.x), int(self.position.y)

        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            self.velocity.x = self.speed
            self.angle -= 1
            if self.angle < -25:
                self.angle = -25
        elif keys[pg.K_LEFT]:
            self.velocity.x = -self.speed
            self.angle += 1
            if self.angle > 25:
                self.angle = 25
        else:
            self.velocity.x = 0
            if self.angle < 0:
                self.angle += 1
            elif self.angle > 0:
                self.angle -= 1
        if keys[pg.K_UP]:
            self.velocity.y -= self.acceleration
            if self.velocity.y < -self.speed:
                self.velocity.y = -self.speed
        elif keys[pg.K_DOWN]:
            self.velocity.y += self.acceleration
            if self.velocity.y > self.speed:
                self.velocity.y = self.speed
        else:
            if self.velocity.y < 0:
                self.velocity.y += self.acceleration
                if self.velocity.y > 0:
                    self.velocity.y = 0
            elif self.velocity.y > 0:
                self.velocity.y -= self.acceleration
                if self.velocity.y < 0:
                    self.velocity.y = 0


class Car(pg.sprite.Sprite):
    def __init__(self, x, y, img):
        pg.sprite.Sprite.__init__(self)

        if img == fuel_image:
            self.image = img
            self.speed = 0
        elif img == canister_image:
            self.image = img
            self.speed = 1
        else:
            self.image = pg.transform.flip(img, False, True)
            self.speed = random.randint(2, 3)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            if self == canister:
                self.kill()
            else:
                count[0] += 1
                list_x.remove(self.rect.centerx)
                while True:
                    self.rect.centerx = random.randrange(80, WIDTH, 80)
                    if self.rect.centerx in list_x:
                        continue
                    else:
                        list_x.append(self.rect.centerx)
                        self.speed = random.randint(2, 3)
                        self.rect.bottom = 0
                        break


class Road(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.Surface(screen.get_size())
        self.image.fill(GREY)
        pg.draw.line(self.image, GREEN, (20, 0), (20, 600), 40)
        pg.draw.line(self.image, GREEN, (780, 0), (780, 600), 40)
        for xx in range(10):
            for yy in range(10):
                pg.draw.line(
                    self.image, WHITE,
                    (40 + xx * 80, 0 if xx == 0 or xx == 9 else 10 + yy * 60),
                    (40 + xx * 80, 600 if xx == 0 or xx == 9 else 50 + yy * 60), 5)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 1

    def update(self):
        self.rect.y += self.speed
        if self.rect.top >= HEIGHT:
            self.rect.bottom = 0


all_sprite = pg.sprite.Group()
cars_group = pg.sprite.Group()
canister_group = pg.sprite.Group()

for r in range(2):
    all_sprite.add(Road(0, 0 if r == 0 else -HEIGHT))
player = Player()

list_x = []
n = 0
while n < 6:
    x = random.randrange(80, WIDTH, 80)
    if x in list_x:
        continue
    else:
        list_x.append(x)
        cars_group.add(Car(x, -cars[0].get_height(), random.choice(cars)))
        n += 1

fuel = Car(720, 40, fuel_image)
canister = Car(0, 0, canister_image)
water = Car(0, 0, water_image)
all_sprite.add(cars_group, player, fuel)


def screen1():
    sc = pg.Surface(screen.get_size())
    sc.fill(pg.Color('navy'))
    sc.blit(button_start, button_start_rect)
    sc.blit(button_stop, button_stop_rect)
    screen.blit(sc, (0, 0))


game = True
while game:
    for e in pg.event.get():
        if e.type == pg.QUIT:
            game = False
        elif e.type == pg.MOUSEBUTTONDOWN:
            if e.button == 1:
                if button_start_rect.collidepoint(e.pos):
                    scr1 = False
                    level = 40
                    count[0] = 0
                elif button_stop_rect.collidepoint(e.pos):
                    game = False
        elif e.type == user_event:
            canister_group.add(canister)
            all_sprite.add(canister)
            canister.rect.center = \
                random.randrange(80, WIDTH, 80), -canister.rect.h
            pg.time.set_timer(user_event, random.randrange(7000, 27001, 5000))

    if pg.sprite.spritecollideany(player, cars_group):
        if not block:
            player.position.x += 50 * random.randrange(-1, 2, 2)
            player.angle = 50 * random.randrange(-1, 2, 2)
            sound_car_accident.play()
            car_accident += 1
            block = True
    else:
        block = False

    if pg.sprite.spritecollide(player, canister_group, True):
        level = 40
        sound_canister.play()

    if pg.sprite.spritecollide(player, canister_group, True):
        level = 40
        sound_canister.play()

    if pg.sprite.spritecollideany(player, water_group):
        if not block2:
            player.angle = random.randint(60, 90) * random.randrange(-1, 2, 2)
            block2 = True
    else:
        block2 = False

    if scr1:
        screen1()
    else:
        level -= 0.01
        if level <= 0 or car_accident > 9:
            scr1 = True
        elif level <= 10:
            rgb[:2] = 250, 0
        elif level <= 20:
            rgb[0] = 250
        else:
            rgb[:2] = 0, 250

        all_sprite.update()
        all_sprite.draw(screen)
        pg.draw.rect(
            screen, rgb,
            (fuel.rect.left + 10, fuel.rect.bottom - level - 8, 21, level))
        screen.blit(font.render(f'аварий: {car_accident}', 1, GREEN), (45, 10))

    pg.display.update()
    clock.tick(FPS)
    pg.display.set_caption(f'Rally   FPS: {int(clock.get_fps())}')

# pg.image.save(screen, 'road.jpg')
