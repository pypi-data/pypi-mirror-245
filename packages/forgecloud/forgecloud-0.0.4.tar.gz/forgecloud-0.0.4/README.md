# forgecloud

pip install twine

(delete old dist folder before creating new one, else twine upload will fail)

Create wheel and dist:
python setup.py sdist bdist_wheel

upload with twine
twine upload dist/*

Set your username to __token__
Set your password to the token value:

pypi-AgEIcHlwaS5vcmcCJDVlY2MyYjU5LTczYzQtNDYwMS1hNmZmLThiMzIxNWNjYThlOQACKlszLCJlZjQ4MGEwZS1mZWIyLTRjOWQtODAwMS1iMTVmZWNkNjliNzQiXQAABiClQ-4FIdz0Xle7AylatZ_BhbnoBMwGIvysCAmg_7sBzQ