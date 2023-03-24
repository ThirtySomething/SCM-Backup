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

import logging

from scmbackup.backup import Backup


class BackupGit(Backup):
    """Backup process of git repositories"""

    def buildCommandClone(self: object) -> str:
        """Create command to clone repository

        Returns:
            str: Command to be executed on OS level
        """
        command: str = "git clone {} {}".format(self.repo.url, self.repo.name)
        return command

    def process(self: object, filneame_export: str, scmusr: str, scmpwd: str) -> None:
        """process - common used method

        Used for each specified client to deal with different kind of repositories.

        Args:
            filneame_export (str): Filename to store backup
            scmusr (str): Username to access git
            scmpwd (str): Password to access git
        """
        command = self.buildCommandClone()
        logging.debug("BackupGit [{}]".format(command))
