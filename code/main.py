import time
from UI import *
import pygame
from GameEngine import * 
from Info import *
from minmax import *
# from game import *
import sys

pygame.init()
pygame.display.set_caption('BYTE')
screen = pygame.display.set_mode((WIDTH, HEIGHT))

Field = CreateMatrix(DIM, DIM)
clock = pygame.time.Clock()


def mainLoop():
    size = chose_table_dim()
    # pocetni igrac
    racunar = ai_play()
    starting_player = chose_player()

    num_stack_x = 0
    num_stack_y = 0
    x = 0
    y = 0
    z = 0
    move = ""
    
    while not pygame.event.get(pygame.QUIT):
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        tabla(screen)
        pygame.display.update()
        print("Na potezu je igrac: ", starting_player)
        potez = True if starting_player =='X' else False

        if starting_player == 'X' or (starting_player == 'O' and not racunar):
            if len(operator(stack_dictionary, starting_player)) == 0:
                print("Nemate potez koji mozete da odigrate! Potez se prepusta protivniku!")
                starting_player = change_player(starting_player)
            else:
                x, y, z, move = move_with_input(x, y, z, move)
                if check_move(stack_dictionary, x, y, z, move, starting_player):
                    odigraj_potez(x, y, z, move)
                    tabla(screen)
                    pygame.display.update()
                    print("Igrac: ", starting_player, " je zavrsio potez!")
                    num_stack_x, num_stack_y = look_for_stacks(stack_dictionary, num_stack_x, num_stack_y)
                    if game_over(num_stack_x, num_stack_y):
                        if num_stack_x > num_stack_y:
                            print("Game Over! Pobednik je igrac: X")
                        else:
                            print("Game Over! Pobednik je igrac: O")
                        pygame.quit()
                        sys.exit()
                    else:
                        starting_player = change_player(starting_player)
                else:
                    print("Nemoguci potez! Igrate opet.")
        elif starting_player == 'O' and racunar:
            print("Racunar je na potezu!")
            start_time = time.time()
            bot_res = min_max(stack_dictionary, 3, potez, starting_player)
            b = bot_res[0] if type(bot_res) is tuple else (0,0)
            if b is None:
                print("Računar nema moguće poteze! Potez se prepušta igraču X.")
                starting_player = change_player(starting_player)
            else:
                odigraj_potez(b[0], b[1], b[2], b[3])
                end_time = time.time()
                execution_time = end_time - start_time  
                #print(execution_time)
                if execution_time < 2.0:
                    time.sleep(2.0 - execution_time)
                
                tabla(screen)
                pygame.display.update()
                print("Racunar je zavrsio potez!")
                num_stack_x, num_stack_y = look_for_stacks(stack_dictionary, num_stack_x, num_stack_y)
                if game_over(num_stack_x, num_stack_y):
                    if num_stack_x > num_stack_y:
                        print("Game Over! Pobednik je igrac: X")
                    else:
                        print("Game Over! Pobednik je igrac: O")
                    pygame.quit()
                    sys.exit()
                else:
                    starting_player = change_player(starting_player)
        pygame.display.update()

        clock.tick(60)

if __name__ == "__main__":
    mainLoop()
    pygame.quit()
    sys.exit()


















