import matplotlib.pyplot as plt
from qlearning import *

def main_training():
    agent, eval_results = QLearningAIPlayer.train_agent(
        episodes=10000,
        save_interval=1000,
        minimax_depth=3
    )
    
    plt.figure(figsize=(10, 6))
    plt.plot(eval_results, 'b-o')
    plt.title('performance vs minimax (training)')
    plt.xlabel('training checkpoints (x1000 episodes)')
    plt.ylabel('win rate')
    plt.grid(True)
    plt.savefig('training_performance.png')
    plt.show()
    
    metrics = QLearningAIPlayer.evaluate_agent(agent, num_games=500)
    comparison = QLearningAIPlayer.compare_vs_minimax(agent, depth=3, num_games=100)
    
    print("\n" + "="*50)
    print("final evaluation results")
    print("="*50)
    print(f"overall win rate: {metrics['win_rate']:.2%}")
    print(f"average score: {metrics['avg_score']:.2f}")
    print(f"moves per game: {metrics['avg_moves']:.1f}")
    
    print("\n" + "-"*50)
    print("comparison with minimax")
    print("-"*50)
    print(f"q-learning wins: {comparison['q_win_rate']:.2%}")
    print(f"minimax wins: {comparison['minimax_win_rate']:.2%}")
    print(f"draws: {comparison['draw_rate']:.2%}")
    
    with open('evaluation_report.txt', 'w') as f:
        f.write("q-learning agent evaluation report\n")
        f.write("="*50 + "\n")
        f.write(f"overall win rate: {metrics['win_rate']:.2%}\n")
        f.write(f"average score: {metrics['avg_score']:.2f}\n")
        f.write(f"moves per game: {metrics['avg_moves']:.1f}\n\n")
        f.write("comparison with minimax\n")
        f.write("-"*50 + "\n")
        f.write(f"q-learning wins: {comparison['q_win_rate']:.2%}\n")
        f.write(f"minimax wins: {comparison['minimax_win_rate']:.2%}\n")
        f.write(f"draws: {comparison['draw_rate']:.2%}\n")

if __name__ == "__main__":
    main_training()