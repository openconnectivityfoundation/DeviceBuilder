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


import os
import json
import sys
import argparse
import traceback
from os import listdir
from os.path import isfile, join

if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))


                    
index_rt     = 0
index_href   = 1
index_if     = 2
index_type   = 3
index_prop   = 4
index_method = 5 
                    

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
    #print ("eraseElement:", k)
    if isinstance(d, dict):
        found = k in d
        if found:
            decendants = d[k]
            kill_list = []
            if isinstance(decendants, dict):
                for key, value in decendants.items():
                    if key.startswith("/"):
                        pass
                    else:
                        kill_list.append(key)
                for key in kill_list:
                    decendants.pop(key)
            else:
                d.pop(k)
            if eraseEntry:
                try:
                    d.pop(k)
                except:
                    print("eraseElement : could not delete:", k)
                
        else:
            print("eraseElement: Cannot find matching key:", k)
    elif isinstance(d, list):
        remove_index = []
        index = 0
        for list_item in d:
            for key in list_item:
                if key == k:
                    remove_index.append(index)
            index += 1
        for index in remove_index:
            del d[index] 
            
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


def find_key_value(rec_dict, searchkey, target, depth=0):
    """
    find the first key with value "target" recursively
    also traverse lists (arrays, oneOf,..) but only returns the first occurance
    returns the dict that contains the search key.
    so the returned dict can be updated by dict[searchkey] = xxx
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param searchkey: target key to search for
    :param target: target value that belongs to key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    #print ("")
    #print ("find_key_value:", searchkey, target, depth)
    #print ("find_key_value:", rec_dict)
    if isinstance(rec_dict, dict):
        # direct key
        for key, value in rec_dict.items():
            if key == searchkey and value == target:
                #print ("  find_key_value found!: find_key_value:", rec_dict)
                return rec_dict
            elif isinstance(value, dict):
                r = find_key_value(value, searchkey, target, depth+1)
                if r is not None:
                    return r
            elif isinstance(value, list):
                for entry in value:
                    if isinstance(entry, dict):
                        r = find_key_value(entry, searchkey, target, depth+1)
                        if r is not None:
                            return r
                            
                            
                            
def find_key_and_clean(rec_dict, searchkey, depth=0):
    """
    find all keys and clean the value, e.g. make the value an empty string
    also traverse lists (arrays, oneOf,..) 
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param searchkey: target key to search in the dict and to be updated
    :param depth: depth of the search (recursion)
    :return:
    """
    #print ("")
    #print ("find_key_and_clean:", searchkey, target, depth)
    #print ("find_key_and_clean:", rec_dict)
    if isinstance(rec_dict, dict):
        # direct key
        for key, value in rec_dict.items():
            if key == searchkey:
                rec_dict[key] = ""
            elif isinstance(value, dict):
                r = find_key_and_clean(value, searchkey, depth+1)
            elif isinstance(value, list):
                for entry in value:
                    if isinstance(entry, dict):
                        r = find_key_and_clean(entry, searchkey, depth+1)
           
def find_oic_res_resources(filename, args):
    """
    find the rt values for introspection, uses the ingore list and excludes oic.d and .com. in the rt values.
    :param filename: filename with oic/res response (json)
    :return: array with found [rt, href, if, type,[props to be removed], [methods to be removed]] values
    """
    args_type = args.type
    args_props = args.remove_property
    
    #args_ignore_prop = args.
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
                            found_rt_values.append([rt_value, href, prop_if, args_type, args_props, None])
                        else:
                            print ("find_resources: device type rt (not handled):", rt_value)
                    else:
                        print ("find_resources: vendor defined rt (not handled):", rt_value)
    return found_rt_values
    
    
                    
def find_input_resources(filename):
    """
    find the rt values for introspection, uses the ingore list and excludes oic.d and .com. in the rt values.
    :param filename: filename with oic/res response (json)
    :return: array with found [rt, href, if, type,[props to be removed], [methods to be removed]] values
    """
    rt_ingore_list = ["oic.wk.res", "oic.r.doxm", "oic.r.pstat", "oic.r.acl2", "oic.r.cred", "oic.r.csr", "oic.r.crl", "oic.r.roles", "oic.wk.d", "oic.wk.p", "oic.wk.introspection"]
    json_data = load_json(filename)
    found_rt_values = []
    for entry in json_data:
        rt = entry.get("rt")
        href = entry.get("path")
        prop_if = entry.get("if")
        type = entry.get("override_type")
        methods = entry.get("remove_methods")
        props = entry.get("remove_properties")
        if rt:
            for rt_value in rt:
                if rt_value not in rt_ingore_list:
                    #print ("rt to handle:", rt_value)
                    if ".com." not in rt_value:
                        if "oic.d." not in rt_value:
                            found_rt_values.append([rt_value, href, prop_if, type, props, methods])
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
    :return: array of file names, no duplicates...
    """
    file_list = get_dir_list(dirname, ext=".swagger.json")
    print ("find_files: directory:", dirname)
    found_file = []
    for myfile in file_list:
            #print ("  find_files: file :", myfile)
            file_data = load_json(myfile, dirname)
            rt_values_file = swagger_rt(file_data)
            #print ("      rt_values:", rt_values_file)
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
    """
    clear the descriptions e.g. set them on empty string e.g. ""
    :param json_data: the parsed swagger file
    """
    # remove the descriptions in the path
    #for path, path_item in json_data["paths"].items():
    #    for method, method_item in path_item.items():
    #        if isinstance(method_item, dict):
    #            description = method_item.get("description")
    #            if description is not None:
    #                method_item["description"] = ""
    # remove the descriptions in the definitions         
    #for definition, definition_item in json_data["definitions"].items():
    #    # definition - values
    #    for defvalue, defvalue_item in definition_item.items():
    #        if isinstance(defvalue_item, dict):
    #            description = method_item.get("description")
    #            if description is not None:
    #                method_item["description"] = ""
    #            for propvalue, propvalue_item in defvalue_item.items():
    #                print ("clear_descriptions", propvalue)
    #                description = propvalue_item.get("description")
    #                if description is not None:
    #                    propvalue_item["description"] = ""
    find_key_and_clean(json_data,"description")                    
                    
              
