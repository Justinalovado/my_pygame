from random import randint
from turtle import left, screensize
import pygame
# from pyrsistent import T
# ATTACKSTATE NEEDS TO BE ADDED, ENEMY-BULLET HITBOX COLLISION EVENTS HAVE MINOR BUGS (ENEMIES DONT GET DMG EVEN WHEN THEY COLLIDE)
SECOND = 60
BULLETSPEED = 4
ATTACKSTATE = 0.5 * SECOND


class Player:
    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.health = 30
        self.attack_point = 10
        self.speed = 3
        self.img = pygame.image.load("img/man.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.hitbox = self.img.get_rect()
        self.is_invincible = False
        self.invinc_countdown = 0
        self.bullets = []
        self.bulletVelocity = (1, 1)

    def update(self, keys, enemies):
        self.move(keys)
        self.is_taking_melee(enemies)
        if self.invinc_countdown > 0:
            self.invinc_countdown -= 1
        else:
            self.is_invincible = False
        if self.health <= 0:
            self.dead = True
        # updating bullets
        for bullet in self.bullets:
            bullet.update()
        self.bullets = [b for b in self.bullets if not b.is_outbound()]

    def move(self, keys):
        velocity = (0, 0)
        if keys[pygame.K_d]:
            velocity = (self.speed, velocity[1])
        if keys[pygame.K_a]:
            velocity = (-self.speed, velocity[1])
        if keys[pygame.K_s]:
            velocity = (velocity[0], self.speed)
        if keys[pygame.K_w]:
            velocity = (velocity[0], -self.speed)
        if velocity != (0, 0):
            self.bulletVelocity = velocity
        if keys[pygame.K_k]:
            self.bullets.append(
                Bullet(self.x, self.y, self.attack_point,
                       self.bulletVelocity[0], self.bulletVelocity[1]))
        self.x, self.y = self.x + velocity[0], self.y + velocity[1]
        pygame.Rect.move_ip(self.hitbox, velocity[0], velocity[1])
        if self.is_outbound():
            self.x, self.y = self.x - velocity[0], self.y - velocity[1]
            pygame.Rect.move_ip(self.hitbox, -velocity[0], -velocity[1])

    def is_outbound(self):
        screen_right = 1024 - self.width
        screen_bottom = 768 - self.width
        return True if (self.x < 0 or self.x > screen_right or self.y < 0
                        or self.y > screen_bottom) else False

    def is_taking_melee(self, enemies):
        for enemy in enemies:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox):
                self.take_dmg(enemy.attack_point)

    def take_dmg(self, dmg):
        if self.is_invincible == False:
            self.health -= dmg
            print(f"Player took {dmg} dmg, current health is {self.health}")
            self.is_invincible = True
            self.invinc_countdown = 60

    def is_dead(self):
        return True if self.health <= 0 else False

    def show(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def getBullets(self):
        return self.bullets


class Enemy:
    def __init__(self, x=None, y=None) -> None:
        self.img = pygame.image.load("img/enemy.png").convert_alpha()
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        self.x = x if x != None else randint(0, 1024 - self.width)
        self.y = y if y != None else randint(0, 768 - self.width)
        # self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = self.img.get_rect()
        self.health = 100
        self.velocity = (randint(0, 5), randint(0, 5))
        self.attack_point = 10
        self.name = "Enemy"

    def update(self, bullets):
        self.move()
        self.is_taking_range(bullets)

    def move(self):
        self.x, self.y = self.x - self.velocity[0], self.y - self.velocity[1]
        screen_right = 1024 - self.width
        screen_bottom = 768 - self.width
        if self.x < 0 or self.x > screen_right:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if self.y < 0 or self.y > screen_bottom:
            self.velocity = (self.velocity[0], -self.velocity[1])
        self.x, self.y = self.x - self.velocity[0], self.y - self.velocity[1]
        self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)

    def is_outbound(self):
        screen_right = 1024 - self.width
        screen_bottom = 768 - self.width
        return True if (self.x < 0 or self.x > screen_right or self.y < 0
                        or self.y > screen_bottom) else False

    def is_taking_range(self, bullets):
        for bullet in bullets:
            if pygame.Rect.colliderect(self.hitbox, bullet.hitbox):
                self.take_dmg(bullet.dmg)

    def take_dmg(self, dmg):
        self.health -= dmg
        print(f"{self.name} took {dmg} dmg, current health is {self.health}")

    def show(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def is_dead(self):
        return True if self.health <= 0 else False


class Bullet:
    def __init__(self, x, y, dmg, vX, vY) -> None:
        self.x = x
        self.y = y
        self.dmg = dmg
        self.velocity = (vX, vY)
        self.speed = BULLETSPEED
        self.img = pygame.image.load("img/bullet.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (10, 10))
        self.width = self.img.get_width()
        self.height = self.img.get_height()
        # self.hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        self.hitbox = self.img.get_rect()
        

    def update(self):
        self.x += self.velocity[0] * self.speed
        self.y += self.velocity[1] * self.speed

    def is_outbound(self):
        screen_right = 1024
        screen_bottom = 768
        return True if (self.x < 0 or self.x > screen_right or self.y < 0
                        or self.y > screen_bottom) else False

    def show(self, screen):
        screen.blit(self.img, (self.x, self.y))
