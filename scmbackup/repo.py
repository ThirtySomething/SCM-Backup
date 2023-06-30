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

import os


class Repo:
    """Repository representation"""

    def __init__(self: object, name: str, namespace: str, type: str) -> None:
        """Default constructor

        Args:
            name (str): Name of repository
            namespace (str): Namespace of repository
            type (str): Type of repository, either 'SVN' or 'GIT
        """
        self.name: str = name
        self.namespace: str = namespace
        self.type: str = type

    def __str__(self: object) -> str:
        """String representation of this kind of object

        Returns:
            str: This object as string
        """
        return "[{}, {}, {}]".format(self.name, self.namespace, self.type)

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

    def getNamespace(self: object) -> str:
        """Returns namespace of repository

        Returns:
            str: Namespace
        """
        return self.namespace

    def getPattern(self: object, wdir: str) -> str:
        nameRaw: str = "{}-{}*.gz".format(self.getNamespace(), self.getName())
        pattern: str = os.path.join(wdir, self.getName(), nameRaw)
        return pattern

    def getType(self: object) -> str:
        """Returns type of repository

        Returns:
            str: Repository type
        """
        return self.type.lower()
