from argparse import ArgumentParser, ArgumentTypeError
from os.path import exists
from platform import python_version
from sys import exit
from engine import Engine
from lib.const import modes


def valid_int(n):
    if not n.isdigit():
        raise ArgumentTypeError('mode must be a number')

    n = int(n)

    if n > 3:
        raise ArgumentTypeError('maximum for a mode is 3')

    if n < 0:
        raise ArgumentTypeError('minimum for a mode is 0')

    return n


def args():
    args = ArgumentParser()
    args.add_argument('service', help='service to crack')
    args.add_argument('username', help='email or username')
    args.add_argument('passlist', help='password list')
    args.add_argument('-nc', '--no-color', dest='color', action='store_true', help='disable colors')
    args.add_argument('-m', '--mode', default=2, type=valid_int, help='modes: 0 => 32 bots; 1 => 16 bots; 2 => 8 bots; 3 => 4 bots')
    return args.parse_args()


def main():
    arguments = args()
    service = arguments.service
    mode = arguments.mode
    username = arguments.username
    passlist = arguments.passlist

    if not exists(passlist):
        print('Passlist file not found: {}'.format(passlist))
        exit()

    is_color = True if not arguments.color else False
    Engine(service, username, modes[mode], passlist, is_color).start()


if __name__ == '__main__':
    if int(python_version()[0]) < 3:
        print('[!] Please use Python 3')
        exit()

    main()
