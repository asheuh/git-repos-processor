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

    def perform_computation(self):
        """
        to compute the number of lines of python
        code used in the repository
        (excludes comments, whitespaces, blank lines)
        TODO: Optimize this method to consider complexity
        """

        repository = os.listdir(self.directory)
        ignore_dir = ['.git', '.github', '__pycache__']
        result = []

        if os.path.isdir(self.directory):
            for item in os.listdir(self.directory):
                total = 0
                package_list = []
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
                                    lib_packages = [
                                            line for line in content
                                            if line.startswith((b'import', b'from'))
                                            ]
                                    package_list[:] = lib_packages
                                    total += len(content)
                libraries = self.external_lib_pkg(package_list)
                result.append(self.to_json(total, libraries))
        return result

    def to_json(self, total_lines, libraries):
        data = {
                'number_of_lines': total_lines,
                'libraries': libraries
                }
        return data

    def generate_list(self, lib_list):
        for item in lib_list:
            yield f'{item.decode("utf-8").split()[1]}'

    def external_lib_pkg(self, package_list):
        """
        finds all the libraries/packages used in
        the repository and stores them in a list data
        structure
        """
        generator = self.generate_list(package_list)
        return list(generator)

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



