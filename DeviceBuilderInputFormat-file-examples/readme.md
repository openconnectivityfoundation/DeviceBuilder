# DeviceBuilder Input File examples

The DeviceBuilder Input format is to list all resources that needs to be included in the device that will make up the application.
E.g. the resources that will be sensor/actuators/etc. that make up the functionality of the device.
The format supports additional information per resource to that the OCF data model can be changed.
The changes that are allowed are limited, the result still needs to be OCF compliant. So optional properties, methods etc can be removed from the resource.
The property that is being used to find the resource is the rt value, the rt value being used as lookup towards the oneIOTa/Core github repos where the resource will be pulled from.
To use the properties to change the resource one needs to know what the resource implements. 

The DeviceBuilder input format is an json array that define each resource separately
the following properties are defined:
  -  "path" : the path to be used in the implementation
        - required
        - type string
        - must start with "/"
        - must be unique over all resources
  -  "rt"   : the resource type that needs to be populated
        - required
        - array of strings
  -  "if"   : the interfaces that needs to be supported
        - required
        - array of strings
        - order is maintained, hence the first listed interface is the default interface
  -  "remove_properties" : properties that will be removed
        - optional
        - array of strings, 
        - example: "remove_properties : ["range", "step" "value"]
  -  "remove_methods" :  methods to remove from the implementation[]
        - optional
        - array of strings
        - example: "remove_methods" : ["post"]
  -  "override_type" :  override the type of the property value,  
        - optional
        - string, optional, e.g. can be omitted,
        - example  "override_type" :  "integer" 
        - typical values "integer", "number" or "string"

The advantage of this format that it is:
- instructions per resource instance to change things.
- format may change by adding new fields to introduce new features to the tool


Examples of DeviceBuilderInput Format:


- input-lightdevice.json
    The minimal light device, implementing only on/off.

    https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/DeviceBuilderInputFormat-file-examples/input-lightdevice.json
  
    - minimal define resource for oic.d.light 
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
              "remove_properties" : [ "n", "range", "value", "step", "precision", "vid"  ]
            }
        ]

        ```

  
  
  
- input-lightdevice-dimming.json
    The light device implementing on/off and dimming.

    https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/DeviceBuilderInputFormat-file-examples/input-lightdevice-dimming.json
  
    - resource list for oic.d.light 
        - resource type : oic.r.switch.binary
        - resource type : oic.r.light.dimming
    - added resource type oic.wk.p for introspection generation, since IOTivity has optional implemented properties in this resource.