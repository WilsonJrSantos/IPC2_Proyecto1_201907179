# clases/nodo.py
# Implementación de la clase Nodo para estructuras de datos enlazadas
# Esta clase es fundamental para implementar listas propias sin usar estructuras nativas de Python

class Nodo:
    """
    Clase que representa un nodo genérico para estructuras de datos enlazadas.
    Cada nodo puede almacenar cualquier tipo de dato y mantiene una referencia al siguiente nodo.
    """
    
    def __init__(self, dato):
        """
        Inicializar un nuevo nodo con un dato específico
        
        Args:
            dato: Información a almacenar en el nodo (puede ser cualquier tipo)
        """
        self.__dato = dato  # Dato almacenado en el nodo (privado)
        self.__siguiente = None  # Referencia al siguiente nodo (privado)
    
    def get_dato(self):
        """
        Obtener el dato almacenado en el nodo
        
        Returns:
            El dato almacenado en este nodo
        """
        return self.__dato
    
    def set_dato(self, dato):
        """
        Establecer un nuevo dato en el nodo
        
        Args:
            dato: Nuevo dato a almacenar
        """
        self.__dato = dato
    
    def get_siguiente(self):
        """
        Obtener la referencia al siguiente nodo
        
        Returns:
            Referencia al siguiente nodo o None si es el último
        """
        return self.__siguiente
    
    def set_siguiente(self, siguiente):
        """
        Establecer la referencia al siguiente nodo
        
        Args:
            siguiente: Referencia al nodo que seguirá a este nodo
        """
        self.__siguiente = siguiente
    
    def tiene_siguiente(self):
        """
        Verificar si el nodo tiene un siguiente
        
        Returns:
            bool: True si tiene siguiente, False si es el último nodo
        """
        return self.__siguiente is not None
    
    def __str__(self):
        """
        Representación en string del nodo (para debugging)
        
        Returns:
            str: Representación del dato contenido
        """
        return str(self.__dato)
    
    def __repr__(self):
        """
        Representación técnica del nodo
        
        Returns:
            str: Representación técnica del nodo
        """
        return f"Nodo({self.__dato})"