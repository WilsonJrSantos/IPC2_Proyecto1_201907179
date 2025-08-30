# utils/graphviz_generator.py
import os
import subprocess
from clases.lista import Lista
from clases.diccionario import Diccionario
from clases.contador import Contador 

class GraphvizGenerator:
    def __init__(self):
        """Inicializar generador de gráficas"""
        self.colores_matriz = Diccionario()
        self.colores_matriz.insertar('frecuencias', '#E8F4FD')
        self.colores_matriz.insertar('patrones', '#FFF2CC')
        self.colores_matriz.insertar('reducida', '#D5E8D4')
        self.directorio_graficas = 'archivos/graficas'

    def generar_grafica_matriz(self, matriz, tipo_matriz, campo_nombre, nombre_archivo, etiquetas_filas=None, etiquetas_columnas=None):
        """Generar gráfica de matriz específica"""
        try:
            if not matriz:
                print("Error: Matriz no disponible para generar gráfica")
                return False

            if not os.path.exists(self.directorio_graficas):
                os.makedirs(self.directorio_graficas)

            dot_content = self._crear_contenido_dot(
                matriz, tipo_matriz, campo_nombre, etiquetas_filas, etiquetas_columnas
            )

            ruta_completa = os.path.join(self.directorio_graficas, nombre_archivo)
            return self.guardar_grafica(dot_content, ruta_completa)

        except Exception as e:
            print(f"Error generando gráfica: {str(e)}")
            return False

    def _crear_contenido_dot(self, matriz, tipo_matriz, campo_nombre, etiquetas_filas, etiquetas_columnas):
        dot_content = f'digraph matriz_{tipo_matriz.replace(" ", "_")} {{\n'
        dot_content += '    rankdir=LR;\n'
        dot_content += '    node [shape=plaintext];\n'
        dot_content += f'    graph [label="{campo_nombre} - {tipo_matriz.title()}", labelloc=t, fontsize=16, fontname="Arial Bold"];\n\n'

        color_fondo = self.colores_matriz.obtener(tipo_matriz.lower().split()[0]) or '#FFFFFF'

        dot_content += '    matriz [label=<\n'
        dot_content += f'        <TABLE BORDER="1" CELLBORDER="1" CELLSPACING="0" BGCOLOR="{color_fondo}">\n'

        if etiquetas_columnas:
            dot_content += '            <TR><TD BGCOLOR="#4472C4"><FONT COLOR="white">&nbsp;</FONT></TD>'
            iterador_columnas = etiquetas_columnas.crear_iterador()
            while iterador_columnas.hay_siguiente():
                etiqueta_obj = iterador_columnas.siguiente()
                etiqueta_id = etiqueta_obj.get_id() if hasattr(etiqueta_obj, 'get_id') else str(etiqueta_obj)
                etiqueta_cortada = self._cortar_string(etiqueta_id, 8)
                dot_content += f'<TD BGCOLOR="#4472C4"><FONT COLOR="white"><B>{etiqueta_cortada}</B></FONT></TD>'
            dot_content += '</TR>\n'

        contador_filas = Contador(0, matriz.get_filas())
        while contador_filas.hay_siguiente():
            i = contador_filas.siguiente()
            fila_datos = matriz.obtener_fila(i)

            etiqueta_fila = f"F{i}"
            if etiquetas_filas and i < etiquetas_filas.obtener_tamaño():
                etiqueta_obj = etiquetas_filas.obtener_en_posicion(i)
                etiqueta_id = etiqueta_obj.get_id() if hasattr(etiqueta_obj, 'get_id') else str(etiqueta_obj)
                etiqueta_fila = self._cortar_string(etiqueta_id, 8)
            
            dot_content += f'            <TR><TD BGCOLOR="#70AD47"><FONT COLOR="white"><B>{etiqueta_fila}</B></FONT></TD>'

            iterador_valores = fila_datos.crear_iterador()
            while iterador_valores.hay_siguiente():
                valor = iterador_valores.siguiente()
                color_celda = self._obtener_color_celda(valor, tipo_matriz)
                dot_content += f'<TD BGCOLOR="{color_celda}">{str(valor)}</TD>'

            dot_content += '</TR>\n'

        dot_content += '        </TABLE>\n'
        dot_content += '>];\n'
        dot_content += '}\n'
        return dot_content

    def _cortar_string(self, texto, longitud):
        """Método auxiliar para simular el slicing de string"""
        if not texto:
            return ""
        
        resultado = ""
        caracteres = Lista()
        for c in texto:
            caracteres.insertar(c)
        
        iterador = caracteres.crear_iterador()
        contador = 0
        while iterador.hay_siguiente() and contador < longitud:
            resultado += iterador.siguiente()
            contador += 1
        return resultado

    def _obtener_color_celda(self, valor, tipo_matriz):
        """Obtener color de celda según el valor y tipo de matriz"""
        if 'patron' in tipo_matriz.lower():
            return '#90EE90' if valor == 1 else '#FFB6C1'
        elif 'frecuencia' in tipo_matriz.lower() or 'reducida' in tipo_matriz.lower():
            if valor == 0:
                return '#FFFFFF'
            elif valor <= 100:
                return '#E8F4FD'
            elif valor <= 1000:
                return '#B4D7FF'
            else:
                return '#7BB3FF'
        else:
            return '#FFFFFF'

    def crear_nodos_matriz(self, matriz, etiquetas_filas, etiquetas_columnas):
        """Crear nodos para representación de matriz"""
        nodos = Lista()
        
        contador_filas = Contador(0, matriz.get_filas())
        while contador_filas.hay_siguiente():
            i = contador_filas.siguiente()
            contador_columnas = Contador(0, matriz.get_columnas())
            while contador_columnas.hay_siguiente():
                j = contador_columnas.siguiente()
                valor = matriz.get_valor(i, j)
                
                etiqueta_fila = etiquetas_filas.obtener_en_posicion(i) if etiquetas_filas and i < etiquetas_filas.obtener_tamaño() else f"F{i}"
                etiqueta_columna = etiquetas_columnas.obtener_en_posicion(j) if etiquetas_columnas and j < etiquetas_columnas.obtener_tamaño() else f"C{j}"
                
                nodo_info = Diccionario()
                nodo_info.insertar('id', f"n_{i}_{j}")
                nodo_info.insertar('fila', i)
                nodo_info.insertar('columna', j)
                nodo_info.insertar('valor', valor)
                nodo_info.insertar('etiqueta_fila', str(etiqueta_fila))
                nodo_info.insertar('etiqueta_columna', str(etiqueta_columna))
                
                nodos.insertar(nodo_info)
        
        return nodos

    def aplicar_estilo_matriz(self, tipo_matriz):
        """Aplicar estilos específicos según tipo de matriz"""
        estilos_frecuencias = Diccionario()
        estilos_frecuencias.insertar('color_fondo', '#E8F4FD')
        estilos_frecuencias.insertar('color_borde', '#4472C4')
        estilos_frecuencias.insertar('grosor_borde', '2')

        estilos_patrones = Diccionario()
        estilos_patrones.insertar('color_fondo', '#FFF2CC')
        estilos_patrones.insertar('color_borde', '#D6B656')
        estilos_patrones.insertar('grosor_borde', '2')

        estilos_reducida = Diccionario()
        estilos_reducida.insertar('color_fondo', '#D5E8D4')
        estilos_reducida.insertar('color_borde', '#82B366')
        estilos_reducida.insertar('grosor_borde', '2')

        estilos = Diccionario()
        estilos.insertar('frecuencias', estilos_frecuencias)
        estilos.insertar('patrones', estilos_patrones)
        estilos.insertar('reducida', estilos_reducida)
        
        tipo_clave = tipo_matriz.lower().split()[0]
        return estilos.obtener(tipo_clave) or estilos.obtener('frecuencias')
    
    def guardar_grafica(self, dot_content, nombre_archivo, formato="png"):
        """Guardar gráfica en formato especificado"""
        try:
            if not self.validar_graphviz_instalado():
                print("Error: Graphviz no está instalado en el sistema")
                return False

            archivo_dot = f"{nombre_archivo}.dot"
            archivo_salida = f"{nombre_archivo}.{formato}"
            
            f = None
            try:
                f = open(archivo_dot, 'w', encoding='utf-8')
                f.write(dot_content)
            finally:
                if f:
                    f.close()
            
            comando = Lista()
            comando.insertar('dot')
            comando.insertar(f'-T{formato}')
            comando.insertar(archivo_dot)
            comando.insertar('-o')
            comando.insertar(archivo_salida)
            
            comando_nativo = []
            iterador_comando = comando.crear_iterador()
            while iterador_comando.hay_siguiente():
                comando_nativo.append(iterador_comando.siguiente())
            
            resultado = subprocess.run(comando_nativo, capture_output=True, text=True)
            
            if resultado.returncode == 0:
                print(f"Gráfica generada exitosamente: {archivo_salida}")
                if os.path.exists(archivo_dot):
                    os.remove(archivo_dot)
                return True
            else:
                print(f"Error ejecutando Graphviz: {resultado.stderr}")
                return False
                
        except FileNotFoundError:
            print("Error: Comando 'dot' no encontrado. Instale Graphviz.")
            return False
        except Exception as e:
            print(f"Error guardando gráfica: {str(e)}")
            return False
    
    def validar_graphviz_instalado(self):
        """Verificar si Graphviz está instalado"""
        try:
            subprocess.run(['dot', '-V'], check=True, capture_output=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
            
    def mostrar_opciones_graficacion(self, lista_campos):
        """Mostrar menú de opciones para graficación"""
        print("\n" + "="*50)
        print("OPCIONES DE GRAFICACIÓN")
        print("="*50)
        
        if lista_campos.esta_vacia():
            print("No hay campos disponibles para graficar")
            return
        
        print("Campos disponibles:")
        i = 0
        iterador_campos = lista_campos.crear_iterador()
        while iterador_campos.hay_siguiente():
            campo = iterador_campos.siguiente()
            print(f"{i + 1}. {campo.get_nombre()} ({campo.obtener_cantidad_estaciones()} estaciones)")
            i += 1
        
        print("\nTipos de gráficas disponibles:")
        print("1. Matriz de Frecuencias de Suelo")
        print("2. Matriz de Frecuencias de Cultivo")
        print("3. Matriz de Patrones de Suelo")
        print("4. Matriz de Patrones de Cultivo")
        print("5. Matriz Reducida de Suelo")
        print("6. Matriz Reducida de Cultivo")
        print("7. Todas las matrices del campo seleccionado")

    def generar_graficas_completas(self, resultado_optimizacion):
        """
        Generar todas las gráficas de un proceso de optimización.
        """
        if not resultado_optimizacion:
            print("No hay resultados de optimización para graficar")
            return False
        
        try:
            campo_original = resultado_optimizacion.obtener('campo_original')
            campo_nombre = campo_original.get_nombre() if campo_original else "Campo Desconocido"
            exito_total = True
            
            etiquetas_estaciones = campo_original.obtener_estaciones() if campo_original else Lista()
            etiquetas_suelo = campo_original.obtener_sensores_suelo() if campo_original else Lista()
            etiquetas_cultivo = campo_original.obtener_sensores_cultivo() if campo_original else Lista()
            
            nombre_base = campo_nombre.replace(" ", "_").lower()
            
            matrices_a_graficar = Lista()
            
            info_suelo_original = Diccionario()
            info_suelo_original.insertar('matriz', resultado_optimizacion.obtener('matriz_freq_suelo_original'))
            info_suelo_original.insertar('titulo', 'Frecuencias Suelo Original')
            info_suelo_original.insertar('nombre_archivo', f'{nombre_base}_matriz_freq_suelo_original')
            info_suelo_original.insertar('etiquetas_filas', etiquetas_estaciones)
            info_suelo_original.insertar('etiquetas_columnas', etiquetas_suelo)
            matrices_a_graficar.insertar(info_suelo_original)

            info_cultivo_original = Diccionario()
            info_cultivo_original.insertar('matriz', resultado_optimizacion.obtener('matriz_freq_cultivo_original'))
            info_cultivo_original.insertar('titulo', 'Frecuencias Cultivo Original')
            info_cultivo_original.insertar('nombre_archivo', f'{nombre_base}_matriz_freq_cultivo_original')
            info_cultivo_original.insertar('etiquetas_filas', etiquetas_estaciones)
            info_cultivo_original.insertar('etiquetas_columnas', etiquetas_cultivo)
            matrices_a_graficar.insertar(info_cultivo_original)

            info_patron_suelo = Diccionario()
            info_patron_suelo.insertar('matriz', resultado_optimizacion.obtener('matriz_patron_suelo'))
            info_patron_suelo.insertar('titulo', 'Patrones Suelo')
            info_patron_suelo.insertar('nombre_archivo', f'{nombre_base}_matriz_patron_suelo')
            info_patron_suelo.insertar('etiquetas_filas', etiquetas_estaciones)
            info_patron_suelo.insertar('etiquetas_columnas', etiquetas_suelo)
            matrices_a_graficar.insertar(info_patron_suelo)

            info_patron_cultivo = Diccionario()
            info_patron_cultivo.insertar('matriz', resultado_optimizacion.obtener('matriz_patron_cultivo'))
            info_patron_cultivo.insertar('titulo', 'Patrones Cultivo')
            info_patron_cultivo.insertar('nombre_archivo', f'{nombre_base}_matriz_patron_cultivo')
            info_patron_cultivo.insertar('etiquetas_filas', etiquetas_estaciones)
            info_patron_cultivo.insertar('etiquetas_columnas', etiquetas_cultivo)
            matrices_a_graficar.insertar(info_patron_cultivo)
            
            iterador_matrices = matrices_a_graficar.crear_iterador()
            while iterador_matrices.hay_siguiente():
                matriz_info = iterador_matrices.siguiente()
                matriz = matriz_info.obtener('matriz')
                if matriz:
                    exito = self.generar_grafica_matriz(
                        matriz,
                        matriz_info.obtener('titulo'),
                        campo_nombre,
                        matriz_info.obtener('nombre_archivo'),
                        matriz_info.obtener('etiquetas_filas'),
                        matriz_info.obtener('etiquetas_columnas')
                    )
                    exito_total = exito_total and exito
            
            matrices_reducidas = resultado_optimizacion.obtener('matrices_reducidas')
            if matrices_reducidas:
                etiquetas_grupos = Lista()
                grupos = resultado_optimizacion.obtener('grupos_estaciones')
                if grupos:
                    i = 1
                    iterador_grupos = grupos.crear_iterador()
                    while iterador_grupos.hay_siguiente():
                        grupo = iterador_grupos.siguiente()
                        etiquetas_grupos.insertar(f"Grupo_{i}")
                        i += 1
                
                matriz_reducida_suelo = matrices_reducidas.obtener('suelo')
                if matriz_reducida_suelo:
                    exito = self.generar_grafica_matriz(
                        matriz_reducida_suelo,
                        'Reducida Suelo',
                        campo_nombre,
                        f'{nombre_base}_matriz_reducida_suelo',
                        etiquetas_grupos,
                        etiquetas_suelo
                    )
                    exito_total = exito_total and exito
                
                matriz_reducida_cultivo = matrices_reducidas.obtener('cultivo')
                if matriz_reducida_cultivo:
                    exito = self.generar_grafica_matriz(
                        matriz_reducida_cultivo,
                        'Reducida Cultivo',
                        campo_nombre,
                        f'{nombre_base}_matriz_reducida_cultivo',
                        etiquetas_grupos,
                        etiquetas_cultivo
                    )
                    exito_total = exito_total and exito

            if exito_total:
                print(f"Todas las gráficas generadas exitosamente en directorio: {self.directorio_graficas}")
            else:
                print("Algunas gráficas no se pudieron generar")
            
            return exito_total
            
        except Exception as e:
            print(f"Error generando gráficas completas: {e}")
            return False