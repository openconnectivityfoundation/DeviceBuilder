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
# usage
# sh DeviceBuilder_C++IotivityServer.sh <devicbuilder input file>  <output directory> <device type>
# <devicbuilder input file>  : see https://github.com/openconnectivityfoundation/DeviceBuilder/tree/master/test/input_define_device for examples
# <output directory> will be created
#
#  This script generates:
#  - introspection file in json and cbor
#  - swagger file for code generation
#  - node.js code
#
#  things one needs:
#  - git
#  - python3 installation
#  - wb-swagger https://github.com/WAvdBeek/wb-swagger-node globally installed
#
# example command:
#$ sh DeviceBuilder_NodeIotivityServer.sh ./test/input_define_device/input-lightdevice.json ../out-device/light
#
# This will create an output folder 1 level higher than the github repo and should have the generated files in the  sub folder.
# This will have :
# -	Input-lightdevice.json (e.g. the input file…)
# -	out_codegeneration_merged.swagger.json : the input file for swagger2x
# -	out_introspection_merged.swagger.json : the introspection file in json
# -	out_introspection_merged.swagger.json.cbor : the introspection file in cbor
# -	code (folder)




PYTHON_EXE=python3
DeviceBuilder=./src/DeviceBuilder.py
SWAG2CBOR=./src/swag2cbor.py
CBOR2INC=./src/cbor2include.py
SWAGGER2XDIR=../swagger2x
SWAGGER2X=$SWAGGER2XDIR/src/swagger2x.py
PIP3=pip3

INPUTFILE=$1
OUTPUTDIR=$2
DEVICETYPE=$3
TITLE=$4
MODELS_DIR=../IoTDataModels
CORE_DIR=../core

if [ -z "$TITLE" ]
then
      echo "\$TITLE is empty, setting PID"
      TITLE=$$
      echo "==> $TITLE"
else
      echo "\$TITLE is NOT empty"
fi


stringContain() { [ -z "${2##*$1*}" ]; }


echo "input file:   " $INPUTFILE
echo "output folder:" $OUTPUTDIR

PIP_INSTALLED=`which pip3`
if stringContain "not found" $PIP_INSTALLED;then 
    echo "== installing pip3"
    sudo apt-get -y install python3-pip 
else
    echo "pip3 installed: $PIP_INSTALLED"
fi 

#
# multiple checks on what is already there. 
#
`$PYTHON_EXE -c "import sys, pkgutil; sys.exit(0 if pkgutil.find_loader('cbor') else 1)"`
PyPACKAGE_INSTALLED=$?
if [ $PyPACKAGE_INSTALLED -eq 1 ];then 
    echo "== installing python dependencies" $PyPACKAGE_INSTALLED
    $PIP3 install -U -r requirements-setuptools.txt
    $PIP3 install -U -r requirements.txt
else
    echo "python package cbor installed, assuming all other packages are installed too"
    echo "if not run on the commandline: $PIP3 install -U -r requirements.txt"
fi 

`$PYTHON_EXE -c "import sys, pkgutil; sys.exit(0 if pkgutil.find_loader('Jinja2') else 1)"`
PyPACKAGE_INSTALLED=$?
if [ $PyPACKAGE_INSTALLED -eq 1 ];then 
    echo "== installing python dependencies" $PyPACKAGE_INSTALLED
    $PIP3 install -U -r requirements-setuptools.txt
    $PIP3 install -U -r requirements.txt
else
    echo "python package Jinja2 installed, assuming all other packages are installed too"
    echo "if not run on the commandline: $PIP3 install -U -r requirements.txt"
fi 

`$PYTHON_EXE -c "import sys, pkgutil; sys.exit(0 if pkgutil.find_loader('deepdiff') else 1)"`
PyPACKAGE_INSTALLED=$?
if [ $PyPACKAGE_INSTALLED -eq 1 ];then 
    echo "== installing python dependencies" $PyPACKAGE_INSTALLED
    $PIP3 install -U -r requirements-setuptools.txt
    $PIP3 install -U -r requirements.txt
else
    echo "python package deepdiff installed, assuming all other packages are installed too"
    echo "if not run on the commandline: $PIP3 install -U -r requirements.txt"
fi 

if [ ! -f $MODELS_DIR/README.md ]
then
echo "== installing oneIOTa models"
ORGDIR=`pwd`
cd ..
git clone https://github.com/openconnectivityfoundation/IoTDataModels.git --branch master
cd $ORGDIR
fi

if [ ! -f $CORE_DIR/README.md ]
then
echo "== installing core models"
ORGDIR=`pwd`
cd ..
git clone https://github.com/openconnectivityfoundation/core.git --branch master
cd $ORGDIR
fi

#if [ ! -f $MODELS_DIR/oic.wk.res.swagger.json ]
#then
echo "copying $CORE_DIR/swagger2.0/*.swagger.json $MODELS_DIR/*"
cp $CORE_DIR/swagger2.0/*.swagger.json $MODELS_DIR
#fi


if [ ! -f $SWAGGER2X ]
then
echo "== installing swagger2x"
ORGDIR=`pwd`
cd ..
git clone https://github.com/openconnectivityfoundation/swagger2x.git --branch master
cd $ORGDIR
fi

echo "creating $OUTPUTDIR"
mkdir -p $OUTPUTDIR
cp $INPUTFILE $OUTPUTDIR

mkdir -p $OUTPUTDIR/code

$PYTHON_EXE $DeviceBuilder -input $INPUTFILE -resource_dir $MODELS_DIR -out $OUTPUTDIR/out -title $TITLE
WB_INSTALLED=`which wb-swagger`
if stringContain "not found" $WB_INSTALLED;then 
    echo "== wb-swagger not installed, see https://github.com/WAvdBeek/wb-swagger-tools to install"
else
    echo "wb-swagger installed: verifying generated swagger"
    wb-swagger validate $OUTPUTDIR/out_introspection_merged.swagger.json
fi 
$PYTHON_EXE $SWAG2CBOR -file $OUTPUTDIR/out_introspection_merged.swagger.json
cp $OUTPUTDIR/out_introspection_merged.swagger.json.cbor $OUTPUTDIR/code/server_introspection.dat
# the introspection generation as include file
$PYTHON_EXE $CBOR2INC -file $OUTPUTDIR/code/server_introspection.dat

$PYTHON_EXE $SWAGGER2X -template_dir $SWAGGER2XDIR/src/templates -template IOTivity-lite -swagger $OUTPUTDIR/out_codegeneration_merged.swagger.json -out_dir $OUTPUTDIR/code  -devicetype $DEVICETYPE

