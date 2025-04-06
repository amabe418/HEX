import HexBoard

class Player:
    def __init__(self, player_id: int):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board: HexBoard) -> tuple:
        raise NotImplementedError("¡Implementa este método!")

    def evaluate(self, board: HexBoard) -> float: 
        """metodo que evalua el estado del tablero y devuelve el puntaje"""
        player_distance = board.heuristic_value_dijkstra(self.player_id)
        opponent_distance = board.heuristic_value_dijkstra(3 - self.player_id)
        if player_distance == float('inf'): return -1000
        if opponent_distance == float('inf'): return 1000
        return opponent_distance - player_distance
