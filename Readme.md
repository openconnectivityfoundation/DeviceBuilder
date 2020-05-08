# DeviceBuilder

This script has various functions to work with OCF swagger type definitions.
The base function is to:
- create an single swagger file from OCF swagger type definitions (oneIOTa, Core,...)
This swagger definition file of an full device (application level resources) can be used for:
- code generation (as input of swagger2x) 
- generate introspection file.

Typical flow to define an OCF device using DeviceBuilder is:
- determine device type :
    - see for list of [OCF devices specification](https://openconnectivity.org/specs/OCF_Device_Specification.pdf) or [interactive webpage](https://openconnectivityfoundation.github.io/devicemodels/docs/index.html)
    - chosing a Device Type determines the mandatory resources that has to be implemented.
    - add optional resources to the device:
        - this can be any resource described in [oneIOTa](https://www.oneiota.org)
        - alternatively one can [search interactively](https://openconnectivityfoundation.github.io/devicemodels/docs/resource.html)
    - create the input for the DeviceBuilder
        - see https://github.com/openconnectivityfoundation/DeviceBuilder/tree/master/DeviceBuilderInputFormat-file-examples
    - determine which code generator needs to be used:
        - [IoTivity-Lite](www.iotivity.org): C code (for Linux, Windows,..)
    - run one of the toolchain scripts
        - scripts in the main directory of the DeviceBuilder repo.
        - scripts are written in BASH, e.g. requiring a Linux command prompt.

            
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
     

The generated code depends on the available code generation templates in swagger2x.
  
Currently available DeviceBuilder scripts are:
-  DeviceBuilder_IotivityLiteServer.sh
    - C code generation for the IOTivity-Lite stack in C.
    - see for details [here](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/IOTivity-lite)
    - usage :
        see  [here](DeviceBuilder/DeviceBuilderInputFormat-file-examples/readme.md) for examples of the DeviceBuilder input format and command line options.
-  DeviceBuilder_C++IotivityServer.sh
    - C++ code generation for the C++ IOTivity API
    - see for details: https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/C%2B%2BIotivityServer
    - usage :
        see [here](DeviceBuilder/DeviceBuilderInputFormat-file-examples/readme.md)for examples of the DeviceBuilder input format and command line options. 
 
 The DeviceBuilder script installs the following components:
 - github repos:
    - [swagger2x - the code generation tool] (https://github.com/openconnectivityfoundation/swagger2x)
    - [oneIOTa - resource data models](https://github.com/OpenInterConnect/IoTDataModels
    - core - core resource models
        https://github.com/openconnectivityfoundation/core
 - installs needed python (3.5) packages.
 Note that this only works if one has already downloaded/cloned the DeviceBuilder github repo.
 
    
Additional manual steps to build the generated code:
- download IoTivity 
  - see: https://www.iotivity.org/documentation
- edit build files in IoTivity 
    - see additional instructions that are supplied with generated with the code.
- build
    - instructions vary according the used platform
    - see read me file with the generated code
- test against CTT (see additional instructions that are supplied with the generated code)
    - using the generated PICS file.

            
## Individual python tools

The usage of the individual python scripts in this repo can be found [here](https://openconnectivityfoundation.github.io/swagger2x/individual_tools.md).
           

