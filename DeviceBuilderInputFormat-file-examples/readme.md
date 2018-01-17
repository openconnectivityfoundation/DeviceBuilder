# DeviceBuilder Input File examples


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


Examples of DeviceBuilderInput Format.


- input-lightdevice.json

  https://github.com/openconnectivityfoundation/DeviceBuilder/blob/master/DeviceBuilderInputFormat-file-examples/input-lightdevice.json
  
 - minimal define resource for oic.d.light 
    - resource type : oic.r.switch.binary
 - added resource type oic.wk.p for introspection generation, since IOTivity has optional implemented properties in this resource.
  
