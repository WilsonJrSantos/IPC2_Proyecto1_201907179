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
from procesadores.optimizador import Optimizador

class SistemaOptimizacionAgricola:
    """Clase principal del sistema de optimización agrícola"""
    
    def __init__(self):
        """Inicializar el sistema"""
        self.xml_handler = XMLHandler()
        self.menu_helper = MenuHelper()
        self.optimizador = Optimizador()
                
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
            
            ruta_archivo = self.menu_helper.solicitar_ruta_archivo('carga')
            if not ruta_archivo:
                self.menu_helper.mostrar_mensaje_advertencia("Operación cancelada")
                return
            
            valido, mensaje = self.menu_helper.validar_archivo_xml(ruta_archivo)
            if not valido:
                self.menu_helper.mostrar_mensaje_error(mensaje)
                return
            
            self.menu_helper.mostrar_progreso_carga("Cargando archivo XML...")
            tiempo_inicio = time.time()
            
            self.campos_cargados = self.xml_handler.cargar_archivo(ruta_archivo)
            
            tiempo_fin = time.time()
            print(" Completado")
            
            if self.campos_cargados.esta_vacia():
                self.menu_helper.mostrar_mensaje_error("No se cargaron campos del archivo")
                return
            
            self.mostrar_resumen_carga()
            self.archivo_carga = ruta_archivo
            
            self.menu_helper.mostrar_tiempo_ejecucion(tiempo_inicio, tiempo_fin)
            self.menu_helper.mostrar_mensaje_exito("Archivo cargado exitosamente")
            
        except Exception as e:
            self.menu_helper.manejar_errores(e, "Carga de Archivo")

    def mostrar_campos_disponibles(self):
        """Mostrar lista de campos disponibles para optimizar"""
        print("\nCAMPOS DISPONIBLES PARA OPTIMIZACIÓN:")
        
        # Usar el iterador de la lista personalizada ---
        campos_iterador = self.campos_cargados.crear_iterador()
        i = 1
        while campos_iterador.hay_siguiente():
            campo = campos_iterador.siguiente()
            print("   {}. {} ({} estaciones)".format(
                i, campo.get_nombre(), campo.obtener_cantidad_estaciones()
            ))
            i += 1

    def procesar_archivo(self):
        # ...
        # Verificar que haya campos cargados
        if self.campos_cargados.esta_vacia():
            self.menu_helper.mostrar_mensaje_advertencia("Primero debe cargar un archivo XML")
            return
        
        # Mostrar campos disponibles
        self.mostrar_campos_disponibles()
        
        # Seleccionar campo a optimizar
        if self.campos_cargados.obtener_tamaño() == 1:
            campo_seleccionado = self.campos_cargados.obtener_en_posicion(0)
            print("Procesando único campo: {}".format(campo_seleccionado.get_nombre()))
        else:
            indice = self.solicitar_seleccion_campo()
            if indice == -1:
                return
            campo_seleccionado = self.campos_cargados.obtener_en_posicion(indice)
        
        # Confirmar optimización
        mensaje = "Se iniciará la optimización del campo '{}'".format(campo_seleccionado.get_nombre())
        if not self.menu_helper.confirmar_accion(mensaje):
            self.menu_helper.mostrar_mensaje_info("Optimización cancelada")
            return
        
        # Ejecutar optimización
        self.menu_helper.mostrar_separador("EJECUTANDO OPTIMIZACIÓN")
        tiempo_inicio = time.time()
        
        resultado = self.optimizador.optimizar_estaciones(campo_seleccionado)
        
        tiempo_fin = time.time()
        
        if resultado:
            # Asumiendo que 'resultado' es una instancia de la clase Diccionario
            resultado.insertar('campo_original', campo_seleccionado)
            self.resultados_optimizacion.insertar(resultado)
            
            self.menu_helper.mostrar_tiempo_ejecucion(tiempo_inicio, tiempo_fin)
            self.menu_helper.mostrar_resumen_optimizacion(resultado)
            self.menu_helper.mostrar_mensaje_exito("Optimización completada exitosamente")
        else:
            self.menu_helper.mostrar_mensaje_error("Error en el proceso de optimización")
            


    def escribir_archivo_salida(self):
        """Opción 3: Escribir Archivo de salida XML"""
        try:
            self.menu_helper.mostrar_separador("ESCRIBIR ARCHIVO DE SALIDA")
            
            # Verificar que haya resultados de optimización
            if self.resultados_optimizacion.esta_vacia():
                self.menu_helper.mostrar_mensaje_advertencia("Primero debe procesar un archivo para generar resultados")
                return
            
            # Solicitar ruta de archivo de salida
            ruta_salida = self.menu_helper.solicitar_ruta_archivo('salida')
            if not ruta_salida:
                self.menu_helper.mostrar_mensaje_advertencia("Operación cancelada")
                return
            
            # Verificar sobrescritura
            if not self.menu_helper.obtener_confirmacion_sobrescritura(ruta_salida):
                self.menu_helper.mostrar_mensaje_info("Operación cancelada")
                return
            
            # Crear lista de campos optimizados usando un iterador para evitar listas nativas
            campos_optimizados = Lista()
            resultados_iterador = self.resultados_optimizacion.crear_iterador()
            
            while resultados_iterador.hay_siguiente():
                resultado = resultados_iterador.siguiente()
                campo_opt = resultado.obtener('campo_optimizado')
                if campo_opt:
                    campos_optimizados.insertar(campo_opt)
            
            # Escribir archivo
            self.menu_helper.mostrar_progreso_carga("Escribiendo archivo XML...")
            tiempo_inicio = time.time()
            
            exito = self.xml_handler.escribir_archivo_salida(ruta_salida, campos_optimizados)
            
            tiempo_fin = time.time()
            print("Completado")
            
            if exito:
                self.archivo_salida = ruta_salida
                self.menu_helper.mostrar_tiempo_ejecucion(tiempo_inicio, tiempo_fin)
                self.menu_helper.mostrar_mensaje_exito("Archivo guardado: {}".format(ruta_salida))
            else:
                self.menu_helper.mostrar_mensaje_error("Error escribiendo archivo de salida")
            
        except Exception as e:
            self.menu_helper.manejar_errores(e, "Escritura de Archivo")


    def mostrar_datos_estudiante(self):
        """Opción 4: Mostrar datos del estudiante"""
        self.menu_helper.mostrar_datos_estudiante()

    def generar_graficas(self):
        """Opción 5: Generar gráficas con Graphviz"""
        print("Función aún no implementada")

    def salir_sistema(self):
        """Opción 6: Salir del sistema"""
        self.menu_helper.mostrar_separador("SALIR DEL SISTEMA")
        print("Gracias por usar el Sistema de Optimización Agrícola")
        
        if not self.resultados_optimizacion.esta_vacia():
            print("\nResumen de la sesión:")
            # Usar el método de tamaño de la Lista personalizada
            print("   - Campos procesados: {}".format(self.resultados_optimizacion.obtener_tamaño()))
            if self.archivo_carga:
                print("   - Archivo de entrada: {}".format(self.archivo_carga))
            if self.archivo_salida:
                print("   - Archivo de salida: {}".format(self.archivo_salida))
        
        print("\n¡Hasta pronto! 🌾")
        sys.exit(0)

    def mostrar_resumen_carga(self):
        """Mostrar resumen de los campos cargados"""
        print("\n RESUMEN DE CARGA:")
        
        # Usar el iterador de la lista personalizada ---
        campos_iterador = self.campos_cargados.crear_iterador()
        i = 1
        while campos_iterador.hay_siguiente():
            campo = campos_iterador.siguiente()
            print("   Campo {}: {}".format(i, campo.get_nombre()))
            print("      - ID: {}".format(campo.get_id()))
            print("      - Estaciones: {}".format(campo.obtener_cantidad_estaciones()))
            print("      - Sensores de suelo: {}".format(campo.obtener_cantidad_sensores_suelo()))
            print("      - Sensores de cultivo: {}".format(campo.obtener_cantidad_sensores_cultivo()))
            i += 1
            
    # Esta función debe ser un método de la clase ---
    def solicitar_seleccion_campo(self):
        """Solicita al usuario que seleccione un campo de la lista"""
        while True:
            try:
                opcion = int(input("Ingrese el número del campo a procesar (o 0 para cancelar): "))
                if opcion == 0:
                    return -1
                
                # Obtener el tamaño de la lista personalizada
                if 1 <= opcion <= self.campos_cargados.obtener_tamaño():
                    return opcion - 1
                else:
                    self.menu_helper.mostrar_mensaje_advertencia("Opción no válida. Ingrese un número de la lista.")
            except ValueError:
                self.menu_helper.mostrar_mensaje_error("Entrada no válida. Ingrese un número entero.")

if __name__ == "__main__":
    # Punto de entrada principal del programa
    sistema = SistemaOptimizacionAgricola() 
    sistema.ejecutar()