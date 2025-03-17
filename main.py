from colorama import Fore, Style, init

init() # init colorama

BOARD_SIZE = 6

PLAYER_1 = 'X'  # Player 1 (RED)
PLAYER_2 = 'O'  # Player 2 (BLUE)
EMPTY = '.'

DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),          (0, 1),
              (1, -1),  (1, 0), (1, 1)]

class TwixtGame:
    def __init__(self):
        self.board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = PLAYER_1
        self.game_over = False

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
        if self.is_valid_move(x, y):
            self.board[x][y] = self.current_player
            if self.check_win():
                self.game_over = True
                self.print_board()
                print(Fore.RED + f"player {self.current_player} wins!" + Style.RESET_ALL if self.current_player == PLAYER_1 else Fore.BLUE + f"player {self.current_player} wins!" + Style.RESET_ALL)
            else:
                self.current_player = PLAYER_2 if self.current_player == PLAYER_1 else PLAYER_1
            return True
        return False

    def check_win(self):
        if self.current_player == PLAYER_1:
            for start_y in range(BOARD_SIZE):
                if self.board[0][start_y] == PLAYER_1:
                    for end_y in range(BOARD_SIZE):
                        if self.board[BOARD_SIZE-1][end_y] == PLAYER_1 and self.check_connection(0, start_y, BOARD_SIZE-1, end_y):
                            return True
        else:
            for start_x in range(BOARD_SIZE):
                if self.board[start_x][0] == PLAYER_2:
                    for end_x in range(BOARD_SIZE):
                        if self.board[end_x][BOARD_SIZE-1] == PLAYER_2 and self.check_connection(start_x, 0, end_x, BOARD_SIZE-1):
                            return True
        return False

    def check_connection(self, start_x, start_y, target_x, target_y):
        visited = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        stack = [(start_x, start_y)]
        while stack:
            cx, cy = stack.pop()
            if cx == target_x and cy == target_y:
                return True
            if not visited[cx][cy]:
                visited[cx][cy] = True
                for dx, dy in DIRECTIONS:
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and self.board[nx][ny] == self.current_player:
                        stack.append((nx, ny))
        return False
    
    def get_successor_states(self):
        successor_states = []
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == EMPTY:
                    new_board = [row[:] for row in self.board]
                    new_board[i][j] = self.current_player
                    successor_states.append(new_board)
        return successor_states

    def play(self):
        print(Fore.RED + "player 1 (X) connect top to bottom." + Style.RESET_ALL)
        print(Fore.BLUE + "player 2 (O) connect left to right." + Style.RESET_ALL)
        while not self.game_over:
            self.print_board()
            
            if self.current_player == PLAYER_1:
                print(Fore.RED + f"player {self.current_player} turn" + Style.RESET_ALL)
            else:
                print(Fore.BLUE + f"player {self.current_player} turn" + Style.RESET_ALL)
            try:
                x, y = map(int, input("coordinates (x y): ").split())
                if not self.place_pin(x, y):
                    print("invalid move. try again.")
            except ValueError:
                print("invalid input. enter coordinates separated by spaces.")

if __name__ == "__main__":
    game = TwixtGame()
    game.play()