#Script que se encarga de calcular las filas de un documento CSV obtenido de la planificación
#de una ruta (trayectoria) y que las devuelve como parámetro de salida
import csv
import os

def crear_ordenes():
    xp=[]
    yp=[]

    #os.chdir("D:\\Sincronizacion_MEGA\\Universidad\\US\\ASIGNATURAS\\Proyectos_de_Robotica\\SCRIPTS")
    #os.getcwd()
    with open('path.csv') as File:
        reader = csv.reader(File)
        
        for row in reader:
            # Es mapa[fila,columna]; entonces [y,x]
            #print(row[0])
            y=row[0]
            x=row[1]
            xp.append(x)
            yp.append(y)
        n_puntos=len(xp)
        #print(n_puntos)  
    #return [xp, yp]  
    return n_puntos  

'''if __name__=="__main__":
    n_puntos=crear_ordenes()
    print(n_puntos)
#sol=getXY()
#print(sol)

    '''