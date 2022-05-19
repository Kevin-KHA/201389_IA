import math
import random
import re
from matplotlib import pyplot
from PyQt5 import QtWidgets, uic
import cv2

# desplegamos
app = QtWidgets.QApplication([])

# Cargamos ventanas
interfaz = uic.loadUi("vistas/principal.ui")
interfazError = uic.loadUi("vistas/error.ui")

# lista para guardar los individuos generados y cruzados
individuos_Generados = []
arregloSeleccion = []
argAleatorios = []
individuos_Cruza = []
individous_Resultantes_deCruza = []
argMutados1 = []
argMutados2 = []
generacion = 1

# Obtenemos datos de las cajas de texto
def obtenerDatos():
    avalue = interfaz.txta.text()
    bvalue = interfaz.txtb.text()
    precision = interfaz.txtPrec.text()
    povalue = interfaz.txtPo.text()
    pmaxvalue = interfaz.txtPm.text()
    cantidadGen = interfaz.txtGen.text()
    pd = interfaz.txtPD.text()
    pmi = interfaz.txtPMI.text()
    pmg = interfaz.txtPMG.text()
    # validamos que no esten vacios
    if len(avalue) == 0 or len(bvalue) == 0 or len(precision) == 0 or len(povalue) == 0 or len(pmaxvalue) == 0 or len(
            pd) == 0 or len(pmi) == 0 or len(pmg) == 0 or len(cantidadGen) == 0:
        mostrarErrorLabel("Debe llenar todos los campos")
    else:
        interfaz.lblError.setText("")
        partition = precision.partition('.')
        if precision.isdigit():
            newelement = float(precision)
            validarEntradas(avalue, bvalue, precision, povalue, pmaxvalue, pd, pmi, pmg, cantidadGen)
        elif (partition[0].isdigit() and partition[1] == '.' and partition[2].isdigit()) or (
                partition[0] == '' and partition[1] == '.' and partition[2].isdigit()) or (
                partition[0].isdigit() and partition[1] == '.' and partition[2] == ''):
            newelement = float(precision)
            validarEntradas(avalue, bvalue, precision, povalue, pmaxvalue, pd, pmi, pmg, cantidadGen)
        else:
            mostrarError()


# Metodo para saber si los caracteres ingresados son numéricos
def validarEntradas(a, b, prec, init, max, pd, pmi, pmg, generaciones):
    num_format = re.compile(r'^-?[0-9][0-9]*$')
    valorA = re.match(num_format, a)
    valorB = re.match(num_format, b)
    valorInit = re.match(num_format, init)
    valorMax = re.match(num_format, max)
    valorPd = re.match(num_format, pd)
    valorPmi = re.match(num_format, pmi)
    valorPmg = re.match(num_format, pmg)
    valorGen = re.match(num_format, generaciones)
    if valorA and valorB and valorInit and valorMax and valorPd and valorPmi and valorPmg and valorGen:
        print("todos son números")
        Pd = int(interfaz.txtPD.text())
        Pmi = int(interfaz.txtPMI.text())
        Pmg = int(interfaz.txtPMG.text())
        if (0 < Pd <= 100) and (0 < Pmi <= 100) and (0 < Pmg <= 100):
            print("RANGOS DE PROBABILIDAD CORRECTOS")
            calcularValores(a, b, prec)
        else:
            mostrarErrorLabel("El % de probabilidad debe estar entre 1 - 100")
    else:
        print("no son números")
        mostrarError()


# para los calculos de numero de soluciones, bits
def calcularValores(a, b, prec):
    # Convertimos datos de entrada
    a = int(interfaz.txta.text())
    b = int(interfaz.txtb.text())
    prec = float(interfaz.txtPrec.text())
    # calculamos numero de soluciones
    solucion = ((b - a) / prec) + 1
    print("Número de soluciones:", solucion)
    # calculamos bits a usar
    bits = math.ceil(math.log(solucion, 2))
    print("potencia encontrada:", bits)
    cantidadGen = int(interfaz.txtGen.text())
    for inicio in range(0, cantidadGen):
        generarIndiviuos(solucion - 1, bits,inicio+1)
        individuos_Generados.clear()
        arregloSeleccion.clear()
        argAleatorios.clear()
        individuos_Cruza.clear()
        individous_Resultantes_deCruza.clear()
        argMutados1.clear()
        argMutados2.clear()
        individuos_pDescendencia.clear()
        valores_deX.clear()
        valores_deY.clear()
        argpara_X.clear()
        argpara_Y.clear()
    generarVideo(cantidadGen)


