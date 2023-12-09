"""
TOML types
-----------

Types classes - objects used to store templating information (comments, 
formatting and validation information) and to deal with writing values to string

Also includes the Exceptions and some utility functions used in the to_str 
methods and main encoder class

TODO: 
string formatting options
datetime formatting / validation options
"""
import os
import datetime
import string
import numpy as np  #for handling numpy data types

#%%-----------------------------------------------------------------------------
# Exceptions
#-------------------------------------------------------------------------------
class EncodingError(Exception):
    pass
 
# Define exception to raise when parsing fails.
class ParsingError(Exception):
    pass
 
class ValidationError(Exception):
    pass
    
#%%-----------------------------------------------------------------------------
# utility function
#-------------------------------------------------------------------------------
VALID_TYPES = [bool, int, float, str, datetime.datetime, dict, list, tuple]

def _quote_name( name, allowed = set(string.ascii_letters+string.digits+'_-') ):
    """ Return a quote version of the name if required """
    #check if empty name stirng
    if name=='':
        return '""'
        
    #check if allowed wihtout quotes
    sname = set(name)
    if (sname <= allowed):
        return name
    
    #check if contains quotes
    has_single = "'" in sname
    has_double = '"' in sname
    
    if has_single and not has_double:
        #wrap in double quotes
        return '"'+name+'"'
    if has_double and not has_single:
        #wrap in single quotes
        return "'"+name+"'"
    
    #has both - wrap in double quotes and escape any "
    return '"' + name.replace('"', r'\"')+ '"'
        
def _is_table_array(value):
    """
    check if list value should be treated as an array of tables i.e. all 
    elements are dicts
    """
    if isinstance(value, (list,tuple) ) is False:
        return False
    return all(isinstance(elem ,dict) for elem in value)

def _is_inline_array(value):
    """
    check if list value should be treated as an inline array i.e. some
    elements are not dicts
    """
    if isinstance(value, (list,tuple) ) is False:
        return False
    return not all(isinstance(elem ,dict) for elem in value)
    
def _get_default_type( value ):
    """
    Get a new template object for a value or None
    """
    # Arrays can be inline array or TableArray
    if isinstance( value, (list,tuple)):
        if _is_table_array( value):
            return TableArray()
        else:
            return ArrayType()
            
    #numpy data types need to be converted to python float/int first
    if isinstance(value, np.generic):
        value = value.item()
        
    # Rest are easy
    DEFAULT_TYPES = {   
                    int : IntType,
                    float: FloatType,
                    bool: BoolType,
                    datetime.datetime: DateTimeType,
                    str : StringType,
                    dict: TableType,                 
                    }
    t = DEFAULT_TYPES.get( type(value), None)
    if t is None:
        return None
        
    return t()

