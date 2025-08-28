"""
Sistema de Optimización de Estaciones Base para Agricultura de Precisión
Proyecto 1 - IPC2
"""

import time
import sys
import os

# Importar componentes del sistema
from clases.lista import Lista
from procesadores.xml_handler import XMLHandler
from utils.menu_helper import MenuHelper


class SistemaOptimizacionAgricola:
    """Clase principal del sistema de optimización agrícola"""
    
    def __init__(self):
        """Inicializar el sistema"""
        self.xml_handler = XMLHandler()
        self.menu_helper = MenuHelper()
        
        # Estado del sistema
        self.campos_cargados = Lista()
        self.resultados_optimizacion = Lista()
        self.archivo_carga = None
        self.archivo_salida = None

    def ejecutar(self):
        """Función principal del programa"""
        self.menu_helper.limpiar_pantalla()
        self.mostrar_bienvenida()
        
        while True:
            try:
                self.menu_helper.mostrar_menu_principal()
                opcion = self.menu_helper.solicitar_opcion_menu(1, 6)
                self.procesar_opcion(opcion)
                
            except KeyboardInterrupt:
                print("\n\nSaliendo del sistema...")
                break
            except Exception as e:
                self.menu_helper.manejar_errores(e, "Sistema Principal")

    def mostrar_bienvenida(self):
        """Mostrar mensaje de bienvenida"""
        print("="*60)
        print(" BIENVENIDO AL SISTEMA DE OPTIMIZACIÓN AGRÍCOLA ")
        print("="*60)
        print("Este sistema optimiza la distribución de estaciones base")
        print("para agricultura de precisión usando matrices de frecuencias.")
        print("="*60)
        self.menu_helper.pausar_pantalla()

    def procesar_opcion(self, opcion):
        """Procesar la opción seleccionada por el usuario"""
        if opcion == 1:
            self.cargar_archivo()
        elif opcion == 2:
            self.procesar_archivo()
        elif opcion == 3:
            self.escribir_archivo_salida()
        elif opcion == 4:
            self.mostrar_datos_estudiante()
        elif opcion == 5:
            self.generar_graficas()
        elif opcion == 6:
            self.salir_sistema()

    def cargar_archivo(self):
        """Opción 1: Cargar Archivo XML"""
        try:
            self.menu_helper.mostrar_separador("CARGAR ARCHIVO XML")
            
            # Solicitar ruta del archivo
            ruta_archivo = self.menu_helper.solicitar_ruta_archivo('carga')
            if not ruta_archivo:
                self.menu_helper.mostrar_mensaje_advertencia("Operación cancelada")
                return
            
            # Validar archivo
            valido, mensaje = self.menu_helper.validar_archivo_xml(ruta_archivo)
            if not valido:
                self.menu_helper.mostrar_mensaje_error(mensaje)
                return
            
            # Cargar archivo
            self.menu_helper.mostrar_progreso_carga("Cargando archivo XML...")
            tiempo_inicio = time.time()
            
            self.campos_cargados = self.xml_handler.cargar_archivo(ruta_archivo)
            
            tiempo_fin = time.time()
            print(" Completado")
            
            if self.campos_cargados.esta_vacia():
                self.menu_helper.mostrar_mensaje_error("No se cargaron campos del archivo")
                return
            
            # Mostrar resumen de carga
            self.mostrar_resumen_carga()
            self.archivo_carga = ruta_archivo
            
            self.menu_helper.mostrar_tiempo_ejecucion(tiempo_inicio, tiempo_fin)
            self.menu_helper.mostrar_mensaje_exito("Archivo cargado exitosamente")
            
        except Exception as e:
            self.menu_helper.manejar_errores(e, "Carga de Archivo")

    def procesar_archivo(self):
        """Opción 2: Procesar el Archivo (Optimización)"""
        print("Función aun no implementada")

    def escribir_archivo_salida(self):
        """Opción 3: Escribir Archivo de salida XML"""
        print("Función aun no implementada")

    def mostrar_datos_estudiante(self):
        """Opción 4: Mostrar datos del estudiante"""
        self.menu_helper.mostrar_datos_estudiante()

    def generar_graficas(self):
        """Opción 5: Generar gráficas con Graphviz"""
        print("Función aun no implementada")

    def salir_sistema(self):
        """Opción 6: Salir del sistema"""
        self.menu_helper.mostrar_separador("SALIR DEL SISTEMA")
        print("Gracias por usar el Sistema de Optimización Agrícola")
        
        if not self.resultados_optimizacion.esta_vacia():
            print("\nResumen de la sesión:")
            print("   - Campos procesados: {}".format(self.resultados_optimizacion.obtener_tamaño()))
            if self.archivo_carga:
                print("   - Archivo de entrada: {}".format(self.archivo_carga))
            if self.archivo_salida:
                print("   - Archivo de salida: {}".format(self.archivo_salida))
        
        print("\n🌾 ¡Hasta pronto! 🌾")
        sys.exit(0)

    def mostrar_resumen_carga(self):
        """Mostrar resumen de los campos cargados"""
        print("\n RESUMEN DE CARGA:")
        campos = self.campos_cargados.recorrer()
        
        for i, campo in enumerate(campos):
            print("   Campo {}: {}".format(i + 1, campo.get_nombre()))
            print("      - ID: {}".format(campo.get_id()))
            print("      - Estaciones: {}".format(campo.obtener_cantidad_estaciones()))
            print("      - Sensores de suelo: {}".format(campo.obtener_cantidad_sensores_suelo()))
            print("      - Sensores de cultivo: {}".format(campo.obtener_cantidad_sensores_cultivo()))


if __name__ == "__main__":
# Punto de entrada principal del programa
    sistema = SistemaOptimizacionAgricola() 
    sistema.ejecutar()