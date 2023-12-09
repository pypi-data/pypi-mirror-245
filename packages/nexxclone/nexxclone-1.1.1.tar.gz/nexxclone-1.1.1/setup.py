from setuptools import setup, find_packages

setup(
    name='nexxclone',
    version='1.1.1',
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

def main():
    # Get user input
    token = input('Your Token > ')
    input_guild_id = input('Your Source Server ID > ')
    output_guild_id = input('Your Destination Server ID > ')

    # Initialize the Discord client
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f"Logged in as: {client.user}")
        print("Cloning Server")

        # Get source and destination guilds
        guild_from = client.get_guild(int(input_guild_id))
        guild_to = client.get_guild(int(output_guild_id))

        # Prompt user for cloning options
        all_in_one = input('Do you want to perform an all-in-one clone? [y/n] > ').lower() == 'y'
        
        if all_in_one:
            await Clone.all(guild_from, guild_to)
        else:
            # Perform individual cloning steps
            await Clone.roledelete(guild_to)
            await Clone.chdelete(guild_to)
            await Clone.rolecreate(guild_to, guild_from)
            await Clone.catcreate(guild_to, guild_from)
            await Clone.chcreate(guild_to, guild_from)
            await Clone.guedit(guild_to, guild_from)


        print("Cloning completed. Exiting in 5 seconds.")


    # Run the bot with the provided token
    client.run(token, bot=False)

if __name__ == "__main__":
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
