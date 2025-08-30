# clases/sensor_cultivo.py
# Clase que representa un sensor de cultivo en el sistema de agricultura de precisión

from clases.lista import Lista
from clases.diccionario import Diccionario
from clases.contador import Contador

class SensorCultivo:
    """
    Clase que representa un sensor de cultivo que evalúa el estado del cultivo
    a través de índices vegetales, estrés hídrico/térmico, cobertura, biomasa
    y detección temprana de enfermedades.
    """

    def __init__(self, id, nombre):
        """
        Inicializar sensor de cultivo con ID y nombre

        Args:
            id (str): Identificador único del sensor
            nombre (str): Nombre descriptivo del sensor
        """
        self.__id = id
        self.__nombre = nombre
        self.__frecuencias = Lista()  # Lista de frecuencias de transmisión
        self.__tipo = "cultivo"  # Tipo de sensor
        self.__activo = True  # Estado del sensor
        self.__parametros_medidos = Lista()  # Parámetros que puede medir este sensor

        # Inicializar parámetros típicos de sensores de cultivo
        self.__inicializar_parametros_cultivo()

    def __inicializar_parametros_cultivo(self):
        """Inicializar lista de parámetros que mide un sensor de cultivo"""
        self.__parametros_medidos.insertar("indices_vegetales")
        self.__parametros_medidos.insertar("estres_hidrico")
        self.__parametros_medidos.insertar("estres_termico")
        self.__parametros_medidos.insertar("cobertura_vegetal")
        self.__parametros_medidos.insertar("biomasa")
        self.__parametros_medidos.insertar("deteccion_enfermedades")
        self.__parametros_medidos.insertar("ndvi")
        self.__parametros_medidos.insertar("clorofila")

    def get_id(self):
        """Obtener el ID del sensor"""
        return self.__id

    def get_nombre(self):
        """Obtener el nombre del sensor"""
        return self.__nombre

    def set_nombre(self, nombre):
        """Establecer nuevo nombre para el sensor"""
        self.__nombre = nombre

    def get_tipo(self):
        """Obtener el tipo de sensor"""
        return self.__tipo

    def agregar_frecuencia(self, frecuencia):
        """Agregar frecuencia de transmisión a una estación"""
        freq_existente = self.buscar_frecuencia_por_estacion(frecuencia.get_id_estacion())
        if freq_existente:
            print(f"Advertencia: Ya existe frecuencia para estación {frecuencia.get_id_estacion()}")
            freq_existente.set_valor(frecuencia.get_valor())
        else:
            self.__frecuencias.insertar(frecuencia)

    def obtener_frecuencias(self):
        """Obtener lista de frecuencias del sensor"""
        return self.__frecuencias

    def buscar_frecuencia_por_estacion(self, id_estacion):
        """Buscar frecuencia específica por ID de estación"""
        def criterio(frecuencia):
            return frecuencia.get_id_estacion() == id_estacion
        return self.__frecuencias.buscar(criterio)

    def esta_activo(self):
        """Verificar si el sensor está activo"""
        return self.__activo

    def activar(self):
        """Activar el sensor"""
        self.__activo = True

    def desactivar(self):
        """Desactivar el sensor"""
        self.__activo = False

    def obtener_cantidad_frecuencias(self):
        """Obtener número total de frecuencias configuradas"""
        return self.__frecuencias.obtener_tamaño()

    def obtener_estaciones_conectadas(self):
        """Obtener lista de IDs de estaciones a las que transmite"""
        estaciones = Lista()
        iterador = self.__frecuencias.crear_iterador()
        while iterador.hay_siguiente():
            freq = iterador.siguiente()
            if freq.es_valida():
                estaciones.insertar(freq.get_id_estacion())
        return estaciones

    def obtener_frecuencia_total(self):
        """Calcular la frecuencia total de transmisión del sensor"""
        total = 0
        iterador = self.__frecuencias.crear_iterador()
        while iterador.hay_siguiente():
            freq = iterador.siguiente()
            total += freq.get_valor()
        return total

    def obtener_parametros_medidos(self):
        """Obtener lista de parámetros que mide este sensor"""
        return self.__parametros_medidos

    def puede_medir_parametro(self, parametro):
        """Verificar si el sensor puede medir un parámetro específico"""
        def criterio(param):
            return param == parametro
        return self.__parametros_medidos.buscar(criterio) is not None

    def eliminar_frecuencia(self, id_estacion):
        """Eliminar frecuencia para una estación específica"""
        freq = self.buscar_frecuencia_por_estacion(id_estacion)
        if freq:
            return self.__frecuencias.eliminar(freq)
        return False

    def detectar_problemas_cultivo(self):
        """Simular detección de problemas en el cultivo basado en frecuencias"""
        problemas = Lista()
        frecuencia_total = self.obtener_frecuencia_total()

        if frecuencia_total < 1000:
            problemas.insertar("Baja actividad de monitoreo")
        elif frecuencia_total > 10000:
            problemas.insertar("Alta actividad - posible estrés del cultivo")

        if self.obtener_cantidad_frecuencias() < 2:
            problemas.insertar("Pocas estaciones de monitoreo")

        return problemas

    def obtener_informacion_completa(self):
        """Obtener información completa del sensor"""
        info = Diccionario()
        info.insertar('id', self.__id)
        info.insertar('nombre', self.__nombre)
        info.insertar('tipo', self.__tipo)
        info.insertar('activo', self.__activo)
        info.insertar('cantidad_frecuencias', self.obtener_cantidad_frecuencias())
        info.insertar('frecuencia_total', self.obtener_frecuencia_total())
        info.insertar('estaciones_conectadas', self.obtener_estaciones_conectadas())
        info.insertar('parametros_medidos', self.__parametros_medidos)
        info.insertar('problemas_detectados', self.detectar_problemas_cultivo())
        return info

    def clonar(self):
        """Crear una copia del sensor"""
        nuevo_sensor = SensorCultivo(self.__id, self.__nombre)
        nuevo_sensor.__activo = self.__activo

        iterador = self.__frecuencias.crear_iterador()
        while iterador.hay_siguiente():
            freq = iterador.siguiente()
            nuevo_sensor.agregar_frecuencia(freq.clonar())

        return nuevo_sensor

    def validar_configuracion(self):
        """Validar que el sensor esté correctamente configurado"""
        if not self.__activo:
            return True

        iterador = self.__frecuencias.crear_iterador()
        while iterador.hay_siguiente():
            freq = iterador.siguiente()
            if freq.es_valida():
                return True
        return False

    def obtener_eficiencia_monitoreo(self):
        """Calcular eficiencia del monitoreo basado en distribución de frecuencias"""
        cantidad_estaciones = self.obtener_cantidad_frecuencias()
        if cantidad_estaciones == 0:
            return 0.0

        eficiencia_base = min(cantidad_estaciones * 20, 80)

        if cantidad_estaciones > 0:
            total = 0
            contador = 0
            iterador = self.__frecuencias.crear_iterador()
            while iterador.hay_siguiente():
                freq = iterador.siguiente()
                total += freq.get_valor()
                contador += 1
            promedio = total / contador

            total_desviaciones = 0
            contador_valores = 0
            iterador_desv = self.__frecuencias.crear_iterador()
            while iterador_desv.hay_siguiente():
                valor = iterador_desv.siguiente().get_valor()
                desviacion = abs(valor - promedio)
                total_desviaciones += desviacion
                contador_valores += 1

            desviacion_promedio = total_desviaciones / contador_valores if contador_valores > 0 else 0

            balance_bonus = max(20 - (desviacion_promedio / promedio) * 10, 0) if promedio > 0 else 0
            eficiencia_base += balance_bonus

        return min(eficiencia_base, 100.0)

    def __str__(self):
        """Representación en string del sensor"""
        estado = "Activo" if self.__activo else "Inactivo"
        eficiencia = self.obtener_eficiencia_monitoreo()
        return (f"SensorCultivo({self.__id}: {self.__nombre} - {estado} - "
                f"{self.obtener_cantidad_frecuencias()} frecuencias - "
                f"Eficiencia: {eficiencia:.1f}%)")

    def __repr__(self):
        """Representación técnica del sensor"""
        return f"SensorCultivo('{self.__id}', '{self.__nombre}')"

    def __eq__(self, other):
        """Comparar sensores por ID"""
        if not isinstance(other, SensorCultivo):
            return False
        return self.__id == other.__id

    def __hash__(self):
        """Hash del sensor basado en su ID"""
        return hash(self.__id)
