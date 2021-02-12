#############################
#
#    copyright 2016-2021 Open Interconnect Consortium, Inc. All rights reserved.
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
import requests
import wget
#from  collections import OrderedDict

try: 
    from deepdiff import DeepDiff
except:
    print("missing DeepDiff:")
    print ("Trying to Install required module: DeepDiff ")
    os.system('python3 -m pip install deepdiff')
import deepdiff
from deepdiff import grep

if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))

index_rt = 0
index_href = 1
index_if = 2
index_type = 3
index_prop = 4
index_method = 5 
index_rts = 6 
index_add_props = 7
index_remove_query = 8
index_file = 9  # always the last one

VERBOSE=False

class MyArgs(object):
    def __init__(self):
        self.type = None
        self.out = None
        self.resource_dir = None
        self.ocfres = None
        self.input = None
        self.title = None
        self.remove_property = []
        self.intermediate_files = False
    
    def my_print(self):
        print("out                 : " + str(self.out))
        print("resource dir        : " + str(self.resource_dir))
        # print("")
        print("oic/res file        : " + str(self.ocfres))
        print("input file          : " + str(self.input))
        # print("")
        print("remove_property     : " + str(self.remove_property))
        print("type                : " + str(self.type))
        print("title               : " + str(self.title))
        print("intermediate files  : " + str(self.intermediate_files))
        print("")

def load_json(filename, my_dir=None):
    """
    load the JSON file
    :param filename: filename (with extension)
    :param my_dir: path to the file
    :return: json_dict
    """
    print ("load_json: ",filename)
    full_path = filename
    if my_dir is not None:
        full_path = os.path.join(my_dir, filename)
    if filename.startswith("http"):
        r = requests.get(filename)
        return r.json()
    else:
        if os.path.isfile(full_path) is False:
            print ("json file does not exist:", full_path)
        linestring = open(full_path, 'r').read()
    #json_dict = json.loads(linestring, object_pairs_hook=OrderedDict)
    json_dict = json.loads(linestring)
    return json_dict

    
def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]
    
def write_json(filename, file_data): 
    """
    write the JSON  file
    :param filename: filename (with extension)
    :param file_data: json data to be written to file
    """ 
    fp = open(filename, "w")
    json_string = json.dumps(file_data, indent=2, sort_keys=True)
    fp.write(json_string)
    fp.close()

    
def get_dir_list(my_dir, ext=None):
    """
    get all files (none recursive) in the specified dir
    :param my_dir: path to the directory
    :param ext: filter on extension
    :return: list of files (only base_name)
    """
    only_files = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    # remove .bak files
    new_list = [x for x in only_files if not x.endswith(".bak")]
    if ext is not None:
        cur_list = new_list
        new_list = [x for x in cur_list if x.endswith(ext)]
    return new_list


def erase_element(d, k, erase_entry=False):
    """
    erases an the sub entries of k in the dict d, if the subkey does not start with an /, e.g. an sub end point
    
    :param d: node tree representing the (partial) json file
    :param k: descendants of this key should be deleted (if not the starting with an /)
    :param erase_entry : also erases the element k.
    """
    if isinstance(d, dict):
        found = k in d
        if found:
            descendant = d[k]
            kill_list = []
            if isinstance(descendant, dict):
                for key, value in descendant.items():
                    if key.startswith("/"):
                        pass
                    else:
                        kill_list.append(key)
                for key in kill_list:
                    if VERBOSE:
                        print("erase_element: pop:", key)
                    descendant.pop(key)
            else:
                if VERBOSE:
                    print("erase_element: pop:", key)
                d.pop(k)
            if erase_entry:
                try:
                    d.pop(k)
                except:
                    print("erase_element : could not delete:", k)
                
        else:
            print("erase_element: Cannot find matching key:", k)
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
        print("erase_element: Not able to delete: ", k)
        

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
    if isinstance(rec_dict, dict):
        # direct key
        for key, value in rec_dict.items():
            if key == searchkey and value == target:
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
        for key,value in rec_dict.items():
            if key == target:
                return rec_dict[key]
        # key is in array
        rvalues = []
        found = False
        for key,value in rec_dict.items():
            if key in ["oneOf", "allOf", "anyOf"]:
                for val in value:
                    #print ("xxx", depth, key, val)
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
        for key,value in rec_dict.items():
            r = find_key_link(value, target, depth+1)
            if r is not None:
                return r #[list(r.items())]
                
def find_target_value(rec_dict, target, depth=0):
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
        for key,value in rec_dict.items():
            if key == target:
                return rec_dict[key]
        # key is in array
        rvalues = []
        found = False
        for key,value in rec_dict.items():
            if key in ["oneOf", "allOf", "anyOf"]:
                for val in value:
                    #print ("xxx", depth, key, val)
                    if val == target:
                        return val
                    if isinstance(val, dict):
                        r = find_target_value(val, target, depth+1)
                        if r is not None:
                            if not r.startswith("#/definitions/"):
                                found = True
                                # TODO: this should return an array, now it only returns the last found item
                                rvalues = r
        if found:
            return rvalues
        # key is an dict
        for key,value in rec_dict.items():
            r = find_target_value(value, target, depth+1)
            if r is not None:
                if not r.startswith("#/definitions/"):
                    return r #[list(r.items())]

def find_key(rec_dict, target, depth=0):
    """
    find key "target" in recursive dict
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    :return:
    """
    #print ("find key", target);
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
        print("xxxxx")
        traceback.print_exc()
        
def get_dict_recursively(search_dict, field):
    """
    Takes a dict with nested lists and dicts,
    and searches all dicts for a key of the field
    provided.
    :param search_dict: dict to search
    :param field: key to search
    """
    fields_found = []

    try:
        for key, value in search_dict.items():

            if key == field:
                fields_found.append([key, value, search_dict])

            elif isinstance(value, dict):
                results = get_dict_recursively(value, field)
                for result in results:
                    fields_found.append(result)

            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, dict):
                        more_results = get_dict_recursively(item, field)
                        for another_result in more_results:
                            fields_found.append(another_result)
    except:
        traceback.print_exc()

    return fields_found  
        
                            
