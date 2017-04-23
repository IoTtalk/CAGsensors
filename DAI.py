import time, DAN, requests, cag, os

ServerIP = '140.113.199.246' #Change to your IoTtalk IP or None for autoSearching
Reg_addr=None # if None, Reg_addr is MAC address.

DAN.profile['dm_name']='CAGsensors'
DAN.profile['df_list']=['PM2.5','Temperature' ,'Humidity']
DAN.profile['d_name']= None # None for autoNaming
DAN.device_registration_with_retry(ServerIP, Reg_addr)
os.system('echo \"default-on\" > /sys/class/leds/ds:green:usb/trigger')

previous_pm25 = 999
previous_temperature = 999
previous_humidity = 999

while True:
    try:
        pm25 = round(cag.fetch_sensor_value(cag.cmd_pm25), 1)
        temperature = round(cag.fetch_sensor_value(cag.cmd_temp), 1)
        humidity = round(cag.fetch_sensor_value(cag.cmd_humd), 1)

        if (pm25 != previous_pm25):
            os.system('echo \"default-on\" > /sys/class/leds/ds:green:wlan/trigger')
            previous_pm25 = pm25           
            DAN.push ('PM2.5', pm25)
            print ('Push PM2.5: '+str(pm25))
            os.system('echo \"none\" > /sys/class/leds/ds:green:wlan/trigger')

        if (temperature != previous_temperature):
            os.system('echo \"default-on\" > /sys/class/leds/ds:green:wlan/trigger')
            previous_temperature = temperature
            DAN.push ('Temperature', temperature)
            print ('Push Temperature: '+str(temperature))
            os.system('echo \"none\" > /sys/class/leds/ds:green:wlan/trigger')

        if (humidity != previous_humidity):
            os.system('echo \"default-on\" > /sys/class/leds/ds:green:wlan/trigger')
            previous_humidity = humidity
            DAN.push ('Humidity', humidity)
            print ('Push Humidity: '+str(humidity))
            os.system('echo \"none\" > /sys/class/leds/ds:green:wlan/trigger')

    except Exception as e:
        print(e)
        os.system('echo \"none\" > /sys/class/leds/ds:green:usb/trigger')
        DAN.device_registration_with_retry(ServerIP, Reg_addr)
        os.system('echo \"default-on\" > /sys/class/leds/ds:green:usb/trigger')

    time.sleep(2)
