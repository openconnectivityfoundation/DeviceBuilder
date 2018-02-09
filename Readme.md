# DeviceBuilder

This tool has various functions to work with OCF swagger type definitions.
The base function is to:
- create an single swagger file from OCF swagger type definitions (oneIOTa, Core,...)
This swagger definition file of an full device (application level resources) can be used for:
- code generation (as input of swagger2x) 
- generate introspection file.

Typical flow to define an OCF device using DeviceBuilder is:
- determine device type
    - see for list of devices: https://openconnectivity.org/specs/OCF_Device_Specification_v1.3.0.pdf 
    - this determines the mandatory resources that has to be implemented.
    - add optional resources to the device
        - this can be any resource described in oneIOTa, www.oneIOTa.org
    - create the input for the DeviceBuilder
        - see https://github.com/openconnectivityfoundation/DeviceBuilder/tree/master/DeviceBuilderInputFormat-file-examples
    - determine which code generator needs to be used
        - C++ code (for Linux, Windows,..)
    - run one the tool chain script
        - scripts in the main directory of the DeviceBuilder repo
        - these are bash scripts.
        


            
The tool chain script implements the following tool chain to generate code:


                       __________
                      |          |
                      | oneIOTa  |
                      |__________|
                           |
              Resource Type|descriptions
                           |
                    _______v________                                          __________           _______________
     input         |                |    introspection data (swagger.json)   |          |  cbor   |               |
     description   |                |--------------------------------------->| swag2cbor|-------->|               |
     ------------->|  DeviceBuilder |        ___________         __________  |__________|         | actual device |
                   |                | code  |           |  src  |          |                      |               |
                   |                |------>| swagger2x |------>| compiler |--------------------->|               |
                   |________________| data  |___________|       |__________|     executable       |_______________|
                                     (swagger)
                                       
                                      
     Note that swag2cbor is only needed if the device read cbor as introspection format and not the swagger.json
     this depends on the implementation of the stack, IOTivity reads CBOR as input file.
     
Currently available scripts are:
-  DeviceBuilder_C++IotivityServer.sh
    - C++ code generation for the C++ IOTivity API
    - see: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/C%2B%2BIotivityServer
-  DeviceBuilder_NodeIotivityServer.sh
    - javascript code generation for the node.js IOTivity API
    - see: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/NodeIotivityServer
     

 The generated code depends on the available code generation templates in swagger2x.
 The script installs:
 - github repos:
    - swagger2x
        https://github.com/openconnectivityfoundation/swagger2x
    - oneIOTa - resource data models
        https://github.com/OpenInterConnect/IoTDataModels
    - core - core resource models
        https://github.com/openconnectivityfoundation/core
 - installs needed python (3.5) packages.
    
additional manual steps:
- download IOTivity 
- edit build files in IOTivity (see additional instructions that are supplied with generated with the code)
- build
- test against CTT (see additional instructions that are supplied with the generated code)
    - using the generated PICS file.

            
            

# Usage of the individual tools
The tools are python3.5 code.

to install the dependencies run : ``` python3 src\install.py```

run the tool(s) from the commandline in the src directory (DeviceBuilder):

```python3 DeviceBuilder.py -h```

or (cbor conversion)


```python3 swag2cbor.py -h```


Running the above commands gives all command line options available. 

# swagger file creation from oic/res.
Running DeviceBuilder gives the 2 swagger files:
- The Introspection Device Data (IDD) swagger file
- The swagger file representing the device.
The swagger file is ignored.

Tool chain:

                         __________
                        |          |
                        | oneIOTa  |
                        |__________|
                             |
                     resource|descriptions
                             |
                      _______v________                                    ___________           _______________
     oic/res         |                | introspection data(swagger.json) |           |  cbor   |               |
     description     |                |--------------------------------->| swag2cbor | ------->|               |
     --------------->|  DeviceBuilder |            ___________           |___________|         | actual device |
                     |                |  code     |           |                                |               |
                     |                |---------->| /dev/null |                                |               |
                     |________________|  data     |___________|                                |_______________|
                                        (swagger)
     
     Note that swag2cbor is only needed if the device read cbor as introspection format and not the swagger.json     
                                      
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

The advantage of this input format is:
- can be used for existing devices, e.g. just retrieve the oic/res of an existing device

### Options needed to run the tool (oic/res response):
- introspection : output base file, more files are generated with different extensions.
- ocfres: the oic/res output in json
- resource_dir: the directory with the swagger resource files (e.g. download the contents of this folder from oneIOTa/github)


### Optional options depended on the wanted output:
- remove_property : array of properties that needs to be removed, for example the properties "range", "step", etc that will not be part of the implementation
- type: if the resource is multi-valued, e.g. oneOf(integer,number) then one force an single type for this
note that this is done on all the resources in the same way.


### Simplified oic/res response input format
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

note that the generation works for:
- resources that are an actuator or sensor
- works for collections, but without batch interface
  - the batch introduces the next level of resources, which is not handled in the format.
      

### Options needed to run the tool (deviceBuilder):
- introspection : output base file
- input: the manually crafted deviceBuilder input file
- resource_dir: the directory with the swagger resource files (e.g. download the contents of this folder from oneIOTa/github)      
      
      
# Implemented DeviceBuilder features
This is about the DeviceBuilder python code.

Per resource (output file per detected and found resource)
- add default rt taken from oic/res
- fix the href
- replace enum of if from oic/res
- remove properties: n, value, range, precision, step as command line option
- collapse/replace oneOf of types per property in definition part by the given argument
- for introspection:
    - remove the x-examples
    - clear the descriptions (e.g. make string empty)
merge different output files into 1 swagger file.

## Optimizations (introspection):
- clean descriptions (e.g. make them empty string, so that swagger is still valid)
- removal of x-examples

# How it works

- The oic/res response file is read from disk
- All resources from core/security resources are ignored.
- for all remaining resources    
  - the swagger file that belongs to the "rt" is looked up
  - for all found files with an "rt" that belongs to the device
    - fix the rt value as definition
    - fix the href
    - remove unwanted properties
    - fix the type
    - (remove unwanted (not needed) text descriptions)
  - merge all files into 1 output file

  
 ### documentation of the internals
 https://openconnectivityfoundation.github.io/DeviceBuilder/
 