def find_key_and_clean(rec_dict, search_key, depth=0):
    """
    find all keys and clean the value, e.g. make the value an empty string
    also traverse lists (arrays, oneOf,..) 
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param search_key: target key to search in the dict and to be updated
    :param depth: depth of the search (recursion)
    :return:
    """
    if isinstance(rec_dict, dict):
        # direct key
        for key, value in rec_dict.items():
            if key == search_key:
                rec_dict[key] = ""
            elif isinstance(value, dict):
                find_key_and_clean(value, search_key, depth+1)
            elif isinstance(value, list):
                for entry in value:
                    if isinstance(entry, dict):
                        find_key_and_clean(entry, search_key, depth+1)


def find_oic_res_resources(filename, my_args):
    """
    find the rt values for introspection, uses the ingore list and excludes oic.d and .com. in the rt values.
    :param filename: filename with oic/res response (json)
    :param my_args: argument object
    :return: array with found [rt, href, if, type,[props to be removed], [methods to be removed]] values
    """
    args_type = my_args.type
    args_props = my_args.remove_property
    rt_ingore_list = ["oic.wk.res", "oic.r.doxm", "oic.r.pstat", "oic.r.acl2", "oic.r.cred",
                      "oic.r.csr", "oic.r.crl", "oic.r.roles", "oic.wk.d", "oic.wk.p", "oic.wk.introspection", "oic.wk.rd"]

    json_data = load_json(filename)
    found_rt_values = []
    for entry in json_data[0].get("links"):
        rt = entry.get("rt")
        href = entry.get("href")
        prop_if = entry.get("if")
        if rt:
            for rt_value in rt:
                if rt_value not in rt_ingore_list:
                    if ".com." not in rt_value:
                        if "oic.d." not in rt_value:
                            found_rt_values.append([rt_value, href, prop_if, args_type, args_props, None, None])
                        else:
                            print ("find_resources: device type rt (not handled):", rt_value)
                    else:
                        print ("find_resources: vendor defined rt (not handled):", rt_value)
    return found_rt_values

                    
def find_input_resources(filename):
    """
    find the rt values for introspection, uses the ingore list and excludes oic.d and .com. in the rt values.
    :param filename: filename with oic/res response (json)
    :return: array with found 
    [rt, href, if, type,[props to be removed], [methods to be removed], [rts enum values], [new prop (names)], remove query param names] values
    """
    rt_ingore_list = ["oic.wk.res",  "oic.wk.introspection"]
    json_data = load_json(filename)
    found_rt_values = []
    for entry in json_data:
        rt = entry.get("rt")
        href = entry.get("path")
        prop_if = entry.get("if")
        my_type = entry.get("override_type")
        methods = entry.get("remove_methods")
        props = entry.get("remove_properties")
        query_params = entry.get("remove_queryparm")
        rts = entry.get("collection_rts_enum")
        new_props = entry.get("additional_properties")
        if rt:
            for rt_value in rt:
                if rt_value not in rt_ingore_list:
                    if ".com." not in rt_value:
                        #if "oic." not in rt_value:
                        found_rt_values.append([rt_value, href, prop_if, my_type, props, methods, rts, new_props, query_params])
                        #else:
                        #    print ("find_resources: device type rt (not handled):", rt_value)
                    else:
                        print ("find_resources: vendor defined rt (not handled):", rt_value)
    return found_rt_values

def db_get_key(input_json_data, dict_path):
    """
    find key from input json
    dict_path defined as '#/something/something/somethingelse
    
    """
    #print("db_get_key", dict_path)
    my_data = input_json_data
    
    if isinstance(dict_path,str) == False:
        return []
    
    my_path_segments = dict_path.split("/")
    for path_seg in my_path_segments:
        #print (path_seg)
        if path_seg != "#":
            if isinstance(my_data, dict):
                if path_seg in my_data:
                    my_data = my_data[path_seg]
                else:
                   #print("db_get_key key not in my_data not a dict", path_seg, my_data)
                   return []
            else:
                #print("db_get_key my_data not a dict", my_data)
                return []
    return my_data
    
    

def db_remove_key(input_json_data, dict_path):
    """
    remove key from input json
    dict_path defined as '#/something/something/somethingelse
    
    """
    #print("db_remove_key", dict_path)
    my_data = input_json_data
    
    my_path_segments = dict_path.split("/")
    last_entry = my_path_segments[-1]
    #print (last_entry)
    my_path_segments.pop()
    #print (my_path_segments)
    
    for path_seg in my_path_segments:
        #print (path_seg)
        if path_seg != "#":
            if isinstance(my_data, dict):
                if path_seg in my_data:
                    #if my_data[path_seg].get(
                    my_data = my_data[path_seg]
                    #if my_data 
    my_data.pop(last_entry)



def swagger_rt(json_data):
    """
    get the rt value from the example
    :param json_data: the swagger file as json struct
    :return: array of arrays of found values e.g. [ [a,b],[a,b] ]
    """
    rt_values = []
    for path, item in json_data["paths"].items():
        #print ("swagger_rt ", path)
        rt = db_get_key(item, "get/responses/200/x-example/rt")
        if isinstance(rt, list) and len(rt) > 0:
            for rt_value in rt:
               rt_values.append(rt_value)
        else:
            rt = db_get_key(item, "post/responses/200/x-example/rt")
            if isinstance(rt, list)  and len(rt) > 0:
                for rt_value in rt:
                   rt_values.append(rt_value)
            else:
                #print(" swagger_rt : rt from schema")
                schema_id = db_get_key(item, "get/responses/200/schema/$ref")
                #print(" swagger_rt : schema_id",schema_id)
                my_data = db_get_key(json_data, schema_id)
                rt = db_get_key(my_data,"properties/rt/items/enum")
                #print ("  RT ",rt)
                for rt_value in rt:
                    rt_values.append(rt_value)
    print (" swagger_rt rt (array):", rt_values)
    return rt_values


