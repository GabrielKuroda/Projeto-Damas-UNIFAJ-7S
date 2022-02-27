board = [['  ' for i in range(8)] for i in range(8)]
cannot_continue = True
player_option={}
player_playing = 1
possibles_position = []
mandatory_position = []
pos_to_move = []
passed_pos = []
history_pos = []
path_pos = []
cannot_move_areas = []


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

    print_board()


def eat_piece(target_pos):
    get_path(target_pos)
    for pos in path_pos:
        board[pos[0]][pos[1]] = '  '


def get_path(target_pos):
    global path_pos
    global history_pos
    
    is_valid = True
    for history in history_pos:
        if history[1] == target_pos:
            for pos in path_pos:
                if pos == history[1]:
                    is_valid = False
                    history_pos.remove(history)
            if is_valid:
                path_pos.append(history[1])
            get_path(history[0])


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


def get_positions():
    global cannot_continue
    global pos_to_move
    
    while cannot_continue:
        origin_pos = get_positions_index(input("Digite a posição da peça que deseja movimentar (Ex: 1A) : ").upper())
        verify_chosen_positions(origin_pos)
        verify_piece_owner(origin_pos)
        pos_to_move = origin_pos
        get_cannot_move_areas(origin_pos)
        get_moves(origin_pos)
        
    print(history_pos)        
    cannot_continue = True
    print("Possiveis movimentos -> ", get_positions_formated(possibles_position))
    while cannot_continue:    
        target_pos = get_positions_index(input("Digite a posição para onde deseja movimentar (Ex: 1A) : ").upper())
        verify_chosen_positions(target_pos)
        verify_possibles_moves(target_pos)

    eat_piece(target_pos)

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
    global passed_pos
    global history_pos
    global path_pos

    possibles_position.clear()
    mandatory_position.clear()
    passed_pos.clear()
    history_pos.clear()
    path_pos.clear()

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

        if pos_left != None and verify_pos(pos_left) and board[y][x] != '  ':
            if did_not_passed(pos_left):
                possibles_position.append(pos_left)
                passed_pos.append(pos_left)
        elif pos_left != None and board[pos_left[0]][pos_left[1]] != player_option["piece_option"]  and board[pos_left[0]][pos_left[1]] != '  ':
            if did_not_passed(pos_left):
                passed_pos.append(pos_left)
                history_pos.append([origin_pos,pos_left])
                get_mandatory_moves(pos_left)

        if pos_right != None and verify_pos(pos_right) and board[y][x] != '  ':
            if did_not_passed(pos_right):
                possibles_position.append(pos_right)
                passed_pos.append(pos_right)
        elif pos_right != None and board[pos_right[0]][pos_right[1]] != player_option["piece_option"] and board[pos_right[0]][pos_right[1]] != '  ':
            if did_not_passed(pos_right):
                passed_pos.append(pos_right)
                history_pos.append([origin_pos,pos_right])
                get_mandatory_moves(pos_right)
 
        if possibles_position == []:
            print("A peça escolhida não pode se mover agora!")
            cannot_continue = True


def did_not_passed(pos_to_check):
    for pos in passed_pos:
        if pos == pos_to_check:
            return False
    return True


def verify_pos(pos):
    if board[pos[0]][pos[1]] == '  ':
        return True
    return False


def get_mandatory_moves(pos):
    global cannot_continue
    global mandatory_position
    global possibles_position
    global history_pos

    if pos != None:
        y = pos[0]
        x = pos[1]

        if player_playing == 1:
            right = verify_position_in_board(y-1,x+1)
            left = verify_position_in_board(y-1,x-1)
            right_back = verify_position_in_board(y+1,x+1)
            left_back = verify_position_in_board(y+1,x-1)
        elif player_playing == 2:
            right = verify_position_in_board(y+1,x+1)
            left = verify_position_in_board(y+1,x-1)
            right_back = verify_position_in_board(y-1,x+1)
            left_back = verify_position_in_board(y-1,x-1)

        if basic_pos_verify(left,x,y):
            if verify_side(left,pos):
                if verify_pos(left) and board[y][x] != '  ' and check_phb_pos(left):
                    mandatory_position.append(left)
                    possibles_position.append(left)
                    passed_pos.append(left)
                    history_pos.append([pos,left])
                    get_mandatory_moves(left)
                elif board[left[0]][left[1]] != '  ' and board[left[0]][left[1]] != player_option["piece_option"]:
                    passed_pos.append(left)
                    history_pos.append([pos,left])
                    get_mandatory_moves(left)
                

        if basic_pos_verify(right,x,y):
            if verify_side(right,pos):
                if verify_pos(right) and board[y][x] != '  ' and check_phb_pos(right):
                    mandatory_position.append(right)
                    possibles_position.append(right)
                    passed_pos.append(right)
                    history_pos.append([pos,right])
                    get_mandatory_moves(right)
                elif board[right[0]][right[1]] != '  ' and board[right[0]][right[1]] != player_option["piece_option"]:
                    passed_pos.append(right)
                    history_pos.append([pos,right])
                    get_mandatory_moves(right)
                
        if basic_pos_verify(right_back,x,y):
            if verify_side(right_back,pos):
                if board[right_back[0]][right_back[1]] != player_option["piece_option"] and board[right_back[0]][right_back[1]] != '  ': 
                    history_pos.append([pos,right_back])
                    get_mandatory_moves(right_back)
                elif board[right_back[0]][right_back[1]] != player_option["piece_option"] and check_phb_pos(right_back):
                    mandatory_position.append(right_back)
                    possibles_position.append(right_back)
                    passed_pos.append(right_back)
                    history_pos.append([pos,right_back])
                    get_mandatory_moves(right_back)

        if basic_pos_verify(left_back,x,y):
            if verify_side(left_back,pos):
                if board[left_back[0]][left_back[1]] != player_option["piece_option"] and board[left_back[0]][left_back[1]] != '  ' :
                    history_pos.append([pos,left_back])
                    get_mandatory_moves(left_back)
                elif board[left_back[0]][left_back[1]] != player_option["piece_option"] and check_phb_pos(left_back):
                    mandatory_position.append(left_back)
                    possibles_position.append(left_back)
                    passed_pos.append(left_back)
                    history_pos.append([pos,left_back])
                    get_mandatory_moves(left_back)
            

def basic_pos_verify(pos,x,y):
    if pos != None and board[pos[0]][pos[1]] != board[y][x] and did_not_passed(pos) and is_possible_move(pos):
        return True
    else:
        return False

def check_phb_pos(pos):
    if pos[0] == pos_to_move[0] and pos[1] != (pos_to_move[1]+4) and pos_to_move[1] <=3:
        return False
    elif pos[0] == pos_to_move[0] and pos[1] != (pos_to_move[1]-4) and pos_to_move[1] >= 4:
        return False
    else:
        return True


def verify_side(pos, origin):  
    
    for prev in history_pos:
        if prev[1] == origin:
            previous_pos = prev[0]
    if (pos[0] == previous_pos[0] or pos[1] == previous_pos[1]) and board[pos[0]][pos[1]] == '  ':
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
    #initial_position(player_otion["piece_option"])
    board[4][6] = 'PB'
    board[3][5] = 'PP'
    board[3][3] = 'PP'
    board[3][1] = 'PP'
    board[1][5] = 'PP'
    board[1][3] = 'PP'
    board[1][1] = 'PP' 
    print_board()
    
    if '2' in player_option["vs_option"]:
        start_shift()


main()
