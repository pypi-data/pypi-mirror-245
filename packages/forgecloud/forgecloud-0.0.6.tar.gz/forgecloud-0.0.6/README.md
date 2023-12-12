# forgecloud

pip install twine

(delete old dist folder before creating new one, else twine upload will fail)

Create wheel and dist:
python setup.py sdist bdist_wheel

upload with twine
twine upload dist/*

Set your username to __token__
Set your password to the token value:

API TOKEN