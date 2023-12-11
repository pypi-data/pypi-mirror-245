import configparser
import glob
import os
import platform
import re
import subprocess
import sys
from dataclasses import dataclass

import common
from debug_logger import DebugLogger as log
from os_specific import OsSpecific


# --------------------
## holds functions to check all installation and environment
# Do not use any non-built in modules
# Do not use out/ directory
class App:
    ## list of tools needed; max 3 nodes of the version string
    # if cmd is None, then a specific function must be used
    valid_versions = {
        'python': {
            'cmd': None,
            'valid': {
                'ubuntu': ['3.8', '3.9', '3.10'],
                'macos': [],
                'win': [],
                'rpi': [],
            },
            'verbose': True,
        },
        'tkinter': {
            'cmd': None,
            'valid': {
                'ubuntu': ['8.6'],
                'macos': [],
                'win': [],
                'rpi': [],
            },
            'verbose': True,
        },
        'doxygen': {
            'cmd': 'doxygen -v',
            'valid': {
                'ubuntu': ['1.8.17', '1.9.1', '1.9,5'],
                'macos': [],
                'win': [],
                'rpi': [],
            },
            'verbose': False,
        },
        'libreoffice': {
            'cmd': 'libreoffice --version',
            'valid': {
                'ubuntu': ['7.6.2'],
                'macos': [],
                'win': [],
                'rpi': [],
            },
            'verbose': False,
        },
        'graphviz': {
            'cmd': 'dot -V',
            'valid': {
                'ubuntu': ['2.43.0'],
                'macos': [],
                'win': [],
                'rpi': [],
            },
            'verbose': False,
        },
    }

    # --------------------
    ## constructor
    def __init__(self):
        OsSpecific.init()

        ## holds additional scripts to check for permissions
        self._scripts = []

    # --------------------
    ## run the check
    #
    # @return None
    def run(self):
        self._check_ostype()
        self._check_python_version()

        if common.cmn_is_module:
            log.start(f'{common.cmn_mod_name} is a module')
        else:
            log.start(f'{common.cmn_mod_name} is not a module')

        if common.cmn_mod_name == 'module-name':
            log.err(f'{common.cmn_mod_name} must be changed to correct name')
        if common.cmn_mod_dir_name == 'module_name':
            log.err(f'{common.cmn_mod_dir_name} must be changed to correct dir name')

        # make sure mod names are correct before create version.json
        self._check_mod_names()
        # initialize and creaet version.json
        common.init()

        # check everything else
        self._check_versions()
        self._check_pypi()
        self._check_tkinter()
        self._check_bash_scripts()
        self._check_common()

    # --------------------
    ## check the OS name and platform are recognized
    #
    # @return None
    def _check_ostype(self):
        log.line(f'os_name : {OsSpecific.os_name}')

        log.line(f'system  : {platform.system()}')
        # Linux: Linux
        # Mac: Darwin
        # Windows: Windows
        # RPI: ??

        log.line(f'platform: {sys.platform}')
        # Linux: linux (lower case)
        # Mac: ??
        # Win MSYS2: msys (need to confirm)
        # Win MING : mingw64
        # WIN WSL  : linux2
        # RPI: ??

    # --------------------
    ## check the python version
    #
    # @return True if a valid version, False otherwise
    def _check_python_version(self):
        log.start('python version:')
        version = sys.version.replace('\n', ' ')
        log.line(f'version : {version}')
        log.line(f'info    : {sys.version_info}')

        version = f'{sys.version_info.major}.{sys.version_info.minor}'
        self._check_tool_version2('python', version, True)

    # --------------------
    ## check all tool versions
    #
    # @return None
    def _check_versions(self):
        msgs = []
        ok = True
        for key, item in self.valid_versions.items():
            if item['cmd'] is None:
                continue
            ok = ok and self._check_tool_version(msgs, key, item)

        if ok:
            log.ok('all tool versions')
        else:
            for msg in msgs:
                log.err(msg)

    # --------------------
    ## check the version for the given tool
    #
    # @param msgs    list of error messages to display
    # @param key     the name of the tool
    # @param item    tool information from valid_versions
    # @return None
    def _check_tool_version(self, msgs, key, item):
        result = subprocess.run(item['cmd'],
                                shell=True,
                                check=False,
                                text=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)

        out = result.stdout.strip()
        ok = True
        if result.returncode != 0:
            ok = False
            msgs.append(f'{key} version failed, rc:{result.returncode}, out:"{out}"')
        else:
            m = re.search(r'(\d+\.\d+\.\d+)', out)
            if m:
                version = m.group(1)
            else:
                version = out
            self._check_tool_version2(key, version, item['verbose'])

        return ok

    # --------------------
    def _check_tool_version2(self, tool_name, act_version, verbose):
        valid = self.valid_versions[tool_name]['valid'][OsSpecific.os_name]
        # version is sometimes a float
        if str(act_version) in valid:
            if verbose:
                log.ok(f'{tool_name} {act_version}')
        else:
            log.err(f'{tool_name} valid versions {valid}, actual: {act_version}')

    # --------------------
    ## check for the existence of $HOME/.pypirc and its content
    #
    # @return None
    def _check_pypi(self):
        home = os.path.expanduser('~')
        path = os.path.join(home, '.pypirc')
        exists = os.path.isfile(path)

        msg = f'{".pypirc exists": <15}: {exists}'
        log.log(exists, msg)

        if exists:
            self._check_pypi_content(path)

    # --------------------
    ## check for the existence of $HOME/.pypirc and its content
    #
    # @return None
    def _check_tkinter(self):
        # >>> import tkinter
        # >>> tkinter.TkVersion
        # 8.6
        import importlib.util
        tkmod = importlib.util.find_spec('tkinter')
        if tkmod is None:
            log.warn('tkinter not installed')
        else:
            import tkinter
            version = tkinter.TkVersion
            self._check_tool_version2('tkinter', version, True)

    # --------------------
    ## check the content of the .pypirc file
    #
    # @param path the path to the file
    # @return None
    def _check_pypi_content(self, path):
        config = configparser.ConfigParser()
        config.read(path)
        msg = ''
        ok = 'pypi' in config.sections()
        if not ok:
            msg += 'missing "pypi" section'
            log.log(ok, msg)
            return

        msgs = []
        # check username
        if 'username' not in config['pypi']:
            msgs.append('missing pypi.username')
            ok = False
        elif config['pypi']['username'] != '__token__':
            msgs.append('pypi.username should be "__token__"')
            ok = False

        # check password
        if 'password' not in config['pypi']:
            msgs.append('missing pypi.password')
            ok = False

        log.log_all(ok, f'{".pypirc content": <15}', msgs)

    # --------------------
    ## check permissions on the executable scripts
    #  * all scripts that start with do_*
    #  * any given in self._scripts
    #
    # @return None
    def _check_bash_scripts(self):
        scripts = glob.glob('do*')
        self._scripts.extend(scripts)
        ok = True
        for path in self._scripts:
            if not os.path.isfile(path):
                continue
            ok = ok and self._check_script(path)
        if ok:
            log.ok('execute permissions')

    # --------------------
    ## checks the permissions for the given script
    #
    # @param path   the script to check
    # @return None
    def _check_script(self, path):
        ok = os.access(path, os.X_OK)
        if not ok:
            msg = f'execute permission missing: {path}'
            log.err(msg)
        return ok

    # --------------------
    ## check values against common.py content
    #
    # @return None
    def _check_common(self):
        self._check_manifest()
        self._check_doxyfile()
        self._check_gitignore()
        self._check_gitconfig()
        self._check_license()

    # --------------------
    ## check module names
    #
    # @return None
    def _check_mod_names(self):
        if not common.cmn_mod_name:
            log.err('cmd_mod_name in tools/common.py not set')
        elif '-' not in common.cmn_mod_name or '_' in common.cmn_mod_name:
            log.err(f'cmd_mod_name should contain "-", not "_": {common.cmn_mod_name}')
        else:
            log.ok(f'{"cmn_mod_name": <18}: {common.cmn_mod_name}')

        if common.cmn_mod_dir_name == '':
            log.err('cmn_mod_dir_name in tools/common.py not set')
        elif '_' not in common.cmn_mod_dir_name or '-' in common.cmn_mod_dir_name:
            log.err(f'cmn_mod_dir_name should contain "_", not "-": {common.cmn_mod_dir_name}')
        else:
            log.ok(f'{"cmn_mod_dir_name": <18}: {common.cmn_mod_dir_name}')

    # --------------------
    ## check manifest.in file
    #
    # @return None
    def _check_manifest(self):
        if not common.cmn_is_module:
            # skip, non-modules don't use manifest
            return

        fname = 'MANIFEST.in'
        with open(fname, 'r', encoding='UTF-8') as fp:
            line1 = fp.readline().strip()

            ok = True
            if line1 != f'graft {common.cmn_mod_dir_name}':
                ok = False
                log.err(f'{fname}: line1 is incorrect: {line1}')

            if ok:
                log.ok(f'{fname}')

    # --------------------
    ## check Doxyfile
    #
    # @return None
    def _check_doxyfile(self):
        tag = 'Doxyfile'
        fname = os.path.join('tools', 'Doxyfile')

        @dataclass
        class state:  # pylint: disable=invalid-name
            found_version = False
            found_name = False
            found_exclude = False
            ok = True

        with open(fname, 'r', encoding='UTF-8') as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                line = line.strip()

                self._doxyfile_project_name(tag, line, state)
                self._doxyfile_project_number(tag, line, state)
                self._doxyfile_excludes(tag, line, state)

        if not state.found_version:
            log.err(f'{tag}: "PROJECT_NUMBER" line not found')
            state.ok = False

        if not state.found_name:
            log.err(f'{tag}: "PROJECT_NAME" line not found')
            state.ok = False

        if not state.found_exclude:
            # even if the module doesn't use build_info, Doxyfile can exclude it
            log.err(f'{tag}: "EXCLUDE" build_info line not found')
            state.ok = False

        if state.ok:
            log.ok(f'{tag}')

    # --------------------
    ## check Doxyfile project name
    # e.g. PROJECT_NAME = "gui-api-tkinter Module" or
    # for apps: PROJECT_NAME = "gui-api-tkinter App"
    #
    # @return None
    def _doxyfile_project_name(self, tag, line, state):
        m = re.search(r'PROJECT_NAME\s*=\s*(".+")$', line)
        if not m:
            return

        # found it
        if common.cmn_is_module:
            exp_name = 'Module'
        else:
            exp_name = 'App'

        state.found_name = True
        if m.group(1) != f'"{common.cmn_mod_name} {exp_name}"':
            log.err(f'{tag}: "PROJECT_NAME" line does not match "{common.cmn_mod_name} {exp_name}", '
                    f'actual: {line}')
            state.ok = False

    # --------------------
    ## check Doxyfile project version
    # e.g PROJECT_NUMBER = 0.0.1
    #
    # @return None
    def _doxyfile_project_number(self, tag, line, state):
        m = re.search(r'PROJECT_NUMBER\s*=\s*(.+)\s*$', line)
        if not m:
            return

        # found it
        state.found_version = True
        if m.group(1) != common.cmn_version:
            log.err(f'{tag}: "PROJECT_NUMBER" version does not match version.json: {common.cmn_version}, '
                    f'actual: {line}')
            state.ok = False

    # --------------------
    ## check Doxyfile excludes
    # e.g. EXCLUDE += ./.../lib/build_info.py or
    # for apps EXCLUDE += ./lib/build_info.py
    #
    # @return None
    def _doxyfile_excludes(self, tag, line, state):
        m = re.search(r'EXCLUDE\s*\+=\s*(.+)/build_info\.py', line)
        if not m:
            return

        if common.cmn_is_module:
            exp_dir = f'./{common.cmn_mod_dir_name}/lib'
        else:
            exp_dir = './lib'

        # found it
        state.found_exclude = True
        if m.group(1) != exp_dir:
            log.err(f'{tag}: "EXCLUDE" build_info line does not match {exp_dir}/build_info.py, '
                    f'actual: {line}')
            state.ok = False

    # --------------------
    ## check .gitignore file
    #
    # @return None
    def _check_gitignore(self):
        tag = '.gitignore'
        fname = os.path.join('.', '.gitignore')

        @dataclass
        class state:  # pylint: disable=invalid-name
            found_buildinfo = False
            found_version_json = False
            ok = True

        with open(fname, 'r', encoding='UTF-8') as fp:
            while True:
                line = fp.readline()
                if not line:
                    break
                line = line.strip()

                self._gitignore_build_info(tag, line, state)
                self._gitignore_version(tag, line, state)

        if not state.found_buildinfo:
            log.err(f'{tag}: build_info line not found')
            state.ok = False

        if not state.found_version_json:
            log.err(f'{tag}: version.json line not found')
            state.ok = False

        if state.ok:
            log.ok(f'{tag}')

    # --------------------
    def _gitignore_build_info(self, tag, line, state):
        if common.cmn_is_module:
            # line: module_name/lib/build_info.py
            exp_dir = f'{common.cmn_mod_dir_name}/lib'
        else:
            # line: /lib/build_info.py
            exp_dir = '/lib'

        m = re.search(r'(.+)/build_info.py$', line)
        if m:
            state.found_buildinfo = True
            if m.group(1) != exp_dir:
                log.err(f'{tag}: build_info line does not match {exp_dir}/build_info.py, '
                        f'actual: {line}')
                state.ok = False

    # --------------------
    def _gitignore_version(self, tag, line, state):
        if common.cmn_is_module:
            # line: module_name/lib/version.json
            exp_dir = f'{common.cmn_mod_dir_name}/lib'
        else:
            # line: /lib/version.json
            exp_dir = '/lib'

        m = re.search(r'(.+)/version.json$', line)
        if m:
            state.found_version_json = True
            if m.group(1) != exp_dir:
                log.err(f'{tag}: version.json line does not match {exp_dir}/version.json, '
                        f'actual: {line}')
                state.ok = False

    # --------------------
    ## check .gitignore file
    #
    # @return None
    def _check_gitconfig(self):
        tag = '.gitconfig'
        path = os.path.join(os.path.expanduser('~'), '.gitconfig')

        ok = True
        if not os.path.isfile(path):
            log.err(f'{tag} cannot find {path}')
            return

        config = configparser.ConfigParser()
        config.read(path)
        ok = ok and self._check_gitconfig_section(tag, config, 'pull', 'rebase', 'false')
        ok = ok and self._check_gitconfig_section(tag, config, 'push', 'autoSetupRemote', 'true')

        if ok:
            log.ok(f'{tag}')

    # --------------------
    ## check a section in the .gitignore file
    #
    # @param tag      the logging tag
    # @param config   reference to the configparser
    # @param section  the section name
    # @param name     the name of the line
    # @param value    the value of the line
    # @return return True if everything is okay in the section, false otherwise
    def _check_gitconfig_section(self, tag, config, section, name, value):
        ok = True
        if section not in config.sections():
            ok = False
            log.err(f'{tag} cannot find "{section}" section')
        elif name not in config[section]:
            ok = False
            log.err(f'{tag} cannot find "{name}" in "{section}" section')
        elif config[section][name] != value:
            ok = False
            log.err(f'{tag} {section}.{name} should be "{value}", actual: {config[section][name]}')
        return ok

    # --------------------
    ## check license file
    #
    # @return None
    def _check_license(self):
        # * check license, for "Copyright line"
        tag = 'LICENSE.txt'
        fname = 'LICENSE.txt'
        path = os.path.join('.', fname)

        if common.cmn_is_module and not os.path.isfile(path):
            log.err(f'{tag} modules must have a LICENSE.txt file')
            return

        if not common.cmn_is_module and not os.path.isfile(path):
            # apps may or may not have a LICENSE.txt file
            return

        with open(path, 'r', encoding='UTF-8') as fp:
            line1 = fp.readline().strip()
            line2 = fp.readline().strip()
            line3 = fp.readline().strip()
            line4 = fp.readline().strip()

            ok = True
            # MIT License
            if line1 != f'{common.cmn_license} License':
                ok = False
                log.err(f'{fname}: line1 invalid license line: "{line1}"')

            if line2:
                ok = False
                log.err(f'{fname}: line2 should be blank: "{line2}"')

            # Copyright (c) since (etc)
            m = re.search(r'^Copyright \(c\) since \d{4}: ', line3)
            if not m:
                ok = False
                log.err(f'{fname}: line3 invalid copyright line: "{line3}"')

            if line4:
                ok = False
                log.err(f'{fname}: line4 should be blank: "{line4}"')

            if ok:
                log.ok(f'{fname}')


# --------------------
def main():
    app = App()
    app.run()


main()