def update_definition_with_rt(json_data, rt_value_file, rt_values):
    """
    update the defintion section with the default rt value as array
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("update_definition_with_rt")
    for rt_value in rt_values:
        print ("  rt:",rt_value[index_rt])
        
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            #print ("update_definition_with_rt schema stuff:", schema, ref)
            if find_in_array(rt[index_rt], rt_values):
                for rt_f in rt_values:
                    if rt_f[index_rt] == rt[index_rt]:
                        keyvaluepairs.append([path,rt,ref ])
        except:
            pass
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_defname = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[0] == full_defname:
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
    print ("update_definition_with_if")
    for rt_value in rt_values:
        print ("  href:",rt_value[index_href], " if:",rt_value[index_if])
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            #print ("update_definition_with_if schema stuff:", schema, ref)
            if find_in_array(rt[index_rt], rt_values):
                for rt_f in rt_values:
                    if rt_f[index_rt] == rt[index_rt]:
                        keyvaluepairs.append([path,rt,ref, rt_f ])
        except:
            pass
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_defname = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_defname:
                # found entry
                properties = def_item.get("properties")
                for prop_name, property in properties.items():
                    if prop_name == "if":
                        print (" replacing if with", entry[3][index_if])
                        property["items"]["enum"] = entry[3][index_if]
                        
                        
def update_parameters_with_if(json_data, rt_value_file, rt_values):
    """
    update the defintion if enum with the values of rt_values
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("update_parameters_with_if")
    for rt_value in rt_values:
        print ("  href:",rt_value[index_href], " if:",rt_value[index_if])
    #keyvaluepairs =[]
    #for path, path_item in json_data["paths"].items():
    #    try:
    #        x_example = path_item["get"]["responses"]["200"]["x-example"]
    #        rt = x_example.get("rt")
    #        schema = path_item["get"]["responses"]["200"]["schema"]
    #        ref = schema["$ref"]
    #        #print ("update_parameters_with_if schema stuff:", schema, ref)
    #        if find_in_array(rt[index_rt], rt_values):
    #            for rt_f in rt_values:
    #                if rt_f[index_rt] == rt[index_rt]:
    #                    keyvaluepairs.append([path,rt,ref, rt_f ])
    #    except:
    #        pass
    param_data = json_data["parameters"]
    for param_name, param_item in param_data.items():
        print ("update_parameters_with_if", param_name)
        for prop_name, prop in param_item.items():
            if prop_name == "name" and prop == "if":
                print (" replacing if with", rt_value[index_if])
                param_item["enum"] = rt_value[index_if]


