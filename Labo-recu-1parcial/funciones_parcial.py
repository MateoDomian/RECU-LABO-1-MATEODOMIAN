import re
import json
import csv
import random
import os


# funcion imprime menu completo
# parametro 
# retorno 
def imprimir_menu():

    print("\n\nMenu principal\n")
    print("1. Extraccion de datos desde el CSV")
    print("2. Mostrar cantidad de elementos por Marca")
    print("3. Mostrar elementos por Marca")
    print("4. Busqueda de elementos por caractiristica")
    print("5. Listar insumos ordenados")
    print("6. Realizar Compras")
    print("7. Guardar Discos duro en JSON")
    print("8. Leer JSON")
    print("9. Actualizar precios, valor Mayo")
    print("10. Agregar insumo")

# funcion es el menu del programa principal
# parametro respuesta usuario(int), archivo.csv
# retorno 
def menu_principal_respuesta(respuesta_usuario, insumos_csv):

    match(respuesta_usuario):

        case "1":

            global flag_extraccion_datos

            global insumos_csv_diccionario

            insumos_csv_diccionario = traer_datos_csv(insumos_csv)

            insumos_csv_diccionario = agregar_stock(insumos_csv_diccionario)

            flag_extraccion_datos = 1

        case "2":

            try:

                if flag_extraccion_datos:

                    os.system("cls")

                    marca_por_cantidad(insumos_csv_diccionario)
            
            except:

                mensaje_error()

        case "3":

            try:

                if flag_extraccion_datos:

                    marca_por_elementos(insumos_csv_diccionario)
            
            except:

                mensaje_error()

        case "4":

            try:

                if flag_extraccion_datos:

                    if busqueda_caracteristica(insumos_csv_diccionario) == 0:

                        print("Error, no se encuentra la caracteristica")
            
            except:

                mensaje_error()

        case "5":

            try:

                if flag_extraccion_datos:

                    ordenar_lista(insumos_csv_diccionario)
            
            except:

                mensaje_error()
            

        case "6":

            global diccinario_compras

            global cantidad

            try:

                if flag_extraccion_datos:

                    os.system("cls")

                    diccinario_compras, cantidad = realizar_compras(insumos_csv_diccionario)

                    factura_de_compra(diccinario_compras, 'ticket.txt', cantidad)
            
            except:

                mensaje_error()


        case "7":

            try:

                if flag_extraccion_datos:

                    lista_discos_duro = extraer_discos_duro(insumos_csv_diccionario)

                    with open('insumos.json', 'w', encoding = 'utf8') as archivo:

                        json.dump(lista_discos_duro, archivo, indent = 4, ensure_ascii=False)
                    
                    print("\n------------------------------------------")    
                    print("Los datos fueron extraidos del archivo JSON")    
                    print("------------------------------------------\n") 

                    global archivo_json 

                    archivo_json = True

            except:

                mensaje_error()

        case "8":

            try:

                if traer_datos_csv and archivo_json:

                    with open('insumos.json', 'r', encoding = 'utf8') as archivo:

                        carga_json = json.load(archivo)

                        mostrar_lista_disco_duro(carga_json)

            except:

                mensaje_error()

        case "9":

            try:

                if flag_extraccion_datos:

                    actualizar_precios(insumos_csv_diccionario, 8.4)
            
            except:

                mensaje_error() 
            

        case "10":


            try:
                if flag_extraccion_datos:

                    agregar_insumo(insumos_csv)
            
            except:

                mensaje_error()

# funcion  que se usa para imprimir cada producto
# parametro producto 
# retorno
def printeo(insumo):

    for key, value in insumo.items():
        



        if key == "CARACTERISTICAS":

            print(key)
            for x in value:
                print(x)

        print(key, value)

# funcion que imprime un mensaje de error en consola
# parametro
# retorno
def mensaje_error():

    print("\n------------------------------------------------------")    
    print("Error, debe realizar la extraccion de datos primero...")
    print("------------------------------------------------------")    

