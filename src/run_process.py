#!/usr/bin/env python3.7
"""
imports
"""
# external modules
import subprocess
import os
import asyncio
import click
import time
import concurrent.futures

from typing import Generator

# internal modules
from repo_stats import RepoStatistics


def create_git_command(urls: list) -> Generator[str, None, None]:
    """
    For each repository from the list of repo urls
    produce a git clone command and return
    :params: list of urls
    :return: generator
    """
    for url in urls:
        yield f'git clone {url.decode("utf-8")}'


def generate_git_commands(filename: str) -> list:
    """
    read the file specified, then use python generators
    to map through the list of urls and for each url produce
    a git command for it, then convert the generator to list
    :params: filename
    :return: list of git clone commands
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            try:
                lines = f.readlines()
                generator = create_git_command(lines) # creating and initializing a python generator
                git_commands = list(generator)
                git_commands.pop(0)
                return git_commands
            except Exception as e:
                print(e)


def process_command(command):
    """
    process bash commands
    :params: command, bash command
    """
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error is not None:
        return error
    if output:
        return output
    return None

async def run_blocking_tasks(filename, executor):
    loop = asyncio.get_event_loop()
    blocking_tasks = [
            loop.run_in_executor(executor, process_command, command)
            for command in generate_git_commands(filename)
            ]
    completed, pending = await asyncio.wait(blocking_tasks)
    results = [t.result() for t in completed]


@click.command()
@click.argument('threads')
@click.argument('filename')
def start_process(filename: str, threads: int):
    """
    run the process
    """
    with concurrent.futures.ThreadPoolExecutor(int(threads)) as executor:
        event_loop = asyncio.get_event_loop()
        event_loop.run_until_complete(run_blocking_tasks(filename, executor))


@click.group()
def cli(): pass

if __name__ == "__main__":
    cli.add_command(start_process)
    cli()

