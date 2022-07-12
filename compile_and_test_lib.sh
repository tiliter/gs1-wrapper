set -ex

# build the barcode engine, copy files into build-artifacts folder.

rm -rf build_artifacts/*.*
rm -rf gs1-barcode-engine

git clone https://github.com/gs1/gs1-barcode-engine.git  
cd gs1-barcode-engine/src/c-lib
git checkout 2021-09-10
make test
make
cp build/*.* ../../../build_artifacts

cd ../../..
rm -rf gs1-barcode-engine
