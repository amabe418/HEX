import numpy
import collections
import heapq



global RED
global BLUE
global RESET
global PLAYER_1
global PLAYER_2
global oo
oo = float('inf')

RED = '\033[31m'
BLUE = '\033[34m'
YELLOW = '\033[33m'
RESET = '\033[0m'
PLAYER_1 = 1
PLAYER_2 = 2


class HexBoard:
    """ En esta clase se implementa el tablero y los metodos necesarios para su manejo durante el juego"""
    def __init__(self, size: int):
        self.size = size  # Tamaño N del tablero (NxN)
        self.board = numpy.zeros((size, size), dtype = int)  # Matriz NxN (0=vacío, 1=Jugador1, 2=Jugador2)
         
    def clone(self) -> "HexBoard":
        """Devuelve una copia del tablero actual"""
        new_board =  HexBoard(self.size)
        new_board.board = self.board.copy()
        return new_board

    def place_piece(self, row: int, col: int, player_id: int) -> bool: #si la casilla esta vacia, la marca con el id del jugador que la selecciono y devuelve true, si no, pues nadota.
        """Coloca una ficha si la casilla está vacía."""
        if  self.board[row][col] == 0:
            self.board[row][col] = player_id
            return True
        return False

    def remove_piece(self, row:int, col:int):
        self.board[row][col]=0     

    def get_possible_moves(self) -> list: #recorre el tablero en busca de las casillas que aun no han sido marcadas.
        """Devuelve todas las casillas vacías como tuplas (fila, columna)."""
        result = []
        for i in range(self.size):
            for j in range (self.size):
                if self.board[i][j] == 0:
                    result.append((i,j))
        return result
   
    def check_connection(self, player_id: int) -> bool: # para esto, teoricamente, se implementa un bfs con dos nodos fantasma, cada uno en los extremos del tablero correspondientes al jugador.
        """Verifica si el jugador ha conectado sus dos lados"""

        visited = numpy.full((self.size, self.size), False)
        qeue = collections.deque()

        for i in self.adj(id=player_id):
            if self.board[i[0]][i[1]] == player_id:
                visited[i[0]][i[1]] = True
                qeue.append(i)
                
        while qeue:
            node = qeue.popleft()
            row, col = node
            if player_id == 1 and col == self.size - 1 : return True 
            if player_id == 2 and row == self.size - 1 : return True
                
            for i in self.adj(row = row, col = col):
               if not visited[i[0], i[1]] and self.board[i[0]][i[1]] == player_id : 
                   visited[row][col] = True
                   qeue.append(i)
        
        return False
  
    def is_valid(self, row: int, col: int):
        return 0 <= row < self.size and 0 <= col < self.size
    
    def adj(self, row: int = 0, col: int = 0, id: int = 0 ):
        """Devuelve una lista de las casillas adyacentes a la casilla que se introduzca como argumento"""
        if id == 1: return [(i,0) for i in range(self.size)]
        elif id == 2: return [(0,i) for i in range(self.size)]
           
        adj =  [(row, col-1), (row, col+1), (row-1, col+1),(row - 1, col) , (row+1, col), (row+1, col-1)]
        
        return [i for i in adj if self.is_valid(i[0],i[1])]
        
    def heuristic_value_dijkstra(self, player_id: int) -> int:
        """Devuelve el valor del estado del tablero(el menor camino para unir los extremos)"""
        size = self.size
        distance = numpy.full((size,size), float('inf')) #matriz de distancias
        visited = numpy.full((size,size), False) 
        heap=[]

        for position in self.adj(id=player_id): #esto es parecido al check connection, dependiendo del jugador se le dan los adyacentes correspondientes
            row, col = position
            if self.board[row][col] == player_id: distance[row][col]=0
            if self.board[row][col] == 0 : distance[row][col] = 1
            heapq.heappush(heap,(distance[row][col],position))

        while heap:
            cost, position = heapq.heappop(heap)
            row, col = position
            if visited[row][col]: continue
            
            visited[row][col] = True
            if player_id == 1 and col == size - 1 : return cost
            if player_id == 2 and row == size - 1 : return cost

            for position_ in self.adj(row = row, col = col):
                roww, coll = position_
                if  visited[roww][coll] or self.board[roww][coll] == 3-player_id: continue

                new_cost = cost if self.board[roww][coll] == player_id else cost+1
                if new_cost < distance[roww][coll]: 
                    heapq.heappush(heap, (new_cost, position_))
                    distance[roww][coll]= new_cost

            
        return float('inf') #si no devuelve nada por alla es porque no hay camino.

    def pretty_print(self) -> None:
        N = self.size
        tab = 0
        for i in range(N):
            print(' ' * tab,end='')
            for j in range(N):
                if self.board[i][j] == 0: print(f'{self.board[i][j]}{RESET} ', end='')          # Si no está tomada dejamos el '''''hexágono''''' en blanco
                elif self.board[i][j] == 1: print(f'{RED}{self.board[i][j]}{RESET} ', end='')   # Si está tomada por el jugador rojo imprimimos el '''''hexágono''''' en rojo
                elif self.board[i][j] == 'R': print(f'{YELLOW}1{RESET} ',end='')                # Camino de victoria del jugador rojo
                elif self.board[i][j] == 'B': print(f'{YELLOW}2{RESET} ',end='')                # Camino de victoria del jugador azul
                else: print(f'{BLUE}{self.board[i][j]}{RESET} ', end='')                        # Si está tomada por el jugador azul imprimimos el '''''hexágono''''' en azul
            # tab += -1 if i%2 == 0 else 1
            tab += 1
            print()     # Pasamos a la siguiente línea
        
        print() # Dejamos un espacio para el texto que siga

    def bfs(self,player_id) -> list[bool]:
        N = self.size
        visited = {(i,j):False for i in range(N) for j in range(N)}
        parent = {(i,j):None for i in range(N) for j in range(N)}
        visited[(0,N)] = visited[(N,0)] = False 
        
        # Los vértices ficticios sobre los que se hará el BFS son (0,N) y (N,0) respectivamente en dependencia de si el jugador es rojo o azul
        
        start = (0,-1) if player_id == PLAYER_1 else (-1,0)
        q = [start]
        parent[start] = None
        while q:
            v = q.pop()
            visited[v] = True
            for neighbor in self.adj(v[0],v[1],player_id):
                if not visited[neighbor]:
                    q.append(neighbor)
                    parent[neighbor] = v

        return visited,parent

    def get_relevant_moves(self, radius=2) -> list:
        """Devuelve las casillas vacías dentro de un radio de fichas ya colocadas"""
        relevant = set()
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] != 0:
                    for dx in range(-radius, radius + 1):
                        for dy in range(-radius, radius + 1):
                            ni, nj = i + dx, j + dy
                            if self.is_valid(ni, nj) and self.board[ni][nj] == 0:
                                relevant.add((ni, nj))
        return list(relevant) if relevant else self.get_possible_moves()
  