def find_in_array(value, array_values):
    """
    compare the value against the first element of the 1 level down array.
    :param value: value to compare
    :param array_values: array [[ a, b, c],[a,b,c]]
    :return: True = Found, False is not found
    """
    if array_values == None:
        return False
    for array_value in array_values:
        if array_value[0] == value:
            return True
    return False


def find_files(dirname, rt_values):
    """
    find the files where the rt values are stored in (as part of the example)
    :param dirname: dir name
    :param rt_values: array of rt values
    :return found_file: array of file names, no duplicates...
    """
    file_list = get_dir_list(dirname, ext=".swagger.json")
    print ("find_files: directory:", dirname)
    found_file = []
    for myfile in file_list:
            file_data = load_json(myfile, dirname)
            rt_values_file = swagger_rt(file_data)
            for rt_file in rt_values_file:
                if find_in_array(rt_file, rt_values):
                    found_file.append(myfile)
    return found_file
        

def find_schema_files(dirname):
    """
    find the files where the rt values are stored in (as part of the example)
    :param dirname: dir name
    :return found_file: array of file names, no duplicates...
    """
    file_list = get_dir_list(dirname, ext="-schema.json")
    print ("find_files: directory:", dirname)
    found_file = []
    for myfile in file_list:
            #file_data = load_json(myfile, dirname)
            found_file.append(myfile)
    return found_file

def find_resource_in_files(dirname, file_list, property_name):
    """
    find the property where the rt values are stored in (as part of the example)
    :param dirname: dir name
    :return found_file: array of file names, no duplicates...
    """
    for myfile in file_list:
        file_data = load_json(myfile, dirname)
        #print ("find_resource_in_files file:", myfile)
        for key, item in file_data["definitions"].items():
            if key == property_name:
                #print ("find_resource_in_files ", key, item)
                return (key, item)



def remove_unused_defintions(json_data):
    """
    remove unused definitions
    - definitions that are not referenced
    """
    print ("remove_unused_defintions")
    def_data = json_data["definitions"]
    to_remove = []
    for def_name, def_item in def_data.items():
        full_def_name = "#/definitions/" + def_name
        value = find_key_value(json_data, "$ref", full_def_name)
        if value is None:
            # not found, e.g. can be removed
            to_remove.append(def_name)
        
    for item in to_remove:
        print ("  remove_unused_defintions removing :", item)
        erase_element(def_data, item, erase_entry=True)
    
    
def remove_unused_parameters(json_data):
    """
    remove unused definitions
    - definitions that are not referenced
    """
    print ("remove_unused_parameters")
    #paths_data = json_data["paths"]
    par_data = json_data["parameters"]
    to_remove = []
    for par_name, par_item in par_data.items():
        full_par_name = "#/parameters/" + par_name
        value = find_key_value(json_data, "$ref", full_par_name)
        if value is None:
            # not found, e.g. can be removed
            to_remove.append(par_name)
    
    for item in to_remove:
        print ("  remove_unused_parameters removing :", item)
        erase_element(par_data, item, erase_entry=True)
    
def remove_for_optimize(json_data):
    """
    remove things from the swagger file
    - license data
    - x-examples in responses
    - x-examples in body definitions (parameters)
    :param json_data: the swagger file
    """
    info_dict = json_data["info"]["license"]
    erase_element(info_dict, "x-description")
    erase_element(info_dict, "x-copyright")
    erase_element(info_dict, "url")
    
    for path, path_item in json_data["paths"].items():
        for method, method_item in path_item.items():
            if isinstance(method_item, dict):
                #erase_element(method_item, "description", erase_entry=True)
                for response, response_item in method_item.items():
                    if isinstance(response_item, dict):
                        for responsecode, responsecode_item in response_item.items():
                            erase_element(responsecode_item, "x-example", erase_entry=True)
                            #erase_element(responsecode_item, "description", erase_entry=True)
                    if isinstance(response_item, list):
                        for entry in response_item:
                            if isinstance(entry, dict):
                                erase_element(entry, "x-example", erase_entry=True)
                                #erase_element(entry, "description", erase_entry=True)
    
    for defi, defi_item in json_data["definitions"].items():
      for obj, obj_item in defi_item.items():
        if isinstance(obj_item, dict):
          for prop, prop_item in obj_item.items():
            #print (" ======> prop", obj)
            erase_element(prop_item, "description", erase_entry=True)


def clear_descriptions(json_data):
    """
    clear the descriptions e.g. set them on empty string e.g. ""
    :param json_data: the parsed swagger file
    """
    find_key_and_clean(json_data, "description")

def clear_info(json_data):
    """
    clear the info fields e.g. set them on empty string e.g. ""
    :param json_data: the parsed swagger file
    """   
    try:
        json_data["info"]["license"]["name"] = ""
        #json_data["info"]["license"]["url"] = ""
        #json_data["info"]["license"]["x-copyright"] = ""
        json_data["info"]["termsOfService"] = ""
    except:
        pass
              
