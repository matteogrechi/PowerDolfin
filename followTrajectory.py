import csv, cmath, time, socket

def importCSV():
    with open('path.csv') as File:
        points = []
        reader = csv.reader(File)
        
        for row in reader:
            # The map is done like [row, column] so [y,x]
            y=float(row[0])
            x=float(row[1])
            points.append(complex(x,y))
        nPoints=len(points)  
    return nPoints, points

def turn(pointNew,point,pointOld):
    omegaTurn = 0.5 #rad/s

    dzN = pointNew - point
    dz = point - pointOld
    dTheta = cmath.phase(dzN/dz)
    counterClockwise = (dTheta > 0)
    dtTurn = abs(dTheta)/omegaTurn
    
    dtTurn = 1000*dtTurn #Result processed in miliseconds
    if dtTurn > 0:
        if counterClockwise:
            return ("H", dtTurn)
        else:
            return ("L", dtTurn)
    else:
        return ("E", dtTurn)

def goAhead(pointNew,point):
    speed = 2 # m/s
    
    dzN = pointNew-point
    dtFwd = abs(dzN)/speed

    return ("K", dtFwd*1000) #It only returns the goAhead time (given in miliseconds), if it's 0 there isn't

def sendPacket(connection, command):
    print(command)
    if command != None:
        myBytes = bytes.fromhex(command.replace(":"," "))
        connection.send(myBytes)

# Create actions table
nPoints, points = importCSV()
actions = []
for i in range(nPoints-1):
    if i == 0:
        actions.append( turn(points[i+1],points[i],2*points[i]-points[i+1]) )
    else:
        actions.append( turn(points[i+1],points[i],points[i-1]) )
    
    actions.append( goAhead(points[i+1],points[i]) )

# Send commands
cmdSocketAddress = ["192.168.1.12", 20002]
connection = socket.create_connection(cmdSocketAddress)
actionPl = {
            "H" : {"on" : "fe:0b:c9:ff:be:45:00:00:88:13:00:00:18:fc:00:00:04:b0:ae", "off" : "fe:0b:ec:ff:be:45:00:00:88:13:00:00:00:00:00:00:04:bd:c8"},
            "J" : {"on" : "fe:0b:ba:ff:be:45:db:fe:88:13:00:00:00:00:00:00:04:12:27", "off" : "fe:0b:c8:ff:be:45:2a:fc:88:13:00:00:00:00:00:00:04:17:a6"},
            "K" : {"on" : "fe:0b:1e:ff:be:45:67:00:88:13:00:00:00:00:00:00:04:5a:7a", "off" : "fe:0b:45:ff:be:45:00:00:88:13:00:00:00:00:00:00:04:7d:79"},
            "L" : {"on" : "fe:0b:20:ff:be:45:00:00:88:13:00:00:6f:03:00:00:04:f8:a5", "off" : "fe:0b:22:ff:be:45:00:00:88:13:00:00:00:00:00:00:04:3d:16"}, # ?
            "F" : {"on" : "fe:04:07:ff:be:aa:64:00:00:00:f5:81", "off" : "fe:04:45:ff:be:aa:00:00:00:00:cf:70"}
}
for (action, dt) in actions:
    sendPacket(connection,actionPl.get(action,{}).get("on",None))
    for i in range(int(dt/2000)):
        time.sleep(2)
        sendPacket(connection,actionPl.get(action,{}).get("on",None))
    time.sleep((dt%2000)/2000)
    sendPacket(connection,actionPl.get(action,{}).get("off",None))
connection.close()