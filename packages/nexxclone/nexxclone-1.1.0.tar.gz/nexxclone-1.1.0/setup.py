from setuptools import setup, find_packages

setup(
    name='nexxclone',
    version='1.1.0',
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
    long_description="""
    # nexxclone

A Discord Selfbot for Cloning Discord Servers.

## Installation

```bash
pip install nexxclone
```

# Usage

```py
from nexxclone import Clone
import discord
import asyncio

client = discord.Client()

def main():
    token = input('Your Token > ')
    guild_s = input('Your Server ID That You Want To Copy > ')
    guild = input('Your Server ID To Copy The Server In There > ')
    input_guild_id = guild_s
    output_guild_id = guild

    @client.event
    async def on_ready():
        print(f"Logged In as: {client.user}")
        print("Cloning Server")
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))

        anser = input('Do You Want To all in one clone? [y/n] > ')
        if anser.lower() == 'y':
            await Clone.all(guild_from, guild_to)
        else:
            await Clone.roledelete(guild_to)
            await Clone.chdelete(guild_to)
            await Clone.rolecreate(guild_to, guild_from)
            await Clone.catcreate(guild_to, guild_from)
            await Clone.chcreate(guild_to, guild_from)
            await Clone.guedit(guild_to, guild_from)

        answer = input('Do You Want To Clone The Template Of The Server? [y/n] > ')
        if answer.lower() == 'y':
            await Clone.gutemplate(guild_to)
        else:
            pass

        await asyncio.sleep(5)
        exit()

    client.run(token, bot=False)

main()

```

# Contributing
Feel free to contribute by opening issues or creating pull requests. Your feedback and suggestions are welcome!""",
    long_description_content_type='text/markdown',
    license='MIT',
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
    ],
    keywords='discord selfbot clone nexxclone',


)
