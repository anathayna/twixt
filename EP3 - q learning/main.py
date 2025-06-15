from game import *
from minimax import *
from qlearning import *
import time
import os

def play_game():
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

def main():
    print("select mode:")
    print("1. play game")
    print("2. train q-learning agent")
    print("3. evaluate trained agent")
    
    choice = int(input("option: "))
    
    if choice == 1:
        play_game()
    elif choice == 2:
        from train import main_training
        main_training()
    elif choice == 3:
        agent = QLearningAgent()
        
        if os.path.exists('twixt_q_learning_final.pkl'):
            agent.load_data('twixt_q_learning_final.pkl')
            print("trained agent loaded successfully.")
        else:
            print("no trained agent found. please train first.")
            return
        
        print("\nevaluating against random player...")
        metrics = QLearningAIPlayer.evaluate_agent(agent, num_games=100)
        
        print("\nevaluation results:")
        print(f"win rate: {metrics['win_rate']:.2%}")
        print(f"average score: {metrics['avg_score']:.2f}")
        print(f"average moves per game: {metrics['avg_moves']:.1f}")
        
        print("\nevaluating against minimax...")
        comparison = QLearningAIPlayer.compare_vs_minimax(agent, depth=3, num_games=50)
        
        print("\ncomparison with minimax:")
        print(f"q-learning win rate: {comparison['q_win_rate']:.2%}")
        print(f"minimax win rate: {comparison['minimax_win_rate']:.2%}")
        print(f"draw rate: {comparison['draw_rate']:.2%}")
    else:
        print("invalid option")

if __name__ == "__main__":
    main()