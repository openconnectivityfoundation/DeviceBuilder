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

import argparse
import os
import jsonschema
import json
import sys
import traceback

try:
    from deepdiff import DeepDiff
except:
    print("missing DeepDiff:")
    print("Trying to Install required module: DeepDiff ")
    os.system('python3 -m pip install deepdiff')
import deepdiff

if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))

def json_print(data):
    """
    pretty print json
    :param data: json to be printed
    """
    try:
        json_string = json.dumps(data, indent=2)
        print(json_string)
    except:
        print(data)


def load_json(filename, my_dir=None):
    """
    load the JSON file
    :param filename: filename (with extension)
    :param my_dir: path to the file
    :return: json_dict
    """
    full_path = filename
    if my_dir is not None:
        full_path = os.path.join(my_dir, filename)
    if os.path.isfile(full_path) is False:
        print("json file does not exist:", full_path)
    linestring = open(full_path, 'r').read()
    json_dict = json.loads(linestring)
    return json_dict


def compare_json(file1, file2):
    """
    compare 2 json files, ignoring the order..
    :param file1: filename (with extension)
    :param file2: path to the file
    """
    file_data1 = load_json(file1) 
    file_data2 = load_json(file2)  
    ddiff = DeepDiff(file_data1, file_data2, ignore_order=True)
    if ddiff == {}:
        print(" == EQUAL ==")
    else:
        print(" == NOT EQUAL == ")
        json_print(ddiff)


#
#   main of script
#
if __name__ == '__main__':
    print("***************************")
    print("***  compareJson (v1)   ***")
    print("***************************")
    parser = argparse.ArgumentParser()

    parser.add_argument( "-ver", "--verbose", help="Execute in verbose mode", action='store_true')
    parser.add_argument( "-file1", "--file1", default=None, help="swagger file name 1",  nargs='?', const="", required=True)
    parser.add_argument( "-file2", "--file2", default=None, help="swagger file name 2",  nargs='?', const="", required=True)

    args = parser.parse_args()

    print("file1        : " + str(args.file1))
    print("file2        : " + str(args.file2))

    compare_json(args.file1, args.file2)
