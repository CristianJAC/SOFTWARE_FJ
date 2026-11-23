"""Gestor del sistema: administra listas en memoria y registro de eventos."""
import logging
from excepciones.errores import ClienteError, ServicioError, ReservaError
from modelos.reserva import Reserva

class SistemaGestor:
    def __init__(self):
        self.clientes = []
        self.servicios = []
        self.reservas = []
        logging.info("Sistema gestor iniciado.")

    def registrar_cliente(self, cliente):
        if any(c.identificador == cliente.identificador for c in self.clientes):
            raise ClienteError(f"Ya existe el cliente {cliente.identificador}.")
        self.clientes.append(cliente)
        logging.info("Cliente registrado: %s", cliente.identificador)
        return cliente

    def registrar_servicio(self, servicio):
        if any(s.identificador == servicio.identificador for s in self.servicios):
            raise ServicioError(f"Ya existe el servicio {servicio.identificador}.")
        self.servicios.append(servicio)
        logging.info("Servicio registrado: %s", servicio.identificador)
        return servicio

    def buscar_cliente(self, identificador):
        for cliente in self.clientes:
            if cliente.identificador == identificador:
                return cliente
        raise ClienteError(f"No se encontró cliente {identificador}.") from LookupError(f"Identificador {identificador} no localizado en la lista interna.")

    def buscar_servicio(self, identificador):
        for servicio in self.servicios:
            if servicio.identificador == identificador:
                return servicio
        raise ServicioError(f"No se encontró servicio {identificador}.")

    # Método flexible con parámetros opcionales: emula sobrecarga por cantidad de argumentos.
    def crear_reserva(self, id_reserva, id_cliente, id_servicio, unidades=1, descuento=0):
        cliente = self.buscar_cliente(id_cliente)
        servicio = self.buscar_servicio(id_servicio)
        servicio.validar_disponibilidad(unidades)
        reserva = Reserva(id_reserva, cliente, servicio, unidades)
        if descuento:
            reserva.costo = servicio.calcular_costo(unidades, descuento)
        if any(r.identificador == id_reserva for r in self.reservas):
            raise ReservaError(f"Ya existe la reserva {id_reserva}.")
        self.reservas.append(reserva)
        logging.info("Reserva creada: %s", id_reserva)
        return reserva

    def confirmar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        reserva.confirmar()
        logging.info("Reserva confirmada: %s", identificador)
        return reserva

    def cancelar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        reserva.cancelar()
        logging.info("Reserva cancelada: %s", identificador)
        return reserva

    def procesar_reserva(self, identificador):
        reserva = self.buscar_reserva(identificador)
        reserva.procesar()
        logging.info("Reserva procesada: %s", identificador)
        return reserva

    def buscar_reserva(self, identificador):
        for reserva in self.reservas:
            if reserva.identificador == identificador:
                return reserva
        raise ReservaError(f"No se encontró reserva {identificador}.")

    def listar_reservas(self):
        return [r.describir() for r in self.reservas]
