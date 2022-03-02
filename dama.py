board = [['  ' for i in range(8)] for i in range(8)]
cannot_continue = True
player_option={}
player_playing = 1
possibles_position = []
mandatory_position = []
pos_to_move = []
number_pos = {}
all_mandatory = {}
jump_pieces = []
passed_history = {}
path_to_eat= []
will_eat = False
end_path = False
number_pos_origin_pos = {}
madatory_pos_origin_pos = []


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

    if will_eat:
        eat_piece()

    print_board()


def eat_piece():
    global path_to_eat
    if len(path_to_eat) >=2: 
        pos1 = path_to_eat[0]
        pos2 = path_to_eat[1]

        y_to_eat = int((pos1[0] + pos2[0])/2)
        x_to_eat = int((pos1[1] + pos2[1])/2)

        board[y_to_eat][x_to_eat] = '  '
        
        path_to_eat.remove(pos1)

        eat_piece()


def get_path(target_pos):
    global passed_history
    global path_to_eat
    global end_path

    found_idx = None
    for idx in dict(reversed(list(passed_history.items()))):
        for idx_pos,pos in enumerate(passed_history[idx]):
            if pos == target_pos:
                found_idx = idx
                                
                path_to_eat.append(passed_history[idx][idx_pos])
                passed_history[idx].pop(idx_pos)
                if passed_history[idx] == []:
                    passed_history.pop(idx)

                get_path([found_idx[0],found_idx[1]])
                end_path = True
                break
        if end_path:
            path_to_eat.append(pos_to_move)
            break
        


def get_cannot_move_areas(origin):
    global cannot_move_areas

    cannot_move_areas.clear()

    y = origin[0]
    x = origin[1]

    for idx_line,line in enumerate(board):
        for idx_pos,pos in enumerate(line):
            if idx_line % 2 == 0 and idx_pos % 2 != 0:
                cannot_move_areas.append([idx_line,idx_pos])
            elif idx_line % 2 != 0 and idx_pos % 2 == 0:
                cannot_move_areas.append([idx_line,idx_pos])
    
    if x > 1:
        cannot_move_areas.append([y,(x-2)])
        if y > 4:
            cannot_move_areas.append([(y-4),(x-2)])
        if y < 4:
            cannot_move_areas.append([(y+4),(x-2)])
    if x < 6:
        cannot_move_areas.append([y,(x+2)])
        if y > 4:
            cannot_move_areas.append([(y-4),(x+2)])
        if y < 4:
            cannot_move_areas.append([(y+4),(x+2)])
    if y > 1:
        cannot_move_areas.append([(y-2),x])
        if x > 4:
            cannot_move_areas.append([(y-2),(x-4)])
        if x < 4:
            cannot_move_areas.append([(y-2),(x+4)])
    if y < 6:
        cannot_move_areas.append([(y+2),x])
        if x > 4:
            cannot_move_areas.append([(y+2),(x-4)])
        if x < 4:
            cannot_move_areas.append([(y+2),(x+4)])


def is_possible_move(pos):
    if pos in cannot_move_areas:
        return False
    else:
        return True


def remove_from_mandatory(target):
    exists = False
    for pos in mandatory_position:
        if pos == target:
            exists = True
            break
    if exists:
        mandatory_position.remove(target)


def get_all_mandatory():
    global possibles_position
    global mandatory_position
    global number_pos
    global jump_pieces
    global number_pos_origin_pos
    global madatory_pos_origin_pos

    number_pos_origin_pos.clear()
    madatory_pos_origin_pos.clear()
    
    max_per_pos = 0
    for idx_y,y in enumerate(board):
        for idx_x,x in enumerate(y):
            if board[idx_y][idx_x] == player_option["piece_option"]:
                possibles_position.clear()
                mandatory_position.clear()
                number_pos.clear()
                jump_pieces.clear()
                
                get_mandatory_moves([idx_y,idx_x])

                for idx in number_pos:
                    if number_pos[idx] > max_per_pos:
                        max_per_pos = number_pos[idx]

                number_pos_origin_pos[(idx_y,idx_x)] = max_per_pos
                max_per_pos = 0
    
    max = 0
    for idx in number_pos_origin_pos:
        if number_pos_origin_pos[idx] > max:
            max = number_pos_origin_pos[idx]
    
    for idx2 in number_pos_origin_pos:
        if number_pos_origin_pos[idx2] == max:
            madatory_pos_origin_pos.append([idx2[0], idx2[1]])
            