def _write_dict(ttable, dtable, 
                    indent=0, indent_subtables=4, table_name=None):
    """
    Utility function to write a dictionary of values - used for Table and 
    TableArray.
    
    ttable  - the template dict
    dtable  - the data dict
    
    indent - current indent in characters
    indent_subtables - Number of characters to indent subtable by
    table_name - None or ['table_name'] to write as
    """
    # ----------------------------------------------------------------------
    # sort keys to next ensure all keys are written before subtables
    # in keeping with toml syntax
    # ----------------------------------------------------------------------
    subs = []
    keys = []
    for key in dtable:
        value = dtable[key]
        
        #sub tables
        if isinstance(value, dict):
            #check if formatted to be written inline
            ttype  = ttable.get( key, TableType() )
            if ttype.inline is False:
                subs.append(key) #write as table
            else:
                keys.append(key) #write as inline table
                
        # check for arrays of tables
        elif isinstance(value, (list,tuple)):          
        
            #check if formated to be written as an array
            ttype  = ttable.get( key, None )
            if (ttype is None) and (_is_table_array(value)):
                ttype = TableArray()
            elif (ttype is None):
                ttype = ArrayType()
            
            if isinstance(ttype, TableArray):
                subs.append(key) #an array of tables
            else:
                keys.append(key) #an inline table

        # everything else
        else:
            keys.append(key)
            
    # ----------------------------------------------------------------------        
    # loop over keys and write first
    # ----------------------------------------------------------------------  
    s = ''
    sindent = ' '*indent      
    for key in keys:

        # get the value and tomltype
        value = dtable[key]
        tvalue = ttable.get( key, None)
        if tvalue is None:
            tvalue = _get_default_type(value)
        if tvalue is None:
            raise EncodingError(f'unknown type in dict {key}{type(value)}')
            
        # check if keyname needs quotes
        key = _quote_name(key)
        
        # write precomments for item
        precomments =  (os.linesep + sindent).join(tvalue.pre_comments) 
        if precomments:
            s +=  sindent + precomments + os.linesep 

        # get string representation - indent passed to multiline types to 
        # enable indenting to start of value in key = value
        try:
            svalue = tvalue.to_str(value, indent+len(key)+3)
        except Exception as e:
            raise ValueError(f'{key}: failed template validation: {e}')
        
        # write key = value
        s += f'{sindent}{key} = {svalue}'
        
        # write post comment and indent new line
        if tvalue.post_comment is not None:
            s += sindent + tvalue.post_comment + os.linesep
        else:
            s += os.linesep

    # ----------------------------------------------------------------------
    # loop over subsections (tables, array of tables)
    # ----------------------------------------------------------------------
    # calculate new indent for subtables
    sub_indent = indent + indent_subtables
    for key in subs:
        
        # get value and tomltype
        value = dtable[key]
        tvalue = ttable.get(key, None)
        if tvalue is None:
            tvalue = _get_default_type(value)
        if tvalue is None:
            raise EncodingError(f'Unknown type in dict {key}{type(value)}')                

        # get full section name
        if table_name:
            name = table_name+'.'+ _quote_name(key)
        else:
            name =  _quote_name(key)

        # add the subtable string
        s += tvalue.to_str( value,  indent=sub_indent, 
                                    indent_subtables=indent_subtables,
                                    table_name=name)

        #add newline at end of table
        if s.endswith(os.linesep*2) is False:
            s += os.linesep
    
    s +=''
    return s
#%%-----------------------------------------------------------------------------
# Type classes define how to write, Type and validate items in the
# dictionaries
#-------------------------------------------------------------------------------

#Base Type class only
class TomlBaseType():
    def __init__(self, **kwargs):
        """
        TomlType base type - not used directly
         - implements comments/validation interface
        """
        # Comments
        self.pre_comments = []   #list of comments written before the item
        self.post_comment = None  #list of comments written after the item  
        
    def __repr__(self):
        return str(self.__class__.__name__.rstrip('Type'))

    # Comments interfaces
    def set_comments(self, comments, post=False):
        """
        Set the list of comments assoicated with the item
        post false - written before the item
        post True  - writen after the item (or inline)
        """
        if post:
            self.post_comments = comments
        else:
            self.pre_comments = comments
    
    def add_comment(self, comment, post=False):
        """
        Add a comment.
        post false - written before the item
        post True  - writen inline after the item
        """
        comment = str(comment)
        if comment.startswith('#') is False:
            comment = '# '+comment.lstrip()
        if post:
            self.post_comment=comment
        else:
            self.pre_comments.append(comment)
            
    def get_comments(self, sep=os.linesep):
        """
        Get pre and post comments strings
        """
        pre = os.linesep.join(self.pre_comments) 
        post = self.post_comment+os.linesep
        return pre,post
    
    # Validation interface
    def validate(self, value):
        """
        Check if the value passed meets the templated requirements .
        
        If the value fails type specific tests (i.e. min, max or allowed values)
        this should raise a ValidationError.
        """
        return True
    

