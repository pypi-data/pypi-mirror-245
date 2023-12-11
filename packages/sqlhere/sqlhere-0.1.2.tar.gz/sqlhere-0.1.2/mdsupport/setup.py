from setuptools import setup, find_packages

setup(
    name='sqlhere',
    version='0.1.2',
    packages=['mdsupport'],
    install_requires=[
        # List dependencies here
        'csv'
        'json'
        'sqlite3'
        'datetime'  
    ],
)
