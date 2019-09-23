"""
imports
"""
import os
import time


class RepoStatistics:
    """
    Computes certain statistics only for python code present
    in each github repository
    """
    def __init__(self, repository):
        self.repository = repository

    def lines_of_code(self):
        """
        to compute the number of lines of python
        code used in the repository
        (excludes comments, whitespaces, blank lines)
        TODO: Optimize this method to consider complexity
        """
        ignore_dir = ['.git', '.github']
        total = 0
        if os.path.isdir(self.repository):
            for dir_name, subdir, files in os.walk(self.repository):
                subdir[:] = [d for d in subdir if d not in ignore_dir]
                for filename in files:
                    if filename.endswith('.py'):
                        with open(os.path.join(dir_name, filename), 'rb') as f:
                            content = [
                                    line for line in f.readlines()
                                    if not line.startswith(b'#')
                                    ]
                            total += len(content)
        return total

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
    start = time.time()
    REPO = RepoStatistics("Multitask-and-Transfer-Learning")
    REPO.lines_of_code()
    elapsed = time.time() - start

    print(f'Time taken: {elapsed} seconds')