def get_positions():
    global cannot_continue
    global pos_to_move
    
    get_all_mandatory()
    while cannot_continue:
        origin_pos = get_positions_index(input("Digite a posição da peça que deseja movimentar (Ex: 1A) : ").upper())
        verify_origin_positions(origin_pos)
        verify_piece_owner(origin_pos)
        pos_to_move = origin_pos
        get_moves(origin_pos)

    get_final_target_list()
    cannot_continue = True
    print("Possiveis movimentos -> ", get_positions_formated(possibles_position))
    while cannot_continue:    
        target_pos = get_positions_index(input("Digite a posição para onde deseja movimentar (Ex: 1A) : ").upper())
        verify_chosen_positions(target_pos)
        verify_possibles_moves(target_pos)

    get_path(target_pos)
    cannot_continue = True
    return origin_pos, target_pos


def verify_origin_positions(position):
    global cannot_continue

    if madatory_pos_origin_pos != {}:
        if position in madatory_pos_origin_pos:
            cannot_continue = False
        else:
            print("Há peças obrigatórias para comer!")
            cannot_continue = True
            return

    verify_chosen_positions(position)


def verify_chosen_positions(positions):
    global cannot_continue

    for pos in positions:
        if pos <= 7:
            cannot_continue = False
        else:
            cannot_continue = True
            print("Erro! Verifique as posições!")
            break


def did_not_choose_mandatory(target_pos):
    if mandatory_position == []:
        return False
    for pos in mandatory_position:
        if target_pos == pos:
            return False
    return True


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
    global number_pos

    possibles_position.clear()
    mandatory_position.clear()
    number_pos.clear()

    get_possible_moves(origin_pos)
    get_mandatory_moves(origin_pos)


def get_possible_moves(origin_pos):
    global cannot_continue
    global possibles_position

    if cannot_continue != True:

        pos_left = get_left_pos(origin_pos)
        pos_right = get_right_pos(origin_pos)
        
        if pos_left != None and verify_pos(pos_left):
            possibles_position.append(pos_left)

        if pos_right != None and verify_pos(pos_right):
            possibles_position.append(pos_right)


def verify_pos(pos):
    if board[pos[0]][pos[1]] == '  ':
        return True
    return False


