import paramiko
import os
from dotenv import load_dotenv
import math


load_dotenv()


host = os.getenv('HOST')
port = os.getenv('PORT')
username = os.getenv('USERSSH')
password = os.getenv('PASSWORD')


def get_information_from_commands(command_name):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command(command_name)
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    return data


def main():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname=host, username=username, password=password, port=port)
    stdin, stdout, stderr = client.exec_command('apt list --installed | cut -d "/" -f 1')
    data = stdout.read() + stderr.read()
    client.close()
    data = str(data).replace('\\n', '\n').replace('\\t', '\t')[2:-1]
    #print(data)
    if len(data) > 4094:
        for i in range(math.ceil(len(data) / 4094)):
            print(data[i * 4094: (i + 1) * 4094])
            print()


if __name__ == '__main__':
    main()
