# Introspection example files

Examples of introspection files

## Table of Contents

- [Introspection example files](#introspection-example-files)
  - [Table of Contents](#table-of-contents)
  - [introspection-empty.txt](#introspection-emptytxt)
  - [introspection-client-iotivity-oic-p](#introspection-client-iotivity-oic-p)
  - [introspection-binaryswitch-actuator.txt](#introspection-binaryswitch-actuatortxt)
  - [introspection-binaryswitch-actuator-oic-p.txt](#introspection-binaryswitch-actuator-oic-ptxt)
  - [introspection-binaryswitch-actuator-if.txt](#introspection-binaryswitch-actuator-iftxt)
  - [introspection-binaryswitch-sensor.txt](#introspection-binaryswitch-sensortxt)
  - [introspection-binaryswitch-actuator-sensor.txt](#introspection-binaryswitch-actuator-sensortxt)
  - [introspection-binaryswitch-2x-actuator.txt](#introspection-binaryswitch-2x-actuatortxt)
  - [binary_switch_if_with_p.txt](#binaryswitchifwithptxt)
  - [ctt_1 test device](#ctt1-test-device)
  - [ctt_2 test device](#ctt2-test-device)
- [Validation of Swagger2.0 introspection files](#validation-of-swagger20-introspection-files)

## introspection-empty.txt

  [introspection-empty.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/ctt_1.swagger.json)
  
  A swagger2.0 file with no paths and no defintions
  can be used if no introspection data is needed.

- manually crafted file
  
## introspection-client-iotivity-oic-p

  [introspection-client-iotivity-oic-p](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/introspection-client-iotivity-oic-p.txt)

  IOTivity response of /oic/p, which also includes optional properties:

    ```
    {
      "rt" : ["oic.wk.p"],
      "if" : ["oic.if.baseline", "oic.if.r"],
      "st" : "2016-06-20T10:10:10Z",
      "mnsl" : "support.default-vendor.com",
      "mnfv" : "1.1.1",
      "mnhw" : "1.1.0",
      "mnos" : "10",
      "mnpv" : "0.0.1",
      "mndt" : "2016-06-01",
      "mnmo" : "ABCDE00004",
      "mnml" : "www.default-vendor.com",
      "mnmn" : "Vendor",
      "pi" : "436f6e66-6f72-6d61-6e63-6553696d756c"
    }
    ```   
  This means that the client needs to convey the DDI file with oic/p indicating the implemented properties in /oic/p.  
  This IDD file contains the IOTivity IDD with all implemented optional properties, (e.g. only optional property not implemented is "vid")

- generated file
  
## introspection-binaryswitch-actuator.txt

[introspection-binaryswitch-actuator.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/introspection-binaryswitch-actuator.txt)
  
single binary switch, as actuator.

- no "if" on the wire
- manually crafted file

## introspection-binaryswitch-actuator-oic-p.txt

[introspection-binaryswitch-actuator-oic-p.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/introspection-binaryswitch-actuator-oic-p.txt)
  
single binary switch, as actuator.

- includes /oic/p as implemented in IOTivity.
- no "if" on the wire
- manually crafted file
  
## introspection-binaryswitch-actuator-if.txt

[introspection-binaryswitch-actuator-if.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/introspection-binaryswitch-actuator-if.txt)

single binary switch, as actuator.

- "if" on the wire
- manually crafted file

## introspection-binaryswitch-sensor.txt

[introspection-binaryswitch-sensor.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/introspection-binaryswitch-sensor.txt)

single binary switch, as sensor e.g. no update mechanism.

- manually crafted file
  
## introspection-binaryswitch-actuator-sensor.txt

[introspection-binaryswitch-actuator-sensor.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/introspection-binaryswitch-actuator-sensor.txt)

binary switch, one as sensor (no update) and one as actuator.

- manually crafted file
  
## introspection-binaryswitch-2x-actuator.txt

[introspection-binaryswitch-2x-actuator.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/introspection-binaryswitch-2x-actuator.txt)
  
binary switch, two as actuator.

- manually crafted file
  
## binary_switch_if_with_p.txt

[binary_switch_if_with_p.txt](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/binary_switch_if_with_p.txt)
  
binary switch,  as actuator.

- has if property
- has oic/p as used in IOTivity
- manually crafted file
  
## ctt_1 test device

[ctt_1 test device](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/ctt_1.swagger.json)

Note that the responses have the "if" property, as currently being used in the binary switch.
All other optional properties are removed.
The temperature has only Temperature and units as properties.

- Full light device (binary switch, dimming, colour chroma)
  - /binaryswitch
  - /dimming
  - /colourchroma
  - Temperature 2x , sensor and actuator
    - /actuatorthermostat
    - /sensorthermostat

Note this example does __not have__ oic/p as implemented by IOTivity

- manually crafted file

## ctt_2 test device

[ctt_2 test device](https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/introspection-examples/ctt_2.swagger.json)

Note that the responses have the "if" property, as currently being used in the binary switch.
All other optional properties are removed.
The temperature has only Temperature and units as properties.

- Full light device (binary switch, dimming, colour chroma)
  - /binaryswitch
  - /dimming
  - /colourchroma
  - Temperature 2x , sensor and actuator
    - /actuatorthermostat
    - /sensorthermostat

Note this example __has__ oic/p described as implemented by IOTivity

- generated file

# Validation of Swagger2.0 introspection files

validation can be done with the tool chain available [here](https://github.com/WAvdBeek/wb-swagger-node)

Please follow the install instructions as available.

Validation changes wrt swagger2.0 validation:

- allows oneOf/allOf/anyOf constructs in the definition part of the swagger file.

Note that this only validates if the structure/content of the introspection device data file is valid.
It does not check if the contents of the introspection device data actually presents the device itself.
Please use the CTT for that purpose.
