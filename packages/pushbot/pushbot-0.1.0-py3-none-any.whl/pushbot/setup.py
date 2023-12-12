from setuptools import setup

with open('README.md', 'r') as file:
    long_description = file.read()

setup(
    name='pushbot',
    version='0.1.0',
    description='A Python package to create repo and push code on Github',
    url="https://github.com/sleepingcat4/push-bot",
    author='TAWSIF AHMED',
    author_email="sleeping4cat@outlook.com",
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
)
