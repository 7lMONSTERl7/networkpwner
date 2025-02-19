from mss import mss
import numpy as np
import requests
import time
import cv2

        
def stream_screen(sct,monitor,server_url,device_name,delay):
    img = np.array(sct.grab(monitor))
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
    try:
        print("sending frame to the server -> ",server_url)
        response = requests.post(f"{server_url}?device_name={device_name}", data=buffer.tobytes())
        if response.status_code != 200:
            print("Failed to send frame:", response.text)
    except requests.exceptions.RequestException as e:
        print("Error sending frame:", e)
    time.sleep(delay)