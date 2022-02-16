board = [['  ' for i in range(8)] for i in range(8)]

def get_player_option():
    while True:
        player_option = input("Digite 1 para jogar contra a máquina e 2 para jogar contra outro jogador: ")

        if player_option not in ["1", "2"]:
            print("Opção invalida!")
        else:
            printBoard()
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

main()