# Generic type class used when a better class doesn't exist
class TomlType(TomlBaseType):
    """
    Class representing formating/validation infomation about a keys value
    """
    def __init__(self, **kwargs):
        """
        TomlType base class
        
        Validation kwargs:
        ------------------
        default - default value
        valid = [] list of valid values
        """
        # base init
        TomlBaseType.__init__(self, **kwargs)
        
        # mew attributes
        self.valid = None       #valid value list or None
        self.default = None
        
        # set valid values
        if 'valid' in kwargs:
            self.set_valid( kwargs['valid']) 
        # set default
        if 'default' in kwargs:
            self.set_default( kwargs['default'])
            
    # Formatting interface    
    def to_str(self, value, indent=0):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        return repr(value) 
        
    def from_str(self, svalue):
        """
        Convert from a string representation, i.e. as returned from GUI controls
        """
        return svalue
        
    # Validation interface
    def validate(self, value):
        """
        Check if the value passed meets the templated requirements .
        
        If the value fails type specific tests (i.e. min, max or allowed values)
        this should raise a ValidationError.
        """
        # check value against valid types
        if type(value) not in VALID_TYPES:
            raise ValidationError(f'Unsupported type {type(value)} for TOML Config - should be bool, int, float, str, datetime.datetime')
        
        # check against allowed valid list
        if self.valid is not None:
            if value not in self.valid:
                raise ValidationError(f'Value {value} not in valid list {self.valid}')
        return True
    
    def set_valid(self, valid):
        """ Set a list of valid values or None to clear """
        # clear valid list check
        if valid is None:
            self.valid = None
            return
        
        # cache old valid list incase of failure
        old = self.valid
        self.valid = None
        # check new values against other tests
        for value in valid:
            try:
                self.validate(value)
            except ValidationError as e:
                self.valid = old
                raise ValueError(f'Value {value} in valid list fails validation conditions: {e}')
        
        #store new valid list
        self.valid = valid

    # Default value
    def get_default(self):
        """ Get the default value or None if not set"""
        return self.default
        
    def set_default(self, value):
        """ Set the default value or None to clear """
        if value is None:
            self.default = None
        else:
            self.validate(value)
            self.default = value

# -----------------------------------------------------------------------------
# Toml Types
# -----------------------------------------------------------------------------
#Boolean
class BoolType(TomlType):
    def to_str(self, value, indent=0):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        if value is True:
            value = 'true'
        else:
            value = 'false'
        return f"{value}"

    def from_str(self, svalue):
        """
        Convert from a string representation, i.e. as returned from GUI controls
        """
        if svalue == 'true': value=True
        elif svalue == 'false': value=False
        else: raise ParsingError(f'Cannot convert string {svalue} to bool')
        return value

    def validate(self, value):
        """
        Check if the value passed is okay to interprete as a bool
        """
        if isinstance(value, bool) is False:
            raise ValidationError(f'Expected booleen type, got {type(value)}')
        return True
    
# General numerical type
class NumericalType(TomlType):
    def __init__(self, **kwargs):
        """
        Numerical type can be int/float
        
        Validation kwargs:
        ------------------
        default = set default value
        min = set minimium value
        max = set maximium value
        valid = [] list of valid values
        
        Formating kwargs:
        -----------------
        format = python format string for output e.g. 'd' or 'f'
        """
        # new attributes
        self.min = None
        self.max = None
        self.fstring = '{value:}'          #formating control for output

        # base init
        TomlType.__init__(self, **kwargs)

        # set min/max
        if 'min' in kwargs:
            self.set_min( kwargs['min'])
        if 'max' in kwargs:
            self.set_max( kwargs['max'])
        if 'format' in kwargs:
            self.set_format(format = kwargs['format'])
            
    def from_str(self, svalue):
        """
        Convert from a string representation, i.e. as returned from GUI controls
        - general numerical type allways converts to float
        """
        value = float(svalue)
        return value
        
    def set_min(self, value):
        """Set the minimium valid value or None to clear"""
        if value is None:
            self.min = None
        elif isinstance( value, (int,float)) is False:
            raise ValueError('Expected int/float for limit')
        else:
            self.min = value
    
    def set_max(self, value):
        """Set the maximium valid value or None to clear"""
        if value is None:
            self.max = None
        elif isinstance( value, (int,float)) is False:
            raise ValueError('Expected int/float for limit')
        else:
            self.max = value
    
    def set_format(self, format='0.2f'):
        """
        Set the output format using python string format notation
        This should be valid for float.
        e.g. '0.2f' to_str(255) -> '255.00'
        """
        fstring = '{value:'+str(format)+'}'
        #test
        fstring.format(value = 255.12345)
        #store
        self.fstring = fstring
        
    def validate(self, value):
        """
        Check if the value passed is valid
        """
        # check type
        if isinstance(value, (int,float)) is False:
            raise ValidationError(f'Expected int or float type, got {type(value)}')
        
        # check min/max
        if self.min is not None:
            if value<self.min:
                raise ValidationError(f'Value {value} smaller than minimium condition {self.min}')
        if self.max is not None:
            if value>self.max:
                raise ValidationError(f'Value {value} larger than maximium condition {self.max}')    
        
        # do base class validation
        return TomlType.validate(self, value)

