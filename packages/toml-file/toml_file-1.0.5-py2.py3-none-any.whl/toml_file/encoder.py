"""
TOML encoder
-----------

TomlEncoder class - writes data dictionary to files/strings using a toml 
compatible syntax.

Templating: 
-----------
The encoder also takes an optional template - a  dictlike object (TableType) 
mirroring the data dictionary containing of TomlType objects defined for the 
types in the TOML syntax. This enables formatting and validation of values and
writing comments assoicated with the value/key.


Actual writing is handled by the TomlTypes.to_str() methods starting with a 
TableType instance representing the toplevel table.
"""
import string
import datetime
import os
import io

from . import types       #types for template/formating

#%%-----------------------------------------------------------------------------
# TomlEncoder
#-------------------------------------------------------------------------------
class TomlEncoder():
    """
    TomLEncoder - writes to a toml compatible syntax:

    Should support almost full toml spec now however there may be some issues.
    + bare names can be any valid utf-8 chars (toml only contain ASCII letters,
     ASCII digits, underscores, and dashes (A-Za-z0-9_-)
    
    + This allows table names to have spaces (not in toml spec) don't use them
    if you want to be 100% compatible
    + Inline tables can have newlines inside {} (not in toml spec) but really 
    normal tables should be used.
    """   
    def save(self, filename, data, template=types.TableType(), indent_subtables=4):
        """
        Write the data dictionary to the filename using the optional
        template given.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        s = template.to_str(  data, indent_subtables=indent_subtables)
        with open( filename, 'w', newline='', encoding='utf-8') as file:
            file.write(s)
    
    def dumps(self, data, template=types.TableType(), indent_subtables=4):
        """
        Write the data dictionary to a string using the optional
        template given.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        #start encoding main dictionary/table
        s = template.to_str(  data, indent_subtables=indent_subtables)

        return s
    
    def dump(self, file, data, template=types.TableType(), indent_subtables=4):
        """
        Write the data dictionary to the open file object using the optional
        template given.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        s = template.to_str(  data, indent_subtables=indent_subtables)
        file.write(s)

