# DeviceBuilder

This tool has various functions to work with OCF swagger type defintions.
The base function is to create an swagger file from OCF swagger type definitons that can be used for:
- code generation (as input of swagger2x) 
- generate introspection file.

Tool chain:

                         __________
                        |          |
                        | oneIOTa  |
                        |__________|
                             |
                     resource|descriptions
                             |
                      _______v_________                                                      _______________
     input           |                |         introspection data (swagger)               |               |
     description     |                |--------------------------------------------------->|               |
     --------------->|  DeviceBuilder |        ___________         __________              | actual device |
                     |                | code  |           |  src  |          | executable  |               |
                     |                |------>| swagger2x |------>| compiler |------------>|               |
                     |________________| data  |___________|       |__________|             |_______________|
                                      (swagger)
                                       

# Usage
The tool is python3.5 code.

run from the commandline in the src directory:

```python3 DeviceBuilder.py```


Running the above command gives all command line options available. 

# swagger file creation from oic/res.
## for introspection
create introspection file from an oic/res (json) input file.
The oic/res file can be used "as is" from an implementation.
This swagger data:
- x-examples removed
- descriptions as emtpy strings

## for code generation data 
create code generation file from an oic/res (json) input file.
The oic/res file can be used "as is" from an implementation.
This swagger data includes:
- x-examples
- full descriptions


## Options needed to run the tool:
- introspection : output base file
- ocfres: the oic/res output in json
- resource_dir: the directory with the swagger resource files (e.g. download the contents of this folder from oneIOTa/github)

## Optional options dependend on the wanted output:
- remove_property : array of properties that needs to be removed, e.g. range, step, etc that are not implemented
- type: if the resource is multi-valued, e.g. oneOf(integer,number) then one force an single type for this
note that this is done on all the resources in the same way.


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

note that this works for:
- resources that are an actuator or sensor
- works for collections, but without batch
  - batch introduces the next level of resources, which is not handled in the format.
      
# Implemented tool features

per resource (output file per detected and found resource)
- add default rt taken from oic/res
- fix the href
- replace enum of if from oic/res
- remove properties: n, value, range, precision, step as commandline option
- collapse/replace oneOf of types per property in definition part by the given argument
- for introspection:
    - remove the x-examples
    - clear the descriptions (e.g. make string empty)
merge different output files into 1 swagger file.

## Optimisations (introspection):
- clean descriptions (e.g. make them empty string, so that swagger is still valid)
- removal of x-examples

# How it works

-The oic/res file is read.
-All resources from core/security resources are ignored.
-for all remaining resources    
  - the swagger file that belongs to the "rt" is looked up
  - for all found files with an "rt" that belongs to the device
    - fix the rt value as definition
    - fix the href
    - remove unwanted properties
    - fix the type
    - (remove unwanted (not needed) text descriptions)
  - merge all files into 1 output file

# Todo
- tests (partially done)
- support multiple rt types 
- collections: batch interface
- bug: fix anyOff in introspection removal, 
   - actually this should be removed in raml2doc..
 