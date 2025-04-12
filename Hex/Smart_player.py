import numpy
import heapq
from player import Player
from hexboard import HexBoard

class Smart_Player(Player):
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
        
        # los movimientos a revisar son los relevantes, los cernanos a los ya colocados por ambos jugadores
        moves = self.get_relevant_moves(board=board)
        
        
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
            for opp_move in self.get_relevant_moves(board=board):
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
        """devuelve la evaluacion del tablero actual"""
        my_id = self.player_id
        opp_id = self.opponent_id
        size = board.size
        
       
        my_dist = self.heuristic_value_dijkstra(my_id,board)
        opp_dist = self.heuristic_value_dijkstra(opp_id,board)
        
        
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
                    for ni, nj in self.adj(board=board,row=i, col=j):
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
                    for ni, nj in self.adj(board=board,row=i, col=j):
                        if board.board[ni][nj] == opp_id:
                            adjacent_friends += 1
                    
                    connectivity_value = adjacent_friends / 6
                    position_value = 1.0 + center_value + progress_value + connectivity_value
                    territory_score -= position_value
        
      
        return base_score * 3 + territory_score
    
    def minimax(self, board, alpha, beta, maximizing, depth) -> float:
        """evalua el tablero luego de haber seleccionado una casilla"""
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
            
        moves = self.get_relevant_moves(board=board)
        
        
        if not moves:
            eval_score = self.evaluate(board)
            self.transposition_table[board_hash] = (depth, eval_score)
            return eval_score
            
      
        if maximizing and self.player_id == 1:  
            moves.sort(key=lambda m: (m[1], -abs(m[0] - board.size//2)), reverse=True)
        elif maximizing and self.player_id == 2:  
            moves.sort(key=lambda m: (m[0], -abs(m[1] - board.size//2)), reverse=True)
        elif not maximizing and self.opponent_id == 1:  
            moves.sort(key=lambda m: (m[1], -abs(m[0] - board.size//2)), reverse=True)
        elif not maximizing and self.opponent_id == 2:  
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
        
    def heuristic_value_dijkstra(self, player_id: int,board:HexBoard) -> int:
        """Devuelve el valor del estado del tablero(el menor camino para unir los extremos)"""
        size = board.size
        distance = numpy.full((size,size), float('inf')) #matriz de distancias
        visited = numpy.full((size,size), False) 
        heap=[]

        for position in self.adj(board=board,id=player_id): #esto es parecido al check connection, dependiendo del jugador se le dan los adyacentes correspondientes
            row, col = position
            if board.board[row][col] == player_id: distance[row][col]=0
            if board.board[row][col] == 0 : distance[row][col] = 1
            heapq.heappush(heap,(distance[row][col],position))

        while heap:
            cost, position = heapq.heappop(heap)
            row, col = position
            if visited[row][col]: continue
            
            visited[row][col] = True
            if player_id == 1 and col == size - 1 : return cost
            if player_id == 2 and row == size - 1 : return cost

            for position_ in self.adj(board=board,row = row, col = col):
                roww, coll = position_
                if  visited[roww][coll] or board.board[roww][coll] == 3-player_id: continue

                new_cost = cost if board.board[roww][coll] == player_id else cost+1
                if new_cost < distance[roww][coll]: 
                    heapq.heappush(heap, (new_cost, position_))
                    distance[roww][coll]= new_cost

            
        return float('inf') #si no devuelve nada por alla es porque no hay camino.

    def is_valid(self, row: int, col: int, board:HexBoard):
        return 0 <= row < board.size and 0 <= col < board.size
    
    def adj(self,board:HexBoard, row: int = 0, col: int = 0, id: int = 0 ):
        """Devuelve una lista de las casillas adyacentes a la casilla que se introduzca como argumento"""
        if id == 1: return [(i,0) for i in range(board.size)]
        elif id == 2: return [(0,i) for i in range(board.size)]
           
        adj =  [(row, col-1), (row, col+1), (row-1, col+1),(row - 1, col) , (row+1, col), (row+1, col-1)]
        
        return [ (x,y) for x,y in adj if self.is_valid(x,y,board)]

    def get_relevant_moves(self,board: HexBoard, radius=2) -> list:
        """Devuelve las casillas vacías dentro de un radio de fichas ya colocadas"""
        relevant = set()
        for i in range(board.size):
            for j in range(board.size):
                if board.board[i][j] != 0:
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            ni, nj = i + dx, j + dy
                            if self.is_valid(board=board, row=ni, col=nj) and board.board[ni][nj] == 0:
                                relevant.add((ni, nj))
        return list(relevant) if relevant else board.get_possible_moves()










