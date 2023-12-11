import getpass
import os
import platform
import re
import shlex
import signal
import subprocess
import sys

from debug_logger import DebugLogger as log


# -------------------
## runs OS specific commands
# there are four recognized OS:
#  * Ubuntu
#  * Mac
#  * Windows
#  * Pi
class OsSpecific:
    os_name = 'unknown'
    impl = None

    # -------------------
    ## implements the Windows specific commands
    class Win:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## simple OS name
        #
        # @return string indicating OS
        def os_name(self):
            return 'win'

        # -------------------
        ## returns the given command line
        # Windows implementation needs the un-parsed command line
        #
        # @param cmdline the command line to parse
        # @return the given cmdline
        def parse_command_line(self, cmdline):
            return 'cmd /C ' + cmdline

        # -------------------
        ## returns a preexec_fn for Popen calls
        # not used in Windows implementation
        #
        # @return None
        def preexec_fn(self):
            return None

        # -------------------
        ## returns the package manager
        # Windows does not have a package manager
        #
        # @return None
        def package_manager(self):
            return None

        # -------------------
        ## kill the process group with the given process ID
        # Windows does not have a process group. TaskKill will delete a tree of processes
        #
        # @return None
        def kill(self, pid):
            cmd = ['TASKKILL', '/F', '/T', '/PID', str(pid)]
            fhandle = subprocess.PIPE
            proc = subprocess.Popen(cmd,  # pylint: disable=consider-using-with
                                    bufsize=0,
                                    universal_newlines=True,
                                    stdin=None,
                                    stdout=fhandle,
                                    stderr=subprocess.STDOUT)
            log.output('OsSpecific:kill', proc.stdout.readlines())

        # -------------------
        ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        #
        # @param arg  the command line argument to parse
        # @return the parses command line as required for the platform
        def split_args(self, arg):
            re_cmd_lex = r'''"((?:""|\\["\\]|[^"])*)"?()|(\\\\(?=\\*")|\\")|(&&?|\|\|?|\d?>|[<])|([^\s"&|<>]+)|(\s+)|(.)'''

            args = []
            accu = None  # collects pieces of one arg
            for quotes, qss, esc, pipe, word, white, fail in re.findall(re_cmd_lex, arg):
                if word:
                    pass  # most frequent
                elif esc:
                    word = esc[1]
                elif white or pipe:
                    if accu is not None:
                        args.append(accu)
                    if pipe:
                        args.append(pipe)
                    accu = None
                    continue
                elif fail:
                    raise ValueError('invalid or incomplete shell string')
                elif quotes:
                    word = quotes.replace('\\"', '"').replace('\\\\', '\\')
                    word = word.replace('""', '"')
                else:
                    word = qss  # may be even empty; must be last

                accu = (accu or '') + word

            if accu is not None:
                args.append(accu)

            return args

    # -------------------
    ## implements the Mac specific commands
    class Mac:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## simple OS name
        #
        # @return string indicating OS
        def os_name(self):
            return 'macos'

        # -------------------
        ## parses the command line into an array of tokens as required by the shell
        #
        # @param cmdline the command line to parse
        # @return an array of elements from the given cmdline
        def parse_command_line(self, cmdline):
            return shlex.split(cmdline)

        # -------------------
        ## returns a preexec_fn for Popen calls
        #
        # @return the sid required by Popen calls
        def preexec_fn(self):
            return os.setsid

        # -------------------
        ## returns the package manager
        #
        # @return Brew package manager
        def package_manager(self):
            return 'brew'

        # -------------------
        ## kill the process group with the given process ID
        #
        # @return None
        def kill(self, pid):
            os.killpg(os.getpgid(pid), signal.SIGTERM)

        # -------------------
        ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        #
        # @param arg  the command line argument to parse
        # @return the parses command line as required for the platform
        def split_args(self, arg):
            return shlex.split(arg)

    # -------------------
    ## implements the Ubuntu specific commands
    class Ubuntu:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## simple OS name
        #
        # @return string indicating OS
        def os_name(self):
            return 'ubuntu'

        # -------------------
        ## parses the command line into an array of tokens as required by the shell
        #
        # @param cmdline the command line to parse
        # @return an array of elements from the given cmdline
        def parse_command_line(self, cmdline):
            return shlex.split(cmdline)

        # -------------------
        ## returns a preexec_fn for Popen calls
        # not used in Ubuntu implementation
        #
        # @return None
        def preexec_fn(self):
            return None

        # -------------------
        ## returns the package manager
        #
        # @return APT package manager
        def package_manager(self):
            return 'apt'

        # -------------------
        ## kill the process group with the given process ID
        #
        # @return None
        def kill(self, pid):
            os.killpg(os.getpgid(pid), signal.SIGTERM)

        # -------------------
        ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        #
        # @param arg  the command line argument to parse
        # @return the parses command line as required for the platform
        def split_args(self, arg):
            return shlex.split(arg)

    # -------------------
    ## implements the Raspberry Pi specific commands
    class RaspberryPi:
        # -------------------
        ## constructor
        def __init__(self):
            pass

        # -------------------
        ## report current OS
        #
        # @return string indicating OS
        def os_name(self):
            return 'rpi'

        # -------------------
        ## parses the command line into an array of tokens as required by the shell
        #
        # @param cmdline the command line to parse
        # @return an array of elements from the given cmdline
        def parse_command_line(self, cmdline):
            return shlex.split(cmdline)

        # -------------------
        ## returns a preexec_fn for Popen calls
        # not used in Ubuntu implementation
        #
        # @return None
        def preexec_fn(self):
            return None

        # -------------------
        ## returns the package manager
        #
        # @return APT package manager
        def package_manager(self):
            return 'apt'

        # -------------------
        ## kill the process group with the given process ID
        #
        # @return None
        def kill(self, pid):
            os.killpg(os.getpgid(pid), signal.SIGTERM)

        # -------------------
        ## splits a command line argument into a list of multiple arguments, used in CLI argparse
        #
        # @param arg  the command line argument to parse
        # @return the parses command line as required for the platform
        def split_args(self, arg):
            return shlex.split(arg)

    # -------------------
    ## initial
    #
    # selects the current platform and sets impl to it
    @classmethod
    def init(cls):
        ## holds the implementation class
        if os.path.isfile('/sys/firmware/devicetree/base/model'):
            cls.impl = OsSpecific.RaspberryPi()
        elif sys.platform == 'win32':
            cls.impl = OsSpecific.Win()
        elif sys.platform == 'darwin':
            cls.impl = OsSpecific.Mac()
        elif sys.platform == 'linux':
            cls.impl = OsSpecific.Ubuntu()
        else:
            log.bug(f'unrecognized OS: "{sys.platform}"')
            sys.exit(1)

        ## holds the simple OS name: win, ubuntu, macos, 'rpi'
        cls.os_name = cls.impl.os_name()

    # -------------------
    ## get current userid
    #
    # @return userid
    @classmethod
    def userid(cls):
        return getpass.getuser()

    # -------------------
    ## get current hostname
    #
    # @return hostname
    @classmethod
    def hostname(cls):
        return platform.uname().node

    # -------------------
    ## parses a command line to be passed into a process start e.g. Popen
    #
    # @param cmdline  the command line to parse
    # @return the parses command line as required for the platform
    @classmethod
    def parse_command_line(cls, cmdline):
        return cls.impl.parse_command_line(cmdline)

    # -------------------
    ## returns a preexec_fn for Popen calls
    #
    # @return the preexec_fn needed for the platform
    @classmethod
    def preexec_fn(cls):
        return cls.impl.preexec_fn()

    # -------------------
    ## returns the name of the package manager
    #
    # @return the package manager for the platform
    @classmethod
    def package_manager(cls):
        return cls.impl.package_manager()

    # -------------------
    ## kill the process tree/group with the given process ID
    #
    # @return None
    @classmethod
    def kill(cls, pid):
        return cls.impl.kill(pid)

    # -------------------
    ## splits a command line argument into a list of multiple arguments, used in CLI argparse
    #
    # @param arg  the command line argument to parse
    # @return the parses command line as required for the platform
    @classmethod
    def split_args(cls, arg):
        return cls.impl.split_args(arg)