def get_mandatory_moves(pos):
    global cannot_continue
    global mandatory_position
    global possibles_position
    global number_pos
    global jump_pieces
    global passed_history

    possible_pos = [player_option["piece_option"], 'D'+player_option["piece_option"][1], '  ']

    pos_left = get_left_pos(pos)
    pos_right = get_right_pos(pos)
    pos_left_back = get_left_back_pos(pos)
    pos_right_back = get_right_back_pos(pos)

    if pos_left != None and board[pos_left[0]][pos_left[1]] not in possible_pos:
        next_left = get_left_pos(pos_left)
        if next_left != None and board[next_left[0]][next_left[1]] == '  ' and pos_left not in jump_pieces:
            if pos != pos_to_move and (pos[0],pos[1]) in number_pos:
                number_pos[(next_left[0],next_left[1])] = number_pos[(pos[0],pos[1])] + 1
            else:
                number_pos[(next_left[0],next_left[1])] = 1
            
            if (pos[0],pos[1]) in passed_history:
                aux = passed_history[(pos[0],pos[1])]
                aux.append(next_left)
                passed_history[(pos[0],pos[1])] = aux
            else:
                passed_history[(pos[0],pos[1])] = [next_left]

            get_mandatory_moves(next_left)
    elif pos_left != None and board[pos_left[0]][pos_left[1]] == '  ' and board[pos[0]][pos[1]] != '  ' and pos_left not in possibles_position:
        mandatory_position.append(pos_left)

    if pos_right != None and board[pos_right[0]][pos_right[1]] not in possible_pos:
        next_right = get_right_pos(pos_right)
        if next_right != None and board[next_right[0]][next_right[1]] == '  ' and pos_right not in jump_pieces:
            jump_pieces.append(pos_right)
            if pos != pos_to_move and (pos[0],pos[1]) in number_pos:
                number_pos[(next_right[0],next_right[1])] = number_pos[(pos[0],pos[1])] + 1
            else:
                number_pos[(next_right[0],next_right[1])] = 1

            if (pos[0],pos[1]) in passed_history:
                aux = passed_history[(pos[0],pos[1])]
                aux.append(next_right)
                passed_history[(pos[0],pos[1])] = aux
            else:
                passed_history[(pos[0],pos[1])] = [next_right]

            get_mandatory_moves(next_right)
    elif pos_right != None and board[pos_right[0]][pos_right[1]] == '  ' and board[pos[0]][pos[1]] != '  ' and pos_right not in possibles_position:
        mandatory_position.append(pos_right)

    if pos_left_back != None and board[pos_left_back[0]][pos_left_back[1]] not in possible_pos and board[pos_left_back[0]][pos_left_back[1]] not in mandatory_position:
        next_left_back = get_left_back_pos(pos_left_back)
        if next_left_back != None and board[next_left_back[0]][next_left_back[1]] == '  ' and pos_left_back not in jump_pieces:
            jump_pieces.append(pos_left_back)
            if pos != pos_to_move and (pos[0],pos[1]) in number_pos:
                number_pos[(next_left_back[0],next_left_back[1])] = number_pos[(pos[0],pos[1])] + 1
            else:
                number_pos[(next_left_back[0],next_left_back[1])] = 1

            if (pos[0],pos[1]) in passed_history:
                aux = passed_history[(pos[0],pos[1])]
                aux.append(next_left_back)
                passed_history[(pos[0],pos[1])] = aux
            else:
                passed_history[(pos[0],pos[1])] = [next_left_back]

            get_mandatory_moves(next_left_back)
    
    if pos_right_back != None and board[pos_right_back[0]][pos_right_back[1]] not in possible_pos :
        next_right_back = get_right_back_pos(pos_right_back)
        if next_right_back != None and board[next_right_back[0]][next_right_back[1]] == '  ' and pos_right_back not in jump_pieces:
            jump_pieces.append(pos_right_back)
            if pos != pos_to_move and (pos[0],pos[1]) in number_pos:
                number_pos[(next_right_back[0],next_right_back[1])] = number_pos[(pos[0],pos[1])] + 1
            else:
                number_pos[(next_right_back[0],next_right_back[1])] = 1
                
            if (pos[0],pos[1]) in passed_history:
                aux = passed_history[(pos[0],pos[1])]
                aux.append(next_right_back)
                passed_history[(pos[0],pos[1])] = aux
            else:
                passed_history[(pos[0],pos[1])] = [next_right_back]

            get_mandatory_moves(next_right_back)
            

def get_right_pos(pos):
    y = pos[0]
    x = pos[1]
    if player_playing == 1:
        return verify_position_in_board(y-1,x+1)
    elif player_playing == 2:
        return verify_position_in_board(y+1,x+1)


def get_left_pos(pos):
    y = pos[0]
    x = pos[1]
    if player_playing == 1:
        return verify_position_in_board(y-1,x-1)
    elif player_playing == 2:
        return verify_position_in_board(y+1,x-1)


def get_right_back_pos(pos):
    y = pos[0]
    x = pos[1]
    if player_playing == 1:
        return verify_position_in_board(y+1,x+1)
    elif player_playing == 2:
        return verify_position_in_board(y-1,x+1)


def get_left_back_pos(pos):
    y = pos[0]
    x = pos[1]
    if player_playing == 1:
        return verify_position_in_board(y+1,x-1)
    elif player_playing == 2:
        return verify_position_in_board(y-1,x-1)


def get_final_target_list():
    global mandatory_position
    global possibles_position
    global will_eat

    get_mandatory_list()

    if mandatory_position == []:
        will_eat = False
        return
    else:
        possibles_position = mandatory_position
        will_eat = True
        return


def check_phb_pos(pos):
    if pos[0] == pos_to_move[0] and pos[1] != (pos_to_move[1]+4) and pos_to_move[1] <=3:
        return False
    elif pos[0] == pos_to_move[0] and pos[1] != (pos_to_move[1]-4) and pos_to_move[1] >= 4:
        return False
    else:
        return True


def verify_position_in_board(y,x):
    if y > 7 or y < 0:
        return None
    if x > 7 or x < 0:
        return None
    else:
        return [y,x]


def get_mandatory_list():
    global number_pos
    global mandatory_position

    max = 0
    for idx in number_pos:
        if number_pos[idx] > max:
            max = number_pos[idx]
    
    for idx2 in number_pos:
        if number_pos[idx2] == max:
            mandatory_position.append([idx2[0], idx2[1]])
    


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
