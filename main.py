import math
import random
import re
from matplotlib import pyplot
from PyQt5 import QtWidgets, uic

# desplegamos
app = QtWidgets.QApplication([])

# Cargamos ventanas
interfaz = uic.loadUi("principal.ui")
interfazError = uic.loadUi("vistas/error.ui")

# lista para guardar los individuos generados y cruzados
individuos_Generados = []
arregloSeleccion = []
argAleatorios = []
individuos_Cruza = []
individous_Resultantes_deCruza = []
argMutados1 = []
argMutados2 = []


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
        individuos_Generados = []
        arregloSeleccion = []
        argAleatorios = []
        individuos_Cruza = []
        individous_Resultantes_deCruza = []
        argMutados1 = []
        argMutados2 = []
        individuos_pDescendencia = []
        valores_deX = []
        valores_deY = []
        argpara_X = []
        argpara_Y = []
        arreglo_valoresMaximo = []
        arreglo_valoresMinimo = []



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
    realizarSeleccion(potencia, inicio)
    print("----------------------------------------------")


# metodo para seleccionar individuos
def realizarSeleccion(potencia, inicio):
    for i in range(int(interfaz.txtPo.text())):
        binario = ""
        for j in range(potencia):
            aleatorio = random.randint(0, 1)
            binario += str(aleatorio)
        arregloSeleccion.append(binario)
    aleatorio = 0
    for k in arregloSeleccion:
        if aleatorio <= 4:
            argAleatorios.append(arregloSeleccion[aleatorio])
        else:
            break
        aleatorio += 1
    for vuelta in argAleatorios:
        argMutados1.append(vuelta)
    calcularCruza(potencia - 1, inicio)


# Metodo para hacer la cruza de la poblacion, la probabilidad de desc y calcular el bit en el que serán cortados
def calcularCruza(bits, inicio):
    n1 = 0
    n2 = 1
    while n1 < len(individuos_Generados):
        auxBinario1 = individuos_Generados[n1]
        while n2 < len(individuos_Generados):
            auxBinario2 = individuos_Generados[n2]
            individuos_Cruza.append(
                (auxBinario1, auxBinario2, round(random.uniform(0, 1), 3), random.randint(1, bits)))
            n2 += 1
        n1 += 1
        n2 = n1 + 1
    argMutados2 = individuos_Cruza
    validarPromedioDescendencia()
    realizarMutacion(inicio)


individuos_pDescendencia = []
def validarPromedioDescendencia():
    print("llega a verificar primedio de descendencia")
    p_Desendencia = (float(interfaz.txtPD.text())) / 100
    for index in individuos_Cruza:
        if index[2] <= p_Desendencia:
            individuos_pDescendencia.append(index)


# metodo para el intercambio de bits en los individuos cruzados
def realizarMutacion(inicio):
    print("llegó a la mutacion")
    for index in individuos_Cruza:
        arregloAux1 = index[0]
        arregloAux2 = index[1]
        cortarArregloAux1 = arregloAux1[0:index[3]]
        cortarArregloAux2 = arregloAux2[0:index[3]]
        res1 = arregloAux1[index[3]:]
        res2 = arregloAux2[index[3]:]
        individous_Resultantes_deCruza.append(((cortarArregloAux1 + res2), (random.randint(1, 100) / 100),
                                               (cortarArregloAux2 + res1), (random.randint(1, 100) / 100)))
    arregloMutados = []
    pm_Individuo = (float(interfaz.txtPMI.text())) / 100
    for i in individous_Resultantes_deCruza:
        if i[1] <= pm_Individuo:
            arregloMutados.append((i[0], i[1]))
        if i[3] <= pm_Individuo:
            arregloMutados.append((i[2], i[3]))
    mutarGen(arregloMutados, inicio)


# metodo para convertir el numero binario a decimal
def convertir_Bin_Dec(bin):
    auxDec = 0
    for index, cadena in enumerate(bin[::-1]):
        auxDec += int(cadena) * 2 ** index
    return auxDec


# dar limpieza y mutación de gen
def mutarGen(mutados, inicio):
    print("-----metodo para hacer la limpieza-----")
    binariosLista = []
    strAuxiliar = ""
    pm_Gen = (float(interfaz.txtPMG.text())) / 100
    for index in mutados:
        arregloBin = index[0]
        for j in arregloBin:
            numAleatorio = (random.randint(0, 100)) / 100
            if numAleatorio <= pm_Gen:
                if j == '0':
                    strAuxiliar += '1'
                elif j == "1":
                    strAuxiliar += '0'
            else:
                strAuxiliar += j
        binariosLista.append(strAuxiliar)
        strAuxiliar = ""
    if len(binariosLista) > 0:
        realizarLimpieza(binariosLista, inicio)


# aqui realizamos la limpieza segun el promedio
def realizarLimpieza(listaBinarios, inicio):
    a = int(interfaz.txta.text())
    b = int(interfaz.txtb.text())
    prec = float(interfaz.txtPrec.text())
    # calculamos numero de soluciones
    solucion = ((b - a) / prec) + 1
    numDecimales = []
    for individuo in listaBinarios:
        if convertir_Bin_Dec(individuo) <= solucion:
            numDecimales.append(convertir_Bin_Dec(individuo))
    calcularPromedio(numDecimales)
    generar_historico(inicio)
    #realizarPoda()

