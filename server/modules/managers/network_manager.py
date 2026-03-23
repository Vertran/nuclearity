import modules.instancer as instancer

assert instancer.log is not None
log = instancer.log

import json
import socket
import threading


class NetworkManager:
    def __init__(self, host="localhost", port=9000):
        log.info("Initializing Network Manager")

        self.host = host
        self.port = port
        self.clients = []
        self.running = False

        instancer.managers["network"] = self
        log.info("Network Manager initialized successfully")

    def start(self):
        self.running = True
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        log.info(f"Listening on {self.host}:{self.port}")
        i = 0
        while self.running:
            print(i)
            try:
                conn, addr = self.sock.accept()
                log.info(f"New connection: {addr}")
                self.clients.append(conn)  # type: ignore

                t = threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True)
                t.start()

                self._send(
                    conn,
                    {
                        "type": "init",
                        "state": {
                            "terminals": [{"id": 0, "name": "Terminal A"}, {"id": 1, "name": "Terminal B"}],
                            "reactor": {"power": 100, "temp": 300},
                        },
                        "sender": "SERVER",
                        "message": "I synced you",
                    },
                )

            except Exception as e:
                log.error("Error:", str(e))
                break
            i += 1

    def _handle_client(self, conn, addr):
        buffer = ""
        while True:
            try:
                data = conn.recv(4096).decode("utf-8")
                if not data:
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    msg = json.loads(line)
                    log.info(f"From {addr}: {msg}")
                    self._on_message(conn, msg)
            except Exception as e:
                log.warn(f"Client {addr} disconnected:", str(e))
                break

        self.clients.remove(conn)  # type: ignore
        conn.close()

    def _on_message(self, sender, msg):
        if msg.get("type") == "terminal_input":
            self.broadcast(msg, exclude=sender)

    def broadcast(self, data, exclude=None):
        print(f"Broadcasting message to {len(self.clients)} clients. Message:\n{data}")
        for client in self.clients:  # type: ignore
            if client != exclude:
                self._send(client, data)

    def _send(self, conn, data):
        msg = json.dumps(data) + "\n"
        conn.sendall(msg.encode("utf-8"))
