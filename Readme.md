# DeviceBuilder

## Description

This Tool has various functions to work with OCF swagger type definitions.
The base function of DeviceBuilder is to:

- create a single Swagger2.0 file from OCF swagger type definitions (oneIOTa, Core,...)
The single swagger definition file of a full device (application level resources) can be used for:
  - code generation (as input of [swagger2x](/swagger2x))
  - generation of the introspection file.

This tool is part of [the tool chain](#tool-chain).

## Table of Contents

- [DeviceBuilder](#devicebuilder)
  - [Description](#description)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Flow](#flow)
    - [Tool Chain](#tool-chain)
    - [Available scripts](#available-scripts)
    - [Manual steps](#manual-steps)
    - [Individual python tools](#individual-python-tools)
  
## Installation

Installation of DeviceBuilder is making a clone of the repository and
use the tool relative of where the repository is located on your system.
To install the dependencies:

run ```pip3 install -U -r requirements.txt``` to install the dependencies.

The full installation of all tools and repos can be achieved via [setup](https://openconnectivity.github.io/IOTivity-Lite-setup/).

## Usage

### Flow

Typical flow to create an OCF device using DeviceBuilder is:

- Create the [input file](/DeviceBuilder/DeviceBuilderInputFormat-file-examples) for the DeviceBuilder
  - Determine device type :
        - see for list of OCF Devices [the Device specification](https://openconnectivity.org/specs/OCF_Device_Specification.pdf) or use [the interactive webpage](https://openconnectivityfoundation.github.io/devicemodels/docs/index.html)
        - choosing an OCF Device Type determines the mandatory resources that has to be implemented.
    - Add optional resources to the device:
      - This can be any resource described in [oneIOTa](https://www.oneiota.org) or from the [Resource Type specification](https://openconnectivity.org/specs/OCF_Resource_Type_Specification.pdf).
        - Alternatively one can [search interactively](https://openconnectivityfoundation.github.io/devicemodels/docs/resource.html)
- Determine which code generator needs to be used:
  - [IoTivity-Lite](www.iotivity.org): C code (for Linux, Windows,..)
- Run one of the toolchain scripts
  - scripts in the [main directory](https://github.com/openconnectivityfoundation/DeviceBuilder) of the DeviceBuilder repo.
    - scripts are written in BASH, e.g. requiring a Linux command prompt.

### Tool Chain

The tool chain script implements the following tool chain to generate code:
![ToolChain](https://openconnectivityfoundation.github.io/DeviceBuilder/data/toolchain.png)

The generated code depends on the available code generation templates in [swagger2x](/swagger2x).

### Available scripts

Currently available DeviceBuilder scripts are:

- DeviceBuilder_IotivityLiteServer.sh
  - C code generation for the IOTivity-Lite stack in C.
  - see for details [here](swagger2x/src/templates/IOTivity-lite)
    - usage :
        see  [here](DeviceBuilder/DeviceBuilderInputFormat-file-examples/readme.md) for examples of the DeviceBuilder input format and command line options.
- DeviceBuilder_C++IotivityServer.sh
  - C++ code generation for the C++ IOTivity API
    - see [here for details](https://github.com/openconnectivityfoundation/swagger2x/tree/master/src/templates/C%2B%2BIotivityServer)
    - usage :
        see [here](DeviceBuilder/DeviceBuilderInputFormat-file-examples/readme.md)for examples of the DeviceBuilder input format and command line options.

 The DeviceBuilder script installs the following components:

- github repos:
  - [swagger2x - the code generation tool](/swagger2x)
  - [IoTDataModels - resource type data models](https://github.com/openconnectivityfoundation/IoTDataModels)
  - [core - core resource models](https://github.com/openconnectivityfoundation/core)
- installs needed python (3.5) packages.
 Note that setup script only works if one has already downloaded/cloned the DeviceBuilder github repo.

### Manual steps

Manual steps to build the generated code:

- [Download IoTivity](https://www.iotivity.org)
- Edit build files in IoTivity
  - see additional instructions that are supplied with generated with the code.
- Build
  - Instructions vary according the used platform
    - See read me file with the generated code
- Test against CTT (see additional instructions that are supplied with the generated code)

### Individual python tools

The usage of the individual python scripts in this repo can be found [here](/DeviceBuilder/individual_tools)