def update_definition_with_rt(json_data, rt_value_file, rt_values):
    """
    update the definition section with the default rt value as array
    :param json_data: the parsed swagger file
    :param rt_value_file: not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    #print ("update_definition_with_rt", rt_values)
    print ("update_definition_with_rt")
    for rt_value in rt_values:
        print ("  rt:", rt_value[index_rt])
        
    keyvaluepairs = []
    
    for path, path_item in json_data["paths"].items():
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[index_rt], rt_values):
                for rt_f in rt_values:
                    if rt_f[index_rt] == rt[index_rt]:
                        keyvaluepairs.append([path, rt, ref])
        except:
            pass
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_def_name = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_def_name:
                # found entry
                properties = def_item.get("properties")
                if properties is not None:
                    rt_prop = properties.get("rt")
                    if rt_prop is None:
                        print ("  update_definition_with_rt rt not found!, inserting..")
                        properties["rt"] =  json.loads("""{
                              "type" : "array",
                              "items" : {
                                "type" : "string",
                                "maxLength" : 64
                              },
                              "minItems" : 1,
                              "readOnly" : true,
                              "default" : ["oic.r.switch.binary"]
                            }""")
                    
                    for prop_name, prop in properties.items():
                        #print ("  update_definition_with_rt ", prop_name)
                        if prop_name == "rt":
                            print ("  update_definition_with_rt ", prop_name)
                            # the default should be an array.
                            if isinstance(entry[1], list):
                                prop["default"] = entry[1]
                            else:
                                prop["default"] = [entry[1]]
                             
              
def update_definition_with_if(json_data, rt_value_file, rt_values):
    """
    update the definition if enum with the values of rt_values
    :param json_data: the parsed swagger file
    :param rt_value_file: not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("update_definition_with_if")
    for rt_value in rt_values:
        print ("  href:", rt_value[index_href], " if:", rt_value[index_if])
    keyvaluepairs = []
    for path, path_item in json_data["paths"].items():
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[index_rt], rt_values):
                for rt_f in rt_values:
                    if rt_f[index_rt] == rt[index_rt]:
                        keyvaluepairs.append([path, rt, ref, rt_f])
        except:
            pass
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_def_name = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_def_name:
                # found entry
                properties = def_item.get("properties")
                if properties is not None:
                    # found entry
                    properties = def_item.get("properties")
                    if_prop = properties.get("if")
                    if if_prop is None:
                        print ("  update_definition_with_if if not found!, inserting..")
                        properties["if"] =  json.loads("""{
                          "type" : "array",
                          "readOnly": true,
                          "items" : {
                            "type" : "string",
                            "maxLength" : 64,
                            "enum" : [
                              "oic.if.a",
                              "oic.if.baseline"
                            ]
                          },
                          "minItems" : 1,
                          "maxItems" : 2,
                          "uniqueItems" : true
                        }""")

                    for prop_name, prop in properties.items():
                        if prop_name == "if":
                            print ("  replacing if with", entry[3][index_if])
                            prop["items"]["enum"] = entry[3][index_if]
                            if entry[3][index_if] is not None:
                                if len(entry[3][index_if]) != 2:
                                    prop["maxItems"] = len(entry[3][index_if])
                        
                        
def update_parameters_with_if(json_data, rt_value_file, rt_values):
    """
    update the definition if enum with the values of rt_values
    :param json_data: the parsed swagger file
    :param rt_value_file: not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],..]
    """
    print ("update_parameters_with_if")
    for rt_value in rt_values:
        print ("  href:", rt_value[index_href], " if:", rt_value[index_if])

    param_data = json_data["parameters"]
    for param_name, param_item in param_data.items():
        print ("update_parameters_with_if", param_name)
        for prop_name, prop in param_item.items():
            if prop_name == "name" and prop == "if":
                if VERBOSE:
                    print (" replacing if with", rt_value[index_if])
                param_item["enum"] = rt_value[index_if]


