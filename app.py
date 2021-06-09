import conf
from boltiot import Sms, Bolt
import json, time

threshold = 380

def toFahrenheit(temp):
    fahrenheit = ((temp/10) * 1.8) + 32
    return int(fahrenheit)

mybolt = Bolt(conf.API_KEY, conf.DEVICE_ID)
sms = Sms(conf.SID, conf.AUTH_TOKEN, conf.TO_NUMBER, conf.FROM_NUMBER)

print("Running")

status = mybolt.isOnline()
print(status)

if status[-2]=="1":
    mybolt.digitalWrite("4", "HIGH")
else:
    mybolt.digitalWrite("4", "LOW")
    print("An error has occured. Check the status.")
    exit()

while True:
    try:
        response = mybolt.analogRead("A0")
        data = json.loads(response)
        data = int(data["value"])

        print("Sensor value:", str(toFahrenheit(data))+"°F.")

        if data > threshold:
            sms.send_sms("PLEASE CONTACT THE HOSPITAL AUTHORITIES! The current temperature of the incubator is " + str(toFahrenheit(data))+"°F.")
            mybolt.digitalWrite("1", "HIGH")
            mybolt.digitalWrite("2", "HIGH")

        else:
            mybolt.digitalWrite("1", "LOW")
            mybolt.digitalWrite("2", "LOW")

        time.sleep(5)

    except KeyboardInterrupt:
        mybolt.digitalWrite("4", "LOW")
        print("Interrupted")
        exit()
