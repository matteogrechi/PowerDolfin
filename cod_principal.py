#Script que se encarga de calcular los tiempos de movimiento del robot
#Pero sólo para giro, ya que luego se calcula unicamente el desplazamiento

#El nombre de la instancia ejecutada es interpreta_CSV(arg1[linea_ini])

import csv, cmath, math, os
import numpy as np

# Function used to read the CSV file

def readCSV(lineNumber):
    #os.chdir("D:\\Sincronizacion_MEGA\\Universidad\\US\\ASIGNATURAS\\Proyectos_de_Robotica\\SCRIPTS")
    #os.getcwd()
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

# Internal function used to turn the drone
def turnNoCSV(xN,yN,x,y,xB,yB):
    omegaTurn = 0.5 #estimate pending

    dzN = (xN-x) + (yN-y) * 1j
    dz = (x-xB) + (y-yB) * 1j
    dTheta = cmath.phase(dzN/dz)
    counterClockwise = (dTheta > 0)
    dtTurn = abs(dTheta)/omegaTurn
    
    dtTurn = 1000*(round(dtTurn)) #Result processed in miliseconds
    if dtTurn > 0:
        return [1 + int(not(counterClockwise)), dtTurn]
        #If it's a left turning the function returns 1
        #If it's a right turning it returns 2
    else:
        return [3, dtTurn]
        #Else, if there isn't turning, it returns 3
# Function for turning the drone
def interpreta_CSV(lineNumber):
    [xN,yN,x,y,xB,yB] = readCSV(lineNumber)
    return turnNoCSV(xN,yN,x,y,xB,yB)

if __name__=="__main__":
    resultado=interpreta_CSV(1) #only for testing
    print(resultado)