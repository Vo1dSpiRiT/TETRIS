import pygame
from pygame.math import Vector2


class Piece:
    def __init__(self, surface, x, y, width, color, shape, gridPosition):
        self.surface = surface
        self.position = Vector2(x, y)
        self.width = width
        self.color = color
        self.shape = shape
        self.gridPosition = gridPosition
        self.rects = self.getRects()
        
    def draw(self):
        for rect in self.rects:
            if rect.y + self.width > self.gridPosition.y:
                pygame.draw.rect(self.surface, self.color, rect)
            
    def update(self):
        self.rects = self.getRects()

    def getRects(self):
        rects = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    rects.append(pygame.Rect(int(self.gridPosition.x + (self.position.x + j) * self.width),
                                             int(self.gridPosition.y + (self.position.y + i) * self.width),
                                             self.width, self.width))
        return rects
    
    def getRectPositions(self):
        positions = []
        for i in range(len(self.shape)):
            for j in range(len(self.shape[i])):
                if self.shape[i][j] == 1:
                    positions.append(Vector2(self.position.x + j, self.position.y + i))
                    
        return positions
        
    def move(self, offsetX, offsetY):
        self.position += Vector2(offsetX, offsetY)
        
    def rotateShape(self):
        self.shape = [[self.shape[j][i] for j in range(len(self.shape))] for i in range(len(self.shape[0])-1,-1,-1)]