# Int class
class IntType(NumericalType):
    def __init__(self, **kwargs):
        """
        int type
        
        Validation kwargs:
        -----------------
        default = set default value
        valid = [] list of valid values
        min = set minimium value
        max = set maximium value
        
        Formating kwargs:
        -----------------
        format = python format string for output e.g. 'd' 
       
        Or combinations of the following keywords
        (these will be ignored if format keyword argument is given)

        base = 2,8, 10, 16 write values in this format e.g. 'b', 'o', 'd', 'x'
        use_sep = True/False write numbers with _ digit seperators  e.g '_d'
        """
        # base init
        NumericalType.__init__(self, **kwargs)

        # formating kwargs
        # set the format base (2 binary, 8 octal, 10 decimal, 16 hexidecimal)
        if 'base' in kwargs:
            base = kwargs['base']
        else: 
            base = 10
        # use digit seperators
        if 'use_sep' in kwargs:
            use_sep = kwargs['use_sep']
        else:
            use_sep = False
        if 'format' in kwargs:
            format = kwargs['format']
        else:
            format = None
        #set the formatting
        self.set_format( base, use_sep, format)
 
    def set_format(self, base=10, use_sep=False, format=None):
        """
        Set the optional foramting used format the string representation of the 
        int.
        
        base    -  i.e. binary=2, octal=8, decimal=10, hexidecimal=16.
        use_sep - write _ digit seperators
        format  - User provided python style format string that is compatible 
                  with the toml syntax. Only the part after the ':' is required.
                  i.e value=255, 
                  format='+d' gives '+255'
                  format='0=+7d' gives '+000255'
                  
                  Note: Use format will ignore other options and format should
                  be toml compatible! see. toml.io
        """
        #User specified format string
        if format:
            fstring = '{value:'+str(format)+'}'
            #test
            fstring.format(value=255)
            #store
            self.fstring = fstring
            return
        
        if use_sep:
            sep='_'
        else:
            sep=''
        
        if base == 2:
            prefix = '0b'
            typecode='b'
        elif base == 8:
            prefix = '0o'
            typecode='o'
        elif base == 10:
            prefix = ''
            typecode='d'
        elif base == 16:
            prefix = '0x'
            typecode='x'
        else:
            raise ValueError('Unsupport integer base for formatting')
        self.fstring = prefix+'{value:'+sep+typecode+'}'
        
    def to_str(self, value, indent=0):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        try:
            self.fstring.format(value=value)
        except:
            print(value)
            raise
        return self.fstring.format(value=value)
        
    def from_str(self, svalue):
        """
        Convert from a string representation, i.e. as returned from GUI controls
        """
        value = int(float(svalue))
        return value
        
    def validate(self, value):
        """
        Check if the value passed is valid
        """
        if isinstance(value, int) is False:
            raise ValidationError(f'Expected int type, got {type(value)}')
        #do numerical type checks
        return NumericalType.validate(self, value)
        
# Float class
class FloatType(NumericalType):
    
    def __init__(self, **kwargs):
        """
        float type
        
        Validation kwargs:
        -----------------
        default = set default value
        valid = [] list of valid values
        min = set minimium value
        max = set maximium value
        
        Formating kwargs:
        -----------------
        format = python format string for output e.g. 'f' 
        """
        # base init
        NumericalType.__init__(self, **kwargs)

        # formating kwargs
        if 'format' in kwargs:
            self.set_format(format = kwargs['format'])
        else:
            self.set_format('')

    def to_str(self, value, indent=0):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        return self.fstring.format(value=value)
        
    def from_str(self, svalue):
        """
        Convert from a string representation, i.e. as returned from GUI controls
        """
        value = float(svalue)
        return
        
    def validate(self, value):
        """
        Check if the value passed is valid
        """
        if isinstance(value, float) is False:
            raise ValidationError(f'Expected float type, got {type(value)}')
        #do numerical type checks
        return NumericalType.validate(self, value)
        
