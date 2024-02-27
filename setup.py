from setuptools import setup, find_packages

setup(
    name='alephium-python-sdk',
    version='1.0.0',
    author='codecoderx',
    author_email='codecoderx@gmail.com',
    description='python sdk for alephium network',
    long_description=open('README.md').read(),
    url='https://github.com/codecoderx/Alephium-python-sdk',
    packages=find_packages(),
    install_requires=[
    ],
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)