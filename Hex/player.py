import HexBoard

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
       best_score = float('-inf')
       best_move = None
       for move in board.get_possible_moves():
           new_board = board.clone()
           new_board.place_piece(move[0], move[1], self.player_id)
           score = self.minimax(new_board, float('-inf'), float('inf'), True,2)
           if score > best_score: 
            best_score = score
            best_move = move

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
            best_evaluation = float('-inf')
            for move in moves:
                row, col = move
                new_board = board.clone()
                new_board.place_piece(row, col, player)
                evaluation = self.minimax(new_board, alpha, beta, False, depth - 1)
                best_evaluation = max(best_evaluation, evaluation)
                alpha = max(alpha, evaluation)
                if beta <= alpha: break
           
        
        else:
            best_evaluation = float('inf')
            for move in moves:
                row, col = move
                new_board = board.clone()
                new_board.place_piece(row, col, player)
                evaluation = self.minimax(new_board, alpha, beta, True, depth - 1)
                best_evaluation = min(evaluation, best_evaluation)
                beta = min(beta, evaluation)
                if beta <= alpha: break
        return best_evaluation
            

