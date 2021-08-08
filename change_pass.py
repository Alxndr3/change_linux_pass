#!/usr/bin/env python3


import logging
import paramiko
from time import sleep


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logging.disable(logging.DEBUG)

client = paramiko.client.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

with open('ips.txt', 'r') as ips:
    ips_list = ips.readlines()

with open('user.txt') as user:
    users_passes = user.readlines()


for ip in ips_list:
    for user_pass in users_passes:
        print(user_pass.split())

        if user_pass[0] == 'root':
            print(f"User found: {user_pass[0]}")
            pass
        try:
            client.connect(ip.strip(), port=22, username=user_pass[0],
                    password=user_pass[1])
        except TimeoutError:
            logging.info(f'Time out {ip}')
            exit()
        except ConnectionError:
            logging.info(f'Connection error {ip}')
            exit()
        except paramiko.ssh_exception.NoValidConnectionsError as nvce:
            logging.info(nvce)
            exit()
        except paramiko.AuthenticationException as ae:
            logging.info(f'{ae} for {user_pass[0]}')
            exit()
        except paramiko.ssh_exception as pe:
            logging.info(pe)
            exit()
        except paramiko.ssh_exception.AuthenticationException as ssh_ae:
            logging.info(f'ssh_ae {user_pass[0]}')
            exit()
        else:
            logging.info(f'Conectado {ip} user: {user_pass[0]}')
            for user in users_passes:
                y = user_pass[0].strip()
                print(y)

                command = f'sudo -S passwd {y[0]}'

                stdin, stdout, stderr = client.exec_command(command)
                sleep(0.3)
                stdin.write(y[1]+'\n')
                stdin.write(y[2]+'\n')
                stdin.write(y[2]+'\n')
                stdin.flush()
                logging.info(stdout.readlines())
                logging.info(stderr.readlines())

            del stdin, stdout, stderr
            ssh.close()
            break