# metodo para generar y guardar individuos de la población
def generarIndiviuos(tope, potencia, inicio):
    poblacionInicial = int(interfaz.txtPo.text())
    print("----------------------------------------------")
    for index in range(poblacionInicial):
        # rango entre 1 y soluciones
        numero = random.randint(1, tope)
        individuo = format(numero, "b")
        print("Binario del individuo #", index + 1, ":", individuo)
        if len(individuo) < potencia:
            cantidad_ceros = potencia - len(individuo)
            print("le faltan", cantidad_ceros, "ceros al #", index + 1)
            individuos_Generados.append("0" * cantidad_ceros + individuo)
        else:
            individuos_Generados.append(individuo)
    realizarSeleccion(potencia-1, inicio)
    print("----------------------------------------------")


# Metodo para hacer la seleccion
def realizarSeleccion(bits, inicio):
    n1 = 0
    n2 = 1
    print("Estamos en seleccion------------------------------")
    print("GENERADOS en seleccion",individuos_Generados)
    while n1 < len(individuos_Generados):
        auxBinario1 = individuos_Generados[n1]
        while n2 < len(individuos_Generados):
            auxBinario2 = individuos_Generados[n2]
            individuos_Cruza.append(
                (auxBinario1, auxBinario2, random.randint(1, bits)))
            n2 += 1
        n1 += 1
        n2 = n1 + 1
    for x in individuos_Cruza:
        argMutados2.append(x)
    validarPromedioDescendencia()
    realizarCruza(inicio)

#metodo para verificar individuos con PD
individuos_pDescendencia = []
def validarPromedioDescendencia():
    print("Estamos en PromedioDescendencia-----------")
    print("lista de la CRUZA", individuos_Cruza)
    p_Desendencia = (float(interfaz.txtPD.text())) / 100
    for index in individuos_Cruza:
        nrandom = (random.randint(1, 100))/100
        if nrandom <= p_Desendencia:
            individuos_pDescendencia.append(index)
        else:
            print("SE va: ", index)


# metodo para hacer la cruza de los bits entre las parejas
def realizarCruza(inicio):
    print("----------llegó a realizarCruza----------------")
    for index in individuos_pDescendencia:
        arregloAux1 = index[0]
        arregloAux2 = index[1]
        cortarArregloAux1 = arregloAux1[0:index[2]]
        cortarArregloAux2 = arregloAux2[0:index[2]]
        res1 = arregloAux1[index[2]:]
        res2 = arregloAux2[index[2]:]
        individous_Resultantes_deCruza.append(((cortarArregloAux1 + res2),
                                               (random.randint(1, 100) / 100),
                                               (cortarArregloAux2 + res1),
                                               (random.randint(1, 100) / 100)))
    realizarMutacion(individous_Resultantes_deCruza, inicio)


# metodo para convertir el numero binario a decimal
def convertir_Bin_Dec(bin):
    auxDec = 0
    for index, cadena in enumerate(bin[::-1]):
        auxDec += int(cadena) * 2 ** index
    return auxDec


# mutación de gen
def realizarMutacion(individuos, inicio):
    print("-----metodo para mutar gen-----")
    binariosLista = []
    strAuxiliar = ""
    mutados = list()
    for itera in individuos:
        mutados.append(list(itera))
    pm_Gen = (float(interfaz.txtPMG.text())) / 100
    pm_Individuo = (float(interfaz.txtPMI.text())) / 100
    for i in mutados:
        try:
            if i[1] <= pm_Individuo:
                    arregloBin = i[0]
                    for j in arregloBin:
                        numAleatorio = (random.randint(1, 100)) / 100
                        if numAleatorio <= pm_Gen:
                            if j == '0':
                                strAuxiliar += '1'
                            elif j == "1":
                                strAuxiliar += '0'
                        else:
                            strAuxiliar += j
                    i[0] = strAuxiliar
                    strAuxiliar = ""

            if i[3] <= pm_Individuo:
                    arregloBin = i[2]
                    for j in arregloBin:
                        numAleatorio = (random.randint(1, 100)) / 100
                        if numAleatorio <= pm_Gen:
                            if j == '0':
                                strAuxiliar += '1'
                            elif j == "1":
                                strAuxiliar += '0'
                        else:
                            strAuxiliar += j
                    i[2] = strAuxiliar
                    strAuxiliar = ""
        except ValueError:
            print("Error ", ValueError)
    for k in mutados:
        binariosLista.append(k[0])
    realizarLimpieza(binariosLista, inicio)