def update_definition_with_type(json_data, rt_value_file, rt_values):
    """
    update the definition type values, e.g. override the type in an oneof construct
    - updates to type, range, step if it contains oneOff subkey
    :param json_data: the parsed swagger file
    :param rt_value_file: not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("update_definition_with_type")
    
    for rt_value in rt_values:
        print ("  href:", rt_value[index_href], " type:", rt_value[index_type])
        
    supported_types = ["integer", "number", "string", "boolean"]  
    keys_to_handle = ["type", "step", "precision", "value"] # range needs to be handled differently since it is an array
    # array of arrays of path, r, ref, rt_values
    keyvaluepairs = []
    for path, path_item in json_data["paths"].items():
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path, rt, ref, rt_f])
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
                        keyvaluepairs.append([path, rt, ref, rt_f])
        except:
            pass
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_defname = "#/definitions/" + def_name   
        if VERBOSE:
            print ("  def_name", def_name)
        for entry in keyvaluepairs:
            if entry[2] == full_defname:
                properties = def_item.get("properties")
                my_type = entry[3][index_type]
                if entry[3][index_type] not in supported_types:
                    # invalid type
                    if my_type is not None:
                        print (" *** ERROR type is not valid:", entry[3][index_type],
                               " supported types:", supported_types)
                elif properties is not None:
                    # properties is the top key 
                    my_type = entry[3][index_type]
                    for prop_name, prop in properties.items():
                        one_off = prop.get("anyOf")
                        if prop_name in keys_to_handle:
                            if VERBOSE:
                                print ("update_definition_with_type ", prop_name)
                            prop["type"] = my_type
                            if one_off is not None:
                                prop.pop("anyOf")
                        if prop_name == "range":
                            one_off = prop["items"].get("anyOf")
                            if one_off is not None:
                                if VERBOSE:
                                    print ("update_definition_with_type ", prop_name)
                                prop["items"].pop("anyOf")
                                prop["items"]["type"] = my_type

                else :
                    try:
                        ds = def_item | grep("type")
                        print (" ===> grep")
                        print(ds)
                    except:
                        print (" ===> grep failed!!")
                        pass
  

def remove_definition_properties(json_data, rt_value_file, rt_values):
    """
    remove the definition properties as indicated in the values of rt_values
    :param json_data: the parsed swagger file
    :param rt_value_file: not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("remove_definition_properties")
    rt = None
    for rt_value in rt_values:
        print ("  rt:", rt_value[index_rt], " prop:", rt_value[index_prop])
    
    if rt_values[0][index_prop] == None :
        return
    
    # array of arrays of path, r, ref, rt_values
    keyvaluepairs = []
    for path, path_item in json_data["paths"].items():
        found_rt = False
        rt_f = None
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path, rt, ref, rt_f])
                        found_rt = True
        except:
            pass
        try:
            schema = path_item["post"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if found_rt:
                keyvaluepairs.append([path, rt, ref, rt_f])
        except:
            pass    
                        
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_def_name = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_def_name:
                if VERBOSE:
                    print ("  definition:", full_def_name)
                # found entry
                properties = def_item.get("properties")
                remove_list = entry[3][index_prop]
                if remove_list is not None:
                    for prop_name in remove_list:
                        erase_element(properties, prop_name, erase_entry=True)
                        
def add_definition_properties(json_data, rt_value_file, rt_values, dirname, file_list):
    """
    add the definition properties as indicated in the values of rt_values
    :param json_data: the parsed swagger file
    :param rt_value_file: not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("add_definition_properties")
    rt = None
    for rt_value in rt_values:
        print ("  new props:", rt_value[index_rt], " prop:", rt_value[index_add_props])
    
    if rt_values[0][index_add_props] == None :
        return

    for item in rt_value[index_add_props]:
        key, items = find_resource_in_files(dirname, file_list, item)
        print ("add_definition_properties", key, items)

    # array of arrays of path, r, ref, rt_values
    keyvaluepairs = []
    for path, path_item in json_data["paths"].items():
        try:
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            keyvaluepairs.append([ref, key, items])
        except:
            pass
        try:
            schema = path_item["post"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            keyvaluepairs.append([ref, key, items])
        except:
            pass    
                        
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_def_name = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[0] == full_def_name:
                if VERBOSE:
                    print ("  definition:", full_def_name)
                # found entry
                properties = def_item.get("properties")
                properties[key] = items


def remove_path_method(json_data, rt_value_file, rt_values):
    """
    remove the method on an path
    :param json_data: the parsed swagger file
    :param rt_value_file:  not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("remove_path_method")
    for rt_value in rt_values:
        print ("   href:", rt_value[index_href], " method:", rt_value[index_method])
        
    # array of arrays of path, r, ref, rt_values
    # keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
        for rt_value in rt_values:
            if rt_value[index_href] == path:
                methods = rt_value[index_method]
                if methods is not None:
                    for method in methods:
                        erase_element(path_item, method, erase_entry=True)
            
            
def update_path_value(json_data, rt_value_file, rt_values):
    """
    update the path value of the rt from the rt_valuees
    :param json_data: the parsed swagger file
    :param rt_value_file: not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("update_path_value:")
    for rt_value in rt_values:
        print ("   rt:", rt_value[index_rt], " href:", rt_value[index_href])
                
    rt_values_file = swagger_rt(json_data)
    #print (rt_values_file)
    
    keyvaluepairs = []
    for path, path_item in json_data["paths"].items():
        #print ("update_path_value", path)
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
        except:
            # no example, use the list of found rt values not using the example
            rt = rt_values_file
            pass
        if find_in_array(rt[0], rt_values):
            for rt_f in rt_values:
                if rt_f[0] == rt[0]:
                    keyvaluepairs.append([path, rt_f[1]])
            
    path_data = json_data["paths"]
    for replacement in keyvaluepairs:
        if replacement[1] != replacement[0]:
            old_path = replacement[0]
            new_path = replacement[1]
            # check if there is an action or interface in the path
            old_path_temp = old_path.split("?")
            if len(old_path_temp) > 1:
                # concatinate everything again
                new_path += "?"
                for path_seg in old_path_temp[1:]:
                    new_path += path_seg
                
            
            print (" update_path_value :", old_path, " with ", new_path)
            path_data[new_path] = path_data[old_path]
            path_data.pop(old_path)
        else:
            print(" update_path_value: already the same :", replacement)

def is_query_to_be_removed(my_dict, remove_param):
  """
    "unit" :  {
            "in": "query",
            "description": "Units",
            "type": "string",
            "enum": ["C", "F", "K"],
            "name": "units",
            "x-queryexample" : "/TemperatureResURI?units=C"
      }
  """
  if isinstance(my_dict, dict):
     in_v = my_dict.get("in")
     name = my_dict.get("name")
     if name is None:
        return False
     if in_v is None:
        return False
     if remove_param is None:
        return False
     if in_v == "query" and name in remove_param:
         return True
  return False


def remove_query_param(json_data, rt_value_file, rt_values):
    """
    remove the query param
    :param json_data: the parsed swagger file
    :param rt_value_file:  not used
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("remove_query_param")
    for rt_value in rt_values:
        print ("   href:", rt_value[index_href], " query name:", rt_value[index_remove_query])
    remove_param = rt_value[index_remove_query]
        
    # array of arrays of path, r, ref, rt_values
    keyvaluepairs =[]
    for path, path_item in json_data["paths"].items():
       for method, method_item in path_item.items():
           remove_item = None
           for param_item in method_item["parameters"]:
              value = param_item.get("$ref")
              if isinstance(value, dict):
                 if is_query_to_be_removed(value, remove_param):
                    remove_item = param_item
                    print ("   removing query:", path, method, remove_param)
              if (value != None) and isinstance(value,str) and value.startswith("#/") :
                # get the reference.
                dict_value = db_get_key(json_data, value)
                if isinstance(dict_value, dict):
                  if is_query_to_be_removed(dict_value, remove_param):
                    remove_item = param_item
                    print ("   removing query:", path, method, remove_param, value)
                    print ("   removing definition:", value)
                    db_remove_key(json_data, value)
           if remove_item:
              method_item["parameters"].remove(remove_item)
                

def collapse_allOf(json_data):
    """
    collapse_allOf
    - only collapses if the keys below allOf are not of [allOf, anyOf, oneOf]
    e.g.
       { oneOf [ properties : {a,b}, properties {a,c}  ] }   ==>    {  properties : {a,b,c } } 
    :param json_data: the parsed swagger file
    """
    print ("collapse_allOf:")
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        print ("  ",def_name)
        handle_allof = False
        new_props = {}
        for prop_name, prop in def_item.items():
            if prop_name == "allOf":
                handle_allof = True
                for item_id in prop:
                    for item_name, item in item_id.items():
                        if item_name == "properties":
                            # check if properties exist already
                            if new_props.get("properties") is None:
                                # no properties yet
                                new_props[item_name] = item
                            else:
                                # add properties decendants to the existing properties key
                                for prop_item_name, prop_item in item.items():
                                   new_props["properties"][prop_item_name] = prop_item 
                        elif item_name == "description":
                            new_props[item_name] = item
                        else:
                            # check if properties exist already
                            if new_props.get("properties") is None:
                                # no properties yet
                                new_props[item_name] = item
                            else:
                                # add properties decendants to the existing properties key
                                if isinstance(item, dict): 
                                    for prop_item_name, prop_item in item.items():
                                       new_props["properties"][prop_item_name] = prop_item
                        if item_name in ["oneOf", "anyOf", "allOf"]:
                            handle_allof = False        
        if handle_allof:
            if VERBOSE:
                print (" processing: ", def_name)
            def_data[def_name] = new_props
            
  
def handle_collections(json_data, rt_value_file, rt_values):
    """
    handle collections
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print("handle_collections")
    
    # array of arrays of path, r, ref, rt_values
    keyvaluepairs = []
    for path, path_item in json_data["paths"].items():
        found_rt = False
        rt_f = None
        try:
            x_example = path_item["get"]["responses"]["200"]["x-example"]
            rt = x_example.get("rt")
            schema = path_item["get"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if find_in_array(rt[0], rt_values):
                for rt_f in rt_values:
                    if rt_f[0] == rt[0]:
                        keyvaluepairs.append([path, rt, ref, rt_f])
                        found_rt = True
        except:
            pass
        try:
            schema = path_item["post"]["responses"]["200"]["schema"]
            ref = schema["$ref"]
            if found_rt:
                keyvaluepairs.append([path, rt, ref, rt_f])
        except:
            pass    
               
    if rt_values[0][index_rts] == None:
        return
               
    def_data = json_data["definitions"]
    for def_name, def_item in def_data.items():
        full_def_name = "#/definitions/" + def_name
        for entry in keyvaluepairs:
            if entry[2] == full_def_name:
                # found entry
                rd = get_dict_recursively (def_item, "rts")
                newval = {'type': 'array', 'minItems': 1, 'items': {""},  'uniqueItems': True}
                my_enum ={}
                my_enum["enum"] = rt_values[0][index_rts]
                newval["items"] = my_enum
                for item in rd:
                    print ("  replacing rts:", full_def_name)
                    mydict = item[2]
                    mydict[item[0]] = newval
    
    
def create_code_generation(json_data, rt_value_file, rt_values, index, dirname, file_list):
    """
    create the introspection data, e.g. morph json_data.
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("")
    rt_single = [rt_values[index]]
    
    # this should 
    rt_ingore_list = ["oic.wk.res",  "oic.wk.introspection", "oic.wk.p", "oic.wk.d"]
    if rt_single[0][index_rt] in rt_ingore_list :
        print("create_code_generation ignored:", rt_single[0][index_rt])
        json_data = None
        return
    
    # if rt_single is not None:
    print("create_code_generation index:", index, rt_single[0][index_href])
    collapse_allOf(json_data)
    handle_collections(json_data, rt_value_file, rt_single)
    update_path_value(json_data, rt_value_file, rt_single)
    update_definition_with_rt(json_data, rt_value_file, rt_single)
    update_definition_with_if(json_data, rt_value_file, rt_single)
    update_parameters_with_if(json_data, rt_value_file, rt_single)
    update_definition_with_type(json_data, rt_value_file, rt_single)
    remove_definition_properties(json_data, rt_value_file, rt_single)
    add_definition_properties(json_data, rt_value_file, rt_single, dirname, file_list)
    remove_path_method(json_data, rt_value_file, rt_single)
    remove_query_param(json_data, rt_value_file, rt_single)
    
    
    
def create_introspection(json_data, rt_value_file, rt_values, index, dirname, file_list):
    """
    create the introspection data, e.g. morph json_data.
    :param json_data: the parsed swagger file
    :param rt_value_file: the filename
    :param rt_values: array of rt values e.g.[[rt_value, href, prop_if, my_type, props, methods],...]
    """
    print ("")
    rt_single = [rt_values[index]]
    # if rt_single is not None:
    print("create_introspection index:", index, rt_single[0][index_href])
    collapse_allOf(json_data)
    handle_collections(json_data, rt_value_file, rt_single)
    update_path_value(json_data, rt_value_file, rt_single)
    update_definition_with_rt(json_data, rt_value_file, rt_single)
    update_definition_with_if(json_data, rt_value_file, rt_single)
    update_parameters_with_if(json_data, rt_value_file, rt_single)
    update_definition_with_type(json_data, rt_value_file, rt_single)
    remove_definition_properties(json_data, rt_value_file, rt_single)
    add_definition_properties(json_data, rt_value_file, rt_single, dirname, file_list)
    remove_path_method(json_data, rt_value_file, rt_single)
    remove_query_param(json_data, rt_value_file, rt_single)
    
def optimize_introspection(json_data):    
    """
    optimize the json
    - clear the descriptions (e.g. remove the text only)
    :param json_data: the parsed swagger file
    """
    #remove_for_optimize(json_data)
    clear_descriptions(json_data)
    clear_info(json_data)
    remove_for_optimize(json_data)
    #remove_unused_defintions(json_data)
    #remove_unused_parameters(json_data)
           
def merge(merge_data, file_data, index):
    """
    merge the file_data (paths and definitions) into merge_data
    :param merge_data: the data that will be used to merge into
    :param file_data: the data to merge
    :param index: index counter of the index that is being merged
    """
   
    if file_data is None:
        print (" merge: data ignored, is empty")
        return
    
    local_index = 0
    for parameter, parameter_item in file_data["parameters"].items():
        local_index += 1
        fixed = False
        for cmp, cmp_data in merge_data["parameters"].items():
            # check if a simular parameter (same tree) set exist.
            ddiff = DeepDiff(cmp_data, parameter_item, ignore_order=True)
            if ddiff == {}:
                # found the same tree, but with a different name
                print ("   ==> parameter merge: found" + parameter +"identical tree with name:", cmp)
                # fix the path data to the existing found parameter, do it 2 times..
                search_parameter = "#/parameters/" + parameter
                new_parameter = cmp #"p" + str(index) +"p"+ str(local_index)
                my_dict = find_key_value(file_data["paths"], "$ref", search_parameter)
                while my_dict is not None:
                    # update the reference
                    my_dict["$ref"] = "#/parameters/" + new_parameter
                    # find next
                    my_dict = find_key_value(file_data["paths"], "$ref", search_parameter)
                fixed = True
                break 
        if fixed == False:
            # there is no matching existing definition, add a new one with a new name
            new_parameter = "p" + str(index) + str(local_index)
            print ("merge: parameter adding new:", parameter, " adding as:", new_parameter)
            # fix the path data, do it 2 times.. 
            search_parameter = "#/parameters/" + parameter
            my_dict = find_key_value(file_data["paths"], "$ref", search_parameter)
            while my_dict is not None:
                # update the reference
                my_dict["$ref"] = "#/parameters/" + new_parameter
                # find next
                my_dict = find_key_value(file_data["paths"], "$ref", search_parameter)
            # add the new parameter.
            merge_data["parameters"][new_parameter] = parameter_item

    local_index = 0
    for definition, definiton_item in file_data["definitions"].items():
        local_index += 1
        fixed = False
        for cmp, cmp_data in merge_data["definitions"].items():
            # check if a simular parameter (same tree) set exist.
            ddiff = DeepDiff(cmp_data, definiton_item, ignore_order=True)
            if ddiff == {}:
                # found the same tree, but with a different name
                print ("   ==> definition merge:"+ definition +"found identical tree with name:", cmp)
                # fix the path data to the existing found parameter, do it 2 times..
                search_definition = "#/definitions/" + definition
                new_definition = cmp #"d" + str(index) + str(local_index)
                my_dict = find_key_value(file_data["paths"], "$ref", search_definition)
                while my_dict is not None:
                    # update the reference
                    my_dict["$ref"] = "#/definitions/" + new_definition
                    # find next
                    my_dict = find_key_value(file_data["paths"], "$ref", search_definition)
                fixed = True
                break 
        if fixed == False:
            # there is no matching existing definition, add a new one with a new name
            new_definition = "d" + str(index) + str(local_index)
            print ("merge: ===> definition adding new:", definition, " adding as:", new_definition)
            # fix the path data, do it 2 times.. 
            search_definition = "#/definitions/" + definition
            my_dict = find_key_value(file_data["paths"], "$ref", search_definition)
            while my_dict is not None:
                # update the reference
                my_dict["$ref"] = "#/definitions/" + new_definition
                # find next
                my_dict = find_key_value(file_data["paths"], "$ref", search_definition)
            # add the new parameter.
            merge_data["definitions"][new_definition] = definiton_item

 
    for path, path_item in file_data["paths"].items():
        merge_data["paths"][path] = path_item

def resolve_ref(json_data, ref_dict):
    """
    find key "target" in recursive dict
    :param rec_dict: dict to search in, json schema dict, so it is combination of dict and arrays
    :param target: target key to search for
    :param depth: depth of the search (recursion)
    """
    try:
        if isinstance(ref_dict, list):
            for value in ref_dict:
                # recurse down in array
                # not that $ref is only in a object, e.g. not part of an array.
                resolve_ref(json_data, value)
        new_data = None
        if isinstance(ref_dict, dict):
            for key, value in ref_dict.items():
                # if $ref found, replace the whole content.
                if key == "$ref":
                    if value.startswith("#"):
                        print("resolve_ref: found local $ref:", value)
                        reference = value.replace('#/definitions/', '')
                        new_data_i = json_data["definitions"]
                        m_ref = reference.split("/")
                        for i in range(len(m_ref)):
                           print("resolve_ref: key:", m_ref[i])
                           new_data = new_data_i[m_ref[i]]
                           new_data_i = new_data
                    if value.startswith("http"):
                        print("resolve_ref: found external $ref: ", value)
                        reference = value.split('#/definitions/')[1]
                        url = value.split("#")[0]
                        filename = "removeme_"+url[url.rfind("/")+1:]
                        wget.download(url, filename)
                        print("resolve_ref: url:", url)
                        #print("resolve_ref: ref:", reference)
                        json_file = load_json(filename)
                        try:
                            os.remove(filename)
                        except OSError:
                            pass
                        new_data_i = json_file["definitions"]
                        m_ref = reference.split("/")
                        for i in range(len(m_ref)):
                           print("resolve_ref: key:", m_ref[i])
                           new_data = new_data_i[m_ref[i]]
                           new_data_i = new_data
                if new_data is not None:
                    # break the loop, just fix the single found reference
                    break
            # this code must be out of the loop, it modifies the object
            if new_data is not None:
                print("resolve_ref: fixing $ref:", value)
                try:
                    ref_dict.pop("$ref")
                except:
                    pass
                for key_n, value_n in new_data.items():
                    ref_dict[key_n] = value_n
                            
            for key, value in ref_dict.items():
                # recurse down in object
                resolve_ref(json_data, value)
    except:
        traceback.print_exc()
        print("resolve_ref: !ERROR!!")
    
def resolve_external(json_data):
    max_loop=100
    ref_dict = json_data["definitions"]
    key = find_key(ref_dict, "$ref")
    while key is not None:
        resolve_ref(json_data, ref_dict)
        key = find_key(ref_dict, "$ref")
        max_loop = max_loop - 1
        if max_loop == 0:
            print ("resolve_external: max loop reached!")
            key = None
    
def main_app(my_args, generation_type):
    """

    :param my_args: argument object
    :param generation_type: string introspection or code
    """
    rt_values = None
    if my_args.ocfres is not None:
        rt_values = find_oic_res_resources(str(my_args.ocfres), my_args)
    elif my_args.input is not None:
        rt_values = find_input_resources(str(my_args.input))
    else:
        print (" no oic/res or input format given")
        
    write_intermediate = False
    if my_args.intermediate_files is not None and my_args.intermediate_files is True:
        write_intermediate = True
        
    print ("handling resources (overview):")
    files_to_process = find_files(str(my_args.resource_dir), rt_values)
    schema_files = find_schema_files(str(my_args.resource_dir)+"/schemas")
    print ("schema files:", schema_files)
    print ("processing files:", files_to_process)

    # not required so not framing...:
    # "consumes": [ "application/json" ],
    #              "termsOfService": "",
    merged_data = {    "definitions": {}, "parameters": {}, "paths": {} ,
                        "swagger": "2.0",
                        "info": { "license": { "name": " " },
                            "title": " ",
                            "version": " " },
                        }

    for my_file in files_to_process:
        print ("")
        print ("  main: File :", my_file)
        file_data = load_json(my_file, str(my_args.resource_dir))
        rt_values_file = swagger_rt(file_data)
        print ("  main: rt :", rt_values_file)
        for rt in rt_values:
            if rt[index_rt] == rt_values_file[0]:
                rt.append(my_file)  
                
    if rt_values is not None:
        for rt in rt_values:
            # always append one...
            rt.append(None)
            print ("  rt                      :", rt[index_rt])
            print ("    href                  :", rt[index_href])
            print ("    if                    :", rt[index_if])
            print ("    type (replace)        :", rt[index_type])
            print ("    props (remove)        :", rt[index_prop])
            print ("    methods (remove)      :", rt[index_method])
            print ("    query params (remove) :", rt[index_remove_query])
            print ("    rts (enum)            :", rt[index_rts])
            print ("    basefile              :", rt[index_file])
            print ("    additional props      :", rt[index_add_props])
        print(" ")   
            
        index = 0
        for rt in rt_values:
            if rt[index_file] is not None:
                file_data = load_json(rt[index_file], str(my_args.resource_dir))
                resolve_external(file_data)
                rt_values_file = swagger_rt(file_data)
                
                if "introspection" == generation_type:
                    print ("optimize for introspection..")
                    create_introspection(file_data, rt_values_file, rt_values, index, str(my_args.resource_dir)+"/schemas", schema_files)
                    optimize_introspection(file_data)
                else:
                    create_code_generation(file_data, rt_values_file, rt_values, index, str(my_args.resource_dir)+"/schemas", schema_files)
                    rt_ingore_list = ["oic.wk.res",  "oic.wk.introspection", "oic.wk.p", "oic.wk.d"]
                    rt_single = [rt_values[index]]
                    if rt_single[0][index_rt] in rt_ingore_list :
                        print("merge ignored:", rt_single[0][index_rt])
                        file_data = None
                    
                if write_intermediate:
                    file_to_write = str(my_args.out) + "_" + generation_type + "_" + str(index) +"_"+rt[6]
                    write_json(file_to_write, file_data)
                
                if merged_data is None:
                    merged_data = file_data
                else:
                    merge(merged_data, file_data, index)
            index = index + 1
            
        if merged_data is not None: 
            file_to_write = str(my_args.out) + "_" + generation_type + "_" + "merged.swagger.json"
            if my_args.title is not None:
                print("  Setting title:",  my_args.title)
                merged_data["info"]["title"] = my_args.title
            write_json(file_to_write, merged_data)

       
#
#   main of script
#
if __name__ == '__main__':
    print ("****************************")
    print ("*** DeviceBuilder (v1.2) ***")
    print ("****************************")
    parser = argparse.ArgumentParser()

    parser.add_argument("-ver", "--verbose", default=False, help="Execute in verbose mode", action='store_true')

    parser.add_argument("-ocfres", "--ocfres", default=None,
                         help="ocf/res input", nargs='?', const="", required=False)
    parser.add_argument("-input", "--input", default=None,
                         help="device builder input format",  nargs='?', const="", required=False)
    parser.add_argument("-out", "--out", default=None,
                         help="output dir + prefix e.g. (../mydir/generated1)", nargs='?', const="", required=True)

    parser.add_argument("-intermediate_files", "--intermediate_files", default=False,
                         help="write intermediate files", required=False)      
                         
    parser.add_argument("-resource_dir", "--resource_dir", default=None,
                         help="resource directory",  nargs='?', const="", required=False)
    parser.add_argument('-remove_property', '--remove_property', default=None, nargs='*',
                        help='remove property (--remove_property  value range step precision id) ')
    parser.add_argument('-type', '--type', default=None, nargs='?',
                        help='type of the value (or renamed value) (--type  integer number) ')
    parser.add_argument('-title', '--title', default=None, nargs='?',
                        help='populates info.title in the full swagger file (to be used as title for the device)(--title  myname) ')

     
    args = parser.parse_args()
    
    myargs = MyArgs()
    myargs.out = args.out
    myargs.resource_dir = args.resource_dir
    myargs.ocfres = args.ocfres
    myargs.input = args.input
    myargs.remove_property = args.remove_property
    myargs.type = args.type
    myargs.intermediate_files = args.intermediate_files
    myargs.title = args.title

    VERBOSE = args.verbose
    myargs.my_print()
    
    try:
        print ("")
        print ("== INTROSPECTION ==")
        main_app(myargs, "introspection")
        
        print ("")
        print ("== CODE GENERATION ==")
        main_app(myargs, "codegeneration")
            
        
    except:
        #print ("error in ", args.ocfres)
        traceback.print_exc()
        pass
