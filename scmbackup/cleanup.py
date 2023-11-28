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

import glob
import logging
import os
import timeit
from operator import itemgetter

from scmbackup.basecommon import BaseCommon


class Cleanup(BaseCommon):
    """
    Cleanup older files, based on the article here:
    https://github.com/grahamlyons/delete-old-files/blob/master/delete_files
    """

    def sort_files_by_last_modified(self: object, files):
        """Given a list of files, return them sorted by the last
        modified times."""
        fileData = {}
        for fname in files:
            fileData[fname] = os.stat(fname).st_mtime
        fileData = sorted(fileData.items(), key=itemgetter(1))
        return fileData

    def delete_oldest_files(self: object, sorted_files, keep) -> None:
        """Given a list of files sorted by last modified time and a number to
        keep, delete the oldest ones."""
        delete = len(sorted_files) - keep
        for x in range(0, delete):
            logging.info("Deleting file [{}]".format(sorted_files[x][0]))
            os.remove(sorted_files[x][0])

    def process(self: object) -> None:
        """Cleanup of old backups"""
        # Memorize startup of process
        start = timeit.default_timer()
        logging.info("Cleanup [{}]".format(self.repo.name))
        # Create file pattern and list of affected files
        filePattern: str = self.repo.getPattern(self.workingpath)
        logging.info("filePattern [{}]".format(filePattern))
        file_paths = glob.glob(filePattern)
        # Sort list
        sorted_files = self.sort_files_by_last_modified(file_paths)
        # Delete files
        self.delete_oldest_files(sorted_files, int(self.config.value_get("app", "backuptokeep")))
        # Memorize stop of process
        stop = timeit.default_timer()
        logging.info("Cleanup of repositories [{}] took [{:03.3f}] seconds".format(filePattern, (stop - start)))