# String class - split into literal string/ string ???
class StringType(TomlType):
    def __init__(self, **kwargs):
        """
        string type
        
        Validation kwargs:
        -----------------
        default = set default value
        valid = [] list of valid values
        """
        # base init
        TomlType.__init__(self, **kwargs)

    def to_str(self, value, indent=0):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        if value.count('\n')>0:
            term = '"""'
        else:
            term = '"'
        #print('in:',repr(value))
        svalue = value.replace('\\', '\\\\')        #escape backslash
        svalue = svalue.replace('"', '\\"')         #escape "
        #print('out: ',repr(svalue))
        return term+svalue+term
    
    def validate(self, value):
        """
        Check if the value passed is valid
        """
        # check type
        if isinstance(value, str) is False:
            raise ValidationError(f'Expected str type, got {type(value)}')
        
        # do base class validation
        return TomlType.validate(self, value)

# LiteralString  - use to write strings as literal strings - encoder default is 
# to treat python strings as toml strings, however literal string can be 
# specified in a template
class LiteralStringType(TomlType):
    def __init__(self, **kwargs):
        """
        literal string type
        
        Validation kwargs:
        -----------------
        default = set default value
        valid = [] list of valid values
        
        Formating kwargs:
        -----------------
        todo:
        """
        # base init
        TomlType.__init__(self, **kwargs)
        
    def to_str(self, value, indent=0):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        #literal strings can only contain upto 2x''
        if (value.count("'''")>0):
            raise EncodingError('Attempt to encode string with three or more single quotes! as literal string')
        
        #use triple quotes for \n or '
        if (value.count('\n')>0) or (value.count("'")>0):
            term = "'''"
        else:
            term = "'"
        return term+value+term

    def validate(self, value):
        """
        Check if the value passed is valid
        """
        # check type
        if isinstance(value, str) is False:
            raise ValidationError(f'Expected str type, got {type(value)}')
        
        # do base class validation
        return TomlType.validate(self, value)
        
class DateTimeType(TomlType):
    def __init__(self, **kwargs):
        """
        DateTime type
        
        Validation kwargs:
        -----------------
        default = set default value
        valid = [] list of valid values
        before = value must be before specified datetime
        after = value must be after specified datetime
        
        formatting kwargs:
        ------------------
        todo: formatstring approach??? valid toml formats only.
        """
        # base init
        TomlType.__init__(self, **kwargs)
        
    def to_str(self, value, indent=0):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        return value.isoformat()
    
    def validate(self, value):
        """
        Check if the value passed is valid
        """
        # check type
        if isinstance(value, datetime.datetime) is False:
            raise ValidationError(f'Expected str type, got {type(value)}')
        
        # do base class validation (valid values check)
        return TomlType.validate(self, value)
    
# ------------------------------------------------------------------------------
# Container types
# ------------------------------------------------------------------------------

# Tables/Dict class
class TableType(TomlBaseType, dict):
    def __init__(self, data={}, **kwargs):
        """
        Template item representing a dict/table in the TOML spec.
                
        data - dict of TomlTypes
        
        validation kwargs:
        -----------------
        require_templated   - True/False. If True validation will fail if 
                                templated key not present
        allow_untemplated   - True/False. If False validation will fail if an
                                untemplated key is present.

        formatting kwargs:
        ------------------
        inline              - True/False write output as inline table
        write_defaults      - Write default values for this table
        """
        # dict init
        dict.__init__(self, data)
        
        # base init
        TomlBaseType.__init__(self)
        
        # formatting attributes
        self.inline = False       
        self.write_defaults = False

        # set inline
        if 'inline' in kwargs:
            self.set_inline(kwargs['inline'])
            
        # set write_defaults
        if 'write_defaults' in kwargs:
            self.set_write_defaults( kwargs['write_defaults'])
            
        # validation attribtues
        self.require_templated = False
        self.allow_untemplated = True

        # set require templated
        if 'require_templated' in kwargs:
            self.set_require_templated(kwargs['require_templated'])

        # set allow untemplated
        if 'allow_untemplated' in kwargs:
            self.set_allow_untemplated(kwargs['allow_untemplated'])
            
    def __repr__(self):
        return 'Table'+dict.__repr__(self)
    
    # --- overload dict methods to only accept TomlBaseTypes
    def __setitem__(self, key, value):
        if isinstance(value, TomlBaseType) is False:
            raise ValueError(f'Can only add TomlBaseType to TableType not {type(value)}')
        dict.__setitem__(self, key, value)

    def update(self, ttable):
        if isinstance(ttable, TableType) is False:
            raise ValueError('Can only update from TableType')
        dict.update(self, ttable)
        
    # formating interface - used when dict is written inline like a value
    def set_inline(self, inline=True):
        """
        Mark this dictionary as written inline
        """
        self.inline = inline

    def set_write_defaults(self, flag=True):
        """
        Write default values for this table
        """
        self.write_defaults = flag

    def to_str(self, dict_value, 
                    indent=0, indent_subtables=4,
                    table_name=None):
        """ 
        Write to string. If formatting option is set to inline write as inline
        table style otherwise write as full table style
        
        Optional kwargs:
        
        indent - current indent in characters
        indent_subtables - Number of characters to indent subtable by
        table_name - None or ['table_name'] to write as
        """
        # if writing defaults get the default dict then update with values 
        # passed in
        if self.write_defaults:
            dtable = self.get_default()
            dtable.update(dict_value)
        # otherwise dtable is just the value passed in
        else:
            dtable = dict_value
        
        if self.inline:
            s = self._to_str_inline(dtable, indent)
        else:
            s = self._to_str(dtable, indent, indent_subtables, table_name)
        return s
        
    def _to_str_inline(self, dtable, indent=0):
        """Helper method - for writing inline table value"""
        # write output 
        sindent = ' '*indent
        s = '{ '        
        for key in dtable:
            # get the value and tomltype
            value = dtable[key]
            ttype = self.get( key, None)
            if ttype is None:
                ttype = _get_default_type(value)
            if ttype is None:
                raise EncodingError(f'unknown type in dict {key}{type(value)}')
            
            # nested inline dicts are possible but weird! make sure written 
            # inline too
            if isinstance(value, dict):
                ttype.set_inline(True)
                
            # get string representation
            svalue = ttype.to_str(value)
            
            # check if keyname needs quotes
            key = _quote_name(key)
            
            # write precomments for item
            precomments =  (os.linesep + sindent).join(ttype.pre_comments) 
            if precomments:
                s += sindent + precomments + os.linesep               
             
            # write key = value
            s += f'{key} = {svalue}, '
             
            # write psot comments and indent new line for next key = value
            if self.post_comment is not None:
                s += self.post_comment + os.linesep + sindent
        
        # remove trailing comma and add }
        s = s[:-2]+' }'
            
        return s
    
    def _to_str(self, dtable, 
                    indent=0, indent_subtables=4,
                    table_name=None):
        """ Helper method - for writing full table style """
        s = ''
        
        # calculate indent for table name 
        sindent = ' '*(indent - indent_subtables)
        
        # write precomments for item
        for precomment in self.pre_comments:
            s += sindent + precomment + os.linesep
        
        if table_name is not None:
            # write section header
            s += sindent + f'[{table_name}]'
            
            # write post comments (should only be post comments in name sections!)
            if self.post_comment is not None:
                s += ' '+self.post_comment
            s += os.linesep

        # write table contents
        s += _write_dict(self, dtable, indent, indent_subtables, table_name)
        return s
        
    # Validation interface
    def set_require_templated(self, flag=True):
        """
        Ensure validation of dictionary fails if a templated key is missing
        """
        self.require_templated = flag
        
    def set_allow_untemplated(self, flag=True):
        """
        Allow untemplated keys in dictionary to be validated
        """
        self.allow_untemplated = flag
    
    def validate(self, dict_value):
        """
        Check if the dict passed in meets the templated requirements .
        
        This will raise a ValidationError on failure
        """
        # check value against valid types
        if isinstance( dict_value, dict) is False:
            raise ValidationError(f'Expected a dict got {type(dict_value)}')

        # loop over each key in template and ensure it is present, and the 
        # value validates
        for key in self:
                
                # check all templated keys are present in dict to being validated
                if self.require_templated:
                    try:
                        value = dict_value[key]
                    except:
                        raise ValidationError(f'key {key} is required but not present')
                
                
                #check value against template
                if key in dict_value:
                    try:
                        value = dict_value[key]
                        tvalue = self[key]
                        tvalue.validate(value)
                        
                    except ValidationError as e:
                        raise ValidationError(f'Value of key {key} fails validation: {e}')
        
        # check other keys present in the dict_value
        for key in dict_value:
        
            # check if key is a string
            if isinstance(key, str) is False:
                raise ValidationError(f'Non-string key {key} in dictionary')
        
            # check if in template
            if (self.allow_untemplated is False) and (key not in self):
                raise ValidationError(f'Untemplated key {key} found in dictionary (use allow_untemplated=True to allow)')
            
        return True
    
    # Get defaults
    def get_default(self):
        """
        Return a dict constructed from default values in the this template dict
        """
        defaults = {}
        for key in self:
            tvalue = self[key]
            if tvalue is not None:
                default = tvalue.get_default()
            defaults[key] = default
        return defaults

# Arrays/lists in the data
class ArrayType(TomlBaseType, list):
    def __init__(self, data=[], **kwargs):
        """
        Template item representing a Array in the TOML spec.
        
        data = list/tuple of TomlTypes
        
        
        Validation kwargs:
        ------------------
        default - default value
        
        allow_untemplated   - True/False. If False validation will fail if extra
                                untemplated values are present.
        """
        # list init
        list.__init__(self, data)
        
        # base init
        TomlBaseType.__init__(self)
        
        # Validation attributes
        self.allow_untemplated = True
        self.default = None
        
        # set default
        if 'default' in kwargs:
            self.set_default( kwargs['default'])
            
        # set allow untemplated
        if 'allow_untemplated' in kwargs:
            self.set_allow_untemplated(kwargs['allow_untemplated'])
        
    def __repr__(self):
        return 'Array'+list.__repr__(self)
        
    # --- overload list method to only accept TomlBaseType
    def __setitem__(self, n, value):
        if isinstance(value, TomlBaseType) is False:
            raise ValueError('Can only add TomlBaseType to TableArray')
        list.__setitem__(self, n, value)
        
    def append(self, object):
        if isinstance(object, TomlBaseType) is False:
            raise ValueError('Can only add TomlBaseType to TableArray')
        list.append(self, object)
        
    def insert(self, index, object):
        if isinstance(object, TomlBaseType) is False:
            raise ValueError('Can only add TomlBaseType to TableArray')
        list.insert(self, index, object)
        
    def extend(self, iterable):
        for value in iterable:
            self.append(value)
            
    # --- formatting         
    def to_str(self, dlist,  indent=0 ):
        """
        Convert the value to a toml style string representation applying any 
        formating options
        """
        # open list
        s = f'[ '
        sindent = ' '*indent

        # loop over elements in list
        for n in range(len(dlist)):
        
            # get the value and tomltype
            value = dlist[n]
            if n<len(self):
                ttype = self[n]
            else:
                ttype = _get_default_type(value)
            if ttype is None:
                raise EncodingError(f'unknown type in array {type(value)}')
            
            # nested dicts are treated as inline
            if isinstance(value, dict):
                ttype.set_inline(True)
                
            # for a list within a list add a newline first
            elif isinstance( value, (list,tuple) ):
                s += os.linesep + sindent
                
            # write precomments for item
            precomments =  (os.linesep + sindent).join(ttype.pre_comments) 
            if precomments:
                s += sindent + precomments + os.linesep               
             
            # get string representation
            svalue = ttype.to_str(value)
            
            # write value 
            s += f'{svalue}, '
             
            # write comments and indent new line for next value
            if ttype.post_comment is not None:
                s += ttype.post_comment + os.linesep + sindent
        
        #remove trailing comma and add ]
        s = s[:-2]+' ]'
            
        return s
    
    # Validation
    def set_allow_untemplated(self, flag=True):
        """
        Allow untemplated values in list/tuple to be validated
        """
        self.allow_untemplated = flag
        
    def validate(self, dlist):
        """
        Check if the dict passed in meets the templated requirements .
        
        This will raise a ValidationError on failure
        """
        if isinstance( dlist, (list,tuple)) is False:
            raise ValidationError(f'Expected a list or tuple, got {type(list_value)}')
        
        # check templated items
        for n in range(0, len(self)):
            tvalue = self[n]
            if len(dlist)>n:
                value = dlist[n]
            else:
                raise ValidationError(f'Missing templated value {n} in array')
            #check value against template
            try:
                tvalue.validate(value)
            except ValidationError as e:
                raise ValidationError(f'Value {n} fails validation: {e}')
        
        # check other items are valid
        if self.allow_untemplated is False:
            if len(dlist) > len(self):
                raise ValidationError(f'Untemplated values in array len(data)={len(dlist)}, len(template)={len(self)}')
        else:
            for n in range(len(self), len(dlist)):
                value = dlist[n]
                tvalue = _get_default_type(value)
                if tvalue is None:
                    raise ValidationError(f'Invalid value of type {type(value)} in array')
                    
                #check value against template
                try:
                    tvalue.validate(value)
                except ValidationError as e:
                    raise ValidationError(f'Invalid value in array: {e}')
        
    # Default value
    def get_default(self):
        """ Get the default value or None if not set"""
        return self.default
        
    def set_default(self, value):
        """ Set the default value or None to clear """
        if value is None:
            self.default = None
        else:
            self.validate(value)
            self.default = value

