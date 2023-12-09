"""
TOML decoder using toml format https://toml.io
-----------------------------------------------

TomlDecoder class - main decoder/parsing class use open/load/loads to load 
                    configuration from filepath, file or string.
                    
Templating: 
-----------
The decoder also generates a template containing formating and
comments found in the file. This can be passed to the encoder to retain comments
and some formatting styles (e.g. int written as hexadecimal).

This template is a nested dictionary/TableType of TomlType objects defined for 
the types in the TOML syntax.

Comments are treated as being associated with a value using the following rules.
 - A full comments line (or multiple full comment lines) are associated with the 
    next key/value or table.
 - Inline comments are associated with the key/value on the same line.
 - Comments inside arrays (lists) or inline tables (dicts) are associated with  
    the preceeding value),
"""
import io                                             #for string buffers
import re                                             #for spliting of values
from dateutil.parser import parse as datetime_parser  #for easy datetime parsing
from ast import literal_eval         #processing of escape sequences in strings

from .types import *                 #types for template creation on load

__all__ = ['toml_parser', 'toml_writer', 'load', 'loads', 'save', 'dumps']

#%%-----------------------------------------------------------------------------
# Toml parser class - using 
#-------------------------------------------------------------------------------
class TomlParser():
    """
    Parser using a toml compatible syntax:

    Should support almost full toml spec now however there may be some issues.
    
    + This allows table names to have spaces (not in toml spec) don't use them
    if you want to be 100% compatible
    + Inline tables can have newlines inside {} (not in toml spec) but really 
    normal tables should be used.
    """
    def open(self, filename):
        """
        Open the filename give and parses returns data,template dictionaries
        """
        with open(filename, 'r', newline='', encoding='utf-8') as f:
            return self.parse(f)
            
    def load(self, f):
        """
        Parse the file object returns data,template dictionaries
        """ 
        #wrap the file object buffer to ensure correct line-ending and encoding mode
        self.buffer = io.TextIOWrapper( f.buffer, newline='', encoding='utf-8')
        return self.parse(f)
        
    def loads(self, s):
        """
        Parse the string returns data,template dictionaries
        """
        f = io.StringIO(s)
        return self.parse(f)

    # Main parsing method
    def parse(self, f):
        """
        Parse the file or buffer given return nested dicts
        
        data      = nested dictionary containing parsed data
        template  = nested dictionary containing comments and format information
        """ 
        # buffer some values internally for access
        self.data = {}   # data
        self.template = TableType()
                        # comments are associated with the next key or for
                        # inline comments the current key
        
        #wrap the buffer to ensure correct line endings
        self.buffer = f
        self.linenum = 0        #line count for error reporting

        #read top of filecomments (until a newline) or key/table is encountered
        while True:
            #read next line
            try:
                rawline = self._read_more()
            except EOFError:
                break
            
            line = rawline.lstrip()
            if line.startswith('#'):
                self.template.pre_comments.append(line.strip())
            else:
                break
        #add a blank line comment after to seperate main table comments to key pre-comment
        self.template.pre_comments.append('')
        
        #current data and template tables
        self.curent_dtable = self.data
        self.curent_ttable = self.template
        self.pre_comments = []     #cached comments to be stored with next key
        
        #parse items until end_of_file
        # line from above is parsed first!
        while True:
            # ignore blank lines unless after comments
            if line=='' and len(self.pre_comments)==0:
                pass
            elif line=='' and len(self.pre_comments)>0:
                self.pre_comments.append('')

            #check for comment line
            elif line.startswith('#'):
                self.pre_comments.append(line.strip())
                
            #check for array of tables (list of dicts)
            elif line.startswith('[['):
                self._parse_array_of_tables(line)
            
            #check for table
            elif line.startswith('['):
                self._parse_table(line)
            
            #check for key/value pairs
            else:
                
                #get key names list
                names, remainder = self._get_names( line, term='=')
                key = names[-1]
                tables = names[:-1]
                #print(f'Parse1: {names} {key} {tables}: {remainder}')
                
                #determine type
                value, ttype, remainder = self._parse_value(remainder) 
                #print(f'Parse: {key} value {value} : {repr(remainder)}')
                
                if len(tables)==0:
                    #store into current table
                    dtable = self.curent_dtable
                    ttable = self.curent_ttable
                else:
                    #get the correct table
                    dtable = self._get_data_table(tables, self.curent_dtable)
                    ttable = self._get_template_table(tables, self.curent_ttable)
                    
                # check for inline comment
                post_comment = self._parse_inline_comment(remainder)
                
                # store comments
                if ttype is None:
                    ttype = TomlType() # create tomltype object for key
                
                if self.pre_comments:
                    ttype.set_comments( self.pre_comments) # store comments
                    self.pre_comments = [] # and clear list
                    
                if post_comment:
                    ttype.add_comment(post_comment, post=True)
                    
                #check key is not already defined
                if key in dtable:
                    raise ParsingError(f'Keyname {key} already assigned!')
            
                #store value
                dtable[key] = value
                
                # store tomltype object into the template table
                ttable[key] = ttype

            #read next line
            try:
                rawline = self._read_more()
            except EOFError:
                break

            #strip whitespace
            line = rawline.lstrip()
            
        #clear cache and return
        data = self.data
        template = self.template
        self.data = None
        self.template = None
        self.curent_dtable = self.data
        self.curent_ttable = self.template
        self.pre_comments = [] 
        
        return data, template
    
    # general helpers
    def _read_more(self):
        """ Read the next line form the stream """
        line = self.buffer.readline()
        self.linenum +=1
        if line=='':
            raise EOFError()
        return line
    
    def _get_string(self, line):
        """ get a complete string from the line and return remainder """
        if line.startswith("'"):
            sep="'"
        elif line.startswith('"'):
            sep = '"'
        else:
            return None, line
        i=1
        escaped=False
        while i <len(line):
            if escaped==True:
                escaped=False
            elif line[i]=='\\':
                escaped=True
            elif line[i]==sep:
                break
            i+=1

        if i==len(line) and line[i]!=sep:
            raise ParsingError(f'Unclosed string {repr(sep)} at line number {self.linenum} ; {line}')
        value = line[1:i]
        remainder = line[i+1:]

        return value, remainder
    
    
    def _get_data_table(self, names, parent):
        """ Get or make the table structure given in names """
        # make correct nested dictionaries for this table
        dtable = parent
        for n in names:
            # get each parent table in turn or create
            if n not in dtable:
                dtable[n] = {}
                dtable = dtable[n]
                
            elif isinstance(dtable[n] , list):
                # get the last element of array of tables/dicts
                # eg { 'first' : [ { 'second' : {'returns':'this dict'},}, ]
                # 'first.second' 
                # 'first' returns { 'second' : {'returns':'this dict'},}
                # 'second' returns {'returns':'this dict'}
                dtable = dtable[n][-1]
                
            elif isinstance( dtable[n], dict):
                dtable = dtable[n]
            else:
                raise ParsingError(f'Table name "{n}" already has value at line number {self.linenum}')
        return dtable
        
    
    def _get_template_table(self, names, parent):
        """ Get or make the template table structure given in names """
        # make correct nested dictionaries for this table
        ttable = parent
        for n in names:
            # get each parent table in turn or create
            if n not in ttable:
                ttable[n] = TableType()
                ttable = ttable[n]
                
            elif isinstance(ttable[n] , ArrayType):
                # get the last element of array of tables/dicts
                # eg { 'first' : [ { 'second' : {'returns':'this dict'},}, ]
                # 'first.second' 
                # 'first' returns { 'second' : {'returns':'this dict'},}
                # 'second' returns {'returns':'this dict'}
                ttable = ttable[n][-1]
                
            elif isinstance( ttable[n], TableType):
                ttable = ttable[n]
            else:
                raise ParsingError(f'Table name "{n}" already has tomltype value at line number {self.linenum}')
        return ttable
    
    
    def _get_names(self, line, term=']'):
        """Get the list of names in a dotted table or key name"""
        #split out the full table name from inside [] or dotted key
    
        # can be quoted and dotted...
        # e.g. [table."[sub].".table]
        remainder = line # for table assumes first [ is stripped
        names = []
        while True:
            #print(names, remainder)
            
            #check for quoted part
            name,remainder = self._get_string(remainder)
            if name is not None:
                #store name
                names.append(name)
                
                #remove any whitespace and '.'
                remainder = remainder.lstrip()
                remainder = remainder.lstrip('.')
                
                #check for end ']]' ']' or '='
                if remainder.startswith(term):
                    remainder = remainder[len(term):] #any comment
                    break #leave search loop
            else:
                #try to split at . or term (']'|'=')
                idot = remainder.find('.')
                iterm = remainder.find(term)
                
                #neither found
                if (idot==-1) and (iterm==-1):
                    raise ParsingError(f'Missing {term} terminator, at line number {self.linenum}; {line}')

                #found term first
                elif (idot==-1) or (iterm<idot):
                    name = remainder[:iterm]
                    names.append( name.strip() )
                    remainder = remainder[iterm+len(term):]
                    break #leave search loop
                    
                #found . first
                elif (iterm==-1) or (idot<iterm):
                    name = remainder[:idot]
                    names.append( name.strip() )
                    remainder = remainder[idot+1:]
                    #remove any whitespace
                    remainder = remainder.lstrip()

            #check remainder for end conditions - this shouldn't happen?
            if remainder in ['', '\n']:
                raise ParsingError(f'Missing {term} terminator, at line number {self.linenum}; {line}')
        return names, remainder
    
    # Top level parsing functions
        
    def _parse_table(self, line):
        """
        Parse a sub table line entry
        """
        # Split out the full table name from inside []:
        # can be quoted and dotted...
        # e.g. [table."[sub].".table]
        #strip initial '[' 
        names, remainder = self._get_names(line[1:], term=']')
        #print(f'names {names}, remainder {repr(remainder)}')
        
        # Get or create new tables, and update the current tables
        self.curent_dtable = self._get_data_table(names, self.data)
        self.curent_ttable = self._get_template_table(names, self.template)
        
        #save any precomments
        if self.pre_comments:
            self.curent_ttable.set_comments( self.pre_comments)
            self.pre_comments = []
            
        # check if remaining is an inline comment and add comment
        post_comment = self._parse_inline_comment(remainder)
        if post_comment:
            self.curent_ttable.add_comment( post_comment, post=True)

    
    def _parse_array_of_tables(self, line):
        """
        Parse array of tables (== [ {}, {} ...]) with elements defined by 
        [[array_of_tables]]
        key = value
        """
        # Split out the full table name from inside []:
        # can be quoted and dotted...
        # e.g. [table."[sub].".table]
        #strip initial '[[' 
        names, remainder = self._get_names(line[2:], term=']]')
        #print(f'names {names}, remainder {repr(remainder)}')
        
        #get the nested tables - but not the last one as this needs to be
        # a list!
        dtable = self._get_data_table(names[:-1], self.data)
        ttable = self._get_template_table(names[:-1], self.template)
        n = names[-1]
        if n not in dtable:
            #create a new list and 1st table/dict inside
            dtable[n] = [{}] 
            ttable[n] = TableArray( [ TableType(),] )
            
            #update current tables
            self.curent_dtable = dtable[n][0]
            self.curent_ttable = ttable[n][0]
            
        elif isinstance(dtable[n], list):
            #add new item to existing list
            dtable[n].append({})
            ttable[n].append( TableType() )
            #update current tables
            self.curent_dtable = dtable[n][-1]
            self.curent_ttable = ttable[n][-1]
            
        else:
            raise ParsingError(f'Name "{n}" is not an array of tables at line number {self.linenum}; {line}')

        #save any precomments
        if self.pre_comments:
            self.curent_ttable.set_comments( self.pre_comments)
            self.pre_comments = []
            
        # check if remaining is an inline comment and add comment
        post_comment = self._parse_inline_comment(remainder)
        if post_comment:
            self.curent_ttable.add_comment( post_comment, post=True)

    # Helper functions working on a line with the inital key = stripped or 
    # inside an array
        
    def _parse_value(self, line):
        """
        Parse a line string containing a value to determine type
        
        Returns (value, ttype, remainder)
        """
        line = line.lstrip()  #strip any leading white space
    
        # ----------------------------------------------------------------------
        # Multi-line types - pass whole line
        # ----------------------------------------------------------------------
        if line.startswith('"""'):
            #multiline string
            return self._parse_ml_string(line)
            
        elif line.startswith("'''"):
            #multiline literal string 
            return self._parse_ml_literal(line)
            
        elif line.startswith("["):
            #array/list
            return self._parse_array(line)
        
        elif line.startswith("{"):
            #in-line table
            return self._parse_inline_table(line)
            
        # ----------------------------------------------------------------------
        # Single line types - but need whole line to test
        # ----------------------------------------------------------------------
        elif line.startswith('"'):
            #string - pass whole line
            return self._parse_string( line)
            
        elif line.startswith("'"):
            #literal string - pass whole line
            return self._parse_literal_string( line)
        
        # ----------------------------------------------------------------------
        #Next test for values on single line after spliting 
        # ----------------------------------------------------------------------
        #print(f'parse_value line {repr(line)}')

        #[] values to split at  ',', '#' '\n' ']' '}'
        #() keep seperator
        try:
            rawvalue, sep, remainder = re.split(r'([,#\n}\]])',line, 1)
        except:
            rawvalue = line
            sep = ''
            remainder =''
        rawvalue = rawvalue.strip()
        remainder = sep+remainder #keep seperator for parsing

        #print(f'parse_value rawvalue {repr(rawvalue)};  remainder {repr(remainder)}')
        
        #a leading comma, ] or \n was found?
        if rawvalue=='':
            return (None, None, remainder)

        # ----------------------------------------------------------------------
        # Single line types - using pre-split value,remainder
        # ----------------------------------------------------------------------
        if rawvalue in ['True', 'true']:
            #bool 
            value = True
            ttype = BoolType()
            
        elif rawvalue in ['False', 'false']:
            #bool
            value = False
            ttype = BoolType()
            
        elif rawvalue.count(':') or rawvalue[1:].count('-')>=2:
            #datetime
            # date: YYYY-MM-DD floats: -1e-5 hence ignore 1st char -
            # time: HH:MM:SS
            value = self._parse_datetime(rawvalue)
            ttype = DateTimeType()
        
        elif rawvalue.startswith( ('0b', '-0b','+0b') ):
            #binary int 0b01
            value = self._parse_int(rawvalue, base=2)
            ttype = IntType(base=2)
            
        elif rawvalue.startswith( ('0o', '-0o','+0o') ):
            #octal int 0o01
            value = self._parse_int(rawvalue, base=8)  
            ttype = IntType(base=8)
            
        elif rawvalue.startswith(('0x', '-0x','+0x') ):
            #hex int 0x01
            value = self._parse_int(rawvalue, base=16)
            ttype = IntType(base=16)
            
        elif rawvalue.count('.') or rawvalue.count('e') or rawvalue.count('E'):
            #float
            # 1.0
            # 1e2
            # 1E2
            value = self._parse_float(rawvalue)
            ttype = FloatType()
        
        elif rawvalue in ['inf', '-inf', '+inf', 'nan', '-nan', '+nan']:
            value = self._parse_float(rawvalue)
            ttype =  FloatType()
            
        else:
            #normal int - try a normal int
            value = self._parse_int(rawvalue, base=10)
            ttype = IntType(base=10)
            
        # ----------------------------------------------------------------------
        # still None raise an exception
        # ----------------------------------------------------------------------
        if value is None:
            raise ParsingError(f'Unparseable value at line number {self.linenum} : {line} ')
        
        return value, ttype, remainder

    
    def _parse_ml_string(self, line):
        """
        Parse multi-line string (triple \") - reading more if required.
        """
        #check for string start
        if line.startswith('"""') is False:
            return None, line
                
        #strip 1st newline (as per toml spec)
        if line[3]=='\n':
            #need to start with next line
            try:
                line = self._read_more()
            except EOFError:
                raise ParsingError(f'Unclosed multiline string at line number {self.linenum}: {line}')
        else:
            #otherwise trim starting quotes
            line = line[3:]
            
        #find the last sequence of unescaped """
        i=-1
        while True:
            #find next triple quote
            i = line.find('"""', i+1) 
            if i==-1:
                #read next line
                try:
                    newline = self._read_more()
                except EOFError:
                    raise ParsingError(f'Unclosed multiline string at line number {self.linenum}: {line}')
                #strip whitespace when lines end with \
                if line.endswith('\\\n'):
                    line = line.rstrip('\\\n')
                    newline = newline.lstrip()
                line = line+newline
                
            #check if there is another "
            elif line[i+3] == '"':
                pass #keep looking

            #check if escaped
            elif line[i-1]=='\\':
                pass
                
            else:
                break

            #print(f'ml_string next {repr(line)}')                

        # split out value and remainder
        value = line[:i]
        remainder = line[i+3:]

        #hack check for possible extra quotes upto |""|"""
        #if remainder.startswith('""'):
        #    value = value + '""'
        #    remainder = remainder[2:]
        #elif remainder.startswith('"'):
        #    value = value + '"'
        #    remainder = remainder[1:]

        try:
            #value = str(value)
            #fix to keep \r inside strings replace with escape sequence
            value = value.replace('\r','\\r')
            value = literal_eval('""" '+value+' """') #add spaces to ensure it works even if " immediately before/after """
            value = value[1:-1] #trim spaces
        except Exception as e:
            raise ParsingError( f"{e} at line number {self.linenum} : {line}") 
        
        #print(f'ml_string {repr(value)} , remainder {repr(remainder)}')
        ttype = StringType()
        
        return value, ttype, remainder

    
    def _parse_string(self, line):
        """
        Parse string "" type from string value.
        """
        value, remainder = self._get_string(line)
        #print(f'[{repr(value)}] {value}')
        #remove escaped chars
        try:
            #value = str(value)
            value = literal_eval('"'+value+'"')
        except Exception as e:
            raise ParsingError( f"{e} at line number {self.linenum} : {line}") 
            
        ttype = StringType() ##todo return string ttype
            
        return value, ttype, remainder
       
    
    def _parse_literal_string(self, line):
        """
        Parse literal string '' type from string value.
        """
        #check for literal string
        if line.startswith("'") is False:
            return None, line
            
        #find the first quote close
        i=line.find("'",1)      
        if i==-1:
            raise ParsingError(f"Unclosed literal string \"'\" at line number {self.linenum} : {line}") 
        # split out value and remainder
        remainder = line[i+1:]
        value = line[1:i]
        
        ttype = LiteralStringType()
            
        return value, ttype, remainder
    
    
    def _parse_ml_literal(self, line):
        """
        Parse multi-line literal string (triple ''') - reading more if required.
        """
        #check for string start
        if line.startswith("'''") is False:
            return None, line
            
        #strip 1st newline (as per toml spec)
        if line[3]=='\n':
            #need to start with next line
            try:
                line = self._read_more()
            except EOFError:
                raise ParsingError(f'Unclosed multiline literal string at line number {self.linenum}: {line}')
        else:
            #otherwise trim starting quotes
            line = line[3:]

        #find the first sequence of unescaped """
        i=-1
        while True:
            #find next triple quote
            i = line.find("'''", i+1) 
            if i==-1:
                #read next line
                try:
                    line = line + self._read_more()
                except EOFError:
                    raise ParsingError(f'Unclosed multiline literal string at line number {self.linenum}: {line}')
            
            #check if there is another "
            elif line[i+3] == "'":
                pass #keep looking

            #check if escaped
            elif line[i-1]=='\\':
                pass
                
            #check if unescaped end found
            else:
                break
                
            #print(f'ml_literal next {repr(line)}') 
        
        # split out value and remainder
        value = line[:i]
        remainder = line[i+3:]
        
        #hack check for possible extra quotes upto |''|'''
        if remainder.startswith("''"):
            value = value + "''"
            remainder = remainder[2:]
        elif remainder.startswith("'"):
            value = value + "'"
            remainder = remainder[1:]
            
        #print(f'ml_literal {repr(value)} , remainder {repr(remainder)}')
        ttype = LiteralStringType()
        return value, ttype, remainder
        
    
    def _parse_array(self, line):
        """
        Parse an array of values - as inline arrays can contain comments this
        returns the parse list and a ArrayType list containing any comments.
        """
        #check for array start
        if line.startswith('[') is False:
            return None, line
            
        #itteratively loop over the line
        array = [] #use a list as toml arrays can be mixed 
        ttype = ArrayType() #shadow list with tomltypes
        remainder = line[1:]
        pre_comments = []
        while True:
            
            # strip any white space
            remainder = remainder.lstrip()
            
            # Pre-checks
            # ----------
            # blank line
            if remainder == '':
                #read next line
                try:
                    remainder = self._read_more()
                    remainder = remainder.lstrip()
                except EOFError:
                    raise ParsingError(f'Unclosed array at line number {self.linenum}: {line}')
                    
            # check for comment before value
            if remainder.startswith('#'):
                comment = remainder.strip()
                remainder = ''
                pre_comments.append(comment)
            
            # check for the end of the array!
            elif remainder.startswith(']'):
                remainder = remainder[1:] #remove ]
                break  
                
            # Read a value
            else:
                #print(f'parse_array next loop remainder {repr(remainder)}')
                value, vttype, remainder = self._parse_value(remainder)
                #print(f'parse_array value {repr(value)};  remainder {repr(remainder)}')
                
                # post read value checks
                # ----------------------
                # strip any whitespace before the comma...
                remainder = remainder.lstrip()
            
                # strip comma and whitespace
                if remainder.startswith(','):
                    remainder = remainder[1:].lstrip() #remove , and whitespace
            
                # check for comment after item
                if remainder.startswith('#'):
                    post_comment = remainder.strip()
                    remainder = ''
                else:
                    post_comment = None

                # store comments with the item
                if (vttype is None):
                    vttype = TomlType()
                
                if pre_comments:
                    #print('storing pre-comments', pre_comments)
                    vttype.set_comments(pre_comments)
                    pre_comments = [] #reset for next item
                
                if post_comment:
                    #print('storing post-comments', post_comment)
                    vttype.add_comment( post_comment, post=True)
                
                # finally store the found item/comments
                if value is not None: #value can be None  from parse_value
                    array.append(value)
                    ttype.append(vttype)
            #---
        #---
        #print(f'parse_array return {array};  remainder {repr(remainder)}')
        return array, ttype, remainder        

    
    def _parse_inline_table(self, line):
        """
        Parse inline tables e.g. key = { name= 'tom', age : 7.5 }
        """
        #check for array start
        if line.startswith('{') is False:
            return None, line
        
        #itteratively loop over the line
        table = {}
        ttype = TableType()
        ttype.set_inline(True)
        pre_comments = []

        remainder = line[1:]
        while True:

            # strip any white space
            remainder = remainder.lstrip()
             
            # Pre-checks
            # ----------
            # blank line
            if remainder == '':
                #read next line
                try:
                    remainder = self._read_more()
                    remainder = remainder.lstrip()
                except EOFError:
                    raise ParsingError(f'Unclosed in-line table at line number {self.linenum}: {line}')
                    
            # check for comment before value
            if remainder.startswith('#'):
                comment = remainder.strip()
                remainder = ''
                pre_comments.append(comment)
            
            # check for the end of the table!
            elif remainder.startswith('}'):
                remainder = remainder[1:] #remove ]
                break  
                
            # Read a value
            else:
                #print(f'parse_inline_table next loop; remainder {repr(remainder)}')
                key, value, vttype, remainder = self._parse_key_value(remainder)
                #print(f'parse_inline_table found;key {key}; value {repr(value)};  remainder {repr(remainder)}')

                # post read value checks
                # ----------------------
                # strip any whitespace before the comma...
                remainder = remainder.lstrip()
            
                # strip comma and whitespace
                if remainder.startswith(','):
                    remainder = remainder[1:].lstrip() #remove , and whitespace
            
                # check for comment after item
                if remainder.startswith('#'):
                    post_comment = remainder.strip()
                    remainder = ''
                else:
                    post_comment = None

                # store comments with the item
                if (vttype is None):
                    vttype = TomlType()
                
                if pre_comments:
                    #print('storing pre-comments', pre_comments)
                    vttype.set_comments(pre_comments)
                    pre_comments = [] #reset for next item
                
                if post_comment:
                    #print('storing post-comments', post_comment)
                    vttype.add_comment( post_comment, post=True)
                
                #check key and store
                if key in table:
                    raise ParsingError(f'key {key} already exists in in-line table at linenuymber {self.linenum}: {line}')
                else:
                    table[key] = value
                    ttype[key] = vttype
        
        #print(f'parse_inline_table return {table};  remainder {repr(remainder)}')
        return table, ttype, remainder
       
    
    def _parse_key_value(self, line):
        """
        Parse a key/value pair to toml rules
        """
        # Check for dotted key names that indicate value should be stored in a 
        # table
        # can be quoted and dotted...
        # e.g. 'table."=.=subtable=.=".key = "value" #comment\n'
        #print(f'parse key/value: {line}')
        
        # check for quoted keys 
        if line.startswith( ("'", '"') ):
            key, remainder = self._get_string( line )
            if remainder.lstrip()[0] !='=':
                raise ParsingError(f'Unrecognised line, at line number {self.linenum}; {line}')
            _, raw_value = remainder.split('=', 1)
        else:
            #check for key = value syntax and split
            has_equal = line.count('=')>0
            if not has_equal:
                #not a valid line entry
                raise ParsingError(f'Unrecognised line, at line number {self.linenum}; {line}')
            key, raw_value = line.split('=', 1)
            key = key.strip()           #tidy up the key
            
        #print(f'parse key {key} : {repr(raw_value)}')

        #determine type
        value, ttype, remainder = self._parse_value(raw_value)    
        
        return key, value, ttype, remainder
        
    # Helper functions working on tidied value strings 
    # - comment removed, whitespace stripped
    # - return None if unsucessfull
        
    def _parse_bool(self, value):
        if (value in [ 'true', 'True']):
            v = True
        elif (value in ['false', 'False']):
            v = False
        else:
            v = None
        return v

    
    def _parse_int(self, value, base=10):
        try:
            v = int(value, base)
        except:
            v = None
        return v

    
    def _parse_float(self, value):
        try:
            v = float(value)
        except:
            v = None
        return v
    
    
    def _parse_datetime(self, value):
        try:
            v = datetime_parser(value)
        except:
            v = None
        return v
    
    
    def _parse_inline_comment(self, remainder):
        """check any remainder on a line for a inline comment and add if needed"""
        comment = remainder.strip()
        #print(f'parse inline comment {comment}')
        if comment=='':
            return None
        elif comment.startswith('#') is False:
            raise ParsingError(f'Non-comment content after value at line number {self.linenum}; {remainder}')
        else:
           return comment

