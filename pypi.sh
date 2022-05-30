rm -rf build dist swaggerjmx.egg-info
pip install wheel
python setup.py sdist bdist_wheel
git config --global user.name "Lijiawei"
git config --global user.email "1456470136@qq.com"

git config user.name
git config user.email