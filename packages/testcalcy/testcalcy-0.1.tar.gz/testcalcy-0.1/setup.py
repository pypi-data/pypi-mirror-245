from setuptools import setup, find_packages

setup(
    name='testcalcy',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'testcalcy = testcalcy.calcy:main',
        ],
    },
    install_requires=[
        # List your dependencies here if you have any
    ],
)
