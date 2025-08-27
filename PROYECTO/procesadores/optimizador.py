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
            cantidad_optimizada = campo_optimizado.obtener_cantidad_estaciones()
            porcentaje_ahorro = self.calcular_ahorro_estaciones(cantidad_original, cantidad_optimizada)
            
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
            resultado.insertar('estaciones_optimizada', cantidad_optimizada)
            resultado.insertar('porcentaje_ahorro', porcentaje_ahorro)
            
            print("Optimización completada exitosamente!")
            print("Estaciones originales: {}".format(cantidad_original))
            print("Estaciones optimizadas: {}".format(cantidad_optimizada))
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
            
            #Usar función propia en lugar de range()
            indices_i = self.crear_rango(0, filas)
            for i in indices_i.recorrer():
                if self._estacion_ya_procesada(i, estaciones_procesadas):
                    continue
                
                grupo_actual = Lista()
                grupo_actual.insertar(i)
                estaciones_procesadas.insertar(i)
                
                # Buscar estaciones con patrones idénticos
                indices_j = self.crear_rango(i + 1, filas)
                for j in indices_j.recorrer():
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
            grupos = grupos_estaciones.recorrer()
            estaciones_originales = campo_original.obtener_estaciones().recorrer()
            
            #Evitar enumerate() - usar contador manual
            contador = 0
            for grupo in grupos:
                indices_grupo = grupo.recorrer()
                #Obtener primer elemento sin indexación directa
                primer_indice = None
                if indices_grupo:
                    primer_indice = indices_grupo[0] if len(indices_grupo) > 0 else 0
                
                if primer_indice is not None:
                    #Usar obtener_en_posicion en lugar de indexación directa
                    estacion_representante = None
                    if primer_indice < len(estaciones_originales):
                        estacion_representante = estaciones_originales[primer_indice]
                    
                    if estacion_representante:
                        # Crear nueva estación optimizada
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
        #Usar buscar() en lugar de 'in'
        def criterio(elemento):
            return elemento == indice
        return estaciones_procesadas.buscar(criterio) is not None

    def _crear_sensores_optimizados_suelo(self, campo_original, campo_optimizado, matriz_reducida):
        """Crear sensores de suelo optimizados"""
        sensores_originales = campo_original.obtener_sensores_suelo().recorrer()
        estaciones_optimizadas = campo_optimizado.obtener_estaciones().recorrer()
        
        #Evitar enumerate() - usar contador manual
        j = 0
        for sensor_original in sensores_originales:
            # Crear nuevo sensor optimizado
            sensor_optimizado = SensorSuelo(
                sensor_original.get_id(),
                sensor_original.get_nombre()
            )
            
            # Agregar frecuencias de la matriz reducida
            i = 0
            for estacion in estaciones_optimizadas:
                valor_frecuencia = matriz_reducida.get_valor(i, j)
                if valor_frecuencia > 0:
                    frecuencia = Frecuencia(estacion.get_id(), valor_frecuencia)
                    sensor_optimizado.agregar_frecuencia(frecuencia)
                i += 1
            
            campo_optimizado.agregar_sensor_suelo(sensor_optimizado)
            j += 1

    def _crear_sensores_optimizados_cultivo(self, campo_original, campo_optimizado, matriz_reducida):
        """Crear sensores de cultivo optimizados"""
        sensores_originales = campo_original.obtener_sensores_cultivo().recorrer()
        estaciones_optimizadas = campo_optimizado.obtener_estaciones().recorrer()
        
        #Evitar enumerate() - usar contador manual
        j = 0
        for sensor_original in sensores_originales:
            # Crear nuevo sensor optimizado
            sensor_optimizado = SensorCultivo(
                sensor_original.get_id(),
                sensor_original.get_nombre()
            )
            
            # Agregar frecuencias de la matriz reducida
            i = 0
            for estacion in estaciones_optimizadas:
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
        #Usar comparación manual en lugar de max()
        return ahorro if ahorro > 0.0 else 0.0

    def validar_optimizacion(self, campo_original, campo_optimizado):
        """Validar que la optimización mantenga la funcionalidad"""
        try:
            # Validar que el campo optimizado tenga estaciones
            if campo_optimizado.obtener_cantidad_estaciones() == 0:
                return False, "Campo optimizado no tiene estaciones"
            
            # Validar que tenga sensores
            if campo_optimizado.obtener_cantidad_sensores_suelo() == 0:
                return False, "Campo optimizado no tiene sensores de suelo"
            
            if campo_optimizado.obtener_cantidad_sensores_cultivo() == 0:
                return False, "Campo optimizado no tiene sensores de cultivo"
            
            # Validar que haya optimización
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