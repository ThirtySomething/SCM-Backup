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

from scmbackup.config import Config
from scmbackup.repo import Repo
import os


class BaseCommon:
    """BaseCommon - Common base class"""

    def __init__(self: object, config: Config, repo: Repo) -> None:
        """Default constructor

        Args:
            config (Config): Config object
            repo (Repo): Repo object
            extension (str): Extension used for the specified class
        """
        self.config: Config = config
        self.repo: Repo = repo
        # Get full qualified name of working directory
        self.workingpath: str = os.path.join(os.path.dirname(os.path.dirname(__file__)), self.config.app_dirworking)
        self.myInit()

    def __str__(self: object) -> str:
        """String representation of this kind of object

        Returns:
            str: This object as string
        """
        return "[{}, {}, {}]".format(self.repo, self.extension, self.workingpath)

    def __repr__(self: object) -> str:
        """Sibling function to __str__

        Returns:
            str: This object as string
        """
        return self.__str__()

    def myInit(self: object) -> None:
        """Init method for subclasses when constructor is called"""
        pass
