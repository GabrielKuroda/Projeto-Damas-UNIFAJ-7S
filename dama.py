board = [['  ' for i in range(8)] for i in range(8)]
cannot_continue = True
player_option={}
player_playing = 1
possibles_position = []
mandatory_position = []
pos_to_move = []


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
        piece_option = input("Digite PB para começar com peças brancas ou PP para começar com peças pretas: ").upper()

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
    global player_option
    origin_pos,target_pos = get_positions()
    
    piece = board[origin_pos[0]][origin_pos[1]]
    board[origin_pos[0]][origin_pos[1]] = '  '
    board[target_pos[0]][target_pos[1]] = piece

    if player_playing == 1:
        if player_option["piece_option"] in piece and target_pos[0] == 0:
            piece_list = list(piece)
            piece_list[0] = "D"
            
            p = "".join(piece_list)
            board[target_pos[0]][target_pos[1]] = p
    elif player_playing == 2:
        if player_option["piece_option"] in piece and target_pos[0] == 7:
            piece_list = list(piece)
            piece_list[0] = "D"
            
            p = "".join(piece_list)
            board[target_pos[0]][target_pos[1]] = p

    eat_piece(origin_pos,target_pos)
    print_board()

def eat_piece(origin_pos, target_pos):
    pos_to_eat_y = int((target_pos[0] + origin_pos[0]) / 2)
    pos_to_eat_x = int((target_pos[1] + origin_pos[1]) / 2)
    pos_to_eat = [pos_to_eat_y,pos_to_eat_x]
    if player_playing == 1:
        if pos_to_eat_y != target_pos[0] and pos_to_eat_x != target_pos[1]:
            aux_y = int(pos_to_eat_y)
            aux_x = int(pos_to_eat_x)
            board[aux_y][aux_x] = '  '
            eat_piece(pos_to_eat, target_pos)
            eat_piece(origin_pos, pos_to_eat)
            remove_from_mandatory(target_pos)
    else:
        if pos_to_eat_y != origin_pos[0] and pos_to_eat_x != origin_pos[1]:
            aux_y = int(pos_to_eat_y)
            aux_x = int(pos_to_eat_x)
            board[aux_y][aux_x] = '  '
            eat_piece(pos_to_eat, target_pos)
            eat_piece(origin_pos, pos_to_eat)
            remove_from_mandatory(target_pos)


def remove_from_mandatory(target):
    exists = False
    for pos in mandatory_position:
        if pos == target:
            exists = True
            break
    if exists:
        mandatory_position.remove(target)


def get_positions():
    global cannot_continue
    global pos_to_move
    
    while cannot_continue:
        origin_pos = get_positions_index(input("Digite a posição da peça que deseja movimentar (Ex: 1A) : ").upper())
        verify_chosen_positions(origin_pos)
        verify_piece_owner(origin_pos)
        pos_to_move = origin_pos
        get_moves(origin_pos)
            
    cannot_continue = True
    print(mandatory_position)
    print("Possiveis movimentos -> ", get_positions_formated(possibles_position))
    while cannot_continue:    
        target_pos = get_positions_index(input("Digite a posição para onde deseja movimentar (Ex: 1A) : ").upper())
        verify_chosen_positions(target_pos)
        verify_possibles_moves(target_pos)
    
    eat_piece(origin_pos,target_pos)

    if did_not_choose_mandatory(target_pos):
        print("Você Perdeu")
        
    cannot_continue = True
        
    return origin_pos, target_pos


def did_not_choose_mandatory(target_pos):
    if mandatory_position == []:
        return False
    for pos in mandatory_position:
        if target_pos == pos:
            return False
    return True


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

        piece = board[y][x]
        piece_list = list(piece)
            
        p = "".join(piece_list[1])
        
        if player_option["piece_option"] == board[y][x] or (p in board[y][x] and p in player_option["piece_option"][1]):
            cannot_continue = False
        else:
            print("Essa peça não é sua!")
            cannot_continue = True


def verify_possibles_moves(target_pos):
    global cannot_continue

    for pos in possibles_position:
        if pos == target_pos and pos != None:
            cannot_continue= False
            break
        else:
            cannot_continue = True

    if cannot_continue:
        print("Não é possivel mover para essa posição")


def get_moves(origin_pos):
    global possibles_position
    global mandatory_position

    possibles_position.clear()
    mandatory_position.clear()
    get_possible_moves(origin_pos)


def get_possible_moves(origin_pos):
    global cannot_continue

    if cannot_continue != True:
        y = origin_pos[0]
        x = origin_pos[1]

        if player_playing == 1:
            pos_right = verify_position_in_board(y-1,x+1)
            pos_left = verify_position_in_board(y-1,x-1)
        elif player_playing == 2:
            pos_right = verify_position_in_board(y+1,x+1)
            pos_left = verify_position_in_board(y+1,x-1)

        if pos_left != None and board[pos_left[0]][pos_left[1]] == '  ' and board[y][x] != '  ':
            print("Left -> " + str(pos_left))
            possibles_position.append(pos_left)
        elif pos_left != None and board[pos_left[0]][pos_left[1]] != player_option["piece_option"]  and board[pos_left[0]][pos_left[1]] != '  ':
            get_mandatory_moves(pos_left)

        if pos_right != None and board[pos_right[0]][pos_right[1]] == '  ' and board[y][x] != '  ':
            print("Right -> " + str(pos_right))
            possibles_position.append(pos_right)
        elif pos_right != None and board[pos_right[0]][pos_right[1]] != player_option["piece_option"] and board[pos_right[0]][pos_right[1]] != '  ':
            get_mandatory_moves(pos_right)

        if possibles_position == []:
            print("A peça escolhida não pode se mover agora!")
            cannot_continue = True


def verify_pos(pos):
    if board[pos[0]][pos[1]] == '  ':
        return True
    return False


def get_mandatory_moves(pos):
    global cannot_continue
    global mandatory_position
    global possibles_position

    y = pos[0]
    x = pos[1]

    if player_playing == 1:
        right = verify_position_in_board(y-1,x+1)
        left = verify_position_in_board(y-1,x-1)
    elif player_playing == 2:
        right = verify_position_in_board(y+1,x+1)
        left = verify_position_in_board(y+1,x-1)

    if left != None and left[1] != pos_to_move[1]:
        if verify_pos(left):
            mandatory_position.append(left)
            possibles_position.append(left)
            get_possible_moves(left)

    if right != None and right[1] != pos_to_move[1]:
        if verify_pos(right):
            mandatory_position.append(right)
            possibles_position.append(right)
            get_possible_moves(right)


def verify_position_in_board(y,x):
    if y > 7 or y < 0:
        return None
    if x > 7 or x < 0:
        return None
    else:
        return [y,x]


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
