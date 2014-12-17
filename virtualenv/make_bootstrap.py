#!/usr/bin/env python

import virtualenv

s = '''
import subprocess, os

def after_install(options, home_dir):
    if os.name == 'posix':
        subprocess.call([os.path.join(home_dir, 'bin', 'pip'), 'install', '-r', 'requirements.txt'])
    else:
        subprocess.call([os.path.join(home_dir, 'Scripts', 'pip.exe'), 'install', '-r', 'requirements.txt'])
'''

script = virtualenv.create_bootstrap_script(s, python_version='2.7')
f = open('bootstrap.py','w')
f.write(script)
f.close()
