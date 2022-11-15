from setuptools import find_packages,setup
from typing import List 

with open('requirements.txt') as f:
    requirements = f.read().splitlines()



setup(

    name="sensor",
    version="1.0.0",
    author="prikshit singh",
    author_email="prikshitsingh79@gmail.com",
    packages=find_packages(),
    install_requires=requirements, 
)

