from machine import Pin
from time import sleep
import dht
import time
import network
from machine import Pin
from umqtt.simple import MQTTClient


wifi_ssid = "SHARE-RESIDENTE"
wifi_password = "Share@residente23"

sensor = dht.DHT11(Pin(2)) 

def dht11():
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        return [temp, hum]
    
    except OSError as e:
        print('Failed to read sensor')
        return "Error"

    #print("Temperature: {}°C   Humidity: {:.0f}% ".format(temp, hum))
    #sleep(2)    


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")

mqtt_host = "industrial.api.ubidots.com"
mqtt_username = "BBUS-4WEuAi1Hmj7JdRcPukcaoAB1Uzwo8V"  
mqtt_password = "" 
mqtt_publish_topic = "/v1.6/devices/raspberry/temperature" 


mqtt_client_id = "sarah123"

mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)


mqtt_client.connect()


try:
    while True:
        data_dht11 = dht11()
        temperature = data_dht11[0]
        
        print(f'Publish {temperature:.2f}')
        mqtt_client.publish(mqtt_publish_topic, str(temperature))
        
        time.sleep(3)
except Exception as e:
    print(f'Failed to wait for MQTT messages: {e}')
finally:
    mqtt_client.disconnect()
