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


import time
import os
import json
import random
import sys
import argparse
import traceback
from datetime import datetime
from time import gmtime, strftime
import jsonref
from os import listdir
from os.path import isfile, join


if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))



def load_json(filename, my_dir=None):
    """
    load the JSON schema file
    :param filename: filename (with extension)
    :param my_dir: path to the file
    :return: json_dict
    """
    full_path = filename
    if my_dir is not None:
        full_path = os.path.join(my_dir, filename)
    if os.path.isfile(full_path) is False:
        print ("json file does not exist:", full_path)
    linestring = open(full_path, 'r').read()
    json_dict = json.loads(linestring)
    return json_dict


def get_dir_list(dir, ext=None):
    """
    get all files (none recursive) in the specified dir
    :param dir: path to the directory
    :param ext: filter on extension
    :return: list of files (only base_name)
    """
    only_files = [f for f in listdir(dir) if isfile(join(dir, f))]
    # remove .bak files
    new_list = [x for x in only_files if not x.endswith(".bak")]
    if ext is not None:
        cur_list = new_list
        new_list = [x for x in cur_list if x.endswith(ext)]
    return new_list

def eraseElement(d,k , eraseEntry=False):
    """
    erases an the subentries of k in the dict d, if the subkey does not start with an /, e.g. an sub end point
    
    :param d: node tree representing the (partial) raml file
    :param k: decendenants of this key should be deleted (if not the starting with an /)
    :param eraseEntry : also erases the element k.
    """
    print ("eraseElement:", k)
    if isinstance(d, dict):
        found = k in d
        if found:
            print("eraseElement: erased sub elements of key:", k)
            decendants = d[k]
            kill_list = []
            if isinstance(decendants, dict):
                for key, value in decendants.items():
                    print ("eraseElement:", key)
                    if key.startswith("/"):
                        pass
                    else:
                        kill_list.append(key)
                for key in kill_list:
                    decendants.pop(key)
            else:
                d.pop(k)
            if eraseEntry:
                d.pop(k)
                
        else:
            print("eraseElement: Cannot find matching key:", k)
    elif isinstance(d, list):
        remove_index = []
        index = 0
        for list_item in d:
            for key in list_item:
                print("eraseElement: list key:", k)
                if key == k:
                    print("eraseElement: removing key:", k)
                    remove_index.append(index)
            index += 1
        for index in remove_index:
            print("eraseElement: removing index:", index)
            print ("eraseElement: before remove:", d)
            del d[index] 
            print ("eraseElement: after remove:", d)
            
    else:
        print("eraseElement: Not able to delete: ", k)
        
    
    
def find_key(rec_dict, target, depth=0):
    """
    find key "target" in recursive dict
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    try:
        if isinstance(rec_dict, dict):
            for key, value in rec_dict.items():
                if key == target:
                    return rec_dict[key]
            for key, value in rec_dict.items():
                r = find_key(value, target, depth+1)
                if r is not None:
                        return r
        #else:
        #    print ("no dict:", rec_dict)
    except:
        traceback.print_exc()


def find_key_link(rec_dict, target, depth=0):
    """
    find the first key recursively
    also traverse lists (arrays, oneOf,..) but only returns the first occurance
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    if isinstance(rec_dict, dict):
        # direct key
        for key, value in rec_dict.items():
            if key == target:
                return rec_dict[key]
        # key is in array
        rvalues = []
        found = False
        for key, value in rec_dict.items():
            if key in ["oneOf", "allOf", "anyOf"]:
                for val in value:
                    if val == target:
                        return val
                    if isinstance(val, dict):
                        r = find_key_link(val, target, depth+1)
                        if r is not None:
                            found = True
                            # TODO: this should return an array, now it only returns the last found item
                            rvalues = r
        if found:
            return rvalues
        # key is an dict
        for key, value in rec_dict.items():
            r = find_key_link(value, target, depth+1)
            if r is not None:
                return r #[list(r.items())]

                    
