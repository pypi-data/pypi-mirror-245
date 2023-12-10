from setuptools import setup, find_packages

setup(
    name='http-bruteforce',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'requests',
        'argparse',
        'termcolor',
    ],
    entry_points={
        'console_scripts': [
            'http-bruteforce=http_bruteforce:main',
        ],
    },
)

