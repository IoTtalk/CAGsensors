import serial, time, config

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
    ser.write(cmd)
    ser.flush()
    time.sleep(0.5)
    str = ser.read(7)

    result=[]
    for x in str:
        result.append(x.encode('hex'))
    return (int(result[3]+result[4], 16) * 0.1)




