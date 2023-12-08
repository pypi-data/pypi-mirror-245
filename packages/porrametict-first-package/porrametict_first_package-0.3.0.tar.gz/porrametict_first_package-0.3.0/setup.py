# setup.py

from setuptools import setup, find_packages

setup(
    name='porrametict_first_package',
    version='0.3.0',
    description='My first package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Poramet Tangon',
    author_email='porrametict@gmail.com',
    url='https://github.com/porrametict',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'requests',
        # Add other dependencies here
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)
