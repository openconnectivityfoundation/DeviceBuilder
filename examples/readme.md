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
