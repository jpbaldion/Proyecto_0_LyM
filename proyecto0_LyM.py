import re
"""
    Variables globales declaradas por fuera de todas las funciones para facilitar la lectura del código. 
"""
bloqs = ["while", "if", "repeat", "times"]
conditions = ["facing", "can", "not"]
valores_permitidos = [  "front",
                        "right", 
                        "left", 
                        "back",
                        "north",
                        "south",
                        "west",
                        "east",
                        "around"]
directions = ["front","right","left","back"]
cardinals = ["north","south","west","east"]
variables = {}
prodedures = {}
comands = [ "jump", 
            "walk",
            "leap",
            "turn",
            "turnto",
            "drop",
            "get",
            "grab",
            "letGo",
            "nop"
            ]

comands2_V_D_O = ["walk","leap",]
comands1_V = ["drop","get","grab","letGo"]

ultimo_proc = []

def leer_archivo(nombre_archivo: str)-> None:
    try:
        archivo = open("./Pruebas/" + nombre_archivo, 'r')
        contenido = archivo.read()
        return contenido
    except FileNotFoundError:
        return "El archivo no fue encontrado"
    except Exception as e:
        return f"Ocurrió un error: {e}"
    
def comprobar_emparejados(codigo: str)->list:
    """
        Función que comprueba que él código que le pasen por parámetro
        tenga parentesis y llaves emparejadas. Además aprovecha el
        recorrido para hacer una lista que separa las definiciones de
        variables, los bloques y la definición de procedimientos.

    """
    pila_corchetes = []
    pila_parentesis = []

    codigo_seccionado = [] #Aquí se guardan las partes que se van separando del código.
    aux = "" #Variable auxiliar para guardar cada bloque o definición del código para luego agregarlo a la lista codigo_seccionado
    seguir = True #Variable auxiliar
    n = 0 #Variable auxiliar
    
    try: 
        i = 0
        #Se realiza un ciclo while que recorre toda la lista del código
        while i < len(codigo):
            #Las comprobaciones de la variable aux en el if son para que no se confunda una de de una definición (defVar, defProc) con una de de un comando como, por ejemplo, drop().
            if codigo[i] == "d" and (aux == "" or aux == "\n" or aux.isspace()): 
                #Esta segunda comprobación sirve para saber si en el codigo hay en este punto una defVar
                #esto es importante porque las defVar son las únicas partes de código que no están delimitadas por llaves ({})
                if codigo[i] + codigo[i+1] + codigo[i+2] + codigo[i+3] + codigo[i+4] + codigo[i+5] == "defVar":
                    n = i
                    #Aquí se agrega la linea que define la variable
                    while seguir:
                        aux += codigo[n]
                        if codigo[n] == "\n" or n + 1 >= len(codigo):
                            seguir = False
                        n += 1
                    
                    seguir = True
                    
                    codigo_seccionado.append(aux)
                    #Aquí se tiene que actualizar el i porque ya dentro del if se recorrió parte de la cadena
                    i = n
                    aux = ""
                else: 
                    aux += codigo[i]
                    i += 1
            else:
                aux += codigo[i]
                #Aquí es donde se hace comprobación de las llaves y corchetes emparejados.
                if codigo[i] == "{":
                    pila_corchetes.append(1)

                elif codigo[i] == "}":
                    pila_corchetes.pop()
                    #Con este if se comprueba que la llave de cierre pertenece a un bloque grande, es decir que no pertenence a ún bloque dentro de otro
                    if len(pila_corchetes) == 0:
                        codigo_seccionado.append(aux)
                        aux = ""
                elif codigo[i] == "(":
                    pila_parentesis.append(1)
                elif codigo[i] == ")":
                    pila_parentesis.pop()

                i += 1

        if aux != "" or aux.isspace():
            codigo_seccionado.append(aux)

        if len(pila_corchetes) == 0 and len(pila_parentesis) == 0:
            return codigo_seccionado
        else:
            print(codigo_seccionado)
            return [False]
        
    except IndexError as e:
        print(e)
        print("Codigo no valido")
        return [False]

def quitar_extremos(s: str)->str:
    """
        Función auxiliar a formatear strings quitandoles los espacios y saltos de linea de los extremos,
        tanto derecho como izquierdo. 
    """
    s = s.strip("\n")
    s = s.strip(" ")
    return s

