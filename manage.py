#!/usr/bin/env python3
from django.core.management import execute_from_command_line
import os
import sys

os.environ.setdefault("DJANGO_SETTINGS_MODULE", 'config.settings.dev')

execute_from_command_line(sys.argv)
