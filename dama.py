import enum
from turtle import pos


board = [['  ' for i in range(8)] for i in range(8)]
cannot_continue = True
player_option={}
player_playing = 1
aux_right = None
aux_left = None


def initial_position(player_choice):
    other_option = "PB" if player_choice == "PP" else "PP"

    for idx_line,line in enumerate(board):
        for idx_column,column in enumerate(line):
            if idx_line < 3:
                if idx_line % 2 == 0 and idx_column % 2 == 0:
                    column = other_option
                    board[idx_line][idx_column] = column

                if idx_line %2 != 0 and idx_column % 2 != 0:
                    column = other_option
                    board[idx_line][idx_column] = column
            
            if idx_line > 4:
                if idx_line % 2 == 0 and idx_column % 2 == 0:
                    column = player_choice
                    board[idx_line][idx_column] = column

                if idx_line %2 != 0 and idx_column % 2 != 0:
                    column = player_choice
                    board[idx_line][idx_column] = column
            

def get_player_option():
    global player_option

    while True:
        vs_option = input("Digite 1 para jogar contra a máquina e 2 para jogar contra outro jogador: ")
        piece_option = input("Digite PB para começar com peças brancas ou PP para começar com peças pretas: ")

        if vs_option not in ["1", "2"]:
            print("Opção de adversário invalida!")
        elif piece_option not in ["PB", "PP"]:
            print("Opção de peça invalida!")
        else:
            player_option["vs_option"] = vs_option
            player_option["piece_option"] = piece_option
            break
        
    return player_option


def print_board():
    score_pb,score_pp = get_number_pieces_board()
    print("--------------------------")
    print("  A  B  C  D  E  F  G  H")
    
    for idx_line,line in enumerate(board):
        for idx_column,column in enumerate(line):
            if idx_column == 0:
                print(str(idx_line)+"|"+column, end = "|")
            elif idx_column == 7:
                print(column+"|")
            else:
                print(column, end = "|")
                
    print("--------------------------")
    print("Peças Pretas em Jogo: " + str(score_pb))
    print("Peças Brancas em Jogo: " + str(score_pp))
    print("--------------------------")


def get_number_pieces_board():
    score_pb = 0
    score_pp = 0

    for y in board:
        for x in y:
            if x == 'PB':
                score_pb = score_pb+1
            if x == 'PP':
                score_pp = score_pp+1

    return score_pb,score_pp

def move_piece():
    origin_pos,target_pos = get_positions()
    
    piece = board[origin_pos[0]][origin_pos[1]]
    board[origin_pos[0]][origin_pos[1]] = '  '
    board[target_pos[0]][target_pos[1]] = piece
    eat_piece(origin_pos,target_pos)
    print_board()

def eat_piece(origin_pos, target_pos):
    pos_to_eat_y = int((target_pos[0] + origin_pos[0]) / 2)
    pos_to_eat_x = int((target_pos[1] + origin_pos[1]) / 2)
    if pos_to_eat_y != target_pos[0] and pos_to_eat_x != target_pos[1]:
        aux_y = int(pos_to_eat_y)
        aux_x = int(pos_to_eat_x)
        board[aux_y][aux_x] = '  '

def get_positions():
    global cannot_continue
    
    while cannot_continue:
        origin_pos = get_positions_index(input("Digite a posição da peça que deseja movimentar (Ex: 1A) : "))
        verify_chosen_positions(origin_pos)
        verify_piece_owner(origin_pos)
        possible_moves = get_possible_moves(origin_pos)
            
    cannot_continue = True
    print("Possiveis movimentos -> ", get_positions_formated(possible_moves))
    while cannot_continue:    
        target_pos = get_positions_index(input("Digite a posição para onde deseja movimentar (Ex: 1A) : "))
        verify_chosen_positions(target_pos)
        verify_possibles_moves(possible_moves, target_pos)
        
    cannot_continue = True
        
    return origin_pos, target_pos


def verify_chosen_positions(positions):
    global cannot_continue

    for pos in positions:
        if pos <= 7:
            cannot_continue = False
        else:
            cannot_continue = True
            print("Erro! Verifique as posições!")
            break


def verify_piece_owner(origin_pos):
    global cannot_continue
    if cannot_continue != True: 
        y = origin_pos[0]
        x = origin_pos[1]
        
        if player_option["piece_option"] == board[y][x]:
            cannot_continue = False
        else:
            print("Essa peça não é sua!")
            cannot_continue = True


