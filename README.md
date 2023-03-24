# SCM-Backup

Backup of SCM-Manager repositories

## Motivation

The [SCM-Manager][scm-manager] is a self hosted [git][scm-git], [mercurial][scm-hg] and [subversion][scm-svn] service. Allthough it's open source, the company [Cloudogu][cloudogu] supports the major developer [Sebastian Sdorra][sdorra].

From my point of view one important feature is missing - the possibility of a scheduled backup. In the past I've did this with some [batch][wbatch] files. To have a full remote backup without access to servers file system, you have to use the API of [SCM-Manager][scm-manager]. This is why [Python][python] now is used instead of good old Windows [batch][wbatch].

## 3rd party

- For the cleanup module I use [code][cleanupcode] I borrowed from [Graham Lyons][glyons] - thank you for providing this snippet.
- For the config file I'm using my [MDO][mdo] class.

[cleanupcode]: https://github.com/grahamlyons/delete-old-files/blob/master/delete_files
[cloudogu]: https://cloudogu.com/
[glyons]: https://grahamlyons.com/
[mdo]: https://github.com/ThirtySomething/MDO
[python]: https://www.python.org/
[scm-git]: https://git-scm.com/
[scm-hg]: https://www.mercurial-scm.org/
[scm-manager]: https://scm-manager.org/
[scm-svn]: https://subversion.apache.org/
[sdorra]: https://sdorra.dev/
[wbatch]: https://en.wikipedia.org/wiki/Batch_file
