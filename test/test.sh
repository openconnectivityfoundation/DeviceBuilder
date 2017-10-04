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

resfile=./input_oic_res/oic-res-response-binaryswitch.json
python3 ../src/DeviceBuilder.py -ocfres $resfile -resource_dir ../../IoTDataModels -out ./out/test1
wb-swagger validate ./out/test1_codegeneration_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test1_codegeneration_merged.swagger.json
wb-swagger validate ./out/test1_introspection_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test1_introspection_merged.swagger.json

resfile=./input_oic_res/oic-res-response-binaryswitch-href.json
python3 ../src/DeviceBuilder.py -ocfres $resfile -resource_dir ../../IoTDataModels -out ./out/test2
wb-swagger validate ./out/test2_codegeneration_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test2_codegeneration_merged.swagger.json
wb-swagger validate ./out/test2_introspection_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test2_introspection_merged.swagger.json

resfile=./input_oic_res/oic-res-response-binaryswitch-brightness.json
python3 ../src/DeviceBuilder.py -ocfres $resfile -resource_dir ../../IoTDataModels -out ./out/test3 -remove_property step range precision
#test3_codegeneration_BinarySwitchResURI.swagger
#test3_codegeneration_BrightnessResURI.swagger
wb-swagger validate ./out/test3_codegeneration_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test3_codegeneration_BrightnessResURI.swagger.json
wb-swagger validate ./out/test3_codegeneration_merged.swagger.json
wb-swagger validate ./out/test3_introspection_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test3_introspection_BrightnessResURI.swagger.json
wb-swagger validate ./out/test3_introspection_merged.swagger.json


resfile=./input_oic_res/oic-res-response-binaryswitch-brightness.json
python3 ../src/DeviceBuilder.py -ocfres $resfile -resource_dir ../../IoTDataModels -out ./out/test4 -type int
wb-swagger validate ./out/test4_codegeneration_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test4_codegeneration_BrightnessResURI.swagger.json
wb-swagger validate ./out/test4_codegeneration_merged.swagger.json
wb-swagger validate ./out/test4_introspection_BinarySwitchResURI.swagger.json
wb-swagger validate ./out/test4_introspection_BrightnessResURI.swagger.json
wb-swagger validate ./out/test4_introspection_merged.swagger.json

resfile=./input_oic_res/oic-res-response-testdevice.json
python3 ../src/DeviceBuilder.py -ocfres $resfile -resource_dir ../../IoTDataModels -out ./out/test5 -type integer
wb-swagger validate ./out/test5_codegeneration_merged.swagger.json
wb-swagger validate ./out/test5_introspection_merged.swagger.json

