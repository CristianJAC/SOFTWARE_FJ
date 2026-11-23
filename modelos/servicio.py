"""Clase abstracta de servicios y validación compartida."""
from abc import ABC, abstractmethod
from modelos.entidad import Entidad
from excepciones.errores import DatosInvalidosError

class Servicio(Entidad, ABC):
    def __init__(self, identificador, nombre, tarifa):
        super().__init__(identificador)
        if not isinstance(nombre, str) or not nombre.strip():
            raise DatosInvalidosError("El nombre del servicio no puede estar vacío.")
        if not isinstance(tarifa, (int, float)) or tarifa <= 0:
            raise DatosInvalidosError("La tarifa debe ser un número positivo.")
        self.nombre = nombre.strip()
        self.tarifa = float(tarifa)

    @abstractmethod
    def calcular_costo(self, unidades=1, descuento=0):
        """Calcula el costo según el tipo de servicio."""
        raise NotImplementedError

    @abstractmethod
    def validar_disponibilidad(self, unidades):
        raise NotImplementedError

    def describir(self):
        return f"{self.nombre} | tarifa base: ${self.tarifa:,.2f}"