def find_resources(filename):
    """
    find the rt values for introspection, uses the ingore list and excludes oic.d and .com. in the rt values.
    :param filename: filename with oic/res response (json)
    :return: array with found [rt, href] values
    """
    rt_ingore_list = ["oic.wk.res", "oic.r.doxm", "oic.r.pstat", "oic.r.acl2", "oic.r.cred", "oic.r.csr", "oic.r.crl", "oic.r.roles", "oic.wk.d", "oic.wk.p", "oic.wk.introspection"]
    json_data = load_json(filename)
    found_rt_values = []
    for entry in json_data[0].get("links"):
        rt = entry.get("rt")
        href = entry.get("href")
        prop_if = entry.get("if")
        #print ("rt (array)", rt, href)
        if rt:
            for rt_value in rt:
                if rt_value not in rt_ingore_list:
                    #print ("rt to handle:", rt_value)
                    if ".com." not in rt_value:
                        if "oic.d." not in rt_value:
                            found_rt_values.append([rt_value, href,prop_if])
                        else:
                            print ("find_resources: device type rt (not handled):", rt_value)
                    else:
                        print ("find_resources: vendor defined rt (not handled):", rt_value)
    return found_rt_values
    
def swagger_rt(json_data):
    """
    get the rt value from teh example
    :param json_data: the swagger file as json struct
    :return: array of arrays of found values e.g. [ [a,b],[a,b] ]
    """
    rt_values = []
    for path, item in json_data["paths"].items():
        #print ("  path:", path)
        try:
            x_example = item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            for rt_value in rt:
                rt_values.append(rt_value)
        except:
            try:
                rt = item["post"]["responses"]["200"]["x-example"]["rt"]
                for rt_value in rt:
                    rt_values.append(rt_value)
            except:
                pass
    return rt_values
    
def find_in_array(value, array_values):
    """
    compare the value against the first element of the 1 level down array.
    :param value: value to compare
    :param array_values: array [[ a, b, c],[a,b,c]]
    :return: True = Found, False is not found
    """
    for array_value in array_values:
        if array_value[0] == value:
            return True
    return False
    
def find_files(dirname, rt_values):
    """
    find the files where the rt values are stored in (as part of the example)
    :param dirname: dir name
    :param rt_values: array of rt values
    :return: array of file names
    """
    file_list = get_dir_list(dirname, ext=".swagger.json")
    print ("find_files: directory:", dirname)
    found_file = []
    for myfile in file_list:
            #print ("  find_files: file :", myfile)
            file_data = load_json(myfile, dirname)
            rt_values_file = swagger_rt(file_data)
            #print ("      rt_values:", rt_file)
            for rt_file in rt_values_file:
                if find_in_array(rt_file, rt_values):
                    found_file.append (myfile)
    return  found_file     
            
    
def remove_for_optimize(json_data):
    """
    remove things from the swagger file
    - license data
    - x-examples in responses
    - x-examples in body defintions (parameters)
    :param json_data: the swagger file
    """
    info_dict = json_data["info"]["license"]
    eraseElement(info_dict,"x-description")
    
    for path, path_item in json_data["paths"].items():
        for method, method_item in path_item.items():
            if isinstance(method_item, dict):
                for response, response_item in method_item.items():
                    if isinstance(response_item, dict):
                        # the responses
                        for responsecode, responsecode_item in response_item.items():
                            eraseElement(responsecode_item,"x-example", eraseEntry=True)
                    if isinstance(response_item, list):
                        # the bodies in the params
                        for entry in response_item:
                            #print ("remove_for_optimize: entry", entry)
                            if isinstance(entry, dict):
                                eraseElement(entry,"x-example", eraseEntry=True)
              
def clear_descriptions(json_data):
    # remove the descriptions in the path
    for path, path_item in json_data["paths"].items():
        for method, method_item in path_item.items():
            if isinstance(method_item, dict):
                description = method_item.get("description")
                if description is not None:
                    method_item["description"] = ""
    # remove the descriptions in the definitions         
    for definition, definition_item in json_data["definitions"].items():
        # definition - values
        for defvalue, defvalue_item in definition_item.items():
            if isinstance(defvalue_item, dict):
                description = method_item.get("description")
                if description is not None:
                    method_item["description"] = ""
                for propvalue, propvalue_item in defvalue_item.items():
                    print ("clear_descriptions", propvalue)
                    description = propvalue_item.get("description")
                    if description is not None:
                        propvalue_item["description"] = ""
                    
              
