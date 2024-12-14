from setuptools import find_packages, setup
from typing import List

def get_requirements(filepath:str)->List[str]:
    """
    This function will return the requiements for this project
    """
    requirements = []
    with open(filepath) as file_object:
        requirements=file_object.readlines()
        requirements=[req.replace('\n',"") for req in requirements]
        
    return requirements

setup(
    name="Major_project",
    version="0.0.1",
    author="Arnav, Pratham,Maitreyee, Prachi ",
    author_email="lahanearnav9@gmail.com,prathampatharkar09@gmail.com,maitreyee08deshmukh@gmail.com, prachisatpute25@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)