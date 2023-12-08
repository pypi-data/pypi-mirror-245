from setuptools import setup, find_packages

setup(
    name='nexxclone',
    version='1',
    py_modules=['nexxclone'],  # Include your module directly
    install_requires=[
        'discord.py==1.7.3',
        'requests',
        'colorama',
        'psutil',
        'pyperclip'
    ],
    
    entry_points={
        'console_scripts': [
            'nexxclone=nexxclone:main',  # Update the entry point to match your module name
        ],
    },
    author='nexxrar',
    author_email='tech@moxx.tech',
    url='https://github.com/noritem/nexx_clone',
    description='A Discord Selfbot for Clone Discord Server',
)
