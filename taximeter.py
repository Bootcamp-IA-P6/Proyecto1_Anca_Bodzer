# taximetro.py
# Taxímetro CLI - Nivel Esencial (con tarifa inicial de arranque)

import time

# Tarifas por segundo
STOPPED_RATE = 0.02    # 0.02 € / s (parado)
MOVING_RATE = 0.05     # 0.05 € / s (en movimiento)

# Tarifa inicial de arranque (se cobra por inicio de trayecto)
BASE_FARE = 2.00       # 2 euros

def calculate_fare(seconds_stopped, seconds_moving, base_fare=0.0):
    """
    Calcula la tarifa total en euros y devuelve un desglose:
      - total: suma de base_fare + stopped_cost + moving_cost
      - stopped_cost: coste por tiempo parado
      - moving_cost: coste por tiempo en movimiento
      - base_fare: tarifa de arranque pasada como argumento
    """
    stopped_cost = seconds_stopped * STOPPED_RATE
    moving_cost = seconds_moving * MOVING_RATE
    total = base_fare + stopped_cost + moving_cost
    return total, stopped_cost, moving_cost, base_fare

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
            print(f"Trayecto iniciado. Estado inicial: 'stopped' (parado). Tarifa de arranque: €{BASE_FARE:.2f} aplicada.")

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

            # calculamos la tarifa incluyendo la tarifa inicial
            total, stopped_cost, moving_cost, base = calculate_fare(stopped_time, moving_time, base_fare=BASE_FARE)

            print("\n--- Resumen del trayecto ---")
            print(f"Tarifa de arranque: €{base:.2f}")
            print(f"Tiempo parado: {stopped_time:.1f} segundos")
            print(f"Tiempo en movimiento: {moving_time:.1f} segundos")
            print(f"Coste por tiempo parado: €{stopped_cost:.2f}")
            print(f"Coste por tiempo en movimiento: €{moving_cost:.2f}")
            print(f"----------------------------")
            print(f"Total a pagar: €{total:.2f}")
            print("----------------------------\n")

            # dejamos el programa listo para un nuevo trayecto
            trip_active = False
            state = None

        elif command == "exit":
            print("¡Hasta luego!👋")
            break

        else:
            print("Comando desconocido. Usa: start, stop, move, finish o exit")

if __name__ == "__main__":
    taximeter()

