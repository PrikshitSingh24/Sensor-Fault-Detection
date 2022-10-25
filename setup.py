from setuptools import find_packages,setup
from typing import List 

def get_requirements()->List[str]:

    requirement_list:List[str]=[]

    return requirement_list



setup(

    name="sensor",
    version="1.0.0",
    author="prikshit singh",
    author_email="prikshitsingh79@gmail.com",
    packages=find_packages(),
    install_requires=[], 
)

