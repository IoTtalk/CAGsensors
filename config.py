IoTtalkServerIP = 'IP' #Change to your IoTtalk IP
SerialPort = '/dev/ttyATH0'

cmd = {}
#Please add new sensor command in {cmd}. The key of {cmd} should be the Device Feature Name.
cmd['PM2.5'] = [0x01, 0x03, 0x00, 0x02, 0x00, 0x01, 0x25, 0xCA]
cmd['Temperature'] = [0x01, 0x03, 0x00, 0x04, 0x00, 0x01, 0xC5, 0xCB]
cmd['Humidity'] = [0x01, 0x03, 0x00, 0x03, 0x00, 0x01, 0x74, 0x0A]
