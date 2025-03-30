from pygame import *
from random import randint


win_width = 700
win_height = 500

window = display.set_mode((win_height, win_height))
display.set_caption("Shooter Game")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))


font.init()
font1 = font.SysFont("Arial", 36)

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.005)

fire_play = mixer.Sound("fire.ogg")

FPS = 60
run = True
clock = time.Clock()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, image_x, image_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (image_x, image_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite): 
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

lost = 0
score = 0

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1


monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 420), -40, 60, 60, randint(1, 5))
    monsters.add(monster)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()
        



bullets = sprite.Group() 

ship = Player("rocket.png", 0, 400, 60, 80, 10)
#Bullet = Player("bullet.png", 0, 400, 10)

collides = 0 
win = font1.render("Победа♿", True, (255,215,0))
lose = font1.render("Чмо", True, (255,215,0))

finish = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_play.play()
                ship.fire()
    
    

    if not finish:
        window.blit(background,(0, 0))

        text_lose = font1.render("Ещкереешки:" + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        text_score = font1.render("Парацетамолы:" + str(collides), 1, (255, 255, 255))
        window.blit(text_score, (10, 20))

        ship.update()
        ship.reset()

        monsters.draw(window)
        monsters.update()
        
        bullets.draw(window)
        bullets.update()

        sprite_list = sprite.groupcollide(monsters, bullets, True, True)

        #sprite_loss = sprite.groupcollide(ship, monsters, False)


        for s in sprite_list:
            collides = collides + 1
            monster = Enemy('ufo.png', randint(80, 420), -40, 60, 60, randint(1, 5))
            monsters.add(monster)

        if collides >= 100:
            finish = True
            window.blit(win, (200, 200))

        if lost >= 100:
            finish = True
            window.blit(lose, (200, 200))

            monster = Enemy('ufo.png', randint(80, 420), -40, 60, 60, randint(1, 5))
            monsters.add(monster)
           

       



        display.update()
    clock.tick(FPS)



