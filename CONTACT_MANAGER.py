#Daniel Cabrera 
#Sophia Gamarro
import requests
from requests.exceptions import HTTPError
import validators
import time
import csv
# validar si en el nombre ingresado hay dos palabras (nombre y apellido)
def validar_nombre(nombre):
    return len(nombre.split()) == 2
# validar si el celular contiene solo numeros
def validar_celular(celular):
    return celular.isdecimal()

# guardar un contacto en el libro de contactos, si no se encuentra la letra aun
# crear una llave con la inicial del nombre a guardar
def guardar_contacto(nombre, telefono, email, company, extra, libro_contactos):
        inicial = nombre[0].upper()
    if (libro_contactos.get(inicial, 'non-existent') == 'non-existent'):
        libro_contactos[inicial] = {}
    libro_contactos[inicial][nombre] = {
            'telefono': telefono,
            'email': email,
            'company': company,
            'extra': extra
        }

def buscar_contactos(ingreso, libro_contactos):
    coincidencias = []