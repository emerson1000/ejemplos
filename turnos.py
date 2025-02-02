import datetime

class Turno:
    def __init__(self, cliente, fecha_hora):
        self.cliente = cliente
        self.fecha_hora = fecha_hora

class Agenda:
    def __init__(self):
        self.turnos = []

    def agregar_turno(self, cliente, fecha_hora):
        nuevo_turno = Turno(cliente, fecha_hora)
        self.turnos.append(nuevo_turno)
        print(f"Turno agregado para {cliente} el {fecha_hora}")

    def mostrar_turnos(self):
        for turno in self.turnos:
            print(f"Cliente: {turno.cliente}, Fecha y Hora: {turno.fecha_hora}")

    def eliminar_turno(self, cliente, fecha_hora):
        self.turnos = [turno for turno in self.turnos if not (turno.cliente == cliente and turno.fecha_hora == fecha_hora)]
        print(f"Turno eliminado para {cliente} el {fecha_hora}")

# Ejemplo de uso
agenda = Agenda()
agenda.agregar_turno("Juan Perez", datetime.datetime(2023, 10, 15, 10, 30))
agenda.agregar_turno("Maria Lopez", datetime.datetime(2023, 10, 15, 11, 0))
agenda.mostrar_turnos()
agenda.eliminar_turno("Juan Perez", datetime.datetime(2023, 10, 15, 10, 30))
agenda.mostrar_turnos()
