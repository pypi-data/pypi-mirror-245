# TOML_file
TOML file reader - python module to read/write toml configuration files

- Files can be loaded and saved completed with comments and formating
- Configuration files can be templated and values validated on load or value changes

Two interfaces:

Simple dictionaries {key: value} 
    - data dictionary with nested dictionary with {key: value}
    - template dictionary with comments/type information
    - template allows type, min/max  and other validators to be set and stores 
      comments
    - use load/save functions to open/save to file.
	- use loads/dumps functions to load/convert to string

Config object interface:
    - allows seamless use of template/data via custom dictlike interface
    - use cfg = Config(filename) to open
    - access subtables/keys via exteneded key indexing e.g. cfg['Table1.subtable.key'] = 1
    - if a template has been set any value will be validated when it is set.
    - if a template has been set any missing values will return the defualt and be created.
    - use cfg.save(filename) to save