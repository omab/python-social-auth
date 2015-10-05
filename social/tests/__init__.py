import sys
import warnings


# Ignore deprecation warnings on Python2.6. Maybe it's time to ditch this
# oldie?
if sys.version_info[0] == 2 and sys.version_info[1] == 6 or \
   hasattr(sys, 'pypy_version_info'):
    warnings.filterwarnings('ignore', category=Warning)