# funcion que valida que la respuesta del usuario sea un int, (para el menu principal)
# parametro
# retorno es la respuesta del user
def validar_entero():

    respuesta_usuario = input("Ingrese un numero del menu: ")

    while True:

        if (respuesta_usuario.isdigit()) == False:

            respuesta_usuario = input("Error, ingrese un numero del menu: ")
        
        else:

            break
        
    return respuesta_usuario

# funcion transforma el str de precio, en un float
# parametro el diccionario de insumos
# retorno boleano
def normalizar_datos(insumos_csv_diccionario):

    flag_cambios = False

    for linea in insumos_csv_diccionario:

        for clave in linea:

            value = linea[clave]

            if clave == "PRECIO":

                value = float(value)
                flag_cambios = True

    return flag_cambios

# funcion que extrae todas las lineas del csv, de forma ordenada, sin el signo $, ni el |!*| que separa la caract
# parametro archivo.csv
# retorno devuelve una lista con diccionarios
def traer_datos_csv(insumos_csv):

    bandera_clave = 0

    diccionario_insumos_csv = []

    with open(insumos_csv, 'r', encoding = 'utf8') as archivo:

        lector_archivo_csv = archivo.readlines()

        for fila in lector_archivo_csv:

            fila = fila.strip('\n')
            fila = fila.replace('"', '')
            fila = fila.replace('$', '')

            if bandera_clave == 0:

                listado_clave = fila.split(',')

                bandera_clave = 1

            else:

                listado_fila = fila.split(',')

                diccionario_datos = listado_fila[4].split('|!*|')

                listado_fila[4] = diccionario_datos

                diccionario_insumos_csv.append(dict(zip(listado_clave, listado_fila)))

        normalizar_datos(diccionario_insumos_csv)        

        print("\n------------------------------------------")    
        print("Los datos fueron extraidos del archivo CSV")    
        print("------------------------------------------\n") 

    return diccionario_insumos_csv

# funcion imprime todas las marcas, con la cantidad de elementos de cada una
# parametro lista de diccionarios
# retorno
def marca_por_cantidad(insumos_csv_diccionario):
    
    lista_en_cero = []
    
    lista_de_marcas = []
    
    for linea in insumos_csv_diccionario:
        
        for clave in linea:
            
            if clave == "MARCA":
                
                lista_de_marcas.append(linea[clave])

    setear_marcas = set(lista_de_marcas)
    
    for i in range(len(setear_marcas)):
        
        lista_en_cero.append(0)
        
    dic_marcas_ceros = dict(zip(setear_marcas, lista_en_cero))
    
    for linea in insumos_csv_diccionario:
        
        for clave in linea:
            
            if clave == "MARCA":
                
                dic_marcas_ceros[linea[clave]] = dic_marcas_ceros[linea[clave]] + 1


    print("\nMarcas y cantidad de insumos: \n")

    for marca, cantidad in dic_marcas_ceros.items():
        print(f"{marca:<16} | {cantidad:>2}")
        print("----------------------------")

# funcion  imprime todos los productos, separados por marca
# parametro lista de diccionarios
# retorno
def marca_por_elementos(insumos_csv_diccionario):

    lista_de_marcas = []

    for linea in insumos_csv_diccionario:
        
        for clave in linea:
            
            if clave == "MARCA":
                
                lista_de_marcas.append(linea[clave])

    setear_marcas = set(lista_de_marcas)

    for marca in setear_marcas:

        print("--------------{}--------------".format(marca))

        for linea in insumos_csv_diccionario:
        
            for clave in linea:
            
                if clave == "MARCA":

                    if linea[clave] == marca:


                        print("¬¬¬¬  {:<52} | Precio: ${:<8}|".format(linea["NOMBRE"], linea["PRECIO"]))

