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

# my_crt = contents of <filename>_cert.der.hex
# my_key = contents of <filename>_key.der.hex
# int_ca = contents of ./chain/1-subca-cert.der.hex
# root_ca = contents of ./chain/0-root-cert.der.hex

import argparse
import os
from time import gmtime, strftime
from zipfile import ZipFile

import sys
import traceback
import io
import re


def write_contents(f, data, name):
    decl = "const char *" + name + " = "
    f.write(decl)
    data = data.decode('utf-8')
    lines = io.StringIO(data)
    line = lines.readline()
    while line != '':
        mychar = line[-2:-1]
        mychar2 = line[-1:]
        if hex(ord(mychar)) == "0xd":
            # print ("-2", len(line[-2:]), hex(ord(mychar)),hex(ord(mychar2)))
            f.write("\"" + line[:-2] + "\\r\\n\"")
        else:
            # print ("-1",len(line[-2:]),hex(ord(mychar)),hex(ord(mychar2)))
            f.write("\"" + line[:-1] + "\\r\\n\"")
        line = lines.readline()
        if line == '':
            f.write(";\n\n")
        else:
            f.write("\n")


if sys.version_info < (3, 5):
    raise Exception("ERROR: Python 3.5 or more is required, you are currently running Python %d.%d!" %
                    (sys.version_info[0], sys.version_info[1]))

print("***************************")
print("***  pki2include (v1)   ***")
print("***************************")
parser = argparse.ArgumentParser()

parser.add_argument("-ver", "--verbose", help="Execute in verbose mode", action='store_true')
parser.add_argument("-file", "--file", default=None, help="zip file name", nargs='?', const="", required=False)
args = parser.parse_args()

print("file        : " + str(args.file))

if (args.file):
    f = open(args.file + ".h", "w")

    file_name = str(args.file)
    filename = file_name.split(".z")[0]
    prefix = filename.split("/")[-1]

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
    f.write("*/\n")

    f.write("#ifndef PKI_CERT_INCLUDE_H\n")
    f.write("#define PKI_CERT_INCLUDE_H\n")
    f.write("#if defined(OC_SECURITY) && defined(OC_PKI)\n\n")

    f.write("/* PKI certificate data\n")
    f.write(" input file = ")
    f.write(args.file)
    f.write("\n")
    f.write(" prefix = ")
    f.write(prefix)
    f.write("\n")

    f.write(" date ")
    f.write(strftime("%Y-%m-%d %H:%M:%S", gmtime()))
    f.write("\n*/\n\n")
    try:
        # opening the zip file in READ mode
        with ZipFile(args.file, 'r') as zip:
            # printing all the contents of the zip file
            zip.printdir()
            chain_prefix = "chain"

            # determine if the zip has a parent directory
            pattern = r"/?([a-zA-Z0-9 _]+)?/pki_certs_cert.pem"
            dir_list = zip.namelist()
            for zfile in dir_list:
                match_object = re.match(pattern, zfile)
                if match_object:
                    prefix = match_object.group(1) + '/' + prefix
                    chain_prefix = match_object.group(1) + '/' + chain_prefix

            data = zip.read(prefix + "_cert.pem")
            write_contents(f, data, "my_cert")

            data = zip.read(prefix + "_key.pem")
            write_contents(f, data, "my_key")

            data = zip.read(chain_prefix + "/1-subca-cert.pem")
            write_contents(f, data, "int_ca")

            data = zip.read(chain_prefix + "/0-root-cert.pem")
            write_contents(f, data, "root_ca")

    except:
        print(" ERROR zip file not found: no certificate data")
        data = " FAKE".encode("windows-1252")
        write_contents(f, data, "my_cert")
        write_contents(f, data, "my_key")
        write_contents(f, data, "int_ca")
        write_contents(f, data, "root_ca")

    f.write("#endif /* OC_SECURITY && OC_PKI */\n")
    f.write("#endif /* PKI_CERT_INCLUDE_H */\n")
    f.close()