import os
import copy
import time
import random
from colorama import init, Fore, Back, Style

# 0 -> NO hay barco
# 1 -> SI hay barco
# 2 -> Tiro fallido
# 3 -> Tiro efectivo

TABLERO_BASE = [
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0],
        [0, 0, 0, 0 ,0]
    ]

VACIO = [-1, -1]

NUMEROS_A_LETRAS = ['A', 'B', 'C', 'D', 'E']

LETRAS_A_NUMEROS = {
    'A': 0,
    'B': 1,
    'C': 2,
    'D': 3,
    'E': 4,
}

NUMERO_A_EMOJI = ["🌊", "🚢", "❌", "🔥"]

def coord_a_pos (coords: str):
    coords = coords.capitalize()
    if len(coords) != 2:
        print("Coordenada Inválida")
        return VACIO
    letra, numero = [coord for coord in coords]
    numero = int(numero) - 1
    if not(letra in LETRAS_A_NUMEROS):
        print(Fore.RED+"Coordenada Inválida:"+Style.RESET_ALL)
        return VACIO
    if numero > 4:
        print("Coordenada Inválida:")
        return VACIO
    
    posicion = [LETRAS_A_NUMEROS[letra], numero]

    return posicion

def limpiar_consola ():
    os.system('cls' if os.name == "nt" else 'clear')

def print_separator ():
    print("------------------------------")

def graficar_tablero (tablero: list):
    print_separator()
    print("|   | A  | B  | C  | D  | E  |")
    contador = 0
    for n in range(len(tablero)):
        fila = tablero[n]
        print_separator()
        fila_str = f"| {n + 1} | "
        contador += 1
        for casilla in fila:
            fila_str += NUMERO_A_EMOJI[casilla] + " | "
        print(fila_str)
    print_separator()

def coords_aleatoria ():
    x = random.randrange(5)
    y = random.randrange(5)
    return [x,y]

def guardar_tablero (jugador: int): 
    if jugador != 1 and jugador != 2:
        print("Número de jugador no válido")
        return tablero

    tablero = copy.deepcopy(TABLERO_BASE)
    confirmar = False

    while not(confirmar):
        print(f"Jugador {jugador} elige posiciones:")
        aleatorio = input("Barcos aleatorios? (s/n): ")

        for n in range(5):
            posicion = [-1,-1]
            while (posicion[0] == -1):
                if aleatorio == "s":
                    posicion = coords_aleatoria()
                    valor_previo = tablero[posicion[1]][posicion[0]]
                    while valor_previo != 0:
                        posicion = coords_aleatoria()
                        valor_previo = tablero[posicion[1]][posicion[0]]
                else:
                    coordenada = input(f"Jugador {jugador} - Barco {n + 1}°: ")
                    posicion = coord_a_pos(coordenada)
                    valor_previo = tablero[posicion[1]][posicion[0]]
                    if valor_previo == 1 and aleatorio != "s":
                        posicion = VACIO
                        print("Coordenada inválida, ya hay un barco en esa coordenada")

            x,y = posicion
            tablero[y][x] = 1

        print(f"Barcos Jugador {jugador}:")
        graficar_tablero(tablero)

        confirmacion = input("Confirmar selección: (s/n): ")
        if confirmacion != "s":
            tablero = copy.deepcopy(TABLERO_BASE)
        else:
            confirmar = True

    return tablero

def siguiente_jugador (segundos: int):
    for n in range(segundos):
        limpiar_consola()
        print(n + 1)
        time.sleep(1)

def main ():
    ESPERA = 3
    limpiar_consola()
    tablero1 = guardar_tablero(1)
    siguiente_jugador(ESPERA)
    tablero2 = guardar_tablero(2)
    siguiente_jugador(ESPERA)
    # Tableros de los jugadores
    tableros = [tablero1, tablero2]
    # Tableros enemigos de los jugadores
    tableros_oculto = [copy.deepcopy(TABLERO_BASE),copy.deepcopy(TABLERO_BASE)]
    barcos = [5,5]
    turno_jugador = 0


    while barcos[0] > 0 and barcos[1] > 0:
        print(f"Turno del Jugador {turno_jugador + 1}")
        posicion = [-1,-1]
        while (posicion[0] == -1):
            print("Tablero enemigo:")
            graficar_tablero(tableros_oculto[turno_jugador])
            coordenada = input(f"Coordenadas de ataque: ")
            posicion = coord_a_pos(coordenada)
            y,x = posicion

            turno_jugador_enemigo = 1 if turno_jugador == 0 else 0
            valor = tableros[turno_jugador_enemigo][x][y]

            if valor == 0:
                print("Tiro fallido:")
                tableros_oculto[turno_jugador][x][y] = 2
                
            elif valor == 1:
                print("Tiro acertado")
                tableros[turno_jugador_enemigo][x][y] = 3
                tableros_oculto[turno_jugador][x][y] = 3
                barcos[turno_jugador_enemigo] = barcos[turno_jugador_enemigo] - 1

                
            elif valor == 2 or valor == 3:
                print("Ya disparaste en esa coordenada, intenta otra vez")

            limpiar_consola()
            graficar_tablero(tableros_oculto[turno_jugador])
            if valor == 0:
                time.sleep(3)
                turno_jugador = 1 if turno_jugador == 0 else 0
                siguiente_jugador(ESPERA)
            limpiar_consola()

    ganador = -1
    if barcos[0] == 0:
        ganador = 2
    elif barcos[1] == 0:
        ganador = 1


    print(f"Ganó el Jugador {ganador}")
        
main()
