from colorama import Fore, Style, init
from collections import deque
import math
import copy

init()

BOARD_SIZE = 6
PLAYER_1 = 'X'
PLAYER_2 = 'O'
EMPTY = '.'

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]

class TwixtGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER_1
        self.game_over = False
        self.winner = None

    def print_board(self):
        print("  " + " ".join(Fore.RED + str(i) + Style.RESET_ALL for i in range(BOARD_SIZE)))

        for i in range(BOARD_SIZE):
            if i == 0:
                print(Fore.RED + str(i) + " " + Style.RESET_ALL, end="")
            else:
                print(Fore.BLUE + str(i) + " " + Style.RESET_ALL, end="")
            
            for j in range(BOARD_SIZE):
                if self.board[i][j] == PLAYER_1:
                    print(Fore.RED + PLAYER_1 + Style.RESET_ALL, end=" ")
                elif self.board[i][j] == PLAYER_2:
                    print(Fore.BLUE + PLAYER_2 + Style.RESET_ALL, end=" ")
                else:
                    if i == 0 or i == BOARD_SIZE - 1:  
                        print(Fore.RED + EMPTY + Style.RESET_ALL, end=" ")
                    elif j == 0 or j == BOARD_SIZE - 1: 
                        print(Fore.BLUE + EMPTY + Style.RESET_ALL, end=" ")
                    else:
                        print(EMPTY, end=" ")
            print()

    def is_valid_move(self, x, y):
        return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE and self.board[x][y] == EMPTY

    def place_pin(self, x, y):
        if not self.is_valid_move(x, y):
            return False
            
        self.board[x][y] = self.current_player
        self.print_board()
        
        if self.check_win():
            self.game_over = True
            self.winner = self.current_player
        else:
            if not self.get_valid_moves():
                self.game_over = True
            else:
                self.switch_player()
                
        return True

    def check_win(self):
        return self.has_connection(self.current_player)

    def has_connection(self, player):
        visited = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        queue = deque()

        if player == PLAYER_1:
            start_points = [(0, y) for y in range(BOARD_SIZE) if self.board[0][y] == player]
            is_goal = lambda x, y: x == BOARD_SIZE - 1
        else:
            start_points = [(x, 0) for x in range(BOARD_SIZE) if self.board[x][0] == player]
            is_goal = lambda x, y: y == BOARD_SIZE - 1

        for x, y in start_points:
            queue.append((x, y))
            visited[x][y] = True

        while queue:
            x, y = queue.popleft()
            if is_goal(x, y):
                return True
            for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                if (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE
                    and not visited[nx][ny]
                    and self.board[nx][ny] == player
                ):
                    visited[nx][ny] = True
                    queue.append((nx, ny))
        return False
    
    def get_valid_moves(self):
        moves = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == EMPTY:
                    moves.append((i, j))
        return moves
    
    def switch_player(self):
        self.current_player = PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
    
    def successor_func(self, move):
        x, y = move
        if not self.is_valid_move(x, y):
            return None
            
        new_game = TwixtGame()
        new_game.board = [row[:] for row in self.board]
        new_game.board[x][y] = self.current_player
        new_game.current_player = PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
        new_game.game_over = False
        new_game.winner = None
        
        if new_game.has_connection(self.current_player):
            new_game.game_over = True
            new_game.winner = self.current_player
        return new_game
    
    def is_game_over(self):
        return self.game_over

    def evaluate_func(self):
        if self.game_over:
            if self.winner == PLAYER_1:
                return math.inf
            elif self.winner == PLAYER_2:
                return -math.inf
            else:
                return 0
        
        # heurística 1: contagem de peças conectadas potencialmente vencedoras
        player1_score = self.evaluate_player(PLAYER_1)
        player2_score = self.evaluate_player(PLAYER_2)
        
        # heurística 2: número de movimentos possíveis
        valid_moves = len(self.get_valid_moves())
        
        # heurística 3: posições estratégicas (cantos e centro)
        strategic_position = self.evaluate_strategic_positions()
        
        score = (player1_score - player2_score) + 0.1 * valid_moves + 0.2 * strategic_position

        return score
    
    def evaluate_player(self, player):
        score = 0
        if player == PLAYER_1:
            for y in range(BOARD_SIZE):
                if self.board[0][y] == PLAYER_1:
                    for y2 in range(BOARD_SIZE):
                        if self.board[BOARD_SIZE-1][y2] == PLAYER_1:
                            distance = self.find_connection_distance(0, y, BOARD_SIZE-1, y2, player)
                            if distance != -1:
                                score += (BOARD_SIZE - distance) * 2
        else:
            for x in range(BOARD_SIZE):
                if self.board[x][0] == PLAYER_2:
                    for x2 in range(BOARD_SIZE):
                        if self.board[x2][BOARD_SIZE-1] == PLAYER_2:
                            distance = self.find_connection_distance(x, 0, x2, BOARD_SIZE-1, player)
                            if distance != -1:
                                score += (BOARD_SIZE - distance) * 2
        
        connected = self.count_connection(player)
        score += connected * 2
        
        return score
    
    def find_connection_distance(self, x1, y1, x2, y2, player):
        visited = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        queue = [(x1, y1, 0)]
        visited[x1][y1] = True
        
        while queue:
            cx, cy, dist = queue.pop(0)
            if cx == x2 and cy == y2:
                return dist
            
            for dx, dy in DIRECTIONS:
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and not visited[nx][ny] and (self.board[nx][ny] == player or (nx, ny) == (x2, y2)):
                    visited[nx][ny] = True
                    queue.append((nx, ny, dist + 1))
        
        return -1
    
    def count_connection(self, player):
        count = 0
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == player:
                    for dx, dy in DIRECTIONS:
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < BOARD_SIZE and 0 <= nj < BOARD_SIZE and self.board[ni][nj] == player:
                            count += 1
        return count // 2
    
    def evaluate_strategic_positions(self):
        score = 0
        center = BOARD_SIZE // 2
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == PLAYER_1:
                    distance_to_center = abs(i - center) + abs(j - center)
                    score += (BOARD_SIZE - distance_to_center)
                elif self.board[i][j] == PLAYER_2:
                    distance_to_corner = min(i + j, i + (BOARD_SIZE-1 - j), 
                                            (BOARD_SIZE-1 - i) + j, (BOARD_SIZE-1 - i) + (BOARD_SIZE-1 - j))
                    score -= (BOARD_SIZE - distance_to_corner)
        return score