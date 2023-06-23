from funciones_parcial import *

insumos_csv = "Insumos.csv - Hoja 1.csv"

respuesta = "si"

while respuesta == "si":

    imprimir_menu()

    respuesta_usuario = validar_entero()

    menu_principal_respuesta(respuesta_usuario, insumos_csv)