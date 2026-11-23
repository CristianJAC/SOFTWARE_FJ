"""Servicio de reserva de salas."""
from modelos.servicio import Servicio
from excepciones.errores import DatosInvalidosError, ServicioNoDisponibleError

class ServicioSala(Servicio):
    def __init__(self, identificador, nombre, tarifa_por_hora, horas_maximas=12):
        super().__init__(identificador, nombre, tarifa_por_hora)
        self.horas_maximas = horas_maximas

    def validar_disponibilidad(self, unidades):
        if not isinstance(unidades, (int, float)) or unidades <= 0 or unidades > self.horas_maximas:
            raise ServicioNoDisponibleError(f"La sala admite entre 1 y {self.horas_maximas} horas por reserva.")
        return True

    def calcular_costo(self, unidades=1, descuento=0):
        self.validar_disponibilidad(unidades)
        if not 0 <= descuento <= 100:
            raise DatosInvalidosError("El descuento debe estar entre 0 y 100 %.")
        return self.tarifa * unidades * (1 - descuento / 100)

    def describir(self):
        return f"Sala: {self.nombre} | ${self.tarifa:,.2f}/hora | máximo {self.horas_maximas} horas"
