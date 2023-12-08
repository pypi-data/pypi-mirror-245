from setuptools import setup

setup(
    name='seven-wallpaper',
    version='1.0.0',
    author='huangwenbin',
    description='wallpaper project base framework',
    packages=['seven_wallpaper','seven_wallpaper.bizhi_web'],
    install_requires=[
        'seven-framework>=1.1.32'
    ],    
)

