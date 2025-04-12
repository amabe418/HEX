INFINITY=float('inf')

class Player:
    def __init__(self, player_id):
        self.player_id = player_id  # Tu identificador (1 o 2)

    def play(self, board) -> tuple:
        raise NotImplementedError("¡Implementa este método!")