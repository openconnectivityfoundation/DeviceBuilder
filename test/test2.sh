#
#
#

if [ ! -f ../../IoTDataModels/README.md ]
then
pushd `pwd`
cd ../..
git clone https://github.com/OpenInterConnect/IoTDataModels.git --branch master
popd
fi

mkdir out

#resfile=./input_define_device/input-testdevice.json
#python3 ../src/DeviceBuilder.py -input $resfile -resource_dir ../../IoTDataModels -out ./out/test_input1
#wb-swagger validate ./out/test_input1_codegeneration_merged.swagger.json
#wb-swagger validate ./out/test_input1_introspection_merged.swagger.json

resfile=./input_define_device/input-testdevice-2.json
python3 ../src/DeviceBuilder.py -input $resfile -resource_dir ../../IoTDataModels -out ./out/test_input2
wb-swagger validate ./out/test_input2_codegeneration_merged.swagger.json
wb-swagger validate ./out/test_input2_introspection_merged.swagger.json

