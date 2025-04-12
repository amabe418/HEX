import HexBoard
INFINITY=float('inf')

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
       best_score = float('-inf')
       best_move = None
       for move in board.get_possible_moves():
           new_board = board.clone()
           new_board.place_piece(move[0], move[1], self.player_id)
           score = self.minimax(new_board, float('-inf'), float('inf'), True,4)
           if score > best_score: 
            best_score = score
            best_move = move
       return best_move
       
    def evaluate(self, board: HexBoard) -> float:
        my_id = self.player_id
        opp_id = 3 - my_id

        my_dist = board.heuristic_value_dijkstra(my_id)
        opp_dist = board.heuristic_value_dijkstra(opp_id)

        # Prioridad total si uno de los dos está a punto de ganar
        if my_dist == 0: return 10_000  # ya ganaste
        if opp_dist == 0: return -10_000  # el oponente ya ganó
        if my_dist == 1: return 5_000     # estás a una de ganar
        if opp_dist == 1: return -5_000   # bloquear urgente

        # Penalización si estamos bloqueados
        if my_dist == float('inf'): return -999
        if opp_dist == float('inf'): return 999

        # Bonus por centro del tablero
        center_bonus = 0
        size = board.size
        for i in range(size):
            for j in range(size):
                if board.board[i][j] == my_id:
                    center_bonus += (1 - (abs(i - size//2) + abs(j - size//2)) / size)

        # Bonus por grupos conectados
        def count_connected_groups(player_id):
            visited = [[False]*size for _ in range(size)]
            count = 0
            for i in range(size):
                for j in range(size):
                    if board.board[i][j] == player_id and not visited[i][j]:
                        stack = [(i, j)]
                        while stack:
                            r, c = stack.pop()
                            if visited[r][c]: continue
                            visited[r][c] = True
                            for nr, nc in board.adj(r, c):
                                if board.board[nr][nc] == player_id:
                                    stack.append((nr, nc))
                        count += 1
            return count

        my_groups = count_connected_groups(my_id)
        opp_groups = count_connected_groups(opp_id)
        group_score = (opp_groups - my_groups) * 2

        return (opp_dist - my_dist) + center_bonus + group_score

    def minimax(self, board: HexBoard, alpha, beta, maximizing,depth)-> float:
        """Devuelve el mejor resultado de las decisiones del futuro cercano"""
        if depth == 0 or board.check_connection(self.player_id) or board.check_connection(3 - self.player_id):
            return self.evaluate(board)
        moves = board.get_relevant_moves()
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
    

    
    # def evaluate(self, board: HexBoard) -> float: 
    #     """Evalua el estado del tablero y devuelve el puntaje"""
    #     player_distance = board.heuristic_value_dijkstra(self.player_id)
    #     opponent_distance = board.heuristic_value_dijkstra(3 - self.player_id)
    #     if player_distance == float('inf'): return -1000
    #     if opponent_distance == float('inf'): return 1000
    #     return opponent_distance - player_distance

    # def evaluate(self, board: HexBoard) -> float:
    #     my_id = self.player_id
    #     opp_id = 3 - my_id

    #     my_dist = board.heuristic_value_dijkstra(my_id)
    #     opp_dist = board.heuristic_value_dijkstra(opp_id)

    #     # Penalización si estamos bloqueados
    #     if my_dist == float('inf'): return -999
    #     if opp_dist == float('inf'): return 999

    #     # Bonus por centro del tablero
    #     center_bonus = 0
    #     size = board.size
    #     for i in range(size):
    #         for j in range(size):
    #             if board.board[i][j] == my_id:
    #                 center_bonus += (1 - (abs(i - size//2) + abs(j - size//2)) / size)

    #     # Bonus por cantidad de piezas propias conectadas
    #     def count_connected_groups(player_id):
    #         visited = [[False]*size for _ in range(size)]
    #         count = 0
    #         for i in range(size):
    #             for j in range(size):
    #                 if board.board[i][j] == player_id and not visited[i][j]:
    #                     stack = [(i, j)]
    #                     while stack:
    #                         r, c = stack.pop()
    #                         if visited[r][c]: continue
    #                         visited[r][c] = True
    #                         for nr, nc in board.adj(r, c):
    #                             if board.board[nr][nc] == player_id:
    #                                 stack.append((nr, nc))
    #                     count += 1
    #         return count

    #     my_groups = count_connected_groups(my_id)
    #     opp_groups = count_connected_groups(opp_id)

    #     # Menos grupos = mejor conexión
    #     group_score = (opp_groups - my_groups) * 2

    #     return (opp_dist - my_dist) + center_bonus + group_score
            


# import HexBoard

# class Player:
#     def __init__(self, player_id: int):
#         self.player_id = player_id

#     def evaluate(self, board: HexBoard) -> float:
#         my_dist = board.heuristic_value_dijkstra(self.player_id)
#         opp_dist = board.heuristic_value_dijkstra(3 - self.player_id)
#         if my_dist == float('inf'): return -1000
#         if opp_dist == float('inf'): return 1000
#         return opp_dist - my_dist

#     def minimax(self, board, alpha, beta, maximizing, depth):
#         if depth == 0 or board.check_connection(self.player_id) or board.check_connection(3 - self.player_id):
#             return self.evaluate(board)

#         best_eval = float('-inf') if maximizing else float('inf')
#         moves = board.get_relevant_moves()
#         player = self.player_id if maximizing else 3 - self.player_id

#         for move in moves:
#             new_board = board.clone()
#             new_board.place_piece(*move, player)
#             eval = self.minimax(new_board, alpha, beta, not maximizing, depth - 1)
#             if maximizing:
#                 best_eval = max(best_eval, eval)
#                 alpha = max(alpha, eval)
#             else:
#                 best_eval = min(best_eval, eval)
#                 beta = min(beta, eval)
#             if beta <= alpha: break

#         return best_eval

#     def play(self, board: HexBoard) -> tuple:
#         best_move = None
#         best_score = float('-inf')
#         for move in board.get_relevant_moves():
#             new_board = board.clone()
#             new_board.place_piece(*move, self.player_id)
#             score = self.minimax(new_board, float('-inf'), float('inf'), False, 2)
#             if score > best_score:
#                 best_score = score
#                 best_move = move
#         return best_move

