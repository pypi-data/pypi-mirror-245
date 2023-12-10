import os
import time

class Cop:
    def __init__(self, path):
        self.path = path
        self.modificaciones_previas = None

    def prev_revision(self):
        self.modificaciones_previas = self._revisar_modificaciones()

    def post_revision(self, print_output=True):
        modificaciones_actuales = self._revisar_modificaciones()
        archivos_modificados = self._comparar_modificaciones(modificaciones_actuales)
        if print_output:
            self._print(archivos_modificados)

    def _revisar_modificaciones(self):
        modificaciones = {}
        if os.path.isfile(self.path):
            tiempo_modificacion = os.path.getmtime(self.path)
            modificaciones[os.path.basename(self.path)] = tiempo_modificacion
        elif os.path.isdir(self.path):
            for archivo in os.listdir(self.path):
                ruta_completa = os.path.join(self.path, archivo)
                if os.path.isfile(ruta_completa):
                    tiempo_modificacion = os.path.getmtime(ruta_completa)
                    modificaciones[archivo] = tiempo_modificacion
        return modificaciones

    def _comparar_modificaciones(self, modificaciones_actuales):
        archivos_modificados = []
        for archivo, tiempo_modificacion in modificaciones_actuales.items():
            if archivo in self.modificaciones_previas and tiempo_modificacion != self.modificaciones_previas[archivo]:
                tiempo_pasado = time.time() - tiempo_modificacion
                archivos_modificados.append((archivo, tiempo_pasado))
        return archivos_modificados

    def _print(self, archivos_modificados):
        if os.path.isfile(self.path):
            if len(archivos_modificados) > 0:
                archivo, tiempo = archivos_modificados[0]
                print(f"{archivo} modified {tiempo:.2f} seconds ago.")
            else:
                print(f"No modifications in {self.path}")
        else:
            if len(archivos_modificados) != 0:
                print(f'Modified files in {self.path}:')
                for archivo, tiempo in archivos_modificados:
                    print(f"{archivo}, {tiempo:.2f} seconds ago.")
            else:
                print(f"No file was modified in {self.path}")