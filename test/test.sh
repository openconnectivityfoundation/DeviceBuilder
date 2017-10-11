#!/bin/bash

PYTHON_EXE=C:\\python35-32\\python3.exe
DeviceBuilder=../src/deviceBuilder.py
SWAG2CBOR=../src/swag2cbor.py
DIFF=../src/compareJson.py

#MODELS_DIR=./input_swagger
MODELS_DIR=../../IoTDataModels
OUTPUT_DIR=./out
OUTPUT_DIR_DOCS=../test/$OUTPUT_DIR
REF_DIR=./ref
EXT=.txt

function compare_output {
    diff -w $OUTPUT_DIR/$TEST_CASE$EXT $REF_DIR/$TEST_CASE$EXT
    echo "testcase difference: $TEST_CASE $?"
    #echo "blah"
}

function compare_to_reference_file {
    diff -w $OUTPUT_DIR/$1 $REF_DIR/$1
    echo "output $1 difference: $TEST_CASE $?"
    #echo "blah"
}


function compare_to_reference_file_in_dir {
    diff -w $OUTPUT_DIR/$1 $REF_DIR/$2/$1
    echo "output $1 difference: $TEST_CASE $?"
    #echo "blah"
}

function compare_file {
    echo "comparing ($TEST_CASE): " $1 $2
    diff -wb $1 $2
    #echo "blah"
}

function compare_json {
    echo "comparing json ($TEST_CASE): " $1 $2
    $PYTHON_EXE $DIFF -file1 $1 -file2 $2
}


function my_test {
    $PYTHON_EXE $DeviceBuilder $* > $OUTPUT_DIR/$TEST_CASE$EXT 2>&1
    compare_output
} 

function my_test_in_dir {
    mkdir -p $OUTPUT_DIR/$TEST_CASE
    $PYTHON_EXE $DeviceBuilder $* > $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    compare_file $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT $REF_DIR/$TEST_CASE/$TEST_CASE$EXT
    
    wb-swagger validate $OUTPUT_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json    
    wb-swagger validate $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json
    $PYTHON_EXE $SWAG2CBOR -file $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json  #> $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    $PYTHON_EXE $SWAG2CBOR -cbor $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json.cbor #> $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    compare_file $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json.cbor.json
    
    compare_json $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json $REF_DIR/$TEST_CASE/out_introspection_merged.swagger.json
    compare_json $OUTPUT_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json $REF_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json
    #compare_file $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json $REF_DIR/$TEST_CASE/out_introspection_merged.swagger.json
    #compare_file $OUTPUT_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json $REF_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json
    
} 

function my_test_in_dir_with_compare {
    mkdir -p $OUTPUT_DIR/$TEST_CASE
    $PYTHON_EXE $DeviceBuilder $* > $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    compare_file $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT $REF_DIR/$TEST_CASE/$TEST_CASE$EXT
    
    wb-swagger validate $OUTPUT_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json    
    wb-swagger validate $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json
    
    $PYTHON_EXE $SWAG2CBOR -file $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json  #> $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    $PYTHON_EXE $SWAG2CBOR -cbor $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json.cbor #> $OUTPUT_DIR/$TEST_CASE/$TEST_CASE$EXT 2>&1
    compare_file $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json.cbor.json
 
    compare_file $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json $REF_DIR/$TEST_CASE/out_introspection_merged.swagger.json
    compare_file $OUTPUT_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json $REF_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json
    
} 



TEST_CASE="testcase_1"

function generic_tests {

# option -h
TEST_CASE="testcase_1"
my_test -h

}


function oic_res_tests {

TEST_CASE="oic_res_1"
resfile=./input_oic_res/oic-res-response-binaryswitch.json
my_test_in_dir -ocfres $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out

TEST_CASE="oic_res_2"
resfile=./input_oic_res/oic-res-response-binaryswitch-href.json
my_test_in_dir -ocfres $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out


TEST_CASE="oic_res_3"
resfile=./input_oic_res/oic-res-response-binaryswitch-brightness.json
my_test_in_dir -ocfres $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out -remove_property step range precision

TEST_CASE="oic_res_4"
resfile=./input_oic_res/oic-res-response-binaryswitch-brightness.json
my_test_in_dir -ocfres $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out -type int

TEST_CASE="oic_res_5"
resfile=./input_oic_res/oic-res-response-binaryswitch-brightness.json
my_test_in_dir -ocfres $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out -type int

TEST_CASE="oic_res_6"
resfile=./input_oic_res/oic-res-response-testdevice.json
my_test_in_dir -ocfres $resfile -resource_dir ../../IoTDataModels -out $OUTPUT_DIR/$TEST_CASE/out -type integer

}


function deviceBuilder_tests {

# option -h
TEST_CASE="testcase_1"
my_test -h


TEST_CASE="lightdevice"
resfile=./input_define_device/input-lightdevice.json
my_test_in_dir -input $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out


TEST_CASE="switch"
resfile=./input_define_device/input-switch.json
my_test_in_dir_with_compare -input $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out


TEST_CASE="thermostat"
resfile=./input_define_device/input-thermostat.json
my_test_in_dir -input $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out


TEST_CASE="coffeemachine"
resfile=./input_define_device/input-coffeemachine.json
my_test_in_dir -input $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out
}

function deviceBuilder_tests2 {

TEST_CASE="cooktop"
resfile=./input_define_device/input-cooktop.json
my_test_in_dir -input $resfile -resource_dir $MODELS_DIR -out $OUTPUT_DIR/$TEST_CASE/out

}

if [ ! -f ../../IoTDataModels/README.md ]
then
pushd `pwd`
cd ../..
git clone https://github.com/OpenInterConnect/IoTDataModels.git --branch master
popd
fi


generic_tests
oic_res_tests
deviceBuilder_tests 
deviceBuilder_tests2  
