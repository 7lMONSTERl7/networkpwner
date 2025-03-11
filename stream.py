from mss import mss
import numpy as np
import requests
import time
import cv2

        
def stream_screen(sct,monitor,server_url,device_name,delay):
    img = np.array(sct.grab(monitor))
    _, buffer = cv2.imencode('.jpg', cv2.cvtColor(img, cv2.COLOR_BGRA2BGR))
    response = requests.post(f"{server_url}?device_name={device_name}", data=buffer.tobytes())
    time.sleep(delay)