import requests
import datetime as dt
import smtplib
import time

gmail = "tr633064@gmail.com"
gmail_password = "aampvujzzotxxdio"
yahoo = "tr633064@yahoo.com"
MY_LAT = -50
MY_LNG = -80
parameters = {
    "lat": MY_LAT,
    "lng": MY_LNG,
    "formatted": 0
}
script_running = True

while script_running:
    current_hour = dt.datetime.now().hour
    sunset_response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    sunset_response.raise_for_status()

    sunset_hour = int(sunset_response.json()["results"]["sunset"].split("T")[1].split(":")[0])
    sunrise_hour = int(sunset_response.json()["results"]["sunrise"].split("T")[1].split(":")[0])
    iss_response = requests.get("http://api.open-notify.org/iss-now.json")
    iss_response.raise_for_status()

    iss_latitude = float(iss_response.json()["iss_position"]["latitude"])
    iss_longitude = float(iss_response.json()["iss_position"]["longitude"])

    print(f"Sunset: {sunset_hour}, Sunrise: {sunrise_hour}, Now: {current_hour}\nMy Location: {(MY_LAT, MY_LNG)}\n"
          f"ISS Location: {(iss_latitude, iss_longitude)}")

    if iss_latitude - 5 < MY_LAT < iss_latitude + 5 and iss_longitude - 5 < MY_LNG < iss_longitude + 5:
        if current_hour > sunset_hour or current_hour < sunrise_hour:
            with smtplib.SMTP("smtp.gmail.com") as gmail_connection:
                gmail_connection.starttls()
                gmail_connection.login(user=gmail, password=gmail_password)
                gmail_connection.sendmail(from_addr=gmail, to_addrs=yahoo, msg="Subject:Hey Look Up!\n\nThe ISS is "
                                                                               "hovering over your current location. "
                                                                               "Look above to see it in the night sky!")
    time.sleep(60)