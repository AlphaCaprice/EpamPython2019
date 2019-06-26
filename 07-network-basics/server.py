import socket
import time


class ServerException(Exception):
    """ This is server exception """


class Server:
    def __init__(self):
        self.host = socket.gethostbyname(socket.gethostname())
        # print(self.host)
        self.port = 4242
        self.clients = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        self.server_socket.bind((self.host, self.port))
        working = True
        print("[ Server Started ]")

        while working:
            try:
                data, addr = self.server_socket.recvfrom(1024)
                data = data.decode()
                if data == r"\exit":
                    msg_left = f"{self.clients[addr]} left the chat!"
                    self.print_server_msg(msg_left, addr)
                    self.broadcast(msg_left, addr)
                    self.clients.pop(addr)
                    continue

                if addr not in self.clients:
                    self.clients[addr] = data
                    msg = f"{self.clients[addr]} is join to chat"
                    self.print_server_msg(msg, addr)
                    self.broadcast(msg, addr)
                else:
                    self.broadcast(data, addr)
                    self.print_server_msg(data, addr)

            except ServerException:
                print("\n[ Server Stopped ]")
                working = False

        self.server_socket.close()

    def print_server_msg(self, msg: str, addr: tuple):
        time_ = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())
        print(f"[{addr[0]}]=[{addr[1]}]=[{time_}]/", end="")
        print(f"{self.clients[addr]}: {msg}")

    def broadcast(self, msg: str, not_send: tuple):
        msg = f"{self.clients[not_send]} > {msg}".encode()
        for client in self.clients:
            if not_send != client:
                self.server_socket.sendto(msg, client)

if __name__ == "__main__":
    my_server = Server()
    my_server.start()
