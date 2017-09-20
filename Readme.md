# DeviceBuilder

This tool has various functions to work with swagger.
The base function is to create an swagger file that can be used for
- code generation (as input of swagger2x)
- introspection.

# introspection data file creation from oic/res.


- create introspection file from an oic/res input file.



# implemented checks

per resource (output file per detected and found resource)
- add default rt taken from oic/res
- replace enum of if from oic/res


# todo

- remove value from definition part
- remove range/precision if type is boolean
- remove range as commandline option
  - remove step as sub command line option
- remove precision as commandline option
- remove n as commandline option
- collapse oneOf of types in definition part

- merge different output files into 1