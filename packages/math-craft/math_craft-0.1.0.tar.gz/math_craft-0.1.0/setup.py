from setuptools import setup, find_packages

setup(
    name='math_craft',
    version='0.1.0',
    description='A MatLab like Python package for academics, students, and enthusiasts',
    author='Marcelo Eduardo Benencase',
    author_email='marcelo.benencase@gmail.com',
    url='https://github.com/mbenencase/mathcraft',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'numpy',
        'scipy',
        'beartype',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    entry_points={
        'console_scripts': [
            'mathcraft-script = mathcraft.module1:main',
        ],
    },
)
