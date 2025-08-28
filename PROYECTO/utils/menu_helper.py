import os
import sys
from datetime import datetime

# Importar la clase Diccionario y Lista 
from clases.diccionario import Diccionario
from clases.lista import Lista

class MenuHelper:
    def __init__(self):
        """Inicializar helper del menú"""
        # Usar Diccionario personalizado para datos_estudiante ---
        self.datos_estudiante = Diccionario()
        self.datos_estudiante.insertar('nombre', 'Wilson Manuel Santos Ajcot')
        self.datos_estudiante.insertar('carnet', '201907179')
        self.datos_estudiante.insertar('curso', 'Introducción a la Programación y Computación 2')
        self.datos_estudiante.insertar('Seccion', 'P')
        self.datos_estudiante.insertar('proyecto', 'Proyecto 1 - Agricultura de Precisión')
        self.datos_estudiante.insertar('Repositorio', 'https://github.com/WilsonJrSantos/IPC2_Proyecto1_201907179')
        self.datos_estudiante.insertar('fecha', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def mostrar_datos_estudiante(self):
        """Mostrar información del estudiante"""
        print("\n" + "="*70)
        print("INFORMACIÓN DEL ESTUDIANTE")
        print("="*70)
        # Acceder a los datos con el método obtener() ---
        print("Nombre: {}".format(self.datos_estudiante.obtener('nombre')))
        print("Carnet: {}".format(self.datos_estudiante.obtener('carnet')))
        print("Curso: {}".format(self.datos_estudiante.obtener('curso')))
        print("Sección: {}".format(self.datos_estudiante.obtener('Seccion')))
        print("Proyecto: {}".format(self.datos_estudiante.obtener('proyecto')))
        print("Repositorio: {}".format(self.datos_estudiante.obtener('Repositorio')))
        print("Fecha de consulta: {}".format(self.datos_estudiante.obtener('fecha')))
        print("="*70)
        
        self.pausar_pantalla()

    def solicitar_ruta_archivo(self, tipo_operacion):
        """
        Solicita al usuario la ruta y el nombre de un archivo,
        gestionando la carga del archivo.
        """
        print("\n" + "-" * 50)
        print("SOLICITUD DE ARCHIVO - {}".format(tipo_operacion.upper()))
        print("-" * 50)

        # Usamos cadenas, no diccionarios
        directorio_sugerido = "archivos/entrada" if tipo_operacion.lower() == 'carga' else "archivos/salida"
        descripcion_ruta = "a cargar" if tipo_operacion.lower() == 'carga' else "donde guardar"
        
        while True:
            print(f"\nIngrese la ruta del directorio {descripcion_ruta}:")
            print(f"Sugerencia: {directorio_sugerido}")
            ruta_directorio = input("Ruta del directorio: ").strip() or directorio_sugerido
            
            print(f"Ingrese el nombre del archivo {descripcion_ruta}:")
            print(f"Ejemplo: {'campo_agricola.xml' if tipo_operacion.lower() == 'carga' else 'campo_optimizado.xml'}")
            nombre_archivo = input("Nombre del archivo: ").strip()

            if not nombre_archivo:
                self.mostrar_mensaje_error("Error: El nombre del archivo no puede estar vacío.")
                continue

            if not nombre_archivo.endswith('.xml'):
                nombre_archivo += '.xml'

            ruta_completa = os.path.join(ruta_directorio, nombre_archivo)
            ruta_completa = os.path.normpath(ruta_completa)
            
            print(f"\nUsando la ruta completa: {ruta_completa}")

            if tipo_operacion.lower() == 'carga':
                if os.path.exists(ruta_completa):
                    print("Archivo encontrado. .")
                    return ruta_completa
                else:
                    self.mostrar_mensaje_error(f"Error: El archivo no existe en la ruta especificada. {ruta_completa}")
                    continuar = input("Desea intentar con otra ruta? (s/n): ").lower()
                    if continuar != 's':
                        return None
            else:
                try:
                    os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
                    print("Directorio verificado/creado. .")
                    return ruta_completa
                except Exception as e:
                    self.mostrar_mensaje_error(f"Error al crear el directorio: {e}")
                    continuar = input("Desea intentar con otra ruta? (s/n): ").lower()
                    if continuar != 's':
                        return None

    def mostrar_progreso_carga(self, mensaje):
        """Mostrar mensajes de progreso durante carga"""
        print("{}".format(mensaje), end="")
        sys.stdout.flush()

    def mostrar_progreso_procesamiento(self, paso_actual, total_pasos):
        """Mostrar progreso durante procesamiento"""
        porcentaje = (paso_actual / total_pasos) * 100
        barra_longitud = 30
        barra_completa = int((paso_actual / total_pasos) * barra_longitud)
        barra_vacia = barra_longitud - barra_completa
        
        barra = "[" + "█" * barra_completa + "░" * barra_vacia + "]"
        print("\rProcesando: {} {:.1f}% ({}/{})".format(
            barra, porcentaje, paso_actual, total_pasos
        ), end="")
        sys.stdout.flush()
        
        if paso_actual == total_pasos:
            print("\nProcesamiento completado!")

    def validar_entrada_usuario(self, entrada, tipo_esperado):
        """Validar entrada del usuario"""
        try:
            if tipo_esperado == 'int':
                return int(entrada.strip())
            elif tipo_esperado == 'float':
                return float(entrada.strip())
            elif tipo_esperado == 'str':
                return entrada.strip()
            elif tipo_esperado == 'bool':
                entrada_lower = entrada.lower().strip()
                return entrada_lower in ['s', 'si', 'sí', 'y', 'yes', 'true', '1']
            else:
                return entrada.strip()
        except ValueError:
            return None

    def manejar_errores(self, excepcion, contexto):
        """Manejar y mostrar errores de manera amigable"""
        print("\n" + "="*50)
        print("ERROR EN: {}".format(contexto.upper()))
        print("="*50)
        
        tipo_error = type(excepcion).__name__
        mensaje_error = str(excepcion)
        
        # Usar Diccionario personalizado para mensajes ---
        mensajes_amigables = Diccionario()
        mensajes_amigables.insertar('FileNotFoundError', "El archivo especificado no fue encontrado")
        mensajes_amigables.insertar('PermissionError', "No tiene permisos para acceder al archivo")
        mensajes_amigables.insertar('XMLParseError', "El archivo XML tiene errores de formato")
        mensajes_amigables.insertar('ValueError', "Los datos ingresados no tienen el formato correcto")
        mensajes_amigables.insertar('IndexError', "Error accediendo a los datos (índice fuera de rango)")
        mensajes_amigables.insertar('KeyError', "Falta información requerida en los datos")
        mensajes_amigables.insertar('MemoryError', "No hay suficiente memoria para completar la operación")
        
        # Usar el método obtener() para acceder al valor ---
        mensaje_amigable = mensajes_amigables.obtener(tipo_error)
        if mensaje_amigable is None:
            mensaje_amigable = "Error desconocido"
        
        print("Tipo de error: {}".format(tipo_error))
        print("Descripción: {}".format(mensaje_amigable))
        print("Detalle técnico: {}".format(mensaje_error))
        print("="*50)
        
        # Sugerencias de solución
        self._mostrar_sugerencias_error(tipo_error)
        
        self.pausar_pantalla()

    def _mostrar_sugerencias_error(self, tipo_error):
        """Mostrar sugerencias para resolver errores comunes"""
        # Usar Diccionario y Lista personalizados para las sugerencias ---
        sugerencias_dict = Diccionario()
        
        file_not_found = Lista()
        file_not_found.insertar("Verifique que la ruta del archivo sea correcta")
        file_not_found.insertar("Asegúrese de que el archivo existe en la ubicación especificada")
        file_not_found.insertar("Revise los permisos de la carpeta")
        sugerencias_dict.insertar('FileNotFoundError', file_not_found)
        
        permission_error = Lista()
        permission_error.insertar("Ejecute el programa como administrador si es necesario")
        permission_error.insertar("Verifique que no tenga el archivo abierto en otro programa")
        permission_error.insertar("Revise los permisos de escritura en la carpeta de destino")
        sugerencias_dict.insertar('PermissionError', permission_error)
        
        xml_parse_error = Lista()
        xml_parse_error.insertar("Verifique la sintaxis del archivo XML")
        xml_parse_error.insertar("Asegúrese de que todas las etiquetas estén cerradas correctamente")
        xml_parse_error.insertar("Revise que el archivo no esté corrupto")
        sugerencias_dict.insertar('XMLParseError', xml_parse_error)

        value_error = Lista()
        value_error.insertar("Verifique que los números ingresados sean válidos")
        value_error.insertar("Revise el formato de los datos en el archivo XML")
        value_error.insertar("Asegúrese de que no haya caracteres especiales no válidos")
        sugerencias_dict.insertar('ValueError', value_error)
        
        # Acceder a la lista de sugerencias con el método obtener() ---
        sugerencias_lista = sugerencias_dict.obtener(tipo_error)
        
        if sugerencias_lista:
            print("\nSugerencias para resolver el problema:")
            # Usar el iterador de la Lista personalizada ---
            sugerencias_iterador = sugerencias_lista.crear_iterador()
            i = 1
            while sugerencias_iterador.hay_siguiente():
                sugerencia = sugerencias_iterador.siguiente()
                print("   {}. {}".format(i, sugerencia))
                i += 1

    def confirmar_accion(self, mensaje):
        """Solicitar confirmación para acciones importantes"""
        print("\n" + " " + mensaje)
        respuesta = input("Desea continuar? (s/n): ").lower().strip()
        return respuesta in ['s', 'si', 'sí', 'y', 'yes']

    def mostrar_resumen_optimizacion(self, resultado_optimizacion):
        """Mostrar resumen de resultados de optimización"""
        # Se asume que resultado_optimizacion es un objeto Diccionario
        if not resultado_optimizacion.obtener_tamaño() > 0:
            print("No hay resultados de optimización para mostrar")
            return
        
        print("\n" + "="*60)
        print("RESUMEN DE OPTIMIZACIÓN")
        print("="*60)
        
        # Acceder a los valores con el método obtener() ---
        campo = resultado_optimizacion.obtener('campo_optimizado')
        if campo:
            print("Campo: {}".format(campo.get_nombre()))
        
        # Estadísticas de estaciones
        estaciones_original = resultado_optimizacion.obtener('estaciones_original')
        estaciones_optimizada = resultado_optimizacion.obtener('estaciones_optimizada')
        porcentaje_ahorro = resultado_optimizacion.obtener('porcentaje_ahorro')
        
        print("\nEstadísticas de Estaciones:")
        print("   Estaciones originales: {}".format(estaciones_original))
        print("   Estaciones optimizadas: {}".format(estaciones_optimizada))
        print("   Estaciones eliminadas: {}".format(estaciones_original - estaciones_optimizada))
        print("   Ahorro logrado: {:.2f}%".format(porcentaje_ahorro))
        
        # Información de grupos
        grupos = resultado_optimizacion.obtener('grupos_estaciones')
        if grupos:
            print("\nInformación de Grupos:")
            print("   Total de grupos formados: {}".format(grupos.obtener_tamaño()))
            
            # Usar el iterador de la Lista personalizada ---
            grupos_iterador = grupos.crear_iterador()
            i = 1
            while grupos_iterador.hay_siguiente():
                grupo = grupos_iterador.siguiente()
                # Usar el iterador y el método de tamaño de la Lista ---
                print("   Grupo {}: {} estaciones (índices: {})".format(
                    i, grupo.obtener_tamaño(), self._formato_lista_str(grupo)
                ))
                i += 1
        
        # Matrices generadas
        print("\nMatrices Generadas:")
        # Usar una lista personalizada para las matrices ---
        matrices_info = Lista()
        matrices_info.insertar(Diccionario())
        matrices_info.obtener_en_posicion(0).insertar('nombre', 'Frecuencias Suelo Original')
        matrices_info.obtener_en_posicion(0).insertar('matriz', resultado_optimizacion.obtener('matriz_freq_suelo_original'))
        matrices_info.insertar(Diccionario())
        matrices_info.obtener_en_posicion(1).insertar('nombre', 'Frecuencias Cultivo Original')
        matrices_info.obtener_en_posicion(1).insertar('matriz', resultado_optimizacion.obtener('matriz_freq_cultivo_original'))
        matrices_info.insertar(Diccionario())
        matrices_info.obtener_en_posicion(2).insertar('nombre', 'Patrones Suelo')
        matrices_info.obtener_en_posicion(2).insertar('matriz', resultado_optimizacion.obtener('matriz_patron_suelo'))
        matrices_info.insertar(Diccionario())
        matrices_info.obtener_en_posicion(3).insertar('nombre', 'Patrones Cultivo')
        matrices_info.obtener_en_posicion(3).insertar('matriz', resultado_optimizacion.obtener('matriz_patron_cultivo'))
        
        # Iterar sobre la lista de diccionarios ---
        matrices_iterador = matrices_info.crear_iterador()
        while matrices_iterador.hay_siguiente():
            info = matrices_iterador.siguiente()
            nombre = info.obtener('nombre')
            matriz = info.obtener('matriz')
            if matriz:
                print("   {} [{}x{}]".format(nombre, matriz.get_filas(), matriz.get_columnas()))
            else:
                print("   {} (no disponible)".format(nombre))

        matrices_reducidas = resultado_optimizacion.obtener('matrices_reducidas')
        if matrices_reducidas:
            # Usar un iterador sobre las claves del diccionario ---
            tipos_iterador = matrices_reducidas.obtener_claves().crear_iterador()
            while tipos_iterador.hay_siguiente():
                tipo = tipos_iterador.siguiente()
                matriz = matrices_reducidas.obtener(tipo)
                if matriz:
                    print("   Reducida {} [{}x{}]".format(
                        tipo.title(), matriz.get_filas(), matriz.get_columnas()
                    ))
        
        print("="*60)
        self.pausar_pantalla()

    def mostrar_menu_principal(self):
        """Mostrar el menú principal del sistema"""
        print("\n" + "="*60)
        print(" SISTEMA DE OPTIMIZACIÓN AGRÍCOLA")
        print("="*60)
        print("1. Cargar Archivo XML")
        print("2. Procesar Archivo (Optimización)")
        print("3. Escribir Archivo de Salida XML")
        print("4. Mostrar Datos del Estudiante")
        print("5. Generar Gráficas con Graphviz")
        print("6. Salir del Sistema")
        print("="*60)

    def solicitar_opcion_menu(self, min_opcion=1, max_opcion=6):
        """Solicitar opción del menú al usuario"""
        while True:
            try:
                opcion = input("Seleccione una opción (1-{}): ".format(max_opcion)).strip()
                opcion_int = int(opcion)
                
                if min_opcion <= opcion_int <= max_opcion:
                    return opcion_int
                else:
                    print("Por favor, ingrese un número entre {} y {}".format(min_opcion, max_opcion))
                    
            except ValueError:
                print("Por favor, ingrese un número válido")

    def pausar_pantalla(self):
        """Pausar la ejecución hasta que el usuario presione Enter"""
        input("\nPresione Enter para continuar...")

    def limpiar_pantalla(self):
        """Limpiar la pantalla de la consola"""
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

    def mostrar_mensaje_exito(self, mensaje):
        """Mostrar mensaje de éxito"""
        print("\n{}".format(mensaje))

    def mostrar_mensaje_advertencia(self, mensaje):
        """Mostrar mensaje de advertencia"""
        print("\n {}".format(mensaje))

    def mostrar_mensaje_info(self, mensaje):
        """Mostrar mensaje informativo"""
        print("\n{}".format(mensaje))

    def mostrar_mensaje_error(self, mensaje):
        """Mostrar mensaje de error"""
        print("\n{}".format(mensaje))

    def mostrar_separador(self, titulo=""):
        """Mostrar separador visual"""
        if titulo:
            print("\n" + "="*20 + " {} ".format(titulo.upper()) + "="*20)
        else:
            print("\n" + "-"*50)

    def obtener_confirmacion_sobrescritura(self, ruta_archivo):
        """Obtener confirmación para sobrescribir archivo existente"""
        if os.path.exists(ruta_archivo):
            print("\n El archivo ya existe: {}".format(ruta_archivo))
            return self.confirmar_accion("Desea sobrescribirlo?")
        return True

    def mostrar_tiempo_ejecucion(self, tiempo_inicio, tiempo_fin):
        """Mostrar tiempo de ejecución de una operación"""
        tiempo_transcurrido = tiempo_fin - tiempo_inicio
        print("Tiempo de ejecución: {:.2f} segundos".format(tiempo_transcurrido))

    def validar_archivo_xml(self, ruta_archivo):
        """Validar que el archivo sea XML y exista"""
        if not os.path.exists(ruta_archivo):
            return False, "El archivo no existe"
        
        if not ruta_archivo.lower().endswith('.xml'):
            return False, "El archivo debe tener extensión .xml"
        
        try:
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read(100)
                if not contenido.strip().startswith('<?xml') and not contenido.strip().startswith('<'):
                    return False, "El archivo no parece ser un XML válido"
        except Exception as e:
            return False, "Error leyendo archivo: {}".format(str(e))
        
        return True, "Archivo XML válido"

    # ---  MÉTODO HELPER para dar formato a una lista como string ---
    def _formato_lista_str(self, lista_custom):
        """Formatea una lista personalizada en una cadena de texto"""
        resultado = ""
        iterador = lista_custom.crear_iterador()
        primera_iteracion = True
        while iterador.hay_siguiente():
            if not primera_iteracion:
                resultado += ", "
            resultado += str(iterador.siguiente())
            primera_iteracion = False
        return resultado