def quitar_espacios(ls: list)->list:
    """
        Función auxiliar que le quita los items vacios a la lista que se le pasa por parametro y
        retorna una lista sin esos items vacios.
    """
    sin_espacios = []
    for l in ls:
        if l != "":
            sin_espacios.append(l)

    return sin_espacios

def comprobar_nombres(nombre: str)->bool:

    """
        Función auxiliar que comprueba que el string que se le pasa por parametro no deben ser 
        palabras reservadas ni deben estar anteriormente definido como variable o procedimiento,
        además que tampoco deben emperzar por un número y solo debe tener letras y números.
    """

    if nombre[0].isnumeric():
        print("Los nombres no pueden empezar con un número")
        return False
    
    if not nombre.isalnum():
        print([nombre])
        print("Los nombres solo pueden contener letras de la 'a' a la 'z' y número de '0' al '9'")
        return False
    
    if nombre in prodedures or nombre in variables:
        print("PROCEDIMIENTOS", prodedures)
        print("VARIABLES", variables)
        print("No puedes declarar algo que ya ha sido declarado")
        return False

    
    if nombre in bloqs or nombre in conditions or nombre in comands or nombre in valores_permitidos:
        print("El nombre de un procedimiento no puede ser una palabra reservada")
        return False
    return True

def comprobar_variables(variable: list)->bool:
    """
        Función que comprueba que la lista que le pasen por parametros es equivalente a una correcta
        declaración de una variable, es decir que tenga la forma de defVar nombre n donde nombre no 
        deben ser palabras reservadas ni deben estar anteriormente definidas, además que tampoco 
        deben emperzar por un número y solo debe tener letras y números. Además que n no puede ser
        un tipo de dato que no soporte el lenguaje(orentacion, dirección, número)
    """
    if len(variable) != 3:
        declaracion = []
        for i in variable:
            if i != "":
                declaracion.append(i)
        variable = declaracion
    
    if len(variable) == 3:
        nombre = variable[1].lower()
        if not comprobar_nombres(nombre):
            return False
        
        valor = variable[2]

        if (not valor.isnumeric()) and (not (valor in valores_permitidos)):
            print("Las variables solo pueden tener como valor números, orientaciones o direcciones")
            return False
        
        variables[nombre] = valor
        return True
    else:
        print("Variable mal declarada")
        return False

def comprobar_cabecera(cabecera: str)->bool:

    """
    Función que comprueba que el string pasado por parametro sea una declaración valida de un procedimiento, 
    es decir que tenga la forma de defProc nombre(a, b, c) donde nombre y a, b, c no deben ser palabras reservadas
    ni deben estar anteriormente definidas, además que tampoco deben emperzar por un número y solo debe tener letras
    y números. 
    """

    cabecera = quitar_extremos(cabecera)
    cabecera = cabecera.split(" ", 1)
    cabecera = quitar_espacios(cabecera)[1]
    cabecera = cabecera.split("(", 1)
    nombre = cabecera[0].lower()
    nombre = quitar_extremos(nombre)
    parametros = quitar_extremos(cabecera[1])
    parametros = parametros.strip(")")

    if parametros.find(",") != -1:
        parametro = parametros.split(",")
        parametros = []
        for p in parametro:
            p = quitar_extremos(p)
            parametros.append(p)
    else:
        parametros = quitar_extremos(parametros)
        parametros = [parametros]

    if not comprobar_nombres(nombre):
        return False
    
    if parametros[0] == "":
            parametros = []
    else:
        for p in parametros:
            if not comprobar_nombres(p):
                return False
    
    prodedures[nombre] = {}
    for p in parametros:
        prodedures[nombre][p] = ""
    ultimo_proc.append(nombre)
    return True

def comprobar_repeat(repeat: str):
    """
    Función que comprueba que el string que se le pasa por parametro es una declaración valida de un repeat times.
    """

    repeat = repeat.split(" ")
    print(repeat)
    repeat = quitar_espacios(repeat)
    try:
        valor = repeat[1]
        if not(valor.isnumeric()):
            print("Error en el valor de repeat-times")
            return False

        if not(repeat[2] == "times"):
            print("Error en la escritura del repeat-times")
            return False
        return True
    except IndexError:
        print("Error")
        return False

