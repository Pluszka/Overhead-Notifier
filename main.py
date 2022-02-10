import requests
from datetime import datetime
from config import *
import smtplib
import time

MY_PASSWORD = password
MY_EMAIL = login
MY_LAT = 51.507351 # Your latitude
MY_LONG = -0.127758 # Your longitude


def check_position():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if iss_latitude - 5 >= MY_LAT >= iss_latitude + 5 and iss_longitude - 5 >= MY_LONG >= iss_longitude + 5:
        return True
    return False

def check_time():
    time_now = datetime.now().hour
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

    if time_now > sunset or time_now > sunrise:
        return True
    return False

while True:
    time.sleep(60)
    if check_time() and check_position():
        connection = smtplib.SMTP('smtp.gmail.com')
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL,
                            msg=f'Subject:Check the sky\n\n ISS ist right above you snd it\'s dark enough to see it.')
