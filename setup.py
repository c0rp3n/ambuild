#!/usr/bin/env python
# vim: set ts=2 sw=2 tw=99 et:

import sys

def detect_distutils():
  sys.path.pop(0)
  try:
    import ambuild2.util
    try:
      val = getattr(ambuild2.util, 'INSTALLED_BY_PIP_OR_SETUPTOOLS')
    except AttributeError:
      sys.exit(1)
  except ImportError:
    pass

  sys.exit(0)

# This if statement is supposedly required by multiprocessing.
if __name__ == '__main__':
  import os
  import multiprocessing as mp

  print('Checking for distutils installed version of AMBuild')

  mp.freeze_support()
  proc = mp.Process(target=detect_distutils)
  proc.start()
  proc.join()

  if proc.exitcode != 0:
    sys.stderr.write('''You have an older installation of AMBuild. AMBuild must
now be installed using pip (see README.md). To prevent
conflicts, please remove the old distutils version. You can
do this by inspecting the following paths and removing
any ambuild folders:
\n''')

    for path in sys.path[1:]:
      found = False
      for candidate in ( os.path.join(path, 'ambuild'), os.path.join(path, 'ambuild2') ):
        if os.path.exists(candidate):
          found = True
          break

      if found:
        sys.stderr.write(path + '\n')

    sys.stderr.write('Aborting installation.\n')
    sys.stderr.flush()
    sys.exit(1)

  from setuptools import setup, find_packages
  try:
    import sqlite3
  except:
    raise SystemError('py-sqlite3 must be installed')

  amb_scripts = []
  if sys.platform != 'win32':
    if sys.platform == 'darwin':
      amb_scripts.append('scripts/ambuild_dsymutil_wrapper.sh')
    else:
      amb_scripts.append('scripts/ambuild_objcopy_wrapper.sh')

  setup(
    name = 'AMBuild',
    version = '2.0',
    description = 'AlliedModders Build System',
    author = 'David Anderson',
    author_email = 'dvander@alliedmods.net',
    url = 'http://www.alliedmods.net/ambuild',
    packages = find_packages(),
    python_requires='>=2.6',
    entry_points = {
      'console_scripts': [
        'ambuild = ambuild2.run:cli_run'
      ]
    },
    scripts=amb_scripts,
    zip_safe=False
  )
