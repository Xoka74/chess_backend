from Chessnut import Game


class Bot:
    def __init__(self):
        self.piece_values = {'p': 10, 'n': 30, 'b': 30, 'r': 50, 'q': 90, 'k': 900}

        self.pawn_eval_white = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0, 5.0],
            [1.0, 1.0, 2.0, 3.0, 3.0, 2.0, 1.0, 1.0],
            [0.5, 0.5, 1.0, 2.5, 2.5, 1.0, 0.5, 0.5],
            [0.0, 0.0, 0.0, 2.0, 2.0, 0.0, 0.0, 0.0],
            [0.5, -0.5, -1.0, 0.0, 0.0, -1.0, -0.5, 0.5],
            [0.5, 1.0, 1.0, -2.0, -2.0, 1.0, 1.0, 0.5],
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        ]

        self.pawn_eval_black = self.pawn_eval_white[::-1]

        self.knight_eval = [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0, 0.0, 0.0, 0.0, 0.0, -2.0, -4.0],
            [-3.0, 0.0, 1.0, 1.5, 1.5, 1.0, 0.0, -3.0],
            [-3.0, 0.5, 1.5, 2.0, 2.0, 1.5, 0.5, -3.0],
            [-3.0, 0.0, 1.5, 2.0, 2.0, 1.5, 0.0, -3.0],
            [-3.0, 0.5, 1.0, 1.5, 1.5, 1.0, 0.5, -3.0],
            [-4.0, -2.0, 0.0, 0.5, 0.5, 0.0, -2.0, -4.0],
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0]
        ]

        self.bishop_eval_white = [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 1.0, 1.0, 0.5, 0.0, -1.0],
            [-1.0, 0.5, 0.5, 1.0, 1.0, 0.5, 0.5, -1.0],
            [-1.0, 0.0, 1.0, 1.0, 1.0, 1.0, 0.0, -1.0],
            [-1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, -1.0],
            [-1.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ]

        self.bishop_eval_black = self.bishop_eval_white[::-1]

        self.rook_eval_white = [
            [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
            [0.5, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [-0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -0.5],
            [0.0, 0.0, 0.0, 0.5, 0.5, 0.0, 0.0, 0.0]
        ]

        self.rook_eval_black = self.rook_eval_white[::-1]

        self.eval_queen = [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-0.5, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [0.0, 0.0, 0.5, 0.5, 0.5, 0.5, 0.0, -0.5],
            [-1.0, 0.5, 0.5, 0.5, 0.5, 0.5, 0.0, -1.0],
            [-1.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ]

        self.king_eval_white = [

            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [2.0, 2.0, 0.0, 0.0, 0.0, 0.0, 2.0, 2.0],
            [2.0, 3.0, 1.0, 0.0, 0.0, 1.0, 3.0, 2.0]
        ]

        self.king_eval_black = self.king_eval_white[::-1]

    def make_best_move(self, depth, game, is_maximising_player):
        new_game_moves = game.get_moves()
        board = game.get_fen()
        is_white = board.split(' ')[1] == 'w'
        best_move = -9999
        best_move_found = None

        for i in range(len(new_game_moves)):
            new_game_move = new_game_moves[i]
            game.apply_move(new_game_move)
            value = self.minimax(depth - 1, game, -10000, 10000, not is_maximising_player, is_white)
            game.set_fen(fen=board)

            if value >= best_move:
                best_move = value
                best_move_found = new_game_move

        game.apply_move(best_move_found)

        return game

    def evaluate_board(self, board, is_white):
        total_evaluation = 0
        for i in range(8):
            for j in range(8):
                total_evaluation += self.get_piece_value(board[i][j], i, j, is_white)

        return total_evaluation

    def minimax(self, depth, game, alpha, beta, is_maximising_player, is_white):
        if depth == 0:
            return -1 * self.evaluate_board(self.fen_to_list(game.get_fen()), is_white)
        board = game.get_fen()
        new_game_moves = game.get_moves()

        best_move = -9999
        for i in range(len(new_game_moves)):
            game.apply_move(new_game_moves[i])
            evaluated_move = self.minimax(depth - 1, game, alpha, beta, not is_maximising_player, is_white)
            game.set_fen(board)
            if is_maximising_player:
                best_move = max(best_move, evaluated_move)
                alpha = max(alpha, best_move)
            else:
                best_move = min(best_move, evaluated_move)
                beta = min(beta, best_move)

            if beta <= alpha:
                return best_move

        return best_move

    def get_piece_value(self, piece, x, y, is_white):
        if piece == ' ':
            return 0
        piece_lower = piece.lower()
        if piece_lower == 'p':
            return 10 + self.pawn_eval_white[y][x] if is_white else self.pawn_eval_black[y][x]
        elif piece_lower == 'r':
            return 50 + self.rook_eval_white[y][x] if is_white else self.rook_eval_black[y][x]
        elif piece_lower == 'n':
            return 30 + self.knight_eval[y][x]
        elif piece_lower == 'b':
            return 30 + self.bishop_eval_white[y][x] if is_white else self.bishop_eval_black[y][x]
        elif piece_lower == 'q':
            return 90 + self.eval_queen[y][x]
        elif piece_lower == 'k':
            return 900 + self.king_eval_white[y][x] if is_white else self.king_eval_black[y][x]

    @staticmethod
    def fen_to_list(fen):
        chunks = fen.split(' ')
        fen_board = chunks[0]
        new_board = ""
        for i in range(len(fen_board)):
            if fen_board[i].isnumeric():
                new_board += ' ' * int(fen_board[i])
            else:
                new_board += fen_board[i]

        return [list(i) for i in new_board.split('/')]


if __name__ == '__main__':
    bot = Bot()
    while True:
        board = input()
        game = Game(board)
        is_white = game.get_fen().split(' ')[1] == 'w'
