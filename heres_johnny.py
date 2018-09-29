#!/usr/bin/env python3

import os
import itertools
import time
import subprocess
import argparse


class Johnny:

    def __init__(self):
        self.host = ""
        self.ports = ""


    def get_args(self):
        args = argparse.ArgumentParser()
        args.add_argument("host", help="Target to Knock")
        args.add_argument("ports", help="Ports to knock, separated by space. example: \"80 443 445\"")
        parsed = args.parse_args()
        self.host = parsed.host
        self.ports = parsed.ports


    def get_port_list(self):
        p1, p2, p3 = self.ports.split(" ")
        port_list = [p1, p2, p3]
        return port_list


    def knock(self, tuple_of_three_ports):
        p1, p2, p3 = tuple_of_three_ports
        ports = [p1, p2, p3]
        print("\n*************************************************")
        print("Here's Johnny!!")
        print("Port order: " + str(p1) + " " + str(p2) + " " + str(p3))
        time.sleep(1)
        i:int = 0
        while i < 3:
            for p in ports:
                port = str(p)
                command = "\nnmap -T2 -sT -Pn --host-timeout 100 --max-retries 0 -p " + port + " " + self.host
                print("\nExecuting: " + command)
                subprocess.run([command], stdout=subprocess.PIPE, shell=True)
                time.sleep(1)
            time.sleep(1)
            print("\nChecking for open SSH...")
            sshcheck = "nmap -T2 -sT -n " + self.host + " -Pn --open -p 22"
            proc = subprocess.run([sshcheck], stdout=subprocess.PIPE, shell=True)
            out = proc.stdout
            out = out.decode()
            out = str(out)
            if "open" in out:
                print("\n!!! PORT 22 OPEN !!!")
                print(self.host + " now has SSH open")
                exit(0)
            else:
                time.sleep(3)
            i += 1


    def all_combinations(self, port_list):
        '''
        Generate all possible combinations of ports
        '''
        order = itertools.permutations(port_list)
        permutations = [o for o in order]
        return permutations


def main():
    os.system("clear")
    john = Johnny()
    john.get_args()
    port_list = john.get_port_list()
    combos = john.all_combinations(port_list)
    [john.knock(c) for c in combos]


if __name__ == '__main__':
    main()
