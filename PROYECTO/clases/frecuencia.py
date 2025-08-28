# clases/frecuencia.py
# Clase que representa la frecuencia de transmisión entre un sensor y una estación base
from clases.diccionario import Diccionario
class Frecuencia:
    """
    Clase que representa la frecuencia de transmisión de datos
    entre un sensor específico y una estación base.
    """
    
    def __init__(self, id_estacion, valor):
        """
        Inicializar frecuencia con ID de estación y valor
        
        Args:
            id_estacion (str): ID de la estación base receptora
            valor (int): Valor numérico de la frecuencia de transmisión
        """
        self.__id_estacion = id_estacion
        self.__valor = int(valor)  # Asegurar que sea entero
        self.__timestamp = None  # Tiempo de última actualización
    
    def get_id_estacion(self):
        """
        Obtener el ID de la estación asociada
        
        Returns:
            str: ID de la estación base
        """
        return self.__id_estacion
    
    def get_valor(self):
        """
        Obtener el valor de frecuencia
        
        Returns:
            int: Valor numérico de la frecuencia
        """
        return self.__valor
    
    def set_valor(self, valor):
        """
        Establecer nuevo valor de frecuencia
        
        Args:
            valor (int): Nuevo valor de frecuencia
        """
        self.__valor = int(valor)
    
    def set_timestamp(self, timestamp):
        """
        Establecer timestamp de última actualización
        
        Args:
            timestamp: Tiempo de actualización
        """
        self.__timestamp = timestamp
    
    def get_timestamp(self):
        """
        Obtener timestamp de última actualización
        
        Returns:
            Timestamp de última actualización o None
        """
        return self.__timestamp
    
    def es_valida(self):
        """
        Verificar si la frecuencia es válida (valor positivo)
        
        Returns:
            bool: True si el valor es positivo, False si no
        """
        return self.__valor > 0
    
    def incrementar(self, cantidad):
        """
        Incrementar el valor de frecuencia
        
        Args:
            cantidad (int): Cantidad a incrementar
        """
        self.__valor += int(cantidad)
    
    def sumar_frecuencia(self, otra_frecuencia):
        """
        Sumar otra frecuencia a esta (para optimización)
        
        Args:
            otra_frecuencia (Frecuencia): Otra frecuencia a sumar
            
        Returns:
            Frecuencia: Nueva frecuencia con la suma
        """
        if self.__id_estacion != otra_frecuencia.get_id_estacion():
            raise ValueError("No se pueden sumar frecuencias de diferentes estaciones")
        
        valor_sumado = self.__valor + otra_frecuencia.get_valor()
        return Frecuencia(self.__id_estacion, valor_sumado)
    
    def convertir_a_patron(self):
        """
        Convertir frecuencia a patrón binario (0 o 1)
        
        Returns:
            int: 1 si hay frecuencia (>0), 0 si no hay frecuencia
        """
        return 1 if self.__valor > 0 else 0
    
    def obtener_informacion_completa(self):
        """
        Obtener información completa de la frecuencia usando Diccionario personalizado
        
        Returns:
            Diccionario: Diccionario personalizado con toda la información
        """
        info = Diccionario()  # Usar Diccionario personalizado
        info.insertar('id_estacion', self.__id_estacion)
        info.insertar('valor', self.__valor)
        info.insertar('timestamp', self.__timestamp)
        info.insertar('valida', self.es_valida())
        info.insertar('patron', self.convertir_a_patron())
        return info
    
    def clonar(self):
        """
        Crear una copia de la frecuencia
        
        Returns:
            Frecuencia: Copia de la frecuencia actual
        """
        nueva_freq = Frecuencia(self.__id_estacion, self.__valor)
        nueva_freq.__timestamp = self.__timestamp
        return nueva_freq
    
    def __str__(self):
        """
        Representación en string de la frecuencia
        
        Returns:
            str: Descripción de la frecuencia
        """
        return f"Frecuencia(Estación: {self.__id_estacion}, Valor: {self.__valor})"
    
    def __repr__(self):
        """
        Representación técnica de la frecuencia
        
        Returns:
            str: Representación técnica
        """
        return f"Frecuencia('{self.__id_estacion}', {self.__valor})"
    
    def __eq__(self, other):
        """
        Comparar frecuencias por estación y valor
        
        Args:
            other (Frecuencia): Otra frecuencia para comparar
            
        Returns:
            bool: True si son iguales
        """
        if not isinstance(other, Frecuencia):
            return False
        return (self.__id_estacion == other.__id_estacion and 
                self.__valor == other.__valor)
    
    def __lt__(self, other):
        """
        Comparar si esta frecuencia es menor que otra
        
        Args:
            other (Frecuencia): Otra frecuencia para comparar
            
        Returns:
            bool: True si esta frecuencia es menor
        """
        if not isinstance(other, Frecuencia):
            return NotImplemented
        return self.__valor < other.__valor
    
    def __add__(self, other):
        """
        Sobrecarga del operador + para sumar frecuencias
        
        Args:
            other (Frecuencia): Otra frecuencia para sumar
            
        Returns:
            Frecuencia: Nueva frecuencia con la suma
        """
        if isinstance(other, Frecuencia):
            return self.sumar_frecuencia(other)
        elif isinstance(other, int):
            return Frecuencia(self.__id_estacion, self.__valor + other)
        else:
            return NotImplemented