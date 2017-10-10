#############################
#
#    copyright 2016 Open Interconnect Consortium, Inc. All rights reserved.
#    Redistribution and use in source and binary forms, with or without modification,
#    are permitted provided that the following conditions are met:
#    1.  Redistributions of source code must retain the above copyright notice,
#        this list of conditions and the following disclaimer.
#    2.  Redistributions in binary form must reproduce the above copyright notice,
#        this list of conditions and the following disclaimer in the documentation and/or other materials provided
#        with the distribution.
#
#    THIS SOFTWARE IS PROVIDED BY THE OPEN INTERCONNECT CONSORTIUM, INC. "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
#    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE OR
#    WARRANTIES OF NON-INFRINGEMENT, ARE DISCLAIMED. IN NO EVENT SHALL THE OPEN INTERCONNECT CONSORTIUM, INC. OR
#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
#    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
#    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#############################

import pytest
import sys
import os
import json
from . import DeviceBuilder

  
def test_find_files():
    found_files = DeviceBuilder.find_files(".","blah")  
    assert len(found_files) == 0
    
    
def test_load_json():
    data = DeviceBuilder.load_json("../examples/introspection-binaryswitch-sensor.txt")
    data = DeviceBuilder.load_json("introspection-binaryswitch-sensor.txt", my_dir="../examples")
    DeviceBuilder.write_json("blah", data)
       
def test_find_oic_res_resources():
    myargs = DeviceBuilder.MyArgs()
    data = DeviceBuilder.find_oic_res_resources("../test/input_oic_res/oic-res-response-binaryswitch.json", myargs)
    print (data)
    

def test_find_input_resources():
    myargs = DeviceBuilder.MyArgs()
    data = DeviceBuilder.find_input_resources("../test/input_define_device/input-switch.json")
    print (data)
    
def test_find_files():
    myargs = DeviceBuilder.MyArgs()
    myargs.my_print()
    rt_values = DeviceBuilder.find_input_resources("../test/input_define_device/input-switch.json")
    files_to_process = DeviceBuilder.find_files("../test/input_swagger",rt_values)
    for my_file in files_to_process:
        file_data = DeviceBuilder.load_json(my_file, "../test/input_swagger")
        rt_values_file = DeviceBuilder.swagger_rt(file_data)
        print ("  main: rt :", rt_values_file)
        #[rt, href, if, type,[props to be removed], [methods to be removed]]
        mydata = [ [["oic.r.xxx"]   ,"/blahblha", ["oic.if.a"], None, [], [] ]]
        DeviceBuilder.create_introspection(file_data, None, mydata, 0)
        DeviceBuilder.optimize_introspection(file_data)

    file_data1 = DeviceBuilder.load_json("BinarySwitchResURI.swagger.json", "../test/input_swagger")
    mydata1 = [['oic.r.switch.binary', '/binaryswitch', ['oic.if.baseline', 'oic.if.a'], None, ['range', 'step', 'id', 'precision'], None, 'BinarySwitchResURI.swagger.json']]    
    DeviceBuilder.create_introspection(file_data1, None, mydata1, 0)
    DeviceBuilder.optimize_introspection(file_data1)    
        
    file_data2 = DeviceBuilder.load_json("AccelerationResURI.swagger.json", "../test/input_swagger")
    mydata2 = [[ "oic.r.sensor.acceleration"   ,"/blahblha", ["oic.if.a"], "number", ["value", "step"], ["post"] ]]
    DeviceBuilder.create_introspection(file_data2, None, mydata2, 0)
    DeviceBuilder.optimize_introspection(file_data2)  
    DeviceBuilder.merge(file_data1, file_data2, 0)    
    
    file_data3 = DeviceBuilder.load_json("AccelerationResURI.swagger.json", "../test/input_swagger")
    mydata3 = [[ "oic.r.sensor.acceleration"   ,"/AccelerationResURI", ["oic.if.a"], "number", [], [] ]]
    DeviceBuilder.create_introspection(file_data3, None, mydata3, 0)
    DeviceBuilder.optimize_introspection(file_data3)    
    DeviceBuilder.merge(file_data1, file_data3, 1) 
            
    file_data4 = DeviceBuilder.load_json("AirQualityCollectionResURI_if=oic.if.baseline.swagger.json", "../test/input_swagger")
    mydata4 = [[ "oic.r.airqualitycollection","oic.wk.col"   ,"/blahblha", ["oic.if.a"], "number", [], [] ]]
    DeviceBuilder.create_introspection(file_data4, None, mydata4, 0)
    DeviceBuilder.optimize_introspection(file_data4)  
    DeviceBuilder.merge(file_data1, file_data4, 2) 
        
       
def test_merge():
    data1 = DeviceBuilder.load_json("../examples/introspection-binaryswitch-sensor.txt")
    data2 = DeviceBuilder.load_json("introspection-binaryswitch-sensor.txt", my_dir="../examples")
    DeviceBuilder.merge(data1, data2, 0)
    
    data3 = DeviceBuilder.load_json("../test/input_swagger/DimmingResURI.swagger.json")
    DeviceBuilder.merge(data1, data3, 1)
    data4 = DeviceBuilder.load_json("../test/input_swagger/ColourChromaResURI.swagger.json")
    DeviceBuilder.merge(data1, data4, 2)

    
    
def test_main_app():
    myargs = DeviceBuilder.MyArgs()
    myargs.resource_dir = "../test/input_swagger/"
    data1 = DeviceBuilder.main_app(myargs, "introspection")
    
    myargs = DeviceBuilder.MyArgs()
    myargs.resource_dir = "../test/input_swagger/"
    myargs.input = "../test/input_define_device/input-switch.json"
    data1 = DeviceBuilder.main_app(myargs, "introspection")
    
    myargs = DeviceBuilder.MyArgs()
    myargs.resource_dir = "../test/input_swagger/"
    myargs.ocfres = "../test/input_oic_res/oic-res-response-testdevice.json"
    myargs.out = "../test/blah"
    myargs.intermediate_files = True
    data1 = DeviceBuilder.main_app(myargs, "introspection")