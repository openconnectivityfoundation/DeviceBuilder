This folder contains the reference files of the test cases.
There is 1 specific test case that generates the Introspection Device 




# IOTivity 
IOTivity response of /oic/p, which also includes optional properties

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

The full schema :
https://github.com/openconnectivityfoundation/core/blob/master/schemas/oic.wk.p-schema.json
contains the following optional (besides the core common properties) properties:
- mnml
- mndt
- mnpv
- mnos
- mnhw
- mnfv
- mnsl
- st
- vid (only one not in IOTivity)


This means that the oic.wk.p resource needs to be in the IDD.

section of the DeviceBuilder input file:
```
    {
      "path" : "/oic/p",
      "rt"   : [ "oic.wk.p" ],
      "if"   : ["oic.if.baseline", "oic.if.r" ],
      "remove_properties" : [ "n", "range", "value", "step", "precision", "vid" ]
    }
```