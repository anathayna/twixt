from collections import defaultdict
import numpy as np
import pickle
import os
import random
import threading
from game import TwixtGame, PLAYER_1, PLAYER_2
from minimax import MinimaxAIPlayer

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, min_epsilon=0.01, decay=0.9995):
        self.q_table = defaultdict(lambda: defaultdict(float))
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.min_epsilon = min_epsilon
        self.decay = decay
        self.training_data = []
        
    def get_state_representation(self, game):
        return (
            tuple(tuple(row) for row in game.board),
            game.current_player
        )
    
    def get_valid_actions(self, game):
        return game.get_valid_moves()
    
    def get_q_value(self, state, action):
        return self.q_table[state][action]
    
    def update_q_value(self, state, action, reward, next_state):
        if next_state not in self.q_table or not self.q_table[next_state]:
            best_next = 0
        else:
            best_next = max(self.q_table[next_state].values())
        
        td_target = reward + self.gamma * best_next
        td_error = td_target - self.get_q_value(state, action)
        self.q_table[state][action] += self.alpha * td_error
    
    def choose_action(self, game, training_mode=True):
        state = self.get_state_representation(game)
        valid_actions = self.get_valid_actions(game)
        
        if not valid_actions:
            return None
            
        # ε-greedy
        if training_mode and np.random.rand() < self.epsilon:
            return random.choice(valid_actions)  # exploração
        else:
            q_values = [self.get_q_value(state, a) for a in valid_actions]
            max_q = max(q_values) if q_values else 0
            best_actions = [a for a, q in zip(valid_actions, q_values) if q == max_q]
            return random.choice(best_actions) if best_actions else None
    
    def decay_epsilon(self):
        self.epsilon = max(self.min_epsilon, self.epsilon * self.decay)
    
    def save_data(self, filename, async_save=True):
        if async_save:
            threading.Thread(target=self._save_data, args=(filename,)).start()
        else:
            self._save_data(filename)
    
    def _save_data(self, filename):
        q_table_serializable = {state: dict(actions) for state, actions in self.q_table.items()}
        with open(filename, 'wb') as f:
            pickle.dump({
                'q_table': q_table_serializable,
                'epsilon': self.epsilon,
                'training_data': self.training_data
            }, f)
    
    def load_data(self, filename):
        if os.path.exists(filename):
            with open(filename, 'rb') as f:
                data = pickle.load(f)
                self.q_table = defaultdict(lambda: defaultdict(float))
                for state, actions in data['q_table'].items():
                    self.q_table[state] = defaultdict(float, actions)
                self.epsilon = data['epsilon']
                self.training_data = data.get('training_data', [])

class QLearningAIPlayer:
    def __init__(self, agent):
        self.agent = agent
    
    def make_move(self, game):
        action = self.agent.choose_action(game, training_mode=False)
        if action:
            x, y = action
            print(f"q-learning played at ({x}, {y})")
            success = game.place_pin(x, y)
            if not success:
                print("ERROR: q-learning made an invalid move!")
            return success
        return False

def train_agent(episodes=10000, save_interval=1000, minimax_depth=3):
    agent = QLearningAgent()
    wins = []
    evaluation_results = []
    
    if os.path.exists('twixt_q_learning.pkl'):
        agent.load_data('twixt_q_learning.pkl')
    
    for episode in range(1, episodes + 1):
        game = TwixtGame()
        done = False
        total_reward = 0
        
        while not done:
            state = agent.get_state_representation(game)
            
            if game.current_player == PLAYER_1:
                action = agent.choose_action(game, training_mode=True)
                if action is None:
                    break
                    
                x, y = action
                success = game.place_pin(x, y)
                if not success:
                    continue

                if game.winner == PLAYER_1:
                    reward = 100
                elif game.winner == PLAYER_2:
                    reward = -100
                elif game.is_game_over():
                    reward = -10  # draws
                else:
                    reward = game.evaluate_func() * 0.1
                
                next_state = agent.get_state_representation(game)
                agent.update_q_value(state, action, reward, next_state)
                total_reward += reward
            
            else:
                minimax_ai = MinimaxAIPlayer(game, PLAYER_2, depth=minimax_depth)
                minimax_ai.make_move()
            
            done = game.is_game_over()
        
        wins.append(1 if game.winner == PLAYER_1 else 0)
        agent.decay_epsilon()
        agent.training_data.append(total_reward)
        
        if episode % save_interval == 0:
            win_rate = np.mean(wins[-save_interval:]) if wins else 0
            print(f"episode {episode}: win rate {win_rate:.2f}, epsilon {agent.epsilon:.4f}")
            
            eval_win_rate = evaluate_against_minimax(agent, minimax_depth, games=10)
            evaluation_results.append(eval_win_rate)
            print(f"  evaluation against minimax: {eval_win_rate:.2f}")
            
            agent.save_data('twixt_q_learning_temp.pkl')
            os.replace('twixt_q_learning_temp.pkl', 'twixt_q_learning.pkl')
    
    agent.save_data('twixt_q_learning_final.pkl')
    return agent, evaluation_results

def evaluate_against_minimax(agent, minimax_depth, games=50):
    wins = 0
    for i in range(games):
        game = TwixtGame()
        q_player = QLearningAIPlayer(agent)
        minimax_player = MinimaxAIPlayer(game, PLAYER_2, depth=minimax_depth)
        
        while not game.is_game_over():
            if game.current_player == PLAYER_1:
                q_player.make_move(game)
            else:
                minimax_player.make_move()
        
        if game.winner == PLAYER_1:
            wins += 1
        print(f"match {i+1}/{games} - agent wins: {wins}")
    
    return wins / games