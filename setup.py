from setuptools import find_packages,setup
from types import list 
import pandas as pd

def get_requirements()->list[str]:
    """
    this function return list of requirements 
    """
    requirements_list:list[str]=[]
    rq=pd.read_csv(r"E:\ml projects\Sensor fault detection\Sensor-Fault-Detection\requirements.txt",delim_whitespace=True)
    for j in rq:
        requirements_list[j]=rq[j,1]
    return requirements_list

setup(

    name="sensor",
    version="1.0.0",
    author="prikshit singh",
    author_email="prikshitsingh79@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(), 
)

