#
#
#
resfile=../input/oic-res-response-binaryswitch.json
resfile=../input/oic-res-response-binaryswitch-href.json
resfile=../input/oic-res-response-binaryswitch-brightness.json
resfile=../input/binaryswitch-brightness-minimal.json

resfile=../input/oic-res-response-testdevice.json


if [ ! -f ../../IoTDataModels/README.md ]
then
pushd `pwd`
cd ../..
git clone https://github.com/OpenInterConnect/IoTDataModels.git --branch master
popd
fi

#python3 DeviceBuilder.py -ocfres $resfile -resource_dir ../../IoTDataModels -out ../test/out.swagger.json
#python3 DeviceBuilder.py -ocfres $resfile -resource_dir ../examples -out ../test/out.swagger.json
#python3 DeviceBuilder.py -ocfres $resfile -resource_dir ../examples -out ../test/out.swagger2.json -remove_property step range precision
#python3 DeviceBuilder.py -ocfres $resfile -resource_dir ../examples -out ../test/out.swagger2.json -type int

python3 ../src/DeviceBuilder.py -ocfres $resfile -resource_dir ../../../IoTDataModels -out ../test/out -type integer