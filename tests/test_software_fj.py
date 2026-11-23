"""Pruebas automatizadas básicas usando unittest (sin librerías externas)."""
import unittest
from modelos.cliente import Cliente
from servicios.sala import ServicioSala
from servicios.equipo import ServicioEquipo
from servicios.asesoria import ServicioAsesoria
from gestor.sistema_gestor import SistemaGestor
from excepciones.errores import DatosInvalidosError, ServicioNoDisponibleError, ReservaError

class SoftwareFJTests(unittest.TestCase):
    def setUp(self):
        self.g = SistemaGestor()
        self.c = self.g.registrar_cliente(Cliente("C1", "Test Usuario", "test@example.com", "3001234567"))
        self.sala = self.g.registrar_servicio(ServicioSala("S1", "Sala", 100))
        self.eq = self.g.registrar_servicio(ServicioEquipo("S2", "Equipo", 20, 3))
        self.ases = self.g.registrar_servicio(ServicioAsesoria("S3", "Asesoría", 50))

    def test_cliente_validacion(self):
        with self.assertRaises(DatosInvalidosError):
            Cliente("C2", "A", "mal", "123")

    def test_sala_coste_y_limite(self):
        self.assertEqual(self.sala.calcular_costo(2), 200)
        with self.assertRaises(ServicioNoDisponibleError):
            self.sala.calcular_costo(20)

    def test_equipo_reserva_liberacion(self):
        r = self.g.crear_reserva("R1", "C1", "S2", 2)
        r.confirmar()
        self.assertEqual(self.eq.disponibles, 1)
        r.cancelar()
        self.assertEqual(self.eq.disponibles, 3)

    def test_inventario_insuficiente(self):
        with self.assertRaises(ServicioNoDisponibleError):
            self.g.crear_reserva("R1", "C1", "S2", 4)

    def test_reserva_estados(self):
        r = self.g.crear_reserva("R1", "C1", "S1", 2)
        with self.assertRaises(ReservaError):
            r.procesar()
        r.confirmar()
        r.procesar()
        self.assertEqual(r.estado, "Procesada")

    def test_descuento(self):
        self.assertEqual(self.ases.calcular_costo(2, 10), 90)

if __name__ == "__main__":
    unittest.main()
