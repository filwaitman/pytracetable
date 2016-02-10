from setuptools import setup

VERSION = '0.1'


setup(
    name='pytracetable',
    packages=['pytracetable', ],
    version=VERSION,
    author='Filipe Waitman',
    author_email='filwaitman@gmail.com',
    install_requires=[x.strip() for x in open('requirements.txt').readlines()],
    url='https://github.com/filwaitman/pytracetable',
    download_url='https://github.com/filwaitman/pytracetable/tarball/{}'.format(VERSION),
    test_suite='tests',
    keywords=['tracetable', 'debug'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Operating System :: OS Independent",
    ],
)
