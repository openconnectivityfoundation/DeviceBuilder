#############################
#
#    copyright 2018 Open Interconnect Consortium, Inc. All rights reserved.
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
from time import gmtime, strftime

import sys
import traceback

 
if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))
 
print ("*************************")
print ("***  cbor2include (v1)   ***")
print ("*************************")
parser = argparse.ArgumentParser()

parser.add_argument( "-ver", "--verbose", help="Execute in verbose mode", action='store_true')
parser.add_argument( "-file", "--file", default=None, help="swagger file name",  nargs='?', const="", required=False)

args = parser.parse_args()

print("file        : " + str(args.file))

if (args.file) :
    cbor_data = open(args.file, 'rb').read()

    if args.verbose:
        print("cbor data:")
        print (cbor_data)

    f = open(args.file+".h", "w")

    size_cbor = len(cbor_data)
    if args.verbose:
        print("size:", size_cbor)

    f.write("/*\n")
    f.write("#    copyright 2019 Open Interconnect Consortium, Inc. All rights reserved.\n")
    f.write("#    Redistribution and use in source and binary forms, with or without modification,\n")
    f.write("#    are permitted provided that the following conditions are met:\n")
    f.write("#    1.  Redistributions of source code must retain the above copyright notice,\n")
    f.write("#        this list of conditions and the following disclaimer.\n")
    f.write("#    2.  Redistributions in binary form must reproduce the above copyright notice,\n")
    f.write("#        this list of conditions and the following disclaimer in the documentation and/or other materials provided\n")
    f.write("#        with the distribution.\n")
    f.write("#\n")
    f.write("#    THIS SOFTWARE IS PROVIDED BY THE OPEN INTERCONNECT CONSORTIUM, INC. \"AS IS\" AND ANY EXPRESS OR IMPLIED WARRANTIES,\n")
    f.write("#    INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE OR\n")
    f.write("#    WARRANTIES OF NON-INFRINGEMENT, ARE DISCLAIMED. IN NO EVENT SHALL THE OPEN INTERCONNECT CONSORTIUM, INC. OR\n")
    f.write("#    CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES\n")
    f.write("#    (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;\n")
    f.write("#    OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,\n")
    f.write("#    OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,\n")
    f.write("#    EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n")
    f.write("*/\n\n")
    
    f.write("#ifndef INTROSPECTION_INCLUDE_H\n")
    f.write("#define INTROSPECTION_INCLUDE_H\n")
    
    f.write("/* introspection data\n")
    f.write(" input file = ")
    f.write(args.file)
    f.write("\n")
    
    f.write(" date ")
    f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    f.write(" */\n\n")
    
    f.write("#define introspection_data_size ")
    f.write(str(size_cbor))
    f.write("  /* size of the CBOR */\n")
    
    f.write("const uint8_t introspection_data[] = {\n")
    counter = 0
    for item in cbor_data[:-1]:
        counter += 1
        int_item = int(item)
        f.write(" ")
        f.write(hex(int_item))
        f.write ("," )
        if counter == 12:
             f.write ("\n")
             counter = 0
    f.write(hex(int(cbor_data[len(cbor_data) - 1])))

    f.write("};\n\n")
    f.write("#endif /* INTROSPECTION_INCLUDE_H */\n")
    f.close()

