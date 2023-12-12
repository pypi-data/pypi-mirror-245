from setuptools import setup, find_packages

setup(
    name='astaria-signing-lib',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'web3',
        # Add other dependencies as needed
    ],
)