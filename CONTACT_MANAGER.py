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

# Buscar los nombres de contactos que hagan match con el dato ingresado
def buscar_contactos(ingreso, libro_contactos):
    coincidencias = []
    for letra, contactos in libro_contactos.items():
        for contacto, value in contactos.items():
            if(ingreso in contacto):
                coincidencias.append(contacto)
    return coincidencias

# esta url puede ser sustituida antes de iniciar el programa
url = ' http://demo7130536.mockable.io/final-contacts-100'

contactos_cargados = False
variable_control = 0

while contactos_cargados == False:
    #  descomentar la linea de abajo para que el usuario pueda ingresar la url 
    #url = input("Ingrese la url con el álbum de contactos para iniciar el programa: ")
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as http_err:
        print('HTTP error occurred')  
    except Exception as err:
        print('Other error occurred')
    else:
        print('Se han actualizado los contactos')
        contact_book = response.json()
        contactos_cargados = True

while variable_control != '9':
    print("""
    ----------MANEJADOR DE CONTACTOS-----------
            Elije una opción:
            1. Agregar Contactos
            2. Buscar Contactos
            3. Listar Contactos 
            4. Borrar Contacto
            5. Llamar Contacto
            6. Enviar Mensaje a un Contacto
            7. Enviar Correo a Contacto
            8. Exportar Contactos
            9. Salir""")
    variable_control = input(">>>")
    # validar nombre, telefono y email con las funciones de validación
    # si cumple con todas las características llamar a la función
    # guardar_contacto, con los valores provistos
    if (variable_control == '1'):
        nombre = input("Nombre: ")
        if validar_nombre(nombre):
            celular = input("Teléfono: ")
            if validar_celular(celular):
                mail = input("Correo: ")
                if validators.email(mail):
                    empresa = input("ingrese una empresa (Si no tiene una, presione Enter): ")
                    extra = input("ingrese datos extra (Si no desea ingresar extras, presione Enter): ")     
                    guardar_contacto(nombre, celular, mail, empresa, extra, contact_book)
                else:
                    print("Por favor ingrese un email válido")
                    variable_control ='1'    
            else:
                print("El teléfono debe contener solo números")
                variable_control ='1'    
        else:
            print("El nombre tiene que tener dos palabras")
            variable_control='1'

# solicitar un nombre de contacto a buscar, llamar a la función buscar_contactos
# y mostrar todos los contactos que contengan el string ingresado por el usuario
    elif (variable_control == '2'):
        ingreso = input('Buscar: ')
        contactos = buscar_contactos(ingreso,contact_book)
        for contacto in contactos:
           print('- '+ contacto)

    elif (variable_control == '3'):
        array_contactos = []
        orden = 0
        for letra, contactos in contact_book.items():
            print(letra +':')
            for contacto, value in contactos.items():
                orden += 1
        

        




