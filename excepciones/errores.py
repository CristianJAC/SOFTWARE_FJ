"""Jerarquía de excepciones específicas del proyecto."""
class SoftwareFJError(Exception):
    """Excepción base para errores controlados del sistema."""

class DatosInvalidosError(SoftwareFJError):
    pass

class ClienteError(SoftwareFJError):
    pass

class ServicioError(SoftwareFJError):
    pass

class ServicioNoDisponibleError(ServicioError):
    pass

class ReservaError(SoftwareFJError):
    pass
