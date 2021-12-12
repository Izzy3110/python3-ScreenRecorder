import socket
import threading
import time


class SocketServer(threading.Thread):
    server_process = None
    running = True
    is_started = False

    def __init__(self):
        super(SocketServer, self).__init__()

    def run(self) -> None:
        while self.running:
            if not self.is_started:
                self.server_process = ServerThread()
                self.server_process.start()
                self.is_started = True


class ServerThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    server = None
    host = ""
    port = 8001

    def __init__(self):
        self.server = ThreadedServer(self.host, self.port)
        super(ServerThread, self).__init__()
        self._stop_event = threading.Event()

    def run(self) -> None:
        print("starting server at: " + ("0.0.0.0" if len(self.host) == 0 else self.host) + ":" + str(self.port))
        self.server.listen()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ThreadedServer(object):
    socket_open = None

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.socket_open = True

    def stop(self):
        self.sock.close()
        self.socket_open = False

    def listen(self):
        self.sock.listen(5)
        while self.socket_open:
            try:
                client, address = self.sock.accept()
                client.settimeout(60)
                threading.Thread(target=self.listen_to_client, args=(client, address)).start()
            except OSError as e:
                if "kein Socket" in str(e):
                    break

    connected_printed = False

    def print_connected(self, address):
        print("client connected: " + address)
        self.connected_printed = True
        time.sleep(3)
        self.connected_printed = False

    def listen_to_client(self, client, address):
        self.print_connected(address)
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data
                    response = data
                    client.send(response)
                else:
                    raise socket.error('Client disconnected')
            except socket.gaierror:
                client.close()
                return False
