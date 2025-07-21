# Protokol:
# Ob prvi povezavi client pošlje 32 bajtov, v katerih napiše svoje
# ime, UTF-8 zakodirano
# Za vsako sporočilo pošlje prvo 4 bajte, ki povedo dolžino sporočila v bajtih,
# nato pa še sporočeno število bajtov.
# Strežnik pošlje naslednje sporočilo vsem: 32 bajtov z imenom, 4 bajte z
# dolžino, sporočilo.
# Vsa števila so big-endian

import socket
import socketserver
import threading


clients = []
clients_lock = threading.Lock()


def get_local_ip():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("1.1.1.1", 80))
        return s.getsockname()[0]


class Handler(socketserver.BaseRequestHandler):
    def decode_name(self, data):
        for i in range(len(data)):
            if data[i] != '\0':
                data = data[i:]
                break

        return data.decode()

    def broadcast(self, message):
        with clients_lock:
            for client in clients:
                client.send(self.name + len(message).to_bytes(4, "big") + message)

    
    def handle(self):
        try:
            introduction = self.decode_name(self.request.recv(32))
        except:
            print(f"Failed connection request: {self.request}")
            return

        self.name = introduction.encode()
        self.name = bytes(32 - len(self.name)) + self.name
        with clients_lock:
            clients.append(self.request)
            print(f"Incoming connection from '{introduction}'")

        try:
            while True:
                length = self.request.recv(4)
                if not length:
                    break

                length = int.from_bytes(length, "big")

                data = self.request.recv(length)
                if not data:
                    break

                self.broadcast(data)

        finally:
            with clients_lock:
                clients.remove(self.request)
                print(f"'{introduction}' disconnected.")
            self.request.close()


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True


if __name__ == "__main__":
    local_ip = get_local_ip()
    port = 8080

    with ThreadedTCPServer((local_ip, port), Handler) as server:
        print(f"Serving on IP {local_ip}, port {port}")
        server.serve_forever()