def seccionar_bloque(bloque: str)->list:
    """
        Función a la que se pasa un string que deberá se equivalente al interior de un bloque.
        La función toma ese bloque y los secciona por comandos que se saben deben estar separados por ';'
        deja commandos por aparte y agrupa 'sub-bloques' como los whiles o los if. Importante: los if 
        los deja en 2 partes, por un lado el if y por otro el else.
    """
    i = 0
    seccionado = []
    aux = ""
    pila_corchetes = []
    while i < len(bloque):
        aux += bloque[i]
        if bloque[i] == ";":
            seccionado.append(aux)
            aux = ""
        elif bloque[i] == "i" and bloque[i+1] == "f":
            seguir = True
            while seguir:
                n = i + 1
                aux += bloque[n]
                if bloque[n] == "{":
                    pila_corchetes.append(1)
                elif bloque[n] == "}":
                    pila_corchetes.pop()
                    #Con este if se comprueba que la llave de cierre pertenece a un bloque grande, es decir que no pertenence a ún bloque dentro de otro
                    if len(pila_corchetes) == 0:
                        seccionado.append(aux)
                        aux = ""
                        seguir = False
                i = n

        elif bloque[i] == "w" and bloque[i+1] == "h" and bloque[i+2] == "i" and bloque[i+3] == "l" and bloque[i+4] == "e":
            seguir = True
            while seguir:
                n = i + 1
                aux += bloque[n]
                if bloque[n] == "{":
                    pila_corchetes.append(1)
                elif bloque[n] == "}":
                    pila_corchetes.pop()
                    #Con este if se comprueba que la llave de cierre pertenece a un bloque grande, es decir que no pertenence a ún bloque dentro de otro
                    if len(pila_corchetes) == 0:
                        seccionado.append(aux)
                        aux = ""
                        seguir = False
                i = n

        elif i == len(bloque) - 1:
            seccionado.append(aux)

        i += 1
    return seccionado

def comprobar_condicion_proc(condicion: str, procedimiento: str):
    condicion = condicion.split("(", 1)
    cond = quitar_extremos(condicion[0])
    if not(cond in conditions):
        return False
    comando = quitar_extremos(condicion[1])
    #TODO pasar comando por la funcion que comprueba comandos que vienen de un procedimiento
    return True
def comprobar_condicion(condicion: str):
    pass

def comprobar_if(condicion: str, sino: str):
    pass

def comprobar_if_proc(condicion: str, sino: str, procedimiento: str):
    condicion = condicion.split("{", 1)
    cond = condicion[0]
    cuerpo = quitar_extremos(condicion[1])
    sino = quitar_extremos(sino)

    #Comprobar la condición
    cond = cond.split(" ")
    cond = quitar_extremos(cond[1])
    if not comprobar_condicion_proc(cond, procedimiento):
        print("Mala condición")
        return False
    #Comprobar el cuerpo del if
    cuerpo = quitar_extremos(cuerpo.rstrip("}"))
    if comprobar_bloque(cuerpo):
        print("F")
        return False
    #comprobar el else
    if sino.endswith(";"):
        sino = quitar_extremos(sino.lstrip("else"))
        sino = quitar_extremos(sino.lstrip("{"))
        sino = quitar_extremos(sino.rstrip("}"))
        if not comprobar_bloque(sino):
            pass
            #return False
    return True

#    print(cond)
#    print(cuerpo)
#    print(sino)

    return True
    

def comprobar_while(ciclo: str):
    pass

def comprobar_while_proc(ciclo: str, procedimiento: str):
    pass

def comprobar_bloque(bloque: list):
    pass

def comprobar_bloque_proc(bloque: list, procedimiento: str):
    print("BLOque", bloque)
    i = 0
    while i < len(bloque):
        print("I", i)
        b = quitar_extremos(bloque[i])
        if b.startswith("if"):
            i += 1
            sino = quitar_extremos(bloque[i])
            if not comprobar_if_proc(b, sino, procedimiento):
                print("RAIos")
                return False
        elif b.startswith("while"):
            pass
        else:
            comprobarComandosDefProc(bloque[i], procedimiento)
        i += 1

