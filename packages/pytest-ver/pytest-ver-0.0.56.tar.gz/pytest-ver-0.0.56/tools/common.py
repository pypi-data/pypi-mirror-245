import json
import os
from pathlib import Path

# flag indicating this is a python module (True) or just an app (False)
cmn_is_module = True

# the version string held in cmn_mod_dir_name/lib/version.json
cmn_version = '0.0.56'

# the module name (with dashes)
cmn_mod_name = 'pytest-ver'

# the local directory name for the module (with underscores)
cmn_mod_dir_name = 'pytest_ver'

# the license for the module
cmn_license = 'MIT'

# the license string for the classifier section
cmn_classifier_license = 'License :: OSI Approved :: MIT License'

# the url for the homepage link
cmn_homepage_url = f'https://bitbucket.org/arrizza-public/{cmn_mod_name}/src/master'
# the url for the download link
cmn_download_url = f'https://bitbucket.org/arrizza-public/{cmn_mod_name}/get/master.zip'

# the author name
cmn_author = 'JA'

# the contact email
cmn_email = 'cppgent0@gmail.com'

# the long version of the version string
cmn_long_version = 'unknown'
# the long description of the module (usually content of README)
cmn_long_desc = 'unknown'
# the format of the long desc (usually markdown)
cmn_long_desc_type = 'unknown'


# --------------------
## return the module name for this given arg
#
# @return the module name or an error message
def get(var):
    if not var:
        return 'var is not set'

    if var == 'cmn_mod_name':
        return cmn_mod_name

    if var == 'cmn_mod_dir_name':
        return cmn_mod_dir_name

    return f'unknown var: {var}'


# --------------------
## get the version string from the module's version.json file
# get the long desc i.e. the README.md content
#
#  note: must not use Constants here; causes the install/setup to fail
#
# @return the version string and the long version of it
def init():
    global cmn_long_version  # pylint: disable=global-statement
    global cmn_long_desc  # pylint: disable=global-statement
    global cmn_long_desc_type  # pylint: disable=global-statement

    # generate version.json
    root_dir = Path('..').parent
    if cmn_is_module:
        # generate version.json
        version = {'version': cmn_version}
        path = os.path.join(root_dir, cmn_mod_dir_name, 'lib', 'version.json')
        with open(path, 'w', encoding='utf-8') as fp:
            json.dump(version, fp, indent=4)

    cmn_long_version = cmn_version.replace('.', '_')

    cmn_long_desc = (root_dir / 'README.md').read_text()
    cmn_long_desc_type = 'text/markdown'
