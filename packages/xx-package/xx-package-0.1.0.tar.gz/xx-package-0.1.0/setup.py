from setuptools import setup, find_packages
 
with open('README.md', 'r') as fh:
    long_description = fh.read()
 
setup(
    name='xx-package',
    version='0.1.0',
    description='A short description of your package',
    author='xiaoxing',
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License"
    ],
)
