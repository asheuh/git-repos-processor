"""
imports
"""

class RepoStatistics:
    """
    Computes certain statistics only for python code present
    in each github repository
    """
    def __init__(self, repository):
        self.repository = repository

    @classmethod
    def lines_of_code(cls):
        """
        to compute the number of lines of python
        code used in the repository
        (excludes comments, whitespaces, blank lines)
        """
        return None

    @classmethod
    def external_lib_pkg(cls):
        """
        finds all the libraries/packages used in
        the repository and stores them in a list data
        structure
        """
        return None

    @classmethod
    def nesting_factor(cls):
        """
        Computes the nesting factor for the repository
        :this is the average depth of a nested for loop
        throughout the code
        """
        return None
