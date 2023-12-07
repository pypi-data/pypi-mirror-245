from setuptools import setup, find_packages

setup(
    name='aicloud-lp-new',
    version='0.3.0',  # Update the version number
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas'
    ],
)