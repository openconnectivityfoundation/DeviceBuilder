# DeviceBuilder Input File

## Introduction

The DeviceBuilder Input format is to list all resources that needs to be included in the device that will make up the application.
It lists the resources that will be sensor/actuators/etc. that make up the functionality of the device.
The format supports additional information per resource to that the OCF data model can be changed.
The changes that are allowed are limited, the result still needs to be OCF compliant. So optional properties, methods etc can be removed from the resource.
The property that is being used to find the resource is the rt value, the rt value being used as lookup towards the oneIOTa/Core github repos where the resource will be pulled from.
To use the properties to change the resource one needs to know what the resource implements.

## Table of Contents

- [DeviceBuilder Input File](#devicebuilder-input-file)
  - [Introduction](#introduction)
  - [Table of Contents](#table-of-contents)
  - [Where to obtain information about OCF Devices and Resources](#where-to-obtain-information-about-ocf-devices-and-resources)
  - [Description of DeviceBuilder Input Format](#description-of-devicebuilder-input-format)
  - [Examples with IoTivity](#examples-with-iotivity)
    - [input-lightdevice.json](#input-lightdevicejson)
    - [input-lightdevice-dimming.json](#input-lightdevice-dimmingjson)
    - [input-lightdevice-dimming.json](#input-lightdevice-dimmingjson-1)

## Where to obtain information about OCF Devices and Resources

In OCF devices are defined by the Device Type.
The Device Types can have mandatory resources.

Device Types are defined in the [device specification](https://openconnectivity.org/specs/OCF_Smart_Home_Device_Specification.pdf).

But for ease of use (search) the list also can be found as [interactive web page.](
https://openconnectivityfoundation.github.io/devicemodels/docs/index.html)

The list of standardized resources can be found in the [Resource Type Specification.](
https://openconnectivity.org/specs/OCF_Resource_Type_Specification.pdf)

For ease of use (search) the resources can also be found in [the interactive web page.](
https://openconnectivityfoundation.github.io/devicemodels/docs/resource.html)

## Description of DeviceBuilder Input Format

The DeviceBuilder input file format is an JSON array that define each resource separately.
The following properties are defined:

- "path" : the path to be used in the implementation
  - required
  - type string
  - must start with "/"
  - must be unique over all resources
- "rt"   : the resource type that needs to be populated
  - required
  - array of strings
- "if"   : the interfaces that needs to be supported
  - required
  - array of strings
  - order is maintained, hence the first listed interface is the default interface.
- "remove_properties" : properties that will be removed
  - optional
  - array of strings, 
  - example: "remove_properties : ["range", "step" "value"]
- "remove_methods" :  methods to remove from the implementation[]
  - optional
  - array of strings
  - example: "remove_methods" : ["post"]
- "override_type" :  override the type of the property value,  
  - optional
  - string, optional, e.g. can be omitted,
  - example  "override_type" :  "integer"
  - typical values "integer", "number" or "string"

The advantage of the file format that it is:
  
- Instructions per resource instance to change the behaviour.
- Format may change by adding new fields to introduce new features to the tool.

## Examples with IoTivity

### input-lightdevice.json

This input file describes the minimal light device, implementing only binary switch (on/off).

- The input file is [here](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/DeviceBuilderInputFormat-file-examples/input-lightdevice.json)
- minimal define resources for oic.d.light:
  - resource type : oic.r.switch.binary
- added resource type oic.wk.p for introspection generation, since IOTivity has optional implemented properties in this resource.
    ```
    [
        {
            "path" : "/binaryswitch",
            "rt"   : [ "oic.r.switch.binary" ],
            "if"   : ["oic.if.a", "oic.if.baseline" ],
            "remove_properties" : [ "range", "step" , "id", "precision" ]
        },
        {
            "path" : "/oic/p",
            "rt"   : [ "oic.wk.p" ],
            "if"   : ["oic.if.baseline", "oic.if.r" ],
            "remove_properties" : [ "n", "range", "value", "step", "precision", "vid"  
        }
    ]
    ```

- DeviceBuilder command:
  - Invoked from the top level github repo, where the script resides
  - Creates output directory outside the github tree.
  ```
    sh DeviceBuilder_IotivityLiteServer.sh ./test/input_DeviceBuilderInputFormat/input-lightdevice.json  ../lightdevice "oic.d.light"
    ```
- actual copy of the generated data available [here](https://github.com/openconnectivityfoundation/DeviceBuilder/tree/master/DeviceBuilderInputFormat-file-examples/code_examples/lightdevice)
  
### input-lightdevice-dimming.json

The light device implementing binary switch (on/off) and the dimming resource.

- The input file is [here](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/DeviceBuilderInputFormat-file-examples/input-lightdevice-dimming.json)

- Resource list for oic.d.light:
  - Resource Type : oic.r.switch.binary
  - Resource Type : oic.r.light.dimming
- Added resource type oic.wk.p for introspection generation.
- DeviceBuilder command
  - Invoked from the top level github repo, where the script resides
  - Creates output directory outside the github tree.
    ```
    sh DeviceBuilder_IotivityLiteServer.sh ./test/input_DeviceBuilderInputFormat/input-lightdevice-dimming.json  ../lightdevice-dimming "oic.d.light"
    ```
- actual copy of the generated data is [here](https://github.com/openconnectivityfoundation/DeviceBuilder/tree/master/DeviceBuilderInputFormat-file-examples/code_examples/lightdevice-dimming)
  
### input-lightdevice-dimming.json
    
The light device implementing binary switch (on/off), dimming and colour chroma.

- The input file is [here](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/DeviceBuilderInputFormat-file-examples/input-lightdevice-dimming-chroma.json)
  
- Resource list for oic.d.light 
  - Resource Type : oic.r.switch.binary
  - Resource Type : oic.r.light.dimming
  - Resource Type : oic.r.colour.chroma
- Added resource type oic.wk.p for introspection generation.
- DeviceBuilder command (IoTivity)
  - Invoked from the top level github repo, where the script resides
  - Creates output directory outside the github tree.
    ```
    sh DeviceBuilder_IotivityLiteServer.sh ./test/input_DeviceBuilderInputFormat/
    input-lightdevice-dimming-chroma.json  ../input-lightdevice-dimming-chroma "oic.d.light"
    ```

- Actual copy of the generated data is [here](https://github.com/openconnectivityfoundation/DeviceBuilder/tree/master/DeviceBuilderInputFormat-file-examples/code_examples/lightdevice-dimming-chroma)