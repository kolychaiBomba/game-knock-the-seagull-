from random import *

from pygame import *

window = display.set_mode((1000, 700))
display.set_caption('Cтрелялки')

background = transform.scale(image.load('bitch.jpg'), (1000, 700))

clock = time.Clock()
FPS = 70

mixer.init()
mixer.music.load('alarming.mp3')
mixer.music.play()

#класс стрелы
class Strela(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.rotate( transform.scale(image.load(player_image), (75, 75)), 225)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = 'left'
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

strela = sprite.Group()


#класс игрока
class qwerSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.rotate( transform.scale(image.load(player_image), (160, 160)), 295)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = 'left'
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= 5    
        if keys_pressed[K_d] and self.rect.x < 800:
            self.rect.x += 5

    #пуля
    def fire(self):
        strela1 = Strela('strela.png', self.rect.x + 45, self.rect.top, 10)
        strela.add(strela1)

lost = 0

#класс врага
class Enemy(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.rotate( transform.scale(image.load(player_image), (170, 110)), 0)
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.direction = 'left'
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def update(self):
        self.rect.x += self.speed
        global lost
        if self.rect.x > 1000:
            self.rect.y = randint(0,  300)
            lost += 1
            self.rect.x = 0

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('gull.png', -100, randint(0, 300), randint(2, 5))
    monsters.add(monster)
sprite1 = qwerSprite('bow.png', 500, 580, 2)
game = True

font.init()
font1 = font.SysFont('microsoftjhengheimicrosoftjhengheiuilight', 36)
#print(font.get_fonts())
font2 = font.SysFont('microsoftjhengheimicrosoftjhengheiuilight', 60)
number = 0



while game:
    window.blit(background,(0, 0))
    sprite1.update()
    monsters.update()
    monsters.draw(window)
    strela.update()
    strela.draw(window)
    sprite1.reset()
    sprites_list = sprite.groupcollide(monsters, strela, True, True)
    for i in sprites_list:
        number += 1 
        monster = Enemy('gull.png', -100, randint(0, 300), randint(2, 5))
    monsters.add(monster)
    text_lose = font1.render('Пропущено:' + str(lost), 1,(67, 107, 196))
    text_numder = font1.render('Счет:' + str(number), 1,(67, 107, 196))
    window.blit(text_lose,(5, 5))
    window.blit(text_numder,(5, 50))
    for i in event.get():
        if i.type == QUIT:
            game = False
        elif i.type == KEYDOWN:
            if i.key ==K_SPACE:
                sprite1.fire()
    if number > 30:
        window.blit(background,(0, 0))
        text_win = font2.render('Победа!!!', 1, (230, 191, 0))
        window.blit(text_win,(400, 300))
    if lost > 10:
        window.blit(background,(0, 0))
        text_lost = font2.render('Проиграл...', 1, (22, 34, 46))
        window.blit(text_lost,(400, 300))
    display.update()
    clock.tick(FPS)