def verify_possibles_moves(possible_moves, target_pos):
    global cannot_continue

    for pos in possible_moves:
        if pos == target_pos and pos != None:
            cannot_continue= False
            break
        else:
            cannot_continue = True

    if cannot_continue:
        print("Não é possivel mover para essa posição")


def get_possible_moves(origin_pos):
    global cannot_continue

    if cannot_continue != True:
        y = origin_pos[0]
        x = origin_pos[1]

        if player_playing == 1:
            pos_right = verify_position_ocupation(y-1,x+1,x)
            pos_left = verify_position_ocupation(y-1,x-1,x)
        elif player_playing == 2:
            pos_right = verify_position_ocupation(y+1,x+1,x)
            pos_left = verify_position_ocupation(y+1,x-1,x)

        if x == 0 and y > 0:
            if pos_right == None:
                print("Essa peça não pode se mover agora!")
                cannot_continue = True
                return None
            return [pos_right]
        elif x == 7 and y > 0:
            if pos_left == None:
                print("Essa peça não pode se mover agora!")
                cannot_continue = True
                return None
            return [pos_left]
        elif y > 0:
            if pos_right == None and pos_left == None:
                print("Essa peça não pode se mover agora!")
                cannot_continue = True
                return None
            if pos_right == None:
                return [pos_left]
            if pos_left == None:
                return [pos_right]
            return [pos_left, pos_right]
        else:
            print("Essa peça não pode se mover agora!")
            cannot_continue = True
            return None


def get_possible_ahead_moves(origin_pos):
    global cannot_continue
    global aux_right
    global aux_left

    if cannot_continue != True:
        y = origin_pos[0]
        x = origin_pos[1]

        if player_playing == 1:
            right = verify_position_ocupation(y-1,x+1,x)
            left = verify_position_ocupation(y-1,x-1,x)
        elif player_playing == 2:
            right = verify_position_ocupation(y+1,x+1,x)
            left = verify_position_ocupation(y+1,x-1,x)

        aux_right = right
        aux_left = left

        if aux_right != None and aux_left != None:
            return [aux_left,aux_right]
        elif aux_right != None:
            return aux_right
        elif aux_left != None:
            return aux_left


def verify_position_ocupation(y,x,x_origin):
    if y > 7 or y < 0:
        return None
    if x > 7 or x < 0:
        return None
    if board[y][x] == '  ':
        return [y,x]
    elif board[y][x] != player_option["piece_option"]:
        value = [y,x]
        positions = get_possible_ahead_moves(value)
        if positions != None:
            if isinstance(positions[0], list):
                for pos in positions:
                    if pos[1] != x_origin:
                        return pos
            if positions[1] != x_origin:
                return positions
        else:
            return None
            
    else:
        return None


def get_positions_index(input_position):
    y = switch_positions_y(input_position[0])
    x = switch_positions_x(input_position[1])
    
    return [int(y),int(x)]


def get_positions_formated(positions):
    formated_positions = []
    if None in positions:
        return formated_positions

    for pos in positions:
        x = switch_positions_letters(pos[1])
        new_pos = [pos[0],x]
        formated_positions.append(str(new_pos[0])+str(new_pos[1]))
    return formated_positions


def switch_positions_x(position):
    positions = {
        'A': 0,
        'B': 1,
        'C': 2,
        'D': 3,
        'E': 4,
        'F': 5,
        'G': 6,
        'H': 7,
    }
    return positions.get(position, 8)
    

def switch_positions_y(position):
    positions = {
        '0': 0,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7,
    }
    return positions.get(position, 8)


def switch_positions_letters(position):
    positions = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'D',
        4: 'E',
        5: 'F',
        6: 'G',
        7: 'H',
    }
    return positions.get(position, 8)


def start_shift():
    global player_playing
    options = ["PB", "PP"]
    original_player_option = player_option["piece_option"]
    while True:
        print(f"Player {player_playing} faça sua jogada")
        print("-----------------------------------------")

        if player_playing == 1:
            player_option["piece_option"] = original_player_option
            move_piece()
        elif player_playing == 2:
            player_option["piece_option"] = options[0] if original_player_option == options[1] else options[1]
            move_piece()
        
        if player_playing == 1:
            player_playing += 1
        else:
            player_playing -=1


def main():
    player_otion = get_player_option()
    print(player_otion)
    initial_position(player_otion["piece_option"])
    print_board()
    
    if '2' in player_option["vs_option"]:
        start_shift()


main()