def update_definition_with_type(json_data, rt_value_file, rt_values):
    """
    update the defintion type values, e.g. override the type in an oneof construct
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    :param type: string, json type to use 
    """
    print ("update_definition_with_type")
    for rt_value in rt_values:
        print ("  href:",rt_value[index_href], " type:",rt_value[index_type])
        
    supported_types = ["integer", "number", "string", "boolean"]      
    # array of arrays of path, r, ref, rt_values
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path,rt,ref, rt_f ])
        except:
            pass  
        try:
            x_example = path_item["post"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["post"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path,rt,ref, rt_f ])
        except:
            pass  
            
    
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_defname = "#/definitions/" + def_name        
        for entry in keyvaluepairs:
            if entry[2] == full_defname:
                properties = def_item.get("properties")
                type = "integer"
                type = entry[3][index_type]
                if entry[3][index_type] not in supported_types:
                    if type is not None:
                        print (" *** ERROR type is not valid:", entry[3][index_type], " supported types:", supported_types)
                else:
                    type = entry[3][index_type]
                    if properties is not None:
                        for prop_name, property in properties.items():
                            one_off = property.get("anyOf")
                            if one_off is not None:
                                print ("update_definition_with_type ", prop_name)
                                property.pop("anyOf")
                                property["type"] = type
                            if prop_name == "range":
                                one_off = property["items"].get("anyOf")
                                if one_off is not None:
                                    print ("update_definition_with_type ", prop_name)
                                    property["items"].pop("anyOf")
                                    property["items"]["type"] = type
  

def remove_definition_properties(json_data, rt_value_file, rt_values):
    """
    remove the defintion properties as indicated in the values of rt_values
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("remove_definition_properties")
    for rt_value in rt_values:
        print ("   rt:",rt_value[index_rt], " prop:",rt_value[index_prop])
    
    # array of arrays of path, r, ref, rt_values
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        found_rt = False
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path, rt, ref, rt_f ])
                        found_rt = True
        except:
            pass
        try:
            schema = path_item["post"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if found_rt == True:
                keyvaluepairs.append([path, rt, ref, rt_f ])
        except:
            pass    
                        
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_defname = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_defname:
                print ("  definition:",full_defname)
                # found entry
                properties = def_item.get("properties")
                remove_list = entry[3][index_prop]
                if remove_list is not None:
                    for prop_name in remove_list:
                        eraseElement(properties,prop_name, eraseEntry=True)
  
  

def remove_path_method(json_data, rt_value_file, rt_values):
    """
    remove the method on an path
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("remove_path_method")
    for rt_value in rt_values:
        print ("   href:",rt_value[index_href], " method:",rt_value[index_method])
    
    # array of arrays of path, r, ref, rt_values
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        for rt_value in rt_values:
            if rt_value[index_href] == path:
                methods = rt_value[index_method]
                if methods is not None:
                    for method in methods:
                        eraseElement(path_item,method, eraseEntry=True)
            
            
