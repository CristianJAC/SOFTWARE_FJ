"""Reserva que relaciona cliente, servicio, unidades y estado."""
from modelos.entidad import Entidad
from excepciones.errores import ReservaError

class Reserva(Entidad):
    ESTADOS = ("Pendiente", "Confirmada", "Cancelada", "Procesada")

    def __init__(self, identificador, cliente, servicio, unidades):
        super().__init__(identificador)
        if cliente is None or servicio is None:
            raise ReservaError("La reserva debe asociar cliente y servicio.")
        servicio.validar_disponibilidad(unidades)
        self.cliente = cliente
        self.servicio = servicio
        self.unidades = unidades
        self.estado = "Pendiente"
        self.costo = servicio.calcular_costo(unidades)
        self._inventario_apartado = False

    def confirmar(self):
        if self.estado != "Pendiente":
            raise ReservaError("Solo se pueden confirmar reservas pendientes.")
        if hasattr(self.servicio, "reservar_inventario"):
            self.servicio.reservar_inventario(self.unidades)
            self._inventario_apartado = True
        self.estado = "Confirmada"

    def cancelar(self):
        if self.estado not in ("Pendiente", "Confirmada"):
            raise ReservaError("Esta reserva no se puede cancelar en su estado actual.")
        if self._inventario_apartado and hasattr(self.servicio, "liberar_inventario"):
            self.servicio.liberar_inventario(self.unidades)
            self._inventario_apartado = False
        self.estado = "Cancelada"

    def procesar(self):
        if self.estado != "Confirmada":
            raise ReservaError("Solo se pueden procesar reservas confirmadas.")
        self.estado = "Procesada"

    def describir(self):
        return (f"Reserva {self.identificador}: {self.cliente.nombre} -> {self.servicio.nombre}; "
                f"unidades={self.unidades}, costo=${self.costo:,.2f}, estado={self.estado}")
