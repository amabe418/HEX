import numpy as np
from typing import Tuple
import Player
import HexBoard

class Player:
    def __init__(self, player_id: int):
        super().__init__(player_id)
        self.opponent_id = 3 - player_id
        self.transposition_table = {} 
    
    def play(self, board) -> tuple:
        """Returns the best move according to minimax with alpha-beta pruning"""
        # la primera estrategia es jugar cerca del centro.
        if len(board.get_possible_moves()) == board.size * board.size:
            center = board.size // 2
            return (center, center)
            
        # se cambia la profundidad de busqueda dependiendo del tamaño del tablero
        max_depth = 3 if board.size > 6 else 4
        
        best_move = None
        best_score = float('-inf')
        
        # los movimientos a revisar son los relevantes, los carnanos a los ya colocados por ambos jugadores
        moves = board.get_relevant_moves()
        
        
        if self.player_id == 1:  
            moves.sort(key=lambda m: (m[1], -abs(m[0] - board.size//2)))
        else: 
            moves.sort(key=lambda m: (m[0], -abs(m[1] - board.size//2)))
        
        
        for move in moves:
            new_board = board.clone()
            new_board.place_piece(move[0], move[1], self.player_id)
            
            # si ya con este movimiento se gana, entonces se devuelve
            if new_board.check_connection(self.player_id):
                return move
                
            # si mi enemigo gana con ese movimiento, pues no puede hacerse, hay que bloquear esa vaina.
            for opp_move in board.get_relevant_moves():
                if opp_move == move:
                    continue
                test_board = board.clone()
                test_board.place_piece(opp_move[0], opp_move[1], self.opponent_id)
                if test_board.check_connection(self.opponent_id):
                    # bloquear el movimiento de mi enemigo
                    return opp_move
            
            
            score = self.minimax(new_board, float('-inf'), float('inf'), False, max_depth)
            
            if score > best_score:
                best_score = score
                best_move = move
        
        return best_move
    

    def evaluate(self, board) -> float:
        """Evaluates the current board position from this player's perspective"""
        my_id = self.player_id
        opp_id = self.opponent_id
        size = board.size
        
       
        my_dist = board.heuristic_value_dijkstra(my_id)
        opp_dist = board.heuristic_value_dijkstra(opp_id)
        
        
        if my_dist == 0:
            return 100000
        if opp_dist == 0: 
            return -100000
            
       
        if my_dist == 1:  
            return 50000
        if opp_dist == 1:  
            return -50000
            
        
        if my_dist == float('inf') and opp_dist < float('inf'):
            return -10000
        if opp_dist == float('inf') and my_dist < float('inf'):
            return 10000
        if my_dist == float('inf') and opp_dist == float('inf'):
            return 0  
        
        
        base_score = opp_dist - my_dist  
        
        
        territory_score = 0
        for i in range(size):
            for j in range(size):
                if board.board[i][j] == my_id:
                   
                    center_value = 1 - (abs(i - size//2) + abs(j - size//2)) / size
                    
                
                    if my_id == 1:  
                        progress_value = j / (size - 1)
                    else:  
                        progress_value = i / (size - 1)
                        
                    
                    adjacent_friends = 0
                    for ni, nj in board.adj(i, j):
                        if board.board[ni][nj] == my_id:
                            adjacent_friends += 1
                    
                    connectivity_value = adjacent_friends / 6 
                    
                    
                    position_value = 1.0 + center_value + progress_value + connectivity_value
                    territory_score += position_value
                    
                elif board.board[i][j] == opp_id:
                    
                    center_value = 1 - (abs(i - size//2) + abs(j - size//2)) / size
                    
                    if opp_id == 1:  
                        progress_value = j / (size - 1)
                    else:  
                        progress_value = i / (size - 1)
                        
                    adjacent_friends = 0
                    for ni, nj in board.adj(i, j):
                        if board.board[ni][nj] == opp_id:
                            adjacent_friends += 1
                    
                    connectivity_value = adjacent_friends / 6
                    position_value = 1.0 + center_value + progress_value + connectivity_value
                    territory_score -= position_value
        
      
        return base_score * 3 + territory_score
    
    def minimax(self, board, alpha, beta, maximizing, depth) -> float:
        """Returns the best outcome from future decisions using alpha-beta pruning"""
        board_hash = hash(board.board.tobytes())
        
        
        if board_hash in self.transposition_table and self.transposition_table[board_hash][0] >= depth:
            return self.transposition_table[board_hash][1]
            
     
        if board.check_connection(self.player_id):
            return 100000  
        if board.check_connection(self.opponent_id):
            return -100000  
            
        
        if depth <= 0:
            eval_score = self.evaluate(board)
            self.transposition_table[board_hash] = (0, eval_score)
            return eval_score
            
        moves = board.get_relevant_moves()
        
        
        if not moves:
            eval_score = self.evaluate(board)
            self.transposition_table[board_hash] = (depth, eval_score)
            return eval_score
            
      
        if maximizing and self.player_id == 1:  # Red wants east progress
            moves.sort(key=lambda m: (m[1], -abs(m[0] - board.size//2)), reverse=True)
        elif maximizing and self.player_id == 2:  # Blue wants south progress
            moves.sort(key=lambda m: (m[0], -abs(m[1] - board.size//2)), reverse=True)
        elif not maximizing and self.opponent_id == 1:  # Red wants east progress
            moves.sort(key=lambda m: (m[1], -abs(m[0] - board.size//2)), reverse=True)
        elif not maximizing and self.opponent_id == 2:  # Blue wants south progress
            moves.sort(key=lambda m: (m[0], -abs(m[1] - board.size//2)), reverse=True)
        
        current_player = self.player_id if maximizing else self.opponent_id
        
        if maximizing:
            best_value = float('-inf')
            for move in moves:
                row, col = move
                
                
                if board.board[row][col] != 0:
                    continue
                    
               
                new_board = board.clone()
                new_board.place_piece(row, col, current_player)
                
               
                value = self.minimax(new_board, alpha, beta, False, depth - 1)
                best_value = max(best_value, value)
                
               
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break  
                    
            
            self.transposition_table[board_hash] = (depth, best_value)
            return best_value
        else:
            best_value = float('inf')
            for move in moves:
                row, col = move
                
                
                if board.board[row][col] != 0:
                    continue
                    
                
                new_board = board.clone()
                new_board.place_piece(row, col, current_player)
                
               
                value = self.minimax(new_board, alpha, beta, True, depth - 1)
                best_value = min(best_value, value)
                
                
                beta = min(beta, best_value)
                if beta <= alpha:
                    break  
                    
            
            self.transposition_table[board_hash] = (depth, best_value)
            return best_value