from multiprocessing.connection import wait
from crear_ordenes import crear_ordenes 
from cod_principal import interpreta_CSV
import calcula_despl, csv, cmath
import matplotlib.pyplot as plt
import time

def importCSV():
    with open('path.csv') as File:
        points = []
        #yp = []
        reader = csv.reader(File)
        
        for row in reader:
            # Es mapa[fila,columna]; entonces [y,x]
            #print(row[0])
            y=float(row[0])
            x=float(row[1])
            points.append(complex(x,y))
        nPoints=len(points)
        #print(n_puntos)  
    return nPoints, points

def turn(pointNew,point,pointOld):
    omegaTurn = 0.5 #estimate pending

    dzN = pointNew - point
    dz = point - pointOld
    dTheta = cmath.phase(dzN/dz)
    counterClockwise = (dTheta > 0)
    dtTurn = abs(dTheta)/omegaTurn
    
    dtTurn = 1000*dtTurn #Result processed in miliseconds
    if dtTurn > 0:
        return (1 + int(not(counterClockwise)), dtTurn)
        #If it's a left turning the function returns 1
        #If it's a right turning it returns 2
    else:
        return (3, dtTurn)

def goAhead(pointNew,point):
    speed = 2 #estimate pending
    
    dzN = pointNew-point
    dtFwd = abs(dzN)/speed

    return (0, dtFwd*1000) #It only returns the goAhead time (given in miliseconds), if it's 0 there isn't

def sendPacket(str):
    print(str)

# Create actions table
nPoints, points = importCSV()
actions = []
for i in range(nPoints-1):
    if i == 0:
        actions.append( turn(points[i+1],points[i],-points[i+1]) )
    else:
        actions.append( turn(points[i+1],points[i],points[i-1]) )
    
    actions.append( goAhead(points[i+1],points[i]) )

# Send commands
#timer = threading.Timer(1.0,sendPacket)
#timer.start()
for (action, dt) in actions:
    sendPacket(action)
    for i in range(int(dt/2000)):
        time.sleep(2)
        sendPacket(action)
    time.sleep((dt%2000)/2000)
    sendPacket(action)
    
#print(actions)

