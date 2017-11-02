# Introspection example files

These files are manually crafted.

- introspection-empty.txt

  an swagger2.0 file with no paths and no defintions
  can be used if no introspection data is needed.
  
- introspection-binaryswitch-acutator.txt

  single binary switch, as actuator.
  - no "if" on the wire

- introspection-binaryswitch-acutator-if.txt

  single binary switch, as actuator.
  - "if" on the wire

- introspection-binaryswitch-sensor.txt

  single binary switch, as sensor e.g. no update mechanism.
  
 
- introspection-binaryswitch-actuator-sensor.txt

  binary switch, one as sensor (no update) and one as actuator.
  
- introspection-binaryswitch-2x-actuator.txt

  binary switch, two as actuator.
  
  
- ctt_1 test device

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

- introspection-client-iotivity-oic-p

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
        
