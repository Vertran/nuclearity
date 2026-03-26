from ctypes import memset

import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

import json
import socket
import threading


class NetworkManager:
    @instancer.manager
    def __init__(self, host="localhost", port=9000):

        self.host = host
        self.port = port
        self.sock = None
        self.running = False

        instancer.managers["network"] = self

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.host, self.port))
            self.running = True
            print(f"[CLIENT] Connected to {self.host}:{self.port}")

            # слушаем в отдельном потоке
            t = threading.Thread(target=self._recv_loop, daemon=True)
            t.start()
        except Exception as e:
            log.error('A Network Exception occured:', str(e))

    def _recv_loop(self):
        buffer = ""
        while self.running:
            try:
                data = self.sock.recv(4096).decode("utf-8")  # type: ignore
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    msg = json.loads(line)
                    self._on_message(msg)
            except Exception as e:
                print(f"[CLIENT] Error: {e}")
                break

    def _on_message(self, msg):
        match msg['type']:
            case 'init':
                print('You`re now an initialised client')
            case 'terminal_input':
                message = msg['message']
                sender = msg['sender']
                print(f'{sender}:> {message}')
            case _:
                print("unserialized input.", msg)

    def send(self, data):
        msg = json.dumps(data) + "\n"
        self.sock.sendall(msg.encode("utf-8"))  # type: ignore

    def disconnect(self):
        self.running = False
        self.sock.close()  # type: ignore
