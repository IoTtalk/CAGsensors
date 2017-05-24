import serial, time, config, crc16

ser = serial.Serial(
    port=config.SerialPort,
    baudrate=9600,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

if not ser.isOpen(): 
    print ('Serial port failed to initiate.')
    exit()

def fetch_sensor_value(cmd):
    ser.write(str(bytearray(cmd)))
    ser.flush()
    time.sleep(0.5)
    value = ser.read(7)
    
    crcCheck = ord(value[6])*256 + ord(value[5]) 
    #print (crcCheck)
    
    crcCalculation = crc16.calcString(value[:5], 0xFFFF) 
    #print (crcCalculation)
       
    if crcCheck == crcCalculation:
        #print ('CRC check pass.')
        return (ord(value[3])*256 + ord(value[4])) * 0.1
    else: 
        print ('CRC check failed.')
        return None

if __name__ == '__main__':

    print (fetch_sensor_value(config.cmd['PM2.5']))

    '''
    data = str(bytearray(config.cmd['PM2.5']))
    print data[0:6].encode('hex') 
    crc = crc16.calcString( data[0:6], 0xFFFF) 
    print str(hex(crc))
    '''
    
