#!/usr/bin/python3

import argparse
import threading
import subprocess
import sys
import os
import signal
import time
from contextlib import suppress


PROCESS = []


def cli_args():
    parser = argparse.ArgumentParser(description='A Python thread/subprocess launcher to group dependent proces launch')
    parser.add_argument('-c', '--cmd', action='append', required=True, nargs='+', help='Command to run and its arguments as a single string', metavar="\"/usr/bin/nc -l $PORT0\"")
    return parser.parse_args()


def cleanup():
    for remaining_process in PROCESS[::-1]:
        with suppress(Exception):
            os.killpg(os.getpgid(remaining_process.pid), signal.SIGTERM)
        time.sleep(2)
        with suppress(Exception):
            os.killpg(os.getpgid(remaining_process.pid), signal.SIGKILL)

    os._exit(10)

def handle_exit(_, __):
    cleanup()

def exit_callback(cmd_line):

    print('PYTHON_START_WRAPPER: %s exited, killing myself and children' % cmd_line, file=sys.stderr)
    cleanup()

def run_in_separe_process(exit_callback, cmd_line):

    def run_process(exit_callback, cmd_line):
        sub_proc = subprocess.Popen(cmd_line, shell=True, preexec_fn=os.setsid, env=os.environ)
        PROCESS.append(sub_proc)
        print('PYTHON_START_WRAPPER: %s started as %s' % (cmd_line, sub_proc.pid), file=sys.stderr)
        sub_proc.wait()
        exit_callback()
        return

    thread = threading.Thread(target=run_process, args=(lambda: exit_callback(cmd_line), cmd_line))
    thread.start()
    return thread


if __name__ == '__main__':

    signal.signal(signal.SIGINT,  handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    config = cli_args()

    for command in config.cmd:
        run_in_separe_process(exit_callback, command)
