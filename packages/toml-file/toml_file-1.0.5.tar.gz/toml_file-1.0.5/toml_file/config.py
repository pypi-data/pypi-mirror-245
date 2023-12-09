"""
Configuration file object

A dict-like subclass to manage data and templates seemlessly.

The TomlDecoder returns two nested dictionaries which can be used directly 
however, this class provides a convience wrapper for both.

It returns subdicts together with their template as a new Config instances for
and automatically applys defualts and validation from the template.

Templating:

c = Config()
c['int'] = types.IntType(valid=[2,8,10,16], default=2) 
c['float'] = types.FloatType(min=0, max=255, default=1.0) 
c['string'] = types.StringType(default='test')

sub = types.DictType()
c['section'] = sub
sub['test'] = types.IntType(default=1) 
sub['pi'] = types.FloatType(default=3.14) 

"""
from . import types
from .types import ValidationError
from .parser import toml_parser

#%%-----------------------------------------------------------------------------
# Main config class
#-------------------------------------------------------------------------------
class Config():
    def __init__(self, file=None, data={}, template='load' ):
        """
        Config object stores both data/template together with convience   
        
        file - path of toml file to open
        
        or
        
        data - dictionary of values to store in Config
        
        template -  option templating dictionary/TableType
                    or 
                    'load' to create template from file
                    or
                    'new' to create blank template 
        """
        #create empty config (optionally using template)
        if file is None:
            self.data = data
            if isinstance(template, types.TableType):
                self.template = template
            else:
                self.template = types.TableType()
            
        #load from file
        else:
            self.load(file, template=template)
       
    # --- interface methods
    def load(self, file, template='load'):
        """
        Load the filename or open file object given.
        
        [optional] 
        template TableType to validate loaded values against.
            or
        'load' to create template from file (keep comments/types defined in file)
            or
        'new' to create blank template.(all comment/type infomation from file is discarded)
        """
        #get data and template dictionaries from file
        if isinstance(file, str):
            d,t = toml_parser.open(file)
        else:
            d,t = toml_parser.load(file)
            
        #set template/data attributes
        if isinstance(template, types.TableType):
            self.data = d
            self.template = template
            #validate loaded data against provided template
            self.template.validate( d)
        
        elif template == 'new':
            #use only loaded data create empty template
            self.data = d
            self.template = types.TableType()
            
        elif template == 'load':
            # use loaded template
            self.data = d
            self.template = t

    def loads(self, s, template='load'):
        """
        Parse the string given into this Config object.
        
        [optional] 
        template TableType to validate loaded values against.
            or
        'load' to create template from file (keep comments/types defined in file)
            or
        'new' to create blank template.(all comment/type infomation from file is discarded)
        """
        #get data and template dictionaries from string
        d,t = toml_parser.loads(s)
        
        #set template/data attributes
        if isinstance(template, types.TableType):
            self.data = d
            self.template = template
            #validate loaded data against provided template
            self.template.validate( d)
        
        elif template == 'new':
            #use only loaded data create empty template
            self.data = d
            self.template = types.TableType()
            
        elif template == 'load':
            # use loaded template
            self.data = d
            self.template = t
        
    def save(self, filename, indent_subtables=4):
        """
        Save the Config to the filename given.
        """
        s = self.template.to_str(  self.data, indent_subtables=indent_subtables)
        with open( filename, 'w', newline='', encoding='utf-8') as file:
            file.write(s)
        
    def dump(self, file, indent_subtables=4):
        """
        Write the Config to open file object given.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        s = self.template.to_str(  self.data, indent_subtables=indent_subtables)
        file.write(s)   
         
    def dumps(self, indent_subtables=4 ):
        """
        Write the Config to a string.
        
        Optional kwargs:
        
        indent_subtables - Number of characters to indent subtable by.
        """
        s = self.template.to_str(  self.data, indent_subtables=indent_subtables)
        return s
    
    def as_dict(self):
        """
        Return the configuration dictionary only
        """
        return self.data
        
    # --- Basic dict-like interfaces to alow subdicts to retreive together with
    # their template as a new Config instance sharing the same dictionaries
    def __getitem__(self, key):
        """
        Get item:
            - allow only string keys
            - allow multilevel indexing
            - return sub-dicts as Configs
            - return default value if key is templated but not set
            todo:
            - return lists/tuples as ConfigList with template info
        """
        if isinstance(key, str) is False:
            raise KeyError(f'Config keys much be strings {key}')
            
        table = self.data       # start with data dict
        ttable = self.template  # start with template dict
        
        while True:
            #check if key in the table
            if key in table:
                break
        
            #Check if first parent is quoted key
            if key.startswith( ('"',"'")):
                end = key.find(key[0], 1)
                parent = key[1:end]
                key = key[end+2:] #skip next dot!
                if key=='': #no more parts
                    key = parent
                    break
            
            #check for dotted part
            else: 
                parent, *rest = key.split('.',1)
                if rest==[]:#no remaining parts get current key
                    key = parent
                    break
                key = rest[0]
                 
            #get parent
            table = table[parent]
            ttable = ttable.get(parent, {})
           
            #print('parent ', repr(parent),'key', repr(key))
        
        #get the value and template type
        #print('key', repr(key))
        value = table.get( key, None)
        tvalue = ttable.get( key, None)
        
        # no value - try template for default
        if (value is None) and (tvalue is not None):
            value = tvalue.get_default()
        
        # still no value assoicated with the key
        if value is None:
            raise KeyError(f'{key}')
        
        # wrap as config object if a dict
        if isinstance(value, dict):
            value = Config(data=value, template=tvalue)

        return value
        
    def __setitem__(self, key, value):
        """
        set item:
            - allow multilevel indexing
            - validate key value against template
            - if config.type.TomlType instance store as template
        """
        if isinstance(key, str) is False:
            raise KeyError('Config keys much be strings')
        
        table = self.data       # start with data dict
        ttable = self.template  # start with template dict
        
        while True:
            #check if key in the table
            if key in table:
                break
        
            #Check if first parent is quoted key
            if key.startswith( ('"',"'")):
                end = key.find(key[0], 1)
                parent = key[1:end]
                key = key[end+2:] #skip next dot!
                if key=='': #no more parts
                    key = parent
                    break
            
            #check for dotted part
            else: 
                parent, *rest = key.split('.',1)
                if rest==[]:#no remaining parts get current key
                    key = parent
                    break
                key = rest[0]
                 
            #get parent
            table = table[parent]
            ttable = ttable.get(parent, {})
           
            #print('parent ', repr(parent),'key', repr(key))
        
        # Check if setting a Config object
        if isinstance(value, Config):
            table[key] = value.data
            ttable[key] = value.template
            
        # Check if setting the template value
        elif isinstance(value, types.TomlBaseType):
            #p assed value is actually a template value
            tvalue = value
            
            # check if existing value passes validation
            value = table.get( key, None)
            if (value is not None):
                try:
                    tvalue.validate(value)
                except ValidationError as e:
                    raise ValidationError(f'Existing value does not meet new template requirements! {e}')
                
            # all okay - store new template
            ttable[key] = tvalue
        
        # otherwise setting the value
        else:
            # get the template type
            tvalue = ttable.get( key, None)
            
            # check value against template type
            if tvalue is not None:
                # this will raise ValidationError if value is not acceptable
                tvalue.validate(value)
                
            elif types._get_default_type(value) is None:
                raise ValueError(f'Unsupported type {type(value)} for TOML Config - should be bool, int, float, str, list, tuple, dict, datetime.datetime')
        
            # store
            table[key] = value 

    def __iter__(self):
        return iter(self.data)
        
    def __len__(self):
        return self.data.__len__()
        
    def keys(self):
        return self.data.keys()
    
    def items(self):
        return self.data.items()
        
    def pop(self, key):
        """
        Remove specified key from data and template returning both
        """
        value = self.data.pop(key)
        tvalue = self.template.pop(key)
        return (value, tvalue)

    def update(self, data):
        """
        Update the internal values from the data dictionary given.
        
        This will validate each value against the internal template.
        """
        for key in data:
            #get value
            value = data[key]
            
            # get the template value
            tvalue = self.template.get( key, None)
            
            # check value against template type
            if tvalue is not None:
                # this will raise ValidationError if value is not acceptable
                tvalue.validate(value)
                
            elif types._get_default_type(value) is None:
                raise ValueError(f'Unsupported type {type(value)} for TOML Config - should be bool, int, float, str, list, tuple, dict, datetime.datetime')
        
            # store
            self.data[key] = value 
        
    def get(self, key, default=None):
        """"
        Dictlike get method that will store the default in the dictionary when 
        requested
        """
        try:
            value = self[key]
        except KeyError:
            self[key] = value = default
        return value
        
    # --- pretty printing functions
    def __repr__(self):
        s= 'Config section:\n'
        for key,value in self.items():
            if isinstance(value, dict):
                s +=f'[{repr(key)}]\n'
            #elif isinstance(value, (list, tuple)):
            #    s +=f'{repr(key)} = {repr\n'
            else:
                s +=f'{repr(key)} = {repr(value)}\n'
        return s
        
    # --- extra config interfaces using template
    def add_template(self, key, type, **kwargs):
        pass
        
    def add_comment(self, key, comment):
        pass
        
    def set_from_string(self, key, svalue):
        pass
