#!/usr/bin/env python
class Logger(object):
    def __init__(self, filename="output.log"):
        #self.terminal = sys.stdout
        self.log = open(filename, "a")

    def write(self, message):
        #self.terminal.write(message)
        self.log.write(message)
