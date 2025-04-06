import HexBoard

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
       best_score = float('-inf')
       best_move = None
       for move in board.get_possible_moves():
           new_board = board.clone()
           new_board.place_piece(self.player_id)
           score = self.minimax(new_board, float('-inf'), float('inf'), True,5)
           if score> best_score: best_score = score, best_move = move

       return best_move
       
    def evaluate(self, board: HexBoard) -> float: 
        """Evalua el estado del tablero y devuelve el puntaje"""
        player_distance = board.heuristic_value_dijkstra(self.player_id)
        opponent_distance = board.heuristic_value_dijkstra(3 - self.player_id)
        if player_distance == float('inf'): return -1000
        if opponent_distance == float('inf'): return 1000
        return opponent_distance - player_distance

    def minimax(self, board: HexBoard, alpha, beta, maximizing,depth)-> float:
        """Devuelve el mejor resultado de las decisiones del futuro cercano"""
        if depth == 0 or board.check_connection(self.player_id) or board.check_connection(3 - self.player_id):
            return self.evaluate(board)
        moves = board.get_possible_moves()
        player = self.player_id if maximizing else 3 - self.player_id

        if maximizing:
            max_evaluation = float('-inf')
            for move in moves:
                row, col = move
                new_board = board.clone()
                new_board.place_piece(row, col, player)
                evaluation = self.minimax(new_board, alpha, beta, False, depth - 1)
                max_evaluation = max(max_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta<= alpha: break
            return max_evaluation
        
        else:
            min_evaluation = float('inf')
            for move in moves:
                row, col = move
                new_board = board.clone()
                new_board.place_piece(row, col, player)
                evaluation = self.minimax(new_board, alpha, beta, True, depth - 1)
                min_evaluation = min(evaluation, min_evaluation)
                beta = min(beta, evaluation)
                if beta<= alpha: break
                return min_evaluation
            

