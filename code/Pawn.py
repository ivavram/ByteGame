import pygame

outline_color_black = (0, 0, 0)
outline_color_white = (255, 255, 255)

class Pawn:
    def __init__(self, color):
        self.color = color

    
    def draw_pawn(self, surface, coord, radius):
        pygame.draw.circle(surface, self.color, coord, radius)
        if(self.color == (0 , 0, 0)):
            pygame.draw.circle(surface, outline_color_white, coord, radius, 1)
        if(self.color == (255,255,255)):
            pygame.draw.circle(surface, outline_color_black, coord, radius, 1)

    def __repr__(self):
        return str(self.color)
