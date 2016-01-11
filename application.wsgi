#!/usr/bin/python

import sys
sys.stdout = sys.stderr
sys.path.insert(0, '/var/www/orchid')
from main import app as application
