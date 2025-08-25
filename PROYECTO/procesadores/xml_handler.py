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

    def cargar_archivo(self, ruta_archivo):
        """Cargar y parsear archivo XML de entrada"""
        try:
            if not os.path.exists(ruta_archivo):
                raise FileNotFoundError("El archivo XML no existe: {}".format(ruta_archivo))
            
            tree = ET.parse(ruta_archivo)
            root = tree.getroot()
            
            # Limpiar lista antes de cargar
            self.lista_campos = Lista()
            
            # Procesar cada campo en el XML
            for elemento_campo in root.findall('campo'):
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
            
            # Procesar estaciones base
            elemento_estaciones = elemento_campo.find('estacionesBase')
            if elemento_estaciones is not None:
                self.procesar_estaciones(elemento_estaciones, campo)
            
            # Procesar sensores de suelo
            elemento_sensores_suelo = elemento_campo.find('sensoresSuelo')
            if elemento_sensores_suelo is not None:
                self.procesar_sensores_suelo(elemento_sensores_suelo, campo)
            
            # Procesar sensores de cultivo
            elemento_sensores_cultivo = elemento_campo.find('sensoresCultivo')
            if elemento_sensores_cultivo is not None:
                self.procesar_sensores_cultivo(elemento_sensores_cultivo, campo)
            
            return campo
            
        except Exception as e:
            print("Error procesando campo: {}".format(str(e)))
            return None

    def procesar_estaciones(self, elemento_estaciones, campo):
        """Procesar estaciones base del XML"""
        for elemento_estacion in elemento_estaciones.findall('estacion'):
            id_estacion = elemento_estacion.get('id')
            nombre_estacion = elemento_estacion.get('nombre')
            
            if id_estacion and nombre_estacion:
                estacion = EstacionBase(id_estacion, nombre_estacion)
                campo.agregar_estacion(estacion)

    def procesar_sensores_suelo(self, elemento_sensores, campo):
        """Procesar sensores de suelo del XML"""
        for elemento_sensor in elemento_sensores.findall('sensorS'):
            id_sensor = elemento_sensor.get('id')
            nombre_sensor = elemento_sensor.get('nombre')
            
            if id_sensor and nombre_sensor:
                sensor = SensorSuelo(id_sensor, nombre_sensor)
                
                # Procesar frecuencias del sensor
                for elemento_frecuencia in elemento_sensor.findall('frecuencia'):
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
        for elemento_sensor in elemento_sensores.findall('sensorT'):
            id_sensor = elemento_sensor.get('id')
            nombre_sensor = elemento_sensor.get('nombre')
            
            if id_sensor and nombre_sensor:
                sensor = SensorCultivo(id_sensor, nombre_sensor)
                
                # Procesar frecuencias del sensor
                for elemento_frecuencia in elemento_sensor.findall('frecuencia'):
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
            
            campos = lista_campos_optimizados.recorrer()
            for campo in campos:
                elemento_campo = self.crear_elemento_campo_optimizado(campo)
                root.append(elemento_campo)
            
            # Crear árbol XML y escribir archivo
            tree = ET.ElementTree(root)
            ET.indent(tree, space="  ")
            
            # Asegurar que el directorio existe
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
        
        # Crear elemento estaciones base
        elemento_estaciones = ET.SubElement(elemento_campo, "estacionesBase")
        estaciones = campo_optimizado.obtener_estaciones().recorrer()
        for estacion in estaciones:
            elemento_estacion = ET.SubElement(elemento_estaciones, "estacion")
            elemento_estacion.set("id", estacion.get_id())
            elemento_estacion.set("nombre", estacion.get_nombre())
        
        # Crear elemento sensores de suelo
        elemento_sensores_suelo = ET.SubElement(elemento_campo, "sensoresSuelo")
        sensores_suelo = campo_optimizado.obtener_sensores_suelo().recorrer()
        for sensor in sensores_suelo:
            elemento_sensor = ET.SubElement(elemento_sensores_suelo, "sensorS")
            elemento_sensor.set("id", sensor.get_id())
            elemento_sensor.set("nombre", sensor.get_nombre())
            
            frecuencias = sensor.obtener_frecuencias().recorrer()
            for frecuencia in frecuencias:
                elemento_frecuencia = ET.SubElement(elemento_sensor, "frecuencia")
                elemento_frecuencia.set("idEstacion", frecuencia.get_id_estacion())
                elemento_frecuencia.text = str(frecuencia.get_valor())
        
        # Crear elemento sensores de cultivo
        elemento_sensores_cultivo = ET.SubElement(elemento_campo, "sensoresCultivo")
        sensores_cultivo = campo_optimizado.obtener_sensores_cultivo().recorrer()
        for sensor in sensores_cultivo:
            elemento_sensor = ET.SubElement(elemento_sensores_cultivo, "sensorT")
            elemento_sensor.set("id", sensor.get_id())
            elemento_sensor.set("nombre", sensor.get_nombre())
            
            frecuencias = sensor.obtener_frecuencias().recorrer()
            for frecuencia in frecuencias:
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
            
            # Validar que tenga al menos un campo
            campos = root.findall('campo')
            if len(campos) == 0:
                return False, "Debe contener al menos un campo agrícola"
            
            # Validar estructura de cada campo
            for campo in campos:
                if not campo.get('id') or not campo.get('nombre'):
                    return False, "Cada campo debe tener id y nombre"
                
                # Verificar que tenga las secciones requeridas
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