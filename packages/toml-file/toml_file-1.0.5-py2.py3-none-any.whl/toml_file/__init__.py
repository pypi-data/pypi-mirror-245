"""
Built-in configuration libary for use with server-client model instruments.

Currently supports toml syntax but internally data is treated as nested 
dictionaries(tables) or lists of dicts (arrays of tables) so other syntax are
possible by writing a parser.

decoder -  Decoder object responsible for loading data into nested dicts structure
encoder -  Encoder object for writing nested dicts to string/file.
types   -  Templating objects used to add comments and define fomrating to use.

config - Config object provides a top-level interface, combining data and 
         template, together with pretty printing and automatic validation of 
         values against template.
"""
__version__ = "1.0.5"
#import the parser
from . import parser
from .parser import *

# import the Config wrapper class for data and templating classes
from . import types
from .config import Config
