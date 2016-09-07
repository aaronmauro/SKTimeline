#!/usr/bin/python
import sys
import logging
import os

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.dirname(__file__) )

from sktimeline import app as application 
