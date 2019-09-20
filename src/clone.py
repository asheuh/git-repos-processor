#!/usr/bin/env python3.7
"""
imports
"""
# external modules
import subprocess
import os
import click
import time
import concurrent.futures

from multiprocessing import Pool
from functools import lru_cache
from typing import Generator

# internal modules
from repo_stats import RepoStatistics

@click.group()
def cli():
    pass

def repo_generator(array: list) -> Generator[str, None, None]:
    """
    generator implementation to help clone repo 
    one by one
    """
    for item in array:
        yield f'git clone {item.decode("utf-8")}'


def generate_gclone_links(filename: str) -> list:
    """
    clone repos from a specified txt file
    utilize python generators to create an
    iterator that has list of all repos
    """
    if os.path.exists(filename):
        with open(filename, 'rb') as f:
            try:
                content = f.readlines()
                generator = repo_generator(content) # creating and initializing a python generator
                repos = list(generator)
                repos.pop(0)
                return repos
            except Exception as e:
                print(e)


def process_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    if error is not None:
        return error
    if output:
        return output
    return None


@click.command('file')
@click.argument('filename')
@click.argument('number_of_threads')
@lru_cache(maxsize=128, typed=False)
def run_command(filename, number_of_threads):
    t1 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(int(number_of_threads)) as executor:
        executor.map(process_command, generate_gclone_links(filename))
    t2 = time.perf_counter()

    print(f"Finished cloning in {t2-t1} second(s)")


if __name__ == "__main__":
    cli.add_command(run_command)
    cli()