# metodo para generar la grafica que contiene mejor, peor y promedio
def generar_historico(inicio):
    print(inicio)
    if inicio == int(interfaz.txtGen.text()):
        print("si entro a historico")
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
        pyplot.title(f"Gráfico Histórico")
        pyplot.plot(auxuliar, argMejor, label="Mejor")
        pyplot.plot(auxuliar, argPromedio, label="Promedio")
        pyplot.plot(auxuliar, argPeor, label="Peor")
        pyplot.legend()
        pyplot.show()

# para datos para mejor, peor y promedio
def calcularPromedio(decimales):
    calcularX(decimales)
    calcularY()
    arregloAux_Y = argpara_Y
    arregloAux_Y.sort(reverse=True)
    mejor = arregloAux_Y[0]
    peor = arregloAux_Y[len(arregloAux_Y)-1]
    print("peor", peor)
    print("mejor", mejor)
    #for i in decimales:
    #    if i < peor:
    #        peor = i
    #    if i > mejor:
    #        mejor = i
    promedio = (peor + mejor) / 2
    print("individuo promedio calculado", promedio)
    guardar_pmm(mejor, promedio, peor)


# guardamos en un arreglo el mejor, promedio y peor
arg_Historico = []
def guardar_pmm(mejor, promedio, peor):
    arg_Historico.append((mejor, promedio, peor))


def realizarPoda():
    print("llega a poda")
    mutadosSt = []
    mutadosNd = []
    for index in argMutados1:
        mutadosSt.append((index, (random.randint(1, 100) / 100)))
    for j in argMutados2:
        mutadosSt.append((j[0], (random.randint(1, 100) / 100)))
        mutadosSt.append((j[1], (random.randint(1, 100) / 100)))
    # calculamos probabilidad de poda
    probabilidadPoda = int(interfaz.txtPm.text()) / len(mutadosSt)
    for k in mutadosSt:
        if k[1] <= probabilidadPoda:
            mutadosNd.append(k)
    conversionXY(mutadosNd)


# arreglos para guardar valores calculados de X & Y
valores_deX = []
valores_deY = []

# metodo auxiliar para rescatar valores a graficar
argpara_X = []
argpara_Y = []


def conversionXY(arregloNd):
    numDec = []
    for i in arregloNd:
        aux = i[0]
        numDec.append(convertir_Bin_Dec(aux))
    calcularX(numDec)
    calcularY()
    for i in argpara_X:
        valores_deX.append(i)
    for y in argpara_Y:
        valores_deY.append(y)
    verificarRadioBtns()


# calculamos valores de X
def calcularX(decimales):
    argpara_X.clear()
    a = int(interfaz.txta.text())
    precision = float(interfaz.txtPrec.text())
    for itera in decimales:
        valor_x = a + itera * precision
        argpara_X.append(valor_x)


# calculamos valores de Y en la funcion dada
def calcularY():
    argpara_Y.clear()
    for y in argpara_X:
        valor_y = (1.50 * math.cos(1.50 * y) * math.sin(1.50 * y)) - (0.75 * math.cos(0.75 * y))
        argpara_Y.append(valor_y)


def verificarRadioBtns():
    if interfaz.rbtnMin.isChecked():
        print("Seleccion = calcular minimo")
        #calcularMinimo(1)
    elif interfaz.rbtnMax.isChecked():
        print("Seleccion = calcular máximo")
        #calcularMaximo(2)
    else:
        interfaz.lblError.setText("Seleccione minimo o maximo")


# metodo para calcular minimo de la funcion
arreglo_valoresMinimo = []
def calcularMinimo(indicador):
    print("Inicia metodo para minimo")
    contador = 0
    while contador < len(valores_deX):
        arreglo_valoresMinimo.append((valores_deX[contador], valores_deY[contador]))
        contador += 1
    # ordenamos arreglo para valopres del maximo
    arreglo_valoresMinimo.sort(key=lambda valy: valy[1])
    cantidadGen = int(interfaz.txtGen.text())
    for i in range(0, cantidadGen):
        graficar_xy(i, arreglo_valoresMinimo, indicador)


# metodo para realizar el máximo
arreglo_valoresMaximo = []
def calcularMaximo(indicador):
    print("Inicia metodo para maximo")
    contador = 0
    while contador < len(valores_deX):
        arreglo_valoresMaximo.append((valores_deX[contador], valores_deY[contador]))
        contador += 1
    # ordenamos arreglo para valopres del maximo
    arreglo_valoresMaximo.sort(key=lambda valx: valx[1], reverse=True)
    cantidadGen = int(interfaz.txtGen.text())
    for i in range(0, cantidadGen):
        graficar_xy(i, arreglo_valoresMaximo, indicador)


# vamos agraficar los valores de x, y
def graficar_xy(numero, argMax, indicador):
    print("empieza metodo graficar xy ")
    valorx = []
    valory = []
    for i in argMax:
        valorx.append(i[0])
        valory.append(i[1])
    pyplot.scatter(valorx, valory)
    pyplot.xlim(-8, 70)
    pyplot.ylim(-8, 70)
    print("llega antes del nombre")
    if indicador == 1:
        pyplot.title(f"Gráfica generacion#{numero + 1}")
        pyplot.savefig(f"graficas_minimo/Generacion#{numero + 1}.png")
    elif indicador == 2:
        pyplot.title(f"Gráfica de generacion#{numero + 1}")
        pyplot.savefig(f"graficas_maximo/Generacion#{numero + 1}.png")
    pyplot.show()



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