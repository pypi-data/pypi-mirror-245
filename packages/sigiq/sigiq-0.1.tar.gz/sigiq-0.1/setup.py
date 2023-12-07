from setuptools import setup, find_packages

setup(
    name='sigiq',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'sigiq-login = sigiq.login:login_main',
        ],
    },
    install_requires=[
        'requests',
    ],
)
