from setuptools import setup

setup(
    name='bizhi-framework',
    version='1.0.17',
    author='huangwenbin',
    description='bizhi project base framework',
    packages=['bizhi_framework','bizhi_framework.bizhi_web'],
    install_requires=[
        'seven-framework>=1.1.32'
    ],    
)

