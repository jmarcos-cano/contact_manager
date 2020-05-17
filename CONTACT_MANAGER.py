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

     # Listar contactos iterando sobre el libro de contactos y luego sobre cada contacto individual
    # array_contactos almacena los contactos en orden para poder presentárselo a los usuarios con
    # números.
    # Luego imprimir el contacto seleccionado, dependiendo de si ingresa el nombre o el número de 
    # la lista

    elif (variable_control == '3'):
        array_contactos = []
        orden = 0
        for letra, contactos in contact_book.items():
            print(letra +':')
            for contacto, value in contactos.items():
                orden += 1
                print('   ' + str(orden) + '. '+contacto)
                dict_modificado = value.copy()
                dict_modificado['nombre'] = contacto
                array_contactos.append(dict_modificado)
        seleccionado = input('Ver Contacto: ')
        if (seleccionado.isnumeric()):
            seleccionado = int(seleccionado)
            print(array_contactos[seleccionado-1].get('nombre'))
            print("\U0001f4DE  telefono: "+ array_contactos[seleccionado-1].get('telefono'))
            print("\U0001F4E7  email: "+ array_contactos[seleccionado-1].get('email'))
            print("\U0001F3E2  company: "+ array_contactos[seleccionado-1].get('company'))
            print('\U00012795  extra: '+ array_contactos[seleccionado-1].get('extra'))
        else:
            for persona in array_contactos:
                if persona.get('nombre') == seleccionado:
                    print(persona.get('nombre'))
                    print("\U0001f4DE  telefono: "+ persona.get('telefono'))
                    print("\U0001F4E7  email: "+ persona.get('email'))
                    print("\U0001F3E2  company: "+ persona.get('company'))
                    print("\U00012795  extra: "+ persona.get('extra'))
    
    # Mostrar los contactos con el mismo método de iteración que la opción anterior
    # solicitar qué contacto desea borrar (nombre o número de la lista)
    # Borrar el contacto con diferentes métodos dependiendo de si ingresó un número o el nombre
    # esperar 3 segundos y volver al menú principal
    elif (variable_control == '4'):
        array_contactos = []
        orden = 0
        for letra, contactos in contact_book.items():
            print(letra +':')
            for contacto, value in contactos.items():
                orden += 1
                print('   ' + str(orden) + '. '+contacto)
                dict_modificado = value.copy()
                dict_modificado['nombre'] = contacto
                array_contactos.append(dict_modificado)
        seleccionado = input('Borrar Contacto: ')
        if (seleccionado.isnumeric()):
            seleccionado = int(seleccionado)
            letra = array_contactos[seleccionado-1].get('nombre')[0].upper()
            contact_book[letra].pop(array_contactos[seleccionado-1].get('nombre'))
            print("Contacto "+ array_contactos[seleccionado-1].get('nombre') + " Borrado")
            time.sleep(3)
        else:
            contact_book[seleccionado[0].upper()].pop(seleccionado)     
            print("Contacto "+ seleccionado + " Borrado")
            time.sleep(3)   

    # Mostrar los contactos con el mismo método de iteración que la opción (3)
    # Si el usuario seleccionó 5, solicitar a qué contacto desea llamar
    # si el usuario seleccionó 6, solicitar a qué contacto desea enviar mensaje
    # solicitar qué contacto desea utilizar para realizar la acción (nombre o número de la lista)
    # Mostrar en pantalla que se está llamando al contacto (opción 5) o que se está enviando mensaje (opción 6)
    # esperar 3 segundos y volver al menú principal

    elif (variable_control == '5' or variable_control == '6'):
        array_contactos = []
        orden = 0
        for letra, contactos in contact_book.items():
            print(letra +':')
            for contacto, value in contactos.items():
                orden += 1
                print('   ' + str(orden) + '. '+contacto)
                dict_modificado = value.copy()
                dict_modificado['nombre'] = contacto
                array_contactos.append(dict_modificado)
        if(variable_control == '5'):
            seleccionado = input('A qué contacto desea llamar?: ')
        else:
            seleccionado = input('A qué contacto desea Enviar Mensaje?: ')

        if (seleccionado.isnumeric()):
            seleccionado = int(seleccionado)
            nombre = array_contactos[seleccionado-1].get('nombre')
            telefono = array_contactos[seleccionado-1].get('telefono')
        else:
            nombre = seleccionado
            telefono = contact_book[seleccionado[0].upper()].get(seleccionado).get('telefono')     
        if(variable_control == '5'):
            print("Llamando a  "+ nombre + " al \U0001f4DE: " + telefono)    
        else:
            mensaje = input('Mensaje >>> ')
            print("Hola "+ nombre + " - " + telefono)    
            print('    > '+mensaje)
        time.sleep(3)        
        
    # Mostrar los contactos con el mismo método de iteración que la opción (3)
    # solicitar qué contacto desea utilizar para enviar un correo (nombre o número de la lista)
    # Solicitar asunto del correo
    # solicitar cuerpo del correo
    # mostrar contacto al que se le está enviando el correo junto con su dirección
    # esperar tres segundos y salir al menú principal
    elif (variable_control == '7'):
        array_contactos = []
        orden = 0
        for letra, contactos in contact_book.items():
            print(letra +':')
            for contacto, value in contactos.items():
                orden += 1
                print('   ' + str(orden) + '. '+contacto)
                dict_modificado = value.copy()
                dict_modificado['nombre'] = contacto
                array_contactos.append(dict_modificado)

        seleccionado = input('A qué contacto desea enviar Correo?: ')

        if (seleccionado.isnumeric()):
            seleccionado = int(seleccionado)
            nombre = array_contactos[seleccionado-1].get('nombre')
            email = array_contactos[seleccionado-1].get('email')
        else:
            nombre = seleccionado
            email = contact_book[seleccionado[0].upper()].get(seleccionado).get('email')     
        
        subject = input('Subject >>> ')
        mensaje = input('Mensaje >>> ')
        print("Enviando \U0001F4E7 a "+ nombre + " - " + email)    
        print('    > '+subject)
        print('    > '+mensaje)
        time.sleep(3)        