def comprobar_bloques(codigo_bloques: list)->bool:
    """
    Función que recorre la lista con el codigo partido por bloques y comprueba bloque a bloque
    que sea valido, tan pronto encuentra algo invalido, se detiene y retorna false que quiere decir
    que el codigo es invalido. Si retorna true el codigo es valido. 
    
    """

    simb = ["{","}"," ","","},","{,",","]
    aux = 0
    print("SECCIONADO", codigo_bloques)
    for b in codigo_bloques:
        aux += 1
        b = quitar_extremos(b)
        
        if b.startswith("defVar"):
            defVar = b.split(" ")
            valid_var = comprobar_variables(defVar)
            if not valid_var:
                print("Error encontrado en:", " ".join(defVar))
                return False
        elif b.startswith("defProc"):
            cabecera = ""
            cuerpo = ""
            

            i = 0
            while b[i] != "{":
                cabecera += b[i]
                i += 1
            print("CABECERA", cabecera)
            valid_cabecera = comprobar_cabecera(cabecera)
            if not valid_cabecera:
                print("Error encontrado en ", cabecera)
                return False


            cuerpo = b[i:]
            cuerpo = quitar_extremos(cuerpo)
            cuerpo = cuerpo.lstrip("{")
            cuerpo = cuerpo.rstrip("}")
            cuerpo = quitar_extremos(cuerpo)

            if "while " in cuerpo or ("if " in cuerpo and "else " in cuerpo):
                cuerpo = seccionar_bloque(cuerpo)
            else:
                cuerpo = cuerpo.split(";")

            print(cuerpo)
            comprobar_bloque_proc(cuerpo, ultimo_proc)
            
            #TODO Aquí luego se recorre la variable cuerpo comprobando linea por linea que todo esté bien.
            # Se usaría la función de comprobar comandos y otra de pruebe if(s) y otra que pruebe while(s)
            print(cuerpo)
        elif b.startswith("{"):
            bloque = seccionar_bloque(b)
            print(bloque)
            #TODO Aquí luego se recorre la variable bloque comprobando linea por linea que todo esté bien.
            # Se usaría la función de comprobar comandos y otra de pruebe if(s) y otra que pruebe while(s)
        elif b.startswith("repeat"):
            repeticion = b.split("{", 1)
            
            repeat = repeticion[0]
            repeat = quitar_extremos(repeat)

            valid_repeat = comprobar_repeat(repeat)
            if not valid_repeat:
                print(repeat)
                return False
            else: print("repeat valido")
            
            cuerpo = repeticion[1]
            cuerpo = quitar_extremos(cuerpo)
            cuerpo = cuerpo.rstrip("}")
            cuerpo = seccionar_bloque(cuerpo)



            #TODO Aquí luego se recorre la variable cuerpo comprobando linea por linea que todo esté bien.
            # Se usaría la función de comprobar comandos y otra de pruebe if(s) y otra que pruebe while(s)
        else: 
            return False
    return True

def comprobarComandos(bloque: list):
    i = 0
    while i < len(bloque):
        bloque[i] = bloque[i].strip("\n")
        bloque[i] = re.sub(" ","",bloque[i])
        bloque[i] = bloque[i].lstrip(" ")
        bloque[i] = bloque[i].rstrip(" ")
        i += 1
    x = 0
    c = True
    while x < len(bloque):
        cadena = ""
        for i in bloque[x]:
            if cadena in comands2_V_D_O:
                if len(bloque[x]) == 7:
                    if bloque[x][-2].isnumeric():
                        c = True
                    else:
                        c = False
                elif len(bloque[x]) == 9:
                    if bloque[x][len(cadena)+2].isnumeric():
                        c = True
                    else:
                        c = False
                    if bloque[x][len(cadena)+4] in directions or bloque[x][len(cadena)+4] in cardinals:
                        c = True
                    else:
                        c = False
            elif cadena in comands1_V:
                pos_parent = bloque[x].index("(")
                if bloque[x][pos_parent+1].isnumeric():
                    c = True
                else:
                    c = False
            elif cadena == "jump":
                if bloque[x][len(cadena)+2].isnumeric():
                        c = True
                else:
                    c = False
                if bloque[x][len(cadena)+4].isnumeric():
                    c = True
                else:
                    c = False
            elif cadena == "turn":
                if bloque[x][-2] in directions:
                        c = True
                else:
                    c = False
            elif cadena == "turnto":
                if bloque[x][-2] in cardinals:
                        c = True
                else:
                    c = False
            elif cadena.lower() in ultimo_proc:
                if bloque[x][len(cadena)+1].isnumeric():
                    c = True
                elif bloque[x][len(cadena)+1] in valores_permitidos:
                    c = True
                if bloque[x][len(cadena)+3].isnumeric():
                    c = True
                elif bloque[x][len(cadena)+3] in valores_permitidos:
                    c = True
                else:
                    c = False
            else:
                cadena += i
                
        x += 1
                    
                    
    return c
    
