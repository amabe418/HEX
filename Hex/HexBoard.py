import numpy

class HexBoard:
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = numpy.zeros((size, size), dtype = int)  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
         

    def clone(self) -> "HexBoard":
        """Devuelve una copia del tablero actual"""
        pass  # Aquí luego puedes implementar la clonación del tablero

    def place_piece(self, row: int, col: int, player_id: int) -> bool:
        if  self.board[row][col] is 0:
            self.board[row][col] = player_id
            return True
        return False
        
    def get_possible_moves(self) -> list:
        """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
        pass

    def check_connection(self, player_id: int) -> bool:
        """Verifica si el jugador ha conectado sus dos lados"""
        pass
