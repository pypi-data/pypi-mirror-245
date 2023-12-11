from setuptools import setup, find_packages

from facelook import __version__

extra_dev = [
    'pytest',
    'pytest-cov',
]

setup(
    name='facelook',
    version=__version__,
    description='face image analysis toolbox',

    url='https://github.com/wkabbani/facelook',
    author='Wassim Kabbani',
    author_email='se.wassim.kabbani@gmail.com',

    packages=find_packages(exclude=['tests', 'tests.*']),

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

    install_requires=[

    ],

    python_requires=">=3.5.5",

    extras_require={
        'dev': extra_dev,
    },

)