# aqui realizamos la limpieza segun el promedio
def realizarLimpieza(listaBinarios, inicio):
    print("inicia limpieza-----------------------------")
    a = int(interfaz.txta.text())
    b = int(interfaz.txtb.text())
    prec = float(interfaz.txtPrec.text())
    # calculamos numero de soluciones
    solucion = ((b - a) / prec) + 1
    numDecimales = []
    print("lista de bin", listaBinarios)
    for individuo in listaBinarios:
        if convertir_Bin_Dec(individuo) <= solucion:
            numDecimales.append(convertir_Bin_Dec(individuo))
    listaAux = list()
    for iniciales in individuos_Generados:
        listaAux.append(convertir_Bin_Dec(iniciales))
    for x in numDecimales:
        listaAux.append(x)
    print("termina realiza limp---------------")
    calcularPromedio(listaAux)
    generar_historico(inicio)
    realizarPoda(listaAux, inicio)

# metodo para generar la grafica que contiene mejor, peor y promedio
def generar_historico(inicio):
    print(inicio)
    if inicio == int(interfaz.txtGen.text()):
        print("ESTA GENERANDO HISTORICO")
        print("si entro a historico")
        print(arg_Historico)
        auxuliar = []
        argPeor = []
        argPromedio = []
        argMejor = []
        iter = 0
        for i in arg_Historico:
            argMejor.append(i[0])
            argPromedio.append(i[1])
            argPeor.append(i[2])
            iter += 1
            auxuliar.append(iter)
        figura = pyplot.figure(figsize=(12, 7))
        pyplot.title(f"Gráfico Histórico")
        pyplot.plot(auxuliar, argMejor, label="Mejor")
        pyplot.plot(auxuliar, argPromedio, label="Promedio")
        pyplot.plot(auxuliar, argPeor, label="Peor")
        pyplot.legend()
        pyplot.show()

# para datos para mejor, peor y promedio
def calcularPromedio(decimales):
    try:
        print("CALCULANDO MEJOR, PROMEDIO Y PEOR---------------------")
        calcularX(decimales, 1)
        calcularY()
        arregloAux_Y = argpara_Y
        arregloAux_Y.sort(reverse=True)
        mejor = arregloAux_Y[0]
        peor = arregloAux_Y[len(arregloAux_Y)-1]
        print("peor", peor)
        print("mejor", mejor)
        promedio = (peor + mejor) / 2
        print("individuo promedio calculado", promedio)
        guardar_pmm(mejor, promedio, peor)
    except ValueError:
        print(ValueError)


# guardamos en un arreglo el mejor, promedio y peor
arg_Historico = []
def guardar_pmm(mejor, promedio, peor):
    arg_Historico.append((mejor, promedio, peor))


def realizarPoda(arreglo, inicio):
    print("INICIA METODO DE PODA-------------------------")
    mutadosSt = []
    mutadosNd = []
    for index in arreglo:
        mutadosSt.append((index, (random.randint(1, 100) / 100)))
    # calculamos probabilidad de poda
    probabilidadPoda = int(interfaz.txtPm.text()) / len(mutadosSt)
    if len(mutadosSt) > int(interfaz.txtPm.text()):
        for k in mutadosSt:
            if k[1] <= probabilidadPoda:
                mutadosNd.append(k)
    else:
        for k in mutadosSt:
            mutadosNd.append(k)
    print("fin De poda----------------------------------")
    conversionXY(mutadosNd, inicio)


# arreglos para guardar valores calculados de X & Y
valores_deX = []
valores_deY = []
# metodo auxiliar para rescatar valores a graficar
argpara_X = []
argpara_Y = []
def conversionXY(arregloNd, inicio):
    print("Estamos en conversionXY-----------------------------")
    calcularX(arregloNd, 2)
    calcularY()
    listaXY = list()
    count = 0
    print("arreglo de X:", argpara_X)
    for x in range(len(argpara_X)):
        listaXY.append([x, argpara_Y[count]])
        count += 1
    verificarRadioBtns(listaXY, inicio)