#%%-----------------------------------------------------------------------------
# TomlWriter
#-------------------------------------------------------------------------------
class TomlWriter():
    """
    TomlWriter - writes to a toml compatible syntax:

    Should support almost full toml spec now however there may be some issues.
    + bare names can be any valid utf-8 chars (toml only contain ASCII letters,
     ASCII digits, underscores, and dashes (A-Za-z0-9_-)
    
    + This allows table names to have spaces (not in toml spec) don't use them
    if you want to be 100% compatible
    + Inline tables can have newlines inside {} (not in toml spec) but really 
    normal tables should be used.
    """ 
     
    def save(self, filename, data, template=TableType(), indent_subtables=4):
        """
        Write the data dictionary to the filename using the optional
        template given.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        s = template.to_str(  data, indent_subtables=indent_subtables)
        with open( filename, 'w', newline='', encoding='utf-8') as file:
            file.write(s)
            
    
    def dumps(self, data, template=TableType(), indent_subtables=4):
        """
        Write the data dictionary to a string using the optional
        template given.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        #start encoding main dictionary/table
        s = template.to_str(  data, indent_subtables=indent_subtables)

        return s
    
    
    def dump(self, file, data, template= TableType(), indent_subtables=4):
        """
        Write the data dictionary to the open file object using the optional
        template given.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        s = template.to_str(  data, indent_subtables=indent_subtables)
        file.write(s)

#%%-----------------------------------------------------------------------------
# Create interface instance / functions
#-------------------------------------------------------------------------------
toml_parser = TomlParser()
toml_writer = TomlWriter()

def load(filename, return_template=False):
    """ 
    Open the filename given and parses
    
    returns data dictionary and optional template
    """
    data,template = toml_parser.open(filename)
    if return_template:
        return data, template
    else:
        return data

def loads(s, return_template=False):
    """ 
    Parse the string given and return data dictionary and optional template
    """
    data,template = toml_parser.loads(s)
    if return_template:
        return data, template
    else:
        return data

def save(filename, data, template=TableType(), indent_subtables=4):
    """
    Write the data dictionary to the filename
    
    Optional kwargs:
    
    template = type.TableType instance with key templating classes
    indent_subtables - Number of characters to indent subtable by.
    """
    s = template.to_str(  data, indent_subtables=indent_subtables)
    with open( filename, 'w', newline='', encoding='utf-8') as file:
        file.write(s)
        
def dumps(data, template=TableType(), indent_subtables=4):
    """
    Write the data dictionary to a string
    
    Optional kwargs:
    
    template = type.TableType instance with key templating classes
    indent_subtables - Number of characters to indent subtable by.
    """
    s = template.to_str(  data, indent_subtables=indent_subtables)
    return s  