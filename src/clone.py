#! /usr/bin/env python3
"""
imports
"""
import subprocess
import os
import click
from functools import reduce

@click.group()
def cli():
    pass

@click.command('file')
@click.argument('filename')
def clone_repos_from_file(filename):
    """
    clone repos from a specified txt file
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            try:
                content = f.readlines()
                reduce(lambda _, b: clone_it(f'git clone {b}'), 
                        map(lambda repo: repo.decode("utf-8"), content))
            except Exception as e:
                print(e)


def clone_it(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error is not None:
        return error
    if output:
        return output
    return None


@click.command('user')
@click.argument('username')
def clone_user_repos(username):
    """
    This script clones repos for a specified user
    """
    bash_commands = (
            f"""
            brew install jq;
            mkdir cloned-repos;
            cd cloned-repos && \
                    UserName={username}; curl -s \
                    https://api.github.com/users/$UserName/repos\?per_page\=1000 | \
                    jq -r '.[]|.clone_url' | xargs -L1 git clone
                    """)
    clone_it(bash_commands)


def add_commands():
    """Add command to groups"""
    cli.add_command(clone_repos_from_file)
    cli.add_command(clone_user_repos)


if __name__ == "__main__":
    add_commands()
    cli()
