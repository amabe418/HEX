import numpy
import collections
class HexBoard:
    """ En esta clase se implementa el tablero y los metodos necesarios para su manejo durante el juego"""
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = numpy.zeros((size, size), dtype = int)  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
         
    def clone(self) -> "HexBoard":
        """Devuelve una copia del tablero actual"""
        board =  HexBoard(self.size)
        board.board = self.board
        return board

    def place_piece(self, row: int, col: int, player_id: int) -> bool: #si la casilla esta vacia, la marca con el id del jugador que la selecciono y devuelve true, si no, pues nadota.
        """Coloca una ficha si la casilla está vacía."""
        if  self.board[row][col] is 0:
            self.board[row][col] = player_id
            return True
        return False
        
    def get_possible_moves(self) -> list: #recorre el tablero en busca de las casillas que aun no han sido marcadas.
        """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
        result = []
        for i in range(self.size):
            for j in range (self.size):
                if self.board[i][j] is 0:
                    result.append((i,j))
        return result
   
    def check_connection(self, player_id: int) -> bool: # para esto, teoricamente, se implementa un bfs con dos nodos fantasma, cada uno en los extremos del tablero correspondientes al jugador.
        """Verifica si el jugador ha conectado sus dos lados"""

        visited = numpy.zeros((self.size, self.size))
        qeue = collections.deque()

        for i in self.adj(id=player_id):
            if self.board[i[0]][i[1]] == player_id:
                qeue.append(i)
       
        while qeue:
            node = qeue.popleft()
            row, col = node
            visited[row][col] = 1
            if player_id == 1 and row == self.size - 1 : return True 
            if player_id == 2 and col == self.size - 1 : return True
                
            for i in self.adj(row = row, col = col):
               if not visited[i[0], i[1]] and self.board[i[0]][i[1]] == player_id : 
                   qeue.append(i)
        
        return False
  
    def adj(self, row: int = 0, col:int = 0, id: int = 0 ):
        """Devuelve una lista de las casillas adyacentes a la casilla que se introduzca como argumento"""
        if id is 1:
            return [(i,0) for i in range(self.size)]
        elif id is 2:
            return [(0,i) for i in range(self.size)]
        elif row % 2 is 0: # fila par
            if row > 0: 
                if col>0:return [(row, col-1), (row, col + 1), (row - 1, col),(row + 1, col),(row - 1, col + 1), (row + 1, col + 1)] #fila y columna mayores que cero 
                return [ (row, col + 1), (row - 1, col),(row + 1, col),(row - 1, col + 1), (row + 1, col + 1)] #fila mayor que cero y columna igual a cero.
            
            elif col > 0:  return [(row, col-1), (row, col + 1), (row + 1, col), (row + 1, col + 1)] #fila igual a cero, pero columna mayor que cero
            return [(row, col + 1), (row + 1, col), (row + 1, col + 1)] #fila y columna iguales a cero
        
        else: # fila impar
            if row > 0:
                if col>0: return [(row, col - 1),(row, col + 1) ,(row - 1, col),(row + 1, col) ,(row - 1, col - 1) (row + 1, col - 1) ] #fila y columna mayores que cero 
                return [(row, col + 1) ,(row - 1, col),(row + 1, col)] #fila mayor que cero y columna igual a cero.
            
            elif col > 0 : return [(row, col + 1) ,(row + 1, col) , (row + 1, col - 1) ] #fila igual a cero, pero columna mayor que cero
            return [(row, col + 1) ,(row + 1, col) ] #fila y columna iguales a cero