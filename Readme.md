# DeviceBuilder

This tool has various functions to work with swagger.
The base function is to create an swagger file that can be used for
- code generation (as input of swagger2x)
- generate introspection file.

# usage
python3.5 tool.

run from the commandline in the src directory:

```python3 DeviceBuilder.py```


this gives all command line options available. 

# introspection data file creation from oic/res.
create introspection file from an oic/res input file.
The file can be used "as is" from an implementation.

## options needed:
- introspection : output base file
- ocfres: the oic/res output in json
- resource_dir: the directory with the swagger resource files (e.g. download the contents of this folder from oneIOTa/github)

## optional options:
- remove_property : array of properties that needs to be removed, e.g. range, step, etc that are not implemented
- type: if the resource is multi-valued, e.g. oneOf(integer,number) then one force an single type for this


## simple input format
  this is an stripped down version of oic/res, but still have all needed properties to create an introspection file.
  see: input/binaryswitch-brightness-minimal.json as example.
  e.g. removing all core/security resources and just having an list of links of the application level resources.
  the resource is defined with minimal options per resource:
  - href : will be the url to be called
  - "href" : "/BrightnessResURI"  == will be the url to be called
  - "rt" : ["oic.r.light.brightness"] == array of implemented types (only 1 type is suppported)
  - "if" : ["oic.if.a","oic.if.baseline"] == array of implemented interfaces

# implemented features

per resource (output file per detected and found resource)
- add default rt taken from oic/res
- replace enum of if from oic/res
- remove properties: n, value, range, precision, step as commandline option
- collapse/replace oneOf of types per property in definition part by the given argument
merge different output files into 1 swagger file.

## optimisations:
- clean descriptions (e.g. make them empty string, so that swagger is still valid)
- removal of x-examples

# Todo

- tests
- examples
- support multiple rt types 
 