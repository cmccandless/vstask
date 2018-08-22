from contextlib import contextmanager
import subprocess


class Timer(object):
    def __init__(self):
        self.is_started = False
        self.p = None

    def __cmd__(self, cmd):
        try:
            self.p.stdin.write(cmd)
        except TypeError:
            self.p.stdin.write(cmd.encode())
        self.p.stdin.flush()

    def start(self):
        self.p = subprocess.Popen(
            ['bash', '--login'],
            stdin=subprocess.PIPE,
            shell=True,
        )
        self.__cmd__('time read\n')

    def stop(self):
        self.__cmd__('\nexit\n')
        self.p.communicate()
        self.p.wait()
        self.p = None


@contextmanager
def timed(time_it=True):
    if time_it:
        timer = Timer()
        timer.start()
    try:
        yield
    finally:
        if time_it:
            timer.stop()