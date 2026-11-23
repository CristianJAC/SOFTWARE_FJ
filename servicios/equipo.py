"""Servicio de alquiler de equipos con control básico de inventario."""
from modelos.servicio import Servicio
from excepciones.errores import DatosInvalidosError, ServicioNoDisponibleError

class ServicioEquipo(Servicio):
    def __init__(self, identificador, nombre, tarifa_por_unidad, inventario):
        super().__init__(identificador, nombre, tarifa_por_unidad)
        if not isinstance(inventario, int) or inventario < 0:
            raise DatosInvalidosError("El inventario debe ser un entero no negativo.")
        self.inventario = inventario
        self.disponibles = inventario

    def validar_disponibilidad(self, unidades):
        if not isinstance(unidades, int) or unidades <= 0:
            raise DatosInvalidosError("La cantidad de equipos debe ser un entero positivo.")
        if unidades > self.disponibles:
            raise ServicioNoDisponibleError(f"Solo hay {self.disponibles} unidades disponibles.")
        return True

    def reservar_inventario(self, unidades):
        self.validar_disponibilidad(unidades)
        self.disponibles -= unidades

    def liberar_inventario(self, unidades):
        self.disponibles = min(self.inventario, self.disponibles + unidades)

    def calcular_costo(self, unidades=1, descuento=0):
        if not isinstance(unidades, int) or unidades <= 0:
            raise DatosInvalidosError("La cantidad de equipos debe ser un entero positivo.")
        if not 0 <= descuento <= 100:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 100 %.")
        return self.tarifa * unidades * (1 - descuento / 100)

    def describir(self):
        return f"Equipo: {self.nombre} | ${self.tarifa:,.2f}/unidad | disponibles {self.disponibles}/{self.inventario}"
