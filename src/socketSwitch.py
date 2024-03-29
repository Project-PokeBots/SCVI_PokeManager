import socket


class SocketConnection():
    def __init__(self) -> None:
        self.ip = None
        self.port = None
        self.sock = None

    def setConnection(self, ip, port):
        self.ip = ip
        self.port = port
    
    def connect(self):
        if self.ip == None or self.port == None:
            return f"No IP or Port set."
            
        if not self.sock:
            try:
                self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.sock.connect((self.ip, int(self.port)))
            except socket.error: 
                return f"Unable to connect to {self.ip}:{self.port}."
        return "Connected."

    def send(self, content):
        if not self.sock:
            self.connect()
        try:
            content += "\r\n"
            self.sock.sendall(content.encode())
        except Exception as e:
            return f"Unable to send commands: {e}"
        return None

    def recv(self, content):
        if not self.sock:
            self.connect()
        try:
            content += "\r\n"
            self.sock.sendall(content.encode())
            return self.sock.recv(689)[:-1].decode("utf-8")
            
        except Exception as e:
            return f"Unable to send commands: {e}"
        return None

    def get_static(self, box, pos):
        if not self.sock:
            self.connect()
        main_heap = self.recv("pointerRelative 0x43A7778 0xA90 0x9B0 0x0")
        return hex(int(main_heap, 16) + ((box - 1) * 30 * int(0x158)) + ((pos - 1) * int(0x158)))
