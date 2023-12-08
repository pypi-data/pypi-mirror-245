from setuptools import setup, find_packages

setup(
    name='logicplum_ai',
    version='1.0.2',  # Update the version number
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas'
    ],
)