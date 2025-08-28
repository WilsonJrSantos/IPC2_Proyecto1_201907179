# clases/nodo.py
# Implementación de nodo para estructuras enlazadas

class Nodo:
    """
    Clase que representa un nodo para estructuras de datos enlazadas.
    Cada nodo contiene un dato y una referencia al siguiente nodo.
    """
    
    def __init__(self, dato):
        """
        Inicializar nodo con un dato
        
        Args:
            dato: Información a almacenar en el nodo
        """
        self.__dato = dato
        self.__siguiente = None
    
    def get_dato(self):
        """
        Obtener el dato almacenado en el nodo
        
        Returns:
            El dato del nodo
        """
        return self.__dato
    
    def set_dato(self, dato):
        """
        Establecer nuevo dato para el nodo
        
        Args:
            dato: Nuevo dato a almacenar
        """
        self.__dato = dato
    
    def get_siguiente(self):
        """
        Obtener referencia al siguiente nodo
        
        Returns:
            Nodo: Referencia al siguiente nodo o None si no hay siguiente
        """
        return self.__siguiente
    
    def set_siguiente(self, nodo):
        """
        Establecer referencia al siguiente nodo
        
        Args:
            nodo (Nodo): Nodo que será el siguiente o None
        """
        self.__siguiente = nodo
    
    def tiene_siguiente(self):
        """
        Verificar si el nodo tiene un siguiente
        
        Returns:
            bool: True si tiene siguiente, False si no
        """
        return self.__siguiente is not None
    
    def __str__(self):
        """
        Representación en string del nodo
        
        Returns:
            str: Representación del dato contenido
        """
        return f"Nodo({self.__dato})"
    
    def __repr__(self):
        """
        Representación técnica del nodo
        
        Returns:
            str: Representación técnica del nodo
        """
        return f"Nodo(dato={repr(self.__dato)}, tiene_siguiente={self.tiene_siguiente()})"