# script to run the test with coverage
# to run do:
# sh do_coverage
# in the src directory

# python installation requires:
# python3 -m pip install pydoc
# python3 -m pip install pytest
# python3 -m pip install pytest-cov
# 

python3 -m pydoc -w DeviceBuilder
mkdir -p ../docs
mv DeviceBuilder.html ../docs


coverage run --source . -m py.test
coverage report
coverage html -d ../docs


