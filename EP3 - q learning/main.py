from game import *
from minimax import *

def main():
    game = TwixtGame()
    ai_player = AIPlayer(game, PLAYER_2, depth=3)
    
    print(Fore.RED + "player 1 (X - human) connects top to bottom." + Style.RESET_ALL)
    print(Fore.BLUE + "player 2 (O - AI) connects left to right." + Style.RESET_ALL)
    
    while not game.game_over:
        game.print_board()
        
        if game.current_player == PLAYER_1:
            print(Fore.RED + "ur turn (X)" + Style.RESET_ALL)
            try:
                x, y = map(int, input("enter coordinates (x y): ").split())
                if not game.place_pin(x, y):
                    print("invalid move. try again.")
            except ValueError:
                print("invalid input. enter coordinates separated by spaces.")
        else:
            print(Fore.BLUE + "AI's turn (O)" + Style.RESET_ALL)
            ai_player.make_move()

if __name__ == "__main__":
    main()