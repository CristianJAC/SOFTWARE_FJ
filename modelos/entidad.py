"""Clase abstracta que representa una entidad identificable."""
from abc import ABC, abstractmethod

class Entidad(ABC):
    def __init__(self, identificador):
        if not isinstance(identificador, str) or not identificador.strip():
            raise ValueError("El identificador debe ser un texto no vacío.")
        self._identificador = identificador.strip()

    @property
    def identificador(self):
        return self._identificador

    @abstractmethod
    def describir(self):
        """Devuelve una descripción de la entidad."""
        raise NotImplementedError
