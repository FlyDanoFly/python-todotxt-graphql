#!/usr/bin/env python3

from pathlib import Path
import logging
import sys

logging.basicConfig(stream=sys.stderr)

this_dir = Path(__file__).resolve().parent
sys.path.insert(0, this_dir)

from todotxt_graphql import app as application

