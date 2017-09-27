# DeviceBuilder

This tool has various functions to work with OCF swagger type defintions.
The base function is to create an swagger file from OCF swagger type definitons that can be used for:
- code generation (as input of swagger2x) (work in progress)
- generate introspection file.

# Usage
The tool is python3.5 code.

run from the commandline in the src directory:

```python3 DeviceBuilder.py```


Running the above command gives all command line options available. 

# Introspection data file creation from oic/res.
create introspection file from an oic/res (json) input file.
The oic/res file can be used "as is" from an implementation.

## Options needed to run the tool:
- introspection : output base file
- ocfres: the oic/res output in json
- resource_dir: the directory with the swagger resource files (e.g. download the contents of this folder from oneIOTa/github)

## Optional options dependend on the wanted output:
- remove_property : array of properties that needs to be removed, e.g. range, step, etc that are not implemented
- type: if the resource is multi-valued, e.g. oneOf(integer,number) then one force an single type for this


## Simple input format
  The ```simple input format``` is an stripped down version of oic/res json file.
  It still has all needed data to create an introspection file.
  The intention is that if you do not have an implementation yet, this file format can be used to create an introspection file.
  see for example: input/binaryswitch-brightness-minimal.json
  
  where it differs from oic/res json file:
  - removed all core/security resources 
  - having only list of links of the application level resources.
      the resources are defined with minimal options per resource:
      - "href" : "/BrightnessResURI"  == will be the url to be called
      - "rt" : ["oic.r.light.brightness"] == array of implemented types (only 1 type is suppported)
      - "if" : ["oic.if.a","oic.if.baseline"] == array of implemented interfaces

# Implemented features

per resource (output file per detected and found resource)
- add default rt taken from oic/res
- replace enum of if from oic/res
- remove properties: n, value, range, precision, step as commandline option
- collapse/replace oneOf of types per property in definition part by the given argument
merge different output files into 1 swagger file.

## Optimisations:
- clean descriptions (e.g. make them empty string, so that swagger is still valid)
- removal of x-examples

# Todo

- tests
- examples
- support multiple rt types 
 