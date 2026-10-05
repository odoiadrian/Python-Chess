import pygame

class MyImage:
    def __init__(self, image, x, y):
        self.image = image
        self.rect = image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def move_ip(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy