#!/bin/bash

PYTHON_EXE=C:\\python35-32\\python3.exe
DeviceBuilder=../src/deviceBuilder.py

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
    compare_file $OUTPUT_DIR/$TEST_CASE/out_introspection_merged.swagger.json $REF_DIR/$TEST_CASE/out_introspection_merged.swagger.json
    compare_file $OUTPUT_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json $REF_DIR/$TEST_CASE/out_codegeneration_merged.swagger.json
    
} 


TEST_CASE="testcase_1"

function tests {

# option -h
TEST_CASE="testcase_1"
my_test -h

# default docx 
TEST_CASE="lightdevice"

resfile=./input_define_device/input-lightdevice.json

my_test_in_dir -input $resfile -resource_dir ../../IoTDataModels -out $OUTPUT_DIR/$TEST_CASE/out

}

tests  
