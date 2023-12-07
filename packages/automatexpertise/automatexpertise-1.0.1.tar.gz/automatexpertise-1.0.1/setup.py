# setup.py

from setuptools import setup, find_packages

with open('requirements.txt', encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name='automatexpertise',
    author="sKillseries",
    description="Utilitaire qui permet de d'automatiser l'initialisation d'AutomateXpertise",
    version="1.0.1",
    packages=find_packages(),
    entry_points='''
        [console_scripts]
        automatexpertise=automate.cli:cli
    ''',
    install_requires=requirements
)
