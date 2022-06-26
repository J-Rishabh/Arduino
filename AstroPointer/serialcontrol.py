import serial
import time\


# Some code based on https://forum.arduino.cc/t/serial-input-basics-updated/382007/3
def initialize():
    arduino  = serial.Serial('COM3',9600)       
    print ("You have new message from Arduino")
    print (arduino.readline().decode("utf-8"))     
    print (arduino.readline().decode("utf-8"))     
    #while len(arduino.readline().decode("utf-8")) > 1:
        #print(len(arduino.readline().decode("utf-8")))
        #print (arduino.readline().decode("utf-8"))
    
    return arduino

def returnMotor():
    arduino = initialize()
    arduino.write(b'<E>')                          
    #reachedPos = str(arduino.readline())
    #print (reachedPos)
    time.sleep(1)
    
    print("CLOSING")
    arduino.close()

def moveMotor(alt, az):
    arduino = initialize()
    datastring = "<R, " + str(alt) + ", " + str(az) + ">"
    print(datastring)
    arduino.write(bytes(datastring, encoding='utf8'))                        
    #reachedPos = str(arduino.readline())           
    #print (reachedPos) 
    time.sleep(1)

    print("CLOSING")
    arduino.close()



