import enum


board = [['  ' for i in range(8)] for i in range(8)]
cannot_continue = True
player_option={}


def initial_potision(player_choice):
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

def move_piece():
    origin_pos,target_pos = get_positions()
    
    piece = board[origin_pos[0]][origin_pos[1]]
    board[origin_pos[0]][origin_pos[1]] = '  '
    board[target_pos[0]][target_pos[1]] = piece
    print_board()


def get_positions():
    global cannot_continue
    
    while cannot_continue:
        origin_pos = get_positions_index(input("Digite a posição da peça que deseja movimentar (Ex: 1A) : "))
        verify_chosen_positions(origin_pos)
        if cannot_continue != True:
            verify_piece_owner(origin_pos)
        if cannot_continue != True:
            posible_moves = get_posible_moves(origin_pos)
            if posible_moves == None:
                print("Essa peça não pode se mover agora!")
                cannot_continue = True
            
    cannot_continue = True
    print("Possiveis movimentos -> ", posible_moves)
    while cannot_continue:    
        target_pos = get_positions_index(input("Digite a posição para onde deseja movimentar (Ex: 1A) : "))
        verify_chosen_positions(target_pos)
        verify_posibles_moves(posible_moves, target_pos)
        
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


def verify_posibles_moves(posible_moves, target_pos):
    global cannot_continue
    print(posible_moves)
    for pos in posible_moves:
        if pos == target_pos and pos != None:
            cannot_continue= False
            break
        else:
            cannot_continue = True

    if cannot_continue:
        print("Não é possivel mover para essa posição")
    
def get_posible_moves(origin_pos):
    y = origin_pos[0]
    x = origin_pos[1]
    
    if player_option["piece_option"] == board[y][x]:
        if x == 0 and y > 0:
            return [verify_position_ocuation(y-1,x+1)]
        elif x == 7 and y > 0:
           return [verify_position_ocuation(y-1,x-1)]
        elif y > 0:
            pos_right = verify_position_ocuation(y-1,x+1)
            pos_left = verify_position_ocuation(y-1,x-1)
            if pos_right == None and pos_left == None:
                return None
            return [pos_left,pos_right]
        else:
            return None
    

def verify_position_ocuation(y,x):
    if board[y][x] == '  ':
        return [y,x]
    else:
        return None  

def get_positions_index(input_position):
    y = switch_positions_y(input_position[0])
    x = switch_positions_x(input_position[1])
    
    return [int(y),int(x)]
    

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
    

def main():
    player_otion = get_player_option()
    print(player_otion)
    initial_potision(player_otion["piece_option"])
    print_board()
    while True:
        move_piece()
    

main()