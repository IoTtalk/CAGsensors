import time, DAN, requests, cag, os, config

ServerIP = config.IoTtalkServerIP #Change to your IoTtalk IP or None for autoSearching
Reg_addr=None # if None, Reg_addr is MAC address.

DAN.profile['dm_name']='CAGsensors'
DAN.profile['df_list'] = []
DAN.profile['d_name']= 'Indoor311' # None for autoNaming

previous = {}
for feature in config.cmd:
    DAN.profile['df_list'].append(feature)
    previous[feature] = 999

DAN.device_registration_with_retry(ServerIP, Reg_addr)
os.system(r'echo "heartbeat" > /sys/class/leds/ds:green:usb/trigger')   #For ArduinoYun Only, need to install packages. "opkg install kmod-ledtrig-heartbeat"
#os.system(r'echo "default-on" > /sys/class/leds/ds:green:usb/trigger') #For ArduinoYun Only. LED constant ON.
#os.system(r'echo "timer" > /sys/class/leds/ds:green:usb/trigger')      #For ArduinoYun Only. LED Blink.

record = {}
for feature in config.cmd:
    record[feature] = [0]*10

while True:
    try:
        for feature in previous:
            data = cag.fetch_sensor_value(config.cmd[feature])
            if data != None:
                data = round(data, 1)
            else: continue  # CRC check failed.
            
            record[feature].append(data)
            record[feature].pop(0)
            current = round(sum(record[feature])/10.0, 2)
            
            if (current != previous[feature]):
                os.system(r'echo "default-on" > /sys/class/leds/ds:green:wlan/trigger') #For ArduinoYun Only 
                previous[feature] = current
                DAN.push (feature, current)
                print ('Push {}: {}'.format(feature, str(current)))
                os.system(r'echo "none" > /sys/class/leds/ds:green:wlan/trigger')       #For ArduinoYun Only
                
    except Exception as e:
        print('Error: '+ str(e))
        os.system(r'echo "none" > /sys/class/leds/ds:green:usb/trigger')                #For ArduinoYun Only
        DAN.device_registration_with_retry(ServerIP, Reg_addr)
        os.system(r'echo "heartbeat" > /sys/class/leds/ds:green:usb/trigger')           #For ArduinoYun Only

    time.sleep(3)
