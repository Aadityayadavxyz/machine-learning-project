from setuptools import find_packages,setup
from typing import List
hyphen_e_dot = '-e .'
def get_requirements(file_path:str)->List[str]:
      requirements = []
      with open(file_path) as f:
            requirements = f.readlines()
            requirements = [req.replace("\n"," ") for req in requirements]
            if  hyphen_e_dot in requirements:
                  requirements.remove(hyphen_e_dot)
      
      return requirements

setup(name = 'Machine leanring project',
      version='0.0.1',
      author='Aaditya',
      author_email='aadityayadav698@gmail.com',
      packages=find_packages(),
      install_requires = get_requirements('requirements.txt'))
      