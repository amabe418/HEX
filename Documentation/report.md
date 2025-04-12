# Documentación del Proyecto Hex Game

## Resumen Ejecutivo

Este documento proporciona una documentación completa del proyecto de implementación del juego Hex, incluyendo la arquitectura del sistema, la lógica del juego, y la inteligencia artificial que controla al jugador computacional. El proyecto consiste en dos componentes principales: el tablero del juego (HexBoard) y la inteligencia artificial del jugador (Player), que utiliza el algoritmo minimax con poda alfa-beta.

## Índice

- [Documentación del Proyecto Hex Game](#documentación-del-proyecto-hex-game)
  - [Resumen Ejecutivo](#resumen-ejecutivo)
  - [Índice](#índice)
  - [Introducción al Juego Hex](#introducción-al-juego-hex)
  - [Arquitectura del Sistema](#arquitectura-del-sistema)
  - [Clase HexBoard](#clase-hexboard)
    - [Atributos Principales](#atributos-principales)
    - [Métodos Clave](#métodos-clave)
    - [Algoritmo de Búsqueda de Caminos](#algoritmo-de-búsqueda-de-caminos)
  - [Clase Player](#clase-player)
    - [Atributos Principales](#atributos-principales-1)
    - [Métodos Clave](#métodos-clave-1)
  - [Algoritmo Minimax con Poda Alfa-Beta](#algoritmo-minimax-con-poda-alfa-beta)
  - [Función de Evaluación](#función-de-evaluación)
    - [Factores Clave](#factores-clave)
    - [Cálculo de la Puntuación](#cálculo-de-la-puntuación)
  - [Optimizaciones Implementadas](#optimizaciones-implementadas)
  - [Posibles Mejoras Futuras](#posibles-mejoras-futuras)
  - [Conclusiones](#conclusiones)

## Introducción al Juego Hex

Hex es un juego de estrategia para dos jugadores que se juega en un tablero romboidal de celdas hexagonales. El tablero tiene forma de diamante y típicamente tiene 11×11 celdas, aunque puede ser de cualquier tamaño. Los jugadores alternan para colocar fichas de su color en celdas vacías, con los siguientes objetivos:

- El jugador Rojo (jugador 1) busca formar un camino conectado de este a oeste.
- El jugador Azul (jugador 2) busca formar un camino conectado de norte a sur.

Una característica importante de Hex es que nunca puede terminar en empate, siempre hay un ganador. Además, existe una prueba matemática de que el primer jugador tiene una estrategia ganadora, aunque para tableros grandes esta estrategia óptima es desconocida en la práctica.

## Arquitectura del Sistema

El sistema está compuesto por dos clases principales:

1. **HexBoard**: Implementa el tablero de juego y sus reglas.

2. **Smart_Player**: Implementa la inteligencia artificial que decide los movimientos y hereda de la clase **Player**

Esta arquitectura permite la separación clara entre la lógica del juego y la estrategia de la IA, facilitando su desarrollo y mantenimiento independientes.

## Clase HexBoard

La clase HexBoard es el núcleo del juego y proporciona las siguientes funcionalidades:

### Atributos Principales

- `size`: Tamaño N del tablero (N×N)
- `board`: Matriz NumPy N×N que representa el estado del tablero (0=vacío, 1=Jugador1, 2=Jugador2)

### Métodos Clave

- `clone()`: Crea una copia del tablero para simular movimientos futuros.
- `place_piece(row, col, player_id)`: Coloca una ficha del jugador en la posición especificada.
- `remove_piece(row, col)`: Elimina una ficha de la posición especificada.
- `get_possible_moves()`: Devuelve todas las casillas vacías como posibles movimientos.
- `get_relevant_moves(radius)`: Devuelve movimientos relevantes cercanos a fichas existentes.
- `check_connection(player_id)`: Verifica si el jugador ha conectado sus dos lados (condición de victoria).
- `heuristic_value_dijkstra(player_id)`: Calcula la menor distancia para conectar los extremos usando el algoritmo de Dijkstra.
- `adj(row, col, id)`: Devuelve las casillas adyacentes a una posición dada.
- `pretty_print()`: Imprime el tablero en la consola con colores para mejor visualización.

### Algoritmo de Búsqueda de Caminos

La implementación utiliza el algoritmo de Dijkstra para calcular la distancia mínima entre los bordes correspondientes a cada jugador. Esta información es crucial para la evaluación heurística de la posición.

## Clase Player

La clase Player implementa la inteligencia artificial que decide los mejores movimientos para el juego.

### Atributos Principales

- `player_id`: Identificador del jugador (1 para Rojo, 2 para Azul)
- `opponent_id`: Identificador del oponente (calculado como 3 - player_id)
- `transposition_table`: Tabla que almacena posiciones evaluadas previamente para evitar recalcular

### Métodos Clave

- `play(board)`: Determina y devuelve el mejor movimiento para la posición actual.
- `evaluate(board)`: Evalúa la posición actual desde la perspectiva del jugador.
- `minimax(board, alpha, beta, maximizing, depth)`: Implementa el algoritmo minimax con poda alfa-beta.

## Algoritmo Minimax con Poda Alfa-Beta

El algoritmo minimax es un método de toma de decisiones utilizado en juegos de suma cero con dos jugadores. La implementación en este proyecto incluye:

1. **Búsqueda recursiva**: Explora el árbol de juego hasta una profundidad predeterminada.
2. **Poda alfa-beta**: Optimiza la búsqueda eliminando ramas que no afectarán la decisión final.
3. **Tabla de transposición**: Evita recalcular posiciones ya evaluadas.
4. **Ordenamiento de movimientos**: Mejora la eficiencia de la poda alfa-beta al evaluar primero los movimientos más prometedores.

El pseudocódigo básico del algoritmo implementado es:

```
function minimax(board, alpha, beta, maximizing, depth):
    if depth == 0 or game_over(board):
        return evaluate(board)
    
    if maximizing:
        value = -∞
        for each move in possible_moves(board):
            apply_move(board, move)
            value = max(value, minimax(board, alpha, beta, false, depth-1))
            undo_move(board, move)
            alpha = max(alpha, value)
            if beta <= alpha:
                break  // Beta cut-off
        return value
    else:
        value = +∞
        for each move in possible_moves(board):
            apply_move(board, move)
            value = min(value, minimax(board, alpha, beta, true, depth-1))
            undo_move(board, move)
            beta = min(beta, value)
            if beta <= alpha:
                break  // Alpha cut-off
        return value
```

## Función de Evaluación

La función de evaluación es crucial para el rendimiento de la IA, ya que determina la valoración de cada posición del tablero. La implementación actual considera:

### Factores Clave

1. **Distancia del camino mínimo**: Diferencia entre la longitud del camino más corto del jugador y del oponente.
2. **Detección de victoria/derrota inmediata**: Valores extremos para posiciones ganadas o perdidas.
3. **Control territorial**: Evaluación de la posición de las piezas en el tablero.
4. **Progreso direccional**: Valoración del avance en la dirección objetivo (este-oeste para Rojo, norte-sur para Azul).
5. **Conectividad**: Evaluación de la conexión entre piezas del mismo color.

### Cálculo de la Puntuación

La puntuación final combina los factores anteriores con diferentes pesos:

```
score = (path_length_difference * weight_1) + (territory_control * weight_2)
```

donde `territory_control` incorpora factores como la posición central, el progreso direccional y la conectividad.

## Optimizaciones Implementadas

Para mejorar el rendimiento y la calidad de juego, se han implementado las siguientes optimizaciones:

1. **Movimiento inicial óptimo**: Jugar cerca del centro en el primer movimiento.
2. **Detección de amenazas inmediatas**: Identificar y bloquear movimientos ganadores del oponente.
3. **Movimientos relevantes**: Priorizar celdas cercanas a piezas existentes.
4. **Profundidad adaptativa**: Ajustar la profundidad de búsqueda según el tamaño del tablero.
5. **Ordenamiento de movimientos**: Evaluar primero los movimientos más prometedores.
6. **Tabla de transposición**: Evitar recalcular posiciones idénticas.
7. **Terminación temprana**: Detectar condiciones de victoria o derrota sin explorar todo el árbol.

## Posibles Mejoras Futuras

A pesar de las optimizaciones implementadas, existen varias áreas de mejora potencial:

1. **Patrones de juego**: Incorporar reconocimiento de patrones comunes en Hex.
2. **Aprendizaje automático**: Utilizar técnicas de aprendizaje para mejorar la función de evaluación.
3. **Búsqueda Monte Carlo**: Implementar algoritmos MCTS (Monte Carlo Tree Search) para mejorar la exploración.
4. **Paralelización**: Dividir la búsqueda en múltiples hilos para mayor eficiencia.
5. **Base de datos de aperturas**: Incorporar movimientos de apertura conocidos.
6. **Análisis de conectividad virtual**: Evaluar conexiones potenciales además de las existentes.

## Conclusiones

La implementación actual del juego Hex proporciona una base sólida para un jugador de IA competente. El uso del algoritmo minimax con poda alfa-beta, combinado con una función de evaluación específica para Hex, permite a la IA tomar decisiones estratégicas efectivas.

Las optimizaciones implementadas mejoran significativamente tanto el rendimiento computacional como la calidad de juego, permitiendo una experiencia fluida incluso en tableros de tamaño moderado.

El proyecto demuestra cómo los principios de la teoría de juegos y la búsqueda heurística pueden aplicarse para crear inteligencias artificiales efectivas en juegos de estrategia.

---

Documento preparado el 11 de abril de 2025.