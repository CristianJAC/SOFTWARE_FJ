"""Punto de entrada del proyecto. Ejecutar: python main.py"""
import logging
from modelos.cliente import Cliente
from servicios.sala import ServicioSala
from servicios.equipo import ServicioEquipo
from servicios.asesoria import ServicioAsesoria
from gestor.sistema_gestor import SistemaGestor
from excepciones.errores import SoftwareFJError

logging.basicConfig(filename="software_fj.log", level=logging.INFO,
                    format="%(asctime)s | %(levelname)s | %(message)s", encoding="utf-8")


def ejecutar_operacion(etiqueta, funcion):
    """Ejecuta una demostración y captura errores para que el programa continúe."""
    print(f"\n--- {etiqueta} ---")
    try:
        resultado = funcion()
    except SoftwareFJError as error:
        print(f"Error controlado: {error}")
        logging.exception("Error controlado durante %s", etiqueta)
    except Exception as error:
        print(f"Error inesperado: {error}")
        logging.exception("Error inesperado durante %s", etiqueta)
    else:
        if resultado is not None:
            print(resultado)
    finally:
        print("Operación finalizada.")


def demo():
    sistema = SistemaGestor()
    # 1-3: alta de clientes, incluyendo un intento inválido.
    ejecutar_operacion("1. Crear cliente válido", lambda: sistema.registrar_cliente(Cliente("C001", "Ana Torres", "ana@example.com", "3001234567")).describir())
    ejecutar_operacion("2. Crear segundo cliente", lambda: sistema.registrar_cliente(Cliente("C002", "Luis Pérez", "luis@example.com", "3101234567")).describir())
    ejecutar_operacion("3. Cliente con correo inválido", lambda: Cliente("C003", "Cliente Prueba", "correo-invalido", "3001234567"))
    # 4-6: registrar servicios de tres tipos.
    ejecutar_operacion("4. Registrar sala", lambda: sistema.registrar_servicio(ServicioSala("S001", "Sala de reuniones", 80000)).describir())
    ejecutar_operacion("5. Registrar equipos", lambda: sistema.registrar_servicio(ServicioEquipo("S002", "Proyector", 50000, 5)).describir())
    ejecutar_operacion("6. Registrar asesoría", lambda: sistema.registrar_servicio(ServicioAsesoria("S003", "Consultoría de software", 120000)).describir())
    # 7-10: reservas válidas y aplicación de descuentos.
    ejecutar_operacion("7. Reserva de sala", lambda: sistema.crear_reserva("R001", "C001", "S001", 3).describir())
    ejecutar_operacion("8. Reserva de equipos", lambda: sistema.crear_reserva("R002", "C002", "S002", 2).describir())
    ejecutar_operacion("9. Reserva de asesoría con descuento", lambda: sistema.crear_reserva("R003", "C001", "S003", 2, 10).describir())
    ejecutar_operacion("10. Confirmar reserva de equipos", lambda: sistema.confirmar_reserva("R002").describir())
    # 11-15: validaciones y excepciones de operaciones.
    ejecutar_operacion("11. Intento de exceso de horas", lambda: sistema.crear_reserva("R004", "C001", "S001", 20))
    ejecutar_operacion("12. Reserva de más equipos que inventario", lambda: sistema.crear_reserva("R005", "C001", "S002", 10))
    ejecutar_operacion("13. Buscar cliente inexistente", lambda: sistema.buscar_cliente("C999"))
    ejecutar_operacion("14. Cancelar reserva de equipos y liberar inventario", lambda: sistema.cancelar_reserva("R002").describir())
    ejecutar_operacion("15. Confirmar reserva de sala", lambda: sistema.confirmar_reserva("R001").describir())
    # 16-20: procesar, duplicar, cancelar y listar.
    ejecutar_operacion("16. Procesar reserva confirmada", lambda: sistema.procesar_reserva("R001").describir())
    ejecutar_operacion("17. Intentar procesar reserva pendiente", lambda: sistema.procesar_reserva("R003"))
    ejecutar_operacion("18. Intentar registrar cliente duplicado", lambda: sistema.registrar_cliente(Cliente("C001", "Ana duplicada", "ana2@example.com", "3009876543")))
    ejecutar_operacion("19. Cancelar reserva pendiente", lambda: sistema.cancelar_reserva("R003").describir())
    ejecutar_operacion("20. Listar reservas", lambda: "\n".join(sistema.listar_reservas()))
    ejecutar_operacion("21. Disponibilidad de equipos al cierre", lambda: sistema.buscar_servicio("S002").describir())
    print("\nDemostración terminada. Consulte software_fj.log para el registro de eventos.")

if __name__ == "__main__":
    demo()
