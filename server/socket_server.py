import socket
import threading
import time
import uuid


class SocketServer(threading.Thread):
    server_process = None
    running = True
    is_started = False

    def __init__(self, main_controller):
        self.main_controller_instance = main_controller
        super(SocketServer, self).__init__()

    def run(self) -> None:
        while self.running:
            if not self.is_started:
                self.server_process = ServerThread(self.main_controller_instance)
                self.server_process.start()
                self.is_started = True
                self.server_process.main_controller = self.main_controller_instance


class ServerThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""
    server = None
    host = ""
    port = 8001
    main_controller = None

    def __init__(self, main_controller_instance):
        self.main_controller = main_controller_instance
        self.server = ThreadedServer(self.host, self.port, self.main_controller)
        super(ServerThread, self).__init__()
        self._stop_event = threading.Event()

    def run(self) -> None:
        self.main_controller.print_data("starting server at: " + ("0.0.0.0" if len(self.host) == 0 else self.host) + ":" + str(self.port), prefix="net:")
        self.server.listen()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()


class ThreadedServer(object):
    socket_open = None
    main_controller_instance = None
    connected_printed = False
    buffer_size = 1024
    running = True
    clients = None

    def __init__(self, host, port, main_controller_instance):
        self.main_controller_instance = main_controller_instance
        self.host = host
        self.port = port
        self.clients = {}
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.socket_open = True

    def new_client_uuid(self):
        return str(uuid.uuid4())

    def stop(self):
        self.sock.close()
        self.socket_open = False

    def listen(self):
        self.sock.listen(5)
        self.main_controller_instance.print_data("Server listening", prefix="net:")
        while self.socket_open:
            try:
                client, address = self.sock.accept()
                client_uuid = self.new_client_uuid()
                print(client_uuid)
                if client_uuid not in self.clients.keys():
                    self.clients[client_uuid] = {
                        "client": client,
                        "address": str(address[0]),
                        "port": int(address[1])
                    }
                client.settimeout(60)
                threading.Thread(target=self.listen_to_client, args=(client, address)).start()
            except OSError as e:
                if "kein Socket" in str(e):
                    break

    def print_connected(self, address):
        self.main_controller_instance.print_data("client connected: " + str(address[0])+":"+str(address[1]), prefix="net:")
        self.connected_printed = True
        time.sleep(3)
        self.connected_printed = False

    def listen_to_client(self, client, address):
        self.print_connected(address)

        while self.running:
            try:
                data = client.recv(self.buffer_size)
                if data:
                    if data.decode("utf-8") == "Hello World!":
                        for i in range(0,10):
                            client.send(str(i).encode("utf-8"))
                    self.main_controller_instance.print_data(data.decode("utf-8"))
                    client.send(data)
                else:
                    raise socket.error('Client disconnected')
            except ConnectionAbortedError as e:
                self.main_controller_instance.print_data("ConnectionAbortedError", prefix="err:")
                return  False
            except socket.gaierror:
                client.close()
                return False
            except ConnectionResetError as e:
                self.main_controller_instance.print_data("Connection Reset by Client", prefix="err:")
                for c_uuid in self.clients.keys():
                    c_ = self.clients[c_uuid]
                    if c_["address"] == address[0] and c_["port"] == address[1]:
                        del self.clients[c_uuid]
                        break
                return False
            except socket.timeout as e:
                self.main_controller_instance.print_data("Socket Timeout", prefix="err:")
                return False