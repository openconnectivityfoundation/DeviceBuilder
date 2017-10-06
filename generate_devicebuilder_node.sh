#!/bin/bash

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

#
#
#
#

PYTHON_EXE=C:\\python35-32\\python3.exe
DeviceBuilder=./src/deviceBuilder.py
SWAG2CBOR=./src/swag2cbor.py
SWAGGER2XDIR=../swagger2x
SWAGGER2X=$SWAGGER2XDIR/src/swagger2x.py

INPUTFILE=$1
OUTPUTDIR=$2
MODELSDIR=../IoTDataModels

echo "input file:   " $INPUTFILE
echo "output folder:" $OUTPUTDIR


if [ ! -f $MODELS_DIR/README.md ]
then
pushd `pwd`
cd ..
git clone https://github.com/OpenInterConnect/IoTDataModels.git --branch master
popd
fi


if [ ! -f $SWAGGER2X ]
then
pushd `pwd`
cd ..
git clone https://github.com/OpenInterConnect/swagger2x.git --branch master
popd
fi

echo "creating $OUTPUTDIR"
mkdir -p $OUTPUTDIR

$PYTHON_EXE $DeviceBuilder -input $INPUTFILE -resource_dir $MODELSDIR -out $OUTPUTDIR/out 
wb-swagger validate $OUTPUTDIR/out_introspection_merged.swagger.json
$PYTHON_EXE $SWAG2CBOR -file $OUTPUTDIR/out_introspection_merged.swagger.json

#-template_dir ../src/templates -template NodeIotivityServer -swagger ../test/in/test_swagger_1/test_swagger_1.swagger.json -out_dir $OUTPUT_DIR/$TEST_CAS
$PYTHON_EXE $SWAGGER2X -template_dir $SWAGGER2XDIR/src/templates -template NodeIotivityServer -swagger $OUTPUTDIR/out_introspection_merged.swagger.json -out_dir $OUTPUTDIR/code


