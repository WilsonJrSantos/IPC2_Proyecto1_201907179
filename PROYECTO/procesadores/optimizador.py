from clases.lista import Lista
from clases.diccionario import Diccionario
from clases.campo_agricola import CampoAgricola
from clases.estacion_base import EstacionBase
from clases.sensor_suelo import SensorSuelo
from clases.sensor_cultivo import SensorCultivo
from clases.frecuencia import Frecuencia
from .procesador_matrices import ProcesadorMatrices

class Optimizador:
    def __init__(self):
        """Inicializar optimizador"""
        self.procesador_matrices = ProcesadorMatrices()

    def crear_rango(self, inicio, fin):
        """Crear rango de números sin usar range() nativo"""
        numeros = Lista()
        i = inicio
        while i < fin:
            numeros.insertar(i)
            i += 1
        return numeros

    def optimizar_estaciones(self, campo):
        """Proceso principal de optimización"""
        try:
            print("Iniciando proceso de optimización para campo: {}".format(campo.get_nombre()))
            
            # Paso 1: Crear matrices de frecuencias
            print("Paso 1: Creando matrices de frecuencias...")
            matriz_freq_suelo = self.procesador_matrices.crear_matriz_frecuencias_suelo(campo)
            matriz_freq_cultivo = self.procesador_matrices.crear_matriz_frecuencias_cultivo(campo)
            
            if not matriz_freq_suelo or not matriz_freq_cultivo:
                raise Exception("Error creando matrices de frecuencias")
            
            # Paso 2: Convertir a matrices de patrones
            print("Paso 2: Convirtiendo a matrices de patrones...")
            matriz_patron_suelo = self.procesador_matrices.convertir_a_patrones(matriz_freq_suelo)
            matriz_patron_cultivo = self.procesador_matrices.convertir_a_patrones(matriz_freq_cultivo)
            
            if not matriz_patron_suelo or not matriz_patron_cultivo:
                raise Exception("Error convirtiendo a matrices de patrones")
            
            # Paso 3: Identificar grupos de estaciones con patrones idénticos
            print("Paso 3: Identificando grupos de estaciones...")
            estaciones = campo.obtener_estaciones()
            grupos_estaciones = self.identificar_grupos_estaciones(
                matriz_patron_suelo, matriz_patron_cultivo, estaciones
            )
            
            if grupos_estaciones.esta_vacia():
                raise Exception("No se pudieron identificar grupos de estaciones")
            
            # Paso 4: Crear matrices reducidas
            print("Paso 4: Creando matrices reducidas...")
            matrices_reducidas = self.crear_matrices_reducidas(
                matriz_freq_suelo, matriz_freq_cultivo, grupos_estaciones
            )
            
            # Paso 5: Crear campo optimizado
            print("Paso 5: Creando campo optimizado...")
            campo_optimizado = self.crear_campo_optimizado(
                campo, grupos_estaciones, matrices_reducidas
            )
            
            # Calcular estadísticas de optimización
            cantidad_original = campo.obtener_cantidad_estaciones()
            cantidad_optimada = campo_optimizado.obtener_cantidad_estaciones()
            porcentaje_ahorro = self.calcular_ahorro_estaciones(cantidad_original, cantidad_optimada)
            
            # Usar Diccionario personalizado en lugar de dict nativo
            resultado = Diccionario()
            resultado.insertar('campo_optimizado', campo_optimizado)
            resultado.insertar('matriz_freq_suelo_original', matriz_freq_suelo)
            resultado.insertar('matriz_freq_cultivo_original', matriz_freq_cultivo)
            resultado.insertar('matriz_patron_suelo', matriz_patron_suelo)
            resultado.insertar('matriz_patron_cultivo', matriz_patron_cultivo)
            resultado.insertar('matrices_reducidas', matrices_reducidas)
            resultado.insertar('grupos_estaciones', grupos_estaciones)
            resultado.insertar('estaciones_original', cantidad_original)
            resultado.insertar('estaciones_optimizada', cantidad_optimada)
            resultado.insertar('porcentaje_ahorro', porcentaje_ahorro)
            
            print("Optimización completada exitosamente!")
            print("Estaciones originales: {}".format(cantidad_original))
            print("Estaciones optimizadas: {}".format(cantidad_optimada))
            print("Ahorro: {:.2f}%".format(porcentaje_ahorro))
            
            return resultado
            
        except Exception as e:
            print("Error en proceso de optimización: {}".format(str(e)))
            return None

    def identificar_grupos_estaciones(self, matriz_patrones_suelo, matriz_patrones_cultivo, estaciones):
        """Identificar grupos de estaciones con patrones idénticos"""
        try:
            filas = matriz_patrones_suelo.get_filas()
            grupos = Lista()
            estaciones_procesadas = Lista()
            
            indices_i = self.crear_rango(0, filas)
            iterador_i = indices_i.crear_iterador()
            
            while iterador_i.hay_siguiente():
                i = iterador_i.siguiente()
                if self._estacion_ya_procesada(i, estaciones_procesadas):
                    continue
                
                grupo_actual = Lista()
                grupo_actual.insertar(i)
                estaciones_procesadas.insertar(i)
                
                indices_j = self.crear_rango(i + 1, filas)
                iterador_j = indices_j.crear_iterador()

                while iterador_j.hay_siguiente():
                    j = iterador_j.siguiente()
                    if self._patrones_identicos_combinados(
                        matriz_patrones_suelo, matriz_patrones_cultivo, i, j
                    ):
                        grupo_actual.insertar(j)
                        estaciones_procesadas.insertar(j)
                
                grupos.insertar(grupo_actual)
            
            return grupos
            
        except Exception as e:
            print("Error identificando grupos de estaciones: {}".format(str(e)))
            return Lista()

    def crear_matrices_reducidas(self, matriz_freq_suelo, matriz_freq_cultivo, grupos_estaciones):
        """Crear matrices Fr[n,s] y Fr[n,t] reducidas"""
        try:
            # Crear matriz reducida de suelo
            matriz_reducida_suelo = self.procesador_matrices.crear_matriz_reducida(
                matriz_freq_suelo, grupos_estaciones
            )
            
            # Crear matriz reducida de cultivo
            matriz_reducida_cultivo = self.procesador_matrices.crear_matriz_reducida(
                matriz_freq_cultivo, grupos_estaciones
            )
            
            # Usar Diccionario personalizado en lugar de dict nativo
            matrices = Diccionario()
            matrices.insertar('suelo', matriz_reducida_suelo)
            matrices.insertar('cultivo', matriz_reducida_cultivo)
            return matrices
            
        except Exception as e:
            print("Error creando matrices reducidas: {}".format(str(e)))
            return None

    def crear_campo_optimizado(self, campo_original, grupos_estaciones, matrices_reducidas):
        """Crear nuevo campo agrícola optimizado"""
        try:
            # Crear nuevo campo con mismo ID y nombre actualizado
            campo_optimizado = CampoAgricola(
                campo_original.get_id(),
                campo_original.get_nombre() + " (Optimizado)"
            )
            
            # Crear estaciones optimizadas (una por grupo)
            grupos_iterador = grupos_estaciones.crear_iterador()
            estaciones_originales = campo_original.obtener_estaciones()
            
            contador = 0
            while grupos_iterador.hay_siguiente():
                grupo = grupos_iterador.siguiente()
                primer_indice = grupo.obtener_en_posicion(0)
                
                if primer_indice is not None:
                    estacion_representante = estaciones_originales.obtener_en_posicion(primer_indice)
                    
                    if estacion_representante:
                        nueva_estacion = EstacionBase(
                            "e{:02d}_opt".format(contador + 1),
                            "Estacion Optimizada {:02d}".format(contador + 1)
                        )
                        campo_optimizado.agregar_estacion(nueva_estacion)
                
                contador += 1
            
            # Crear sensores de suelo optimizados
            self._crear_sensores_optimizados_suelo(
                campo_original, campo_optimizado, matrices_reducidas.obtener('suelo')
            )
            
            # Crear sensores de cultivo optimizados
            self._crear_sensores_optimizados_cultivo(
                campo_original, campo_optimizado, matrices_reducidas.obtener('cultivo')
            )
            
            return campo_optimizado
            
        except Exception as e:
            print("Error creando campo optimizado: {}".format(str(e)))
            return None

    def _estacion_ya_procesada(self, indice, estaciones_procesadas):
        """Verificar si una estación ya fue procesada"""
        def criterio(elemento):
            return elemento == indice
        return estaciones_procesadas.buscar(criterio) is not None

    def _crear_sensores_optimizados_suelo(self, campo_original, campo_optimizado, matriz_reducida):
        """Crear sensores de suelo optimizados"""
        sensores_originales = campo_original.obtener_sensores_suelo()
        estaciones_optimizadas = campo_optimizado.obtener_estaciones()

        iterador_sensores = sensores_originales.crear_iterador()
        j = 0
        while iterador_sensores.hay_siguiente():
            sensor_original = iterador_sensores.siguiente()
            sensor_optimizado = SensorSuelo(
                sensor_original.get_id(),
                sensor_original.get_nombre()
            )
            
            iterador_estaciones = estaciones_optimizadas.crear_iterador()
            i = 0
            while iterador_estaciones.hay_siguiente():
                estacion = iterador_estaciones.siguiente()
                valor_frecuencia = matriz_reducida.get_valor(i, j)
                if valor_frecuencia > 0:
                    frecuencia = Frecuencia(estacion.get_id(), valor_frecuencia)
                    sensor_optimizado.agregar_frecuencia(frecuencia)
                i += 1
            
            campo_optimizado.agregar_sensor_suelo(sensor_optimizado)
            j += 1

    def _crear_sensores_optimizados_cultivo(self, campo_original, campo_optimizado, matriz_reducida):
        """Crear sensores de cultivo optimizados"""
        sensores_originales = campo_original.obtener_sensores_cultivo()
        estaciones_optimizadas = campo_optimizado.obtener_estaciones()
        
        iterador_sensores = sensores_originales.crear_iterador()
        j = 0
        while iterador_sensores.hay_siguiente():
            sensor_original = iterador_sensores.siguiente()
            sensor_optimizado = SensorCultivo(
                sensor_original.get_id(),
                sensor_original.get_nombre()
            )
            
            iterador_estaciones = estaciones_optimizadas.crear_iterador()
            i = 0
            while iterador_estaciones.hay_siguiente():
                estacion = iterador_estaciones.siguiente()
                valor_frecuencia = matriz_reducida.get_valor(i, j)
                if valor_frecuencia > 0:
                    frecuencia = Frecuencia(estacion.get_id(), valor_frecuencia)
                    sensor_optimizado.agregar_frecuencia(frecuencia)
                i += 1
            
            campo_optimizado.agregar_sensor_cultivo(sensor_optimizado)
            j += 1

    def calcular_ahorro_estaciones(self, cantidad_original, cantidad_optimizada):
        """Calcular porcentaje de optimización logrado"""
        if cantidad_original == 0:
            return 0.0
        
        ahorro = ((cantidad_original - cantidad_optimizada) / cantidad_original) * 100
        if ahorro < 0.0:
            return 0.0
        return ahorro

    def validar_optimizacion(self, campo_original, campo_optimizado):
        """Validar que la optimización mantenga la funcionalidad"""
        try:
            if campo_optimizado.obtener_cantidad_estaciones() == 0:
                return False, "Campo optimizado no tiene estaciones"
            
            if campo_optimizado.obtener_cantidad_sensores_suelo() == 0:
                return False, "Campo optimizado no tiene sensores de suelo"
            
            if campo_optimizado.obtener_cantidad_sensores_cultivo() == 0:
                return False, "Campo optimizado no tiene sensores de cultivo"
            
            original = campo_original.obtener_cantidad_estaciones()
            optimizado = campo_optimizado.obtener_cantidad_estaciones()
            
            if optimizado >= original:
                return False, "No se logró optimización (misma cantidad o más estaciones)"
            
            return True, "Optimización válida"
            
        except Exception as e:
            return False, "Error validando optimización: {}".format(str(e))

    def _patrones_identicos_combinados(self, matriz_suelo, matriz_cultivo, fila1, fila2):
        """Verificar si dos estaciones tienen patrones idénticos en suelo y cultivo"""
        patron_suelo_identico = matriz_suelo.comparar_fila(fila1, fila2)
        patron_cultivo_identico = matriz_cultivo.comparar_fila(fila1, fila2)
        return patron_suelo_identico and patron_cultivo_identico