# calculamos valores de X
def calcularX(decimales, tipo):
    argpara_X.clear()
    print("CALCUAR X----------------------------")
    a = int(interfaz.txta.text())
    precision = float(interfaz.txtPrec.text())
    print("ARREGLO DE DECIAMLES:", decimales)
    for itera in decimales:
        if tipo == 1 :
            valor_x = a + (itera * precision)
        else:
            valor_x = a + (itera[0] * precision)
        argpara_X.append(valor_x)
    print("termina calcular x------------------------------")


# calculamos valores de Y en la funcion dada
def calcularY():
    argpara_Y.clear()
    print("CALCULANDO Y-----------------------------------")
    for y in argpara_X:
        valor_y = (1.50 * math.cos(1.50 * y) * math.sin(1.50 * y)) - (0.75 * math.cos(0.75 * y))
        argpara_Y.append(valor_y)

    print("termina calcular y------------------------------------")

#verificamos si se va a calcular minimo o máximo
def verificarRadioBtns(listXY, inicio):
    auxiliar = True
    tipo = 0
    print("valores", listXY)
    if interfaz.rbtnMin.isChecked():
        tipo =1
        listXY.sort(key= lambda xy: xy[1])
        print("Seleccion = calcular minimo")
    elif interfaz.rbtnMax.isChecked():
        tipo =2
        print("Seleccion = calcular máximo")
        listXY.sort(key=lambda xy: xy[1], reverse=True)
    else:
        auxiliar = False
        interfaz.lblError.setText("Seleccione minimo o maximo")
    if len(listXY) > int(interfaz.txtPm.text()):
        cantidadborrar = len(listXY) - int(interfaz.txtPm.text())
        for borrar in range(cantidadborrar):
            listXY.pop()
    print("valores2", listXY)
    if auxiliar == True:
        graficar_xy(listXY, tipo, inicio)


# vamos agraficar los valores de x, y
def graficar_xy(argMax, indicador, generacion):
    print("empieza metodo graficar xy------------------------- ")
    valorx = []
    valory = []
    print("ARREGLO DE MAXIMOS",argMax)
    for i in argMax:
        valorx.append(i[0])
        valory.append(i[1])
    figura2 = pyplot.figure(figsize=(12, 7))
    pyplot.scatter(valorx, valory)
    pyplot.xlim(-1, 11)
    pyplot.ylim(-3,3)
    pyplot.title(f"Gráfica de la generacion#{generacion}")
    if indicador == 1:
        pyplot.savefig(f"graficas_minimo/Generacion#{generacion}.png")
    elif indicador == 2:
        pyplot.savefig(f"graficas_maximo/Generacion#{generacion}.png")
    pyplot.close()


#metodo para el video del comportamiento
def generarVideo(nGeneracion):
    print("Generando video")
    rutaVideo = ""
    rutaImagen = ""
    if interfaz.rbtnMin.isChecked():
        rutaVideo = "video_Minimo/Comportamiento_Minimo.mp4"
        rutaImagen = "graficas_minimo/Generacion#"
    elif interfaz.rbtnMax.isChecked():
        rutaVideo = "video_Maximo/Comportamiento_Maximo.mp4"
        rutaImagen = "graficas_maximo/Generacion#"
    imagenesGeneradas = list()
    for vuelta in range(nGeneracion):
        nombreImg = rutaImagen+(str(vuelta+1))+".png"
        imagenesGeneradas.append(cv2.imread(nombreImg))
    alto, ancho = imagenesGeneradas[-1].shape[:2]
    video = cv2.VideoWriter(rutaVideo, cv2.VideoWriter_fourcc(*"mp4v"), 2, (ancho, alto))
    for itera in imagenesGeneradas:
        video.write(itera)
    video.release()

# mostramos error por datos invalidos
def mostrarErrorLabel(mensaje):
    interfaz.lblError.setText(mensaje)

# damos pantalla de error para el ingreso de datos no validos
def mostrarError():
    interfaz.hide()
    interfazError.show()

# Regresar para ingresar nuevos datos
def regresar():
    interfazError.hide()
    interfaz.show()


# meotodo para salir con boton
def salir():
    app.exit()

# definicion de botones
interfaz.ejecutar.clicked.connect(obtenerDatos)
interfazError.btnRegresar.clicked.connect(regresar)
interfaz.btnSalir.clicked.connect(salir)

# inicio de la app
interfaz.show()
app.exec()