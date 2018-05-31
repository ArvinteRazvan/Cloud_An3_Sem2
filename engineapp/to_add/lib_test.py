from __future__ import print_function
import httplib2
import os
import base64
import email
from apiclient import errors
# from mapcoordinates import get_coordonates

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

print(httplib2.__version__)
'''
- name: httplib2
  version: "0.10.3"
'''