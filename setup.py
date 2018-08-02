from setuptools import setup

setup(
    name='selenium-robot',
    version='0.0.6',
    author='Puke',
    author_email='1129090915@qq.com',
    description='This is a robot description base selenium.',
    long_description=open('README.rst').read(),
    license='Apache',
    url='https://pypi.python.org/pypi',
    packages=['selenium_robot'],
    install_requires=[
        'selenium'
    ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
    ]
)