def comprobarComandosDefProc(comando: str, procedimiento: str)->bool:
    print("COMANDO", comando)
    comando = comando.split("(", 1)
    nombre = quitar_extremos(comando[0])
    print("NOMBRE", nombre)
    if nombre in comands:
        print("siu")
        pass
    elif nombre.lower() in variables:
        print("nou")
        pass
    elif nombre.lower() in prodedures:
        print("cool")
        pass
    else:
        print("NINGUNO")
    # x = 0
    # c = True

    # if cadena in comands2_V_D_O:
    #     if len(bloque[x]) == 7:
    #         if bloque[x][-2].isnumeric():
    #             c = True
    #         elif bloque[x][-2] in para:
    #             c = True
    #         else:
    #             c = False
    #     elif len(bloque[x]) == 9:
    #         if bloque[x][len(cadena)+2].isnumeric():
    #             c = True
    #         elif bloque[x][len(cadena)+2] in para:
    #             c = True
    #         else:
    #             c = False
    #         if bloque[x][len(cadena)+4] in directions or bloque[x][len(cadena)+4] in cardinals:
    #             c = True
    #         elif bloque[x][len(cadena)+4] in para:
    #             c = True
    #         else:
    #             c = False
    # elif cadena in comands1_V:
    #     pos_parent = bloque[x].index("(")
    #     if bloque[x][pos_parent+1].isnumeric():
    #         c = True
    #     elif bloque[x][pos_parent+1] in para:
    #         c = True
    #     else:
    #         c = False
    # elif cadena == "jump":
    #     if bloque[x][len(cadena)+2].isnumeric():
    #             c = True
    #     elif bloque[x][len(cadena)+2] in para:
    #         c = True
    #     else:
    #         c = False
    #     if bloque[x][len(cadena)+4].isnumeric():
    #         c = True
    #     elif bloque[x][len(cadena)+4] in para:
    #         c = True
    #     else:
    #         c = False
    # elif cadena == "turn":
    #     if bloque[x][-2] in directions:
    #             c = True
    #     elif bloque[x][-2] in para:
    #         c = True
    #     else:
    #         c = False
    # elif cadena == "turnto":
    #     if bloque[x][-2] in cardinals:
    #             c = True
    #     elif bloque[x][-2] in para:
    #         c = True
    #     else:
    #         c = False
    # elif cadena.lower() == proc:
    #     if bloque[x][len(cadena)+1].isnumeric():
    #         c = True
    #     elif bloque[x][len(cadena)+1] in valores_permitidos:
    #         c = True
    #     if bloque[x][len(cadena)+3].isnumeric():
    #         c = True
    #     elif bloque[x][len(cadena)+3] in valores_permitidos:
    #         c = True
    #     else:
    #         c = False
    # else:
    #     cadena += i
        
    # x += 1
                    
                    
    # return c               
        
    
def ejecutar():
    nombre_archivo = input("Ingrese el nombre del archivo: ")
    codigo = leer_archivo(nombre_archivo)
    result = (comprobar_emparejados(codigo))
    if result[0] != False:
        print("El codigo tiene corchetes y parentesis emparejados")
        print("Sin embargo, seguiremos estudiandolo")
        if not comprobar_bloques(result):
            print("El codigo no es valido")
        print(prodedures)
    else:
        print("Codigo no valido")

ejecutar()