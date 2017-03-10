import paramiko
from Loging import Logger
class Server():
    """
    :returns SSHClient

    """
    def __init__(self):
        self.name = self
    def hook(self, local_ip, jump_ip, prov_ip, dest_ip, username):
        try:

            vm=paramiko.SSHClient()
            vm.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            vm.connect(jump_ip,username=username)
            return vm
        except paramiko.ssh_exception.AuthenticationException as e:
            logging =Logger(filename='ErrorLog.log')
            logging.write('Authentication Exception, check jump host ip, provisioner ip, destination ip or app name and username inputs')
            return None







