import os
import re
import subprocess
import sys

from ..debug_logger import DebugLogger as logger


# --------------------
## generates the build_info information
class GenBuildInfo:
    # --------------------
    ## constructor
    def __init__(self):
        ## the file pointer for the build_info file
        self._fp = None
        ## the path to the build_info file
        self._path = None
        ## the overall exit return code
        self._exitrc = 0

    # --------------------
    ## initialize
    #
    # @param path     the path to the build_info file
    # @param verbose  whether to log to stdout or not
    # @return None
    def init(self, path, verbose):
        self._path = path
        logger.verbose = verbose

        self._fp = open(self._path, 'wb')  # pylint: disable=consider-using-with

    # --------------------
    ## terminate
    #
    # @return None
    def term(self):
        if self._fp is not None:
            self._fp.close()

    # --------------------
    ## generate all common info
    #
    # @return error return code
    def gen(self):
        self._gen_init()
        self._gen_git_sha()
        self._gen_git_branch()
        self._gen_uncommitted_changes()
        self._gen_unpushed_commits()
        return self._exitrc

    # --------------------
    ## generate common values
    #
    # @return None
    def _gen_init(self):
        self._writeln('class BuildInfo:  # pylint: disable=too-few-public-methods')

        m = re.search(r'^(\d+\.\d+\.\d+) ', sys.version)
        self._set('python version', 'python_version', m.group(1))
        self._set('OS name', 'os_name', os.name)

        # ensure file is created & flushed here so the import works cleanly
        self._fp.flush()
        from pytest_ver.lib.constants import Constants

        Constants.init()
        self._set('version', 'version', Constants.version)

    # --------------------
    ## set the value in BuildInfo object
    #
    # @param tag    tag for logging
    # @param name   the name of the variable
    # @param val    the value of the variable
    # @return None
    def _set(self, tag, name, val):
        logger.ok(f'{tag: <25}: {val}')
        self._writeln(f'    {name} = \'{val}\'')

    # --------------------
    ## set a list of value in BuildInfo object
    #
    # @param name   the name of the list variable
    # @param items  the values of the list variable
    # @return None
    def _setlist(self, name, items):
        self._writeln(f'    {name} = [')
        for item in items:
            self._writeln(f'        \'{item}\',')
        self._writeln('    ]')

    # --------------------
    ## write a line to the build_info file
    # ensures it is terminated with a linefeed
    #
    # @param line  the line to write
    # @return None
    def _writeln(self, line):
        self._fp.write(bytes(f'{line}\x0A', 'UTF-8'))

    # --------------------
    ## gen the current git SHA for the latest commit
    #
    # @return None
    def _gen_git_sha(self):
        result = subprocess.run('git rev-parse --verify HEAD',
                                stdout=subprocess.PIPE,
                                shell=True,
                                check=False)

        if result.returncode != 0:
            self._exitrc += result.returncode
            logger.err(f'git SHA failed: rc={result.returncode}')
            return

        self._set('git SHA', 'git_sha', result.stdout.decode().strip())

    # --------------------
    ## gen the current branch name
    #
    # @return None
    def _gen_git_branch(self):
        result = subprocess.run('git rev-parse --abbrev-ref HEAD',
                                stdout=subprocess.PIPE,
                                shell=True,
                                check=False)

        if result.returncode != 0:
            self._exitrc += result.returncode
            logger.err(f'git Branch failed: rc={result.returncode}')
            return

        self._set('git branch', 'git_branch', result.stdout.decode().strip())

    # --------------------
    ## show any uncommitted changes
    #
    # @return None
    def _gen_uncommitted_changes(self):
        result = subprocess.run('git status -s',
                                stdout=subprocess.PIPE,
                                shell=True,
                                check=False)

        if result.returncode != 0:
            self._exitrc += result.returncode
            logger.err(f'git uncomitted changeds failed: rc={result.returncode}')
            return

        logger.ok(f'{"git uncommitted": <25}:')
        uncommitted = []
        count = 0
        for line in result.stdout.decode().split('\n'):
            if line != '':
                count += 1
                uncommitted.append(line)
                logger.line(f'    {line}')

        if count == 0:
            line = 'none'
            logger.line(f'    {line}')
        else:
            logger.warn(f'{"git_uncommitted": <25}: has uncommitted changes')
        self._exitrc += count

        self._setlist('git_uncommitted', uncommitted)

    # --------------------
    ## show any unpushed commits
    #
    # @return None
    def _gen_unpushed_commits(self):
        result = subprocess.run('git cherry -v',
                                stdout=subprocess.PIPE,
                                shell=True,
                                check=False)

        if result.returncode != 0:
            self._exitrc += result.returncode
            logger.err(f'git unpushed commits failed: rc={result.returncode}')
            return

        logger.ok(f'{"git unpushed commits": <25}:')
        unpushed = []
        count = 0
        for line in result.stdout.decode().split('\n'):
            if line != '':
                unpushed.append(line)
                logger.line(f'    {line}')
                count += 1

        if count == 0:
            line = 'none'
            logger.line(f'    {line}')
        else:
            logger.warn(f'{"git_unpushed": <25}: has unpushed changes')
        self._exitrc += count

        self._setlist('git_unpushed', unpushed)
