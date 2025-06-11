from game import *
from minimax import *
from qlearning import *
import time

def main():
    game = TwixtGame()
    
    q_agent = QLearningAgent()
    if os.path.exists('twixt_q_learning_final.pkl'):
        q_agent.load_data('twixt_q_learning_final.pkl')
    
    print("choose the players:")
    print("1. human")
    print("2. minimax")
    print("3. q-learning")
    
    player1_choice = int(input("player 1 (X): "))
    player2_choice = int(input("player 2 (O): "))
    
    player1 = None
    player2 = None
    
    if player1_choice == 2:
        depth1 = int(3)
        player1 = MinimaxAIPlayer(game, PLAYER_1, depth=depth1)
    elif player1_choice == 3:
        player1 = QLearningAIPlayer(q_agent)
    
    if player2_choice == 2:
        depth2 = int(3)
        player2 = MinimaxAIPlayer(game, PLAYER_2, depth=depth2)
    elif player2_choice == 3:
        player2 = QLearningAIPlayer(q_agent)

    print(Fore.RED + "player 1 (X) connects top to bottom." + Style.RESET_ALL)
    print(Fore.BLUE + "player 2 (O) connects left to right." + Style.RESET_ALL)
    
    move_count = 0
    start_time = time.time()
    
    while not game.is_game_over():
        game.print_board()
        print(f"move: {move_count}")
        
        if game.current_player == PLAYER_1:
            print("player 1's turn (X)")
            if player1:
                if isinstance(player1, MinimaxAIPlayer):
                    player1.make_move()
                else:
                    player1.make_move(game)
            else:
                try:
                    x, y = map(int, input("coordinates (x y): ").split())
                    if not game.place_pin(x, y):
                        print("invalid move. try again.")
                except ValueError:
                    print("invalid entry. use numbers separated by spaces")
        
        else:
            print("player 2's turn (O)")
            if player2:
                if isinstance(player2, MinimaxAIPlayer):
                    player2.make_move()
                else: 
                    player2.make_move(game)
            else:
                try:
                    x, y = map(int, input("coordinates (x y): ").split())
                    if not game.place_pin(x, y):
                        print("invalid move. try again.")
                except ValueError:
                    print("invalid entry. use numbers separated by spaces")
        
        move_count += 1

    game.print_board()
    elapsed_time = time.time() - start_time
    print(f"game finished in {move_count} moves. time: {elapsed_time:.2f} seconds.")
    
    if game.winner == PLAYER_1:
        print("player 1 (X) wins!")
    elif game.winner == PLAYER_2:
        print("player 2 (O) wins!")
    else:
        print("draw!")

if __name__ == "__main__":
    main()