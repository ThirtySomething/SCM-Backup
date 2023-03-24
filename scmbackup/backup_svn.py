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
import os
import timeit

from scmbackup.backup import Backup


class BackupSVN(Backup):
    """BackupSVN - Create copy from server to filesystem"""

    def buildCommand(self: object, scmusr: str, scmpwd: str, exportFilename: str) -> str:
        """buildCommand - Prepares command for SVN dump

        Args:
            scmusr (str): Username to access SVN
            scmpwd (str): Password to access SVN
            exportFilename (str): Filename to export repository to

        Returns:
            str: Full command for commandline execution
        """
        command: str = 'svnrdump --no-auth-cache --username {} --password "{}" dump {} > {}'.format(scmusr, scmpwd, self.repo.url, exportFilename)
        return command

    def process(self: object, filneame_export: str, scmusr: str, scmpwd: str) -> None:
        """process - Control function for export SVN to filesystem

        Args:
            filneame_export (str): Filename to export repository to
            scmusr (str): Username to access SVN
            scmpwd (str): Password to access SVN
        """
        if os.path.isfile(filneame_export):
            os.remove(filneame_export)
        command = self.buildCommand(scmusr, scmpwd, filneame_export)
        startExport = timeit.default_timer()
        logging.info("Exporting [{}]".format(self.repo.name))
        os.system(command)
        # Memorize stop of process
        stopExport = timeit.default_timer()
        logging.info("Export of [{}] took [{:03.3f}]".format(self.repo.name, (stopExport - startExport)))
