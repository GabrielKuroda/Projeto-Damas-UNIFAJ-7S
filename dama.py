def get_player_option():
    while True:
        player_option = input("Digite 1 para jogar contra a máquina e 2 para jogar contra outro jogador: ")

        if player_option not in ["1", "2"]:
            print("Opção invalida!")
        else:
            break
        
    return player_option


def main():
    player_otion = get_player_option()
    print(player_otion)


main()