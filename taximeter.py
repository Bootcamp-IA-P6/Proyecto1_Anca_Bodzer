
# taximetro.py
# Taxímetro CLI - Nivel Esencial

import time

# 0.02 € = 2 céntimos por segundo (parado)
# 0.05 € = 5 céntimos por segundo (en movimiento)
STOPPED_RATE = 0.02
MOVING_RATE = 0.05

def calculate_fare(seconds_stopped, seconds_moving):
    """
    Calcula la tarifa total en euros.
    - seconds_stopped: segundos totales en los que el taxi estuvo parado
    - seconds_moving: segundos totales en los que el taxi estuvo en movimiento
    """
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    # imprimimos el total con 2 decimales al final del trayecto
    return fare

def taximeter():
    """
    Interfaz CLI del taxímetro.
    Comandos: start, stop, move, finish, exit
    """
    print("========================================")
    print("     👋 BIENVENIDO AL TAXÍMETRO F5 🚕      ")
    print("========================================")
    print("Comandos disponibles: 'start', 'stop', 'move', 'finish', 'exit'\n")

    trip_active = False
    stopped_time = 0.0
    moving_time = 0.0
    state = None
    state_start_time = 0.0

    while True:
        command = input("> ").strip().lower()

        if command == "start":
            if trip_active:
                print("Error: ya hay un trayecto en curso.")
                continue
            trip_active = True
            stopped_time = 0.0
            moving_time = 0.0
            state = "stopped"  # asumimos que empieza parado
            state_start_time = time.time()
            print("Trayecto iniciado. Estado inicial: 'stopped' (parado).")

        elif command in ("stop", "move"):
            if not trip_active:
                print("Error: no hay trayecto activo. Usa 'start' primero.")
                continue

            # medimos cuánto tiempo duró el estado anterior
            duration = time.time() - state_start_time

            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration

            # actualizamos el estado al nuevo pedido por el usuario
            state = "stopped" if command == "stop" else "moving"
            state_start_time = time.time()
            print(f"Estado cambiado a '{state}'. (Se añadieron {duration:.1f} s al estado anterior)")

        elif command == "finish":
            if not trip_active:
                print("Error: no hay trayecto activo para finalizar.")
                continue

            # agregamos el tiempo desde el inicio del estado actual hasta finish
            duration = time.time() - state_start_time
            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration

            total = calculate_fare(stopped_time, moving_time)

            print("\n--- Resumen del trayecto ---")
            print(f"Tiempo parado: {stopped_time:.1f} segundos")
            print(f"Tiempo en movimiento: {moving_time:.1f} segundos")
            print(f"Total a pagar: €{total:.2f}")
            print("----------------------------\n")

            # dejamos el programa listo para un nuevo trayecto
            trip_active = False
            state = None

        elif command == "exit":
            print("Good bye!👋")
            break

        else:
            print("Comando desconocido. Usa: start, stop, move, finish o exit")

if __name__ == "__main__":
    taximeter()
