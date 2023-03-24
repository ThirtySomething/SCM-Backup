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

import requests
from requests.auth import HTTPBasicAuth

from scmbackup.backup_git import BackupGit
from scmbackup.backup_svn import BackupSVN
from scmbackup.cleanup import Cleanup
from scmbackup.config import Config
from scmbackup.packer import Packer
from scmbackup.repo import Repo


class Process:
    """The backup process"""

    extensionGit: str = "bundle"
    extensionPacked: str = "gz"
    extensionSVN: str = "dump"

    def __init__(self: object, config: Config) -> None:
        """Default constructor

        Args:
            config (Config): Common used config object
        """
        self.config = config
        logging.debug("config [{}]".format(self.config))

    def getRepolist(self: object) -> list[str]:
        """Read list of repositories

        Returns:
            list[str]: List of repositories
        """
        # Memorize startup of process
        start = timeit.default_timer()
        # Create dummy list
        repolist: list[str] = []
        # Get payload
        payload: str = self.config.scm_payload
        # Perform request
        response = requests.get(self.config.scm_url_repos, auth=HTTPBasicAuth(self.config.scm_scm_usr, self.config.scm_scm_pwd), params=payload)
        # Check result
        if not 200 == response.status_code:
            logging.error("Got invalid response code [{}] from url call [{}]".format(response.status_code, self.config.scm_url_repos))
            return repolist
        # Read JSON result
        result_json = response.json()
        # Access to repolist
        repolist_raw = result_json["_embedded"]["repositories"]
        # Loop over repositories and create internal object
        for repo_raw in repolist_raw:
            # Get url for checkout
            url_outer = repo_raw["_links"]["protocol"]
            url_inner = url_outer[0]
            url = url_inner["href"]
            # Create internal repo object
            obj = Repo(repo_raw["name"], repo_raw["type"], url)
            # Add repo to list
            repolist.append(obj)
        # Memorize stop of process
        stop = timeit.default_timer()
        logging.info("Reading list of repositories took [{:03.3f}] seconds".format(stop - start))
        return repolist

    def backupRepositories(self: object, repolist: list[str]) -> None:
        """Backup the repositories

        Args:
            repolist (list[str]): List of repositories
        """
        # Memorize startup of process
        start = timeit.default_timer()
        for currentRepo in repolist:
            doBackup: bool = False
            if currentRepo.isGit():
                backupRepo: BackupGit = BackupGit(self.config, currentRepo, Process.extensionGit)
                doBackup = True
            if currentRepo.isSVN():
                backupRepo: BackupSVN = BackupSVN(self.config, currentRepo, Process.extensionSVN)
                doBackup = True
            if not doBackup:
                logging.info("Skip invalid repository [{}]".format(currentRepo))
                continue
            logging.info("Start backup process of svn repo [{}]".format(currentRepo.name))
            # Memorize startup of process
            startBackup = timeit.default_timer()
            cleanup: Cleanup = Cleanup(self.config, currentRepo, Process.extensionPacked)
            packer: Packer = Packer(self.config, currentRepo, Process.extensionPacked)
            # Create filenames
            strFilenameExport: str = os.path.join(backupRepo.workingpath, backupRepo.getFilename())
            strFilenamePacked: str = os.path.join(backupRepo.workingpath, packer.getFilename())
            # Perform backup
            backupRepo.process(strFilenameExport, self.config.scm_scm_usr, self.config.scm_scm_pwd)
            # Pack export
            packer.process(strFilenameExport, strFilenamePacked)
            # Cleanup
            cleanup.process(backupRepo.workingpath)
            # Memorize stop of process
            stopBackup = timeit.default_timer()
            logging.info("End backup process [{}] after [{:03.3f}] seconds".format(currentRepo.name, (stopBackup - startBackup)))
        # Memorize stop of process
        stop = timeit.default_timer()
        logging.info("Process over all repositories took [{:03.3f}] seconds".format(stop - start))

    def process(self: object) -> None:
        """Start backup process"""
        repolist: list[str] = self.getRepolist()
        self.backupRepositories(repolist)
