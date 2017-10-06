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

import argparse
import os
import jsonschema
import json
import sys

try: 
    import cbor
except:
    print("missing cbor:")
    print ("Trying to Install required module: cbor ")
    os.system('python3 -m pip install cbor')
import cbor
 
if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))
 
print ("*************************")
print ("***  swag2cbor (v1)   ***")
print ("*************************")
parser = argparse.ArgumentParser()

parser.add_argument( "-ver", "--verbose", help="Execute in verbose mode", action='store_true')
parser.add_argument( "-file", "--file", default=None, help="swagger file name",  nargs='?', const="", required=False)
parser.add_argument( "-cbor", "--cbor", default=None, help="cbor file name",  nargs='?', const="", required=False)

args = parser.parse_args()

print("file        : " + str(args.file))
print("cbor        : " + str(args.cbor))

if (args.file) :
    swagger_raw = open(args.file, 'r').read()
    schema_data = json.loads(swagger_raw)
    if args.verbose:
        print("json data:")
        print (schema_data)

    cbor_data = cbor.dumps(schema_data)
    if args.verbose:
        print("cbor data:")
        print (cbor_data)
        
    f = open(args.file+".cbor", "wb")
    f.write(cbor_data)
    f.close()
    
if (args.cbor) :

    try:
        cbor_raw = open(args.cbor, 'rb').read()
    except:
        print ("cbor_to_txt: failed:", args.cbor)
        traceback.print_exc()
        
    if args.verbose:
        print("cbor data:")
        print (cbor_raw)

    json_data = None
    try:
        json_data = cbor.loads(cbor_raw)
    except:
        print ("cbor_to_txt: failed:", cbor_raw)
        traceback.print_exc()
        
    if args.verbose:
        print("json data:")
        print (json_data)
        
    fp = open(str(args.cbor)+".json", "w")
    json_string = json.dumps(json_data, indent=2, sort_keys=True)
    fp.write(json_string)
    fp.close()
   
    
    