# funcion busca una caracteristica, usando un match e imprime todas las que contengan la misma
# parametro lista de diccionarios
# retorno boleano 
def busqueda_caracteristica(insumos_csv_diccionario):

    valor_busqueda = input("\nIngrese la caracteristica que desea buscar: ").lower()

    retorno = 0

    for insumo in insumos_csv_diccionario:

        for caracteristica in insumo["CARACTERISTICAS"]:

            if re.match(valor_busqueda, caracteristica, re.IGNORECASE):

                # print(insumo)
                # retorno = 1

                print("ID: {:<3} | Dispositivo: {:<15} | Marca {:<10} |Precio: {:<8} | Caracteristica {} | Stock: {:<3}".format(
                    insumo.get("ID", "No disponible"),
                    insumo.get("MARCA", "No disponible"),
                    insumo.get("NOMBRE", "No disponible"),
                    insumo.get("PRECIO", "No disponible"),
                    insumo["CARACTERISTICAS"],
                    insumo.get("STOCK", "No disponible")
                ))

    return retorno

# funcion ordena todos los insumos por Marca y si tienen la misma marca por precio, usando un Sorted()
# parametro lista de diccionarios
# retorno
def ordenar_lista(insumo_csv_diccionario):

    lista_ordenada = sorted(insumo_csv_diccionario, key= lambda x: (x["MARCA"], x["PRECIO"]))

    for elemento in lista_ordenada:

        print("------------------------------------------------")

        printeo(elemento)

# funcion funcion que muestra las marcas y hace seleccionar para luego proceder con las compras 
# parametro lista de diccionarios
# retorno lista id que es usada como "carrito de compras"
def seleccionar_marca_compras(insumos_csv_diccionario):

    lista_de_marcas = []
    lista_id = []

    for linea in insumos_csv_diccionario:
        
        for clave in linea:
            
            if clave == "MARCA":
                
                lista_de_marcas.append(linea[clave])

    setear_marcas = set(lista_de_marcas)

    print("Todas las marcas son {}".format(setear_marcas))

    marca_input = input("Ingrese que marca desea buscar: ")

    print("********      {}      ********".format(marca_input))

    for marca in setear_marcas:

        for linea in insumos_csv_diccionario:

            for clave in linea:

                if clave == "MARCA":

                    if linea[clave] == marca:

                        if marca_input == linea[clave]:

                            print("ID: {} | Dispositivo: {} | Precio: {} | Stock: {}".format(
                                    linea.get("ID", "No disponible"),
                                    linea.get("NOMBRE", "No disponible"),
                                    linea.get("PRECIO", "No disponible"),
                                    linea.get("STOCK", "No disponible")
                                ))

                            lista_id.append(linea["ID"])

                            

    return lista_id

# funcion funcion que valida que puedas comprar el objeto y que tenga stock disponible
# parametro lista de diccionarios
# retorno carrito de compras
def realizar_compras(insumos_csv_diccionario):

    carrito_compras = []
    carrito_cantidad = []
    stock_producto = 0
    respuesta = "s"

    while respuesta == "s":

        validacion_id = seleccionar_marca_compras(insumos_csv_diccionario)

        id_seleccionado = input("\nIngrese el numero de ID que desea Comprar: ")

        for linea in insumos_csv_diccionario:

            for clave in linea:

                if clave == "ID":

                    if linea[clave] == id_seleccionado:

                        if id_seleccionado in validacion_id:

                            stock_producto = linea["STOCK"]

                            cantidad = int(input("\nCual es la cantidad del producto que desea comprar?: "))

                            if cantidad > 0 and cantidad <= stock_producto:

                                stock_producto -= cantidad

                                linea["STOCK"] = stock_producto

                                carrito_compras.append(linea)
                                carrito_cantidad.append(cantidad)

                                print("\n\nEl producto se agrego correctamente\n\n")

                            else:

                                print("\nError, no se encuentra disponible stock de este producto\n")
                                print("\nContamos con: {} de stock en este momento\n".format( linea["STOCK"]))

                        else:

                            print("\nError, no se encuentra el id\n") 

        respuesta = input("\nDesea comprar otro producto ? s / n:  ")

        while respuesta != "s" and respuesta != "n":

            respuesta = input("\nError, Desea comprar otro producto ? s / n: ")

    print(carrito_compras)
    return carrito_compras, carrito_cantidad

