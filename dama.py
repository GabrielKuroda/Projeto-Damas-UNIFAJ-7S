import enum


board = [['  ' for i in range(8)] for i in range(8)]


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
    player_option = {}

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


def printBoard():
    print("------------------")
    print("  0  1  2  3  4  5  6  7")
    for idxLine,line in enumerate(board):
        for idxColumn,column in enumerate(line):
            if idxColumn == 0:
                print(str(idxLine)+"|"+column, end = "|")
            elif idxColumn == 7:
                print(column+"|")
            else:
                print(column, end = "|")
    print("------------------")


def main():
    player_otion = get_player_option()
    print(player_otion)
    initial_potision(player_otion["piece_option"])
    printBoard()

main()