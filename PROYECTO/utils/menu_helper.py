import os
import sys
from datetime import datetime

class MenuHelper:
    def __init__(self):
        """Inicializar helper del menú"""
        self.datos_estudiante = {
            'nombre': 'Wilson Manuel Santos Ajcot',  
            'carnet': '201907179',            
            'curso': 'Introducción a la Programación y Computación 2',
            'Seccion': 'P',
            'proyecto': 'Proyecto 1 - Agricultura de Precisión',
            'Repositorio': 'https://github.com/WilsonJrSantos/IPC2_Proyecto1_201907179',
            'fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

    def mostrar_datos_estudiante(self):
        """Mostrar información del estudiante"""
        print("\n" + "="*70)
        print("INFORMACIÓN DEL ESTUDIANTE")
        print("="*70)
        print("Nombre: {}".format(self.datos_estudiante['nombre']))
        print("Carnet: {}".format(self.datos_estudiante['carnet']))
        print("Curso: {}".format(self.datos_estudiante['curso']))
        print("Sección: {}".format(self.datos_estudiante['Seccion']))
        print("Proyecto: {}".format(self.datos_estudiante['proyecto']))
        print("Repositorio: {}".format(self.datos_estudiante['Repositorio']))
        print("Fecha de consulta: {}".format(self.datos_estudiante['fecha']))
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
                print("Error: El nombre del archivo no puede estar vacío. ❌")
                continue

            if not nombre_archivo.endswith('.xml'):
                nombre_archivo += '.xml'

            # Construir la ruta completa y normalizarla
            ruta_completa = os.path.join(ruta_directorio, nombre_archivo)
            ruta_completa = os.path.normpath(ruta_completa)
            
            print(f"\nUsando la ruta completa: {ruta_completa}")

            if tipo_operacion.lower() == 'carga':
                if os.path.exists(ruta_completa):
                    print("Archivo encontrado. ✅")
                    return ruta_completa
                else:
                    print(f"Error: El archivo no existe en la ruta especificada. {ruta_completa} ❌")
                    continuar = input("¿Desea intentar con otra ruta? (s/n): ").lower()
                    if continuar != 's':
                        return None
            else:  # Operación de guardado
                try:
                    # Crear el directorio si no existe
                    os.makedirs(os.path.dirname(ruta_completa), exist_ok=True)
                    print("Directorio verificado/creado. ✅")
                    return ruta_completa
                except Exception as e:
                    print(f"Error al crear el directorio: {e} ❌")
                    continuar = input("¿Desea intentar con otra ruta? (s/n): ").lower()
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
        
        # Mensajes amigables para errores comunes
        mensajes_amigables = {
            'FileNotFoundError': "El archivo especificado no fue encontrado",
            'PermissionError': "No tiene permisos para acceder al archivo",
            'XMLParseError': "El archivo XML tiene errores de formato",
            'ValueError': "Los datos ingresados no tienen el formato correcto",
            'IndexError': "Error accediendo a los datos (índice fuera de rango)",
            'KeyError': "Falta información requerida en los datos",
            'MemoryError': "No hay suficiente memoria para completar la operación"
        }
        
        mensaje_amigable = mensajes_amigables.get(tipo_error, "Error desconocido")
        
        print("Tipo de error: {}".format(tipo_error))
        print("Descripción: {}".format(mensaje_amigable))
        print("Detalle técnico: {}".format(mensaje_error))
        print("="*50)
        
        # Sugerencias de solución
        self._mostrar_sugerencias_error(tipo_error)
        
        self.pausar_pantalla()

    def _mostrar_sugerencias_error(self, tipo_error):
        """Mostrar sugerencias para resolver errores comunes"""
        sugerencias = {
            'FileNotFoundError': [
                "Verifique que la ruta del archivo sea correcta",
                "Asegúrese de que el archivo existe en la ubicación especificada",
                "Revise los permisos de la carpeta"
            ],
            'PermissionError': [
                "Ejecute el programa como administrador si es necesario",
                "Verifique que no tenga el archivo abierto en otro programa",
                "Revise los permisos de escritura en la carpeta de destino"
            ],
            'XMLParseError': [
                "Verifique la sintaxis del archivo XML",
                "Asegúrese de que todas las etiquetas estén cerradas correctamente",
                "Revise que el archivo no esté corrupto"
            ],
            'ValueError': [
                "Verifique que los números ingresados sean válidos",
                "Revise el formato de los datos en el archivo XML",
                "Asegúrese de que no haya caracteres especiales no válidos"
            ]
        }
        
        if tipo_error in sugerencias:
            print("\n💡 Sugerencias para resolver el problema:")
            for i, sugerencia in enumerate(sugerencias[tipo_error], 1):
                print("   {}. {}".format(i, sugerencia))

    def confirmar_accion(self, mensaje):
        """Solicitar confirmación para acciones importantes"""
        print("\n" + " " + mensaje)
        respuesta = input("¿Desea continuar? (s/n): ").lower().strip()
        return respuesta in ['s', 'si', 'sí', 'y', 'yes']

    def mostrar_resumen_optimizacion(self, resultado_optimizacion):
        """Mostrar resumen de resultados de optimización"""
        if not resultado_optimizacion:
            print("No hay resultados de optimización para mostrar")
            return
        
        print("\n" + "="*60)
        print("RESUMEN DE OPTIMIZACIÓN")
        print("="*60)
        
        campo = resultado_optimizacion.get('campo_optimizado')
        if campo:
            print("Campo: {}".format(campo.get_nombre()))
        
        # Estadísticas de estaciones
        estaciones_original = resultado_optimizacion.get('estaciones_original', 0)
        estaciones_optimizada = resultado_optimizacion.get('estaciones_optimizada', 0)
        porcentaje_ahorro = resultado_optimizacion.get('porcentaje_ahorro', 0)
        
        print("\nEstadísticas de Estaciones:")
        print("   Estaciones originales: {}".format(estaciones_original))
        print("   Estaciones optimizadas: {}".format(estaciones_optimizada))
        print("   Estaciones eliminadas: {}".format(estaciones_original - estaciones_optimizada))
        print("   Ahorro logrado: {:.2f}%".format(porcentaje_ahorro))
        
        # Información de grupos
        grupos = resultado_optimizacion.get('grupos_estaciones')
        if grupos:
            print("\n🔗 Información de Grupos:")
            print("   Total de grupos formados: {}".format(grupos.obtener_tamaño()))
            
            grupos_lista = grupos.recorrer()
            for i, grupo in enumerate(grupos_lista):
                indices = grupo.recorrer()
                print("   Grupo {}: {} estaciones (índices: {})".format(
                    i + 1, len(indices), ', '.join(map(str, indices))
                ))
        
        # Matrices generadas
        print("\nMatrices Generadas:")
        matrices_info = [
            ('Frecuencias Suelo Original', resultado_optimizacion.get('matriz_freq_suelo_original')),
            ('Frecuencias Cultivo Original', resultado_optimizacion.get('matriz_freq_cultivo_original')),
            ('Patrones Suelo', resultado_optimizacion.get('matriz_patron_suelo')),
            ('Patrones Cultivo', resultado_optimizacion.get('matriz_patron_cultivo'))
        ]
        
        for nombre, matriz in matrices_info:
            if matriz:
                print("   {} [{}x{}]".format(nombre, matriz.get_filas(), matriz.get_columnas()))
            else:
                print("   {} (no disponible)".format(nombre))
        
        matrices_reducidas = resultado_optimizacion.get('matrices_reducidas')
        if matrices_reducidas:
            for tipo in ['suelo', 'cultivo']:
                matriz = matrices_reducidas.get(tipo)
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
        if os.name == 'nt':  # Windows
            os.system('cls')
        else:  # Unix/Linux/MacOS
            os.system('clear')

    def mostrar_mensaje_exito(self, mensaje):
        """Mostrar mensaje de éxito"""
        print("\n{}".format(mensaje))

    def mostrar_mensaje_advertencia(self, mensaje):
        """Mostrar mensaje de advertencia"""
        print("\n {}".format(mensaje))

    def mostrar_mensaje_info(self, mensaje):
        """Mostrar mensaje informativo"""
        print("\n💡 {}".format(mensaje))

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
            return self.confirmar_accion("¿Desea sobrescribirlo?")
        return True

    def mostrar_tiempo_ejecucion(self, tiempo_inicio, tiempo_fin):
        """Mostrar tiempo de ejecución de una operación"""
        tiempo_transcurrido = tiempo_fin - tiempo_inicio
        print("⏱️ Tiempo de ejecución: {:.2f} segundos".format(tiempo_transcurrido))

    def validar_archivo_xml(self, ruta_archivo):
        """Validar que el archivo sea XML y exista"""
        if not os.path.exists(ruta_archivo):
            return False, "El archivo no existe"
        
        if not ruta_archivo.lower().endswith('.xml'):
            return False, "El archivo debe tener extensión .xml"
        
        try:
            # Verificar que el archivo se pueda leer
            with open(ruta_archivo, 'r', encoding='utf-8') as f:
                contenido = f.read(100)  # Leer primeros 100 caracteres
                if not contenido.strip().startswith('<?xml') and not contenido.strip().startswith('<'):
                    return False, "El archivo no parece ser un XML válido"
        except Exception as e:
            return False, "Error leyendo archivo: {}".format(str(e))
        
        return True, "Archivo XML válido"