# funcion se encarga de hacer el archivo donde se encuentra los productos, el subtotal y el total
# parametro diccionario de la funcion de realizar_compras, archivo compra(ticket) carrito de la funcion de realizar_compras
# retorno
def factura_de_compra(diccinario_compras, archivo_compra, carrito_cantidad):

    total = 0

    with open(archivo_compra, 'w') as archivo:

        archivo.write(

            "--------------------------------------------------------------------\n\n"
            "\nfactura A\n\n"
            "\nProductos totales"
        )

        for producto, numero in zip(diccinario_compras, carrito_cantidad):

            total += float(producto["PRECIO"]) * numero

            archivo.write(f"\nProducto: {producto['NOMBRE']}, \n\nPrecio: ${producto['PRECIO']}, \n\nCantidad: {numero}\n\n")

        print("--------------------------------------------------------------------\n\n")
        archivo.write(f"\n Total: ${total}")
        print("El diccionario se guardo correctamente en {archivo_compras}.")

# funcion se encarga de separar todos los insumos que contengan "Disco Duro" en su nombre y los separa a un .json
# parametro lista de diccionarios
# retorno la lista de discos duros
def extraer_discos_duro(insumos_csv_diccionario):

    lista_discos_duros = []

    encontrar_discos_duros = r'Disco Duro'

    for linea in insumos_csv_diccionario:

        for clave in linea:

            if clave == "NOMBRE":

                busqueda = linea[clave]

                fin = re.search(encontrar_discos_duros, busqueda)

                if fin:

                    lista_discos_duros.append(linea)
    
    return lista_discos_duros


# funcion que muestra el .json extraido
# parametro lista de diccionarios
# retorno 
def mostrar_lista_disco_duro(insumos_csv_diccionario):

    for linea in insumos_csv_diccionario:

        print(linea)


# funcion que actualiza todos los precios de los productos, aumentandolos un 8.4% cada vez que se llame a la funcion
# parametro lista de diccionarios
# retorno 
def actualizar_precios(insumos_csv_diccionario, porcentaje: float):

    lista_precios = []

    for linea in insumos_csv_diccionario:

        lista_precios.append(float(linea["PRECIO"]))

    aumento = list(map(lambda precio: precio + ((precio * porcentaje) / 100), lista_precios))

    for i in range(len(insumos_csv_diccionario)):

                insumos_csv_diccionario[i]["PRECIO"] = aumento[i]

    with open("Insumos.csv - Hoja 1.csv", "w", encoding="utf-8") as archivo:

        for linea in insumos_csv_diccionario:

            archivo.write(f"{linea}\n")

# funcion agrega un producto al archivo csv.
# parametro archivo.csv para poder sobreescribirlo 
# retorno 
def agregar_insumo(insumos_csv="Insumos.csv - Hoja 1.csv"):

    insumo = {}

    id_predeterminado = 50

    nuevo_id = id_predeterminado +1

    insumo['ID'] = str(nuevo_id)

    insumo['nombre'] = input("Ingrese el nombre del insumo: ")

    insumo['marca'] = input("Ingrese la marca del insumo: ")

    insumo['precio'] = input("Ingrese el precio del insumo: ")

    insumo['caracteristicas'] = input("Ingrese las características del insumo: ")

    with open(insumos_csv, 'a', newline='') as archivo_csv:

        campos = ['ID','nombre', 'marca', 'precio', 'caracteristicas']

        escritor_csv = csv.DictWriter(archivo_csv, fieldnames=campos, quoting=csv.QUOTE_NONNUMERIC)

        archivo_csv.write('\n')
        
        escritor_csv.writerow(insumo)

    print("Insumo agregado exitosamente al archivo CSV.")

# funcion que mediante el la funcion map. y la funcion random.radint crea un numero aleatorio, y lo agrega al final del diccionario, usando el **
# parametro lista de diccionarios
# retorno lista con el producto con stock
def agregar_stock(insumos_csv_diccionario):

    return list(map(lambda insumo: {**insumo, 'STOCK': int(random.randint(0,10))}, insumos_csv_diccionario))