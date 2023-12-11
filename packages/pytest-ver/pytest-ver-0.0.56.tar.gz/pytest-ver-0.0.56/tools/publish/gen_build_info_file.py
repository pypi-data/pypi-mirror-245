import argparse
import os
import sys

from tools import common
from tools.debug_logger import DebugLogger as logger
from tools.publish.gen_build_info import GenBuildInfo

# --------------------
## generate the build information file
parser = argparse.ArgumentParser()
parser.add_argument('--no_log', dest='log', action='store_false', default=True)
args = parser.parse_args()

if common.cmn_is_module:
    path = os.path.join(common.cmn_mod_dir_name, 'lib', 'build_info.py')
else:
    path = os.path.join('lib', 'build_info.py')

binfo = GenBuildInfo()
binfo.init(path, args.log)
rc = binfo.gen()
binfo.term()

if rc == 0:
    logger.ok(f'GenBuildInfo passed rc={rc}')
else:
    logger.err(f'GenBuildInfo failed with rc={rc}, exiting')
sys.exit(rc)
