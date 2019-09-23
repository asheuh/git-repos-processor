"""
imports
"""
import os
import re
import time


class RepoStatistics:
    """
    Computes certain statistics only for python code present
    in each github repository
    """
    def __init__(self, directory):
        self.directory = directory

    def repository(self):
        """
        get all the repositories in a directory
        """
        dir_list = []
        if os.path.isdir(self.directory):
            for dirname in os.listdir(self.directory):
                dir_list.append(dirname)
        return dir_list

    def perform_computation(self):
        """
        to compute the number of lines of python
        code used in the repository
        (excludes comments, whitespaces, blank lines)
        TODO: Optimize this method to consider complexity
        """

        repository = self.repository()
        ignore_dir = ['.git', '.github', '__pycache__']
        result = []

        for item in repository:
            total = 0
            repo = f'cloned-repos/{item}'
            if os.path.isdir(repo):
                for dir_name, subdir, files in os.walk(repo):
                    subdir[:] = [d for d in subdir if d not in ignore_dir]
                for filename in files:
                    if filename.endswith('.py'):
                        with open(os.path.join(dir_name, filename), 'rb') as f:
                            content = [
                                    line for line in f.readlines()
                                    if not line.startswith(b'#') 
                                    and not (re.match(b'\r?\n', line))
                                    ]
                            total += len(content)
            result.append(self.to_json(total))
        return result

    def to_json(self, total_lines):
        return {'number_of_lines': total_lines}

    def external_lib_pkg(self):
        """
        finds all the libraries/packages used in
        the repository and stores them in a list data
        structure
        """
        return None

    def nesting_factor(self):
        """
        Computes the nesting factor for the repository
        :this is the average depth of a nested for loop
        throughout the code
        """
        return None


if __name__ == "__main__":
    import pprint
    start = time.time()
    REPO = RepoStatistics("cloned-repos")
    result = REPO.perform_computation()

    pprint.pprint(result)
    elapsed = time.time() - start

    print(f'Time taken: {elapsed} seconds')



