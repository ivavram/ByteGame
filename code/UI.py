import pygame
from Info import *
from Pawn import * 


DIM = 8
WIDTH = DIM * 70
HEIGHT = DIM * 70
SQSIZE = WIDTH // DIM
FIGURE_NUM = (DIM - 2) * (DIM // 2)
STACK_NUM = FIGURE_NUM // DIM

pawn_black = Pawn((0, 0, 0))
pawn_white = Pawn((255, 255, 255))
stack_dictionary = {}
'''stack_dictionary = {
    (0, 0): [],
    (0, 2): [],
    (0, 4): [],
    (0, 6): [],
    (1, 1): [],
    (1, 3): [],
    (1, 5): [(255, 255, 255)],
    (1, 7): [],
    (2, 0): [],
    (2, 2): [],
    (2, 4): [],
    (2, 6): [(255, 255, 255),(0, 0, 0),(255, 255, 255),(255, 255, 255),(0, 0, 0),(255, 255, 255),(255, 255, 255)],
    (3, 1): [(0, 0, 0),(255, 255, 255)],
    (3, 3): [(0, 0, 0)],
    (3, 5): [],
    (3, 7): [],
    (4, 0): [],
    (4, 2): [(255, 255, 255),(255, 255, 255), (0, 0, 0)],
    (4, 4): [],
    (4, 6): [],
    (5, 1): [], 
    (5, 3): [],
    (5, 5): [],
    (5, 7): [],
    (6, 0): [],
    (6, 2): [],
    (6, 4): [(255, 255, 255), (0, 0, 0), (255, 255, 255), (255, 255, 255), (0, 0, 0)],
    (6, 6): [],
    (7, 1): [],
    (7, 3): [],
    (7, 5): [],
    (7, 7): []
}'''

# stek pocetnog stanja
def pocetno_stanje():
    for row in range(DIM):
        for col in range (DIM):
            if (row + col) % 2 == 0:
                stack_dictionary[(row, col)] = []
            if row % 2 != 0 and row != 0 and row != DIM - 1 and col % 2 != 0:
                stack_dictionary[(row, col)].append((0,0,0))
            elif row % 2 == 0 and row != 0 and row != DIM - 1 and col % 2 == 0:
                stack_dictionary[(row, col)].append((255, 255, 255))
    return stack_dictionary

stack_dictionary = pocetno_stanje()

# prikaz table
def tabla(surface):
    black = (0, 0, 0)
    gray = (153, 153, 153)
    white = (247, 212, 212)
    for row in range(DIM):
        for col in range (DIM):
            if (row + col) % 2 == 0:
                color = gray
            else:
                color = white
            rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)                             
            pygame.draw.rect(surface, color, rect)

            font_label = pygame.font.SysFont('Segoe UI', 13) #font za numeraciju

            #brojevi
            lbl_row = font_label.render(str(col + 1), 1, black)
            lbl_pos_row = (col * SQSIZE + SQSIZE - 10, 2)
            # blit
            surface.blit(lbl_row, lbl_pos_row)


            #slova
            lbl_col = font_label.render(get_alphacol(row), 1, black)
            lbl_pos_col = (2, 2 + row * SQSIZE)  # Podešavanje položaja
            surface.blit(lbl_col, lbl_pos_col)  # Blitovanje na površinu
            
            #figure
            if row % 2 != 0  and row != DIM  and col % 2 != 0:
                y = row * SQSIZE + SQSIZE // 2
                for color_tuple in stack_dictionary[(row, col)]:
                    pawn = Pawn(color_tuple)
                    pawn.draw_pawn(surface, (col * SQSIZE + SQSIZE // 2, y), SQSIZE // 4)
                    y -= 7
            elif row % 2 == 0 and row != DIM  and col % 2 == 0:
                y = row * SQSIZE + SQSIZE // 2
                for color_tuple in stack_dictionary[(row, col)]:
                    pawn = Pawn(color_tuple)
                    pawn.draw_pawn(surface, (col * SQSIZE + SQSIZE // 2, y), SQSIZE // 4)
                    y -= 7   


def get_alphacol(row):
    ALPHACOLS = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T', 20: 'U'}
    return ALPHACOLS[row]


