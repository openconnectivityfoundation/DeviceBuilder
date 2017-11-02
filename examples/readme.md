# Introspection example files

Examples of introspection files


- introspection-empty.txt

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/ctt_1.swagger.json
  
  an swagger2.0 file with no paths and no defintions
  can be used if no introspection data is needed.
  - manually crafted
  
- introspection-client-iotivity-oic-p

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/introspection-client-iotivity-oic-p.txt

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
  - generated
  
- introspection-binaryswitch-acutator.txt

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/introspection-binaryswitch-actuator.txt
  
  single binary switch, as actuator.
  - no "if" on the wire
  - manually crafted

- introspection-binaryswitch-acutator-if.txt

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/introspection-binaryswitch-actuator-if.txt

  single binary switch, as actuator.
  - "if" on the wire
  - manually crafted

- introspection-binaryswitch-sensor.txt

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/introspection-binaryswitch-sensor.txt

  single binary switch, as sensor e.g. no update mechanism. 
  - manually crafted
  
 
- introspection-binaryswitch-actuator-sensor.txt

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/introspection-binaryswitch-actuator-sensor.txt

  binary switch, one as sensor (no update) and one as actuator.
  - manually crafted
  
- introspection-binaryswitch-2x-actuator.txt

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/introspection-binaryswitch-2x-actuator.txt
  
  binary switch, two as actuator.
  - manually crafted
  
  
- ctt_1 test device

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/examples/ctt_1.swagger.json

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
        
   Note this example does not have oic/p as implemented by IOTivity
   - manually crafted


        
