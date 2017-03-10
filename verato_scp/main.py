import paramiko

from server import Server
import sys
import os

from argparse import ArgumentParser
from scp import SCPClient

import socket
from Loging import Logger
from paramiko.buffered_pipe import BufferedPipe, PipeTimeout

class SCPException(Exception):
    """SCP exception class"""
    pass



def run_file(jumpIp, provisionerIp, appNameOrIp, username, command, time, printout,recursive,filename):
    try:
        newCon = Server()

        myIp = str(socket.gethostbyname(socket.gethostname()))

        vm = newCon.hook(myIp, jumpIp, provisionerIp, appNameOrIp , username)


        if vm is not None:
                    runthis  = str(command)
                    vmtransport = vm.get_transport()
                    dest_addr = (provisionerIp, 22) #edited#


                    local_addr = (myIp, 22)
                    vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)


                    jhost=paramiko.SSHClient()
                    jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                    jhost.connect('appNameOrIp', username=username, sock=vmchannel)



                    ntransport = jhost.get_transport()
                    app1 = (appNameOrIp, 22)
                    prov = (provisionerIp, 22)

                    pro_channel = ntransport.open_channel('direct-tcpip', app1, prov)

                    apphost = paramiko.SSHClient()
                    apphost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    apphost.connect(appNameOrIp, username=username, sock = pro_channel)

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
                        print "time out"
                    except socket.timeout as t:
                        print "T", t



                    sys.stdout = Logger()
                    string  = stdout.read()
                    logging = Logger()
                    logging.write(string)
                    scp.close()
                    jhost.close()
                    vm.close()




        else:
            print "Connection Failed, read ErrorLog.log for more details"

    except (OSError, SCPException, AttributeError, TypeError) as e:

            logging =Logger(filename='ErrorLog.log')
            logging.write(str(e))
            raise




def run(jumpIp, provisionerIp, appNameOrIp, username, command, time, printout,recursive):
    try:
        newCon = Server()

        myIp = str(socket.gethostbyname(socket.gethostname()))

        vm = newCon.hook(myIp, jumpIp, provisionerIp, appNameOrIp , username)


        if vm is not None:
                    runthis  = str(command)
                    vmtransport = vm.get_transport()
                    dest_addr = (provisionerIp, 22) #edited#


                    local_addr = (myIp, 22)
                    vmchannel = vmtransport.open_channel("direct-tcpip", dest_addr, local_addr)


                    jhost=paramiko.SSHClient()
                    jhost.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                    jhost.connect('appNameOrIp', username=username, sock=vmchannel)



                    ntransport = jhost.get_transport()
                    app1 = (appNameOrIp, 22)
                    prov = (provisionerIp, 22)

                    pro_channel = ntransport.open_channel('direct-tcpip', app1, prov)

                    apphost = paramiko.SSHClient()
                    apphost.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    apphost.connect(appNameOrIp, username=username, sock = pro_channel)

                    #scp = SCPClient(apphost.get_transport())
                    #scp.put('command.js', recursive=recursive)
                    try:

                        stdin, stdout, stderr = apphost.exec_command(runthis, timeout=int(time))
                        if printout:
                            print stderr.read(), stdout.read()
                    except PipeTimeout as pt:
                        print pt
                    except socket.error as e:
                        print e
                        print "time out"
                    except socket.timeout as t:
                        print "T", t



                    sys.stdout = Logger()
                    string  = stdout.read()
                    logging = Logger()
                    logging.write(string)
                    #scp.close()
                    jhost.close()
                    vm.close()




        else:
            print "Connection Failed, read ErrorLog.log for more details"

    except (OSError, SCPException, AttributeError, TypeError) as e:

            logging =Logger(filename='ErrorLog.log')
            logging.write(str(e))
            raise




def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

def main(argv):
    parser = ArgumentParser(description='Utility to run commands on cXXXX stacks using paramiko')

    parser.add_argument('-i', '--inputfile', help='Input file with mongo.js commands')
    parser.add_argument('-v', '--verbose', default='False', help='Display more detail')
    parser.add_argument('-o','--outputlog', default= 'outputlog.log')

    parser.add_argument('-r', '--run', help='For mongo use: mongo --port=27018 < inputfilename.js')

    parser.add_argument('-timeout', default='15', help='Set timeout time for the command, default is 15 sec')
    parser.add_argument('-username', help='username, it has to match in all the machines')
    parser.add_argument('-jumpip', help='Jump Host IP')
    parser.add_argument('-provisioner', help='Provisioner IP')
    parser.add_argument('-appNameOrIp', help='AppName or AppIp')
    parser.add_argument('-p', '--printout', default='False', help = 'Print output True/False')
    parser.add_argument('-recursive', default='False', help = 'If you need to scp directory user recursive True, default is False')

    args = parser.parse_args()
    try:

        input = args.inputfile
        output = args.outputlog
        command = args.run
        timeout = int(args.timeout)
        username = str(args.username)
        jump_ip = args.jumpip
        prov_ip = args.provisioner
        app_ip = args.appNameOrIp
        recursive = str_to_bool(args.recursive)
        printout = str_to_bool(args.printout)



        if os.path.exists(input):
            print "File exists, now perform scp to host and run"
            '''
            for root, dirs, filenames in os.walk(input):
                    print "root", root
                    print "dir", dirs
                    print "filename", filenames

                    for f in filenames:
                        filename = os.path.join(root , f)
            '''
            run_file(jump_ip, prov_ip, app_ip, username, command, timeout, printout, recursive,input)
        else:
            print "File does not exist in path", input
        run(jump_ip, prov_ip, app_ip, username, command, timeout, printout, recursive)
    except ValueError as e:
        print "Check input values, for more info pass -v, or --verbose to get more details"
        print e

if __name__== '__main__':
    main(sys.argv)

