from random import randint
import pygame
from utility import Animation, State, Vector

pygame.init()
# ATTACKSTATE NEEDS TO BE ADDED
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
SECOND = 60
BULLETSPEED = 1
ATTACKSTATE = 0.5 * SECOND
PLAYER_RELOAD_TIME = 0.5
PROJECTILES_LIMIT = 4 
HOSTILITY_LIST = [
    ['player', 'enemy'],
]
dummy_screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
PLAYER_CENTER = pygame.image.load("img/player/center.png").convert_alpha()
PLAYER_UP = pygame.image.load("img/player/up.png").convert_alpha()
PLAYER_DOWN = pygame.image.load("img/player/down.png").convert_alpha()
PLAYER_RIGHT = pygame.image.load("img/player/right.png").convert_alpha()
PLAYER_LEFT = pygame.image.load("img/player/left.png").convert_alpha()
HEALTH_FONT = pygame.font.Font("font/xeros_karma.ttf", 32)
MASK = pygame.image.load("img/mask.png").convert_alpha()



class Player:
    def __init__(self, x, y) -> None:
        self.name = "player"
        self.img = PLAYER_CENTER
        self.hitbox = pygame.Rect(x, y, self.img.get_width(), self.img.get_height())
        self.health = 50
        self.attack_point = 10
        
        self.bulletVelocity = (1, 1)
        self.remoteVelocity = self.bulletVelocity
        self.invincible = State(cooldown=0, duration=SECOND)
        self.reloading = State(cooldown=0, duration=PLAYER_RELOAD_TIME*SECOND)
        self.mouth_attack_animation = Animation("img/player/", "mouth_attack")
        self.remote_bullet_item = False
        self.velocity = Vector((0, 0))
        self.damping = 0.5
        self.cap_speed = 3
        self.acceleration = 1

    def update(self, keys, enemies, projectiles):
        self.move(keys)
        self.is_taking_melee(enemies)
        self.invincible.update()
        self.reloading.update()
        if keys[pygame.K_k]:
            self.attack(projectiles)
        
        
    def attack(self, projectiles):
        if not self.reloading.is_active() and not self.is_overloaded(projectiles):
            projectiles.append(Bullet(
                self.hitbox.centerx,
                self.hitbox.centery,
                self.attack_point,
                self.bulletVelocity[0], 
                self.bulletVelocity[1],
                self.name
            ))
            self.reloading.activate()
            self.mouth_attack_animation.play(PLAYER_RELOAD_TIME)
                
    def move(self, keys):
        acceleration = Vector((0, 0))
        flag = 1
        if keys[pygame.K_s]:
            # velocity = (velocity[0], self.speed)
            acceleration.add(y=self.acceleration)
            # self.img = PLAYER_DOWN
            flag = 0
            self.remoteVelocity = self.velocity
        if keys[pygame.K_w]:
            # velocity = (velocity[0], -self.speed)
            acceleration.add(y=-self.acceleration)
            # self.img = PLAYER_UP
            flag = 0
            self.remoteVelocity = self.velocity
        if keys[pygame.K_d]:
            # velocity = (self.speed, velocity[1])
            acceleration.add(x=self.acceleration)
            # self.img = PLAYER_RIGHT
            flag = 0
            self.remoteVelocity = self.velocity
        if keys[pygame.K_a]:
            # velocity = (-self.speed, velocity[1])
            acceleration.add(x=-self.acceleration)
            # self.img = PLAYER_LEFT
            flag = 0
            self.remoteVelocity = self.velocity
        # if flag:
            # self.img = PLAYER_CENTER
        if self.velocity != (0, 0) and not self.remote_bullet_item:
            self.bulletVelocity = self.velocity
        self.velocity.add(vector=acceleration)
        self.velocity.damp(self.damping)
        pygame.Rect.move_ip(self.hitbox, self.velocity.x, self.velocity.y)

        if self.is_outbound():
            pygame.Rect.move_ip(self.hitbox, -self.velocity.x, -self.velocity.y)

    def is_outbound(self):
        screen_right = SCREEN_WIDTH - self.hitbox.width
        screen_bottom = SCREEN_HEIGHT - self.hitbox.height
        return True if (self.hitbox.left < 0 or 
                        self.hitbox.left > screen_right or 
                        self.hitbox.top < 0 or 
                        self.hitbox.top > screen_bottom) else False

    def is_taking_melee(self, enemies):
        for enemy in enemies:
            if pygame.Rect.colliderect(self.hitbox, enemy.hitbox):
                self.take_dmg(enemy.attack_point, enemy.name)
                self.invincible.activate()

    def take_dmg(self, dmg, source=None):
        if not self.invincible.is_active():
            self.health -= dmg
            if source:
                print(f"{self.name} took {dmg} dmg from {source}, current health is {self.health}")
            else:
                print(f"{self.name} took eMOtional dmg, current health is {self.health}")
            self.is_invincible = True
            self.invinc_countdown = 60

    def is_dead(self):
        return self.health <= 0
    
    def show(self, screen, show_hitbox=True):
        screen.blit(self.img, (self.hitbox.left, self.hitbox.top))
        if self.invincible.is_active():
            screen.blit(pygame.transform.scale(MASK, (self.hitbox.width, self.hitbox.height)), 
                        (self.hitbox.left, self.hitbox.top))
        if show_hitbox:
            pygame.draw.rect(screen, "lightgreen", self.hitbox, width=1)
        health_txt = HEALTH_FONT.render(str(self.health), True, 'green', None)
        screen.blit(health_txt, (20, 0))
        self.mouth_attack_animation.update(screen, pos=self.hitbox.center)

    def is_overloaded(self, projectiles):
        if not self.remote_bullet_item:
            return False
        if self.remote_bullet_item and len(projectiles) >= PROJECTILES_LIMIT:
            return True
        
        
    
    


