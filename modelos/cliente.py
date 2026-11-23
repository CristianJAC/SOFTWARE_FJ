"""Modelo Cliente con datos encapsulados y validación."""
from .entidad import Entidad
from excepciones.errores import DatosInvalidosError

class Cliente(Entidad):
    def __init__(self, identificador, nombre, correo, telefono):
        super().__init__(identificador)
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self.__nombre
    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise DatosInvalidosError("El nombre debe tener al menos dos caracteres.")
        self.__nombre = valor.strip()

    @property
    def correo(self):
        return self.__correo
    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or "@" not in valor or "." not in valor.split("@")[-1]:
            raise DatosInvalidosError("El correo no tiene un formato válido.")
        self.__correo = valor.strip().lower()

    @property
    def telefono(self):
        return self.__telefono
    @telefono.setter
    def telefono(self, valor):
        digits = "".join(ch for ch in str(valor) if ch.isdigit())
        if len(digits) < 7:
            raise DatosInvalidosError("El teléfono debe contener al menos siete dígitos.")
        self.__telefono = str(valor).strip()

    def describir(self):
        return f"Cliente {self.identificador}: {self.nombre} ({self.correo})"
