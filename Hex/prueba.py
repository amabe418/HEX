import HexBoard
import Player
import os
import re
import random


# region GLOBALS

# Variables globales para los colores
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
# endregion


# region UTILS
def clear_console():
    '''
    Permite limpiar la consola en dependencia del sistema operativo.
    '''
    os.system('cls' if os.name == 'nt' else 'clear')
    
def print_board(board,msg=None,clear=True):
    '''
    Imprime el tablero en pantalla.\n
    msg: Mensaje opcional.\n
    clear: Limpia la pantalla de forma opcional (por defecto en True).
    '''
    if clear: clear_console()
    if msg: print(msg+'\n')
    board.pretty_print()

def game_selection():
    print('Selecciona el modo de juego:\n1 Jugador vs Jugador\n2 Jugador vs IA\n3 IA vs IA')
    choice = input('> ')
    while choice not in ['1','2','3']:
        clear_console()
        print(f'{RED}Entrada inválida{RESET}')
        print('Selecciona el modo de juego:\n1 Jugador vs Jugador\n2 Jugador vs IA\n3 IA vs IA')
        choice = input('> ')
    return int(choice)

def get_size() -> int:
    '''
    Obtiene la entrada del usuario correspondiente al tamaño del tablero.
    '''
    size_pattern = r'[1-9]+'
    size = re.search(size_pattern,(input("Introduce el tamaño del tablero:\n> ")))
    
    while not size:
        size = re.search(size_pattern,input('El tamaño introducido es inválido, por favor brinde un tamaño de tablero válido:\n> '))
        
    N = int(size.group())
    return N

def get_coords(player_id,board) -> tuple[int,int]:
    '''
    Obtiene la entrada del usuario correspondiente a la posición donde se colocará la ficha.
    '''
    tuple_pattern = r'(\d+)\s*\:\s*(\d+)'
    coords = re.search(tuple_pattern,input(f'Jugador {RED + 'rojo' if player_id == 1 else BLUE + 'azul'}{RESET} coloca ficha en:\n> '))
    while not coords:
        print_board(board,msg='--> Las coordenadas introducidas no son válidas.')
        coords = re.search(tuple_pattern,input(f'Jugador {RED + 'rojo' if player_id == 1 else BLUE + 'azul'}{RESET} coloca ficha en:\n> '))
    i,j = map(int,coords.groups())
    return i,j    

def human_vs_human():
    N = get_size()
    board = HexBoard(N)
    player_id = random.randint(1,2) # Decidimos de forma aleatoria el jugador que empieza
    while True: # Game Loop
        print_board(board)
        i,j = get_coords(player_id,board)
        while not board.place_piece(i,j,player_id):
            print_board(board,clear=False)
            i,j = get_coords(player_id)
        player_id = PLAYER_1 if player_id == PLAYER_2 else PLAYER_2
        if board.check_connection(1) or board.check_connection(2): break

def human_vs_ai():
    N = get_size()
    board = HexBoard.HexBoard(N)
    human = random.randint(1,2)
    bot = Player.Player(3-human)
    actual = random.randint(1,2)
    
    while True: # Game Loop
        print_board(board)
        i,j = get_coords(human,board) if human == actual else bot.play(board)
        while not board.place_piece(i,j,actual):
            print_board(board,clear=False)
            i,j = get_coords(actual,board)
        actual = PLAYER_1 if actual == PLAYER_2 else PLAYER_2
        if board.check_connection(PLAYER_1):
            clear_console()
            print(f"\n--> Gana el jugador {RED}rojo{RESET}.")
            board.pretty_print()
            break
        if board.check_connection(PLAYER_2):
            clear_console()
            print(f"\n--> Gana el jugador {BLUE}azul{RESET}.")
            board.pretty_print()
            break

def ai_vs_ai():
    N = get_size()
    board = HexBoard(N)
    act = random.randint(1,2)
    bot1 = Player(PLAYER_1)
    bot2 = Player(PLAYER_2)

    while True:
        print_board(board)
        i,j = bot1.play(board) if act == PLAYER_1 else bot2.play(board)
        board.place_piece(i,j,act)
        act = PLAYER_2 if act == PLAYER_1 else PLAYER_1
        print_board(board)
        if board.check_connection(PLAYER_1):
            clear_console()
            print(f"\n--> Gana el jugador {RED}rojo{RESET}.")
            print_path(board,PLAYER_1)
            break
        if board.check_connection(PLAYER_2):
            clear_console()
            print(f"\n--> Gana el jugador {BLUE}azul{RESET}.")
            board.pretty_print()
            print_path(board,PLAYER_2)
            break
        
def print_path(board,player_id):
    N = board.size
    _,parent = board.bfs(player_id)
    last = (0,N) if player_id is PLAYER_1 else (N,0)
    q = [parent[last]]
    while q:
        v = q.pop()
        if parent[v] is not None:
            q.append(parent[v])
            x,y = v
            board.board[x][y] = 'R' if player_id == PLAYER_1 else 'B'
    print_board(board,msg=f'\n--> Gana el jugador {RED + 'rojo' if player_id == PLAYER_1 else BLUE + 'azul'}{RESET}.')
# endregion


choice = game_selection()
match(choice):
    case 1: human_vs_human()
    case 2: human_vs_ai()
    case 3: ai_vs_ai()