class Enemy:
    def __init__(self, x=None, y=None) -> None:
        self.img = pygame.image.load("img/enemy.png").convert_alpha()
        width = self.img.get_width()
        height = self.img.get_height()
        self.hitbox = pygame.Rect(
            x if x != None else randint(0, SCREEN_WIDTH - width),
            y if y != None else randint(0, SCREEN_HEIGHT - height),
            width,
            height
        )
        self.health = 30
        self.velocity = (randint(1, 3), randint(1, 3))
        self.attack_point = 10
        self.name = "enemy"

    def update(self):
        self.move()
        
    def move(self):
        screen_right = SCREEN_WIDTH - self.hitbox.width
        screen_bottom = SCREEN_HEIGHT - self.hitbox.height
        if self.hitbox.left < 0 or self.hitbox.left > screen_right:
            self.velocity = (-self.velocity[0], self.velocity[1])
        if self.hitbox.top < 0 or self.hitbox.top > screen_bottom:
            self.velocity = (self.velocity[0], -self.velocity[1])
        pygame.Rect.move_ip(self.hitbox, self.velocity[0], self.velocity[1])

    def is_outbound(self):
        screen_right = SCREEN_WIDTH - self.hitbox.width
        screen_bottom = SCREEN_HEIGHT - self.hitbox.height
        return True if (self.hitbox.left < 0 or 
                        self.hitbox.left > screen_right or 
                        self.hitbox.top < 0 or 
                        self.hitbox.top > screen_bottom) else False

    def take_dmg(self, dmg, source=None):
        self.health -= dmg
        if source:
            print(f"{self.name} took {dmg} dmg from {source}, current health is {self.health}")
        else:
            print(f"{self.name} took eMOtional dmg, current health is {self.health}")
    def show(self, screen, show_hitbox=True):
        screen.blit(self.img, (self.hitbox.left, self.hitbox.top))
        if show_hitbox:
            pygame.draw.rect(screen, "lightgreen", self.hitbox, width=1)

    def is_dead(self):
        return self.health <= 0

class Bullet:
    def __init__(self, x, y, dmg, vX, vY, source) -> None:
        self.dmg = dmg
        self.velocity = (vX, vY)
        self.speed = BULLETSPEED
        self.img = pygame.image.load("img/bullet.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (10, 10))
        width = self.img.get_width()
        height = self.img.get_height()
        self.hitbox = pygame.Rect(x, y, width, height)
        self.source = source
        self.pierce = 0
        self.dead = False
        

    def update(self, entities):
        self.hitbox.left += self.velocity[0] * self.speed
        self.hitbox.top += self.velocity[1] * self.speed
        self.check_hit(entities)

    
    def is_outbound(self):
        screen_right = SCREEN_WIDTH - self.hitbox.width
        screen_bottom = SCREEN_HEIGHT - self.hitbox.height
        return True if (self.hitbox.left < 0 or 
                        self.hitbox.left > screen_right or 
                        self.hitbox.top < 0 or 
                        self.hitbox.top > screen_bottom) else False

    def show(self, screen, show_hitbox=True):
        screen.blit(self.img, (self.hitbox.left, self.hitbox.top))
        if show_hitbox:
            pygame.draw.rect(screen, "lightgreen", self.hitbox, width=1)
    
    def is_dead(self):
        return self.dead

    def check_hit(self, entities):
        for entity in entities:
            if pygame.Rect.colliderect(self.hitbox, entity.hitbox):
                relation = [self.source, entity.name]
                if relation in HOSTILITY_LIST or relation[::-1] in HOSTILITY_LIST:
                    entity.take_dmg(self.dmg, self.source)
                    if self.pierce > 0:
                        self.pierce -= 1
                    else:
                        self.dead = True
                        