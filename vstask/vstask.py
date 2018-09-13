#!/usr/bin/env python
import json
import os
import subprocess
from .Timer import timed
from . import cli


def get_task_label(task, index):
    if 'label' in task:
        return task['label']
    elif 'group' in task and isinstance(task['group'], str):
        return task['group']
    return 'task{}'.format(index)


def get_tasks():
    old_cwd = os.getcwd()
    try:
        while not os.path.isdir('.vscode'):
            if os.getcwd() == '/':
                raise IOError('.vscode directory not found')
            os.chdir('..')

        with open(os.path.join('.vscode', 'tasks.json')) as f:
            tasks = json.loads(
                '\n'.join(
                    line for line in f.readlines()
                    if not line.strip().startswith('//')
                )
            )['tasks']
    except IOError:
        tasks = []
    root = os.path.abspath(os.getcwd())
    os.chdir(old_cwd)
    return root, {
        get_task_label(task, i): task
        for i, task in enumerate(tasks)
    }


def run_task(task, root='.'):
    options = task.get('options', {})
    cmd = task['command']
    print(cmd)
    cwd = root
    if 'cwd' in options:
        cwd = os.path.join(root, options['cwd'])
    p = subprocess.Popen(
        ['bash', '--login'],
        stdin=subprocess.PIPE,
        cwd=cwd,
        shell=task['type'] == 'shell',
    )
    try:
        p.stdin.write(cmd + '\n')
        p.stdin.write('exit\n')
    except TypeError:
        p.stdin.write((cmd + '\n').encode())
        p.stdin.write('exit\n'.encode())
        p.communicate()
    return p.wait()


def main(args=None):
    opts = cli.parser.parse_args(args)
    root, tasks = get_tasks()

    if opts.completion:
        from .completion import COMPLETION
        print(COMPLETION)
        return 0

    if not tasks and opts.tasks:
        print('Unable to locate .vscode directory or tasks.json')
        return 1

    if opts.list or not opts.tasks:
        for task_name in tasks.keys():
            print(task_name)
        return 0

    with timed(opts.time):
        for task_name in opts.tasks:
            if run_task(tasks[task_name], root) != 0:
                return 1
    return 0
