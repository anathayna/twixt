from game import *
import math

class AIPlayer:
    def __init__(self, game, player, depth=3):
        self.game = game
        self.player = player
        self.depth = depth
    
    def get_best_move(self):
        best_move = None
        best_value = -math.inf if self.game.current_player == self.player else math.inf
        
        legal_moves = self.game.get_valid_moves()
        if not legal_moves:
            return None
        
        for move in legal_moves:
            successor = self.game.successor_func(move)
            if successor:
                if self.game.current_player == self.player:
                    value = self.minimax(successor, self.depth - 1, -math.inf, math.inf, False)
                    if value > best_value:
                        best_value = value
                        best_move = move
                else:
                    value = self.minimax(successor, self.depth - 1, -math.inf, math.inf, True)
                    if value < best_value:
                        best_value = value
                        best_move = move
        
        return best_move
    
    def minimax(self, game_state, depth, alpha, beta, maximizing_player):
        if depth == 0 or game_state.is_game_over():
            return game_state.evaluate_func()
        
        legal_moves = game_state.get_valid_moves()
        if not legal_moves:
            return game_state.evaluate_func()
        
        if maximizing_player:
            value = -math.inf
            for move in legal_moves:
                successor = game_state.successor_func(move)
                if successor:
                    value = max(value, self.minimax(successor, depth - 1, alpha, beta, False))
                    alpha = max(alpha, value)
                    if alpha >= beta:
                        break
            return value
        else:
            value = math.inf
            for move in legal_moves:
                successor = game_state.successor_func(move)
                if successor:
                    value = min(value, self.minimax(successor, depth - 1, alpha, beta, True))
                    beta = min(beta, value)
                    if alpha >= beta:
                        break
            return value

    def make_move(self):
        best_move = self.get_best_move()
        if best_move:
            x, y = best_move
            print(f"AI ({self.player}) plays at ({x}, {y})")
            return self.game.place_pin(x, y)
        return False