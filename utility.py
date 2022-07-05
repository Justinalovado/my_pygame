from math import acos, sqrt
import pygame
# file containing utility classes
# does not need to be implemented
  
class State:
    def __init__(self, cooldown=0, duration=1) -> None:
        self.cooldown = cooldown
        self.duration = duration
        self.cool_counter = 0
        self.active_counter = 0
    def is_active(self):
        return self.active_counter > 0
    def is_cooldown(self):
        return self.cool_counter > 0 
    def update(self):
        if self.cool_counter and self.active_counter:
            print("Error on Count class")
        if self.cool_counter:
            self.cool_counter -= 1
        if self.active_counter>1:
            self.active_counter -= 1
        elif self.active_counter == 1:
            self.active_counter -= 1
            self.cool_counter = self.cooldown
    def activate(self):
        if not self.is_active and not self.is_cooldown:
            self.active_counter = self.duration
    def reset(self):
        self.cool_counter = 0
        self.active_counter = 0

class Point:
    def __init__(self, tup = None, x=0, y=0) -> None:
        if tup:
            self.x, self.y = tup[0], tup[1]
        else:
            self.x, self.y = x, y

    # move point to (x, y)
    def move_to(self, point=None, targetX=0, targetY=0):
        if point:
            self.x, self.y = point.x, point.y
        else:
            self.x, self.y = targetX, targetY
        return self
    # move point by offsets (x_offset, y_offset)
    def move_by(self, vector = None, x_offset=0, y_offset=0):
        if vector:
            self.x += vector.x
            self.y += vector.y
        else:
            self.x += x_offset
            self.y += y_offset
        return self
    
    def copy(self): return Point(self.x, self.y)

    # calculate straight to the point, targetX, targetY for alternative input
    # if nothing is inputted, return distance to (0,0)
    def distance_to(self, point=None, targetX=0, targetY=0):
        if point:
            return sqrt((point.x - self.x)**2 + (point.y - self.y)**2)
        return sqrt((targetX - self.x)**2 + (targetY - self.y)**2)

    def angle_to(self, point=None, targetX=0, targetY=0, zero_vector='right'):
        def mod(vec):
            return sqrt(vec[0]**2 + vec[1]**2)
        def dot(a, b):
            ans = a[0]*b[0] + a[1]*b[1]
        vA = {
            'up': [0, 1],
            'right': [1, 0],
            'down': [0, -1],
            'left': [-1, 0]
        }[zero_vector]
        t = [point.x, point.y] if point else [targetX, targetY]
        vB = [t[0] - self.x, t[1] - self.y]
        return acos(dot(vA, vB)/(mod(vA)*mod(vB)))
        
class Body:
    def __init__(self,topLeftX, topLeftY, width, height, img) -> None:
        self.hitbox = pygame.Rect(topLeftX, topLeftY, width=width, height=height)
        self.width, self.height = width, height
        self.img = img
    # return point 
    def topLeft(self):
        return Point(self.hitbox.topleft)
    def top(self):
        return Point(self.hitbox.midtop)
    def topRight(self):
        return Point(self.hitbox.topright)
    def Left(self):
        return Point(self.hitbox.midleft)
    def center(self):
        return Point(self.hitbox.center)
    def Right(self):
        return Point(self.hitbox.midright)
    def bottomLeft(self):
        return Point(self.hitbox.bottomleft)
    def bottom(self):
        return Point(self.hitbox.midbottom)
    def bottomRight(self):
        return Point(self.hitbox.bottomright)

    def move_by(self, x, y):
        self.hitbox.move_ip(x, y)
    def move_to(self, x, y):
        self.update(x, y, self.width, self.height)