def update_path_value(json_data, rt_value_file, rt_values):
    """
    update the path value of the rt from the rt_valuees
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("update_path_value:")
    for rt_value in rt_values:
        print ("   rt:",rt_value[index_rt], " href:",rt_value[index_href])

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
        
def create_introspection(json_data, rt_value_file, rt_values, index):
    """
    create the introspection data, e.g. morph json_data.
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values
    """
    print ("")
    #print("create_introspection index:", index)
    rt_single = [rt_values[index]]
    #if rt_single is not None:
    print("create_introspection index:", index, rt_single[0][index_href])
    
    update_path_value(json_data, rt_value_file, rt_single)
    update_definition_with_rt(json_data, rt_value_file, rt_single)
    update_definition_with_if(json_data, rt_value_file, rt_single)
    update_parameters_with_if(json_data, rt_value_file, rt_single)
    update_definition_with_type(json_data, rt_value_file, rt_single)
    remove_definition_properties(json_data, rt_value_file, rt_single)
    remove_path_method(json_data, rt_value_file, rt_single)
    
    
def optimize_introspection(json_data):    
    """
    optimize the json
    - clear the descriptions (e.g. remove the text only)
    :param json_data: the parsed swagger file
    """
    remove_for_optimize(json_data)
    clear_descriptions(json_data)
           

def merge(merge_data, file_data, index):
    """
    merge the file_data (paths and defintions) into merge_data
    :param merge_data: the data that will be used to merge into
    :param file_data: the data to merge
    :param index: index counter of the index that is being merged
    """
    local_index = 0
    for parameter, parameter_item in file_data["parameters"].items():
        data = merge_data["parameters"].get(parameter)
        if data is None:
            merge_data["parameters"][parameter] = parameter_item
        else:
            print ("merge: parameter exist:", parameter)
            new_parameter = parameter + str(index) + str(local_index)
            local_index = local_index + 1
            print ("merge: parameter exist:", parameter, " adding as:", new_parameter)
            merge_data["parameters"][new_parameter] = parameter_item
            # fix the path data
            search_parameter = "#/parameters/"+parameter
            my_dict = find_key_value(file_data["paths"], "$ref", search_parameter)
            print (" -->",my_dict)
            my_dict["$ref"] = "#/parameters/"+new_parameter

    for definition, definiton_item in file_data["definitions"].items():
        data = merge_data["definitions"].get(definition)
        if data is None:
            merge_data["definitions"][definition] = definiton_item
        else:
            print ("merge: definition exist:", definition)
            new_definition = definition + str(local_index) + str(local_index)
            local_index = local_index + 1
            print ("merge: parameter exist:", definition, " adding as:", new_definition)
            merge_data["definitions"][new_definition] = definiton_item
            # fix the definition data
            search_definition = "#/definitions/" + definition
            my_dict = find_key_value(file_data["paths"], "$ref", search_definition)
            print (" -->",my_dict)
            my_dict["$ref"] = "#/definitions/" +new_definition
            # try again for the other method
            my_dict = find_key_value(file_data["paths"], "$ref", search_definition)
            if my_dict is not None:
                my_dict["$ref"] = "#/definitions/" + new_definition
    
    for path, path_item in file_data["paths"].items():
        merge_data["paths"][path] = path_item
    
    
def main_app(args, generation_type):  

    if args.ocfres is not None: 
        rt_values = find_oic_res_resources(str(args.ocfres), args)
    elif args.input is not None:
            rt_values = find_input_resources(str(args.input))
    else:
        print (" no oic/res or input format given" )
        
    write_intermediate=False
    if args.intermediate_files is not None and args.intermediate_files == True:    
        write_intermediate=True
        
    print ("handling resources (overview):")
    files_to_process = find_files(str(args.resource_dir), rt_values)
    print ("processing files:",files_to_process )
    
    index = 0
    merged_data = None
    for myfile in files_to_process:
        print ("")
        print ("  main: File :", myfile)
        file_data = load_json(myfile, str(args.resource_dir))
        rt_values_file = swagger_rt(file_data)
        print ("  main: rt :", rt_values_file)
        for rt in rt_values:
            if rt[0] == rt_values_file[0]:
                rt.append(myfile)
                
    for rt in rt_values:
        print ("  rt                 :", rt[0])
        print ("    href             :", rt[1])
        print ("    if               :", rt[2])
        print ("    type (replace)   :", rt[3])
        print ("    props (remove)   :", rt[4])
        print ("    methods (remove) :", rt[5])
        if len(rt) > 6:
            print ("    basefile         :", rt[6])
        else:
            ("    no base file found! : ignored")
    print(" ")   
        
    index = 0
    for rt in rt_values:
        if len(rt) > 6:
            file_data = load_json(rt[6], str(args.resource_dir))
            rt_values_file = swagger_rt(file_data)
            create_introspection( file_data, rt_values_file, rt_values, index)
            
            if "introspection" == generation_type:
                print ("optimize for introspection..")
                optimize_introspection(file_data)
            
            if write_intermediate:
                file_to_write = str(args.out) + "_" + generation_type + "_" + myfile
                fp = open(str(file_to_write),"w")
                json_string = json.dumps(file_data,indent=2, sort_keys=True)
                fp.write(json_string)
                fp.close()
            
            if merged_data is None:
                merged_data = file_data
            else:
                merge(merged_data, file_data, index)
        index = index + 1
        
    if merged_data is not None: 
        file_to_write = str(args.out) + "_" + generation_type + "_" + "merged.swagger.json"
        fp = open(str(file_to_write),"w")
        json_string = json.dumps(merged_data,indent=2, sort_keys=True)
        fp.write(json_string)
        fp.close()    
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
parser.add_argument( "-input"    , "--input"    , default=None,
                     help="device builder input format",  nargs='?', const="", required=False)
parser.add_argument( "-out"    , "--out"    , default=None,
                     help="output dir + prefix e.g. (../mydir/generated1)",  nargs='?', const="", required=True)

parser.add_argument( "-intermediate_files"    , "--intermediate_files"    , default=False,
                     help="write intermediate files", required=False)      
                     
parser.add_argument( "-resource_dir"    , "--resource_dir"    , default=None,
                     help="resource directory",  nargs='?', const="", required=False)
parser.add_argument('-remove_property', '--remove_property', default=None, nargs='*', help='remove property (--remove_property  value range step precision id) ')
parser.add_argument('-type', '--type', default=None, nargs='?', help='type of the value (or renamed value) (--type  integer number) ')

 
args = parser.parse_args()

print("out                 : " + str(args.out))
print("resource dir        : " + str(args.resource_dir))
#print("")
print("oic/res file        : " + str(args.ocfres))
print("input file          : " + str(args.input))
#print("")
print("remove_property     : " + str(args.remove_property))
print("type                : " + str(args.type))
print("intermediate files  : " + str(args.intermediate_files))
print("")

try:
    print ("== INTROSPECTION ==")
    main_app(args, "introspection")
    
    print ("== CODE GENERATION ==")
    main_app(args, "codegeneration")
        
    
except:
    print ("error in ", args.ocfres)
    traceback.print_exc()
    pass
