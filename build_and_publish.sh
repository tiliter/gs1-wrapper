set -ex

rm -rf dist
python -m build
python -m twine upload --repository testpypi --verbose dist/* --username stolmen
