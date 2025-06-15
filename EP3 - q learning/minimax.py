from game import *
import math

class MinimaxAIPlayer:
    def __init__(self, game, player, depth=3):
        self.game = game
        self.player = player
        self.depth = depth
    
    def get_best_move(self):
        best_move = None
        best_value = -math.inf
        legal_moves = self.game.get_valid_moves()
        
        for move in legal_moves:
            new_game = self.game.successor_func(move)
            if new_game is None:
                continue
            value = self.minimax(new_game, self.depth-1, -math.inf, math.inf, False)
            if value > best_value:
                best_value = value
                best_move = move
        return best_move
    
    def minimax(self, game, depth, alpha, beta, maximizing):
        if depth == 0 or game.game_over:
            return game.evaluate_func()
            
        if maximizing:
            value = -math.inf
            for move in game.get_valid_moves():
                new_game = game.successor_func(move)
                if new_game is None:
                    continue
                value = max(value, self.minimax(new_game, depth-1, alpha, beta, False))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break
            return value
        else:
            value = math.inf
            for move in game.get_valid_moves():
                new_game = game.successor_func(move)
                if new_game is None:
                    continue
                value = min(value, self.minimax(new_game, depth-1, alpha, beta, True))
                beta = min(beta, value)
                if alpha >= beta:
                    break
            return value

    def make_move(self):
        best_move = self.get_best_move()
        if best_move:
            x, y = best_move
            print(f"minimax ({self.player}) played at ({x}, {y})")
            return self.game.place_pin(x, y)
        return False