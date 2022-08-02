set -ex

python -m pip install -r requirements.txt
rm -rf dist
# python -m build  # build both
poetry install 
poetry run build-c-lib
poetry build --format sdist   # build sdist only
poetry publish --username stolmen
