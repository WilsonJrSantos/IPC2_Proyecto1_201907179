import xml.etree.ElementTree as ET
import os
from clases.lista import Lista
from clases.campo_agricola import CampoAgricola
from clases.estacion_base import EstacionBase
from clases.sensor_suelo import SensorSuelo
from clases.sensor_cultivo import SensorCultivo
from clases.frecuencia import Frecuencia

class XMLHandler:
    def __init__(self):
        """Inicializar manejador de XML"""
        self.lista_campos = Lista()

    def _convertir_a_lista(self, elementos):
        """Convertir un iterable de ElementTree a una Lista personalizada"""
        lista = Lista()
        for elemento in elementos:
            lista.insertar(elemento)
        return lista

    def cargar_archivo(self, ruta_archivo):
        """Cargar y parsear archivo XML de entrada"""
        try:
            if not os.path.exists(ruta_archivo):
                raise FileNotFoundError("El archivo XML no existe: {}".format(ruta_archivo))
            
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            self.lista_campos = Lista()
            
            elementos_campos = self._convertir_a_lista(root.findall('campo'))
            iterador_campos = elementos_campos.crear_iterador()
            while iterador_campos.hay_siguiente():
                elemento_campo = iterador_campos.siguiente()
                campo = self.procesar_campo(elemento_campo)
                if campo:
                    self.lista_campos.insertar(campo)
            
            return self.lista_campos
            
        except ET.ParseError as e:
            raise Exception("Error al parsear XML: {}".format(str(e)))
        except Exception as e:
            raise Exception("Error al cargar archivo XML: {}".format(str(e)))

    def procesar_campo(self, elemento_campo):
        """Procesar elemento campo del XML"""
        try:
            id_campo = elemento_campo.get('id')
            nombre_campo = elemento_campo.get('nombre')
            
            if not id_campo or not nombre_campo:
                return None
            
            campo = CampoAgricola(id_campo, nombre_campo)
            
            elemento_estaciones = elemento_campo.find('estacionesBase')
            if elemento_estaciones is not None:
                self.procesar_estaciones(elemento_estaciones, campo)
            
            elemento_sensores_suelo = elemento_campo.find('sensoresSuelo')
            if elemento_sensores_suelo is not None:
                self.procesar_sensores_suelo(elemento_sensores_suelo, campo)
            
            elemento_sensores_cultivo = elemento_campo.find('sensoresCultivo')
            if elemento_sensores_cultivo is not None:
                self.procesar_sensores_cultivo(elemento_sensores_cultivo, campo)
            
            return campo
            
        except Exception as e:
            print("Error procesando campo: {}".format(str(e)))
            return None

    def procesar_estaciones(self, elemento_estaciones, campo):
        """Procesar estaciones base del XML"""
        elementos_estacion = self._convertir_a_lista(elemento_estaciones.findall('estacion'))
        iterador_estaciones = elementos_estacion.crear_iterador()
        while iterador_estaciones.hay_siguiente():
            elemento_estacion = iterador_estaciones.siguiente()
            id_estacion = elemento_estacion.get('id')
            nombre_estacion = elemento_estacion.get('nombre')
            
            if id_estacion and nombre_estacion:
                estacion = EstacionBase(id_estacion, nombre_estacion)
                campo.agregar_estacion(estacion)

    def procesar_sensores_suelo(self, elemento_sensores, campo):
        """Procesar sensores de suelo del XML"""
        elementos_sensor = self._convertir_a_lista(elemento_sensores.findall('sensorS'))
        iterador_sensores = elementos_sensor.crear_iterador()
        while iterador_sensores.hay_siguiente():
            elemento_sensor = iterador_sensores.siguiente()
            id_sensor = elemento_sensor.get('id')
            nombre_sensor = elemento_sensor.get('nombre')
            
            if id_sensor and nombre_sensor:
                sensor = SensorSuelo(id_sensor, nombre_sensor)
                
                elementos_frecuencia = self._convertir_a_lista(elemento_sensor.findall('frecuencia'))
                iterador_frecuencias = elementos_frecuencia.crear_iterador()
                while iterador_frecuencias.hay_siguiente():
                    elemento_frecuencia = iterador_frecuencias.siguiente()
                    id_estacion = elemento_frecuencia.get('idEstacion')
                    valor_frecuencia = elemento_frecuencia.text
                    
                    if id_estacion and valor_frecuencia:
                        try:
                            valor = int(valor_frecuencia.strip())
                            frecuencia = Frecuencia(id_estacion, valor)
                            sensor.agregar_frecuencia(frecuencia)
                        except ValueError:
                            print("Error: Valor de frecuencia inválido: {}".format(valor_frecuencia))
                
                campo.agregar_sensor_suelo(sensor)

    def procesar_sensores_cultivo(self, elemento_sensores, campo):
        """Procesar sensores de cultivo del XML"""
        elementos_sensor = self._convertir_a_lista(elemento_sensores.findall('sensorT'))
        iterador_sensores = elementos_sensor.crear_iterador()
        while iterador_sensores.hay_siguiente():
            elemento_sensor = iterador_sensores.siguiente()
            id_sensor = elemento_sensor.get('id')
            nombre_sensor = elemento_sensor.get('nombre')
            
            if id_sensor and nombre_sensor:
                sensor = SensorCultivo(id_sensor, nombre_sensor)
                
                elementos_frecuencia = self._convertir_a_lista(elemento_sensor.findall('frecuencia'))
                iterador_frecuencias = elementos_frecuencia.crear_iterador()
                while iterador_frecuencias.hay_siguiente():
                    elemento_frecuencia = iterador_frecuencias.siguiente()
                    id_estacion = elemento_frecuencia.get('idEstacion')
                    valor_frecuencia = elemento_frecuencia.text
                    
                    if id_estacion and valor_frecuencia:
                        try:
                            valor = int(valor_frecuencia.strip())
                            frecuencia = Frecuencia(id_estacion, valor)
                            sensor.agregar_frecuencia(frecuencia)
                        except ValueError:
                            print("Error: Valor de frecuencia inválido: {}".format(valor_frecuencia))
                
                campo.agregar_sensor_cultivo(sensor)

    def escribir_archivo_salida(self, ruta_archivo, lista_campos_optimizados):
        """Escribir archivo XML de salida con resultados"""
        try:
            root = ET.Element("camposAgricolas")
            
            iterador_campos = lista_campos_optimizados.crear_iterador()
            while iterador_campos.hay_siguiente():
                campo = iterador_campos.siguiente()
                elemento_campo = self.crear_elemento_campo_optimizado(campo)
                root.append(elemento_campo)
            
            tree = ET.ElementTree(root)
            ET.indent(tree, space="    ")
            
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                os.makedirs(directorio)
            
            tree.write(ruta_archivo, encoding='utf-8', xml_declaration=True)
            return True
            
        except Exception as e:
            print("Error escribiendo archivo XML: {}".format(str(e)))
            return False

    def crear_elemento_campo_optimizado(self, campo_optimizado):
        """Crear elemento XML para campo optimizado"""
        elemento_campo = ET.Element("campo")
        elemento_campo.set("id", campo_optimizado.get_id())
        elemento_campo.set("nombre", campo_optimizado.get_nombre())
        
        elemento_estaciones = ET.SubElement(elemento_campo, "estacionesBase")
        estaciones = campo_optimizado.obtener_estaciones()
        iterador_estaciones = estaciones.crear_iterador()
        while iterador_estaciones.hay_siguiente():
            estacion = iterador_estaciones.siguiente()
            elemento_estacion = ET.SubElement(elemento_estaciones, "estacion")
            elemento_estacion.set("id", estacion.get_id())
            elemento_estacion.set("nombre", estacion.get_nombre())
        
        elemento_sensores_suelo = ET.SubElement(elemento_campo, "sensoresSuelo")
        sensores_suelo = campo_optimizado.obtener_sensores_suelo()
        iterador_sensores_suelo = sensores_suelo.crear_iterador()
        while iterador_sensores_suelo.hay_siguiente():
            sensor = iterador_sensores_suelo.siguiente()
            elemento_sensor = ET.SubElement(elemento_sensores_suelo, "sensorS")
            elemento_sensor.set("id", sensor.get_id())
            elemento_sensor.set("nombre", sensor.get_nombre())
            
            frecuencias = sensor.obtener_frecuencias()
            iterador_frecuencias = frecuencias.crear_iterador()
            while iterador_frecuencias.hay_siguiente():
                frecuencia = iterador_frecuencias.siguiente()
                elemento_frecuencia = ET.SubElement(elemento_sensor, "frecuencia")
                elemento_frecuencia.set("idEstacion", frecuencia.get_id_estacion())
                elemento_frecuencia.text = str(frecuencia.get_valor())
        
        elemento_sensores_cultivo = ET.SubElement(elemento_campo, "sensoresCultivo")
        sensores_cultivo = campo_optimizado.obtener_sensores_cultivo()
        iterador_sensores_cultivo = sensores_cultivo.crear_iterador()
        while iterador_sensores_cultivo.hay_siguiente():
            sensor = iterador_sensores_cultivo.siguiente()
            elemento_sensor = ET.SubElement(elemento_sensores_cultivo, "sensorT")
            elemento_sensor.set("id", sensor.get_id())
            elemento_sensor.set("nombre", sensor.get_nombre())
            
            frecuencias = sensor.obtener_frecuencias()
            iterador_frecuencias = frecuencias.crear_iterador()
            while iterador_frecuencias.hay_siguiente():
                frecuencia = iterador_frecuencias.siguiente()
                elemento_frecuencia = ET.SubElement(elemento_sensor, "frecuencia")
                elemento_frecuencia.set("idEstacion", frecuencia.get_id_estacion())
                elemento_frecuencia.text = str(frecuencia.get_valor())
        
        return elemento_campo

    def validar_xml(self, ruta_archivo):
        """Validar estructura del archivo XML"""
        try:
            if not os.path.exists(ruta_archivo):
                return False, "Archivo no encontrado"
            
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            if root.tag != "camposAgricolas":
                return False, "Elemento raíz debe ser 'camposAgricolas'"
            
            campos_encontrados = Lista()
            for campo in root.findall('campo'):
                campos_encontrados.insertar(campo)

            if campos_encontrados.esta_vacia():
                return False, "Debe contener al menos un campo agrícola"
            
            iterador_campos = campos_encontrados.crear_iterador()
            while iterador_campos.hay_siguiente():
                campo = iterador_campos.siguiente()
                if not campo.get('id') or not campo.get('nombre'):
                    return False, "Cada campo debe tener id y nombre"
                
                if campo.find('estacionesBase') is None:
                    return False, "Campo {} no tiene estacionesBase".format(campo.get('id'))
                
                if campo.find('sensoresSuelo') is None:
                    return False, "Campo {} no tiene sensoresSuelo".format(campo.get('id'))
                
                if campo.find('sensoresCultivo') is None:
                    return False, "Campo {} no tiene sensoresCultivo".format(campo.get('id'))
            
            return True, "XML válido"
            
        except ET.ParseError as e:
            return False, "Error de sintaxis XML: {}".format(str(e))
        except Exception as e:
            return False, "Error validando XML: {}".format(str(e))

    def obtener_lista_campos(self):
        """Retornar lista de campos cargados"""
        return self.lista_campos