from setuptools import setup, find_packages

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name='floraflow',
    author='Gilles de PERETTI',  # Votre nom ou le nom de l'organisation
    author_email='gillesdeperetti@gmail.com',  # Votre email ou celui de l'organisation
    description='FloraFlow - a plant recognition data science project',  # Brève description
    url='https://github.com/gillesdeperetti/AU23_Plantes',
    version='0.1.2',
    packages=find_packages(),
    install_requires=required,
)
