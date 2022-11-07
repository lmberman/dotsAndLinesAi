import pygame


class Dot(object):
    indexX = 0
    indexY = 0
    width = 4
    locationX = 0
    locationX = 0

    def __init__(self, indexX, indexY):
        self.indexX = indexX
        self.indexY = indexY

    def set_location(self, x, y):
        self.locationX = x
        self.locationY = y

