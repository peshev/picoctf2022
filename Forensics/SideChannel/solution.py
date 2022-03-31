#!/usr/bin/env python3

import math
import os
import re
import socket
import stat
from subprocess import Popen, PIPE
from time import time

import sys

sys.path.insert(1, '../..')
from utils import download_artifacts

download_artifacts()


def mean(lst):
    return sum(lst) / len(lst)


def stddev(lst):
    m = mean(lst)
    return math.sqrt(sum((i - m) ** 2 for i in lst) / (len(lst) - 1))


def getter(key):
    def _get(item):
        return key(item) if callable(key) else item[key]

    return _get


def find_outliers(lst, calc_key, value_key, deviation=1):
    calc_lst = list(map(getter(calc_key), lst))
    d = stddev(calc_lst)
    m = mean(calc_lst)
    return [
        getter(value_key)(x)
        for x in
        lst
        if getter(calc_key)(x) > m + d * deviation
    ]


def check_pin(pin, pin_checker):
    start = time()
    p = Popen([pin_checker], stdout=PIPE, stdin=PIPE, stderr=PIPE)
    stdout_data = p.communicate(
        input=b"".join(str(i).encode() for i in pin))[0]
    return b"Access granted." in stdout_data, time() - start


def attack_pin(pin_checker, pin_length=8, print_digits=True):
    pin = [0] * pin_length
    for position in range(pin_length):
        result = []
        digit_to_try = None
        for digit_to_try in range(10):
            current_try = list(pin)
            current_try[position] = digit_to_try
            success, exec_time = check_pin(current_try, pin_checker)
            if success:
                if print_digits:
                    print(digit_to_try, flush=True)
                return "".join(map(str, current_try))
            result.append((exec_time, digit_to_try))
        outliers = find_outliers(result, 0, 1)
        assert len(outliers) == 1, (result, outliers, digit_to_try, pin)
        guessed_digit = outliers[0]
        pin[position] = guessed_digit
        if print_digits:
            print(guessed_digit, end="", flush=True)


pin_checker_filename = "./pin_checker"
st = os.stat(pin_checker_filename)
os.chmod(pin_checker_filename, st.st_mode | stat.S_IEXEC)

cracked_pin = attack_pin(pin_checker_filename)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(("saturn.picoctf.net", 50562))
    s.sendall(cracked_pin.encode() + b"\n")
    response = ""
    while True:
        response += s.recv(1024).decode()
        match = re.search("picoCTF{.+?}", response)
        if match:
            print(match.group(0))
            break
