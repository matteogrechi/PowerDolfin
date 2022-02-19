#Función encargada de calcular el tiempo de desplazamiento adelante

#El nombre de la funcion invocada debe ser "desplaza"


import csv, cmath, math, os
import numpy as np

# Function used to read the CSV file
def readCSV(lineNumber):
    os.chdir("D:\\Sincronizacion_MEGA\\Universidad\\US\\ASIGNATURAS\\Proyectos_de_Robotica\\SCRIPTS")
    os.getcwd()
    '''
    with open('path.csv') as File:
        reader = csv.reader(File)
        ruta=list(reader)
    '''
    with open("path.csv") as file_name:
        array = np.loadtxt(file_name, delimiter=",")
        #print(array)
        punto_actual=array[lineNumber]
        punto_siguiente=array[lineNumber+1]
        if lineNumber == 0:
            punto_anterior = -array[lineNumber+1]
        else:
            punto_anterior = array[lineNumber-1]

    return float(punto_siguiente[1]), float(punto_siguiente[0]), float(punto_actual[1]), float(punto_actual[0]), float(punto_anterior[1]), float(punto_anterior[0])

# Internal function used to move forward the drone
def goAheadNoCSV(xN,yN,x,y):
    speed = 2 #estimate pending
    
    dzN = (xN-x) + (yN-y) * 1j
    dtFwd = abs(dzN)/speed

    dtFwd = round(dtFwd)
    return dtFwd*1000 #It only returns the goAhead time (given in miliseconds), if it's 0 there isn't
                      #forward movement
    '''
        if dtFwd > 0:
        return 1, dtFwd
    else:
        return 3, 0
    
    '''
# Function for moving ahead the drone
def desplaza(lineNumber):
    [xN,yN,x,y,xB,yB] = readCSV(lineNumber)
    return goAheadNoCSV(xN,yN,x,y)