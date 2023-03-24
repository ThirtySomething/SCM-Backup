"""
******************************************************************************
Copyright 2023 ThirtySomething
******************************************************************************
This file is part of SCM-Backup.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
******************************************************************************
"""


class Repo:
    """Repository representation"""

    def __init__(self: object, name: str, type: str, url: str) -> None:
        """Default constructor

        Args:
            name (str): Name of repository
            type (str): Type of repository, either 'SVN' or 'GIT
            url (str): URL to repository
        """
        self.name: str = name
        self.type: str = type
        self.url: str = url

    def __str__(self: object) -> str:
        """String representation of this kind of object

        Returns:
            str: This object as string
        """
        return "[{}, {}, {}]".format(self.name, self.type, self.url)

    def __repr__(self: object) -> str:
        """Sibling function to __str__

        Returns:
            str: This object as string
        """
        return self.__str__()

    def getName(self: object) -> str:
        """Returns name of repository

        Returns:
            str: Repository name
        """
        return self.name

    def getType(self: object) -> str:
        """Returns type of repository

        Returns:
            str: Repository type
        """
        return self.type.lower()

    def getUrl(self: object) -> str:
        """Returns URL of repository

        Returns:
            str: Repository URL
        """
        return self.url

    def isGit(self: object) -> bool:
        """Check repo for kind git

        Returns:
            str: True for git, otherwise False
        """
        if "git" == self.getType():
            return True
        return False

    def isSVN(self: object) -> None:
        """Check repo for kind SVN

        Returns:
            str: True for SVN, otherwise False
        """
        if "svn" == self.getType():
            return True
        return False