# Arrays of tables/list of dicts
class TableArray(TomlBaseType, list):
    def __init__(self, data=[], **kwargs):
        """
        Template item representing a list of dicts/array of tables in the TOML 
        spec.
        
        data = list/tuple of TomlTypes

        TableArrays can be templated by adding individual TableTypes or by 
        using the default table Table.Array.default which will be applied to
        all Tables.
        """
        # list init
        list.__init__(self, data)
        
        # base init
        TomlBaseType.__init__(self)
        
        # attributes
        self.default = None     # default value

        # set default
        if 'default' in kwargs:
            self.set_default( kwargs['default'])
        
    def __repr__(self):
        return 'TableArray'+list.__repr__(self)
    
    # --- overload list method to only accept TableType
    def __setitem__(self, n, value):
        if isinstance(value, TableType) is False:
            raise ValueError('Can only add TableType to TableArray')
        list.__setitem__(self, n, value)
        
    def append(self, object):
        if isinstance(object, TableType) is False:
            raise ValueError('Can only add TableType to TableArray')
        list.append(self, object)
        
    def insert(self, index, object):
        if isinstance(object, TableType) is False:
            raise ValueError('Can only add TableType to TableArray')
        list.insert(self, index, object)
        
    def extend(self, iterable):
        for value in iterable:
            self.append(value)
    # ---        
    def to_str(self, dlist, 
                    indent=0, indent_subtables=4, table_name=None):
        """ 
        Write to string. 
        Optional kwargs:
        
        indent - current indent in characters
        indent_subtables - Number of characters to indent subtable by
        table_name - None or [['table_name']] to write as
        """
        s = ''
        
        # calculate indent for table name 
        sindent = ' '*(indent - indent_subtables)
        
        #loop over dicts in the list
        for n in range(0,len(dlist)):
            
            # get the dicts from the lists
            dtable = dlist[n]
            
            # if the template has multiple dicts use them, otherwise use the 
            # first table as template for all, if none defined use an empty 
            # table
            if len(self)>n:
                ttable = self[n]
            elif len(self)==1:
                ttable = self[0]
            else:
                ttable = TableType()
            
            # write precomments
            # write precomments for item
            for precomment in ttable.pre_comments:
                s += sindent + precomment + os.linesep
            
            # write section header
            if table_name:
                s += sindent + f'[[{table_name}]]'
                
            # write post comment and indent new line
            if ttable.post_comment is not None:
                s += ' '+ttable.post_comment
            s += os.linesep
                
            # write the dict items
            s += _write_dict(ttable, dtable, indent, indent_subtables, table_name)
            s += os.linesep
            
        return s
    
    # Default value
    def get_default(self):
        """ Get the default Table used for Tables in the array """
        return self.default
        
    def set_default(self, value):
        """ Set the default Table used for Tables in the array """
        if value is None:
            self.default = None
        else:
            self.validate(value)
            self.default = value

    def validate(self, dlist):
        """
        Check if the list passed in meets the templated requirements .
        
        This will raise a ValidationError on failure
        """
        if isinstance( dlist, (list,tuple)) is False:
            raise ValidationError(f'Expected a list or tuple, got {type(list_value)}')
        if _is_table_array(dlist) is False:
            raise ValidationError(f'Expected a list or tuple of dicts')
        
        #loop over dicts in the list
        for n in range(0,len(dlist)):
            
            # get the dicts from the lists
            dtable = dlist[n]
            
            # if the template has multiple dicts use them, otherwise use the 
            # first table as template for all, if none defined use an empty 
            # table
            if len(self)>n:
                ttable = self[n]
            elif len(self)==1:
                ttable = self[1]
            else:
                ttable = TableType()
            
            # validate
            ttable.validate( dtable)
