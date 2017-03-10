#!/usr/bin/env python

import os
from argparse import ArgumentParser

from verato_scp import output_info
from verato_scp import run
from verato_scp import run_file
from verato_scp import str_to_bool

parser = ArgumentParser(description='Utility to run commands on cXXXX stacks using paramiko')

parser.add_argument('-i', '--inputfile', help='Input file with mongo.js commands')
parser.add_argument('-v', '--verbose', default='False', help='Display more detail')
parser.add_argument('-o', '--outputlog', default='outputlog.log')

parser.add_argument('-r', '--run', help='For mongo use: mongo --port=27018 < inputfilename.js')

parser.add_argument('-timeout', default='15', help='Set timeout time for the command, default is 15 sec')
parser.add_argument('-username', help='username, it has to match in all the machines')

parser.add_argument('-jumpip', help='Jump Host IP')
parser.add_argument('-provisioner', help='Provisioner IP')
parser.add_argument('-appNameOrIp', help='AppName or AppIp')
parser.add_argument('-p', '--printout', default='False', help='Print output True/False')
parser.add_argument('-recursive', default='False',
                    help='If you need to scp directory user recursive True, default is False')

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

    if input:

        try:
            if os.path.exists(input):
                print "File exists, now perform scp to host and run"
                output_info()
                print input

                '''
                for root, dirs, filenames in os.walk(input):
                        print "root", root
                        print "dir", dirs
                        print "filename", filenames

                        for f in filenames:
                            filename = os.path.join(root , f)
                '''
                run_file(jump_ip, prov_ip, app_ip, username, command, timeout, printout, recursive, input)
            else:
                print "File does not exist in path", input
        except:
            print " Use -h flag to get more info"
    else:

        output_info()

        run(jump_ip, prov_ip, app_ip, username, command, timeout, printout, recursive)
except ValueError as e:
    print "Check input values, for more info pass -v, or --verbose to get more details"
    print e
