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
import re
import timeit

import requests
from requests.auth import HTTPBasicAuth

from scmbackup.basecommon import BaseCommon


class Backup(BaseCommon):
    """Backup - Common base class for backup

    This base class is used for either git or SVN backup

    Args:
        BaseBaPa (_type_): _description_
    """

    def myInit(self: object) -> None:
        # Ensure path for repo exists
        repoPath: str = os.path.join(self.workingpath, self.repo.getName())
        if not os.path.exists(repoPath):
            os.makedirs(repoPath)

    def buildUrlExport(self: object) -> str:
        """Create URL for export

        Returns:
            str: URL for exporting a repo
        """
        exportUrl: str = "{}/{}/{}/export/full".format(self.config.value_get("scm", "url_repos"), self.repo.getNamespace(), self.repo.getName())
        return exportUrl

    def getExportFilename(self: object, dataraw: str) -> str:
        """Extract filename from request header"""
        # Get field with filename from headers
        field: str = dataraw["content-disposition"]
        # Split field with regular expression
        result = re.search(r"(attachment;\s+)(filename\s+=\s+)([a-zA-Z0-9\.\-]+)", field)
        # Filename is in 3rd group, prefix with
        fname: str = os.path.join(self.workingpath, self.repo.getName(), result.group(3))
        # Return filename
        return fname

    def process(self: object) -> None:
        """process - common used method
        Used for each repository to call export URL
        """
        # Memorize startup of process
        start = timeit.default_timer()
        # Get URL for export
        exportUrl: str = self.buildUrlExport()
        logging.debug("exportUrl [{}]".format(exportUrl))
        # Create payload and headers for HTTP-GET
        payload: str = {"namespace": self.repo.getNamespace(), "name": self.repo.getName()}
        headers = {"Content-Type": "text/html"}
        # Call URL
        response = requests.get(
            exportUrl, auth=HTTPBasicAuth(self.config.value_get("scm", "scm_usr"), self.config.value_get("scm", "scm_pwd")), params=payload, headers=headers, stream=True
        )
        # Check result
        if not 200 == response.status_code:
            # Abort when not okay
            logging.error("Response code [{}] when calling URL [{}]".format(response, exportUrl))
            stop = timeit.default_timer()
            logging.error("Process abort after [{:03.3f}] seconds".format(stop - start))
            return
        # Extract filename from response headers
        fname: str = self.getExportFilename(response.headers)
        # Write file
        with open(fname, "wb") as repodata:
            repodata.write(response.content)
        # Stop process and print message
        stop = timeit.default_timer()
        logging.info("Backup process took [{:03.3f}] seconds".format(stop - start))
