import paramiko
from subprocess import Popen, PIPE
import pytest
import time

server_ip = "192.168.1.153"
password = "0420"
username = "shiwusa1"


@pytest.fixture(scope='function')
def server():
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    stderr_content = None
    ssh.connect(hostname=server_ip, username=username, password=password, look_for_keys=False, allow_agent=False)
    stdin, stdout, stderr = ssh.exec_command('iperf -s &')
    time.sleep(1)  # ensure command is executed
    stderr_content = stderr.read()
    yield ssh, stderr_content
    ssh.close()


@pytest.fixture(scope='function')
def client(server):
    ssh, server_stderr = server
    process = Popen(['iperf', '-c', server_ip, '-i', '1', '-t', '10'], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    return stdout.decode(), stderr.decode(), server_stderr.decode()

