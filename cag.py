import serial, time

cmd_pm25 = [0x01, 0x03, 0x00, 0x02, 0x00, 0x01, 0x25, 0xCA]
cmd_temp = [0x01, 0x03, 0x00, 0x04, 0x00, 0x01, 0xC5, 0xCB]
cmd_humd = [0x01, 0x03, 0x00, 0x03, 0x00, 0x01, 0x74, 0x0A]

ser = serial.Serial(
    port='/dev/ttyATH0',
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
    ser.write(cmd)
    ser.flush()
    time.sleep(0.5)
    str = ser.read(7)

    result=[]
    for x in str:
        result.append(x.encode('hex'))

    return (int(result[3]+result[4], 16) * 0.1)


#print (fetch_sensor_value(cmd_pm25))
#print (fetch_sensor_value(cmd_temp))
#print (fetch_sensor_value(cmd_humd))