def update_definition_with_rt(json_data, rt_value_file, rt_values):
    """
    update the defintion section with the default rt value as array
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("update_definition_with_rt", rt_values)
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        print ("update_definition_with_rt", path)
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            print ("update_definition_with_rt schema stuff:", schema, ref)
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path,rt,ref ])
        except:
            pass
    print ("update_definition_with_rt found stuff:", keyvaluepairs)
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_defname = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_defname:
                # found entry
                properties = def_item.get("properties")
                for prop_name, property in properties.items():
                    print ("update_definition_with_rt ", prop_name)
                    if prop_name == "rt":
                        property["default"] = [entry[1]]
                        
                             
              
def update_definition_with_if(json_data, rt_value_file, rt_values):
    """
    update the defintion if enum with the values of rt_values
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("update_definition_with_if", rt_values)
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        #print ("update_definition_with_if", path)
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            print ("update_definition_with_if schema stuff:", schema, ref)
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path,rt,ref, rt_f ])
        except:
            pass
    print ("update_definition_with_if found stuff:", keyvaluepairs)
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_defname = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_defname:
                # found entry
                properties = def_item.get("properties")
                for prop_name, property in properties.items():
                    print ("update_definition_with_if ", prop_name)
                    if prop_name == "if":
                        print (" replacing if with", entry[3][2])
                        property["items"]["enum"] = entry[3][2]
  

def update_path_value(json_data, rt_value_file, rt_values):
    """
    update the path value of the rt from the rt_valuees
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("update_path_value:", rt_values)
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        print ("update_path_value", path)
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path,rt_f[1] ])
        except:
            pass
    path_data = json_data["paths"]
    for replacement in keyvaluepairs:
        if replacement[1] != replacement[0]:
            old_path = replacement[0]
            new_path = replacement[1]
            print ("update_path_value ::", old_path, new_path)
            path_data[new_path]= path_data[old_path]
            path_data.pop(old_path)
        else:
            print("update_path_value: already the same :", replacement)
        
def create_introspection(json_data, rt_value_file, rt_values):
    """
    create the introspection data, e.g. morph json_data.
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print("")
    update_path_value(json_data, rt_value_file, rt_values)
    update_definition_with_rt(json_data, rt_value_file, rt_values)
    update_definition_with_if(json_data, rt_value_file, rt_values)
    
    remove_for_optimize(json_data)
    clear_descriptions(json_data)
    
def remove_from_introspection(json_data, property_list):
    """
    remove the properties (for all resources) from the json data
    :param json_data: the parsed swagger file
    :param property_list: the properties to be removed
    """
    print("remove_from_introspection", property_list)
    if property_list is not None:
        for property in property_list:
            print ("remove_from_introspection:", property)
        def_data = json_data["definitions"]
        for def_name, def_item in def_data.items():
                #full_defname = "#/definitions/" + def_name

                properties = def_item.get("properties")
                #for prop_name, property in properties.items():
                for prop_name in property_list:
                    eraseElement(properties,prop_name, eraseEntry=True)
                    
    
#
#   main of script
#
print ("**************************")
print ("*** DeviceBuilder (v1) ***")
print ("**************************")
parser = argparse.ArgumentParser()

parser.add_argument( "-ver"        , "--verbose"    , help="Execute in verbose mode", action='store_true')

parser.add_argument( "-ocfres"    , "--ocfres"    , default=None,
                     help="ocf/res input",  nargs='?', const="", required=False)
parser.add_argument( "-introspection"    , "--introspection"    , default=None,
                     help="introspection file file name (output)",  nargs='?', const="", required=True)
                     
parser.add_argument( "-resource_dir"    , "--resource_dir"    , default=None,
                     help="resource directory",  nargs='?', const="", required=False)
parser.add_argument('-remove_property', '--remove_property', default=None, nargs='*', help='remove property (--remove_property  value range step precision id) ')

                     
parser.add_argument('-derived', '--derived', default=None, help='derived data model specificaton (--derived XXX) e.g. XXX Property Name in table use "." to ignore the property name setting')

args = parser.parse_args()


print("oic/res file        :  " + str(args.ocfres))
print("introspection (out) : " + str(args.introspection))
print("resource dir        : " + str(args.resource_dir))
print("remove_property     : " + str(args.remove_property))

print("")

try:
    rt_values = find_resources(str(args.ocfres))
    print ("resources:")
    for rt in rt_values:
        print ("  rt     :", rt[0])
        print ("    href :", rt[1])
        print ("    if   :", rt[2])

    files_to_process = find_files(str(args.resource_dir), rt_values)
    for myfile in files_to_process:
        print ("  file :", myfile)
        file_data = load_json(myfile, str(args.resource_dir))
        rt_values_file = swagger_rt(file_data)
        create_introspection( file_data, rt_values_file, rt_values)
        remove_from_introspection(file_data, args.remove_property)
        
        fp = open(str(args.introspection),"w")
        json_string = json.dumps(file_data,indent=2)
        fp.write(json_string)
        fp.close()
        
        
        
    
except:
    print ("error in ", args.ocfres)
    traceback.print_exc()
    pass
