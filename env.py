from os import environ as env
from dotenv import load_dotenv, find_dotenv
import sys

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

if env.get('PYC_FILES') == 'FALSE':
    sys.dont_write_bytecode = True
