import requests
from datetime import datetime
from config import *


MY_PASSWORD = password
MY_EMAIL = login
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude

response = requests.get(url="http://api.open-notify.org/iss-now.json")
response.raise_for_status()
data = response.json()

iss_latitude = float(data["iss_position"]["latitude"])
iss_longitude = float(data["iss_position"]["longitude"])


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}

response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
response.raise_for_status()
data = response.json()
sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

time_now = datetime.now().hour

def check_position():
    if MY_LAT <= iss_latitude + 5 and MY_LAT >= iss_latitude - 5:
        if MY_LONG <= iss_longitude and MY_LONG >= iss_longitude:
            return True
    return False

def check_time():
    if time_now > sunset or time_now > sunrise:
        return True
    return False

if check_time():
    print('night')

#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



