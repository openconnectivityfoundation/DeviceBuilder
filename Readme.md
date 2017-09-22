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
- remove properties: n, value, range, precision, step as commandline option


# todo

- collapse oneOf of types per property in definition part

- merge different output files into 1