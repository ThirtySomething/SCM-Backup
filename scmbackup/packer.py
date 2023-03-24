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
from datetime import datetime

from scmbackup.basecommon import BaseCommon


class Packer(BaseCommon):
    """This module will pack a repository export"""

    def buildCommandPack(self: object, filename_export: str, filename_packed: str) -> str:
        """Create pack command

        This method will create a command used on the commandline to pack the
        repository export.

        Args:
            filename_export (str): Filename of repository export
            filename_packed (str): Filename of packed repository export

        Returns:
            str: Full command for commandline execution
        """
        command: str = "gzip -c {} > {}".format(filename_export, filename_packed)
        return command

    def process(self: object, filename_export: str, filename_packed: str) -> None:
        """Packing process

        Args:
            filename_export (str): Filename of repository export
            filename_packed (str): Filename of packed repository export
        """
        if not os.path.isfile(filename_export):
            logging.info("Packing of [{}] skiped, file does not exist".format(self.repo.name))
            return
        # Memorize startup of process
        start = timeit.default_timer()
        if os.path.isfile(filename_packed):
            os.remove(filename_packed)
        command = self.buildCommandPack(filename_export, filename_packed)
        logging.info("Packing [{}]".format(self.repo.name))
        os.system(command)
        os.remove(filename_export)
        # Memorize stop of process
        stop = timeit.default_timer()
        logging.info("Packing of [{}] ends after [{:03.3f}] seconds".format(self.repo.name, (stop - start)))
