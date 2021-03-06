#!/usr/bin/env python
import socket
import sys

import paramiko
from paramiko.buffered_pipe import PipeTimeout

from logging import Logger
from scp import SCPClient
from server import Server


def output_info():
    print "Check output.log"


def str_to_bool(s):
    if s == 'True':
        return True
    elif s == 'False':
        return False
    else:
        raise ValueError


class SCPException(Exception):
    """SCP exception class"""
    pass


def run(jump_ip, provisioner_ip, app_name_ip, username, command, time, printout):
    try:
        connection = Server()

        my_ip = str(socket.gethostbyname(socket.gethostname()))

        vm = connection.hook(my_ip, jump_ip, provisioner_ip, app_name_ip, username)

        if vm is not None:
            runthis = str(command)
            vmtransport = vm.get_transport()
            dest_addr = (provisioner_ip, 22)  # edited#
            local_addr = (my_ip, 22)
            vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
            jhost = paramiko.SSHClient()
            jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            jhost.connect('appNameOrIp', username=username, sock=vmchannel)
            ntransport = jhost.get_transport()
            app1 = (app_name_ip, 22)
            prov = (provisioner_ip, 22)
            pro_channel = ntransport.open_channel('direct-tcpip', app1, prov)
            apphost = paramiko.SSHClient()
            apphost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            apphost.connect(app_name_ip, username=username, sock=pro_channel)
            try:

                stdin, stdout, stderr = apphost.exec_command(runthis, timeout=int(time))
                if printout:
                    print stderr.read(), stdout.read()
            except PipeTimeout as pt:
                print pt
            except socket.error as e:
                print e

            sys.stdout = Logger()
            string = stdout.read()
            logging = Logger()
            logging.write(string)
            jhost.close()
            vm.close()

            return True


        else:
            print "Connection Failed, read ErrorLog.log for more details"
            return False

    except (OSError, SCPException, AttributeError, TypeError) as e:

        logging = Logger(filename='ErrorLog.log')
        logging.write(str(e))
        raise


def run_file(jump_ip, provisioner_ip, app_name_ip, username, command, time, printout, recursive, filename):
    try:
        connection = Server()

        my_ip = str(socket.gethostbyname(socket.gethostname()))

        vm = connection.hook(my_ip, jump_ip, provisioner_ip, app_name_ip, username)

        if vm is not None:
            runthis = str(command)
            vmtransport = vm.get_transport()
            dest_addr = (provisioner_ip, 22)  # edited#
            local_addr = (my_ip, 22)
            vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)
            jhost = paramiko.SSHClient()
            jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            jhost.connect('appNameOrIp', username=username, sock=vmchannel)
            ntransport = jhost.get_transport()
            app1 = (app_name_ip, 22)
            prov = (provisioner_ip, 22)
            pro_channel = ntransport.open_channel('direct-tcpip', app1, prov)
            apphost = paramiko.SSHClient()
            apphost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            apphost.connect(app_name_ip, username=username, sock=pro_channel)
            scp = SCPClient(apphost.get_transport())
            scp.put(filename, recursive=recursive)
            try:

                stdin, stdout, stderr = apphost.exec_command(runthis, timeout=int(time))
                if printout:
                    print stderr.read(), stdout.read()
            except PipeTimeout as pt:
                print pt
            except socket.error as e:
                print e

            sys.stdout = Logger()
            string = stdout.read()
            logging = Logger()
            logging.write(string)
            scp.close()
            jhost.close()
            vm.close()

        else:
            print "Connection Failed, read ErrorLog.log for more details"

    except (OSError, SCPException, AttributeError, TypeError) as e:

        logging = Logger(filename='ErrorLog.log')
        logging.write(str(e))
        raise
